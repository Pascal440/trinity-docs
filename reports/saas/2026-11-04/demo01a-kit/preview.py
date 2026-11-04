"""Render a separate PDF using the pinned, disposable offline Calc runtime."""
import argparse
import json
from pathlib import Path
import subprocess
import uuid

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("workbook", type=Path)
parser.add_argument("pdf", type=Path)
args = parser.parse_args()
if args.workbook.suffix.lower() != ".xlsx" or args.pdf.suffix.lower() != ".pdf":
    parser.error("Attendu : un XLSX source et une destination PDF.")
if args.pdf.exists() or args.workbook.stat().st_size > 25 * 1024**2:
    parser.error("Destination déjà présente ou source au-delà de 25 Mio.")
available = int(next(line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines()
                     if line.startswith("MemAvailable:")))
if available < 2 * 1024**2:
    parser.error("Le rendu exige au moins 2 Gio de mémoire hôte disponible.")
image = json.loads((ROOT / "image-manifest.json").read_text())["terminal"]["reference"]
name = f"demo01a-preview-{uuid.uuid4().hex}"
worker = (ROOT / "preview-worker.py").read_text()
try:
    with args.workbook.open("rb") as source:
        result = subprocess.run(
            ["docker", "run", "--rm", "-i", "--name", name, "--pull", "never",
             "--network", "none", "--read-only", "--user", "1000:1000",
             "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
             "--memory", "768m", "--memory-swap", "768m", "--cpus", "1",
             "--pids-limit", "128", "--ulimit", "fsize=33554432:33554432",
             "--tmpfs", "/tmp:rw,nosuid,nodev,size=192m,mode=1777",
             "--env", "HOME=/tmp", "--entrypoint", "/usr/bin/python3",
             image, "-c", worker],
            stdin=source, stdout=subprocess.PIPE, check=True, timeout=60,
        )
except (subprocess.TimeoutExpired, KeyboardInterrupt):
    subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=15)
    raise
if not result.stdout.startswith(b"%PDF-") or len(result.stdout) > 32 * 1024**2:
    raise SystemExit("Sortie PDF invalide ou hors limite.")
with args.pdf.open("xb") as output:
    output.write(result.stdout)
