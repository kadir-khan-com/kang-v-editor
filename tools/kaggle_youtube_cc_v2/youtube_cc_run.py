"""Kaggle kernel VERSION 2 of ironindiarat/kang-youtube-cc (KANG v16, decision B 2026-11-04): second fetch ONLY for
queries Shivrajpur beach Dwarka, Rukmini temple Dwarka, Dwarka lighthouse, then Gomti ghat Dwarka (only if cap left),
cap 600 MB, same licence gate ("Creative Commons Attribution license (reuse allowed)") + place + auto shot checks.
Videos already downloaded by v1 (run 2026-11-04_KANG_008) are skipped (config skip_video_ids).
Everything else = tools/kaggle_youtube_cc/youtube_cc_run.py (v1)."""

import glob, json, os, shutil, subprocess, sys, tarfile, time, traceback

W = "/kaggle/working"
SKIP_IDS = ["VyCGeLVYFcQ", "K_M4hMxOZts", "7E1uvEdpz_A", "TgEnExGJhgs", "1fO8Pz6bWsY", "_qIsz-cucvo", "cHlZl3eHxtY", "6UeWT5njaWc", "8P5e9p6u5Kc", "0mHRDNcnInQ", "YE-HIWmUdNI", "FyHJoEe9F-k", "WpVHUntgUa0", "LGstwA3-M0E", "2G6aOF2kscY", "zA7cTMe7C8U", "1WTSTCar4_4", "HGSn3yfKfog", "R3eU4MuD5rY", "XdjWenYOjWc", "BTKdh85DEHc", "wezT3Y_2_uU", "0nHOTe8wftc", "hj7yrqu5GGc", "mt_xdx4S_Ok", "3YVQe5MYyhE", "WvSeKRB9dDE", "Q6uAkdpenYI", "mR0q9xb8HGQ", "L4aWKp7MNzs", "GpOYik73qXs", "58XlQQJS1Lg", "csJxLzDtQsw", "vONk9ANANrM", "hKkrDKT1w3Q", "Obr0l9wqcS0", "qan150S2dpI", "9hVvnEfxYBE", "yCFMF12GhVM", "wUmG5cRQqtU", "827X3BoSRo4", "SlcDvJhAsO0", "uG5FkpgZrJQ", "zdimPq45Xp8", "37NjPvIxyr0", "BPENmTR-o08"]
RUN_ID = "2026-11-04_KANG_011"
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
ORDER = ["shivrajpur", "rukmini", "lighthouse", "gomti"]  # Gomti last = only if cap left
cfg["queries"] = sorted([q for q in cfg["queries"] if q["place"] in ORDER], key=lambda q: ORDER.index(q["place"]))
cfg["download"]["cap_bytes"] = 600_000_000
cfg["skip_video_ids"] = SKIP_IDS
json.dump(cfg, open(f"{K}/config/youtube_cc_kaggle_v2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
cfg_path = f"{K}/config/youtube_cc_kaggle_v2.json"
rep["cfg_path"] = "config/youtube_cc.json + v2 overrides (4 queries, 600 MB cap, skip v1 ids)"
rep["queries"] = [q["query"] for q in cfg["queries"]]

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
