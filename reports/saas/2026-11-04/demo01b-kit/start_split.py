"""Split the published offline lab into two network-none namespaces."""
import argparse
import json
import os
from pathlib import Path
import secrets
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time

import socket_bridge

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "demo01a-kit"))
from start import available_memory, docker, interrupt, preflight, prepare_demo

BRIDGE = (ROOT / "socket_bridge.py").read_text()


def bridge(container, python, mode, path, port):
    docker("exec", "-d", container, python, "-c", BRIDGE, mode, path, str(port))


def wait_socket(path):
    deadline = time.monotonic() + 15
    while not path.is_socket():
        if time.monotonic() >= deadline:
            raise RuntimeError("Socket de laboratoire indisponible.")
        time.sleep(0.1)


def model_fixture(listener):
    client, _ = listener.accept()
    with client:
        client.settimeout(5)
        with client.makefile("rb") as stream:
            while stream.readline() not in (b"\r\n", b""):
                pass
        client.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 7\r\nConnection: close\r\n\r\nfixture")


def check_model_boundary(webui, terminal, model_socket):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
        listener.bind(str(model_socket))
        os.chown(model_socket, 1000, 1000)
        model_socket.chmod(0o660)
        listener.listen(1)
        worker = threading.Thread(target=model_fixture, args=(listener,), daemon=True)
        worker.start()
        code = 'import urllib.request; print(urllib.request.urlopen("http://127.0.0.1:18081/v1/models",timeout=5).read().decode())'
        assert docker("exec", webui, "python", "-c", code).strip() == b"fixture"
        worker.join(timeout=5)
        print("Pont modèle vérifié depuis WebUI.", flush=True)
    model_socket.unlink()
    code = """
import pathlib, socket
assert not pathlib.Path('/run/demo-model').exists()
assert not pathlib.Path('/var/run/docker.sock').exists()
for endpoint in [('127.0.0.1', 18081), ('1.1.1.1', 443)]:
    with socket.socket() as client:
        client.settimeout(2)
        assert client.connect_ex(endpoint) != 0
"""
    docker("exec", terminal, "python3", "-c", code)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Vérifier avec une réponse Unix locale, sans fournisseur.")
    args = parser.parse_args()
    images = preflight()
    config = json.loads((ROOT.parent / "demo01a-kit/config.json").read_text())
    admin = secrets.token_urlsafe(24)
    demo = secrets.token_urlsafe(24)
    terminal_key = secrets.token_urlsafe(36)
    config["term_env"]["OPEN_TERMINAL_API_KEY"] = terminal_key
    config["web_env"].update(
        WEBUI_SECRET_KEY=secrets.token_urlsafe(40),
        WEBUI_ADMIN_EMAIL="demo01a-admin@example.test",
        WEBUI_ADMIN_PASSWORD=admin,
        TERMINAL_SERVER_CONNECTIONS=json.dumps([{
            "id": "demo01a", "name": "Atelier Boréal — Terminal", "url": "http://127.0.0.1:8000",
            "key": terminal_key, "enabled": True, "auth_type": "bearer", "path": "/openapi.json",
        }]),
    )
    common = ["run", "-d", "--pull", "never", "--label", "mission=demo01b", "--init",
              "--network", "none", "--read-only", "--user", "1000:1000", "--cap-drop", "ALL",
              "--security-opt", "no-new-privileges", "--cpus", "1", "--ulimit", "fsize=67108864:67108864",
              "--log-opt", "max-size=5m", "--log-opt", "max-file=2"]
    signal.signal(signal.SIGTERM, interrupt)
    session = Path(tempfile.mkdtemp(prefix="demo01b-", dir="/dev/shm"))
    containers = []
    ui = None
    try:
        os.chown(session, 1000, 1000)
        for name in ("terminal", "ui", "model"):
            directory = session / name
            directory.mkdir(mode=0o750)
            os.chown(directory, 1000, 1000)
        for name, values in config.items():
            path = session / name
            path.touch(mode=0o600)
            path.write_text("".join(f"{key}={value}\n" for key, value in values.items()))
        terminal = docker(*common, "--name", "demo01b-terminal", "--memory", "2g", "--memory-swap", "2g",
                          "--pids-limit", "512", "--shm-size", "256m",
                          "--tmpfs", "/home/user:rw,nosuid,nodev,size=512m,uid=1000,gid=1000,mode=0700",
                          "--tmpfs", "/tmp:rw,nosuid,nodev,size=256m,mode=1777",
                          "--mount", f"type=bind,src={session/'terminal'},dst=/run/demo-terminal",
                          "--env-file", str(session/"term_env"), "--entrypoint", "sh",
                          images["terminal"]["reference"], "-c",
                          "mkdir -m 700 -p /tmp/runtime-1000; exec python3 -m open_terminal run --host 127.0.0.1 --port 8000").decode().strip()
        containers.append(terminal)
        bridge(terminal, "python3", "unix-to-tcp", "/run/demo-terminal/api.sock", 8000)
        wait_socket(session/"terminal/api.sock")
        webui = docker(*common, "--name", "demo01b-webui", "--memory", "1g", "--memory-swap", "1g",
                       "--pids-limit", "384",
                       "--tmpfs", "/app/backend/data:rw,nosuid,nodev,size=512m,uid=1000,gid=1000,mode=0700",
                       "--tmpfs", "/tmp:rw,nosuid,nodev,size=128m,mode=1777",
                       "--mount", f"type=bind,src={session/'terminal'},dst=/run/demo-terminal,readonly",
                       "--mount", f"type=bind,src={session/'model'},dst=/run/demo-model,readonly",
                       "--mount", f"type=bind,src={session/'ui'},dst=/run/demo-ui",
                       "--env-file", str(session/"web_env"),
                       images["webui"]["reference"]).decode().strip()
        containers.append(webui)
        bridge(webui, "python", "tcp-to-unix", "/run/demo-terminal/api.sock", 8000)
        bridge(webui, "python", "tcp-to-unix", "/run/demo-model/api.sock", 18081)
        bridge(webui, "python", "unix-to-tcp", "/run/demo-ui/api.sock", 8080)
        wait_socket(session/"ui/api.sock")
        prepare_demo(webui, terminal, admin, demo)
        print("Compte, grant et entrées vérifiés.", flush=True)
        code = """
import urllib.request
with urllib.request.urlopen('http://127.0.0.1:8000/openapi.json',timeout=5) as response:
    assert response.status == 200
"""
        docker("exec", webui, "python", "-c", code)
        print("Pont Terminal vérifié.", flush=True)
        if args.check:
            check_model_boundary(webui, terminal, session/"model/api.sock")
            print("PASS WebUI → Terminal, modèle local fictif réservé à WebUI, Terminal hors réseau, catalogue WebUI vide.")
            return
        access = session / "access.txt"
        access.touch(mode=0o600)
        access.write_text(f"Admin demo01a-admin@example.test {admin}\nDémo demo01a@example.test {demo}\n")
        os.chown(access, 1000, 1000)
        print(f"Accès local et répertoire du relais de cette session : {session}", flush=True)
        ui = subprocess.Popen([sys.executable, str(ROOT/"socket_bridge.py"), "tcp-to-unix",
                               str(session/"ui/api.sock"), "18760"])
        deadline = time.monotonic() + 1200
        while ui.poll() is None and time.monotonic() < deadline and available_memory() >= 1024**2:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    except subprocess.CalledProcessError as error:
        tail = (error.stderr or b"").decode(errors="replace").splitlines()
        if tail:
            print("Classe de diagnostic:", tail[-1].split(":", 1)[0], flush=True)
        if tail and ("HTTP Error" in tail[-1] or "URLError:" in tail[-1]):
            print(tail[-1].split(": ", 1)[0])
            if "HTTP Error" in tail[-1]:
                print(tail[-1].split("HTTP Error ", 1)[1].split(":", 1)[0])
        raise SystemExit("Échec d’un contrôle Docker ou HTTP local.") from None
    finally:
        if ui and ui.poll() is None:
            ui.terminate()
            ui.wait(timeout=5)
        for cid in reversed(containers):
            subprocess.run(["docker", "rm", "-f", cid], capture_output=True, timeout=30)
        shutil.rmtree(session)


if __name__ == "__main__":
    main()
