# Queries

One query per question and system: `queries/<system>/<qid>.sql` (or `.py` for LOTUS). Every query runs on
the **masked** database, where the columns in `data/masked_columns.json` do not exist, so the LLM is the only
way to the hidden values. `swan-bench run --system <system>` runs them and scores them against the gold query
on the original database.

| directory | system | written for |
|---|---|---|
| `blendsql/` | [BlendSQL](https://github.com/parkervg/blendsql) 0.1.x | the reference: the 2024 queries, translated (docs/CHANGES.md) |
| `blendsql_2024/` | BlendSQL 0.0.x | the 2024 queries verbatim, kept for provenance; not run |
| `aisql/` | [SWAN-AISQL](https://github.com/) (DuckDB + `aisql` extension) | ports of the BlendSQL queries |
| `lotus/` | [LOTUS](https://github.com/lotus-data/lotus) 1.2.x | ports of the BlendSQL queries |

## How the SWAN-AISQL and LOTUS queries were written

The comparison is between systems, not between prompts. So each SWAN-AISQL and LOTUS query is a port of
the BlendSQL query for the same question:

- **Same LLM work.** Each BlendSQL `LLMMap` or `LLMQA` becomes one AI call of the other system, over the
  same rows, with the same question text (verbatim, typos included) and the same context value.
- **Same relational logic.** Joins, filters, grouping, ordering and limits follow the BlendSQL query.
  Where BlendSQL filters rows before the LLM call, the port does too.
- **Prompt layout.** The question, a space, then the context as `<name>: <value>`, where `<name>` is the
  BlendSQL context column's name. For example `Does the hero has blue eye? superhero_name: 3-D Man`.
- **Options.** A BlendSQL `options=` list becomes the label list of `ai_classify` (SWAN-AISQL) or, since
  LOTUS has no label argument, the sentence ` Answer with exactly one of: A, B, C.` at the end of the
  prompt (LOTUS). Options taken from a column use its distinct values, sorted.
- **Value answers.** BlendSQL's own prompt for a value asks for the bare answer, without commentary. Both
  ports append the equivalent instruction to every call that returns a value (`ai_complete`/`ai_agg`,
  `sem_map`/`sem_agg`) and carries no options: ` Answer with the number only.` where the answer must become
  a number, ` Answer with the date only, in YYYY-MM-DD format.` for a date, and
  ` Answer with the value only, without any other words.` otherwise.

### SWAN-AISQL mapping

| BlendSQL | SWAN-AISQL |
|---|---|
| `{{LLMMap('q', t.c)}} = TRUE` | `ai_filter('q c: ' \|\| t.c)` |
| `{{LLMMap('q', t.c, options=(...))}}` | `ai_classify('q c: ' \|\| t.c, ['A', 'B'])` |
| `{{LLMMap('q', t.c)}}` (a value) | `ai_complete('q c: ' \|\| t.c)`, `TRY_CAST(... AS DOUBLE)` for numbers |
| `{{LLMQA('q', (SELECT ...))}}` | `ai_agg(list(<row as text>), 'q')` over the same rows |

SWAN-AISQL is DuckDB SQL, not sqlite, so the BlendSQL logic is translated to keep sqlite's meaning:
double quotes instead of backticks, `//` for sqlite integer division, `DOUBLE` instead of `REAL` in casts,
`ILIKE` for sqlite's case-insensitive `LIKE`, `NULLS FIRST` where an ascending sort meets NULLs, and
`any_value()` for sqlite's bare columns in a GROUP BY.

### LOTUS mapping

A LOTUS query is a Python file with `run(db)`. `db.table(name)` loads a masked table as a DataFrame;
`db.sql(query, **frames)` runs relational SQL on the masked database with DataFrames as extra tables. The
relational steps may use either; every LLM call is a LOTUS operator:

| BlendSQL | LOTUS |
|---|---|
| `{{LLMMap('q', t.c)}} = TRUE` | `df.sem_filter("q c: {c}")` |
| `{{LLMMap('q', t.c, options=(...))}}` | `df.sem_map("q c: {c} Answer with exactly one of: A, B.", suffix="x")` |
| `{{LLMMap('q', t.c)}}` (a value) | `df.sem_map("q c: {c}", suffix="x")` |
| `{{LLMQA('q', (SELECT ...))}}` | `df.sem_agg("q {c}")` over the same rows |

LOTUS runs an operator once per DataFrame row, so where BlendSQL maps a column's distinct values, the port
maps the distinct values too (`drop_duplicates`) and merges the answers back.
