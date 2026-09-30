"""BlendSQL (0.1.x): runs the question's AISQL query, translated mechanically (`translate_blendsql.py`).

Needs the extra: `uv sync --extra blendsql`.
"""

import os

from .. import paths


class BlendSQLSystem:
    name = "blendsql"

    def __init__(self, model: str, endpoint: str | None, shots: int = 0, api_key: str | None = None,
                 concurrency: int = 20, **_):
        # BlendSQL's in-flight request limit (its default is 32); the same 20 as the other systems
        os.environ["BLENDSQL_ASYNC_LIMIT"] = str(concurrency)
        try:
            from blendsql import BlendSQL
            from blendsql.ingredients import LLMJoin, LLMMap, LLMQA
            from blendsql.models import OpenAI
        except ImportError as ex:
            raise SystemExit("BlendSQL is not installed: run `uv sync --extra blendsql`") from ex
        from .blendsql_fewshot import LLMQA_EXAMPLES

        base_url = endpoint.rstrip("/") + "/v1" if endpoint else None
        self._engine = BlendSQL
        self.llm = OpenAI(model, api_key=api_key or "unused", base_url=base_url)
        llmqa = LLMQA.from_args(few_shot_examples=LLMQA_EXAMPLES, num_few_shot_examples=shots) if shots else LLMQA
        self.ingredients = {LLMMap, llmqa, LLMJoin}

    def execute(self, question, query: str) -> list[tuple]:
        # a fresh engine per query: an engine keeps the temporary tables of the queries it ran, and a later
        # query with a CTE of the same name would read them
        masked = str(paths.require_database(question.db, masked=True))
        from ..translate_blendsql import to_blendsql

        smoothie = self._engine(masked, model=self.llm, ingredients=self.ingredients).execute(to_blendsql(query))
        return [tuple(r) for r in smoothie.pl().iter_rows()]
