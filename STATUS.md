# KANG - Current status (refresh: 3 November 2026, 17:35 IST)


This summary separates reported test evidence, implementation and final acceptance.

## External free sources: Openverse + Pixabay (v0.7.0-dev, 3 Nov 2026, sandbox)
| Item | Status | Evidence |
|---|---|---|
| core/openverse_fetch.py + `kang.py fetch-openverse` (by/by-sa/cc0/pdm only, min width 1600 configurable, place check, sha256 + dHash + known-Commons-title dedupe, 24 h cache) | IMPLEMENTED | tests/test_openverse_fetch.py 9 PASS (mock HTTP) |
| Openverse live fetch (3 queries: bhadkeshwar, shivrajpur, dwarka) | WARN | KANG_026 (timed out mid-download, resumed) + KANG_027: 42 results -> 7 downloaded, 23 metadata rejects (21 wrong place), 11 same Commons file already in pool, 1 Wikimedia 429. Sandbox IP got Cloudflare 429 for a while; responses fetched once outside were kept as `_seed` fallback (not used in the final runs) |
| core/pixabay_fetch.py + `kang.py fetch-pixabay` (videos; rate limiter <=95/60 s, 24 h cache, eye-ok gate before any download) | IMPLEMENTED | tests/test_pixabay_fetch.py 10 PASS (mock HTTP, incl. plan_stock + trim) |
| Pixabay auth, videos endpoint | PASS (HTTP 200) | KANG_028 pixabay_auth.json |
| Pixabay auth, images endpoint | FAIL (HTTP 400 from the credential proxy: connected URL covers /api/videos/ only), stopped after 2 tries | KANG_028 |
| Pixabay CDN downloads | PASS via direct connection (proxy returns 400 for cdn.pixabay.com; CDN needs no key) | KANG_031/032 |
| Unified asset index (Commons + Openverse + Pixabay + own) | WARN (507 items; new sources duplicate nothing; 131 old cross-folder copies + 1 old CREDITS sha mismatch in dwarika_v9) | KANG_037 assets/asset_index.json |
| `beats-stock` (stock only on continued_with_motion after a hold cap; exact same-place Openverse may replace earlier) | IMPLEMENTED | KANG_033 runs/.../visuals_beats_v12.csv |
| v12 package (140 shots, 19 PX, 19 Pixabay clips, 4 Openverse stills, 186 markers) | WARN (sandbox QA PASS, human review pending) | KANG_034 out/dwarika_v12_sources_premiere.zip -> E:\kang\packages\dwarika_v12; grid KANG_035 out/dwarika_v12_new_sources_grid.jpg |
| Premiere 24.6.1 import / playback of STK_*.mp4 stock clips | NOT_TESTED | user PC |
| Human review of the 23 new picks (labels, fit to narration) | NOT_TESTED | combined review (user pref) |
- v12 numbers: continued_with_motion beats 34 -> 11; longest shot 19.44 s (S14 Gopi Talav text card, by design);
  longest photo shot 11.44 s (S03_b03, exact, parallax); S21 27.2 -> 7.4 s, S22 22.2 -> 7.4 s, S10 Bhadkeshwar
  12.6 / 15.2 -> 5.2 / 5.4 s. Labels per shot: exact 47 (+4 Openverse Bhadkeshwar), representative 88 (+19 Pixabay),
  text_card 4, archival 1. Every Pixabay clip is 'representative'.
- Shortened parallax holds keep their v11 PX clip with in=0 (only the first part of the camera move is shown).
- Wrong-place items seen and rejected: Delhi Dwarka metro stations / Dwarka Expressway / Yashobhoomi, Shivrajpur
  (Allahabad, UP), Bardia temple, Kanpur; Pixabay: Japan/Kyoto/Osaka, ISKCON Bangalore, Taj Mahal, Manali/Himachal,
  Bengal hills, Delhi road, Switzerland, Germany, Netherlands, Italy, Greece, Bosnia, Sri Lanka, Oregon, California,
  Caribbean, New Zealand, Australia, Spain, China; eye check: British train, green-cliff foreign coast, Hong Kong
  bridge, Monument Valley, Dwarka lighthouse near-duplicate, Gurudwara Bet Dwarka (off-topic). Reasons:
  config/stock_sources.json eye_rejects.

## 2.5D parallax layer (v0.7.0-dev, 3 Nov 2026, sandbox CPU)
| Item | Status | Evidence |
|---|---|---|
| core/parallax.py + parallax / parallax-batch / parallax-apply / beats-assign --parallax / beats-package | IMPLEMENTED | tests/test_parallax.py 11 PASS (mock depth) |
| Depth model DA-V2 Small, rev 5426e4f0f36572d16453bbda7a8389317b1bef99, Apache-2.0 | PASS (licence + pin recorded) | config/model_licenses.json depth_parallax |
| 3-still test (S01_b03 temple, S21_b02 27.2 s, S22_b03 22.2 s) | PASS (agent eye check) | KANG_020, out/dwarika_v10_parallax_ab.mp4, out/dwarika_v10_parallax_grid.jpg (KANG_022) |
| Gate on 19 long-hold / continued_with_motion clips | PASS 19 / FAIL 0 (after gate fix; first pass 17 PASS / 2 FAIL) | runs/2026-11-03_KANG_023/parallax_report.csv (first pass: parallax_report_pass1.csv) |
| v11 package (19 parallax clips, 98 Ken Burns stills, 186 markers) | WARN (sandbox QA PASS, human review pending) | KANG_025, out/dwarika_v11_parallax_premiere.zip -> E:\kang\packages\dwarika_v11 |
| Premiere 24.6.1 import / playback of PX_*.mp4 clips | NOT_TESTED | user PC |
| Render speed on user PC (i5, 8 GB) | NOT_TESTED | sandbox 2 vCPU: 1.79 s render per 1 s video at 1920x1080 |
- Artefacts seen (agent eye check, 1:1 crops): soft smear on near crowd at the bottom-right frame edge (S01_b03
  dolly); slight bending of straight carved lines (S07_b02 zoom); slight edge softening where temple spires meet
  sky (S16_b06, S19_b01). No tearing, no black borders, no visible jitter. Parallax is subtle by design.
- Gate fixes during the test: black-edge check false-FAILed a dark night silhouette (S10_b05) -> now compared with
  the same camera without depth; S21_b02 dolly/pan failed stretch -> alternate moves tried, zoom 0.6 PASS.

## Current product state
- Workflow G: narration + captions + scene markers + NEW approved local visuals track (prototype).
  `kang.py visuals-template scenes.json` -> visuals.csv (brief/asset/licence per scene, manual).
  `kang.py visuals media words scenes visuals.csv --assets DIR --preview S01,S02,S03 [--win-root]`
  -> gate visual_selection -> integration preview mp4 + Premiere package (visual track at scene times).
- First integration run KANG_018 (Dwarika S01-S03, 81.4 s): TEST PLACEHOLDER assets only (not real
  visuals), auto(--yes) approval = NOT human; transcript = draft v4 (KANG_016, not accepted).
  Sandbox QA PASS (xml structure, preview duration, glyphs/shaping, caption-vs-words sync).
- Real visuals for Dwarika: NOT_STARTED (needs user's own images/clips + licence).
- Premiere 24.6.1 actual import (with visual track): NOT_TESTED. Windows package check 2026-10-31 (Antigravity, file-level, no GUI): unzip to E:\kang\packages\dwarika_visuals_v1 PASS; XML 25 fps/17309 frames, A1 dwarika.mp3, V1 9 clipitems 0-81.40 s, 22 markers, all 4 media paths exist on disk PASS; SRT UTF-8 PASS. GUI import 2026-10-31 by user: **FAIL** — Premiere 24 'File Import Failure ... sequence.prproj: The project could not be loaded, it may be damaged or contain outdated elements.' Diagnosis kit out/kang_xml_diag.zip (T1 audio only, T2 +markers, T3 +stills, T4 +mp4 loop, T5 full with valid GUID uuid; suspect: non-GUID <uuid>). Result: T1–T5 all FAIL; T0 empty sequence (no media, valid GUID) also FAIL → cause is not our XML content; Premiere-side XML importer suspected. Test B (Premiere's own FCP XML export re-import) also fails once the source sequence is deleted → Premiere FCP XML importer broken on user's install (environment). CAVEAT 10:27: user's Project panel was collapsed (list area hidden; Sequence 03 existed but was invisible) → T1–T5/T0/Test B 'fail' verdicts may be invisible successes; only the first sequence.xml import had a real error popup. Re-verify with maximized panel. 10:38: T0 XML opened via File > Open Project = PASS (project T0_empty_sequence, sequence 'T0 empty', 25 fps) → XML path works on this install through Open Project; Import-into-project route unreliable. 10:39: real sequence.xml via Open Project = FAIL (same 'project could not be loaded'). T0 PASS vs package FAIL → our XML content is the cause. Hardened bisection kit out/kang_xml_diag3.zip (H1 audio, H2 +ascii markers, H3 +hindi markers, H4 +stills, H5 +mp4 loop, H6 full; T0-style track enabled/locked, audio format, file timecode/width/height, masterclipid). Results pending. T6 EDL: importer accepted file (title parsed, PAL/sequence dialogs). Next: T6 EDL import test (out/kang_edl_test.zip); options: official Premiere repair/reinstall, EDL path, or ExtendScript builder.
- Transcript acceptance: false (32 blank + 14 pending listening rows); changed-word timing unverified.
- qa.check_sync compares ASS onsets with words.json, NOT with audio: serialization check, not speech sync.
- Spelling policy: per-video opt-in --spelling-policy; global glossary neutral (frozen).

## Pending acceptance list (does not block visual development)
1. Transcript listening decisions (reviews/dwarika_names_alldiffer.csv).
2. Changed-word timing verification.
3. Human-reference subtitle sync against audio.
4. Actual Premiere import/playback (scene-marker package and visual-track package).

- Latest test run: see build_report.json (build_and_check), 30 Oct 2026 22:45 IST.

## Reported evidence (not independently reproduced here)
- 29 Oct 2026 Kaggle T4 / kernel v7: full Dwarika run, 831 s processing;
  8 detected gaps, 245 recovered words, 6/6 suspect repairs;
  unfilled 0, 2-3 s review gaps 0; 16 cuts auto-approved, NOT human-approved.
- Current (30 Oct 2026, after readiness patch): see "Latest test run" line below.
  Older 111/126-test and 32/34-file records are historical.
- v7 run evidence and v6-derived package acceptance are different checks.

## Code changes (readiness patch, applied 30 Oct 2026)
- Package generation emits draft_package_ready or
  package_generated_pending_verification (or qa_failed), never final accepted.
- Text acceptance and changed-word timing review are separate metadata fields.
- Unknown full-file audio sync is explicitly NOT_TESTED.
- Text acceptance metadata records whether changed-word timing remains unverified.
- These changes still require repository regression tests and a fresh long-form run.

- Earlier 29 Oct review-5: cut approval re-verified by plan hash + source media sha256; review timing labels.
- Historical: 143 pytest + 21 legacy PASS, 37 files, 30 Oct 2026 15:27 IST. Caption option --english-script asr|latin|devanagari (core/script_style.py, config/english_script.json; captions only, words.json unchanged).

## Next acceptance work
1. Listen to flagged regions, fill keep/fix/delete decisions and apply human review.
2. Re-align or manually verify changed-word timing; do not mark it verified without evidence.
3. Regenerate captions/scenes/package from the corrected revision.
4. Test actual Premiere import, full playback and selected visuals.
5. Complete the 100-word hand-check and separate broader long-form audit.

## Historical notes (preserved verbatim below)
The following text may contain superseded current-status labels; dates and context apply.

---

# Kang AI Creative Automation — Status (Master Roadmap v2.0, 29 Oct 2026; earlier notes said "v4.0")

Last verified: 2026-10-29 IST (111 pytest + 21 legacy, 32 bundle files in sync). `python build_and_check.py` → **PASS** (see build_report.json).

## Quick start (VS Code, local)
```bash
pip install -r requirements.txt          # ffmpeg 6+ with libass/HarfBuzz must be on PATH
python scripts/fetch_fonts.py            # Mukta ExtraBold + Noto Sans Devanagari + Montserrat (OFL)
python build_and_check.py                # Phase 0 gate: must say RESULT: PASS
python kang.py transcribe voice.mp3 --device cpu
python kang.py fix-words runs/<id>/words.json     # config/glossary.json
python kang.py promo voice.mp3 runs/<id>/words.json --start 0 --dur 20
```
Har command ek naya `runs/<date>_KANG_NNN/` folder banata hai: manifest.json (relative paths + SHA-256),
inputs ka hash, ffmpeg.log, qa_report.json. Originals kabhi overwrite nahi hote.

## Feature status
| Phase/Feature | Status | Evidence |
|---|---|---|
| Phase 0 build_and_check | Verified | files → syntax → env → 21 legacy + 111 pytest → bundle → sync |
| Phase 1 transcription | Verified (CPU), script-level only | Darjeeling + Dwarika 60 s, audit 0 issues (overlap/glyph/gap checks, not word accuracy). 100-word hand-check sheet: out/dwarika_v6_handcheck.xlsx, pending |
| API (app.py /upload) | Verified (mock) | now calls pipeline.api_transcribe = same stack as kang.py; tests/test_api_parity.py |
| Glossary fix (proper nouns) | Verified | Dwarika: 6 fixes (द्वारी का → द्वारका, कृष्णे → कृष्ण, पैरे → प्यारे) |
| F01 animated Hindi subtitles | Generation + cue serialization: tested. Hindi rendering: user-reviewed (Dwarika 9:16, 2026-10-28). Audio sync vs human-marked reference (±100 ms, 20 markers): NOT_TESTED | glyph, safe zone, cue-vs-words.json, export checks |
| Phase 2 exit (20 s Hindi promo) | Verified | Darjeeling + Dwarika, 1080×1920, 20.01 s, QA pass |
| F02 presets | Verified | 4 presets, schema-checked |
| F03 silence/filler cut | Verified | Dwarika 60 s → 56.925 s, 6 cuts, 0 truncated words |
| F04 audio cleanup | Metrics PASS; full acceptance WARN until human listen | Dwarika −20.0 → −14.3 LUFS, TP −2.0 dBTP. **Human listen pending** |
| F05 multi-format | Verified (synthetic) | 9:16/16:9/1:1 tests |
| F19-lite palette | Verified | contrast-checked brand_draft.json |
| Phase 3 workflow (`kang.py workflow`, `--full`) | Verified (Kaggle T4 GPU) | Full Dwarika 692 s: 880 s workflow, 0 unfilled gaps, -14.9 LUFS / -2.4 dBTP, 16:9 render PASS |
| Suspect-span + seam repair | Verified | Dwarika: 5/5 spans repaired, 6:06 'शिव के बारह ज्योतिर्लिंग' fixed; swallowed-word guard |
| Spelling voter (default ON) | Verified (Kaggle) | 4 Hindi models (Vaani, collabora medium, IndicWhisper medium/large), ≥2 must agree; 76 changes on Dwarika; batched, 1 model per GPU, ~3.3 min |
| Speech-gap re-transcription | Verified | Dwarika 60–120 s: Whisper skipped 13.1–29.98 s; 34 words recovered |
| Script sanitizer | Verified | Cyrillic/Hebrew hallucinations stripped, repeated-word loops flagged |
| Kaggle bundle + real GPU runs | Verified | Real Kaggle T4 runs: 2026-10-28 (v1, v2), 2026-10-29 (v3 voter, v6 fast final). Voter models prebuilt by kernel kang-voter-models |

## Master Roadmap v2.0 mapping (honesty rule: PASS / FAIL / WARN / NOT_TESTED / NOT_APPLICABLE)
Old "Verified" above = our own script/test evidence. Under v2.0 a feature is only PASS with a natural 10–15 min run + qa/ evidence + human checks, so most rows are still **WARN** or **NOT_TESTED**.

| Milestone | Scope (v2.0) | Kang today | Status |
|---|---|---|---|
| M0 core contracts | IDs, schemas, manifests, logging, recovery | run IDs, manifest + SHA-256, read-only originals, build gate. hash-bound `approvals.json` (approver + plan sha256, --yes recorded as auto). Missing: `schema_version`, `<artifact>.vN.json`, run sub-folders (input/ transcript/ qa/…), cancel/resume tests, `job_queue.json` | WARN (partial) |
| M1 input router | audio / face / no-face / mixed / corrupt | not built (audio-only assumed); no `input_profile.json` | NOT_TESTED |
| M2 transcript intelligence | ASR draft, coverage, targeted retry, correction | raw layer (words_raw.json), coverage gaps ≥2 s detected + retried (2–3 s leftovers = needs_review, ≥3 s blocks), suspect-span repair (gaps ≥0.8 s, stretched words), voter, glossary, diff logs. Missing: 100-word Quick Sample result, ≥500-word long audit, human correction step, `coverage_report.json` name/shape | WARN (hand-check pending) |
| M3 Workflow G | scenes.json, Gate 1, visuals, captions, preview, Premiere package (F12) | captions/cuts/audio/16:9 render done. Missing: scene plan, Gate 1 visuals, package, Premiere import test | NOT_TESTED |
| M4 face video | F04, F06, F01, F05 on face clips | F06 not built | NOT_TESTED |
| M5 motion + design | F16, F20, F19-lite, F13, F15 | brand.json + F19-lite only | NOT_TESTED |
| M6 extensions | F07–F11, F12 AE, F14, F18, F21, F23 | none (must not start before M3 exit, risk R6) | NOT_TESTED |
| M7 batch | F17 queue | none | NOT_TESTED |

Licences: fonts/OFL-{Mukta,Noto,Montserrat}.txt; models + wordlist in config/model_licenses.json (collabora medium is CC-BY-4.0, attribution needed; hi_IN.dic is GPL, downloaded at setup, not shipped). D1 = Premiere Pro 24.6.1 (+ After Effects 24.6.2), user 2026-10-29. D2 = Windows 10 (per user "10th"), Intel i5, 8 GB RAM, GTX 1650 (4 GB VRAM assumed, typical), 562 GB free SSD. Implication: Premiere path = FCP7 XML (xmeml) import, test on 24.6.1; local GPU = turbo only (--no-vote, ENGINE_COMPUTE_TYPE=int8_float16 if OOM), 4-model voter stays on Kaggle T4. D3–D7 still open (recommended defaults in roadmap notes).

## External review fixes (2026-10-29)
API cut default OFF (narration preserved); approvals.json bound to plan hash; setup_kaggle pip runs without shell (the `pydantic>=2.5` redirect bug) + `KANG_INPUT_AUDIO` explicit input; coverage threshold 2 s; overlap guard no longer pushes ends past the next start (no word dropped). The 2 s threshold is NOT yet re-run on full Dwarika (Kaggle) — status WARN until then.

## Third review fixes (2026-10-29 20:00)
transcript.srt/json now built from the FINAL words (raw ASR layer kept in raw/); API/status report processing_complete, review_required, accepted=False, warnings separately; approval hash covers preview/ASS/words content + render settings and is re-verified before the final burn; a human "no" = rejected, default-deny = pending, auto(--yes) = human_approved False; setup same-file copy guard; CLI exit 0 done / 1 failed / 2 waiting at a gate.

## Full Dwarika re-run on new code (Kaggle T4, kernel v7, 2026-10-29 20:22 IST)
build_and_check PASS on Kaggle (111 pytest + 21 legacy). workflow --full --yes: 831 s, pass. Coverage at 2.0 s: 8 gaps found, 245 words added, 6/6 suspect spans repaired, unfilled 0, needs_review(2-3 s) 0. Audit 3 review flags (non-blocking), 172 glossary fixes. Cut 16 (6.3 s) auto-approved via --yes = NOT human-approved. Loudness -14.9 LUFS, TP -2.4 dBTP. Report: out/kaggle_gpu_full_v7/. Human listening + sync still NOT_TESTED.

## M3 Workflow G prototype (2026-10-29 21:15 IST)
`kang.py package <media> <words.json> [--scenes edited.json] [--cuts approved cuts.json] [--fps 25] [--win-root E:\...]`:
words -> scenes.json (~30 s scenes at sentence/pause breaks, tiles the timeline, every word owned once) -> Gate 1 `scene_plan` (hash of scenes.json + words.json + keep/fps) -> premiere_package/ (sequence.xml FCP7 xmeml on ORIGINAL media, scene markers, captions.srt, scenes.json, words.json, media/, README_IMPORT.txt, package_manifest.json sha256). Cuts only from a run whose cut_list gate is approved; default = narration whole.
Status: XML structure/frame QA PASS (10 tests, Dwarika v6 words: 23 scenes, 17309 frames @25 fps). Gate 1 for that test was auto(--yes) = not human. **Premiere 24.6.1 import: NOT_TESTED** (user's PC). Visuals per scene: NOT_TESTED (placeholders only).

## Known limits
- Subtitle font is Mukta ExtraBold (Hindi + English in one face). Noto Sans Devanagari has no Latin letters, so Hinglish words failed QA.
- large-v3 vs turbo compared (A/B 2026-10-28): turbo + seed + spelling voter chosen; large-v3 3.3x slower, worse timing.
- Subtitle sync check compares rendered cues to words.json; it cannot judge whether ASR timing matches the voice. Watch the preview.
- Promo background is a plain brand colour; B-roll/motion graphics are Phase 3+ (unblocked: subtitle preview signed off 2026-10-28).
- ASR still mishears names; extend config/glossary.json per client/topic.

## 2026-10-29 22:25 — review-4 (external review of Workflow G)
- Transcript acceptance loop: `kang.py review` (review.csv + clips, changes no words) → user fills action/correct_text → `kang.py apply-review` (new words.json; transcript gate; transcript_acceptance.json bound to words sha256). Package reads acceptance: currently **transcript_accepted = False**.
- Dwarika v6 review sheet: 54 spans (39 P1 amounts/names incl. 4 reviewer phrases, 4 P2 fragments/low-conf, 11 P3 repeats). Human listen: NOT_TESTED.
- Scene planner: no split before continuation words (से/की/का...) or after dangling (जो/के...), bare pause needs ≥1.0 s, fallback prefers sentence end near target. Dwarika: 22 scenes. Still needs human scene review.
- README: "Target" + "Actual import verification: pending"; states video track empty, captions separate SRT. Manifest has status block.
- v7 run PASS ≠ v6-based package acceptance (separate checks). Premiere import: NOT_TESTED. Visuals: NOT_STARTED.
- 126 pytest + 21 legacy PASS; build_and_check PASS (34 files).

## 2026-10-29 23:10 — review-5
- apply_review timing: same word count keeps ASR timing; different count = interpolated, `timing_method=interpolated_after_review`, `timing_status=unverified`, listed in `timing_unverified`; no fake probability; `text_status=human_reviewed`.
- premiere_package cuts: plan hash of current cuts.json must equal approved hash AND source media sha256 must match the cut run's input; `cuts_human_approved` reported separately.
- Scenes: break before narrator opener "दोस्तो/दोस्तों", never before a clause predicate (… | X है). Dwarika 22 scenes; still NOT human-reviewed.
- 131 pytest + 21 legacy PASS; build PASS. Packages: dwarika_v6c (E:\kang\packages\dwarika_v6c), review pack run KANG_004.

## 2026-10-31 11:25 Premiere XML fix
- H1-H6 (out/kang_xml_diag3.zip) via Open Project: ALL PASS on user's Premiere 24.6.1 (audio, ascii markers, Hindi markers, stills, mp4 loop, full). Old KANG_018 sequence.xml: FAIL again (same error).
- Root cause = old xmeml layout (exact single element not isolated; fix applied as whole H-layout). core/premiere.py now: GUID uuid (uuid5), media before timecode/markers, track enabled/locked, audio format, file timecode + width/height, masterclipid, alphatype. check_xmeml enforces it. tests/test_premiere_layout.py (6). 194 pytest, bundle 44 files, build_and_check PASS.
- New package: runs/2026-10-31_KANG_001 -> out/dwarika_visuals_v2_package.zip (E:\kang\packages\dwarika_visuals_v2). README says Open Project. Premiere GUI verify: NOT_TESTED (user).
- 12:50 v2 sequence.xml via Open Project: PARSE PASS (no load error); Link Media dialog showed 4 files missing at E:\kang\packages\dwarika_visuals_v2 -> folder name/extract path mismatch likely. Timeline content NOT_TESTED until relink.
- 12:53 v2 after relink: Premiere timeline PASS (sequence 'KANG 2026-10-31_KANG_001 visuals', V1 stills+loop playing at 01:02:08, A1 audio, 22 markers, duration 00:11:32:09). Media path mismatch was extract-folder naming; future zips should contain a top-level folder named as win-root. captions.srt import in Premiere: NOT_TESTED.
- 13:35 user listened 00:13 (N002): extra 'का' after द्वारिका -> N002 = द्वारिका, human_reviewed. Asked user to confirm N001/N005/N006/N010/N029/N007/N018 same pattern. SRT sync issue: SRT times correct (0.91s first cue); user to place SRT at 00:00:00:00.
- 14:07 captions.srt import at 0:00 = PASS (cue 34 'तो द्वारिका यात्रा की' 00:00:37:09 matches SRT). Premiere package incl. captions now PASS (placeholder visuals, draft transcript).
- 14:15 user's remaining issue = Locate/Link Media. Added FIX_PATHS.bat + fix_paths.ps1 (rewrites sequence.xml pathurls to the folder it sits in; PASS/WARN for missing files) to both package writers; zips now have a top-level folder. Run KANG_002 -> out/dwarika_visuals_v2_1.zip. Python simulation of the ps1 logic PASS (Downloads path with space); real PowerShell run on Windows NOT_TESTED. 195 pytest, build_and_check PASS.
- 15:17 FIX_PATHS.bat on Windows: PASS (user). Extract-anywhere -> bat -> Ctrl+O works without Link Media.
- 15:25 User approved removing extra का (N001/N005/N006/N007/N010/N018/N029). CSV: N002 decided_by=listened; 7 rows editorial-policy (user-confirmed pattern, per-row listening not stated), content_review cleared. apply-review on KANG_012 -> KANG_004 (2265 words, 0 'द्वारिका का', 0 द्वारका); scenes re-planned, 22 scenes identical times. Visuals package KANG_005 -> out/dwarika_visuals_v3.zip + out/captions_v3.srt. Merged-word timing NOT_TESTED. Remaining review: 30 blank rows, 8 pending.
- 15:55 Real assets S01–S03 (Wikimedia Commons, CC BY-SA 4.0, assets/dwarika_real + CREDITS.txt/json). KANG_006 (words KANG_004) preview + package -> out/dwarika_visuals_v4_preview_S01_S03.mp4, out/dwarika_visuals_v4.zip. Preview frames full 16:9, no empty area. Premiere check pending user. Framing list: notes/framing_checks.md. Transcript pending review kept separate (not a blocker).
- 17:55 v5_full: KANG_007, 54 shots S01–S22 (reviews/dwarika_visuals_full.csv, multi-shot shot_start), preview 692.36 s 1920x1080 25fps + audio, 0 black frames, 0 silences >3 s, XML 54 visual clipitems + 22 markers check PASS, all 54 mid-frames inspected (qa/shot_midframes.jpg). out/dwarika_visuals_v5_full.zip + _preview.mp4. Premiere import of v5 pending user.
- 20:25 v5_1 (KANG_008): manifest fixes from user review — CREDITS.txt/json packaged + hashed (65 files), stats.source_has_video/visual_track added (legacy 'video' kept = source media), visuals.json assets_dir relative. Visuals/XML identical to v5_full except uuid. Approval flags + premiere_import stay false/NOT_TESTED until user evidence. Listening spans: reviews/dwarika_listen_spans_2026-10-31.md. test_visuals 21.
- 21:30 Asset Brain Phase 1: core/asset_index.py, kang.py ingest/asset-search, assets/dwarika_real/index.json (54; 48 BY-SA/3 BY/2 PD/1 CC0), out/dwarika_assets_contact_sheet.jpg, tests/test_asset_index.py (4). Full pytest 204 PASS. docs/KANG_Extended_Roadmap_v5.2.{md,pdf}. NEXT Phase 2 kang.py match → broll_suggestions.json.
- 21:45 Asset Brain Phase 2 (rule-based): core/broll_match.py, config/asset_aliases.json, kang.py match / match-approve, tests/test_broll_match.py (4). Fixed asset_index tokenizer (underscores, danda, s13 ids). 208 pytest PASS. out/dwarika_broll_suggestions_phase2.zip: hit@3 15/22 (optimistic, file names are mine). Semantic: NOT_STARTED.
- 21:58 Phase 2 v2: match-check (qa) + approve-broll (A/B/C prompt or --choices → approved_broll.json + visuals.csv) + review_sheet; fallback fill (S22). Structure PASS 22/22, 66/66, 0 dup. Content review PENDING. 210 pytest. out/dwarika_broll_suggestions_phase2_v2.zip
- 22:05 Phase 2 v3: entity minor-mention rule + scene profiles (config/scene_profiles.json); S03 fixed, S22 outro. hit@3 19/22 (tuned on this video, optimistic). 211 pytest (209 full run + 2 broll tests fixed & rerun). out/dwarika_broll_suggestions_phase2_v3.zip
- 2026-11-01 00:33 Hinglish layer v1 IMPLEMENTED (WARN draft): kang.py hinglish (Yapper romanizer + config/hinglish_names.json, same timings). out/dwarika_hinglish_v1.zip delivered. 164 review words, 79 Apex diff hints. 220 pytest PASS, build PASS. Pending: user Dwarka/Dwarika choice, listening, Yapper data licence.
- 2026-11-01 14:56 Hinglish Review Assistant v0 IMPLEMENTED: hinglish-layer / review-hinglish / apply-hinglish-review. Run 2026-11-01_KANG_001 (45 blocks + clips + html), out/dwarika_hinglish_review_v0.zip delivered. 227 pytest PASS, build PASS. Awaiting user review CSV. Reels Caption Styles NOT_STARTED.

## 2026-11-02 07:30 IST fetch v2 (Dwarika)
- fetch-plan: multi-word place kept whole + max 2 scene tags; fetch skips 3D/stereo/anaglyph titles. 
- Query CSV reviews/dwarika_fetch_queries_v2.csv (place "Dwarka Gujarat", 2 per scene) → assets/dwarika_fetch_v2: 29 stills, all CC BY-SA, ingested; 1 download error; no result S11,S15,S16,S21,S22.
- My eye check (agent, not user): ~25/29 relevant, all Gujarat Dwarka; weak: S19 egret + district map, S08 lotus, S01_2 estuary egret. v1 errors (Delhi hotels, salt, 3D) gone. Next: match + approve-broll.

## 2026-11-02 12:45 IST fetch-pool v3 (Dwarika)
- New `kang.py fetch-pool SCENES --pool 'deepcat:"Dwarka";deepcat:"Bet_Dwarka"' --out DIR [--per-scene 2 --min-score 1 --dry-run --pool-cache]`: pulls the Commons category pool once (pool.json), ranks it per scene with named phrases (hinglish_names) and alias tags, spelling-normalised (Dwaraka/Dwarika→Dwarka), then downloads through the same licence/3D/size filters and writes pool_ranking.csv (top 5 per scene).
- Dwarika: pool 839 files, 782 with a free licence. 40 stills (34 CC BY-SA, 5 CC BY, 1 PD), 0 download errors, ingested to assets/dwarika_fetch_v3. Only S21 and S22 have no pick; both are talk scenes and fall back to profile.
- My eye check (agent, not user): ~33/40 relevant. Weak: S09 auto → temple; S11 Siddheshwar → Nageshwar Shiva; S18 Shivrajpur → Bet Dwarka sea; S03_1 sunset lamp.
- Tests: 244 passed, 1 skipped. build_and_check PASS. Next step: match + approve-broll.
- 13:05 match on fetch v3: out/dwarika_v3_broll.{json,csv} + sheet out/dwarika_v3_broll_sheet.jpg. Ingest now normalises Commons spellings (dwaraka/dwarakadhish/gomati/nageshvara) and records fetched_for_scene; match gives ×1.5 to the asset fetched for that scene. 22/22 scenes have 3 options (16 high, 5 profile, 1 low = S09). 244 tests passed. Waiting for the user's A/B/C choices, then approve-broll --choices.
- 13:15 v7 package: visuals from reviews/dwarika_visuals_v7.csv (42 unique shots, each scene uses its own fetch-pool stills; S21/S22 one generic each; picked by me under user delegation 13:01, no repeats). Run KANG_001 (Hindi captions, caption QA PASS) → package-captions → KANG_002 with accepted Hinglish captions → out/dwarika_v7_premiere.zip (E:\kang\packages\dwarika_v7). Premiere import NOT_TESTED.
- Fix: fetch now asks for the 1280 px standard thumbnail when Commons returns an unscaled original. Original-file downloads were the cause of the 429s. 245 tests.
- 14:10 v8 (after user's v7 review): v7 had narration mismatches (S04,S05,S09,S10,S11,S18 + my own find S14 Gopi Talav, S20, S03/S08 swap). New stills: Dwarka station, Okha train, rickshaws (Vadodara, representative), Bhadkeshwar x2, Shivrajpur x2 → assets/dwarika_fix_v8; combined assets/dwarika_v8. reviews/dwarika_visuals_v8.csv: 46 unique shots, notes match:exact 29 / representative 15 / partial 4 (metadata + my eye; not human-reviewed). Commons "Gopi Talav" = Surat lake → rejected. Run KANG_003 (visuals + preview S04–S18) → KANG_004 (Hinglish captions) → out/dwarika_v8_premiere.zip + out/dwarika_v8_preview_S04_S18.mp4 + out/dwarika_v8_visual_sheet.jpg. Code: visuals --selected-by (README/manifest), last shot clamped to sequence frame end, README separates Hindi transcript / Hinglish text / timing / visual review; package-captions adds caption status lines. 245 pytest. Premiere import NOT_TESTED; human visual review PENDING.
- 16:10 v9 (user review of v8): cuts on narration transitions (word times): S09 card at 228.10 (scooty/prices), S10 Bhadkeshwar at 260.67, S11 lighthouse 304.43 / sunset beach 313.19, S14 Bet Dwarka 424.85, S17 bridge 519.33. Text cards (own, Mukta OFL) for Swaminarayan, Siddheshwar, Gopi Talav, transport prices; S17 under-construction bridge labelled "Archival" on screen (derived CC BY-SA, noted). reviews/dwarika_visuals_v9.csv 49 shots: exact 29 / representative 15 / text_card 4 / archival 1. README documents 692.376 source vs 692.36 frame end. Runs KANG_005 (preview S09–S17) → KANG_006 → out/dwarika_v9_premiere.zip. My frame check at all 6 cuts PASS. 245 pytest. Import NOT_TESTED; human visual review PENDING.
- 18:10 user reviewed v9 docs: fixes present; no v10 now. Cuts ~200 ms lead before word onset (by design; do not call "exact"). Next: user playback of KANG_006 (03:35-05:34, 06:45-07:22, 08:31-08:49 + full pass, card/Hinglish-caption overlap), then record visual rough-cut approval on this run.
- 22:07 user: "playback me thik chal raha hai" → KANG_006 manifest approvals.visual_rough_cut = approved (user verbal). Premiere import still NOT_TESTED unless user confirms playback was in Premiere.
- 2026-11-03 15:11 NEXT proposed: beat layer (3-6 s beats + markers). Awaiting user yes + crop-reuse decision.

## 2026-11-03 16:15 IST beat layer v10 (Dwarika)
- New: `kang.py beats / beats-assign / beats-package / beats-preview / beats-grid` (core/beats.py, core/beats_package.py, config/beat_rules.json; Ken Burns Basic Motion in core/premiere.py, check_xmeml checks keyframes). Rules from louisedesadeleer/b-roll-finder (MIT), our own code.
- Runs: beats KANG_001 (lead, 164) / KANG_002 (lag, 166); final assign KANG_014 (lead) / KANG_013 (lag) [KANG_003-012 = superseded curation passes]; previews KANG_018 (lead) / KANG_017 (lag); package KANG_019 (lead) -> out/dwarika_v10_beats_premiere.zip (E:\kang\packages\dwarika_v10). Grid out/dwarika_v10_beats_grid.jpg.
- Package (lead): 164 beat markers + 22 scene markers, 117 still shots (avg 5.92 s, median 4.32, max 27.2 S21) vs v9 49 shots ~14 s; 117 unique stills (49 v9 + 68 new Commons pool, assets/dwarika_beats_pool_v10), 0 repeats; beats: continued_with_motion 34, card_hold 13; labels per shot exact 43 / representative 69 / text_card 4 / archival 1. New stills: agent eye check (58 rejected in beat_rules eye_rejects), NOT human-reviewed.
- Anchor: lead (-0.2 s) chosen after frame check: Hinglish cues show the place name at/before onset; lag keeps the old shot (often a card naming another place) 0.25 s under it.
- 253 pytest passed, 1 skipped (tests/test_beats.py 8). Premiere import, motion scale/centre in Premiere, cut timing: NOT_TESTED. visuals_human_approved false.

## 2026-11-04 07:37 IST user decisions
- Crop/zoom reuse of the same photo: ALLOWED (different framing, e.g. full temple then spire). Label reuse as `crop_reuse` in plan.
- Combined review + Premiere test only AFTER all features are ready. No per-feature reviews.
- No publishing for now; rights clearance deferred (not a blocker for building).
- Second (non-Dwarika) video test only after all features are finished.
- Previous day: v11 (KANG_025) parallax, v12 (KANG_034) free sources, v13 plan KANG_038-040 (cards+maps; package NOT built yet). See notes/history.md.

## 2026-11-04 v13b fix run (cards + maps) — run 2026-11-04_KANG_001
- `kang.py motion-fix 2026-11-03_KANG_038 --force M0_S03_overview [--run ...]` (core/motion_assign.fix_build_cmd): re-plans all cards/maps, re-renders only changed clips; other beats keep KANG_038 clips. Output runs/2026-11-04_KANG_001/visuals_beats_v13b.csv + card_values.csv (new column lead_s; FAIL if > 0.25 s).
- Re-rendered 14: C01 C03 C05 C07 C08 C11 C12 C15 C16 C17 M0 M1 M2 M4. Kept from KANG_038: C02 C04 C06 C09 C10 C13 C14 M3 M5.
- Lead rule (no value/label > 0.25 s before its spoken word): PASS, 133 PASS / 2 WARN / 0 FAIL. Each value of a line now appears at its own word (−0.2 s). M1 extended over S04_b04 and M4 over S14_b07 (both were representative) so "135 km" / "Sudarshan Setu" appear 0.2 s before the word. C12 evening times (5–8 PM) are spoken after the card ends and S15_b07 is exact → WARN, not shown. C10 title uses spoken_id 916 ('Siddhnath', ASR variant).
- Map safe zone: PASS (graphics fade over 770–800 px, pixel check that nothing differs from the plain map below y=800; FAIL otherwise). Labels: 5 % margin + above the fade band, region labels avoid place labels: PASS. Coast NE→OSM feather (40 px cross-fade): PASS by agent eye, faint ghost coast visible at full res where the two coasts differ.
- Not changed: map credit line stays at y=14 (outside 5 % margin; not a label). M3/M5 not re-rendered (no change except a tiny drift-timing difference).
- Tests: tests/test_map_route.py (14) new; test_motion_cards 15, test_beats 8, test_windows_compat 4: all pass. config/data_licenses.json added. Grid out/dwarika_v13b_fix_grid.jpg. Not human-reviewed; package not built.

## 2026-11-04 08:20 IST v13 Premiere package — run 2026-11-04_KANG_002
- `beats-package` = KANG_034 inputs (dwarika.mp3, words/scenes KANG_004, beats_lead KANG_001, Hinglish accepted SRT) with CSV runs/2026-11-04_KANG_001/visuals_beats_v13b.csv; extras captions_hindi.srt, hinglish_acceptance.json, parallax_report.csv (from KANG_034 package). → out/dwarika_v13_motion_premiere.zip (252,989,734 B, sha256 a1a9e221b206…, top folder dwarika_v13, win-root E:\kang\packages\dwarika_v13).
- 129 shots (avg 5.37 / median 4.56 / max 19.44 s = CARD_C11 Gopi Talav over S14_b01–b04), 186 markers (164 beat + 22 scene), 23 motion clips (17 cards + 6 maps, own work), 16 parallax, 13 stock video, 77 Ken Burns stills. Labels per shot: exact 47, representative 58, text_card 17, map 6, archival 1.
- Code: core/beats_package.py now adds config/data_licenses.json (Natural Earth, OSM ODbL + credit line + elements, Wikidata items) to CREDITS.json (kind=data_source) and CREDITS.txt (DATA lines) when MAP_ clips are on the timeline; recorded as run input DATA_LICENSES.
- Checks PASS: check_xmeml, beats contiguous, beat markers, motion on every still, stock/parallax clips cover beats, credits cover every asset; zip: one top folder, 130 pathurls all present, 130 unique file/clipitem ids, package_manifest hashes match. Tests: beats 8, parallax 11, map_route 14, motion_cards 15, premiere_layout 7, package_captions 2, package_readiness_patch 6, windows_compat 4 — all pass.
- Premiere import NOT_TESTED (per user: combined review + Premiere test after all features). Not human-reviewed.

## 2026-11-04 v14 crop reuse — runs 2026-11-04_KANG_003 (superseded pass) / KANG_004 (crop pass) / KANG_005 (package)
- User decision 07:37: same photo may come back as a distinctly different crop. New `core/crop_reuse.py`; `kang.py beats-assign --allow-crop-reuse [--hinglish-words]` and `kang.py beats-crop-reuse VISUALS_BEATS --beats B --out CSV --grid JPG` (same pass on an existing CSV, keeps parallax/stock/cards/maps). Config: `config/beat_rules.json` → `crop_reuse` (limits, extra place `dwarkadhish`, `continued_exact_needs_exact`, `rejects`, `eye_accepted`).
- Rules: crop area ≤ 50 % of the first framing (16:9 cover view), IoU ≤ 0.3 with every earlier framing, ≥ 4 beats from every appearance and after the first one, ≤ 2 reuses per photo, ≥ 1280 px wide; region by spectral-residual saliency + Canny edges; sky/flat/blurry refused; crops touching a face refused (OpenCV YuNet, tools/models, MIT; OpenCV 5 has no Haar CascadeClassifier). Depth cache not used. Each crop = new file `CR_<beat>_<photo>.jpg` (run/crop_reuse + CREDITS.json: modified = crop); CSV columns reuse / reuse_of / crop_box; label = photo's own label.
- Only continued_with_motion beats + representative beats whose narration (Hinglish words) names a place with an exact photo: 11 candidates (6 continued + 5 representative; the "11 continued" figure was v12, v13b had 6). Used 4: S07_b04 (Dwarkadhish entrance crop of S01_2, exact), S08_b08 (Gomati ghat crop of B10_S06_015, exact), S15_b08 (Bet Dwarka exhibit niche of S15_1, exact), S22_b04 (ferry crop of S12_1, representative). Rejected by agent eye 2 (rocks+litter crop for S08_b08; Dwarka promenade replacing an exact Shivrajpur hold, now also a rule). Remaining continued_with_motion 4 (S01_b04, S03_b04, S08_b10, S18_b06).
- Main limit: all stills are 1920 px wide, so a 1280 px crop is ≥ 44 % of a 16:9 framing (IoU ≥ 0.44 when inside it) → only photos taller than 4:3 give a second framing, and only outside the first framing (top/bottom bands). The "spire inside the temple view" crop needs Commons originals ≥ ~2400 px wide (not fetched).
- v14 package KANG_005 → out/dwarika_v14_crop_premiere.zip (253,380,403 B, sha256 4ec3e2d1…, top folder dwarika_v14, win-root E:\kang\packages\dwarika_v14), same extras as v13. 131 shots (avg 5.29 / median 4.52 / max 19.44 s CARD_C11), labels exact 50 / representative 57 / text_card 17 / map 6 / archival 1. Checks PASS (xmeml, beats, markers, motion on every still, stock/parallax cover, crop_reuse_files_ok, credits; zip: 1 top folder, 132 pathurls present, unique ids, manifest hashes). Grid out/dwarika_v14_crop_grid.jpg.
- Tests: test_crop_reuse 5 (new), test_beats 8, test_premiere_layout 7, test_windows_compat 4, test_parallax 11, test_motion_cards 15, test_map_route 14 — pass. Not human-reviewed; Premiere import NOT_TESTED.

## 2026-11-04 v15 YouTube CC BY clips — runs 2026-11-04_KANG_006 (fetch, blocked) / KANG_007 (search-only after place-check fix)
- Approach picked: yt-dlp (Unlicense, pip, Windows OK, no key): CC-filtered search URL (sp=EgIwAQ%3D%3D) = pre-filter only; acceptance = per-video metadata `license` == "Creative Commons Attribution license (reuse allowed)" + place check; `--download-sections`, video only ≤1080p, 1 GB cap. Not used: YouTube Data API v3 (videoLicense=creativeCommon needs a key); Commons video (0 Gujarat-Dwarka videos, only Delhi-Dwarka airport clips) / Openverse (no video).
- New: core/youtube_cc.py, config/youtube_cc.json, `kang.py fetch-youtube-cc --out DIR [--search-only]`, `kang.py beats-youtube-cc VISUALS_BEATS --beats B --pool DIR --out CSV` (replaces only representative Pixabay clips + continued_with_motion tails where narration/held photo names the clip's place; continued of an exact hold needs an exact clip; never exact/card/map/archival; no repeats). Shot split = ffmpeg scene filter; shot checks: min 2.5 s, jitter (phase correlation), static edge overlay (text/logo/watermark), YuNet face close-up; eye_rejects / eye_exact in config. Credit "Title — Channel (YouTube), CC BY 3.0"; run README notes YouTube ToS download = grey area, recorded not cleared.
- BLOCKED: sandbox IP gets HTTP 429 (watch page) + 403 (player API) on every video; tried 2 ways (web client + node JS runtime; tv_simply/android_vr/mweb clients) → stopped. Search endpoint works: 8 queries × 20 = 126 unique (KANG_007: 23 rejected by title place check, 103 not probed); licence field read for 0 → 0 accepted, 0 downloaded, 0 clips used. No v15 package/grid built.
- Tests: tests/test_youtube_cc.py 11 (mocked runner + synthetic ffmpeg media, no network) pass; download → shot split → contact sheet path is unit-tested only, never run on a real YouTube file; api_parity/windows_compat/pixabay/openverse 26, beats/crop_reuse 13 pass.
- To unblock (user choice): run `python kang.py fetch-youtube-cc --out assets\dwarika_youtube_cc_v1` on the user's Windows PC (home IP), then agent eye check on the contact sheet + `beats-youtube-cc` + `beats-package --win-root E:\kang\packages\dwarika_v15`.

## 2026-11-04 v15 YouTube CC BY via Kaggle — runs 2026-11-04_KANG_008 (fetch on Kaggle) / KANG_009 (assign) / KANG_010 (package)
- Sandbox IP blocked (KANG_006/007) → ran the same `core.youtube_cc.fetch_cmd` on Kaggle: tools/kaggle_youtube_cc (kernel ironindiarat/kang-youtube-cc, private, CPU, internet ON; dataset ironindiarat/kang-youtube-cc-input = core/ config/ tools/models/ Mukta font). Only kernel differences: download timeout 1200 s, `max_probe` 200. Kaggle IP 35.204.107.38: NOT blocked, 1 kernel run, 59 min. yt-dlp 2026.10.26 + node 22.
- KANG_008: 125 unique search hits; 102 probed, all 102 licence field = "Creative Commons Attribution license (reuse allowed)"; 84 accepted (licence + place), 41 rejected (23 title place check, 18 place/wrong-place on metadata). 1 GB cap reached after 46 videos (998,982,813 B; Dwarkadhish/Gomti/Bet Dwarka/Setu/Nageshwar query order) → Shivrajpur, Rukmini, lighthouse videos never downloaded. 213 shots → 47 passed auto checks (113 shaky, 23 text/logo, 20 face, 10 <720p). Pool: assets/dwarika_youtube_cc_v1 (copy of Kaggle pool/, unchanged).
- Agent eye check (contact sheet, not human): 33 more rejected (burned-in text/lyrics, channel/news logos, PM/VIP event footage, presenter talking head, cartoon/drawing/diorama, letterboxed Nageshwar aerial, dashcam) → config/youtube_cc.json eye_rejects; 11 exact (9 Sudarshan Setu drone/aerial: Narendra Modi channel; 2 Dwarkadhish spire: Narendra Modi, Mahendra art) → eye_exact; 3 representative (LuckyHere temple gate, Narendra Modi temple courtyard, Travels Positive Nageshwar sanctum live-cam). New core.youtube_cc.apply_eye applies these at beats-youtube-cc time (Kaggle CREDITS.json left as fetched).
- KANG_009 beats-youtube-cc on runs/2026-11-04_KANG_004/visuals_beats_v14.csv: only 1 replacement: S01_b04 (continued hold of exact S01_2 still) → YTC_S01_b04_YT_FyHJoEe9F-k_02 (exact Dwarkadhish, Mahendra art). 13 Pixabay representative units name no place in narration → kept; 3 continued tails kept (S03_b04 gomti, S18_b06 shivrajpur: no pool clip; S08_b10). Sudarshan Setu clips unused: the only Setu-narration beats are a map (S14_b07) and the archival bridge still (S17_b03), both protected. Dwarkadhish-narration representative stills (S07_b05, S15_b03, S16_b02) are not replaceable units under the current rule.
- v15 package KANG_010 → out/dwarika_v15_youtube_premiere.zip (255,887,040 B, sha256 8e11c318…, top folder dwarika_v15, win-root E:\kang\packages\dwarika_v15), extras as v14. 132 shots (avg 5.25 / median 4.44 / max 19.44), labels exact 51 / representative 57 / text_card 17 / map 6 / archival 1 (v14: 50/57). Checks PASS (xmeml, beats contiguous, no repeats, markers 186, motion on every still, stock/parallax cover, pixabay_representative_only, crop_reuse_files_ok, credits cover every asset; zip: 1 top folder, 133 pathurls present, 133 unique file/clipitem ids, 147 manifest hashes match). Grid out/dwarika_v15_youtube_grid.jpg (before/after S01_b04 + 13 unused eye-passed clips).
- Tests: test_youtube_cc 12 (+1 apply_eye), test_beats 8, test_premiere_layout 7 pass. Not human-reviewed; Premiere import NOT_TESTED; YouTube ToS download = grey area, recorded not cleared.

## 2026-11-04 v16 YouTube CC fetch 2 + rule A/C — runs 2026-11-04_KANG_011 (Kaggle fetch) / KANG_012 (superseded) / KANG_013 (assign) / KANG_014 (package)
- Agent decisions under the user's delegation (2026-11-04): **A** an EXACT YouTube CC clip may replace (1) the S17 archival under-construction Sudarshan Setu hold when narration is about the Setu and (2) REPRESENTATIVE stills/stock whose own narration names the clip's place; maps/cards/exact shots stay protected, no repeats, replaced archival still dropped (only the protected map beats S14_b06/b07 also talk about the bridge). **B** second Kaggle fetch only for Shivrajpur / Rukmini / lighthouse (+ Gomti if cap left), cap 600 MB, same licence + place + auto checks. **C** remove the Pixabay "subscribe/like button" clip STK_S22_b06 → real Dwarka shot. Config: `config/youtube_cc.json` → `v16_rules` (archival_replace_places, named_representative, force, prefer, offsets) used by `kang.py beats-youtube-cc ... --v16-rules`; without the flag v15 behaviour is unchanged.
- Code: core/youtube_cc.py `_units`/`plan_youtube(vrules)` (archival / named_representative / forced units; eye `prefer`; clips already on the timeline count as used), `skip_video_ids` in fetch, trim `offsets`, fetch place label prefers the query place (v1 labelled a Shivrajpur video "dwarkadhish" alphabetically). tools/kaggle_youtube_cc_v2/ (kernel script, v1 left as is); scripts/changes_grid.py (before/after grid).
- B (KANG_011): kernel version 2 = BLOCKED (bot check on Kaggle IP 34.75.229.80, 0 probed); one identical retry = kernel version 3 on IP 35.195.0.115: done, 29 min. 69 unique hits, 16 skipped (already downloaded in v1), 33 probed, 26 accepted (licence exact + place), 27 rejected; 26 videos downloaded, 581,358,630 B (under 600 MB cap; Gomti: no new candidate passed). 110 shots → 15 passed auto checks (80 shaky, 7 text/logo, 4 face, 4 <720p). Agent eye check: **all 15 rejected** (burned-in Gujarati captions, letterbox/vehicle window, train/station, sky, and 6 shots of a Rukmini temple in Amravati, Maharashtra). Pool assets/dwarika_youtube_cc_v2 (as fetched). → S18_b06, S03_b04 and the Rukmini/lighthouse beats unchanged.
- KANG_013 on runs/2026-11-04_KANG_009/visuals_beats_v15.csv: S17_b03–b05 archival still → YT_7E1uvEdpz_A@1 (exact Setu aerial, Narendra Modi, start 2.5 s to avoid a dissolve); S22_b06 Pixabay subscribe animation → YT_3YVQe5MYyhE@9 (exact sunset Setu aerial, start 0.0). Rule A (2) found 6 named-representative units (S07_b05, S15_b03, S16_b02 Dwarkadhish; S17_b01, S20_b01, S20_b02 other temples) but no unused exact clip of their place is long enough (0mHRDNcnInQ@5 = 2.97 s; FyHJoEe9F-k@2 already on S01_b04) → kept. Note: S15_b03/S16_b02 are in the Bet Dwarka section, so a Jagat Mandir clip would show the wrong temple anyway.
- v16 package KANG_014 → out/dwarika_v16_youtube2_premiere.zip (266,500,166 B, sha256 e96b9868…, top folder dwarika_v16, win-root E:\kang\packages\dwarika_v16), extras as v15. 132 shots (avg 5.25 / median 4.44 / max 19.44 s CARD_C11), labels exact 53 / representative 56 / text_card 17 / map 6 / archival 0 (v15: 51/57/17/6/1). Checks PASS (xmeml, beats contiguous, no repeats, 186 markers, motion on every still, stock/parallax cover, pixabay_representative_only, crop_reuse_files_ok, credits; zip: 1 top folder, 133 pathurls present, 133 unique file/clipitem ids, 147 manifest hashes match). Grid out/dwarika_v16_changes_grid.jpg.
- Tests: test_youtube_cc 15 (+3: rule A archival/named representative, forced outro + prefer + no reuse of on-timeline clips, skip_video_ids), test_beats 8, test_premiere_layout 7, api_parity + windows_compat 7 pass. Not human-reviewed; Premiere import NOT_TESTED; YouTube ToS download = grey area, recorded not cleared.

## 2026-11-04 v17 AI motion (image-to-video on real photos) — runs 2026-11-04_KANG_015 (plan, 3-still test) / KANG_016 (Kaggle kernel, BLOCKED)
- Model research (licence from HF model card / LICENSE files, recorded in config/model_licenses.json → ai_motion_i2v): **pick Wan2.2-TI2V-5B** (hf:Wan-AI/Wan2.2-TI2V-5B-Diffusers @ b8fff73, Apache-2.0, 5B, 1280x704 24 fps I2V in diffusers). OK but not used: Wan2.1-Fun-1.3B-InP (Apache-2.0, 480P, needs VideoX-Fun code), Wan2.1-I2V-14B-480P (Apache-2.0, too big for T4). Rejected (custom licence → idea only): LTX-Video (RAIL-M / LTXV Open Weights License, $10M revenue clause), CogVideoX-5B-I2V (CogVideoX License, registration + 1M visits cap), Stable Video Diffusion (Stability AI Community License, $1M cap).
- New: core/ai_motion.py, config/ai_motion.json, tools/kaggle_ai_motion/ (kernel ironindiarat/kang-ai-motion, worker, dataset ironindiarat/kang-ai-motion-input), `kang.py ai-motion-plan` / `ai-motion-apply`, scripts/zip_checks.py; hooks in core/beats.py (AI_MOTION_COLUMNS, motion=ai_animated) and core/beats_package.py (AI_*.mp4 on V1, check ai_motion_clips_cover_their_beats_1080p_no_audio_label_kept, CREDITS model entry + "modified (AI motion)", README "AI animated" note).
- Design: masked composite — AI pixels only where the AI clip moves AND the photo is sky / flat / water-coloured (or a small flag blob near the top); every other pixel = original 1920x1080 photo framing, so buildings/people cannot be re-drawn. Gate: first-frame SSIM, global + cell flicker, rigid-cell edge stability (Canny F-score), camera drift (phase correlation), motion present, mask area, composite first-frame SSIM; FAIL → shot keeps parallax / Ken Burns; only gate PASS/WARN + config eye_pass clips are applied. Label kept (exact/representative) + motion ai_animated + on-screen "AI animated" (top right).
- Plan (agent eye check of 34 keyword candidates, eye_rejects_plan in config): 14 candidates (sea/boat/water/flag), test set S11_b06 (Dwarka beach waves, exact), S16_b06 (Dwarkadhish spire flag, representative), S12_b01 (boat near Bet Dwarka, representative).
- **BLOCKED (KANG_016)**: Kaggle T4 x2, kernel versions 1 and 2 both CUDA OOM on all 3 jobs (v1 weights + VAE resident 12.85 GB; v2 model CPU offload, 14.2 GiB allocated) at diffusers transformer_wan.py:472 — TI2V-5B's per-token fp32 timestep modulation (~1.33 GiB at 85 frames 1280x704 = 19.4k tokens). Stopped after 2 identical failures (task rule). 0 clips rendered → no v17 package, no grid. Next fix options: generate at 960x544 (-42 % tokens) and upscale only the masked pixels, or diffusers group offload at 1280x704.
- Tests: tests/test_ai_motion.py 11 (mocked I2V frames, no GPU) + test_beats 8, test_premiere_layout 7, crop_reuse 5, youtube_cc 15, windows_compat 4, parallax 11 pass. Real-model gate thresholds, Premiere import of AI clips: NOT_TESTED.

## 2026-11-04 v17 AI motion attempt 2 — runs 2026-11-04_KANG_021 (plan, 9 jobs) / KANG_022–025 (superseded S16 re-composite iterations) / KANG_026 (gate + eye) — **AI motion WARN / blocked, v16 stays current**
- S16_b06 re-composite (no kernel, attempt-1 raw): new flag-colour core in core/ai_motion.py (`flag_hue`, `flag_colour_core`: union of saffron/red pixels over the photo + every AI frame, seeded by the photo's own flag components, moving only, dilated; inside it the composite is 100 % AI). Flag shots now take AI pixels only in LARGE flat sky components + the core (KANG_023 heat map showed blue-grey stone carving shimmering through the old flat|fluid mask; KANG_024 warm stone specks entered an unseeded core). New `ghost_frac` (photo flag pixels still showing through) → FAIL > 0.0002. Final (KANG_026): gate PASS, ghost 0.0, mask 0.026, composite first-frame SSIM 0.9992, agent eye **PASS** (no ghost, stone untouched outside the finial the photo flag hung over).
- Gate: `new_blobs` = bright / compact dark blobs APPEARING in the water/sky mask vs frame 0 (local-contrast, >= 2 px high, thin ripple lines ignored) in >= 2 sampled frames → FAIL (attempt-1 S12_b01 seagull → FAIL). Beach/sea shots: eye-set `mask_keep` row limits in config (open water + sky only, shoreline / breakers / wet sand = photo); a sea / sea_flag clip without one FAILs. Plan: `negative_extra` ("birds, people, boats moving, new objects, text, camera motion") appended to every job's negative prompt (user asked for S12_b01 + S11_b06; applied to all), `seed_overrides` 20261104 for S12_b01 + S11_b06. Kernel v4 = LPT GPU split.
- Kernel ironindiarat/kang-ai-motion version 4 (T4 x2, 1024x576, group offload): COMPLETE, 9/9 rendered, 5331 s (88.9 min; split 248/293 frames; 763–1335 s per clip, peak VRAM ≤ 6.2 GB). Raw in work/kaggle_ai_motion_out_v4 (report copy runs/2026-11-04_KANG_026/kernel_v4).
- KANG_026 (10 clips = 9 new + S16_b06): gate PASS 2 (S16_b06, S20_b01) / FAIL 8 — S12_b01 new blobs (+ eye: skyline towers wobble), S11_b06 new blob (breaker in the thin open-water band), S18_b05 no motion + slow 2.42, S11_b04 composite SSIM 0.948, S11_b05 blob at lighthouse railing, S11_b08 no motion, S06_b04 composite SSIM 0.931 (whole frame shimmers), S16_b05 fluid flicker 18.5 + a new flag entering from the top. Agent eye (runs/2026-11-04_KANG_026/ai_motion_eye_sheet.jpg, first/mid/last + motion heat; ai_motion_eye.csv): S16_b06 PASS, S20_b01 REJECT (people on the platform move/morph). **1 < 2 passed → no v17 package, no grid (task rule)**; config eye_pass = [S16_b06] kept for a later batch.
- Tests: test_ai_motion 18 (+7: blob FAIL / ripple ignore, flag core + no ghost vs attempt-1 mask, stone specks not in core, sea needs shoreline limit, negative/seed), test_beats 8, test_premiere_layout 7 pass. Packaging with an AI clip dry-run (S16_b06 only, scratch runs dir, not kept): all package checks PASS incl. ai_motion_clips_cover_their_beats. NOT_TESTED: Premiere import of AI clips, blob gate on clips other than these 13 raws.

## 2026-11-05 v17 package + combined review — runs 2026-11-04_KANG_027 (AI apply) / KANG_028 (package) / KANG_029 (review) — version 0.7.0
- Package: out/dwarika_v17_premiere.zip (265,663,223 B, sha256 00e0c076eb4a…, top folder dwarika_v17, win-root E:\kang\packages\dwarika_v17) from runs/2026-11-04_KANG_027/visuals_beats_v17.csv (= v16 + AI_S16_b06). 132 visual clipitems, 186 markers, 15 parallax, 38 stock/YouTube video clips, 4 crop reuses, 1 AI motion clip; labels as v16. All package + zip checks PASS (incl. ai_motion_clips_cover_their_beats_1080p_no_audio_label_kept).
- **AI motion = WARN**: only 1 clip passed gate + agent eye (S16_b06 Dwarkadhish flag, representative, on-screen "AI animated"); 8 FAIL + S20_b01 eye REJECT kept their parallax / Ken Burns.
- Combined review: out/dwarika_v17_combined_review.mp4 (238.2 s, 14 segments with slates, tagged shots, A/B lead-lag cut at M2), sheet out/dwarika_v17_review_sheet.jpg (132 shots), review list out/dwarika_v17_review_v2.csv (39 rows; v2 fixes the 2 A/B rows that read feature "BEAT CUT A/B", label "MAP" → MAP / map; every row checked against visuals_beats_v17.csv, no other mismatch; original v1 kept). scripts/combined_review.py fixed for the same label bug + ffmpeg/ffprobe text I/O now encoding="utf-8".
- Tests (full suite, per file from tests/): **349 passed, 1 skipped, 1 failed** of 351. Skip: test_captions_adapter (karaoke_subs not installed). Fail: test_hinglish::test_repo_table_loads uses the cwd-relative path config/hinglish_names.json, so it fails only when run from tests/ (pre-v13 test, table itself loads fine). Not human-reviewed; Premiere import NOT_TESTED.

## 2026-11-05 v17b fix: no in-between numbers + M4/M2 labels — runs 2026-11-05_KANG_001 (motion-fix) / KANG_002 (package) / KANG_003 (review)
- Bug (user frame check of the v17 review, C17 ~200–216 s): count-up showed "2 people • 0 days" and "₹9,990–5,056". Fix (core/motion_cards.py, core/map_route.py): **no count-up anywhere** — values appear already final; a value line fades/slides in in 0.3 s (VALUE_ENTER_S), a later value of the same line pops in whole at its word (v13b lead rule kept: e.g. "₹500" then "₹500–600"); map km badge final from its first frame (0.3 s fade). Count-up only if a spec value opts in with `"count_up": true` AND it is the line's only value, a number ≥ 100, each in-between frame a rounded step ≤ final (count_up_step) — config/motion_cards.json opts in nothing.
- M4: "Good highway" chip (`near_route: [0, 0, 0.5]`) now sits beside the Gopi Talav → Sudarshan Setu leg (side/fraction chosen at the phase-end camera: 5 % margin, above y=770, clear of labels/dots/km badge; dropped if no spot); top-left chips restack without a gap. Place labels (all maps, incl. M2 "Bet Dwarka"): 0.15 s fade ending by the spoken word (was 0.4 s → 0.875 opacity at the word); a label whose word is at the clip start pops in at full opacity.
- New QA (FAIL, in `motion-fix`/plan QA: motion_plan_qa.json value_display_fail): every frame of every card (render plan, same `_line_text` the renderer draws) — each shown number must equal the number at the same position of the final text; km badges final whenever visible; each spoken place label at alpha 1 at its word. Result: **0 problems on all 23 clips**. Lead rule 133 PASS / 2 WARN (unchanged).
- KANG_001: `kang.py motion-fix 2026-11-04_KANG_001 --base-csv runs/2026-11-04_KANG_027/visuals_beats_v17.csv --base-values runs/2026-11-04_KANG_001/card_values.csv --out visuals_beats_v17b.csv --force <23 ids>` (new flags --base-csv/--base-values; fix run now writes motion_clips/CREDITS.json). Re-rendered all 17 cards + 6 maps (every card has a value line → enter speed changed; every map has place labels → fade changed); frames/1080p/no audio PASS. visuals_beats_v17b.csv = v17 with only the 50 card/map rows' source_dir/notes changed (AI S16_b06 etc. untouched).
- Package KANG_002: out/dwarika_v17b_premiere.zip (265,084,019 B, sha256 422e9e571ad6…, top folder dwarika_v17b, win-root E:\kang\packages\dwarika_v17b; extras captions_hindi.srt, hinglish_acceptance.json, parallax_report.csv from KANG_028). 132 clipitems, 186 markers, all package checks PASS; scripts/zip_checks.py PASS (133 pathurls, 0 missing, ids unique, 147 manifest hashes OK).
- Review KANG_003: scripts/combined_review.py gained `init --profile v17b` + `reuse` (copies segments whose shots are identical to KANG_029). Re-rendered 6 segments (S09_card, M2_map, AB_lead_lag, S14_gopi_talav_card, M4_map, S21_card), reused 8 → out/dwarika_v17b_combined_review.mp4 (238.2 s), out/dwarika_v17b_review_sheet.jpg (132 shots), out/dwarika_v17b_review_v3.csv (39 rows). Agent eye: 217 frames (every 0.5 s of those 6 segments, work/v17b_frames/grid_*.jpg) — no in-between number; C17 shows "2 people" → "· 3 days" → "/ 2 nights", "₹10,000" → "₹10,000–12,000"; "22 km" final; "Good highway" beside the route; "Bet Dwarka" full at its word.
- Tests: test_motion_cards 20 (+5), test_map_route 19 (+5), test_beats 8, test_premiere_layout 7, test_windows_compat 4 — pass. Not human-reviewed; Premiere import NOT_TESTED.

## 2026-11-06 07:40 — Creative layer adopted (critic side)
- Vendor package v2 kept unmodified in creative/vendor/creative_layer_v2 (PROVENANCE.md). Adapter core/creative.py; CLI `kang.py creative-check VISUALS_CSV LAYER [--profile travel_vlog_hi] [--captions SRT] [--with-audio]`.
- KANG overlay config/creative_rulebook_kang.json from Hark research (notes/creative_research/): 24 evidence re-tags (8 of 10 🟢 dropped to 🟡), 9 rules removed (superseded/profile-off), 63 new rules (G-001..033 gap, S-001..022 science, Q-001..008 Qwen Apache). Audio rules off: config/creative_audio_deferred.json (58). Idea-only sources kept as own-words rules (user 2026-11-06); never copy their text/code.
- First v17b report: runs/2026-11-06_KANG_001 (engine 14 evaluated, 4 PASS; KANG checks: G-004 FAIL 12 stills <3 s, G-008 FAIL 3 back-to-back parallax, G-013 FAIL 16 captions >22 cps, S-004 FAIL 95 captions <0.83 s, no hook beat, first card at 57.5 s). Critic only; planner/hands NOT_STARTED.
- Tests: tests/test_creative.py 6 PASS; full tests/ 293 passed, 5 failed (ModuleNotFound in crop_reuse/youtube_cc = sandbox missing deps), 5 skipped. Vendor 36/36.

- 07:56 notes/creative_research/editor_tool_repos.{md,json}; T-001..033 merged into creative_rulebook_kang.json (96 new rules total).

## Editor-app options (user 2026-11-06 10:19: keep all as options; no editing app besides Premiere/AE now)
- Techniques from AE/Premiere/Resolve/CapCut repos: ACTIVE as rules (T-001..033 etc.).
- Code paths parked as NOT_STARTED options: CapCut draft export (renezander030/capcut-cli MIT; pyJianYingDraft Apache China edition), Premiere CEP MCP (hetpatel-11 MIT), AE nexrender (MIT), Resolve (free has no external scripting). Revisit only if user installs the app.

- BUG (10:23): core/creative.py graphic text repeats revealed items (S03_b05 counted 14 words, real ~9) -> dedupe before word count; R-236 is Shorts-only, misapplied to long-form. Fix before v18.

## 2026-11-07 v18 picture desk + cold open — runs 2026-11-07_KANG_007 (desk) / 008 (cold open) / 009 (package) / 010 (review) / 011 (critic v18) / 012 (critic v17b re-check) / 013 (contact sheet); KANG_001–006 = superseded first pass (status superseded, kept)
- Critic fixes tested: tests/test_creative.py +3 (card items deduped per (clip, shown_text) → S03_b05 10 tokens / 9 words, was 14; R-236 removed for travel_vlog_hi, kept for vendor `shorts`). Critic now: KANG checks G-004/G-006/G-008/Q-001/Q-002 per SHOT (same-asset beats merged like B.merge_clips), new Q-006 accent check, teaser rows → one hook beat (kind hook, tease, overlay; exempt from still rules), card_values.csv found via the card clips' source_dir, still move read from `desk_motion`.
- **Picture desk** IMPLEMENTED: core/picture_desk.py + `kang.py plan-pictures VISUALS --out PREFIX [--words]` (rule-based, deterministic; every decision = rule id + reason in *_plan.json/.csv and desk_rule/desk_note CSV columns). On v17b (KANG_007): 15 decisions — G-008 ×3 (S03_b04, S08_b10, S18_b06 holds = one shot, parallax clip 11.44/10.44/17.88 s covers it), G-004 ×11 (all 11 short stills fixed by moving one cut to another word onset − 0.2 s; 0 merges, 0 unresolved; S16_b07 takes 0.32 s from the AI clip), Q-006 ×1 (S03_b06 parallax → Ken Burns; accents 16 → 15), G-006 0 changes needed. Q-002-aware: 4 cuts skip the smallest shift because it would make 3 equal shots. Package honours `desk_motion` (core/beats_package._clips).
- **Cold open** IMPLEMENTED: core/cold_open.py + config/cold_open.json + `kang.py cold-open`. Visual-only teaser 0–6.32 s (ends 0.2 s before 'bhagwan' 6.51 s; narration/captions/audio unchanged, no inserted time): TSR_01 Setu drone day (mt_xdx4S_Ok@1), TSR_02 Setu night lasers (mt_xdx4S_Ok@4), TSR_03 Dwarkadhish spire (0mHRDNcnInQ@5) — 3 eye_exact YouTube CC clips not used elsewhere — and TSR_04 S16_b06 AI flag (representative, 'AI animated' label baked in). Title overlay "DWARKA · GUJARAT / Shri Krishna ki nagri" in card style from 0.3 s. CREDITS.json in runs/2026-11-07_KANG_008/teaser_clips (source records copied + modified + teaser:true; AI one carries model + licence). S01_b01 (exact S01_1 still) and S01_b02 (representative photo) leave the timeline; S01_b03 (S01_2 temple parallax, 8.2 s clip) starts at 6.32 s.
- **v18 package** (KANG_009): out/dwarika_v18_premiere.zip 258,685,654 B, sha256 0aaf2944b7432539a47165ce52e2dcd578645bf835d0b6b39557aa71547ba17e, top folder dwarika_v18, win-root E:\kang\packages\dwarika_v18, same inputs/extras as v17b. 134 clipitems (4 teaser), 186 markers, 14 parallax, 1 AI, labels exact 55 / representative 56 / text_card 17 / map 6. All package checks PASS; scripts/zip_checks.py PASS (135 pathurls, 0 missing, ids unique, 149 manifest hashes OK). Eased xfade: NOT done (needs xmeml transitions; not trivial).
- Review (KANG_010): out/dwarika_v18_combined_review.mp4 (238.2 s, 34.2 MB; 4 segments re-rendered — opening, crop_reuse_1, S10, S16 — 10 reused from v17b review; reuse signature now includes the still move), out/dwarika_v18_review_sheet.jpg (134 shots), out/dwarika_v18_review.csv (41 rows). Contact sheet (KANG_013): out/dwarika_v18_contact_sheet.jpg (167 beat rows, time / beat / treatment / desk rule), agent eye-checked.
- Critic v17b re-check → v18: engine 4/13 → 13/17 passed (score 30.8 → 76.5 %); KANG checks 4/9 → 6/9. Fixed: R-001, R-005, R-028, R-031, R-112, R-400, G-004, Q-006; new PASS R-064/R-158/R-221. Still FAIL: R-180 (hook 7 words vs 9–24), R-091 (S08_b04 card), R-160 (S17 Setu clip 10 s), R-338, G-013/S-004 (captions, unchanged by rule); Q-001 WARN ×2. Table: notes/creative_research/v17b_vs_v18.md.
- Tests: test_creative 9, test_picture_desk 13 (new), full tests/ per file 382 passed, 1 skipped (test_captions_adapter: karaoke_subs not installed), 0 failed. The earlier ModuleNotFound failures (crop_reuse/youtube_cc) are gone after `pip install opencv-python-headless` (already in requirements.txt). Manifests now also carry `rel_path` (project-relative) next to the absolute `path`.
- NOT_TESTED: Premiere import of v18; teaser/desk not human-reviewed.
