"""M3 Workflow G, step 1: accepted transcript -> scenes.json (scene plan for Gate 1).

A scene is a contiguous stretch of narration (~15-45 s) split at sentence ends (। ? !) or pauses.
Scenes tile the timeline from 0 to the media duration with no gap and no overlap, so every
spoken word belongs to exactly one scene. Visual fields are placeholders the user fills or
approves; nothing here invents visuals.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

SCHEMA = "kang.scenes/1.0"
SENT_END = ("।", "?", "!", "॥", ".")


# A scene must not start with a word that continues the previous phrase ("शुरुआत | से", "135 km | की दूरी")
CONTINUES = {"जो", "जिसे", "जिसका", "जिसकी", "जिसके", "जहाँ", "जहां", "से", "की", "का", "के", "को", "में", "पर", "ने", "तक", "भी", "ही", "है", "हैं", "था", "थी", "थे",
             "वाला", "वाली", "वाले", "लिए", "द्वारा", "और", "या", "तो", "कि", "जो", "गया", "गई", "गए", "रहा",
             "रही", "रहे", "सकते", "सकता", "सकती", "जाता", "जाती", "जाते", "करके", "बाद", "पहले", "साथ", "चाहिए", "होगा", "होगी", "होंगे", "पड़ेगा",
             "पड़ता", "ज्योतिर्लिंग", "मंदिर", "जी", "महादेव", "नगरी", "दर्शन"}


def _sent_end(w: Dict[str, Any]) -> bool:
    return w["word"].rstrip().endswith(SENT_END)


# ...and must not end on a word that opens a phrase ("... में है जो | द्वारका का")
DANGLING = {"जो", "कि", "और", "या", "तो", "के", "की", "का", "ने", "को", "एक", "यह", "वह", "इस", "उस", "ये",
            "वो", "जिस", "जहाँ", "जहां", "आप", "हम", "मैं", "भगवान", "श्री", "स्वामी", "संत", "माता", "बेट",
            "बहुत", "सबसे"}


def _clean(t: str) -> str:
    return t.strip().strip(",.।?!")


def _continues(words: List[Dict[str, Any]], i: int) -> bool:
    """True when words[i+1] grammatically continues words[i]'s phrase (or words[i] dangles)."""
    if words[i]["word"].rstrip().endswith((",",) + SENT_END):
        return i + 1 < len(words) and _clean(words[i + 1]["word"]) in {"से", "की", "का", "के", "को", "में", "ने",
                                                                          "जो", "जिसे", "जिसका", "जिसकी", "जिसके"}
    if i > 0 and _clean(words[i]["word"]) == "से" and _clean(words[i - 1]["word"]) == "में":
        return True  # "... में से | एक"
    if i + 2 < len(words) and _clean(words[i + 2]["word"]) in {"है", "हैं", "था", "थी", "थे", "हो", "होता", "होती"}:
        return True  # "... भी | स्थापित है": next two words are this clause's predicate
    return i + 1 < len(words) and (_clean(words[i + 1]["word"]) in CONTINUES or _clean(words[i]["word"]) in DANGLING)


TOPIC_START = {"दोस्तो", "दोस्तों"}


def _topic_next(words: List[Dict[str, Any]], i: int) -> bool:
    """Narrator's topic opener ("दोस्तो ...") right after i: a natural scene start."""
    return i + 1 < len(words) and _clean(words[i + 1]["word"]) in TOPIC_START


def _is_break(words: List[Dict[str, Any]], i: int, pause_s: float) -> bool:
    w = words[i]
    if _sent_end(w):
        return True
    if i + 1 >= len(words):
        return False
    if (_topic_next(words, i) and words[i + 1]["start"] - w["end"] >= 0.2
            and _clean(w["word"]) not in DANGLING):  # "... लगाते हैं, तो | दोस्तों" still dangles
        return True
    if _continues(words, i):
        return False
    gap = words[i + 1]["start"] - w["end"]
    # a bare pause (no comma) needs to be long; a comma pause can be short
    return gap >= (pause_s if w["word"].rstrip().endswith(",") else max(pause_s, 1.0))


def plan_scenes(words: List[Dict[str, Any]], duration: float, target_s: float = 30.0,
                min_s: float = 15.0, max_s: float = 45.0, pause_s: float = 0.6) -> Dict[str, Any]:
    """Greedy: close a scene at the first break after target_s; if none by max_s, close at the
    widest pause inside (min_s, max_s]. Boundaries sit mid-pause so no word is ever split."""
    if not words:
        return {"schema": SCHEMA, "duration": round(duration, 3), "scenes": []}
    groups: List[List[int]] = []
    cur: List[int] = []
    seg_start = 0.0
    for i, w in enumerate(words):
        cur.append(i)
        length = w["end"] - seg_start
        last = i == len(words) - 1
        if last:
            break
        if length >= target_s and _is_break(words, i, pause_s):
            groups.append(cur)
            cur, seg_start = [], (w["end"] + words[i + 1]["start"]) / 2
        elif length >= max_s:
            # widest pause between words whose end is past min_s
            # best boundary inside (min_s, max_s]: sentence end > clean pause > any pause; widest wins
            best, best_score = len(cur) - 1, -1.0
            for k in range(len(cur) - 1):
                a, b = words[cur[k]], words[cur[k + 1]]
                if a["end"] - seg_start < min_s:
                    continue
                gap = b["start"] - a["end"]
                length = a["end"] - seg_start
                score = (100.0 if _sent_end(a) else 20.0 if a["word"].rstrip().endswith(",") else 0.0) \
                    + (50.0 if _topic_next(words, cur[k]) else 0.0) \
                    - (80.0 if _clean(a["word"]) in DANGLING else 0.0) \
                    + (10.0 if not _continues(words, cur[k]) else -40.0) + 5.0 * min(gap, 1.5) \
                    - abs(length - target_s) / 5.0
                if score > best_score:
                    best, best_score = k, score
            groups.append(cur[: best + 1])
            j = cur[best]
            seg_start = (words[j]["end"] + words[j + 1]["start"]) / 2
            cur = cur[best + 1:]
    if cur:
        if groups and words[cur[-1]]["end"] - words[cur[0]]["start"] < min_s / 2:
            groups[-1].extend(cur)  # tiny tail joins the previous scene
        else:
            groups.append(cur)
    scenes = []
    for n, g in enumerate(groups):
        start = 0.0 if n == 0 else (words[groups[n - 1][-1]]["end"] + words[g[0]]["start"]) / 2
        end = duration if n == len(groups) - 1 else (words[g[-1]]["end"] + words[groups[n + 1][0]]["start"]) / 2
        text = " ".join(words[i]["word"] for i in g)
        scenes.append({
            "id": f"S{n + 1:02d}", "start": round(start, 3), "end": round(max(end, start), 3),
            "first_word": g[0], "last_word": g[-1], "word_count": len(g),
            "title": " ".join(words[i]["word"] for i in g[:6]).rstrip("।?!,. "),
            "text": text,
            "visual": {"type": "tbd", "brief": "", "source": "", "licence": ""},
            "status": "proposed",
        })
    return {"schema": SCHEMA, "duration": round(duration, 3), "scenes": scenes}


def validate_scenes(plan: Dict[str, Any], n_words: Optional[int] = None, tol: float = 0.002) -> List[str]:
    """Problems as plain strings; [] = valid. Tiling + word ownership + required fields."""
    errs: List[str] = []
    if plan.get("schema") != SCHEMA:
        errs.append(f"schema must be {SCHEMA}")
    sc = plan.get("scenes") or []
    if not sc:
        return errs + ["no scenes"]
    if abs(sc[0]["start"]) > tol:
        errs.append(f"first scene starts at {sc[0]['start']} not 0")
    if abs(sc[-1]["end"] - plan["duration"]) > tol:
        errs.append(f"last scene ends at {sc[-1]['end']} not {plan['duration']}")
    seen = set()
    for a, b in zip(sc, sc[1:]):
        if abs(a["end"] - b["start"]) > tol:
            errs.append(f"{a['id']}->{b['id']}: gap/overlap {a['end']} vs {b['start']}")
        if b["first_word"] != a["last_word"] + 1:
            errs.append(f"{a['id']}->{b['id']}: words not contiguous")
    for s in sc:
        if s["id"] in seen:
            errs.append(f"duplicate id {s['id']}")
        seen.add(s["id"])
        if s["end"] <= s["start"]:
            errs.append(f"{s['id']}: end <= start")
        for k in ("title", "text", "visual"):
            if k not in s:
                errs.append(f"{s['id']}: missing {k}")
    if n_words is not None and (sc[0]["first_word"] != 0 or sc[-1]["last_word"] != n_words - 1):
        errs.append("scenes do not cover every word")
    return errs


def scene_plan_text(plan: Dict[str, Any]) -> str:
    def ts(t: float) -> str:
        return f"{int(t // 60):02d}:{t % 60:04.1f}"
    lines = [f"{len(plan['scenes'])} scenes, {plan['duration']:.1f} s"]
    for s in plan["scenes"]:
        lines.append(f"{s['id']}  {ts(s['start'])}-{ts(s['end'])}  {s['word_count']:3d} words  {s['title']}")
    return "\n".join(lines)
