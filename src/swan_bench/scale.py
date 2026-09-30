"""Build the SWAN 2.0 databases from the BIRD ones: sample large tables, then duplicate prompt entities.

The rules are in `data/swan2.json`; docs/SWAN2_DESIGN.md explains them. Everything is seeded, so the same
config always produces the same databases.

**Sample.** A `sample` entry keeps a random subset of `table`'s keys, sized so that `size_by` (the table
itself, or a dependent) ends with about `target_rows` rows. Rows of the dependents that reference a dropped
key are deleted with it. A table that is already small enough is left alone.

**Duplicate.** A `duplicate` entry gives each row of `table` `1 + Poisson(mean_copies - 1)` copies in total.
A copy gets fresh values in its `ids` columns (integers: above the column's maximum; text: `<value>_<n>`)
and keeps every other value, so it yields the same LLM prompt as the original. The rows of each dependent
that reference the original are copied too, pointing at the copy; a dependent's own integer primary key,
when it has one that is not a foreign key, gets fresh values as well.
"""

import json
import math
import random
import shutil
import sqlite3
from pathlib import Path

from . import paths
from .sqlite_util import rebuild_table


def load_config(path: Path | None = None) -> dict:
    return json.loads((path or paths.SWAN2_CONFIG).read_text())


def _q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _rng(seed: int, *parts: str) -> random.Random:
    return random.Random(f"{seed}:" + ":".join(parts))


def poisson(rng: random.Random, lam: float) -> int:
    """Knuth's method; fine for the small means used here."""
    if lam <= 0:
        return 0
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def _count(con: sqlite3.Connection, table: str) -> int:
    return con.execute(f"SELECT count(*) FROM {_q(table)}").fetchone()[0]


def sample(con: sqlite3.Connection, rule: dict, target_rows: int, seed: int, db: str) -> dict:
    table, key = rule["table"], rule["key"]
    size_by = rule.get("size_by", table)
    size = _count(con, size_by)
    if size <= target_rows:
        return {"table": table, "kept": None}
    keys = sorted(r[0] for r in con.execute(f"SELECT DISTINCT {_q(key)} FROM {_q(table)} WHERE {_q(key)} IS NOT NULL"))
    n_keep = max(1, round(len(keys) * target_rows / size))
    kept = sorted(_rng(seed, db, "sample", table).sample(keys, n_keep))
    con.execute("CREATE TEMP TABLE __swan_keep (k)")
    con.executemany("INSERT INTO __swan_keep VALUES (?)", [(k,) for k in kept])
    for dep in rule.get("dependents", []):
        (fk_col, _), = dep["fk"].items()
        con.execute(f"DELETE FROM {_q(dep['table'])} WHERE {_q(fk_col)} NOT IN (SELECT k FROM __swan_keep)")
    con.execute(f"DELETE FROM {_q(table)} WHERE {_q(key)} NOT IN (SELECT k FROM __swan_keep)")
    con.execute("DROP TABLE __swan_keep")
    return {"table": table, "kept": len(kept), "of": len(keys)}


class _Ids:
    """Fresh values for an id column: integers above the maximum, text as `<value>_<n>`."""

    def __init__(self, con: sqlite3.Connection, table: str, column: str):
        values = [r[0] for r in con.execute(f"SELECT {_q(column)} FROM {_q(table)} WHERE {_q(column)} IS NOT NULL")]
        self.integer = all(isinstance(v, int) for v in values) and bool(values)
        self.next = (max(values) + 1) if self.integer else None

    def fresh(self, value, copy_number: int):
        if value is None:
            return None
        if self.integer:
            self.next += 1
            return self.next - 1
        return f"{value}_{copy_number}"


def _integer_pk(con: sqlite3.Connection, table: str) -> str | None:
    pk = [r for r in con.execute(f"PRAGMA table_info({_q(table)})") if r[5]]
    if len(pk) == 1 and "INT" in (pk[0][2] or "").upper():
        return pk[0][1]
    return None


def duplicate(con: sqlite3.Connection, rule: dict, mean_copies: float, seed: int, db: str) -> dict:
    table, ids = rule["table"], rule["ids"]
    for t in [table] + [d["table"] for d in rule.get("dependents", [])]:
        rebuild_table(con, t, keep_unique=False)  # copies repeat natural keys (urls, names)
    columns = [r[1] for r in con.execute(f"PRAGMA table_info({_q(table)})")]
    id_gen = {c: _Ids(con, table, c) for c in ids}
    deps = []
    for dep in rule.get("dependents", []):
        dcols = [r[1] for r in con.execute(f"PRAGMA table_info({_q(dep['table'])})")]
        pk = _integer_pk(con, dep["table"])
        pk = pk if pk and pk not in dep["fk"] else None
        deps.append((dep, dcols, _Ids(con, dep["table"], pk) if pk else None, pk))
    rng = _rng(seed, db, "duplicate", table)
    order = ", ".join(_q(c) for c in ids)
    rows = con.execute(f"SELECT {', '.join(_q(c) for c in columns)} FROM {_q(table)} ORDER BY {order}").fetchall()
    placeholders = ", ".join("?" * len(columns))
    added, added_deps = 0, {d[0]["table"]: 0 for d in deps}
    for row in rows:
        extra = poisson(rng, mean_copies - 1)
        original = dict(zip(columns, row))
        for n in range(1, extra + 1):
            copy = dict(original)
            for c in ids:
                copy[c] = id_gen[c].fresh(original[c], n)
            con.execute(f"INSERT INTO {_q(table)} VALUES ({placeholders})", [copy[c] for c in columns])
            added += 1
            for dep, dcols, pk_gen, pk in deps:
                where = " AND ".join(f"{_q(fk)} = ?" for fk in dep["fk"])
                params = [original[parent] for parent in dep["fk"].values()]
                if any(p is None for p in params):
                    continue
                for drow in con.execute(f"SELECT * FROM {_q(dep['table'])} WHERE {where}", params).fetchall():
                    d = dict(zip(dcols, drow))
                    for fk, parent in dep["fk"].items():
                        d[fk] = copy[parent]
                    if pk_gen:
                        d[pk] = pk_gen.fresh(d[pk], n)
                    con.execute(f"INSERT INTO {_q(dep['table'])} VALUES ({', '.join('?' * len(dcols))})",
                                [d[c] for c in dcols])
                    added_deps[dep["table"]] += 1
    return {"table": table, "rows": len(rows), "copies_added": added, "dependent_rows_added": added_deps}


def build_swan2(db: str, force: bool = False, config: dict | None = None) -> Path:
    """The SWAN 2.0 original database of `db`, from the BIRD database."""
    config = config or load_config()
    source, target = paths.bird_path(db), paths.database_path(db)
    if target.is_file() and not force:
        return target
    if not source.is_file():
        raise FileNotFoundError(f"{source} does not exist; unzip the BIRD databases first")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".building")
    shutil.copyfile(source, tmp)
    con = sqlite3.connect(tmp)
    con.execute("PRAGMA foreign_keys = OFF")
    spec = config["databases"][db]
    report = {"config": {k: config[k] for k in ("seed", "target_rows", "mean_copies")}, "sample": [], "duplicate": []}
    for rule in spec.get("sample", []):
        report["sample"].append(sample(con, rule, config["target_rows"], config["seed"], db))
    for rule in spec.get("duplicate", []):
        report["duplicate"].append(duplicate(con, rule, config["mean_copies"], config["seed"], db))
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    report["rows"] = {t: _count(con, t) for t in tables}
    con.commit()
    con.execute("VACUUM")
    con.close()
    tmp.replace(target)
    (target.parent / "swan2_build.json").write_text(json.dumps(report, indent=2) + "\n")
    return target
