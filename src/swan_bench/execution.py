"""SQL execution and result matching, as in the 2024 notebooks.

A predicted result matches the gold result when both have the same number of rows and, row by row, the same
multiset of values: rows are compared in order when the query has an ORDER BY, as sets otherwise. The values
inside a row are compared independently of column order.

Floats are compared to 10 significant digits. The gold query runs in sqlite and a system may compute the
same number in another engine (DuckDB, pandas), where summation order changes the last bits.
"""

import math
import multiprocessing as mp
import sqlite3
from decimal import Decimal
from pathlib import Path


def _canonical_value(value):
    if hasattr(value, "item"):  # numpy scalar
        value = value.item()
    if isinstance(value, Decimal):
        value = float(value)
    if isinstance(value, float):
        if math.isnan(value):
            return None
        return float(f"{value:.10g}")
    return value


def _canonical_row(row) -> tuple:
    return tuple(sorted((_canonical_value(v) for v in row), key=hash))


def results_match(predicted: list, gold: list, ordered: bool) -> bool:
    if len(predicted) != len(gold):
        return False
    if ordered:
        return all(_canonical_row(a) == _canonical_row(b) for a, b in zip(predicted, gold))
    return {_canonical_row(a) for a in predicted} == {_canonical_row(b) for b in gold}


def execute(db_path: Path | str, sql: str) -> list:
    con = sqlite3.connect(db_path)
    try:
        return con.execute(sql).fetchall()
    finally:
        con.close()


def _execute_into(db_path: str, sql: str, queue) -> None:
    try:
        queue.put(execute(db_path, sql))
    except Exception as ex:  # noqa: BLE001 -- the exception itself is the result
        queue.put(ex)


def execute_with_timeout(db_path: Path | str, sql: str, timeout: float = 120.0):
    """Run `sql` in a child process; returns the rows or the exception raised (a TimeoutError on timeout)."""
    queue = mp.Queue()
    proc = mp.Process(target=_execute_into, args=(str(db_path), sql, queue))
    proc.start()
    try:
        result = queue.get(True, timeout + 5)
    except Exception:  # noqa: BLE001 -- queue.Empty
        result = TimeoutError("SQL query took too much time to execute.")
    proc.join(timeout)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return TimeoutError("SQL query took too much time to execute.")
    return result

