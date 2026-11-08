#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creative Layer — Step 4: Python Rules Engine (Worker + Critic)

User ka design: engine Claude NAHI hai. Koi LLM/API call nahi — sirf stdlib.
Engine teen cheezein padhta hai:
  1. rules.json   (Step 2 — 463 rules; check!=null wale machine-checkable)
  2. ORDER.md + ORDER_ADDENDUM.md ke faisle (Step 3 — is code me profiles +
     override/gate tables ke roop me; addendum A1-A14: destination loudness
     table, alternating punch-in, overshoot context, ducker maps, auto-pass)
  3. profiles.json (ORDER Section 5 ke profiles + addendum defaults — 7 profiles)

WORKER : har machine-checkable rule ko beats+profile par evaluate karta hai.
         Profile defaults, ORDER ke faislo par, rule ke raw numbers ko override
         karte hain (max_visual_gap, caption chars, LUFS, interrupt cadence,
         pause model, thumbnail cap, payoff band).
TAKRAAV: ORDER Section 2 ki seedhi — layer > evidence > profile > kam-hastakshep,
         aur Section 4 ke khaas faisle (jo aam seedhi se upar hain).
CRITIC : har evaluated rule ka PASS/FAIL, layer-wise score, overall score,
         aur human_flags — emotion/payoff/dramatic pal sirf FLAG hote hain,
         engine un par kabhi PASS/FAIL nahi deta (ORDER Section 3).

Seema: jo field beats/meta me nahi hai, wo check "data nahi — skip" hai, FAIL nahi.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULES = os.path.join(HERE, "..", "step_2_rules", "rules.json")
DEFAULT_PROFILES = os.path.join(HERE, "profiles.json")

LAYER_RANK = {"kahani": 4, "samajh": 3, "rhythm": 2, "style": 1}
LAYER_ORDER = ["kahani", "samajh", "rhythm", "style"]
EVIDENCE_RANK = {"🟢": 3, "🟡": 2, "🟠": 1}

# ---------- ORDER Section 4 ke khaas faisle: gating / override tables ----------
# Short-form ke hook rules (when: "Short ke pehle 3 seconds") — long-form par lagu nahi.
SHORT_HOOK_RULES = {"R-053", "R-054", "R-111", "R-121", "R-227"}
SHORT_PROFILES = {"shorts", "talking_reel"}
LONG_PROFILES = {"long_explainer", "long_entertainment", "hindi_hinglish"}
# Long-form opening structure rule.
LONG_HOOK_RULES = {"R-061"}
# Demo/launch video ka five-beat spine — sirf demo type par.
DEMO_ONLY_RULES = {"R-074"}
# Spoken hook <=12 shabd wale rules — ORDER #17: long-form hook band 9-24 hai,
# isliye ye sirf short profiles par chalenge.
SHORT_HOOK_WORD_RULES = {"R-030", "R-072"}
# Long-form hook word band (R-180: 9-24).
LONG_HOOK_WORD_RULES = {"R-180"}
# Visual cadence family — ORDER #2 ka ek number (profile ka max_visual_gap) inpar override.
CADENCE_OVERRIDE_RULES = {"R-134", "R-158", "R-160", "R-164", "R-221"}
CADENCE_PROFILE_GATE = {"R-134": SHORT_PROFILES, "R-164": {"shorts"}}
# Fast-section wale cadence rules — sirf pehle 30s ya 'fast' flag wale beats ke stretches.
FAST_SECTION_RULES = {"R-158", "R-221"}
# Interrupt-interval rules — ORDER #1: ghadi ka default nahi, profile ki hadd
# (explainer 120s / entertainment 60s) override karegi; series = rehook/interrupt beats.
INTERRUPT_RULES = {"R-155", "R-181"}
# Cold-open counts (words/cuts pehle 30s) — sirf long-form (ORDER #2).
COLD_OPEN_RULES = {"R-032", "R-159"}
# ASL band — fast-paced formats ke liye (beats ko shot ka proxy mana gaya).
ASL_RULES = {"R-173"}
ASL_PROFILES = {"shorts", "talking_reel", "long_entertainment"}
# B-roll cadence (marketing wali, R-167) — chhote marketing/social formats par.
BROLL_MARKETING_RULES = {"R-167"}
# Relevance gate (Samajh) aur motivated punch-in (ORDER #8 / #5) — takraav ke jode.
RELEVANCE_GATE_RULE = "R-088"   # B-roll exactness: bola wahi dikhe (check=null, ORDER #8 se gate)
MOTIVATED_PUNCH_RULE = "R-200"  # Punch-in sirf motivated, hadd ke andar
SPONSOR_AFTER_PAYOFF_RULE = "R-038"  # ORDER #9 — check=null tha, yahan machine roop diya
# --- ORDER ADDENDUM (editor round) ke khaas faisle ---
# A1: smart-cut >1s threshold sirf AUTO pehle pass ke liye (profile/meta flag auto_first_pass)
AUTO_FIRST_PASS_RULES = {"R-282"}
# A7: ye loudness band sirf broadcast/netflix destination par lagu
DESTINATION_LOUDNESS_RULES = {"R-271": ("broadcast", "netflix")}
# A8: SFX asset-level normalize — master LUFS par lagu nahi
SFX_ASSET_RULES = {"R-334"}
# Motion-piece cadence rule — aam video par lagu nahi
MOTION_PIECE_RULES = {"R-310"}


# ----------------------------------------------------------------------------
# Chhote helpers
# ----------------------------------------------------------------------------

def words_of(text):
    return len((text or "").split())


def beat_dur(b):
    return max(0.0, float(b.get("end_s", 0)) - float(b.get("start_s", 0)))


def relevant_flag(b):
    """B-roll beat ki relevance — teeno naam chalte hain: relevant / visual_relevant / broll_relevant."""
    for key in ("relevant", "visual_relevant", "broll_relevant"):
        if key in b:
            return bool(b[key])
    return None


def is_interrupt_beat(b):
    return bool(b.get("rehook") or b.get("pattern_interrupt") or b.get("interrupt"))


class Ctx:
    """Ek video ka saara derived data — evaluators isi se padhte hain."""

    def __init__(self, meta, beats, profile_name, profile):
        self.meta = meta
        self.profile_name = profile_name
        self.profile = profile
        self.beats = sorted(beats, key=lambda b: (float(b.get("start_s", 0)), str(b.get("id", ""))))
        ends = [float(b.get("end_s", 0)) for b in self.beats]
        self.duration = float(meta.get("duration_s") or (max(ends) if ends else 0))
        self.by_id = {b.get("id"): b for b in self.beats}
        # A5: overshoot ki pankti content type (motion_class) se — meta override, warna profile
        self.motion_class = meta.get("motion_class") or profile.get("motion_class") or "brand"

    def beats_of_kind(self, *kinds):
        return [b for b in self.beats if b.get("kind") in kinds]

    def first_of_kind(self, *kinds):
        bs = self.beats_of_kind(*kinds)
        return bs[0] if bs else None

    def static_stretches(self):
        """Bina visual change ke lagatar stretches.
        visual_change=true wala beat = us beat ke andar badlav hota hai (annotation);
        stretch = lagatar visual_change!=true beats ka jod (start..end)."""
        stretches, run = [], []
        for b in self.beats:
            if b.get("visual_change") is True:
                if run:
                    stretches.append(run)
                    run = []
            else:
                run.append(b)
        if run:
            stretches.append(run)
        return [(r[0].get("start_s", 0), r[-1].get("end_s", 0), r[0]) for r in stretches]

    def words_in_window(self, t0, t1):
        """Window ke andar ke shabd — overlap ke hisaab se proportional ginati."""
        total = 0.0
        for b in self.beats:
            s, e = float(b.get("start_s", 0)), float(b.get("end_s", 0))
            ov = max(0.0, min(e, t1) - max(s, t0))
            d = e - s
            if ov > 0 and d > 0:
                total += words_of(b.get("text")) * (ov / d)
        return int(round(total))

    def changes_in_window(self, t0, t1):
        return [b for b in self.beats
                if b.get("visual_change") is True and t0 <= float(b.get("start_s", 0)) < t1]


def result(status, findings=None, flags=None, note=""):
    return {"status": status, "findings": findings or [], "flags": flags or [], "note": note}


def finding(rule, ctx, beat_id, detail):
    return {"rule_id": rule["id"], "beat_id": beat_id or "global",
            "detail": detail, "layer": rule["layer"]}


def flag(rule_id, beat_id, reason, layer=None):
    return {"rule_id": rule_id, "beat_id": beat_id or "global",
            "reason": reason, "layer": layer}


# ----------------------------------------------------------------------------
# Evaluators — har check-kind ke liye ek function.
# Har evaluator (status, findings, flags, note) deta hai.
# status: "pass" | "fail" | "skip"  (skip = data/profile nahi — fail NAHI)
# ----------------------------------------------------------------------------

def ev_max_visual_gap(rule, ctx, chk):
    limit = chk["value"]
    if rule["id"] in CADENCE_OVERRIDE_RULES and ctx.profile.get("max_visual_gap_s") is not None:
        limit = ctx.profile["max_visual_gap_s"]
    if ctx.profile_name == "podcast" or ctx.profile.get("max_visual_gap_s") is None and rule["id"] in CADENCE_OVERRIDE_RULES:
        return result("skip", note="profile me visual cadence lagu nahi (audio pehle)")
    if not ctx.beats:
        return result("skip", note="beats nahi hain")
    finds = []
    for (s, e, first_beat) in ctx.static_stretches():
        gap = e - s
        seg_limit = limit
        # ORDER #2: hook ke pehle 5s me hadd aur sakht (profile.hook_window_gap_s)
        if s < 5 and ctx.profile.get("hook_window_gap_s"):
            seg_limit = min(seg_limit, ctx.profile["hook_window_gap_s"])
        if rule["id"] in FAST_SECTION_RULES:
            fast = s < 30 or any(b.get("fast") for b in ctx.beats
                                 if float(b.get("start_s", 0)) < e and float(b.get("end_s", 0)) > s)
            if not fast:
                continue
        if gap > seg_limit:
            finds.append(finding(rule, ctx, first_beat.get("id"),
                                 f"{s:g}-{e:g}s tak {gap:g}s koi visual change nahi — hadd {seg_limit:g}s (ORDER #2)"))
    if rule["id"] in FAST_SECTION_RULES and not finds:
        applicable = any(s < 30 for (s, e, _) in ctx.static_stretches()) or \
            any(b.get("fast") for b in ctx.beats)
        if not applicable:
            return result("skip", note="fast section / pehle 30s ka stretch nahi mila")
    return result("fail" if finds else "pass", finds)


def ev_interrupt_gap(rule, ctx, chk):
    events = [b for b in ctx.beats if is_interrupt_beat(b)]
    if not events:
        return result("skip", note="rehook/interrupt flag wala beat nahi — data nahi")
    limit = ctx.profile.get("interrupt_max_interval_s") or chk["value"]
    finds = []
    starts = [float(b.get("start_s", 0)) for b in events]
    for prev, cur, b in zip(starts, starts[1:], events[1:]):
        if cur - prev > limit:
            finds.append(finding(rule, ctx, b.get("id"),
                                 f"pichle re-hook/interrupt ke baad {cur - prev:g}s tak koi deliberate interrupt nahi — hadd {limit:g}s (ORDER #1)"))
    return result("fail" if finds else "pass", finds)


def ev_hook_within(rule, ctx, chk):
    what = chk.get("what", "")
    if what and ("proof" in what or "saboot" in what or "destination" in what):
        # R-359 type: vaada pehle, saboot (destination proof) hadd ke andar
        evs = [b for b in ctx.beats if b.get("proof") is True
               or b.get("kind") in ("broll", "graphic", "destination")]
        if not evs:
            return result("skip", note="proof/destination beat marked nahi — data nahi")
        first = evs[0]
        start = float(first.get("start_s", 0))
        if start <= chk["value"]:
            return result("pass")
        return result("fail", [finding(rule, ctx, first.get("id"),
                                       f"vaade ka saboot (destination proof) {start:g}s par — hadd {chk['value']:g}s")])
    hook = ctx.first_of_kind("hook")
    if hook is None:
        return result("fail", [finding(rule, ctx, "global",
                                       "koi hook beat hi nahi hai — hook window check fail")])
    start = float(hook.get("start_s", 0))
    if start <= chk["value"]:
        return result("pass")
    return result("fail", [finding(rule, ctx, hook.get("id"),
                                   f"hook {start:g}s par aata hai — hadd {chk['value']:g}s ke andar chahiye tha")])


def ev_proof_within(rule, ctx, chk):
    evs = [b for b in ctx.beats if b.get("proof") is True or b.get("kind") in ("broll", "graphic")]
    if not evs:
        return result("skip", note="proof/b-roll/graphic beat marked nahi — data nahi")
    first = evs[0]
    start = float(first.get("start_s", 0))
    if start <= chk["value"]:
        return result("pass")
    return result("fail", [finding(rule, ctx, first.get("id"),
                                   f"pehla proof/visual saboot {start:g}s par — hadd {chk['value']:g}s")])


def ev_artifact_within(rule, ctx, chk):
    promised = ctx.meta.get("promised_artifact") or any(
        b.get("promises_artifact") for b in ctx.beats)
    if not promised:
        return result("skip", note="hook ne koi artifact ka vaada nahi kiya — rule lagu nahi")
    evs = [b for b in ctx.beats if b.get("kind") in ("broll", "graphic")]
    if not evs:
        return result("fail", [finding(rule, ctx, "global",
                                       "vaada kiya gaya artifact screen par aaya hi nahi")])
    first = evs[0]
    start = float(first.get("start_s", 0))
    if start <= chk["value"]:
        return result("pass")
    return result("fail", [finding(rule, ctx, first.get("id"),
                                   f"vaada kiya artifact {start:g}s par aaya — hadd {chk['value']:g}s")])


def ev_max_first_overlay(rule, ctx, chk):
    ovs = [b for b in ctx.beats if b.get("kind") == "graphic" or b.get("overlay") is True]
    if not ovs:
        return result("skip", note="koi overlay/graphic beat nahi — data nahi")
    first = ovs[0]
    start = float(first.get("start_s", 0))
    if start <= chk["value"]:
        return result("pass")
    return result("fail", [finding(rule, ctx, first.get("id"),
                                   f"pehla text overlay {start:g}s par — hadd {chk['value']:g}s")])


def ev_min_open_loops(rule, ctx, chk):
    if not any(("open_loop_open" in b) or ("open_loop_close" in b) for b in ctx.beats):
        return result("skip", note="open_loop fields kisi beat me nahi — data nahi")
    need = chk["value"]
    alive, opened, finds = 0, False, []
    last_idx = len(ctx.beats) - 1
    for i, b in enumerate(ctx.beats):
        if b.get("open_loop_open"):
            alive += 1
            opened = True
        if opened and alive < need and i != last_idx and b.get("kind") != "payoff":
            finds.append(finding(rule, ctx, b.get("id"),
                                 f"is pal koi open loop zinda nahi (alive={alive}) — kam se kam {need} loop hamesha khula rehna chahiye"))
        if b.get("open_loop_close"):
            alive = max(0, alive - 1)
    if not opened:
        return result("fail", [finding(rule, ctx, "global",
                                       "poori video me ek bhi open loop khula hi nahi")])
    return result("fail" if finds else "pass", finds)


def ev_max_silence(rule, ctx, chk):
    pauses = ctx.beats_of_kind("pause")
    if not pauses:
        return result("skip", note="koi pause beat nahi — data nahi")
    finds, flags = [], []
    for b in pauses:
        d = beat_dur(b)
        if d > chk["value"]:
            if b.get("dramatic_pause"):
                flags.append(flag(rule["id"], b.get("id"),
                                  f"dramatic pause {d:g}s (>1s) — ORDER #7: visual/chehra use utha raha hai ya nahi, insaan dekhe",
                                  rule["layer"]))
            else:
                finds.append(finding(rule, ctx, b.get("id"),
                                     f"bina-wajah ki khamoshi {d:g}s — hadd {chk['value']:g}s, kategi (ORDER #7)"))
    return result("fail" if finds else "pass", finds, flags)


def ev_min_gap(rule, ctx, chk):
    what = chk.get("what", "")
    lo = chk.get("value", chk.get("min"))
    hi = chk.get("max")
    if what == "punch_in":
        pts = [(float(b.get("start_s", 0)), b) for b in ctx.beats if b.get("punch_in")]
        pts.sort(key=lambda x: x[0])
        if len(pts) < 2:
            return result("skip", note="punch-in beats 2 se kam — spacing ka data nahi")
        finds = [finding(rule, ctx, pts[i + 1][1].get("id"),
                         f"do punch-in ke beech {pts[i + 1][0] - pts[i][0]:g}s — kam se kam {lo:g}s (ORDER #5)")
                 for i in range(len(pts) - 1) if pts[i + 1][0] - pts[i][0] < lo]
        return result("fail" if finds else "pass", finds)
    if what == "speaker_handoff":
        pm = ctx.profile.get("pause_model", {})
        lo, hi = (pm.get("speaker_handoff_s") or [lo, hi])
        vals = [(b, float(b["gap_before_s"])) for b in ctx.beats
                if b.get("speaker_change") and "gap_before_s" in b]
        vals += [(b, beat_dur(b)) for b in ctx.beats_of_kind("pause") if b.get("handoff")]
        if not vals:
            return result("skip", note="speaker handoff ka data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"speaker handoff gap {v:g}s — band {lo:g}-{hi:g}s (ORDER #6)")
                 for (b, v) in vals if v < lo or (hi and v > hi)]
        return result("fail" if finds else "pass", finds)
    if what in ("pause_remainder", "clean_silence_cut"):
        pauses = ctx.beats_of_kind("pause")
        if what == "clean_silence_cut":
            pauses = [b for b in pauses if b.get("silence_cut")]
        if not pauses:
            return result("skip", note="pause beats nahi — data nahi")
        finds = []
        for b in pauses:
            d = beat_dur(b)
            if b.get("dramatic_pause"):
                continue
            if d < lo or (hi and d > hi):
                rng = f"kam se kam {lo:g}s" + (f", zyada se zyada {hi:g}s" if hi else "")
                finds.append(finding(rule, ctx, b.get("id"),
                                     f"pause remainder {d:g}s — {rng} (ORDER #6 pause model)"))
        return result("fail" if finds else "pass", finds)
    if what == "reaction_after_event":
        vals = []
        for i, b in enumerate(ctx.beats):
            if b.get("punchline") or b.get("kind") == "payoff":
                if isinstance(b.get("reaction_s"), (int, float)):
                    vals.append((b, float(b["reaction_s"])))
                elif i + 1 < len(ctx.beats):
                    gap = float(ctx.beats[i + 1].get("start_s", 0)) - float(b.get("end_s", 0))
                    if gap > 0:
                        vals.append((b, gap))
        if not vals:
            return result("skip", note="punchline/payoff ke baad reaction ka data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"reaction gap {v:g}s — kam se kam {lo:g}s (A11: beat ko land hone do)")
                 for b, v in vals if v < lo]
        return result("fail" if finds else "pass", finds)
    if what == "min_piece_duration":
        pieces = [b for b in ctx.beats if b.get("piece") or b.get("kind") == "shot"]
        if not pieces and ctx.profile_name in SHORT_PROFILES:
            pieces = list(ctx.beats)  # shorts me beats hi pieces hain (sliver hadd 0.5s, A3)
        if not pieces:
            return result("skip", note="shot/piece level data nahi — is profile me beats ko piece nahi mana gaya")
        finds = [finding(rule, ctx, b.get("id"),
                         f"piece/sliver {beat_dur(b):g}s — kam se kam {lo:g}s chahiye")
                 for b in pieces if 0 < beat_dur(b) < lo]
        return result("fail" if finds else "pass", finds)
    if what in ("pause_removal_threshold", "min_silence_to_cut"):
        key = "pause_removal_threshold_s" if what == "pause_removal_threshold" else "min_silence_cut_s"
        v = ctx.meta.get(key)
        if v is None:
            return result("skip", note=f"ye editor ke pass ka threshold hai — meta.{key} mile to check hoga (A1: floor 250ms)")
        if float(v) < lo:
            return result("fail", [finding(rule, ctx, "global",
                                           f"pass ka threshold {v:g}s — rule ki floor {lo:g}s se neeche hai (zabardasti kaat)")])
        return result("pass")
    return result("skip", note=f"min_gap_s what='{what}' ke liye beat field nahi")


def ev_gap_range_ms(rule, ctx, chk):
    # ORDER #6 pause model override: phrase gap ka final band profile se (0.2-0.45s)
    pm = ctx.profile.get("pause_model", {})
    rem = pm.get("remainder_range_s")
    lo = (rem[0] * 1000) if rem else chk.get("min")
    hi = (rem[1] * 1000) if rem else chk.get("max")
    pauses = [b for b in ctx.beats_of_kind("pause") if not b.get("dramatic_pause")]
    if not pauses:
        return result("skip", note="pause beats nahi — data nahi")
    finds = []
    for b in pauses:
        ms = beat_dur(b) * 1000
        if (lo and ms < lo) or (hi and ms > hi):
            finds.append(finding(rule, ctx, b.get("id"),
                                 f"phrase gap {ms:g}ms — band {lo:g}-{hi:g}ms (ORDER #6)"))
    return result("fail" if finds else "pass", finds)


def ev_max_gap_s(rule, ctx, chk):
    what = chk.get("what", "")
    if what in ("broll_or_screen_share", "broll"):
        evs = [b for b in ctx.beats if b.get("kind") in ("broll", "graphic")]
        label = "B-roll/screen-share"
    elif what == "speech_gap":
        evs = None
        pauses = [b for b in ctx.beats_of_kind("pause") if not b.get("dramatic_pause")]
        if not pauses:
            return result("skip", note="pause beats nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"speech gap {beat_dur(b):g}s — hadd {chk['value']:g}s (dead air)")
                 for b in pauses if beat_dur(b) > chk["value"]]
        return result("fail" if finds else "pass", finds)
    else:
        return result("skip", note=f"max_gap_s what='{what}' ke liye series nahi")
    if len(evs) < 2:
        return result("skip", note=f"{label} beats 2 se kam — cadence ka data nahi")
    finds = []
    starts = [float(b.get("start_s", 0)) for b in evs]
    for prev, cur, b in zip(starts, starts[1:], evs[1:]):
        if cur - prev > chk["value"]:
            finds.append(finding(rule, ctx, b.get("id"),
                                 f"{label} cadence gap {cur - prev:g}s — hadd {chk['value']:g}s"))
    return result("fail" if finds else "pass", finds)


def ev_max_per_min(rule, ctx, chk):
    what = chk.get("what", "")
    if what == "punch":
        if not any("punch_in" in b for b in ctx.beats):
            return result("skip", note="punch_in field kisi beat me nahi — data nahi")
        n = sum(1 for b in ctx.beats if b.get("punch_in"))
    elif what == "pattern_interrupt":
        n = sum(1 for b in ctx.beats if is_interrupt_beat(b))
    elif "transition" in what:
        if not any(b.get("kind") == "transition" or "transition" in b for b in ctx.beats):
            return result("skip", note="transition beats nahi — data nahi")
        n = sum(1 for b in ctx.beats if b.get("kind") == "transition" or b.get("transition"))
    else:
        return result("skip", note=f"max_per_min what='{what}' ka counter nahi")
    if not ctx.duration:
        return result("skip", note="duration nahi")
    rate = n / (ctx.duration / 60.0)
    if rate > chk["value"]:
        return result("fail", [finding(rule, ctx, "global",
                                       f"{what} rate {rate:.1f}/min — hadd {chk['value']:g}/min")])
    return result("pass")


def ev_per_min_range(rule, ctx, chk):
    what = chk.get("what", "")
    if what == "zoom_in":
        if not any(("punch_in" in b) or ("zoom" in b) for b in ctx.beats):
            return result("skip", note="punch_in/zoom field kisi beat me nahi — data nahi")
        n = sum(1 for b in ctx.beats if b.get("punch_in") or b.get("zoom"))
    else:
        return result("skip", note=f"per_min_range what='{what}' ka counter nahi")
    if not ctx.duration:
        return result("skip", note="duration nahi")
    rate = n / (ctx.duration / 60.0)
    if rate < chk["min"] or rate > chk["max"]:
        return result("fail", [finding(rule, ctx, "global",
                                       f"{what} rate {rate:.1f}/min — band {chk['min']:g}-{chk['max']:g}/min")])
    return result("pass")


def ev_max_count(rule, ctx, chk):
    what = chk.get("what", "")
    if what == "sound_effects_per_video":
        if not any("sfx" in b for b in ctx.beats):
            return result("skip", note="sfx field kisi beat me nahi — data nahi")
        n = sum(1 for b in ctx.beats if b.get("sfx"))
        if n > chk["value"]:
            return result("fail", [finding(rule, ctx, "global",
                                           f"SFX kul {n} — hadd {chk['value']:g} per video")])
        return result("pass")
    return result("skip", note=f"max_count what='{what}' ka counter nahi")


def ev_max_chars(rule, ctx, chk):
    what = chk.get("what", "")
    limit = chk["value"]
    if what == "caption_line":
        if ctx.profile.get("caption_chars") is not None:
            limit = ctx.profile["caption_chars"]  # ORDER #13: format se chars
        caps = [b for b in ctx.beats if b.get("caption_chars") is not None]
        if not caps:
            return result("skip", note="caption_chars kisi beat me nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"caption {b['caption_chars']} chars — hadd {limit:g} chars/line (profile: {ctx.profile_name}, ORDER #13)")
                 for b in caps if float(b["caption_chars"]) > limit]
        return result("fail" if finds else "pass", finds)
    if what == "title":
        n = ctx.meta.get("title_chars")
        if n is None and ctx.meta.get("title"):
            n = len(ctx.meta["title"])
        if n is None:
            return result("skip", note="title/title_chars nahi — data nahi")
        finds = []
        if n > limit:
            finds.append(finding(rule, ctx, "global", f"title {n} chars — hadd {limit:g} (ORDER #23 checklist)"))
        caps_words = ctx.meta.get("title_caps_words")
        if caps_words is None and ctx.meta.get("title"):
            caps_words = sum(1 for w in re.findall(r"[A-Za-z]+", ctx.meta["title"])
                             if len(w) > 1 and w.isupper())
        cap_limit = ctx.profile.get("title_max_caps_words", 1)
        if caps_words is not None and caps_words > cap_limit:
            finds.append(finding(rule, ctx, "global",
                                 f"title me {caps_words} shabd full-CAPS — hadd {cap_limit} (ORDER #16)"))
        return result("fail" if finds else "pass", finds)
    if what == "description":
        n = ctx.meta.get("description_chars")
        if n is None:
            return result("skip", note="description_chars nahi — data nahi")
        if n > limit:
            return result("fail", [finding(rule, ctx, "global", f"description {n} chars — hadd {limit:g}")])
        return result("pass")
    return result("skip", note=f"max_chars what='{what}' ka field nahi")


def ev_max_words(rule, ctx, chk):
    what = chk.get("what", "")
    limit = chk["value"]
    if what == "thumbnail_text":
        cap = ctx.profile.get("thumbnail_hard_cap_words")
        note = ""
        if cap is not None and limit > cap:
            limit = cap
            note = f" (ORDER #15: raw hadd {chk['value']:g} reject, hard cap {cap:g})"
        n = ctx.meta.get("thumbnail_words")
        if n is None:
            return result("skip", note="thumbnail_words nahi — data nahi")
        if n > limit:
            return result("fail", [finding(rule, ctx, "global",
                                           f"thumbnail text {n} shabd — hadd {limit:g}{note} (ORDER #15)")])
        return result("pass")
    if what == "spoken_hook":
        hook = ctx.first_of_kind("hook")
        if hook is None:
            return result("skip", note="hook beat nahi")
        n = words_of(hook.get("text"))
        if n > limit:
            return result("fail", [finding(rule, ctx, hook.get("id"),
                                           f"spoken hook {n} shabd — hadd {limit:g}")])
        return result("pass")
    if what == "on_screen_hook":
        ovs = [b for b in ctx.beats if b.get("kind") == "graphic" or b.get("overlay") is True]
        if not ovs:
            return result("skip", note="on-screen hook (graphic/overlay) nahi — data nahi")
        n = words_of(ovs[0].get("text"))
        if n > limit:
            return result("fail", [finding(rule, ctx, ovs[0].get("id"),
                                           f"on-screen hook {n} shabd — hadd {limit:g}")])
        return result("pass")
    if what == "cover_title":
        n = ctx.meta.get("cover_words")
        if n is None:
            return result("skip", note="cover_words nahi — data nahi")
        if n > limit:
            return result("fail", [finding(rule, ctx, "global", f"cover title {n} shabd — hadd {limit:g}")])
        return result("pass")
    if what in ("subtitle_line", "subtitle_chunk_bold"):
        caps = [b for b in ctx.beats if b.get("caption_words") is not None]
        if not caps:
            return result("skip", note="caption_words kisi beat me nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"subtitle chunk {b['caption_words']} shabd — hadd {limit:g}")
                 for b in caps if float(b["caption_words"]) > limit]
        return result("fail" if finds else "pass", finds)
    return result("skip", note=f"max_words what='{what}' ka field nahi")


def ev_max_words_exclusive(rule, ctx, chk):
    hook = ctx.first_of_kind("hook")
    if hook is None:
        return result("skip", note="hook beat nahi")
    n = words_of(hook.get("text"))
    if n >= chk["value"]:
        return result("fail", [finding(rule, ctx, hook.get("id"),
                                       f"bhara hua hook {n} shabd — {chk['value']:g} se KAM hona chahiye (ORDER #17, sakht)")])
    return result("pass")


def ev_word_range(rule, ctx, chk):
    what = chk.get("what", "")
    if what == "hook":
        target = ctx.first_of_kind("hook")
    elif what == "hook_overlay":
        ovs = [b for b in ctx.beats if b.get("kind") == "graphic" or b.get("overlay") is True]
        target = ovs[0] if ovs else None
    else:
        return result("skip", note=f"word_range what='{what}' ka field nahi")
    if target is None:
        return result("skip", note="target beat nahi — data nahi")
    n = words_of(target.get("text"))
    if n < chk["min"] or n > chk["max"]:
        return result("fail", [finding(rule, ctx, target.get("id"),
                                       f"{what} {n} shabd — band {chk['min']:g}-{chk['max']:g} (ORDER #17)")])
    return result("pass")


def ev_count_range(rule, ctx, chk):
    what = chk.get("what", "")
    if what == "words_first_30s":
        n = ctx.words_in_window(0, 30)
        label = "pehle 30s me shabd"
    elif what == "cuts_first_30s":
        n = len(ctx.changes_in_window(0, 30))
        label = "pehle 30s me cuts/visual changes"
    if what in ("words_first_30s", "cuts_first_30s"):
        if n < chk["min"] or n > chk["max"]:
            return result("fail", [finding(rule, ctx, "global",
                                           f"{label}: {n} — band {chk['min']:g}-{chk['max']:g} (ORDER #2 cold open)")])
        return result("pass")
    # --- Editor round ke naye count whats (bounds ek-tarfa ho sakte hain) ---
    lo, hi = chk.get("min"), chk.get("max")

    def _band_fail(n, label, bid="global"):
        if (lo is not None and n < lo) or (hi is not None and n > hi):
            return result("fail", [finding(rule, ctx, bid,
                                           f"{label}: {n} — band {lo}-{hi}")])
        return result("pass")

    if "highlighted words" in what:
        caps = [b for b in ctx.beats if isinstance(b.get("highlighted_words"), (int, float))]
        if not caps:
            return result("skip", note="highlighted_words kisi caption beat me nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"highlighted words {b['highlighted_words']} — band {lo}-{hi}")
                 for b in caps if (lo is not None and b["highlighted_words"] < lo)
                 or (hi is not None and b["highlighted_words"] > hi)]
        return result("fail" if finds else "pass", finds)
    if "cover title" in what:
        n = ctx.meta.get("cover_title_words", ctx.meta.get("cover_words"))
        if n is None:
            return result("skip", note="cover title words ka data nahi (meta.cover_title_words)")
        return _band_fail(n, "cover title words")
    if "visual styles" in what:
        n = ctx.meta.get("visual_styles")
        if n is None:
            styles = {b["style"] for b in ctx.beats if b.get("style")}
            n = len(styles) if styles else None
        if n is None:
            return result("skip", note="visual styles ka data nahi (meta.visual_styles ya beat style fields)")
        return _band_fail(n, "visual styles")
    if "decorative transitions" in what:
        if not any(b.get("kind") == "transition" or "transition" in b for b in ctx.beats):
            return result("skip", note="transition beats nahi — data nahi")
        run = maxrun = 0
        for b in ctx.beats:
            if b.get("kind") == "transition" and b.get("decorative"):
                run += 1
                maxrun = max(maxrun, run)
            else:
                run = 0
        return _band_fail(maxrun, "lagatar decorative transitions")
    if "stacked SFX" in what:
        vals = _beat_field_values(ctx, "sfx_stack")
        if not vals and isinstance(ctx.meta.get("max_sfx_stack"), (int, float)):
            vals = [({"id": "global"}, float(ctx.meta["max_sfx_stack"]))]
        if not vals:
            return result("skip", note="sfx_stack ka data nahi")
        finds = [finding(rule, ctx, b.get("id"), f"stacked SFX {v:g} — hadd {hi}")
                 for b, v in vals if hi is not None and v > hi]
        return result("fail" if finds else "pass", finds)
    if "breathing" in what:
        chapters = []
        cur = []
        for b in ctx.beats:
            if b.get("chapter_start") and cur:
                chapters.append(cur)
                cur = []
            cur.append(b)
        if cur:
            chapters.append(cur)
        if len(chapters) < 2 and not any(b.get("chapter_start") for b in ctx.beats):
            return result("skip", note="chapter boundaries nahi — data nahi")
        bad = [i + 1 for i, ch in enumerate(chapters)
               if not any(b.get("breathing_shot") or b.get("kind") == "payoff" or b.get("payoff")
                          for b in ch)]
        if bad:
            return result("fail", [finding(rule, ctx, "global",
                                           f"chapters {bad} me ek bhi breathing/payoff shot nahi — har chapter me kam se kam {lo:g} chahiye")])
        return result("pass")
    return result("skip", note=f"count_range what='{what}' ka counter nahi")


def ev_duration_range(rule, ctx, chk):
    what = chk.get("what", "")
    lo, hi = chk.get("min"), chk.get("max")
    def in_range(v):
        return (lo is None or v >= lo) and (hi is None or v <= hi)
    if what == "reels_duration":
        if ctx.profile_name not in SHORT_PROFILES and \
                (ctx.meta.get("platform") or "").lower() not in ("reels", "instagram", "tiktok"):
            return result("skip", note="reels/short duration band sirf short-form platforms par lagu")
        wins = ctx.profile.get("duration_windows_s") or {}
        plat = (ctx.meta.get("platform") or "").lower()
        win = wins.get(plat) or wins.get("reels") or wins.get("instagram")
        if win:
            lo, hi = win
        if not ctx.duration:
            return result("skip", note="duration nahi")
        if not in_range(ctx.duration):
            return result("fail", [finding(rule, ctx, "global",
                                           f"video duration {ctx.duration:g}s — band {lo:g}-{hi:g}s (ORDER #18)")])
        return result("pass")
    if what in ("clip_from_long_form", "short_span"):
        v = ctx.meta.get("clip_duration_s")
        if v is None:
            return result("skip", note="clip_duration_s nahi — ye rule source clip par hai, data nahi")
        if not in_range(float(v)):
            return result("fail", [finding(rule, ctx, "global",
                                           f"clip duration {v:g}s — band {lo:g}-{hi:g}s")])
        return result("pass")
    if what == "avg_shot_length":
        if not ctx.beats:
            return result("skip", note="beats nahi")
        asl = sum(beat_dur(b) for b in ctx.beats) / len(ctx.beats)
        if not in_range(asl):
            return result("fail", [finding(rule, ctx, "global",
                                           f"average shot length ~{asl:.1f}s (beats proxy) — band {lo:g}-{hi:g}s")])
        return result("pass")
    if what == "cta_segment":
        ctas = [b for b in ctx.beats if b.get("cta")]
        if not ctas:
            return result("skip", note="cta flag wala beat nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"), f"CTA segment {beat_dur(b):g}s — band {lo:g}-{hi:g}s")
                 for b in ctas if not in_range(beat_dur(b))]
        return result("fail" if finds else "pass", finds)
    if what in ("chapter_title_card", "title_card"):
        cards = [b for b in ctx.beats if b.get("title_card")]
        if not cards:
            return result("skip", note="title_card flag wala beat nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"), f"title card {beat_dur(b):g}s — band {lo:g}-{hi:g}s")
                 for b in cards if not in_range(beat_dur(b))]
        return result("fail" if finds else "pass", finds)
    if what == "explanation_card":
        cards = [b for b in ctx.beats if b.get("explanation_card")]
        if not cards:
            return result("skip", note="explanation_card flag wala beat nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"), f"explanation card {beat_dur(b):g}s — band {lo:g}-{hi:g}s")
                 for b in cards if not in_range(beat_dur(b))]
        return result("fail" if finds else "pass", finds)
    if what == "cold_open_tease":
        hook = ctx.first_of_kind("hook")
        if hook is None or not hook.get("tease"):
            return result("skip", note="tease flag wala hook nahi — data nahi")
        d = beat_dur(hook)
        if not in_range(d):
            return result("fail", [finding(rule, ctx, hook.get("id"),
                                           f"cold-open tease {d:g}s — band {lo:g}-{hi:g}s")])
        return result("pass")
    # --- Editor round ke naye whats: kind/flag wale beats ki lambai ---
    _kind_whats = {"scene_transition": ("transition", None),
                   "talking_head_shot": ("talking_head", "talking_head"),
                   "climax_shot": ("climax", "climax"),
                   "comedy_incident_total": ("comedy_incident", "comedy_incident"),
                   "comedy_single_cut": ("comedy_cut", "comedy_single_cut"),
                   "motion_sequence": ("motion", "motion_sequence"),
                   "text_reveal": ("text", "text_reveal"),
                   "B-roll hold": ("broll", None)}
    if what in _kind_whats:
        kind, flagname = _kind_whats[what]
        sel = [b for b in ctx.beats if b.get("kind") == kind or (flagname and b.get(flagname))]
        if not sel:
            return result("skip", note=f"'{what}' wala beat nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"{what}: beat {beat_dur(b):g}s — band {lo}-{hi}s (beats ko shot proxy mana gaya)")
                 for b in sel if not in_range(beat_dur(b))]
        return result("fail" if finds else "pass", finds)
    if "hero title" in what:
        sel = [b for b in ctx.beats if b.get("hero_title")]
        if not sel:
            return result("skip", note="hero_title flag wala beat nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"), f"hero title hold {beat_dur(b):g}s — band {lo}-{hi}s")
                 for b in sel if not in_range(beat_dur(b))]
        return result("fail" if finds else "pass", finds)
    if "screencast" in what:
        if ctx.meta.get("video_type") != "screencast" or not ctx.beats:
            return result("skip", note="screencast video nahi — data nahi")
        d = beat_dur(ctx.beats[0])
        if not in_range(d):
            return result("fail", [finding(rule, ctx, ctx.beats[0].get("id"),
                                           f"screencast opening context {d:g}s — band {lo}-{hi}s")])
        return result("pass")
    # Field-based whats: beats/meta me usi naam ke numeric fields
    _field_cands = [what, what + "_s"]
    if "aftertaste" in what:
        _field_cands.append("ending_hold_s")
    if what == "element_entrance":
        _field_cands.append("entrance_s")
    if what == "pop_total":
        _field_cands.append("pop_s")
    fvals = []
    for fc in _field_cands:
        fvals = _beat_field_values(ctx, fc)
        if fvals:
            break
    if not fvals and isinstance(ctx.meta.get(what), (int, float)):
        fvals = [({"id": "global"}, float(ctx.meta[what]))]
    if fvals:
        finds = [finding(rule, ctx, b.get("id"), f"{what}: {v:g}s — band {lo}-{hi}s")
                 for b, v in fvals if not in_range(v)]
        return result("fail" if finds else "pass", finds)
    return result("skip", note=f"duration_range_s what='{what}' beats schema me nahi (edit-level data)")


def ev_percent_range(rule, ctx, chk):
    what = chk.get("what", "")
    if what == "payoff_position_percent":
        payoff = ctx.first_of_kind("payoff")
        if payoff is None or not ctx.duration:
            return result("skip", note="payoff beat/duration nahi — data nahi")
        start = float(payoff.get("start_s", 0))
        if ctx.profile_name in SHORT_PROFILES:
            win = ctx.profile.get("payoff_shorts_window_s") or [15, 25]
            if win[0] <= start <= win[1]:
                return result("pass", note=f"short-form: payoff {start:g}s par — seconds band {win[0]:g}-{win[1]:g}s (ORDER #22)")
            return result("fail", [finding(rule, ctx, payoff.get("id"),
                                           f"payoff {start:g}s par — short-form me seconds band {win[0]:g}-{win[1]:g}s chahiye (ORDER #22)")])
        lo, hi = chk["min"], chk["max"]
        band = ctx.profile.get("payoff_position_percent")
        if band:
            lo, hi = band  # ORDER #22: long-form payoff band 55-85%
        pct = start / ctx.duration * 100.0
        if pct < lo or pct > hi:
            return result("fail", [finding(rule, ctx, payoff.get("id"),
                                           f"payoff {pct:.0f}% par hai — band {lo:g}-{hi:g}% (ORDER #22)")])
        return result("pass")
    if what == "sponsor_container_position_percent":
        sp = ctx.first_of_kind("sponsor")
        if sp is None or not ctx.duration:
            return result("skip", note="sponsor beat nahi — data nahi")
        pct = float(sp.get("start_s", 0)) / ctx.duration * 100.0
        if pct < chk["min"] or pct > chk["max"]:
            return result("fail", [finding(rule, ctx, sp.get("id"),
                                           f"sponsor {pct:.0f}% par — container band {chk['min']:g}-{chk['max']:g}% (ORDER #9)")])
        return result("pass")
    # --- Editor round (ADDENDUM): motion/animation percentages ---
    if what in ("overshoot_pct_premium", "follow_through_overshoot_pct_of_distance", "exaggeration_pct"):
        # A5 context table: pankti motion_class se tay hoti hai
        need_class = {"overshoot_pct_premium": "premium",
                      "follow_through_overshoot_pct_of_distance": "brand",
                      "exaggeration_pct": "character"}[what]
        if ctx.motion_class != need_class:
            return result("skip", note=f"overshoot ki ye pankti '{need_class}' context ke liye hai — is video ka motion_class '{ctx.motion_class}' hai (A5)")
        field = {"overshoot_pct_premium": "overshoot_pct",
                 "follow_through_overshoot_pct_of_distance": "follow_through_overshoot_pct",
                 "exaggeration_pct": "exaggeration_pct"}[what]
        vals = _beat_field_values(ctx, field)
        if not vals and isinstance(ctx.meta.get(field), (int, float)):
            vals = [({"id": "global"}, float(ctx.meta[field]))]
        if not vals:
            return result("skip", note=f"{field} ka data beats/meta me nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"{what}: {v:g}% — band {chk['min']:g}-{chk['max']:g}% (motion_class: {need_class}, A5)")
                 for b, v in vals if v < chk["min"] or v > chk["max"]]
        return result("fail" if finds else "pass", finds)
    if what == "punch_in_scale_pct":
        # A4: alternating 100<->112 sirf fast talking-head profile me
        if not ctx.profile.get("alternating_punch_in"):
            return result("skip", note="alternating punch-in sirf fast talking-head profile me hai (A4) — baaki jagah motivated-only (R-200) chalega")
        vals = [(b, float(b["scale_pct"])) for b in ctx.beats
                if b.get("punch_in") and isinstance(b.get("scale_pct"), (int, float))]
        if not vals:
            return result("skip", note="scale_pct wala punch-in beat nahi — data nahi")
        finds = [finding(rule, ctx, b.get("id"),
                         f"punch-in scale {v:g}% — alternating pair 100<->112% ke andar hona chahiye (A4)")
                 for b, v in vals if v < chk["min"] or v > chk["max"]]
        return result("fail" if finds else "pass", finds)
    if what == "creative_lut_intensity_pct":
        vals = _beat_field_values(ctx, "lut_intensity_pct")
        if not vals and isinstance(ctx.meta.get("lut_intensity_pct"), (int, float)):
            vals = [({"id": "global"}, float(ctx.meta["lut_intensity_pct"]))]
        if not vals:
            return result("skip", note="lut_intensity_pct ka data nahi")
        hi = chk["max"] if ctx.profile.get("strong_look") else 55  # A9: default band 50-55%
        finds, flags = [], []
        for b, v in vals:
            if v < chk["min"] or v > hi:
                finds.append(finding(rule, ctx, b.get("id"),
                                     f"LUT intensity {v:g}% — default band {chk['min']:g}-55% (A9); 70 tak sirf strong-look profile me"))
            elif v > 55:
                flags.append(flag(rule["id"], b.get("id"),
                                  f"LUT intensity {v:g}% strong-look band me hai — grade sundarta se juda hai, insaan dekhe (A9)",
                                  rule["layer"]))
        return result("fail" if finds else "pass", finds, flags)
    _pct_field = None
    if "split_edit" in what:
        _pct_field = "split_edit_share_pct"
    elif "exit_vs_entrance" in what:
        _pct_field = "exit_entrance_ratio_pct"
    elif "bloom" in what:
        _pct_field = "bloom_coverage_pct"
    elif "anticipation" in what:
        _pct_field = "anticipation_pct"
    elif "push_in" in what:
        _pct_field = "push_in_pct"
    elif "grain" in what:
        _pct_field = "grain_pct"
    elif "skin saturation" in what:
        _pct_field = "skin_saturation_pct"
    elif "emphasis zoom" in what:
        _pct_field = "zoom_scale_pct"
    elif "unique BGM" in what:
        if (ctx.meta.get("bgm_cues") or 0) < 20:
            return result("skip", note="BGM cues 20 se kam — variety rule (≥20 cues par) lagu nahi")
        _pct_field = "bgm_unique_pct"
    elif "motion accent" in what:
        _pct_field = "accent_transition_pct"
    if _pct_field:
        vals = _beat_field_values(ctx, _pct_field)
        if not vals and isinstance(ctx.meta.get(_pct_field), (int, float)):
            vals = [({"id": "global"}, float(ctx.meta[_pct_field]))]
        if not vals:
            return result("skip", note=f"{_pct_field} ka data beats/meta me nahi")
        lo, hi = chk.get("min"), chk.get("max")
        finds = [finding(rule, ctx, b.get("id"), f"{what}: {v:g}% — band {lo}-{hi}%")
                 for b, v in vals if (lo is not None and v < lo) or (hi is not None and v > hi)]
        return result("fail" if finds else "pass", finds)
    if what == "average_percentage_viewed":
        v = ctx.meta.get("apv_percent")
        label = "APV"
    elif what == "retention_at_end_screen":
        v = ctx.meta.get("end_screen_retention_percent")
        label = "end-screen retention"
    else:
        return result("skip", note=f"percent_range what='{what}' ka field nahi")
    if v is None:
        return result("skip", note=f"{label} analytics data nahi — publish ke baad ka data hai")
    if v < chk["min"] or v > chk["max"]:
        return result("fail", [finding(rule, ctx, "global",
                                       f"{label} {v:g}% — band {chk['min']:g}-{chk['max']:g}%")])
    return result("pass")


def ev_max_delay(rule, ctx, chk):
    if chk.get("what") != "exit_after_payoff":
        return result("skip", note=f"max_delay_s what='{chk.get('what')}' supported nahi")
    payoffs = ctx.beats_of_kind("payoff")
    if not payoffs or not ctx.duration:
        return result("skip", note="payoff beat nahi — data nahi")
    tail = ctx.duration - float(payoffs[-1].get("end_s", 0))
    if tail > chk["value"]:
        return result("fail", [finding(rule, ctx, payoffs[-1].get("id"),
                                       f"payoff ke baad {tail:g}s aur video chalta hai — hadd {chk['value']:g}s, tez exit")])
    return result("pass")


def ev_db_range(rule, ctx, chk):
    fld = chk.get("field", "")
    vals = None
    if fld:
        v = ctx.meta.get(fld)
        if v is None:
            return result("skip", note=f"meta.{fld} nahi — data nahi")
        vals = [("global", float(v))]
    else:
        what = chk.get("what", "")
        if "ducker" in what:
            v = ctx.meta.get("ducker_depth_db")
            if v is None:
                return result("skip", note="meta.ducker_depth_db nahi — data nahi (A8: default band profile me hai, 2.7-5 dB)")
            vals = [("global", float(v))]
        elif "de-hum" in what or "dehum" in what:
            v = ctx.meta.get("dehum_db")
            if v is None:
                return result("skip", note="meta.dehum_db nahi — data nahi")
            vals = [("global", float(v))]
        elif "music bed" in what:
            v = ctx.meta.get("music_bed_relative_lufs")
            if v is None:
                v = ctx.meta.get("music_bed_db_under_voice")
            if v is None:
                return result("skip", note="music bed relative level ka data nahi")
            vals = [("global", float(v))]
        elif "voice" in what and "upar" in what:
            v = ctx.meta.get("voice_above_music_db")
            if v is None:
                return result("skip", note="meta.voice_above_music_db nahi — data nahi")
            vals = [("global", float(v))]
        elif "boost" in what:
            vals = _beat_field_values(ctx, "manual_boost_db")
            vals = [(b.get("id"), v) for b, v in vals]
            if not vals:
                return result("skip", note="manual_boost_db kisi beat me nahi — data nahi")
        else:
            return result("skip", note=f"db_range what='{what}' ka field nahi")
    lo, hi = chk.get("min"), chk.get("max")
    if fld == "music_db_under_voice" and ctx.profile.get("music_db_range"):
        lo, hi = ctx.profile["music_db_range"]  # ORDER #11: ek bhasha — voice ke neeche relative dB
    finds = []
    for bid, val in vals:
        if (lo is not None and val < lo) or (hi is not None and val > hi):
            band = (f"{lo:g}" if lo is not None else "-inf") + ".." + (f"{hi:g}" if hi is not None else "+inf")
            finds.append(finding(rule, ctx, bid,
                                 f"{fld or chk.get('what')} = {val:g} dB — band {band} dB"))
    return result("fail" if finds else "pass", finds)


def ev_lufs(rule, ctx, chk):
    # A8: SFX asset-level normalize (R-334) — master LUFS par lagu NAHI
    if rule["id"] in SFX_ASSET_RULES:
        v = ctx.meta.get("sfx_lufs")
        if v is None:
            return result("skip", note="asset-level check hai (generated SFX) — meta.sfx_lufs nahi; master LUFS ispar lagu nahi")
        target, tol = chk.get("value", -16), chk.get("tolerance", 1)
        if abs(float(v) - target) > tol:
            return result("fail", [finding(rule, ctx, "global",
                                           f"SFX asset loudness {v:g} LUFS — normalize target {target:g} ±{tol:g} (asset-level, A8)")])
        return result("pass")
    # Band-style checks (editor round: min_lufs/max_lufs) — apne context gate ke saath
    if chk.get("min_lufs") is not None or chk.get("max_lufs") is not None:
        gate = (chk.get("profile") or "").lower()
        if "podcast" in gate and ctx.profile_name != "podcast" and ctx.meta.get("destination") != "podcast":
            return result("skip", note="ye loudness band podcast dialogue ke liye hai")
        if "short" in gate and ctx.profile_name not in SHORT_PROFILES and ctx.profile_name != "fast_talking_head":
            return result("skip", note="ye loudness band talking-head short-form ke liye hai")
        v = ctx.meta.get("lufs")
        if v is None:
            return result("skip", note="meta.lufs nahi — data nahi")
        lo, hi = chk.get("min_lufs"), chk.get("max_lufs")
        if (lo is not None and v < lo) or (hi is not None and v > hi):
            band = (f"{lo:g}" if lo is not None else "-inf") + ".." + (f"{hi:g}" if hi is not None else "+inf")
            return result("fail", [finding(rule, ctx, "global",
                                           f"loudness {v:g} LUFS — band {band} LUFS ({chk.get('profile', 'band')})")])
        return result("pass")
    v = ctx.meta.get("lufs")
    if v is None:
        return result("skip", note="meta.lufs nahi — data nahi")
    # A7: destination tay ho to destination table ka target sabse upar
    dest = ctx.meta.get("destination") or ctx.profile.get("destination")
    dests = ctx.profile.get("loudness_destinations") or {}
    target, tol = None, chk.get("tolerance")
    if dest and dest in dests:
        target = dests[dest]["target"]
        if tol is None:
            tol = dests[dest].get("tolerance", 1)
    if target is None:
        target = ctx.profile.get("lufs_target", chk.get("value"))  # ORDER #12: profile se target
    if target is None:
        return result("skip", note="loudness target tay nahi")
    if tol is None:
        tol = ctx.profile.get("lufs_tolerance", 1)
    finds = []
    if abs(float(v) - target) > tol:
        finds.append(finding(rule, ctx, "global",
                             f"master loudness {v:g} LUFS — target {target:g} ±{tol:g} (destination: {dest or ctx.profile_name}, ADDENDUM A7)"))
    if dest == "netflix":
        tp = ctx.meta.get("true_peak_db")
        tp_max = (dests.get("netflix") or {}).get("true_peak_max", -2)
        if tp is not None and float(tp) > tp_max:
            finds.append(finding(rule, ctx, "global",
                                 f"true peak {tp:g} dBTP — Netflix hadd {tp_max:g} dBTP (A7)"))
    return result("fail" if finds else "pass", finds)


def ev_wpm(rule, ctx, chk):
    v = ctx.meta.get("wpm")
    if v is None:
        return result("skip", note="meta.wpm nahi — data nahi")
    lo, hi = ctx.profile.get("wpm_range") or [chk["min"], chk["max"]]
    if v < lo or v > hi:
        return result("fail", [finding(rule, ctx, "global",
                                       f"narration {v:g} WPM — delivery band {lo:g}-{hi:g} (ORDER #19; planning 150 WPM alag hai)")])
    return result("pass")


def ev_min_score(rule, ctx, chk):
    v = ctx.meta.get("hook_score")
    if v is None:
        return result("skip", note="meta.hook_score nahi — data nahi (score insaan/tool dega)")
    if v < chk["value"]:
        return result("fail", [finding(rule, ctx, "global",
                                       f"hook score {v:g}/{chk.get('scale', 10)} — kam se kam {chk['value']:g} chahiye")])
    return result("pass")


def ev_min_drop_percent(rule, ctx, chk):
    # R-123 ek review-trigger hai (video ki galti nahi): drop threshold se zyada
    # ho to restructure ka signal — dono haal me ye rule "fail" nahi hota.
    v = ctx.meta.get("retention_drop_percent")
    if v is None:
        return result("skip", note="retention analytics nahi — publish ke baad ka data hai")
    if v < chk["value"]:
        return result("pass", note=f"retention drop {v:g}% — {chk['value']:g}% threshold se kam, refresh trigger lagu nahi")
    return result("pass", note=f"retention drop {v:g}% >= {chk['value']:g}% — refresh/restructure ka signal (chetaavni, fail nahi)")


def ev_min_chapter(rule, ctx, chk):
    chapters = ctx.meta.get("chapters")
    durs = []
    if isinstance(chapters, list):
        for c in chapters:
            if isinstance(c, (int, float)):
                durs.append(float(c))
            elif isinstance(c, dict) and "end_s" in c and "start_s" in c:
                durs.append(float(c["end_s"]) - float(c["start_s"]))
    if not durs:
        starts = [float(b.get("start_s", 0)) for b in ctx.beats if b.get("chapter_start")]
        if len(starts) >= 2:
            bounds = starts + [ctx.duration]
            durs = [bounds[i + 1] - bounds[i] for i in range(len(starts))]
    if not durs:
        return result("skip", note="chapters ka data nahi")
    finds = [finding(rule, ctx, "global", f"ek chapter {d:g}s ka hai — kam se kam {chk['value']:g}s (platform niyam)")
             for d in durs if d < chk["value"]]
    return result("fail" if finds else "pass", finds)


def ev_safe_zone(rule, ctx, chk):
    flagged = [b for b in ctx.beats if b.get("inside_safe_zone") is False]
    pos = [b for b in ctx.beats if "x_pct" in b and "y_pct" in b]
    if not flagged and not pos:
        return result("skip", note="overlay position/safe-zone data beats me nahi — data nahi")
    finds = [finding(rule, ctx, b.get("id"), "overlay safe zone ke bahar hai (ORDER #14 master table)")
             for b in flagged]
    for b in pos:
        if not (chk["x_min"] <= b["x_pct"] <= chk["x_max"] and chk["y_min"] <= b["y_pct"] <= chk["y_max"]):
            finds.append(finding(rule, ctx, b.get("id"),
                                 f"overlay position ({b['x_pct']:g}%, {b['y_pct']:g}%) safe zone ke bahar"))
    return result("fail" if finds else "pass", finds)


def ev_min_font(rule, ctx, chk):
    v = ctx.meta.get("font_px")
    if v is None:
        return result("skip", note="font size ka data meta me nahi")
    if v < chk["value"]:
        return result("fail", [finding(rule, ctx, "global",
                                       f"body text {v:g}px — kam se kam {chk['value']:g}px @1080p")])
    return result("pass")


def ev_max_lead(rule, ctx, chk):
    gs = [b for b in ctx.beats if "lead_s" in b]
    if not gs:
        return result("skip", note="graphic lead_s (word se kitna pehle aaya) ka data nahi")
    finds = [finding(rule, ctx, b.get("id"),
                     f"graphic apne shabd se {b['lead_s']:g}s pehle — hadd {chk['value']:g}s")
             for b in gs if float(b["lead_s"]) > chk["value"]]
    return result("fail" if finds else "pass", finds)


def ev_formula(rule, ctx, chk):
    if chk.get("what") != "on_screen_text_duration_s":
        return result("skip", note="formula ka ye roop supported nahi")
    expr = chk.get("expr", "")
    m = re.fullmatch(r"max\(\s*([\d.]+)\s*,\s*words\s*\*\s*([\d.]+)\s*\+\s*([\d.]+)\s*\)", expr or "")
    if not m:
        return result("skip", note=f"formula expr samajh nahi aaya: {expr}")
    base, per_word, extra = float(m.group(1)), float(m.group(2)), float(m.group(3))
    gs = [b for b in ctx.beats if b.get("kind") == "graphic" and words_of(b.get("text")) > 0]
    if not gs:
        return result("skip", note="text wala graphic beat nahi — data nahi")
    finds = []
    for b in gs:
        need = max(base, words_of(b.get("text")) * per_word + extra)
        if beat_dur(b) < need:
            finds.append(finding(rule, ctx, b.get("id"),
                                 f"on-screen text {words_of(b.get('text'))} shabd, {beat_dur(b):g}s dikhta hai — kam se kam {need:.1f}s chahiye (formula)"))
    return result("fail" if finds else "pass", finds)


def _beat_field_values(ctx, field):
    """Beats me kisi numeric field ki (beat, value) jodiyan."""
    return [(b, float(b[field])) for b in ctx.beats if isinstance(b.get(field), (int, float))]


def ev_min_gap_ms(rule, ctx, chk):
    # Editor round ke ms-level gap rules — beats me ms field ho to naap, warna skip
    field = {"cut_edge_true_silence": "edge_silence_ms",
             "speech_to_cut_distance": "speech_cut_distance_ms"}.get(chk.get("what", ""))
    if field is None:
        return result("skip", note=f"min_gap_ms what='{chk.get('what')}' ka field map nahi")
    vals = _beat_field_values(ctx, field)
    if not vals:
        return result("skip", note=f"{field} kisi beat me nahi — edit-level ms data nahi")
    finds = [finding(rule, ctx, b.get("id"),
                     f"{chk.get('what')}: {v:g}ms — kam se kam {chk['value']:g}ms chahiye")
             for b, v in vals if v < chk["value"]]
    return result("fail" if finds else "pass", finds)


def ev_frame_range(rule, ctx, chk):
    cands = {"follow_through_offset_frames": ["follow_through_frames", "follow_through_offset_frames"],
             "stagger": ["stagger_frames"],
             "attack_frames": ["attack_frames"]}.get(chk.get("what", ""))
    if cands is None:
        return result("skip", note=f"frame_range what='{chk.get('what')}' ka field map nahi")
    vals = []
    for f in cands:
        vals = _beat_field_values(ctx, f)
        if vals:
            break
    if not vals:
        return result("skip", note="animation frame data beats me nahi — data nahi")
    finds = [finding(rule, ctx, b.get("id"),
                     f"{chk.get('what')}: {v:g} frames — band {chk['min']:g}-{chk['max']:g} frames")
             for b, v in vals if v < chk["min"] or v > chk["max"]]
    return result("fail" if finds else "pass", finds)


def ev_ratio_range(rule, ctx, chk):
    if chk.get("what") != "longest_to_shortest_shot":
        return result("skip", note=f"ratio_range what='{chk.get('what')}' supported nahi")
    durs = [beat_dur(b) for b in ctx.beats if beat_dur(b) > 0]
    if len(durs) < 2:
        return result("skip", note="2 se kam beats — ratio ka data nahi")
    ratio = max(durs) / min(durs)
    if ratio < chk["min"] or ratio > chk["max"]:
        return result("fail", [finding(rule, ctx, "global",
                                       f"sabse lamba / sabse chhota shot (beats proxy) ratio {ratio:.1f} — band {chk['min']:g}-{chk['max']:g}")])
    return result("pass")


def ev_min_per_min(rule, ctx, chk):
    what = chk.get("what", "")
    if "caption" in what:
        if ctx.meta.get("voiceover") is not False:
            return result("skip", note="ye rule bina-voiceover film ke liye hai — VO hai ya maloom nahi")
        cues = [b for b in ctx.beats if b.get("kind") == "caption" or b.get("caption_cue")]
        has_cap_data = bool(cues) or any(("caption_cue" in b) or ("caption_chars" in b) for b in ctx.beats)
        if not has_cap_data:
            return result("skip", note="caption cue ka data beats me nahi")
        if not ctx.duration:
            return result("skip", note="duration nahi")
        rate = len(cues) / (ctx.duration / 60.0)
        if rate < chk["min"]:
            return result("fail", [finding(rule, ctx, "global",
                                           f"caption cues {rate:.1f}/min — bina-VO film me kam se kam {chk['min']:g}/min (captions hi kahani hai)")])
        return result("pass")
    return result("skip", note=f"min_per_min what='{what}' ka counter nahi")


EVALUATORS = {
    "max_visual_gap_s": ev_max_visual_gap,
    "hook_within_s": ev_hook_within,
    "proof_within_s": ev_proof_within,
    "artifact_within_s": ev_artifact_within,
    "max_first_overlay_s": ev_max_first_overlay,
    "min_open_loops_alive": ev_min_open_loops,
    "max_silence_s": ev_max_silence,
    "min_gap_s": ev_min_gap,
    "gap_range_ms": ev_gap_range_ms,
    "max_gap_s": ev_max_gap_s,
    "max_per_min": ev_max_per_min,
    "per_min_range": ev_per_min_range,
    "max_count": ev_max_count,
    "max_chars": ev_max_chars,
    "max_words": ev_max_words,
    "max_words_exclusive": ev_max_words_exclusive,
    "word_range": ev_word_range,
    "count_range": ev_count_range,
    "duration_range_s": ev_duration_range,
    "percent_range": ev_percent_range,
    "max_delay_s": ev_max_delay,
    "db_range": ev_db_range,
    "lufs_target": ev_lufs,
    "wpm_range": ev_wpm,
    "min_score": ev_min_score,
    "min_drop_percent": ev_min_drop_percent,
    "min_chapter_duration_s": ev_min_chapter,
    "safe_zone_pct": ev_safe_zone,
    "min_font_px": ev_min_font,
    "max_lead_s": ev_max_lead,
    "formula": ev_formula,
    "min_gap_ms": ev_min_gap_ms,
    "frame_range": ev_frame_range,
    "ratio_range": ev_ratio_range,
    "min_per_min": ev_min_per_min,
}

# Ye kinds beat-data se evaluate hi nahi ho sakte — edit-level micro data
# (ms fades, cut-edge/sentence padding) beats schema me hota hi nahi.
# (A2: edge padding aur jumla-saans dono edit-level hain — report me alag
# naam se aate hain, lekin naap ek hi wajah se nahi banta.)
# max_per_act yahan NAHI hai: act field mile to uska evaluator chalta hai,
# warna wo khud skip karta hai.
NOT_EVALUABLE_KINDS = {
    "fade_ms": "segment boundary par audio fade (ms) — edit-level data, beats schema me nahi",
    "padding_range_ms": "cut edge padding / jumla-saans (ms) — edit-level data, beats schema me nahi (A2)",
}


# ----------------------------------------------------------------------------
# Check normalization — editor-round ke checks me range keys ke kai roop hain
# (min_s / min_db / min_lufs / min_pct, hook me value ki jagah max_s).
# Evaluators ek hi roop (value / min / max) samajhte hain; yahan sab ek ho jata hai.
# ----------------------------------------------------------------------------

_RANGE_ALIASES = (("min", ("min_s", "min_db", "min_lufs", "min_pct")),
                  ("max", ("max_s", "max_db", "max_lufs", "max_pct")))


def norm_check(chk):
    if not isinstance(chk, dict):
        return chk
    c = dict(chk)
    if c.get("value") is None and c.get("kind") == "hook_within_s" and c.get("max_s") is not None:
        c["value"] = c["max_s"]
    for base, aliases in _RANGE_ALIASES:
        if c.get(base) is None:
            for a in aliases:
                if c.get(a) is not None:
                    c[base] = c[a]
                    break
    return c


def gate_skip(rule, ctx):
    """Profile/context gating — ORDER ke faislo se. (skip_reason ya None)"""
    rid = rule["id"]
    p = ctx.profile_name
    if rid in SHORT_HOOK_RULES and p not in SHORT_PROFILES:
        return "ye hook rule short-form ke liye hai — is profile par lagu nahi"
    if rid in LONG_HOOK_RULES and p not in LONG_PROFILES:
        return "ye long-form opening ka rule hai — is profile par lagu nahi"
    if rid in DEMO_ONLY_RULES and ctx.meta.get("video_type") != "demo":
        return "sirf demo/launch video par lagu"
    if rid in SHORT_HOOK_WORD_RULES and p not in SHORT_PROFILES:
        return "ORDER #17: long-form hook band 9-24 shabd hai — 12-wala sakht rule sirf short-form par"
    if rid in LONG_HOOK_WORD_RULES and p in SHORT_PROFILES:
        return "ORDER #17: short-form hook <12 shabd wala rule chalega, 9-24 band nahi"
    if rid in CADENCE_PROFILE_GATE and p not in CADENCE_PROFILE_GATE[rid]:
        return "is cadence rule ka format is profile se alag hai — profile cadence chalegi"
    if rid in COLD_OPEN_RULES and p not in LONG_PROFILES:
        return "cold-open band sirf long-form par (ORDER #2)"
    if rid in ASL_RULES and p not in ASL_PROFILES:
        return "ASL band fast-paced formats ke liye hai"
    if rid in BROLL_MARKETING_RULES and p not in SHORT_PROFILES:
        return "ye B-roll cadence marketing/short videos ke liye hai"
    # --- ORDER ADDENDUM ke gates ---
    if rid in AUTO_FIRST_PASS_RULES and not (ctx.profile.get("auto_first_pass") or ctx.meta.get("auto_first_pass")):
        return "smart-cut >1s threshold sirf AUTO pehle pass ke liye hai (ADDENDUM A1) — haath ke pass me 400ms model chalega"
    if rid in DESTINATION_LOUDNESS_RULES:
        dest = ctx.meta.get("destination") or ctx.profile.get("destination")
        if dest not in DESTINATION_LOUDNESS_RULES[rid] and p != "broadcast":
            return "ye loudness band broadcast/netflix destination ke liye hai (ADDENDUM A7)"
    chk0 = rule.get("check") or {}
    if chk0.get("scope") == "short-form" and p not in SHORT_PROFILES:
        return "ye rule short-form scope ka hai — is profile par lagu nahi"
    if rid in MOTION_PIECE_RULES and not (ctx.meta.get("motion_piece")
                                          or ctx.meta.get("video_type") == "motion_piece"
                                          or any(b.get("kind") == "motion" for b in ctx.beats)):
        return "ye motion-piece ka cadence rule hai — aam video par lagu nahi"
    return None


def evaluate_rule(rule, ctx):
    raw = rule.get("check")
    if raw is None:
        return None  # critic/human hisse me jayega
    kind = raw.get("kind")
    chk = norm_check(raw)
    if kind in NOT_EVALUABLE_KINDS:
        return result("skip", note="not_evaluable: " + NOT_EVALUABLE_KINDS[kind])
    gs = gate_skip(rule, ctx)
    if gs:
        return result("skip", note=gs)
    if kind == "max_per_act":
        # act data ho to ginati, warna skip (schema me act nahi hota aam taur par)
        acts = {}
        for b in ctx.beats:
            if "act" in b and is_interrupt_beat(b):
                acts[b["act"]] = acts.get(b["act"], 0) + 1
        if not acts:
            return result("skip", note="act/interrupt data nahi — skip")
        finds = [finding(rule, ctx, "global", f"act {a} me {n} pattern interrupt — hadd {chk['value']:g}/act")
                 for a, n in acts.items() if n > chk["value"]]
        return result("fail" if finds else "pass", finds)
    fn = EVALUATORS.get(kind)
    if fn is None:
        return result("skip", note=f"kind '{kind}' ka evaluator nahi bana")
    if kind == "max_visual_gap_s" and rule["id"] in INTERRUPT_RULES:
        return ev_interrupt_gap(rule, ctx, chk)
    return fn(rule, ctx, chk)


# ----------------------------------------------------------------------------
# ORDER #9 — R-038 (sponsor pehle payoff ke baad hi): check=null tha,
# ORDER ke faisle se ise machine roop diya gaya hai.
# ----------------------------------------------------------------------------

def evaluate_sponsor_order(rule, ctx):
    sp = ctx.first_of_kind("sponsor")
    payoff = ctx.first_of_kind("payoff")
    if sp is None:
        return result("skip", note="sponsor beat nahi — data nahi")
    if payoff is None:
        return result("skip", note="payoff beat nahi — sponsor ki jagah napna adhura data hai")
    if float(sp.get("start_s", 0)) < float(payoff.get("start_s", 0)):
        return result("fail", [finding(rule, ctx, sp.get("id"),
                                       f"sponsor {float(sp.get('start_s', 0)):g}s par hai, pehla payoff {float(payoff.get('start_s', 0)):g}s par — sponsor pehle payoff ke BAAD hi (ORDER #9)")])
    return result("pass")


# ----------------------------------------------------------------------------
# TAKRAAV (conflicts) — ORDER Section 2 ki seedhi + Section 4 ke khaas faisle
# ----------------------------------------------------------------------------

def resolve_by_order(rule_a, rule_b):
    """Aam seedhi: layer > evidence. Jeetne wale ka (winner, basis)."""
    la, lb = LAYER_RANK.get(rule_a["layer"], 0), LAYER_RANK.get(rule_b["layer"], 0)
    if la != lb:
        w = rule_a if la > lb else rule_b
        return w, f"layer: {w['layer']} upar hai (Kahani > Samajh > Rhythm > Style — ORDER §2.1)"
    ea, eb = EVIDENCE_RANK.get(rule_a.get("evidence"), 0), EVIDENCE_RANK.get(rule_b.get("evidence"), 0)
    if ea != eb:
        w = rule_a if ea > eb else rule_b
        return w, f"ek hi layer me evidence: {w.get('evidence')} wala rule jeeta (ORDER §2.2)"
    return None, "barabar — profile/kam-hastakshep dekho (ORDER §2.3/2.4)"


def detect_conflicts(ctx, rule_results, rules_by_id):
    """Do pakke cases (ORDER #8 aur #5) + relevance gate ke findings."""
    resolutions = []
    extra_findings = []
    cadence_fails = [rr for rr in rule_results
                     if rr["status"] == "fail" and (rules_by_id[rr["rule_id"]].get("check") or {}).get("kind") == "max_visual_gap_s"
                     and rr["rule_id"] not in INTERRUPT_RULES]
    gate_rule = rules_by_id.get(RELEVANCE_GATE_RULE)

    # --- Case (a): cadence vs relevance gate (ORDER #8) ---
    irrelevant = [b for b in ctx.beats if b.get("kind") == "broll" and relevant_flag(b) is False]
    for b in irrelevant:
        extra_findings.append({"rule_id": RELEVANCE_GATE_RULE, "beat_id": b.get("id"),
                               "detail": "ye B-roll bola gaya shabd/visual nahi dikhata — relevance gate fail (bola wahi dikhe, ORDER #8)",
                               "layer": "samajh"})
    if cadence_fails and irrelevant:
        for rr in cadence_fails:
            for b in irrelevant:
                resolutions.append({
                    "beat": b.get("id"),
                    "winner_rule": RELEVANCE_GATE_RULE,
                    "loser_rule": rr["rule_id"],
                    "basis": "layer: samajh > rhythm — relevance gate hamesha jeetega; cadence sajawati B-roll se nahi, punch-in/graphic/layout badlav se puri hogi (ORDER §2.1 + faisla #8)",
                })

    # --- Case (b): cadence punch-in vs motivated-only (ORDER #5) ---
    # A4 apvaad: fast talking-head profile me alternating 100<->112% pattern
    # khud ek wajah hai — wahan scale 112 wale pattern punches par R-200 nahi lagega.
    alternating_ok = bool(ctx.profile.get("alternating_punch_in"))
    unmotivated = [b for b in ctx.beats if b.get("punch_in") and b.get("motivated") is False
                   and not (alternating_ok and b.get("scale_pct") == 112)]
    punch_rule = rules_by_id.get(MOTIVATED_PUNCH_RULE)
    for b in unmotivated:
        extra_findings.append({"rule_id": MOTIVATED_PUNCH_RULE, "beat_id": b.get("id"),
                               "detail": "punch-in bina wajah (unmotivated) — default sirf motivated punch-in chalega (ORDER #5)",
                               "layer": "style"})
    if cadence_fails and unmotivated:
        for rr in cadence_fails:
            for b in unmotivated:
                resolutions.append({
                    "beat": b.get("id"),
                    "winner_rule": MOTIVATED_PUNCH_RULE,
                    "loser_rule": rr["rule_id"],
                    "basis": "ORDER faisla #5 (khaas faisla): punch-in default sirf motivated hai; cadence ki demand unmotivated punch-in ko justify nahi karti — cadence dusre badlav (graphic/layout) se puri hogi",
                })
    return resolutions, extra_findings


# ----------------------------------------------------------------------------
# HUMAN FLAGS — check=null rules + ORDER Section 3 (emotion insaan par)
# ----------------------------------------------------------------------------

HUMAN_SIGNALS = [
    (("emotion", "jazbaat", "bhavna", "jazbati"), lambda b: bool(b.get("emotion_peak")), "emotion wala pal"),
    (("payoff",), lambda b: b.get("kind") == "payoff", "payoff wala pal"),
    (("dramatic",), lambda b: bool(b.get("dramatic_pause")), "dramatic pause wala pal"),
    (("sponsor",), lambda b: b.get("kind") == "sponsor", "sponsor wala pal"),
    (("hook",), lambda b: b.get("kind") == "hook", "hook wala pal"),
    (("open loop", "loop zinda"), lambda b: bool(b.get("open_loop_open")), "open loop khulne wala pal"),
]


# ----------------------------------------------------------------------------
# LANGUAGE PASS — Hindi/Hinglish flag sanket (flag_keywords_hi.json)
# Purane flags structural fields (emotion_peak / kind / dramatic_pause) par
# chalte hain; ASR/narration beats me wo fields aksar hote hi nahi — isiliye
# beat ke TEXT se bhi topic pehchanna padta hai (Devanagari + Roman Hinglish).
# Ye koi alag system nahi: flags usi build_human_flags ki list me jate hain.
# ----------------------------------------------------------------------------

FLAG_KEYWORDS_PATH = os.path.join(HERE, "flag_keywords_hi.json")
_FLAG_TOPICS_CACHE = None

# Nukta wale akshar unke bina-nukta roop me — ASR kabhi ख़ास kabhi खास likhta hai.
_NUKTA_FORMS = {"क़": "क", "ख़": "ख", "ग़": "ग", "ज़": "ज", "फ़": "फ",
                "ड़": "ड", "ढ़": "ढ", "ऱ": "र"}
# Roman Hinglish ke aam spelling badlav — dono taraf (text aur keyword) ek hi
# map lagta hai, isliye bahot/bahut, fir/phir jaise jode hamesha mil jate hain.
_ROMAN_VARIANTS = {
    "bahot": "bahut", "bohot": "bahut", "boht": "bahut",
    "fir": "phir",
    "aakhirkar": "aakhirkaar", "akhirkkar": "aakhirkaar",
    "khaas": "khas", "khass": "khas",
    "zarur": "zaroor",
    "dhyaan": "dhyan",
    "sawaal": "sawal",
    "jante": "jaante",
    "manyata": "maanyata",
    "darsan": "darshan",
    "aashirwad": "aashirwaad",
    "pooja": "puja",
}
_FLAG_PUNCT_RE = re.compile(r"[,.\!?;:()\[\]{}'\"।॥\-–—/\\|•…*]")


def normalize_flag_text(s):
    """Flag matching ke liye text ko token list me badlo: lowercase,
    punctuation strip, nukta hatao, chandrabindu (ँ) ko anusvara (ं) mano,
    zero-width akshar hatao, Roman variants ko ek roop me lao."""
    s = (s or "").lower()
    s = s.replace("​", "").replace("‌", "").replace("‍", "")
    for a, b in _NUKTA_FORMS.items():
        s = s.replace(a, b)
    s = s.replace("ँ", "ं")
    s = _FLAG_PUNCT_RE.sub(" ", s)
    return [_ROMAN_VARIANTS.get(t, t) for t in s.split()]


def _flag_tok_match(kw_tok, txt_tok):
    if kw_tok == txt_tok:
        return True
    # Lambey Devanagari shabd par pratyay lag jata hai (मान्यता -> मान्यताओं),
    # isliye kam se kam 4 akshar wale keyword par prefix match bhi chalega.
    return len(kw_tok) >= 4 and txt_tok.startswith(kw_tok)


def _flag_phrase_in(txt_toks, kw_toks):
    """Keyword ke tokens text me lagataar aaye hon to match."""
    n = len(kw_toks)
    if n == 0 or len(txt_toks) < n:
        return False
    return any(all(_flag_tok_match(kw_toks[i], txt_toks[j + i]) for i in range(n))
               for j in range(len(txt_toks) - n + 1))


def load_flag_topics():
    """flag_keywords_hi.json se topics — har topic ke keywords pehle se
    normalized token lists me. File na mile to khaali list (purana vyavhaar)."""
    global _FLAG_TOPICS_CACHE
    if _FLAG_TOPICS_CACHE is None:
        topics = []
        try:
            with open(FLAG_KEYWORDS_PATH, encoding="utf-8") as f:
                raw = json.load(f)
            for key, spec in (raw.get("topics") or {}).items():
                kws = []
                for form in ("devanagari", "roman", "variants", "english"):
                    for kw in spec.get(form, []):
                        toks = normalize_flag_text(kw)
                        if toks:
                            kws.append((kw, toks))
                if kws:
                    topics.append({"key": key, "label": spec.get("label", key),
                                   "layer": spec.get("layer", "kahani"),
                                   "keywords": kws})
        except Exception:
            topics = []
        _FLAG_TOPICS_CACHE = topics
    return _FLAG_TOPICS_CACHE


def build_human_flags(rules, ctx):
    flags = []
    flagged_beats = set()
    for rule in rules:
        if rule.get("check") is not None:
            continue
        # Signal sirf name+when se — action ka lamba text galat pal par flag laga deta tha
        text = (rule.get("name", "") + " " + rule.get("when", "")).lower()
        for needles, pred, label in HUMAN_SIGNALS:
            if any(n in text for n in needles):
                for b in ctx.beats:
                    if pred(b):
                        flags.append(flag(rule["id"], b.get("id"),
                                          f"{label} — rule '{rule['name']}' is pal par lagu hai; faisla insaan ka (ORDER §3)",
                                          rule["layer"]))
                        flagged_beats.add(b.get("id"))
                break
    # ORDER §3 generic flag: emotion/payoff/dramatic pal — koi rule match ho ya na ho
    for b in ctx.beats:
        if (b.get("emotion_peak") or b.get("kind") == "payoff" or b.get("dramatic_pause")) \
                and b.get("id") not in flagged_beats:
            flags.append(flag("ORDER-§3", b.get("id"),
                              "emotion/payoff/dramatic pal — engine naapta nahi, insaan ki nazar ke liye flag (ORDER §3)",
                              "kahani"))
    # LANGUAGE PASS: beat ke text se Hindi/Hinglish topic sanket (upar wala section).
    # Har beat par har topic ka zyada se zyada EK flag; structural flags se alag
    # jaankari hai, isliye unke saath-saath rehta hai.
    topics = load_flag_topics()
    if topics:
        for b in ctx.beats:
            toks = normalize_flag_text(b.get("text"))
            if not toks:
                continue
            for topic in topics:
                hit = next((orig for orig, ktoks in topic["keywords"]
                            if _flag_phrase_in(toks, ktoks)), None)
                if hit:
                    flags.append(flag(
                        "LANG:" + topic["key"], b.get("id"),
                        f"text me {topic['label']} ka sanket ('{hit}') — engine naapta nahi, "
                        "insaan ki nazar ke liye flag (ORDER §3)",
                        topic["layer"]))
    return flags


# ----------------------------------------------------------------------------
# WORKER + CRITIC
# ----------------------------------------------------------------------------

def run_engine(data, rules, profiles, profile_override=None):
    meta = dict(data.get("meta") or {})
    beats = data.get("beats") or []
    profile_name = profile_override or meta.get("profile") or "long_explainer"
    if profile_name not in profiles:
        raise ValueError(f"profile '{profile_name}' profiles.json me nahi hai")
    profile = profiles[profile_name]
    ctx = Ctx(meta, beats, profile_name, profile)
    rules_by_id = {r["id"]: r for r in rules}

    rule_results, all_findings, all_flags = [], [], []
    for rule in rules:
        rid = rule["id"]
        if rule.get("check") is None and rid != SPONSOR_AFTER_PAYOFF_RULE:
            continue
        if rid == SPONSOR_AFTER_PAYOFF_RULE:
            res = evaluate_sponsor_order(rule, ctx)
        else:
            res = evaluate_rule(rule, ctx)
        if res is None:
            continue
        rule_results.append({"rule_id": rid, "name": rule["name"], "layer": rule["layer"],
                             "evidence": rule.get("evidence"), "status": res["status"],
                             "note": res["note"], "findings": res["findings"]})
        all_findings.extend(res["findings"])
        all_flags.extend(res["flags"])

    resolutions, gate_findings = detect_conflicts(ctx, rule_results, rules_by_id)
    all_findings.extend(gate_findings)
    # gate findings R-088 human-list se nikal kar critic me ginne ke liye:
    # R-088 ka apna result entry banao agar gate fail hua
    if gate_findings:
        gate_res = [f for f in gate_findings if f["rule_id"] == RELEVANCE_GATE_RULE]
        rule_results.append({"rule_id": RELEVANCE_GATE_RULE,
                             "name": rules_by_id[RELEVANCE_GATE_RULE]["name"],
                             "layer": "samajh", "evidence": rules_by_id[RELEVANCE_GATE_RULE].get("evidence"),
                             "status": "fail", "note": "ORDER #8 relevance gate (worker ne lagaya)",
                             "findings": gate_res})

    human_flags = build_human_flags(rules, ctx)
    all_flags.extend(human_flags)

    # ---- CRITIC ----
    evaluated = [rr for rr in rule_results if rr["status"] in ("pass", "fail")]
    passed = [rr for rr in evaluated if rr["status"] == "pass"]
    layer_scores = {}
    for layer in LAYER_ORDER:
        ev = [rr for rr in evaluated if rr["layer"] == layer]
        ps = [rr for rr in ev if rr["status"] == "pass"]
        layer_scores[layer] = {"evaluated": len(ev), "passed": len(ps),
                               "score_pct": round(100.0 * len(ps) / len(ev), 1) if ev else None}
    human_rules = [r for r in rules if r.get("check") is None and r["id"] != SPONSOR_AFTER_PAYOFF_RULE]
    summary = {
        "profile": profile_name,
        "platform": meta.get("platform"),
        "duration_s": ctx.duration,
        "total_rules": len(rules),
        "machine_checkable": sum(1 for r in rules if r.get("check") is not None),
        "human_review_rules": len(human_rules),
        "evaluated": len(evaluated),
        "passed": len(passed),
        "failed": len(evaluated) - len(passed),
        "skipped": len([rr for rr in rule_results if rr["status"] == "skip"]),
        "findings_count": len(all_findings),
        "resolutions_count": len(resolutions),
        "human_flags_count": len(all_flags),
        "overall_score_pct": round(100.0 * len(passed) / len(evaluated), 1) if evaluated else None,
        "layer_scores": layer_scores,
    }
    return {"summary": summary, "rule_results": rule_results, "findings": all_findings,
            "resolutions": resolutions, "human_flags": all_flags}


# ----------------------------------------------------------------------------
# Report (Markdown, Hinglish)
# ----------------------------------------------------------------------------

def render_md(report):
    s = report["summary"]
    lines = ["# Engine Report — Creative Layer Rules Engine", ""]
    lines.append(f"**Profile:** {s['profile']} · **Platform:** {s.get('platform') or '-'} · "
                 f"**Duration:** {s['duration_s']:g}s")
    lines.append("")
    lines.append("## Saar (Summary)")
    lines.append(f"- Kul rules: **{s['total_rules']}** (machine-checkable: {s['machine_checkable']}, "
                 f"insaan ki nazar wale: {s['human_review_rules']})")
    lines.append(f"- Evaluate hue: **{s['evaluated']}** · PASS: **{s['passed']}** · FAIL: **{s['failed']}** · "
                 f"Skip (data/profile nahi): {s['skipped']}")
    lines.append(f"- **Overall score: {s['overall_score_pct']}%** (evaluate hue rules me se PASS)")
    lines.append(f"- Findings: {s['findings_count']} · Takraav resolutions: {s['resolutions_count']} · "
                 f"Human flags: {s['human_flags_count']}")
    lines.append("")
    lines.append("## Layer-wise score")
    lines.append("| Layer | Evaluate | PASS | Score |")
    lines.append("|---|---|---|---|")
    names = {"kahani": "Kahani", "samajh": "Samajh aana", "rhythm": "Rhythm", "style": "Style/Effect"}
    for layer in LAYER_ORDER:
        ls = s["layer_scores"][layer]
        score = f"{ls['score_pct']}%" if ls["score_pct"] is not None else "—"
        lines.append(f"| {names[layer]} | {ls['evaluated']} | {ls['passed']} | {score} |")
    lines.append("")
    lines.append("## Findings (jo toota, kahan toota)")
    if report["findings"]:
        for f in report["findings"]:
            lines.append(f"- **{f['rule_id']}** [{f['layer']}] beat `{f['beat_id']}` — {f['detail']}")
    else:
        lines.append("- Koi finding nahi. Sab machine-niyam paas.")
    lines.append("")
    lines.append("## Takraav resolutions (kaun jeeta, kyun)")
    if report["resolutions"]:
        for r in report["resolutions"]:
            lines.append(f"- Beat `{r['beat']}` — jeeta: **{r['winner_rule']}**, hara: {r['loser_rule']} · Aadhar: {r['basis']}")
    else:
        lines.append("- Koi takraav nahi mila.")
    lines.append("")
    lines.append("## Human flags (insaan ki nazar — engine yahan faisla nahi deta)")
    if report["human_flags"]:
        for f in report["human_flags"]:
            lines.append(f"- Beat `{f['beat_id']}` · {f['rule_id']} — {f['reason']}")
    else:
        lines.append("- Koi flag nahi.")
    lines.append("")
    lines.append("## Fail hue rules (detail)")
    failed = [rr for rr in report["rule_results"] if rr["status"] == "fail"]
    if failed:
        for rr in failed:
            lines.append(f"- **{rr['rule_id']}** ({rr['layer']}, {rr.get('evidence')}) {rr['name']}")
    else:
        lines.append("- Koi rule fail nahi hua.")
    lines.append("")
    lines.append("> Seema: emotion aur sundarta par engine sirf flag lagata hai — aakhiri faisla insaan ka (ORDER §3).")
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="engine.py",
        description="Creative Layer Rules Engine (worker + critic) — koi LLM nahi, sirf stdlib.")
    ap.add_argument("beats", help="beats JSON file (meta + beats)")
    ap.add_argument("--profile", default=None, help="profile override (long_explainer/long_entertainment/shorts/talking_reel/podcast)")
    ap.add_argument("--out", default=".", help="output directory (report wahi jayega)")
    ap.add_argument("--rules", default=DEFAULT_RULES, help="rules.json ka path")
    ap.add_argument("--profiles", default=DEFAULT_PROFILES, help="profiles.json ka path")
    args = ap.parse_args(argv)

    with open(args.rules, encoding="utf-8") as f:
        rules = json.load(f)
    with open(args.profiles, encoding="utf-8") as f:
        profiles = {k: v for k, v in json.load(f).items() if not k.startswith("_")}
    with open(args.beats, encoding="utf-8") as f:
        data = json.load(f)

    report = run_engine(data, rules, profiles, profile_override=args.profile)

    os.makedirs(args.out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.beats))[0]
    jpath = os.path.join(args.out, stem + ".report.json")
    mpath = os.path.join(args.out, stem + ".report.md")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(render_md(report))
    s = report["summary"]
    print(f"[engine] profile={s['profile']} evaluated={s['evaluated']} pass={s['passed']} "
          f"fail={s['failed']} skip={s['skipped']} score={s['overall_score_pct']}%")
    print(f"[engine] findings={s['findings_count']} resolutions={s['resolutions_count']} human_flags={s['human_flags_count']}")
    print(f"[engine] report: {jpath} · {mpath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
