"""Translate SWAN's 2024 BlendSQL queries (written for BlendSQL 0.0.x) to the BlendSQL 0.1.x syntax.

Used once by `migrate_2024_layout.py`; kept as the record of how `data/questions.csv:blendsql_sql` was derived
from `blendsql_sql_2024`. Every rewrite is syntactic and preserves the query's meaning:

1. Column arguments: `'table::column'` and `(table::column)` become plain SQL references, `table.column`.
2. A missing comma between an ingredient's question and its column (`LLMMap('q?' 'T1::c')`): BlendSQL 0.0.x
   read the two adjacent strings as one, so the column was silently dropped. The comma is added.
3. A CTE named `temp` is renamed `temp_cte`: BlendSQL 0.1.x rewrites the CTE's table but leaves `temp.column`
   references behind (`temp` is also SQLite's temp schema).
4. Inside `{{ ... }}`, a table the query only uses under an alias is referred to by that alias.
5. `SELECT t.*, {{...}} FROM t` becomes `SELECT *, {{...}} FROM t` (same columns; 0.1.x does not rewrite `t.*`).
"""

import re

_IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
_SQL_WORDS = {"on", "where", "inner", "left", "right", "outer", "cross", "join", "group", "order", "limit",
              "union", "having", "natural", "using", "as", "and", "or"}


def _ref(table: str, column: str) -> str:
    def quote(x: str) -> str:
        x = x.strip().strip('`"')
        return x if re.fullmatch(_IDENT, x) else '"' + x.replace('"', '""') + '"'

    return f"{quote(table)}.{quote(column)}"


def _outside_strings(query: str, fn) -> str:
    """Apply `fn` to the parts of `query` outside single-quoted string literals."""
    parts = re.split(r"('(?:[^']|'')*')", query)
    return "".join(p if i % 2 else fn(p) for i, p in enumerate(parts))


def column_references(query: str) -> str:
    query = re.sub(r"'\s*([^':()]+?)\s*::\s*([^':()]+?)\s*'", lambda m: _ref(m.group(1), m.group(2)), query)
    return re.sub(r"\(\s*(" + _IDENT + r")\s*::\s*(" + _IDENT + r")\s*\)", lambda m: _ref(m.group(1), m.group(2)),
                  query)


def missing_commas(query: str) -> str:
    return re.sub(r"(LLM(?:Map|QA|Join)\s*\(\s*'(?:[^']|'')*')(\s+)(?=[A-Za-z_\"(])", r"\1,\2", query)


def rename_temp_cte(query: str) -> str:
    if not re.search(r"(?i)(\bWITH|,)\s*temp\s+AS\s*\(", query):
        return query
    return _outside_strings(query, lambda s: re.sub(r"\btemp\b", "temp_cte", s))


def aliases_in_ingredients(query: str) -> str:
    aliased: dict[str, set[str]] = {}
    bare: set[str] = set()
    for m in re.finditer(r"(?i)\b(?:FROM|JOIN)\s+(\"?" + _IDENT + r"\"?)(?:\s+(?:AS\s+)?(" + _IDENT + r"))?", query):
        table, alias = m.group(1).strip('"'), m.group(2)
        if alias and alias.lower() not in _SQL_WORDS:
            aliased.setdefault(table, set()).add(alias)
        else:
            bare.add(table)

    def fix(block: str) -> str:
        for table, aliases in aliased.items():
            if table in bare or len(aliases) != 1:
                continue
            block = re.sub(r"(?<![\w.\"])\"?" + re.escape(table) + r"\"?\.", next(iter(aliases)) + ".", block)
        return block

    return re.sub(r"\{\{.*?\}\}", lambda m: fix(m.group(0)), query, flags=re.S)


def unqualified_star(query: str) -> str:
    def fix(m: re.Match) -> str:
        table, rest = m.group(1), m.group(2)
        from_clause = re.search(r"(?is)\bFROM\s+" + re.escape(table) + r"\b\s*(?:\)|WHERE\b|GROUP\b|ORDER\b|LIMIT\b|$)",
                                rest)
        return ("SELECT *" if from_clause else f"SELECT {table}.*") + rest

    return re.sub(r"(?is)SELECT\s+(" + _IDENT + r")\.\*(.*?\bFROM\s+" + _IDENT + r"\b[^,]*?(?:\)|$))", fix, query)


def semicolon_options(query: str) -> str:
    """0.0.x took `options='a;b;c'`; 0.1.x iterates a string option character by character, so the list
    becomes a SQL tuple `options=('a', 'b', 'c')`."""
    def tuple_of(m):
        items = ", ".join("'" + o.strip() + "'" for o in m.group(1).split(";"))
        return f"options=({items})"
    return re.sub(r"options\s*=\s*'([^']*;[^']*)'", tuple_of, query)


def translate(query: str) -> str:
    """The full 0.0.x -> 0.1.x translation."""
    for step in (column_references, missing_commas, rename_temp_cte, aliases_in_ingredients, unqualified_star,
                 semicolon_options):
        query = step(query)
    return query
