"""Swap the viewer captions of an existing Premiere package into a NEW run (original package untouched).

captions.srt            <- new captions (e.g. accepted Hinglish layer SRT)
captions_<old_tag>.srt  <- the package's previous captions, kept for reference
extra files (layer json, acceptance json) are copied into the package; package_manifest.json is rehashed;
README_IMPORT.txt gets a header describing the change. sequence.xml / media / visuals are copied unchanged.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional


def repackage_captions(src_pkg: str, srt: str, *, old_tag: str = "hindi", extras: Optional[List[str]] = None,
                       caption_note: str = "", run=None) -> Dict[str, Any]:
    from core.runs import Run, sha256_file
    src = Path(src_pkg)
    if not (src / "sequence.xml").exists() or not (src / "captions.srt").exists():
        return {"error": f"{src} is not a KANG Premiere package (sequence.xml + captions.srt needed)"}
    srt_text = Path(srt).read_text(encoding="utf-8-sig")
    if "-->" not in srt_text:
        return {"error": f"{srt} does not look like an SRT"}
    run = run or Run()
    run.add_input(srt, "captions_new")
    run.add_input(str(src / "package_manifest.json"), "package_in_manifest")
    dst = run.path("premiere_package")
    shutil.copytree(src, dst)
    shutil.copy2(dst / "captions.srt", dst / f"captions_{old_tag}.srt")
    (dst / "captions.srt").write_text(srt_text, encoding="utf-8")
    for e in extras or []:
        shutil.copy2(e, dst / Path(e).name)
    status_lines = []
    acc_p = dst / "hinglish_acceptance.json"
    if acc_p.is_file():  # say plainly what was accepted and what was not
        acc = json.loads(acc_p.read_text(encoding="utf-8"))
        status_lines = [
            f"Hinglish display text: {acc.get('status', 'unknown')} (mode {acc.get('acceptance_mode', 'per-block review')})",
            "Word-level caption timing: " + ("verified" if acc.get("timing_verified") else "NOT verified"),
            "Hindi source transcript (words.json): unchanged, its own review status applies",
            "Premiere import/playback of this package: NOT_TESTED"]
    readme = dst / "README_IMPORT.txt"
    old = readme.read_text(encoding="utf-8") if readme.exists() else ""
    head = (f"CAPTIONS CHANGED ({run.run_id}): captions.srt = {Path(srt).name}. {caption_note}\n"
            f"Previous captions kept as captions_{old_tag}.srt. sequence.xml, media/, visuals/ unchanged from "
            f"{src.parent.name}.\n" + "".join(l + "\n" for l in status_lines) + "\n")
    readme.write_text(head + old, encoding="utf-8")
    files = {p.relative_to(dst).as_posix(): sha256_file(p) for p in sorted(dst.rglob("*"))
             if p.is_file() and p.name != "package_manifest.json"}
    pm = json.loads((src / "package_manifest.json").read_text(encoding="utf-8"))
    pm.update({"run_id": run.run_id, "parent_package_run": pm.get("run_id"), "files": files,
               "captions": {"file": "captions.srt", "source": Path(srt).name, "previous": f"captions_{old_tag}.srt",
                            "note": caption_note, "status": status_lines}})
    (dst / "package_manifest.json").write_text(json.dumps(pm, ensure_ascii=False, indent=2), encoding="utf-8")
    run.add_output(dst / "captions.srt", "captions_srt")
    run.add_output(dst / "package_manifest.json", "package_manifest")
    run.log_step("repackage_captions", parent=str(src), captions=Path(srt).name, files=len(files))
    run.set_status("premiere_package_ready_import_not_tested")
    return {"run_id": run.run_id, "package": str(dst), "files": len(files), "captions": Path(srt).name}
