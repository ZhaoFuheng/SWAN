"""Translate a SWAN 2.0 AISQL query into a BlendSQL (0.1.x) query, mechanically.

| AISQL | BlendSQL |
|---|---|
| `ai_filter('Q name: ' \|\| t.name)` | `{{LLMMap('Q', t.name)}} = TRUE` (no parentheses: BlendSQL then loses the alias) |
| `NOT ai_filter(...)` | `{{LLMMap('Q', t.name)}} = FALSE` |
| `ai_complete('Q name: ' \\|\\| t.name \\|\\| ' S')` | `{{LLMMap('Q S', t.name, return_type='str')}}` |
| `ai_classify('Q name: ' \\|\\| t.name, ['A', 'B'])` | `{{LLMMap('Q', t.name, options=('A', 'B'))}}` |
| `ai_classify(..., (SELECT list(DISTINCT c ORDER BY c) FROM u))` | `{{LLMMap('Q', t.name, options=u.c)}}` |
| `(SELECT ai_agg(list(t.name), 'I') FROM ... WHERE ...)` | `{{LLMQA('I', (SELECT t.name FROM ... WHERE ...))}}` |

BlendSQL shows the model `{"name": value}` as context, the same `name: value` SWAN-AISQL and LOTUS show.
The rest of the query is transpiled from DuckDB to sqlite by sqlglot (`//`, `ILIKE`, `TRY_CAST`, NULL
ordering, ...), so BlendSQL, which runs on sqlite, keeps the query's meaning.
"""

from sqlglot import exp

from .aisql import AICall, ai_calls, parse


def _str(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def _column(column: exp.Column) -> str:
    return f"{column.table}.{column.name}" if column.table else column.name


def ingredient(call: AICall, agg_context_sql: str | None = None, negated: bool = False) -> str:
    if call.fn == "ai_filter":
        # `NOT {{...}} = TRUE` makes BlendSQL skip the ingredient entirely: a negation becomes `= FALSE`
        return f"{{{{LLMMap({_str(call.question)}, {_column(call.context)})}}}} = {'FALSE' if negated else 'TRUE'}"
    if call.fn == "ai_complete":
        # an explicit type: BlendSQL otherwise infers it from nearby columns (e.g. a CASE condition's int)
        return f"{{{{LLMMap({_str(call.question + call.suffix)}, {_column(call.context)}, return_type='str')}}}}"
    if call.fn == "ai_classify":
        if call.labels is not None:
            options = "(" + ", ".join(_str(label) for label in call.labels) + ")"
        else:
            options = f"{call.labels_from[0]}.{call.labels_from[1]}"
        return f"{{{{LLMMap({_str(call.question)}, {_column(call.context)}, options={options}, return_type='str')}}}}"
    return f"{{{{LLMQA({_str(call.instruction)}, ({agg_context_sql}))}}}}"


def to_blendsql(query: str) -> str:
    tree = parse(query)
    replacements = {}
    for i, call in enumerate(ai_calls(tree)):
        placeholder = f"__swan_ai_{i}"
        if call.fn == "ai_agg":
            select = call.node.find_ancestor(exp.Select)
            context = select.copy()
            context.set("expressions", [call.context.copy()])
            text = ingredient(call, context.sql("sqlite"))
            target = select.parent if isinstance(select.parent, exp.Subquery) else None
            if target is not None:
                target.replace(exp.column(placeholder))
            else:  # top-level SELECT ai_agg(...) FROM ...: the answer is the whole result
                tree = exp.select(exp.column(placeholder))
            replacements[placeholder] = text
        else:
            target, negated = call.node, False
            parent = call.node.parent
            while isinstance(parent, exp.Paren):
                parent = parent.parent
            if call.fn == "ai_filter" and isinstance(parent, exp.Not):
                target, negated = parent, True
            replacements[placeholder] = ingredient(call, negated=negated)
            target.replace(exp.column(placeholder))
    sql = tree.sql("sqlite", pretty=True)
    for placeholder, text in replacements.items():
        sql = sql.replace(placeholder, text)
    return sql
