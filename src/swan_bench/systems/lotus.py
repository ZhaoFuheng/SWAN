"""LOTUS: semantic operators on pandas DataFrames. Runs the question's AISQL query as the LOTUS program
derived from it mechanically (`lotus_exec.py`).

Every LLM call goes through LOTUS's operators (`sem_filter`, `sem_map`, `sem_agg`). LOTUS's in-process cache
stays off: the benchmark rule is that one query's answers never serve another; cross-run reuse is the cache
proxy's job, which still reports the recorded cost and latency.

Needs the extra: `uv sync --extra lotus`. Prompt rendering depends on set order, so the runner pins
PYTHONHASHSEED=0 to keep the prompts, and so the proxy's cache keys, stable across runs.
"""

from .. import paths


class LotusSystem:
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
        from ..lotus_exec import LotusExecutor, rows_of

        executor = LotusExecutor(paths.require_database(question.db, masked=True))
        try:
            return rows_of(executor.run(query))
        finally:
            executor.close()
