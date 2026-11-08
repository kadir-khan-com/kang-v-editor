# junwen853/travel-video-studio-skill

- **Repo:** junwen853/travel-video-studio-skill — Codex/Claude agent skill: bina-GPS unordered travel footage se route-aware DaVinci Resolve travel films; Jianying/CapCut native finish ka raasta bhi andar hai
- **Link:** https://github.com/junwen853/travel-video-studio-skill
- **Licence:** MIT (repo page par verify; LICENSE file root me hai)
- **Activity:** 2 stars · 0 forks · 208 commits · 203 releases · repo bana 2026-06-28 (repo page, 2026-11-06) — stars kam, lekin is round ka sabse actively developed repo (lagatar release gates)
- **Content map:** Editorial judgment wala poora system — footage scoring/tiering, opening story (pehle 3 minute: promise, destination proof, title, arrival, texture, handoff), chapter story spine (context → movement → texture → payoff → aftertaste), shot-flow continuity, rhythm/pacing watchability, BGM beat-cut + phrase alignment, transition grammar/cadence, narration/subtitles, quality gates, DaVinci Resolve API path aur Jianying/CapCut draft automation ki taiyaari/audit. Neeche SKILL.md FULL hai + 22 technique references full hain. Baaki ~80 references (zyada tar audit-gate "contracts") naam se list me diye hain — unka kaam gates/checks hain, core technique SKILL.md + in references me hai.

---

## SKILL.md (full)

---
name: travel-video-studio
description: Complete travel video production workflow for Codex and Agent Skills-compatible coding agents. Use when an agent must turn unordered travel footage into a deliverable edit package with full-folder location recognition, route reconstruction, recognition/route MD reports, SRT captions, BGM cues, licensed aerial/stock footage search, typography, day-to-day transitions, and FFmpeg/FCPXML/DaVinci/Premiere/Final Cut handoff without relying on Computer Use unless no direct path exists.
---

# Travel Video Studio

## Operating Rule

Use this skill as a delivery workflow, not just a planning checklist. The default project directory is the user's selected VideoClaw Studio app or project directory. When `--project-dir` is omitted, helper scripts check `VIDEO_CLAW_STUDIO_DIR` first, then fall back to:

```bash
~/Pictures/Video-make/video-claw-studio
```

Default to Codex visual inspection. Use DaVinci Resolve API editing for the generic unattended finish, but use the verified Jianying native-draft path when the user explicitly wants Jianying and the current machine passes app, entitlement, draft-roundtrip, TTS, and export gates. Do not pull, install, or depend on local Ollama/7B vision models unless the user explicitly asks for that route. Codex should inspect contact sheets/sampled frames itself, write auditable review notes, and then build the selected editor timeline through the direct API or draft backend before using GUI control for the smallest unavoidable boundary.

This folder also works as a portable Agent Skill for Claude Code, Hermes, OpenClaw, Lobster/OpenClaw workspace, or another local coding agent that can read a `SKILL.md` folder. For non-Codex runtimes, resolve `<skill-dir>` to the installed folder, keep the same approval gates, run bundled scripts directly, and read `references/agent-runtime-compatibility.md` before changing install or runtime behavior. Do not fork the core travel-video workflow per runtime.

Treat every live edit as Skill regression testing. The primary goal is to improve this reusable Skill so future unordered travel-footage folders can be delivered with less user correction; the current film is only the test case. When a draft exposes a failure such as bad titles, missing BGM, sparse subtitles, portrait regressions, weak transitions, route uncertainty, Resolve/API gaps, stale QA evidence, or style mismatch, fix the current package only after generalizing the lesson into at least one durable Skill asset: a `SKILL.md` rule, script behavior, audit check, Definition-of-Done item, or reusable reference. Do not call a turn complete when it only patches one output and leaves the Skill unable to prevent or detect the same failure next time.

After substantial Skill changes, forward-test the Skill against more than one trip when suitable evidence is available. A credible forward-test should include at least one known-good rendered package, one separate matched project that is correctly blocked before cutting, and any unknown mounted media roots that must be identified rather than silently selected. This proves the Skill is learning reusable behavior instead of only overfitting the current film.

When no user footage is available, or after changing editor integration behavior, create a synthetic benchmark before claiming the Skill was tested:

```bash
python3 <skill-dir>/scripts/create_skill_benchmark_fixture.py --output-dir /tmp/travel-video-studio-benchmark --overwrite --json
```

The fixture produces read-only landscape, portrait, square, source-audio, BGM-only bridge, scenic-title, black-slate, SRT, TXT, and bad-caption probes. Use it for regression testing only; do not confuse it with real trip/location proof.

For a mixed-camera road-trip regression covering Mini-series drone identity, Action-camera speech, a persistent lower dashboard obstruction, synchronized phone capture, hard/scenic music selection, A3 ducking, Resolve transforms, and source immutability, run:

```bash
python3 <skill-dir>/scripts/run_no_material_multicamera_drone_smoke.py --output-dir /tmp/travel-video-studio-multicamera-drone --overwrite --json
python3 <skill-dir>/scripts/run_no_material_xinjiang_edit_smoke.py --output-dir /tmp/travel-video-studio-multicamera-roadtrip --overwrite --json
```

It must pass dashboard detection and timeline-height reframe math, authentic A1 speech retention, audience-caption quality gating, non-story source-voice muting, hard opening music, calmer ending music, measured A3 ducking, real local-bed creation, and byte-identical source checks. This synthetic proof does not replace a real Resolve render; after render, `audit_dashboard_reframe_render.py` must prove that the lower obstruction is gone in output pixels.

For a single no-material editor integration test, run:

```bash
python3 <skill-dir>/scripts/run_no_material_editor_smoke.py --output-dir /tmp/travel-video-studio-editor-smoke --overwrite --json
```

This combines fixture generation, audience-caption clean/bad probe auditing, a procedural sine-hum BGM musicality trap, DaVinci Resolve install/API reachability audit, Jianying/CapCut no-GUI app state audit, Jianying/CapCut media/SRT/TXT handoff packaging, GUI smoke checklist generation, Jianying/CapCut handoff contract auditing, false GUI export-origin traps, a fake completed GUI proof trap, and a current-audit bootstrap trap into one report without writing Resolve, launching Jianying/CapCut, starting renders, downloading assets, modifying source footage, or assuming a direct Jianying API. Its summary must expose `audienceCaptionBadProbeBlocked`, `bgmHumTrapBlocked`, `bgmHumTrapRejectedAsHumTone`, `guiSmokeChecklistPrepared`, `guiProofPendingFields`, `checklistPathMatchesLocal`, `jianyingFakeCompletedGuiProofTrapBlocked`, `jianyingCurrentAuditBootstrapTrapBlocked`, `jianyingCurrentAuditBootstrapAcceptedByCurrentRun`, `appPathMatchesStateApplication`, `postExportProofIdentity`, `currentAuditJsonWillBeWritten`, `currentAuditJsonMatchesChecklist`, `acceptedByCurrentRun`, and `exportFileIsPreparedInput` through the contracts so a copied folder, stale manifest, fake state/app/post-export JSON, editor-facing caption text, source media masquerading as export, or technically audible but hum-like placeholder BGM is not mistaken for a tested delivery path. The clean caption probe must pass with viewer-facing SRT/TXT, the bad-caption probe must block on the fixture's edit-status subtitle, the BGM hum trap must block through `audit_bgm_musicality_contract.py`, the false GUI trap must remain blocked when a synthetic fixture or arbitrary MP4 is passed as `--export-origin gui`, the no-file GUI trap must remain blocked when `--export-origin gui` is claimed without `--export-file`, the stale manifest copied-handoff trap must remain blocked when a copied handoff still points its manifest checklist path at the original folder, the fake completed GUI proof trap must remain blocked when fake state/app/post-export proof plus a source-media file is presented as a GUI export, and the current-audit bootstrap trap must accept the planned current audit JSON while still blocking fake app identity and source-media-as-export proof. Use `--require-resolve-reachable` only when the next step must write a real Resolve timeline.

For a focused Jianying/CapCut TTS/export readiness check, run:

```bash
python3 <skill-dir>/scripts/run_jianying_gui_tts_export_smoke.py --output-dir /tmp/travel-video-studio-jianying-gui-smoke --overwrite --json
```

This command creates or consumes a handoff package, audits local Jianying/CapCut app state, verifies the TTS text and GUI proof contract, and runs the TTS/export readiness gate without launching the app. Add `--require-installed` when the next step specifically depends on Jianying/CapCut being installed; it must block on machines where the app is missing. After a real GUI export, rerun it with `--handoff-dir <handoff> --export-file <mp4> --export-origin gui --state-json <state-audit-json>` and require `claimsJianyingTtsOrExport=true`, `exportCountsAsGuiProof=true`, `currentAuditJsonWillBeWritten=true` or an accepted prior post-export audit, and `exportFileIsPreparedInput=false` before claiming Jianying generated TTS or export.

When the user asks whether Jianying/CapCut can be connected without Computer Use, read `references/capcut-jianying-draft-automation.md` and run:

```bash
python3 <skill-dir>/scripts/audit_jianying_capcut_draft_automation.py --output-dir /tmp/travel-video-studio-capcut-draft-automation --json
```

This detects local non-GUI draft automation readiness without installing packages, launching Jianying/CapCut, decrypting drafts, writing draft projects, or claiming TTS/export. It checks for community tools such as `capcut-cli`, `cutcli`, `pyCapCut`, `pyJianYingDraft`, `CapCutAPI`, `CapCut-Mate-API`, `capcut-mcp`, `cli-anything-capcut`, `jianying-editor-skill`, and `capcut-export`, scans known local draft roots for `draft_content.json`, `draft_info.json`, `draft_meta_info.json`, and `template-2.tmp`, and classifies readable plaintext JSON versus encrypted/opaque Jianying 6+ draft files. Add `--require-plaintext-template` when the task is to modify or learn from an existing template; the audit must then expose `plaintextTemplateReady=true` before a non-GUI template experiment is allowed. Treat `directDraftAutomationReady=true` as permission to generate a separate draft, not as export proof. Treat `toolCandidateCount`, `cloudRenderCandidateCount`, `cloudRenderVerified=false`, `cutcliCloudRenderVerified=false`, `claimsCutcliCloudRender=false`, and `requiresSeparateCloudRenderExperiment=true` as research inventory. On an unverified machine, keep Resolve as the reliable finish. On a machine where the same generated project passes the native roundtrip, in-app TTS/playback, and ffprobe export gates below, Jianying is an approved finish for Jianying-requested work; this still does not prove no-GUI macOS export.

For a real Jianying native draft with built-in transitions, effects, filters, SRT, BGM, optional Jianying TTS, and audited export, start from `examples/jianying-native-edit-spec.example.json` and use the pinned `pyJianYingDraft==0.3.0` runtime prepared by `prepare_capcut_jianying_tooling_bootstrap.py`. For a hotel/car/airport/gate/aircraft departure chain, read `references/homeward-flight-pov-style.md` and start from `examples/jianying-homeward-pov-edit-spec.example.json` instead. Its `editorialPolicy` is enforced by `build_jianying_native_draft.py`: BGM-only camera audio, enabled TTS, missing viewer subtitles, duplicate/missing clean title, excessive or adjacent motion accents, and directional motion accents without motion/BGM/title/landing evidence must block before a draft is written.

For a mixed original-audio plus scenic-BGM Jianying edit, original source sound is the default, not the exception. Set `editorialPolicy.preserveOriginalSourceAudioByDefault=true`, `faceToCameraOriginalAudioRequired=true`, and `highVolumeBgmOverAudibleSourceForbidden=true`. Every clip must carry `sourceAudioClassification` and `sourceSpeechEvidence`; only explicit drone, generated graphic/title, pure-scenic Action-camera, or proved in-car-outward windows may be muted. Keep face-to-camera, transcript-backed speech, meals, walking, reactions, and lived-in scene sound audible. A deliberately quiet music bed over walking or street texture may not exceed `peopleAndWalkingLowBedMaximumVolume`; loud scenic BGM may overlap only muted picture. When TTS is requested, set `tts.narrationScheduledOnlyOnMutedPictureWindows=true`; any SRT/TTS interval that overlaps audible original source sound is a build blocker. Use `bgmForbidden=true` on frustration, conflict, sensitive human, or deliberately dry narrative windows. Music rows must include `title`, `provider`, `sceneType`, `use`, `requestedReference`, and `matchType` so licensed substitutions and scene fit remain auditable.

Selected drone and pure-scenic Action-camera windows must not become silent wallpaper. For a scenic-led travel edit, set `droneScenicBgmCoverageRequired=true`, `pureScenicAction4BgmCoverageRequired=true`, `requiredScenicBgmMinimumCoverageRatio=0.995`, and a deliberate `maximumMutedAudioDesertSeconds` such as `18`. The native builder must measure timeline overlap, not merely count music rows: every selected `drone_pure_scenic` and `action4_pure_scenic` clip needs near-complete named, playable BGM coverage, while every muted picture run needs either BGM or viewer narration before the configured desert limit. Use strong, scene-matched music for aerial scale, follow-car, grassland, canyon, mountain-pass, and road-payoff sequences; vary the source excerpt and motif by chapter instead of looping one track mechanically. TTS may sit over muted scenic BGM, but it must stay viewer-facing, humanized, and short enough to leave musical breathing room. This rule does not rescue weak takeoff, landing, controller, phone-dominant, or redundant drone footage; reject those during selection first.

When a draft loses exciting material or the user asks for Jianying-native music, read `references/editorial-judgment-jianying-music-contract.md`. Metadata scores, filenames, technical quality, and sparse frames are discovery hints, not final rejection evidence. Scan the full duration of every active source, review every time-ranged candidate in motion, protect high-value windows with a reversible keep/reserve/reject ledger, and run a second-pass omission challenge against the strongest unused moments. Never delete source files. When Jianying music is requested, search and audition inside Jianying, record exact native asset IDs and entitlement, use music only on approved scenic windows, preserve authentic speech, vary the catalog, and align phrases to picture cuts. Run `audit_editorial_judgment_contract.py`; it must block silent highlight loss, lazy two-song reuse, non-native placeholder music, off-phrase cuts, source-audio damage, or changes outside the dedicated BGM graph.

When the user supplies a large DOCX/CSV/JSON music guide or asks for many online tracks, read `references/bgm-catalog-beatcut-contract.md`. Parse the full catalog before selection, resolve exact requested versions through a lawful or user-authorized provider, reject mismatched variants, stabilize and probe every approved asset, and cut varied musical phrases on strong beats and picture boundaries. For long-form edits with at least 20 cues, require at least `max(12, ceil(cue_count * 0.35))` unique songs and no repeat within the prior six cues unless the approved pool is exhausted and the exception is recorded. Long forest/lake/canyon/road hero passages should carry a deliberate calm-to-lift-to-climax arc. Run `audit_bgm_catalog_beatcut_contract.py` against the application report and block delivery if it finds weak variety, off-beat starts, invalid source ranges, uncovered scenic windows, authentic-audio overlap, or any change outside the dedicated BGM graph. The audit never replaces a human listen pass.

Materialize those decisions before draft creation. The scenic plan is a JSON placement list with named, locally playable music; the narration plan is a reviewed Humanizer replacement/addition list, never raw model prose or editor-facing status text.

```bash
python3 <skill-dir>/scripts/apply_jianying_scenic_audio_plan.py \
  --spec <base-edit-spec.json> \
  --plan <scenic-audio-plan.json> \
  --output-spec <scenic-audio-spec.json> \
  --report <scenic-audio-report.json> \
  --json
python3 <skill-dir>/scripts/materialize_humanized_narration.py \
  --source-srt <viewer-narration-base.srt> \
  --plan <humanizer-narration-plan.json> \
  --output-srt <viewer-narration-final.srt> \
  --output-txt <viewer-narration-final.txt> \
  --report <humanizer-narration-report.json> \
  --json
```

When the user names an exact Jianying voice and hundreds of GUI clicks would be wasteful, use the optional prepared-audio path before Computer Use:

```bash
<isolated-python> <skill-dir>/scripts/generate_jianying_sami_tts.py \
  --srt <viewer-facing-narration.srt> \
  --output-dir <prepared-tts-dir> \
  --speaker-id ICL_zh_female_manbo_jianying \
  --speaker-name "曼波讲故事"
```

The isolated runtime needs `websockets==15.0.1` and `truststore==0.10.4`; use the macOS trust store and never disable TLS verification. The generator must discover local Jianying User Data, use the requested speaker ID exactly, forbid fallback voices, ffprobe every result, fit each line without truncation, and bind the manifest to the current SRT hash. Bind the prepared rows and the final viewer text through the checked helper instead of editing a large spec by hand:

```bash
python3 <skill-dir>/scripts/bind_jianying_prepared_tts.py \
  --spec <scenic-audio-spec.json> \
  --srt <viewer-narration-final.srt> \
  --txt <viewer-narration-final.txt> \
  --manifest <prepared-tts-dir>/jianying_sami_tts_manifest.json \
  --humanizer-plan <humanizer-narration-plan.json> \
  --maximum-muted-audio-desert-seconds 18 \
  --output-spec <final-edit-spec.json> \
  --report <tts-binding-report.json> \
  --json
```

The binder must rerun the full story contract and block stale SRT, wrong voice, missing files, row-count mismatch, scenic BGM gaps, long silent picture, source-audio overlap, or a missing actual TTS track. Prepared audio is not playback proof: open/save the draft, hear representative opening/middle/ending lines, record the exact voice and playback position, and keep human audition required. On another Mac, rediscover that machine's local Jianying config and regenerate; if the direct service is unavailable, use exact in-app TTS through Computer Use and do not silently substitute another voice.

After changing this path, run `run_no_material_jianying_native_roundtrip_smoke.py` and require `preparedJianyingSamiTtsAccepted=true`, `preparedTtsStaleSrtTrapBlocked=true`, `preparedTtsWrongVoiceTrapBlocked=true`, and `preparedTtsDoesNotClaimPlaybackBeforeProof=true`. These fields prove exact-voice manifest handling and stale/wrong-voice rejection; only the separate GUI playback plus human-listen proof may claim that the prepared narration was actually heard in Jianying.

After any visual-timeline rebuild, run `scripts/realign_jianying_approved_speech_plan.py` before planning BGM ducking or final audio. It maps every approved source-speech range back to the exact selected visual window and rewrites stale timeline positions; `finalize_jianying_delivery_spec.py` independently blocks speech that is still out of sync by more than 50 ms. Before final visual approval, run `scripts/audit_jianying_selected_windows.py`; same-source near-duplicate visual clusters above its default three-window limit are blockers, not harmless review notes. For a mixed BGM/ambience/approved-speech finish, build the plans with `prepare_jianying_music_placement_plan.py`, `prepare_jianying_ambience_placement_plan.py`, and `prepare_jianying_authentic_audio_plan.py`, then use `finalize_jianying_delivery_spec.py` as the only path that binds the final TXT/SRT and master audio rows to the native draft spec.

When selected-window evidence shows a persistent dashboard or vehicle obstruction, run `prepare_dashboard_reframe_plan.py`, render exact candidate/time mappings with `prepare_jianying_dashboard_reframe_preview.py`, and close every candidate through `finalize_jianying_dashboard_reframe_review.py` before using `apply_jianying_dashboard_reframe_plan.py`. The finalizer must reject swapped candidate/source mappings, missing decisions, overlapping approve/reject lists, or changed source files. Convert only approved zoom/tilt rows into Jianying clip transforms. The source stays read-only, and completion still requires `audit_dashboard_reframe_render.py --spec <final-jianying-spec.json> --render <final.mp4>` pixel inspection of the actual exported frame; a plan or draft transform alone is not render proof.

After building any BGM or ambience master with `build_bgm_bed.py`, require its manifest to report `durationMatchesTarget=true`, `audioStreamStartsAtZero=true`, `audioStreamMatchesTarget=true`, and `nonAudioStreamCount=0`. Independently probe the primary audio stream, not only the container format. Sparse placement plans must be padded through the full timeline, timestamps must start at zero, and inherited chapter/data streams must be stripped; a successful ffmpeg exit with a late-starting or short audio stream is a blocker.

```bash
python3 <skill-dir>/scripts/run_bgm_bed_duration_smoke.py --output-dir /tmp/travel-video-studio-bgm-duration --overwrite --json
```

On macOS, Jianying is sandboxed. `--media-mode reference` is approved for large same-machine projects only when `codex_native_draft_build.json` reports `referenceMediaAuthorization.roots`, each reported root is selected once through Jianying's Import folder picker, the draft is closed and reopened without a relink dialog, and readable opening, middle, and ending frames are recorded. Never relink hundreds of files one by one. Security-scoped folder access is machine-local and must be repeated after moving the Skill or draft to another Mac. Use `--media-mode copy` for small portable fixtures or a deliberately consolidated delivery package.

```bash
<isolated-python> <skill-dir>/scripts/audit_jianying_resource_entitlements.py --spec <edit-spec.json> --require-free-delivery --json
<isolated-python> <skill-dir>/scripts/generate_jianying_sami_tts.py --srt <viewer-facing-narration.srt> --output-dir <prepared-tts-dir> --speaker-id <exact-speaker-id> --speaker-name <exact-voice-name>
<isolated-python> <skill-dir>/scripts/build_jianying_native_draft.py --spec <edit-spec.json> --draft-root <jianying-draft-root> --draft-name <project-name> --media-mode copy --json
python3 <skill-dir>/scripts/record_jianying_gui_proof.py --project-dir <project-dir> --record-tts --tts-voice <exact-voice-name> --playback-position <observed-timecode> --human-listen-approved --json
python3 <skill-dir>/scripts/record_jianying_gui_proof.py --project-dir <project-dir> --record-reference-media --reference-media-root <reported-root> --reference-media-sample <opening-timecode> --reference-media-sample <middle-timecode> --reference-media-sample <ending-timecode> --no-relink-dialog-observed --json
python3 <skill-dir>/scripts/record_jianying_gui_proof.py --project-dir <project-dir> --record-export --export-path <jianying-export.mp4> --json
python3 <skill-dir>/scripts/audit_jianying_native_draft.py --project-dir <project-dir> --require-app-roundtrip --require-export --json
python3 <skill-dir>/scripts/audit_jianying_native_draft.py --project-dir <project-dir> --require-app-roundtrip --require-tts-generated --require-export --json  # narration only
```

Run the entitlement audit before building. Free-delivery mode is the default and must reject VIP transitions, effects, filters, or voices; use `--allow-vip-assets` or `tts.allowVipVoice=true` only when the current editor account entitlement is known and the brief accepts it. Use `--media-mode copy` for a portable small-media roundtrip, or the folder-authorization-gated reference mode above for large same-machine edits. Zero additional video effects is valid when the build report contains an explicit zero count; do not force effect clutter merely to satisfy QA. `subtitles` are always viewer-facing; they do not enable voiceover. Set `tts.enabled=true` only when the brief asks for spoken narration. A BGM-only brief keeps TTS disabled and retains only TXT/SRT copy. Use Computer Use only to open/save the generated project, authorize reported media roots, select the audited Jianying voice, trigger text-to-speech, play the timeline, and export; draft construction, native assets, captions, BGM, entitlement checks, and readback audits stay script-driven. If the runtime has no GUI control, emit the proof commands for an operator and remain blocked instead of claiming TTS/export.

For the no-material homeward POV story-policy regression, run:

```bash
python3 <skill-dir>/scripts/run_no_material_jianying_homeward_story_smoke.py --output-dir /tmp/travel-video-studio-jianying-homeward-story --overwrite --json
```

It must pass the good BGM-only task-chain specification and block the bad trap for audible camera clips, enabled TTS, missing viewer subtitles, duplicate clean titles, motion-transition overuse, insufficient spacing, missing two-sided movement, missing BGM hit, title collision, excessive duration, and short landing hold. It proves the reusable Jianying specification gate, not a native app roundtrip or final-film taste.

For the native-draft proof traps, run:

```bash
python3 <skill-dir>/scripts/run_no_material_jianying_native_roundtrip_smoke.py --output-dir /tmp/travel-video-studio-jianying-native-roundtrip --overwrite --json
```

It must prove `freeNativeAssetAccepted=true`, `vipNativeAssetTrapBlocked=true`, `freeTtsVoiceDetectedFromLocalCache=true`, `subtitleDoesNotAutoEnableTts=true`, `preservedSourceAudioPolicyAccepted=true`, `mutedSpeechTrapBlocked=true`, `audiblePureScenicDroneTrapBlocked=true`, `highVolumeBgmOverSourceAudioTrapBlocked=true`, `ttsOverSourceAudioTrapBlocked=true`, `missingDroneScenicBgmTrapBlocked=true`, `missingAction4ScenicBgmTrapBlocked=true`, `mutedAudioDesertTrapBlocked=true`, `opaqueJianying11RoundtripAccepted=true`, `zeroNativeVideoEffectsAccepted=true`, `referenceMediaAuthorizationProofAccepted=true`, `incompleteReferenceMediaProofTrapBlocked=true`, `ttsFilesAloneDoNotClaimPlayback=true`, `ttsGeneratedAndPlaybackVerified=true`, `exportReadBackVerified=true`, `videoOnlyExportTrapBlocked=true`, and `claimsFinalTravelFilm=false`. This synthetic smoke validates the portable contract; only a current real app roundtrip plus human TTS/BGM listen and rendered-film QA can approve a delivery.

For no-material Jianying/CapCut local draft regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_capcut_draft_automation_smoke.py --output-dir /tmp/travel-video-studio-capcut-draft-smoke --overwrite --json
```

This smoke creates synthetic plaintext and opaque draft roots, then proves the Skill can allow a throwaway plaintext draft experiment while blocking opaque Jianying 6+ template modification and preserving the researched tool registry. It must surface `goodPlaintextDraftExperimentReady=true`, `opaqueDraftTrapBlocked=true`, `plaintextDraftDetected=true`, `encryptedDraftDetectedNotModified=true`, `directDraftExportStillUnverified=true`, `requiresGuiForFinalCapCutExport=true`, `toolCandidateCount`, `cloudRenderCandidateCount`, `cloudRenderVerified=false`, `cutcliAvailableInFixture=true`, `cutcliCloudRenderVerified=false`, `claimsCutcliCloudRender=false`, `macosNoGuiFinalExportStillUnverified=true`, `requiresSeparateCloudRenderExperiment=true`, `claimsJianyingTtsOrExport=false`, `claimsFinalCapcutBackendAutomation=false`, and `claimsFinalCapcutDraftAutomation=false`. Passing this smoke does not mean the current machine can control Jianying/CapCut; it means the Skill will not fake support when tools, plaintext roots, cloud credentials, or real GUI/export proof are missing.

Before installing or trying community draft tools on a new machine, prepare an isolated bootstrap and proof pack:

```bash
python3 <skill-dir>/scripts/prepare_capcut_jianying_tooling_bootstrap.py --output-dir /tmp/travel-video-studio-capcut-tooling --overwrite --json
python3 <skill-dir>/scripts/run_no_material_capcut_tooling_bootstrap_smoke.py --output-dir /tmp/travel-video-studio-capcut-tooling-smoke --overwrite --json
```

The bootstrap probes Python, pip, Node 18+, npm, `capcut-cli`, `cutcli`, `pyCapCut`, and `pyJianYingDraft`; creates only an isolated sandbox and throwaway draft root; and writes pinned npm/Python install commands plus post-install and cloud-render proof commands. It does not run an install, download an installer, launch Jianying/CapCut, scan common real draft roots unless `--include-common-draft-roots` is supplied, or modify a real draft. Add `--require-tooling-ready` when Python/Node prerequisites are mandatory and `--require-installed-tool` when a local draft tool must already exist. The smoke must expose `toolingBootstrapReady=true`, `safeThrowawayExperimentReady=true`, `missingToolTrapBlocked=true`, `temporaryInstallPlanPrepared=true`, `postInstallProofCommandsPrepared=true`, `downloadOrInstallRan=false`, `realDraftModificationAllowed=false`, and `requiresDaVinciDefaultFinish=true`. Even after a local draft tool is ready, keep `requiresGuiForFinalCapCutExport=true`, `cloudRenderVerified=false`, `claimsCutcliCloudRender=false`, `claimsFinalCapcutBackendAutomation=false`, and `claimsFinalCapcutDraftAutomation=false` until a separate real export proof passes.

When the goal is to hand a real GUI operator or another AI a concrete Jianying/CapCut TTS/export proof package, run:

```bash
python3 <skill-dir>/scripts/prepare_jianying_gui_verification_pack.py --skill-dir <skill-dir> --output-dir /tmp/travel-video-studio-jianying-gui-pack --overwrite --json
```

This writes a focused smoke report, handoff folder, `Jianying_GUI_VERIFICATION_PACK.md`, and executable `POST_EXPORT_AUDIT_COMMANDS.sh`. If Jianying/CapCut is installed, the pack should reach `readyForGuiOperator=true`; if the app is missing, it should reach `readyForInstallThenGuiProof=true` unless `--require-installed` is supplied, in which case missing app proof is a blocker. The pack must not launch Jianying/CapCut, assume a direct API, or claim `claimsJianyingTtsOrExport=true`; it only creates the exact post-export command that must be rerun with a real GUI-exported MP4.

After a real Jianying/CapCut GUI export, prefer the proof-field filler before the post-export smoke:

```bash
python3 <skill-dir>/scripts/fill_jianying_gui_proof_fields.py --handoff-dir <handoff> --state-json <state-audit-json> --app-path <Jianying-or-CapCut.app> --export-file <gui-export.mp4> --tts-voice-preset <voice-name> --tts-generated-in-app --tts-audio-auditioned --source-media-untouched --subtitle-visibility-checked --apply --json
```

This updates `gui_smoke_checklist.json` only when the app path matches the state audit, the export is ffprobe-readable, the export is not source/handoff input media, required proof paths exist or point to the current post-export audit, and no proof fields remain pending. If it blocks, do not hand-edit `proofStatus=completed_gui_proof`; fix the app/export/proof mismatch and rerun.

For the strongest no-material editor readiness sweep, run:

```bash
python3 <skill-dir>/scripts/run_editor_delivery_matrix.py --output-dir /tmp/travel-video-studio-editor-matrix --overwrite --json
python3 <skill-dir>/scripts/run_editor_delivery_matrix.py --output-dir /tmp/travel-video-studio-editor-matrix-apply --overwrite --apply-resolve-all --json
python3 <skill-dir>/scripts/run_editor_delivery_matrix.py --output-dir /tmp/travel-video-studio-editor-matrix-jianying-required --overwrite --require-jianying-installed --json
```

This matrix runs the no-material editor smoke, transition-smoothness smoke, music-pacing smoke, cover/title smoke, viewer-friction smoke, rendered-watchdown smoke, CapCut/Jianying draft-automation smoke, CapCut/Jianying tooling-bootstrap smoke, Jianying native-roundtrip proof traps, Resolve writeability audit, Resolve live-write smoke dry-run, Resolve V1/V3/A3 delivery-structure smoke, and Resolve render-readiness smoke in one report. It must include the Jianying/CapCut handoff contract status plus `jianyingCurrentAuditBootstrapTrapBlocked`/`jianyingCurrentAuditBootstrapAcceptedByCurrentRun` so a copied folder or first-run audit bootstrap is not mistaken for verified in-app TTS/export support, and it must report whether any export proof actually has `--export-origin gui`. It must also expose `badRenderedWatchdownTrapBlocked`, `goodFrameSamplesNonblank`, `goodAudioNotHumLike`, `claimsFinalRenderedWatchdown=false`, `opaqueDraftTrapBlocked`, `goodPlaintextDraftExperimentReady`, `toolingBootstrapReady`, `safeThrowawayExperimentReady`, `missingToolTrapBlocked`, `temporaryInstallPlanPrepared`, `postInstallProofCommandsPrepared`, `jianyingNativeRoundtripSmokeStatus`, `vipNativeAssetTrapBlocked`, `subtitleDoesNotAutoEnableTts`, `jianyingVideoOnlyExportTrapBlocked`, `downloadOrInstallRan=false`, `realDraftModificationAllowed=false`, `requiresDaVinciDefaultFinish=true`, `toolCandidateCount`, `cloudRenderCandidateCount`, `cloudRenderVerified=false`, `cutcliCloudRenderVerified=false`, `claimsCutcliCloudRender=false`, `macosNoGuiFinalExportStillUnverified=true`, `requiresSeparateCloudRenderExperiment=true`, `claimsFinalCapcutBackendAutomation=false`, and `claimsFinalCapcutDraftAutomation=false` so watchdown proof and non-GUI CapCut proof cannot be reduced to metadata rows. Use `--require-jianying-installed` only when the machine is expected to have Jianying/CapCut installed; then the matrix and shorter no-material smoke must expose `jianyingInstalledRequired`, `jianyingBlockedByMissingApp`, `jianyingHandoffOnlyNotGuiProof`, and `jianyingClaimsTtsOrExport` at top level. Add `--apply-resolve-all` when all safe non-render Resolve proofs are approved; it expands to live-write, V1/V3/A3 delivery-structure, and render-settings apply/readback, but still never queues or starts a render. Use the narrower `--apply-resolve-live-write`, `--apply-resolve-delivery-structure`, or `--apply-resolve-render-settings` flags only when debugging one proof. When Resolve apply flags are used, the report must expose `readbackIdentityProof`, `readbackIdentityAccepted`, and `sourcePathsMatch`; a pass requires the readback project/timeline, item counts, and source paths to match this current throwaway apply. The matrix still must not launch Jianying/CapCut, queue renders, start renders, download assets, create TTS, or modify user/source footage.

For no-material transition-smoothness regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_transition_smoothness_smoke.py --output-dir /tmp/travel-video-studio-transition-smoothness --overwrite --json
```

This synthetic smoke tests the Skill's transition rules without real footage or Resolve writes. It must pass the good transition rows and block the bad trap, surfacing `badTransitionTrapBlocked=true`, `smoothImportantTransitionsHaveBridgeOrMatch=true`, `motionAccentRarityPassed=true`, `motionAccentBgmHitPassed=true`, `motionAccentTitleSafePassed=true`, `noBackToBackMotionEffects=true`, `noTemplateEffectLanguage=true`, `requiresRealFootageForFinalSmoothness=true`, and `claimsFinalTransitionSmoothness=false`. Passing this smoke proves the rules reject random/template rotation, hard important-boundary cuts, missing bridge/match evidence, missing BGM hit, title-unsafe motion, short landing holds, source-voice leakage, and back-to-back flashy effects; it does not prove a real trip's final transitions are smooth.

For no-material music-pacing regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_music_pacing_smoke.py --output-dir /tmp/travel-video-studio-music-pacing --overwrite --json
```

This synthetic smoke tests the Skill's BGM rhythm rules without real footage, real music, or Resolve writes. It must pass the good music cue rows and block the bad trap, surfacing `badMusicPacingTrapBlocked=true`, `allRowsHaveBgmFileOrSearchBrief=true`, `allRowsHaveBeatGridEvidence=true`, `importantCutsLandOnBgmHitOrPhrase=true`, `scenicBridgesHaveMusicBreath=true`, `sourceVoiceMutedForBgmOnly=true`, `noHumOrPlaceholderBgm=true`, `rhythmVarietyPassed=true`, `requiresRealBgmForFinalMusicPacing=true`, and `claimsFinalMusicPacing=false`. Passing this smoke proves the rules reject hum/tone/placeholder BGM, source-voice leakage, beat-spam cutting, missing cue/source evidence, missing phrase or BGM-hit anchors, short scenic breathing room, and mismatched mood; it does not prove a real film's music edit is final.

For no-material BGM musicality regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_bgm_musicality_smoke.py --output-dir /tmp/travel-video-studio-bgm-musicality --overwrite --json
```

This synthetic smoke materializes real audio probes and runs the BGM musicality contract without user footage, Resolve writes, downloads, or Jianying/CapCut. It must pass the good local fixture and block the hum/tone trap, surfacing `goodBgmMusicalityPassed=true`, `badBgmMusicalityTrapBlocked=true`, `badBgmMusicalityRejectedAsHumTone=true`, `goodBgmActiveBandCount`, `goodBgmDynamicRangeDb`, `requiresRealBgmForFinalMusicality=true`, `humanListenStillRequiredForFinalBgm=true`, and `claimsFinalBgmMusicality=false`. Passing this smoke proves the Skill rejects single-frequency/flat procedural BGM and keeps a human-listen gate for real final music taste; it does not prove a real trip's selected BGM is emotionally right.

For no-material large-catalog beat-cut regression testing, run:

```bash
python3 <skill-dir>/scripts/audit_bgm_catalog_beatcut_contract.py --self-test --json
```

This self-test must accept a varied, beat-aligned fixture and block a repeated, off-beat fixture. It proves the catalog/variety/beat/coverage/protected-track gates are active; it does not download music, touch an editor, or prove final music taste.

For no-material editorial-judgment and Jianying-native music regression testing, run:

```bash
python3 <skill-dir>/scripts/audit_editorial_judgment_contract.py --self-test --json
```

This self-test must accept full-duration source review, keep-window lineage, a completed omission challenge, and varied Jianying-native scenic cues, while blocking a deleted/rejected highlight plus repeated non-native off-phrase music. It does not inspect real footage, operate Jianying, or prove final taste; a real film still requires the full omission challenge and human in-editor listen pass.

For no-material cover/title composition regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_cover_title_composition_smoke.py --output-dir /tmp/travel-video-studio-cover-title --overwrite --json
```

This synthetic smoke tests the Skill's opening cover/title rules without real footage or Resolve writes. It must pass the good cover-title rows and block the bad trap, surfacing `badCoverTitleTrapBlocked=true`, `singleMainTitleLayer=true`, `cleanDestinationTitlePassed=true`, `bilingualHierarchyPassed=true`, `noDuplicateOrGhostedTitle=true`, `noRouteDateInternalOverlay=true`, `titleSubtitleSafeZonePassed=true`, `scenicEstablishingEvidencePassed=true`, `noPortraitOpeningRegression=true`, `requiresRealFrameProofForFinalCoverTitle=true`, and `claimsFinalCoverTitle=false`. Passing this smoke proves the rules reject ghosted/stacked titles, duplicate city text, route/date/internal labels, subtitle-title collisions, portrait opening regressions, non-scenic backgrounds, low contrast, missing support title hierarchy, and source-voice leakage on title cards; it does not prove a real cover/title frame is final.

For no-material viewer-friction regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_viewer_friction_smoke.py --output-dir /tmp/travel-video-studio-viewer-friction --overwrite --json
```

This synthetic smoke tests whether a first draft avoids obvious viewer-facing friction without real footage or Resolve writes. It must pass the good viewer rows and block the bad trap, surfacing `badViewerFrictionTrapBlocked=true`, `viewerFacingCaptionsPassed=true`, `noInternalWorkflowText=true`, `noBlackSlateOpeningOrEnding=true`, `noPortraitRegression=true`, `bgmOnlyNoSourceVoicePassed=true`, `noHumPlaceholderBgmPassed=true`, `bridgeContinuityPassed=true`, `subtitleDensityCuePassed=true`, `endingAftertastePassed=true`, `requiresRealRenderWatchdownForFinalViewerFriction=true`, and `claimsFinalViewerFriction=false`. Passing this smoke proves the rules reject AI-looking delivery failures such as editor-report captions, black/slate openings, portrait regressions, source voice under scenic/title sections, hum/placeholder BGM, sparse captions, missing route/scene bridge, random/template transition language, missing viewer purpose, and no ending aftertaste; it does not prove a real render has been watched down.

For no-material rendered-watchdown regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_rendered_watchdown_smoke.py --output-dir /tmp/travel-video-studio-rendered-watchdown --overwrite --json
```

This smoke creates real synthetic MP4 samples and verifies ffprobe streams, frame samples, landscape layout, nonblank frames, and non-hum-like audio without touching user footage, Resolve, or Jianying/CapCut. It must pass the good rendered watchdown probe and block the bad trap, surfacing `badRenderedWatchdownTrapBlocked=true`, `goodFrameSamplesNonblank=true`, `goodFrameSamplesLandscape=true`, `goodAudioStreamPresent=true`, `goodAudioNotHumLike=true`, `badBlackFrameTrapBlocked=true`, `badPortraitTrapBlocked=true`, `badInternalTextTrapBlocked=true`, `badHumAudioTrapBlocked=true`, `badFinalClaimTrapBlocked=true`, `requiresRealRenderWatchdownForFinalQuality=true`, and `claimsFinalRenderedWatchdown=false`. Passing this smoke proves the Skill no longer relies only on table rows for watchdown-level claims; it does not prove a real trip render has final BGM, subtitles, transitions, or viewer polish.

For no-material final-render bundle regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_final_render_quality_bundle_smoke.py --output-dir /tmp/travel-video-studio-final-render-bundle --overwrite --json
```

This smoke creates a synthetic good package with a real MP4 plus bound final-render reports, then creates a bad package with weak/missing proof. It must surface `goodFinalRenderQualityBundlePassed=true`, `badFinalRenderQualityBundleTrapBlocked=true`, `goodFinalRenderQualityBundleReady=true`, `goodAllRequiredReportsPassed=true`, `goodOutputMatchesRenderVerification=true`, `requiresRenderReportBundle=true`, `claimsDaVinciLevelWithoutBundle=false`, and `claimsFinalRenderQualityFromNoMaterial=false`. Passing this smoke proves the final-render quality bundle audit rejects missing final MP4/report closure, but it does not prove a real trip is DaVinci-level.

For no-material whole-film satisfaction regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_whole_film_satisfaction_smoke.py --output-dir /tmp/travel-video-studio-whole-film-satisfaction --overwrite --json
```

This smoke creates a synthetic good package with accepted whole-film source reports, then creates a bad package with missing reports, open watchdown rows, and metric failures. It must surface `goodWholeFilmSatisfactionPassed=true`, `badWholeFilmSatisfactionTrapBlocked=true`, `goodRequiredWholeFilmReportCount`, `goodPassedWholeFilmReportCount`, `requiresCurrentFinalOutputWatchdown=true`, `requiresNoOpenUnattendedRepairRows=true`, `claimsReferenceLevelWithoutWholeFilmGate=false`, and `claimsWholeFilmSatisfactionFromNoMaterial=false`. Passing this smoke proves the whole-film satisfaction gate rejects missing opening/chapter/rhythm/audio/transition/reference/director/watchdown closure, but it does not prove a real trip film is satisfying.

For no-material one-shot autonomy regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_one_shot_autonomy_smoke.py --output-dir /tmp/travel-video-studio-one-shot-autonomy --overwrite --json
```

This smoke creates a synthetic good package with every one-shot source report accepted, then creates a bad package with missing reports and metric failures across raw intake, opening, transition sequence, unattended repair, and whole-film closure. It must surface `goodOneShotAutonomyPassed=true`, `badOneShotAutonomyTrapBlocked=true`, `goodRequiredOneShotReportCount`, `goodPassedOneShotReportCount`, `requiresRawFolderToFinalChain=true`, `requiresNoExtraDiagnosis=true`, `requiresResolveBlueprintPreflight=true`, `claimsOneShotV14FromNoMaterial=false`, and `claimsDaVinciLevelFirstRunFromNoMaterial=false`. Passing this smoke proves the raw-folder-to-reference-level first-draft gate rejects incomplete evidence before another AI receives the Skill; it does not prove a real trip can be cut perfectly without real footage QA.

For no-material forward-test contract regression testing, run:

```bash
python3 <skill-dir>/scripts/run_no_material_forward_test_smoke.py --skill-dir <skill-dir> --output-dir /tmp/travel-video-studio-forward-test-smoke --overwrite --json
```

This smoke creates a synthetic good forward-test fixture and a bad trap fixture, then runs `audit_skill_forward_test_contract.py` against a temporary installed-shape copy of the Skill. It must surface `goodForwardTestContractPassed=true`, `badForwardTestTrapBlocked=true`, `requiresKnownGoodRenderedPackage=true`, `requiresMatchedBlockedProject=true`, `requiresUnknownMountedRoot=true`, `requiresBlockedProjectRecoveryPlan=true`, `claimsCrossTripGeneralizationFromNoMaterial=false`, and `claimsFutureTripPerfectionFromNoMaterial=false`. Passing this smoke proves the forward-test contract still rejects stale single-trip evidence, missing unknown-root handling, unsafe matched projects, and missing blocked-project recovery plans; it does not prove future real trips will cut perfectly without real footage QA.

For a single no-material release-confidence drill that ties the release audit, editor matrix, forward-test smoke, focused Jianying/CapCut smoke, and optional Resolve export smoke together, run:

```bash
python3 <skill-dir>/scripts/run_no_material_full_editor_drill.py --skill-dir <skill-dir> --output-dir /tmp/travel-video-studio-full-editor-drill --expected-version v0.1.201 --overwrite --apply-resolve-all --json
python3 <skill-dir>/scripts/run_no_material_full_editor_drill.py --skill-dir <skill-dir> --output-dir /tmp/travel-video-studio-full-editor-drill-4k --expected-version v0.1.201 --overwrite --apply-resolve-all --apply-resolve-render-export --quality-profile delivery-4k --json
python3 <skill-dir>/scripts/run_no_material_full_editor_drill.py --skill-dir <skill-dir> --output-dir /tmp/travel-video-studio-full-editor-drill-jianying-required --expected-version v0.1.201 --overwrite --apply-resolve-all --require-jianying-installed --json
```

The first command is no-render and should surface expected warnings rather than claiming full editor proof. Its top-level summary must expose `releaseAuditStatus`, `editorMatrixStatus`, `noMaterialDrillStageStatuses`, `noMaterialDrillStageBlockerCounts`, `noMaterialDrillStageWarningCounts`, transition fields including `badTransitionTrapBlocked` and `claimsFinalTransitionSmoothness=false`, music pacing fields including `badMusicPacingTrapBlocked`, `importantCutsLandOnBgmHitOrPhrase`, `noHumOrPlaceholderBgm`, and `claimsFinalMusicPacing=false`, BGM musicality fields including `goodBgmMusicalityPassed`, `badBgmMusicalityTrapBlocked`, `badBgmMusicalityRejectedAsHumTone`, `goodBgmActiveBandCount`, `goodBgmDynamicRangeDb`, `humanListenStillRequiredForFinalBgm=true`, and `claimsFinalBgmMusicality=false`, cover/title fields including `badCoverTitleTrapBlocked`, `noDuplicateOrGhostedTitle`, `noRouteDateInternalOverlay`, `titleSubtitleSafeZonePassed`, and `claimsFinalCoverTitle=false`, viewer-friction fields including `badViewerFrictionTrapBlocked`, `viewerFacingCaptionsPassed`, `noInternalWorkflowText`, `noBlackSlateOpeningOrEnding`, `bridgeContinuityPassed`, and `claimsFinalViewerFriction=false`, final-render bundle fields including `finalRenderQualityBundleSmokeStatus`, `goodFinalRenderQualityBundlePassed`, `badFinalRenderQualityBundleTrapBlocked`, `goodFinalRenderQualityBundleReady`, `requiresRenderReportBundle=true`, `claimsDaVinciLevelWithoutBundle=false`, and `claimsFinalRenderQualityFromNoMaterial=false`, whole-film satisfaction fields including `wholeFilmSatisfactionSmokeStatus`, `goodWholeFilmSatisfactionPassed`, `badWholeFilmSatisfactionTrapBlocked`, `goodRequiredWholeFilmReportCount`, `claimsReferenceLevelWithoutWholeFilmGate=false`, and `claimsWholeFilmSatisfactionFromNoMaterial=false`, one-shot autonomy fields including `oneShotAutonomySmokeStatus`, `goodOneShotAutonomyPassed`, `badOneShotAutonomyTrapBlocked`, `goodRequiredOneShotReportCount`, `requiresRawFolderToFinalChain=true`, `requiresNoExtraDiagnosis=true`, `requiresResolveBlueprintPreflight=true`, `claimsOneShotV14FromNoMaterial=false`, and `claimsDaVinciLevelFirstRunFromNoMaterial=false`, forward-test fields including `forwardTestSmokeStatus`, `goodForwardTestContractPassed`, `badForwardTestTrapBlocked`, `requiresKnownGoodRenderedPackage=true`, `requiresMatchedBlockedProject=true`, `requiresUnknownMountedRoot=true`, `requiresBlockedProjectRecoveryPlan=true`, `claimsCrossTripGeneralizationFromNoMaterial=false`, and `claimsFutureTripPerfectionFromNoMaterial=false`, and the Resolve apply/readback proof fields from the matrix, including `resolveLiveWriteReadbackIdentityAccepted`, `resolveLiveWriteReadbackSourcePathsMatch`, `resolveDeliveryStructureReadbackIdentityAccepted`, `resolveDeliveryStructureReadbackSourcePathsMatch`, `resolveRenderSettingsApplied`, `resolveSetRenderSettingsAccepted`, `resolveRenderStructurePrerequisiteReadbackIdentityAccepted`, and `resolveRenderStructurePrerequisiteSourcePathsMatch`, so another agent does not have to inspect nested reports to know which stage blocked or whether the throwaway Resolve writes matched current source paths. The second command may queue/start exactly one synthetic Resolve render and must report `resolveRenderExportCompleted=true`, 3840x2160 or better, FPS at least 59, `resolveRenderExportVideoQuality>=80000`, `resolveRenderExportClaimsFinalRender=false`, `toolchainOnlyNoRealFootage=true`, and `jianyingClaimsTtsOrExport=false` unless real GUI proof was supplied elsewhere. The third command is only for a machine that claims Jianying/CapCut is installed and ready; it must expose `jianyingInstalledRequired=true`, `jianyingMissingAppBlocksWhenRequired=true` when the app is absent, and `jianyingHandoffOnlyNotGuiProof=true` unless a real GUI export proof exists. It must never use user footage, launch Jianying/CapCut, assume a Jianying direct API, download assets, modify a source drive, or claim Bilibili/Malta/V14 film quality from synthetic evidence.

Do not run Resolve `--apply` smoke tests in parallel. Resolve scripting has global current-project/current-timeline state, so parallel smokes can cross-read each other's timeline; use `readbackIdentityProof` and `sourcePathsMatch` to block stale or cross-read evidence.

No-material tests prove the toolchain, not the film's taste. Do not claim Bilibili/Malta/V14-level viewer quality from synthetic fixtures alone; that still requires real footage or reference-package evidence through the normal package QA gates.

When DaVinci Resolve itself must be proven without user footage, run the stronger live-write smoke test:

```bash
python3 <skill-dir>/scripts/run_resolve_live_write_smoke.py --output-dir /tmp/travel-video-studio-resolve-live-smoke --overwrite --json
```

This default command creates the same read-only synthetic fixture, writes a Resolve blueprint and write contract, and performs a dry-run summary without changing Resolve. Add `--apply` only when the current operator explicitly approves a throwaway Resolve write: it must create a new smoke-test project/timeline, import only synthetic fixture clips as video-only V1 media, save the project, read it back with `audit_resolve_timeline.py`, require accepted `readbackIdentityProof` with matching source paths, and still never queue renders, download assets, generate TTS, or modify user footage.

When no user footage is available but the DaVinci delivery track structure must be guarded, run:

```bash
python3 <skill-dir>/scripts/run_resolve_delivery_structure_smoke.py --output-dir /tmp/travel-video-studio-resolve-structure-smoke --overwrite --json
```

This dry-run creates a synthetic V1/V3/A3 delivery blueprint with landscape V1 clips, a transparent V3 subtitle-overlay probe, and an A3 BGM-structure bed. Add `--apply` only after explicit approval for a throwaway Resolve project/timeline write; the readback must show accepted `readbackIdentityProof`, matching V1/V3/A3 source paths, V1 video items, V3 overlay items, A3 audio items, zero A1 source-camera items, zero A2 voiceover items, no render jobs, no downloads, and no source-footage writes. Treat this as editor-structure proof only: synthetic A3 audio is not approved music, and synthetic V3 overlay readback is not final subtitle visibility proof.

When no user footage is available but Resolve export defaults must be guarded, run:

```bash
python3 <skill-dir>/scripts/run_resolve_render_readiness_smoke.py --output-dir /tmp/travel-video-studio-resolve-render-readiness --overwrite --json
```

This creates a synthetic package, calls `prepare_resolve_render.py` in dry-run mode, and audits that the default render plan targets 4K, high frame rate, numeric high bitrate `VideoQuality` of at least `80000`, video+audio export, and no queued or started render job. It intentionally expects real-package blockers such as missing `delivery_audit.json` and `resolve_audit.json`; passing this smoke proves the render-settings contract is safe, not that a Resolve timeline or final MP4 exists. Add `--apply-resolve-settings` only when a throwaway Resolve project/timeline write is approved: it creates a synthetic V1/V3/A3 project, requires the prerequisite structure report to have accepted readback identity plus `sourcePathsMatch`, applies render format/codec/settings, reads back current format/codec/mode, verifies zero render-job delta, and still never calls `AddRenderJob` or `StartRendering`. If Resolve's Python API exposes full `GetRenderSettings`, compare those fields too; if the method is unavailable in the current Resolve build, report that as a warning rather than pretending full settings readback exists.

When no user footage is available but the actual DaVinci Resolve export path must be proven, run:

```bash
python3 <skill-dir>/scripts/run_resolve_render_export_smoke.py --output-dir /tmp/travel-video-studio-resolve-render-export --overwrite --apply --json
python3 <skill-dir>/scripts/run_resolve_render_export_smoke.py --output-dir /tmp/travel-video-studio-resolve-render-export-4k --overwrite --apply --quality-profile delivery-4k --json
```

This is the only no-material smoke that may queue and start a render, and only when `--apply` is supplied. It first creates a throwaway synthetic V1/V3/A3 Resolve project/timeline with accepted readback identity and `sourcePathsMatch`, then sets render settings, calls `AddRenderJob`/`StartRendering`, waits for completion, finds the exported MP4/MOV, runs ffprobe plus sample-frame extraction, and reports `qualityProfile`, `renderStarted`, `renderCompleted`, `renderVideoQuality`, output duration/resolution/FPS/bitrate/audio, sample-frame count, and `claimsFinalRender=false`. Use `--quality-profile delivery-4k` when the actual high-quality export path must be proven: it must request 3840x2160, 59.94fps, `VideoQuality=80000`, and require ffprobe output at least 3840x2160 and 59fps. It must never use user footage, launch Jianying/CapCut, download assets, modify the source drive, or claim route/style/subtitle/BGM quality from the synthetic output. Keep it separate from the default editor matrix because the normal matrix must not queue or start renders.

Start with read-only inspection:

```bash
python3 <skill-dir>/scripts/check_project_state.py --project-dir "$VIDEO_CLAW_STUDIO_DIR"
```

Then create or update a 20-minute long-form delivery package:

```bash
python3 <skill-dir>/scripts/build_delivery_package.py --project-dir "$VIDEO_CLAW_STUDIO_DIR" --target-duration-minutes 20
```

For the safe local end-to-end workflow, prefer:

```bash
python3 <skill-dir>/scripts/run_delivery_workflow.py --project-dir "$VIDEO_CLAW_STUDIO_DIR" --target-duration-minutes 20
```

This writes `workflow_run_report.json`/`.md`, checks Resolve API reachability, prepares route review when needed, prepares a route decision sheet, dry-runs route decision application, builds or refreshes the package, prepares local title cards, refreshes asset sourcing/enrichment, runs audience-caption, large-source unattended-readiness, transition source coverage, motion-accent repair, rendered transition proof, transition reference-readiness, transition-sequence-satisfaction, story-style, reference-alignment, director-intent, route-texture, title-bridge, stock/aerial closure, director-polish, final-viewer-friction, first-draft-satisfaction, unattended repair queue, whole-film-satisfaction, unattended-first-draft, one-shot-autonomy, Skill maturity, and V14 baseline audits, normalizes any `blocked*` audit status into top-level workflow blockers, dry-runs asset sourcing reconciliation, dry-runs the Resolve blueprint, prepares a Resolve apply approval contract, prepares a safe `render_plan.json`, and re-audits delivery readiness. It never writes Resolve, queues render jobs, downloads external assets, applies route/asset decisions, or generates local TTS unless the corresponding explicit flag is passed. Use `--skip-render-plan` only when a package-level render plan is intentionally deferred.

Use `scripts/make_voiceover_audio.py` after the narration script is approved or when the user explicitly asks for local TTS audio.

Use `scripts/prepare_delivery_assets.py` after `delivery_plan.json` and `resolve_timeline_blueprint.json` exist. It generates local title/place card media, refreshes Resolve enrichment, and writes `delivery_assets_report.json`/`.md`. It only generates local TTS voiceover when called with `--generate-local-voiceover`.

Use `scripts/check_resolve_api.py` after DaVinci Resolve is installed. Use `scripts/audit_resolve_writeability_state.py --json` before any Resolve `--apply` or whenever the Resolve API is reachable but project creation, timeline creation, current database, or current page evidence is missing. If this audit reports that the project library database is not exposed to scripting, inspect the Resolve UI for foreground modals such as Software Update, dismiss them, select the local project library, and rerun the audit before claiming DaVinci is write-ready. Use `scripts/audit_jianying_capcut_state.py --json` before claiming Jianying/CapCut support or attempting GUI/TTS/export work; it must not launch the app, write projects, queue renders, or treat handoff readiness as proof of in-app TTS/export. Use `scripts/audit_editor_integration_contract.py --json` after editor setup changes, before claiming DaVinci or Jianying/CapCut support, and when a user asks what editor path is available. The audit must distinguish Resolve app/scripting installation from live API reachability: missing Resolve app or scripting files blocks the default finishing path; API unreachable is a warning unless the next step writes an actual Resolve timeline, in which case Resolve must be open with local external scripting enabled. It must not assume a direct Jianying API.

Use `scripts/build_resolve_timeline.py` only after the package writes `resolve_timeline_blueprint.json`.

Use `scripts/prepare_jianying_handoff_package.py` when the user wants Jianying/CapCut, Jianying TTS, or a CapCut-style handoff but no verified direct API is available. Run `scripts/audit_jianying_capcut_state.py --json` first: if the app is absent, deliver only the handoff package and state that in-app TTS/export are unverified; if the app is present, GUI/Computer Use may be attempted only after approval. The package should contain media, SRT, TXT text-for-TTS, `tts_import/tts_script.txt`, `tts_import/tts_segments.json`, timing references, approved BGM assets for GUI import, and `gui_smoke_checklist.json`/`Jianying_GUI_SMOKE_CHECKLIST.md` for real GUI proof fields. Then run `scripts/audit_jianying_handoff_contract.py --handoff-dir <handoff>` to prove media exists, TTS text is nonempty and audience-facing, GUI smoke checklist proof fields exist, the manifest checklist path matches the current handoff folder, `guiProofPendingFields` is surfaced until real GUI evidence is filled, direct API/TTS/export claims are not fabricated, and source footage remains untouched. Use `scripts/prepare_jianying_gui_verification_pack.py` when the next operator needs one folder containing the handoff, GUI steps, proof fields, proof-filler command, and post-export audit shell command. After the real GUI export, run `scripts/fill_jianying_gui_proof_fields.py --apply` before the post-export smoke so checklist completion is machine-checked instead of hand-edited. Do not claim Jianying TTS, effects, or export were generated from a copied/stale handoff, or unless Jianying/CapCut was actually opened, operated, exported, GUI proof fields were completed by the filler or equivalent audited evidence, and the output was read back with ffprobe plus normal travel-video QA. Computer Use remains a fallback only for GUI-only import/TTS/export after explicit approval.

Use `scripts/audit_jianying_tts_export_readiness.py --handoff-dir <handoff>` after a Jianying/CapCut handoff is prepared, or use `scripts/run_jianying_gui_tts_export_smoke.py` as the combined state/handoff/readiness entrypoint. Run readiness again with `--export-file <mp4> --export-origin gui --output-dir <audit-dir>` after any real GUI export. This audit is the gate for Jianying's in-app TTS/export path: without an installed app it must remain warning/blocked readiness, without an audited handoff it blocks, with nonempty `guiProofPendingFields` it cannot claim GUI TTS/export completion, if checklist `proofStatus` is not `completed_gui_proof` it cannot claim GUI completion, if required proof paths such as `stateAuditJson`, `ttsScriptSource`, or `exportFile` are missing it cannot claim GUI completion, and `postExportAuditJson` must either point to a prior passed readiness audit for the same handoff/export or to the current `<audit-dir>/jianying_tts_export_readiness_audit.json` that this run will write. If `appPathMatchesStateApplication` or trusted Applications-root identity fails the app proof is not valid, if `exportFileMatchesChecklist` is false the supplied export is not bound to the GUI checklist, if `exportFileIsPreparedInput` is true the export is only source/handoff input media, if `postExportProofIdentity` is not accepted by either a prior report or `acceptedByCurrentRun` the post-export audit is not bound to this handoff/export, if `--export-origin gui` is supplied without `--export-file` it must block with `missingExportFileForGuiOrigin`, and without an ffprobe-readable GUI-origin exported file it cannot claim TTS/export delivery. The report must surface `currentAuditJsonWillBeWritten` and `currentAuditJsonMatchesChecklist` so the first real GUI export can be audited without a circular proof requirement. Never pass `--export-origin gui` for a synthetic fixture, Resolve export, arbitrary MP4, source/handoff input media, or missing export file. It never launches Jianying/CapCut, writes editor projects, queues renders, downloads assets, or modifies source footage; it only records the GUI smoke contract and the proof still required.

Use `scripts/discover_external_media.py --volume-root /Volumes` after the user plugs in a travel footage drive. It discovers likely mounted travel media roots, filters `._` AppleDouble shadow files, reports video counts/sizes/sample paths, and flags Japan/Tokyo/Osaka/Hong Kong/Macau naming cues without modifying the drive.

Use `scripts/prepare_external_media_intake.py --volume-root /Volumes` when a mounted drive contains multiple trips, when the app has multiple candidate projects, or when a project title/route may not match its media root. It writes an auditable project/media-root choice packet and prevents the workflow from silently using a mismatched default project.

Use `scripts/run_videoclaw_media_index.py` when a selected VideoClaw project has mounted `mediaRoots` but no `media_index.json`. Run it without `--apply` first to verify video counts and missing roots; add `--apply` only when writing `media_index.json`, `duplicate_groups.json`, and `scan.json` into the project directory is approved. It never modifies the source drive.

Use `scripts/run_videoclaw_route_pipeline.py` after `media_index.json` exists but route/location artifacts are missing. By default it runs local project writes only: media index refresh, frame extraction, frame index, visual scoring, local prefilter, route scaffolding attempts, and reports. It keeps real cloud location recognition disabled unless `--allow-cloud-call` is explicitly passed.

Use `scripts/run_local_ollama_vision_recognition.py` only when the user explicitly requests a local 7B/8B vision-model pass. It reads extracted frames, sends representative frames to an Ollama vision model such as `qwen2.5vl:7b`, and writes `local_vision_recognition/<timestamp>/local_ollama_vision_recognition.md` plus a local location-map candidate. By default it does not overwrite `video_location_map.json`; use `--update-project-location-map` only after reviewing the local results.

Use `scripts/run_local_tesseract_ocr.py` only as an optional helper when the user allows local OCR or when visible signs/station names need text extraction. It runs Tesseract locally with Japanese/English/Chinese language packs and writes `local_ocr_recognition/<timestamp>/local_tesseract_ocr_recognition.md` plus an OCR-only location-map candidate. OCR evidence is not enough for GPS-grade certainty, but it is useful for route review.

Use `scripts/prepare_footage_recognition_report.py` after media indexing and location recognition, before building or refreshing any delivery package. It writes `recognition_reports/<timestamp>/footage_recognition_route_report.md` and `.json`, plus `latest_footage_recognition_route_report.json`. This is a required customer-facing evidence document: it must list all source videos, recognized/unknown places, confidence, route-readiness, orientation, derived-source warnings, and next actions. If it says `blocked`, do not cut.

Use `scripts/audit_location_truth_contract.py` after the footage recognition report and before any route/location claim. It distinguishes route-aware edit readiness from verified per-video location truth: full visual/Codex coverage may be `passed_with_caveats`, but exact per-clip geolocation can only be claimed when GPS, user-confirmed, or verified cloud/per-video evidence exists. Run with `--require-verified-per-clip-location` only when the user requires GPS-grade/per-video truth; otherwise keep the caveat explicit and do not label visual reconstruction as exact.

Use `scripts/prepare_blocked_project_recovery_plan.py` whenever `prepare_footage_recognition_report.py`, `audit_location_truth_contract.py`, or the forward-test contract blocks a matched project before cutting. This writes a blocked-project recovery plan with ordered phases, exact next commands, approval gates, and safety flags so the next agent can move from "matched but unsafe" to route-ready without cutting the wrong material, modifying the source drive, calling cloud vision, writing Resolve, downloading assets, or applying route files by default. If a ready confirmed-route candidate already exists, the recovery plan must surface it in `summary.confirmedRouteCandidate`, mark route confirmation as `candidate_ready_awaiting_approval`, and keep `editingAllowedNow=false` until the route is explicitly applied and truth gates pass.

Use `scripts/prepare_codex_visual_confirmed_route.py` after Codex visual inspection has produced a stable route review markdown file such as `codex_visual_route_review.md`. It converts Codex-reviewed day/place chapters into a fresh `confirmed_route_timeline.json`, backs up the previous route file, marks the review decision as `codex_visual_confirmed`, and removes human-review blockers when all source videos are covered. This is the preferred route confirmation path for this user's workflow; do not run a local 7B/Ollama pass just to create the confirmed route unless the user explicitly asks for it. When multiple route nodes occur on the same date, the Codex visual report must provide explicit `videoNames`, `videoIds`, or `videoPaths` for each chapter so the script does not duplicate all same-day videos into every chapter. Never hard-code `country`/region from a previous project such as Japan; infer it from the project and Codex visual chapter, and keep Hong Kong/Macau, Europe, or other multi-region trips labeled honestly.

Use `scripts/audit_confirmed_route_candidate.py` after `prepare_codex_visual_confirmed_route.py` or `prepare_confirmed_route_candidate.py` writes a candidate and before any route `--apply`. It must prove the candidate is apply-ready, matches the selected project/media index, assigns every active source video exactly once, has no unknown/excluded/duplicated source references, keeps same-date multi-stop chapters explicitly mapped, and does not inherit the wrong trip country such as Japan on a Hong Kong/Macau project. A `passed_with_caveats` result may allow route-aware editing only with explicit non-GPS/visual-reconstruction wording; a `blocked` result forbids writing `confirmed_route_timeline.json`.

Use `scripts/prepare_footage_select_plan.py --project-dir <project>` after media indexing and route/location recognition, before `build_delivery_package.py`. Read `references/footage-select-engine.md`, `references/source-selection-repair-contract.md`, and `references/large-source-unattended-readiness-contract.md` first when cutting from a large unordered source folder or when the user wants the first draft closer to the Parallel World/Malta references. The script writes `footage_select_plan/footage_select_plan.json` and `.md` with one row per active source video, selection score, hero/main/texture/utility/reject tier, orientation repair risk, derived-source rejection, chapter-pool coverage, local bridge candidates, and exact decision fields. After package build, run `scripts/audit_raw_intake_completeness.py --project-dir <project> --package-dir <package>`, `scripts/prepare_source_selection_repair_plan.py --package-dir <package> --project-dir <project>`, `scripts/audit_source_selection_coverage_contract.py --package-dir <package>`, and `scripts/audit_large_source_unattended_readiness_contract.py --package-dir <package>` so the full selected source tree is indexed, every active source video is recognized, routed exactly once, scored, non-derived, fresh, chapter-covered, first-assembled by scored selection, connected to unattended first-draft/preflight, protected from source-drive writes, backed by resume checkpoints, and covered by an explicit workspace free-space budget before effects or stock fallback. `build_delivery_package.py` uses this plan when present to sort chapter media by selected local footage quality rather than raw file order. This prevents a 100GB folder from becoming a filename-order montage or a half-finished run that fills the MacBook or writes generated artifacts into the source footage root.

`build_delivery_package.py` must produce a Resolve blueprint whose `longFormCoverage.finalVideoCoverageSeconds` can sustain the requested long-form target when enough source media exists. Opening, bridge, and ending gaps should be filled with labeled visual-bed clips instead of silently leaving a 20-minute timeline under-covered.

Use `scripts/prepare_opening_story_plan.py --package-dir <package>` immediately after `build_delivery_package.py` and before trusting title, BGM, visual-establishing, edit-rhythm, creator-cut, or director-intent claims. Read `references/opening-story-engine.md` first when the user wants Parallel World/Malta quality or when the first minutes feel generic. The script writes `opening_story_plan/opening_story_plan.json` and `.md` with six required first-three-minute beats: viewer promise, destination proof, clean hero title, practical arrival, lived-in texture, and first chapter handoff. It does not write Resolve, download assets, or modify source footage.

Use `scripts/prepare_chapter_arc_plan.py --package-dir <package>` after the opening story plan and before edit-rhythm, creator-cut, transition, BGM, caption, or Resolve trust. Read `references/chapter-arc-engine.md` first for Parallel World/Malta quality. The script writes `chapter_arc_plan/chapter_arc_plan.json` and `.md` with one row per chapter covering context, movement, lived-in texture, destination payoff, and aftertaste/handoff; after rhythm/creator/source/transition audits, read `references/chapter-story-spine-contract.md`, `references/shot-flow-continuity-contract.md`, and `references/scene-flow-arc-contract.md`, then run `scripts/audit_chapter_story_spine_contract.py`, `scripts/audit_shot_flow_continuity_contract.py`, and `scripts/audit_scene_flow_arc_contract.py` so missing beats, random chapter shot order, or landmark-stack scene arcs are not hidden by effects.

Use `scripts/enrich_resolve_blueprint.py` after `delivery_plan.json`, `subtitles.srt`, voiceover audio, title cards, BGM cues, and asset search/ledger data change. It writes `resolve_timeline_enrichment.json` and updates `resolve_timeline_blueprint.json` with subtitle cues, voiceover/BGM mix plan, stock/aerial placeholders, transition cues, and Resolve timeline markers.

Use `scripts/audit_resolve_blueprint.py --blueprint <package>/resolve_timeline_blueprint.json --package-dir <package>` before any Resolve `--apply`. It writes `resolve_blueprint_preflight.json`/`.md` and verifies missing media, source ranges, source-duration bounds, same-track overlaps, V1 coverage gaps, title/place cards, subtitle sidecar, markers, BGM/stock/transition placeholders, and source-audio policy without writing Resolve.

Use `scripts/analyze_reference_video.py` for an optional local reference film:

```bash
python3 <skill-dir>/scripts/analyze_reference_video.py --reference /path/to/reference-travel-film.mp4 --output-dir <package>/reference --timeline-strip-seconds 2
```

The local reference analysis must be a reusable style profile, not only a contact sheet. It must decode scene scores across at least 95 percent of the film, suppress sustained-motion frames into spaced boundary candidates, generate ordered beginning-to-end timeline sheets, generate before/after sheets for every candidate boundary, materialize whole-film waveform/spectrogram evidence, and preserve the mandatory human review gate. Automated candidates are navigation evidence: classify each as a real cut, stylized transition, hidden cut, or fast-motion false positive and still play the opening, phase changes, audio decisions, and ending continuously. Use the confirmed observations to calibrate shot rhythm, route texture, BGM/no-voiceover support, subtitle density, and breathing room before judging an edit as Bilibili/reference-like.

Run the analyzer regression after changing reference learning:

```bash
python3 <skill-dir>/scripts/run_no_material_reference_full_timeline_smoke.py --output-dir /tmp/travel-video-studio-reference-full-timeline --overwrite --json
```

It must prove full-frame coverage, ordered timeline and boundary sheets, whole-film audio evidence, adaptive peak suppression, a valid ordered shot-length target, a passing full-timeline evidence gate, and a blocked shallow-reference trap. It cannot claim that a synthetic fixture taught the Skill final style.

Use `scripts/prepare_reference_batch_profile.py` when the user supplies multiple creator/reference videos or a reference folder, especially the four Parallel World videos plus a Malta final. Read `references/reference-batch-profile-engine.md` first. The script writes `reference/reference_batch_profile.json`, `.md`, and a compatibility `reference/reference_analysis.json`, aggregating per-video scene-cut pacing, audio loudness, sample-frame worksheet rows, and non-copying style targets for rhythm, scene grammar, opening, transitions, captions, and ending.
Use `scripts/prepare_reference_review_repair_plan.py --package-dir <package> --json` immediately after `prepare_reference_batch_profile.py` whenever the user supplies full reference videos. Read `references/reference-review-completeness-contract.md` first. This plan enforces full-film reference review evidence before learning: full timeline strip evidence, opening/title observations, chapter rhythm, transition language, ending aftertaste, BGM/audio/caption behavior, and non-copying Skill takeaways. `ready_with_reference_review_repair_plan` is a repair state, not a delivery pass; close its decision fields until it returns `ready_no_reference_review_repairs_needed` before final QA, V14, Skill maturity, or any claim that the Skill learned from the references.
When the supplied reference is a first-person departure/homeward chain through hotel, road, airport, gate, and aircraft, read `references/homeward-flight-pov-style.md`. Inherit its task-chain clarity, action anchors, transport compression, threshold shots, and state-change ending. Do not inherit its repeated `向上` effect, missing BGM, absent viewer captions, or absent clean title. The user confirmed that the reference used Jianying's free native `向上` transition; use it for about 0.34-0.42 seconds only across compatible upward travel or a motivated phase change, keep it at or below 18 percent of visual boundaries, leave at least five stable boundaries before another motion accent, and downgrade to a clean/action match or `叠化` whenever movement, BGM hit, title safety, or landing evidence is weak.
When the user provides multiple downloaded creator-reference videos, especially `叽叽歪歪的平行世界`, do not learn from a few random frames only. Review full-film timeline strips, opening strips, ending strips, scene-cut pacing, audio continuity, transition context, and any provided cover/title screenshots before writing Skill rules. Do not rely on memory or conversation context to preserve the v0.1.2 Parallel World lessons; keep them in durable references, scripts, or audits. Then read `references/parallel-world-vlog-style.md`, `references/reference-profile-application-contract.md`, `references/reference-transition-profile-contract.md`, `references/chapter-story-spine-contract.md`, `references/shot-flow-continuity-contract.md`, `references/scene-flow-arc-contract.md`, `references/final-cut-smoothness-contract.md`, `references/transition-continuity-rehearsal-contract.md`, `references/pacing-watchability-contract.md`, `references/narrative-adjacency-contract.md`, `references/transition-viewer-orientation-contract.md`, `references/transition-scene-settlement-contract.md`, `references/transition-execution-readiness-engine.md`, `references/transition-microstructure-contract.md`, `references/transition-scene-arc-contract.md`, `references/transition-effect-palette-contract.md`, `references/transition-motif-coherence-contract.md`, `references/transition-visual-match-contract.md`, `references/transition-source-coverage-contract.md`, `references/transition-choreography-engine.md`, `references/transition-choreography-contract.md`, `references/transition-motion-direction-contract.md`, `references/transition-motion-accent-contract.md`, `references/transition-effect-recipe-contract.md`, `references/transition-cutpoint-contract.md`, `references/transition-action-anchor-contract.md`, `references/transition-sensory-continuity-contract.md`, `references/transition-bridge-visual-evidence-contract.md`, `references/transition-preview-packet-engine.md`, `references/transition-preview-quality-contract.md`, `references/transition-audition-packet-engine.md`, `references/transition-audition-quality-contract.md`, `references/transition-audition-visual-proof-contract.md`, `references/transition-audition-role-integrity-contract.md`, `references/transition-storyboard-contract.md`, `references/transition-breathing-room-contract.md`, `references/reference-scene-grammar-engine.md`, and `references/timeline-variety-contract.md`, run `scripts/audit_transition_execution_readiness_contract.py`, `scripts/audit_transition_microstructure_contract.py`, `scripts/audit_transition_scene_arc_contract.py`, `scripts/audit_transition_effect_palette_contract.py`, `scripts/audit_transition_motif_coherence_contract.py`, `scripts/audit_transition_visual_match_contract.py`, `scripts/audit_transition_source_coverage_contract.py`, `scripts/prepare_transition_choreography_plan.py`, `scripts/audit_transition_choreography_contract.py`, `scripts/audit_transition_motion_direction_contract.py`, `scripts/audit_transition_motion_accent_contract.py`, `scripts/audit_transition_effect_recipe_contract.py`, `scripts/audit_transition_cutpoint_contract.py`, `scripts/audit_transition_action_anchor_contract.py`, `scripts/audit_transition_sensory_continuity_contract.py`, `scripts/audit_transition_bridge_visual_evidence_contract.py`, `scripts/prepare_transition_preview_packet.py`, `scripts/audit_transition_preview_quality_contract.py`, `scripts/prepare_transition_audition_packet.py --build-clips`, `scripts/audit_transition_audition_quality_contract.py`, `scripts/audit_transition_audition_visual_proof_contract.py`, `scripts/audit_transition_audition_role_integrity_contract.py`, `scripts/audit_transition_storyboard_contract.py`, `scripts/audit_reference_transition_profile_contract.py`, `scripts/audit_reference_scene_grammar_contract.py`, `scripts/audit_reference_profile_application_contract.py`, `scripts/audit_chapter_story_spine_contract.py`, `scripts/audit_shot_flow_continuity_contract.py`, `scripts/audit_scene_flow_arc_contract.py`, `scripts/audit_final_cut_smoothness_contract.py`, `scripts/audit_transition_continuity_rehearsal_contract.py`, `scripts/audit_pacing_watchability_contract.py`, `scripts/audit_narrative_adjacency_contract.py`, `scripts/audit_transition_viewer_orientation_contract.py`, `scripts/audit_transition_scene_settlement_contract.py`, and `scripts/audit_timeline_variety_contract.py` after pair-continuity/source/creator audits, and apply their non-copying cover/title, opening, scene-function, chapter story spine, shot-flow continuity, source-backed transition coverage, scene-flow arc, final-cut smoothness, transition-continuity rehearsal, pacing watchability, narrative adjacency, reference-profile application, reference-transition profile, timeline-variety, choreography, motion-direction, motion-accent restraint, effect-recipe parameter restraint, cutpoint timing, action-anchor proof, sensory continuity, bridge visual evidence, transition audition/storyboard, effect, audio, caption, and ending rules.

Use `scripts/generate_title_cards.py` after `delivery_plan.json` exists to create cinematic title/place card MP4 assets and inject them into the Resolve blueprint.

Use `scripts/make_city_aerial_title.py` for the opening and major city chapter hooks. It composites clean English city typography such as `TOKYO`, `OSAKA`, `PARIS`, or `LOS ANGELES` onto licensed aerial/establishing footage. Do not use a black title slate as the opening hook for a client delivery.

Use `scripts/build_asset_ledger.py` after `delivery_plan.json` exists to create the BGM/aerial/font license ledger. Final render is not allowed while BGM or stock/aerial rows remain `unverified`.

Use `scripts/prepare_asset_sourcing_packet.py` after the asset ledger exists. It writes `asset_sourcing/asset_sourcing_packet.json` and `.md` with official provider/license URLs, exact decision fields, approval evidence requirements, and next actions for BGM, aerial/stock, and font sourcing.

Use `scripts/prepare_bgm_sourcing_brief.py` after `prepare_asset_sourcing_packet.py` and before asset decisions. It writes `bgm_sourcing/bgm_sourcing_brief.json` and `.md` with a proactive long-form travel BGM search strategy: Mixkit/Pixabay-first searches, paid-library fallbacks, mood buckets by chapter, continuous-bed/opening/transition/ending section plans, decision fields, and a selection rubric. It does not download music or claim licensing; it prevents the recurring missing-BGM failure by making the exact search/selection work explicit even when no BGM has been chosen yet.

Use `scripts/prepare_bgm_selection_package.py` after the BGM sourcing brief and before transition/audio planning. It writes `bgm_selection_package/bgm_selection_package.json` and `.md`, plus `track_manifest_for_build_bed.json` when local source tracks exist. The package proves whether the selected BGM is local, license-traceable, target-duration-covering, referenced by the active Resolve blueprint, explicitly auditioned, real-music identified, non-procedural, non-tone, Content-ID checked, section-fit approved, and rebuildable with `build_bgm_bed.py`; after `prepare_bgm_phrase_blueprint.py`, read `references/bgm-musicality-contract.md` and run `scripts/audit_bgm_musicality_contract.py` so hum/tone/silence/placeholder beds cannot pass as music. It never downloads music or writes Resolve; it turns "find a suitable travel BGM" into an auditable selection/build contract.

Use `scripts/prepare_transition_bridge_plan.py` after the BGM sourcing brief and before asset/stock decisions. It writes `transition_bridge_plan/transition_bridge_plan.json` and `.md` with one boundary row per day/place/chapter transition, local-footage-first search hints, licensed stock/aerial fallback queries, BGM-only/no-camera-voice audio policy, subtitle/title-zone policy, restrained effect guidance, bridge evidence read from the Resolve blueprint, exact decision fields, and pass/reject rubric. It does not download assets or write Resolve; it prevents hard-cut day jumps, black-card transitions, and generic AI-looking route changes before the edit is built.

Use `scripts/prepare_caption_story_plan.py` after the transition bridge plan and before subtitle overlay generation. It writes `caption_story_plan/caption_story_plan.json`, `.md`, and `text_only_narration_export.txt` with full-film and per-chapter subtitle density targets, cue/gap evidence, title-zone suppression policy, no-voiceover/TXT/SRT handoff policy, caption function rows, rewrite decision fields, and pass/reject rubric. It does not generate TTS or write Resolve; it prevents the recurring sparse-subtitle and unwanted-voiceover failures by making the text-only narration/SRT plan explicit before the edit is rendered.

Final subtitles, SRT cues, TXT narration exports, and any burned-in caption text must be audience-facing travel-film text only. Never write captions that report to the user what was edited, fixed, removed, exported, rendered, QA-checked, delivered, or changed in the workflow. Do not expose terms such as `V14`, `QA`, `DaVinci`, `Resolve`, `Codex`, `skill`, `交付包`, `时间线`, `修复`, `去掉`, `本次剪辑`, `已经完成`, `SRT`, `TXT`, `A1/A2/A3`, or `BGM-only` inside final viewer-facing captions. Use `scripts/audit_audience_caption_contract.py --package-dir <package>` before subtitle overlay generation, after subtitle rewrites, and inside final QA. If it blocks, rewrite the captions as natural travel-film lines for the viewer before rendering.

After visible subtitles are required, run `scripts/prepare_subtitle_overlay_asset.py --package-dir <package> --update-blueprint`, then run `scripts/audit_subtitle_overlay_contract.py --package-dir <package>` before Resolve preflight or final QA. This contract must prove the subtitle manifest passed, dense overlay cue counts are materialized as package-local alpha video files, sampled overlay frames contain non-transparent subtitle pixels, the Resolve blueprint carries the subtitle clips on V3 with source audio disabled, and opening/chapter/ending title zones have zero subtitle-overlap unless the user explicitly allowed title-zone captions.

Use `scripts/prepare_title_typography_plan.py` before generating or trusting scenic title bridge media, then run `scripts/audit_cover_title_contract.py`, `scripts/audit_title_visual_proof_contract.py --extract-frames`, and `scripts/audit_title_bridge_contract.py --package-dir <package>` after scenic title media exists. After the final MP4 is rendered, run `scripts/audit_rendered_title_visibility_contract.py --package-dir <package>` so opening/chapter/ending title windows are proven visible over non-flat scenic/establishing background texture in the exported film, not only in source assets or Resolve blueprint rows. The plan writes `title_typography_plan/title_typography_plan.json` and `.md` with opening/chapter/ending title rows, approved title/subtitle text fields, font/license evidence, scenic background/segment evidence, title-safe rules, forbidden visible text, subtitle title-zone suppression, and stacked/ghosted-title evidence. The cover, visual-proof, title-bridge, and rendered-title audits enforce the Parallel World/Malta formula with high-recognition scenic video, oversized destination title, short designed English/place subtitle, clean 16:9 local frame proof, matching Resolve V2 title clips, final-MP4 visible title pixels, non-flat scenic background proof, and no route/date/project labels.

When title typography, title bridge, cover/title, or title visual proof blocks, run `scripts/prepare_title_typography_repair_plan.py --package-dir <package> --json` before Resolve apply, render, or handoff. `ready_with_title_typography_repair_plan` is a repair state, not a delivery pass; close its owner-script rows until it returns `ready_no_title_typography_repairs_needed`. Use this gate for ghosted/stacked titles, route/date/internal labels behind the hero title, black slate or stale `title_cards` media, title-zone subtitle collisions, missing scenic video proof, and weak cover/hero title formula.

Use `scripts/prepare_visual_establishing_plan.py` after the title typography plan and before trusting aerial/stock/title-bridge coverage. It writes `visual_establishing_plan/visual_establishing_plan.json` and `.md` with one row for the opening, every chapter establishing moment, and the ending; each row includes local-footage-first search hints, famous-place/landmark hints derived from the selected trip city, licensed stock/aerial fallback searches, BGM-only/no-camera-voice policy, title typography evidence, existing timeline evidence, exact decision fields, and pass/reject rubric. It does not download assets or write Resolve; it prevents missing city aerials, generic establishing shots, black/title-card openings, and stale previous-trip landmark defaults before the edit is built.

Use `scripts/prepare_effect_motion_plan.py` after the visual establishing plan and before Resolve effect decisions. It writes `effect_motion_plan/effect_motion_plan.json` and `.md` with restrained opening/chapter/ending title reveal rows and route-transition motion rows, tied to title typography, transition bridge, visual establishing, and blueprint `effectPlan` evidence. It records subtle fade/dissolve/match-cut/route-marker guidance plus motivated whip-pan/rotation match-cut options only when real route motion supports them; after transition/bridge candidate blueprints exist, read `references/effect-motion-blueprint-engine.md` and `references/effect-motion-application-contract.md`, run `scripts/prepare_effect_motion_blueprint.py`, then run `scripts/audit_effect_motion_application_contract.py` after final blueprint lineage so effects become applied candidate metadata instead of prose-only suggestions.

Use `scripts/prepare_feedback_regression_plan.py` after effect motion planning and before audio scene policy. It writes `feedback_regression_plan/feedback_regression_plan.json` and `.md` with reusable probes for concrete rejected draft failures such as `opening_title=0`, `reported_vertical_clip=7:04`, `reported_voice_at_7_04=7:04`, and `opening_bgm_no_voice=0`. The plan produces the exact `--feedback-timestamps` strings for `prepare_audio_scene_policy_plan.py`, `audit_feedback_regressions.py`, and `run_final_qa_suite.py`. It does not write Resolve, queue renders, download assets, or touch source media; it makes the user's complaint set machine-readable before the next edit.

Use `scripts/prepare_audio_scene_policy_plan.py` after the feedback regression plan and before asset decisions or Resolve writes. It writes `audio_scene_policy_plan/audio_scene_policy_plan.json` and `.md` with opening, title, visual-establishing, transition, effect, and feedback-timestamp audio windows; every row must be A3 BGM-led, `bgm_only_no_camera_voice`, and free of A1/A2 source-camera or voiceover leakage unless an explicit ambient exception is approved. It also consumes `feedback_regression_plan.json` and keeps known user feedback probes such as `7:04` scenic/voice complaints as reusable regression rows. It does not download assets or write Resolve; it prevents missing-BGM and accidental user/source-voice failures before the timeline is built.

Use `scripts/prepare_edit_rhythm_plan.py` after the footage select plan, opening story plan, audio scene policy plan, and package build, and before asset decisions or Resolve writes. It writes `edit_rhythm_plan/edit_rhythm_plan.json` and `.md` with one row per primary visual shot, one row per chapter, Malta/reference pacing targets, rhythm-role categories, long-shot/cutaway risks, recommended trim/split/cutaway treatments, exact Resolve/readback decision fields, and pass/reject rubric. It does not write Resolve; it prevents bare concatenation and AI-looking flat pacing by forcing every selected shot to have a route, street, lived-in, landmark, scenic, title, transition, or ending function before the cut is trusted.

Use `scripts/prepare_creator_cut_plan.py` after the edit rhythm plan and before rhythm recut or Resolve writes when the user wants the cut closer to the four Parallel World videos, the Malta final, or creator-quality long-form travel. Read `references/creator-cut-engine.md` first, then read `references/creator-cut-application-contract.md` and `references/final-source-usage-contract.md` before auditing final candidates. The script writes `creator_cut_plan/creator_cut_plan.json` and `.md` with one creator-function row per visual clip, hero/main/texture/utility/reject tiers, explicit weak-clip rejection or demotion, chapter coverage rows, and motivated transition recipes including whip-pan/rotation only when movement evidence supports them. Run `scripts/audit_final_source_usage_contract.py` and `scripts/audit_creator_cut_application_contract.py` after transition-polish/rhythm candidates so unmatched raw sources, reject/repair clips, utility-dominant source choices, and weak creator-cut rows cannot remain active in the final candidate blueprint. It does not write Resolve; it prevents the Skill from keeping every usable clip and calling that a creator edit.

Use `scripts/prepare_transition_grammar_plan.py` after the creator cut plan and before rhythm recut or Resolve writes when transitions need to feel closer to the Parallel World/Malta references. Read `references/transition-grammar-engine.md` first. The script writes `transition_grammar_plan/transition_grammar_plan.json` and `.md` with one row per adjacent visual pair, recommended transition type, fallback transition type, bridge evidence, motion evidence, title/caption safety, BGM phrase cue fields, and exact Resolve/readback decision fields. It only allows whip-pan, rotation, and speed-ramp transitions when physical route motion supports them; otherwise it recommends match cuts, short dissolves, straight cuts, or `insert_bridge_first`. Do not treat field presence as approval: every row must carry a concrete non-generic pre-Resolve decision, BGM cue, preview requirement, frame/sample evidence, and title/motion safety evidence before the plan is trusted.

Use `scripts/prepare_transition_execution_plan.py` after the transition grammar plan and before rhythm recut, Resolve blueprint updates, or Resolve writes when transitions must become executable rather than advisory. Read `references/transition-execution-engine.md` first, then run `scripts/prepare_transition_reference_candidates.py`, `scripts/prepare_transition_reference_selection.py`, `scripts/prepare_transition_motif_plan.py`, `scripts/prepare_bridge_sequence_plan.py`, `scripts/prepare_bridge_sequence_blueprint.py`, `scripts/prepare_transition_choreography_plan.py`, and `scripts/prepare_transition_execution_blueprint.py`; read `references/transition-reference-candidate-engine.md`, `references/transition-reference-selection-engine.md`, `references/transition-motif-engine.md`, `references/bridge-sequence-engine.md`, `references/bridge-sequence-blueprint-engine.md`, `references/transition-choreography-engine.md`, and `references/transition-execution-blueprint-engine.md` so repeated dissolves, random motion, missing BGM cues, effect-hidden route jumps, and single-effect transitions become reference-calibrated A/B/C candidates, unattended-safe default selections with boundary-specific from/to reasons plus preview/audition/execution/readiness proof plans, Resolve marker/clip metadata carrying the selected candidate plus `transitionMotionExecution`, `transitionCutpointPlan`, `transitionActionAnchorPlan`, and `transitionSensoryContinuityPlan`, and Resolve-ready bridge clips with repair owners. After BGM phrase and rhythm recut candidates exist, run `scripts/prepare_transition_polish_blueprint.py`, `scripts/audit_transition_quality_contract.py`, `scripts/audit_shot_transition_boundary_contract.py`, `scripts/audit_transition_motivation_contract.py`, `scripts/audit_transition_pair_continuity_contract.py`, `scripts/audit_transition_execution_readiness_contract.py`, `scripts/audit_transition_polish_application_contract.py`, `scripts/audit_resolve_transition_materialization_contract.py`, `scripts/prepare_resolve_transition_apply_plan.py`, `scripts/audit_resolve_transition_apply_contract.py`, `scripts/audit_bridge_sequence_application_contract.py`, `scripts/audit_transition_bridge_visual_evidence_contract.py`, `scripts/audit_final_blueprint_lineage_contract.py`, `scripts/audit_effect_motion_application_contract.py`, `scripts/audit_transition_cadence_contract.py`, `scripts/audit_transition_microstructure_contract.py`, `scripts/audit_transition_scene_arc_contract.py`, `scripts/audit_transition_effect_palette_contract.py`, `scripts/audit_transition_motif_coherence_contract.py`, `scripts/audit_transition_visual_match_contract.py`, `scripts/audit_transition_source_coverage_contract.py`, `scripts/prepare_transition_choreography_plan.py`, `scripts/audit_transition_choreography_contract.py`, `scripts/audit_transition_motion_direction_contract.py`, `scripts/audit_transition_motion_accent_contract.py`, `scripts/audit_transition_cutpoint_contract.py`, `scripts/audit_transition_action_anchor_contract.py`, `scripts/audit_transition_sensory_continuity_contract.py`, `scripts/prepare_transition_preview_packet.py`, `scripts/audit_transition_preview_quality_contract.py`, `scripts/prepare_transition_audition_packet.py --build-clips`, `scripts/audit_transition_audition_quality_contract.py`, `scripts/audit_transition_audition_visual_proof_contract.py`, `scripts/audit_transition_audition_role_integrity_contract.py`, `scripts/audit_transition_storyboard_contract.py`, `scripts/audit_reference_transition_profile_contract.py`, `scripts/audit_scene_flow_arc_contract.py`, `scripts/audit_final_cut_smoothness_contract.py`, `scripts/audit_transition_continuity_rehearsal_contract.py`, `scripts/audit_narrative_adjacency_contract.py`, `scripts/audit_transition_viewer_orientation_contract.py`, `scripts/audit_transition_scene_settlement_contract.py`, and `scripts/audit_timeline_variety_contract.py`, then read `references/transition-polish-blueprint-engine.md`, `references/transition-choreography-engine.md`, `references/transition-choreography-contract.md`, `references/transition-motion-direction-contract.md`, `references/transition-motion-accent-contract.md`, `references/transition-cutpoint-contract.md`, `references/transition-action-anchor-contract.md`, `references/transition-sensory-continuity-contract.md`, `references/reference-transition-profile-contract.md`, `references/scene-flow-arc-contract.md`, `references/final-cut-smoothness-contract.md`, `references/transition-continuity-rehearsal-contract.md`, `references/narrative-adjacency-contract.md`, `references/transition-viewer-orientation-contract.md`, `references/transition-scene-settlement-contract.md`, `references/transition-execution-readiness-engine.md`, `references/transition-polish-application-contract.md`, `references/resolve-transition-materialization-contract.md`, `references/resolve-transition-apply-contract.md`, `references/bridge-sequence-application-contract.md`, `references/transition-bridge-visual-evidence-contract.md`, `references/final-blueprint-lineage-contract.md`, `references/effect-motion-application-contract.md`, `references/transition-cadence-contract.md`, `references/transition-microstructure-contract.md`, `references/transition-scene-arc-contract.md`, `references/transition-effect-palette-contract.md`, `references/transition-motif-coherence-contract.md`, `references/transition-visual-match-contract.md`, `references/transition-source-coverage-contract.md`, `references/transition-preview-packet-engine.md`, `references/transition-preview-quality-contract.md`, `references/transition-audition-packet-engine.md`, `references/transition-audition-quality-contract.md`, `references/transition-audition-visual-proof-contract.md`, `references/transition-audition-role-integrity-contract.md`, `references/transition-storyboard-contract.md`, and `references/timeline-variety-contract.md` so every final transition carries BGM-hit timing, title/subtitle avoidance, sensory-continuity proof, motion-evidence, motion-accent restraint, source-level outgoing/bridge/landing coverage, and direction-match proof, cutpoint leave/hit/landing timing, readable action-anchor proof, restrained Resolve keyframes, three-beat outgoing/bridge-or-motion/landing choreography, reference-profile bridge/breath/match/motion balance, per-boundary from/to coverage, pair-continuity evidence, package-local Resolve recipe/handle readiness, shot-to-shot landing/handle/BGM-only/title-safe microstructure, outgoing/bridge-or-motion/BGM-hit/title-safe/landing scene-arc proof, whole-film effect-palette and motif-coherence balance, pair-level visual-match proof, concrete bridge video probe/frame evidence, generated nonblank preview evidence, muted watchable MP4 audition plus frame-delta and role-integrity proof, viewer-purpose/outgoing/bridge/landing storyboard, row-to-row transition-continuity rehearsal, Resolve marker/readback payload survival, API/manual/bridge apply-path proof, final-blueprint polish survival, final-candidate bridge-beat survival, final-blueprint candidate-chain lineage, effect-motion application proof, whole-film cadence, scene-flow arc proof, final-cut smoothness proof, narrative adjacency proof, viewer-orientation and scene-settlement proof, and route/bridge/motion/title/BGM motivation while the full timeline still varies movement, lived-in texture, payoff, and aftertaste instead of generic hard cuts or random rotations. In unattended/default delivery, `prepare_transition_reference_selection.py` must return zero decision issues before Resolve apply, and `prepare_resolve_transition_apply_plan.py` plus `audit_resolve_transition_apply_contract.py` must block pending manual visible effects; a planned Resolve/Fusion instruction is not proof of application unless the row has completed Resolve readback plus frame-sample evidence, or the effect is replaced by materialized bridge clips.

When `scripts/audit_transition_motion_accent_contract.py` blocks on random rotation, whip, push, slide, zoom, speed-ramp, overuse, weak direction, missing BGM hit, title/subtitle risk, or unstable landing, run `scripts/prepare_transition_motion_accent_repair_plan.py --package-dir <package> --json` before another Resolve write. Its `ready_with_transition_motion_accent_repair_plan` status is a repair state, not a delivery pass; run each owner script in its repair rows and rerun final QA until the plan returns `ready_no_motion_accent_repairs_needed`.

When transition cadence, microstructure, scene arc, effect palette, motif coherence, visual match, source coverage, choreography, cutpoint, action-anchor, sensory-continuity, preview/audition, breathing-room, final-cut smoothness, pacing, narrative adjacency, viewer orientation, or scene settlement blocks, run `scripts/prepare_transition_flow_repair_plan.py --package-dir <package> --json` before Resolve apply, render, or handoff. `ready_with_transition_flow_repair_plan` is a repair state, not a delivery pass; close its owner-script rows until it returns `ready_no_transition_flow_repairs_needed`. Use this gate for weak adjacent-shot flow, random hard cuts, template-effect cadence, missing bridge/landing footage, marker-only visible effects, unpreviewed transitions, unstable landings, and route/story jumps that still feel unlike the Parallel World/Malta references.

Use `scripts/prepare_rhythm_recut_blueprint.py` after the BGM phrase candidate exists and before asset decisions or Resolve writes. It writes `rhythm_recut_blueprint/resolve_timeline_blueprint_rhythm_recut.json` plus JSON/MD reports that convert long-shot diagnosis into a non-destructive Resolve blueprint candidate while preserving transition/effect/BGM phrase metadata: long raw holds are split into shorter main segments with existing-footage cutaways, total timeline duration is preserved, A1/A2/source audio stays disabled for inserted video, and the original `resolve_timeline_blueprint.json` is not modified unless `--update-blueprint` is explicitly requested. Read `references/rhythm-recut-application-contract.md`, run `scripts/audit_rhythm_recut_application_contract.py` after transition polish/final lineage, and always preflight final candidates with `audit_resolve_blueprint.py --blueprint <candidate> --package-dir <package>` before any Resolve apply.

Use `scripts/prepare_rhythm_recut_apply_package.py` after the rhythm-recut candidate is reviewed and before any Resolve write. It forks a new package, copies only reusable input/assets/plans instead of stale final render proof, rewrites package-internal paths, makes the candidate blueprint the new package's active `resolve_timeline_blueprint.json`, runs optional preflight, and writes `rhythm_recut_apply_package_report.json`/`.md`. This is the safe bridge from "candidate looks good" to "new Resolve-ready package"; do not manually overwrite the source package blueprint unless the user explicitly asks for an in-place update.

Use `scripts/prepare_reference_style_repair_plan.py` after rhythm recut planning, reference-style audits, director-intent audits, director-polish audits, or final QA when the cut still feels unlike the Parallel World/Malta references. Read `references/reference-style-repair-engine.md` first. The script writes `reference_style_repair_plan/reference_style_repair_plan.json` and `.md` with one repair row per blocked style/director/QA gap: owner script, required artifact, repair action, acceptance evidence, reference rule, safety flags, and Resolve/readback/render-frame decision fields. Then run `scripts/audit_reference_repair_closure.py` so P0 style rows cannot be treated as fixed until required artifacts, post-repair audits, and readback/frame evidence close them. These scripts convert vague "make it better" feedback into a repair queue and closure gate without writing Resolve, rendering, downloading assets, or modifying source footage; after closure/preflight, read `references/transition-sequence-satisfaction-contract.md`, `references/final-viewer-friction-contract.md`, `references/first-draft-satisfaction-contract.md`, `references/whole-film-satisfaction-contract.md`, and `references/unattended-repair-queue-engine.md`, then run `scripts/audit_transition_sequence_satisfaction_contract.py`, `scripts/audit_final_viewer_friction_contract.py`, `scripts/audit_first_draft_satisfaction_contract.py`, `scripts/prepare_unattended_repair_queue.py`, and `scripts/audit_whole_film_satisfaction_contract.py` so transition-sequence, viewer-facing, `blocked_first_draft_satisfaction`, `blocked_whole_film_satisfaction`, and remaining QA blockers have owner scripts, resolved commands, execution order, required artifacts, acceptance evidence, post-repair commands, and forbidden-workaround rules. If whole-film satisfaction blocks, rerun the unattended queue so its embedded repair rows become executable. The unattended repair queue must also route `resolve_transition_apply_contract_audit.json` blockers: pending manual visible effects are not acceptable repairs until they become API-supported cuts, materialized bridge clips, or completed Resolve readback plus frame-sample evidence. When `final_qa_suite_report.json` exists, the repair queue must ingest blocked final-QA stages and route each untracked BGM, caption, title, reference-style, source, transition, render, or package-integrity failure to the concrete owner preparation script instead of leaving the next agent to infer repairs from final QA alone. Queue rows with unresolved placeholders such as `<project-dir>` or `<final-mp4>` are not unattended-ready.

Use `scripts/build_route_coverage_scaffold.py` when `route_timeline.json` covers too little media. It builds a full-media route scaffold from ordered media plus chapter/map filename cues, writes `route_coverage_scaffold.json`, `.md`, `contact_sheet.jpg`, and `latest_route_coverage_scaffold.json`, and marks every scaffold chapter as needing human review.

Use `scripts/prepare_route_review.py` whenever route chapters need human review, the project title/route conflicts with recognized media, or `confirmed_route_timeline.json` is stale. It writes `route_review.json`, `route_review.md`, `contact_sheet.jpg`, and `latest_route_review.json`.

Use `scripts/prepare_route_decision_sheet.py` after a route review packet exists. It writes `route_decision_sheet.json`/`.md` with suggested per-chapter decisions and a region-mismatch approval block. It never applies decisions or writes `confirmed_route_timeline.json`.

Use `scripts/apply_route_decision_sheet.py` after `route_decision_sheet.json` has been reviewed and approved. By default it writes `route_decision_application.json`/`.md` only. Use `--apply` only after the user explicitly approves writing decisions back into `route_review.json`; it still never writes `confirmed_route_timeline.json`.

Use `scripts/prepare_confirmed_route_candidate.py` after route review decisions are made. It writes a gated `confirmed_route_candidate.json`/`.md` and only writes `confirmed_route_timeline.json` with `--apply` when all route gates pass and the user explicitly approves.

Use `scripts/apply_asset_sourcing_decisions.py` after exact BGM/stock/aerial/font choices are filled in `asset_sourcing_packet.json`. By default it writes `asset_decision_reconciliation.json`/`.md` only. Use `--apply` only after every final asset row has exact asset, license, approval, and local/URL evidence.

Use `scripts/audit_unattended_first_draft_contract.py` after audience captions, BGM/audio policy, title/cover, rhythm/creator-cut, transition motivation, pair-continuity, execution-readiness, transition-microstructure, transition-scene-arc, transition-effect-palette, transition-motif-coherence, transition-visual-match, transition-choreography, transition-motion-direction, transition-motion-accent, transition-cutpoint, transition-action-anchor, transition-bridge-visual-evidence, transition-preview-packet, transition-preview-quality, transition-audition-packet, transition-audition-quality, transition-audition-visual-proof, transition-audition-role-integrity, transition-storyboard, transition-breathing-room, scene-flow-arc, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, transition-sequence-satisfaction, reference-transition-profile, reference scene-grammar, timeline-variety, reference-repair closure, final-viewer-friction, first-draft-satisfaction, whole-film-satisfaction, unattended repair queue, and Resolve blueprint preflight exist; then use `scripts/audit_delivery_package.py` before claiming the package is ready. The first audit proves the safe first-draft chain is connected before Resolve apply and that blockers are routed to executable repairs, while the delivery audit writes `delivery_audit.json` and `delivery_audit.md` with blockers and next actions.

Use `scripts/prepare_resolve_apply_contract.py` after the Resolve blueprint and delivery audit exist. It writes `resolve_apply_contract.json`/`.md` with project/timeline name, tracks, source counts, clip counts, write/readback commands, current blockers, and approval fields. It never writes Resolve.

Use `scripts/prepare_resolve_render.py` after the Resolve timeline is written and read back. It writes `render_plan.json` by default without changing Resolve and must include a `VideoQuality` high-bitrate target, normally numeric `80000` or higher for 4K long-form masters. `--queue` and `--start` require explicit user approval plus a clean delivery audit and `resolve_audit.json`.

Use `scripts/verify_render_delivery.py` after any Resolve or FFmpeg final render before claiming delivery. It verifies the final MP4 with `ffprobe`, full-film `blackdetect`, sampled frame extraction/luma checks, audio/video stream checks, and subtitle evidence. Then read `references/rendered-transition-proof-contract.md` and run `scripts/audit_rendered_transition_proof_contract.py` so actual rendered transition windows cannot hide black flashes, white flashes, raw pillarboxed vertical footage, or unstable landings. A render that exists but fails either verification is not deliverable.

Use `scripts/audit_longform_delivery.py` after `verify_render_delivery.py` passes. It writes `longform_delivery_audit.json`/`.md` and checks the whole 20-minute-film promise: final MP4, duration, 4K video, audio, black-frame scan, DaVinci readback, voiceover, subtitles, BGM, aerial/stock evidence, title cards, transitions, route-recognition artifacts, route honesty, and handoff documents. `passed_with_caveats` is acceptable for a rough travel film when the caveat is explicitly about non-GPS/per-clip route certainty; it is not acceptable if the user requires verified per-clip locations.

Use `scripts/audit_client_delivery_rules.py` before claiming a film is usable for a customer. It blocks if recognition did not cover the whole folder, the confirmed route is a single scaffold chapter, derived exports are mixed into raw footage, portrait/rotated media lacks a normalization policy, the actual Resolve blueprint source paths contain any raw portrait/square/unknown video clip in the 16:9 master, the opening does not start with city aerial/establishing footage plus clean city title typography, title text exposes internal IDs or placeholder Chinese, opening/chapter/ending title moments are black slates instead of scenic video bridges, SRT is missing/sparse, BGM is not on A3, transitions are not represented by visual bridge clips, effects are not planned, licenses are unverified, the final render is not valid 4K high-frame-rate/high-bitrate, or render verification has not passed.

When a draft has already rendered but its first frame, chapter cards, or ending feel like generic AI output, create a `visual_polish` or `v8_visual_polish` package before re-verification. This package must include a manifest with route-aware opening, chapter, and ending replacement segments. Each segment must use real approved video footage or licensed stock/aerial footage as its background, not PNG/JPG title cards, `title_cards` black slates, random project IDs, generic `JAPAN` labels, phone/hand-obstructed frames, or placeholder Chinese.

Do not trust a visual-polish manifest by itself. The final Resolve blueprint must actually reference the scenic title/bridge clips on V2. `audit_client_delivery_rules.py` must inspect the blueprint source paths and block if any opening/chapter/ending title moment still points to `title_cards/*.mp4`, PNG/JPG slates, missing media, or long place-description text that can crop at 4K. Use a role such as `chapter_title_bridge` for scenic chapter title clips that replace old `place_card` slates.

Use `scripts/prepare_quality_recut.py` when a draft looks too AI-made, too low frame-rate, too sparse, or too narration-heavy. It prepares a v4-style package with 59.94fps defaults, no rendered voiceover audio, text-only narration export, dense full-film captions, BGM kept as a required audible asset, and opening/ending aerial inserts. After rendering such a package, run `verify_render_delivery.py` with `--min-fps 50 --min-video-bitrate-mbps 60`.

Use `scripts/prepare_scenic_title_bridges.py` whenever opening/chapter/ending title moments contain black slates, stale `title_cards`, full-route labels, generic date labels, subtitles over the hero title, or template-looking lower-corner route text. It regenerates scenic title bridge videos from approved aerial/establishing/travel footage, draws only a clean main title plus optional short day/place subtitle, writes a contact sheet, and can update the Resolve blueprint. The default title policy forbids global route labels such as `TOKYO / OSAKA`, `JAPAN 2025`, `OSAKA - TOKYO - OSAKA`, or `OSAKA -> TOKYO -> OSAKA` inside final title bridge media.

Use `scripts/audit_feedback_regressions.py` after any concrete user complaint about a rendered draft. Pass the exact timestamps from the user, for example `--feedback-timestamps opening_title=0,reported_vertical_clip=7:04 --include-title-points`. It turns the complaint into a reusable regression gate by checking the final Resolve render, clean title policy, sampled frames, portrait/pillarbox metrics, BGM audibility, A1/A2/A3 Resolve readback, no source-camera/voiceover leakage in scenic sections, dense V3 subtitle overlays, and title-zone subtitle suppression. Do not close a feedback loop until this audit passes or the remaining blockers are written as explicit next actions.

Use `scripts/audit_reference_style_alignment.py` after `audit_story_style_contract.py` when the user wants the Skill to approach Bilibili/Malta-style long-form travel quality rather than merely pass technical checks. It scores reference material, long-form duration, route chapters, transport connective tissue, street/lived-in/landmark balance, real-footage variety, scenic title/bridge structure, no-voiceover BGM/caption support, and upstream QA evidence. Treat it as the "does this still feel like a travel film instead of an AI assembly" gate.

Use `scripts/audit_director_intent_contract.py` after reference-style alignment and before director-polish claims. It writes `director_intent_manifest.json` plus `director_intent_contract_audit.json`/`.md`, proving the cut has an explicit director intent: opening mission and city signal, chapter beat categories, arrival-to-return route arc, long-form shot pacing, caption-led story/honesty, BGM/no-voiceover support, and an ending with scenic aftertaste. This is the reusable guard against technically valid but emotionally flat AI assemblies.

Use `scripts/audit_route_texture_contract.py` after reference-style alignment and before title/package-integrity handoff. It verifies that route transitions are backed by actual bridge clips on the timeline, chapter title moments have nearby route connective tissue, every chapter has lived-in texture beyond title cards, and the global cut balances movement, street life, daily detail, and landmark payoff. This is the deterministic guard against landmark-only montages, hard-cut day jumps, or AI-looking travel assemblies that technically render but do not feel traveled.

Use `scripts/audit_director_polish_contract.py` after title, BGM, route-texture, and reference-style audits. It cross-checks the director-level delivery promise: verified aerial/establishing opening, clean typography and font evidence, travel-appropriate BGM mood/licensing, restrained title/transition effects, dense rendered subtitles, Resolve track readback, and 4K high-frame-rate/high-bitrate output. Treat `passed_with_warnings` as acceptable only when the warnings are explicit handoff risks such as optional stock/aerial search placeholders that have not been materialized; do not hide those warnings.

Use `scripts/audit_stock_aerial_closure.py` after route-texture and title audits, and before director polish. It verifies that every stock/aerial search placeholder in `stockInsertPlan` is either materialized as a verified local asset or explicitly closed as not used in the final Resolve render and covered by real local route/title footage. Run with `--update-blueprint` when you want `resolve_timeline_blueprint.json` to record the closure policy. Do not fabricate that a stock clip was downloaded; unresolved placeholders must remain blockers.

Use `scripts/audit_package_integrity.py` before any handoff claim, especially after copying or deriving a package from an older package. It verifies that final render evidence points at the current package, Resolve readback identity matches the current blueprint, core QA reports have acceptable statuses, and stale/cross-package paths are visible. A historical cross-package voiceover marker may be closed only when Resolve readback has zero A1/A2 items, A3 BGM exists, and BGM/story contracts prove BGM-only no-voiceover delivery. Run `--strict-portable` before giving the package to another editor, another AI, or a client; strict mode blocks when active core package evidence still depends on previous delivery package paths.

Use `scripts/audit_title_bridge_contract.py` after scenic title bridges are generated and again after the final Resolve render, then run `scripts/audit_title_visual_proof_contract.py --package-dir <package> --extract-frames` so the clean title claim has actual local probe/frame evidence. These verify that the clean title-bridge manifest, segment files, overlay files, Resolve V2 title clips, single-city opening title, forbidden visible text, no stacked text or subtitle overlay layers inside title windows, video-only scenic source policy, subtitle title-zone suppression, and three-frame 16:9 visual proof all agree. This is the deterministic guard for the user's repeated opening-title complaint; OCR is useful evidence, but the title contracts are the stronger structural proof.

Use `scripts/audit_bgm_audio_contract.py` after BGM is selected/built and again after the final Resolve render, then run `scripts/audit_bgm_musicality_contract.py` before Resolve apply/final QA. After the final MP4 exists, read `references/final-bgm-mix-contract.md` and run `scripts/audit_final_bgm_mix_contract.py --package-dir <package>` before story/style/V14/maturity claims. The audio contract verifies that the BGM manifest output, Resolve blueprint `assets.bgm`, A3 cue, current-package materialized audio bed, asset ledger BGM row, DaVinci A1/A2/A3 readback, visual/audio loudness, feedback timestamp audio windows, no-camera/no-voiceover policy, and no A1/A2 voice or source-audio clips overlapping scenic/title/transition windows all agree; the musicality contract rejects sine/hum/tone/silence/placeholder beds, one-band audio, flat dynamics, missing phrase sections, or unnamed/untraceable music; the final mix contract samples the exported MP4 so title, scenic bridge, transition, and ending windows cannot pass with missing, quiet, or hum-like BGM. This is the deterministic guard for the user's repeated BGM complaint: scenic openings, title moments, and transition/landscape sections must be BGM-led and must not leak source-camera/user voice.

Use `scripts/audit_skill_maturity_contract.py` after package-integrity QA when judging whether the reusable Skill, not just one film, covers the user's repeated delivery failures. It checks Skill instructions, bundled scripts, Bilibili/Malta style anchors, render quality, rendered transition proof, feedback regressions, clean non-duplicated opening title plus actual title visual proof and title repair planning, proactive raw-footage selection, first-assembly source-order proof via `audit_first_assembly_source_order_contract.py` and `first-assembly-source-order-contract.md`, large-source unattended readiness via `audit_large_source_unattended_readiness_contract.py` and `large-source-unattended-readiness-contract.md`, opening story planning, proactive BGM, BGM musicality, final rendered BGM mix, transition-bridge, caption-story, title-typography, visual-establishing, effect-motion, audio-scene-policy, edit-rhythm planning, creator-cut shot selection/application, final-source usage, timeline-variety, transition-grammar pair decisions, transition cadence, transition microstructure, transition scene-arc, transition effect-palette, transition motif-coherence, transition visual-match, transition-flow repair planning, transition-effect recipe, transition-breathing-room, scene-flow-arc, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, reference-transition-profile, transition bridge visual evidence, transition preview-quality, transition pair-continuity, transition execution-readiness, transition-polish application, Resolve transition materialization/apply-path proof, bridge-sequence application, final-blueprint lineage, reference scene-grammar, reference-profile application, rhythm-recut candidate blueprints, rhythm-recut apply package forks, `audit_unattended_first_draft_contract.py`, `audit_first_draft_satisfaction_contract.py`, `audit_whole_film_satisfaction_contract.py`, BGM/no-voiceover, recognition/route evidence, director intent, route texture, stock/aerial closure, director polish, and strict portable handoff. Treat it as one-package evidence; it does not prove the long-term Skill goal complete without more forward tests on other trips.

Use `scripts/audit_trip_generalization_contract.py` after adding or changing any rescue/repair script that was born from a specific trip failure. It blocks if reusable package, style-fix, orientation-repair, quality-recut, or route-decision scripts still force previous-trip defaults such as TOKYO/Japan/Tokyo-to-Osaka instead of deriving titles, countries, Resolve names, BGM mood, and route labels from the selected project or explicit arguments. Passing it does not prove the film is good; it proves the Skill will not silently contaminate a Hong Kong/Macau, Europe, or future trip with stale Japan-specific rescue logic.

Use `scripts/audit_v012_baseline_regression.py --skill-dir <skill-dir>` after substantial Skill edits and before publishing a release. It blocks if the original v0.1.2 lessons regress: Parallel World references must still require full-film review rather than random frames, cover/hero titles must still use the high-recognition scenic background plus oversized destination title formula, the main workflow must still load `parallel-world-vlog-style.md`, title typography and cover contracts must still guard the opening/title style, Skill maturity must still preserve the cover/opening/transition/ending lessons, and private local download/desktop/temp-frame paths from the reference-learning run must not leak into the portable Skill.

Use `scripts/run_skill_release_audit.py --skill-dir <skill-dir>` before publishing a release or handing the Skill to another agent. It is a portable, no-network, no-Resolve-write release gate that checks SKILL.md trigger metadata, required release-gate files including `create_skill_benchmark_fixture.py`, `audit_editor_integration_contract.py`, `audit_resolve_writeability_state.py`, `audit_jianying_capcut_state.py`, `prepare_jianying_handoff_package.py`, `audit_jianying_handoff_contract.py`, `audit_jianying_tts_export_readiness.py`, `run_no_material_editor_smoke.py`, `run_no_material_music_pacing_smoke.py`, `run_no_material_bgm_musicality_smoke.py`, `run_no_material_rendered_watchdown_smoke.py`, `run_no_material_final_render_quality_bundle_smoke.py`, `run_no_material_whole_film_satisfaction_smoke.py`, `run_no_material_one_shot_autonomy_smoke.py`, `run_no_material_forward_test_smoke.py`, `run_no_material_capcut_draft_automation_smoke.py`, `run_resolve_live_write_smoke.py`, `run_resolve_delivery_structure_smoke.py`, `run_resolve_render_readiness_smoke.py`, and `run_editor_delivery_matrix.py`, release-audit wiring, Python compilation, the v0.1.2 baseline audit, and trip-generalization. If it blocks, fix the missing Skill file, integration token, compile error, v0.1.2 regression, or trip-specific default before tagging or publishing.

Use `scripts/audit_skill_forward_test_contract.py` after substantial Skill revisions or before claiming the Skill is mature across trips. It consumes an external media intake packet, a known-good package, a separate blocked project/location-truth report, and that blocked project's recovery plan to prove the Skill can both deliver a ready trip, refuse unsafe/mismatched trip states, and hand the next agent an actionable recovery route. The known-good package must pass both its full final QA suite and the current client delivery audit, including the latest actual-blueprint source-orientation gate; do not trust a stale final QA report generated before a new regression gate existed. A credible run should look like `audit_skill_forward_test_contract.py --intake-json <external_media_intake.json> --ready-package-dir <passed-package> --blocked-project-dir <separate-trip-project> --blocked-location-truth-json <blocked-location-truth.json> --blocked-recovery-plan-json <blocked_project_recovery_plan.json> --output-dir <skill-upgrade>/qa/<forward-test-run>`. Passing it is stronger than one-package QA, but still not a universal completion proof.

Use `scripts/run_final_qa_suite.py` as the final handoff gate after a Resolve render exists. It infers the final MP4, visual title-bridge manifest, and BGM manifest when possible, then runs or verifies render delivery, visual/audio style, BGM/audio and BGM-musicality contracts, location truth contract, client rules, long-form delivery, story style, reference alignment, director intent contract, route texture contract, title bridge/cover/title-visual-proof/title-repair contracts, stock/aerial closure, director polish contract, feedback regression, default package integrity, strict portable package integrity, transition pair-continuity, transition execution-readiness, transition-polish application, Resolve transition materialization/apply contract, bridge-sequence application, transition bridge visual evidence, source-selection coverage, first-assembly source-order, large-source unattended-readiness, final-blueprint lineage, transition cadence, transition microstructure, transition scene-arc, transition effect-palette, transition motif-coherence, transition visual-match, transition motion-direction, transition-flow repair, transition reference-readiness, transition-sequence-satisfaction, transition effect-recipe, rendered transition proof, transition preview-quality, transition audition quality/visual/role proof, transition-breathing-room, scene-flow-arc, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, final-source usage, creator-cut application, reference scene-grammar, reference-review repair, reference-profile application, reference-transition-profile, timeline-variety, first-draft-satisfaction, whole-film-satisfaction, unattended-first-draft contract, and Skill maturity contract in one reproducible report. Final QA must require `title_typography_repair_plan` to be `ready_no_title_typography_repairs_needed`, `reference_review_repair_plan` to be `ready_no_reference_review_repairs_needed`, `transition_flow_repair_plan` to be `ready_no_transition_flow_repairs_needed`, `transition_sequence_satisfaction_contract_audit` to be `passed`, `first_draft_satisfaction_contract_audit` to be `passed`, `whole_film_satisfaction_contract_audit` to be `passed`, and `unattended_repair_queue` to be `ready_no_unattended_repairs_needed`; repair-plan statuses with rows are actionable repair states, not handoff passes. Do not claim the Skill or a package is ready for another AI, editor, or client unless `final_qa_suite_report.json` is `passed` with zero remaining repair rows, or the remaining blockers are explicitly listed as next actions.

Use `scripts/audit_v14_baseline_contract.py` as the reusable "first draft should already feel like V14" gate. It proves the Skill has internalized the successful V14 lessons rather than only storing a historical edit: DaVinci Resolve finishing and readback, full-source first-assembly ordering instead of filename order or blueprint fallback, 100GB large-source unattended-readiness, first-three-minute opening story plan, clean scenic title bridges with actual frame proof and no duplicate/ghosted route/date text, reusable opening/7:04/BGM regression probes, BGM-only no-voiceover TXT/SRT delivery plus BGM musicality and final rendered mix proof, dense title-safe V3 subtitle overlays, source-orientation scan plus V14-style portrait repair, opening/chapter/ending establishing material with aerial or local scenic evidence, Bilibili/Malta reference rhythm, scene grammar, reference-profile application, and reference-transition-profile, creator-cut shot selection/application, final-source usage, timeline-variety, transition grammar, transition cadence, transition microstructure, transition scene-arc, transition effect-palette, transition motif-coherence, transition visual-match, transition motion-direction, transition-breathing-room, transition-sequence-satisfaction via `transition-sequence-satisfaction-contract.md`, scene-flow-arc, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, transition bridge visual evidence, transition preview-quality, transition audition quality/visual/role proof, pair-continuity, execution-readiness, transition-polish application, Resolve transition materialization/apply-path proof, bridge-sequence application, final-blueprint lineage, rendered transition proof, final-viewer-friction closure, first-draft-satisfaction closure via `first-draft-satisfaction-contract.md`, whole-film-satisfaction closure via `whole-film-satisfaction-contract.md`, route texture, director polish, the final QA floor, and the Skill maturity floor. Run it after Skill edits and in final QA. If it blocks, fix the Skill rule/script/report that failed; do not create a V15/V16 package just to work around the missing reusable behavior.

## Style QA Upgrade
Read `references/bilibili-travel-style.md` before any long-form travel structure, title, narration, BGM, transition, or final QA work. Treat the listed creators and the local Malta film as non-copying style references: extract pacing, route rhythm, transition craft, title restraint, BGM energy, and subtitle density, but never copy their exact titles, music, narration, or footage. Read `references/parallel-world-vlog-style.md` when the user references `叽叽歪歪的平行世界`, provides downloaded videos from that creator, asks how the cover/thumbnail is made, or wants a first draft closer to that Bilibili long-form travel style.

For cover, thumbnail, and hero title design, follow the Parallel World cover formula: high-recognition aerial/skyline/coast/landmark/route background; oversized 1-5 word Chinese destination title; smaller English/place subtitle beneath; yellow/orange/white high-contrast typography; no route/date clutter, stacked city names, internal labels, project slugs, or subtitles over the hero title.

Resolve is the default finishing surface when DaVinci Resolve is installed and reachable. Do not stop at an FFmpeg-only assembly when the user asks for DaVinci, a finished film, or a reusable Skill. Build or revise a real Resolve project/timeline through the official API, read it back with `audit_resolve_timeline.py`, and render from Resolve unless Resolve is unavailable or the user explicitly chooses a non-Resolve route.

For final delivery, block the edit if:

- the opening title has duplicate/ghosted text, stacked city names, route/date labels near the hero title, project IDs, placeholder text, or subtitles sitting in the title safe zone
- a portrait/vertical clip appears inside a 16:9 master with black side bars and no explicit designed-phone-insert exception
- scenic openings, city hooks, or day/place transitions expose source-camera voice after the user asked for BGM-only or no voiceover
- BGM is missing, inaudible, stylistically wrong, or lacks a manifest with local track paths and license URLs
- day/place transitions are only hard cuts or black cards instead of route-aware bridge footage such as train, station, street, skyline, weather, food, hotel-window, or aerial inserts

Use `scripts/build_bgm_bed.py` to create a continuous, traceable BGM bed from approved local music tracks. Use `scripts/make_davinci_stylefix_blueprint.py` when an existing Resolve blueprint has title clutter, portrait/pillarbox clips, source-camera voice, or missing BGM; it creates a DaVinci-first v10-style blueprint with clean opening title, video-only footage import, A3 BGM, and explicit replacement segments. It must ffprobe-scan every actual video `sourcePath` in the blueprint, write `manualQualityFix.orientationFixes`, and replace or block all raw portrait/square/unknown clips before Resolve import; never hard-code only the user-reported timestamp. Use `scripts/prepare_orientation_repair_package.py` when a previously rendered/QA-passed package becomes blocked by a newer source-orientation gate. It creates a new package directory, materializes reusable package assets, rewrites package-internal paths including copied asset-directory JSON/text files, syncs title bridge manifest segment paths from the final blueprint, generates a v14-style repaired blueprint, and writes `orientation_repair_package_report.json`; do not mutate the old package or reuse its stale final QA as current proof. Use `scripts/prepare_subtitle_overlay_asset.py` when the finished film needs visible subtitles in DaVinci: it converts dense SRT/TXT-style guidance into a transparent QuickTime alpha overlay and can add a V3 `subtitle_overlay_video` clip to the Resolve blueprint. Use `scripts/audit_visual_audio_style.py` after every final render and after user feedback timestamps to verify clean title policy, pillarbox/vertical regressions, BGM manifest, audio mode, loudness, silence ratio, and optional OCR. Use `scripts/audit_story_style_contract.py` after render verification to check the director-level contract: clean opening, visual bridge transitions, scenic ending, subtitle density/rendered subtitle mode, BGM-only readback, loudness/silence, orientation, asset evidence, and long-form pacing. Its opening-title evidence must show exactly one main title value such as `TOKYO`, not repeated/stacked text such as `TOKYO TOKYO`, conflicting `cityTitle`/`titleText` values, route/date copy, or opening subtitles.

For user-reported regressions, always run `scripts/audit_feedback_regressions.py` in addition to the broader visual/audio and story audits. The feedback audit is the durable memory of what the user already rejected: duplicate/ghosted opening title text, portrait clips at named timestamps, missing or inaudible BGM, source-camera/user voice during scenic/title moments, sparse subtitles, and captions overlapping title zones.

Before that final feedback audit exists, run `scripts/prepare_feedback_regression_plan.py` so the same rejected failures are already present as pre-render probes. The plan must carry opening-title, 7:04 portrait, 7:04 BGM/voice, and opening BGM/no-voiceover timestamps into `prepare_audio_scene_policy_plan.py`, `audit_feedback_regressions.py`, and `run_final_qa_suite.py`; do not rely on memory or conversation context to retype them later.

Run `scripts/audit_reference_style_alignment.py` before saying the Skill can deliver in the style direction the user asked for. Passing `audit_story_style_contract.py` proves core story/editorial gates; passing reference-style alignment proves the route has enough transport, street texture, lived-in detail, landmarks, varied footage, BGM/caption support, and non-copying Malta/Bilibili reference evidence.

Run `scripts/audit_director_intent_contract.py` before saying the edit has a real director intent. It must prove the opening tells the viewer what kind of journey this is, the chapters form a route arc rather than a list, shot pacing has long-form breathing room, subtitles carry route/emotion/honesty without voiceover, and the ending leaves aftertaste.

Run `scripts/audit_route_texture_contract.py` before trusting that the edit feels route-aware. It must prove every planned day/place transition is backed by physical bridge footage, chapter title moments have nearby connective tissue, chapters contain transport/street/lived-in/landmark texture beyond title cards, and opening/ending sections breathe on real visual material. If it blocks, revise the timeline structure or bridge-footage roles instead of only changing titles.

Run `scripts/audit_director_polish_contract.py` before claiming the Skill can produce a premium travel film rather than a technically valid assembly. It must connect the clean title/aerial evidence, font and asset ledger, BGM mood/license evidence, subtle effect plan, rendered subtitle policy, Resolve readback, and final export quality. A warning about unmaterialized stock/aerial search placeholders is allowed as a visible handoff risk, but a blocker means the package is not director-polished.

Run `scripts/audit_stock_aerial_closure.py` before director-polish QA if the blueprint has `stockInsertPlan` rows. The report must prove search-only stock/aerial rows did not enter the final timeline and were either replaced by verified assets or closed by local-footage coverage evidence. If this audit blocks, materialize the required stock/aerial asset, remove stale search-only plan rows, or revise the timeline so real footage covers the need.

Run `scripts/audit_title_bridge_contract.py` before trusting a clean-title claim. It must prove the opening has one city title, the actual Resolve title clips point to the generated scenic bridge videos, the title text avoids previously rejected route/date labels, title clips import video-only, and V3 subtitle overlays are suppressed during title zones. If OCR fails to recognize the expected title but this contract passes, keep the OCR miss as a warning rather than treating it as the only source of truth.

Run `scripts/prepare_bgm_selection_package.py` before trusting a BGM/no-voiceover claim. It must prove that the selected BGM bed or source tracks are local, license-traceable, target-duration-covering, blueprint-referenced, explicitly auditioned as real music, marked non-procedural/non-tone, section-fit approved, Content-ID checked, and rebuildable with `build_bgm_bed.py`; if it blocks, fill exact track/license/local-path/provider/music-identity/audition/section-fit decisions before Resolve apply.

Run `scripts/audit_bgm_audio_contract.py` before trusting a BGM/no-voiceover claim. It must prove the BGM bed referenced by Resolve is the same file named in the BGM manifest and asset ledger, materialized inside the current delivery package, long enough for the final render, licensed/traceable, mixed on A3, audible in the final MP4, and accompanied by zero A1 source-audio and zero A2 voiceover items. If it blocks on stale BGM paths, repair the package manifest/ledger/blueprint first, then re-run dependent audits.

Run `scripts/prepare_audio_scene_policy_plan.py` before any Resolve apply when the user has complained about missing BGM, scenic voice leakage, or unwanted voiceover. It must enumerate opening/title/transition/establishing/effect/feedback windows, prove ready A3 BGM coverage, require A1/A2 mute or absence, and preserve exact user complaint times such as `reported_voice_at_7_04=7:04` as regression probes.

Run `scripts/prepare_footage_select_plan.py` before package build, then run `prepare_source_selection_repair_plan.py` and `audit_source_selection_coverage_contract.py` after package build and before first-assembly trust when the user provides a large unordered source folder or says the edit should reach the four Parallel World videos/Malta final level. They must score the raw media pool, surface hero/main/texture bridge candidates, reject derived exports, flag portrait/square/unknown clips for repair, and close chapter movement/texture/payoff coverage gaps before any transition effect, stock aerial, or rhythm recut is allowed to compensate for weak source choice. Warning repair rows are not harmless: orientation/weak-source rows must be closed with concrete decision evidence and `ready_no_source_selection_repairs_needed`, not blank default fields.

Run `scripts/prepare_reference_batch_profile.py` before edit-rhythm planning or reference-style audits when multiple local reference videos are available. Do not reduce a multi-video reference set to a few screenshots; produce aggregate pacing/audio/sample-frame targets and keep the non-copying contract visible. Then run `scripts/prepare_reference_review_repair_plan.py`; do not claim reference learning is complete until it returns `ready_no_reference_review_repairs_needed`.

Run `scripts/prepare_chapter_arc_plan.py` before edit rhythm or Resolve apply when a long-form travel chapter feels like random clips. It must turn every chapter into context, movement, texture, payoff, and aftertaste rows with owner scripts for missing beats.

Run `scripts/prepare_edit_rhythm_plan.py` before any Resolve apply when the user says the edit feels AI-made, badly cut, too flat, or unlike the Malta/Bilibili reference. It must enumerate primary visual shots and chapter rhythm rows, compare pacing to the reference profile, identify long raw holds and missing cutaways, and turn them into trim/split/insert decisions instead of relying only on post-render style audits.

Run `scripts/prepare_creator_cut_plan.py` immediately after edit-rhythm planning when the user asks whether the edit can get closer to the four Parallel World videos or Malta final. It must classify every visual clip into hero, main story, texture bridge, utility, or reject/review; assign creator functions such as opening hook, route movement, lived-in detail, destination payoff, and ending aftertaste; and recommend transition recipes. After the final candidate blueprint exists, run `scripts/audit_creator_cut_application_contract.py` so the cut proves it applied the selection instead of merely planning it. Do not let a whip, rotation, zoom, or speed-ramp effect rescue weak footage; physical route evidence and selective shot choice come first.

Run `scripts/prepare_transition_grammar_plan.py` immediately after creator-cut planning when the user says transitions are still weak or asks for more polished shot-to-shot flow. Then read `references/transition-source-coverage-contract.md` and run `scripts/audit_transition_source_coverage_contract.py` so adjacent clip pairs prove selected outgoing, bridge, motion, and landing source material before visible effects are trusted. It must inspect adjacent clip pairs, recommend exact transition types, mark boundaries that need bridge inserts, and allow whip/rotation only when both sides carry route-motion energy. Do not approve a flashy transition across static or weak footage; add bridge material or use a simpler cut. Empty or generic transition decisions such as `done`, blank BGM cue, missing preview/frame evidence, or motion effects without bridge evidence are blockers, not polish notes.

Run `scripts/prepare_transition_execution_plan.py`, `scripts/prepare_transition_reference_candidates.py`, `scripts/prepare_transition_reference_selection.py`, `scripts/prepare_transition_motif_plan.py`, `scripts/prepare_bridge_sequence_plan.py`, `scripts/prepare_bridge_sequence_blueprint.py`, `scripts/prepare_transition_execution_blueprint.py`, and later `scripts/prepare_transition_polish_blueprint.py` when the user asks for better transitions or Resolve finishing. They must translate every adjacent-pair decision into a concrete Resolve recipe, non-copying A/B/C candidate ladder, and unattended-safe default selection with boundary-specific reason plus proof plan, audit repeated/template motifs, turn important route/title/timeline-gap changes into 2-5 shot bridge sequences, materialize bridge beats, and after BGM/rhythm recut add final BGM-hit/title-safe/motion-proven micro-transition metadata plus `audit_transition_source_coverage_contract.py`, `prepare_transition_choreography_plan.py`, `audit_transition_choreography_contract.py`, `audit_transition_motion_direction_contract.py`, `audit_transition_motion_accent_contract.py`, `audit_transition_effect_recipe_contract.py`, `audit_transition_cutpoint_contract.py`, `audit_transition_action_anchor_contract.py`, `audit_transition_sensory_continuity_contract.py`, `audit_transition_polish_application_contract.py`, `audit_resolve_transition_materialization_contract.py`, `prepare_resolve_transition_apply_plan.py`, `audit_resolve_transition_apply_contract.py`, `audit_bridge_sequence_application_contract.py`, `audit_transition_bridge_visual_evidence_contract.py`, `audit_final_blueprint_lineage_contract.py`, `audit_transition_cadence_contract.py`, `audit_transition_microstructure_contract.py`, `audit_transition_scene_arc_contract.py`, `audit_transition_effect_palette_contract.py`, `audit_transition_motif_coherence_contract.py`, `audit_transition_visual_match_contract.py`, `prepare_transition_preview_packet.py`, `audit_transition_preview_quality_contract.py`, `prepare_transition_audition_packet.py --build-clips`, `audit_transition_audition_quality_contract.py`, `audit_transition_audition_visual_proof_contract.py`, `audit_transition_audition_role_integrity_contract.py`, `audit_transition_storyboard_contract.py`, `audit_transition_breathing_room_contract.py`, and `audit_transition_continuity_rehearsal_contract.py` proof instead of hiding missing bridge beats behind an effect, leaving visible effects marker-only, approving rotation/whip/zoom/speed-ramp rows without selected source coverage and restrained keyframes/easing/envelopes, applying an old blueprint, making the next agent manually choose A/B/C rows, accepting selected rows with generic/pending decision text, stacking motion accents without buffer, or making the whole film feel like hard-cut/effect-spam cadence without readable action anchors and sensory continuity.

Treat strong transitions as needing aftercare: `audit_transition_continuity_rehearsal_contract.py` must block if high-energy route/title/time-jump/BGM/motion boundaries recur inside a short window without a texture bridge, scenic breath, or same-scene continuity buffer. Fix by adding calmer local footage or downgrading motion effects, not by stacking more rotation/whip/zoom.

Treat transition auditions as role-separated proof, not only ordered MP4s: `audit_transition_audition_role_integrity_contract.py` must block when outgoing, bridge/motion, and landing segments reuse the same rendered file or same source window. Important route/title/time-jump boundaries need a bridge/motion source window that is distinct from both endpoints before storyboard, Resolve apply, V14, or maturity can pass.

Treat BGM-hit transition auditions as evidence-bound, not boolean claims: `prepare_transition_audition_packet.py --build-clips` must carry concrete BGM cue or phrase evidence plus numeric hit offset/tolerance into each audition row, and `audit_transition_audition_quality_contract.py` must block when a row only says `bgmHitAligned=true` without cue, phrase, hit-second, or offset/tolerance proof.

Treat bridge-sequence repair rows as blockers, not as acceptable polish notes: `prepare_bridge_sequence_plan.py` may claim `ready_with_bridge_sequence_plan` only when `missingBeatRowCount == 0`, `repairRowCount == 0`, `blockingBridgeSequenceIssueCount == 0`, and every required beat has local candidate evidence or an approved verified fallback.

Treat bridge-sequence source diversity as part of the edit, not metadata: `prepare_bridge_sequence_blueprint.py` and `audit_bridge_sequence_application_contract.py` must block if a 2-5 shot bridge repeats one clip across most beats or repeats the same source on adjacent beats, because that reads as AI filler instead of a route/title/day-change bridge.

Treat bridge-sequence source handles as a hard visual-quality gate: `prepare_bridge_sequence_blueprint.py` must reject candidate clips whose real `sourceEndSeconds - sourceStartSeconds` cannot cover the planned bridge-beat duration, and `audit_bridge_sequence_application_contract.py` must block final candidates that would need freeze, stretch, or looped filler to make a scenic bridge beat last long enough.

When applying the Parallel World reference, run `scripts/prepare_opening_story_plan.py --package-dir <package>` and require the first 3 minutes to contain a viewer promise, destination proof, clean hero title, practical route/arrival footage, lived-in texture, and first chapter handoff; long person/context sections must be supported by B-roll or visual evidence; the ending must include route aftertaste rather than stopping on a leftover clip.

Run `scripts/prepare_rhythm_recut_blueprint.py` immediately after the BGM phrase candidate when long-shot risks exist, then run `scripts/audit_rhythm_recut_application_contract.py` after transition polish/final lineage. The output must be a separate candidate blueprint that uses existing local footage as motivated cutaways, keeps transition/effect/BGM phrase candidate metadata, keeps total duration stable, and can be preflighted before any active Resolve blueprint is replaced; the application audit must prove those main segments and cutaways survived into the final candidate.

Run `scripts/prepare_rhythm_recut_apply_package.py` after the candidate passes review/preflight and before Resolve apply. Prefer a new package fork over in-place blueprint replacement so the source package remains valid evidence, stale final render QA is not reused, and the recut package gets its own active blueprint, preflight, dry-run, apply-contract, readback, render, and final QA chain.

Run `scripts/prepare_reference_style_repair_plan.py` and `scripts/audit_reference_repair_closure.py` whenever reference-style, director-intent, director-polish, or final QA checks are blocked. Do not leave style blockers as prose; turn them into repair rows with scripts, artifacts, acceptance evidence, post-repair audits, and closure evidence before another Resolve claim.

Run `scripts/prepare_final_delivery_report.py` after render verification, client delivery rules, BGM audio contract, story style, and strict package integrity pass. It writes `FINAL_DELIVERY_REPORT.json` and `.md` with final output path, Resolve identity, render parameters, BGM/no-voiceover evidence, and explicit non-GPS route caveat wording. Do this before `audit_longform_delivery.py` and before the final `run_final_qa_suite.py` pass.

Run `scripts/audit_package_integrity.py` after the feedback/style audits and again after any blueprint/report path repair. Treat stale contact sheets, old render reports, previous-package subtitle/BGM paths, and disabled voiceover paths as package-integrity risks until the audit explains or clears them. A disabled voiceover path is not clear just because it is unused in prose; it must appear in `closedCoreCrossPackagePaths` with A1=0, A2=0, A3>0, and passing BGM/story no-voiceover evidence. Do not use a report from an older package as proof of the current Resolve render.

`prepare_subtitle_overlay_asset.py` suppresses or trims subtitle overlay cues that overlap Resolve title zones by default. Do not let V3 captions appear during opening city titles, chapter title bridges, or ending title moments unless the user explicitly requests that exception with `--allow-title-zone-subtitles`. The manifest must record the title-zone subtitle policy so missing captions during title cards are understood as intentional title cleanliness, not a dropped-subtitle bug.

`audit_subtitle_overlay_contract.py` is the delivery gate for visible captions. It blocks when the overlay manifest is missing, cue counts are sparse, overlay files are outside the package, sampled overlay videos are not alpha-capable, sampled frames are blank/fully transparent, files contain audio, V3 clips are missing from the Resolve blueprint, or subtitle clips overlap title zones. Run it again after any subtitle, title, or blueprint change.

After the final MP4 is rendered, run `scripts/audit_rendered_subtitle_visibility_contract.py --package-dir <package>` when visible subtitles are expected. It samples the final render at V3 subtitle cue times and blocks when the lower-third caption area does not show caption-like bright/dark/contrast pixels. Do not treat overlay assets, sidecar SRT, or Resolve blueprint rows as proof that subtitles survived into the exported MP4.

After the final MP4 is rendered, run `scripts/audit_rendered_title_visibility_contract.py --package-dir <package>` when opening, chapter, or ending titles are expected. It samples final-render title windows from the Resolve blueprint and blocks when central title pixels are not visible, when the surrounding background is flat enough to read like a black card or pure color slate, when opening/chapter/ending samples are missing, when structural title contracts did not pass, or when OCR detects internal/status text. Do not treat scenic title media, contact sheets, OCR misses, or Resolve blueprint rows as proof that titles survived into the exported MP4.

`audit_visual_audio_style.py` must be run with a visual manifest and `--require-clean-title` for final QA. It automatically adds title/bridge timestamps from the manifest, clears stale frame folders before sampling, uses precise frame extraction, and runs OCR across enough title samples to catch hidden route/date/template text. A stale contact sheet, or one generated from old samples, is not valid delivery evidence.

When the user rejects voiceover, keep narration as TXT/SRT and render scenic/title/transition sections with `bgm_only_no_camera_voice`; do not sneak in generated voiceover or source-camera talking.

Do not assume DaVinci can directly import an SRT through the Python API. Local Resolve 21 smoke testing showed that a new subtitle track can be created, but `Timeline.ImportIntoTimeline(<srt>)` returned `False` and produced zero subtitle items. For visible subtitles, prefer a transparent subtitle overlay video on V3 via `prepare_subtitle_overlay_asset.py`, then read back the V3 item count after `build_resolve_timeline.py --apply`. Sidecar-only SRT is acceptable only when the user explicitly wants separate TXT/SRT handoff; otherwise it is a warning or blocker in `audit_story_style_contract.py`.

## Definition of Done

Do not call the job complete unless the package contains all required handoff pieces:

- location and route status, with stale/mismatch blockers resolved or clearly marked
- raw intake completeness audit plus footage recognition/route MD report proving the whole selected folder was indexed, recognized, routed exactly once, and scored before editing
- full-folder recognition coverage, or an explicit blocked status; do not cut from a 12-video sample when the folder has 59 videos
- location truth contract audit proving whether the package can only claim visual route reconstruction with caveats or can actually claim verified per-video geolocation
- footage select plan proving every active source video was scored and tiered before first assembly, with hero/main/texture/utility/reject rows, orientation repair flags, derived-export rejection, local bridge candidates, and chapter-pool coverage gaps
- blocked-project recovery plan when recognition/location truth/forward-test blocks a matched project; it must list ordered phases, exact next commands, approval gates, and safety flags before any cutting resumes
- external media intake packet when mounted drives contain multiple trip roots or project/media roots can be confused
- media index readiness for the chosen project, or a safe `run_videoclaw_media_index.py --apply` report when the index had to be created from mounted media roots
- frame index, location map, and route timeline readiness, or a safe `run_videoclaw_route_pipeline.py` report explaining which local/cloud steps remain
- Codex visual review notes for contact sheets/sampled frames when route labels are low-confidence or automatic labels are suspicious
- a fresh Codex-visual-confirmed route timeline when Codex visual inspection covered the whole folder and produced enough evidence to cut
- local Ollama vision or Tesseract OCR reports only when the user explicitly authorizes those local helper routes
- route coverage scaffold when automatic route coverage is too low
- route review packet when route/location artifacts need human review
- route decision sheet when route review needs chapter decisions or region mismatch approval
- route decision application report proving whether approved route decisions can be safely copied into `route_review.json`
- confirmed route candidate or fresh `confirmed_route_timeline.json` before final route-aware cutting
- confirmed route candidate audit proving the candidate covers every active source video exactly once, has no duplicated/unknown/excluded refs, preserves honest region labels, and only advances with non-GPS caveats when exact per-video truth is unverified
- voiceover script
- TTS or recorded voiceover audio plan/file
- when the user rejects voiceover, a text-only narration document and proof that no voiceover audio asset is imported/rendered
- subtitle SRT draft; when the user asks for Jianying/CapCut generation, deliver SRT/TXT and do not generate local TTS
- local delivery assets report covering title cards, optional local voiceover, and refreshed Resolve enrichment
- BGM cue plan with licensing/source status
- aerial/establishing-shot search plan or approved local/stock assets
- opening city aerial/establishing clip with clean English city title typography; never expose project slugs, random IDs, or placeholder copy in the first frame
- visual polish manifest proving opening, chapter, and ending titles use scenic route-aware video bridges rather than black slates; include a contact sheet or sampled-frame evidence for these moments
- title typography plan proving every opening/chapter/ending title row has approved text, verified font evidence, scenic background/segment evidence, forbidden-text checks, title-zone subtitle suppression, and no stacked/ghosted text before final title claims
- visual establishing plan proving the opening, every chapter establishing moment, and the ending have local-footage-first search hints, trip-derived famous-place/landmark hints, licensed stock/aerial fallback searches, title typography evidence, existing timeline evidence, exact decision fields, and no previous-trip defaults before aerial/landmark claims
- effect motion plan, blueprint, and application audit proving opening/chapter/ending title reveals and day/place transition motions are restrained, source-evidence-backed, title-zone safe, BGM-only, decision-field ready, candidate-materialized, final-blueprint applied, and free of glitch/random-spin/flash/template-heavy effects before director-polish claims
- feedback regression plan proving concrete rejected draft failures such as opening title ghosting, 7:04 portrait footage, 7:04 source/user voice, and opening BGM/no-voiceover are preserved as reusable pre-render audio-policy probes, post-render feedback-audit probes, and final-QA timestamps
- audio scene policy plan proving opening/title/transition/visual-establishing/effect/feedback windows are A3 BGM-led, have exact mute/readback decision fields, include known complaint probes such as `7:04` when applicable, and contain no A1/A2 source-camera or voiceover leakage before Resolve writes
- reference batch profile plus application audit proving multiple supplied reference videos were analyzed into aggregate pacing/audio/sample-frame style targets and then consumed by opening, chapter, rhythm, creator, transition, caption, audio, scene-grammar, and style gates before claiming the Skill learned from the four Parallel World videos or Malta final
- first assembly source-order and large-source unattended-readiness contract evidence proving `build_delivery_package.py` used the full-source footage select plan when present to sort local chapter media by selection tier/score instead of raw filename order, blueprint fallback samples, or repair/reject rows, and proving the package can connect media-root intake, whole-folder recognition, source selection, first assembly, unattended first draft, and blueprint preflight for large unordered folders
- opening story plan proving the first three minutes have viewer promise, destination proof, one clean hero title, practical arrival, lived-in texture, first chapter handoff, BGM-only opening policy, and title-zone subtitle suppression before rhythm/style claims
- edit rhythm plan proving every primary visual shot has a route/street/lived-in/landmark/scenic/title/transition/ending function, Malta/reference pacing targets, long-shot/cutaway risk rows, chapter variety rows, timeline-variety owner evidence, and trim/split/insert decision fields before any "not AI-made" style claim
- creator cut plan plus application audit proving every visual clip has a creator function, editorial tier, recommended use, weak-clip reject/demotion path, chapter coverage row, motivated transition recipe, and final-candidate matching before claiming the cut approaches the four Parallel World videos or Malta final
- transition grammar plan proving every adjacent visual pair has a recommended transition, fallback transition, concrete non-generic pre-Resolve decision, bridge-evidence decision, title/caption safety fields, BGM phrase cue fields, preview/frame evidence requirements, and no unmotivated whip/rotation effect before Resolve writes
- transition execution plan/blueprint, reference candidate ladder, motif, bridge sequence, bridge sequence blueprint, transition source coverage, transition-polish application, Resolve transition materialization/apply, bridge-sequence application, transition bridge visual evidence, final-blueprint lineage, transition cadence, transition microstructure, transition preview packet, transition storyboard, transition-breathing-room, final-cut-smoothness, narrative-adjacency, and timeline-variety audits proving every transition grammar row has a Resolve-ready recipe and A/B/C candidate metadata, bridge-missing rows remain blocked, motion effects cite route-motion evidence and selected source coverage, BGM-hit/title-safe polish and marker/readback payloads survive into the final blueprint, every adjacent shot has a landed BGM-only/title-safe/handle-ready transition beat and viewer-readable route/place/story-function/bridge/BGM/title reason, visible effects have API/manual/bridge apply paths instead of marker-only metadata, important boundaries have 2-5 shot bridge beats materialized and preserved in the final candidate as video-only clips with local source/video-probe/frame evidence plus viewer-purpose/outgoing/bridge/landing generated preview evidence, motion accents are rare and separated by stable landing footage, the final active blueprint inherits the latest candidate chain, title boundaries suppress subtitles, the whole film avoids bare-cut/repeated-template/effect-spam cadence, final adjacent joins have bridge/match/breathing proof instead of rough hard cuts, movement/texture/payoff/aftertaste vary across the timeline, and scenic/title/transition audio stays BGM-only
- rhythm recut candidate and application audit proving long raw holds were automatically converted into shorter main segments plus existing-footage cutaways, survived into the final candidate blueprint, kept unchanged total timeline duration, A3 BGM-only safety, row-level approval/readback fields, and Resolve preflight readiness before replacing the active blueprint
- rhythm recut apply package proving an approved candidate can become a separate Resolve-ready package fork with active recut blueprint, rewritten package-local paths, no copied final-render proof, preflight evidence, dry-run/apply-contract next actions, and no source package mutation
- reference style repair plan plus unattended repair queue proving every blocked reference/director/QA/style/preflight gap has a concrete repair row with owner script, required artifact, resolved command, execution order, repair key, post-repair commands, acceptance evidence, forbidden workaround, reference rule, and post-repair audit/readback fields before another "make it better" iteration
- final Resolve blueprint proof that the opening, chapter, and ending title moments actually reference scenic bridge video clips, not stale `title_cards` slates or long cropped place descriptions
- scenic title bridge contact sheet proving title frames do not contain hidden global route labels, generic date labels, template lower-corner route text, stale black cards, or subtitles sitting over the title safe zone
- machine-readable asset license ledger for BGM, aerial/stock, and fonts
- asset sourcing packet with provider/license URLs, selection fields, approval evidence, and download/import gates
- BGM sourcing brief proving the Skill proactively generated mood-appropriate search rows, section plans, provider/license URLs, and exact decision fields before any BGM/no-voiceover final claim
- BGM selection and phrase-blueprint package proving the selected music bed is local, license-traceable, target-duration-covering, referenced by the active Resolve blueprint, rebuildable from local source tracks, and materialized into section/phrase/transition-cue candidate metadata before BGM/audio contract audits
- asset decision reconciliation report after sourcing decisions are filled or confirmed still missing
- typography plan for titles, place cards, subtitles, and map labels
- day/chapter transition plan
- transition bridge plan proving every day/place/chapter boundary has local bridge-footage search hints, licensed stock/aerial fallback queries, BGM-only audio policy, title-zone subtitle policy, exact decision fields, and final bridge evidence before route-texture claims
- caption story plan proving no-voiceover delivery has dense SRT cues, per-chapter caption targets, gap limits, title-zone suppression policy, text-only narration export, and rewrite decision fields before subtitle overlay generation or maturity claims
- audience caption contract audit proving final SRT/TXT/burned-caption text is for viewers, not a user-facing edit report about fixes, QA, tools, versions, exports, or delivery state
- natural visual transition clips between days/places, such as station, street, skyline, vehicle, signage, food, hotel window, weather, or aerial bridge footage
- effect plan for restrained title reveals, route motion, transitions, or chapter emphasis; do not overuse effects, but a client delivery cannot be a bare concatenation
- 20-minute long-form structure, not a 1-2 minute short-video outline
- 4K high-frame-rate export target, normally 59.94/60fps for DJI/action/phone travel footage unless source or platform requirements justify otherwise
- high-bitrate final output target, normally at least 60 Mbps for 4K long-form H.264/H.265 masters
- DaVinci Resolve API timeline blueprint and a dry-run/apply command
- Resolve source-footage clips preserve camera/source audio on A1 unless a clip is explicitly video-only
- long-form coverage evidence showing initial selected seconds, gap-fill seconds, final covered seconds, and target seconds
- Resolve timeline enrichment report with subtitle cues, audio plan, stock/aerial placeholders, transition markers, and chapter markers
- subtitle delivery mode proof: native subtitle items, V3 transparent subtitle overlay readback, or an explicitly accepted sidecar-only SRT/TXT handoff
- subtitle title-zone policy proof showing V3 subtitle overlays were suppressed or trimmed during opening, chapter title bridges, and ending title moments unless explicitly overridden
- rendered subtitle visibility proof showing final MP4 frames sampled at subtitle cue times visibly contain lower-third caption pixels
- rendered title visibility proof showing final MP4 opening, chapter, and ending title windows visibly contain clean central title pixels over non-flat scenic/establishing background texture
- Resolve blueprint preflight proving source files, source ranges, track overlaps, V1 coverage, title cards, subtitles, markers, and source-audio policy are safe before `--apply`
- generated title/place card media or a clear reason they are pending
- Resolve apply approval contract before any actual `build_resolve_timeline.py --apply`
- Resolve readback audit after any actual timeline write
- delivery package audit with no blockers before final render
- safe workflow run report showing which local steps ran, command return codes, project-state summary, Resolve API summary, route decision summary, route decision application summary, asset decision summary, audience-caption, large-source unattended-readiness, motion-accent repair, rendered transition proof, transition-reference-readiness, transition-sequence-satisfaction, story-style, reference-alignment, director-intent, route-texture, stock/aerial closure, director-polish, final-viewer-friction, first-draft-satisfaction, unattended repair queue, whole-film-satisfaction, one-shot-autonomy, shot-flow continuity, unattended-first-draft, Skill maturity, V14 baseline contract summaries, normalized `blocked*` status handling, Resolve dry-run summary, Resolve apply contract summary, render-plan summary, audit status, safety flags, and remaining blockers
- Resolve render plan with final export settings
- queued/rendered Resolve job status only after explicit approval
- final render delivery verification plus rendered transition proof proving the output file duration, resolution, audio stream, sample frames, black-frame scan, subtitle evidence, and actual transition-window frames are clean
- final render delivery verification proving frame rate and bitrate meet the quality target
- final render quality bundle audit proving the final MP4 is bound to render verification, visual/audio style, BGM audio, final BGM mix, rendered subtitle visibility, rendered title visibility, rendered transition proof, editorial watchdown, final viewer friction, whole-film satisfaction, and package integrity before any DaVinci-level claim
- long-form delivery audit proving the 20-minute film requirements are met, or explicitly listing route/location caveats that still prevent a claim of perfect per-clip geolocation
- location truth contract audit proving full-source accounting, per-video recognition rows, frame evidence, provider provenance, confirmed-route linkage, derived-source exclusion, and whether exact per-video location claims are allowed
- client delivery rules audit proving the opening, route, actual blueprint source orientation scan, SRT-only/no-voiceover mode, BGM, transitions, effects, titles, assets, and export quality satisfy the product bar
- story style contract audit proving the cut does not merely pass technical checks but also has Bilibili/Malta-style travel rhythm: one non-duplicated opening title value, dense captions, BGM-led scenic sections, route-aware bridges, scenic ending, no portrait/pillarbox regressions, traceable assets, and DaVinci readback evidence
- reference style alignment audit proving the edit has non-copying Malta/Bilibili reference evidence, route chapters, transport connective tissue, street/lived-in/landmark balance, real-footage variety, scenic title/bridge structure, and BGM/caption-led no-voiceover storytelling
- director intent contract audit proving the cut has an explicit opening mission, route arc, chapter beat categories, long-form pacing, caption story/honesty, and ending aftertaste before any premium style claim
- route texture contract audit proving planned day/place transitions are backed by actual bridge clips, chapter titles have nearby connective tissue, chapters contain lived-in route texture beyond title cards, and the timeline balances transport, streets, daily detail, and landmarks
- stock/aerial closure audit proving search-only stock/aerial placeholders are either materialized as verified local assets or explicitly closed as not used in the final Resolve render and covered by real local route/title footage
- director polish contract audit proving the aerial/establishing opening, typography/font evidence, BGM mood and license, restrained title/transition effects, dense rendered subtitles, Resolve track readback, and premium export settings form one coherent delivery chain; list any unmaterialized stock/aerial search placeholders as warnings
- title bridge contract audit proving clean scenic title manifests, segment/overlay files, Resolve V2 title clips, opening city title policy, forbidden visible text, video-only import, and subtitle title-zone suppression are consistent
- BGM/audio contract audit proving the actual BGM bed is current-package materialized, traceable/licensed, long enough, referenced by Resolve, present on A3, audible in the MP4, and not mixed with source-camera or voiceover audio
- final BGM mix contract audit proving the exported MP4 has audible multi-band music across timeline samples and scenic/title/bridge/ending windows, with no hum/tone collapse
- feedback regression audit for every concrete user complaint timestamp proving the same failure cannot silently recur in the next run
- package integrity audit proving final render evidence, Resolve readback identity, core QA statuses, and cross-package/stale paths are coherent for the current package; disabled voiceover leftovers must be explicitly closed with A1/A2/A3 and BGM/story evidence; strict portable mode must not block before external handoff
- Skill maturity contract audit proving the reusable Skill itself covers the user's repeated failures: clean title, no portrait regression in final render or actual Resolve blueprint source paths, feedback regression planning, proactive BGM sourcing and selection/build packaging, proactive audio-scene BGM/no-voiceover planning, chapter-arc structure, proactive edit-rhythm/shot-purpose planning, creator-cut selective shot choice, final-source usage, timeline-variety, shot-flow continuity, final-candidate application, transition-grammar/execution/transition-blueprint/transition-cutpoint/transition-action-anchor/transition-sensory-continuity/motif/bridge-sequence/bridge-blueprint/transition-polish-application/resolve-transition-materialization/resolve-transition-apply/bridge-application/final-blueprint-lineage/transition-microstructure/pair-continuity/execution-readiness decisions, transition-sequence-satisfaction, reference scene-grammar, rhythm-recut candidate blueprints and apply-package forks, large-source unattended-readiness, final-viewer-friction aggregation, first-draft-satisfaction closure, whole-film-satisfaction closure, one-shot-autonomy/`blocked_one_shot_autonomy` closure via `audit_one_shot_autonomy_contract.py` and `references/one-shot-autonomy-contract.md`, unattended repair queue, unattended-first-draft chain closure, dense subtitles, director intent, route texture, Bilibili/Malta style anchors, DaVinci delivery, location-truth honesty, stock/aerial closure, and portable handoff
- V14 baseline contract audit proving the Skill has converted the V1-V14 correction history into a reusable first-draft baseline, not a one-off Tokyo/Osaka package
- trip generalization contract audit proving rescue scripts do not force stale previous-trip defaults such as TOKYO/Japan/Tokyo-to-Osaka on future projects
- Skill forward-test contract audit after substantial Skill revisions, proving the Skill handles at least one known-good package, one matched-but-blocked separate trip, and one unknown or ambiguous mounted media root without silently cutting the wrong material
- final QA suite report proving all final gates were run or intentionally reused: render verification, visual/audio style, BGM/audio contract, BGM musicality, final BGM mix, location truth contract, client rules, long-form delivery, story style, reference alignment, director intent contract, route texture contract, title bridge contract, rendered title visibility contract, stock/aerial closure, director polish contract, feedback regression, final-viewer-friction, first-draft-satisfaction, whole-film-satisfaction, one-shot-autonomy, default package integrity, strict portable package integrity, transition pair-continuity, transition execution-readiness, transition reference candidates, transition reference selection, transition source coverage, transition-polish application, Resolve transition materialization/apply contract, bridge-sequence application, transition bridge visual evidence, final-blueprint lineage, transition cadence, transition microstructure, transition scene-arc, transition effect-palette, transition motif-coherence, transition visual-match, transition flow repair, transition-sequence-satisfaction, transition action-anchor, transition sensory-continuity, transition storyboard, transition-breathing-room, final-cut-smoothness, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, final-source usage, creator-cut application, reference scene-grammar, chapter-story-spine, shot-flow continuity, timeline-variety, large-source unattended-readiness, unattended repair queue, unattended-first-draft contract, and Skill maturity contract
- QA checklist covering black frames, audio levels, subtitle sync, licenses, route accuracy, and export settings

If any required item is missing, report the missing item and the next action instead of saying it is deliverable.

## Workflow

1. Inspect project state and artifacts with `check_project_state.py`.
2. Read `references/editor-integration.md` before choosing an editing route.
3. Read `references/delivery-workflow.md` before building a package.
4. Read `references/davinci-resolve-api.md` before touching Resolve.
5. Read `references/long-form-travel-style.md` before drafting structure or narration.
5a. Read `references/bilibili-travel-style.md` before cutting style, titles, BGM, transitions, or final QA when the user asks for Bilibili/travel-vlog polish or provides a local reference film.
5b. Read `references/parallel-world-vlog-style.md` when the user provides `叽叽歪歪的平行世界` videos/screenshots, asks how their cover/title is made, or wants the Skill to learn that creator's opening, transition, cover, and ending style.
5c. Read `references/multicamera-roadtrip-story-engine.md` when the source mixes Mini-series drone, Action camera, phone/synchronized dual capture, dash-mounted driving footage, authentic camera speech, and local user-supplied music.
5d. Read `references/homeward-flight-pov-style.md` for hotel/car/airport/gate/aircraft departure or return-home chapters, then use its task-chain and restrained Jianying `向上` motion-accent policy without inheriting the reference's missing BGM/title/captions or repeated effect habit.
6. Read `references/narration-subtitles.md` before writing narration, TTS, or subtitles.
7. Read `references/music-stock-fonts.md` before searching for BGM, aerials, stock inserts, or fonts.
8. Read `references/output-contracts.md` when interpreting route/location JSON artifacts.
9. Run `discover_external_media.py` when an external drive such as `/Volumes/<drive-name>` is mounted and the source media root is not yet confirmed.
10. Run `prepare_external_media_intake.py` before any long-form package build when multiple mounted trip roots or project/media mismatches exist.
11. Run `run_videoclaw_media_index.py` when the selected project has no media index but mounted media roots are present; use `--apply` only after the dry-run shows the expected source videos.
12. Run `run_videoclaw_route_pipeline.py` when frame/location/route artifacts are missing; add `--allow-cloud-call` only after the user approves real cloud recognition.
13. Use Codex visual inspection on contact sheets and sampled frames to reject bad automatic labels, identify obvious route nodes, and write auditable route review notes. For same-date multi-stop travel days, write explicit per-chapter `videoNames`/`videoIds` coverage instead of relying on date-only grouping.
14. Run `prepare_codex_visual_confirmed_route.py --project-dir <project>` without `--apply` when Codex visual inspection has covered the whole folder and the route evidence is sufficient. Then run `audit_confirmed_route_candidate.py --project-dir <project>` and use `--apply` only after the candidate audit is not blocked and the user explicitly approves writing `confirmed_route_timeline.json`; this is the preferred confirmation path for this user.
15. Run `run_local_ollama_vision_recognition.py` or `run_local_tesseract_ocr.py` only when the user explicitly requests those local helper routes.
16. Run `prepare_footage_recognition_report.py`; if it is blocked, fix recognition/route coverage before cutting.
16a. Run `audit_location_truth_contract.py`; if it is `passed_with_caveats`, the edit may proceed with visual-route language, but do not claim exact per-video GPS/per-clip geolocation. If the user requires exact location truth, rerun with `--require-verified-per-clip-location` and fix blockers before cutting.
16b. If the recognition report or location truth audit is blocked for a matched project, run `prepare_blocked_project_recovery_plan.py` immediately. Treat the blocked-project recovery plan as the handoff contract for the next AI: it must say whether to fix media/frame artifacts, choose Mimo/cloud approval or Codex visual review, resolve route review, rerun truth gates, and only then build a package.
16c. Run `prepare_footage_select_plan.py --project-dir <project>` after recognition/location truth is usable and before package build, then read `references/editorial-judgment-jianying-music-contract.md`. Treat automatic scores as provisional: complete full-duration temporal scan and in-motion candidate-window review, keep `reject_or_review` rows recoverable, and build a reversible keep/reserve/reject ledger before package build. After the rough cut, run the omission challenge and `audit_editorial_judgment_contract.py --report <editorial-judgment-application.json>`. Then run `prepare_source_selection_repair_plan.py --package-dir <package> --project-dir <project>`, `audit_source_selection_coverage_contract.py --package-dir <package>`, and `audit_large_source_unattended_readiness_contract.py --package-dir <package>`, so the first assembly prefers hero/main/texture bridge candidates without silently losing exciting windows, rejects only derived/explicitly reviewed material, closes chapter movement/texture/payoff gaps, flags portrait/square/unknown footage for repair, requires warning repair rows to have non-generic closure decisions, and proves large unordered folders connect to unattended first-draft/preflight instead of cutting raw filename order. For 100GB-class or mounted-drive jobs, the same audit must also prove package/project outputs are outside the source footage root, the workspace has the required free-space budget, and resume checkpoints exist before any long render, Resolve write, cleanup, or style-polish pass.
16d. Before footage selection on mixed-camera jobs, run `prepare_multicamera_intake_plan.py`, `prepare_dashboard_reframe_plan.py`, and `prepare_sync_sound_plan.py`. Pass a local transcript directory when available. Treat embedded device identity as authoritative, keep low-quality transcript words out of audience captions, retain approved authentic speech and lived-in source sound by default, mute only proved pure-scenic/outward-view classes, and carry dashboard transforms into the Resolve blueprint.
17. Run `build_route_coverage_scaffold.py` if automatic route coverage is too low for a 20-minute film.
18. Run `prepare_route_review.py` if route chapters are stale, mismatched, under-covered, or marked for human review. Use `--route-source <route_coverage_scaffold.json>` when reviewing a full-media scaffold.
19. Run `prepare_route_decision_sheet.py` so route decisions and region mismatch approval are editable and auditable.
20. Run `apply_route_decision_sheet.py` after the decision sheet is approved; use `--apply` only after explicit approval to update `route_review.json`.
21. Run `prepare_confirmed_route_candidate.py` after review decisions; then run `audit_confirmed_route_candidate.py` and use `--apply` only after the user approves confirmed route writes and the candidate audit is not blocked.
22. Run the safe local workflow with `run_delivery_workflow.py` when preparing a package from scratch or refreshing all safe local artifacts.
23. Build a delivery package with `build_delivery_package.py` when only the package skeleton is needed.
23a. Run `prepare_opening_story_plan.py --package-dir <package>` immediately after package build and before title, visual establishing, BGM/audio, rhythm, creator-cut, or director-intent planning. If any of the six opening beats lacks evidence, repair with selected local hero/route/lived-in clips before Resolve apply.
24. Analyze the optional local reference film with `analyze_reference_video.py` when calibrating long-form pacing.
24a. Reject a stale or shallow local reference analysis when it lacks `pacingProfile`, `audioProfile`, at least 12 sampled frames, a contact sheet, >=95% `fullTimelineReview` decode/timeline coverage, ordered timeline sheets, complete boundary-candidate sheets, and whole-film waveform/spectrogram evidence; rerun `analyze_reference_video.py` before `audit_reference_style_alignment.py` or `audit_skill_maturity_contract.py`.
25. Generate local delivery assets with `prepare_delivery_assets.py`; add `--generate-local-voiceover` only after explicit approval for local TTS.
26. Use `make_city_aerial_title.py` for opening/city hooks when an approved aerial or establishing clip exists.
27. Refresh Resolve enrichment with `enrich_resolve_blueprint.py` after title, subtitle, voiceover, BGM, stock, or transition changes.
27a. When visual title bridges are generic, black, cluttered, or contain global route/date/template text, run `prepare_scenic_title_bridges.py --package-dir <package> --update-blueprint` before subtitle overlay generation and Resolve preflight. Inspect its contact sheet; reject if opening/chapter/ending title frames contain global route labels, subtitles over the main title, black slates, or stale `title_cards` media.
27b. When visible final subtitles are required, run `prepare_subtitle_overlay_asset.py --package-dir <package> --update-blueprint` after dense SRT approval and title-bridge cleanup, and before Resolve blueprint preflight. Run a short `--sample-duration-seconds 5` smoke test first on new machines to verify the alpha overlay path. Keep the default title-zone subtitle suppression unless the user explicitly asks for captions over titles.
28. Generate title/place cards with `generate_title_cards.py --update-blueprint` only when the combined asset-prep script is not appropriate; do not use black slates for the opening hook.
29. Generate the asset ledger with `build_asset_ledger.py`.
30. Generate the asset sourcing packet with `prepare_asset_sourcing_packet.py`.
30a. Generate the BGM sourcing brief with `prepare_bgm_sourcing_brief.py --package-dir <package>` so missing BGM turns into a concrete Mixkit/Pixabay/paid-library search and selection packet before asset decisions.
30aa. Generate the BGM selection package with `prepare_bgm_selection_package.py --package-dir <package>` so any selected music bed is proven local, license-traceable, target-duration-covering, blueprint-referenced, explicitly auditioned as real music, non-procedural/non-tone, section-fit approved, Content-ID checked, and rebuildable before audio policy or Resolve writes.
30aa1. When the user supplies a local music folder, run `prepare_music_library_plan.py --project-dir <project> --music-dir <music> --blueprint <package>/resolve_timeline_blueprint.json`, then build A3 with `build_bgm_bed.py --placement-plan <music-plan.json> --ducking-plan <blueprint> --update-blueprint <blueprint>`. Normalize every selected segment before role gain, cover the intended timeline, and measure that authentic-speech windows duck roughly 8 dB instead of becoming silent.
30aa2. When the user supplies a large DOCX/CSV/JSON song guide or requests online-catalog selection, read `references/bgm-catalog-beatcut-contract.md`, preserve exact requested versions and rejection reasons, materialize approved files into a stable project-local library, cut phrase cues on strong beats and picture boundaries, and run `audit_bgm_catalog_beatcut_contract.py --report <application-report.json>` before editor writeback or handoff.
30aa3. When the user requests Jianying built-in music, use `provider=jianying_native_catalog`, search and audition inside the installed editor, record exact native asset IDs and entitlement, preserve authentic speech, place music only on approved scenic windows, and run `audit_editorial_judgment_contract.py --report <editorial-judgment-application.json>` after timeline playback. A search plan, local cache row, or external audio file does not prove Jianying-native music use.
30ab. After transition/effect candidate blueprints exist, read `references/bgm-phrase-blueprint-engine.md` and run `prepare_bgm_phrase_blueprint.py --package-dir <package>` so BGM sections, phrase markers, clip annotations, and transition cue metadata are materialized before rhythm recut or Resolve writes.
30b. Generate the transition bridge plan with `prepare_transition_bridge_plan.py --package-dir <package>` so every day/place/chapter boundary gets a concrete local-footage-first bridge row, licensed stock/aerial fallback queries, BGM-only transition audio policy, subtitle/title-zone guidance, and exact decision fields before asset decisions or Resolve writes.
30c. Generate the caption story plan with `prepare_caption_story_plan.py --package-dir <package>` so sparse subtitles and unwanted voiceover become a concrete dense SRT/TXT handoff plan with per-chapter targets, title-zone suppression, and no-voiceover policy before subtitle overlay generation.
30c1. Run `audit_audience_caption_contract.py --package-dir <package>` after subtitle/TXT generation and before subtitle overlay rendering. Rewrite any blocked caption or TXT line that reports edit status, repair actions, version labels, QA, tool names, delivery state, source-audio muting, music entering/leaving, transition construction, or shot-cutting technique instead of speaking naturally to the audience. The editor smoke must expose `audienceCaptionTechnicalMetaTrapBlocked=true` so technical edit narration cannot silently return.
30c2. Run `audit_subtitle_overlay_contract.py --package-dir <package>` after `prepare_subtitle_overlay_asset.py --update-blueprint` and before Resolve preflight/final QA. Do not accept sidecar-only SRT/TXT as visible subtitles unless the user explicitly requested sidecar delivery; for normal Bilibili/Malta-style delivery, V3 overlay clips must be dense, alpha-capable, visibly nonblank, package-local, audio-free, and title-zone safe.
30d. Generate the title typography plan with `prepare_title_typography_plan.py --package-dir <package>` before generating, trusting, or handing off title bridge media, then run `audit_cover_title_contract.py --package-dir <package>` after scenic title media exists, so opening/chapter/ending titles have exact clean text, font evidence, scenic source evidence, no stacked layers, title-zone subtitle suppression, and a reference-style hero cover title. If title typography, title bridge, cover/title, or title visual proof blocks, run `prepare_title_typography_repair_plan.py --package-dir <package> --json` and close every repair row before Resolve apply.
30e. Generate the visual establishing plan with `prepare_visual_establishing_plan.py --package-dir <package>` before trusting aerial, landmark, or city-establishing coverage, so opening/chapter/ending rows have local footage hints, famous-place/landmark fallback searches, title evidence, timeline evidence, and exact asset decision fields.
30f. Generate the effect motion plan with `prepare_effect_motion_plan.py --package-dir <package>`, then materialize it with `prepare_effect_motion_blueprint.py --package-dir <package>` after transition/bridge candidate blueprints exist, and run `audit_effect_motion_application_contract.py --package-dir <package>` after final blueprint lineage, so motion rows are restrained, evidence-backed, title-zone safe, candidate-materialized, final-applied, and not template-heavy.
30g. Generate the feedback regression plan with `prepare_feedback_regression_plan.py --package-dir <package>` so known complaint probes such as `opening_title=0`, `reported_vertical_clip=7:04`, `reported_voice_at_7_04=7:04`, and `opening_bgm_no_voice=0` become shared timestamps for pre-render audio policy, post-render feedback audit, and final QA.
30h. Generate the audio scene policy plan with `prepare_audio_scene_policy_plan.py --package-dir <package>` before asset decisions or Resolve writes, adding `--feedback-timestamps <label=mm:ss,...>` when the user names an extra moment, so opening/scenic/title/transition/effect windows are A3 BGM-led and cannot leak A1/A2 source or voiceover audio.
30h1. If a package was created without a project-level raw selection pass, generate the footage select fallback with `prepare_footage_select_plan.py --package-dir <package>`, then read `references/first-assembly-source-order-contract.md` and run `prepare_source_selection_repair_plan.py --package-dir <package>`, `audit_source_selection_coverage_contract.py --package-dir <package>`, and `audit_first_assembly_source_order_contract.py --package-dir <package>` before edit-rhythm planning, so selected clips still receive source-quality, orientation, derived-export, chapter-pool triage, full-source ordering, and blocking source-coverage repair evidence.
30h2. If a package was created before this opening-story gate existed, generate `opening_story_plan/opening_story_plan.json` before edit-rhythm planning and treat missing beats as structure blockers, not only polish notes.
30h3. Generate `chapter_arc_plan/chapter_arc_plan.json` with `prepare_chapter_arc_plan.py --package-dir <package>` before edit-rhythm planning, so every chapter has context, movement, texture, payoff, and aftertaste decisions or owner-script repair rows; after rhythm/creator/source/transition audits, run `audit_chapter_story_spine_contract.py --package-dir <package>`, `audit_shot_flow_continuity_contract.py --package-dir <package>`, `audit_transition_breathing_room_contract.py --package-dir <package>`, `audit_transition_continuity_rehearsal_contract.py --package-dir <package>`, `audit_pacing_watchability_contract.py --package-dir <package>`, `audit_narrative_adjacency_contract.py --package-dir <package>`, and `audit_transition_viewer_orientation_contract.py --package-dir <package>`.
30i. Generate the edit rhythm plan with `prepare_edit_rhythm_plan.py --package-dir <package>` before asset decisions or Resolve writes, so long raw holds, missing cutaways, weak chapter variety, and flat AI-looking pacing become exact shot-purpose and trim/split/insert decision rows.
30j. Generate the creator cut plan with `prepare_creator_cut_plan.py --package-dir <package>` after edit-rhythm planning and before rhythm recut or Resolve writes, so the Skill selects hero/main/texture/utility/reject tiers, demotes weak clips, assigns creator functions, and only allows whip/rotation transitions when route-motion evidence exists; later run `audit_final_source_usage_contract.py --package-dir <package>` and `audit_creator_cut_application_contract.py --package-dir <package>` after final candidate blueprint creation.
30k. Generate the transition grammar plan with `prepare_transition_grammar_plan.py --package-dir <package>` after creator-cut planning and before rhythm recut or Resolve writes, then read `references/transition-source-coverage-contract.md` and run `audit_transition_source_coverage_contract.py --package-dir <package>`, `prepare_transition_choreography_plan.py --package-dir <package>`, `audit_transition_choreography_contract.py --package-dir <package>`, `audit_transition_motion_direction_contract.py --package-dir <package>`, `prepare_transition_execution_blueprint.py --package-dir <package>`, `audit_transition_cutpoint_contract.py --package-dir <package>`, `audit_transition_action_anchor_contract.py --package-dir <package>`, `audit_transition_sensory_continuity_contract.py --package-dir <package>`, `prepare_transition_preview_packet.py --package-dir <package> --extract-frames --update-transition-grammar`, `audit_transition_preview_quality_contract.py --package-dir <package>`, `prepare_transition_audition_packet.py --package-dir <package> --build-clips`, `audit_transition_audition_quality_contract.py --package-dir <package>`, `prepare_transition_watch_reel.py --package-dir <package> --build-reel --require-muted`, `audit_transition_watch_reel_review_contract.py --package-dir <package>`, `prepare_transition_watch_reel_watchdown_repair_plan.py --package-dir <package>`, `audit_transition_audition_visual_proof_contract.py --package-dir <package> --extract-frames`, `audit_transition_audition_role_integrity_contract.py --package-dir <package>`, `audit_transition_motion_accent_contract.py --package-dir <package>`, and `audit_transition_effect_recipe_contract.py --package-dir <package>` after transition candidate audits so every adjacent clip pair has an exact cut/dissolve/match/whip/rotation/speed-ramp/bridge-insert decision plus concrete non-generic pre-Resolve decision evidence, source-level outgoing/bridge/landing coverage, restrained Resolve keyframes/easing/envelopes, three-beat choreography, motion-direction proof, motion-accent restraint, cutpoint leave/hit/landing timing, readable outgoing/bridge-or-match/landing action anchors, sensory continuity, package-local preview/frame evidence, one ordered muted transition watch reel with sequence-level review plus `ready_no_transition_watch_reel_watchdown_repairs_needed` current-reel watchdown decisions, and muted watchable MP4 audition plus frame-delta and role-integrity proof for important boundaries.
30k1. Generate transition execution, reference candidates, reference selection, motif, bridge-sequence, bridge-sequence candidate-blueprint, transition candidate-blueprint, final transition-polish candidate plans, transition-quality, shot-boundary, motivation, pair-continuity, execution-readiness, transition-polish application, Resolve transition materialization/apply, bridge-sequence application, transition-bridge-visual-evidence, final-blueprint lineage, effect-motion application, transition-cadence, transition-microstructure, transition-scene-arc, transition-effect-palette, transition-motif-coherence, transition-visual-match, transition-source-coverage, transition-choreography, transition-motion-direction, transition-motion-accent, transition-effect-recipe, transition-cutpoint, transition-action-anchor, transition-sensory-continuity, transition-preview-packet, transition-audition-packet, transition-storyboard, transition-breathing-room, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, final-source usage, creator-cut application, rhythm-recut application, reference-scene grammar, reference-profile application, chapter-story-spine, shot-flow-continuity, and timeline-variety audits with `prepare_transition_execution_plan.py --package-dir <package>`, `prepare_transition_reference_candidates.py --package-dir <package>`, `prepare_transition_reference_selection.py --package-dir <package>`, `prepare_transition_motif_plan.py --package-dir <package>`, `prepare_bridge_sequence_plan.py --package-dir <package>`, `prepare_bridge_sequence_blueprint.py --package-dir <package>`, `prepare_transition_execution_blueprint.py --package-dir <package>`, `audit_transition_cutpoint_contract.py --package-dir <package>`, `audit_transition_action_anchor_contract.py --package-dir <package>`, `audit_transition_sensory_continuity_contract.py --package-dir <package>`, then after BGM/rhythm recut `prepare_transition_polish_blueprint.py --package-dir <package>`, `audit_transition_quality_contract.py --package-dir <package>`, `audit_shot_transition_boundary_contract.py --package-dir <package>`, `audit_transition_motivation_contract.py --package-dir <package>`, `audit_transition_pair_continuity_contract.py --package-dir <package>`, `audit_transition_execution_readiness_contract.py --package-dir <package>`, `audit_transition_polish_application_contract.py --package-dir <package>`, `audit_resolve_transition_materialization_contract.py --package-dir <package>`, `prepare_resolve_transition_apply_plan.py --package-dir <package>`, `audit_resolve_transition_apply_contract.py --package-dir <package>`, `audit_bridge_sequence_application_contract.py --package-dir <package>`, `audit_transition_bridge_visual_evidence_contract.py --package-dir <package> --extract-frames`, `audit_final_blueprint_lineage_contract.py --package-dir <package>`, `audit_effect_motion_application_contract.py --package-dir <package>`, `audit_transition_cadence_contract.py --package-dir <package>`, `audit_transition_microstructure_contract.py --package-dir <package>`, `audit_transition_scene_arc_contract.py --package-dir <package>`, `audit_transition_effect_palette_contract.py --package-dir <package>`, `audit_transition_motif_coherence_contract.py --package-dir <package>`, `audit_transition_visual_match_contract.py --package-dir <package>`, `audit_transition_source_coverage_contract.py --package-dir <package>`, `prepare_transition_choreography_plan.py --package-dir <package>`, `audit_transition_choreography_contract.py --package-dir <package>`, `audit_transition_motion_direction_contract.py --package-dir <package>`, `audit_transition_motion_accent_contract.py --package-dir <package>`, `audit_transition_effect_recipe_contract.py --package-dir <package>`, `audit_transition_cutpoint_contract.py --package-dir <package>`, `audit_transition_action_anchor_contract.py --package-dir <package>`, `prepare_transition_preview_packet.py --package-dir <package> --extract-frames --update-transition-grammar`, `audit_transition_preview_quality_contract.py --package-dir <package>`, `prepare_transition_audition_packet.py --package-dir <package> --build-clips`, `audit_transition_audition_quality_contract.py --package-dir <package>`, `audit_transition_audition_visual_proof_contract.py --package-dir <package> --extract-frames`, `audit_transition_audition_role_integrity_contract.py --package-dir <package>`, `audit_transition_storyboard_contract.py --package-dir <package>`, `audit_transition_breathing_room_contract.py --package-dir <package>`, `audit_final_cut_smoothness_contract.py --package-dir <package>`, `audit_transition_continuity_rehearsal_contract.py --package-dir <package>`, `audit_pacing_watchability_contract.py --package-dir <package>`, `audit_narrative_adjacency_contract.py --package-dir <package>`, `audit_transition_viewer_orientation_contract.py --package-dir <package>`, `audit_transition_scene_settlement_contract.py --package-dir <package>`, `prepare_transition_flow_repair_plan.py --package-dir <package> --json`, `audit_transition_reference_readiness_contract.py --package-dir <package>`, `audit_final_source_usage_contract.py --package-dir <package>`, `audit_creator_cut_application_contract.py --package-dir <package>`, `audit_rhythm_recut_application_contract.py --package-dir <package>`, `audit_reference_scene_grammar_contract.py --package-dir <package>`, `audit_reference_profile_application_contract.py --package-dir <package>`, `audit_chapter_story_spine_contract.py --package-dir <package>`, `audit_shot_flow_continuity_contract.py --package-dir <package>`, and `audit_timeline_variety_contract.py --package-dir <package>` before Resolve writes, so approved transitions and final shot choices have concrete Resolve recipes/A-B/C candidate metadata, auto-selected default transitions, BGM-hit timing, title/subtitle avoidance, selected outgoing/bridge/landing source coverage, restrained keyframes/easing/envelopes, three-beat choreography, motion-direction match proof, motion-accent rarity/restraint proof, cutpoint leave/hit/landing timing, readable action-anchor proof, sensory continuity, full boundary coverage, exact from/to pair matching, package-local recipe/handle readiness, shot-to-shot landing proof, scene-arc proof, effect-palette and motif-coherence balance, pair-level visual-match proof, local bridge-video probe/frame proof, generated preview evidence, motion-execution-aware muted watchable transition audition plus frame-delta and role-integrity proof, viewer-purpose/outgoing/bridge/landing storyboard proof, post-transition breathing-room proof, final-cut smoothness proof, row-to-row continuity rehearsal proof, reference-calibrated pacing watchability proof, narrative adjacency proof, viewer-orientation and scene-settlement proof, transition-flow repair closure, transition reference-readiness aggregation, reference-profile application proof, chapter story-spine and shot-flow proof, Resolve marker/readback payload survival, visible-effect API/manual/bridge apply paths, final-blueprint polish survival, restrained effect-motion survival, rhythm-recut main/cutaway survival, materialized 2-5 shot bridge clips, whole-film transition cadence, selected raw-source usage, movement/texture/payoff/aftertaste variety, and latest candidate-chain lineage preserved in the final candidate instead of repeated/template effects or stale active blueprints.
30l. Generate the rhythm recut candidate blueprint with `prepare_rhythm_recut_blueprint.py --package-dir <package>` after the BGM phrase candidate and before asset decisions or Resolve writes, so long raw holds are split with existing-footage cutaways while preserving transition/effect/BGM phrase metadata in a separate `rhythm_recut_blueprint/resolve_timeline_blueprint_rhythm_recut.json`. Do not replace the active blueprint unless `--update-blueprint` is explicitly approved; preflight the candidate first.
30m. When the rhythm recut candidate is approved, fork a Resolve-ready package with `prepare_rhythm_recut_apply_package.py --source-package <package> --run-preflight --output-dir <new-package>`. The new package must make the recut blueprint active, keep the source package unmodified, avoid copying stale final-render proof, and pass blueprint preflight before `prepare_resolve_apply_contract.py`.
30n. Generate `reference_style_repair_plan/reference_style_repair_plan.json` with `prepare_reference_style_repair_plan.py --package-dir <package>` after rhythm recut planning and after any blocked reference/director/final QA audit, then run `audit_reference_repair_closure.py --package-dir <package>`, `audit_transition_reference_readiness_contract.py --package-dir <package>`, `audit_transition_sequence_satisfaction_contract.py --package-dir <package>`, `audit_final_viewer_friction_contract.py --package-dir <package>`, `audit_first_draft_satisfaction_contract.py --package-dir <package>`, `prepare_unattended_repair_queue.py --package-dir <package>`, `audit_whole_film_satisfaction_contract.py --package-dir <package>`, and `audit_one_shot_autonomy_contract.py --package-dir <package>`, so style, transition-readiness, ordered muted transition watch-reel review, current-output editorial watchdown, transition-sequence-satisfaction/`blocked_transition_sequence_satisfaction`, viewer-friction, first-draft-satisfaction, `blocked_whole_film_satisfaction`, `blocked_one_shot_autonomy`, and QA gaps become executable repair rows with `executionOrder`, `commandResolved`, zero unresolved placeholders, and `postRepairCommands`; P0 rows cannot be called fixed without required artifacts plus post-repair evidence. Rerun the queue if whole-film or one-shot autonomy blocks.
31. Run `apply_asset_sourcing_decisions.py` after exact asset decisions are filled; use `--apply` only after approval evidence is complete.
32. Run `audit_delivery_package.py` and follow P0 next actions.
33. Run `audit_client_delivery_rules.py`; if it is blocked, fix the product/editorial issue before Resolve writes or final claims. If the blocker is a black/generic title moment, build a visual-polish package with scenic opening/chapter/ending video bridges and re-run the audit. If the blocker is `Resolve blueprint contains no raw portrait/square/unknown video clips in the 16:9 master`, run `prepare_orientation_repair_package.py --source-package <old-package> --output-dir <new-package>` or repair the stylefix/orientation pass so every actual video `sourcePath` is landscape or an explicitly designed insert, then re-run blueprint/client audits on the new package.
34. Run `build_resolve_timeline.py --blueprint <package>/resolve_timeline_blueprint.json` for dry-run.
35. Run `audit_resolve_blueprint.py --blueprint <package>/resolve_timeline_blueprint.json --package-dir <package>`, `audit_chapter_story_spine_contract.py --package-dir <package>`, `audit_shot_flow_continuity_contract.py --package-dir <package>`, `audit_transition_breathing_room_contract.py --package-dir <package>`, `audit_final_cut_smoothness_contract.py --package-dir <package>`, `audit_transition_continuity_rehearsal_contract.py --package-dir <package>`, `audit_pacing_watchability_contract.py --package-dir <package>`, `audit_narrative_adjacency_contract.py --package-dir <package>`, `audit_transition_viewer_orientation_contract.py --package-dir <package>`, `audit_transition_scene_settlement_contract.py --package-dir <package>`, `audit_transition_motion_accent_contract.py --package-dir <package>`, `audit_transition_effect_recipe_contract.py --package-dir <package>`, `prepare_transition_flow_repair_plan.py --package-dir <package> --json`, `audit_transition_reference_readiness_contract.py --package-dir <package>`, `audit_transition_sequence_satisfaction_contract.py --package-dir <package>`, `audit_final_viewer_friction_contract.py --package-dir <package>`, `audit_first_draft_satisfaction_contract.py --package-dir <package>`, `prepare_unattended_repair_queue.py --package-dir <package>`, `audit_whole_film_satisfaction_contract.py --package-dir <package>`, `audit_unattended_first_draft_contract.py --package-dir <package>`, `audit_one_shot_autonomy_contract.py --package-dir <package>`, and `audit_large_source_unattended_readiness_contract.py --package-dir <package>` before any Resolve write approval.
36. Run `prepare_resolve_apply_contract.py --package-dir <package>` before requesting approval for `build_resolve_timeline.py --apply`.
37. Use `--apply` only after the user approves the new Resolve project/timeline write contract, Resolve blueprint preflight is not blocked, and the delivery audit has no blockers.
38. After any `--apply`, run `audit_resolve_timeline.py` and save the report.
39. Run `prepare_resolve_render.py --package-dir <package>` to write `render_plan.json`; confirm the plan records `VideoQuality` at a high-bitrate target, normally numeric `80000` or higher for 4K long-form masters.
40. Run `audit_delivery_package.py` again; final render is allowed only when it reports `ready_for_final_render`.
41. Use `prepare_resolve_render.py --queue` or `--queue --start` only after the user explicitly approves final render queue/start.
42. Run `verify_render_delivery.py --package-dir <package> --output <final.mp4>` after the render completes. Use `--expect-subtitles burned-in`, `embedded`, or `sidecar` according to the actual subtitle delivery mode. Do not claim delivery if this report is blocked.
42a. When subtitles are expected in the MP4, run `audit_rendered_subtitle_visibility_contract.py --package-dir <package>` after `verify_render_delivery.py`. If it blocks, inspect the saved sample frames, fix the Resolve track/export/overlay issue, rerender, and rerun the audit; do not count SRT files or overlay assets as final-render subtitle proof.
42b. When opening/chapter/ending title moments are expected in the MP4, run `audit_rendered_title_visibility_contract.py --package-dir <package>` after `verify_render_delivery.py` and after title bridge/cover/title-visual audits. If it blocks, inspect the saved sample frames, fix missing/invisible/black-card/ghosted title layers in Resolve or the blueprint, rerender, and rerun the audit; do not count scenic title assets or blueprint rows as final-render title proof.
42c. When any blueprint clip has `dashboardObstructionDetected=true`, run `audit_dashboard_reframe_render.py --blueprint <package>/resolve_timeline_blueprint.json --render <final.mp4>`. Do not accept only `SetProperty` readback; require rendered source-vs-output pixel evidence with no solid black lower edge.
After `verify_render_delivery.py` passes, run `scripts/audit_visual_audio_style.py` with opening, chapter, transition, ending, and user-feedback timestamps, then run `scripts/audit_rendered_transition_proof_contract.py --package-dir <package>` so final-MP4 transition windows have frame evidence. Include `--require-clean-title`, the visual manifest, the BGM manifest, and `--audio-mode bgm_only` whenever the user requested no voiceover or BGM-led scenic sections. If either audit is blocked, fix and re-render before running or trusting `audit_client_delivery_rules.py`.
42d. After the individual final-render checks pass, run `audit_final_render_quality_bundle.py --package-dir <package> --output <final.mp4>`. It must return `finalRenderQualityBundleReady=true`, `outputMatchesRenderVerification=true`, `allRequiredReportsPassed=true`, and `claimsDaVinciLevelWithoutBundle=false`; if it blocks, regenerate the missing stale report or rerender before claiming a DaVinci-level delivery.
42e. After any user complaint about a rendered draft, run `scripts/audit_feedback_regressions.py --package-dir <package> --feedback-timestamps <label=time,...> --include-title-points`. Include exact complaint times such as `opening_title=0` or `reported_vertical_clip=7:04`. If this audit is blocked, fix the package and Skill rule/script that allowed the failure, then re-render or re-audit until it passes.
43. Run `audit_location_truth_contract.py --package-dir <package>` before long-form/client final claims. Treat `passed_with_caveats` as acceptable only when the final language is honest about visual/non-GPS route reconstruction; run `--require-verified-per-clip-location` when exact per-video geolocation is required.
43a. Run `audit_longform_delivery.py --package-dir <package>` after final render verification and location-truth QA pass. Use `--require-verified-per-clip-location` only when the user requires GPS-grade/per-clip location truth; otherwise keep route uncertainty as an explicit caveat.
44. Extract a final render contact sheet around the opening, every chapter title/transition, several mid-film subtitles, and the ending. Reject the render if these frames show black slates, generic country titles where city titles are expected, internal labels, hand/phone-obstructed title backgrounds, unreadable text, missing BGM evidence, or incoherent portrait/rotated footage.
45. Run `audit_client_delivery_rules.py` again after final render verification and before saying a client can receive it.
45a. Run `audit_bgm_audio_contract.py --package-dir <package> --audio-mode bgm_only` and `audit_final_bgm_mix_contract.py --package-dir <package>` after visual/audio QA and before story QA. Read `references/final-bgm-mix-contract.md` first when the final MP4 BGM sounds missing, quiet, or hum-like. If either audit blocks on stale BGM manifest output, stale asset-ledger localPath, missing A3 cue, audible silence, leaked A1/A2 audio, non-audible title/bridge windows, or hum-risk windows, repair the package and re-render/re-run before continuing.
45b. Run `audit_story_style_contract.py --package-dir <package> --audio-mode bgm_only` after client-rule QA. Add `--require-rendered-subtitles` when subtitles must be visible in the MP4, not merely delivered as SRT/TXT. Treat `passed_with_warnings` as not perfect; fix or explain the warning before saying the Skill can deliver unattended.
45c. Run `audit_reference_style_alignment.py --package-dir <package>` after the story contract audit when the user asks for Bilibili/Malta/creator-reference quality. If the score is below the configured threshold, revise the route structure, bridge footage, lived-in details, subtitle density, BGM support, or title/ending polish before claiming the Skill is mature.
45cc. Run `audit_director_intent_contract.py --package-dir <package>` after reference-style QA. If it blocks, revise the opening mission, chapter arc, shot pacing, caption story, BGM/no-voiceover support, or ending before saying the edit has a real director intent.
45d. Run `audit_route_texture_contract.py --package-dir <package>` after director-intent QA. If it blocks, add or relabel real bridge footage around day/place boundaries, strengthen chapter texture with transport/street/food/hotel/weather/detail clips, and re-run before title/package-integrity handoff.
45e. Run `audit_title_bridge_contract.py --package-dir <package>` after route-texture QA and before package integrity. If it blocks, regenerate scenic title bridges or repair Resolve blueprint title clips before trusting contact sheets or OCR.
45f. Run `audit_stock_aerial_closure.py --package-dir <package>` after title and route-texture audits. Add `--update-blueprint` when the final blueprint should record that search-only stock/aerial placeholders were closed. If it blocks, materialize/verify required stock assets or remove/close stale placeholders with evidence before director-polish QA.
45g. Run `audit_director_polish_contract.py --package-dir <package>` after stock/aerial closure and title/BGM/route/style audits. If it blocks, fix the missing director-polish evidence before handoff.
45h. Run `audit_package_integrity.py --package-dir <package>` after all final QA reports are regenerated. Run `audit_package_integrity.py --package-dir <package> --strict-portable` before any external handoff. If strict mode blocks, copy/materialize sidecar assets into the package or update stale blueprint/report paths, then re-run the affected audits.
45i. Run `audit_skill_maturity_contract.py --package-dir <package>` after package-integrity QA to prove the Skill's reusable safeguards cover the original complaint set, including first-assembly source-order, large-source unattended-readiness, transition-reference-readiness, transition-sequence-satisfaction, final-viewer-friction, first-draft-satisfaction, whole-film-satisfaction, one-shot-autonomy, unattended repair queue, creator-cut application, rhythm-recut application, chapter-story-spine, shot-flow-continuity, timeline-variety, transition-polish application, restrained effect-motion application, Resolve transition materialization/apply, bridge-sequence application, transition bridge visual evidence, final-blueprint lineage, transition cadence, transition microstructure, transition scene-arc, transition effect-palette, transition motif-coherence, transition visual-match, transition-action-anchor, transition-sensory-continuity, transition-motion-accent, transition-breathing-room, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, transition pair-continuity, and execution-readiness. If it blocks, fix the Skill rule/script/report that let the gap through; for orientation failures, prefer actual blueprint source-path repairs over relying only on final-render sampled frames.
45ia. Run `run_skill_release_audit.py --skill-dir <skill-dir>` after substantial Skill changes and before tagging/publishing, then run `audit_v012_baseline_regression.py --skill-dir <skill-dir>` and `audit_trip_generalization_contract.py --skill-dir <skill-dir>` directly if the aggregate report points to one of those child gates. If no real footage is available, run `run_editor_delivery_matrix.py` so fixture generation, DaVinci integration audit, Resolve writeability, Jianying/CapCut state audit, Jianying/CapCut handoff behavior, Jianying/CapCut handoff contract, Jianying/CapCut TTS/export readiness, current-audit bootstrap trapping, no-material transition/music-pacing/BGM-musicality/cover/viewer/rendered/CapCut draft traps, Resolve live-write dry-run, Resolve V1/V3/A3 delivery-structure dry-run, and Resolve render-readiness dry-run are exercised in one report; for release confidence, prefer `run_no_material_full_editor_drill.py --expected-version <tag>` so release audit, editor matrix, focused Jianying/CapCut smoke, BGM musicality smoke, final-render bundle smoke, whole-film satisfaction smoke, one-shot autonomy smoke, forward-test smoke, and Resolve export smoke evidence live in one report. When a machine is expected to have Jianying/CapCut installed, add `--require-jianying-installed` to `run_no_material_editor_smoke.py`, `run_editor_delivery_matrix.py`, or the full drill and require top-level `jianyingInstalledRequired=true`, `jianyingBlockedByMissingApp=false`, `jianyingHandoffOnlyNotGuiProof=true` until real GUI proof exists, and `jianyingClaimsTtsOrExport=false` unless a current ffprobe-readable GUI export is supplied. When Resolve live writes and settings must be proven, run `audit_resolve_writeability_state.py --json`, then run `run_editor_delivery_matrix.py --apply-resolve-all` or `run_no_material_full_editor_drill.py --apply-resolve-all`; use `run_resolve_live_write_smoke.py --apply` plus `run_resolve_delivery_structure_smoke.py --apply` plus `run_resolve_render_readiness_smoke.py --apply-resolve-settings` only when debugging one sub-proof. These apply paths require approved throwaway project/timeline writes plus readback, accepted `readbackIdentityProof`, `sourcePathsMatch`, render-readiness `resolveStructurePrerequisiteSourcePathsMatch`, and no parallel Resolve apply smokes; `--apply-resolve-all` must still not queue or start a render. When the actual Resolve export path must be proven without user footage, run `run_resolve_render_export_smoke.py --apply` separately or `run_no_material_full_editor_drill.py --apply-resolve-render-export`, then require `renderStarted=true`, `renderCompleted=true`, ffprobe-readable output, nonblank sample frames, and `claimsFinalRender=false`; when the actual high-quality export path must be proven, run `run_resolve_render_export_smoke.py --apply --quality-profile delivery-4k` or `run_no_material_full_editor_drill.py --apply-resolve-all --apply-resolve-render-export --quality-profile delivery-4k` and require `qualityProfile=delivery-4k`, `renderVideoQuality>=80000`, output width/height at least 3840x2160, output FPS at least 59, and `toolchainOnlyNoRealFootage=true`. Do not merge this queue/start render smoke into the default matrix. Use the individual `create_skill_benchmark_fixture.py`, `audit_resolve_writeability_state.py`, `audit_jianying_capcut_state.py`, `audit_jianying_handoff_contract.py`, `audit_jianying_tts_export_readiness.py`, `audit_editor_integration_contract.py`, `run_no_material_editor_smoke.py`, `run_no_material_bgm_musicality_smoke.py`, `run_no_material_one_shot_autonomy_smoke.py`, `run_no_material_forward_test_smoke.py`, `run_jianying_gui_tts_export_smoke.py`, `run_editor_delivery_matrix.py`, `run_no_material_full_editor_drill.py`, `run_resolve_live_write_smoke.py`, `run_resolve_delivery_structure_smoke.py`, `run_resolve_render_readiness_smoke.py`, `run_resolve_render_export_smoke.py`, and `prepare_jianying_handoff_package.py` scripts only when debugging one sub-step. If any release gate blocks, restore the v0.1.2 Parallel World cover/reference baseline, remove hard-coded trip defaults, fix compile/integration failures, or add explicit/derived title, country, route, Resolve-name, and BGM-mood parameters before forward-testing.
45ia1. When changing Jianying/CapCut behavior, also run `run_jianying_gui_tts_export_smoke.py --output-dir <tmp> --overwrite --json`, `prepare_jianying_gui_verification_pack.py --output-dir <tmp> --overwrite --json`, and the `fill_jianying_gui_proof_fields.py` trap through `run_no_material_full_editor_drill.py`; if the app is required, add `--require-installed` and treat `blockedByMissingApp=true` as a real blocker. Do not claim Jianying TTS/export until the proof filler or equivalent checked evidence has safely reached `completed_gui_proof`, and the post-export focused smoke has `claimsJianyingTtsOrExport=true`, `exportCountsAsGuiProof=true`, and `exportFileIsPreparedInput=false`; a verification pack with `readyForInstallThenGuiProof=true` or `readyForGuiOperator=true` is only handoff readiness, not GUI completion.
45ib. Run `audit_skill_forward_test_contract.py` after substantial Skill changes when cross-trip evidence exists. Use the latest external media intake packet, the known-good package, a separate blocked project/location-truth report, and that blocked project's recovery plan; if it blocks, fix the Skill so it does not overfit one successful trip or leave blocked projects without a next route. When no real forward-test evidence is available, run `run_no_material_forward_test_smoke.py --skill-dir <skill-dir>` as a contract-regression trap only, and keep `claimsCrossTripGeneralizationFromNoMaterial=false`. Save the report under the Skill upgrade QA folder and summarize it in the regression report before handing the Skill to another AI.
45j. Run `run_final_qa_suite.py --package-dir <package> --feedback-timestamps <label=time,...>` after the final individual audits, or when handing work to another AI/editor. Include exact user complaint timestamps such as `opening_title=0,reported_vertical_clip=7:04`. Treat the suite as the final "nothing got forgotten" gate, including the final render quality bundle audit, first-assembly source-order, large-source unattended-readiness, transition-reference-readiness via `references/transition-reference-readiness-contract.md` and `audit_transition_reference_readiness_contract.py` returning `passed` instead of `blocked_transition_reference_readiness`, final-viewer-friction via `references/final-viewer-friction-contract.md` and `audit_final_viewer_friction_contract.py` returning `passed` instead of `blocked_final_viewer_friction`, first-draft-satisfaction via `references/first-draft-satisfaction-contract.md` and `audit_first_draft_satisfaction_contract.py` returning `passed` instead of `blocked_first_draft_satisfaction`, whole-film-satisfaction via `references/whole-film-satisfaction-contract.md` and `audit_whole_film_satisfaction_contract.py` returning `passed` instead of `blocked_whole_film_satisfaction`, one-shot-autonomy via `references/one-shot-autonomy-contract.md` and `audit_one_shot_autonomy_contract.py` returning `passed` instead of `blocked_one_shot_autonomy`, unattended repair queue, rhythm-recut application, transition-polish application, effect-motion application, Resolve transition materialization/apply, final-blueprint lineage, transition cadence, transition microstructure, transition scene-arc, transition effect-palette, transition motif-coherence, transition visual-match, transition-flow repair, transition-action-anchor, transition-sensory-continuity, transition-motion-accent, transition-breathing-room, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, transition-watch-reel via `references/transition-watch-reel-contract.md`, `references/transition-watch-reel-review-contract.md`, `prepare_transition_watch_reel.py`, `audit_transition_watch_reel_review_contract.py`, and `prepare_transition_watch_reel_watchdown_repair_plan.py` returning `ready_with_transition_watch_reel`/`ready_no_important_transitions`, `passed`/`passed_no_important_transitions`, and `ready_no_transition_watch_reel_watchdown_repairs_needed`, reference-review repair, editorial-watchdown repair with `prepare_editorial_watchdown_repair_plan.py` and `ready_no_editorial_watchdown_repairs_needed`, reference-profile application, chapter-story-spine, shot-flow-continuity, and timeline-variety.
45k. Run `audit_v14_baseline_contract.py --package-dir <package>` after final QA or substantial Skill edits. Treat a pass as proof that V14's lessons, including first-assembly source-order, large-source unattended-readiness, transition-reference-readiness, final-viewer-friction, first-draft-satisfaction, whole-film-satisfaction, one-shot-autonomy, unattended repair queue, chapter-story-spine, shot-flow-continuity, final-blueprint transition-polish survival, restrained effect-motion application, Resolve transition payload materialization, apply-path proof, candidate-chain lineage, film-level transition cadence, transition microstructure, transition scene-arc, transition effect-palette, transition motif-coherence, transition visual-match, transition-action-anchor, transition-sensory-continuity, transition-motion-accent, transition-watch-reel and transition-watch-reel-review, transition-breathing-room, final-cut-smoothness, transition-continuity-rehearsal, pacing-watchability, narrative-adjacency, transition-viewer-orientation, transition-scene-settlement, reference-profile application, editorial-watchdown closure, and timeline-variety, are encoded into the Skill gates; treat a block as a Skill integration bug, not as a reason to keep generating V15/V16 drafts.
45. When the user rejects voiceover or criticizes draft quality, run `prepare_quality_recut.py --source-package <package>` before the next Resolve write. The recut must remove voiceover audio, export narration as TXT/SRT, increase caption density, keep BGM audible, insert opening/ending city aerials, and target 59.94/60fps.
46. Use web search only for current licensed music, stock footage, aerial footage, fonts, or tool documentation; record source URLs and license notes.
47. Use Computer Use only when a GUI editor has no reliable API/import-file path or a Resolve modal blocks the scripting API.

## Editor Preference

Prefer direct, file/API-based workflows:

1. FFmpeg or platform media tools for deterministic preview/final assembly.
2. DaVinci Resolve Python/Lua API when Resolve is installed and available. This is the preferred route for 20-minute final assembly.
3. FCPXML/EDL/XML import for Final Cut Pro, DaVinci Resolve, or Premiere.
4. Computer Use for CapCut/Jianying/GUI-only flows only after explaining why direct control is unavailable.

## Safety

- Original footage folders are read-only.
- Cloud vision, TTS, BGM download, stock download, and external asset use require explicit user approval.
- Local Ollama vision may run on extracted local frames, but it is not GPS truth; keep low-confidence results auditable and human-reviewed.
- Local OCR may support route review, but OCR-only place hints must stay low/medium confidence unless corroborated by visual/cloud evidence.
- Never use unlicensed music, fonts, stock footage, or aerial footage in a final delivery.
- Do not fabricate that a Tokyo aerial, BGM track, font, or license has been downloaded. Search, cite, and record it.
- Never put project slugs, random IDs, placeholder Chinese, or internal workflow labels on the opening frame.
- Never claim a customer-ready cut when the opening, chapter cards, or ending are black slates instead of approved aerial/establishing/scenic hooks with clean city/place title typography.
- Never claim a customer-ready cut when any actual Resolve blueprint video `sourcePath` ffprobe-scans as portrait, square, unknown, or unprobeable unless that exact clip is explicitly declared as a designed phone/split-screen/PiP insert with crop/matte/blur/reframe treatment and the client delivery audit passes.
- Never claim GPS-grade, exact, or verified per-video location truth from visual frame review alone; use `audit_location_truth_contract.py` to decide the allowed claim level.
- Never overwrite `confirmed_route_timeline.json` from a blocked/pending route review. Use `prepare_confirmed_route_candidate.py` or `prepare_codex_visual_confirmed_route.py` first, run `audit_confirmed_route_candidate.py`, and require explicit `--apply` approval.
- Never queue or start a Resolve render while `delivery_audit.json` has blockers, asset rows are unverified, or `resolve_audit.json` is missing.
- Keep raw route and recognition artifacts auditable.

---

## FILE: references/chapter-story-spine-contract.md

# Chapter Story Spine Contract

Use this contract after `prepare_chapter_arc_plan.py`, `prepare_edit_rhythm_plan.py`, `prepare_creator_cut_plan.py`, `audit_reference_scene_grammar_contract.py`, `audit_timeline_variety_contract.py`, `audit_transition_scene_arc_contract.py`, and `audit_reference_transition_profile_contract.py`.

Run:

```bash
python3 <skill-dir>/scripts/audit_chapter_story_spine_contract.py --package-dir <package>
```

The audit blocks when a chapter is only a title, landmark pile, stock/aerial placeholder, hard-cut chain, or transition-effect cover-up. A ready chapter must carry this spine:

- context: why the chapter matters to the viewer
- movement: how the trip physically enters or changes place
- texture: street, food, hotel, weather, waiting, sign, room, crowd, or other lived-in detail
- payoff: landmark, activity, skyline, coast, mountain, aerial, or destination reward
- aftertaste: quiet handoff, departure, night, route callback, or bridge into the next chapter

Passing requires the story spine to survive into rhythm rows, creator-cut rows, selected raw footage usage, reference scene grammar, timeline variety, transition scene arcs, and reference-transition profile balance. Effects, whip/rotation moves, or BGM hits cannot compensate for missing route movement or lived-in footage.

The script writes `chapter_story_spine_contract_audit.json` and `.md` without writing Resolve, downloading assets, queueing renders, or modifying source footage.

---

## FILE: references/opening-story-engine.md

# Opening Story Engine

Use this reference when a travel edit needs to feel closer to the four `叽叽歪歪的平行世界` videos or the Malta final, especially when the first minutes feel generic, AI-made, over-titled, or disconnected from the actual route.

## Purpose

The first three minutes decide whether a long travel film feels authored. A strong opening is not only a title card or a pretty montage. It must give the viewer a reason to watch, prove the destination visually, and then return to practical travel reality.

The Opening Story Engine checks six beats:

- viewer promise: why should the viewer keep watching?
- destination proof: can the viewer immediately tell where this trip is going?
- clean hero title: is there one readable place title on real footage, without route/date/internal clutter?
- practical arrival: does the film show airport, train, car, station, road, walking, luggage, ticket, ferry, or hotel arrival?
- lived-in texture: does the film show street, food, hotel, sign, room, weather, crowd, shop, or waiting detail before minute three?
- first handoff: does the opening transition into the first chapter with route or lived-in bridge material rather than a hard reset?

## Required Script

Run this after the first package blueprint exists and before trusting title, BGM, visual establishing, edit rhythm, or director-intent claims:

```bash
python3 <skill-dir>/scripts/prepare_opening_story_plan.py --package-dir <package>
```

The script writes:

- `opening_story_plan/opening_story_plan.json`
- `opening_story_plan/opening_story_plan.md`

It does not write Resolve, download assets, or modify source footage. It turns the first three minutes into auditable beat rows with evidence clips and decision fields.

## Acceptance Bar

Before Resolve apply:

- the first 40 seconds contain a viewer promise backed by real destination or route footage
- the first minute contains a readable destination proof clip such as aerial, skyline, coast, landmark, city, station, bridge, or street identity
- the hero title is one short city/place title on real video, not a black card or stacked route/date label
- the edit returns to practical arrival or route material before minute three
- the opening includes lived-in details before the first main chapter payoff
- the first handoff uses movement, street, hotel, food, weather, or signage evidence
- scenic/title/opening windows stay BGM-led and suppress subtitles inside the hero-title safe zone

Reject openings that:

- start with a black slate, generic country card, or cluttered route/date title
- show only disconnected scenic shots with no route proof
- spend three minutes on explanation without practical arrival footage
- use stock/aerial beauty shots while ignoring usable local route or texture clips
- expose internal labels, project names, edit status, or tool terms in visible text

## Downstream Order

Use this order for a strong first draft:

1. `prepare_footage_select_plan.py` to select the raw source pool.
2. `build_delivery_package.py` to create the initial blueprint using selected local footage.
3. `prepare_opening_story_plan.py` to verify the first three minutes have story intent.
4. `prepare_title_typography_plan.py` and `prepare_visual_establishing_plan.py` to materialize clean title and establishing evidence.
5. `prepare_audio_scene_policy_plan.py` and `prepare_bgm_selection_package.py` to keep the opening BGM-led.
6. `prepare_edit_rhythm_plan.py`, `prepare_creator_cut_plan.py`, and `prepare_transition_grammar_plan.py` to polish the selected timeline.

Do not claim a cut has Parallel World/Malta-style direction if the opening story plan is missing or if any of the six opening beats has no evidence.

---

## FILE: references/chapter-arc-engine.md

# Chapter Arc Engine

Use this reference when a travel edit needs to feel like a complete long-form vlog chapter instead of a folder-order montage.

## Purpose

`prepare_chapter_arc_plan.py` creates one row per route/chapter and checks whether that chapter has the five beats that repeatedly appear in strong Parallel World/Malta-style travel films:

- `context`: person, reaction, route purpose, or clear viewer-facing reason
- `movement`: airport, station, train, road, walking, map, ticket, luggage, ferry, or practical travel motion
- `texture`: street, hotel, food, shop, sign, weather, room, waiting, crowd, or other lived-in detail
- `payoff`: landmark, skyline, coast, mountain, activity, museum/site, aerial, or strong destination reward
- `aftertaste`: quiet observation, dusk/night, departure, window/road callback, or bridge into the next chapter

The plan does not write DaVinci Resolve, render, download assets, or modify source footage. It turns the chapter story shape into a reviewable decision artifact before edit rhythm, creator cut, transition execution, subtitle overlay, BGM, or final QA claims.

## Command

```bash
python3 <skill-dir>/scripts/prepare_chapter_arc_plan.py --package-dir <package> --json
```

Outputs:

- `<package>/chapter_arc_plan/chapter_arc_plan.json`
- `<package>/chapter_arc_plan/chapter_arc_plan.md`

## Inputs

The script reads these files when present:

- `delivery_plan.json`
- `resolve_timeline_blueprint.json`
- `opening_story_plan/opening_story_plan.json`
- `edit_rhythm_plan/edit_rhythm_plan.json`
- `creator_cut_plan/creator_cut_plan.json`
- `transition_bridge_plan/transition_bridge_plan.json`
- `reference/reference_batch_profile.json`

It can infer chapter rows from `delivery_plan.json` first, then from blueprint `chapterIndex` values when the delivery plan has no chapters.

## How To Use The Rows

Each chapter row includes:

- target timeline window
- detected beat evidence and example clips
- missing beat IDs
- local source-search hints
- owner scripts for repairs
- decision fields for selected clips, captions, BGM, transition handoff, Resolve evidence, and readback evidence

Treat missing beats as structure work, not post-render polish. Repair them with source footage first:

- `context` -> `prepare_caption_story_plan.py`
- `movement` -> `prepare_footage_select_plan.py`
- `texture` -> `prepare_creator_cut_plan.py`
- `payoff` -> `prepare_visual_establishing_plan.py`
- `aftertaste` -> `prepare_transition_bridge_plan.py`

Only after real movement/bridge evidence exists should transition grammar or execution choose whip-pan, rotation, speed-ramp, or other motion effects. If evidence is missing, use straight cuts, short dissolves, or insert real bridge footage.

## Acceptance Bar

Pass:

- `chapter_arc_plan.json` exists and status is `ready_with_chapter_arc_plan`
- every chapter row has the full decision-field set
- missing beats, if any, are assigned to owner scripts before Resolve apply
- captions are audience-facing travel-film lines, not editor/status reports
- BGM and transition handoff fields explain how the viewer moves emotionally or geographically into the next chapter

Reject:

- a chapter is only scenic shots with no movement, texture, or aftertaste
- flashy effects hide a missing boundary
- captions report workflow state such as version, QA, Resolve, export, or fixes
- the edit claims Parallel World/Malta influence without chapter-level beat rows

---

## FILE: references/pacing-watchability-contract.md

# Pacing Watchability Contract

## Purpose

`audit_pacing_watchability_contract.py` is the reference-calibrated viewing-rhythm gate. It blocks a package that passes source selection, transition, scene-flow, and final-cut checks but still feels like a flat asset dump, long raw-footage hold, or unreadable flicker montage.

Use it after these upstream reports exist:

- `edit_rhythm_plan/edit_rhythm_plan.json`
- `rhythm_recut_application_contract_audit.json`
- `timeline_variety_contract_audit.json`
- `reference_scene_grammar_contract_audit.json`
- `final_cut_smoothness_contract_audit.json`
- `final_blueprint_lineage_contract_audit.json`

## Command

```bash
python3 <skill-dir>/scripts/audit_pacing_watchability_contract.py \
  --package-dir <package>
```

The script writes:

- `pacing_watchability_contract_audit.json`
- `pacing_watchability_contract_audit.md`

It is read-only. It does not write Resolve, queue renders, download assets, or modify source footage.

## Pass Criteria

A passed report means:

- the final candidate blueprint is inside the package and readable;
- the edit rhythm plan proves a ready local reference pacing profile;
- average and median final visual shot lengths are inside the reference-calibrated target ranges;
- long non-scenic raw holds do not remain after rhythm recut;
- sub-register short clips do not form accidental flicker runs;
- each substantial chapter has at least one readable breathing, payoff, or aftertaste shot;
- upstream rhythm-recut, timeline-variety, scene-grammar, final-cut smoothness, and final-blueprint lineage gates passed.

## Blocked Means Repair

If this audit blocks, repair the edit instead of adding more effects:

- long flat shots: repair `rhythm_recut_blueprint` / `rhythm_recut_application_contract_audit.json`;
- short flicker runs: lengthen or remove unreadable micro-clips before Resolve apply;
- missing chapter breath: add a real scenic, payoff, aftertaste, or quiet texture clip from user footage;
- reference range mismatch: regenerate `edit_rhythm_plan` from the local reference profile and rebuild the latest candidate chain;
- missing upstream reports: rerun final QA in order rather than approving Resolve apply.

Rerun this audit before Resolve apply, final QA, maturity, or V14 baseline claims.

---

## FILE: references/rhythm-recut-application-contract.md

# Rhythm Recut Application Contract

Use this contract after `prepare_rhythm_recut_blueprint.py`, `prepare_transition_polish_blueprint.py`, final blueprint lineage, creator-cut application, final-source usage, and timeline-variety audits. The goal is to prove that long-shot rhythm repairs actually survived into the final candidate blueprint, not only into an advisory report.

## Command

```bash
python3 <skill-dir>/scripts/audit_rhythm_recut_application_contract.py \
  --package-dir <package>
```

Optional explicit candidate:

```bash
python3 <skill-dir>/scripts/audit_rhythm_recut_application_contract.py \
  --package-dir <package> \
  --blueprint <package>/transition_polish_blueprint/resolve_timeline_blueprint_transition_polish.json
```

## Inputs

- `edit_rhythm_plan/edit_rhythm_plan.json`
- `rhythm_recut_blueprint/rhythm_recut_blueprint_report.json`
- `final_blueprint_lineage_contract_audit.json`
- `creator_cut_application_contract_audit.json`
- `final_source_usage_contract_audit.json`
- `timeline_variety_contract_audit.json`
- best package-local candidate blueprint in this order: transition polish, rhythm recut, then active `resolve_timeline_blueprint.json`

## Pass Criteria

- Upstream rhythm, creator-cut, source-usage, lineage, and timeline-variety reports are ready or passed.
- If a rhythm recut was needed, the final candidate comes from the rhythm/transition-polish candidate chain.
- Every planned recut source has the expected `main_segment` and `cutaway_insert` `rhythmRecut` annotations in the final candidate.
- Cutaway inserts are BGM-only/video-only and do not leak source-camera audio.
- The recut report reduces average primary shot length and long-shot risk while keeping timeline duration stable.
- If no recut is needed, the edit rhythm plan has no outstanding rhythm-risk rows.
- The audit is read-only: it never writes Resolve, queues renders, downloads assets, or modifies source footage.

## Blocked Means Repair

If blocked, do not hide the problem with a rotation, whip, zoom, speed-ramp, or extra title. Rebuild the rhythm recut candidate from the latest BGM phrase/effect/transition candidate chain, run transition polish again, rerun final blueprint lineage, then rerun this contract. If the candidate is approved for the actual package, fork with `prepare_rhythm_recut_apply_package.py` before Resolve apply so stale final-render evidence is not reused.

---

## FILE: references/creator-cut-engine.md

# Creator Cut Engine

Use this reference when the user wants the edit to get closer to the four `叽叽歪歪的平行世界` videos, the Malta final, or any creator-quality long-form travel vlog. This is a non-copying editorial standard. Do not copy footage, titles, music, or narration from references.

## Purpose

The Skill already knows how to build a route-aware package. The Creator Cut Engine adds the timeline-level editorial judgment layer: choose fewer and better selected shots, assign every kept shot a function, and make transitions feel like a traveled route instead of a raw clip stack.

Run the raw-footage selection layer first when a project source folder is available:

```bash
python3 <skill-dir>/scripts/prepare_footage_select_plan.py --project-dir <project>
```

The creator cut should refine the selected timeline, not compensate for a missing source-pool triage pass.

## Shot Tiers

Classify every usable visual clip before Resolve apply.

- Hero: aerial, skyline, coast, landmark, strong human reaction, or unusually clear place identity. Use for opening, chapter payoff, cover/title background, or ending.
- Main story: route movement, arrival, street exploration, meal/activity, room view, local detail, or companion/context that moves the film forward.
- Texture bridge: station, road, vehicle window, signage, weather, food table, walking, escalator, hotel window, night street, water, skyline, or quiet ambient detail.
- Utility only: technically usable but visually ordinary; use only to patch route continuity, not as a long hold.
- Reject/review: repeated, shaky, obstructed, black, accidental, low-recognition, internal slate, or long raw footage with no route/story value.

The default bias is selective. A clip should not enter the final timeline just because it exists.

## Creator Chapter Pattern

Each chapter should contain at least three functions:

- establish: where are we now?
- movement: how did we get here or leave here?
- lived-in detail: what makes this moment feel real?
- payoff: what was worth seeing?
- aftertaste: what emotional or route residue carries into the next section?

If adjacent clips share the same function, split them with a different function before adding effects.

## Transition Rules

Prioritize real route evidence before motion effects.

Strong transition sources:

- road, train, plane, ferry, car window, taxi, airport, station, bridge, escalator, elevator
- walking direction, pan/tilt, skyline, water movement, weather, day-night shift
- signage, tickets, maps, phone navigation, hotel window, food-table reset

Allowed transition effects:

- straight cut when action or eyeline matches
- short dissolve for time, weather, mood, or day-night change
- match cut by motion, color, shape, water, road, window, or skyline
- whip-pan or rotation match cut only when both sides have clear motion/route energy
- short speed ramp only for actual movement footage such as vehicle, aerial, water, walking, or crowd flow

Reject effects that hide weak material: random spin, flash, glitch, shake, particle, repeated whoosh, template pack, or a route jump with no physical bridge footage.

After this shot-selection pass, run the pair-level transition grammar:

```bash
python3 <skill-dir>/scripts/prepare_transition_grammar_plan.py --package-dir <package>
```

Use the transition grammar rows to decide exactly how adjacent clips connect. If a row says `insert_bridge_first`, add or relabel real route footage before choosing an effect.

## Subtitle And BGM Role

No-voiceover cuts must let BGM and captions carry structure.

- Captions should sound like travel-film observations, not editor reports.
- BGM should change or breathe with sections: opening promise, city exploration, route transition, scenic payoff, ending aftertaste.
- After transition/effect candidate blueprints exist, run `prepare_bgm_phrase_blueprint.py` so section changes and transition effects are tied to candidate BGM phrase markers instead of loose notes.
- Scenic/title/transition windows should be BGM-led unless intentional ambient is approved.

## Acceptance Bar

Before calling a cut creator-like:

- The first minute has a strong visual hook and a clear destination signal.
- Every primary clip has a creator function, not only a location label.
- Weak or duplicate clips are explicitly rejected or demoted to utility.
- Every chapter has establish/movement/detail/payoff/aftertaste coverage or an explicit missing-coverage row.
- Every day/place boundary has real bridge footage before any transition effect.
- BGM phrase blueprint rows cover opening/body/transition/ending sections and every candidate transition has a phrase cue.
- Whip/rotation transitions are motivated by movement; they are not default decoration.
- The ending uses quiet route aftertaste, not a leftover clip.

---

## FILE: references/scene-flow-arc-contract.md

# Scene Flow Arc Contract

Use this contract after chapter story-spine, shot-flow continuity, timeline-variety, reference scene-grammar, transition scene-arc, and transition breathing-room reports exist.

Run:

```bash
python3 <skill-dir>/scripts/audit_scene_flow_arc_contract.py --package-dir <package>
```

This is a no-write audit. It reads the final candidate Resolve blueprint plus upstream QA reports and writes:

- `scene_flow_arc_contract_audit.json`
- `scene_flow_arc_contract_audit.md`

## Purpose

This gate prevents a technically valid edit from still feeling like an AI montage. Adjacent transitions may pass while the viewer still experiences the film as random landmarks, hard chapter jumps, or decorative motion. A reference-like travel sequence needs a scene arc:

- context or setup
- route movement
- lived-in texture
- destination payoff
- aftertaste or handoff

## Blocks

Block the package when any chapter:

- has too few visual clips to form a readable scene
- lacks movement, lived-in texture, or destination payoff
- opens on a payoff without nearby route grounding
- ends without aftertaste or a real handoff
- contains weak, placeholder, black-slate, generic, duplicate, or unclassified clips
- stacks landmark/payoff shots without movement or texture between them
- relies on title cards, effects, or transition metadata to hide missing route footage

Block chapter handoffs when:

- the outgoing chapter has no aftertaste, movement, or route texture near its end
- the incoming chapter starts with payoff imagery before grounding the new place
- a boundary becomes payoff-to-payoff, producing a tourist-slideshow jump

## Relationship To Other Gates

This gate does not replace:

- `audit_chapter_story_spine_contract.py`: proves the planned story spine exists and survives.
- `audit_shot_flow_continuity_contract.py`: proves chapter clip order is readable.
- `audit_timeline_variety_contract.py`: proves whole-film function variety.
- `audit_transition_breathing_room_contract.py`: proves transitions have readable landings.

It sits above them and verifies the viewer-facing scene arc created by their combined evidence.

## Repair

If blocked, repair the package by:

- adding or replacing clips from the footage select plan, preferring local route texture first
- inserting movement or lived-in detail between destination payoffs
- using bridge-sequence clips for day/place handoffs
- demoting utility or weak clips through creator-cut/final-source usage repair
- rerunning transition scene-arc, shot-flow, timeline-variety, scene-flow arc, unattended-first-draft, V14 baseline, maturity, and final QA

Do not fix a blocked scene-flow arc by adding more spin, zoom, whip, glitch, or speed-ramp effects. The missing unit is usually source selection, route texture, chapter structure, or aftertaste.

---

## FILE: references/shot-flow-continuity-contract.md

# Shot Flow Continuity Contract

Use this contract after chapter-story-spine, timeline-variety, reference-scene, and transition continuity gates. It proves the final candidate timeline is not only varied at film level, but also ordered inside each chapter in a viewer-readable travel-film flow.

Run:

```bash
python3 <skill-dir>/scripts/audit_shot_flow_continuity_contract.py --package-dir <package>
```

The audit is read-only. It never writes Resolve, queues renders, downloads assets, modifies source footage, or touches the source drive.

## Pass Contract

A passing package must prove:

- The selected final candidate blueprint exists inside the package and has at least three primary visual clips.
- Chapter story-spine, timeline-variety, reference-scene grammar, transition pair-continuity, and transition microstructure reports are accepted.
- Every chapter's final clip order carries movement, lived-in texture, destination payoff, and aftertaste or handoff evidence.
- Payoff shots are supported by nearby movement or texture, not dropped in randomly as effect cover.
- Aftertaste or handoff beats happen near the end of a chapter, not in the middle before more unresolved footage.
- Adjacent story beats avoid random jumps such as aftertaste returning to route setup, repeated payoffs without texture, or long title/effect/utility runs.
- Active final clips do not include rejected, utility-only, weak, placeholder, or unclassified material.
- Same-source, same-beat, and utility/title runs stay short enough that transitions cannot hide a poor shot sequence.

## Repair Guidance

If blocked, repair the actual candidate order before adding more effects. Preferred repairs:

- Move transport, walking, station, road, ferry, or map-like movement clips before landmark payoff when the route feels unearned.
- Insert lived-in texture such as streets, food, markets, hotel, signs, weather, waiting, tickets, or small human moments before or after scenic payoffs.
- Replace title/effect-only bridges with real local bridge footage or a restrained match cut.
- Move aftertaste, sunset, quiet, departure, or callback material to the end of the chapter.
- Replace active rejected, utility-only, weak, black, placeholder, duplicated, obstructed, or unclassified clips through creator-cut/source-selection repair instead of masking them with rotations or speed ramps.

Do not call a draft Parallel World/Malta-like when this gate blocks. The references use scenic openings and clean transitions, but their strength comes from ordered viewer comprehension: setup, movement, texture, payoff, and emotional landing.

---

## FILE: references/footage-select-engine.md

# Footage Select Engine

Use this reference before building the first delivery package from a large unordered travel source folder. This layer is earlier than the edit rhythm, creator cut, and transition grammar passes: it decides which raw videos deserve to enter the first assembly at all.

## Purpose

The user wants a future agent to receive 100GB+ of mixed footage and make a strong first draft without repeated correction. That requires raw-footage triage before the Resolve blueprint is built.

The Footage Select Engine turns a source folder or `media_index.json` into a machine-readable shot pool:

- hero candidates for opening, chapter payoff, cover/title background, and ending
- main story candidates for route and experience beats
- texture bridge candidates for transport, street, food, hotel, weather, signage, and daily travel details
- utility context that should be short and secondary
- repair/reject rows for portrait, square, unknown-orientation, duplicate, derived, placeholder, weak, or excluded clips

## Selection Bias

Default to selective editing. A clip should not enter the first assembly just because it exists.

The automatic score is provisional. Read
`editorial-judgment-jianying-music-contract.md` before turning any
`reject_or_review` source into a final rejection. Filenames, resolution,
stabilization, orientation, and sampled frames may rank a source for review,
but only a full-duration temporal scan plus in-motion candidate-window review
can decide that the source contains no valuable moment.

Prefer local user footage before stock or aerial fallback:

- use local skyline, transport, station, street, food, hotel-window, weather, and signage clips as bridge material
- use local landmark or scenic clips as chapter payoff when they are readable and landscape
- use stock/aerial only when local footage cannot make the place legible, and only with license evidence

Reject or demote:

- prior exports, final masters, VLOG renders, screen recordings, slates, and placeholder title cards
- raw portrait/square/unknown-orientation clips unless there is an explicit phone/PiP/reframe design
- shaky, obstructed, black, duplicate, too-short, or extremely long clips with no story value
- weak footage that would need a random transition effect to feel interesting

Do not delete source files. Keep a reversible keep/reserve/reject ledger, and
run a second-pass omission challenge against the strongest unused windows after
the rough cut. A technically imperfect clip with unique story, emotion, humor,
or route value can outrank a clean but generic scenic shot.

## Required Script

Run this after media indexing and route/location recognition, before `build_delivery_package.py`:

```bash
python3 <skill-dir>/scripts/prepare_footage_select_plan.py --project-dir <project>
```

After `build_delivery_package.py` creates a package, run the source coverage repair gate before trusting the first assembly:

```bash
python3 <skill-dir>/scripts/prepare_source_selection_repair_plan.py --package-dir <package> --project-dir <project>
python3 <skill-dir>/scripts/audit_source_selection_coverage_contract.py --package-dir <package>
```

When only a package exists, run the fallback mode:

```bash
python3 <skill-dir>/scripts/prepare_footage_select_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_source_selection_repair_plan.py --package-dir <package>
python3 <skill-dir>/scripts/audit_source_selection_coverage_contract.py --package-dir <package>
```

The script writes:

- `footage_select_plan/footage_select_plan.json`
- `footage_select_plan/footage_select_plan.md`
- `source_selection_repair_plan/source_selection_repair_plan.json`
- `source_selection_repair_plan/source_selection_repair_plan.md`
- `source_selection_coverage_contract_audit.json` / `.md`
- `raw_intake_completeness_audit.json` / `.md` after the package exists and `audit_raw_intake_completeness.py` is run

If run at project level, `build_delivery_package.py` should read the plan and sort each chapter's media pool by `selectionTier` and `selectionScore`, while dropping `reject_excluded` rows and deprioritizing repair/review rows.

## Acceptance Bar

Before first assembly:

- every active source video is represented in `selectionRows`
- every active source reaches at least 99.5% full-temporal scan coverage, and
  every candidate window is reviewed in motion with sound where applicable
- `reject_or_review` remains a recoverable review hold until its full-duration
  review, final decision, and rejection evidence are complete
- `audit_raw_intake_completeness.py` passes, proving media index, recognition report, confirmed route, and footage select agree on every active source video
- hero/main/texture/utility/reject tiers exist where the source supports them
- every row has decision fields for approved use, trim, orientation repair, BGM/caption role, Resolve implementation, and readback evidence
- chapter pools show whether movement, lived-in detail, and payoff coverage are missing
- `source_selection_repair_plan.json` closes those missing chapter functions into blocking repair rows before effects, stock/aerial fallback, rhythm, creator-cut, or Resolve apply
- vertical/square/unknown footage is marked for repair before use
- derived exports and active exclusions are blocked from first-cut selection
- the plan proves source media was triaged before stock, effects, or transition grammar are used
- after the final candidate blueprint exists, `audit_final_source_usage_contract.py` proves final raw clips still match selected hero/main/texture rows and do not reintroduce unmatched, repair, reject, or utility-dominant material
- `audit_editorial_judgment_contract.py` proves keep windows survived, high-value
  omissions were challenged, and no source file was deleted

## Downstream Order

Use the output in this order:

1. Build or refresh the package so high-score local footage is chosen first.
2. Run `prepare_source_selection_repair_plan.py` and `audit_source_selection_coverage_contract.py`; stop when blocking repair rows exist.
3. Run `prepare_edit_rhythm_plan.py` to decide pacing and cutaway needs.
4. Run `prepare_creator_cut_plan.py` to classify the selected timeline clips by creator function.
5. Run `prepare_transition_grammar_plan.py` to decide exact adjacent-pair transitions.
6. Run rhythm recut and Resolve preflight only after the above plans agree.

Do not claim the Skill can reliably make a Bilibili/Malta-style first draft if this raw-footage selection layer is missing or only run after the timeline has already been assembled.

---

## FILE: references/transition-grammar-engine.md

# Transition Grammar Engine

Use this reference when a travel cut needs better shot-to-shot flow, especially after the user says transitions still feel weak, abrupt, template-like, or unlike the Parallel World/Malta references.

## Purpose

The transition bridge plan decides what material is needed between chapters. The effect motion plan decides what motion style is allowed. The transition grammar layer decides how each adjacent pair of timeline clips should connect.

This layer prevents three common failures:

- hard jumps between places with no route evidence
- flashy effects used to hide weak footage
- repeated dissolves that make the edit feel generic

## Pair-Level Rules

For every adjacent pair of primary visual clips, identify:

- whether this is a same-scene cut, chapter boundary, title boundary, route movement, or ending transition
- whether physical bridge evidence exists: road, station, train, ferry, plane, car window, walking, signage, map, hotel window, weather, water, skyline, food table, or night/day change
- whether the two clips share a visual match: motion direction, water, road, window, skyline, food, sign, color, shape, or camera movement
- whether BGM phrasing should carry the transition
- whether captions should be suppressed because the transition overlaps a title zone
- the storyboard purpose, outgoing shot, bridge-or-motion beat, landing shot, and preview/frame evidence fields needed by `prepare_transition_preview_packet.py`, `audit_transition_preview_quality_contract.py`, and `audit_transition_storyboard_contract.py`

## Recommended Transition Types

- `straight_cut`: same scene, same activity, or clear action continuity.
- `match_cut`: shared shape, direction, object, color, water, road, window, skyline, sign, or food-table logic.
- `short_dissolve`: time, weather, mood, day-night, scenic aftertaste, or memory-like chapter change.
- `whip_pan_match`: both sides have clear pan, walking, vehicle, crowd, or route-motion energy.
- `rotation_match_cut`: both sides have circular/turning/camera-rotation energy or a strong route-motion bridge. Use rarely.
- `speed_ramp_bridge`: real vehicle, aerial, water, crowd, walking, or camera motion supports a brief ramp.
- `insert_bridge_first`: the pair has no physical route evidence; add bridge footage before effects.

## Hard Rejections

- random spin because the cut feels boring
- flash/glitch/shake/strobe/template-pack transition without story purpose
- route jump covered only by a title card
- whip/rotation across two static scenic shots
- transition effect over unreadable title typography
- source-camera voice leaking under scenic/title transition windows

## Acceptance Bar

Before Resolve apply:

- every chapter/day/place boundary has a transition grammar row
- every row has one recommended transition and one fallback
- every row has concrete non-generic pre-Resolve decision fields: `approvedTransitionType`, `fallbackTransitionType`, `storyboardPurpose`, `outgoingShotEvidence`, `bridgeOrMotionBeatEvidence`, `landingShotEvidence`, `motionDirection`, `bgmPhraseCue`, `resolveImplementation`, `previewStripEvidence`, and `frameSampleEvidence`
- whip/rotation rows cite route-motion evidence
- rows lacking physical bridge evidence are marked `insert_bridge_first`, not effect-ready
- blank or generic decisions such as `done`, missing BGM cue, missing preview/frame evidence, or motion effects without bridge evidence block V14/Skill maturity
- important day/place/title/timeline-gap/ending transitions include a ready `transition_preview_packet` and passed transition preview quality contract before approval
- transition decisions align with creator cut tiers and route texture goals

---

## FILE: references/transition-cadence-contract.md

# Transition Cadence Contract

## Purpose

`audit_transition_cadence_contract.py` is the film-level transition rhythm gate. It does not replace pair-level transition audits; it summarizes them and blocks the edit when the whole film still feels like bare concatenation, a repeated template chain, or decorative effect spam.

Use it after these upstream reports exist:

- `transition_motif_plan/transition_motif_plan.json`
- `transition_quality_contract_audit.json`
- `shot_transition_boundary_contract_audit.json`
- `transition_motivation_contract_audit.json`
- `transition_pair_continuity_contract_audit.json`
- `transition_execution_readiness_contract_audit.json`
- `resolve_transition_apply_contract_audit.json`
- `bridge_sequence_application_contract_audit.json`
- `final_blueprint_lineage_contract_audit.json`

## Command

```bash
python3 <skill-dir>/scripts/audit_transition_cadence_contract.py \
  --package-dir <package>
```

The script writes:

- `transition_cadence_contract_audit.json`
- `transition_cadence_contract_audit.md`

It is read-only. It does not write Resolve, queue renders, download assets, or modify source footage.

## Pass Criteria

A passed report means:

- every visual boundary has transition coverage;
- enough crafted transitions exist for the film length;
- motion transitions stay below the configured share and have evidence;
- repeated decorative runs stay below four;
- no single transition style dominates the film;
- important route/title/timeline-gap boundaries have materialized bridge-sequence beats;
- Resolve apply evidence is not marker-only;
- the final blueprint lineage proves the latest candidate chain survived.

## Blocked Means Repair

If this audit blocks, do not write Resolve or claim the draft is V14-quality. Repair the owner report named in `blockers`:

- bare-cut coverage: repair `transition_quality_contract_audit.json`;
- repeated-template cadence: repair `transition_motif_plan.json` or transition polish;
- unmotivated motion: repair motivation, pair-continuity, and execution-readiness rows;
- missing important bridge beats: repair bridge sequence plan/blueprint/application;
- marker-only visible effects: repair Resolve transition apply plan;
- stale candidate chain: repair final blueprint lineage and rerun later audits.

Rerun this audit after the upstream repair. A later final QA or maturity pass should treat a missing cadence audit as a Skill integration bug.

---

## FILE: references/final-cut-smoothness-contract.md

# Final Cut Smoothness Contract

Use `scripts/audit_final_cut_smoothness_contract.py` after final-blueprint lineage, transition breathing-room, scene-flow arc, shot-flow continuity, visual-match, choreography, and storyboard reports pass.

This gate exists because a package can pass many plan-level transition checks and still feel like a rough AI assembly if the active/final candidate blueprint has abrupt adjacent joins. It audits the final candidate itself.

## Run

```bash
python3 <skill-dir>/scripts/audit_final_cut_smoothness_contract.py \
  --package-dir <package> \
  --json
```

It writes:

- `final_cut_smoothness_contract_audit.json`
- `final_cut_smoothness_contract_audit.md`

## What Must Pass

- The candidate blueprint must be package-local and contain enough visual clips and adjacent boundaries to audit.
- Upstream final-blueprint lineage, transition breathing-room, scene-flow arc, shot-flow continuity, visual-match, choreography, and storyboard reports must be accepted.
- Important chapter, title, and timeline-gap boundaries need final transition metadata plus bridge, match, or breathing-room proof.
- Whip, rotation, push/slide, and speed-ramp accents must be rare, evidence-backed, and land on stable primary clips.
- Payoff-to-payoff hard jumps, weak/placeholder clips, unclassified landings, and effect-hidden title/unknown jumps are blockers.

## Repair Rules

Do not repair a blocked row by adding a flashier transition. Fix the underlying cut:

- Add or relabel physical route bridge footage: station, street, vehicle, sign, hotel window, food, weather, or walking detail.
- Replace weak or unclassified landing clips with creator-cut hero/main/texture selections.
- Use clean cut, match cut, short dissolve, or bridge insert when the two shots do not have motion energy.
- Keep rotation, whip, push, and speed-ramp accents for rare two-sided route-motion joins only.
- Give every high-intensity transition enough stable landing footage before the next title, caption, or idea.
- Rerun final-blueprint lineage, transition breathing-room, scene-flow arc, and this contract after any candidate rewrite.

## Relationship To Other Gates

- `transition_visual_match_contract` proves transition rows have visual or bridge evidence.
- `transition_choreography_contract` proves important transitions have outgoing, bridge-or-motion, and landing beats.
- `transition_breathing_room_contract` proves important boundaries land before the next idea.
- `scene_flow_arc_contract` proves chapters form readable travel arcs.
- This contract proves the final candidate blueprint did not lose those decisions and still cuts smoothly shot-to-shot.

---

## FILE: references/narration-subtitles.md

# Narration, TTS, and Subtitles

## Voiceover Style

Default voiceover language is Chinese unless the user asks otherwise. Keep it long-form travel-documentary-like:

- natural and warm
- not a tourist-guide lecture
- location-aware
- not overconfident when route recognition is uncertain
- allow short pauses around establishing shots and transitions
- preserve quiet stretches; a 20-minute film should not be wall-to-wall narration

For each chapter, write:

- one place-card line
- one voiceover paragraph
- one optional transition line into the next chapter

For a 20-minute film, the voiceover can be only a few minutes total if the footage, BGM, and natural sound carry the rest.

## TTS

Local default is macOS `say`, because it avoids cloud upload and can create audio immediately. Use cloud TTS only after explicit approval.

Use:

```bash
python3 <skill-dir>/scripts/make_voiceover_audio.py --script voiceover_script.txt --output-dir voiceover
```

For a package-level flow that also refreshes title cards and Resolve enrichment, prefer:

```bash
python3 <skill-dir>/scripts/prepare_delivery_assets.py --package-dir <package> --generate-local-voiceover
```

Omit `--generate-local-voiceover` when only title/place cards and enrichment should be prepared.

The script creates:

- `voiceover.aiff`
- `voiceover.m4a` when FFmpeg is available
- `subtitles.srt` estimated from line lengths and audio duration

If a high-quality commercial TTS is required, create a provider-specific request plan and record provider, voice, cost, and license/usage rules.

## Subtitle Rules

- Generate SRT even if timing is approximate.
- Write every final subtitle and TXT narration line for the audience, not for the editor or user. The viewer should see travel-film narration, route context, emotion, visual observation, or honest uncertainty.
- Never use final captions to report workflow state, such as "本次剪辑完成", "已经修复竖屏", "去掉了口播", "已通过 QA", "V14", "交付包", "DaVinci", "Resolve", "Codex", "SRT", "TXT", "A1/A2/A3", or "BGM-only".
- Keep each subtitle short enough for mobile reading.
- Use punctuation to create natural pauses.
- After audio is produced, retime subtitles by actual audio duration or ASR alignment.
- Burn-in subtitles only after user approves style; otherwise deliver `.srt`.
- When the user rejects voiceover, treat TXT/SRT captions as the narrative layer and do not generate local TTS.
- Keep opening, chapter, and ending title zones clean. Suppress or trim rendered subtitle overlays inside those title windows unless the user explicitly asks for captions over titles.
- For a no-voiceover long-form travel film, subtitles should be dense enough to carry route, emotion, and visual honesty. Use at least 4 cues/minute as a planning target unless a slower reference profile justifies otherwise.

Run:

```bash
python3 <skill-dir>/scripts/prepare_caption_story_plan.py --package-dir <package>
python3 <skill-dir>/scripts/audit_audience_caption_contract.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_subtitle_overlay_asset.py --package-dir <package> --update-blueprint
python3 <skill-dir>/scripts/audit_subtitle_overlay_contract.py --package-dir <package>
python3 <skill-dir>/scripts/audit_rendered_subtitle_visibility_contract.py --package-dir <package>
```

This plan and audit must exist before subtitle overlay generation or maturity claims. The plan writes `caption_story_plan/caption_story_plan.json`, `.md`, and `text_only_narration_export.txt`. The TXT export must contain only audience-facing narration/caption lines, not package metadata or policy notes. The plan records full-film and per-chapter cue targets, actual cue count, cues/minute, longest subtitle gap, title-zone suppression policy, no-voiceover/TXT/SRT policy, caption functions, rewrite decision fields, and a pass/reject rubric. If it reports `needs_caption_expansion` or `blocked_editor_facing_caption_text`, add or rewrite the SRT/TXT before rendering.

For visible-subtitle deliveries, the overlay contract must pass after overlay generation and before Resolve preflight/final QA. It proves dense SRT cues became package-local alpha overlay video files, sampled overlay frames contain non-transparent subtitle pixels, V3 blueprint clips have source audio disabled, and title zones have zero subtitle overlap unless the user explicitly allowed captions over titles.

After the final MP4 is exported, run `audit_rendered_subtitle_visibility_contract.py`. It samples subtitle cue times in the rendered MP4 and blocks if the lower-third caption area does not show visible caption pixels. This catches Resolve/export cases where the overlay asset exists but was not actually burned into the final file.

## Audio QA

Target final mix:

- voiceover intelligible over BGM
- music under narration, typically around -24 to -18 LUFS relative bed depending on content
- avoid clipping
- include short fades around chapter changes

When the user rejects voiceover or complains that scenic/opening/transition moments contain their voice, switch the planning default to `bgm_only_no_camera_voice`. Before any Resolve apply, run:

```bash
python3 <skill-dir>/scripts/prepare_audio_scene_policy_plan.py --package-dir <package> --feedback-timestamps reported_voice_at_7_04=7:04
```

Use the timestamp argument only for actual user-reported moments. The resulting plan must keep A3 BGM active, A1/A2 source or voiceover audio muted/absent, and intentional ambience disabled unless explicitly approved with a reason.

---

## FILE: references/long-form-travel-style.md

# Long-Form Travel Style

## Target

Default target is a 20-minute travel film, not a short recap. A 1-2 minute output is a failure unless the user explicitly changes the target duration. Local reference films may be 20-40 minutes, so the workflow must scale beyond short recap pacing.

Use `analyze_reference_video.py` to write `reference_analysis.json`, >=95% full-decode coverage, ordered timeline sheets, candidate-boundary sheets, whole-film audio evidence, and a contact sheet before applying its non-copying pacing assumptions to a new project. Automated scene candidates still require human classification and continuous playback around opening, phase changes, audio decisions, and ending.

Use `prepare_reference_batch_profile.py` when the user provides multiple reference videos. The generated `reference_batch_profile.json` should become the pacing/audio/sample-frame source for rhythm planning and reference-style audits.

Use Bilibili long-form travel creators such as `叽叽歪歪的平行世界` as a pacing reference, not as material to copy. The useful traits are sustained route, lived-in travel reality, chapter breathing, transport, street texture, food/waiting/weather details, natural reactions, and a watchable documentary-vlog rhythm. Do not copy titles, narration lines, thumbnails, music, or footage.

The film should feel like a real trip being reconstructed, not a montage of scenic shots. Every chapter needs a reason to exist in the route: arrival, exploration, transition, mistake, meal, weather change, landmark, night walk, hotel, train, airport, or emotional callback.

## Structure

For a 20-minute film:

- opening route promise: 35-60s
- 4-6 main chapters: usually 2.5-5 minutes each when footage supports it
- transitions: 15-45s each, using transport, street details, hotel windows, food prep, maps, signage, stations, airports, escalators, rain, night streets, or ambient cutaways
- ending: 45-75s, with callback and emotional aftertaste

For a 40-minute Malta-like reference film, expand chapter duration instead of increasing narration density. Use more natural sound, street sequences, transportation, food, waiting, map pauses, and human reaction beats.

Do not compress every place into equal time. Give more time to chapters with stronger footage, richer human moments, clearer local texture, or more important route meaning. Shorter chapters are acceptable only when they function as bridges.

## Minimum 20-Minute Shape

A normal 20-minute trip film should usually follow this shape:

- 00:00-01:00: opening route promise, best hook visuals, title typography, and route expectation
- 01:00-05:00: arrival and first city texture
- 05:00-09:00: first major place or day-one experience
- 09:00-13:00: transport, meal, hotel, street wandering, or route change
- 13:00-17:30: strongest landmark, neighborhood, or day-two/day-three chapter
- 17:30-19:15: final movement, night/morning contrast, or emotional return
- 19:15-20:00: ending callback, quiet close, credits or final title card

If source footage supports a different structure, adjust the timings, but keep the same long-form principles: route, chapters, breathing room, and lived-in transitions.

## Narration

Narration should guide, not flood:

- use sparse spoken paragraphs
- leave long stretches for natural sound and BGM
- avoid explaining what the viewer can see
- mark uncertain locations honestly
- tie every claim to actual route evidence or user-confirmed context
- leave 20-60 second stretches where only source audio, BGM, and visuals carry the film

## Visual Rhythm

Use repeated long-form patterns:

- establish place with aerial/skyline/map/title card
- enter street-level detail
- show human reaction, food, transit, weather, or waiting
- widen again before leaving the place
- transition with geography, sound, or motion

Do not use short-video pacing as the default. Avoid constant speed ramps, over-dense captions, generic beat cuts, and endless beauty shots with no route function. Let selected clips breathe when they show walking, ordering food, entering stations, checking maps, changing weather, or people reacting.

Before first assembly from unordered source media, generate `footage_select_plan/footage_select_plan.json` with:

```bash
python3 <skill-dir>/scripts/prepare_footage_select_plan.py --project-dir <project>
python3 <skill-dir>/scripts/audit_raw_intake_completeness.py --project-dir <project> --package-dir <package>
```

This plan should exist before `build_delivery_package.py` when the user expects a strong first draft from a large folder. After the package exists, the raw-intake audit should prove the index, recognition report, confirmed route, and selection rows agree on every active source video. The first assembly should use this plan to sort local footage before stock, effects, or rhythm recut are considered.

After `build_delivery_package.py`, generate `opening_story_plan/opening_story_plan.json` with:

```bash
python3 <skill-dir>/scripts/prepare_opening_story_plan.py --package-dir <package>
```

This plan should exist before title, BGM/audio, visual establishing, rhythm, or creator-cut planning. It verifies that the first three minutes have a viewer promise, destination proof, one clean hero title, practical arrival, lived-in texture, and first chapter handoff. Missing opening beats are structure blockers, not minor polish notes.

Generate `chapter_arc_plan/chapter_arc_plan.json` with:

```bash
python3 <skill-dir>/scripts/prepare_chapter_arc_plan.py --package-dir <package>
```

This plan should exist before edit rhythm, creator cut, transition execution, captions, BGM decisions, or Resolve trust. It converts each chapter into context, movement, lived-in texture, destination payoff, and aftertaste/handoff rows. Missing chapter beats must map to owner scripts before an effect or stock insert is allowed to compensate.

Generate `edit_rhythm_plan/edit_rhythm_plan.json` with:

```bash
python3 <skill-dir>/scripts/prepare_edit_rhythm_plan.py --package-dir <package>
```

This plan should exist before Resolve writes when the user wants Malta/Bilibili-style quality. It compares the current blueprint to the reference pacing profile, lists every primary visual shot, marks long raw holds and missing cutaway beats, and creates per-chapter rhythm rows. Use it to decide where to trim, split, insert transport/street/food/hotel/weather details, or keep a deliberate breathing shot.

Then generate `rhythm_recut_blueprint/resolve_timeline_blueprint_rhythm_recut.json` with:

```bash
python3 <skill-dir>/scripts/prepare_creator_cut_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_transition_grammar_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_transition_execution_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_transition_motif_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_bridge_sequence_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_bridge_sequence_blueprint.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_transition_execution_blueprint.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_bgm_phrase_blueprint.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_rhythm_recut_blueprint.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_transition_polish_blueprint.py --package-dir <package>
python3 <skill-dir>/scripts/audit_transition_quality_contract.py --package-dir <package>
python3 <skill-dir>/scripts/audit_shot_transition_boundary_contract.py --package-dir <package>
python3 <skill-dir>/scripts/audit_cover_title_contract.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_reference_style_repair_plan.py --package-dir <package>
python3 <skill-dir>/scripts/audit_reference_repair_closure.py --package-dir <package>
```

The creator cut plan must run first. It decides which clips are hero, main story, texture bridge, utility, or reject/review; assigns creator functions; and records whether any whip-pan or rotation transition is truly motivated by route motion. The transition grammar plan gives every adjacent clip pair an exact transition recommendation and fallback, the transition execution plan turns those rows into Resolve recipes, the transition execution blueprint makes those recipes visible in the candidate timeline, the transition motif plan audits the whole chain for repeated dissolves, random motion, missing BGM phrase cues, title-zone risk, or effects hiding weak route jumps, the bridge sequence plan turns important route/title/timeline-gap changes into 2-5 shot connective beats, the bridge sequence blueprint turns local bridge beats into a preflightable Resolve candidate, and the BGM phrase blueprint ties selected music sections to clip and transition cues. The rhythm recut candidate then turns the diagnosis into an executable Resolve blueprint draft without touching the original blueprint by default. It should start from the BGM phrase candidate, shorten flat holds into main segments plus existing-footage cutaways, preserve transition/effect/BGM phrase metadata, preserve the package duration, keep inserted clips video-only/BGM-led, and pass `audit_resolve_blueprint.py --blueprint <candidate> --package-dir <package>` before any `--update-blueprint` or Resolve apply. The transition polish blueprint must then add BGM-hit timing, title/subtitle avoidance, motion-proof, and restrained Resolve keyframe metadata to every final transition; the transition quality contract must prove every visual boundary is covered without random/repeated effects; and the shot transition boundary contract must prove each adjacent from/to pair has matching transition metadata instead of generic hard cuts or random rotations. The reference style repair plan converts blocked style/director/QA checks into P0/P1 repair rows with scripts and acceptance evidence.

When the candidate is approved, use a package fork before touching Resolve:

```bash
python3 <skill-dir>/scripts/prepare_rhythm_recut_apply_package.py --source-package <package> --output-dir <new-package> --run-preflight
```

The new package is the Resolve target. It should carry the active recut blueprint, package-local rewritten asset paths, no copied final-render proof, and explicit next actions for dry-run, apply contract, Resolve readback, render, and final QA.

Before Resolve apply or final QA, preserve concrete user complaints as package-level feedback probes:

```bash
python3 <skill-dir>/scripts/prepare_feedback_regression_plan.py --package-dir <package>
```

This plan should feed `opening_title=0`, `reported_vertical_clip=7:04`, `reported_voice_at_7_04=7:04`, and `opening_bgm_no_voice=0` into audio-scene policy, feedback audit, and final QA instead of relying on conversation memory.

## Aerials, Inserts, BGM, and Typography

A 20-minute delivery package must plan more than raw footage:

- aerial or establishing inserts for the main city/region, using licensed stock or approved local assets
- local texture inserts for chapter bridges: streets, stations, signs, hotel windows, food, traffic, weather, crowds, water, skyline, or train/plane movement
- BGM arcs that can sustain long sections: opening theme, city exploration bed, transition bed, emotional ending bed
- restrained cinematic title cards and place cards with special fonts only when license status is recorded
- subtitles that support the voiceover and do not crowd the frame

When legal assets are not available yet, write exact search/sourcing tasks and keep final render blocked until licensing is verified.

## Route Honesty

If GPS is missing and location recognition is uncertain, do not pretend every clip has exact location truth. Use confidence language in plans and narration:

- confirmed by metadata, folder, OCR, or user decision
- visually likely
- route scaffold only
- needs human review

The edit can still be watchable with a scaffolded route, but the delivery report must state what was confirmed and what was inferred.

## Acceptance Bar

The package is not long-form ready unless it has:

- `long_form_structure.md`
- target duration around 20 minutes unless the user changes it
- an explicit rejection of 1-2 minute short-video pacing
- coverage ratio in `resolve_timeline_blueprint.json` is high enough to support the target duration
- `resolve_timeline_blueprint.json.longFormCoverage` explains initial selected footage, opening/transition/ending fill, final covered seconds, and target seconds
- `footage_select_plan/footage_select_plan.json` proves source media was scored and selected before first assembly
- `reference/reference_batch_profile.json` exists when multiple reference videos are supplied, and exposes aggregate pacing/audio/sample-frame targets
- `opening_story_plan/opening_story_plan.json` proves the first three minutes contain viewer promise, destination proof, clean hero title, practical route/arrival material, lived-in texture, and first handoff
- `chapter_arc_plan/chapter_arc_plan.json` proves each chapter has context/movement/texture/payoff/aftertaste rows, or assigned owner-script repairs for missing beats
- `transition_execution_plan/transition_execution_plan.json` proves adjacent-pair transitions have Resolve-ready recipes and no bridge-missing row is hidden behind an effect
- `transition_execution_blueprint/transition_execution_blueprint_report.json` proves transition recipes were materialized as candidate blueprint metadata before Resolve apply
- `transition_motif_plan/transition_motif_plan.json` proves the whole transition chain avoids repeated/template defaults and has BGM/title-zone/repair evidence
- `bridge_sequence_plan/bridge_sequence_plan.json` proves important route/title/timeline-gap transitions have 2-5 shot bridge beats or owner-script repairs
- `bridge_sequence_blueprint/bridge_sequence_blueprint_report.json` proves local bridge beats were materialized into a non-destructive candidate blueprint before Resolve apply
- `effect_motion_blueprint/effect_motion_blueprint_report.json` proves restrained title/transition motion rows were materialized into candidate clip metadata before Resolve apply
- `bgm_phrase_blueprint/bgm_phrase_blueprint_report.json` proves selected music was materialized into phrase rows, clip annotations, and transition cues before rhythm recut or Resolve apply
- `rhythm_recut_blueprint/rhythm_recut_blueprint_report.json` proves long-shot recuts started from the BGM phrase candidate and preserved transition/effect/BGM phrase metadata
- `transition_polish_blueprint/transition_polish_blueprint_report.json` proves final transitions have BGM-hit timing, title/subtitle avoidance, motion-evidence checks, and restrained keyframes before Resolve apply
- `transition_quality_contract_audit.json` proves the transition-polish candidate covers every visual boundary with BGM-hit/title-safe/BGM-only evidence and no repeated/template effects
- `shot_transition_boundary_contract_audit.json` proves each adjacent visual boundary maps to the correct from/to transition row with BGM-hit, title-safe, BGM-only, and motion-evidence checks
- `cover_title_contract_audit.json` proves the cover/hero title follows the high-recognition background, oversized destination title, short English/place subtitle, clean 16:9 formula
- `reference_style_repair_plan/reference_style_repair_plan.json` proves blocked reference/director/QA style gaps become executable repair rows before another Resolve write
- `reference_repair_closure_audit.json` proves P0 style repair rows have required artifacts plus post-repair evidence before another Resolve or final-quality claim
- chapter time allocations
- transition plan between chapters/days
- feedback regression plan preserving known rejected timestamps before final render QA
- route-aware clip selection blueprint
- BGM plan that can sustain long sections
- aerial/establishing-shot plan or approved assets for major cities/regions
- typography and subtitle style plan
- narration density check proving the voiceover is not flooding the film
- route honesty notes for uncertain location recognition
- DaVinci timeline blueprint for actual assembly
- final render verification after export, including duration, resolution, audio, sampled frames, black-frame scan, and subtitle evidence

---

## FILE: references/homeward-flight-pov-style.md

# Homeward Flight POV Style

Use this profile when a trip chapter follows a practical departure chain such as hotel to car to airport to gate to aircraft. It was distilled from a complete review of a user-provided 6:13 Urumqi-to-Hongqiao homeward film. It is a non-copying story and transition profile, not a template to reproduce shot for shot.

## Review Evidence

- The source was reviewed from opening through ending, including one-second timeline strips, continuous playback, full audio evidence, and before/after frames around every broad boundary candidate.
- Full-decode evidence covered 11,207 of 11,207 proxy frames.
- Human review confirmed about 35 editorial boundaries and 36 shots: average 10.38 seconds, median 10.05 seconds, p10 3.07 seconds, and p90 17.87 seconds.
- About 27 of 35 boundaries used the repeated Jianying `向上` transition, as confirmed by the user who made the edit. That repetition is an observed weakness, not a target.
- The reference relied on source speech/ambience and had no convincing authored BGM bed, viewer-caption system, or clean destination title. Those omissions must not override this Skill's BGM-only, viewer-caption, and clean-title requirements.

## Story Grammar

Build the chapter as an understandable task chain. The viewer should always know the current place, current practical action, and next destination.

| Phase | Useful visual anchor | Viewer purpose |
| --- | --- | --- |
| Leave | room door, suitcase, elevator button | prove departure has begun |
| Handoff | lobby, loading luggage, vehicle door | move from private space to transport |
| Travel | road direction, window motion, vehicle display | compress distance without losing orientation |
| Arrive | airport exterior, parking, trolley | make the location change legible |
| Process | check-in, luggage, security, escalator | turn ordinary logistics into forward progress |
| Threshold | gate sign, boarding pass, jet bridge | show that the route is nearly complete |
| New state | aircraft seat, window, settled luggage | close on a changed state, not an arbitrary last clip |

Prefer action continuity over effect continuity. Hands, luggage, doors, screens, signs, escalators, walking direction, and thresholds are stronger joins than decorative transitions.

## Opening And Ending

- An action-first cold open is allowed: begin on leaving, packing, or a door opening rather than a generic montage.
- Preserve the existing clean-title contract. Place one destination/route title over a high-recognition establishing image within the first 6-12 seconds; never stack a second title, date, route debug text, or ghosted duplicate.
- Keep subtitles out of the title zone and give the title at least 1.2 seconds without competing viewer text.
- End after the traveler reaches a new state, then hold 3-6 seconds of stable visual aftertaste when suitable footage exists. A seat/window/arrival image is stronger than an abrupt cut during movement.

## Transition Policy

The reference's slice effect explains why a phase jump can feel energetic, but its 77 percent repetition is too template-like. Apply this restrained mix instead:

- Clean cut, action match, direction match, or hidden cut: 55-70 percent.
- Physical bridge or short dissolve: 15-30 percent, especially for emotional or location changes.
- Motion accent: no more than 18 percent of visual boundaries, never adjacent, and leave at least five stable boundaries before repeating the family.
- For Jianying, use the user-confirmed free native `向上` transition for about 0.34-0.42 seconds only when the outgoing and landing shots support upward travel or when a major route phase changes on a BGM hit.
- `向下`, `向左`, `向右`, spin, zoom, and split effects are not a palette to cycle through. Direction must follow the two shots.
- Run the native entitlement audit on the current machine even when an asset was free in the verified `pyJianYingDraft==0.3.0` catalog.
- If motion evidence, BGM-hit alignment, title safety, or a stable landing is weak, downgrade to a clean match cut or `叠化`.

Never use a spin, zoom, flash, or slice effect to hide two unrelated weak shots. Never place a motion accent across a clean hero title, subtitle collision, or source-voice leak.

## Audio And Captions

- For a BGM-only brief, mute every camera clip, keep Jianying TTS disabled, and deliver viewer-facing TXT/SRT text only.
- Choose real musical BGM with a clear phrase grid. Use a firmer opening cue for departure, a quieter travel/process middle, and a soft arrival/aftertaste phrase when the music supports it.
- Cut important route-phase changes on a phrase boundary or clear BGM hit. Do not cut every beat.
- Captions describe the travel experience for the audience. They must never report what the editor changed, removed, checked, or delivered.
- Use captions to clarify only the route turns that are not already obvious from signs and action. Keep scenic and title shots visually quiet.

## Jianying Application

Start from `examples/jianying-homeward-pov-edit-spec.example.json` after replacing every placeholder path with selected media, generated clean-title media, real BGM, and viewer SRT. The example intentionally uses one `向上` accent across seven boundaries, two soft dissolves, muted source clips, a full BGM bed, and TTS disabled.

Before final export, require:

1. Native free-asset entitlement audit passes.
2. Motion accents remain at or below 18 percent and are not adjacent.
3. Every motion accent has two-sided movement, a route-phase reason, a BGM hit, and at least 0.8 seconds of stable landing footage.
4. The full title is clean at rendered pixels and viewer subtitles do not overlap it.
5. Source voice is absent for BGM-only delivery, BGM is musical rather than a hum/tone, and a human listen passes.
6. The final exported film is watched from beginning to end; synthetic or draft evidence cannot claim final taste.

## Non-Copying Contract

Learn the task-chain clarity, action anchors, transport compression, threshold shots, and state-change ending. Do not copy the original footage, exact boundary order, repeated slice pattern, speech, branding, or any creator-specific title/music. Preserve stronger existing Skill rules when the reference omits BGM, titles, captions, scenic bridges, or audience polish.

---

## FILE: references/music-stock-fonts.md

# Music, Aerials, Stock, and Fonts

## Search Policy

Use web search for current assets whenever the package needs material not already in the user's footage. Record source URLs, license notes, price/free status, and attribution requirements.

Never claim an asset is usable in final delivery until its license is checked.

Current source guidance from the 2026-06-28 web check:

- Bilibili creator-space references for 影视飓风 (`https://space.bilibili.com/946974`, official site `https://www.ysjf.com/`) and 叽叽歪歪的平行世界 (`https://space.bilibili.com/405004967/`) are style anchors only; do not copy footage, music, titles, or narration.
- Mixkit remains the preferred first-pass free BGM/stock source because its music (`https://mixkit.co/free-stock-music/`) and license (`https://mixkit.co/license/#musicFree`) pages can be recorded in the package.
- Pixabay Music (`https://pixabay.com/music/`) can be used, but keep the exact track URL, license summary URL (`https://pixabay.com/service/license-summary/`), and download/license certificate evidence. Pixabay's own FAQ (`https://pixabay.com/service/faq/`) warns that some music can still trigger automated Content ID claims even when legal to use.
- A private/nonprofit draft still uses license-friendly sourcing in this Skill so future public/client deliveries do not inherit avoidable copyright or Content ID risk.

Run:

```bash
python3 <skill-dir>/scripts/build_asset_ledger.py --delivery-plan <package>/delivery_plan.json --output-dir <package>/asset_ledger
```

The ledger is the source of truth for final delivery. BGM and aerial/stock rows must have a selected URL/local path and verified license status before final render.

After the ledger exists, run:

```bash
python3 <skill-dir>/scripts/prepare_asset_sourcing_packet.py --package-dir <package>
```

The sourcing packet is the working packet for selecting exact assets. It must include official license URLs, provider search URLs, price/free/subscription status, attribution requirements, selected asset URL, local path after download/import, and approval evidence. A search URL or license homepage is not enough by itself; every final asset must be an exact selected asset with a verified license row in the ledger.

Then run:

```bash
python3 <skill-dir>/scripts/prepare_bgm_sourcing_brief.py --package-dir <package>
```

This brief narrows BGM work into a usable travel-film search packet. It must include Mixkit/Pixabay-first searches, paid-library fallbacks, chapter mood buckets, continuous-bed/opening/transition/ending section plans, exact decision fields, and a pass/reject rubric. A missing BGM complaint is not closed until this brief exists and either a verified BGM row is recorded or the brief clearly lists the next exact asset-selection work.

Then run:

```bash
python3 <skill-dir>/scripts/prepare_bgm_selection_package.py --package-dir <package>
```

This package proves the selected music can actually ship: the final BGM bed must be local, license-traceable, long enough for the film, referenced by the active Resolve blueprint, explicitly auditioned as real music, marked non-procedural and non-tone, Content-ID checked, section-fit approved for opening/body/transitions/ending, and rebuildable from local source tracks through `build_bgm_bed.py`. A provider search URL or license homepage is not enough; the package must expose exact candidate rows, decision fields, track manifest, build command, and next BGM/audio plus musicality contract audits.

Record the BGM phrase blueprint as a required later step. After transition and effect candidate blueprints exist, read `bgm-phrase-blueprint-engine.md` and run:

```bash
python3 <skill-dir>/scripts/prepare_bgm_phrase_blueprint.py --package-dir <package>
```

This blueprint step turns the selected bed into section/phrase/transition-cue metadata. A BGM complaint is not closed until opening/body/transition/ending windows, clip annotations, timeline markers, and per-transition BGM cue rows exist in a non-destructive candidate blueprint.

After phrase rows exist, read `bgm-musicality-contract.md` and run `audit_bgm_musicality_contract.py`. A BGM complaint is still open if the selection package lacks a positive audition decision, provider/music identity, non-procedural/non-tone flags, section-fit notes, or Content-ID check, or if the selected bed is a sine tone, hum, buzz, silence, placeholder, one-band audio, flat dynamics, unnamed/untraceable music, or missing opening/body/transition/ending phrase coverage.

Then run:

```bash
python3 <skill-dir>/scripts/prepare_transition_bridge_plan.py --package-dir <package>
```

This plan narrows transition and stock-footage work into usable boundary rows. It must include local-footage-first search hints, licensed stock/aerial fallback searches, exact license/provider URLs, BGM-only/no-camera-voice audio policy, subtitle title-zone policy, selected-clip decision fields, and existing Resolve bridge evidence when available. A day/place transition complaint is not closed until each boundary has a selected local bridge clip or a verified licensed fallback and `audit_route_texture_contract.py` can prove the bridge is on the actual timeline.

Then run:

```bash
python3 <skill-dir>/scripts/prepare_visual_establishing_plan.py --package-dir <package>
```

This plan narrows city aerial, landmark, and establishing-shot work into usable opening/chapter/ending rows. It must include local-footage-first search hints, trip-derived famous-place/landmark hints, licensed stock/aerial fallback searches, exact provider/license URLs, title typography evidence, existing timeline evidence, BGM-only/no-camera-voice policy, and selected-asset decision fields. A missing-aerial or generic-opening complaint is not closed until the opening, each chapter establishing row, and the ending have local scenic evidence or a verified licensed fallback and the actual Resolve blueprint/title bridge evidence can be audited.

Then run:

```bash
python3 <skill-dir>/scripts/prepare_effect_motion_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_effect_motion_blueprint.py --package-dir <package>
```

This plan narrows effect work into restrained opening/chapter/ending title reveal rows and day/place transition motion rows. Then the blueprint script materializes those rows as non-destructive candidate metadata. It must tie each motion row to title typography, transition bridge, visual establishing, and blueprint `effectPlan` evidence; record exact implementation/readback decision fields; and reject glitch, random spin, flash, shake, particle, logo-reveal, or generic template-pack effects. Motivated whip-pan or rotation match cuts are allowed only when real route-motion footage supports the boundary. A client delivery cannot be a bare concatenation, but motion should support real route footage rather than hiding weak BGM, missing bridges, duplicate titles, or wrong location evidence.

For shot-to-shot decisions, run `prepare_transition_grammar_plan.py` after creator-cut planning. Its rows decide exact adjacent-pair transitions before effect choices are implemented in Resolve.

Then run:

```bash
python3 <skill-dir>/scripts/prepare_audio_scene_policy_plan.py --package-dir <package>
```

This plan turns BGM/no-voiceover work into exact scene-window rows before Resolve writes. It must prove opening/title/visual-establishing/transition/effect/feedback windows are covered by ready A3 BGM, contain zero accidental A1/A2 source-camera or voiceover leakage, and preserve user complaint timestamps such as `reported_voice_at_7_04=7:04` as reusable regression probes. Selecting or downloading music is not enough if the scene windows can still carry the user's voice.

## BGM

For Japan/Tokyo footage, default mood:

- calm, spacious, melodic
- light piano, ambient synth, soft strings, subtle city pulse
- avoid overused high-energy vlog tracks unless user asks

Search query examples:

- `licensed cinematic Japan travel piano ambient BGM`
- `royalty free Tokyo travel documentary music license`
- `Artlist Japan travel documentary ambient`
- `Epidemic Sound Tokyo travel calm ambient`
- `Pixabay Music Japanese travel cinematic license`

## Aerial and Establishing Shots

For Tokyo, useful establishing targets:

- Tokyo Tower
- Shibuya crossing
- Shinjuku skyline
- Tokyo Skytree
- Sumida River
- Tokyo Station
- Asakusa/Senso-ji

Search query examples:

- `licensed Tokyo Tower aerial 4K stock footage`
- `Tokyo skyline aerial 4K royalty free`
- `Shibuya crossing timelapse licensed stock video`
- `Tokyo Skytree drone stock footage license`

If drone footage is legally restricted in a location, prefer licensed stock from professional libraries or high-rise/skyline establishing shots instead of pretending to fly a drone.

Do not wait until final QA to decide the city signal. `prepare_visual_establishing_plan.py` should be generated before asset decisions so the editor knows which row needs local footage, which row can use a verified stock/aerial fallback, and which exact famous-place hints are appropriate for the selected trip. The hints may include known landmarks for common cities such as Tokyo, Osaka, Hong Kong, Macau, Paris, or London, but they must be treated as selectable hints derived from the current route text, never as defaults that contaminate another trip.

## Transition Bridge Assets

Use the user's footage first. Search for station platforms, train or road windows, airport movement, taxi/metro shots, street signs, hotel windows, convenience stores, food/table details, weather, skyline, and quiet walking texture around the same chapter boundary before looking online.

Only use stock/aerial fallback when local footage cannot explain the route change. Good fallback queries are generated by `prepare_transition_bridge_plan.py`, but they should follow this shape:

- `<next city or region> station train window travel stock footage license`
- `<next city or region> skyline street ambience 4K stock video license`
- `<next city or region> airport transfer street signage travel video license`
- `<next city or region> food market hotel window travel detail stock footage`

Every fallback clip needs exact selected asset URL, license URL, local path after download, approval evidence, and a note explaining why local footage was insufficient. Do not use a stock search result as if it were already a selected/downloaded bridge clip.

## Fonts and Typography

For Japan-themed edits, prefer restrained cinematic typography:

- place cards: Hiragino Mincho ProN, Yu Mincho, Noto Serif CJK, Shippori Mincho
- subtitles: Hiragino Sans, Noto Sans CJK, Source Han Sans
- map labels: Noto Sans CJK or system sans

If a font is not installed, search for a licensed source and record the license. Do not bundle commercial fonts without permission.

Treat generic font fallback as unverified. For example, if `fc-match` returns Verdana for Noto CJK or Shippori Mincho, the requested style is not actually available; choose an installed family, download a licensed open font, or record an approved fallback before final render.

Before generating or trusting title bridge media, run:

```bash
python3 <skill-dir>/scripts/prepare_title_typography_plan.py --package-dir <package>
python3 <skill-dir>/scripts/audit_cover_title_contract.py --package-dir <package>
```

This plan must prove the opening has one clean hero title, no secondary city/date/route label behind it, no rendered subtitle overlay in the title zone, verified render-only system font or licensed font evidence, and scenic/video background evidence. The cover title contract must additionally prove the reference-style formula: high-recognition scenic background, oversized destination title, short designed English/place subtitle, clean 16:9 frame, and no route/date/project clutter. If either report blocks, regenerate scenic title bridges or repair the font/title manifest before final render.

## Visual Packaging

Use typography for:

- opening title
- day cards
- place cards
- route/map labels
- subtitle burn-in style

Keep route transitions understated: map line, ambient street insert, station/vehicle movement, or match cut by color/motion.

Before trusting effects, run:

```bash
python3 <skill-dir>/scripts/prepare_effect_motion_plan.py --package-dir <package>
python3 <skill-dir>/scripts/prepare_effect_motion_blueprint.py --package-dir <package>
```

Use effects only for subtle support:

- title reveals: short fade, tiny scale settle, or gentle dissolve
- transitions: match cut by direction/color, route marker, or short dissolve over real bridge footage
- ending: music-tail fade and scenic breathing room

Reject effects that feel like template overlays or short-video packs. If the cut lacks BGM, route bridges, title cleanliness, or real establishing footage, fix those upstream assets instead of masking the problem with motion graphics.

---

## FILE: references/final-bgm-mix-contract.md

# Final BGM Mix Contract

Use this after `verify_render_delivery.py`, `audit_bgm_audio_contract.py`, and `audit_bgm_musicality_contract.py` when the exported MP4 must prove that BGM survived the final render.

## Command

```bash
python3 <skill-dir>/scripts/audit_final_bgm_mix_contract.py --package-dir <package>
```

The audit writes:

- `final_bgm_mix_contract_audit.json`
- `final_bgm_mix_contract_audit.md`

## What It Blocks

- final MP4 files with no audio stream or missing inferred render
- final renders where BGM is only present in manifests, Resolve rows, or source beds but is quiet/missing in the MP4
- opening, title, scenic bridge, transition, or ending windows with inaudible BGM
- final mixes that collapse into hum, sine-like tone, one-band audio, or mostly silent beds
- packages that skipped the upstream BGM/audio or BGM musicality contracts

## Repair Order

1. Re-run `audit_bgm_audio_contract.py` and `audit_bgm_musicality_contract.py`; fix upstream BGM manifest, A3 cue, asset ledger, or source-bed musicality blockers first.
2. Inspect the `sampleWindows` and `summary.nonAudibleFocusWindows` rows to find the quiet title/bridge/scenic sections.
3. Repair Resolve audio routing or BGM bed duration so the A3 music bed covers the full render and focus windows.
4. If `summary.humRiskWindowRatio` is above the accepted threshold, replace the bed with real named music or rebuild the bed from approved local music tracks.
5. Re-render the MP4, then rerun this audit before final QA, V14 baseline, Skill maturity, or external handoff.

## Safety

This audit only reads the final MP4, package JSON, and Resolve blueprint. It decodes short audio windows with ffmpeg and does not write Resolve, queue renders, download assets, or modify source footage.

---

## FILE: references/bgm-musicality-contract.md

# BGM Musicality Contract

Use this after `prepare_bgm_selection_package.py`, `prepare_bgm_phrase_blueprint.py`, and `audit_bgm_audio_contract.py` when a travel film must feel music-led rather than merely contain audible audio.

## Command

```bash
python3 <skill-dir>/scripts/audit_bgm_musicality_contract.py --package-dir <package>
```

After changing BGM selection, BGM fixture generation, music-pacing rules, or release gates, also run:

```bash
python3 <skill-dir>/scripts/run_no_material_bgm_musicality_smoke.py --output-dir /tmp/travel-video-studio-bgm-musicality --overwrite --json
```

That no-material smoke must surface `goodBgmMusicalityPassed=true`, `badBgmMusicalityTrapBlocked=true`, `badBgmMusicalityRejectedAsHumTone=true`, `humanListenStillRequiredForFinalBgm=true`, and `claimsFinalBgmMusicality=false`. It proves the Skill still rejects hum/tone placeholders and still requires a human listen pass before final BGM taste claims.

The audit writes:

- `bgm_musicality_contract_audit.json`
- `bgm_musicality_contract_audit.md`

## What It Blocks

- sine tones, hums, buzzes, silence, placeholders, and procedural test beds that can pass simple audibility checks
- BGM manifests without named, traceable music rows
- BGM selection packages without positive audition evidence, provider/music identity, explicit non-procedural/non-tone decisions, Content-ID check, or opening/body/transition/ending fit notes
- selected beds without opening/body/transition/ending phrase coverage
- one-band audio, flat dynamics, clipped audio, or mostly silent beds
- transitions that are not tied to BGM phrase cues when a phrase blueprint exists

## Repair Order

1. Replace hum/tone/procedural beds with a real local music track or a built bed from traceable local tracks.
2. Fill the BGM selection decision with provider, music identity type, positive audition result, audition notes, structure notes, opening/body/transition/ending fit notes, explicit `isProceduralGenerated=false`, explicit `isPlaceholderTone=false`, and Content-ID risk check.
3. Rebuild the full-duration A3 bed with `build_bgm_bed.py` when multiple source tracks need crossfades.
4. Rerun `prepare_bgm_selection_package.py`, then `prepare_bgm_phrase_blueprint.py`.
5. Rerun `audit_bgm_audio_contract.py` and this musicality audit before Resolve apply or final QA.
6. After the final MP4 exists, read `final-bgm-mix-contract.md` and run `audit_final_bgm_mix_contract.py`; do not treat source-bed musicality as proof that the exported film actually has audible, non-hum BGM.
7. If this audit passes with warnings, do a human listen pass before claiming reference/Malta-quality delivery.

## Safety

This audit only reads package JSON and decodes the selected BGM bed through ffmpeg. It must not download music, write Resolve, queue renders, or modify source footage.

---

## FILE: references/final-viewer-friction-contract.md

# Final Viewer Friction Contract

Run this contract after final technical/style reports, `transition-reference-readiness-contract.md`, and `transition-sequence-satisfaction-contract.md` exist, and before `first-draft-satisfaction-contract.md`, `whole-film-satisfaction-contract.md`, unattended repair queue, final QA handoff, V14 baseline claims, Skill maturity claims, or release.

## Required Command

```bash
python3 <skill-dir>/scripts/audit_final_viewer_friction_contract.py \
  --package-dir <package> \
  --json
```

The only passing status is `passed`. The blocked status is `blocked_final_viewer_friction`.

## Purpose

This is an aggregation gate for viewer-facing roughness. It does not replace watching the whole film, but it prevents a technically valid export from hiding unresolved viewer problems across title, BGM, captions, source selection, story spine, transitions, reference fit, route texture, and editorial watchdown.

## What It Blocks

- missing or blocked final render verification
- weak opening/title proof, ghosted/stacked titles, route/date clutter, or missing title frame evidence
- workflow/report-like subtitles instead of viewer-facing travel text
- hum/tone/silence/voice leakage instead of musical BGM-only scenic sound
- sampled-folder or filename-order cutting from large unordered sources
- weak creator-cut source use, flat pacing, or chapter landmark stacks
- rough transitions, missing bridge/landing proof, repeated high-intensity effects, or marker-only visible transitions
- reference/Malta/Parallel World analysis that was not applied to real package artifacts
- route texture gaps and an unclosed whole-film editorial watchdown

## Required Evidence

Every open row must include:

- viewer symptom
- source report and current status
- owner script
- command
- required artifact
- acceptance evidence
- forbidden workaround

If this contract blocks, repair via the listed owner scripts and rerun the source audits, transition reference-readiness, transition sequence satisfaction, this contract, first-draft satisfaction, unattended repair queue, whole-film satisfaction, final QA, V14 baseline, and Skill maturity. If whole-film satisfaction blocks, rerun the unattended repair queue to expand its repair rows.

## Safety

The script is read-only. It must not write Resolve, queue renders, download external assets, modify source footage, or mutate a source drive.

---

## FILE: references/whole-film-satisfaction-contract.md

# Whole Film Satisfaction Contract

Use `scripts/audit_whole_film_satisfaction_contract.py` after render verification, editorial watchdown, final viewer friction, first-draft satisfaction, transition sequence satisfaction, reference/style, director, and unattended repair queue reports exist.

Run it before final QA, V14 baseline, Skill maturity, release/handoff claims, or telling a user that the Skill can produce a reference-level first serious draft without more feedback.

```bash
python3 <skill-dir>/scripts/audit_whole_film_satisfaction_contract.py --package-dir <package> --json
```

## What It Proves

The contract verifies the film as one viewer experience, not a collection of isolated passes:

- current final MP4 is verified and is the file being judged
- opening has promise, destination signal, clean hero title, BGM-only scenic tone, and title-zone subtitle avoidance
- chapters have context, movement, lived-in texture, payoff, and aftertaste/handoff
- rhythm avoids AI-looking long holds, short flicker runs, and repetitive shot roles
- BGM is musical, traceable, and not replaced by hum/tone/source-camera audio
- captions are audience-facing, dense, and title-safe
- transitions pass as an ordered muted viewer sequence, have rendered proof, and do not rely on random whip/rotation/template effects
- reference learning is actually applied to opening, pacing, transitions, captions, BGM, route texture, and ending
- director intent, route texture, and director polish are proven by current reports
- editorial watchdown is closed for the current output path
- final viewer friction, first-draft satisfaction, and unattended repair queue have zero open rows

## Blocking Status

`blocked_whole_film_satisfaction` means the package is not ready for final QA, V14, Skill maturity, release, or handoff.

Do not bypass this by saying all individual technical audits passed. The point is to catch the common failure where parts are valid but the whole film still feels like an AI assembly.

## Repair Rule

Every open row must name:

- source report
- viewer symptom
- owner script
- required artifact
- command
- acceptance evidence
- forbidden workaround

Repair in this order when possible: final output, opening/title, chapters/source/rhythm, BGM/captions, transitions, reference fit, director/route texture, editorial watchdown, final viewer friction, first-draft satisfaction, unattended repair queue.

After repairs, rerun the source report, then rerun this contract.

## Forbidden Workarounds

- Do not close from screenshots, contact sheets, sampled frames, stale V14 renders, or manifest prose.
- Do not use stronger transitions to hide weak source selection, missing bridge footage, or unclear route/story adjacency.
- Do not pass with hum/tone/silence/camera audio as BGM.
- Do not leave captions that speak to the editor or describe tool/QA status.
- Do not claim reference-level quality without current-output editorial watchdown closure.

## Safety

The contract is read-only. It must not write Resolve timelines, queue renders, download assets, modify source footage, or mutate a source drive.

---

## FILE: references/davinci-resolve-api.md

# DaVinci Resolve API

## Confirmed Local Install

Default macOS paths:

```text
/Applications/DaVinci Resolve/DaVinci Resolve.app
/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting
```

The official local README says external scripts require Resolve to be running and these environment values:

```bash
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

Use `scripts/check_resolve_api.py` to verify:

- app installed
- scripting module present
- `fusionscript.so` present
- Resolve process running
- API reachable
- product/version
- current project/timeline

If `check_resolve_api.py` is reachable but returns `currentPage: null`, `database: null`, `CreateProject` returns `None`, or `AddItemListToMediaPool`/`CreateEmptyTimeline` returns empty inside an `Untitled Project`, inspect the Resolve UI for blocking modals. Resolve Studio 21 can show a software update dialog before the project manager is usable; dismissing it returns the API to `currentPage: media` and `Local Database`.

When importing DJI or other large HEVC media from an external drive, prefer a small proxy smoke test first. Generate short local H.264 proxies, write a Resolve test timeline, and run `audit_resolve_timeline.py` before attempting a long-form write from original files.

## Write Contract

Before `build_resolve_timeline.py --apply`, state:

- project name
- timeline name
- fps and resolution
- tracks that will be created
- number of source files and clips
- fact that the script creates a new project/timeline and does not modify existing work

Prepare the machine-readable write contract first:

```bash
python3 <skill-dir>/scripts/prepare_resolve_apply_contract.py --package-dir <package>
```

The contract must record current delivery blockers, track plan, clip/source counts, write command, readback audit command, and explicit approval fields. It is not approval by itself.

The dry-run command is always safe:

```bash
python3 <skill-dir>/scripts/build_resolve_timeline.py --blueprint <package>/resolve_timeline_blueprint.json
```

The blueprint preflight is also safe and must run before any write approval:

```bash
python3 <skill-dir>/scripts/audit_resolve_blueprint.py --blueprint <package>/resolve_timeline_blueprint.json --package-dir <package>
```

It verifies source file existence, source in/out bounds, timeline ranges, same-track overlaps, V1 coverage gaps, generated title/place cards, subtitle sidecar status, marker/enrichment counts, and source-audio policy. A blocked preflight blocks `--apply`.

The write command requires explicit approval:

```bash
python3 <skill-dir>/scripts/build_resolve_timeline.py --blueprint <package>/resolve_timeline_blueprint.json --apply
```

## Render Contract

Preparing a render plan is safe and does not change Resolve:

```bash
python3 <skill-dir>/scripts/prepare_resolve_render.py --package-dir <package>
```

Before `prepare_resolve_render.py --queue` or `--queue --start`, state:

- project and timeline name
- output directory and custom output name
- format, codec, frame rate, resolution, `VideoQuality` high-bitrate target, and subtitle export mode
- current `delivery_audit.json` status
- current `resolve_audit.json` project/timeline match and warning status
- fact that `--queue` adds a job to the Resolve render queue, while `--start` starts rendering

Queue/start requires explicit user approval. Never queue a final render while package audit blockers remain, BGM/stock/aerial licenses are unverified, or the Resolve timeline has not been read back.

## Current API Coverage

The plugin can:

- connect to Resolve Studio through the official Python API
- create a new project
- set timeline frame rate and resolution
- create a new timeline
- create/name video, audio, and subtitle tracks
- import referenced source media
- append source ranges at explicit record frames
- convert source in/out seconds using each source media file's own probed FPS, while converting timeline record frames using the project timeline FPS
- preserve source/camera audio on A1 for footage clips marked `includeSourceAudio` by omitting `mediaType` in Resolve's append call
- enrich blueprints with subtitle cues, voiceover/BGM mix plans, stock/aerial placeholders, transition plans, and timeline markers
- write chapter, voiceover, BGM, stock/aerial, and transition markers to Resolve timelines during approved `--apply`
- preserve transition recipe payloads in marker customData and prepare/audit apply plans that separate API-supported cuts/bridge clips from manual Resolve/Fusion/effect steps
- import transparent subtitle overlay videos as normal video clips on V3 when visible captions are required
- save the project
- report skipped/missing source files
- generate title/place card MP4 assets and include them on V2
- preflight Resolve blueprints before write approval with ffprobe-backed range and coverage checks
- read back the current/named timeline for track and item counts
- prepare Resolve render settings in `render_plan.json`
- set `VideoQuality` in `render_plan.json`; use a numeric high-bitrate target such as `80000` for 4K long-form H.264/H.265 masters unless a platform-specific export target says otherwise
- queue and optionally start a Resolve render job through `SetRenderSettings`, `SetCurrentRenderFormatAndCodec`, `AddRenderJob`, and `StartRendering` after clean gates and explicit approval
- verify final MP4 delivery with ffprobe, sampled frame checks, full-film blackdetect, and subtitle evidence before claiming the render is deliverable

Known subtitle boundary:

- Resolve Studio 21 local smoke testing can create a subtitle track through the Python API, but `Timeline.ImportIntoTimeline(<srt>)` returned `False` and readback showed zero subtitle items. Do not claim native SRT import unless a fresh smoke test proves it on the user's installed Resolve version.
- For visible subtitles, generate an alpha overlay movie with `scripts/prepare_subtitle_overlay_asset.py`, add it to the blueprint as a V3 `subtitle_overlay_video`, write the Resolve timeline, and verify V3 item count/readback. For sidecar-only delivery, record that choice in the final report and expect `audit_story_style_contract.py` to warn unless sidecar was explicitly requested.

Known transition boundary:

- The local Resolve scripting README documents timeline item `SetProperty`, markers/customData, Fusion comp import, and timeline import/export methods, but it does not document a stable direct API for applying arbitrary adjacent-clip transitions such as Cross Dissolve, whip, rotation, push, slide, or speed ramp between two timeline items.
- Run `prepare_resolve_transition_apply_plan.py` and `audit_resolve_transition_apply_contract.py` before Resolve apply. Visible effects must have either an explicit manual Resolve/Fusion/effect instruction plus readback/frame evidence, or a real materialized bridge-clip fallback. Marker-only transition payloads are not enough.

Still required for later passes:

- exact Resolve-native subtitle item creation if a supported API path is later verified
- verified Resolve-native adjacent-transition application if a stable official API path is later documented and smoke-tested
- route/map graphics beyond static cards
- color correction and stabilization
- extended Resolve render status polling, retry handling, and post-render publish automation

Never report those later passes as finished unless they are actually written and read back.

## Audit

After any actual `--apply`, run:

```bash
python3 <skill-dir>/scripts/audit_resolve_timeline.py --project-name "<project>" --timeline-name "<timeline>" --output <package>/resolve_audit.json
```

Delivery evidence must include item counts by video/audio/subtitle track and warnings from this audit.

---

## FILE: references/capcut-jianying-draft-automation.md

# CapCut/Jianying Draft Automation Notes

Use this reference when the user asks whether Jianying/CapCut can be automated without Computer Use.

## Evidence

- `capcut-cli`: https://github.com/renezander030/capcut-cli
  - Unofficial CLI/library for local CapCut/JianYing draft stores.
  - Reads/writes local draft JSON and exposes commands such as `info`, `lint`, `add-video`, `add-audio`, `import-srt`, `compile`, `diagnose`, and `decrypt`.
  - Current package metadata exposes the local command aliases `capcut` and `capcut-cli`; detect both before claiming local draft tooling is installed.
  - Its docs say CapCut/JianYing projects are local JSON, but newer versions may use multiple timeline files such as `draft_content.json`, `draft_info.json`, `draft_meta_info.json`, and `template-2.tmp`.
  - Its JianYing encryption policy is detect-only: JianYing 6.0+ encrypted `draft_content.json` should be detected and explained, not decrypted by default.
- `cutcli` cookbook: https://github.com/xuliang2024/cutcli-cookbook
  - Cookbook, examples, prompts, and docs for a CapCut/Jianying draft CLI aimed at Cursor, Claude Code, ChatGPT, and MCP agents.
  - The local path creates editable CapCut/Jianying draft folders for the desktop app to open; this is draft-prep proof, not final-render proof.
  - The cookbook documents a `cutcli cloud render` path that uploads a draft and submits it to a cloud renderer. Treat that as a separate credentialed cloud-render experiment requiring API-key approval, returned job/result evidence, ffprobe-readable MP4, and normal render QA before it can compete with DaVinci Resolve.
- `pyCapCut`: https://github.com/GuanYixuan/pyCapCut
  - Python package for generating CapCut drafts, adding local video/audio/text, importing SRT, and adding transitions/effects.
  - The README states Linux/macOS can install and generate drafts, but generated drafts still need Windows CapCut for export.
- `pyJianYingDraft`: https://github.com/GuanYixuan/pyJianYingDraft
  - Python package for Jianying draft generation and template editing.
  - The README warns Jianying 6+ `draft_content.json` is usually no longer plaintext JSON; default template loading supports plaintext, with an optional fallback loader for users who legally have one.
  - The README says macOS/Linux support draft generation and template mode, but automatic export is Windows-only and limited by Jianying version.
  - `0.3.0` is the pinned primary engine for this Skill's native Jianying draft builder.
- `JianyingDraft.PY`: https://github.com/notinmood/JianyingDraft.PY
  - Python implementation for generating Jianying drafts from media/resource files.
  - Treat as an additional local draft-generation candidate; it is not proof of no-GUI final export on macOS.
- `CapCutAPI`: https://github.com/tamedpanda/CapCutAPI
  - Community HTTP/API-style project that can inform a backend draft-generation experiment.
  - Treat it as a candidate source, not proof of local app export.
- `capcut-mcp-back`: https://github.com/MigueDuque/capcut-mcp-back
  - REST API backend candidate for CapCut draft creation, media tracks, text overlays, effects, and keyframes.
  - Treat as a backend/draft experiment candidate; require local output proof before using it in a delivery chain.
- `capcut-mcp-api`: https://github.com/Capsnow467/capcut-mcp-api
  - FastAPI/n8n-oriented CapCut MCP API candidate.
  - Treat as backend draft tooling until a real exported MP4 is audited.
- `capcut-mcp`: https://github.com/fancyboi999/capcut-mcp
  - MCP server candidate for LLM-driven CapCut draft operations.
  - Treat it as a draft/tooling experiment; it is not proof of final app export.
- `cli-anything-capcut`: https://github.com/juliang8507/cli-anything-capcut
  - CapCut/Jianying draft scripting CLI and Claude Code skill candidate built around pyCapCut-style workflows.
  - Treat it as an agent integration candidate; it does not remove the need for app/cloud export proof.
- `capcut-ai-editor`: https://github.com/mrbuslov/capcut-ai-editor
  - MCP-style CapCut project exporter aimed at talking-head automation, subtitle work, and draft handoff.
  - Treat its workflow assumptions as format evidence only; long-form travel delivery still needs normal source, BGM, title, transition, and render QA.
- `capcut-mcp-server-extended`: https://github.com/MigueDuque/capcut-mcp-server-extended
  - Extended MCP server candidate for CapCut tools, presets, and parameterized workflows.
  - Require local draft compatibility proof and ffprobe-readable exported output before delivery use.
- `capcut-draft-info-mcp`: https://github.com/Morfeu333/capcut-mcp
  - MCP server candidate for editing CapCut `draft_info.json` with typed tools, backups, and app-guard behavior.
  - Useful only for compatible plaintext draft experiments; it is not final-render proof.
- `Jianying-CapCut2XML`: https://github.com/Ersiter/Jianying-CapCut2XML
  - Draft-to-FCP7-XML converter candidate for moving Jianying/CapCut draft information toward DaVinci Resolve.
  - Treat it as a handoff bridge to the reliable Resolve path, not as CapCut final export.
- `capcut-project-exporter`: https://github.com/yanghoxom/capcut-project-exporter
  - Windows GUI batch-export helper for CapCut draft segments.
  - Not a macOS no-GUI local export path; use only as platform-specific evidence.
- `CapCut-Mate-API`: https://github.com/SamuraiAIOSS/CapCut-Mate-API
  - Community project oriented around CapCut API/cloud-render style workflows.
  - Treat it as a separate cloud/API render experiment requiring credentials, output MP4 evidence, and normal render QA.
- `CapCutAPI-YYZC`: https://github.com/luhailiang98/CapCutAPI-YYZC
  - FastAPI cloud/API editing candidate with async export claims.
  - Treat it as a credentialed cloud experiment; do not mix it into the local no-GUI CapCut proof path without exported MP4 evidence.
- `jianying-editor-skill`: https://github.com/JGP-Tech/jianying-editor-skill
  - Agent skill/reference for Jianying draft automation patterns.
  - Treat platform/version-specific export claims as unverified until proven on the current machine.
- `capcut-export`: https://github.com/cooperka/capcut-export
  - Draft media inspection/extraction style utility.
  - Useful for handoff/debugging, not a final-render backend.

## Verified macOS Native Roundtrip

The current verified path separates backend work from the unavoidable desktop-app boundary:

1. `audit_jianying_resource_entitlements.py` resolves requested native resources through `pyJianYingDraft==0.3.0` metadata and reads Jianying's local `Cache/ressdk_db/*/rp.db` databases in SQLite read-only mode to classify cached TTS voices.
2. `build_jianying_native_draft.py` creates a new project with copied media, native transitions/effects/filters, BGM, and viewer SRT. It adds the macOS compatibility files expected by the current desktop app and never mutates source media or an opaque existing project.
3. The Jianying desktop app opens and saves that project; the app may then replace plaintext timeline data with opaque/encrypted data and generate cover, backup, timeline, and attachment files. Those current, post-build files are required app-roundtrip signals.
4. If `tts.enabled=true`, use either exact in-app TTS or the prepared Jianying SAMI path. `generate_jianying_sami_tts.py` discovers the current machine's Jianying User Data, requires an exact speaker ID, forbids fallback voices, ffprobes every result, and binds the audio manifest to the current SRT hash. `build_jianying_native_draft.py` rejects stale SRT, wrong voice, missing files, row-count mismatch, source-audio overlap, and a missing real TTS track.
5. `record_jianying_gui_proof.py` records proof only after all expected audio files exist, the exact voice is identified, timeline playback has reached an observed timecode, and the human-listen decision is explicit. Prepared SAMI audio is generation proof, not playback or taste proof.
6. The app exports locally. Proof is accepted only when ffprobe reads both video and audio streams from the exported file.
7. `audit_jianying_native_draft.py --require-app-roundtrip --require-export` ties the build, current project, and export readback together. Add `--require-tts-generated` only when the specification explicitly enables TTS.

This was live-verified on macOS with `/Applications/VideoFusion-macOS.app` version `11.0.12922` and `pyJianYingDraft==0.3.0`. It proves a practical backend-generated Jianying draft plus app TTS/export workflow on that installation. It does not prove a stable no-GUI macOS export API, portability of old proof to another machine, human approval of the selected voice/music, or final travel-film taste.

Use `--media-mode copy` for the reliable desktop roundtrip. Keep free-delivery mode on unless the current account's entitlement is known: the builder blocks VIP native assets by default, and the entitlement audit blocks a VIP preferred voice. The `--allow-vip-assets` and `tts.allowVipVoice=true` overrides are explicit paid-account decisions, never automatic fallbacks.

Subtitle presence alone must not create narration. BGM-only work leaves `tts.enabled` false and exports viewer TXT/SRT only. Spoken narration is opt-in and still requires a human listen gate after playback.

## Skill Policy

- Prefer DaVinci Resolve for generic fully unattended finishing and on machines that have not passed current Jianying roundtrip proof.
- When the user explicitly requests Jianying and the current app, entitlement, native-draft, TTS/playback, and export gates pass, use Jianying as the native-effects/TTS finishing path while keeping only the app-only boundary in GUI control.
- Treat local draft generation as verified preparation, but do not call it no-GUI final export on macOS.
- Treat MCP/HTTP projects as automation surfaces that may create or modify drafts; do not treat them as local macOS export proof until a current exported MP4 is audited.
- Run `scripts/audit_jianying_capcut_draft_automation.py` before trying local draft automation.
- On a new machine, run `scripts/prepare_capcut_jianying_tooling_bootstrap.py` before installing community tools. It prepares an isolated npm prefix, Python venv path, throwaway draft root, pinned install commands, and post-install proof commands without running downloads or installs. The v0.1.199 release pins `capcut-cli@0.13.2`, `pyCapCut==0.0.3`, `pyJianYingDraft==0.3.0`, and `websockets==15.0.1`; refresh these pins from primary package registries in a later release instead of silently using an unknown version.
- For a practical homeward airport chain, read `references/homeward-flight-pov-style.md` and start from `examples/jianying-homeward-pov-edit-spec.example.json`. `build_jianying_native_draft.py` enforces its BGM-only source mute, disabled TTS, viewer subtitle, single clean-title, motion-share, spacing, movement, BGM-hit, title-safety, duration, and landing-hold policy before writing the draft.
- Keep `--include-common-draft-roots` opt-in. The default bootstrap must not scan or modify real user drafts, and `realDraftModificationAllowed` must stay false.
- Only consider local draft automation ready when a compatible tool is available and either a draft root exists for new draft creation or at least one plaintext draft timeline is readable.
- Require `toolCandidateCount`, `cloudRenderCandidateCount`, `cloudRenderVerified=false`, `cutcliCloudRenderVerified=false`, `claimsCutcliCloudRender=false`, `macosNoGuiFinalExportStillUnverified=true`, `requiresSeparateCloudRenderExperiment=true`, and `claimsFinalCapcutBackendAutomation=false` when judging whether GitHub/community tools changed the CapCut/Jianying path.
- Treat cloud/API render candidates as a separate experiment: credentials must be approved, the export must be ffprobe-readable, and the normal rendered-watchdown/client QA chain must pass before it can compete with DaVinci Resolve.
- Use `--require-plaintext-template` before modifying or learning from an existing draft/template; opaque Jianying 6+ draft files are not acceptable template evidence.
- Run `scripts/run_no_material_capcut_draft_automation_smoke.py` after changing draft automation logic; it must prove `goodPlaintextDraftExperimentReady=true`, `opaqueDraftTrapBlocked=true`, `encryptedDraftDetectedNotModified=true`, `directDraftExportStillUnverified=true`, and `claimsFinalCapcutDraftAutomation=false`.
- Run `scripts/run_no_material_capcut_tooling_bootstrap_smoke.py` after changing install/probe/bootstrap behavior; it must prove `toolingBootstrapReady=true`, `safeThrowawayExperimentReady=true`, `missingToolTrapBlocked=true`, `temporaryInstallPlanPrepared=true`, `postInstallProofCommandsPrepared=true`, `downloadOrInstallRan=false`, `realDraftModificationAllowed=false`, and `requiresDaVinciDefaultFinish=true`.
- Run `scripts/run_no_material_jianying_native_roundtrip_smoke.py` after changing native draft, entitlement, TTS, or export proof behavior; it must additionally prove `preparedJianyingSamiTtsAccepted`, `preparedTtsStaleSrtTrapBlocked`, `preparedTtsWrongVoiceTrapBlocked`, `preparedTtsFallbackVoiceForbidden`, `preparedTtsDoesNotClaimPlaybackBeforeProof`, and `preparedTtsPlaybackAndListenVerified`.
- Never blindly modify encrypted/opaque Jianying drafts. Detect and report them.
- Never claim Jianying/CapCut in-app TTS or final export from draft JSON evidence alone. A final claim still needs real app/export proof and normal video QA.

---

## Baaki references (naam-matr list — audit-gate contracts, is file me full nahi)

- references/agent-runtime-compatibility.md
- references/bgm-catalog-beatcut-contract.md
- references/bgm-musicality-contract.md
- references/bgm-phrase-blueprint-engine.md
- references/bilibili-travel-style.md
- references/bridge-sequence-application-contract.md
- references/bridge-sequence-blueprint-engine.md
- references/bridge-sequence-engine.md
- references/capcut-jianying-draft-automation.md
- references/chapter-arc-engine.md
- references/chapter-story-spine-contract.md
- references/creator-cut-application-contract.md
- references/creator-cut-engine.md
- references/davinci-resolve-api.md
- references/delivery-workflow.md
- references/editor-integration.md
- references/editorial-judgment-jianying-music-contract.md
- references/editorial-watchdown-repair-contract.md
- references/effect-motion-application-contract.md
- references/effect-motion-blueprint-engine.md
- references/final-bgm-mix-contract.md
- references/final-blueprint-lineage-contract.md
- references/final-cut-smoothness-contract.md
- references/final-source-usage-contract.md
- references/final-viewer-friction-contract.md
- references/first-assembly-source-order-contract.md
- references/first-draft-satisfaction-contract.md
- references/footage-select-engine.md
- references/homeward-flight-pov-style.md
- references/large-source-unattended-readiness-contract.md
- references/long-form-travel-style.md
- references/multicamera-roadtrip-story-engine.md
- references/music-stock-fonts.md
- references/narration-subtitles.md
- references/narrative-adjacency-contract.md
- references/one-shot-autonomy-contract.md
- references/opening-story-engine.md
- references/output-contracts.md
- references/pacing-watchability-contract.md
- references/parallel-world-vlog-style.md
- references/reference-batch-profile-engine.md
- references/reference-profile-application-contract.md
- references/reference-review-completeness-contract.md
- references/reference-scene-grammar-engine.md
- references/reference-style-repair-engine.md
- references/reference-transition-profile-contract.md
- references/rendered-transition-proof-contract.md
- references/resolve-transition-apply-contract.md
- references/resolve-transition-materialization-contract.md
- references/rhythm-recut-application-contract.md
- references/scene-flow-arc-contract.md
- references/shot-flow-continuity-contract.md
- references/source-selection-repair-contract.md
- references/timeline-variety-contract.md
- references/transition-action-anchor-contract.md
- references/transition-audition-packet-engine.md
- references/transition-audition-quality-contract.md
- references/transition-audition-role-integrity-contract.md
- references/transition-audition-visual-proof-contract.md
- references/transition-breathing-room-contract.md
- references/transition-bridge-visual-evidence-contract.md
- references/transition-cadence-contract.md
- references/transition-choreography-contract.md
- references/transition-choreography-engine.md
- references/transition-continuity-rehearsal-contract.md
- references/transition-cutpoint-contract.md
- references/transition-effect-palette-contract.md
- references/transition-effect-recipe-contract.md
- references/transition-execution-blueprint-engine.md
- references/transition-execution-engine.md
- references/transition-execution-readiness-engine.md
- references/transition-grammar-engine.md
- references/transition-microstructure-contract.md
- references/transition-motif-coherence-contract.md
- references/transition-motif-engine.md
- references/transition-motion-accent-contract.md
- references/transition-motion-direction-contract.md
- references/transition-polish-application-contract.md
- references/transition-polish-blueprint-engine.md
- references/transition-preview-packet-engine.md
- references/transition-preview-quality-contract.md
- references/transition-reference-candidate-engine.md
- references/transition-reference-readiness-contract.md
- references/transition-reference-selection-engine.md
- references/transition-scene-arc-contract.md
- references/transition-scene-settlement-contract.md
- references/transition-sensory-continuity-contract.md
- references/transition-sequence-satisfaction-contract.md
- references/transition-source-coverage-contract.md
- references/transition-storyboard-contract.md
- references/transition-viewer-orientation-contract.md
- references/transition-visual-match-contract.md
- references/transition-watch-reel-contract.md
- references/transition-watch-reel-review-contract.md
- references/unattended-repair-queue-engine.md
- references/whole-film-satisfaction-contract.md
