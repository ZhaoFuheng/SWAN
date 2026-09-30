"""The SWAN 2.0 query language: prompt-form linting, the BlendSQL translation, the LOTUS interpreter, and the
shadow model's reading of each system's prompts."""

import json
import sqlite3

import pytest

from swan_bench.aisql import ai_calls, lint, parse
from swan_bench.lotus_exec import LotusExecutor
from swan_bench.shadow import ShadowModel, classify_answer, complete_answer, filter_answer
from swan_bench.translate_blendsql import to_blendsql

FILTER = "ai_filter('Is the hero male? superhero_name: ' || T1.superhero_name)"


def test_prompt_form():
    assert lint(f"SELECT count(*) FROM superhero AS T1 WHERE {FILTER}") == []
    assert "context column's name" in lint("SELECT 1 FROM t WHERE ai_filter('Male? name: ' || t.other)")[0]
    assert "one column" in lint("SELECT 1 FROM t WHERE ai_filter('Male? k: ' || upper(t.k))")[0]
    assert "suffix" in lint("SELECT ai_complete('Q k: ' || t.k || ' please') FROM t")[0]
    assert "not part of" in lint("SELECT ai_score('Q k: ' || t.k, 'r', 1, 5) FROM t")[0]
    assert "no AI call" in lint("SELECT 1")[0]
    assert "DOUBLE" in lint("SELECT CAST(ai_complete('Q k: ' || t.k) AS REAL) FROM t")[0]
    calls = ai_calls(parse("SELECT ai_classify('Which? k: ' || t.k, ['A', 'B']), "
                           "(SELECT ai_agg(list(u.n), 'Oldest?') FROM u) FROM t"))
    assert [(c.fn, c.question, c.name, c.labels, c.instruction) for c in calls] == [
        ("ai_classify", "Which?", "k", ["A", "B"], ""), ("ai_agg", "", "n", None, "Oldest?")]


def test_blendsql_translation():
    b = to_blendsql(f"SELECT count(*) FROM superhero AS T1 WHERE T1.id // 2 = 1 AND {FILTER} LIMIT 5")
    assert "{{LLMMap('Is the hero male?', T1.superhero_name)}} = TRUE" in b and "({{" not in b
    assert "CAST(CAST(T1.id AS REAL) / 2 AS INTEGER)" in b  # DuckDB // -> sqlite
    b = to_blendsql("SELECT TRY_CAST(ai_complete('Height? k: ' || t.k || ' Answer with the number only.') AS DOUBLE) FROM t")
    assert "{{LLMMap('Height? Answer with the number only.', t.k, return_type='str')}}" in b
    b = to_blendsql("SELECT ai_classify('Which? k: ' || t.k, (SELECT list(DISTINCT c ORDER BY c) FROM u)) FROM t")
    assert "options=u.c" in b
    b = to_blendsql("SELECT (SELECT ai_agg(list(u.n), 'It''s oldest?') FROM u WHERE u.x > 1) AS a")
    assert "{{LLMQA('It''s oldest?', (SELECT u.n FROM u WHERE u.x > 1))}}" in b


class FakeOps:
    """Deterministic stand-in for LOTUS: records how many rows each call saw."""

    def __init__(self):
        self.seen = []

    def filter(self, call, values):
        self.seen.append((call.question, len(values)))
        return [filter_answer(call.question, v) for v in values]

    def complete(self, call, values):
        self.seen.append((call.question, len(values)))
        return [complete_answer(call.question, call.suffix, v) for v in values]

    def classify(self, call, values, labels):
        self.seen.append((call.question, len(values)))
        return [classify_answer(call.question, v, labels) for v in values]

    def agg(self, call, values):
        return f"n={len(values)}"


@pytest.fixture
def db(tmp_path):
    path = tmp_path / "t.sqlite"
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE hero (id INTEGER, name TEXT, team INTEGER)")
    con.execute("CREATE TABLE team (id INTEGER, label TEXT)")
    con.executemany("INSERT INTO hero VALUES (?, ?, ?)", [(i, f"h{i % 7}", i % 3) for i in range(40)])
    con.executemany("INSERT INTO team VALUES (?, ?)", [(0, "a"), (1, "b"), (2, "c")])
    con.commit()
    con.close()
    return path


def test_lotus_follows_the_written_order(db):
    ops = FakeOps()
    ex = LotusExecutor(db, ops)
    # the cheap filter is written after the AI filter, so the AI sees all 40 rows; LOTUS never deduplicates
    ex.run("SELECT count(*) FROM hero AS h WHERE ai_filter('Q1? name: ' || h.name) AND h.id < 10")
    assert ops.seen == [("Q1?", 40)]
    ops.seen.clear()
    ex.run("SELECT count(*) FROM hero AS h WHERE h.id < 10 AND ai_filter('Q1? name: ' || h.name)")
    assert ops.seen == [("Q1?", 10)]
    ops.seen.clear()
    # SELECT-list AI runs on every row that passed WHERE, before ORDER BY / LIMIT
    rows = ex.run("SELECT h.id, ai_complete('City? name: ' || h.name) AS c FROM hero AS h JOIN team AS t "
                  "ON h.team = t.id WHERE t.label = 'a' ORDER BY h.id LIMIT 2")
    assert ops.seen == [("City?", 14)] and len(rows) == 2
    ex.close()


def test_lotus_matches_expected_semantics(db):
    ex = LotusExecutor(db, FakeOps())
    got = ex.run("WITH k AS (SELECT h.id, h.name FROM hero AS h WHERE h.team = 1) "
                 "SELECT count(*) FROM k WHERE ai_filter('Q2? name: ' || k.name) OR k.id = 1")
    want = sum(1 for i in range(40) if i % 3 == 1 and (filter_answer("Q2?", f"h{i % 7}") or i == 1))
    assert got.iloc[0, 0] == want
    agg = ex.run("SELECT (SELECT ai_agg(list(h.name), 'Oldest?') FROM hero AS h WHERE h.id < 5) AS a")
    assert agg.iloc[0, 0] == "n=5"
    ex.close()


def test_shadow_reads_every_system_the_same_way():
    shadow = ShadowModel(["Is the hero male? superhero_name: "])
    want = filter_answer("Is the hero male?", "3-D Man")
    swan = {"response_format": {"json_schema": {"schema": {"properties": {"result": {"type": "boolean"}}}}},
            "messages": [{"role": "system", "content": "x"},
                         {"role": "user", "content": "Is the hero male? superhero_name: 3-D Man"}]}
    assert json.loads(shadow.respond(swan))["result"] == want
    blend = {"messages": [{"role": "user", "content": "Output 'True' if the context satisfies ...\n\nQUESTION:\n"
             "Is this city in the California Bay Area?\n\nCONTEXT:\n{\"city\": \"San Jose\"}\n\nANSWER:\nTrue\n\n---\n\n"
             "QUESTION:\nIs the hero male?\n\nCONTEXT:\n{\"superhero_name\": \"3-D Man\"}\n\nANSWER:\n"}]}
    assert shadow.respond(blend) == ("True" if want else "False")
    lotus = {"messages": [{"role": "system", "content": "claim"},
                          {"role": "user", "content": "Context:\n[Superhero_name]: «3-D Man»\n\n\n"
                                                      "Claim: Is the hero male? Superhero_name"}]}
    assert ("True" in shadow.respond(lotus)) == want


def test_lotus_output_columns_keep_their_names(db):
    ex = LotusExecutor(db, FakeOps())
    got = ex.run("WITH t AS (SELECT h.id, h.name FROM hero AS h WHERE ai_filter('Q3? name: ' || h.name)) "
                 "SELECT count(t.id) FROM t")
    want = sum(1 for i in range(40) if filter_answer("Q3?", f"h{i % 7}"))
    assert got.iloc[0, 0] == want
    star = ex.run("WITH t AS (SELECT * FROM hero AS h WHERE h.id < 3 AND ai_filter('Q3? name: ' || h.name)) "
                  "SELECT t.id FROM t ORDER BY t.id")
    assert list(star.iloc[:, 0]) == [i for i in range(3) if filter_answer("Q3?", f"h{i % 7}")]
    ex.close()


def test_negated_filter_becomes_false():
    b = to_blendsql(f"SELECT count(*) FROM superhero AS T1 WHERE T1.id < 9 AND NOT {FILTER}")
    assert "{{LLMMap('Is the hero male?', T1.superhero_name)}} = FALSE" in b and "NOT" not in b
