#!/usr/bin/env bash
# Shared steps for scripts/run_{swan_aisql,blendsql,lotus}.sh. Source it; do not run it.
#
# Environment variables (all optional):
#   SWAN_AISQL_DIR       the SWAN-AISQL checkout (default: ../SWAN-AISQL next to this repository; cloned if missing)
#   SWAN_BENCH_ENDPOINT  the model endpoint (default http://localhost:4001, the SWAN-AISQL cache proxy, which
#                        records and replays answers). http://localhost:4000 is litellm alone (no recording). Both
#                        are started here. Any other OpenAI-compatible gateway is used as is; it must accept each
#                        system's request parameters, as litellm does (OpenAI itself rejects some of them).
#   SWAN_AISQL_DUCKDB    a SWAN-AISQL binary to use instead of building one
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SWAN_AISQL_DIR="${SWAN_AISQL_DIR:-$(cd "$ROOT/.." && pwd)/SWAN-AISQL}"
SWAN_AISQL_REPO="https://github.com/ZhaoFuheng/SWAN-AISQL"
export SWAN_BENCH_ENDPOINT="${SWAN_BENCH_ENDPOINT:-http://localhost:4001}"
unset VIRTUAL_ENV  # an activated environment elsewhere would confuse uv

say() { printf '\n==> %s\n' "$*"; }

# --stub anywhere in the arguments: no model, no key, no servers
is_stub() { for a in "$@"; do [ "$a" = "--stub" ] && return 0; done; return 1; }
uses_proxy() { [[ "$SWAN_BENCH_ENDPOINT" =~ ^http://(localhost|127\.0\.0\.1):400[01](/|$) ]]; }  # the local stack

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1 ($2)" >&2; exit 1; }; }

load_key() {
	if [ -f "$ROOT/.env" ]; then set -a; . "$ROOT/.env"; set +a; fi
	if [ -z "${OPENAI_API_KEY:-}" ]; then
		echo "OPENAI_API_KEY is not set: copy .env.example to .env and put your key there" >&2
		exit 1
	fi
}

setup_bench() {  # setup_bench <extra>...
	need uv "https://docs.astral.sh/uv/"
	local flags=() e
	for e in "$@"; do flags+=(--extra "$e"); done
	say "Python environment (uv sync --inexact ${flags[*]:-})"
	(cd "$ROOT" && uv sync --inexact ${flags[@]+"${flags[@]}"})  # --inexact: keep the other systems installed
	say "Databases (swan-bench prepare)"
	(cd "$ROOT" && uv run swan-bench prepare)
}

clone_swan_aisql() {
	if [ ! -d "$SWAN_AISQL_DIR/.git" ]; then
		need git "https://git-scm.com"
		say "Cloning SWAN-AISQL into $SWAN_AISQL_DIR"
		git clone --recurse-submodules "$SWAN_AISQL_REPO" "$SWAN_AISQL_DIR"
	fi
}

build_swan_aisql() {
	if [ -n "${SWAN_AISQL_DUCKDB:-}" ] && [ -x "$SWAN_AISQL_DUCKDB" ]; then
		say "SWAN-AISQL binary: $SWAN_AISQL_DUCKDB"
		return
	fi
	clone_swan_aisql
	local bin="$SWAN_AISQL_DIR/build/release/duckdb"
	if [ ! -x "$bin" ]; then
		need cmake "brew install cmake / apt install cmake"
		need ninja "brew install ninja / apt install ninja-build"
		say "Building SWAN-AISQL (about 25 minutes, once)"
		(cd "$SWAN_AISQL_DIR" && git submodule update --init --recursive && GEN=ninja make release)
	fi
	export SWAN_AISQL_DUCKDB="$bin"
	say "SWAN-AISQL binary: $SWAN_AISQL_DUCKDB"
}

serving_env() {  # SWAN-AISQL's own Python environment for litellm, the cache proxy and the embedding server
	clone_swan_aisql
	if [ ! -x "$SWAN_AISQL_DIR/.venv/bin/python" ]; then
		say "SWAN-AISQL serving environment"
		(cd "$SWAN_AISQL_DIR" && uv venv --python 3.12 .venv \
			&& uv pip install --python .venv/bin/python -r requirements.txt -r requirements-embed-st.txt)
	fi
}

wait_for() {  # wait_for <url> <what> <seconds>
	local i
	for ((i = 0; i < $3; i += 2)); do
		curl -sf -m 2 "$1" >/dev/null 2>&1 && return 0
		sleep 2
	done
	echo "$2 did not come up at $1 -- see the logs in $SWAN_AISQL_DIR/serve/" >&2
	exit 1
}

start_servers() {  # start_servers embed|no-embed
	serving_env
	local py="$SWAN_AISQL_DIR/.venv/bin/python"
	if uses_proxy; then
		say "Serving stack: litellm :4000, cache proxy :4001$([ "$1" = embed ] && echo ', embedding server :4002')"
		(export PATH="$SWAN_AISQL_DIR/.venv/bin:$PATH" PYTHON="$py" OPENAI_API_KEY
		 cd "$SWAN_AISQL_DIR" && serve/start_stack.sh $([ "$1" = embed ] || echo --no-embed) >/dev/null)
		wait_for http://127.0.0.1:4000/health/liveliness "litellm" 120
		wait_for http://127.0.0.1:4001/cache/stats "the cache proxy" 60
	elif [ "$1" = embed ] && ! curl -sf -m 2 http://127.0.0.1:4002/ >/dev/null 2>&1; then
		say "Embedding server :4002"
		(cd "$SWAN_AISQL_DIR/serve" && nohup "$py" ai_embed_server.py > embed.log 2>&1 &)
	fi
	if [ "$1" = embed ]; then
		# the first start downloads its models (~1.2 GB)
		wait_for http://127.0.0.1:4002/ "the embedding server" 900
	fi
}

run_system() {  # run_system <system> <args to swan-bench run>...
	local system="$1"; shift
	say "swan-bench run --system $system $*   (endpoint: $SWAN_BENCH_ENDPOINT)"
	(cd "$ROOT" && uv run swan-bench run --system "$system" "$@")
	say "Done. Results: runs/$system/. Compare systems with: uv run swan-bench report"
	if ! is_stub "$@" && uses_proxy; then
		echo "Servers keep running. Stop them with:"
		echo "  pkill -f ai_cache_server.py; pkill -f 'litellm --config'; pkill -f ai_embed_server.py"
	fi
}
