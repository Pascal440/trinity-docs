"""Recreate the offline demo as a foreground session, with fresh local credentials."""
import argparse
import hashlib
import json
from pathlib import Path
import secrets
import shutil
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
PORT = 18760
MAX_SECONDS = 7200


def docker(*args, **kwargs):
    return subprocess.run(["docker", *args], capture_output=True, check=True, timeout=45, **kwargs).stdout


def available_memory():
    return int(next(line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines()
                    if line.startswith("MemAvailable:")))


def preflight():
    if available_memory() < 4 * 1024**2 or shutil.disk_usage(ROOT).free < 20 * 1024**3:
        raise SystemExit("Préconditions insuffisantes : 4 Gio de RAM disponible et 20 Gio libres requis.")
    if int(docker("info", "--format", "{{.NCPU}}")) < 4:
        raise SystemExit("Quatre CPU hôte requis.")
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", PORT))
    manifests = json.loads((ROOT / "image-manifest.json").read_text())
    for item in manifests.values():
        if docker("image", "inspect", "--format", "{{.Id}}", item["reference"]).decode().strip() != item["docker_id"]:
            raise SystemExit("Image épinglée absente ou identité incorrecte.")
    for name, expected in json.loads((ROOT / "inputs-manifest.json").read_text())["files"].items():
        if hashlib.sha256((ROOT / "inputs" / name).read_bytes()).hexdigest() != expected:
            raise SystemExit("Empreinte d'entrée fictive incorrecte.")
    return manifests


def web_request(webui, path, body=None, token=None):
    code = """
import json, sys, urllib.request
p=json.load(sys.stdin)
headers={"Content-Type":"application/json"}
if p["token"]:
    headers["Authorization"]="Bearer "+p["token"]
body=json.dumps(p["body"]).encode() if p["body"] is not None else None
with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8080"+p["path"],data=body,headers=headers),timeout=10) as response:
    sys.stdout.buffer.write(response.read())
"""
    payload = json.dumps(dict(path=path, body=body, token=token)).encode()
    return json.loads(docker("exec", "-i", webui, "python", "-c", code, input=payload))


def prepare_demo(webui, terminal, admin_password, demo_password):
    ready_deadline = time.monotonic() + 90
    while time.monotonic() < ready_deadline:
        try:
            web_request(webui, "/health")
            break
        except subprocess.CalledProcessError:
            time.sleep(1)
    else:
        raise RuntimeError("WebUI indisponible.")
    token = web_request(webui, "/api/v1/auths/signin",
                        {"email": "demo01a-admin@example.test", "password": admin_password})["token"]
    demo = web_request(webui, "/api/v1/auths/add",
                       {"email": "demo01a@example.test", "password": demo_password,
                        "name": "Atelier Boréal", "role": "user", "profile_image_url": "/user.png"}, token)
    path = "/api/v1/configs/terminal_servers"
    config = web_request(webui, path, token=token)
    config["TERMINAL_SERVER_CONNECTIONS"][0]["config"] = {
        "access_grants": [{"principal_type": "user", "principal_id": demo["id"], "permission": "read"}],
    }
    web_request(webui, path, config, token)
    demo_token = web_request(webui, "/api/v1/auths/signin",
                             {"email": "demo01a@example.test", "password": demo_password})["token"]
    terminals = web_request(webui, "/api/v1/terminals/", token=demo_token)
    if [item["id"] for item in terminals] != ["demo01a"]:
        raise RuntimeError("Accès Terminal de démonstration incorrect.")
    if web_request(webui, "/api/models", token=demo_token)["data"]:
        raise RuntimeError("Le catalogue hors ligne doit être vide.")
    docker("exec", terminal, "mkdir", "-p", "/home/user/runtime01/inputs")
    for source in sorted((ROOT / "inputs").iterdir()):
        destination = "/home/user/runtime01/inputs/" + source.name
        docker("exec", "-i", terminal, "sh", "-c", 'cat > "$1"', "sh", destination,
               input=source.read_bytes())
        copied = docker("exec", terminal, "cat", destination)
        if hashlib.sha256(copied).digest() != hashlib.sha256(source.read_bytes()).digest():
            raise RuntimeError("Entrée transférée incorrecte.")


def interrupt(_signal, _frame):
    raise KeyboardInterrupt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Recréer, vérifier puis retirer le labo sans relais.")
    args = parser.parse_args()
    images = preflight()
    config = json.loads((ROOT / "config.json").read_text())
    terminal_key = secrets.token_urlsafe(36)
    admin_password = secrets.token_urlsafe(24)
    demo_password = secrets.token_urlsafe(24)
    config["term_env"]["OPEN_TERMINAL_API_KEY"] = terminal_key
    config["web_env"].update(
        WEBUI_SECRET_KEY=secrets.token_urlsafe(40),
        WEBUI_ADMIN_EMAIL="demo01a-admin@example.test",
        WEBUI_ADMIN_PASSWORD=admin_password,
        TERMINAL_SERVER_CONNECTIONS=json.dumps([{
            "id": "demo01a", "name": "Atelier Boréal — Terminal",
            "url": "http://127.0.0.1:8000", "key": terminal_key,
            "enabled": True, "auth_type": "bearer", "path": "/openapi.json",
        }]),
    )
    common = ["run", "-d", "--pull", "never", "--label", "mission=demo01a",
              "--init", "--read-only", "--user", "1000:1000", "--cap-drop", "ALL",
              "--security-opt", "no-new-privileges", "--cpus", "1",
              "--ulimit", "nofile=4096:4096", "--ulimit", "fsize=67108864:67108864",
              "--log-opt", "max-size=5m", "--log-opt", "max-file=2"]
    deadline = time.monotonic() + MAX_SECONDS
    signal.signal(signal.SIGTERM, interrupt)
    containers = []
    try:
        with tempfile.TemporaryDirectory(prefix="demo01a-", dir="/dev/shm") as directory:
            private = Path(directory)
            for role, values in config.items():
                file = private / role
                file.write_text("".join(f"{key}={value}\n" for key, value in values.items()))
                file.chmod(0o600)
            terminal = docker(*common, "--name", "demo01a-terminal", "--network", "none",
                              "--pids-limit", "512", "--memory", "2g", "--memory-swap", "2g",
                              "--shm-size", "256m",
                              "--tmpfs", "/home/user:rw,nosuid,nodev,size=512m,uid=1000,gid=1000,mode=0700",
                              "--tmpfs", "/tmp:rw,nosuid,nodev,size=256m,mode=1777",
                              "--tmpfs", "/run:rw,nosuid,nodev,size=16m,uid=1000,gid=1000",
                              "--env-file", str(private / "term_env"), "--entrypoint", "sh",
                              images["terminal"]["reference"], "-c",
                              "mkdir -p /tmp/runtime-1000 /home/user/.local/bin; chmod 700 /tmp/runtime-1000; "
                              "exec /usr/local/bin/python3 -m open_terminal run --host 127.0.0.1 --port 8000").decode().strip()
            containers.append(terminal)
            webui = docker(*common, "--name", "demo01a-webui", "--network", "container:" + terminal,
                           "--pids-limit", "384", "--memory", "1g", "--memory-swap", "1g",
                           "--tmpfs", "/app/backend/data:rw,nosuid,nodev,size=512m,uid=1000,gid=1000,mode=0700",
                           "--tmpfs", "/tmp:rw,nosuid,nodev,size=128m,mode=1777",
                           "--env-file", str(private / "web_env"),
                           images["webui"]["reference"]).decode().strip()
            containers.append(webui)
            prepare_demo(webui, terminal, admin_password, demo_password)
            print("WebUI prêt, compte démo configuré, catalogue vide et trois entrées vérifiées.", flush=True)
            if not args.check:
                from ui_relay import serve
                access = private / "access.txt"
                access.write_text(f"Compte opérateur : demo01a-admin@example.test\nMot de passe : {admin_password}\n"
                                  f"Compte démo : demo01a@example.test\nMot de passe : {demo_password}\n")
                access.chmod(0o600)
                print(f"Accès SSH privé sur 127.0.0.1:{PORT}. Identifiants temporaires : {access}", flush=True)
                serve(terminal, PORT, deadline, available_memory)
    except KeyboardInterrupt:
        pass
    except subprocess.CalledProcessError:
        raise SystemExit("Échec Docker ou API locale. Diagnostic sans affichage des identifiants.") from None
    finally:
        for container in reversed(containers):
            result = subprocess.run(["docker", "rm", "-f", container], capture_output=True, timeout=30)
            if result.returncode:
                print(f"Retrait à vérifier pour le conteneur de démo {container}.", flush=True)


if __name__ == "__main__":
    main()
