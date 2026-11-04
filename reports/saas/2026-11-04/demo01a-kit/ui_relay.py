"""Bounded private WebUI relay. Docker exec has a fixed destination and no shell."""
import os
import select
import socketserver
import subprocess
import threading
import time


def serve(terminal, port, deadline, available_memory):
    slots = threading.BoundedSemaphore(12)

    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            if not slots.acquire(blocking=False):
                return
            try:
                with subprocess.Popen(
                    ["docker", "exec", "-i", terminal, "socat", "STDIO", "TCP:127.0.0.1:8080"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                ) as relay:
                    try:
                        self.request.settimeout(5)
                        end = min(deadline, time.monotonic() + 900)
                        while time.monotonic() < end:
                            ready, _, _ = select.select([self.request, relay.stdout], [], [], 2)
                            for source in ready:
                                data = (self.request.recv(65536) if source is self.request
                                        else os.read(relay.stdout.fileno(), 65536))
                                if not data:
                                    return
                                if source is self.request:
                                    relay.stdin.write(data)
                                    relay.stdin.flush()
                                else:
                                    self.request.sendall(data)
                    finally:
                        if relay.poll() is None:
                            relay.kill()
            except OSError:
                pass
            finally:
                slots.release()

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    with Server(("127.0.0.1", port), Handler) as server:
        server.timeout = 0.5
        next_check = 0
        while time.monotonic() < deadline:
            if time.monotonic() >= next_check:
                if available_memory() < 1024**2:
                    print("Arrêt du laboratoire pour préserver la réserve mémoire.", flush=True)
                    return
                next_check = time.monotonic() + 10
            server.handle_request()
