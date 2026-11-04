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

    def test_single_and_parallel_calls(self):
        def call(index, name):
            return {"index": index, "id": f"call_{index}", "type": "function",
                    "function": {"name": name, "arguments": "{}"}}

        upstream = {"max_tokens": 64, "tools": [{"function": {"name": name}} for name in ("one", "two")]}
        for calls in ([call(0, "one")], [call(1.0, "two") | {"id": "call_1"}, call(0, "one")]):
            response = self.parse([chunk({"tool_calls": calls}, "tool_calls"), USAGE])
            relay.validate_response(response, upstream, 100)
            self.assertEqual([c["id"] for c in response["choices"][0]["message"]["tool_calls"]],
                             [f"call_{i}" for i in range(len(calls))])

    def test_tool_structure_diagnostics(self):
        base = {"index": 0, "id": "fixture", "type": "function",
                "function": {"name": "execute", "arguments": '{"private":'}}
        fixtures = [
            (42, "tool_fragment_not_object"),
            ({k: v for k, v in base.items() if k != "index"}, "tool_index_missing_or_invalid"),
            (dict(base, index=0.5), "tool_index_missing_or_invalid"),
            (dict(base, type="other"), "tool_type_invalid"),
            (dict(base, id=[]), "tool_id_invalid_or_conflicting"),
            (dict(base, function=[]), "tool_function_invalid"),
            (dict(base, function={"name": 1}), "tool_name_fragment_invalid"),
            (dict(base, function={"arguments": {}}), "tool_arguments_fragment_invalid"),
        ]
        for fragment, code in fixtures:
            with self.subTest(code=code), self.assertRaises(relay.UpstreamError) as error:
                self.parse([chunk({"tool_calls": [fragment]}, "tool_calls"), USAGE])
            self.assertEqual(error.exception.fields["tool_subcode"], code)

        response = self.parse([chunk({"tool_calls": [base]}, "tool_calls"), USAGE])
        for names, code in [([], "tool_name_not_allowed"), (["execute"], "tool_arguments_json_invalid")]:
            with self.subTest(code=code), self.assertRaises(relay.UpstreamError) as error:
                relay.validate_response(response, {"max_tokens": 64,
                                        "tools": [{"function": {"name": n}} for n in names]}, 100)
            self.assertEqual(error.exception.fields["tool_subcode"], code)
            self.assertNotIn("private", str(error.exception.fields))

    def test_interruption_and_model_mismatch(self):
        with self.assertRaises(relay.UpstreamError) as error:
            self.parse(OPERATOR_SHAPE, done=False)
        self.assertEqual(error.exception.fields["category"], "stream_missing_done")
        with self.assertRaises(relay.UpstreamError) as error:
            self.parse([dict(OPERATOR_SHAPE[0], model="another-model"), USAGE])
        self.assertEqual(error.exception.fields["category"], "incompatible_model")
