"""A masked database differs from its original only by the masked columns."""

import sqlite3

import pytest

from swan_bench import paths
from swan_bench.data import load_masked_columns


@pytest.mark.parametrize("db", paths.DATABASES)
def test_masked_copy_drops_exactly_the_masked_columns(db):
    original, masked = paths.database_path(db), paths.database_path(db, masked=True)
    if not (original.is_file() and masked.is_file()):
        pytest.skip("run `swan-bench prepare` first")
    mask = load_masked_columns()[db]
    o, m = sqlite3.connect(original), sqlite3.connect(masked)
    masked_tables = {r[0] for r in m.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    for (table,) in o.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name != 'sqlite_sequence'"):
        kept = [r for r in o.execute(f'PRAGMA table_info("{table}")') if r[1] not in mask.get(table, [])]
        if not kept:
            assert table not in masked_tables  # every column masked: the table is gone
            continue
        assert [r[1:] for r in kept] == [r[1:] for r in m.execute(f'PRAGMA table_info("{table}")')], table
        columns = ", ".join(f'"{r[1]}"' for r in kept)
        count = f'SELECT count(*) FROM "{table}"'
        assert o.execute(count).fetchone() == m.execute(count).fetchone(), table
        assert set(o.execute(f'SELECT {columns} FROM "{table}"')) == set(m.execute(f'SELECT {columns} FROM "{table}"'))
    o.close()
    m.close()
