"""A local forwarder that meters the LLM traffic of the system under test.

Every system talks to an OpenAI-compatible endpoint. The runner points the system at a `Meter` instead,
which forwards each request to the real endpoint and counts it the same way for every system: requests,
tokens (from the response's `usage`) and cost (from litellm's `x-litellm-response-cost` header, which the
SWAN-AISQL cache proxy replays on a cache hit). A streamed response carries no cost header: its cost is
priced from the token usage in its last chunk with `PRICES`, which are litellm's prices. The runner reads and
resets the counters around each query.

With `upstream=None` the meter answers every chat request itself with a deterministic 'True' or 'False'.
That checks that a system's queries parse and run without any model.
"""

import hashlib
import json
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

COST_HEADER = "x-litellm-response-cost"
_DROP_REQUEST_HEADERS = {"host", "content-length", "connection", "accept-encoding"}
_KEEP_RESPONSE_HEADERS = ("Content-Type", COST_HEADER)

#: USD per token: (input, cached input, output), as in litellm's model cost map
PRICES = {"gpt-5.6-luna": (2e-07, 2e-08, 1.2e-06)}

COUNTERS = ("requests", "errors", "prompt_tokens", "completion_tokens", "reasoning_tokens", "cost_usd")


def _stub_completion(body: dict, responder=None) -> dict:
    text = json.dumps(body.get("messages", ""), sort_keys=True)
    answer = "True" if hashlib.sha256(text.encode()).digest()[0] % 2 == 0 else "False"
    if responder is not None:
        answer = responder(body)
    return {
        "id": "stub", "object": "chat.completion", "created": int(time.time()), "model": body.get("model", "stub"),
        "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": answer}}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


def _as_stream(completion: dict) -> bytes:
    """A completion as server-sent events, for clients that ask for a stream (BlendSQL)."""
    base = {k: completion[k] for k in ("id", "created", "model")} | {"object": "chat.completion.chunk"}
    content = completion["choices"][0]["message"]["content"]
    chunks = [base | {"choices": [{"index": 0, "delta": {"role": "assistant", "content": content}}]},
              base | {"choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]},
              base | {"choices": [], "usage": completion["usage"]}]
    return b"".join(b"data: " + json.dumps(c).encode() + b"\n\n" for c in chunks) + b"data: [DONE]\n\n"


class _Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 1024  # the listen backlog: a system may open hundreds of connections at once


class Meter:
    def __init__(self, upstream: str | None, timeout: float = 900.0, responder=None):
        """`responder(body) -> content`: with no upstream, answers chat requests (e.g. the shadow model);
        without one, the stub answers 'True' or 'False'."""
        self.upstream = upstream.rstrip("/") if upstream else None
        self.responder = responder
        self.timeout = timeout
        self._lock = threading.Lock()
        self._counts = dict.fromkeys(COUNTERS, 0)
        self._server = _Server(("127.0.0.1", 0), self._handler())
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self._server.server_address[1]}"

    def __enter__(self) -> "Meter":
        self._thread.start()
        return self

    def __exit__(self, *exc) -> None:
        self._server.shutdown()
        self._server.server_close()

    def reset(self) -> None:
        with self._lock:
            self._counts = dict.fromkeys(COUNTERS, 0)

    def snapshot(self) -> dict:
        with self._lock:
            counts = dict(self._counts)
        counts["cost_usd"] = round(counts["cost_usd"], 6)
        return counts

    def upstream_misses(self) -> int | None:
        """Cache misses so far at the upstream, when it is the SWAN-AISQL cache proxy (else None)."""
        if not self.upstream:
            return None
        try:
            with urllib.request.urlopen(self.upstream + "/cache/stats", timeout=10) as r:
                return int(json.load(r)["misses"])
        except Exception:  # noqa: BLE001 -- not a cache proxy
            return None

    @staticmethod
    def usage_of(body: bytes) -> dict:
        """The `usage` of a chat completion, or of a streamed one (server-sent events; usage in the last chunk)."""
        text = body.decode("utf-8", "replace").lstrip()
        if text.startswith("data:"):
            usage = {}
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("data:") and line[5:].strip() not in ("", "[DONE]"):
                    try:
                        usage = json.loads(line[5:]).get("usage") or usage
                    except (ValueError, AttributeError):
                        pass
            return usage
        try:
            return json.loads(text).get("usage") or {}
        except (ValueError, AttributeError):
            return {}

    @staticmethod
    def price(model: str, usage: dict) -> float:
        prices = PRICES.get(model.split("/")[-1])
        if not prices:
            return 0.0
        cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
        prompt = usage.get("prompt_tokens") or 0
        return ((prompt - cached) * prices[0] + cached * prices[1]
                + (usage.get("completion_tokens") or 0) * prices[2])

    def _record(self, status: int, body: bytes, headers: dict, model: str) -> None:
        usage = self.usage_of(body)
        details = usage.get("completion_tokens_details") or {}
        cost = headers.get(COST_HEADER)
        if not cost and 200 <= status < 300:
            cost = self.price(model, usage)
        with self._lock:
            self._counts["requests"] += 1
            if not 200 <= status < 300:
                self._counts["errors"] += 1
                return
            self._counts["prompt_tokens"] += usage.get("prompt_tokens") or 0
            self._counts["completion_tokens"] += usage.get("completion_tokens") or 0
            self._counts["reasoning_tokens"] += details.get("reasoning_tokens") or 0
            try:
                self._counts["cost_usd"] += float(cost) if cost else 0.0
            except ValueError:
                pass

    def _handler(self):
        meter = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _reply(self, status: int, body: bytes, headers: dict) -> None:
                self.send_response(status)
                for k, v in headers.items():
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(body)))
                try:
                    self.end_headers()
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass  # the client gave up on this request (e.g. SWAN-AISQL's hedged duplicate lost the race)

            def _forward(self, method: str, raw: bytes | None):
                req = urllib.request.Request(meter.upstream + self.path, data=raw, method=method)
                for k, v in self.headers.items():
                    if k.lower() not in _DROP_REQUEST_HEADERS:
                        req.add_header(k, v)
                try:
                    with urllib.request.urlopen(req, timeout=meter.timeout) as r:
                        return r.status, r.read(), dict(r.headers.items())
                except urllib.error.HTTPError as e:
                    return e.code, e.read(), dict((e.headers or {}).items())
                except Exception as e:  # noqa: BLE001 -- upstream unreachable
                    return 502, json.dumps({"error": {"message": f"meter: {e}"}}).encode(), {}

            def do_GET(self):
                if meter.upstream is None:
                    return self._reply(404, b"{}", {"Content-Type": "application/json"})
                status, body, headers = self._forward("GET", None)
                self._reply(status, body, {k: headers[k] for k in _KEEP_RESPONSE_HEADERS if k in headers})

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                if meter.upstream is None:
                    request = json.loads(raw or b"{}")
                    try:
                        completion = _stub_completion(request, meter.responder)
                    except Exception as ex:  # noqa: BLE001 -- a responder bug is an HTTP 500, not a dead thread
                        error = json.dumps({"error": {"message": f"responder: {type(ex).__name__}: {ex}"}}).encode()
                        return self._reply(500, error, {"Content-Type": "application/json"})
                    if request.get("stream"):
                        body, headers = _as_stream(completion), {"Content-Type": "text/event-stream"}
                    else:
                        body, headers = json.dumps(completion).encode(), {"Content-Type": "application/json"}
                    status = 200
                else:
                    status, body, headers = self._forward("POST", raw)
                    headers = {k: headers[k] for k in _KEEP_RESPONSE_HEADERS if k in headers}
                if self.path.endswith("/chat/completions"):
                    try:
                        model = json.loads(raw or b"{}").get("model") or ""
                    except ValueError:
                        model = ""
                    meter._record(status, body, headers, model)
                self._reply(status, body, headers)

        return Handler
