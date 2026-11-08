"""Before/after grid of every beat whose asset changed between two visuals_beats CSVs (KANG v16).

usage: python scripts/changes_grid.py OLD.csv NEW.csv --out out/x.jpg
One row per changed shot (merged beats): left = old asset frame (still or video middle), right = new asset middle
frame; caption = beats, old -> new label + file names. UTF-8, no network.
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent


def frame(path: Path, w: int = 480) -> Image.Image:
    h = int(w * 9 / 16)
    if path.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
        im = Image.open(path).convert("RGB")
    else:
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip() or "1"
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{float(d) / 2:.2f}", "-i", str(path), "-frames:v", "1",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        from io import BytesIO
        im = Image.open(BytesIO(r.stdout)).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)))
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def rows(p):
    return {r["beat"]: r for r in csv.DictReader(open(p, encoding="utf-8-sig"))}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("old"); ap.add_argument("new"); ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    o, n = rows(a.old), rows(a.new)
    order = sorted(n, key=lambda b: float(n[b]["start"]))
    groups = []
    for b in order:
        if o[b]["asset"] == n[b]["asset"]:
            continue
        if groups and groups[-1]["new"] == n[b]["asset"] and groups[-1]["old"] == o[b]["asset"]:
            groups[-1]["beats"].append(b)
            continue
        groups.append({"beats": [b], "old": o[b]["asset"], "new": n[b]["asset"], "o": o[b], "n": n[b]})
    W, H, CAP = 480, 270, 46
    try:
        font = ImageFont.truetype(str(ROOT / "fonts" / "Mukta-ExtraBold.ttf"), 15)
    except Exception:  # pragma: no cover
        font = ImageFont.load_default()
    sheet = Image.new("RGB", (2 * W + 30, max(1, len(groups)) * (H + CAP) + 10), "white")
    d = ImageDraw.Draw(sheet)
    for i, g in enumerate(groups):
        y = i * (H + CAP) + 5
        for j, (r, key) in enumerate(((g["o"], "old"), (g["n"], "new"))):
            p = ROOT / r["source_dir"] / r["asset"]
            sheet.paste(frame(p, W), (10 + j * (W + 10), y + CAP))
        d.text((10, y + 2), f"{'+'.join(g['beats'])}  BEFORE {g['o']['match']}: {g['old'][:52]}", fill="black", font=font)
        d.text((10, y + 22), f"AFTER {g['n']['match']}: {g['new'][:70]}", fill=(0, 90, 0), font=font)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out, quality=88)
    print({"changed_shots": len(groups), "beats": sum(len(g["beats"]) for g in groups), "out": a.out})


if __name__ == "__main__":
    sys.exit(main())
