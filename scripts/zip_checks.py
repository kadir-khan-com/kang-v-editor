"""Zip checks for a beats-package zip (v17; same checks as the v13-v16 ad-hoc runs): one top folder, every xmeml
pathurl present in the zip, unique file / clipitem ids, package_manifest.json hashes match the zipped files.
Usage: python scripts/zip_checks.py out/x.zip [--run RUN_ID]  (with --run the result is logged as step zip_checks)."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def check(zpath: str) -> dict:
    z = zipfile.ZipFile(zpath)
    names = [n for n in z.namelist() if not n.endswith("/")]
    tops = sorted({n.split("/")[0] for n in names})
    top = tops[0] if len(tops) == 1 else None
    xml = z.read(f"{top}/sequence.xml").decode("utf-8") if top else ""
    urls = re.findall(r"<pathurl>(.*?)</pathurl>", xml)
    missing = []
    for u in urls:
        p = unquote(u.replace("file://localhost/", "").replace("file:///", ""))
        rel = "/".join(PureWindowsPath(p).parts[-2:])
        if f"{top}/{rel}" not in names:
            missing.append(rel)
    fids = re.findall(r'<file id="([^"]+)"', xml)
    cids = re.findall(r'<clipitem id="([^"]+)"', xml)
    man = json.loads(z.read(f"{top}/package_manifest.json")) if top else {"files": {}}
    bad = [k for k, h in man.get("files", {}).items()
           if f"{top}/{k}" not in names or hashlib.sha256(z.read(f"{top}/{k}")).hexdigest() != h]
    res = {"top_folder": top, "top_folders": len(tops), "pathurls": len(urls), "pathurls_missing": len(missing),
           "missing": missing[:10], "file_ids_unique": len(set(fids)), "file_ids": len(fids),
           "clipitem_ids_unique": len(set(cids)), "clipitem_ids": len(cids),
           "manifest_hashes": len(man.get("files", {})), "manifest_bad": len(bad)}
    res["pass"] = bool(top) and not missing and len(set(cids)) == len(cids) and not bad
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("zip")
    ap.add_argument("--run")
    a = ap.parse_args()
    r = check(a.zip)
    if a.run:
        from core.runs import Run
        run = Run(a.run)
        run.log_step("zip_checks", **{k: v for k, v in r.items() if k != "missing"})
    print(json.dumps(r, indent=1))
    sys.exit(0 if r["pass"] else 1)
