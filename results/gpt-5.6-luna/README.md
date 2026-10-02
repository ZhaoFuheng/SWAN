# SWAN 2.0 on gpt-5.6-luna (2026-10-02)

SWAN-AISQL (2026-10-02, with `ai_filter` stating a one-sentence reason before its verdict), BlendSQL 0.1.27
zero-shot and LOTUS 1.2.4 on all 120 questions, 20 requests in flight each, through the SWAN-AISQL cache proxy.

| database | SWAN-AISQL | BlendSQL | LOTUS |
|---|---|---|---|
| california_schools | 0.749 | 0.679 | 0.752 |
| superhero | 0.466 | 0.506 | 0.508 |
| formula_1 | 0.995 | 0.981 | 0.983 |
| european_football_2 | 0.892 | 0.799 | 0.836 |
| **quality (mean)** | **0.775** | **0.741** | **0.770** |
| exact match | 64/120 | 51/120 | 59/120 |
| LLM calls | 23,135 | 59,462 | 69,478 |
| cost | $2.50 | $4.83 | $4.18 |

Quality and exact match are defined in the repository README. Per system, `answers.jsonl` holds each
question's answer, calls, tokens and cost, and `scores.json` the totals per database. Latency is not
reported: these runs replay recorded answers from the cache, and the recording runs of the three systems
overlapped, so their wall-clock times are not comparable.

Run-to-run noise: a second SWAN-AISQL run with an unchanged setup scored 0.729 against 0.750, so mean-quality
differences of about 0.02 are not meaningful; single-answer questions can flip between runs.
