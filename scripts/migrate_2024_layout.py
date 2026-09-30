"""HISTORICAL: this one-off script converted the 2024 notebook layout (still in the git history) to
release 0.2.0. It reads files that are no longer in the tree, and later changes (HQDL removed, queries
moved to `queries/<system>/`) are not reflected in its output.

One-off migration of the 2024 SWAN layout (notebooks, pickles, per-database CSVs) to `data/`.

Run once from the repository root against a checkout of the 2024 layout:

    uv run python scripts/migrate_2024_layout.py

It writes `data/questions.csv`, `data/masked_columns.json`, `data/table_keys.json` and
`data/hqdl/prefix_keys.json`. Every correction to the 2024 data is spelled out below and in docs/CHANGES.md.
"""

import csv
import json
import pickle
import re
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from blendsql_2024_syntax import translate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LEGACY_QUESTIONS = ROOT / "beyond-database-questions"
DATABASES = ["california_schools", "superhero", "formula_1", "european_football_2"]
QUESTION_FILES = {
    "california_schools": ("CASchoolQueries.csv", "CASchool_HybridQueries.csv"),
    "superhero": ("superheroQueries.csv", "superhero_HybridQueries.csv"),
    "formula_1": ("formula_1Queries.csv", "formula_1_HybridQueries.csv"),
    "european_football_2": ("european_football_2Queries.csv", "european_football_2_HybridQueries.csv"),
}

# formula_1: in the 2024 hybrid file, the queries stored at rows 22-24 answer questions 23-25, row 25 is a
# near-duplicate of row 26, and question 22 had no hybrid query. Map each question to the 2024 row that answers it.
FORMULA_1_HYBRID_ROW = {22: None, 23: 22, 24: 23, 25: 24}

# Question formula_1-22 ("For the driver who set the fastest lap speed, what is his nationality?"): written in
# 2026 following the database's other nationality queries (drivers.nationality is masked).
FORMULA_1_22 = """WITH fastest AS (
    SELECT T1.forename || ' ' || T1.surname AS key
    FROM drivers AS T1
    INNER JOIN results AS T2 ON T2.driverId = T1.driverId
    WHERE T2.fastestLapTime IS NOT NULL
    ORDER BY T2.fastestLapSpeed DESC
    LIMIT 1
)
SELECT {{
    LLMMap(
        'Provide the nationality.',
        fastest.key
    )
}} AS nationality
FROM fastest
"""

# Question formula_1-23: the 2024 query put its LLMQA alone in a CTE that the outer query cross-joins, which
# BlendSQL 0.1.x cannot resolve ("no such table"). Same logic with the LLMQA inline; options as a SQL tuple.
MONTHS = "('1','2','3','4','5','6','7','8','9','10','11','12')"
FORMULA_1_23 = f"""WITH race_data AS (
    SELECT *, T1.year || ' ' || T1.name AS key
    FROM races AS T1
    WHERE T1.year = (SELECT DISTINCT MIN(year) FROM races)
)
SELECT name
FROM race_data
WHERE {{{{
    LLMMap(
        'Provide the month of the race.',
        race_data.key,
        options={MONTHS}
    )
}}}} = {{{{
    LLMQA(
        'Earliest month of these races?',
        (SELECT name, year FROM races WHERE year = (SELECT MIN(year) FROM races)),
        options={MONTHS}
    )
}}}}
"""

# european_football_2-01 and -20: the 2024 queries read masked columns (Match.home_team_goal/away_team_goal,
# Player.height) in plain SQL, so part of the answer came from the original data; they fail on the masked
# database. Same logic with the masked values derived by the LLM, as in the database's other queries.
EUROPEAN_FOOTBALL_2_01 = """WITH temp_cte AS (
    SELECT "Match".id,
           'Hometeam: ' || hometeam.team_long_name || ', Awayteam: ' || awayteam.team_long_name AS teamnames,
           'Hometeam: ' || hometeam.team_long_name || ', Awayteam: ' || awayteam.team_long_name
               || ', Date: ' || "Match".date AS match_key
    FROM "Match"
    INNER JOIN Team AS awayteam ON "Match".away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON "Match".home_team_api_id = hometeam.team_api_id
    WHERE "Match".season = '2015/2016'
),
temp2 AS (
    SELECT temp_cte.id, {{
        LLMMap(
            'Provide the football league name.',
            temp_cte.teamnames
        )
    }} AS league_name
    FROM temp_cte
    WHERE {{
        LLMMap(
            'Did the match end in a draw?',
            temp_cte.match_key
        )
    }} = TRUE
)
SELECT temp2.league_name
FROM temp2
GROUP BY temp2.league_name
ORDER BY COUNT(temp2.id) DESC LIMIT 1
"""

EUROPEAN_FOOTBALL_2_20 = """WITH player_key AS (
    SELECT T1.player_name,
           T1.player_api_id,
           'Player Name: ' || T1.player_name AS player_key
    FROM Player AS T1
),
temp_cte AS (
    SELECT *,
           {{
               LLMMap(
                   'Provide the height in cm.',
                   player_key.player_key
               )
           }} AS height
    FROM player_key
)
SELECT A
FROM (
    SELECT AVG(T3.finishing) AS result, 'Max' AS A
    FROM temp_cte
    INNER JOIN Player_Attributes AS T3 ON temp_cte.player_api_id = T3.player_api_id
    WHERE temp_cte.height = (SELECT MAX(height) FROM temp_cte)

    UNION

    SELECT AVG(T3.finishing) AS result, 'Min' AS A
    FROM temp_cte
    INNER JOIN Player_Attributes AS T3 ON temp_cte.player_api_id = T3.player_api_id
    WHERE temp_cte.height = (SELECT MIN(height) FROM temp_cte)
) AS result_table
ORDER BY result DESC
LIMIT 1
"""
OVERRIDES = {
    ("formula_1", 22): FORMULA_1_22,
    ("formula_1", 23): FORMULA_1_23,
    ("european_football_2", 1): EUROPEAN_FOOTBALL_2_01,
    ("european_football_2", 20): EUROPEAN_FOOTBALL_2_20,
}

# 2024 columns_to_drop.pickle: the California table is `frpm` (not `fprm`); `schools.Country` is `schools.County`;
# two entries had lost the comma between them. Everything else is kept as it was.
MASKED_FIXES = {"fprm": "frpm"}
MASKED_COLUMN_FIXES = {("schools", "Country"): ("schools", "County")}


def read_schemas(zip_path: Path) -> dict[str, dict[str, list[str]]]:
    """table -> columns per database, read from the zipped sqlite files."""
    schemas = {}
    with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(zip_path) as zf:
        for db in DATABASES:
            member = f"dev_databases/{db}/{db}.sqlite"
            zf.extract(member, tmp)
            con = sqlite3.connect(Path(tmp) / member)
            tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
            schemas[db] = {t: [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')] for t in tables}
            con.close()
    return schemas


def canonical_table(schema: dict[str, list[str]], name: str) -> str:
    name = MASKED_FIXES.get(name, name)
    for table in schema:
        if table.lower() == name.lower():
            return table
    raise KeyError(name)


def migrate_masked_columns(schemas) -> dict:
    legacy = pickle.load(open(ROOT / "databases" / "columns_to_drop.pickle", "rb"))
    out = {}
    for db in DATABASES:
        tables: dict[str, list[str]] = {}
        for entry in legacy[db]:
            for table, column in re.findall(r"([A-Za-z_]+)\.(`[^`]+`|[A-Za-z_]+)", entry):
                table = canonical_table(schemas[db], table)
                column = column.strip("`")
                table, column = MASKED_COLUMN_FIXES.get((table, column), (table, column))
                assert column in schemas[db][table], (db, table, column)
                tables.setdefault(table, [])
                if column not in tables[table]:
                    tables[table].append(column)
        out[db] = tables
    return out


def migrate_table_keys(schemas) -> dict:
    legacy = pickle.load(open(ROOT / "databases" / "db_table_keys.pickle", "rb"))
    out = {}
    for db in DATABASES:
        out[db] = {}
        for table, spec in legacy[db].items():
            table = canonical_table(schemas[db], table)
            keys = [k.strip("`") for k in spec["keys"]]
            missing = [k for k in keys if k not in schemas[db][table]]
            if missing:  # kept as in 2024 (League/Country list Match's foreign-key names); see docs/CHANGES.md
                print(f"note: {db}.{table} keys {missing} are not columns of {table}")
            out[db][table] = keys
    return out


def migrate_questions() -> list[dict]:
    rows = []
    for db in DATABASES:
        hqdl_file, hybrid_file = QUESTION_FILES[db]
        hqdl = list(csv.reader(open(LEGACY_QUESTIONS / hqdl_file, newline="")))
        hybrid = list(csv.reader(open(LEGACY_QUESTIONS / hybrid_file, newline="")))
        assert len(hqdl) == len(hybrid) == 30
        for i, (h, b) in enumerate(zip(hqdl, hybrid)):
            assert h[:5] == b[:5], (db, i)
            source = FORMULA_1_HYBRID_ROW.get(i, i) if db == "formula_1" else i
            blendsql_2024 = hybrid[source][5] if source is not None else ""
            blendsql = OVERRIDES.get((db, i)) or translate(blendsql_2024)
            rows.append({
                "qid": f"{db}-{i:02d}",
                "db": db,
                "question": h[1],
                "evidence": h[2],
                "difficulty": h[4],
                "gold_sql": h[3],
                "hqdl_sql": h[5],
                "blendsql_sql": blendsql.strip() + "\n",
                "blendsql_sql_2024": blendsql_2024,
            })
    return rows


def main() -> None:
    zip_path = next(p for p in (ROOT / "databases" / "dev_databases.zip", ROOT / "data" / "databases" / "dev_databases.zip")
                    if p.is_file())
    schemas = read_schemas(zip_path)
    data = ROOT / "data"
    (data / "hqdl").mkdir(parents=True, exist_ok=True)

    json.dump(migrate_masked_columns(schemas), open(data / "masked_columns.json", "w"), indent=2)
    json.dump(migrate_table_keys(schemas), open(data / "table_keys.json", "w"), indent=2)

    prefix_keys = pickle.load(open(ROOT / "HQDL" / "prefix_keys.p", "rb"))
    json.dump(prefix_keys, open(data / "hqdl" / "prefix_keys.json", "w"), ensure_ascii=False)
    assert json.load(open(data / "hqdl" / "prefix_keys.json")) == prefix_keys

    rows = migrate_questions()
    with open(data / "questions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} questions and the metadata files to {data}")


if __name__ == "__main__":
    main()
