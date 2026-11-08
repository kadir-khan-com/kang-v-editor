"""Contact sheet: one thumbnail per BEAT row of a visuals_beats CSV (frame of the shot on screen at the beat's midpoint),
labelled with time, beat id and treatment (teaser / parallax / Ken Burns move / card / map / clip source / AI), plus the
picture-desk rule that touched the row (desk_rule). Frames come from the same files the package uses (video clips at
the right offset, stills via core.beats.frame_at at the beat's position inside its shot).

Usage: python scripts/contact_sheet.py VISUALS_CSV OUT_JPG [--run RUN_ID] [--cols 10] [--label v18]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import beats as B  # noqa: E402
from core import beats_package as bpk  # noqa: E402

FONT = ROOT / "fonts" / "Mukta-ExtraBold.ttf"
COLORS = {"TEASER": (255, 120, 220), "PARALLAX": (120, 200, 255), "AI MOTION": (255, 90, 90), "CARD": (255, 220, 80),
          "MAP": (80, 220, 200), "YOUTUBE CC": (255, 110, 110), "STOCK": (120, 230, 120), "CROP REUSE": (255, 170, 60),
          "OPENVERSE": (200, 140, 255), "KEN BURNS": (215, 215, 215)}


def treatment(c, r) -> str:
    sd, a = (c.get("source_dir") or "").lower(), c["asset"].lower()
    if a.startswith("tsr_"):
        return "TEASER"
    if c.get("ai_clip"):
        return "AI MOTION"
    if c["match"] == "text_card":
        return "CARD"
    if c["match"] == "map":
        return "MAP"
    if c.get("parallax_clip"):
        return "PARALLAX"
    if "youtube" in sd or a.startswith("ytc_"):
        return "YOUTUBE CC"
    if "pixabay" in sd or a.startswith("stk_"):
        return "STOCK"
    if c.get("reuse") == "crop_reuse":
        return "CROP REUSE"
    if "openverse" in sd:
        return "OPENVERSE"
    return "KEN BURNS"


def main() -> int:
    from PIL import Image, ImageDraw, ImageFont
    ap = argparse.ArgumentParser()
    ap.add_argument("visuals"); ap.add_argument("out")
    ap.add_argument("--run"); ap.add_argument("--cols", type=int, default=10); ap.add_argument("--label", default="v18")
    a = ap.parse_args()
    rows = B.read_assign_csv(a.visuals)
    clips = bpk._clips(rows)
    tw, th, lh = 288, 162, 46
    tmp = Path(tempfile.mkdtemp(prefix="kang_cs_"))
    tiles = []
    for k, r in enumerate(rows):
        mid = (r["start"] + r["end"]) / 2
        c = next(x for x in clips if x["start"] - 1e-6 <= mid < x["end"] + 1e-6)
        vp = c.get("ai_local") or c.get("parallax_local") or (c["path_local"] if Path(c["asset"]).suffix.lower()
                                                                in B.VIDEO_EXT else None)
        fp = tmp / f"t{k:03d}.jpg"
        if vp:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0.0, mid - c['start']):.3f}", "-i", vp,
                            "-frames:v", "1", "-update", "1", "-vf",
                            f"scale={tw}:{th}:force_original_aspect_ratio=increase,crop={tw}:{th}", str(fp)], check=True)
            im = Image.open(fp).convert("RGB")
        else:
            src = B._cover_source(c["path_local"], 576, 324, c["motion"]["smax"])
            p = (mid - c["start"]) / max(1e-6, c["end"] - c["start"])
            im = B.frame_at(src, c["motion"], p, 576, 324).resize((tw, th))
        tr = treatment(c, r)
        if tr == "KEN BURNS" or tr in ("OPENVERSE", "CROP REUSE"):
            tr2 = f"{tr} {c['motion']['type'].replace('zoom_', 'zoom ')}"
        else:
            tr2 = tr
        tiles.append((im, r, tr, tr2))
    font = ImageFont.truetype(str(FONT), 17)
    fs = ImageFont.truetype(str(FONT), 15)
    head = 64
    n_rows = (len(tiles) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * tw, head + n_rows * (th + lh)), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    d.text((12, 8), f"KANG {a.label} Dwarika - contact sheet, one frame per beat ({len(tiles)} beat rows) at beat midpoint. "
                    f"Label: start time, beat id, treatment; * = picture-desk change; pink = cold-open teaser",
           fill=(255, 255, 255), font=ImageFont.truetype(str(FONT), 22))
    d.text((12, 36), Path(a.visuals).resolve().relative_to(ROOT).as_posix() if Path(a.visuals).resolve().is_relative_to(ROOT)
           else a.visuals, fill=(170, 170, 170), font=fs)
    for k, (im, r, tr, tr2) in enumerate(tiles):
        x, y = (k % a.cols) * tw, head + (k // a.cols) * (th + lh)
        sheet.paste(im, (x, y))
        dr = [x for x in (r.get("desk_rule") or "").split(";") if x and x != "HOOK"]
        star = " *" + ",".join(sorted(set(dr))) if dr else ""
        if dr:
            d.rectangle((x, y, x + tw - 1, y + th - 1), outline=(255, 210, 60), width=3)
        if tr == "TEASER":
            d.rectangle((x, y, x + tw - 1, y + th - 1), outline=COLORS["TEASER"], width=3)
        d.text((x + 5, y + th + 2), f"{r['start']:.2f}s  {r['beat']}{star}", fill=(255, 255, 255), font=font)
        d.text((x + 5, y + th + 24), f"{tr2} | {r['match']}", fill=COLORS.get(tr, (220, 220, 220)), font=fs)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out, quality=86)
    if a.run:
        from core.runs import Run
        run = Run(a.run)
        dst = run.path(Path(a.out).name)
        sheet.save(dst, quality=86)
        run.add_input(a.visuals, "VISUALS_BEATS")
        run.add_output(dst, "contact_sheet")
        run.log_step("contact_sheet", beats=len(tiles), out=str(Path(a.out)))
        run.set_status("done")
    print({"out": a.out, "beats": len(tiles), "size": sheet.size})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
