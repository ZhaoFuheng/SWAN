"""SQLite table surgery shared by masking and the SWAN 2.0 build."""

import sqlite3


def rebuild_table(con: sqlite3.Connection, table: str, drop: set[str] = frozenset(), keep_unique: bool = True) -> None:
    """Recreate `table` without `drop`: same declared types, NOT NULL, defaults and primary key, every index
    that does not use a dropped column, same rows. Used when SQLite cannot drop a column in place (a UNIQUE,
    primary-key or foreign-key column); only the constraints that involved dropped columns are lost.
    Inline UNIQUE constraints are always lost; `keep_unique=False` also drops UNIQUE indexes (SWAN 2.0
    duplicates rows, which breaks natural-key uniqueness by design)."""
    info = [r for r in con.execute(f'PRAGMA table_info("{table}")') if r[1] not in drop]
    columns = []
    for _, name, decl_type, notnull, default, _pk in info:
        column = f'"{name}" {decl_type}'.rstrip()
        if notnull:
            column += " NOT NULL"
        if default is not None:
            column += f" DEFAULT {default}"
        columns.append(column)
    primary_key = [r[1] for r in sorted(info, key=lambda r: r[5]) if r[5]]
    if primary_key:
        columns.append("PRIMARY KEY (" + ", ".join(f'"{c}"' for c in primary_key) + ")")
    indexes = [sql for (sql,) in con.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'index' AND tbl_name = ? AND sql IS NOT NULL", (table,))]
    names = ", ".join(f'"{r[1]}"' for r in info)
    con.execute(f'CREATE TABLE "__swan_masked" ({", ".join(columns)})')
    con.execute(f'INSERT INTO "__swan_masked" ({names}) SELECT {names} FROM "{table}"')
    con.execute(f'DROP TABLE "{table}"')
    con.execute(f'ALTER TABLE "__swan_masked" RENAME TO "{table}"')
    for sql in indexes:
        if not any(c in sql for c in drop) and (keep_unique or "UNIQUE" not in sql.upper()):
            con.execute(sql)
