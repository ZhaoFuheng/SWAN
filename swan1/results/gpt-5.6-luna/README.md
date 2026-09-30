# SWAN on gpt-5.6-luna (2026-09-29)

BlendSQL 0.1.27, LOTUS 1.2.4 and SWAN-AISQL (commit fa54914) on all 120 questions, 20 requests in flight each,
through the SWAN-AISQL cache proxy.

| database | BlendSQL | SWAN-AISQL | LOTUS |
|---|---|---|---|
| california_schools | 0.338 | 0.352 | 0.364 |
| superhero | 0.630 | 0.581 | 0.573 |
| formula_1 | 0.517 | 0.622 | 0.639 |
| european_football_2 | 0.398 | 0.375 | 0.344 |
| **quality (mean)** | **0.471** | **0.482** | **0.480** |
| exact match | 31/120 | 32/120 | 33/120 |
| LLM calls | 393,251 | 381,488 | 396,051 |
| cost | $45.73 | $43.27 | $42.61 |
| wall-clock, recorded | 34,068 s | 34,532 s | 34,784 s |

Quality and exact match are defined in the repository README.

Per system:

- `recording.jsonl` and `recording_scores.json` come from the run that called the model. Calls, cost and
  wall-clock are taken from it. All three systems recorded at the same time, against the same provider.
- `answers.jsonl` and `scores.json` come from a replay of that run from the proxy cache, which stores each
  full answer for scoring. Quality and exact match are taken from it.

BlendSQL fails formula_1-27 every time. The provider ends one of its streamed responses early, and BlendSQL
does not retry. That question scores 0.
