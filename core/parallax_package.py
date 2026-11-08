"""Parallax commands (kang.py parallax / parallax-batch / parallax-ab / parallax-apply).
Every command is one run under runs/ with a manifest (inputs hashed, outputs listed). Originals are never touched:
clips are written into the run folder, depth maps into assets/depth_cache (sha256-keyed)."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from . import parallax as P
from .runs import Run, media_summary, write_json

ROOT = Path(__file__).resolve().parent.parent


def parallax_cmd(img: str, out: str, dur: float, *, move: str = "dolly", strength: float = 1.0, width: int = 1920,
                 fps: int = 25) -> Dict[str, Any]:
    run = Run()
    run.add_input(img, "IMG")
    h = int(round(width * 9 / 16 / 2)) * 2
    res = P.render(img, out, dur, move=move, strength=strength, w=width, h=h, fps=fps)
    if res.get("file"):
        run.add_output(res["file"], "parallax_clip")
    run.log_step("parallax", **{k: v for k, v in res.items() if k != "notes"}, notes="; ".join(res.get("notes", [])))
    run.set_status("done" if res["status"] in ("PASS", "WARN") else "qa_failed")
    return {"run_id": run.run_id, **res, "qa": {"pass": res["status"] in ("PASS", "WARN"), "status": res["status"]}}


def batch_cmd(assign_csv: str, *, run_id: Optional[str] = None, beats: Optional[Sequence[str]] = None,
              min_hold: float = 6.0, width: int = 1920, fps: int = 25, strength: float = 1.0,
              budget_s: float = 90.0) -> Dict[str, Any]:
    """Resumable: renders selected clips until budget_s is used; call again with --run to continue.
    Report CSV = runs/<id>/parallax_report.csv, clips in runs/<id>/parallax_clips/."""
    from . import beats as B
    run = Run(run_id) if run_id else Run()
    if not run_id:
        run.add_input(assign_csv, "VISUALS_BEATS")
    rows = B.read_assign_csv(assign_csv)
    sel = P.select_clips(rows, min_hold)
    if beats:
        want = set(beats)
        sel = [c for c in P.select_clips(rows, 0.0) if c["first_beat"] in want]
    rep_p = run.path("parallax_report.csv")
    done = {r["beat"]: r for r in P.read_report(rep_p)} if rep_p.is_file() else {}
    cdir = run.path("parallax_clips")
    cdir.mkdir(exist_ok=True)
    h = int(round(width * 9 / 16 / 2)) * 2
    est = P.HFDepth()
    t_start = time.time()
    report = list(done.values())
    for k, c in enumerate(sel):
        if c["first_beat"] in done:
            continue
        if time.time() - t_start > budget_s:
            break
        img = ROOT / c["source_dir"] / c["asset"]
        n = round(c["end"] * fps) - round(c["start"] * fps)
        move, direction = P.move_for(k)
        name = P.clip_name(c["asset"])
        res = P.render(img, cdir / name, n / fps, move=move, strength=strength, direction=direction, w=width, h=h,
                       fps=fps, estimator=est, frames=n,
                       alt_moves=[(m, direction) for m in P.MOVES if m != move])
        move = res.get("move", move)
        row = {"clip": c["index"], "beat": c["first_beat"], "scene": c["scene"], "asset": c["asset"],
               "source_dir": c["source_dir"], "match": c["match"], "duration_s": round(n / fps, 3), "move": move,
               "strength": res.get("strength"), "edge_sigma": res.get("edge_sigma"), "status": res["status"],
               "fold_px": res.get("fold_px"), "stretch_frac": res.get("stretch_frac"), "max_dev": res.get("max_dev"),
               "oob_frac": res.get("oob_frac"), "edge_black": res.get("edge_black", ""), "jitter_ratio": res.get("jitter_ratio", ""),
               "spike": res.get("spike", ""), "path_smooth": res.get("path_smooth", ""),
               "luma_diff_max": res.get("luma_diff_max", ""), "frames": n, "render_s": res.get("render_s", ""),
               "render_s_per_video_s": res.get("render_s_per_video_s", ""),
               "parallax_clip": name if res.get("file") else "",
               "fallback": "" if res.get("file") else "ken_burns", "notes": res.get("notes", [])}
        report.append(row)
        P.write_report(sorted(report, key=lambda r: int(r["clip"])), rep_p)
        if res.get("file"):
            run.add_output(res["file"], "parallax_clip")
    report = sorted(report, key=lambda r: int(r["clip"]))
    P.write_report(report, rep_p)
    remaining = [c["first_beat"] for c in sel if c["first_beat"] not in {r["beat"] for r in report}]
    counts: Dict[str, int] = {}
    for r in report:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    rps = [float(r["render_s_per_video_s"]) for r in report if str(r.get("render_s_per_video_s", "")) not in ("", "None")]
    if not remaining:
        run.add_output(rep_p, "parallax_report")
    run.log_step("parallax_batch", selected=len(sel), done=len(report), counts=counts)
    run.set_status("done" if not remaining else "partial")
    return {"run_id": run.run_id, "report": str(rep_p), "clips_dir": str(cdir), "selected": len(sel),
            "done": len(report), "remaining": remaining, "counts": counts,
            "render_s_per_video_s_avg": round(sum(rps) / len(rps), 3) if rps else None,
            "status": "done" if not remaining else "partial",
            **({"next": f"run again with --run {run.run_id}"} if remaining else {})}


def apply_cmd(assign_csv: str, report_csv: str, out: str, fps: int = 25) -> Dict[str, Any]:
    """visuals_beats.csv + parallax report -> new visuals_beats CSV with motion/parallax_clip columns."""
    from . import beats as B
    run = Run()
    run.add_input(assign_csv, "VISUALS_BEATS")
    run.add_input(report_csv, "PARALLAX_REPORT")
    rows = B.read_assign_csv(assign_csv)
    rep = P.read_report(report_csv)
    new, info = P.apply_parallax(rows, rep, Path(report_csv).parent / "parallax_clips", fps=fps)
    for r in new:
        if r.get("parallax_dir"):
            try:
                r["parallax_dir"] = Path(r["parallax_dir"]).resolve().relative_to(ROOT.resolve()).as_posix()
            except ValueError:
                pass
    op = B.write_assign_csv(new, run.path(Path(out).name))
    qa = B.assign_qa(new)
    run.add_output(op, "visuals_beats_csv")
    run.log_step("parallax_apply", **info, no_repeat=qa["pass"])
    run.set_status("done" if qa["pass"] else "qa_failed")
    return {"run_id": run.run_id, "csv": str(op), **info, "qa": {"pass": qa["pass"], "duplicates": qa["duplicates"]}}


# --------------------------------------------------------------------------- A/B preview + grid
def _label(img: np.ndarray, text: str) -> np.ndarray:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(str(ROOT / "fonts" / "Mukta-ExtraBold.ttf"), max(14, img.shape[0] // 18))
    d.rectangle([0, 0, im.width, f.size + 10], fill=(0, 0, 0))
    d.text((8, 2), text, fill=(255, 220, 90), font=f)
    return np.asarray(im)


def ab_cmd(items: Sequence[Dict[str, Any]], out_mp4: str, out_grid: str, *, seconds: float = 8.0, w: int = 640,
           fps: int = 25, run_id: Optional[str] = None) -> Dict[str, Any]:
    """items: [{img, label, dur (s, full clip length), move, direction, k (Ken Burns index), match}].
    A/B: for each item the first `seconds` of the move compressed from the full clip (frames sampled across the
    whole clip so the full travel is visible), Ken Burns left, parallax right. Grid: per item
    photo | depth | KB start | KB end | PX start | PX mid | PX end, plus a 2x crop of the strongest stretch area."""
    import cv2
    from PIL import Image
    run = Run(run_id) if run_id else Run()
    h = int(round(w * 9 / 16 / 2)) * 2
    tmp = Path(tempfile.mkdtemp(prefix="kang_pxab_"))
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                             f"{2 * w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp / "ab.mp4")],
                            stdin=subprocess.PIPE)
    rows_img, info = [], []
    from . import beats as B
    try:
        for it in items:
            run.add_input(it["img"], it["label"][:20].replace(" ", "_"))
            d, dinfo = P.depth_for(it["img"])
            rgb = P.load_rgb(it["img"])
            n = int(round(seconds * fps))
            st0 = it.get("strength", 1.0)
            tries = [(st0, s_) for s_ in P.FEATHER_PASSES] + [(round(st0 * 0.6, 3), P.FEATHER_PASSES[-1])]
            pick = P.choose_setting(rgb, d, 1920, 1080, it["move"], it.get("direction", 1), tries)
            wp_hi = pick["warper"]
            wp = P.Warper(rgb, d, w, h, it["move"], pick["strength"], it.get("direction", 1), edge_sigma=pick["edge_sigma"])
            res = {"label": it["label"], "move": it["move"], "strength": pick["strength"], "edge_sigma": pick["edge_sigma"],
                   **pick["geo"], "pre_gate": pick["status"], "why": pick["why"], "tried": pick["log"]}
            info.append(res)
            m = B.motion_for(it.get("k", 0), it.get("match", "exact"))
            src = B._cover_source(it["img"], w, h, m["smax"])
            for i in range(n):
                p = (i + 0.5) / n
                kb = np.asarray(B.frame_at(src, m, p, w, h))
                px = wp.frame(p)
                if i < fps * 1.5:
                    kb = _label(kb, f"Ken Burns | {it['label']}")
                    px = _label(px, f"Parallax 2.5D {it['move']} | {res['pre_gate']} | {it.get('dur', seconds):.0f}s move in {seconds:.0f}s")
                proc.stdin.write(np.hstack([kb, px]).tobytes())
            # grid row (higher-res frames, 1920 warper, shown at tile size)
            tw, th = 384, 216
            def tile(a, txt):
                return _label(cv2.resize(a, (tw, th), interpolation=cv2.INTER_AREA), txt)
            ih_, iw_ = rgb.shape[:2]
            ch_ = min(ih_, round(iw_ * 9 / 16))
            cw_ = min(iw_, round(ch_ * 16 / 9))
            y_, x_ = (ih_ - ch_) // 2, (iw_ - cw_) // 2
            photo = cv2.resize(np.ascontiguousarray(rgb[y_:y_ + ch_, x_:x_ + cw_]), (tw, th), interpolation=cv2.INTER_AREA)
            dep = cv2.applyColorMap((cv2.resize(wp_hi.depth, (tw, th)) * 255).astype(np.uint8), cv2.COLORMAP_INFERNO)[:, :, ::-1]
            src_hi = B._cover_source(it["img"], 1920, 1080, m["smax"])
            kb0, kb1 = (np.asarray(B.frame_at(src_hi, m, p, 1920, 1080)) for p in (0.0, 1.0))
            f0, f5, f1 = (wp_hi.frame(p) for p in (0.0, 0.5, 1.0))
            # crop around the strongest local stretch at p=1 (where artefacts would be)
            mx, my, r = wp_hi.maps(1.0)
            dev = np.abs(np.diff(mx, axis=1)[:-1, :] / r - 1.0)
            dev = cv2.GaussianBlur(dev, (0, 0), 15)
            yy, xx = np.unravel_index(int(np.argmax(dev)), dev.shape)
            x0, y0 = int(np.clip(xx - 192, 0, 1920 - 384)), int(np.clip(yy - 108, 0, 1080 - 216))
            crop = f1[y0:y0 + 216, x0:x0 + 384]
            row = np.hstack([_label(photo, "photo (centre 16:9)"), _label(dep, "depth (feathered)"), tile(kb0, "KB start"),
                             tile(kb1, "KB end"), tile(f0, "PX start"), tile(f5, "PX mid"), tile(f1, "PX end"),
                             _label(np.ascontiguousarray(crop), f"PX end 1:1 crop @({x0},{y0})")])
            hdr = np.zeros((30, row.shape[1], 3), np.uint8)
            hdr = _label(hdr, f"{it['label']}  move={res['move']} strength={res['strength']} feather={res['edge_sigma']}  "
                              f"gate(pre)={res['pre_gate']} fold={res['fold_px']} stretch={res['stretch_frac']:.2%} "
                              f"maxdev={res['max_dev']} oob={res['oob_frac']:.3%}")
            rows_img.append(np.vstack([hdr, row]))
    finally:
        proc.stdin.close()
        proc.wait()
    Path(out_mp4).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tmp / "ab.mp4", run.path(Path(out_mp4).name))
    shutil.move(str(tmp / "ab.mp4"), out_mp4)
    Image.fromarray(np.vstack(rows_img)).save(out_grid, quality=90)
    shutil.copy2(out_grid, run.path(Path(out_grid).name))
    run.add_output(run.path(Path(out_mp4).name), "parallax_ab")
    run.add_output(run.path(Path(out_grid).name), "parallax_grid")
    write_json(run.path("ab_info.json"), info)
    run.log_step("parallax_ab", items=len(items))
    run.set_status("done")
    pm = media_summary(out_mp4)
    return {"run_id": run.run_id, "ab": out_mp4, "grid": out_grid, "duration": round(pm["duration"], 2), "items": info}
