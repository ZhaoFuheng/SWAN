"""Unzip the BIRD databases, build the SWAN 2.0 databases from them, and build their masked copies.

`data/databases/bird/<db>/`: the four BIRD dev databases as shipped (sqlite + database_description).
`data/databases/original/<db>/<db>.sqlite`: the SWAN 2.0 database: BIRD's, sampled and duplicated
(`scale.py`, `data/swan2.json`). Gold queries run here.
`data/databases/masked/<db>/<db>.sqlite`: the SWAN 2.0 database with every column in
`data/masked_columns.json` removed -- the input a system under test gets. A table whose columns are all
masked is dropped.
"""

import shutil
import sqlite3
import zipfile
from pathlib import Path

from . import paths
from .data import load_masked_columns
from .scale import build_swan2
from .sqlite_util import rebuild_table


def extract_databases(force: bool = False) -> list[Path]:
    """Unzip the four databases (skipping macOS metadata). Returns the sqlite paths."""
    out = []
    with zipfile.ZipFile(paths.DATABASES_ZIP) as zf:
        for db in paths.DATABASES:
            target = paths.bird_path(db)
            if target.is_file() and not force:
                out.append(target)
                continue
            prefix = f"dev_databases/{db}/"
            members = [m for m in zf.namelist()
                       if m.startswith(prefix) and not m.endswith("/") and ".DS_Store" not in m]
            for member in members:
                dest = paths.BIRD_DIR / db / member[len(prefix):]
                dest.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(dest, "wb") as dst:
                    shutil.copyfileobj(src, dst)
            out.append(target)
    return out


def _columns(con: sqlite3.Connection, table: str) -> list[str]:
    return [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]


def build_masked(db: str, force: bool = False) -> Path:
    source = paths.database_path(db)
    target = paths.database_path(db, masked=True)
    if target.is_file() and not force and source.is_file() and target.stat().st_mtime >= source.stat().st_mtime:
        return target
    if not source.is_file():
        raise FileNotFoundError(f"{source} does not exist; extract the databases first")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    con = sqlite3.connect(target)
    con.execute("PRAGMA foreign_keys = OFF")
    for table, masked in load_masked_columns()[db].items():
        columns = _columns(con, table)
        if all(c in masked for c in columns):
            con.execute(f'DROP TABLE "{table}"')
            continue
        remaining = [c for c in masked if c in columns]
        for column in list(remaining):
            try:
                con.execute(f'ALTER TABLE "{table}" DROP COLUMN "{column}"')
                remaining.remove(column)
            except sqlite3.OperationalError:
                break
        if remaining:
            rebuild_table(con, table, drop=set(remaining))
    con.commit()
    con.execute("VACUUM")
    con.close()
    return target


def masked_columns_present(db: str) -> list[str]:
    """`table.column` entries of the mask that still exist in the masked copy (empty when the mask holds)."""
    con = sqlite3.connect(paths.database_path(db, masked=True))
    tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    leaks = [f"{t}.{c}" for t, cols in load_masked_columns()[db].items() if t in tables
             for c in cols if c in _columns(con, t)]
    con.close()
    return leaks


def prepare(force: bool = False, masked: bool = True) -> None:
    for path in extract_databases(force):
        print(f"bird      {path.relative_to(paths.ROOT)}")
    for db in paths.DATABASES:
        path = build_swan2(db, force)
        print(f"original  {path.relative_to(paths.ROOT)}")
    if not masked:
        return
    for db in paths.DATABASES:
        path = build_masked(db, force)
        leaks = masked_columns_present(db)
        if leaks:
            raise RuntimeError(f"{db}: masked columns still present: {leaks}")
        print(f"masked    {path.relative_to(paths.ROOT)}")
