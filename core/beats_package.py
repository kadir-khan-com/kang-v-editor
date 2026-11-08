"""Beat layer commands (kang.py beats / beats-assign / beats-package / beats-preview / beats-grid).
Every command is one run under runs/ with a manifest (inputs hashed, outputs listed). Originals are never
overwritten: new pool stills go to their own folder, the package copies what it uses."""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path, PureWindowsPath
from typing import Any, Dict, List, Optional, Sequence

from . import beats as B
from .runs import Run, media_summary, run_ffmpeg, sha256_file, write_json

ROOT = Path(__file__).resolve().parent.parent


def _out(run: Run, out: str) -> Path:
    p = Path(out)
    return run.path(p.name) if str(p.parent) in ("", ".") else p


def _rel(p: Path) -> str:
    try:
        return Path(p).resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(Path(p).resolve())


def beats_cmd(words_path: str, scenes_path: str, out: str, *, min_s: float, target_s: float, max_s: float,
              anchor: str, fps: int = 25, visuals_csv: Optional[str] = None) -> Dict[str, Any]:
    from . import visuals as V
    run = Run()
    run.add_input(words_path, "W1")
    run.add_input(scenes_path, "SCENES")
    words = json.loads(Path(words_path).read_text(encoding="utf-8"))
    plan = json.loads(Path(scenes_path).read_text(encoding="utf-8"))
    forced = {}
    if visuals_csv:
        run.add_input(visuals_csv, "VISUALS_CSV")
        forced = B.forced_from_visuals(V.read_csv(visuals_csv), words)
    bp = B.segment(words, plan, min_s=min_s, target_s=target_s, max_s=max_s, anchor=anchor, fps=fps, forced=forced)
    probs = B.check_beats(bp, plan)
    pj, pc = B.write_beats(bp, _out(run, out))
    for p, k in ((pj, "beats_json"), (pc, "beats_csv")):
        run.add_output(p, k)
    run.log_step("beats", anchor=anchor, **bp["stats"], forced_cuts=len(forced), problems=len(probs))
    run.set_status("qa_failed" if probs else "done")
    return {"run_id": run.run_id, "json": str(pj), "csv": str(pc), "stats": bp["stats"], "anchor": anchor,
            "forced_v9_cuts": len(forced), "relaxed": bp["relaxed"], "problems": probs,
            "qa": {"pass": not probs, "problems": probs}}


def assign_cmd(beats_path: str, visuals_csv: str, pools: Sequence[str], out: str, *, assets: str,
               download_to: Optional[str] = None, top_n: int = 40, scenes_path: Optional[str] = None,
               no_new_downloads: bool = False, parallax_report: Optional[str] = None,
               allow_crop_reuse: bool = False, hinglish_words: Optional[str] = None) -> Dict[str, Any]:
    from . import visuals as V
    run = Run()
    run.add_input(beats_path, "BEATS")
    run.add_input(visuals_csv, "VISUALS_CSV")
    bp = json.loads(Path(beats_path).read_text(encoding="utf-8"))
    rows = V.read_csv(visuals_csv)
    adir = Path(assets)
    cred = json.loads((adir / "CREDITS.json").read_text(encoding="utf-8"))
    scenes_path = scenes_path or str(Path(beats_path).with_name("scenes.json"))
    plan = json.loads(Path(scenes_path).read_text(encoding="utf-8"))
    rules = B.load_rules()
    cands = B.pool_candidates(pools, plan, top_n=top_n)
    if no_new_downloads and download_to:  # only stills already downloaded (and eye-checked) may be used
        dc = Path(download_to) / "CREDITS.json"
        have = {c["title"]: c["file"] for c in json.loads(dc.read_text(encoding="utf-8"))} if dc.is_file() else {}
        for s_, cs in cands.items():
            for c in cs:
                if not c.get("local_file") and c["title"] in have:
                    c["local_file"] = str(Path(download_to) / have[c["title"]])
            cands[s_] = [c for c in cs if c.get("local_file")]
    exclude: List[str] = []
    dl: Dict[str, Any] = {"files": {}, "errors": []}
    for _ in range(4):
        res = B.assign(bp, rows, plan, cred, cands, rules, exclude_titles=exclude)
        need = [c for c in res["picks"] if not c.get("local_file")]
        if not need:
            break
        if not download_to:
            res["problems"].append(f"{len(need)} pool pick(s) not downloaded (give --download-to)")
            break
        dl = B.download_picks(need, download_to)
        bad = [e["title"] for e in dl["errors"]]
        for c in need:
            if c["title"] in dl["files"]:
                c["local_file"] = dl["files"][c["title"]]
        if not bad:
            res = B.assign(bp, rows, plan, cred, cands, rules, exclude_titles=exclude)
            break
        exclude += bad
    for r in res["rows"]:  # asset = file name, source_dir = its folder (relative to the KANG root)
        if r["asset_source"] == "v9":
            r["source_dir"] = _rel(adir)
        else:
            lf = Path(r.pop("_cand", {}).get("local_file") or r["asset"])
            r["asset"], r["source_dir"] = lf.name, _rel(lf.parent)
        r.pop("_cand", None)
    px_info: Dict[str, Any] = {}
    if parallax_report:  # same photo, same label, motion = parallax_2_5d where the clip passed the gate
        from . import parallax as P
        run.add_input(parallax_report, "PARALLAX_REPORT")
        res["rows"], px_info = P.apply_parallax(res["rows"], P.read_report(parallax_report),
                                                Path(parallax_report).parent / "parallax_clips")
        for r in res["rows"]:
            if r.get("parallax_dir"):
                r["parallax_dir"] = _rel(Path(r["parallax_dir"]))
    crop_info: Dict[str, Any] = {}
    if allow_crop_reuse:  # v14: same photo again only as a distinctly different crop (config beat_rules.json crop_reuse)
        res["rows"], crop_info = _crop_pass(run, res["rows"], bp, hinglish_words)
        res["problems"] += crop_info.get("problems", [])
    qa = B.assign_qa(res["rows"])
    missing = [r["beat"] for r in res["rows"] if not (ROOT / r["source_dir"] / r["asset"]).is_file()]
    probs = res["problems"] + ([f"asset file missing for {len(missing)} beat(s): {missing[:5]}"] if missing else []) + \
        ([f"duplicate assets: {qa['duplicates']}"] if qa["duplicates"] else [])
    op = B.write_assign_csv(res["rows"], _out(run, out))
    summ = op.with_suffix(".json")
    write_json(summ, {"schema": "kang.beats_assign/1.0", "beats": beats_path, "visuals_csv": visuals_csv,
                      "pools": list(pools), "top_n": top_n, "qa": qa, "problems": probs, "rejects": res["rejects"],
                      "download_errors": dl.get("errors", []), "selected_by": "agent_under_user_delegation",
                      "human_reviewed": False})
    run.add_output(op, "visuals_beats_csv")
    run.add_output(summ, "visuals_beats_summary")
    run.log_step("beats_assign", **{k: qa[k] for k in ("beats", "shots", "unique_assets")}, roles=qa["roles"])
    run.set_status("qa_failed" if probs else "done")
    return {"run_id": run.run_id, "csv": str(op), "summary": str(summ), "qa": {"pass": not probs, **qa},
            "problems": probs, "download_errors": dl.get("errors", []), "rejected_candidates": len(res["rejects"]),
            **({"parallax": px_info} if parallax_report else {}), **({"crop_reuse": crop_info} if allow_crop_reuse else {})}


HWORDS_DEFAULT = ROOT / "runs" / "2026-11-01_KANG_001" / "words_hinglish_v1_accepted.json"


def _crop_pass(run: Run, rows: List[Dict[str, Any]], bp: Dict[str, Any], hinglish_words: Optional[str]):
    """Plan + cut crop reuses into run/crop_reuse/, apply them to the rows, re-check the rules. -> (rows, info)."""
    from . import crop_reuse as C
    hp = Path(hinglish_words) if hinglish_words else HWORDS_DEFAULT
    run.add_input(str(hp), "W_HINGLISH")
    run.add_input(str(ROOT / "config" / "beat_rules.json"), "BEAT_RULES")
    if C.FACE_MODEL.is_file():
        run.add_input(str(C.FACE_MODEL), "FACE_MODEL_YUNET")
    hw = json.loads(hp.read_text(encoding="utf-8"))["words"]
    rules = B.load_rules()
    plan = C.plan_crop_reuse(rows, bp, hw, rules)
    cdir = run.path("crop_reuse")
    C.write_crops(plan["reuses"], cdir)
    new = C.apply_reuses(rows, plan["reuses"], _rel(cdir))
    probs = C.crop_qa(new, plan["reuses"], rules)
    write_json(run.path("crop_reuse_plan.json"), {"schema": "kang.crop_reuse/1.0", "settings": C.settings(rules), **plan,
                                                  "problems": probs, "human_reviewed": False})
    run.add_output(run.path("crop_reuse_plan.json"), "crop_reuse_plan")
    run.add_output(cdir / "CREDITS.json", "crop_reuse_credits")
    for u in plan["reuses"]:
        run.add_output(cdir / u["file"], "crop_reuse_still")
    info = {"used": len(plan["reuses"]), "considered": plan["considered"], "skipped": plan["skipped"],
            "rejected_by_eye": len(C.settings(rules).get("rejects", {})), "problems": probs,
            "reuses": [{k: u[k] for k in ("beat", "kind", "asset", "box", "area_ratio", "iou_max", "score", "first_beat", "file")}
                       for u in plan["reuses"]]}
    return new, {**info, "plan": plan}


def crop_reuse_cmd(assign_csv: str, beats_path: str, out: str, *, hinglish_words: Optional[str] = None,
                   grid: Optional[str] = None) -> Dict[str, Any]:
    """v14: the crop-reuse pass of `beats-assign --allow-crop-reuse` on an existing visuals_beats CSV (keeps every
    later layer: parallax, stock, cards, maps) -> new CSV + crop stills + CREDITS + optional first-framing/crop grid."""
    from . import crop_reuse as C
    run = Run()
    run.add_input(assign_csv, "VISUALS_BEATS")
    run.add_input(beats_path, "BEATS")
    bp = json.loads(Path(beats_path).read_text(encoding="utf-8"))
    rows = B.read_assign_csv(assign_csv)
    new, info = _crop_pass(run, rows, bp, hinglish_words)
    plan = info.pop("plan")
    qa = B.assign_qa(new)
    missing = [r["beat"] for r in new if not (ROOT / r["source_dir"] / r["asset"]).is_file()]
    never = [r["beat"] for r, o in zip(sorted(new, key=lambda r: r["start"]), sorted(rows, key=lambda r: r["start"]))
             if r.get("reuse") and (o["match"] in ("exact", "text_card", "map", "archival") and o["role"] != "continued_with_motion")]
    probs = info["problems"] + ([f"duplicates {qa['duplicates']}"] if qa["duplicates"] else []) + \
        ([f"missing files {missing[:5]}"] if missing else []) + ([f"replaced a protected beat {never}"] if never else [])
    op = B.write_assign_csv(new, _out(run, out))
    write_json(op.with_suffix(".json"), {"schema": "kang.crop_reuse_assign/1.0", "base_csv": _rel(Path(assign_csv)),
                                         "qa": qa, "problems": probs, "crop_reuse": info, "selected_by": "agent_under_user_delegation",
                                         "human_reviewed": False})
    run.add_output(op, "visuals_beats_csv")
    run.add_output(op.with_suffix(".json"), "visuals_beats_summary")
    res = {"run_id": run.run_id, "csv": str(op), "used": info["used"], "considered": info["considered"],
           "skipped": info["skipped"], "reuses": info["reuses"], "labels": qa["labels_by_shot"], "roles": qa["roles"],
           "shots": qa["shots"], "shot_stats": qa["shot_stats"], "problems": probs, "qa": {"pass": not probs}}
    if grid:
        g = C.crop_grid(plan["reuses"], grid, crop_dir=run.path("crop_reuse"))
        shutil.copy2(g, run.path(Path(grid).name))
        run.add_output(run.path(Path(grid).name), "crop_grid")
        res["grid"] = str(g)
    run.log_step("crop_reuse", used=info["used"], considered=info["considered"], skipped=len(info["skipped"]),
                 roles=qa["roles"], labels=qa["labels_by_shot"])
    run.set_status("qa_failed" if probs else "done")
    return res


AI_MODEL_NAME = "Wan2.2-TI2V-5B"
AI_MODEL_LICENCE = "Apache-2.0"
AI_MODEL_URL = "https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B-Diffusers"


def _clips(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    clips = B.merge_clips(rows)
    first = {r["beat"]: r for r in rows}
    for c in clips:
        c["path_local"] = str(ROOT / c["source_dir"] / c["asset"])
        r0 = first[c["first_beat"]]
        dm = r0.get("desk_motion", "")
        if dm in ("zoom_in", "zoom_out") and c["motion"]["type"] != dm:
            # v18 picture desk (core/picture_desk.py) chose the move; same zoom range / drift, direction swapped
            m = c["motion"]
            m["type"], m["s0"], m["s1"] = dm, m["s1"], m["s0"]
        if r0.get("parallax_clip"):  # same photo rendered as 2.5D parallax (all its beats carry the same clip)
            c["parallax_clip"] = r0["parallax_clip"]
            c["parallax_local"] = str(ROOT / r0["parallax_dir"] / r0["parallax_clip"])
            c["parallax_status"] = r0.get("parallax_status", "")
        if r0.get("ai_motion_clip"):  # v17: AI motion clip of the same photo (masked composite, core/ai_motion.py)
            c["ai_clip"] = r0["ai_motion_clip"]
            c["ai_local"] = str(ROOT / r0["ai_motion_dir"] / r0["ai_motion_clip"])
            c["ai_status"] = r0.get("ai_motion_status", "")
            c["ai_model"] = r0.get("ai_motion_model", "")
    return clips


def package_cmd(media: str, words_path: str, scenes_path: str, beats_path: str, assign_csv: str, *, captions: str,
                win_root: Optional[str], fps: int = 25, extras: Sequence[str] = (), zip_out: Optional[str] = None,
                selected_by: str = "agent_under_user_delegation") -> Dict[str, Any]:
    from . import premiere
    run = Run()
    inp = run.add_input(media, "A1")
    for p, k in ((words_path, "W1"), (scenes_path, "SCENES"), (beats_path, "BEATS"), (assign_csv, "VISUALS_BEATS"),
                 (captions, "CAPTIONS")):
        run.add_input(p, k)
    ms = media_summary(media)
    plan = json.loads(Path(scenes_path).read_text(encoding="utf-8"))
    bp = json.loads(Path(beats_path).read_text(encoding="utf-8"))
    rows = B.read_assign_csv(assign_csv)
    clips = _clips(rows)
    qa_a = B.assign_qa(rows)
    checks: List[Dict[str, Any]] = [{"name": "beats_contiguous", "pass": not B.check_beats(bp, plan),
                                     "detail": B.check_beats(bp, plan)[:5]},
                                    {"name": "no_repeated_asset", "pass": qa_a["pass"], "detail": qa_a["duplicates"]}]
    pkg = run.path("premiere_package")
    (pkg / "media").mkdir(parents=True, exist_ok=True)
    (pkg / "visuals").mkdir(exist_ok=True)
    mname = Path(media).name
    shutil.copy2(media, pkg / "media" / mname)
    base = PureWindowsPath(win_root) if win_root else None
    seq_end = B.seq_end_of(ms["duration"], fps)
    vclips = []
    n_px = 0
    n_vid = 0
    n_motion = 0
    n_ai = 0
    for c in clips:
        if c.get("ai_clip"):
            dst = pkg / "visuals" / c["ai_clip"]
            if not dst.exists():
                shutil.copy2(c["ai_local"], dst)
            vi = media_summary(dst)
            n_fr = round(min(c["end"], seq_end) * fps) - round(c["start"] * fps)
            vclips.append({"path": str(base / "visuals" / dst.name) if base else str(dst.resolve()), "name": dst.name,
                           "width": vi.get("width"), "height": vi.get("height"), "kind": "video",
                           "start": c["start"], "end": min(c["end"], seq_end), "in": 0.0,
                           "src_duration": max(n_fr, round(vi.get("duration", 0) * fps)) / fps, "loop": False})
            c["ai_frames_file"] = round(vi.get("duration", 0) * fps)
            c["ai_frames_need"] = n_fr
            c["ai_has_audio"] = bool(vi.get("has_audio"))
            c["ai_size"] = (vi.get("width"), vi.get("height"))
            n_ai += 1
            continue
        if c.get("parallax_clip"):
            dst = pkg / "visuals" / c["parallax_clip"]
            if not dst.exists():
                shutil.copy2(c["parallax_local"], dst)
            vi = media_summary(dst)
            n_fr = round(c["end"] * fps) - round(min(c["start"], seq_end) * fps)
            vclips.append({"path": str(base / "visuals" / dst.name) if base else str(dst.resolve()), "name": dst.name,
                           "width": vi.get("width"), "height": vi.get("height"), "kind": "video",
                           "start": c["start"], "end": min(c["end"], seq_end), "in": 0.0,
                           "src_duration": max(n_fr, round(vi.get("duration", 0) * fps)) / fps, "loop": False})
            c["px_frames_file"] = round(vi.get("duration", 0) * fps)
            c["px_frames_need"] = round(min(c["end"], seq_end) * fps) - round(c["start"] * fps)
            n_px += 1
            continue
        dst = pkg / "visuals" / c["asset"]
        if not dst.exists():
            shutil.copy2(c["path_local"], dst)
        vi = media_summary(dst)
        if dst.suffix.lower() in B.VIDEO_EXT:  # v12 stock clip, already trimmed to its beats (no audio, no keyframes)
            n_fr = round(min(c["end"], seq_end) * fps) - round(c["start"] * fps)
            f_fr = round((vi.get("duration") or 0) * fps)
            vclips.append({"path": str(base / "visuals" / dst.name) if base else str(dst.resolve()), "name": dst.name,
                           "width": vi.get("width"), "height": vi.get("height"), "kind": "video",
                           "start": c["start"], "end": min(c["end"], seq_end), "in": 0.0,
                           "src_duration": max(n_fr, f_fr) / fps, "loop": False})
            c["vid_frames_file"], c["vid_frames_need"], c["vid_has_audio"] = f_fr, n_fr, bool(vi.get("has_audio"))
            n_vid += 1
            if c["match"] in ("text_card", "map"):
                n_motion += 1
            continue
        vclips.append({"path": str(base / "visuals" / dst.name) if base else str(dst.resolve()), "name": dst.name,
                       "width": vi.get("width"), "height": vi.get("height"), "kind": "still",
                       "start": c["start"], "end": min(c["end"], seq_end), "in": 0.0, "src_duration": c["end"] - c["start"],
                       "loop": False, "motion": c["motion"]})
    markers = [{"at": s["start"], "name": f"{s['id']} {s['title']}"[:80], "comment": s["text"][:500]} for s in plan["scenes"]]
    markers += [{"at": b["start"], "name": b["id"], "comment": " ".join(b["text"].split()[:8])} for b in bp["beats"]]
    markers.sort(key=lambda m: (m["at"], 0 if " " in m["name"] else 1))
    xml, stats = premiere.build_xmeml(
        f"KANG {run.run_id} beats", {"path": str(base / "media" / mname) if base else str((pkg / "media" / mname).resolve()),
                                     "name": mname, "duration": ms["duration"], "has_video": ms["has_video"],
                                     "channels": ms.get("channels", 2), "sample_rate": ms.get("sample_rate", 48000)},
        [[0.0, ms["duration"]]], fps=fps, markers=markers, visual_clips=vclips)
    (pkg / "sequence.xml").write_text(xml, encoding="utf-8")
    checks.append(premiere.check_xmeml(xml, fps))
    checks.append({"name": "beat_markers", "pass": stats["markers"] == len(plan["scenes"]) + len(bp["beats"]),
                   "detail": {"markers": stats["markers"], "beats": len(bp["beats"]), "scenes": len(plan["scenes"])}})
    checks.append({"name": "motion_on_every_still", "pass": stats["motion_clipitems"] == stats["visual_clipitems"] - n_px - n_vid - n_ai,
                   "detail": {"motion": stats["motion_clipitems"], "visual": stats["visual_clipitems"], "parallax_clips": n_px,
                              "stock_video_clips": n_vid, "ai_motion_clips": n_ai}})
    if n_vid:
        bad = [c["first_beat"] for c in clips if "vid_frames_file" in c and
               (c["vid_frames_file"] < c["vid_frames_need"] or c["vid_has_audio"])]
        checks.append({"name": "stock_clips_cover_their_beats_no_audio", "pass": not bad,
                       "detail": {"stock_video_clips": n_vid, "short_or_audio": bad}})
    pix_exact = [c["first_beat"] for c in clips if "pixabay" in (c.get("source_dir", "") + c["asset"]).lower()
                 and c["match"] != "representative"]
    checks.append({"name": "pixabay_representative_only", "pass": not pix_exact, "detail": pix_exact})
    if qa_a.get("crop_reuses"):
        crop_bad = []
        for c in clips:
            if c.get("reuse") != "crop_reuse":
                continue
            vi_ = media_summary(ROOT / c["source_dir"] / c["asset"])
            if (vi_.get("width") or 0) < 1280 or not c.get("reuse_of") or not c.get("crop_box"):
                crop_bad.append(c["first_beat"])
        checks.append({"name": "crop_reuse_files_ok", "pass": not crop_bad,
                       "detail": {"crop_reuses": qa_a["crop_reuses"], "bad": crop_bad}})
    if n_px:
        short = [c["first_beat"] for c in clips if c.get("parallax_clip") and c["px_frames_file"] < c["px_frames_need"]]
        checks.append({"name": "parallax_clips_cover_their_beats", "pass": not short,
                       "detail": {"parallax_clips": n_px, "too_short": short}})
    if n_ai:
        bad_ai = [c["first_beat"] for c in clips if c.get("ai_clip") and
                  (c["ai_frames_file"] < c["ai_frames_need"] or c["ai_has_audio"] or c["ai_size"] != (1920, 1080)
                   or c["match"] not in ("exact", "representative"))]
        checks.append({"name": "ai_motion_clips_cover_their_beats_1080p_no_audio_label_kept", "pass": not bad_ai,
                       "detail": {"ai_motion_clips": n_ai, "bad": bad_ai}})
    shutil.copy2(captions, pkg / "captions.srt")
    for p, n in ((scenes_path, "scenes.json"), (words_path, "words.json"), (beats_path, "beats.json"),
                 (assign_csv, "visuals_beats.csv")):
        shutil.copy2(p, pkg / n)
    for e in extras:
        shutil.copy2(e, pkg / Path(e).name)
    # credits: exactly the assets on the timeline
    creds, missing_cred = [], []
    by_dir: Dict[str, Dict[str, Any]] = {}
    for c in clips:
        d = c["source_dir"]
        if d not in by_dir:
            cj = ROOT / d / "CREDITS.json"
            by_dir[d] = {x["file"]: x for x in json.loads(cj.read_text(encoding="utf-8"))} if cj.is_file() else {}
        rec = by_dir[d].get(c["asset"])
        if rec:
            extra = {"motion": "parallax_2_5d", "timeline_file": c["parallax_clip"],
                     "modified": "depth-based 2.5D camera motion rendered from this photo by KANG "
                                 "(Depth Anything V2 Small depth map); content not altered or generated"} \
                if c.get("parallax_clip") else {}
            if c.get("ai_clip"):
                extra = {"motion": "ai_animated", "timeline_file": c["ai_clip"], "ai_model": c.get("ai_model", ""),
                         "ai_model_licence": AI_MODEL_LICENCE,
                         "modified": f"modified (AI motion): subtle natural motion (water / clouds / flag) generated by "
                                     f"{c.get('ai_model', 'AI model')} ({AI_MODEL_LICENCE}) from this photo and composited "
                                     "back only on moving sky / water / flag pixels; every other pixel is the original "
                                     "photo; on-screen label 'AI animated'"}
            creds.append({**rec, "file": c["asset"], "used_on_beats": c["beats"], "match": c["match"], **extra,
                          **({"reuse": "crop_reuse", "reuse_of": c.get("reuse_of", ""), "crop_box": c.get("crop_box", "")}
                             if c.get("reuse") == "crop_reuse" else {})})
        else:
            missing_cred.append(c["asset"])
    # v13: geographic data sources of the map clips (config/data_licenses.json), credited in full
    data_lic = ROOT / "config" / "data_licenses.json"
    data_src = []
    if data_lic.is_file() and any(c["asset"].startswith("MAP_") for c in clips):
        run.add_input(str(data_lic), "DATA_LICENSES")
        data_src = json.loads(data_lic.read_text(encoding="utf-8")).get("sources", [])
        for d in data_src:
            creds.append({"file": f"data_source:{d['id']}", "kind": "data_source", "title": d.get("name", ""),
                          "author": d.get("credit", ""), "licence": d.get("licence", ""),
                          "licence_url": d.get("licence_url", ""), "source_page": d.get("url", ""),
                          "credit": d.get("credit", ""), "attribution_required": d.get("attribution_required"),
                          "match": "map_data", "used_in": "MAP_*.mp4",
                          **({"elements": d["elements"]} if d.get("elements") else {}),
                          **({"items": d["items"]} if d.get("items") else {}),
                          **({"share_alike_note": d["share_alike_note"]} if d.get("share_alike_note") else {})})
    if n_ai:
        models = sorted({c.get("ai_model", "") for c in clips if c.get("ai_clip")})
        for mname_ in models:
            creds.append({"file": f"model:{mname_}", "kind": "ai_model", "title": mname_, "author": "Wan Team (Alibaba)",
                          "licence": AI_MODEL_LICENCE, "licence_url": AI_MODEL_URL, "source_page": AI_MODEL_URL,
                          "match": "ai_model", "used_in": "AI_*.mp4 (motion: ai_animated)",
                          "note": "image-to-video model used only to add subtle natural motion to real photos"})
    write_json(pkg / "CREDITS.json", creds)
    lines = ["Credits for every still / clip on the timeline (rights recorded, NOT cleared). Own text cards / maps: KANG, fonts Mukta + "
             "Montserrat (SIL OFL 1.1). Pixabay items: Pixabay Content License (not CC), credited anyway.",
             "Map data (MAP_*.mp4): Natural Earth 1:10m (public domain); © OpenStreetMap contributors (ODbL 1.0, "
             "https://www.openstreetmap.org/copyright); place coordinates Wikidata (CC0)."]
    for d in data_src:
        lines.append(f"DATA {d['id']}: {d.get('name', '')} -- {d.get('licence', '')} ({d.get('licence_url', '')}) {d.get('url', '')}"
                     f" -- credit line: \"{d.get('credit', '')}\" (attribution required: {d.get('attribution_required')})"
                     + (" -- elements: " + "; ".join(f"{e['type']} {e['id']} {e.get('name', '')}" for e in d["elements"])
                        if d.get("elements") else "")
                     + (" -- items: " + "; ".join(d["items"]) if d.get("items") else ""))
    for x in creds:
        if x.get("kind") == "ai_model":
            lines.append(f"AI MODEL {x['title']}: {x['licence']} ({x['licence_url']}) -- used for {x['used_in']}; "
                         "output clips are labelled 'AI animated' on screen")
            continue
        if x.get("kind") == "data_source":
            continue
        lines.append(f"{x['file']}: \"{x.get('title', '').replace('File:', '')}\" by {x.get('author') or 'unknown'}, "
                     f"{x.get('licence', '')} {('(' + x['licence_url'] + ')') if x.get('licence_url') else ''} "
                     f"{x.get('source_page', '')} [{x['match']}]".rstrip()
                     + (f" -- on timeline as {x['timeline_file']} (motion: ai_animated, AI animated with {x.get('ai_model', '')} "
                        f"({x.get('ai_model_licence', '')}), modified (AI motion))"
                        if x.get("timeline_file") and x.get("motion") == "ai_animated" else
                        f" -- on timeline as {x['timeline_file']} (motion: parallax_2_5d, modified: depth-based camera move)"
                        if x.get("timeline_file") else "")
                     + (f" -- CROP REUSE of {x.get('reuse_of', '')} (crop_box {x.get('crop_box', '')})"
                        if x.get("reuse") == "crop_reuse" else "")
                     + (f" -- modified: {x['modified']}" if x.get("modified") and not x.get("timeline_file") else ""))
    (pkg / "CREDITS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    checks.append({"name": "credits_cover_every_asset", "pass": not missing_cred, "detail": missing_cred})
    labels = qa_a["labels_by_shot"]
    roles = qa_a["roles"]
    shot = qa_a["shot_stats"]
    (pkg / "README_IMPORT.txt").write_text(
        f"KANG Premiere package - beat layer (v10 beats, v11 parallax, v12 Openverse/Pixabay, v13 moving cards + map) ({run.run_id})\n"
        "Target: Premiere Pro 24.6.1. Premiere import of THIS package: NOT_TESTED.\n"
        f"Beats: {len(bp['beats'])} (anchor {bp['anchor']}: cut = word onset {bp['shift_s']:+.2f} s, frame-aligned at {fps} fps); "
        f"one sequence marker per beat (name = beat id, comment = first words) plus {len(plan['scenes'])} scene markers.\n"
        f"Video track V1: {stats['visual_clipitems']} shots (avg {shot['avg_s']} s, median {shot['median_s']} s, max {shot['max_s']} s); "
        f"{qa_a['unique_assets']} unique files, none repeated"
        + (f"; {qa_a.get('crop_reuses', 0)} of them are CROP REUSES (visuals/CR_*.jpg = a distinctly different crop of a photo\n"
           "  already on the timeline, e.g. full temple first, later only the spire; crop area <= 50 % of the first framing, IoU <= 0.3,\n"
           "  >= 4 beats apart, max 2 per photo, >= 1280 px wide; label = the photo's own label; visuals_beats.csv reuse=crop_reuse +\n"
           "  crop_box; CREDITS: crop = modification of the original photo)" if qa_a.get("crop_reuses") else "") + ".\n"
        + (f"Stock video clips (v12): {n_vid - n_motion} (visuals/STK_*.mp4, Pixabay Content License or CC, trimmed to their beats,\n"
           f"  1920x1080 {fps} fps H.264, NO audio, no motion keyframes). Label always 'representative' for Pixabay.\n" if n_vid - n_motion else "")
        + (f"Motion graphics (v13): {n_motion} own-work MP4s (visuals/CARD_*.mp4 moving text cards, visuals/MAP_*.mp4 route maps),\n"
           f"  1920x1080 {fps} fps H.264, NO audio, each covers exactly its beats. Every number / time / name on them is read from\n"
           "  the narration words (card_values.csv: word ids + times). Maps: Natural Earth (public domain) + OpenStreetMap\n"
           "  (ODbL, '© OpenStreetMap contributors', credited on-frame); routes are schematic, distances as narrated.\n" if n_motion else "")
        + (f"Cold open (v18): {roles.get('teaser', 0)} teaser shots (visuals/TSR_*.mp4, 1920x1080 {fps} fps H.264, NO audio) over the\n"
           "  UNCHANGED opening narration (no time inserted): sections of YouTube CC clips / the AI motion clip already credited,\n"
           "  with a burned-in Hinglish title (own text, card style). They count among the stock/video clips above; credits:\n"
           "  CREDITS.json 'teaser': true + 'modified'. Picture desk (v18): shot cuts moved to other word onsets (lead rule) or\n"
           "  merged, some parallax -> Ken Burns; every decision in the run's *_plan.csv (desk_rule / desk_note columns).\n"
           if roles.get("teaser") else "")
        + f"Per beat: v9 shot {roles.get('v9_shot', 0)}, new pool still {roles.get('new_pool', 0)}, "
        f"new Openverse/Pixabay item {roles.get('new_stock', 0)}, "
        f"continued_with_motion {roles.get('continued_with_motion', 0)} (no unused correct still -> previous shot runs on, with motion), "
        f"text card/archival held {roles.get('card_hold', 0)}, crop reuse {roles.get('crop_reuse', 0)}.\n"
        f"Labels per shot: " + ", ".join(f"{k} {v}" for k, v in sorted(labels.items())) + " (visuals_beats.csv 'match').\n"
        "  exact = the narrated place; representative = Dwarka/nearby or generic stock, NOT the narrated spot; text_card = own card; archival = labelled old photo.\n"
        "Motion: every still has Basic Motion scale keyframes (cover-fit x 1.00->1.08 or back, cards 1.03, archival 1.02) and a small centre drift.\n"
        + (f"Parallax: {n_px} shots are 2.5D parallax MP4s (visuals/PX_*.mp4, 1920x1080 H.264, {fps} fps, video only) rendered from the\n"
           "  SAME photo (same label exact/representative; motion: parallax_2_5d = depth-based camera move of a real photo,\n"
           "  not AI-generated imagery). Gate: fold/stretch/border/smoothness per clip (parallax_report.csv); failed clips stay Ken Burns.\n"
           "  These clips have NO Premiere motion keyframes (motion is baked in). Parallax in Premiere: NOT_TESTED.\n" if n_px else "")
        + (f"AI animated (v17): {n_ai} shots are AI motion MP4s (visuals/AI_*.mp4, 1920x1080 H.264, {fps} fps, video only) made\n"
           f"  from the SAME real photo with an image-to-video model ({AI_MODEL_NAME}, {AI_MODEL_LICENCE}). Only subtle natural motion\n"
           "  (waves / water / clouds / flag) is taken from the model, and only on moving sky / water / flag pixels; every other\n"
           "  pixel is the untouched photo, so no building, person or place is invented. Label: the photo's own exact /\n"
           "  representative + motion: ai_animated (visuals_beats.csv ai_motion_*); each clip carries a small on-screen 'AI animated'\n"
           "  label (top right); CREDITS: model + licence + 'modified (AI motion)'. Gate + agent eye check: ai_motion_report.csv.\n"
           "  These clips have NO Premiere motion keyframes. AI clips in Premiere: NOT_TESTED. Human review: NOT done.\n" if n_ai else "")
        + "  How Premiere reads the scale/centre values from xmeml: NOT_TESTED (check one still; if it looks too big/small, select all\n"
        "  clips > right-click > Set to Frame Size and the keyframes stay relative).\n"
        f"Visual selection: {selected_by}. visuals_human_approved: false. New pool stills: agent eye-check only.\n"
        "Captions: captions.srt = accepted Hinglish SRT (user bulk approval); word-level timing NOT verified.\n"
        "Hindi source transcript: DRAFT (listening review pending). Timing of cuts vs speech: NOT verified by a human.\n"
        f"Durations: source audio {ms['duration']:.3f} s; sequence/visuals end on the last whole frame ({seq_end:.3f} s).\n"
        "Paths: XML points to " + (str(base) if base else "this folder") + " (media/ and visuals/ next to sequence.xml).\n\n"
        "1. Extract anywhere, then double-click FIX_PATHS.bat (rewrites sequence.xml to this folder, says PASS/WARN).\n"
        "2. Premiere: File > Open Project (Ctrl+O), file type 'All Files', pick sequence.xml (not File > Import).\n"
        "3. Home key (playhead 00:00:00:00), File > Import captions.srt, select it, press '.' (Overwrite).\n"
        "4. If anything still shows offline: right-click > Link Media > media/ or visuals/.\n", encoding="utf-8")
    premiere.write_fix_paths(pkg)
    report_pass = all(c.get("pass") for c in checks)
    files = sorted(p for p in pkg.rglob("*") if p.is_file())
    write_json(pkg / "package_manifest.json", {
        "run_id": run.run_id, "source_sha256": inp["sha256"], "stats": stats,
        "beats": {"count": len(bp["beats"]), "anchor": bp["anchor"], "shift_s": bp["shift_s"], **bp["stats"]},
        "shots": shot, "roles_per_beat": roles, "labels_per_shot": labels, "unique_assets": qa_a["unique_assets"],
        "status": {"transcript_accepted": False, "visuals": "selected_by:" + selected_by, "visuals_human_approved": False,
                   "captions": "captions.srt = captions_hinglish_v1_accepted.srt (text accepted, timing NOT verified)",
                   "premiere_import": "NOT_TESTED", "cut_timing_human_verified": False,
                   "motion_in_premiere": "NOT_TESTED",
                   **({"parallax_clips": n_px, "parallax_in_premiere": "NOT_TESTED"} if n_px else {}),
                   **({"ai_motion_clips": n_ai, "ai_motion_in_premiere": "NOT_TESTED", "ai_motion_human_reviewed": False,
                       "ai_motion_model": AI_MODEL_NAME + " (" + AI_MODEL_LICENCE + ")"} if n_ai else {}),
                   **({"crop_reuses": qa_a["crop_reuses"], "crop_reuse_human_reviewed": False} if qa_a.get("crop_reuses") else {}),
                   **({"stock_video_clips": n_vid - n_motion, "stock_video_in_premiere": "NOT_TESTED"} if n_vid - n_motion else {}),
                   **({"motion_graphics_clips": n_motion, "motion_graphics_in_premiere": "NOT_TESTED",
                       "motion_graphics_human_reviewed": False} if n_motion else {})},
        "checks": checks,
        "files": {str(p.relative_to(pkg)).replace("\\", "/"): sha256_file(p) for p in files}})
    write_json(run.path("qa_report.json"), {"pass": report_pass, "checks": checks})
    run.add_output(pkg / "sequence.xml", "premiere_xml")
    result = {"run_id": run.run_id, "package": str(pkg), "stats": stats, "shots": shot, "roles": roles, "labels": labels,
              "unique_assets": qa_a["unique_assets"], "qa": {"pass": report_pass, "checks": checks}}
    if zip_out and win_root:
        top = PureWindowsPath(win_root).name
        tmp = Path(tempfile.mkdtemp(prefix="kang_zip_"))
        shutil.copytree(pkg, tmp / top)
        z = shutil.make_archive(str(tmp / "pkg"), "zip", tmp, top)
        Path(zip_out).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(z, zip_out)
        result["zip"] = str(zip_out)
        run.add_output(zip_out, "package_zip")
    run.log_step("beats_package", **{k: stats[k] for k in ("visual_clipitems", "markers", "motion_clipitems")})
    run.set_status("draft_package_ready" if report_pass else "qa_failed")
    return result


def preview_cmd(media: str, assign_csv: str, captions: str, t0: float, t1: float, out: str, *, run_id: Optional[str] = None,
                w: int = 1280, h: int = 720, fps: int = 25, crf: int = 26, chunk_s: float = 10.0,
                budget_s: float = 80.0) -> Dict[str, Any]:
    """Resumable: renders chunk_s pieces until budget_s is used, call again with --run to continue."""
    import time
    from .render import _filter_path
    run = Run(run_id) if run_id else Run()
    if not run_id:
        run.add_input(media, "A1")
        run.add_input(assign_csv, "VISUALS_BEATS")
        run.add_input(captions, "CAPTIONS")
    rows = B.read_assign_csv(assign_csv)
    clips = _clips(rows)
    parts = run.path("preview_parts")
    parts.mkdir(exist_ok=True)
    t_start = time.time()
    edges = []
    t = t0
    while t < t1 - 1e-6:
        edges.append((t, min(t1, t + chunk_s)))
        t += chunk_s
    done = 0
    rendered_now = 0
    for k, (a, b) in enumerate(edges):
        part = parts / f"part_{k:03d}.mp4"
        if part.exists() and part.stat().st_size > 0:
            done += 1
            continue
        if time.time() - t_start > budget_s:
            break
        tmp = part.with_suffix(".tmp.mp4")
        B.render_motion_video(clips, lambda c: c["path_local"], a, b, tmp, w=w, h=h, fps=fps, crf=18)
        tmp.replace(part)
        done += 1
        rendered_now += 1
    if done < len(edges) or (rendered_now and time.time() - t_start > budget_s * 0.6):  # mux needs ~50 s: next call
        run.set_status("preview_partial")
        return {"run_id": run.run_id, "status": "partial", "chunks_done": done, "chunks": len(edges),
                "next": f"run again with --run {run.run_id}"}
    (parts / "concat.txt").write_text("".join(f"file '{(parts / f'part_{k:03d}.mp4').resolve().as_posix()}'\n"
                                              for k in range(len(edges))), encoding="utf-8")
    srt = run.path("preview_captions.srt")
    srt.write_text(B.shift_srt(Path(captions).read_text(encoding="utf-8-sig"), t0, t1), encoding="utf-8")
    fonts = ROOT / "fonts"
    vf = (f"subtitles=filename='{_filter_path(srt)}':fontsdir='{_filter_path(fonts)}'"
          f":force_style='FontName=Mukta ExtraBold,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
          f"BorderStyle=1,Outline=2,Shadow=0,MarginV=22'")
    tmpd = Path(tempfile.mkdtemp(prefix="kang_bprev_"))
    tmp_out = tmpd / Path(out).name
    dur = t1 - t0
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(parts / "concat.txt"), "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}",
                "-i", str(media), "-map", "0:v", "-map", "1:a", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
                "-crf", str(crf), "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-t", f"{dur:.3f}",
                "-movflags", "+faststart", str(tmp_out)], run.path("ffmpeg.log"))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tmp_out, run.path(Path(out).name))
    shutil.move(str(tmp_out), out)
    pm = media_summary(out)
    run.add_output(run.path(Path(out).name), "beats_preview")
    run.log_step("beats_preview", range=[t0, t1], width=w, crf=crf)
    ok = abs(pm["duration"] - dur) <= 0.1 and pm["has_video"] and pm["has_audio"]
    run.set_status("done" if ok else "qa_failed")
    return {"run_id": run.run_id, "status": "done", "preview": out, "duration": round(pm["duration"], 3),
            "width": pm.get("width"), "qa": {"pass": ok}}


def grid_cmd(preview: str, assign_csv: str, t0: float, scenes: Sequence[str], out: str, *, cols: int = 5,
             jitter_at: Optional[float] = None) -> Dict[str, Any]:
    """Frame grid at beat midpoints (from the rendered preview, captions included) + simple frame checks:
    near-black frames and a jitter measure on 2 s of consecutive frames."""
    import subprocess
    from PIL import Image, ImageDraw, ImageFont, ImageStat
    rows = [r for r in B.read_assign_csv(assign_csv) if r["scene"] in set(scenes)]
    tmp = Path(tempfile.mkdtemp(prefix="kang_grid_"))
    tiles, black = [], []
    for k, r in enumerate(rows):
        mid = (r["start"] + r["end"]) / 2 - t0
        fp = tmp / f"f{k:03d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{mid:.3f}", "-i", preview, "-frames:v", "1",
                        "-vf", "scale=384:-2", str(fp)], check=True)
        im = Image.open(fp).convert("RGB")
        if sum(ImageStat.Stat(im).mean) / 3 < 12:
            black.append(r["beat"])
        tiles.append((im, r))
    fpath = ROOT / "fonts" / "Mukta-ExtraBold.ttf"
    font = ImageFont.truetype(str(fpath), 15)
    tw, th = 384, 216 + 44
    n_rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, n_rows * th), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for k, (im, r) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * th
        sheet.paste(im.resize((tw, 216)), (x, y))
        d.text((x + 4, y + 218), f"{r['beat']} {r['start']:.1f}s {r['match']} {r['role']}", fill=(255, 220, 90), font=font)
        d.text((x + 4, y + 238), r["asset"][:44], fill=(220, 220, 220), font=font)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    res: Dict[str, Any] = {"grid": out, "tiles": len(tiles), "near_black": black}
    if jitter_at is not None:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{jitter_at - t0:.3f}", "-i", preview, "-frames:v", "50",
                        "-vf", "crop=iw/2:ih/2:iw/4:ih/8", str(tmp / "j%03d.png")], check=True)
        fr = [Image.open(p) for p in sorted(tmp.glob("j*.png"))]
        res["jitter"] = B.jitter_metric(fr)
    return res
