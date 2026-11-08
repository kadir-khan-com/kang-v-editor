"""Phase 0: build_and_check.py -> one command, PASS/FAIL report.

Order (roadmap): files -> syntax -> environment (FFmpeg/libass/shaping, Python libs,
fonts, brand/presets) -> test_offline.py -> pytest suite -> generate_bundle.py -> sync check.
Any failure BLOCKS packaging (generate_bundle is never run after a failure).

Usage:  python build_and_check.py [--no-bundle] [--fetch-fonts] [--quick]
Writes: build_report.json
"""
from __future__ import annotations

import ast
import datetime as dt
import importlib
import json
import shutil
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

REQUIRED_FILES = [
    "app.py", "core/__init__.py", "core/engine.py", "core/gapfill.py", "core/voter.py", "core/runs.py", "core/brand.py", "core/edl.py",
    "core/words.py", "core/subtitles.py", "core/render.py", "core/cutter.py", "core/audio.py",
    "core/style.py", "core/qa.py", "core/pipeline.py", "kang.py", "brand.json", "config/fillers.json",
    "presets/vox_bold_yellow.json", "config/glossary.json", "requirements.txt",
]
# Dev-only files: present in the local project, intentionally NOT in the Kaggle runtime bundle.
DEV_ONLY_FILES = ["test_offline.py", "generate_bundle.py", "tests/test_foundation.py"]
PY_LIBS = ["numpy", "pydantic", "PIL", "fontTools"]
OPTIONAL_LIBS = ["faster_whisper", "fastapi", "pytest"]


class Report:
    def __init__(self):
        self.steps = []

    def add(self, name, ok, detail="", blocking=True):
        self.steps.append({"step": name, "pass": bool(ok), "blocking": blocking, "detail": detail})
        mark = "PASS" if ok else ("FAIL" if blocking else "WARN")
        print(f"[{mark}] {name}" + (f" - {detail}" if detail else ""))
        return ok

    @property
    def ok(self):
        return all(s["pass"] for s in self.steps if s["blocking"])


def _run(cmd, timeout=900):
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}  # Windows console is cp1252 by default
    r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout)
    return r.returncode, (r.stdout + r.stderr)


def check_files(rep):
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    dev_missing = [f for f in DEV_ONLY_FILES if not (ROOT / f).is_file()]
    note = f"{len(REQUIRED_FILES)} present" + (f" (runtime tree: dev-only absent: {dev_missing})" if dev_missing else "")
    return rep.add("files", not missing, f"missing: {missing}" if missing else note)


def check_syntax(rep):
    bad = []
    for p in sorted(ROOT.rglob("*.py")):
        if any(part in {"runs", ".venv", "venv", "__pycache__", "backup_original"} for part in p.parts):
            continue
        try:
            ast.parse(p.read_text(encoding="utf-8"), str(p))
        except SyntaxError as e:
            bad.append(f"{p.relative_to(ROOT)}:{e.lineno}")
    for p in list(ROOT.glob("*.json")) + list((ROOT / "presets").glob("*.json")) + list((ROOT / "config").glob("*.json")):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            bad.append(f"{p.relative_to(ROOT)}: {e}")
    return rep.add("syntax", not bad, ", ".join(bad) if bad else "py + json parse OK")


def check_env(rep, fetch_fonts=False):
    ok = True
    ff = shutil.which("ffmpeg") and shutil.which("ffprobe")
    ok &= rep.add("ffmpeg binary", bool(ff), shutil.which("ffmpeg") or "not on PATH")
    if ff:
        _, conf = _run(["ffmpeg", "-hide_banner", "-buildconf"])
        libs = {k: (f"--enable-{k}" in conf) for k in ("libass", "libharfbuzz", "libfreetype", "libfribidi")}
        ok &= rep.add("ffmpeg libass + HarfBuzz", libs["libass"] and libs["libharfbuzz"], str(libs))
        _, flt = _run(["ffmpeg", "-hide_banner", "-filters"])
        need = ["ass", "loudnorm", "silencedetect", "afftdn", "ebur128", "alimiter"]
        miss = [f for f in need if f" {f} " not in flt]
        ok &= rep.add("ffmpeg filters", not miss, f"missing {miss}" if miss else ", ".join(need))
        _, h = _run(["ffmpeg", "-hide_banner", "-h", "filter=ass"])
        ok &= rep.add("ass shaping=complex option", "shaping" in h and "complex" in h)
    for lib in PY_LIBS:
        try:
            importlib.import_module(lib)
            rep.add(f"python lib {lib}", True)
        except Exception as e:
            ok &= rep.add(f"python lib {lib}", False, str(e))
    for lib in OPTIONAL_LIBS:
        try:
            importlib.import_module(lib)
            rep.add(f"optional lib {lib}", True, blocking=False)
        except Exception:
            rep.add(f"optional lib {lib}", False, "not installed (needed for transcription/API/tests)", blocking=False)
    if fetch_fonts:
        from scripts.fetch_fonts import fetch
        fetch()
    from core.brand import load_brand, resolve_fonts, missing_glyphs
    try:
        brand = load_brand(ROOT / "brand.json")
        rep.add("brand.json schema", True, brand.client)
        fonts, warns = resolve_fonts(brand, ROOT / "fonts")
        rep.add("fonts resolved", not warns, "; ".join(warns) or ", ".join(p.name for p in set(fonts.values())), blocking=False)
        miss = missing_glyphs(fonts["hindi"], "द्वारका क्षत्रिय श्री ज्ञान हृदय Amazing Zip-line 2026")
        ok &= rep.add("Devanagari glyph coverage", not miss, f"missing {miss}" if miss else fonts["hindi"].name)
    except Exception as e:
        ok &= rep.add("brand/fonts", False, str(e))
    from core.subtitles import list_presets, load_preset
    try:
        names = list_presets(ROOT / "presets")
        for n in names:
            load_preset(n, ROOT / "presets")
        rep.add("presets schema", bool(names), ", ".join(names))
    except Exception as e:
        ok &= rep.add("presets schema", False, str(e))
    return ok


def check_tests(rep, quick=False):
    if not (ROOT / "test_offline.py").is_file() or not (ROOT / "tests").is_dir():
        return rep.add("tests", True, "SKIP: dev-only tests not in this (Kaggle runtime) tree; run them locally", blocking=False)
    code, out = _run([sys.executable, "test_offline.py"])
    ok = rep.add("test_offline.py (legacy engine, 21 tests)", code == 0, next((l for l in out.splitlines() if "PASSED" in l or "FAIL" in l), out.strip()[-200:]))
    try:
        importlib.import_module("pytest")
    except Exception:
        return rep.add("pytest suite", False, "pytest not installed: pip install pytest") and ok
    args = [sys.executable, "-m", "pytest", "-q", "tests"]
    if quick:
        args += ["-k", "not multi_format and not promo and not subtitle_video"]
    code, out = _run(args)
    tail = [l for l in out.strip().splitlines() if "passed" in l or "failed" in l or "error" in l]
    return rep.add("pytest suite (tests/)", code == 0, tail[-1] if tail else out[-500:]) and ok


def check_bundle(rep):
    if not (ROOT / "generate_bundle.py").is_file():
        return rep.add("bundle", True, "SKIP: generate_bundle.py not in this (Kaggle runtime) tree", blocking=False)
    code, out = _run([sys.executable, "generate_bundle.py"])
    if not rep.add("generate_bundle.py", code == 0, out.strip().splitlines()[-1] if out.strip() else ""):
        return False
    # sync check: every bundled file in the generated bundle matches the canonical file
    import generate_bundle as gb
    ns = {}
    src = (ROOT / "kaggle_sync_bundle.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "FILES":
            ns["FILES"] = ast.literal_eval(node.value)
    files = ns.get("FILES", {})
    drift = [f for f in gb.BUNDLE_FILES if files.get(f) != (ROOT / f).read_text(encoding="utf-8")]
    nb = json.loads((ROOT / "ai_video_engine_kaggle_ready.ipynb").read_text(encoding="utf-8"))
    nb_ok = "".join(nb["cells"][1]["source"]) == src
    return rep.add("bundle sync check", not drift and nb_ok,
                   f"drift: {drift}, notebook_match={nb_ok}" if (drift or not nb_ok) else f"{len(files)} files in sync")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    rep = Report()
    print(f"KANG build_and_check  {dt.datetime.now().isoformat(timespec='seconds')}\n" + "-" * 50)
    check_files(rep) and check_syntax(rep)
    if rep.ok:
        check_env(rep, fetch_fonts="--fetch-fonts" in argv)
    if rep.ok:
        check_tests(rep, quick="--quick" in argv)
    if rep.ok and "--no-bundle" not in argv:
        check_bundle(rep)
    elif not rep.ok:
        rep.add("packaging", False, "BLOCKED because an earlier step failed")
    (ROOT / "build_report.json").write_text(json.dumps({"pass": rep.ok, "steps": rep.steps,
                                                         "at": dt.datetime.now().isoformat(timespec="seconds")},
                                                        indent=2, ensure_ascii=False), encoding="utf-8")
    print("-" * 50 + f"\nRESULT: {'PASS' if rep.ok else 'FAIL'}  (build_report.json)")
    return 0 if rep.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
