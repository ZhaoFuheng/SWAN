"""Repository-relative locations. Everything under `data/databases/` other than the zip, and all of `runs/`,
is generated locally (`swan-bench prepare`, the runners) and git-ignored.

`data/databases/bird/<db>/`: the BIRD database as shipped. `original/<db>/<db>.sqlite`: the SWAN 2.0 database
built from it (docs/SWAN2_DESIGN.md). `masked/<db>/<db>.sqlite`: the original without the masked columns."""

import os
from pathlib import Path

DATABASES = ("california_schools", "superhero", "formula_1", "european_football_2")

ROOT = Path(os.environ.get("SWAN_BENCH_ROOT", Path(__file__).resolve().parents[2]))
DATA = ROOT / "data"
QUESTIONS_DIR = DATA / "questions"  # one CSV per database
MASKED_COLUMNS_JSON = DATA / "masked_columns.json"
TABLE_KEYS_JSON = DATA / "table_keys.json"
QUERIES = ROOT / "queries"

SWAN2_CONFIG = DATA / "swan2.json"

DATABASES_ZIP = DATA / "databases" / "dev_databases.zip"
BIRD_DIR = DATA / "databases" / "bird"
ORIGINAL_DIR = DATA / "databases" / "original"
MASKED_DIR = DATA / "databases" / "masked"

RESULTS = ROOT / "results"
RUNS = ROOT / "runs"


def bird_path(db: str) -> Path:
    """The BIRD database as shipped, which SWAN 2.0 is built from."""
    if db not in DATABASES:
        raise ValueError(f"unknown database {db!r}; expected one of {', '.join(DATABASES)}")
    return BIRD_DIR / db / f"{db}.sqlite"


def database_path(db: str, masked: bool = False) -> Path:
    """The sqlite file of `db`: the SWAN 2.0 original (scaled and duplicated; gold queries run here), or its
    masked copy (systems run here)."""
    if db not in DATABASES:
        raise ValueError(f"unknown database {db!r}; expected one of {', '.join(DATABASES)}")
    return (MASKED_DIR if masked else ORIGINAL_DIR) / db / f"{db}.sqlite"


def require_database(db: str, masked: bool = False) -> Path:
    path = database_path(db, masked)
    if not path.is_file():
        raise FileNotFoundError(f"{path} does not exist; run `swan-bench prepare` first")
    return path
