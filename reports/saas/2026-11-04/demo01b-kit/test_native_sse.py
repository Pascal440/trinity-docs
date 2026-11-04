"""Local fixtures for Together native SSE. No network or provider key."""
from io import BytesIO
import json
import time
import unittest

import together_relay as relay


def fixture(events, done=True):
    data = b"".join(b"data: " + json.dumps(event).encode() + b"\n\n" for event in events)
    return BytesIO(data + (b"data: [DONE]\n\n" if done else b""))


def chunk(delta, finish=None):
    return {"id": "fixture", "model": relay.MODEL, "usage": None,
            "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}


USAGE = {"choices": [], "usage": {"prompt_tokens": 68, "completion_tokens": 36}}
OPERATOR_SHAPE = [
    chunk({"role": "assistant", "reasoning": "private fixture"}),
    chunk({"content": "connexion "}),
    chunk({"content": "OK"}, "stop"),
    USAGE,
]
TOOL_SHAPE = [
    chunk({"tool_calls": [{"index": 0, "id": "call_fixture", "type": "function",
                          "function": {"name": "exe", "arguments": '{"x":'}}]}),
    chunk({"tool_calls": [{"index": 0, "function": {"name": "cute", "arguments": "1}"}}]}, "tool_calls"),
    USAGE,
]


class NativeSSETests(unittest.TestCase):
    def parse(self, events, done=True):
        return relay.assemble_stream(relay.native_events(fixture(events, done), time.monotonic() + 5))

    def test_operator_shape(self):
        response = self.parse(OPERATOR_SHAPE)
        self.assertEqual(relay.validate_response(response, {"max_tokens": 64}, 100), USAGE["usage"])
        self.assertEqual(response["choices"][0]["message"]["content"], "connexion OK")
        self.assertNotIn(b"private fixture", relay.sse(response))

    def test_fragmented_tool(self):
        response = self.parse(TOOL_SHAPE)
        upstream = {"max_tokens": 64, "tools": [{"function": {"name": "execute"}}]}
        relay.validate_response(response, upstream, 100)
        event, done, _ = relay.sse(response).decode().split("\n\n")
        call = json.loads(event[6:])["choices"][0]["delta"]["tool_calls"][0]
        self.assertEqual(call["index"], 0)
        self.assertEqual(json.loads(call["function"]["arguments"]), {"x": 1})
        with self.assertRaises(relay.UpstreamError) as error:
            relay.validate_response(response, {"max_tokens": 64}, 100)
        self.assertEqual(error.exception.fields["category"], "incompatible_tool_calls")
        self.assertEqual(done, "data: [DONE]")

    def test_interruption_and_model_mismatch(self):
        with self.assertRaises(relay.UpstreamError) as error:
            self.parse(OPERATOR_SHAPE, done=False)
        self.assertEqual(error.exception.fields["category"], "stream_missing_done")
        with self.assertRaises(relay.UpstreamError) as error:
            self.parse([dict(OPERATOR_SHAPE[0], model="another-model"), USAGE])
        self.assertEqual(error.exception.fields["category"], "incompatible_model")
