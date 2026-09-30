# Queries

Every SWAN 2.0 question has two queries here:

| directory | what | runs on |
|---|---|---|
| `aisql/<qid>.sql` | the question's query, in DuckDB SQL with AI functions; **every system runs it** (BlendSQL and LOTUS through mechanical translations) | the masked database |
| `oracle/<qid>.sql` | the same query with each AI call replaced by the true hidden value; it returns the gold answer | the original database |

The rules for writing them are in `docs/SWAN2_AUTHORING.md`. `swan-bench lint` checks the prompt form, and
`swan-bench check` proves that the three systems run the same query.

The SWAN 1.x queries (one hand-written query per system) are in `swan1/queries/`.
