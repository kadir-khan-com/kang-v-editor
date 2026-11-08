"""v15: YouTube Creative Commons (CC BY) clips of Dwarka as real place footage.

Approach (research 2026-11-04, see STATUS.md):
  * yt-dlp (Unlicense, pip, runs on Windows) - `ytsearchN` / CC-filtered search URL (sp=EgIwAQ%3D%3D) to find videos,
    then the per-video metadata field `license` ("Creative Commons Attribution license (reuse allowed)") as the ONLY
    acceptance gate; `--download-sections` for short parts, video only, <= 1080p.  <- picked (free, no key)
  * YouTube Data API v3 search videoLicense=creativeCommon: needs an API key (none; free quota but key/OAuth) - not used.
  * Wikimedia Commons / Openverse video: licence-reviewed mirrors of CC BY YouTube videos; Openverse has no video,
    Commons had 0 Gujarat-Dwarka videos on 2026-11-04 (only Delhi-Dwarka airport clips) - fallback only.

Pipeline: search -> probe (licence + place check) -> sections -> download (byte cap) -> scene split (ffmpeg scene
filter, no extra dependency; PySceneDetect optional) -> shot checks (shake, static overlay = burned text/logo/
watermark, face close-up = vlogger) -> contact sheet for the agent's eye -> pool -> assign onto a visuals_beats CSV.

Blocked IP (bot check / 429 / 403): at most 2 probe ways (config `probe_ways`), then the run stops with status
`blocked`; nothing is faked, no cookies, no proxies.  YouTube ToS on downloading is a grey area: recorded, not cleared.
All yt-dlp calls go through an injectable `runner(args, timeout) -> (rc, stdout, stderr)` so tests need no network.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from . import stock_common as SC
from .runs import Run, media_summary, write_json

ROOT = Path(__file__).resolve().parent.parent
Runner = Callable[[List[str], float], Tuple[int, str, str]]
LICENCE_CC_BY = "Creative Commons Attribution license (reuse allowed)"


class Blocked(RuntimeError):
    """YouTube answered a bot check / 429 / 403 on every allowed way."""

    def __init__(self, msg: str, attempts: List[Dict[str, Any]]):
        super().__init__(msg)
        self.attempts = attempts


def load_cfg(path: Optional[str | Path] = None) -> Dict[str, Any]:
    return json.loads(Path(path or ROOT / "config" / "youtube_cc.json").read_text(encoding="utf-8"))


def ytdlp_runner(args: List[str], timeout: float = 110.0) -> Tuple[int, str, str]:
    """Real runner: `python -m yt_dlp` (pip package, same on Windows), falls back to a `yt-dlp` binary."""
    cmd = [sys.executable, "-m", "yt_dlp", *args]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    if r.returncode != 0 and "No module named yt_dlp" in (r.stderr or ""):
        r = subprocess.run(["yt-dlp", *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
    return r.returncode, r.stdout or "", r.stderr or ""


def is_blocked(stderr: str, cfg: Dict[str, Any]) -> bool:
    return any(m.lower() in (stderr or "").lower() for m in cfg.get("block_markers", []))


# --------------------------------------------------------------------------- search
def search_url(query: str, cfg: Dict[str, Any]) -> str:
    from urllib.parse import quote_plus
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}&sp={cfg['search_filter_sp']}"


def search(query: str, cfg: Dict[str, Any], runner: Runner = ytdlp_runner, n: Optional[int] = None) -> Dict[str, Any]:
    """CC-filtered search (pre-filter only). -> {entries:[{id,title,channel,duration,url}], blocked, stderr_tail}."""
    n = n or cfg.get("per_query", 20)
    rc, out, err = runner(["--flat-playlist", "-J", "--playlist-end", str(n), search_url(query, cfg)], 110.0)
    entries: List[Dict[str, Any]] = []
    try:
        data = json.loads(out) if out.strip() else {}
    except json.JSONDecodeError:
        data = {}
    for e in (data.get("entries") or []):
        if not e or not e.get("id"):
            continue
        entries.append({"id": e["id"], "title": e.get("title") or "", "channel": e.get("channel") or e.get("uploader") or "",
                        "duration": e.get("duration"), "url": f"https://www.youtube.com/watch?v={e['id']}",
                        "query": query})
    return {"entries": entries[:n], "blocked": not entries and is_blocked(err, cfg), "rc": rc,
            "stderr_tail": (err or "")[-300:]}


# --------------------------------------------------------------------------- probe (watch-page metadata)
def probe(video_id: str, cfg: Dict[str, Any], runner: Runner = ytdlp_runner) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Full metadata (licence, description, formats). Tries config `probe_ways` (max 2). Raises Blocked."""
    attempts: List[Dict[str, Any]] = []
    for way in cfg.get("probe_ways", [])[:2]:
        rc, out, err = runner(["--skip-download", "-J", "--no-warnings", *way["args"],
                               f"https://www.youtube.com/watch?v={video_id}"], 110.0)
        info = None
        if rc == 0 and out.strip():
            try:
                info = json.loads(out)
            except json.JSONDecodeError:
                info = None
        blocked = info is None and is_blocked(err, cfg)
        attempts.append({"way": way["name"], "rc": rc, "blocked": blocked, "stderr_tail": (err or "")[-240:]})
        if info:
            return info, attempts
        if not blocked:  # a real error (private, removed): not an IP block; do not try the next way
            return {}, attempts
    raise Blocked(f"{video_id}: watch metadata blocked on {len(attempts)} way(s)", attempts)


def licence_ok(info: Dict[str, Any], cfg: Dict[str, Any]) -> bool:
    return (info.get("license") or "").strip() == cfg.get("licence_required", LICENCE_CC_BY)


def place_check(info: Dict[str, Any], cfg: Dict[str, Any], scfg: Dict[str, Any]) -> Dict[str, Any]:
    """Title + description must name Dwarka / a Dwarka-area place and no wrong place (Delhi's Dwarka etc.)."""
    text = f"{info.get('title', '')} \n {info.get('description', '')} \n {' '.join(info.get('tags') or [])}"
    title = info.get("title", "")
    wrong = {**scfg, "wrong_places": list(scfg.get("wrong_places", [])) + list(cfg.get("wrong_places_extra", []))}
    # wrong places: title + tags strictly; description only for Delhi/expressway cues (long descriptions list many cities)
    rej = SC.text_reject(title + " " + " ".join(info.get("tags") or []), wrong, people=False)
    if not rej:
        delhi = SC.find_terms(info.get("description", ""), ["delhi", "new delhi", "dwarka sector", "dwarka expressway",
                                                           "dwarka mor", "noida", "gurgaon", "gurugram"])
        if delhi:
            rej = f"wrong place in description: {', '.join(delhi[:3])}"
    need = list(scfg.get("openverse", {}).get("require_any", [])) + list(cfg.get("require_any_extra", []))
    hits = SC.find_terms(text, need) or [w for w in need if w in text]  # Devanagari: plain substring
    places = sorted(k for k, al in cfg.get("place_terms", {}).items()
                    if SC.find_terms(text, al) or any(a in text for a in al if not a.isascii()))
    if rej:
        return {"ok": False, "reason": rej, "places": places}
    if not hits:
        return {"ok": False, "reason": "names no Dwarka / Gujarat place", "places": places}
    return {"ok": True, "reason": "", "places": places, "hits": hits[:5]}


def credit_line(v: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None) -> str:
    lic = (cfg or {}).get("credit_licence", "CC BY 3.0")
    return f"{v.get('title', '').strip()} — {v.get('channel', '').strip()} (YouTube), {lic}"


# --------------------------------------------------------------------------- sections + download
def plan_sections(duration: float, cfg: Dict[str, Any], chapters: Optional[Sequence[Dict[str, Any]]] = None) -> List[Tuple[float, float]]:
    """Short evenly spaced sections inside the body of the video (intros/outros skipped = vlogger talk / logos)."""
    d = cfg["download"]
    L, k = float(d["section_s"]), int(d["max_sections_per_video"])
    if not duration or duration <= 0:
        return []
    if duration <= L * 1.5:
        return [(0.0, round(float(duration), 2))]
    a0, a1 = duration * d["skip_head_frac"], duration * (1 - d["skip_tail_frac"])
    if a1 - a0 < L:
        a0, a1 = 0.0, float(duration)
    k = max(1, min(k, int((a1 - a0) // L)))
    step = (a1 - a0 - L) / max(1, k - 1) if k > 1 else 0.0
    return [(round(a0 + i * step, 2), round(a0 + i * step + L, 2)) for i in range(k)]


def pick_format(info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    fs = [f for f in info.get("formats") or [] if f.get("vcodec") not in (None, "none") and (f.get("height") or 0) <= 1080]
    if not fs:
        return None
    return max(fs, key=lambda f: ((f.get("height") or 0), f.get("ext") == "mp4", -(f.get("tbr") or 0)))


def est_bytes(info: Dict[str, Any], sections: Sequence[Tuple[float, float]]) -> int:
    f = pick_format(info) or {}
    total = f.get("filesize") or f.get("filesize_approx")
    dur = float(info.get("duration") or 0)
    secs = sum(b - a for a, b in sections)
    if total and dur:
        return int(total * secs / dur * 1.15)
    tbr = f.get("tbr") or 4000  # kbit/s; 1080p H.264 guess
    return int(tbr * 1000 / 8 * secs * 1.15)


def download_args(video_id: str, sections: Sequence[Tuple[float, float]], out_tmpl: str, cfg: Dict[str, Any],
                  way_args: Sequence[str] = ()) -> List[str]:
    a = ["-f", cfg["download"]["format"], "--no-playlist", "--no-warnings", "-o", out_tmpl, *way_args]
    for s, e in sections:
        a += ["--download-sections", f"*{s:.2f}-{e:.2f}"]
    return a + [f"https://www.youtube.com/watch?v={video_id}"]


# --------------------------------------------------------------------------- shots
def scene_cuts(path: str | Path, threshold: float = 0.3) -> List[float]:
    """Cut times (s) from ffmpeg's scene score (select + showinfo)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(path), "-an", "-vf",
                        f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr or "")]


def shots_from_cuts(cuts: Sequence[float], duration: float, min_s: float, trim: float = 0.2) -> List[Tuple[float, float]]:
    """Shots between cuts, each trimmed 0.2 s at both ends (no half-frame of the neighbour), shorter than min_s dropped."""
    edges = [0.0] + sorted(c for c in cuts if 0 < c < duration) + [float(duration)]
    out = []
    for a, b in zip(edges, edges[1:]):
        a2, b2 = a + (trim if a > 0 else 0), b - (trim if b < duration else 0)
        if b2 - a2 >= min_s:
            out.append((round(a2, 3), round(b2, 3)))
    return out


def _frames(path: str | Path, a: float, b: float, fps: float, w: int = 320):
    import numpy as np
    h = int(w * 9 / 16) // 2 * 2
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}",
                        "-i", str(path), "-an", "-vf", f"fps={fps},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray",
                        "-"], capture_output=True)
    buf = np.frombuffer(r.stdout, np.uint8)
    n = buf.size // (w * h)
    return buf[: n * w * h].reshape(n, h, w) if n else np.zeros((0, h, w), np.uint8)


def shake_px(frames, full_w: int = 1920) -> float:
    """Jitter: median |second difference| of the frame-to-frame translation (phase correlation), in 1920-px units.
    A steady pan has a constant translation (second difference ~0); handheld shake does not."""
    import cv2
    import numpy as np
    if len(frames) < 4:
        return 0.0
    k = full_w / frames.shape[2]
    win = cv2.createHanningWindow((frames.shape[2], frames.shape[1]), cv2.CV_32F)
    t = [cv2.phaseCorrelate(frames[i].astype(np.float32), frames[i + 1].astype(np.float32), win)[0]
         for i in range(len(frames) - 1)]
    t = np.array(t) * k
    dd = np.linalg.norm(np.diff(t, axis=0), axis=1)
    return float(np.median(dd))


def static_overlay_frac(frames) -> float:
    """Fraction of the frame that is edge-rich AND frozen while the picture moves = burned-in text / logo / watermark.
    0 when the camera itself is static (cannot tell overlay from scene)."""
    import cv2
    import numpy as np
    if len(frames) < 4:
        return 0.0
    f = frames.astype(np.float32)
    moving = float(np.mean(np.abs(np.diff(f, axis=0))))
    if moving < 2.0:
        return 0.0
    std = f.std(axis=0)
    edges = np.mean([cv2.Canny(fr, 80, 160) > 0 for fr in frames[:: max(1, len(frames) // 4)]], axis=0) > 0.75
    return float(np.mean(edges & (std < 3.0)))


def face_area_frac(path: str | Path, ts: Sequence[float], detector=None) -> float:
    """Largest detected face area / frame area over the sample times (YuNet, MIT). -1 when no detector."""
    import cv2
    import numpy as np
    if detector is None:
        from .crop_reuse import yunet_detector
        detector = yunet_detector()
    if detector is None:
        return -1.0
    best = 0.0
    for t in ts:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path),
                            "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        if not r.stdout:
            continue
        img = cv2.imdecode(np.frombuffer(r.stdout, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            continue
        H, W = img.shape[:2]
        for (x, y, w, h) in detector(img):
            best = max(best, (w * h) / float(W * H))
    return best


def shot_verdict(m: Dict[str, Any], cfg: Dict[str, Any]) -> Optional[str]:
    s = cfg["shots"]
    if m["duration"] < s["min_shot_s"]:
        return f"too short ({m['duration']:.1f} s)"
    if m.get("height", 1080) < 720:
        return f"below 720p ({m.get('height')})"
    if m["shake_px"] > s["max_shake_px"]:
        return f"shaky (jitter {m['shake_px']:.1f} px)"
    if m["face_area"] > s["max_face_area_frac"]:
        return f"face close-up / talking head ({m['face_area'] * 100:.1f} % of frame)"
    if m["face_area"] < 0:
        return "no face detector (cannot rule out vlogger close-ups)"
    if m["static_overlay"] > s["static_overlay_frac"]:
        return f"burned-in text/logo/watermark (static edges {m['static_overlay'] * 100:.2f} %)"
    return None


def analyse_shot(path: str | Path, a: float, b: float, cfg: Dict[str, Any], detector=None, height: int = 1080) -> Dict[str, Any]:
    fr = _frames(path, a, b, cfg["shots"]["analyse_fps"])
    m = {"start": a, "end": b, "duration": round(b - a, 3), "height": height, "shake_px": round(shake_px(fr), 2),
         "static_overlay": round(static_overlay_frac(fr), 5),
         "face_area": round(face_area_frac(path, [a + (b - a) * q for q in (0.2, 0.5, 0.8)], detector), 4)}
    m["reject"] = shot_verdict(m, cfg)
    return m


def cut_shot(src: str | Path, a: float, b: float, dst: str | Path) -> Dict[str, Any]:
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-nostdin", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}",
                        "-i", str(src), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", str(dst)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-300:])
    return media_summary(dst)


# --------------------------------------------------------------------------- assign (pure)
PROTECTED = ("exact", "text_card", "map", "archival")


def _units(rows: Sequence[Dict[str, Any]], beat_places: Optional[Dict[str, set]] = None,
           vrules: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Replaceable spans. (a) a whole Pixabay representative clip; (b) the tail of continued_with_motion beats of a
    hold (from the first continued beat to the end of the hold, so the held photo never comes back = no repeat).
    v16 rule A (only with `vrules`): (c) a whole ARCHIVAL hold whose narration names a place in
    `archival_replace_places` (e.g. the under-construction Sudarshan Setu still -> real finished bridge), EXACT clip
    only; (d) a whole REPRESENTATIVE still/stock shot whose own narration names a place, EXACT clip of that place only.
    (e) decision C: beats listed in `force` (e.g. an outro stock animation) -> any eye-passed Dwarka clip, done last.
    Cards, maps and exact shots stay protected."""
    from . import beats as B
    by = {r["beat"]: r for r in rows}
    vr = vrules or {}
    bpl = beat_places or {}
    arch_pl = set(vr.get("archival_replace_places") or [])
    force = vr.get("force") or {}
    out, forced = [], []
    for c in B.merge_clips(rows):
        bs = [by[b] for b in c["beats"]]
        named = set().union(*(bpl.get(r["beat"], set()) for r in bs))
        if c["asset"].startswith(("CARD_", "MAP_")) or c["match"] in ("text_card", "map"):
            continue
        if any(r["beat"] in force for r in bs) and c["match"] != "exact":
            forced.append({"kind": "forced", "beats": bs, "match": c["match"], "need_exact": False, "any_place": True,
                           "reason": "; ".join(str(force[r["beat"]].get("reason", "")) for r in bs if r["beat"] in force)})
            continue
        if c["match"] == "archival":
            if vr and named & arch_pl:
                out.append({"kind": "archival", "beats": bs, "match": c["match"], "need_exact": True,
                            "places": named & arch_pl})
            continue
        if bs[0].get("asset_source") == "pixabay" and c["match"] == "representative":
            out.append({"kind": "pixabay", "beats": bs, "match": c["match"]})
            continue
        k = next((i for i, r in enumerate(bs) if r["role"] == "continued_with_motion"), None)
        cont = None
        if k is not None and k > 0 and all(r["role"] == "continued_with_motion" for r in bs[k:]):
            cont = {"kind": "continued", "beats": bs[k:], "match": c["match"], "head": bs[0]}
        if vr.get("named_representative") and c["match"] == "representative" and named \
                and bs[0].get("asset_source") != "youtube_cc":
            out.append({"kind": "named_representative", "beats": bs, "match": c["match"], "need_exact": True,
                        "places": named, "fallback": cont})
            continue
        if cont:
            out.append(cont)
    return out + forced


def plan_youtube(rows: Sequence[Dict[str, Any]], pool: Sequence[Dict[str, Any]], beat_places: Dict[str, set],
                 asset_places: Callable[[Dict[str, Any]], set], vrules: Optional[Dict[str, Any]] = None
                 ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Pure. pool item: {key, file, dir, place, label exact|representative, duration, title, channel, url, credit}.
    A clip goes only where the narration (or, for a continued hold, the held photo) names the clip's place.
    Continued beats of an EXACT hold take only an exact clip. Never touches exact/card/map shots; archival only
    under v16 rule A (`vrules`, see _units). `vrules.prefer` {first_beat: pool key} = eye-picked clip for a unit
    (used when it fits the unit's rules; otherwise the normal pick)."""
    rows = [dict(r) for r in sorted(rows, key=lambda r: float(r["start"]))]
    used: set = set()
    # clips already on the timeline (an earlier beats-youtube-cc pass, trimmed as YTC_<beat>_<pool stem>.mp4) = used
    for r in rows:
        if r.get("asset_source") == "youtube_cc":
            used.update(p["key"] for p in pool
                        if Path(r.get("asset", "")).stem.endswith("_" + Path(p["file"]).stem))
    decisions: List[Dict[str, Any]] = []
    prefer = (vrules or {}).get("prefer") or {}
    units: List[Dict[str, Any]] = []
    for u0 in _units(rows, beat_places, vrules):
        units.append(u0)
        if u0.get("fallback"):
            units.append({**u0["fallback"], "_only_if_kept": [b["beat"] for b in u0["beats"]]})
    done: set = set()
    for u in units:
        if u.get("_only_if_kept") and any(b in done for b in u["_only_if_kept"]):
            continue
        bs = [next(r for r in rows if r["beat"] == b["beat"]) for b in u["beats"]]
        span = float(bs[-1]["end"]) - float(bs[0]["start"])
        if "places" in u:
            places = set(u["places"])
        else:
            places = set().union(*(beat_places.get(r["beat"], set()) for r in bs))
        if u["kind"] == "continued":
            places |= asset_places(u["head"])
        need_exact = u.get("need_exact", u["match"] == "exact")
        best = None
        for p in pool:
            if p["key"] in used or p["duration"] < span + 0.3:
                continue
            if not u.get("any_place") and p["place"] not in places:
                continue
            if need_exact and p["label"] != "exact":
                continue
            sc = (1 if prefer.get(bs[0]["beat"]) == p["key"] else 0, 1 if p["label"] == "exact" else 0, p["duration"])
            if best is None or sc > best[0]:
                best = (sc, p)
        if not best:
            decisions.append({"beats": [r["beat"] for r in bs], "action": "kept", "unit": u["kind"],
                              "places": sorted(places), "span_s": round(span, 2)})
            continue
        p = best[1]
        used.add(p["key"])
        done.update(r["beat"] for r in bs)
        old_asset, old_match = bs[0].get("asset", ""), bs[0].get("match", "")
        tag = "v16" if vrules else "v15"
        for r in bs:
            r.update(asset=p["file"], source_dir=p["dir"], asset_source="youtube_cc", match=p["label"],
                     licence=p["credit"], title=p["title"], source_page=p["url"], role="new_youtube_cc",
                     parallax_clip="", parallax_dir="", parallax_status="", reuse="", reuse_of="", crop_box="",
                     notes=f"{tag} YouTube CC BY clip {p['key']} ({p['label']}: {p['place']}); replaced {u['kind']} "
                           f"{old_asset}; agent-picked, eye-checked by agent, not human-reviewed")
            r["_pick"] = p
        decisions.append({"beats": [r["beat"] for r in bs], "action": "replaced", "unit": u["kind"], "item": p["key"],
                          "label": p["label"], "place": p["place"], "span_s": round(span, 2),
                          "before": old_asset, "before_label": old_match, "eye_preferred": bool(best[0][0]),
                          **({"reason": u["reason"]} if u.get("reason") else {})})
    return rows, decisions


# --------------------------------------------------------------------------- commands
def _rel(p: Path) -> str:
    try:
        return Path(p).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


CAND_COLS = ["video_id", "query", "query_place", "title", "channel", "upload_date", "duration", "licence", "url",
             "search_cc_filter", "licence_ok", "place_ok", "places", "status", "reason"]


def fetch_cmd(out_dir: str, *, runner: Runner = ytdlp_runner, cfg_path: Optional[str] = None, search_only: bool = False,
              max_probe: int = 40, run_id: Optional[str] = None) -> Dict[str, Any]:
    cfg, scfg = load_cfg(cfg_path), SC.load_cfg()
    run = Run(run_id) if run_id else Run()
    run.add_input(cfg_path or ROOT / "config" / "youtube_cc.json", "YOUTUBE_CC_CFG")
    run.add_input(ROOT / "config" / "stock_sources.json", "STOCK_CFG")
    out = ROOT / out_dir if not Path(out_dir).is_absolute() else Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cands: Dict[str, Dict[str, Any]] = {}
    search_log = []
    for q in cfg["queries"]:
        s = search(q["query"], cfg, runner)
        search_log.append({"query": q["query"], "found": len(s["entries"]), "blocked": s["blocked"], "rc": s["rc"]})
        for e in s["entries"]:
            if e["id"] not in cands:
                cands[e["id"]] = {"video_id": e["id"], "query": q["query"], "query_place": q["place"], "title": e["title"],
                                  "channel": e["channel"], "duration": e["duration"], "url": e["url"],
                                  "search_cc_filter": True, "licence": "", "upload_date": "", "licence_ok": "",
                                  "place_ok": "", "places": "", "status": "found", "reason": ""}
    # place pre-check on the search title (cheap; saves probes)
    for c in cands.values():
        pc = place_check({"title": c["title"]}, cfg, scfg)
        c["places"] = "|".join(pc["places"])
        if not pc["ok"]:
            c.update(status="rejected", reason="title: " + pc["reason"], place_ok=False)
    # v16: videos already downloaded by an earlier fetch (config `skip_video_ids`) are not probed or downloaded again
    skip = set(cfg.get("skip_video_ids") or [])
    for c in cands.values():
        if c["video_id"] in skip and c["status"] == "found":
            c.update(status="skipped", reason="already downloaded by an earlier fetch (skip_video_ids)")
    blocked: Optional[Blocked] = None
    probed = 0
    if not search_only:
        for c in [c for c in cands.values() if c["status"] == "found"][:max_probe]:
            try:
                info, att = probe(c["video_id"], cfg, runner)
            except Blocked as b:
                blocked = b
                c.update(status="unverified_blocked", reason="watch metadata blocked (licence field not read)")
                break
            probed += 1
            if not info:
                c.update(status="rejected", reason="metadata error: " + att[-1]["stderr_tail"][-120:])
                continue
            c.update(licence=info.get("license") or "", upload_date=info.get("upload_date") or "",
                     channel=info.get("channel") or c["channel"], title=info.get("title") or c["title"],
                     duration=info.get("duration") or c["duration"])
            c["licence_ok"] = licence_ok(info, cfg)
            pc = place_check(info, cfg, scfg)
            c["place_ok"], c["places"] = pc["ok"], "|".join(pc["places"])
            if not c["licence_ok"]:
                c.update(status="rejected", reason=f"licence '{c['licence'] or 'standard YouTube'}' != CC BY")
            elif not pc["ok"]:
                c.update(status="rejected", reason=pc["reason"])
            else:
                c.update(status="accepted")
                c["_info"] = info
    for c in cands.values():  # never pending: a search-filter hit without a read licence is not accepted
        if c["status"] == "found":
            c.update(status="unverified_blocked" if blocked else "not_probed",
                     reason="licence field not read" + (" (IP blocked)" if blocked else ""))
    csv_p = run.path("youtube_cc_candidates.csv")
    with open(csv_p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAND_COLS, extrasaction="ignore")
        w.writeheader()
        for c in cands.values():
            w.writerow(c)
    accepted = [c for c in cands.values() if c["status"] == "accepted"]
    write_json(run.path("youtube_cc_accepted.json"),
               [{k: c[k] for k in CAND_COLS} | {"credit": credit_line(c, cfg)} for c in accepted])
    readme = run.path("README.md")
    readme.write_text(
        "# KANG v15 - YouTube CC BY fetch\n\n"
        "Only videos whose yt-dlp metadata field `license` is exactly "
        f"\"{cfg['licence_required']}\" are accepted; the YouTube 'Creative Commons' search filter is only a pre-filter.\n"
        "Credit line per clip: \"Title — Channel (YouTube), CC BY 3.0\".\n\n"
        "**Rights:** YouTube's Terms of Service on downloading are a grey area even for CC BY videos. "
        "Recorded here, NOT cleared (user 2026-11-04: no publishing for now).\n\n"
        f"Search: {sum(s['found'] for s in search_log)} hits over {len(search_log)} queries; unique {len(cands)}; "
        f"probed {probed}; accepted {len(accepted)}.\n"
        + (f"\n**BLOCKED:** {blocked} - attempts: {json.dumps(blocked.attempts, ensure_ascii=False)}\n" if blocked else ""),
        encoding="utf-8")
    for p, k in ((csv_p, "youtube_cc_candidates"), (run.path("youtube_cc_accepted.json"), "youtube_cc_accepted"),
                 (readme, "readme")):
        run.add_output(p, k)
    counts: Dict[str, int] = {}
    for c in cands.values():
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    run.log_step("youtube_cc_fetch", search=search_log, counts=counts, probed=probed,
                 blocked=(blocked.attempts if blocked else None))
    status = "blocked" if blocked else "done"
    run.set_status(status)
    res = {"run_id": run.run_id, "status": status, "search": search_log, "unique": len(cands), "counts": counts,
           "probed": probed, "accepted": len(accepted), "csv": str(csv_p),
           "blocked": ({"reason": str(blocked), "attempts": blocked.attempts} if blocked else None),
           "accepted_infos": accepted}
    if blocked or search_only or not accepted:
        res.pop("accepted_infos")
        res["qa"] = {"pass": not blocked}
        return res
    res.pop("accepted_infos")
    res.update(download_cmd(run, accepted, out, cfg, runner))
    return res


def download_cmd(run: Run, accepted: List[Dict[str, Any]], out: Path, cfg: Dict[str, Any], runner: Runner) -> Dict[str, Any]:
    """Sections of accepted videos -> scene split -> shot checks -> out/YT_<id>_<n>.mp4 + CREDITS.json + pool.json."""
    cap = int(cfg["download"]["cap_bytes"])
    spent, got, shots, errors = 0, [], [], []
    raw = run.path("yt_raw")
    det = None
    try:
        from .crop_reuse import yunet_detector
        det = yunet_detector()
    except Exception:  # pragma: no cover
        det = None
    for c in accepted:
        info = c.pop("_info")
        if float(info.get("duration") or 0) > cfg["download"]["max_video_duration_s"]:
            errors.append({"video_id": c["video_id"], "error": "too long"})
            continue
        secs = plan_sections(float(info.get("duration") or 0), cfg, info.get("chapters"))
        est = est_bytes(info, secs)
        if spent + est > cap:
            errors.append({"video_id": c["video_id"], "error": f"byte cap ({spent + est} > {cap})"})
            continue
        rc, so, se = runner(download_args(c["video_id"], secs, str(raw / f"{c['video_id']}_%(section_start)s.%(ext)s"),
                                          cfg), 115.0)
        files = sorted(raw.glob(f"{c['video_id']}_*"))
        if rc != 0 or not files:
            errors.append({"video_id": c["video_id"], "error": ("blocked: " if is_blocked(se, cfg) else "") + se[-200:]})
            if is_blocked(se, cfg):
                break
            continue
        spent += sum(f.stat().st_size for f in files)
        got.append(c["video_id"])
        n = 0
        for f in files:
            ms = media_summary(f)
            d = float(ms.get("duration") or 0)
            for a, b in shots_from_cuts(scene_cuts(f, cfg["shots"]["scene_threshold"]), d, cfg["shots"]["min_shot_s"]):
                n += 1
                key = f"{c['video_id']}@{n}"
                m = analyse_shot(f, a, b, cfg, det, height=int(ms.get("height") or 0))
                if not m["reject"] and key in cfg.get("eye_rejects", {}):
                    m["reject"] = "agent eye: " + cfg["eye_rejects"][key]
                rec = {"key": key, "video_id": c["video_id"], "src": f.name, **m}
                if not m["reject"]:
                    name = f"YT_{c['video_id']}_{n:02d}.mp4"
                    cut_shot(f, a, b, out / name)
                    place = cfg.get("eye_exact", {}).get(key)
                    rec.update(file=name, label="exact" if place else "representative",
                               place=place or (c["query_place"] if c["query_place"] in c["places"].split("|")
                                              else (c["places"].split("|")[0] if c["places"] else c["query_place"])),
                               title=c["title"], channel=c["channel"], url=c["url"], upload_date=c["upload_date"],
                               licence=c["licence"], credit=credit_line(c, cfg))
                shots.append(rec)
    ok = [s for s in shots if not s["reject"]]
    write_json(out / "CREDITS.json", [{"file": s["file"], "title": s["title"], "author": s["channel"], "source": "youtube",
                                       "source_page": s["url"], "licence": cfg["credit_licence"], "licence_metadata": s["licence"],
                                       "credit": s["credit"], "upload_date": s["upload_date"], "label": s["label"],
                                       "place": s["place"], "modified": f"section {s['start']:.2f}-{s['end']:.2f} s of the "
                                       "downloaded part, audio removed, re-encoded H.264 (KANG v15)",
                                       "rights_note": "YouTube ToS on downloading: grey area, recorded not cleared"} for s in ok])
    write_json(run.path("shots.json"), shots)
    run.add_output(run.path("shots.json"), "youtube_cc_shots")
    sheet = None
    if ok:  # for the agent's eye check (eye_rejects / eye_exact in config/youtube_cc.json) before any assign
        from .stock_assign import contact_sheet
        sheet = contact_sheet([{"path": str(out / s["file"]), "label": f"{s['key']} {s['duration']:.1f}s {s['place']}\n"
                                f"{s['title'][:44]}"} for s in ok], run.path("youtube_cc_contact_sheet.jpg"))
        run.add_output(sheet, "contact_sheet")
    return {"contact_sheet": str(sheet) if sheet else None, "downloaded_videos": got, "bytes": spent, "shots": len(shots), "shots_ok": len(ok), "download_errors": errors,
            "pool_dir": _rel(out)}


def shot_key(file_name: str) -> str:
    """'YT_<video_id>_<nn>.mp4' -> '<video_id>@<n>' (the key used in shots.json / eye_rejects / eye_exact)."""
    stem = Path(file_name).stem[3:]
    vid, _, n = stem.rpartition("_")
    return f"{vid}@{int(n)}"


def apply_eye(credits: Sequence[Dict[str, Any]], cfg: Dict[str, Any], skipped: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Agent eye check AFTER the fetch (contact sheet): drop eye_rejects, relabel eye_exact shots exact + their place.
    Every other shot keeps the fetch label (representative unless eye_exact was already set at fetch time)."""
    out = []
    for c in credits:
        k = shot_key(c["file"])
        if k in cfg.get("eye_rejects", {}):
            if skipped is not None:
                skipped.append({"key": k, "file": c["file"], "reason": cfg["eye_rejects"][k]})
            continue
        c = dict(c)
        if k in cfg.get("eye_exact", {}):
            c.update(label="exact", place=cfg["eye_exact"][k])
        out.append(c)
    return out


def assign_cmd(visuals_beats: str, beats_path: str, pool_dirs: Sequence[str], out: str, *,
               hinglish_words: Optional[str] = None, fps: int = 25, v16_rules: bool = False) -> Dict[str, Any]:
    """visuals_beats CSV + YouTube CC pool folder(s) (CREDITS.json from fetch) -> new CSV with trimmed YT clips."""
    from . import beats as B
    from . import crop_reuse as C
    from .beats_package import HWORDS_DEFAULT
    from .stock_assign import trim_video
    run = Run()
    run.add_input(visuals_beats, "VISUALS_BEATS")
    run.add_input(beats_path, "BEATS")
    hw_p = Path(hinglish_words) if hinglish_words else HWORDS_DEFAULT
    run.add_input(hw_p, "HINGLISH_WORDS")
    rules = B.load_rules()
    ccfg = C.settings(rules)
    bp = json.loads(Path(beats_path).read_text(encoding="utf-8"))
    hw = json.loads(hw_p.read_text(encoding="utf-8"))
    hw = hw.get("words", hw) if isinstance(hw, dict) else hw
    roman = C.beat_roman(bp, hw)
    bpl = {k: C.narration_places(v, rules, ccfg) for k, v in roman.items()}
    ycfg = load_cfg()
    run.add_input(ROOT / "config" / "youtube_cc.json", "YOUTUBE_CC_CFG")
    pool, eye_skipped = [], []
    for d in pool_dirs:
        dd = ROOT / d if not Path(d).is_absolute() else Path(d)
        run.add_input(dd / "CREDITS.json", "CREDITS_" + dd.name)
        for c in apply_eye(json.loads((dd / "CREDITS.json").read_text(encoding="utf-8")), ycfg, eye_skipped):
            pool.append({"key": "yt:" + c["file"], "file": c["file"], "dir": str(dd), "place": c["place"], "label": c["label"],
                         "duration": float(media_summary(dd / c["file"]).get("duration") or 0), "title": c["title"],
                         "channel": c["author"], "url": c["source_page"], "credit": c["credit"]})
    rows = B.read_assign_csv(visuals_beats)
    vrules = ycfg.get("v16_rules") if v16_rules else None
    new, decisions = plan_youtube(rows, pool, bpl, lambda r: C.asset_places(r, rules, ccfg), vrules)
    clips_dir = run.path("youtube_clips")
    clips_dir.mkdir(exist_ok=True)
    credits, trims = [], []
    for c in B.merge_clips(new):
        r0 = next(r for r in new if r["beat"] == c["first_beat"])
        p = r0.get("_pick")
        if not p:
            continue
        dur = round(c["end"] * fps) / fps - round(c["start"] * fps) / fps
        name = f"YTC_{c['first_beat']}_{Path(p['file']).stem}.mp4"
        # v16: eye-set start offset (s) per pool clip, e.g. to stay clear of a dissolve the scene filter missed
        off = ((vrules or {}).get("offsets") or {}).get(p["key"])
        t = trim_video(Path(p["dir"]) / p["file"], clips_dir / name, dur, fps=fps,
                       offset=float(off) if off is not None else None)
        trims.append({"beat": c["first_beat"], "clip": name, **t, "need_frames": round(dur * fps)})
        credits.append({"file": name, "original_file": p["file"], "title": p["title"], "author": p["channel"],
                        "source_page": p["url"], "licence": "CC BY 3.0", "credit": p["credit"], "label": p["label"],
                        "modified": f"trimmed to {dur:.2f} s, 1920x1080 {fps} fps, no audio (KANG {'v16' if vrules else 'v15'})"})
        for b in c["beats"]:
            rr = next(r for r in new if r["beat"] == b)
            rr["asset"], rr["source_dir"] = name, _rel(clips_dir)
    for r in new:
        r.pop("_pick", None)
    write_json(clips_dir / "CREDITS.json", credits)
    qa = B.assign_qa(new)
    old = {r["beat"]: r for r in rows}
    allowed = {b for d in decisions if d["action"] == "replaced" and d["unit"] in ("archival", "forced")
               for b in d["beats"]} if vrules else set()
    prot = [r["beat"] for r in new if r.get("asset_source") == "youtube_cc" and old[r["beat"]]["match"] in PROTECTED
            and old[r["beat"]]["role"] != "continued_with_motion" and r["beat"] not in allowed
            and old[r["beat"]].get("asset_source") != "youtube_cc"]  # a clip from an earlier pass is not a change
    bad = [t["beat"] for t in trims if t["has_audio"] or abs((t["duration"] or 0) * fps - t["need_frames"]) > 1]
    probs = ([f"duplicates {qa['duplicates']}"] if qa["duplicates"] else []) + \
        ([f"replaced protected beat {prot}"] if prot else []) + ([f"trim length/audio {bad}"] if bad else [])
    op = B.write_assign_csv(new, run.path(Path(out).name))
    write_json(op.with_suffix(".json"), {"schema": "kang.youtube_cc_assign/1.0", "decisions": decisions, "qa": qa,
                                         "eye_rejected": eye_skipped,
                                         "problems": probs, "selected_by": "agent_under_user_delegation",
                                         "human_reviewed": False})
    run.add_output(op, "visuals_beats_csv")
    run.log_step("youtube_cc_assign", replaced=sum(1 for d in decisions if d["action"] == "replaced"))
    run.set_status("qa_failed" if probs else "done")
    return {"run_id": run.run_id, "csv": str(op), "decisions": decisions, "labels": qa["labels_by_shot"],
            "pool_items": len(pool), "eye_rejected": len(eye_skipped),
            "problems": probs, "qa": {"pass": not probs}}
