"""Run a SWAN 2.0 AISQL query the way a LOTUS program written from it would run: in its written logical order.

LOTUS is a library of semantic operators on DataFrames, not a query engine, so a LOTUS program executes
exactly the order its author wrote. This interpreter is that program, derived mechanically from the AISQL
query, so no author decides LOTUS's plan:

1. CTEs, in order, and subqueries in FROM become DataFrames.
2. The FROM/JOIN frame is built (sqlite). AI conditions in an INNER JOIN's ON go to the front of WHERE.
3. WHERE's top-level AND conditions are applied in the order written: a plain condition filters the frame
   (sqlite); a condition with AI calls first evaluates each call on every row of the current frame
   (`sem_filter` / `sem_map`), then filters.
4. AI calls in SELECT, GROUP BY, HAVING and ORDER BY are evaluated on every row that passed WHERE, before
   grouping, sorting and LIMIT.
5. The rest of the query (grouping, sorting, LIMIT) runs in sqlite on the result.

Each AI call runs once per row it reaches, with no deduplication: that is what `df.sem_filter(...)` does.
A NULL context gives a NULL answer without a call, as in SWAN-AISQL. The relational parts run in sqlite
(the query is transpiled from DuckDB by sqlglot), as BlendSQL's do.

The LLM work goes through `ops` (`LotusOps` in production), so tests can substitute a deterministic model.
"""

import sqlite3

import pandas as pd
from sqlglot import exp

from .aisql import AICall, ai_calls, parse

FRAME = "__swan_frame"


def _q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _python(value):
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and value != value:
        return None
    return value


def _has_ai(node: exp.Expression) -> bool:
    try:
        return bool(ai_calls(node))
    except Exception:  # noqa: BLE001 -- a malformed call still counts as AI
        return True


class LotusOps:
    """The LOTUS operators, one call per row. `values` are non-NULL context values.

    The instruction names the context column as `{name}`; LOTUS then shows the model the value as
    `[Name]: «value»`, its own form of the `name: value` context SWAN-AISQL and BlendSQL show."""

    SUFFIX = "_swan"

    def filter(self, call: AICall, values: list) -> list:
        df = pd.DataFrame({call.name: values})
        out = df.sem_filter(f"{call.question} {{{call.name}}}", return_all=True, suffix=self.SUFFIX)
        return [bool(v) for v in out[self.SUFFIX]]

    def complete(self, call: AICall, values: list) -> list:
        df = pd.DataFrame({call.name: values})
        out = df.sem_map(f"{call.question} {{{call.name}}}{call.suffix}", suffix=self.SUFFIX)
        return [None if v is None else str(v).strip() for v in out[self.SUFFIX]]

    def classify(self, call: AICall, values: list, labels: list[str]) -> list:
        df = pd.DataFrame({call.name: values})
        instruction = (f"{call.question} {{{call.name}}} Answer with exactly one of: "
                       + ", ".join(labels) + ".")
        out = df.sem_map(instruction, suffix=self.SUFFIX)
        return [None if v is None else str(v).strip() for v in out[self.SUFFIX]]

    def agg(self, call: AICall, values: list) -> str:
        df = pd.DataFrame({call.name: values})
        return str(df.sem_agg(f"{call.instruction} {{{call.name}}}", suffix=self.SUFFIX)[self.SUFFIX].iloc[0]).strip()


class LotusExecutor:
    def __init__(self, db_path, ops=None):
        self.con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        self.ops = ops or LotusOps()
        self._n = 0

    def close(self) -> None:
        self.con.close()

    # ---- sqlite helpers -------------------------------------------------------------------------------
    def _name(self, prefix: str) -> str:
        self._n += 1
        return f"__swan_{prefix}_{self._n}"

    def register(self, name: str, df: pd.DataFrame) -> None:
        self.con.execute(f"DROP TABLE IF EXISTS temp.{_q(name)}")
        cols = [str(c) for c in df.columns]
        self.con.execute(f"CREATE TEMP TABLE {_q(name)} ({', '.join(_q(c) for c in cols)})")
        if len(df):
            self.con.executemany(f"INSERT INTO temp.{_q(name)} VALUES ({', '.join('?' * len(cols))})",
                                 [tuple(_python(v) for v in r) for r in df.itertuples(index=False, name=None)])

    def sql(self, node: exp.Expression) -> pd.DataFrame:
        cur = self.con.execute(node.sql("sqlite"))
        return pd.DataFrame(cur.fetchall(), columns=[d[0] for d in cur.description])

    def columns(self, table: str) -> list[str]:
        return [r[1] for r in self.con.execute(f"PRAGMA table_info({_q(table)})")]

    # ---- queries ---------------------------------------------------------------------------------------
    def run(self, query: str) -> pd.DataFrame:
        return self._run(parse(query))

    def _run(self, tree: exp.Expression) -> pd.DataFrame:
        tree = tree.copy()
        with_ = tree.args.get("with_")
        if with_ is not None:
            for cte in with_.expressions:
                self.register(cte.alias, self._run(cte.this))
            tree.set("with_", None)
        if isinstance(tree, exp.SetOperation):
            left, right = self._name("left"), self._name("right")
            self.register(left, self._run(tree.this))
            self.register(right, self._run(tree.expression))
            tree.set("this", exp.select("*").from_(left))
            tree.set("expression", exp.select("*").from_(right))
            return self.sql(tree)
        if isinstance(tree, exp.Subquery):
            return self._run(tree.this)
        if not _has_ai(tree):
            return self.sql(tree)
        return self._run_select(tree)

    def _scalar_subqueries(self, select: exp.Select) -> None:
        """AI subqueries outside FROM (scalar, IN) are evaluated first and replaced by their values."""
        for sub in list(select.find_all(exp.Subquery)):
            if sub.parent is None or isinstance(sub.parent, (exp.From, exp.Join)) or not _has_ai(sub):
                continue
            if sub.find_ancestor(exp.Subquery) not in (None,) and sub.find_ancestor(exp.Subquery) is not sub:
                continue  # nested inside another subquery: evaluated with it
            df = self._run(sub.this)
            values = [_python(v) for v in df.iloc[:, 0]] if len(df.columns) else []
            if isinstance(sub.parent, exp.In):
                sub.replace(exp.Tuple(expressions=[exp.convert(v) for v in values]) if values
                            else exp.Tuple(expressions=[exp.Null()]))
            else:
                sub.replace(exp.convert(values[0]) if values else exp.Null())

    def _sources(self, select: exp.Select) -> list[tuple[str, str]]:
        """(alias, table) of every FROM/JOIN source; subqueries become temp tables."""
        sources = []
        for holder in [select.args.get("from_")] + list(select.args.get("joins") or []):
            if holder is None:
                continue
            src = holder.this
            if isinstance(src, exp.Subquery):
                name = self._name("sub")
                self.register(name, self._run(src.this))
                alias = src.alias or name
                src.replace(exp.to_table(name).as_(alias))
                sources.append((alias, name))
            elif isinstance(src, exp.Table):
                sources.append((src.alias_or_name, src.name))
            else:
                raise NotImplementedError(f"unsupported FROM source: {src.sql()}")
        return sources

    def _run_select(self, select: exp.Select) -> pd.DataFrame:
        self._scalar_subqueries(select)
        if not _has_ai(select):  # the AI was all in scalar subqueries, now values
            return self.sql(select)
        if select.args.get("from_") is None:
            raise NotImplementedError("an AI call in a SELECT without FROM")
        sources = self._sources(select)
        owner = {}  # column name -> aliases that have it
        for alias, table in sources:
            for c in self.columns(table):
                owner.setdefault(c, []).append(alias)

        # AI conditions of INNER JOIN ... ON go to the front of WHERE
        conditions = []
        for join in select.args.get("joins") or []:
            on = join.args.get("on")
            if on is None or not _has_ai(on):
                continue
            if join.side:
                raise NotImplementedError("AI in the ON of an outer join")
            keep = [c for c in _conjuncts(on) if not _has_ai(c)]
            conditions += [c for c in _conjuncts(on) if _has_ai(c)]
            join.set("on", exp.and_(*keep) if keep else exp.true())
        where = select.args.get("where")
        if where is not None:
            conditions += _conjuncts(where.this)

        # the FROM/JOIN frame, every column renamed <alias>__<column>
        frame_select = exp.select(*[exp.column(c, table=a).as_(f"{a}__{c}", quoted=True)
                                    for a, t in sources for c in self.columns(t)])
        frame_select.set("from_", select.args["from_"].copy())
        frame_select.set("joins", [j.copy() for j in select.args.get("joins") or []])
        frame = self.sql(frame_select)

        def rename(node: exp.Expression) -> exp.Expression:
            def fix(n):
                if isinstance(n, exp.Column) and not n.find_ancestor(exp.Subquery):
                    alias = n.table or (owner.get(n.name, [None])[0] if len(owner.get(n.name, [])) == 1 else None)
                    if alias and any(alias == a for a, _ in sources):
                        renamed = exp.column(f"{alias}__{n.name}", quoted=True)
                        renamed.meta["swan_name"] = n.name
                        return renamed
                return n
            return node.transform(fix)

        conditions = [rename(c) for c in conditions]
        for cond in conditions:
            if _has_ai(cond):
                holder = exp.Paren(this=cond)
                frame, _ = self._evaluate(frame, holder)
                cond = holder.this
            self.register(FRAME, frame)
            frame = self.sql(exp.select("*").from_(FRAME).where(cond))

        rest = select.copy()
        rest.set("where", None)
        rest.set("joins", None)
        rest.set("from_", exp.From(this=exp.to_table(FRAME)))
        # output columns keep their SQL names (a CTE's reader refers to them): expand * and alias bare columns
        outputs = []
        for e in rest.expressions:
            if isinstance(e, exp.Star):
                outputs += [exp.column(c, table=a).as_(c) for a, t in sources for c in self.columns(t)]
            elif isinstance(e, exp.Column) and isinstance(e.this, exp.Star):
                outputs += [exp.column(c, table=e.table).as_(c) for a, t in sources if a == e.table
                            for c in self.columns(t)]
            elif isinstance(e, exp.Column):
                outputs.append(e.as_(e.name))
            else:
                outputs.append(e)
        rest.set("expressions", outputs)
        rest = rename(rest)
        for key in ("expressions", "group", "having", "order"):
            part = rest.args.get(key)
            nodes = part if isinstance(part, list) else [part] if part is not None else []
            for node in nodes:
                if _has_ai(node):
                    frame, _ = self._evaluate(frame, node)
        self.register(FRAME, frame)
        return self.sql(rest)

    def _evaluate(self, frame: pd.DataFrame, node: exp.Expression):
        """Evaluate every AI call in `node` on every row of `frame`; the call is replaced by its column."""
        for call in ai_calls(node):
            ctx = call.context.name
            values = frame[ctx].tolist() if ctx in frame.columns else []
            if call.fn == "ai_agg":
                present = [v for v in values if v is not None and v == v]
                answer = self.ops.agg(call, present) if present else None
                call.node.replace(exp.Max(this=exp.convert(answer)))
                continue
            idx = [i for i, v in enumerate(values) if v is not None and v == v]
            present = [values[i] for i in idx]
            if not present:
                answers = []
            elif call.fn == "ai_filter":
                answers = self.ops.filter(call, present)
            elif call.fn == "ai_complete":
                answers = self.ops.complete(call, present)
            else:
                labels = call.labels if call.labels is not None else [
                    r[0] for r in self.con.execute(
                        f"SELECT DISTINCT {_q(call.labels_from[1])} FROM {_q(call.labels_from[0])} "
                        f"WHERE {_q(call.labels_from[1])} IS NOT NULL ORDER BY 1")]
                answers = self.ops.classify(call, present, labels)
            column = [None] * len(values)
            for i, a in zip(idx, answers):
                column[i] = (1 if a else 0) if call.fn == "ai_filter" else a
            name = self._name("ai")
            frame = frame.copy()
            frame[name] = column
            call.node.replace(exp.column(name, quoted=True))
        return frame, node


def _conjuncts(node: exp.Expression) -> list[exp.Expression]:
    if isinstance(node, exp.And):
        return _conjuncts(node.this) + _conjuncts(node.expression)
    if isinstance(node, exp.Paren) and isinstance(node.this, exp.And):
        return _conjuncts(node.this)
    return [node]
