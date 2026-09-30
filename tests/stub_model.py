"""A BlendSQL model that answers locally, so queries can be parsed and executed without an API key."""

import re

from blendsql.common.typing import GenerationResult
from blendsql.models import OpenAI


class StubModel(OpenAI):
    """Answers every prompt with its first listed option, or 't'. Records the prompts it was asked."""

    def __init__(self):
        super().__init__("stub-model", api_key="unused", base_url="http://127.0.0.1:9/v1")
        self.prompts: list[str] = []

    async def generate(self, item, cancel_event=None, max_retries=3):
        self.prompts.append(item.prompt)
        match = re.search(r"Options:\s*\n?\s*(.+)", item.prompt or "")
        answer = "t"
        if match:
            first = re.split(r"[,\n]", match.group(1))[0].strip().strip("'\"[]")
            answer = first or answer
        return GenerationResult(item.identifier, answer, completed=True)
