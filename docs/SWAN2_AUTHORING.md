# Writing SWAN 2.0 questions

Each SWAN 2.0 question is rewritten from the SWAN 1.x question with the same id, keeps its database and the
kind of hidden value it needs, and is reshaped so that a query engine has something to plan
(docs/SWAN2_DESIGN.md). A question has four parts:

| part | where | runs on |
|---|---|---|
| question, evidence, difficulty, shape | a row of `data/questions/<db>.csv` | |
| gold query | the row's `gold_sql` | the SWAN 2.0 original database, `data/databases/original/<db>/<db>.sqlite` (sqlite) |
| AISQL query | `queries/aisql/<qid>.sql` | the masked database; every system runs it |
| oracle query | `queries/oracle/<qid>.sql` | the original database (sqlite): the AISQL query with each AI call replaced by the hidden column it stands for |

## The AISQL query

- Write it plainly, the way a user states the question: conditions in the order the question gives them, no
  hand deduplication, no hand reordering for speed. The engines do the planning.
- Every AI call is in the prompt form of `src/swan_bench/aisql.py` (`swan-bench lint` checks it):
  `ai_filter('Context:\n[<name>]: «' || <alias>.<name> || '»\n\n\nClaim: <question> <name>')` (the claim layout,
  written out; `\n` stands for a newline inside the string),
  `ai_complete('<question> <name>: ' || <alias>.<name> [|| '<suffix>'])`,
  `ai_classify(..., ['A', 'B'])` or `ai_classify(..., (SELECT list(DISTINCT c ORDER BY c) FROM t))`,
  `ai_agg(list(<alias>.<name>), '<instruction>')`. The context is one column; build a composite key in a CTE,
  e.g. `'Driver: ' || forename || ' ' || surname AS driver_key`, and name the key after what it holds: the
  engines show the model that name next to the value.
- The context must let a knowledgeable model answer: a name, a title, a full address, a match with its
  teams and date. Never a bare id.
- A numeric claim must be decidable from public knowledge of the value: football heights are converted from
  inches (185.42 cm is "185 cm" everywhere), so write "at least 185 cm" (`>= 185`), not "taller than 185 cm".
- Only columns that exist in the masked database (`data/masked_columns.json` lists the removed ones). The
  mask hides every column that states a hidden fact outright, including `schools.Charter`, `FundingType`,
  `EdOpsName`/`EdOpsCode` and `SOCType`; `CharterNum` stays, although it is NULL for every non-charter
  school, and the county code inside `CDSCode` cannot be removed.
- A value the SQL then compares or computes with uses the matching suffix: ` Answer with the number only.`
  (then `TRY_CAST(... AS DOUBLE)`), ` Answer with the date only, in YYYY-MM-DD format.`, or
  ` Answer with the value only, without any other words.`
- DuckDB SQL that means the same in sqlite: double-quoted identifiers, `//` for integer division, `DOUBLE`
  not `REAL`, no correlated subqueries, AI calls only in INNER joins' ON. sqlglot translates the rest for
  BlendSQL and LOTUS; `swan-bench check` proves the translation kept the meaning.

## The gold and oracle queries

- The gold query answers the question on the original database with the true values. The oracle query is
  the AISQL query with each AI call replaced by the true hidden value (e.g. the filter whose claim is
  `Is the school in Alameda County?` becomes `schools.County = 'Alameda'`). Its result must equal the gold result: that
  proves the AISQL query is right when the model is right.
- **Answers are about entities, not rows.** The build gives entities copies (a new id, identical
  attributes), so a query must count and list entities: `COUNT(DISTINCT <natural key>)`, `SELECT DISTINCT`
  over natural attributes (never an id), averages over a `SELECT DISTINCT <natural key>, <value>` subquery,
  and top-N over distinct entities ordered by the value and then the natural key. The natural key is the
  smallest set of visible columns that identifies every original BIRD entity (e.g. a school's name and
  street, a driver's forename and surname); check its uniqueness on `data/databases/bird/`.
- The answer is deterministic: an ORDER BY ... LIMIT has a unique tie-breaker, in the gold, oracle and
  AISQL queries alike.
- The answer is small (under about 50 rows) and not empty, unless the question is about emptiness.
- **Any k** questions ("List any 5 ..."): the AISQL query ends with `LIMIT k` and has no ORDER BY; the gold
  query returns every valid row, without LIMIT. Any k valid rows score fully.

## Shapes, per database (30 questions)

| shape | count | what it asks of the engine |
|---|---|---|
| `plain` | 6 | nothing special, as in SWAN 1.x |
| `any_k` | 3 | LIMIT k without ORDER BY over an AI filter: stop after k passing rows |
| `top_n` | 3 | ORDER BY a plain column, LIMIT k, with an AI call in SELECT: map only the k rows |
| `multi_filter` | 5 | 3 to 4 AI filters joined by AND, some written least selective first |
| `boolean` | 2 | AI filters under OR / nested AND-OR |
| `cheap_after` | 3 | an AI filter written before a cheap, selective plain filter |
| `join_fanout` | 3 | an AI call on a dimension's attribute, evaluated through a join to many fact rows |
| `cte_reuse` | 2 | a CTE with an AI call, read twice |
| `case` | 2 | an AI call inside CASE WHEN <plain condition> |
| `distinct_exists` | 1 | DISTINCT or EXISTS over an AI-filtered join |

## Checks

```bash
uv run swan-bench lint --db <db>      # prompt form
uv run swan-bench check --db <db>     # every system gives identical results on the shadow model
uv run pytest -k oracle               # oracle == gold for every question
```
