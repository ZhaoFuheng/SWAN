"""Every SWAN 2.0 question's oracle query (its AISQL query with the true values in place of the AI calls)
returns the gold answer on the original database: the AISQL query is right whenever the model is right."""

import pytest

from swan_bench import paths
from swan_bench.aisql import parse
from swan_bench.data import load_query, load_questions, query_path
from swan_bench.execution import execute
from swan_bench.quality import exact_match

QUESTIONS = [q for q in load_questions() if query_path("oracle", q.qid).is_file()]


@pytest.mark.parametrize("question", QUESTIONS, ids=lambda q: q.qid)
def test_oracle_matches_gold(question):
    db = paths.database_path(question.db)
    if not db.is_file():
        pytest.skip("run `swan-bench prepare` first")
    gold = execute(db, question.gold_sql)
    assert gold, "the gold answer is empty"
    oracle = execute(db, parse(load_query("oracle", question.qid)).sql("sqlite"))
    assert exact_match(oracle, gold, question.gold_sql, load_query("aisql", question.qid)), (oracle[:5], gold[:5])
