"""v12 external-source layer: run wrappers for fetch-openverse / fetch-pixabay / asset-index-all / stock-sheet,
and `beats-stock` = fill beats of an existing visuals_beats CSV (v11) with eye-checked Openverse / Pixabay media.

Priority (per beat): exact photo / CC clip > parallax of the same-place photo > map / card > representative stock
(Openverse / Pixabay) > continued_with_motion. So stock only replaces `continued_with_motion` beats:
  * an exact same-place Openverse photo (title/tags name the shot's own place) may replace any continued beat of an
    exact shot (label exact);
  * representative stock starts only after the held photo / its parallax clip already ran hold_cap_s; from there
    every remaining continued beat of that hold gets its own stock item (the photo may not come back: no repeat).
Pixabay is never 'exact'. Video clips are trimmed to the beat (frame-exact, 1920x1080, 25 fps, H.264, no audio)
into the run folder with their own CREDITS.json (modification recorded); originals are never touched.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from . import beats as B
from . import stock_common as SC
from .runs import Run, media_summary, write_json

ROOT = Path(__file__).resolve().parent.parent
POOL_DIRS = ["assets/dwarika_beats_pool_v10", "assets/dwarika_fetch_v1", "assets/dwarika_fetch_v2", "assets/dwarika_fetch_v3",
             "assets/dwarika_real", "assets/dwarika_v8", "assets/dwarika_v9", "assets/dwarika_fix_v8"]
VID = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}


def _rel(p: Path) -> str:
    try:
        return Path(p).resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(Path(p).resolve())


def _pool_dirs(extra: Sequence[str] = ()) -> List[Path]:
    return [ROOT / d for d in list(POOL_DIRS) + list(extra) if (ROOT / d).is_dir()]


def _known_titles(dirs: Sequence[Path]) -> List[str]:
    out = []
    for d in dirs:
        cj = d / "CREDITS.json"
        if cj.is_file():
            data = json.loads(cj.read_text(encoding="utf-8"))
            out += [c.get("title", "") for c in (data if isinstance(data, list) else data.get("items", []))]
    return out


# --------------------------------------------------------------------------- fetch commands (one run each)
def fetch_openverse_cmd(out_dir: str, *, min_width: Optional[int] = None, queries_json: Optional[str] = None) -> Dict[str, Any]:
    from . import openverse_fetch as OV
    run = Run()
    cfg = SC.load_cfg()
    run.add_input(str(ROOT / "config" / "stock_sources.json"), "STOCK_CFG")
    if min_width:
        cfg["openverse"]["min_width"] = min_width
    qs = json.loads(Path(queries_json).read_text(encoding="utf-8")) if queries_json else cfg["openverse"]["queries"]
    pools = _pool_dirs()
    res = OV.fetch(qs, out_dir, cfg=cfg, pool_dirs=pools, known_titles=_known_titles(pools),
                   hash_cache=ROOT / "assets" / "_dhash_cache.json")
    out = Path(out_dir)
    for f in ("CREDITS.json", "CREDITS.txt", "rejected.json", "fetch_report.json"):
        if (out / f).is_file():
            run.add_output(out / f, f.split(".")[0].lower())
    for s in (out / "_seed").glob("*.json") if (out / "_seed").is_dir() else []:
        run.add_input(str(s), "SEED_" + s.stem)
    run.log_step("fetch_openverse", fetched=res["fetched"], rejected=res["rejected"], http=res["http"])
    run.set_status("done" if res["status"] != "FAIL" else "failed")
    return {"run_id": run.run_id, **res, "qa": {"pass": res["status"] != "FAIL", "status": res["status"]}}


def fetch_pixabay_cmd(out_dir: str, *, verify_only: bool = False, thumbs_only: bool = False,
                      kinds: Sequence[str] = ("video",), per_query: Optional[int] = None) -> Dict[str, Any]:
    from . import pixabay_fetch as PX
    run = Run()
    cfg = SC.load_cfg()
    run.add_input(str(ROOT / "config" / "stock_sources.json"), "STOCK_CFG")
    auth = [PX.verify_auth(cfg, kind=k) for k in kinds] if verify_only else []
    if verify_only:
        write_json(run.path("pixabay_auth.json"), auth)
        run.add_output(run.path("pixabay_auth.json"), "pixabay_auth")
        run.log_step("pixabay_verify_auth", auth=auth)
        ok = all(a["auth"] == "PASS" for a in auth)
        run.set_status("done" if ok else "failed")
        return {"run_id": run.run_id, "auth": auth, "qa": {"pass": ok}}
    qs = [q for q in cfg["pixabay"]["queries"] if q.get("kind", "video") in kinds]
    res = PX.fetch(qs, out_dir, cfg=cfg, per_query=per_query, thumbs_only=thumbs_only, pool_dirs=_pool_dirs())
    out = Path(out_dir)
    for f in ("CREDITS.json", "CREDITS.txt", "rejected.json", "fetch_report.json", "candidates.json"):
        if (out / f).is_file():
            run.add_output(out / f, f.split(".")[0].lower())
    run.log_step("fetch_pixabay", fetched=res["fetched"], candidates=res["candidates"], rejected=res["rejected"],
                 api_requests=res["api_requests"], cache_hits=res["cache_hits"])
    run.set_status("done" if res["status"] != "FAIL" else "failed")
    return {"run_id": run.run_id, **res, "qa": {"pass": res["status"] != "FAIL", "status": res["status"]}}


def index_cmd(dirs: Sequence[str], out: str) -> Dict[str, Any]:
    from .asset_index import build_master_index
    run = Run()
    r = build_master_index([ROOT / d if not Path(d).is_absolute() else Path(d) for d in dirs], out)
    run.add_output(out, "asset_index")
    ext = ("openverse", "pixabay")
    new_dups = [d for d in r["duplicates_sha256"] if any(e in d for e in ext)]
    status = "FAIL" if new_dups else ("WARN" if (r["problems"] or r["duplicates_sha256"]) else "PASS")
    run.log_step("asset_index_all", count=r["count"], by_source=r["by_source"], status=status,
                 old_cross_folder_copies=len(r["duplicates_sha256"]) - len(new_dups), new_source_duplicates=len(new_dups))
    run.set_status("done" if status != "FAIL" else "qa_failed")
    return {"run_id": run.run_id, **r, "duplicates_sha256": r["duplicates_sha256"][:10],
            "old_cross_folder_copies": len(r["duplicates_sha256"]) - len(new_dups), "new_source_duplicates": new_dups,
            "qa": {"pass": status != "FAIL", "status": status,
                   "note": "WARN = pre-existing copies of the same Commons photo in older asset folders / pre-existing "
                           "CREDITS sha mismatch; new Openverse/Pixabay items duplicate nothing"}}


# --------------------------------------------------------------------------- contact sheet for the eye check
def contact_sheet(items: Sequence[Dict[str, Any]], out: str | Path, cols: int = 4, tw: int = 480, th: int = 270) -> Path:
    """items: [{path (image or video), label}] -> labelled grid. Videos show 3 frames (25/50/75 %) side by side."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(str(ROOT / "fonts" / "Mukta-ExtraBold.ttf"), 15)
    tiles = []
    for it in items:
        p = Path(it["path"])
        if p.suffix.lower() in VID:
            frs = [SC.video_frame(p, f) for f in (0.25, 0.5, 0.75)]
            frs = [f for f in frs if f is not None]
            im = Image.new("RGB", (tw, th), (0, 0, 0))
            if frs:
                w3 = tw // len(frs)
                for k, f in enumerate(frs):
                    f = f.copy()
                    f.thumbnail((w3, th))
                    im.paste(f, (k * w3, (th - f.height) // 2))
        else:
            im = Image.open(p).convert("RGB")
            im.thumbnail((tw, th))
            bg = Image.new("RGB", (tw, th), (0, 0, 0))
            bg.paste(im, ((tw - im.width) // 2, (th - im.height) // 2))
            im = bg
        tiles.append((im, it["label"]))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, max(1, rows) * (th + 44)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for k, (im, lab) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * (th + 44)
        sheet.paste(im, (x, y))
        for j, line in enumerate(str(lab).split("\n")[:2]):
            d.text((x + 4, y + th + 2 + 20 * j), line[:58], fill=(255, 220, 90) if j == 0 else (220, 220, 220), font=font)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=86)
    return Path(out)


# --------------------------------------------------------------------------- stock pool + themes
def themes_for(text: str, cfg: Dict[str, Any]) -> List[str]:
    th: List[str] = []
    for kw, t in cfg["themes"]["keywords"]:
        if kw in (text or "") and t not in th:
            th.append(t)
    return th or list(cfg["themes"].get("default", []))


def stock_pool(dirs: Sequence[str | Path], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Eye-accepted items from Openverse / Pixabay folders (CREDITS.json); eye_rejects removed."""
    eye = cfg.get("eye_rejects", {})
    out = []
    for d in map(Path, dirs):
        cj = d / "CREDITS.json"
        if not cj.is_file():
            continue
        for c in json.loads(cj.read_text(encoding="utf-8")):
            key = f"{c['source']}:{c.get('openverse_id') or c.get('pixabay_id')}"
            if key in eye or not (d / c["file"]).is_file():
                continue
            kind = "video" if Path(c["file"]).suffix.lower() in VID else "image"
            text = c.get("title", "") + " " + (" ".join(c["tags"]) if isinstance(c.get("tags"), list) else c.get("tags", ""))
            th = cfg.get("pixabay", {}).get("theme_override", {}).get(key, c.get("theme"))
            out.append({**c, "theme": th, "dir": str(d), "kind": kind, "key": key, "text": text,
                        "duration": c.get("duration") or (media_summary(d / c["file"]).get("duration") if kind == "video" else None)})
    return out


def _places(text: str, rules: Dict[str, Any]) -> set:
    return set(B.title_places(text, rules))


def plan_stock(rows: Sequence[Dict[str, Any]], pool: Sequence[Dict[str, Any]], cfg: Dict[str, Any],
               rules: Dict[str, Any], v9_titles: Dict[str, str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Returns (new rows, decisions). Pure function (no files) so it is unit-testable."""
    ac = cfg["assign"]
    rows = [dict(r) for r in sorted(rows, key=lambda r: float(r["start"]))]
    clips = B.merge_clips(rows)
    by_beat = {r["beat"]: r for r in rows}
    used = {p["key"] for p in pool if p.get("_used")}
    used_names = {Path(r["asset"]).name for r in rows}
    decisions: List[Dict[str, Any]] = []
    for c in clips:
        beats = [by_beat[b] for b in c["beats"]]
        cont = [r for r in beats if r["role"] == "continued_with_motion"]
        if not cont:
            continue
        head = beats[0]
        title = head.get("title") or v9_titles.get(head["asset"], "") or head["asset"].replace("_", " ")
        shot_places = _places(title, rules) | _places(head["asset"].replace("_", " "), rules)
        real = shot_places - B.NON_PLACE_KEYS - set(rules.get("area_keys", []))
        cap = ac["hold_cap_exact_s"] if c["match"] == "exact" else ac["hold_cap_other_s"]
        replacing = False
        last_new: Optional[Dict[str, Any]] = None
        for r in beats:
            if r["role"] != "continued_with_motion":
                continue
            held = float(r["start"]) - float(head["start"])
            dur = float(r["end"]) - float(r["start"])
            pick, label, why_exact = None, None, ""
            # 1) exact same-place Openverse photo (any continued beat of an exact shot)
            if c["match"] == "exact" and real:
                for p in pool:
                    if p["key"] in used or p["source"] != "openverse":
                        continue
                    pp = _places(p["text"], rules)
                    if pp and (pp - B.NON_PLACE_KEYS) and (pp - B.NON_PLACE_KEYS) <= real:
                        pick, label, why_exact = p, "exact", f"names {'/'.join(sorted(pp))} = shot place"
                        break
            # 2) representative stock, after the hold cap (or once replacing started: the photo may not come back)
            if not pick and (replacing or held >= cap - 1e-6):
                th = themes_for(r["text"], cfg)
                best = None
                for p in pool:
                    if p["key"] in used:
                        continue
                    if p["kind"] == "video" and (p.get("duration") or 0) < dur + 0.3:
                        continue
                    if p["source"] == "openverse":
                        pp = _places(p["text"], rules) - B.NON_PLACE_KEYS
                        if pp and not pp <= shot_places:
                            continue  # another named spot than the shot shows
                        score = 2.0 if not pp else 2.5
                    else:
                        if p.get("theme") not in th:
                            continue
                        score = 3.0 - th.index(p["theme"]) * 0.5 + (0.3 if p["kind"] == "video" else 0.0)
                    if best is None or score > best[0]:
                        best = (score, p)
                if not best:  # no item for the beat's own themes: generic default views (sky / sea)
                    for p in pool:
                        if p["key"] in used or p["source"] != "pixabay" or p.get("theme") not in cfg["themes"].get("default", []):
                            continue
                        if p["kind"] == "video" and (p.get("duration") or 0) < dur + 0.3:
                            continue
                        sc = 1.0 - cfg["themes"]["default"].index(p["theme"]) * 0.2
                        if best is None or sc > best[0]:
                            best = (sc, p)
                if best:
                    pick, label = best[1], "representative"
            if pick:
                replacing = True
                used.add(pick["key"])
                pick["_used"] = True
                r.update(asset=pick["file"], source_dir=pick["dir"], asset_source=pick["source"], match=label,
                         licence=pick["licence"], title=pick.get("title", ""), source_page=pick.get("source_page", ""),
                         role="new_stock", parallax_clip="", parallax_dir="", parallax_status="",
                         notes=f"v12 {pick['source']} {pick['kind']} ({pick['key']}) "
                               + (f"exact: {why_exact}" if label == "exact" else
                                  f"representative: generic {pick.get('theme') or 'Dwarka-area'} view, NOT the narrated spot")
                               + "; agent-picked, eye-checked by agent, not human-reviewed")
                r["_pick"] = pick
                last_new = r
                decisions.append({"beat": r["beat"], "action": "replaced", "source": pick["source"], "kind": pick["kind"],
                                  "label": label, "item": pick["key"], "held_before_s": round(held, 2)})
            elif replacing and last_new is not None:
                # no unused item: the previous NEW item runs on (the held photo must not come back)
                r.update({k: last_new[k] for k in ("asset", "source_dir", "asset_source", "match", "licence", "title",
                                                   "source_page", "notes")}, role="continued_with_motion",
                         parallax_clip="", parallax_dir="", parallax_status="")
                r["_pick"] = last_new["_pick"]
                decisions.append({"beat": r["beat"], "action": "continued_new_item", "item": last_new["_pick"]["key"]})
            else:
                decisions.append({"beat": r["beat"], "action": "kept_hold", "held_before_s": round(held, 2),
                                  "cap_s": cap})
    return rows, decisions


def trim_video(src: str | Path, dst: str | Path, dur: float, fps: int = 25, size: Tuple[int, int] = (1920, 1080),
               offset: Optional[float] = None) -> Dict[str, Any]:
    """Frame-exact, cover-fit to size, constant fps, no audio. Offset defaults to centre the beat in the clip."""
    info = media_summary(src)
    sd = float(info.get("duration") or 0)
    n = round(dur * fps)
    off = offset if offset is not None else max(0.0, min(sd - n / fps - 0.05, (sd - n / fps) / 2))
    w, h = size
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},fps={fps},setsar=1"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{off:.3f}", "-i", str(src), "-an", "-vf", vf,
                        "-frames:v", str(n), "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", str(dst)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-300:])
    o = media_summary(dst)
    return {"offset": round(off, 3), "frames": n, "duration": o.get("duration"), "has_audio": o.get("has_audio"),
            "width": o.get("width"), "height": o.get("height")}


def stock_cmd(assign_csv: str, stock_dirs: Sequence[str], out: str, *, v9_assets: str = "assets/dwarika_v9",
              fps: int = 25, run_id: Optional[str] = None, budget_s: float = 95.0) -> Dict[str, Any]:
    """Resumable: trims until budget_s is used; call again with --run to continue (finished clips are kept)."""
    import time
    t0 = time.time()
    run = Run(run_id) if run_id else Run()
    if not run_id:
        run.add_input(assign_csv, "VISUALS_BEATS")
        run.add_input(str(ROOT / "config" / "stock_sources.json"), "STOCK_CFG")
    cfg = SC.load_cfg()
    rules = B.load_rules()
    for d in stock_dirs:
        cj = ROOT / d / "CREDITS.json" if not Path(d).is_absolute() else Path(d) / "CREDITS.json"
        if cj.is_file() and not run_id:
            run.add_input(str(cj), "CREDITS_" + Path(d).name)
    rows = B.read_assign_csv(assign_csv)
    pool = stock_pool([ROOT / d if not Path(d).is_absolute() else Path(d) for d in stock_dirs], cfg)
    v9c = ROOT / v9_assets / "CREDITS.json"
    v9_titles = {c["file"]: c.get("title", "") for c in json.loads(v9c.read_text(encoding="utf-8"))} if v9c.is_file() else {}
    new, decisions = plan_stock(rows, pool, cfg, rules, v9_titles)
    clips_dir = run.path("stock_clips")
    clips_dir.mkdir(exist_ok=True)
    trims: List[Dict[str, Any]] = []
    credits: List[Dict[str, Any]] = []
    pending: List[str] = []
    for c in B.merge_clips(new):
        r0 = next(r for r in new if r["beat"] == c["first_beat"])
        pick = r0.get("_pick")
        if not pick or r0["role"] not in ("new_stock", "continued_with_motion"):
            continue
        if pick["kind"] != "video":
            for b in c["beats"]:
                rr = next(r for r in new if r["beat"] == b)
                rr["source_dir"] = _rel(Path(pick["dir"]))
            continue
        dur = round(c["end"] * fps) / fps - round(c["start"] * fps) / fps
        name = f"STK_{c['first_beat']}_{pick['source']}_{pick.get('pixabay_id') or pick.get('openverse_id')}.mp4"
        done_p = clips_dir / (name + ".json")
        if (clips_dir / name).is_file() and done_p.is_file():
            t = json.loads(done_p.read_text(encoding="utf-8"))
        elif time.time() - t0 > budget_s:
            pending.append(c["first_beat"])
            continue
        else:
            t = trim_video(Path(pick["dir"]) / pick["file"], clips_dir / name, dur, fps=fps,
                           size=tuple(cfg["assign"]["video_size"]))
            done_p.write_text(json.dumps(t), encoding="utf-8")
        trims.append({"beat": c["first_beat"], "clip": name, "src": pick["file"], **t, "need_frames": round(dur * fps)})
        credits.append({k: v for k, v in pick.items() if k not in ("dir", "text", "_used", "key")} |
                       {"file": name, "original_file": pick["file"], "original_folder": _rel(Path(pick["dir"])),
                        "modified": f"trimmed to {dur:.2f} s from {t['offset']:.2f} s, scaled/cropped to 1920x1080, "
                                    f"{fps} fps, audio removed (KANG v12)"})
        for b in c["beats"]:
            rr = next(r for r in new if r["beat"] == b)
            rr["asset"], rr["source_dir"] = name, _rel(clips_dir)
    write_json(clips_dir / "CREDITS.json", credits)
    if pending:
        run.set_status("partial")
        return {"run_id": run.run_id, "status": "partial", "trimmed": len(trims), "pending": pending,
                "next": f"run again with --run {run.run_id}", "qa": {"pass": False}}
    for r in new:
        r.pop("_pick", None)
    qa = B.assign_qa(new)
    missing = [r["beat"] for r in new if not (ROOT / r["source_dir"] / r["asset"]).is_file()]
    bad_trim = [t["beat"] for t in trims if t["has_audio"] or abs((t["duration"] or 0) * fps - t["need_frames"]) > 1]
    rep_exact = [r["beat"] for r in new if r.get("asset_source") == "pixabay" and r["match"] != "representative"]
    probs = ([f"duplicates {qa['duplicates']}"] if qa["duplicates"] else []) + \
        ([f"missing files {missing[:5]}"] if missing else []) + ([f"trim length/audio {bad_trim}"] if bad_trim else []) + \
        ([f"pixabay labelled non-representative {rep_exact}"] if rep_exact else [])
    op = B.write_assign_csv(new, run.path(Path(out).name))
    summ = op.with_suffix(".json")
    write_json(summ, {"schema": "kang.beats_stock/1.0", "assign_csv": assign_csv, "stock_dirs": list(stock_dirs),
                      "decisions": decisions, "trims": trims, "qa": qa, "problems": probs,
                      "priority": "exact > parallax same place > map/card > representative stock > continued_with_motion",
                      "hold_caps": cfg["assign"], "selected_by": "agent_under_user_delegation", "human_reviewed": False})
    run.add_output(op, "visuals_beats_csv")
    run.add_output(summ, "visuals_beats_summary")
    for t in trims:
        run.add_output(clips_dir / t["clip"], "stock_clip")
    run.log_step("beats_stock", replaced=sum(1 for d in decisions if d["action"] == "replaced"), roles=qa["roles"])
    run.set_status("qa_failed" if probs else "done")
    return {"run_id": run.run_id, "csv": str(op), "summary": str(summ), "decisions": decisions, "trims": len(trims),
            "qa": {"pass": not probs, **qa}, "problems": probs}


def new_sources_grid(assign_csv: str, out: str, cols: int = 4) -> Dict[str, Any]:
    """Grid of every newly used external asset (one tile per clip) with label + source + beat."""
    rows = B.read_assign_csv(assign_csv)
    items = []
    for c in B.merge_clips(rows):
        r0 = next(r for r in rows if r["beat"] == c["first_beat"])
        if r0.get("asset_source") not in ("openverse", "pixabay"):
            continue
        items.append({"path": str(ROOT / r0["source_dir"] / r0["asset"]),
                      "label": f"{c['first_beat']} {c['end'] - c['start']:.1f}s {r0['match'].upper()} | {r0['asset_source']}"
                               f"{' video' if Path(r0['asset']).suffix.lower() in VID else ' photo'}\n"
                               f"{(r0.get('title') or '')[:40]} | {r0['licence'][:22]}"})
    run = Run()
    run.add_input(assign_csv, "VISUALS_BEATS")
    p = contact_sheet(items, out, cols=cols)
    shutil.copy2(p, run.path(Path(out).name))
    run.add_output(run.path(Path(out).name), "new_sources_grid")
    run.log_step("stock_grid", tiles=len(items))
    run.set_status("done")
    return {"run_id": run.run_id, "grid": str(p), "tiles": len(items)}
