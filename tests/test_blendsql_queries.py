"""Every AISQL query's BlendSQL translation parses and executes under the installed BlendSQL, on the MASKED
databases (a query that read a masked column would fail here). The model is a local stub, so no API key or
network is needed. `swan-bench check` goes further and compares all three systems' results."""

import pytest

from swan_bench import paths
from swan_bench.data import load_query, load_questions
from swan_bench.translate_blendsql import to_blendsql

blendsql = pytest.importorskip("blendsql")
pytestmark = pytest.mark.blendsql


@pytest.fixture(scope="module")
def make_engine():
    from blendsql import BlendSQL
    from blendsql.ingredients import LLMJoin, LLMMap, LLMQA

    from .stub_model import StubModel

    for db in paths.DATABASES:
        if not paths.database_path(db, masked=True).is_file():
            pytest.skip("run `swan-bench prepare` first")

    # A fresh engine per query: an engine keeps the temporary tables of the queries it ran, and a later query
    # with a CTE of the same name would read them.
    def make(db):
        return BlendSQL(str(paths.database_path(db, masked=True)), model=StubModel(),
                        ingredients={LLMMap, LLMQA, LLMJoin})

    return make


@pytest.mark.parametrize("question", load_questions(), ids=lambda q: q.qid)
def test_query_runs_on_masked_database(make_engine, question):
    make_engine(question.db).execute(to_blendsql(load_query("aisql", question.qid)))
