"""A deterministic stand-in model that gives every system the same answer to the same question.

Each system wraps a question and a value in its own prompt. The shadow model recovers `(question, value)`
from any of the three systems' prompts and answers with a function of those two alone, in the format that
system expects. With the shadow model behind the meter, the three systems must return identical results
for every query, so a difference exposes a translation that changed the query's meaning.

| call | shadow answer |
|---|---|
| filter | true for about half of the (question, value) pairs |
| complete | a number, a date or a word, following the prompt's suffix |
| classify | one of the labels, by hash |
| agg | `n=<number of items>` |
"""

import ast
import hashlib
import json
import re

from .aisql import SUFFIXES

NUMBER, DATE, VALUE = SUFFIXES


def _h(*parts) -> int:
    return int(hashlib.md5("\x1f".join(str(p) for p in parts).encode()).hexdigest()[:12], 16)


def _value_text(v) -> str:
    if isinstance(v, float) and v.is_integer():
        return str(v)  # SQL renders 5.0 as '5.0', as Python does
    return str(v)


def _strip_suffix(text: str) -> tuple[str, str]:
    for s in SUFFIXES:
        if text.endswith(s):
            return text[: -len(s)], s
    return text, ""


def filter_answer(question: str, value) -> bool:
    return _h("filter", question.strip(), _value_text(value)) % 2 == 0


def complete_answer(question: str, suffix: str, value) -> str:
    h = _h("complete", question.strip(), _value_text(value))
    if suffix == NUMBER:
        return str(h % 100)
    if suffix == DATE:
        return f"{1950 + h % 50}-{1 + (h >> 8) % 12:02d}-{1 + (h >> 16) % 28:02d}"
    return f"v{h % 7}"


def classify_answer(question: str, value, labels: list[str]) -> str:
    labels = sorted(set(labels))
    return labels[_h("classify", question.strip(), _value_text(value)) % len(labels)] if labels else ""


def agg_answer(n_items: int) -> str:
    return f"n={n_items}"


class ShadowModel:
    def __init__(self, prefixes: list[str]):
        """`prefixes`: every `'<question> <name>: '` of the benchmark's AI calls (for SWAN-AISQL prompts)."""
        self.prefixes = sorted(set(prefixes), key=len, reverse=True)

    # SWAN-AISQL: structured output {"result": ...}
    def _swan(self, body: dict, user: str) -> str:
        schema = json.dumps((body.get("response_format") or {}).get("json_schema", {}))
        if user.startswith("Instruction: ") and "\n\nItems:\n" in user:
            items = [l for l in user.split("\n\nItems:\n", 1)[1].splitlines() if l.startswith("- ")]
            return json.dumps({"result": agg_answer(len(items))})
        if user.startswith("Categories: "):
            head, rest = user.split("\n\nInput:\n", 1)
            labels = [x.strip() for x in head[len("Categories: "):].split(", ")]
            text = rest.split("\n\nRespond with exactly one", 1)[0]
            question, value = self._split(text)
            return json.dumps({"result": classify_answer(question, value, labels)})
        text, suffix = _strip_suffix(user)
        question, value = self._split(text)
        if '"boolean"' in schema:
            return json.dumps({"result": filter_answer(question, value)})
        if '"enum"' in schema:
            labels = re.search(r'"enum":\s*(\[[^\]]*\])', schema)
            return json.dumps({"result": classify_answer(question, value, json.loads(labels.group(1)) if labels else [])})
        return json.dumps({"result": complete_answer(question, suffix, value)})

    def _split(self, text: str) -> tuple[str, str]:
        for p in self.prefixes:  # p = '<question> <name>: '
            if text.startswith(p):
                return p[: p[:-2].rfind(" ")], text[len(p):]
        return text, ""

    # BlendSQL: few-shot blocks, the last one is the real question
    def _blendsql(self, system_and_user: str) -> str:
        if "\nQuestion: " in "\n" + system_and_user and "Context:" in system_and_user and "QUESTION:" not in system_and_user:
            context = system_and_user.split("Context:", 1)[1].rsplit("Answer:", 1)[0].strip()
            try:
                table = json.loads(context)
                n = len(next(iter(table.values()))) if table else 0
            except ValueError:
                n = 0
            return agg_answer(n)
        block = system_and_user.rsplit("QUESTION:\n", 1)[1]
        question = block.split("\n\nCONTEXT:\n", 1)[0].strip()
        context = json.loads(block.split("\n\nCONTEXT:\n", 1)[1].split("\n\n", 1)[0])
        value = next(iter(context.values()))
        question, suffix = _strip_suffix(question)
        if "OPTIONS:\n" in block:
            labels = ast.literal_eval(block.split("OPTIONS:\n", 1)[1].split("\n", 1)[0])
            return classify_answer(question, value, labels)
        if "Output 'True'" in system_and_user:
            return "True" if filter_answer(question, value) else "False"
        return complete_answer(question, suffix, value)

    # LOTUS: "Context:\n[Name]: «value»" and "Claim: ..." / "Instruction: ..."
    def _lotus(self, system: str, user: str) -> str:
        if "Document 1:" in user or "multiple documents" in user:
            return agg_answer(len(re.findall(r"Document \d+:", user)))
        value = re.search(r"«(.*?)»", user, re.S).group(1)
        name = re.search(r"\[([^\]]+)\]: «", user).group(1)
        if "Claim: " in user:
            claim = user.split("Claim: ", 1)[1].strip()
            question = claim[: -len(name)].strip() if claim.endswith(name) else claim
            return "Answer: " + ("True" if filter_answer(question, value) else "False")
        instruction = user.split("Instruction: ", 1)[1].strip()
        m = re.search(r" Answer with exactly one of: (.*)\.$", instruction)
        if m:
            question = instruction[: m.start()].strip()
            question = question[: -len(name)].strip() if question.endswith(name) else question
            return classify_answer(question, value, [x.strip() for x in m.group(1).split(", ")])
        instruction, suffix = _strip_suffix(instruction)
        question = instruction[: -len(name)].strip() if instruction.endswith(name) else instruction
        return complete_answer(question, suffix, value)

    def respond(self, body: dict) -> str:
        messages = body.get("messages", [])
        system = "\n".join(str(m["content"]) for m in messages if m["role"] == "system")
        user = str(messages[-1]["content"]) if messages else ""
        if body.get("response_format"):
            return self._swan(body, user)
        if "QUESTION:" in user or ("Question: " in user and "Return type" in user):
            return self._blendsql(system + "\n" + user)
        if "«" in user:
            return self._lotus(system, user)
        # SWAN-AISQL's ai_complete: the bare prompt, a plain-text answer
        text, suffix = _strip_suffix(user)
        question, value = self._split(text)
        return complete_answer(question, suffix, value)
