"""Per-video / per-topic caption spelling policy (opt-in, never global).

A policy file (e.g. config/caption_spelling_policy.json) is an EDITORIAL choice of display
spelling between valid variants (द्वारका vs द्वारिका). It is not an ASR fix and not a claim
that anything was listened to. It runs only when a policy is passed explicitly, after the
glossary, and every change is logged (raw ASR stays in words_raw.json / raw/).

Format: {"video": "...", "replace": {"द्वारका": "द्वारिका", ...}, "never": {"रुक्मिणी": "रुक्मणी"}}
Replacement is whole-token only (a glossary-merged entry like "बेट द्वारका" is matched token by
token), longest key first, timing untouched, word count unchanged.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

_TRAIL = re.compile(r"^(.*?)([\s,.!?।॥\"'”’…:;-]*)$", re.S)


def load_policy(path: str | Path) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rep = data.get("replace")
    if not isinstance(rep, dict) or not rep:
        raise ValueError(f"spelling policy {path}: 'replace' map missing or empty")
    for src, dst in rep.items():
        for bad_src, bad_dst in (data.get("never") or {}).items():
            if dst == bad_dst or (src == bad_src and dst == bad_dst):
                raise ValueError(f"spelling policy {path}: replace {src}->{dst} breaks never {bad_src}->{bad_dst}")
    data["_path"] = str(path)
    return data


def _apply_text(text: str, rules: List[Tuple[List[str], str]]) -> str:
    toks = text.split(" ")
    out, i = [], 0
    while i < len(toks):
        for src, dst in rules:
            n = len(src)
            seg = toks[i:i + n]
            if len(seg) == n:
                core = [_TRAIL.match(t).group(1) for t in seg]
                if core == src:
                    tail = _TRAIL.match(seg[-1]).group(2)
                    out.append(dst + tail)
                    i += n
                    break
        else:
            out.append(toks[i])
            i += 1
    return " ".join(out)


def apply_policy(words: List[Dict[str, Any]], policy: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Returns (new_words, changes). Input never mutated; one change entry per word changed."""
    rules = sorted(((k.split(), v) for k, v in policy["replace"].items()), key=lambda r: -len(r[0]))
    out, changes = [], []
    for i, w in enumerate(words):
        new = _apply_text(w["word"], rules)
        if new != w["word"]:
            changes.append({"index": i, "from": w["word"], "to": new, "start": w.get("start"),
                            "end": w.get("end"), "decided_by": "editorial-policy",
                            "policy": policy.get("video") or policy.get("_path")})
            w = {**w, "word": new}
        out.append(w)
    return out, changes
