"""Loaders for the benchmark's questions, the systems' queries, and the masking metadata."""

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from . import paths

#: The query kinds under `queries/<kind>/<qid>.sql`: the AISQL query every system runs, and its oracle.
QUERY_KINDS = ("aisql", "oracle")


@dataclass(frozen=True)
class Question:
    qid: str
    db: str
    question: str
    evidence: str
    difficulty: str
    gold_sql: str
    """Answers the question on the original database."""
    shape: str = ""
    """The SWAN 2.0 query shape (docs/SWAN2_AUTHORING.md), e.g. `multi_filter`."""


def load_questions(db: str | None = None) -> list[Question]:
    questions = []
    for name in ([db] if db else paths.DATABASES):
        with open(paths.QUESTIONS_DIR / f"{name}.csv", newline="") as f:
            questions += [Question(**row) for row in csv.DictReader(f)]
    return questions


def query_path(kind: str, qid: str) -> Path:
    return paths.QUERIES / kind / f"{qid}.sql"


def load_query(kind: str, qid: str) -> str:
    """Question `qid`'s AISQL query (`kind="aisql"`, run by every system) or its oracle query."""
    return query_path(kind, qid).read_text()


def load_masked_columns() -> dict[str, dict[str, list[str]]]:
    """database -> table -> columns hidden from the system under test."""
    return json.load(open(paths.MASKED_COLUMNS_JSON))


def load_table_keys() -> dict[str, dict[str, list[str]]]:
    """database -> table -> columns that identify a row to the LLM."""
    return json.load(open(paths.TABLE_KEYS_JSON))
