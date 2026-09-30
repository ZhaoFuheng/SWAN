"""The meter counts streamed and plain chat completions the same way."""

import json
import urllib.request

from swan_bench.meter import Meter


def test_streamed_usage_is_found_in_the_last_chunk():
    body = (b'data: {"choices":[{"delta":{"content":"x"}}]}\n\n'
            b'data: {"choices":[],"usage":{"prompt_tokens":100,"completion_tokens":10}}\n\ndata: [DONE]\n\n')
    assert Meter.usage_of(body) == {"prompt_tokens": 100, "completion_tokens": 10}
    assert Meter.usage_of(json.dumps({"usage": {"prompt_tokens": 3}}).encode()) == {"prompt_tokens": 3}


def test_price_uses_cached_input_rate():
    usage = {"prompt_tokens": 1000, "prompt_tokens_details": {"cached_tokens": 500}, "completion_tokens": 100}
    assert abs(Meter.price("openai/gpt-5.6-luna", usage) - (500 * 2e-07 + 500 * 2e-08 + 100 * 1.2e-06)) < 1e-12
    assert Meter.price("unknown-model", usage) == 0.0


def test_stub_meter_answers_and_counts():
    with Meter(None) as meter:
        req = urllib.request.Request(meter.url + "/v1/chat/completions", method="POST",
                                     data=json.dumps({"model": "m", "messages": [{"role": "user", "content": "hi"}]}).encode(),
                                     headers={"Content-Type": "application/json"})
        answer = json.load(urllib.request.urlopen(req))["choices"][0]["message"]["content"]
        assert answer in ("True", "False")
        assert meter.snapshot()["requests"] == 1
        meter.reset()
        assert meter.snapshot()["requests"] == 0
