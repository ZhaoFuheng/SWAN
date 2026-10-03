"""The PLOP translation keeps every prompt and maps the three AI functions onto PLOP's dialect."""

import pytest

from swan_bench.data import load_query, load_questions
from swan_bench.translate_plop import to_plop


def test_filter_complete_and_classify_map_onto_plop_functions():
    q = ("SELECT t.name FROM t WHERE ai_filter('Context:\\n[name]: «' || t.name || '»\\n\\n\\nClaim: Is it big? name')"
         " AND ai_classify('Which colour? name: ' || t.name, ['red', 'blue']) = 'red'")
    out = to_plop(q).lower()  # sqlglot upper-cases function names; DuckDB does not care
    assert "semantic('context:" in out and "ai_filter" not in out
    assert "semantic_string('which colour? name: ' || t.name || ' answer with exactly one of the following labels, verbatim: ' || array_to_string(" in out
    assert "'red', 'blue'" in out and "ai_classify" not in out


def test_classify_with_a_label_subquery_keeps_the_subquery():
    out = to_plop("SELECT ai_classify('Colour? name: ' || t.name, (SELECT list(DISTINCT c ORDER BY c) FROM u)) FROM t").lower()
    assert "array_to_string((select" in out and "from u" in out


@pytest.mark.parametrize("question", [q for db in ("california_schools", "superhero", "formula_1", "european_football_2")
                                      for q in load_questions(db)], ids=lambda q: q.qid)
def test_every_query_translates(question):
    out = to_plop(load_query("aisql", question.qid).strip().rstrip(";")).lower()
    assert "ai_filter" not in out and "ai_complete" not in out and "ai_classify" not in out
    assert "semantic" in out
