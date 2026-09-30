"""The systems under test. Each runs its own query for a question on the MASKED database and returns rows.

A system is a class with a `name` (its directory under `queries/`), a constructor taking the model name,
the OpenAI-compatible endpoint the runner hands it (the meter) and system options, and
`execute(question, query) -> list[tuple]`. Optionally `close()` and `last_usage() -> dict` (the system's
own accounting of the query it just ran).
"""

SYSTEMS = ("blendsql", "lotus", "aisql")


def load_system(name: str):
    if name == "blendsql":
        from .blendsql import BlendSQLSystem
        return BlendSQLSystem
    if name == "lotus":
        from .lotus import LotusSystem
        return LotusSystem
    if name == "aisql":
        from .aisql import AISQLSystem
        return AISQLSystem
    raise ValueError(f"unknown system {name!r}; expected one of {', '.join(SYSTEMS)}")
