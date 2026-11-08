"""Creative layer adapter (Creative Office milestone 1, critic side).

Thin KANG adapter around the user-supplied rules engine
(creative/vendor/creative_layer_v2, stdlib only, no LLM). The vendor folder is
kept UNMODIFIED; KANG-specific choices live here and in config/:

- config/creative_profiles.json      KANG profiles (travel_vlog_hi), merged over vendor profiles
- config/creative_audio_deferred.json rules switched off while audio is deferred (user, 2026-11-06)

build_beats():  visuals_beats CSV (v17b) + Hinglish word layer -> engine beats JSON.
Only facts present in the data are filled. Editorial labels (hook, payoff,
open loop, chapter) are NOT invented; missing -> engine skips or reports.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "creative" / "vendor" / "creative_layer_v2"
VENDOR_ENGINE = VENDOR / "step_4_worker_critic" / "engine.py"
VENDOR_RULES = VENDOR / "step_2_rules" / "rules.json"
VENDOR_PROFILES = VENDOR / "step_4_worker_critic" / "profiles.json"
KANG_PROFILES = ROOT / "config" / "creative_profiles.json"
AUDIO_DEFERRED = ROOT / "config" / "creative_audio_deferred.json"

AUDIO_CHECK_KINDS = {"db_range", "lufs_target", "fade_ms"}
AUDIO_WORDS = re.compile(
    r"\b(music|sfx|sound|audio|lufs|lkfs|duck|ducker|ducking|whoosh|riser|j-?cut|l-?cut|loudness|"
    r"voice ?over level|mix|mixing|bgm|ambien\w*|dehum|noise reduction|true peak|dbfs|db)\b", re.I)

GRAPHIC_MATCH = {"text_card", "map"}


def _load_json(p: Path) -> Any:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_engine():
    spec = importlib.util.spec_from_file_location("kang_creative_engine", VENDOR_ENGINE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def load_rules(path: Path = VENDOR_RULES) -> List[Dict[str, Any]]:
    return _load_json(path)


def load_profiles() -> Dict[str, Any]:
    prof = {k: v for k, v in _load_json(VENDOR_PROFILES).items() if not k.startswith("_")}
    if KANG_PROFILES.is_file():
        for name, spec in _load_json(KANG_PROFILES).items():
            if name.startswith("_"):
                continue
            base = dict(prof.get(spec.get("extends", ""), {}))
            base.update({k: v for k, v in spec.items() if k != "extends"})
            prof[name] = base
    return prof


def is_audio_rule(rule: Dict[str, Any]) -> bool:
    chk = rule.get("check") or {}
    if chk.get("kind") in AUDIO_CHECK_KINDS:
        return True
    text = " ".join(str(rule.get(k, "")) for k in ("name", "action", "when"))
    return bool(AUDIO_WORDS.search(text))


def audio_deferred_ids(rules: List[Dict[str, Any]]) -> List[str]:
    if AUDIO_DEFERRED.is_file():
        return list(_load_json(AUDIO_DEFERRED).get("rule_ids", []))
    return [r["id"] for r in rules if is_audio_rule(r)]


# ---------------------------------------------------------------- beats ----
def _words(layer_path: Path) -> List[Dict[str, Any]]:
    d = _load_json(layer_path)
    ws = d["words"] if isinstance(d, dict) else d
    out = []
    for w in ws:
        out.append({"start": float(w["start"]), "end": float(w["end"]),
                    "hi": w.get("hindi") or w.get("word") or "",
                    "en": w.get("hinglish") or ""})
    return out


def _card_items(card_values: Optional[Path]) -> List[Dict[str, Any]]:
    if not card_values or not Path(card_values).is_file():
        return []
    out = []
    for r in csv.DictReader(open(card_values, encoding="utf-8-sig")):
        try:
            out.append({"t": float(r["shown_at"]), "text": r.get("shown_text", ""), "clip": r.get("clip", "")})
        except (KeyError, ValueError):
            continue
    # card_values.csv has one row per spoken value; a shown line with two values
    # appears twice. Keep one item per (clip, shown_text) at its earliest shown_at.
    first: Dict[Any, Dict[str, Any]] = {}
    for it in sorted(out, key=lambda x: x["t"]):
        first.setdefault((it["clip"], it["text"].strip()), it)
    return sorted(first.values(), key=lambda x: x["t"])


def build_beats(visuals_csv: Path, layer_path: Path, profile: str = "travel_vlog_hi",
                platform: str = "youtube", card_values: Optional[Path] = None) -> Dict[str, Any]:
    """text = what the viewer READS on screen for card/map beats (revealed card items),
    and the Hinglish narration for photo/video beats (captions carry it).
    narration = Hinglish narration for every beat. visual_change = new asset, or a new
    card/map item revealed inside the beat (card_values.csv shown_at)."""
    rows = list(csv.DictReader(open(visuals_csv, encoding="utf-8-sig")))
    words = _words(layer_path)
    if card_values is None:
        cand = Path(visuals_csv).parent / "card_values.csv"
        card_values = cand if cand.is_file() else None
    if card_values is None:
        # v18: CSV built in a later run -> card_values.csv next to the motion clips' folder (motion-build/fix run)
        for r in rows:
            if r.get("match") in GRAPHIC_MATCH and r.get("source_dir"):
                sd = Path(r["source_dir"])
                cand = (sd if sd.is_absolute() else ROOT / sd).parent / "card_values.csv"
                if cand.is_file():
                    card_values = cand
                    break
    items = _card_items(card_values)
    beats: List[Dict[str, Any]] = []
    prev_asset: Optional[str] = None
    for r in rows:
        s, e = float(r["start"]), float(r["end"])
        ws = [w for w in words if s <= w["start"] < e]
        asset = r.get("asset", "")
        match = r.get("match", "")
        narration = " ".join(w["en"] for w in ws).strip()
        graphic = match in GRAPHIC_MATCH
        revealed = [it["text"] for it in items if s <= it["t"] < e] if graphic else []
        b: Dict[str, Any] = {
            "id": r["beat"], "scene": r.get("scene"),
            "start_s": round(s, 3), "end_s": round(e, 3),
            "kind": "graphic" if graphic else "broll",
            "text": " ".join(revealed).strip() if graphic else narration,
            "narration": narration,
            "text_hi": " ".join(w["hi"] for w in ws).strip(),
            "visual_change": (bool(asset) and asset != prev_asset) or bool(revealed),
            "match": match, "role": r.get("role", ""), "motion": r.get("desk_motion") or r.get("motion", ""),
            "asset": asset,
        }
        if r.get("role") == "teaser":
            # v18 cold open: visual-only teaser over the unchanged narration -> hook beat (tease, on-screen title)
            b.update(kind="hook", tease=True, overlay=True, relevant=True, visual_change=True,
                     text=(r.get("overlay_text") or "").replace("|", " ").strip())
        if match in ("exact", "text_card", "map"):
            b["relevant"] = True  # exact place / narration-traced card or map
        beats.append(b)
        prev_asset = asset
    beats = _merge_teaser(_merge_graphic_holds(beats))
    duration = max(float(r["end"]) for r in rows) if rows else 0.0
    span = (words[-1]["end"] - words[0]["start"]) if words else 0.0
    wpm = round(len(words) / (span / 60.0), 1) if span > 0 else None
    meta = {"profile": profile, "platform": platform, "duration_s": round(duration, 3),
            "wpm": wpm, "voiceover": True, "video_type": "travel_vlog",
            "language": "hi (captions Hinglish)",
            "source_visuals_csv": str(visuals_csv), "source_layer": str(layer_path),
            "source_card_values": str(card_values) if card_values else None}
    return {"meta": meta, "beats": beats}


def _merge_graphic_holds(beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """One card/map clip held over several narration beats = ONE on-screen graphic
    (the viewer reads it for the whole hold). Merge so reading-time rules see the
    real on-screen duration. Original beat ids kept in `beat_ids`."""
    out: List[Dict[str, Any]] = []
    for b in beats:
        prev = out[-1] if out else None
        if prev and b["kind"] == "graphic" and prev["kind"] == "graphic" and b["asset"] == prev["asset"]:
            prev["end_s"] = b["end_s"]
            prev["text"] = (prev["text"] + " " + b["text"]).strip()
            prev["narration"] = (prev["narration"] + " " + b["narration"]).strip()
            prev["text_hi"] = (prev["text_hi"] + " " + b["text_hi"]).strip()
            prev["beat_ids"].append(b["id"])
            continue
        b = dict(b); b["beat_ids"] = [b["id"]]
        out.append(b)
    return out


def _merge_teaser(beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Consecutive teaser shots = ONE hook beat (the cold open as a whole: R-064 band 3-8 s, R-400/R-001 start).
    Cuts inside it are kept as `teaser_cuts`; visual_change=True (changes happen inside the beat)."""
    out: List[Dict[str, Any]] = []
    for b in beats:
        prev = out[-1] if out else None
        if prev and b.get("tease") and prev.get("tease"):
            prev["end_s"] = b["end_s"]
            prev["narration"] = (prev["narration"] + " " + b["narration"]).strip()
            prev["text_hi"] = (prev["text_hi"] + " " + b["text_hi"]).strip()
            prev["beat_ids"] += b["beat_ids"]
            prev["teaser_cuts"].append(b["start_s"])
            prev["teaser_assets"].append(b["asset"])
            continue
        if b.get("tease"):
            b = dict(b, teaser_cuts=[], teaser_assets=[b["asset"]])
        out.append(b)
    return out


# --------------------------------------------------------------- engine ----
def run(data: Dict[str, Any], profile: Optional[str] = None, defer_audio: bool = True) -> Dict[str, Any]:
    eng = load_engine()
    rules = load_rules()
    deferred = set(audio_deferred_ids(rules)) if defer_audio else set()
    profiles = load_profiles()
    pname = profile or data.get("meta", {}).get("profile") or "long_explainer"
    rules, changes = apply_overlay(rules, pname)
    active = [r for r in rules if r["id"] not in deferred]
    data = json.loads(json.dumps(data))
    if pname in profiles and "wpm_range" in profiles[pname] and profiles[pname]["wpm_range"] is None:
        # no trusted band for this language yet -> keep the measurement, skip the judgement
        data["meta"]["wpm_measured"] = data["meta"].pop("wpm", None)
    report = eng.run_engine(data, active, profiles, profile_override=profile)
    report["summary"]["total_rules_vendor"] = len(rules)
    report["summary"]["deferred_audio_rules"] = len(deferred)
    report["deferred_audio_rule_ids"] = sorted(deferred)
    report["kang_overlay"] = changes
    report["_engine_md"] = eng.render_md(report)
    return report


def beat_stats(data: Dict[str, Any]) -> Dict[str, Any]:
    """Plain measurements KANG adds next to the engine score (no rule judgement)."""
    bs = data["beats"]
    durs = [round(b["end_s"] - b["start_s"], 2) for b in bs]
    same3 = 0
    for i in range(2, len(durs)):
        if abs(durs[i] - durs[i - 1]) < 0.25 and abs(durs[i - 1] - durs[i - 2]) < 0.25:
            same3 += 1
    kinds: Dict[str, int] = {}
    for b in bs:
        kinds[b["match"]] = kinds.get(b["match"], 0) + 1
    first30 = sum(1 for b in bs if b["start_s"] < 30 and b["visual_change"])
    return {"beats": len(bs), "avg_shot_s": round(sum(durs) / len(durs), 2) if durs else None,
            "min_shot_s": min(durs) if durs else None, "max_shot_s": max(durs) if durs else None,
            "same_length_3_in_row": same3, "visual_changes_first_30s": first30, "match_counts": kinds}


def check_cmd(visuals_csv: str, layer: str, profile: str = "travel_vlog_hi", run_id: Optional[str] = None,
              defer_audio: bool = True, captions: Optional[str] = None) -> Dict[str, Any]:
    """kang.py creative-check: new run with beats JSON + engine report (json/md) + KANG stats."""
    from core.runs import Run, write_json
    rn = Run(run_id)
    rn.add_input(visuals_csv, "visuals_beats")
    rn.add_input(layer, "hinglish_layer")
    rn.add_input(VENDOR_ENGINE, "vendor_engine")
    rn.add_input(VENDOR_RULES, "vendor_rules")
    data = build_beats(Path(visuals_csv), Path(layer), profile=profile)
    bpath = rn.path("creative_beats.json"); write_json(bpath, data); rn.add_output(bpath, "creative_beats")
    report = _run_report(data, profile, defer_audio)
    md = report.pop("_engine_md")
    if captions is None:
        cand = Path(layer).parent / "captions_hinglish_v1_accepted.srt"
        captions = str(cand) if cand.is_file() else None
    kc = kang_checks(data, Path(captions) if captions else None)
    report["kang_checks"] = kc
    stats = beat_stats(data)
    report["kang_stats"] = stats
    jpath = rn.path("creative_report.json"); write_json(jpath, report); rn.add_output(jpath, "creative_report")
    mpath = rn.path("creative_report.md")
    extra = ["", "## KANG naap (bina rule ke, sirf data)",
             f"- Beats: {stats['beats']} · avg shot {stats['avg_shot_s']} s (min {stats['min_shot_s']}, max {stats['max_shot_s']})",
             f"- Pehle 30 s me visual changes: {stats['visual_changes_first_30s']}",
             f"- Lagatar 3 shots same length (±0.25 s): {stats['same_length_3_in_row']} jagah",
             f"- Match types: {stats['match_counts']}",
             f"- WPM (naapa, judge nahi kiya): {data['meta'].get('wpm')}",
             f"- Audio rules band (deferred): {report['summary']['deferred_audio_rules']}",
             "", "## KANG overlay (Hark audit 2026-11-06)",
             f"- Hataye (superseded/profile-off): {', '.join(sorted(report['kang_overlay']['removed']))}",
             f"- Evidence badla: {len(report['kang_overlay']['retagged'])} rules · Naye rules: {len(report['kang_overlay']['added'])}",
             "", "## KANG checks (naye rules jo hamare data par naap sakte hain)"]
    for c in kc:
        extra.append(f"- **{c['rule_id']}** {c['name']}: {c['status'].upper()} ({len(c['findings'])} findings) {c['note']}")
        for x in c["findings"][:6]:
            extra.append(f"  - {x}")
    mpath.write_text(md + "\n".join(extra) + "\n", encoding="utf-8"); rn.add_output(mpath, "creative_report_md")
    rn.log_step("creative-check", profile=profile, defer_audio=defer_audio, summary=report["summary"])
    rn.set_status("done")
    return {"run": rn.run_id, "summary": report["summary"], "kang_stats": stats,
            "report_md": str(mpath), "report_json": str(jpath)}


def _run_report(data, profile, defer_audio):
    return globals()["run"](data, profile=profile, defer_audio=defer_audio)


# ------------------------------------------------------- KANG overlay ----
OVERLAY = ROOT / "config" / "creative_rulebook_kang.json"
STILL_MOTIONS = {"zoom_in", "zoom_out", "parallax_2_5d", "pan_left", "pan_right"}


def load_overlay() -> Dict[str, Any]:
    return _load_json(OVERLAY) if OVERLAY.is_file() else {}


def apply_overlay(rules: List[Dict[str, Any]], profile: str, ov: Optional[Dict[str, Any]] = None):
    """-> (rules_for_engine, changes). Vendor rules + KANG corrections:
    evidence re-tags, superseded/profile-off rules removed, new rules added
    WITHOUT check (KANG evaluators below judge the ones we can measure)."""
    ov = load_overlay() if ov is None else ov
    ev = ov.get("evidence_changes", {})
    off = dict(ov.get("superseded", {}))
    off.update(ov.get("profile_off", {}).get(profile, {}))
    out, retagged = [], []
    for r in rules:
        if r["id"] in off:
            continue
        r = dict(r)
        if r["id"] in ev:
            retagged.append({"rule_id": r["id"], "from": r.get("evidence"), "to": ev[r["id"]]["to"]})
            r["evidence"] = ev[r["id"]]["to"]
            r["evidence_note"] = (r.get("evidence_note") or "") + " | KANG audit: " + ev[r["id"]]["why"]
        out.append(r)
    for n in ov.get("new_rules", []):
        m = {k: n.get(k) for k in ("id", "name", "layer", "when", "action", "why", "frequency",
                                    "evidence", "evidence_note", "sources")}
        m["check"] = None
        m["kang_check"] = n.get("check")
        out.append(m)
    return out, {"removed": off, "retagged": retagged, "added": [n["id"] for n in ov.get("new_rules", [])]}


def _srt_cues(path: Optional[Path]) -> List[Dict[str, Any]]:
    if not path or not Path(path).is_file():
        return []
    def ts(t):
        h, m, s = t.strip().replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    cues = []
    for block in re.split(r"\n\s*\n", Path(path).read_text(encoding="utf-8-sig").strip()):
        lines = block.strip().splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            a, b = lines[1].split("-->")
            cues.append({"start": ts(a), "end": ts(b), "text": " ".join(lines[2:])})
    return cues


def shots(bs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Beats -> shots: consecutive b-roll beats on the same asset merged (id = first beat, `beat_ids` all)."""
    out: List[Dict[str, Any]] = []
    for b in bs:
        prev = out[-1] if out else None
        if prev and b["kind"] == "broll" and prev["kind"] == "broll" and b.get("asset") and b["asset"] == prev["asset"]:
            prev["end_s"] = b["end_s"]
            prev["beat_ids"] = prev["beat_ids"] + b.get("beat_ids", [b["id"]])
            continue
        out.append(dict(b, beat_ids=list(b.get("beat_ids", [b["id"]]))))
    return out


def kang_checks(data: Dict[str, Any], captions: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Rules from the KANG overlay that we can measure on our own data."""
    bs = data["beats"]
    res = []

    def add(rid, name, status, finds, note=""):
        res.append({"rule_id": rid, "name": name, "status": status, "findings": finds, "note": note})

    # v18: shot-level rules are measured on SHOTS (consecutive b-roll beats on the same asset = one shot, exactly as
    # the package builds clips with core.beats.merge_clips); the cold-open hook (tease) is exempt (fast teaser cuts).
    sh = shots(bs)
    stills = [b for b in sh if b["kind"] == "broll" and b.get("motion") in STILL_MOTIONS]
    f = [f"{b['id']}: still {b['end_s'] - b['start_s']:.2f}s (band 3-10)" for b in stills
         if not 3 - 1e-6 <= b["end_s"] - b["start_s"] <= 10 + 1e-6]
    add("G-004", "Narrated still hold 3-10 s", "fail" if f else "pass", f, note="per shot; teaser exempt")
    f = [f"{b['id']}: shot {b['end_s'] - b['start_s']:.2f}s > 7" for b in sh
         if b["kind"] == "broll" and b["end_s"] - b["start_s"] > 7 + 1e-6]
    add("Q-001", "Narrated shot <= ~7 s (WARN level)", "warn" if f else "pass", f, note="per shot")
    nt = [b for b in sh if not b.get("tease")]
    d = [b["end_s"] - b["start_s"] for b in nt]
    f = [f"{nt[i]['id']}: 3 shots ~{d[i]:.2f}s in a row" for i in range(2, len(d))
         if abs(d[i] - d[i - 1]) < 0.25 and abs(d[i - 1] - d[i - 2]) < 0.25]
    add("Q-002", "Same shot length not 3x in a row", "fail" if f else "pass", f, note="per shot; teaser exempt")
    f, run = [], 1
    for i in range(1, len(nt)):
        a, b = nt[i - 1].get("motion"), nt[i].get("motion")
        run = run + 1 if (b in STILL_MOTIONS and a == b) else 1
        if run == 3:
            f.append(f"{nt[i]['id']}: 3rd '{b}' in a row")
    add("G-006", "Max 2 same camera moves in a row", "fail" if f else "pass", f, note="per shot")
    f = [f"{nt[i]['id']}: parallax right after parallax" for i in range(1, len(nt))
         if nt[i].get("motion") == "parallax_2_5d" and nt[i - 1].get("motion") == "parallax_2_5d"]
    add("G-008", "Parallax not back to back", "fail" if f else "pass", f, note="per shot")
    acc = [i for i, b in enumerate(nt) if b.get("motion") in ("parallax_2_5d", "ai_animated")]
    f = [f"{nt[j]['id']}: accent {j - i} shot(s) after {nt[i]['id']}" for i, j in zip(acc, acc[1:]) if j - i < 3]
    add("Q-006", "Accent budget (parallax/AI <= ~1 per 3 cuts)", "fail" if f else "pass", f,
        note=f"{len(acc)} accent shots; KANG proxy: accents >= 3 shots apart")
    wpm = data["meta"].get("wpm") or data["meta"].get("wpm_measured")
    if wpm:
        add("S-021", "Narration WPM hard limits 115-230", "pass" if 115 <= wpm <= 230 else "fail",
            [] if 115 <= wpm <= 230 else [f"{wpm} WPM"], note=f"measured {wpm} WPM")
    cues = _srt_cues(captions)
    if cues:
        f = []
        for c in cues:
            dur = c["end"] - c["start"]
            cps = len(c["text"].replace(" ", "")) / dur if dur > 0 else 99
            if cps > 22:
                f.append(f"{c['start']:.2f}s: {cps:.1f} cps '{c['text'][:30]}'")
        add("G-013", "Caption speed <= 22 cps (Hindi/Hinglish)", "fail" if f else "pass", f,
            note=f"{len(cues)} cues; chars counted without spaces")
        f = [f"{c['start']:.2f}s: {c['end'] - c['start']:.2f}s" for c in cues
             if not 0.83 <= c["end"] - c["start"] <= 7]
        add("S-004", "Caption on screen 0.83-7 s", "fail" if f else "pass", f)
    else:
        add("G-013", "Caption speed <= 22 cps", "skip", [], note="no captions file")
    return res
