"""The shipped data files are complete and consistent with each other and with the databases."""

import sqlite3
from collections import Counter

import pytest

from swan_bench import paths
from swan_bench.aisql import lint
from swan_bench.data import load_masked_columns, load_query, load_questions, query_path


def test_questions():
    questions = load_questions()
    assert len(questions) == 120
    assert len({q.qid for q in questions}) == 120
    for db in paths.DATABASES:
        assert len(load_questions(db)) == 30
    for q in questions:
        assert q.question and q.gold_sql, q.qid
        assert q.difficulty in {"simple", "moderate", "challenging"}, q.qid


SHAPES = {"plain": 6, "any_k": 3, "top_n": 3, "multi_filter": 5, "boolean": 2, "cheap_after": 3,
          "join_fanout": 3, "cte_reuse": 2, "case": 2, "distinct_exists": 1}


@pytest.mark.parametrize("kind", ["aisql", "oracle"])
def test_every_question_has_its_queries(kind):
    for q in load_questions():
        assert query_path(kind, q.qid).is_file(), (kind, q.qid)


@pytest.mark.parametrize("db", paths.DATABASES)
def test_shape_quota(db):
    shapes = Counter(q.shape for q in load_questions(db))
    assert shapes == SHAPES, db


def test_every_aisql_query_is_in_prompt_form():
    for q in load_questions():
        assert lint(load_query("aisql", q.qid)) == [], q.qid


def test_metadata_covers_every_database():
    assert set(load_masked_columns()) == set(paths.DATABASES)


@pytest.fixture(scope="module")
def original_schemas():
    schemas = {}
    for db in paths.DATABASES:
        path = paths.database_path(db)
        if not path.is_file():
            pytest.skip("run `swan-bench prepare` first")
        con = sqlite3.connect(path)
        tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
        schemas[db] = {t: [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')] for t in tables}
        con.close()
    return schemas


def test_masked_columns_exist(original_schemas):
    for db, tables in load_masked_columns().items():
        for table, columns in tables.items():
            assert set(columns) <= set(original_schemas[db][table]), (db, table)


def test_gold_sql_runs_on_original_databases():
    for q in load_questions():
        path = paths.database_path(q.db)
        if not path.is_file():
            pytest.skip("run `swan-bench prepare` first")
        con = sqlite3.connect(path)
        con.execute(q.gold_sql).fetchall()
        con.close()
