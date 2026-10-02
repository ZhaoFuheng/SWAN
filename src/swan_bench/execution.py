"""SQL execution and result matching, as in the 2024 notebooks.

A predicted result matches the gold result when both have the same number of rows and, row by row, the same
multiset of values: rows are compared in order when the query has an ORDER BY, as sets otherwise. The values
inside a row are compared independently of column order.

Floats are compared to 10 significant digits. The gold query runs in sqlite and a system may compute the
same number in another engine (DuckDB, pandas), where summation order changes the last bits. URLs are
compared without their scheme, `www.`, percent-encoding and trailing slash, which a model cannot know.
"""

import math
import re
import sqlite3
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote


_URL = re.compile(r"^(?:https?://)?(?:www\.)?", re.I)


def _canonical_url(text: str) -> str:
    """A URL without the parts a model cannot know: scheme, `www.`, percent-encoding, trailing slash, case
    of the host (`http://en.wikipedia.org/wiki/Mika_H%C3%A4kkinen` == `https://en.wikipedia.org/wiki/Mika_Häkkinen`)."""
    rest = _URL.sub("", unquote(text.strip())).rstrip("/")
    host, sep, path = rest.partition("/")
    return host.lower() + sep + path


def _canonical_value(value):
    if hasattr(value, "item"):  # numpy scalar
        value = value.item()
    if isinstance(value, Decimal):
        value = float(value)
    if isinstance(value, str) and _URL.match(value) and _URL.match(value).end() > 0:
        return _canonical_url(value)
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

