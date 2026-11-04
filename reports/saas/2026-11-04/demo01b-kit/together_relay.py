"""One-shot, Unix-socket-only Together relay. Never log credentials or prompt content."""
import argparse
from decimal import Decimal
from http.client import HTTPException, HTTPSConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import ssl
import stat
import time

HOST = "api.together.xyz"
MODEL = "Qwen/Qwen3.8-Flash"
MAX_BODY = 256 * 1024
MAX_CONTEXT = 1_100_000
MAX_OUTPUT = 4096
MAX_CALLS = 8
INPUT_RATE = Decimal("0.15")
OUTPUT_RATE = Decimal("0.47")
RESERVE = (MAX_CONTEXT * INPUT_RATE + MAX_OUTPUT * OUTPUT_RATE) / 1_000_000
USD_CAP = Decimal("1.50")
EUR_CAP = Decimal("5")
MAX_RESPONSE = 2 * 1024**2


def read_private_file(path):
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), encoding="utf8") as file:
        info = os.fstat(file.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise ValueError("Secret hors périmètre privé.")
        return file.read(4097).strip()


def private_text(path):
    value = read_private_file(path)
    if not 20 <= len(value) <= 4096 or any(ord(c) < 33 or ord(c) > 126 for c in value):
        raise ValueError("Format de secret invalide.")
    return value


class UpstreamError(Exception):
    def __init__(self, category, status=None, kind=None, code=None):
        self.fields = {"category": category, "http_status": status,
                       "exception": kind or type(self).__name__, "provider_code": code}


SAFE_CODES = {
    "invalid_request_error", "authentication_error", "permission_error", "rate_limit_error",
    "server_error", "overloaded_error", "model_not_found", "invalid_api_key",
    "insufficient_quota", "insufficient_balance", "invalid_request", "not_found",
    "context_length_exceeded", "billing_error", "payment_required", "rate_limit_exceeded",
}


def provider_code(data):
    try:
        error = json.loads(data)["error"]
        for field in ("code", "type"):
            value = error.get(field)
            if isinstance(value, str) and value in SAFE_CODES:
                return value
    except (ValueError, TypeError, KeyError, AttributeError):
        pass
    return None


def request_upstream(key, method, path, body=None):
    connection = HTTPSConnection(HOST, timeout=60)
    status = None
    try:
        connection.request(method, path, body, {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        response = connection.getresponse()
        status = response.status
        data = response.read(MAX_RESPONSE + 1)
        if status != 200:
            raise UpstreamError("provider_http", status, code=provider_code(data))
        if len(data) > MAX_RESPONSE:
            raise UpstreamError("response_size", status)
        return json.loads(data)
    except ssl.SSLError as error:
        raise UpstreamError("tls", status, type(error).__name__) from None
    except TimeoutError as error:
        raise UpstreamError("timeout", status, type(error).__name__) from None
    except (OSError, HTTPException) as error:
        raise UpstreamError("connection", status, type(error).__name__) from None
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise UpstreamError("invalid_json", status, type(error).__name__) from None
    finally:
        connection.close()


def validate_response(response, upstream, context):
    if not isinstance(response, dict) or response.get("model") != MODEL:
        raise UpstreamError("incompatible_model", 200)
    usage = response.get("usage")
    if not isinstance(usage, dict) or any(
        type(usage.get(name)) is not int or not 0 <= usage[name] <= limit
        for name, limit in (("prompt_tokens", context), ("completion_tokens", upstream["max_tokens"]))
    ):
        raise UpstreamError("incompatible_usage", 200)
    choices = response.get("choices")
    if (not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict)
            or not isinstance(response.get("id"), str)):
        raise UpstreamError("incompatible_choices", 200)
    choice = choices[0]
    message = choice.get("message")
    if (not isinstance(message, dict) or message.get("role") != "assistant"
            or not isinstance(choice.get("finish_reason"), str)
            or (message.get("content") is not None and not isinstance(message["content"], str))):
        raise UpstreamError("incompatible_message", 200)
    calls = message.get("tool_calls")
    if calls is not None:
        names = [tool["function"].get("name") for tool in upstream.get("tools", [])]
        if not isinstance(calls, list) or any(
            not isinstance(call, dict) or call.get("type") != "function"
            or not isinstance(call.get("id"), str) or not isinstance(call.get("function"), dict)
            or not isinstance(call["function"].get("name"), str) or call["function"]["name"] not in names
            or not isinstance(call["function"].get("arguments"), str)
            for call in calls
        ):
            raise UpstreamError("incompatible_tool_calls", 200)
    return usage


def completion(key, upstream, budget, context):
    start = time.monotonic()
    try:
        response = request_upstream(key, "POST", "/v1/chat/completions", json.dumps(upstream))
        usage = validate_response(response, upstream, context)
    except UpstreamError as error:
        budget.closed = True
        print(json.dumps({"call": budget.calls, "reserved_usd": str(budget.usd),
                          "seconds": round(time.monotonic()-start, 3), **error.fields}), flush=True)
        return None
    measured = (usage["prompt_tokens"] * INPUT_RATE + usage["completion_tokens"] * OUTPUT_RATE) / 1_000_000
    print(json.dumps({"call": budget.calls, "http_status": 200,
                      "prompt_tokens": usage["prompt_tokens"], "completion_tokens": usage["completion_tokens"],
                      "estimated_usd_ceiling": str(measured), "reserved_usd": str(budget.usd),
                      "seconds": round(time.monotonic()-start, 3)}), flush=True)
    return response


def sse(response):
    choice = response["choices"][0]
    delta = dict(choice["message"])
    if delta.get("tool_calls"):
        delta["tool_calls"] = [dict(call, index=index) for index, call in enumerate(delta["tool_calls"])]
    chunk = {"id": response["id"], "object": "chat.completion.chunk", "model": MODEL,
             "created": response.get("created", int(time.time())), "usage": response["usage"],
             "choices": [{"index": 0, "delta": delta, "finish_reason": choice["finish_reason"]}]}
    return ("data: " + json.dumps(chunk) + "\n\ndata: [DONE]\n\n").encode()


def approved_catalog(response):
    items = response if isinstance(response, list) else response.get("data", [])
    matches = [item for item in items if item.get("id") == MODEL]
    if len(matches) != 1:
        raise ValueError("Modèle exact absent du catalogue authentifié.")
    item = matches[0]
    pricing = item.get("pricing", {})
    if (item.get("type") != "chat"
            or not 0 < int(item.get("context_length", 0)) <= MAX_CONTEXT
            or not 0 < Decimal(str(pricing.get("input"))) <= INPUT_RATE
            or not 0 < Decimal(str(pricing.get("output"))) <= OUTPUT_RATE):
        raise ValueError("Contexte ou tarifs actifs non bornés.")
    return int(item["context_length"])


def normalize(payload):
    allowed = {"model", "messages", "tools", "tool_choice", "stream", "stream_options",
               "max_tokens", "temperature", "top_p", "stop", "n"}
    if not isinstance(payload, dict) or set(payload) - allowed or payload.get("model") != MODEL:
        raise ValueError("Paramètre ou modèle non autorisé.")
    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages or len(messages) > 64:
        raise ValueError("Messages invalides.")
    for message in messages:
        if not isinstance(message, dict) or set(message) - {"role", "content", "name", "tool_calls", "tool_call_id"}:
            raise ValueError("Message non autorisé.")
        if message.get("role") not in {"user", "assistant", "tool", "system", "developer"}:
            raise ValueError("Rôle non autorisé.")
        if message.get("content") is not None and not isinstance(message["content"], str):
            raise ValueError("Contenu non textuel.")
    tools = payload.get("tools", [])
    if not isinstance(tools, list) or any(
        not isinstance(tool, dict) or set(tool) != {"type", "function"}
        or tool["type"] != "function" or not isinstance(tool["function"], dict)
        for tool in tools
    ):
        raise ValueError("Seuls les outils de fonction locale sont admis.")
    if payload.get("n", 1) != 1 or payload.get("stream", False) not in (False, True):
        raise ValueError("Options de génération invalides.")
    output = payload.get("max_tokens", MAX_OUTPUT)
    if type(output) is not int or not 0 < output <= MAX_OUTPUT:
        raise ValueError("Plafond de sortie dépassé.")
    upstream = dict(payload, max_tokens=output, stream=False, n=1)
    upstream.pop("stream_options", None)
    return upstream


class Budget:
    def __init__(self, eur_per_usd_inclusive, prior_calls=0):
        if not eur_per_usd_inclusive.is_finite() or not 0 < eur_per_usd_inclusive <= Decimal("3"):
            raise ValueError("Borne EUR/USD frais et taxes inclus non confirmée.")
        self.calls = prior_calls
        self.usd = RESERVE * prior_calls
        self.factor = eur_per_usd_inclusive
        self.closed = False

    def reserve(self):
        if (self.closed or self.calls >= MAX_CALLS or self.usd + RESERVE > USD_CAP
                or (self.usd + RESERVE) * self.factor >= EUR_CAP):
            raise ValueError("Budget ou nombre d’appels atteint.")
        self.calls += 1
        self.usd += RESERVE


class UnixServer(HTTPServer):
    address_family = socket.AF_UNIX

    def server_bind(self):
        self.socket.bind(self.server_address)
        self.server_name = "demo01b"
        self.server_port = 0

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(10)
        return connection, address


def handler(key, local_token, budget, context, deadline):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def reply(self, code, data, content_type="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def json_reply(self, code, data):
            self.reply(code, json.dumps(data).encode())

        def authorized(self):
            if time.monotonic() >= deadline or budget.closed:
                self.json_reply(503, {"error": "session fermée"})
                return False
            if not secrets.compare_digest(self.headers.get("Authorization", ""), "Bearer " + local_token):
                self.json_reply(401, {"error": "accès refusé"})
                return False
            return True

        def do_GET(self):
            if not self.authorized():
                return
            if self.path != "/v1/models":
                self.json_reply(404, {"error": "route refusée"})
                return
            self.json_reply(200, {"object": "list", "data": [{"id": MODEL, "object": "model"}]})

        def do_POST(self):
            if not self.authorized():
                return
            if self.path != "/v1/chat/completions":
                self.json_reply(404, {"error": "route refusée"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if self.headers.get("Transfer-Encoding") or not 0 < length <= MAX_BODY:
                    raise ValueError("Corps hors limite.")
                payload = json.loads(self.rfile.read(length))
                upstream = normalize(payload)
                budget.reserve()
            except (ValueError, TypeError):
                self.json_reply(400, {"error": "requête ou budget refusé"})
                return
            response = completion(key, upstream, budget, context)
            if response is None:
                self.json_reply(502, {"error": "fournisseur non qualifié, session fermée"})
                return
            if payload.get("stream"):
                self.reply(200, sse(response), "text/event-stream")
            else:
                self.json_reply(200, response)
    return Handler


def write_marker(path, text):
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as record:
        record.write(text + "\n")
        record.flush()
        os.fsync(record.fileno())


def resume_budget(args):
    if args.budget_lock.name != "budget.lock" or not args.budget_lock.is_absolute():
        raise ValueError("Verrou historique requis.")
    if read_private_file(args.budget_lock) != "One DEMO-01B session reserved. No credential or prompt.":
        raise ValueError("Verrou historique inattendu.")
    return Budget(args.eur_per_usd_inclusive, 1 if args.probe else 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key-file", required=True, type=Path)
    parser.add_argument("--local-token-file", type=Path)
    parser.add_argument("--socket", type=Path)
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--eur-per-usd-inclusive", required=True, type=Decimal)
    parser.add_argument("--budget-lock", required=True, type=Path)
    parser.add_argument("--confirm-one-session", action="store_true", required=True)
    args = parser.parse_args()
    if not args.probe and (not args.local_token_file or not args.socket or not args.socket.is_absolute() or args.socket.parent.stat().st_mode & 0o007
            or not args.socket.parent.is_dir() or args.socket.exists()):
        parser.error("Socket neuve dans un répertoire privé requise.")
    try:
        budget = resume_budget(args)
        key = private_text(args.key_file)
        token = None if args.probe else private_text(args.local_token_file)
        context = approved_catalog(request_upstream(key, "GET", "/v1/models"))
    except Exception:
        raise SystemExit("Clé, catalogue ou budget non qualifiés. Aucune inférence.") from None
    probe_marker = args.budget_lock.with_name("budget.demo01b1.probe")
    pass_marker = args.budget_lock.with_name("budget.demo01b1.pass")
    try:
        if args.probe:
            upstream = normalize({"model": MODEL, "max_tokens": 64, "messages": [
                {"role": "user", "content": "Réponds uniquement : connexion OK"},
            ]})
            budget.reserve()
            write_marker(probe_marker, f"DEMO-01B.1 cumulative USD reserve {budget.usd}")
            response = completion(key, upstream, budget, context)
            if response is None:
                raise SystemExit(2)
            content = response["choices"][0]["message"].get("content") or ""
            if content.strip() != "connexion OK":
                print(json.dumps({"category": "probe_unexpected_text"}), flush=True)
                raise SystemExit(2)
            write_marker(pass_marker, "DEMO-01B.1 probe confirmed exact text and valid usage")
            print(json.dumps({"probe": "pass", "expected_text_matched": True}), flush=True)
            return
        if (read_private_file(probe_marker) != f"DEMO-01B.1 cumulative USD reserve {budget.usd}"
                or read_private_file(pass_marker) != "DEMO-01B.1 probe confirmed exact text and valid usage"):
            raise ValueError("Sonde réussie requise.")
        write_marker(args.budget_lock.with_name("budget.demo01b1.scenario"),
                     f"DEMO-01B.1 scenario starts with USD reserve {budget.usd}")
    except (OSError, ValueError):
        raise SystemExit("Autorisation de reprise absente ou déjà utilisée.") from None

    def stop(_signal, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    deadline = time.monotonic() + 1200
    bound = False
    try:
        with UnixServer(str(args.socket), handler(key, token, budget, context, deadline)) as server:
            bound = True
            args.socket.chmod(0o660)
            server.timeout = 0.5
            while time.monotonic() < deadline and not budget.closed and budget.calls < MAX_CALLS:
                server.handle_request()
    except KeyboardInterrupt:
        pass
    finally:
        if bound:
            args.socket.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
