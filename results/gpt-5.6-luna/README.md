# SWAN 2.0 on gpt-5.6-luna (2026-10-03, one session)

The four systems ran all 120 questions fresh, one after the other, in a single session on 2026-10-03:
SWAN-AISQL (with `ai_filter` stating a one-sentence reason before its verdict), BlendSQL 0.1.27 zero-shot,
LOTUS 1.2.4, then PLOP (Morrila, DP cost-model mode, on the authors' fork). 20 requests in flight each, every
call through the SWAN-AISQL cache proxy with an empty recording cache. Quality, calls, cost and latency
therefore come from the same session and the same model load, and the latencies are comparable. The
session's recorded answers are published with SWAN-AISQL (its `serve/fetch_cache.sh`), so the run replays
with its answers, cost and latency and without a provider key.

| database | SWAN-AISQL | BlendSQL | LOTUS | PLOP-DP |
|---|---|---|---|---|
| california_schools | 0.700 | 0.777 | 0.704 | 0.679 |
| superhero | 0.503 | 0.488 | 0.499 | 0.521 |
| formula_1 | 0.995 | 0.975 | 0.998 | 0.902 |
| european_football_2 | 0.831 | 0.852 | 0.805 | 0.709 |
| **quality (mean)** | **0.757** | **0.773** | **0.751** | **0.703** |
| exact match | 60/120 | 57/120 | 56/120 | 51/120 |
| LLM calls | 22,398 | 59,564 | 69,211 | 25,645 |
| cost | $2.39 | $5.00 | $4.07 | ~$1.73 |
| latency, all 120 questions | 2,181 s | 4,367 s | 4,190 s | 10,264 s |
| latency, median question | 6.7 s | 8.7 s | 23.6 s | 40.9 s |
| fastest on | 43 questions | 63 | 11 | 3 |

Latency is the wall-clock time of a question from the system's start to its last row, model response times
included (`seconds` per question in `answers.jsonl`, summed per database in `scores.json`). BlendSQL's total
includes one question (european_football_2-22) that took 1,910 s at 27,258 calls; without it its total is
2,457 s. PLOP's cost is an estimate from its token counts (its requests carry no provider cost header); one
question (formula_1-02, an AI filter inside an `IN` subquery) fails in its optimizer and scores 0. Quality and exact match are defined in
the repository README. Per system, `answers.jsonl` holds each question's answer, calls, tokens, cost and
seconds, and `scores.json` the totals per database.

Run-to-run noise: the systems' previous runs (2026-10-01 to 10-03, not back to back) scored 0.775
(SWAN-AISQL), 0.741 (BlendSQL), 0.770 (LOTUS) and 0.739 (PLOP), and a same-setup SWAN-AISQL resample scored
0.729 against 0.750. gpt-5.6-luna at temperature 0 returns a different answer text for about 60% of repeated
prompts, and single-answer questions flip between runs, so mean-quality differences of about 0.02 to 0.03
are not meaningful: SWAN-AISQL, BlendSQL and LOTUS answer at the same quality, and calls, cost and latency
are the separation.
