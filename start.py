"""Launch the API and Cloudflare quick tunnel as detached background processes."""
from __future__ import annotations

import os
import re
import secrets
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = os.environ.get("ENGINE_HOST", "0.0.0.0")
PORT = int(os.environ.get("ENGINE_PORT", "8000"))
URL_RE = re.compile(r"https://[A-Za-z0-9.-]+\.trycloudflare\.com")
STARTUP_TIMEOUT_SECONDS = int(os.environ.get("ENGINE_TUNNEL_STARTUP_TIMEOUT", "90"))


def _stop_process(proc: subprocess.Popen | None) -> None:
    if proc is not None and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> int:
    token = secrets.token_urlsafe(32)
    env = os.environ.copy()
    env["ENGINE_TOKEN"] = token
    env.setdefault("ENGINE_BASE_DIR", str(ROOT))

    cloudflared = shutil.which("cloudflared")
    if not cloudflared:
        print("ERROR: cloudflared not found. Run setup_kaggle.py first.", file=sys.stderr)
        return 2

    server_log_path = ROOT / "server.log"
    tunnel_log_path = ROOT / "cloudflared.log"
    server_log = server_log_path.open("a", encoding="utf-8")
    tunnel_log = tunnel_log_path.open("a", encoding="utf-8")
    server = None
    tunnel = None
    success = False
    try:
        server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app:app", "--host", HOST, "--port", str(PORT), "--app-dir", str(ROOT)],
            cwd=ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=server_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        # Give Uvicorn a moment to bind before exposing it through the tunnel.
        time.sleep(1.5)
        if server.poll() is not None:
            print(f"ERROR: API server exited early. Inspect {server_log_path}", file=sys.stderr)
            return 3

        tunnel = subprocess.Popen(
            [cloudflared, "tunnel", "--url", f"http://127.0.0.1:{PORT}", "--no-autoupdate"],
            cwd=ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=tunnel_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
        url = None
        while time.monotonic() < deadline:
            if server.poll() is not None:
                print(f"ERROR: API server stopped. Inspect {server_log_path}", file=sys.stderr)
                return 3
            if tunnel.poll() is not None:
                print(f"ERROR: cloudflared stopped. Inspect {tunnel_log_path}", file=sys.stderr)
                return 4
            try:
                logs = tunnel_log_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                logs = ""
            matches = URL_RE.findall(logs)
            if matches:
                url = matches[-1]
                break
            time.sleep(0.5)

        if not url:
            print(f"ERROR: No tunnel URL appeared within {STARTUP_TIMEOUT_SECONDS}s. Inspect {tunnel_log_path}", file=sys.stderr)
            return 5

        # Keep both children detached; this launcher can exit so notebook cells stay usable.
        print(f"URL={url}", flush=True)
        print(f"TOKEN={token}", flush=True)
        print("WARNING: TOKEN is a secret. Do not share screenshots or logs containing it.", flush=True)
        print(f"Server PID: {server.pid} | Tunnel PID: {tunnel.pid}", flush=True)
        print(f"Logs: {server_log_path.name}, {tunnel_log_path.name}", flush=True)
        success = True
        return 0
    finally:
        server_log.close()
        tunnel_log.close()
        # Stop children if startup failed. On success they remain detached in background.
        if not success:
            _stop_process(tunnel)
            _stop_process(server)


if __name__ == "__main__":
    raise SystemExit(main())
