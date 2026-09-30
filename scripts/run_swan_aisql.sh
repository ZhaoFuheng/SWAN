#!/usr/bin/env bash
# Run SWAN-AISQL on SWAN 2.0, from a fresh clone:
#   1. the benchmark environment and databases;
#   2. SWAN-AISQL: clone next to this repository and build its binary (once, about 25 minutes);
#   3. the serving stack: litellm, the cache proxy and the embedding server, which SWAN-AISQL's filter ordering needs;
#   4. every question (or the ones you pass).
# Arguments go to `swan-bench run`, e.g.:  scripts/run_swan_aisql.sh --qid superhero-05     or  --stub
. "$(dirname "$0")/common.sh"
setup_bench
build_swan_aisql
if ! is_stub "$@"; then
	load_key
	start_servers embed
fi
run_system aisql "$@"
