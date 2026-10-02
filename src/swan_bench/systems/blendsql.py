"""BlendSQL (0.1.x): runs the question's AISQL query, translated mechanically (`translate_blendsql.py`).

BlendSQL's LLMMap prompt carries a built-in one-shot example ("Is this city in the California Bay Area?
... True"). The benchmark is zero-shot for every system, so the model wrapper removes that block from each
prompt before it is sent; the instruction and the question/context layout are BlendSQL's own.

Needs the extra: `uv sync --extra blendsql`.
"""

import os
import re

from .. import paths

# the one-shot block of BlendSQL's "basic" LLMMap prompt: the sentence announcing it, the example, the rule
_ONE_SHOT = re.compile(r" An example is shown below\.\n\n.*?\n---\n\n", re.DOTALL)


def _zero_shot(prompt: str) -> str:
    return _ONE_SHOT.sub("\n\n", prompt, count=1)


class BlendSQLSystem:
    name = "blendsql"

    def __init__(self, model: str, endpoint: str | None, api_key: str | None = None, concurrency: int = 20, **_):
        # BlendSQL's in-flight request limit (its default is 32); the same 20 as the other systems
        os.environ["BLENDSQL_ASYNC_LIMIT"] = str(concurrency)
        try:
            from blendsql import BlendSQL
            from blendsql.ingredients import LLMJoin, LLMMap, LLMQA
            from blendsql.models import OpenAI
        except ImportError as ex:
            raise SystemExit("BlendSQL is not installed: run `uv sync --extra blendsql`") from ex
        base_url = endpoint.rstrip("/") + "/v1" if endpoint else None

        class ZeroShotOpenAI(OpenAI):
            async def _format_inputs(self, extra_body, item):
                item.prompt = _zero_shot(item.prompt)
                return await super()._format_inputs(extra_body, item)

        self._engine = BlendSQL
        self.llm = ZeroShotOpenAI(model, api_key=api_key or "unused", base_url=base_url)
        self.ingredients = {LLMMap, LLMQA, LLMJoin}

    def execute(self, question, query: str) -> list[tuple]:
        # a fresh engine per query: an engine keeps the temporary tables of the queries it ran, and a later
        # query with a CTE of the same name would read them
        masked = str(paths.require_database(question.db, masked=True))
        from ..translate_blendsql import to_blendsql

        smoothie = self._engine(masked, model=self.llm, ingredients=self.ingredients).execute(to_blendsql(query))
        return [tuple(r) for r in smoothie.pl().iter_rows()]
