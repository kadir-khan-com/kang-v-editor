"""
Bundle Generator for AI Video Engine
Packs canonical source files into kaggle_sync_bundle.py and updates ai_video_engine_kaggle_ready.ipynb.
"""
from __future__ import annotations

import json
from pathlib import Path
from pprint import pformat

ROOT = Path(__file__).resolve().parent

BUNDLE_FILES = [
    "app.py",
    "brand.json",
    "build_and_check.py",
    "config/fillers.json",
    "config/glossary.json",
    "STATUS.md",
    "core/__init__.py",
    "core/audio.py",
    "core/brand.py",
    "core/cutter.py",
    "core/edl.py",
    "core/engine.py",
    "core/gapfill.py",
    "core/voter.py",
    "core/pipeline.py",
    "core/premiere.py",
    "core/scenes.py",
    "core/package_readiness.py",
    "core/script_style.py",
    "core/second_opinion.py",
    "core/consensus.py",
    "core/hindi_numbers.py",
    "core/spelling_policy.py",
    "core/visuals.py",
    "config/script_equivalents.json",
    "config/name_suggestions.json",
    "config/english_script.json",
    "core/qa.py",
    "core/render.py",
    "core/runs.py",
    "core/style.py",
    "core/subtitles.py",
    "core/words.py",
    "kang.py",
    "presets/educational.json",
    "presets/promo.json",
    "presets/travel.json",
    "presets/vox_bold_yellow.json",
    "requirements.txt",
    "scripts/__init__.py",
    "scripts/fetch_fonts.py",
    "setup_kaggle.py",
    "start.py",
    "test_30s_sample.py",
]


def build_bundle_code() -> str:
    files_map = {}
    for rel_path in BUNDLE_FILES:
        full_path = ROOT / rel_path
        if not full_path.is_file():
            raise FileNotFoundError(f"Missing canonical file: {full_path}")
        files_map[rel_path] = full_path.read_text(encoding="utf-8")

    formatted_files = pformat(files_map, width=100, sort_dicts=True)

    code = f'''"""Generated Kaggle sync bundle. Run generate_bundle.py to regenerate."""
import os
from pathlib import Path

BASE_DIR = Path(os.environ.get('ENGINE_BASE_DIR', '/kaggle/working/ai-video-engine'))
BASE_DIR.mkdir(parents=True, exist_ok=True)

FILES = {formatted_files}

for rel, content in FILES.items():
    dest = BASE_DIR / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding='utf-8')
    print(f'[SYNC] Wrote {{dest}}')

print('\\n[SYNC] Source files written. Fetching open fonts (Noto Sans Devanagari, Montserrat)...')
import subprocess, sys
subprocess.run([sys.executable, str(BASE_DIR / 'scripts' / 'fetch_fonts.py')], check=False)
print('\\n[SYNC] Starting Kaggle environment setup...')
setup_path = BASE_DIR / 'setup_kaggle.py'
exec(compile(setup_path.read_text(encoding='utf-8'), str(setup_path), 'exec'), {{'__name__': '__main__'}})
'''
    return code


def update_notebook(bundle_code: str, nb_path: Path) -> None:
    if not nb_path.is_file():
        raise FileNotFoundError(f"Notebook file not found: {nb_path}")

    with nb_path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    # In ai_video_engine_kaggle_ready.ipynb, Cell 1 is the bundle code cell
    # Split bundle code preserving exact line endings as standard in ipynb
    code_lines = bundle_code.splitlines(keepends=True)

    nb["cells"][1]["source"] = code_lines

    with nb_path.open("w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    print(f"Reading {len(BUNDLE_FILES)} canonical source files from {ROOT}...")
    bundle_code = build_bundle_code()

    # 1. Write kaggle_sync_bundle.py
    bundle_path = ROOT / "kaggle_sync_bundle.py"
    bundle_path.write_text(bundle_code, encoding="utf-8")
    print(f"Successfully generated {bundle_path} ({len(bundle_code)} chars).")

    # 2. Update ai_video_engine_kaggle_ready.ipynb
    nb_path = ROOT / "ai_video_engine_kaggle_ready.ipynb"
    update_notebook(bundle_code, nb_path)
    print(f"Successfully updated {nb_path} with matching bundle code.")

    # 3. Verify match
    with nb_path.open("r", encoding="utf-8") as f:
        nb_check = json.load(f)
    embedded_code = "".join(nb_check["cells"][1]["source"])
    assert embedded_code == bundle_code, "Verification failed: Embedded notebook code does not match bundle!"
    print("Verification passed: Notebook embedded code exactly matches kaggle_sync_bundle.py.")


if __name__ == "__main__":
    main()
