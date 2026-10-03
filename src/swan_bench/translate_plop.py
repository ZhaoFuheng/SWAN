r"""Translate a SWAN 2.0 AISQL query into PLOP's (Morrila's) dialect, mechanically.

| AISQL | PLOP |
|---|---|
| `ai_filter(<prompt>)` | `semantic(<prompt>)` |
| `ai_complete(<prompt>)` | `semantic_string(<prompt>)` |
| `ai_classify(<prompt>, <labels>)` | `semantic_string(<prompt> \|\| ' Answer with exactly one of the following labels, verbatim: ' \|\| array_to_string(<labels>, ', '))` |

The prompt expressions are kept as written (PLOP appends its own answer-format suffix to every prompt).
`<labels>` is the literal list or the label subquery of the AISQL call, so the labels the model sees are the
same. PLOP has no aggregation function, so a query with `ai_agg` cannot be translated (none of the 120 has one).
The rest of the query is DuckDB SQL, which PLOP's fork of DuckDB runs as is.
"""
from sqlglot import exp

from .aisql import AISQLFormError, _args, _fn_name, parse

PLOP_FUNCTION = {"ai_filter": "semantic", "ai_complete": "semantic_string", "ai_classify": "semantic_string"}
LABELS_LEAD = " Answer with exactly one of the following labels, verbatim: "


def to_plop(query: str) -> str:
    tree = parse(query)
    for node in list(tree.walk()):
        fn = _fn_name(node)
        if fn is None:
            continue
        if fn == "ai_agg":
            raise AISQLFormError("PLOP has no aggregation function: ai_agg cannot be translated")
        args = _args(node)
        prompt = args[0].copy()
        if fn == "ai_classify":
            labels = exp.Anonymous(this="array_to_string", expressions=[args[1].copy(), exp.Literal.string(", ")])
            prompt = exp.DPipe(this=exp.DPipe(this=prompt, expression=exp.Literal.string(LABELS_LEAD)), expression=labels)
        node.replace(exp.Anonymous(this=PLOP_FUNCTION[fn], expressions=[prompt]))
    return tree.sql("duckdb")
