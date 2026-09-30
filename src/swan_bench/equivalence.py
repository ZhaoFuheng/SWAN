"""Check that BlendSQL and LOTUS run the same query as SWAN-AISQL: all three systems answer every AI call
through the shadow model (`shadow.py`), so their results must be identical. `swan-bench check` runs it."""

from . import paths
from .aisql import ai_calls, parse
from .data import load_query, load_questions
from .execution import _canonical_row
from .meter import Meter
from .quality import any_k
from .shadow import ShadowModel


def _prefixes(queries: list[str]) -> list[str]:
    return [c.prompt_prefix for q in queries for c in ai_calls(parse(q)) if c.fn != "ai_agg"]


def _without_limit(query: str) -> str:
    tree = parse(query)
    tree.set("limit", None)
    return tree.sql("duckdb")


def canonical(rows: list, ordered: bool):
    rows = [_canonical_row(r) for r in rows]
    return rows if ordered else sorted(rows, key=repr)


def check(questions, duckdb_bin: str, systems=("aisql", "blendsql", "lotus"), queries: dict | None = None) -> list[dict]:
    from .systems import load_system

    queries = queries or {q.qid: load_query("aisql", q.qid) for q in questions}
    shadow = ShadowModel(_prefixes(list(queries.values())))
    out = []
    with Meter(None, responder=shadow.respond) as meter:
        runners = {s: load_system(s)("shadow", meter.url, duckdb_bin=duckdb_bin, concurrency=4) for s in systems}
        for q in questions:
            results, record = {}, {"qid": q.qid}
            for s, system in runners.items():
                meter.reset()
                try:
                    results[s] = system.execute(q, queries[q.qid])
                    record[s] = {"rows": len(results[s]), "calls": meter.snapshot()["requests"]}
                except Exception as ex:  # noqa: BLE001
                    record[s] = {"error": f"{type(ex).__name__}: {ex}"[:300]}
            ordered = "ORDER BY" in queries[q.qid].upper()
            ok = [s for s in results]
            k = any_k(queries[q.qid])
            if k is not None and len(ok) == len(systems):
                # "any k rows": each system may return a different valid set, so compare with every valid row
                meter.reset()
                every = [_canonical_row(r) for r in runners["aisql"].execute(q, _without_limit(queries[q.qid]))]
                valid = set(every)  # copies of an entity can give identical rows: count them as rows
                record["equal"] = all(len(results[s]) == min(k, len(every))
                                      and all(_canonical_row(r) in valid for r in results[s]) for s in ok)
            else:
                record["equal"] = len(ok) == len(systems) and all(
                    canonical(results[s], ordered) == canonical(results[ok[0]], ordered) for s in ok)
            if not record["equal"] and len(ok) > 1:
                record["sample"] = {s: [list(r) for r in results[s][:3]] for s in ok}
            out.append(record)
    return out
