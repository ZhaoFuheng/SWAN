"""The SWAN 2.0 generator: seeded sampling and duplication that keep every reference intact."""

import random
import sqlite3

import pytest

from swan_bench import paths
from swan_bench.scale import duplicate, poisson, sample


def _db():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE hero (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    con.execute("CREATE TABLE power (pid INTEGER PRIMARY KEY, hero_id INTEGER, power TEXT)")
    con.executemany("INSERT INTO hero VALUES (?, ?)", [(i, f"h{i}") for i in range(1, 201)])
    con.executemany("INSERT INTO power VALUES (?, ?, ?)", [(i, 1 + i % 200, f"p{i}") for i in range(1, 601)])
    return con


RULE = {"table": "hero", "ids": ["id"], "dependents": [{"table": "power", "fk": {"hero_id": "id"}}]}


def test_poisson_mean():
    rng = random.Random(1)
    draws = [poisson(rng, 1.0) for _ in range(20000)]
    assert abs(sum(draws) / len(draws) - 1.0) < 0.03 and min(draws) == 0


def test_duplicates_copy_rows_and_their_dependents():
    con = _db()
    report = duplicate(con, RULE, mean_copies=2, seed=7, db="t")
    heroes = con.execute("SELECT count(*), count(DISTINCT id), count(DISTINCT name) FROM hero").fetchone()
    assert heroes[0] == 200 + report["copies_added"] and heroes[1] == heroes[0] and heroes[2] == 200
    assert 1.7 < heroes[0] / 200 < 2.3
    # every copy has the same powers as its original, under its own id
    per_name = con.execute("""SELECT h.name, count(DISTINCT h.id), count(p.pid) FROM hero h
                              LEFT JOIN power p ON p.hero_id = h.id GROUP BY h.name""").fetchall()
    assert all(powers == copies * 3 for _, copies, powers in per_name)
    assert con.execute("SELECT count(*) FROM power WHERE hero_id NOT IN (SELECT id FROM hero)").fetchone()[0] == 0
    assert con.execute("SELECT count(DISTINCT pid) = count(*) FROM power").fetchone()[0] == 1


def test_duplication_is_seeded():
    a, b = _db(), _db()
    duplicate(a, RULE, 2, seed=7, db="t")
    duplicate(b, RULE, 2, seed=7, db="t")
    dump = lambda c: c.execute("SELECT * FROM hero ORDER BY id").fetchall()
    assert dump(a) == dump(b)


def test_sampling_drops_dependents_of_dropped_rows():
    con = _db()
    rule = {"table": "hero", "key": "id", "size_by": "power",
            "dependents": [{"table": "power", "fk": {"hero_id": "id"}}]}
    report = sample(con, rule, target_rows=150, seed=3, db="t")
    assert report["kept"] == 50
    assert con.execute("SELECT count(*) FROM power").fetchone()[0] == 150
    assert con.execute("SELECT count(*) FROM power WHERE hero_id NOT IN (SELECT id FROM hero)").fetchone()[0] == 0
    assert sample(con, rule, target_rows=1000, seed=3, db="t")["kept"] is None  # already small enough


REFERENCES = {
    "california_schools": [("frpm", "CDSCode", "schools", "CDSCode"), ("satscores", "cds", "schools", "CDSCode")],
    "superhero": [("hero_power", "hero_id", "superhero", "id"), ("hero_attribute", "hero_id", "superhero", "id")],
    "formula_1": [("results", "driverId", "drivers", "driverId"), ("results", "raceId", "races", "raceId"),
                  ("races", "circuitId", "circuits", "circuitId"), ("qualifying", "raceId", "races", "raceId")],
    "european_football_2": [("Player_Attributes", "player_api_id", "Player", "player_api_id"),
                            ("Match", "home_team_api_id", "Team", "team_api_id"),
                            ("Team_Attributes", "team_api_id", "Team", "team_api_id")],
}


def _orphans(path, child, fk, parent, key) -> int:
    con = sqlite3.connect(path)
    try:
        return con.execute(f'SELECT count(*) FROM "{child}" WHERE "{fk}" IS NOT NULL AND "{fk}" NOT IN '
                           f'(SELECT "{key}" FROM "{parent}")').fetchone()[0]
    finally:
        con.close()


@pytest.mark.parametrize("db", paths.DATABASES)
def test_built_databases_add_no_broken_references(db):
    # BIRD itself has dangling references (e.g. 1,361 satscores rows name no school); the build adds none
    built, bird = paths.database_path(db), paths.bird_path(db)
    if not built.is_file() or not bird.is_file():
        pytest.skip("run `swan-bench prepare` first")
    for ref in REFERENCES[db]:
        assert _orphans(built, *ref) <= _orphans(bird, *ref), ref
