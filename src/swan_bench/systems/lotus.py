"""LOTUS: semantic operators on pandas DataFrames.

SWAN 2.0 runs every system on the question's AISQL query; for LOTUS it is executed as the LOTUS program
derived from it mechanically (`lotus_exec.py`). The helpers below (`MaskedDatabase`, `rows_of`) are shared.

Every LLM call goes through LOTUS's operators (`sem_filter`, `sem_map`, `sem_agg`). LOTUS's in-process cache stays off: the benchmark rule is that one query's answers never
serve another; cross-run reuse is the cache proxy's job, which still reports the recorded cost and latency.

Needs the extra: `uv sync --extra lotus`. Prompt rendering depends on set order, so the runner pins
PYTHONHASHSEED=0 to keep the prompts, and so the proxy's cache keys, stable across runs.
"""

import math
import sqlite3

from .. import paths


def _quote(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _python(value):
    if hasattr(value, "item"):  # numpy scalar
        value = value.item()
    if isinstance(value, float) and math.isnan(value):
        return None
    try:
        import pandas as pd
        if value is pd.NA or value is pd.NaT:
            return None
    except ImportError:
        pass
    return value


def rows_of(result) -> list[tuple]:
    if hasattr(result, "itertuples"):
        return [tuple(_python(v) for v in r) for r in result.itertuples(index=False, name=None)]
    if hasattr(result, "tolist"):  # a Series
        return [(_python(v),) for v in result.tolist()]
    if isinstance(result, (list, tuple)):
        return [tuple(_python(v) for v in (r if isinstance(r, (list, tuple)) else (r,))) for r in result]
    return [(_python(result),)]


class MaskedDatabase:
    def __init__(self, db: str):
        self.path = paths.require_database(db, masked=True)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)

    def table(self, name: str):
        import pandas as pd
        with self._connect() as con:
            return pd.read_sql_query(f"SELECT * FROM {_quote(name)}", con)

    def sql(self, query: str, **frames):
        import pandas as pd
        con = self._connect()
        try:
            for name, df in frames.items():
                cols = [str(c) for c in df.columns]
                con.execute(f"CREATE TEMP TABLE {_quote(name)} ({', '.join(_quote(c) for c in cols)})")
                con.executemany(f"INSERT INTO temp.{_quote(name)} VALUES ({', '.join('?' * len(cols))})",
                                [tuple(_python(v) for v in r) for r in df.itertuples(index=False, name=None)])
            return pd.read_sql_query(query, con)
        finally:
            con.close()


class LotusSystem:
    """Runs the question's AISQL query as the LOTUS program derived from it (`lotus_exec.py`)."""

    name = "lotus"

    def __init__(self, model: str, endpoint: str | None, concurrency: int = 20, api_key: str | None = None, **_):
        try:
            import lotus
            from lotus.models import LM
        except ImportError as ex:
            raise SystemExit("LOTUS is not installed: run `uv sync --extra lotus`") from ex
        lotus.settings.configure(enable_cache=False)
        # litellm needs the provider; the request body still carries the bare model name
        lm_model = model if "/" in model else f"openai/{model}"
        kwargs = {"api_base": endpoint.rstrip("/") + "/v1"} if endpoint else {}
        self.lm = LM(model=lm_model, api_key=api_key or "unused", max_batch_size=concurrency, **kwargs)
        lotus.settings.configure(lm=self.lm)

    def execute(self, question, query: str) -> list[tuple]:
        from ..lotus_exec import LotusExecutor

        executor = LotusExecutor(paths.require_database(question.db, masked=True))
        try:
            return rows_of(executor.run(query))
        finally:
            executor.close()
