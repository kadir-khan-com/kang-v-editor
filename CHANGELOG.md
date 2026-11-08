# KANG changelog

## v0.7.0 — 2026-11-05 (tested on Dwarika only; not human-reviewed, Premiere import NOT_TESTED)
- Beat layer: one visual per narration beat (lead cut -0.2 s), beat + scene markers; `beats-assign`, `beats-package`.
- 2.5D parallax on held stills (gate-passed clips baked in as video).
- Free sources: Openverse images (CC BY / BY-SA / CC0 / PDM) and Pixabay videos (Pixabay Content License, representative only); one asset index over all pools.
- Motion cards (17) + route maps (6; Natural Earth + OSM ODbL credits in CREDITS); no value/label shown > 0.25 s before its spoken word.
- Crop reuse: same photo back as a distinctly different crop (≤ 50 % area, IoU ≤ 0.3, ≥ 4 beats apart, no faces); `--allow-crop-reuse`, `beats-crop-reuse`.
- YouTube CC BY clips via Kaggle (sandbox IP blocked): `fetch-youtube-cc`, `beats-youtube-cc [--v16-rules]`; licence field + place check + auto/eye checks; ToS download grey area recorded, not cleared.
- AI motion (Wan2.2-TI2V-5B, Apache-2.0) as masked composite on real photos with a gate + eye check: **WARN** — 1 clip used (S16_b06 flag), labelled "AI animated".
- Combined review: scripts/combined_review.py → one tagged review video + contact sheet + review CSV (v2 fixes A/B MAP rows).
- Package v17: out/dwarika_v17_premiere.zip. Full suite 349 passed, 1 skipped, 1 failed (cwd-relative path in test_hinglish when run from tests/).

## v0.7.0-dev — 2026-11-03 external free sources: Openverse + Pixabay (tested on Dwarika only)
- `fetch-openverse` (core/openverse_fetch.py): api.openverse.org/v1/images, anonymous (page_size <= 20), licence
  filter by,by-sa,cc0,pdm (no NC/ND), min width 1600 (`--min-width`), creator/source/licence_url recorded, place check
  (config/stock_sources.json `wrong_places` + Dwarka-area cue required), dedupe vs the existing pool by sha256, dHash
  (perceptual, 64 bit, distance <= 8) and known Commons title; Wikimedia originals via the 1920 px thumbnail; 24 h
  response cache; `_seed/` fallback only when the live call fails (run records http [code, 'seed_webfetch']).
- `fetch-pixabay` (core/pixabay_fetch.py): videos (images coded, endpoint not authorised); key placeholder
  `key=__SAVED_KEY__` (connect_service 'pixabay' injects the key; key never stored), <= 95 requests / 60 s, 24 h
  cache, `--verify-auth` (one request, HTTP status), `--thumbs-only` (candidates + thumbnails for the eye check),
  downloads only `eye_ok` items; AI-generated / low-quality / wrong-place / landmark / person-cue rejects; prefer
  1920 wide, 4-15 s; CDN files fetched directly (no key). Licence 'Pixabay Content License' (PIXABAY_CL, not CC).
- `asset-index-all`: one index over all asset folders (source, licence family, label, dHash) -> assets/asset_index.json.
- `beats-stock` (core/stock_assign.py): priority exact > parallax same place > map/card > representative stock >
  continued_with_motion; stock only on continued beats after a hold cap (exact 7 s, other 4.5 s); exact same-place
  Openverse photo may replace any continued beat of an exact shot; Pixabay always representative; videos trimmed to
  the beat (frame-exact, 1920x1080, 25 fps, no audio) into the run with CREDITS (modification recorded); resumable.
- `beats-package`: video stock clips as video clipitems; checks stock_clips_cover_their_beats_no_audio,
  pixabay_representative_only. `stock-grid`: grid of every newly used asset.
- Tests: tests/test_openverse_fetch.py (9), tests/test_pixabay_fetch.py (10). Full suite 283 passed, 1 skipped
  (5 chunks). tests/test_windows_compat caught 2 text-I/O lines without encoding (fixed).
- Runs: KANG_026/027 (Openverse), 028 (Pixabay auth), 029-031 (Pixabay candidates), 032 (downloads), 033 (beats-stock),
  034 (package out/dwarika_v12_sources_premiere.zip), 035 (grid), 036 (index, superseded), 037 (index).

## v0.7.0-dev — 2026-11-03 2.5D parallax layer (tested on Dwarika only)
- `core/parallax.py`, `core/parallax_package.py`; commands `parallax IMG --out MP4 --dur S [--move dolly|pan|zoom]
  [--strength]`, `parallax-batch VISUALS_BEATS [--run --beats --min-hold 6 --budget]` (resumable),
  `parallax-apply VISUALS_BEATS REPORT --out`, `beats-assign ... --parallax REPORT`; `beats-package` places
  gate-passed clips as video clipitems (no Premiere motion keyframes, motion baked in).
- Depth: Depth Anything V2 Small (hf:depth-anything/Depth-Anything-V2-Small-hf, Apache-2.0, 24.8M, CPU),
  revision 5426e4f0f36572d16453bbda7a8389317b1bef99 (config/model_licenses.json `depth_parallax`). Base/Large
  (CC-BY-NC) refused in code. Depth maps cached in assets/depth_cache/<image sha256>_<rev8>.npz (768 px long side).
- Renderer: own numpy/OpenCV backward remap + FFmpeg pipe. Approach (depth-influence remap, gradient-weighted depth
  feather, fold rule / relaxation) studied from longweekendlabs/parallax-studio (MIT) @
  32e4cb451abf117a148594269219691f7144ce88 (app/core/animator.py, app/core/depth.py, app/core/depth_model.py);
  no file copied. DepthFlow (AGPL) not used. Mirror pad for samples outside the photo (counted by the gate).
- Gate per clip: fold (Jacobian <= 0.05), stretch (share of pixels with local scale off > 25 %; WARN > 0.1 %,
  FAIL > 1.2 %), outside-photo share, black frame edge (vs the same camera without depth), camera-path smoothness,
  luma frame-diff spikes (floor 1.0 level: OpenCV remap quantises to 1/32 px). Relaxation order: feather 6 -> 14 -> 28,
  strength 0.6, then the other two moves; still FAIL -> Ken Burns stays. Cards/archival never get parallax.
- Labels unchanged: parallax clip = same photo, same match label, `motion: parallax_2_5d`; CREDITS note the
  modification (depth-based camera move). No-repeat check counts the photo, not the clip.
- Tests: tests/test_parallax.py (11, synthetic image + mock depth). Full suite 264 passed, 1 skipped (run in two halves).
- Runs: KANG_020 (3-still test, first gate), KANG_021/022 (A/B + grid), KANG_023 (19 clips), KANG_024 (apply),
  KANG_025 (package out/dwarika_v11_parallax_premiere.zip).

## v0.7.0-dev — 2026-11-03 beat layer (tested on Dwarika only)
- `beats WORDS SCENES --out PREFIX [--min 2.5 --target 4.5 --max 7] [--anchor lead|lag] [--visuals CSV]`: beats that
  never cross a scene, split by DP on word onsets (pause, punctuation, Hindi clause words; penalty before
  postpositions/verb tails), cut = onset -0.2 s (lead) or +0.25 s (lag), frame-aligned, contiguous, last beat ends on
  the sequence frame end; current shot starts (v9) become forced cuts so text cards keep their beats.
- `beats-assign BEATS VISUALS_CSV --pool DIR... --assets DIR --scenes --download-to DIR [--top-n 40 --no-new-downloads]`:
  every v9 asset stays on its own shot's beats; other beats get UNUSED Commons pool stills (deep re-rank of pool.json,
  then a same-place global fallback). No asset twice; place guard (a pick may only show places the shot shows); new
  picks 'representative' unless their title names the same real place as an exact shot (areas like Bet Dwarka never
  exact); wrong-place / off-topic rejects in config/beat_rules.json; dry pool -> `continued_with_motion`.
- Motion: FCP7 Basic Motion scale keyframes (cover-fit x 1.00<->1.08 alternating, cards 1.03, archival 1.02) + small
  centre drift, per-asset focus for off-centre subjects; check_xmeml validates keyframes. Preview renderer: PIL affine
  (float, bilinear) frames piped to FFmpeg = sub-pixel Ken Burns, no integer zoompan.
- `beats-package` (beat + scene markers, CREDITS for exactly the used stills, README statuses, FIX_PATHS, zip with
  top-level folder), `beats-preview` (resumable chunks, burned SRT captions), `beats-grid` (beat-midpoint frame grid,
  near-black + jitter check).
- Design rules (not code) adopted from louisedesadeleer/b-roll-finder (MIT): one visual per beat, drop rather than
  show a wrong visual, cut relative to word onset, sub-pixel Ken Burns, frame-grid self-check, manifest of picks.
- Tests: tests/test_beats.py (8). Full suite 253 passed, 1 skipped.

## v0.6.0 — 2026-11-01 (tag; tested on Dwarika only)
Status words follow STATUS.md rules. Evidence = mine (sandbox/Kaggle tests) unless marked user-reported.

- Hinglish layer: `hinglish-layer`, `review-hinglish`, `apply-hinglish-review [--out] [--bulk-ok-by-user]`
  -> words_hinglish_v1_accepted.json + captions SRT + hinglish_acceptance.json. Dwarika accepted by user bulk
  approval (not per block); timing_verified false (2232 verified_pending, 33 unverified).
- Reels captions: `reels --style karaoke_yellow|bold_pop|clean_travel` (karaoke-subs, MIT, ASS + FFmpeg) and
  `--style pop_safe` (optional pycaps engine, MIT, per-word pop, safe zone, max 2 lines; burned MP4 only).
  pycaps render runs on Kaggle CPU (tools/kaggle_reels) or a PC with pycaps installed. Human playback QA: user liked.
- `package-captions`: swap captions in a Premiere package into a new run. Dwarika v6 (KANG_006):
  Premiere import PASS (user-reported).
- `fetch-plan` + `fetch`: Wikimedia Commons stills with licence metadata -> assets + CREDITS (free licences only,
  NC/ND/unknown skipped, rights recorded_not_cleared) -> `ingest`.
- Tests: see build_report.json.
- Dwarika fetch test (2026-11-01 21:41, sandbox): 29 stills from 22 scene queries (28 CC BY-SA, 1 CC BY), 16 skipped
  (licence/size), 6 scenes no result, 2 downloads hit Wikimedia 429 (shared sandbox IP). My eye check of the
  contact sheet: ~21/29 relevant; wrong: S02 = Dwarka **Delhi** hotels, S21 = salt farming; S13 = 3D stereo pairs.
  Next fix: place "Dwarka Gujarat" in fetch-plan, skip stereo/3D, user edits queries before fetch.

## 2026-11-06 — creative-check (critic) + KANG rulebook overlay
- New core/creative.py, config/creative_profiles.json (travel_vlog_hi), creative_audio_deferred.json, creative_rulebook_kang.json; vendor creative_layer_v2 (user-supplied, unmodified).

## 2026-11-07 — v18: picture desk + cold open (critic-driven)
- New `kang.py plan-pictures` (core/picture_desk.py): deterministic shot planner on a visuals_beats CSV — G-004 (stills 3–10 s: move a cut to another word onset − 0.2 s, else merge, else WARN), G-008 (same-photo holds = one shot; no different parallax back to back), Q-006 (accents ≥ 3 shots apart), G-006 (no 3 identical moves), PD-PXLEN, Q-002-aware cut choice; plan JSON/CSV + desk_motion/desk_rule/desk_note columns.
- New `kang.py cold-open` (core/cold_open.py, config/cold_open.json): visual-only teaser over the unchanged opening narration + card-style Hinglish title overlay; derived TSR_*.mp4 clips with CREDITS.json; teaser rows role/reuse 'teaser'.
- core/beats_package.py: still move from `desk_motion`; README cold-open note. core/beats.py assign_qa: 'teaser' reuse = file-name uniqueness only. core/runs.py: manifest entries gain project-relative `rel_path`.
- core/creative.py: card-item dedupe (tests), shot-level KANG checks, Q-006 check, teaser → hook beat, card_values lookup via source_dir. scripts/combined_review.py: v18 profile, TEASER tag, move-aware reuse. New scripts/contact_sheet.py.
- Tests: tests/test_creative.py +3, tests/test_picture_desk.py 13. v18 package out/dwarika_v18_premiere.zip (sha256 0aaf2944…). Premiere import NOT_TESTED.
