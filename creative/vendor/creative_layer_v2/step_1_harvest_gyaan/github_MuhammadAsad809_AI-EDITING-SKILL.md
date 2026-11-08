# MuhammadAsad809/AI-EDITING-SKILL — AI Editing Skill (Premiere Pro + After Effects software notes)
- Repo: MuhammadAsad809/AI-EDITING-SKILL
- Link: https://github.com/MuhammadAsad809/AI-EDITING-SKILL
- Licence: MIT License (MIT) — LICENSE file verified in clone
- Popularity: small personal repo (repo page not separately star-checked this round); created 2026, active 2026-09
- Last commit (from local clone git log): 2026-09-20
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: A general AI-editing skill repo (knowledge/, workflows/, templates/, genres/) whose per-software translation layer lives in software/. Extracted here are ONLY the two files in this round's scope — software/premiere-pro.md and software/after-effects.md (short notes: how the repo's general method is applied inside each editor — bins/labels/markers/adjustment layers, selects-before-master, smallest native tool, version caveats). The DaVinci Resolve and CapCut notes in the same folder belong to Part 2 of this round; the editor-agnostic knowledge files were not re-harvested.

---

## 📄 SOURCE FILE: `software/premiere-pro.md` (verbatim)

# [PREMIERE PRO]

Use bins, labels, markers, adjustment layers, nested sequences, keyframes, Lumetri, Essential Sound, and Dynamic Link where appropriate. Build a selects sequence before the master; use markers for downbeats and section changes. Keep effect-heavy work on adjustment layers or nests so intensity can be revised.

## Software-aware translation

1. Assemble and trim without effects.
2. Add markers for structural beats and notes for shot purpose.
3. Apply the smallest native tool that solves the problem.
4. Isolate heavy compositing or tracking and preserve editable versions.
5. Test captions, audio, color, and export in the target aspect ratio.

## Do not assume

Feature names, codecs, interpolation quality, caption behavior, and export limits change by version and device. If a requested operation is unavailable, provide a fallback using cuts, keyframes, masks, audio automation, or a rendered intermediate, and mark version-specific details for verification.

---

## 📄 SOURCE FILE: `software/after-effects.md` (verbatim)

# [AFTER EFFECTS]

Use After Effects for tracked graphics, compositing, rotoscoping, complex typography, and controlled stylization—not as a substitute for editorial structure. Send only shots that need it, preserve handles, render with alpha or an intermediate when required, and verify color management and motion blur.

## Software-aware translation

1. Assemble and trim without effects.
2. Add markers for structural beats and notes for shot purpose.
3. Apply the smallest native tool that solves the problem.
4. Isolate heavy compositing or tracking and preserve editable versions.
5. Test captions, audio, color, and export in the target aspect ratio.

## Do not assume

Feature names, codecs, interpolation quality, caption behavior, and export limits change by version and device. If a requested operation is unavailable, provide a fallback using cuts, keyframes, masks, audio automation, or a rendered intermediate, and mark version-specific details for verification.
