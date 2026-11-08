"""Caption script style for English words inside Hindi narration (display layer only).

Modes:
  asr        -> captions exactly as the transcript (mixed: 'railway station' + 'थ्री डेज').  DEFAULT
  latin      -> listed Devanagari-English words/phrases shown in Latin ('three days और two night')
  devanagari -> listed Latin words shown in Devanagari ('रेलवे स्टेशन')

Only entries in config/english_script.json are changed; anything unlisted stays as transcribed and
is reported in `unmapped`. Replacement is word-for-word (same count), so every word keeps its own
start/end timing. words.json / the transcript are NEVER modified: this only feeds captions.
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

MODES = ("asr", "latin", "devanagari")
_PUNCT = re.compile(r"^(.*?)([,.!?।;:\"'\u2019\u201d]*)$", re.S)
_LATIN = re.compile(r"[A-Za-z]")


def load_table(path: str | Path) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("to_devanagari", "to_latin_phrases"):
        data.setdefault(key, {} if key == "to_devanagari" else [])
    for ph in data["to_latin_phrases"]:
        if len(ph["dev"].split()) != len(ph["lat"].split()):
            raise ValueError(f"english_script phrase must keep word count: {ph}")
    return data


def _split(tok: str) -> Tuple[str, str]:
    m = _PUNCT.match(tok)
    return (m.group(1), m.group(2)) if m else (tok, "")


def apply(words: List[Dict[str, Any]], mode: str, table: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if mode not in MODES:
        raise ValueError(f"english script mode must be one of {MODES}, got {mode!r}")
    out = copy.deepcopy(words)
    changes: List[Dict[str, Any]] = []
    if mode == "devanagari":
        tab = {k.lower(): v for k, v in table["to_devanagari"].items()}
        for i, w in enumerate(out):
            core, p = _split(w["word"])
            new = tab.get(core.lower())
            if new:
                changes.append({"i": i, "from": w["word"], "to": new + p})
                w["word"] = new + p
    elif mode == "latin":
        phrases = sorted(table["to_latin_phrases"], key=lambda ph: -len(ph["dev"].split()))
        i = 0
        while i < len(out):
            hit = None
            for ph in phrases:
                dev = ph["dev"].split()
                seg = [_split(out[j]["word"])[0] for j in range(i, min(i + len(dev), len(out)))]
                if seg == dev:
                    hit = ph
                    break
            if not hit:
                i += 1
                continue
            for k, lat in enumerate(hit["lat"].split()):
                core, p = _split(out[i + k]["word"])
                changes.append({"i": i + k, "from": out[i + k]["word"], "to": lat + p})
                out[i + k]["word"] = lat + p
            i += len(hit["dev"].split())
    unmapped = []
    if mode == "devanagari":
        unmapped = sorted({_split(w["word"])[0] for w in out if _LATIN.search(w["word"])})
    return out, {"mode": mode, "changed": len(changes), "changes": changes, "unmapped": unmapped}
