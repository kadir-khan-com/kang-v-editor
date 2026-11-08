# Kang project history (moved out of the project skill on 2026-10-29)

## Windows PC runs (2026-10-28)
- Windows bugs fixed: cp1252 encoding (all text I/O and subprocess calls use utf-8) and FFmpeg 9 dropping -filter_complex_script (runs.filter_script_args). tests/test_windows_compat.py covers both; to simulate, run pytest with `-X warn_default_encoding -W error::EncodingWarning`.
- The kit's EXCLUDE has runs/ and *_report.json. Steps 1–6 passed on Windows (Step 6: Dwarika 60–90 s 9:16 CPU, 722 s).
- The user's PC has 1 CUDA device. A local GPU test (--device cuda) is still pending.

## Kaggle GPU runs
- v1, 2026-10-28 18:36: full Dwarika 692 s, 607 s run, PASS. Outputs in out/kaggle_gpu_full/.
- Fixes at 19:30: gapfill suspect spans (>1.2 s words, ≥0.8 s gaps, re-transcribe the window with 3 s then 5 s context), final_audio check (≤-1.5 dBTP), -c:a copy on burn, AAC_SAFE_TP -3.0, audio.ensure_final_true_peak, join_split_tokens, glossary at ~165 fixes. v2 run: out/kaggle_gpu_full_v2/, delivered dwarika_full_16x9_v2_repaired.mp4.
- v3, 2026-10-29 07:57, voter default ON: setup_voters 380 s + workflow 1807 s. PASS: 104 votes, 7 gaps (237 words added), 4/4 spans repaired, 0 unfilled, 153 glossary fixes, -14.9 LUFS / -2.4 dBTP. Delivered out/dwarika_full_16x9_v3_voter.mp4; outputs in out/kaggle_gpu_full_v3/out/.

## Whisper A/B (kernel ironindiarat/kang-whisper-ab)
- R1 (out/whisper_ab/): hotwords and tight VAD were rejected. large-v3 gives the most complete first pass but is 3.3x slower. The Hindi fine-tunes spell better but drop words. turbo nondeterminism was 9.4% WER. The WER reference is turbo-derived, so it is biased.
- R2 (out/whisper_ab_r2/): engine.SEED 1234 cut turbo determinism WER to 2.18 (v3: 3.95). Repair-only hotwords were negligible. Agree voter on v3: 22 changes, nearly all correct.
- R3 (out/whisper_ab_r3/): voter inside the pipeline with 4 models (vaani, collabora medium, IndicWhisper medium, IndicWhisper large-hi-noldcil). turbo_vote 110 votes, v3_vote 87. Alt passes add ~20 min on T4 for an 11.5 min file. WhisperX (kernel kang-wx-align, tools/kaggle_wx): turbo median start diff 0.074 s / p90 0.25 s; v3 0.14 s with 57 words >0.5 s off. Decision: turbo + seed + agree voter. WhisperX is only a QA cross-check.
- WhisperX install on Kaggle: `python -m venv --without-pip` + get-pip.py (ensurepip fails). Pair words by word_segments, not by segment.
- Risky voter changes to listen for: कहा→कहां (29–33 s), द्वारीका→द्वारिकाधीश (454/457 s), दस्व→दसवें (371 s), पावंधा→पावन (490 s), परिस्तित/इस्ती→स्थित.
- 2026-10-29 user review of the v3 video at 6:06: 'टैक्सी के' should be 'जो भगवान शिव के'. Cause: the gap-fill window ended exactly at a first-pass hallucination (के p=0.10). Fix: gapfill seam_low_conf spans (p<0.2 within 1.5 s of a gap-fill word), accepted on confidence. On real audio (CPU turbo) the window came back 'जो भगवान शिव के बारा जोतिर्लिंग'. Only 1 such word in the whole file. 88 pytest PASS.

## 2026-10-29 speed-up (Kaggle v4-v6)
- Voter alt passes: batched (BatchedInferencePipeline, batch 8, ENGINE_VOTE_BATCH; 0 = sequential), one model per GPU via a free-GPU queue (T4x2), sequential fallback if batched gives <30% of base words. Models prebuilt once by kernel ironindiarat/kang-voter-models (tools/kaggle_voters), mounted via kernel_sources.
- v4: 830 s but IndicWhisper medium failed (2 models on GPU 0 -> CUDA invalid argument) and 6:06 repair swallowed 'शिव के बारह' into one 1.2 s p0.57 word.
- Fix: gapfill._swallowed (word >0.9 s and p<0.7 rejects a repair attempt).
- v6 FINAL: workflow 880 s (v3 1807 s + 380 s setup), voter 198 s, 76 votes (all 4 models), 0 unfilled, 5/5 spans, -14.9 LUFS/-2.4 dBTP, 6:06 correct. out/dwarika_full_16x9_v6_final.mp4. 91 pytest.

## 2026-10-29 Kaggle v7 (review-3 code, 2 s coverage)
831 s workflow, pass. gaps 8, +245 words, spans 6/6, unfilled 0, needs_review 0, audit flags 3, glossary 172, cut 16/6.3 s (auto --yes), -14.9 LUFS / -2.4 dBTP.

## 2026-10-30 Nemotron 3.5 ASR 0.6B A/B (Kaggle kernel kang-nemotron-ab v1, T4, fp16, transformers, hi-IN, 29 silence chunks ~25 s)
- Load 33.9 s, ASR 48.0 s for 692 s audio (text only, no word timestamps via this path).
- Disagreement vs our turbo+voter+glossary words: 15.6% (normalized, NOT a WER vs truth; neither side audio-verified).
- Nemotron reads cleaner at our flagged spots: देखने के लिए घंटों, दर्शन करने जरूर, रूम, आप ऑटो (no dup), पांच सौ से छह सौ, मान्यताओं के अनुसार, दो हजार से ढाई हजार (ours 2,500,000), पैंतीस सौ से चार हजार (ours 35,000 से 4,000), सात बजे (ours साथ).
- Nemotron is worse on names: भेड़ द्वारिका/दौरी का (Bet Dwarka), ध्वरिका अधिश, नागेश्वर जो तिरलिंग, सोने की दौर का; spells all numbers as words; English in Devanagari.
- Both models hear "बजर नाम/बजरनाम" at 02:57 → the narrator likely says it that way; वज्रनाभ remains an editorial choice.
- Files: out/nemotron_ab/nemotron_chunks.json, compare_chunks.json. Idea: use Nemotron as a 2nd-opinion hint column in review CSV (not auto-fix).

## 2026-10-30 15:47 second-opinion hints (KANG_007)
core/second_opinion.py + `kang.py second-opinion words.json chunks.json --review-csv csv`: difflib alignment per chunk, adds nemotron_hint / nemotron_agrees / nemotron_diff (content/spelling/spacing/number/script) to review CSV; disagreements.json. Never edits words. Dwarika: 58 rows, 41 disagree (23 number, 13 content); 99 content disagreements outside the CSV → extra_candidates_nemotron.csv. "number" is NOT cosmetic (2,500,000 vs दो हजार से ढाई हजार). 147 pytest, 22 offline, bundle 38 files PASS. Pack out/dwarika_review_nemotron_hints_pack.zip.

## 2026-10-30 16:26 MAI-Transcribe-2 (user ran it in MAI Playground, share 5cba0bf6-bb9b-4335-92fd-89a22d9b49ef)
Qualitative only (share page JS-rendered, text only, no word timestamps). Cleanest of the three: fixes 2000 से 2500, 3500 से 4000, काठियावाड़ क्षेत्र, विश्व प्रसिद्ध मंदिर, वज्रनाम, भड़केश्वर (ours बरकेश्वर wrong). Errors: भेड़/बेड द्वारिका (बेट), शरपदोष, जीवन दिलाओ, पेरिसी यात्रा. English in Latin. Darshan timing 6:30–1, 5–9:30 differs from ours → listen. Paid API $0.10/h (OpenRouter/Azure) gives word timestamps + phraseList. Offered mai_hint column; awaiting user.
- MAI hint columns (mai_hint/agrees/diff) added to KANG_007 CSV: 31/58 differ from ours; 8 rows where Nemotron and MAI agree with each other against ours. Single-chunk alignment (no timestamps) misaligns near '6:30' and R021. Pack out/dwarika_review_hints_pack_v2.zip.

## 2026-10-30 16:50 Nemotron phrase boosting (NeMo-Speech.cpp v0.2.0, GGUF q8)
- Tool: NVIDIA NeMo-Speech.cpp (official C++ runtime). Prebuilt for linux x86_64/aarch64 cpu/cuda and Windows x86_64 cpu/cuda/vulkan. `nemo-speech transcribe a.wav --model m.gguf -l hi-IN -f json --speech-context PHRASE --speech-context-boost N`. JSON gives WORD TIMESTAMPS (fixes the Transformers-path limitation).
- Kernel kang-nemo-boost (tools/kaggle_nemo_boost), T4 cuda build: full Dwarika 30.6 s baseline, ~33 s boosted. Sandbox aarch64 CPU: 60 s audio took 2m36s (too slow here).
- 17 phrases (names/places). Sweep vs baseline: boost 3 = 277 diff spans, hallucinated names everywhere (UNUSABLE). 1.5 = 100 diffs, 1.0 = 63 diffs (द्वारिका→द्वारिकाधीश, श्रीकृष्ण→शिवकृष्ण: bad). 0.5 = 20 diffs, mostly good (द्वारी का→द्वारिका, जो तिरलिंग→ज्योतिर्लिंग, द्वारकादीश→द्वारकाधीश, दौरिका→द्वारिका); regressions: बीच→बीज, अलौकिक→औलौकिक, some commas dropped. 0.25 = 14 diffs, similar, safer.
- Did NOT fix: भेड़ द्वारिका (बेट), भज्रनाम (वज्रनाभ), शर्पद्रोस. Single-word phrase द्वारिकाधीश is a prefix-trap for द्वारिका at boost ≥1 → drop it next time.
- Outputs out/nemo_boost/out/*.json (A_base + 4 boosts), v1_boost3/. Not applied to any transcript.
- v3 (17:17): tuned 19-phrase list (no single द्वारिकाधीश; added बेट द्वारिका, वज्रनाभ ने, सर्पदोष, गोमती नदी, स्वामीनारायण मंदिर). Boost 0.5 = 18 diffs (~12 good, regressions द्वारिका दीश→द्वीष, बीच→बीज, अलौकिक→औलौकिक, commas). 0.75 = 24 diffs, श्रीकृष्ण→शिवकृष्ण, गोपियां मथुरा→गोपी तालाब (bad). Still unfixed: भेड़ द्वारिका, भज्रनाम, शर्पद्रोस → boosting ceiling reached; use glossary/human review. Best setting: boost 0.5. Outputs out/nemo_boost/v3_tuned/.

## 2026-10-30 17:35 3-model consensus (core/consensus.py, `kang.py consensus`)
ours + Nemotron boost0.5 timed (window-aligned at its pauses) + MAI text-only. Dwarika: 2268 words, 79.5% all-agree; rows others_agree 111, all_differ 72, name_hint 2, ours_majority 139; 8 repeat patterns cover 34 rows; 163 listen rows (p1/p2, no pattern). Run KANG_008, pack out/dwarika_consensus_review_pack.zip. config/name_suggestions.json = suggestion-only names. 153 pytest, 40 bundle files. Hints only.
## 2026-10-30 18:31 consensus v2 (user's critique applied)
core/hindi_numbers.py (number words→values), config/script_equivalents.json (Latin↔Devanagari/units), status format_only, kind amount = priority 0, Nemotron aligned by time (align_timed, no spill). Dwarika: agreement 84.9% (not accuracy); 6 amount rows (2:24 दो पर एक/दोपहर एक, 3:43 छे सो/छह सौ, 3:46 पास/पाँच, 5:53 2,500,000 vs 2000–2500, 5:56 35,000 vs 3500, 7:45 साथ/सात); 8 patterns; 128 listen rows. Run KANG_009, out/dwarika_consensus_review_pack_v2.zip. 157 pytest, 42 bundle files.
## 2026-10-30 18:55 consensus v3 (user critique 2)
review_consensus.csv: consensus_hint_PART + consensus_full_span_UNVERIFIED (whole row; digits only if row had digits) + consensus_note (needs_listen / span_mismatch). apply-review rejects a pasted partial hint. Proper names never in bulk patterns (6 patterns left). User's targeted clip extraction supports ₹2000–2500 (5:53) and ₹3500–4000 (5:57) — still not human-certified. Run KANG_010, out/dwarika_consensus_review_pack_v3.zip. 158+ pytest.

## Project-skill log archive (moved here 2026-10-30 20:45 to keep the skill short)
2026-10-29: Claude-review fixes (api parity, licences, MANIFEST), review-2 (approvals.json, gapfill 2 s/3 s gaps), review-3 (final words → transcript, plan_hash, exit codes; Kaggle v7 PASS 831 s), M3 Workflow G prototype (core/scenes.py, core/premiere.py, `kang.py package`), review-4/5 (core/review.py, review/apply-review, timing labels).
2026-10-30: package_readiness patch; user's 58-row review CSV (KANG_003); --english-script asr|latin|devanagari (KANG_005/006); Nemotron 0.6B A/B (15.6% disagreement); second-opinion cmd; MAI text hints (KANG_007); NeMo-Speech.cpp boost 0.5 (31 s on T4, timestamps); paid APIs declined; consensus v1 (KANG_008, 79.5%), v2 (KANG_009, 84.9%, amount p0), v3 (KANG_010 full-span), v3.1 (KANG_011 protected names); draft v1 KANG_012 (6 amount fixes via auto-extraction); names/all_differ review KANG_013 (70 rows); caption spelling policy + draft v2 KANG_014.

## Visuals / Premiere debugging archive (moved from project skill 2026-10-31 21:50)
- KANG_017 scenes.json (22 scenes); KANG_018 placeholder integration S01–S03 (v1). Premiere v1 import FAIL; diag kits kang_xml_diag (T1–T5), diag2 (T0), diag3 (H1–H6). Cause = our old XML layout (non-GUID uuid etc.); collapsed Project panel hid some successes. Use File > Open Project (Ctrl+O, All Files) for XML.
- core/premiere.py rewritten to H layout (GUID uuid5, media→timecode→markers, closed tracks, audio format, file timecode+dims, masterclipid, alphatype); tests/test_premiere_layout.py. v2 (KANG_001) Premiere PASS 12:53; captions.srt PASS at 0:00 (Home + '.' Overwrite) 14:07; FIX_PATHS.bat/fix_paths.ps1 Windows PASS 15:17 (v2_1, KANG_002).
- Transcript 15:25: extra का removed; words KANG_004; package KANG_005 v3. Merged-word timing NOT_TESTED.
- 15:37 user: stop transcript/spelling discussion; real visuals next. v4 (KANG_006) S01–S03 Commons photos APPROVED 17:22. EDL test kit out/kang_edl_test.zip (unused). Template out/dwarika_visuals_template_22_scenes.csv. Framing notes notes/framing_checks.md.
- v5_full (KANG_007) 54 shots full 692.36 s; v5_1 (KANG_008) CREDITS packaged+hashed, visual_track flag, relative assets_dir; user audit PASS 20:25.

## Phase 3 research (2026-10-31 22:45)
- Options to "see" images: CLIP embeddings (rclip MIT, OpenCLIP ViT-B/32, onnxruntime CPU, py>=3.12 for v4) or VLM captions -> tags (moondream / llava via ollama, as in Ambar Premiere plugin). igoforth/broll-search (MIT) = Jina CLIP v2 + Molmo captions.
- jina-clip-v2 = CC BY-NC 4.0 -> reject for monetised use. Multilingual candidates to verify: mSigLIP (Apache-2.0), LAION XLM-R-B/32 (MIT).
- Proposed blind test: rename 54 assets to blind ids, CLIP hit@3 vs 19/22 filename baseline; user marks top-5. Offered to user, awaiting yes.
- 22:50 moondream2 chosen as VLM candidate (Apache-2.0, Ollama Q4 1.7 GB fits GTX1650; English captions -> aliases). LLaVA 7B too tight on 4 GB. No reverse engineering needed. Offered sandbox test on 54 photos, awaiting yes.
- 22:50 User finds 1.7 GB too big. Small alternatives: Florence-2-base (MIT, 0.23B, ~0.5 GB) and SmolVLM-256M (Apache-2.0, <1 GB, ONNX int8). Hybrid plan: place name from Commons title + visual tags from VLM. Offered blind test of both; awaiting yes.

## 2026-10-31 23:40 Hinglish A/B (Kaggle kang-hinglish-ab v1, T4 fp16, Oriserve/Whisper-Hindi2Hinglish-Apex, 29 silence chunks)
- Speed: load 16.9 s, ASR 30.2 s for 692 s audio. Output out/hinglish_ab/out/hinglish_chunks.json (chunk text only, no word timestamps).
- My qualitative read (no WER; no Hinglish reference): numbers clean (do hazaar se dhai hazaar, paintis sau se chaar hazaar, saadhe chhah baje, ek sau paintis km, chaalis rupe); English words natural (hotel, VIP, AC deluxe room, free locker, lighthouse, sunset point, highway, para gliding).
- Problems: name spelling varies (dvaari ka/dvaarika/dvaarka/daurika; dvaarika desh=Dwarkadhish; bed/bhed dvaarika; naageshvar jo triling; bharkeshvar; shideshvar; rukmani). Misheard: sansad(sunset), sharpan dosh(sarp), sharaab diya(shraap), vote(boat), pyaaz(pyaas), paris yaatra(paavan), jivan dilaav(leela), sthaan(snaan), speed board. Roman style is academic (krshn, dvaarika, double vowels) → needs normalization table to YouTube Hinglish (Krishna, Dwarka).
- Verdict: WARN/promising as Hinglish caption source + number hints; needs Roman name table, word timestamps, listening. Not production.

## 2026-11-01 00:30 — Hinglish layer v1 (agent, user delegated "jo theek lage")
- Route: Devanagari master words.json (KANG_004) -> Yapper Transliterator (map 1.17M + Lipi 544k params, CPU, 0.4 s for 2265 words) -> config/hinglish_names.json (phrases/names/word fixes; suspect ASR words flagged, never hidden) -> same word timings -> Hinglish SRT (599 events).
- New: core/hinglish.py, `kang.py hinglish WORDS --out P --yapper-dir D [--review-csv] [--other-asr chunks.json]`, tests/test_hinglish.py (9). Full suite 220 PASS (sandbox, 2026-11-01 00:30).
- Sources: xlit_map 1911, word_fix 112, name 90, phrase 53, model guess 54, passthrough 45. needs_review 164 (pending listen 57, model 54, suspect 31, interpolated timing 33, content pending 17, low prob 5).
- Apex (untimed Hinglish ASR) as 2nd opinion: mean loose agreement 0.824; 79 word-level diff hints after skeleton filter. Apex catches real master errors (prashit damandir->prasiddh mandir, Kathiawar chetar->kshetra, shanko->shaam ko, maanyat aug->maanyataon, dasva isthan->dasven sthaan, lagbak->lagbhag) and is itself wrong elsewhere (sharaab, vote, pyaaz, daurika) -> hints only.
- Sample: out/hinglish_xlit/dwarika_hinglish_sample_02m40s.mp4 (30 s, Hinglish over v5 preview which already has Devanagari burned). Visual frame check: readable, synced by eye on one frame only; full listening NOT_TESTED.
- Licence: Yapper code Apache-2.0; map/Lipi weights "license: other" (Dakshina/Xlit-Crowd/L3Cube/Aksharantar terms) -> runtime only, not bundled; check before publish. Roman Dwarka family spelling = agent default, user to confirm (Dwarka vs Dwarika).
- Status: WARN (draft). Hinglish follows the master: fixing master transcript fixes captions; rerun after listening.

## 2026-11-02 08:20 IST, why fetch scenes come back empty (my diagnosis)
- Cause: fetch-plan builds queries from our alias tags and drops real names like "Bet" in "Bet Dwarka". Commons search ANDs every word.
- My live test: "Bet Dwarka" gave 193 hits; incategory:"Bet_Dwarka" gave 107; deepcat:"Dwarka" gave 749; "Siddheshwar Mahadev Dwarka" gave 1 (Visavada, not Dwarka). A depicts search (P180) gave 0 for my guessed Dwarka Q-id, which I have not checked; depicts data looks sparse.
- S21 and S22 are talk scenes (budget, outro), so no real photo exists for them; profile fallback stays.
- Approaches seen on GitHub (licences not checked, plan copies no code): commonslens (category deep mode + depicts), daewik-p commons-depicts explorer (categorymembers + subcategories), dubeysanskar/WikiSemanticImgSearch (CLIP + keyword + category), View it! (Q-item to P180/P373).
- Proposed: a category-pool mode that pulls deepcat Dwarka once, ranks it with our matcher, and keeps named phrases whole. Waiting for user yes.

## 2026-11-03 Beat layer research (research-first rule)
- User goal: Claude-style Premiere timeline, marker + new shot at every narration point (not boring), later video clips.
- AutoCut (autocut.com): paid plugin; AutoB-Rolls = transcript -> moments -> Storyblocks stock/AI images. AI Plan $14.9/mo yearly, $19.8 monthly; trial. Hindi not verified; generic/AI visuals conflict with no-wrong-place rule.
- louisedesadeleer/b-roll-finder (MIT, agent skill): per-beat interpretation, drop beat if no accurate visual, land +0.2-0.5 s AFTER word, sub-pixel Ken Burns (no zoompan), frame-grid self-check, manifest. PICK (rules only).
- Montaj b-roll docs: beat = contiguous span with one visual subject, cut on word onset (idea only, licence unchecked).
- auto-editor (Unlicense): silence/motion cuts, --export premiere. Optional for pause detection.
- Proposed: thin `kang.py beats` on words.json -> beats.json + FCP7 markers + shot slots; A/B cut lead (-200 ms, v9) vs lag (+0.2-0.5 s). Open decision: crop/zoom reuse of one photo allowed or unique asset per beat. Awaiting user go.
- 2026-11-03 15:31 clip/image sources research: user has NO own footage. MoneyPrinterTurbo (MIT, ~138k stars) keyword->Pexels/Pixabay/Coverr clips (free keys) = pick to adapt clip search; Openverse API (CC images, no key, 'dwarka' 240 hits incl. Delhi Dwarka) for more photos; Commons has no Gujarat-Dwarka videos (4 hits, all wrong). AI video gen = paid + fake place, rejected. Next: user to create free Pexels key (request_secret), then `fetch-clips`.
- 2026-11-03 15:40 PARALLAX research (no code yet; build after v10 lands): Depth Anything V2 Small HF = Apache-2.0, 24.8M params (CPU OK). Options: longweekendlabs/parallax-studio (MIT, Win/Linux/mac, created 2026-05, depth+pose, MP4 export) = PICK to study/adapt; pierlj/ken-burns-effect (MIT, old 2020, CUDA-ish) = backup; BrokenSource/DepthFlow (AGPL-3.0, best quality, GPU shader) = idea only; Lakshaaysharma/depth-parallax (DA-V2 + pixel warp, licence unchecked). Not yet told user the pick; include in v10 answer. Test plan: 3 stills incl S21/S22, short preview.
- 2026-11-03 15:43 USER DECISION (parallax): "jo best output wahi karna". Plan: DA-V2 Small (Apache) + own thin KANG warp renderer (feathered depth idea from parallax-studio MIT) as default; DepthFlow (AGPL) allowed ONLY as separate external program for A/B, never code merged into KANG; DA-V2 Base/Large (NC) never in outputs. Start after beat-layer v10 lands; first preview = 3 stills incl S21/S22.
- 2026-11-03 15:50 Openverse API test (mine, 20 results/query): dwarka 240 (Flickr, 18/20 CC BY, many ~500 px wide), dwarkadhish 164 (includes Mathura temple = wrong place, some NC), bet dwarka 127 (port/boat CC BY, some BY-ND). Verdict WARN/useful: needs licence filter (by,by-sa,cc0,pdm), min-width filter, place check. MoneyPrinterTurbo untested (needs Pexels key). Agreed order with user: v10 beats -> parallax -> Openverse+Pexels -> cards+map -> YouTube CC + AI motion; show effect previews each. Integration: all sources -> same asset index (licence/label/sha256) -> beats-assign priority (exact photo/CC clip > parallax > map/card > representative stock > AI motion).
- 2026-11-03 15:55 USER PREF: "pura ek sath hi review karwana" -> do not ask for per-feature reviews; build beats+parallax+Openverse/Pexels+cards+map+YouTube CC+AI motion, then ONE combined review (single preview/package with effect variants labelled). Still need Pexels free key from user.
- 2026-11-03 15:58 Pexels: new API key issuance PAUSED (user screenshot). Switched to Pixabay (free key on pixabay.com/api/docs after login; /api/videos/ 1080p/4K; 100 req/60 s, cache 24 h, no mass download; Pixabay Content License, credit source). Secure form for Pixabay key open.
- 2026-11-03 16:05 Pixabay key saved (vault id 31428ecf-80b7-4a50-8e79-f488a55d8c62), connect_service 'pixabay' scheme url (key in ?key=). Same key = images + videos. My video test: "dwarka" 0 hits; "gujarat" 4 (Patan, Kutch, none Dwarka); "arabian sea beach"/"boat sea india"/"india temple" 500 each, 1280-2560 px, 10-49 s. Wrong-place risk in results (Kuwait souq, Alibaug Mumbai, ISKCON Bangalore, Kyoto) -> only generic sea/waves/boat/sky as 'representative', reject recognizable landmarks of other places. Image endpoint call errored once (non-JSON), retest later.

## 2026-11-03 16:50 2.5D parallax layer built (agent)
- DA-V2 Small (Apache-2.0, rev 5426e4f0) + own warp renderer (idea from parallax-studio MIT @32e4cb45). CPU.
- Test KANG_020 (3 stills), A/B + grid KANG_021 -> KANG_022 (gate tightened: stretch >25 % local scale, first PASS
  setting wins). Batch KANG_023: 19 clips, first pass 17 PASS/2 FAIL (false black-edge on night silhouette; S21
  stretch) -> fixes -> 19 PASS. Apply KANG_024, package KANG_025 = out/dwarika_v11_parallax_premiere.zip (186 MB).
- Speed sandbox 2 vCPU: depth 3.8-8.4 s per still (once, cached), render 1.79 s per video second at 1920.
- Artefacts: crowd smear at frame edge (S01), slight line bend (S07), spire/sky edge softening (S16, S19).
- Premiere import of v11: NOT_TESTED. Human visual review: pending (combined review, user pref 15:55).

## 2026-11-03 17:35 v12 external free sources (agent)
- Openverse: size=large results for Dwarka are almost all Wikimedia Commons files (Flickr items ~500 px fail the
  1600 px rule) -> Openverse mostly re-finds Commons; 11 of 42 were already in our pool. New useful: 4 Bhadkeshwar
  photos (exact, S10). Sandbox IP hit Cloudflare 429 for ~15 min (anon limit 20/min, 200/day).
- Pixabay: video API PASS; image API blocked by the credential proxy (connected URL = /api/videos/); proxy also blocks
  cdn.pixabay.com, so CDN downloads go direct. Generic queries still return many foreign/AI/low-quality hits;
  agent eye check: 76 thumbnails looked at, 24 kept and downloaded, 22 kept after checking downloaded frames, 19 used. Road/train/money themes mostly foreign -> few fits.
- Decision: hold caps exact 7 s / other 4.5 s before stock replaces a held photo; photo never returns after stock.
