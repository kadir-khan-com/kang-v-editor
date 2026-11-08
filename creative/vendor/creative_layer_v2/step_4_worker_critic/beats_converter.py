#!/usr/bin/env python3
"""
beats_converter.py — Transcript + Scene Plan  ->  Engine beats JSON

STEP 4 engine (engine.py) ko khilane wala converter: Member-2 style ke
outputs (ASR transcript JSON + scene-plan JSON) se engine-schema wali
beats file banata hai.

Usool: jo cheez DATA se derive hoti hai, sirf wahi bhari jati hai.
Jo data me nahi hai (music level, LUFS, captions, punch-in, open loops...)
uska field hi nahi rakha jata — engine un checks ko "data nahi — skip"
karega, FAIL kabhi nahi. Kuch bhi invent nahi hota.

Usage:
    python3 beats_converter.py --transcript <transcript.json> \
        --scenes <scenes.json> --profile long_explainer --out <beats.json>
    (--platform optional, default: youtube)

Input formats (tolerant):
    Transcript: {"segments": [{"start": s, "end": s, "text": "..."}]}  ya bare list
    Scenes:     {"scenes": [{"scene_id"/"id", "start", "end",
                             "transcript_refs": [segment indices], ...}]}
                ya bare list. transcript_refs na ho to scene ke time-range me
                padne wale segments se text banta hai.

Output beats:
    Har scene = ek beat. kind hamesha "speech" (data narration hi kehta hai;
    "hook"/"payoff" jaise editorial label data me nahi hote, isliye nahi lagaye).
    visual_change = True har beat par (scene badalna hi visual change hai).
    text = scene ke segments ka pura joda hua text (transcript_refs se).

Meta:
    duration_s = scene-plan ke source_media.duration (ffprobe) agar ho,
                 warna aakhri scene/segment ka end.
    wpm        = kul shabd (transcript se) / transcript ke kul samay (minutes).
"""

import argparse
import json
import sys


def _get(d, *names, default=None):
    for n in names:
        if isinstance(d, dict) and d.get(n) is not None:
            return d[n]
    return default


def load_segments(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    segs = data.get("segments") if isinstance(data, dict) else data
    if not isinstance(segs, list):
        raise ValueError(f"transcript me 'segments' list nahi mili: {path}")
    out = []
    for s in segs:
        out.append({
            "start": float(_get(s, "start", "start_s")),
            "end": float(_get(s, "end", "end_s")),
            "text": str(s.get("text", "")).strip(),
        })
    out.sort(key=lambda x: x["start"])
    return out


def load_scenes(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    scenes = data.get("scenes") if isinstance(data, dict) else data
    if not isinstance(scenes, list):
        raise ValueError(f"scene plan me 'scenes' list nahi mili: {path}")
    media_duration = None
    if isinstance(data, dict):
        sm = data.get("source_media") or {}
        if isinstance(sm, dict) and sm.get("duration") is not None:
            media_duration = float(sm["duration"])
    out = []
    for sc in scenes:
        out.append({
            "scene_id": _get(sc, "scene_id", "id"),
            "start": float(_get(sc, "start", "start_s")),
            "end": float(_get(sc, "end", "end_s")),
            "refs": sc.get("transcript_refs"),
        })
    out.sort(key=lambda x: x["start"])
    return out, media_duration


def scene_text(scene, segments):
    """Scene ka pura text: pehle transcript_refs, warna time-range overlap."""
    refs = scene.get("refs")
    if refs:
        parts = [segments[i]["text"] for i in refs
                 if isinstance(i, int) and 0 <= i < len(segments)]
        if parts:
            return " ".join(p for p in parts if p)
    parts = [s["text"] for s in segments
             if s["start"] >= scene["start"] and s["end"] <= scene["end"] + 0.01]
    return " ".join(p for p in parts if p)


def convert(transcript_path, scenes_path, profile, platform):
    segments = load_segments(transcript_path)
    scenes, media_duration = load_scenes(scenes_path)

    beats = []
    for i, sc in enumerate(scenes, 1):
        beats.append({
            "id": f"b{i}",
            "start_s": sc["start"],
            "end_s": sc["end"],
            "kind": "speech",
            "text": scene_text(sc, segments),
            "visual_change": True,
        })

    total_words = sum(len(s["text"].split()) for s in segments)
    span_s = (segments[-1]["end"] - segments[0]["start"]) if segments else 0.0
    wpm = round(total_words / (span_s / 60.0), 1) if span_s > 0 else None

    if media_duration:
        duration_s = media_duration
    elif scenes:
        duration_s = scenes[-1]["end"]
    elif segments:
        duration_s = segments[-1]["end"]
    else:
        duration_s = 0.0

    meta = {"profile": profile, "platform": platform, "duration_s": duration_s}
    if wpm is not None:
        meta["wpm"] = wpm

    return {"meta": meta, "beats": beats}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Transcript + scene plan se engine beats JSON banao.")
    ap.add_argument("--transcript", required=True, help="transcript JSON path")
    ap.add_argument("--scenes", required=True, help="scene plan JSON path")
    ap.add_argument("--profile", default="long_explainer",
                    help="engine profile (default: long_explainer)")
    ap.add_argument("--platform", default="youtube",
                    help="platform (default: youtube)")
    ap.add_argument("--out", required=True, help="output beats JSON path")
    args = ap.parse_args(argv)

    data = convert(args.transcript, args.scenes, args.profile, args.platform)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"beats likhe: {args.out} ({len(data['beats'])} beats, "
          f"duration_s={data['meta']['duration_s']}, wpm={data['meta'].get('wpm')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
