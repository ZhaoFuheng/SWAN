#!/usr/bin/env bash
# Run LOTUS on SWAN 2.0, from a fresh clone:
#   1. the benchmark environment (with LOTUS) and databases;
#   2. the serving stack from SWAN-AISQL (cloned next to this repository; no build): litellm and the cache proxy;
#   3. every question (or the ones you pass), each AISQL query run as its LOTUS program.
# Arguments go to `swan-bench run`, e.g.:  scripts/run_lotus.sh --qid superhero-05     or  --stub
. "$(dirname "$0")/common.sh"
setup_bench lotus
if ! is_stub "$@"; then
	load_key
	uses_proxy && start_servers no-embed
fi
run_system lotus "$@"
