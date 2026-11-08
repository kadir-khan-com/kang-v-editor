#!/usr/bin/env python3
"""Kaggle-style preflight: environment + project checks. Exit 1 if any FAIL."""
import argparse, importlib, os, platform, re, shutil, subprocess, sys
from pathlib import Path

RESULTS = []

def rec(status, name, detail=""):
    RESULTS.append((status, name, detail))
    print(f"[{status:4}] {name}" + (f" - {detail}" if detail else ""))

def run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return p.returncode, (p.stdout + p.stderr)
    except Exception as e:
        return 1, str(e)

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "_kaggle_sandbox", ".mypy_cache", ".pytest_cache"}
# drive-letter path ("E:\\x"), but skip regex like r"I:\s*(...)" (\s \d \w \b followed by a quantifier)
WIN_PATH = re.compile(r"""["'][A-Za-z]:[\\/]{1,4}(?![\\]*[sdwbSDWB][*+?{\[\\(|])[^"'\n]*["']""")
CODE_EXT = {".py", ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".sh", ".ipynb"}

def scan_project(project: Path, max_mb: int):
    hard, backslash, big, total = [], [], [], 0
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = Path(root) / f
            try:
                size = p.stat().st_size
            except OSError:
                continue
            total += size
            if size > max_mb * 1024 * 1024:
                big.append((p.relative_to(project), size // (1024 * 1024)))
            if p.suffix.lower() in CODE_EXT and size < 2_000_000 and f != "kaggle_preflight.py" \
                    and not f.endswith(("_report.json", ".log")):  # generated reports may record local tool paths
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                for i, line in enumerate(txt.splitlines(), 1):
                    if line.lstrip().startswith("#"):
                        continue
                    if WIN_PATH.search(line):
                        hard.append(f"{p.relative_to(project)}:{i}")
                    elif p.suffix == ".py" and re.search(r"os\.system\(.*\\\\", line):
                        backslash.append(f"{p.relative_to(project)}:{i}")
    return hard, backslash, big, total

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="project folder (working copy)")
    ap.add_argument("--require", default="", help="comma list of python modules that MUST import")
    ap.add_argument("--optional", default="numpy,librosa,soundfile,faster_whisper,cv2,PIL,pydantic",
                    help="comma list of python modules (WARN if missing)")
    ap.add_argument("--min-free-gb", type=float, default=2.0)
    ap.add_argument("--max-file-mb", type=int, default=200)
    a = ap.parse_args()
    project = Path(a.project).resolve()

    print("=== KAGGLE-LIKE PREFLIGHT ===")
    rec("INFO", "platform", f"{platform.system()} {platform.release()} | python {platform.python_version()}")
    rec("OK" if sys.version_info >= (3, 10) else "FAIL", "python >= 3.10")
    rec("OK" if project.exists() else "FAIL", "project folder exists", str(project))

    # writable working dir + free disk
    try:
        t = project / ".write_test"; t.write_text("x"); t.unlink()
        rec("OK", "working dir writable")
    except Exception as e:
        rec("FAIL", "working dir writable", str(e))
    free_gb = shutil.disk_usage(project).free / 1e9
    rec("OK" if free_gb >= a.min_free_gb else "FAIL", "free disk", f"{free_gb:.1f} GB")

    # ffmpeg / ffprobe / libass
    ff = shutil.which("ffmpeg"); fp = shutil.which("ffprobe")
    rec("OK" if ff else "FAIL", "ffmpeg on PATH", ff or "missing")
    rec("OK" if fp else "FAIL", "ffprobe on PATH", fp or "missing")
    if ff:
        _, out = run([ff, "-hide_banner", "-filters"])
        rec("OK" if re.search(r"\bsubtitles\b", out) else "FAIL", "ffmpeg 'subtitles' filter (libass)")
        _, out = run([ff, "-hide_banner", "-encoders"])
        rec("OK" if "libx264" in out else "WARN", "ffmpeg libx264 encoder")

    # fonts (Devanagari)
    fonts = []
    for d in ("/usr/share/fonts", "/usr/local/share/fonts", str(project / "fonts"), str(project / "assets" / "fonts")):
        if Path(d).exists():
            fonts += [p.name for p in Path(d).rglob("*") if p.suffix.lower() in (".ttf", ".otf")]
    dev = [f for f in fonts if "devanagari" in f.lower() or "mangal" in f.lower() or "hind" in f.lower()]
    rec("OK" if dev else "WARN", "Devanagari font found", dev[0] if dev else "no Noto Sans Devanagari in system fonts or project/fonts")

    # GPU (optional)
    smi = shutil.which("nvidia-smi")
    rec("INFO", "GPU", "nvidia-smi found" if smi else "no GPU (CPU mode). GPU-only code ko CPU fallback chahiye")

    # python modules
    for m in [x for x in a.require.split(",") if x.strip()]:
        try:
            importlib.import_module(m.strip()); rec("OK", f"import {m.strip()} (required)")
        except Exception as e:
            rec("FAIL", f"import {m.strip()} (required)", type(e).__name__)
    for m in [x for x in a.optional.split(",") if x.strip()]:
        try:
            importlib.import_module(m.strip()); rec("OK", f"import {m.strip()}")
        except Exception as e:
            rec("WARN", f"import {m.strip()}", type(e).__name__)

    # project scan
    hard, bs, big, total = scan_project(project, a.max_file_mb)
    rec("INFO", "project size", f"{total/1e6:.1f} MB")
    rec("OK" if not hard else "FAIL", "no hard-coded Windows paths (C:\\..., E:\\...)",
        "; ".join(hard[:8]) + (" ..." if len(hard) > 8 else "") if hard else "")
    rec("OK" if not bs else "WARN", "no backslash paths in os.system", "; ".join(bs[:5]))
    rec("OK" if not big else "WARN", f"no file > {a.max_file_mb} MB inside project",
        "; ".join(f"{p} ({s}MB)" for p, s in big[:5]))

    fails = [r for r in RESULTS if r[0] == "FAIL"]
    warns = [r for r in RESULTS if r[0] == "WARN"]
    print(f"=== PREFLIGHT: {'FAIL' if fails else 'PASS'} ({len(fails)} fail, {len(warns)} warn) ===")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
