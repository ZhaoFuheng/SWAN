# SWAN 1.x (release 0.3.0), archived

SWAN 2.0 replaced the 120 questions, their queries and the databases (docs/SWAN2_DESIGN.md). This folder
keeps SWAN 1.x as it was measured on 2026-09-29:

| path | contents |
|---|---|
| `questions.csv` | the 120 SWAN 1.x questions with their gold queries (on the full BIRD databases) |
| `queries/blendsql/` | the BlendSQL 0.1.x queries (the 2024 queries, translated; docs/CHANGES.md) |
| `queries/blendsql_2024/` | the 2024 BlendSQL 0.0.x queries, verbatim |
| `queries/lotus/`, `queries/aisql/` | hand ports of the BlendSQL queries to LOTUS and SWAN-AISQL (`queries/README.md`) |
| `results/gpt-5.6-luna/` | the three systems' answers and scores on gpt-5.6-luna |
| `table_keys.json` | database → table → the columns the 2024 prompts used to identify a row |
| `scripts/` | the one-off migration from the 2024 notebook layout (docs/CHANGES.md), kept as provenance |

The SWAN 1.x gold queries ran on the BIRD databases as shipped, which `swan-bench prepare` still unzips to
`data/databases/bird/`. The package's runner now runs SWAN 2.0; the 1.x runner is not kept.
