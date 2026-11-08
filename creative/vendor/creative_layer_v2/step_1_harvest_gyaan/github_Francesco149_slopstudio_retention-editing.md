# Source: Francesco149/slopstudio — "retention-editing" skill

- **Source name:** Francesco149/slopstudio, skill at `.claude/skills/retention-editing/` (the only part of this repo extracted, per scope)
- **Repo link:** https://github.com/Francesco149/slopstudio
- **Licence:** MIT. The cloned repo `LICENSE` file is the MIT License (Copyright (c) 2026 headpats), matching the earlier verified pass. ⚠️ The repo is ARCHIVED (per the earlier verified pass; archived status cannot be re-confirmed from a clone).
- **Content map (one line):** A pre-render review gate of MEASURED rules from a studied reference corpus (5 top explainers, 246k–1M views): long-form rules (cold-open construction with first-30s word/cut counts, APV 40–55% target, ≥1 open loop always live, visual floor = perceived motion not cut count, flat per-minute pacing, 160–195 WPM narration band, sponsor-container placement, callback close) → Shorts rules (hook ≤2.5s, reverse structure, 2–4s cut cadence, VVSA 70–90% target) → a 9-point lint-style review checklist.
- **Extraction method:** `git clone --depth 1` on 2026-11-05; the skill is a single file, reproduced **verbatim** below.
- **Scope note:** The skill cites corroborating research in the repo's `docs/AGENT_TOOLING.md` and the full measured corpus in `../slopstudio-projects/research/video-study/SYNTHESIS.md` (a sibling projects folder, NOT part of this repo). Per the extraction scope, only the skill file itself is reproduced here; the numbers quoted in it are the corpus's headline figures.

---

## Extracted content (verbatim): `.claude/skills/retention-editing/SKILL.md`


---

## 📄 SOURCE FILE: `.claude/skills/retention-editing/SKILL.md` (verbatim)

---
name: retention-editing
description: Apply YouTube retention/pacing rules when structuring or reviewing a cut (hook timing, open loops, cut cadence, visual-change floor, long-form vs shorts). Use before rendering any video — as a review gate over the beats/timeline — and when a cut feels slow or a hook is weak.
---

# Retention editing

A pre-render review gate. Only YouTube's 30s "Intro" metric is official; the rest is
corroborated research (`docs/AGENT_TOOLING.md`) **plus measured numbers from our studied
reference corpus** (5 top explainers, 246k–1M views — metrics + patterns:
`../slopstudio-projects/research/video-study/SYNTHESIS.md`). Treat as defaults, not laws.

## Long-form (10–55 min)
- **Cold open = the hook, branding after.** Open mid-content (threat/countdown, absurd
  exact number, universal observation, question ladder); "hi, I'm X" lands at 0:15–1:00.
  Measured first-30s: 65–98 words, 2–7 cuts, zero throat-clearing. Pay the title/thumbnail
  promise *literally*, and state the payoff line early ("X because Y"), earn it, restate
  it verbatim near the end.
- Target **APV 40–55%** (≥50% = A-grade). Optimize percentage + hook, not raw minutes.
- **≥1 open loop live at all times**; loops can span 45 *minutes* if re-teased mid-way and
  paid off with MORE detail than the tease promised. A measured refrain (same benchmark
  artifact, new number each section) is a permanently open loop.
- **Visual floor = perceived motion, not cut count.** The corpus ranges 2.8–7.5 cuts/min —
  no invariant there. What's invariant: something relevant is always on screen and
  *moving* — footage/diagram under a floating host, in-shot animation (bars filling,
  typewriter), or an ambient-motion backdrop behind a bare host. A static host over a
  static frame >~15s is the violation; 30–50s of one shot survives only when in-shot
  animation or high narrative tension carries it.
- **Consistency beats escalation.** Measured per-minute pacing is FLAT across even 54 min
  (words 160–200 every minute, cuts never decay). No saggy middle, no frantic ramp;
  ~1 pattern interrupt per *act* (skit/prop/gag/location change), not per minute.
- Narration **160–195 WPM** measured across all five references (energetic, not rushed).
  Our old 130–150 default is too slow for this genre; reserve <150 for dense math beats.
- Sponsor/tangent containers: visually distinct, joke segue in, hard re-entry out, at
  20–33% of runtime.
- **Callback close + fast exit:** echo the cold open (phrase/location/metaphor), CTA woven
  into the theme, end within ~30s of the payoff. Bloopers ride after the end card.

## Shorts (portrait, natural-rate speech)
- **Hook ≤2.5s**, first frame high-contrast/in-focus/moving. **Reverse-structure** (payoff
  first, then explain).
- Cut every 2–4s; 6–12 visual changes per 20s; captions always. Author the **first 3s +
  last 3s first**, loop the end into the start. Target **VVSA 70–90%**. Length = the
  longest you can hold near-100% VVSA (don't cap at 30s).

## Review checklist (run over the timeline before render)
Hook paid off ≤15s / ≤2.5s? · promise-line stated early AND restated at the payoff? ·
any static host over static frame >15s (no in-shot animation)? · an open loop always
live? · per-minute pacing flat (no dead middle)? · payoff in the last 15–25%? · callback
close present? · WPM 160–195? · shorts cut cadence 2–4s? → flag violations like `lint`
does. (This drives the planned `slop.py critique`.)
