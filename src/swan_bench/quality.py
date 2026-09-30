"""Per-question quality, following SemBench's metrics.

SemBench scores each query by the shape of its answer. SWAN picks the metric from the gold result:

- **Aggregate**: the gold result is one row holding one number. Quality is `max(0, 1 - relative error)`
  of the system's first number, as in SemBench's single-value aggregation queries. The system must return
  exactly one row. When the gold value is 0, quality is 1 if the system also returns 0, else 0.
- **Rows**: every other answer. Quality is the F1 of the system's rows against the gold rows, as sets, as in
  SemBench's retrieval queries. Rows match when `execution.results_match` would match them: values in any
  column order, floats to 10 significant digits. When the gold query has a LIMIT k, only the system's first
  k rows count (SemBench's limit-aware scoring; the gold result already has at most k rows). Two empty
  results score 1; an empty result against a non-empty gold scores 0.

- **Any k rows**: when the question's AISQL query ends in LIMIT k without ORDER BY ("list any 5 ..."), many
  answers are right. The gold query then returns every valid row (no LIMIT), and the system's rows are
  scored as SemBench scores its limit queries: precision over the rows returned, recall against at most k
  gold rows.

A query that raises scores 0. The headline number is the mean quality over questions, as in SemBench.
"""

import re

from .execution import _canonical_row, _canonical_value

_LIMIT = re.compile(r"\bLIMIT\s+(\d+)\s*;?\s*$", re.I)


def _number(value):
    value = _canonical_value(value)
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def metric_kind(gold: list) -> str:
    if len(gold) == 1 and len(gold[0]) == 1 and _number(gold[0][0]) is not None:
        return "aggregate"
    return "rows"


def _f1(precision: float, recall: float) -> float:
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def any_k(system_sql: str | None) -> int | None:
    """k when the system query is LIMIT k without ORDER BY at its outermost level."""
    if not system_sql:
        return None
    from .aisql import parse

    tree = parse(system_sql)
    limit = tree.args.get("limit")
    if limit is None or tree.args.get("order") is not None:
        return None
    try:
        return int(limit.expression.this)
    except (AttributeError, ValueError, TypeError):
        return None


def exact_match(predicted: list, gold: list, gold_sql: str, system_sql: str | None = None) -> bool:
    """The 2024 exact match; for an any-k question, k (or all) rows that are all valid."""
    from .execution import results_match

    k = any_k(system_sql)
    if k is None:
        return results_match(predicted, gold, ordered="ORDER BY" in gold_sql.upper())
    rows, valid = [_canonical_row(r) for r in predicted], {_canonical_row(r) for r in gold}
    return len(rows) == min(k, len(valid)) and all(r in valid for r in rows)


def quality(predicted: list, gold: list, gold_sql: str, system_sql: str | None = None) -> dict:
    """{"kind", "quality", and the kind's components}."""
    k = any_k(system_sql)
    if k is not None:
        sys_set, gold_set = {_canonical_row(r) for r in predicted}, {_canonical_row(r) for r in gold}
        if not sys_set or not gold_set:
            q = 1.0 if not sys_set and not gold_set else 0.0
            return {"kind": "any_k", "quality": q, "precision": q, "recall": q}
        correct = len(sys_set & gold_set)
        p, r = correct / len(sys_set), min(correct, k) / min(k, len(gold_set))
        return {"kind": "any_k", "quality": round(_f1(p, r), 4), "precision": round(p, 4), "recall": round(r, 4)}
    kind = metric_kind(gold)
    if kind == "aggregate":
        g = _number(gold[0][0])
        s = None
        if len(predicted) == 1:
            s = next((n for n in map(_number, predicted[0]) if n is not None), None)
        if s is None:
            return {"kind": kind, "quality": 0.0, "value": None, "rel_err": None}
        rel = abs(s - g) / abs(g) if g != 0 else (0.0 if s == 0 else 1.0)
        return {"kind": kind, "quality": round(max(0.0, 1.0 - rel), 4), "value": s, "rel_err": round(rel, 4)}

    m = _LIMIT.search(gold_sql.strip())
    rows = predicted[: int(m.group(1))] if m else predicted
    sys_set, gold_set = {_canonical_row(r) for r in rows}, {_canonical_row(r) for r in gold}
    if not sys_set or not gold_set:
        q = 1.0 if not sys_set and not gold_set else 0.0
        return {"kind": kind, "quality": q, "precision": q, "recall": q}
    correct = len(sys_set & gold_set)
    p, r = correct / len(sys_set), correct / len(gold_set)
    return {"kind": kind, "quality": round(_f1(p, r), 4), "precision": round(p, 4), "recall": round(r, 4)}
