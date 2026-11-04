"""Forward a lab Unix socket to a fixed loopback port, or the reverse."""
import argparse
import os
from pathlib import Path
import selectors
import socket
import socketserver
import threading
import time


class UnixListener(socketserver.ThreadingUnixStreamServer):
    daemon_threads = True


class LocalListener(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


def run(mode, path, port):
    slots = threading.BoundedSemaphore(12)

    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            if not slots.acquire(blocking=False):
                return
            family = socket.AF_UNIX if mode == "tcp-to-unix" else socket.AF_INET
            target = str(path) if family == socket.AF_UNIX else ("127.0.0.1", port)
            try:
                with socket.socket(family, socket.SOCK_STREAM) as upstream, selectors.DefaultSelector() as selector:
                    upstream.settimeout(10)
                    upstream.connect(target)
                    self.request.settimeout(10)
                    selector.register(upstream, selectors.EVENT_READ, self.request)
                    selector.register(self.request, selectors.EVENT_READ, upstream)
                    end = time.monotonic() + 1200
                    while time.monotonic() < end:
                        for key, _ in selector.select(timeout=1):
                            data = key.fileobj.recv(65536)
                            if data:
                                key.data.sendall(data)
                            else:
                                selector.unregister(key.fileobj)
                                key.data.shutdown(socket.SHUT_WR)
                        if not selector.get_map():
                            return
            except OSError:
                return
            finally:
                slots.release()

    if mode == "tcp-to-unix":
        with LocalListener(("127.0.0.1", port), Handler) as server:
            server.serve_forever()
    else:
        os.umask(0o117)
        with UnixListener(str(path), Handler) as server:
            try:
                server.serve_forever()
            finally:
                path.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["tcp-to-unix", "unix-to-tcp"])
    parser.add_argument("path", type=Path)
    parser.add_argument("port", type=int, choices=[8000, 8080, 18081, 18760])
    args = parser.parse_args()
    if not args.path.is_absolute():
        parser.error("Chemin absolu requis.")
    run(args.mode, args.path, args.port)
