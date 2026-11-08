"""v13b: one frame per re-rendered clip of a motion-fix run -> out/dwarika_v13b_fix_grid.jpg (red = caption line y=800, green = 5% margin)."""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import motion_assign as MA, motion_cards as MC, beats as B  # noqa: E402

run = sys.argv[1] if len(sys.argv) > 1 else "2026-11-04_KANG_001"
out = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / "out" / "dwarika_v13b_fix_grid.jpg")
rd = ROOT / "runs" / run
summ = json.loads((rd / "visuals_beats_v13b.json").read_text(encoding="utf-8"))
spec = MC.load_spec(); w, hw = MA.load_words()
plans = {p["id"]: p for p in MA.plan_all(spec, B.read_assign_csv(str(ROOT / summ["base_csv"])), w, hw)["plans"]}
picks = []
for i in summ["re_rendered"]:
    p = plans[i]; f = rd / "motion_clips" / f"{'MAP' if p['type'] == 'map' else 'CARD'}_{i}.mp4"
    if i.startswith("M0"):
        picks.append((i, f, p["start"] + 0.4, "start: sea label in 5% margin"))
    if i.startswith("M4"):
        picks.append((i, f, p["phases"][1]["end"] - 0.1, "phase 2 end: route vs caption line"))
        picks.append((i, f, p["end"] - 0.1, "phase 3: Sudarshan Setu"))
        continue
    if i.startswith("M1"):
        picks.append((i, f, 93.6, "135 km badge (phase 2)")); continue
    picks.append((i, f, p["end"] - 0.15, "end"))
tmp = Path(tempfile.mkdtemp()); tiles = []
for k, (i, f, T, lab) in enumerate(picks):
    o = tmp / f"{k}.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{T - plans[i]['start']:.3f}", "-i", str(f), "-frames:v", "1",
                    "-vf", "scale=640:360", str(o)], check=True)
    tiles.append((Image.open(o).convert("RGB"), f"{i}  t={T:.2f}s", lab))
font = ImageFont.truetype(str(ROOT / "fonts" / "Mukta-ExtraBold.ttf"), 17)
cols, tw, th = 4, 640, 360 + 46
sh = Image.new("RGB", (cols * tw, ((len(tiles) + cols - 1) // cols) * th), (20, 20, 20)); d = ImageDraw.Draw(sh)
for k, (im, a, b) in enumerate(tiles):
    x, y = (k % cols) * tw, (k // cols) * th; sh.paste(im, (x, y))
    d.line([(x, y + int(360 * 800 / 1080)), (x + tw, y + int(360 * 800 / 1080))], fill=(230, 50, 50), width=1)
    d.rectangle([x + 32, y + 18, x + tw - 32, y + 360 - 18], outline=(80, 220, 120), width=1)
    d.text((x + 4, y + 362), a, fill=(255, 220, 90), font=font); d.text((x + 4, y + 383), b, fill=(220, 220, 220), font=font)
Path(out).parent.mkdir(parents=True, exist_ok=True); sh.save(out, quality=88); print(out, len(tiles))
