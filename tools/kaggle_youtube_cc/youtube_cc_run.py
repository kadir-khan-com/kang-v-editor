"""Kaggle CPU kernel (internet ON): run KANG v15 `core.youtube_cc.fetch_cmd` from a Kaggle IP (sandbox IP is
blocked by YouTube: 429/403). Same code path as `kang.py fetch-youtube-cc`: CC-filtered search (pre-filter only),
per-video licence field == "Creative Commons Attribution license (reuse allowed)" + place check, max 3 x 20 s
sections, video only <= 1080p, 1 GB cap, ffmpeg scene split, shake/text/face checks, contact sheet.
Input dataset kang-youtube-cc-input: kang_bundle.tar.gz (core/, config/, tools/models/, fonts/Mukta-ExtraBold.ttf).
Output (/kaggle/working): runs/<RUN_ID>/ (candidates CSV, accepted JSON, shots.json, contact sheet, manifest),
pool/ (YT_*.mp4 + CREDITS.json), kernel_report.json. Only difference to the CLI: download timeout raised (Kaggle
CPU, 3 sections per call) and the JS runtime arg follows what the image has (node, else deno from PyPI)."""
import glob, json, os, shutil, subprocess, sys, tarfile, time, traceback

W = "/kaggle/working"
RUN_ID = "2026-11-04_KANG_008"
rep = {"steps": [], "run_id": RUN_ID, "t0": time.time()}


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    rep["steps"].append({"cmd": cmd, "rc": r.returncode, "tail": (r.stdout + r.stderr)[-800:]})
    print("$", cmd, "rc", r.returncode, (r.stdout + r.stderr)[-400:], flush=True)
    return r


def save():
    json.dump(rep, open(f"{W}/kernel_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


K = f"{W}/kang"
os.makedirs(K, exist_ok=True)
tars = glob.glob("/kaggle/input/**/kang_bundle.tar.gz", recursive=True)
if tars:
    with tarfile.open(tars[0]) as t:
        t.extractall(K)
else:  # Kaggle may have unpacked the archive already
    src = os.path.dirname(glob.glob("/kaggle/input/**/core/youtube_cc.py", recursive=True)[0])
    shutil.copytree(os.path.dirname(src), K, dirs_exist_ok=True)
rep["bundle"] = sorted(os.listdir(K))
sh("pip install -q -U 'yt-dlp[default]'")
sh("python -m yt_dlp --version")
node = shutil.which("node")
js = "node"
if not node:
    sh("pip install -q deno")
    js = "deno"
rep["js_runtime"] = js
sh(f"{js} --version")
sh("ffmpeg -version | head -1")
sh("python -c 'import cv2; print(cv2.__version__, hasattr(cv2, \"FaceDetectorYN\"))'")
sh("curl -s https://api.ipify.org")

cfg = json.load(open(f"{K}/config/youtube_cc.json", encoding="utf-8"))
if js != "node":
    for w in cfg["probe_ways"]:
        w["args"] = [js if a == "node" else a for a in w["args"]]
    json.dump(cfg, open(f"{K}/config/youtube_cc_kaggle.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
cfg_path = f"{K}/config/youtube_cc_kaggle.json" if js != "node" else None
rep["cfg_path"] = cfg_path or "config/youtube_cc.json (unchanged)"

os.environ["KANG_RUNS_DIR"] = f"{W}/runs"
sys.path.insert(0, K)
os.chdir(K)
from core import youtube_cc as yc  # noqa: E402


def runner(args, timeout):
    return yc.ytdlp_runner(args, max(timeout, 1200.0) if "--download-sections" in args else timeout)


try:
    res = yc.fetch_cmd(f"{W}/pool", runner=runner, cfg_path=cfg_path, max_probe=200, run_id=RUN_ID)
    rep["result"] = res
except Exception:
    rep["error"] = traceback.format_exc()
    print(rep["error"], flush=True)
rep["elapsed_s"] = round(time.time() - rep["t0"], 1)
save()
# raw section downloads are large; keep only the cut shots + run files
shutil.rmtree(f"{W}/runs/{RUN_ID}/yt_raw", ignore_errors=True)
shutil.rmtree(K, ignore_errors=True)
print(json.dumps(rep.get("result", rep.get("error")), ensure_ascii=False, default=str)[:3000], flush=True)
