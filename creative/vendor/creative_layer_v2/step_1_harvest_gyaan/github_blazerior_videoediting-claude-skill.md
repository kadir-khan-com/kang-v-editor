# blazerior/videoediting-claude-skill — videoediting (ffmpeg editing + colour grading)
- Repo: blazerior/videoediting-claude-skill
- Link: https://github.com/blazerior/videoediting-claude-skill
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 3 stars, 1 fork (repo page, 2026-11-05) — small repo, included because it is the only find with real COLOUR-GRADING technique content
- Last commit (from local clone git log): 2026-09-11
- Extracted: 2026-11-05, Round 2 harvest — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Transcript-first vertical editing via ffmpeg: SKILL.md rules + references — ffmpeg-cookbook.md (grades/eq/curves/vignette/.cube LUTs, effects, transitions, audio, encoding), design-system.md (palette, type scale, safe zones), storyboard.md (9 panel types), pipeline.md (8 steps + acceptance checklist), batch-pipeline.md, fablecut.md, remotion.md, troubleshooting.md (17 failures). Output standard: 1080x1920, loudnorm -14 LUFS, zoom alternates 1.00/1.045 across cuts.


---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/SKILL.md ===== -->

---
name: videoediting
description: "Edit already-shot footage with ffmpeg: re-cut by speech, colour grading, word-level burned-in subtitles, infographic and meaning overlays, assembling vertical videos for Reels/Shorts/TikTok. Invoked with /videoediting. Use when the user says 'edit this video', 're-cut', 'trim the pauses', 'colour grade', 'add subtitles', 'burn in captions', 'add infographics to the video', 'make a reel', 'make a short', 'vertical video', 'stitch these clips', 'normalise the audio', or hands over a .mov/.mp4 and asks to turn it into something watchable. Not for generating footage from scratch with AI models (Veo, Sora, HeyGen, Remotion)."
metadata:
  version: 1.3.0
---

# Video editing with ffmpeg

You are an editor who works with a transcript and filtergraphs rather than a mouse and a timeline. The pipeline is deterministic: everything is edited as text and rebuilt with one command.

```
footage → transcript with word-level timings → EDL (edit list) → ffmpeg → finished video
                    ↑                               ↑
             faster-whisper                 edited by hand — this IS the edit
```

Core principle: **the video is never analysed pixel by pixel — the edit is driven by timed text.** Speech defines the structure; the picture serves it.

## One reel or many?

Decide this first — it changes everything downstream.

- **One or two reels** → follow the step order below, conversationally.
- **Three or more** → switch to the batch pipeline: [references/batch-pipeline.md](references/batch-pipeline.md). Each stage runs once over the whole project and caches by input hash. Doing ten reels conversationally costs roughly ten times the context and buys nothing for it.

## Order of work

Always follow the steps, never skip ahead. Each step produces the input for the next.

1. **Check the environment.** If ffmpeg / faster-whisper / Chrome are missing → [references/setup.md](references/setup.md). On a clean machine this takes ten minutes.
2. **Get the source.** If the user handed you a URL instead of a file, fetch it first with `download.py`.
3. **Inspect the source** — ffprobe, scene detection, a contact sheet. **Look at the frames with your own eyes via Read.** Never edit blind from text alone.
4. **Transcribe** with word-level timings and **proofread the result**. Speech recognition gets words wrong even on clean audio. No local model? `transcribe_cloud.py` gets the same output from Groq/OpenAI.
5. **Agree on the concept** with the user if they have not specified one: format, what goes into graphics, target platform. One question, not a questionnaire.
6. **Build the EDL** — cut pauses, never cut ideas.
7. **Build `base`**, then verify the cuts frame by frame.
8. **Generate subtitles and overlays**, build `final`.
9. **Run the acceptance checklist** and deliver the file with SendUserFile.

Full commands for each step — [references/pipeline.md](references/pipeline.md).

## What this pipeline can and cannot do

Can: semantic cutting, pause removal, punch-in on cuts, colour grading (including `.cube` LUTs), word-level subtitles, arbitrarily complex infographics via HTML/CSS, stabilisation, loudness normalisation for social platforms, batch processing. With the Remotion plugin installed, also animated graphics rendered from React — see [references/remotion.md](references/remotion.md).

**Cannot at all** — say so up front if the user asks for it: object tracking (pinning a caption to a moving hand) and masked grading. Those still need Premiere / DaVinci / After Effects.

**Cannot alone, but can with FableCut installed:** frame-accurate creative cutting, keyframed motion, transitions, speed ramps, chroma key, cutting to a music beat. FableCut is a browser timeline an agent drives through MCP — see [references/fablecut.md](references/fablecut.md). It has no speech recognition and its export needs a human click, so speech-driven structure and unattended batches stay in this pipeline.

## Ready-made tools

`assets/tools/` holds twelve working scripts — **copy them into the project, do not rewrite them from scratch**:

| Script | What it does |
|---|---|
| `download.py` | fetch source footage from a URL (yt-dlp) — skip if you already have a local file |
| `transcribe.py` | faster-whisper → `transcript.json` with word-level timings + `.srt` |
| `transcribe_cloud.py` | same output, via Groq/OpenAI Whisper API — no model download, needs an API key |
| `pauses.py` | lists pauses in speech — the basis for the EDL |
| `dump_words.py` | every word with its index and confidence — for proofreading |
| `make_ass.py` | word-level ASS subtitles, re-timed to the post-cut timeline |
| `render_overlays.py` | HTML/CSS → headless Chrome → 1080×1920 PNG with alpha |
| `build.py` | assembly: `base` (cut + grade), `final` (overlays + subtitles + audio) |
| `build_vo.py` | same, but for a **separate voiceover track** — video from several sources fitted to the audio |
| `batch_vo.py` | transcribe every voiceover in one model load |
| `mute_subs.py` | drop subtitles where a full-screen card is on screen |
| `pipeline.py` | **batch driver** — every stage over every reel, with caching |

`assets/templates/` holds starter `edl.json`, `overlays.json` and `corrections.json`.

Lay the project out like this:

```
<folder with the footage>/
├── IMG_XXXX.MOV
└── edit/
    ├── tools/        ← the copied scripts
    ├── work/         ← intermediates, never shipped
    ├── overlays/     ← rendered PNGs
    ├── out/          ← finished videos
    ├── edl.json  overlays.json  corrections.json  subs.ass
```

## Reference files

Load these on demand, not all at once:

- [references/setup.md](references/setup.md) — installing on a clean machine (Windows/macOS), verifying the ffmpeg build
- [references/pipeline.md](references/pipeline.md) — the workflow step by step, cutting rules, commands
- [references/storyboard.md](references/storyboard.md) — video formats, panel types, how to storyboard a talking head
- [references/design-system.md](references/design-system.md) — palette, type scale, safe zones, overlay techniques
- [references/batch-pipeline.md](references/batch-pipeline.md) — running many reels as stages, and where the context actually goes
- [references/remotion.md](references/remotion.md) — animated graphics tier: when React-rendered overlays earn their cost
- [references/fablecut.md](references/fablecut.md) — timeline tier: when to hand the edit to FableCut, and how the two pipelines meet
- [references/ffmpeg-cookbook.md](references/ffmpeg-cookbook.md) — grades, effects, transitions, audio, encoding
- [references/troubleshooting.md](references/troubleshooting.md) — **read this before your first ffmpeg run**; seventeen failures, each of which cost an hour

## Rules that make or break the video

Learned on real builds, not from documentation.

1. **Look at the frames.** A transcript will not tell you the speaker is standing up or fixing their hair at that exact moment. Those are precisely the places where cuts fall apart.
2. **A card goes above the face, never on it.** The first attempt always drops the panel into the middle of the frame, covering the eyes. The speaker's gaze is half the trust the video earns.
3. **Cut at the end of a phrase, not on a stopwatch.** Cutting "every N seconds" slices ideas in half.
4. **Leave 0.2–0.3 s of every pause.** A pause collapsed to zero sounds like a stutter.
5. **Never touch dramatic pauses** — after a question, before a conclusion. There the silence is doing the work.
6. **Alternate `zoom` between segments.** Then a cut reads as a change of angle rather than a mistake.
7. **Leave one stretch with no graphics at all.** The viewer needs air; a solid wall of cards is exhausting.
8. **Proofread the subtitles.** A recognition error burned into the picture is permanent.
9. **Verify by looking, not by faith.** Pull still frames, stack them with `hstack`, open the result via Read.
10. **Never ship without the acceptance checklist** in pipeline.md.
11. **Never let a tool write back into a config file.** A script that appends its own output to the EDL doubles that file's size, and every later edit echoes the whole thing into context. Generated data belongs in `work/`.
12. **Read the first and last line of the transcript yourself.** Whisper hallucinates fabricated text over silence — classically a fake subtitler credit line on Russian audio — and it can carry a perfectly normal-looking confidence score. Both transcription scripts filter the obvious cases automatically, but the filter is not airtight. See [troubleshooting.md #17](references/troubleshooting.md).

## Orchestration

The task is multi-step — create tasks with TaskCreate for the stages (transcript, EDL, grade, graphics, assembly) and keep their status current. Run long operations (model download, `base` render) in the background and use the time for work that does not depend on them: while the model downloads, design the overlays and test grades on still frames.

Deliver the finished video with SendUserFile and a short note on what changed.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/batch-pipeline.md ===== -->

# Batch pipeline — editing many reels without burning context

One reel is a conversation. Ten reels is a pipeline. The difference is not the ffmpeg work — that scales fine — it is **context**: doing ten reels the conversational way costs roughly ten times the tokens of doing one, and most of that spend buys nothing.

`assets/tools/pipeline.py` runs each stage once over the whole project, caches by input hash, and prints one line per reel.

## Stages

```
ingest      inventory every media file                -> work/media.json
transcribe  every voiceover in ONE model load         -> work/vo/<id>/transcript.json
probe       scene cuts + one contact sheet per source -> work/shots.json, work/sheets/
overlays    graphics for every reel                   -> overlays/<reel>/
subs        subtitles for every reel                  -> subs-<reel>.ass
base        cut + grade video track for every reel    -> work/<reel>_base.mp4
final       composite everything                      -> out/<reel>.mp4
qa          ONE contact strip for all reels + report  -> work/qa.png
```

```bash
python tools/pipeline.py all
```

```bash
python tools/pipeline.py final --only 2a,3b
```

```bash
python tools/pipeline.py overlays --force
```

Every stage is idempotent. Re-running costs nothing when inputs are unchanged — the cache key is the mtime+size of every input plus the relevant config.

## The manifest

`project.json` holds only what is short and shared:

```json
{
  "media_dir": "D:\\path\\to\\footage",
  "qr": "D:\\path\\to\\qr.jpg",
  "lang": "ru",
  "whisper_model": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
  "voices": { "vo1": { "file": "…mp3" } },
  "reels": {
    "1a": { "voice": "vo1", "title": "1A-tutorial", "mute": [[0, 2.35], [31.3, 34.3]] }
  }
}
```

Per-reel detail stays in `edl-<name>.json` and `overlays-<name>.json`. **Do not merge them into the manifest** — see the next section for why.

## Where the tokens actually go

Measured on a real ten-reel project, in descending order of waste:

### 1. Editing large JSON files — the biggest leak by far

Every `Edit` on a file echoes the whole file back into context. An EDL with ten segments and comments is ~4 KB ≈ 1.5k tokens. Touch ten of them twice and that is 30k tokens spent on re-reading your own data.

**Rules:**

- **Never let a tool mutate a config file.** The old `make_reel.py` wrote the overlay timeline and output directory back into the EDL, doubling its size and making every subsequent edit twice as expensive. `build_vo.py` now reads the timeline from `overlays-<name>.json` directly and leaves the EDL alone.
- **Generated data goes in `work/`**, never next to hand-edited config.
- **Write config files whole** with `Write` rather than patching them with several `Edit` calls.
- **Keep the `_note` fields short.** They are useful, but they are also tokens on every echo.

### 2. Looking at frames one reel at a time

Each image costs roughly 1–2k tokens. Checking ten reels at six frames each, as separate strips, is twenty-plus images.

The `qa` stage stacks every reel into a single `work/qa.png` — ten rows, six frames per row. One image, one look, the whole project verified. When something looks wrong, only then pull that one reel in detail.

### 3. Re-probing the same source for every reel

Ten reels usually draw on the same handful of clips. Probing scene cuts and building contact sheets per reel repeats identical work and identical images.

The `probe` stage does it once per **source file**, writes `work/shots.json`, and puts one 8-frame sheet per source in `work/sheets/`. Read those sheets once at planning time; after that work from the timecodes in `shots.json`, which is text.

### 4. Reloading the speech model

`faster-whisper` spends most of its wall clock loading the model, not transcribing. `batch_vo.py` loads it once and walks every voiceover. Seven voiceovers: one load instead of seven.

This is also why `transcribe_cloud.py` and `download.py` are **not** wired into `pipeline.py`: the batch `transcribe` stage's entire value is one model load instead of N, and per-file cloud API calls would trade that away for a per-call cost and network latency multiplied by every voiceover. For a batch project, install faster-whisper properly (setup.md) rather than reaching for the cloud path. `download.py` has nowhere to plug in either — `ingest` inventories `media_dir` as-is; fetch every source into that folder by hand before running `ingest`.

### 5. Verbose command echo

Printing the full ffmpeg command line for every reel is a few hundred tokens each and tells you nothing you didn't already know. The pipeline prints `overlays : 3 rebuilt, 7 cached` and nothing more. Failures still dump stderr — that is the case where the detail is worth paying for.

## Working order for a new batch project

1. `ingest` — then read `work/media.json`. It is text, and it already tells you resolution, duration, rotation and codecs for everything.
2. `transcribe` — read the transcripts. Text again.
3. `probe` — **this is the one place to spend images.** Look at `work/sheets/` once, note what is where, and write it down as timecodes. Every later decision references those numbers instead of re-opening frames.
4. Write all EDLs and overlay specs in one pass, from the notes.
5. `overlays subs base final` — or just `all`.
6. `qa` — one image, one report. Fix what is broken, re-run only the affected stage.

The shape that matters: **look once, write once, build many.** The conversational shape — plan a reel, build it, look at it, fix it, repeat — is what multiplies cost by ten.

## When a reel needs fixing

Change only its own files and re-run the narrow stage:

```bash
python tools/pipeline.py overlays --only 3b && python tools/pipeline.py final --only 3b
```

`base` is the slow stage; it only re-runs when the EDL or the grade changed. Graphics and subtitles iterate in seconds.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/design-system.md ===== -->

# Overlay design system

## Safe zones for 1080×1920

| Zone | Coordinates | What may go there |
|---|---|---|
| Platform UI, top | 0–150 | nothing |
| **Working area for graphics** | **200–1250** | titles, cards, diagrams, CTA |
| Speaker's face | usually 700–1300 | keep out |
| **Subtitles** | 1380–1520 | subtitles only |
| Platform UI, bottom | 1600–1920 | nothing |

**A card goes above the face, never on it.** This rule is broken on nearly every first attempt: the panel lands in the middle of the frame and covers the eyes. The speaker's gaze is half the trust the video earns. Check still frames and move cards up until the eyes are clear.

Account for `zoom` from the EDL: on a segment at 1.09 the face is larger and higher, so a card that sat fine at 1.00 will start clipping the forehead.

## Palette

Warm and calm — suited to expert talking-head content:

| Role | Colour |
|---|---|
| Panel | `rgba(20,16,12,.88)` |
| Text | `#FFF6EC` |
| Secondary text | `#CDBBA5` |
| Accent | `#E8A33D` (amber) |
| Negative, struck through | `#C7523B` (terracotta) |

Pick the accent from what is already in frame — the subject's clothing, the wall, the light. If the user has brand colours, only this block changes; the layout stays.

## Type scale

| Element | Size | Weight |
|---|---|---|
| Hook headline | 100 | 700 |
| Pull quote | 82 | 700 |
| Card body | 58 | 600 |
| List item | 50 | 600 |
| Caption | 36 | 400 |
| Kicker | 29 | 600, uppercase, `letter-spacing:.22em` |
| Subtitles | 72 | bold |

Font stack: `'Bahnschrift','Segoe UI','Helvetica Neue',Arial,sans-serif`. Bahnschrift ships with every Windows and looks contemporary. For a custom face, drop the `.ttf` into `edit/fonts/` and point `fontsdir=fonts` in `build.py`.

## Techniques

**Scrim under text.** A bright background (a window behind the subject) destroys legibility. A gradient fixes it:

```css
.scrim-top{position:absolute;left:0;right:0;top:0;height:820px;
  background:linear-gradient(180deg,rgba(14,11,8,.72) 0%,rgba(14,11,8,.45) 55%,rgba(14,11,8,0) 100%)}
```

**Strike-through** as a pseudo-element with a slight tilt — livelier than a straight line:

```css
.strike{position:relative;color:#C7523B}
.strike:after{content:'';position:absolute;left:-6px;right:-6px;top:52%;height:7px;
  background:#C7523B;transform:rotate(-3deg);border-radius:4px}
```

**Bullets appearing one at a time** — two cards with identical markup, placed back to back in time:

```html
<div class='row off'>...</div>   <!-- opacity:0 -->
<div class='row hi'>...</div>    <!-- revealed and highlighted -->
```

**Accent border** on the left edge of a panel (`border-left:9px solid #E8A33D`) — a cheap way to make a card feel designed.

**A shadow is mandatory**, otherwise the panel looks pasted on: `box-shadow:0 26px 70px rgba(0,0,0,.42)`.

## Subtitles

The style lives in the constants at the top of `make_ass.py`:

| Constant | Value | Meaning |
|---|---|---|
| `FONT_SIZE` | 72 | any larger and lines start to clip |
| `MARGIN_V` | 420 | bottom offset, clears the platform UI |
| `MARGIN_H` | 70 | side margins |
| `MAX_WORDS` | 3 | words per line |
| `MAX_GAP` | 0.7 | pause that forces a line break |
| `ACCENT` | `&H00A9F5FF` | the active word |

**ASS colours are BGR, not RGB.** `&H00A9F5FF` is yellow. It is easy to get backwards and end up with blue.

`WrapStyle: 0` is mandatory — at `2` a long line runs off the screen instead of wrapping.

The active word is tinted and scaled up by 8 % (`\fscx108\fscy108`). Beyond 110 % the line starts jumping around as its width changes.

## What not to do

- Neon colours and four-pixel outlines. They work for entertainment content and destroy credibility in expert content.
- More than two accent colours.
- A card for every sentence — that produces a slide deck, not a video.
- Animation for its own sake: a 0.25 s `fade` is enough; fly-ins and bounces pull attention away from the speech.
- Small type. This is watched on a phone held in one hand; 36 px is the floor, and only for captions.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/fablecut.md ===== -->

# FableCut — the timeline layer

[FableCut](https://github.com/ronak-create/FableCut) is a browser-based non-linear editor that an agent can drive. The whole timeline is one `project.json`; patch it and the open editor hot-reloads in about 150 ms. It does not replace this pipeline — it covers the half of the job ffmpeg filtergraphs are bad at.

**Source and credit.** Written by Ronak Parmar, MIT licence, zero npm dependencies. Everything below was checked against **v1.7.0, commit `e423338`** (September 2026). It is a young project — created July 2026 — so treat the `project.json` schema as something that can still move between versions, and re-read `fablecut_docs` rather than trusting a remembered field name.

## Install

```bash
/plugin marketplace add ronak-create/FableCut
```

```bash
/plugin install fablecut@fablecut
```

Restart Claude Code afterwards. Requirements: Node 18+, a Chromium browser, and ffmpeg on PATH (optional, but without it export falls back to a realtime MediaRecorder capture, which is slower and worse). The editor runs at `http://localhost:7777` and binds to `127.0.0.1` only.

The plugin brings eight MCP tools — `fablecut_status`, `fablecut_docs`, `fablecut_get_project`, `fablecut_set_project`, `fablecut_patch_project`, `fablecut_import_media`, `fablecut_analyze_reference`, `fablecut_encode_profiles` — and two skills, `fablecut:edit-video` and `fablecut:remake-reel`.

## Which tool for which job

| Job | Tool | Why |
|---|---|---|
| Cut by speech, kill pauses | **this pipeline** | the transcript *is* the edit; FableCut has no speech recognition at all |
| Word-level burned-in subtitles | **this pipeline** | `make_ass.py` + libass, one pass, no browser |
| Ten reels as a batch | **this pipeline** | `pipeline.py` is headless and caches; FableCut needs a human click per export |
| Frame-accurate trimming by eye | **FableCut** | a real timeline with snapping beats nudging numbers in `edl.json` |
| Keyframed motion, speed ramps | **FableCut** | ~25 animatable properties with easing curves; ffmpeg cannot do this sanely |
| Transitions between clips | **FableCut** | 17 built-in types against `xfade`'s awkward offset arithmetic |
| Editing to a music beat | **FableCut** | `fablecut_analyze_reference` gives beats, BPM and an energy curve |
| Chroma key, background removal | **FableCut** | MediaPipe in-browser, no green-screen filtergraph to tune |
| Colour grade with a `.cube` LUT | **this pipeline** | `lut3d` is exact and reproducible |

The short version: **speech-driven structure stays here, hand-and-eye work goes to FableCut.**

## How the two hand off

The natural split is to let this pipeline do what it is good at first, then import the result.

1. Transcribe and build the EDL as usual — the transcript is still the cheapest way to find the structure.
2. Render `base` (cut + grade) with `build.py`. That is a single clean MP4.
3. `fablecut_import_media` that file, then work the timeline for the things filtergraphs make painful: transitions, keyframed punch-ins, speed ramps, animated titles.
4. Export from FableCut, then burn subtitles over the export with the existing ffmpeg pass if you want the word-level ASS captions rather than FableCut's kinetic ones.

Going the other way also works: cut in FableCut, export, then run the export through `transcribe.py` and `make_ass.py`. It costs one extra encode.

**Concurrency.** If a human edits a clip in the UI while the agent is mid-write, the agent's next write is rejected with a 409 instead of silently overwriting. Do not defeat this by re-sending the patch blindly — re-read the project with `fablecut_get_project` and rebase the change.

## Remaking a reel you like

`fablecut:remake-reel` is the genuinely novel piece and has no equivalent in this pipeline. Feed it a reference video — a reel, a montage, an ad — and it returns an edit blueprint: shot boundaries, music beats and BPM, an energy curve, where the drop lands. Then it rebuilds that structure with your own footage.

That is the one thing worth installing FableCut for even if you never touch its timeline by hand. Cutting to a beat grid is something the transcript-driven approach here simply cannot see.

## When not to use it

- **You need it headless.** The compositor *is* the browser, so export runs there. The agent cannot render on its own — it asks you to press Export, or you render straight from `media/` with ffmpeg and skip FableCut's compositing. This is what rules it out for a ten-reel batch.
- **You need subtitles from speech.** There is no ASR anywhere in it. That stays here.
- **You need object tracking or masks.** Neither tool does these. That is still Premiere, DaVinci or After Effects.
- **You need Cyrillic titles and have not checked the font.** The UI ships in English, Chinese, Japanese, Spanish and Brazilian Portuguese, and bundles 20 Google Fonts (OFL) — not all of them cover Cyrillic. Load a font that does before typing Russian into a title, or it will render as boxes.

The honest split: this pipeline stays the backbone for anything driven by speech and anything that has to run ten times unattended. FableCut is what you open when the edit needs a pair of eyes on a timeline.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/ffmpeg-cookbook.md ===== -->

# ffmpeg cookbook

## Grading

The base grade — tested against hard backlight from a window. Lifts the face out of shadow and reconciles different locations:

```
eq=contrast=1.13:brightness=0.012:saturation=1.07:gamma=1.07,
curves=all='0/0 0.22/0.285 0.75/0.795 1/1':r='0/0 0.5/0.515 1/1':b='0/0 0.5/0.492 1/1',
vignette=PI/9,unsharp=5:5:0.45
```

What each part does: `eq` sets overall contrast and lifts the midtones; `curves` raises the shadows (the 0.22/0.285 point) and warms the skin by pushing red up and blue down; `vignette=PI/9` gently darkens the edges and keeps the eye on the face; `unsharp` compensates for the softening introduced by `scale` and `crop`.

Alternatives — drop them into `GRADE` in `build.py`:

| Look | Filter |
|---|---|
| Neutral punch | `eq=contrast=1.12:saturation=1.06:gamma=1.06,curves=all='0/0 0.22/0.28 0.75/0.79 1/1'` |
| Warm cinematic | `curves=r='0/0.015 0.5/0.535 1/1':b='0/0 0.5/0.465 1/0.97',eq=contrast=1.14:saturation=1.10,vignette=PI/5` |
| Pastel / film fade | `curves=all='0/0.055 0.3/0.35 0.7/0.73 1/0.965',eq=saturation=0.90,colorbalance=rs=0.04:bs=-0.03` |
| Ready-made LUT | `lut3d=file='look.cube'` |

`vignette=PI/5` is strong and visible; `PI/9` is subtle. Smaller denominator, stronger effect.

**Choose a grade by comparison, not by eye.** Pull one frame, run it through the candidates, stack them and open via Read:

```bash
ffmpeg -y -ss 45 -i "IMG.MOV" -frames:v 1 -vf "eq=contrast=1.12,scale=380:-1" edit/work/gA.png
```

```bash
ffmpeg -y -i edit/work/g0.png -i edit/work/gA.png -i edit/work/gB.png -filter_complex "[0][1][2]hstack=inputs=3" edit/work/grade.png
```

Mind the headroom: 8-bit bt709 phone footage takes a moderate grade. Aggressive curves will band on gradients — most visibly on the wall behind the subject.

## Framing and movement

| Task | Filter |
|---|---|
| Punch-in (static zoom) | `crop=iw/1.06:ih/1.06:(iw-ow)/2:(ih-oh)/2,scale=1080:1920:flags=lanczos` |
| Slow push-in | `zoompan=z='min(zoom+0.0006,1.15)':d=<frames>:s=1080x1920:fps=30` |
| Convert other aspect ratios to 9:16 | `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920` |
| Blurred background instead of bars | `split[a][b];[a]scale=1080:1920,boxblur=40[bg];[b]scale=1080:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2` |
| Stabilisation, pass 1 | `vidstabdetect=shakiness=6:accuracy=15:result=t.trf` |
| Stabilisation, pass 2 | `vidstabtransform=input=t.trf:smoothing=30:zoom=2` |
| Horizontal flip | `hflip` |

## Transitions

A hard cut on a pause is almost invisible and beats any effect. A cross-fade earns its place where there is movement in frame — the subject sitting down, standing up, turning:

```
xfade=transition=fade:duration=0.3:offset=<second_of_the_cut>
```

Others: `wipeleft`, `slideup`, `dissolve`, `smoothleft`, `circleopen`. For a talking head, anything beyond `fade` and `dissolve` looks amateur.

**Important:** `xfade` shortens the result by the transition duration, and every subsequent timing — subtitles and overlays alike — shifts. If you add transitions, either recompute the timings or keep them at the end of the chain.

Audio across a transition — `acrossfade=d=0.3` with a matching duration.

## Overlays

```
-loop 1 -framerate 30 -t 3.5 -i card.png
[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st=3.25:d=0.25:alpha=1,setpts=PTS-STARTPTS+6.35/TB[o1]
[0:v][o1]overlay=0:0:eof_action=pass:repeatlast=0:enable='between(t,6.35,9.85)'[b1]
```

`-t` is mandatory — without it `-loop 1` produces an infinite stream and eats all available memory.

A corner logo:

```
[0:v][1:v]overlay=W-w-40:H-h-260
```

## Subtitles

```
subtitles=subs.ass:fontsdir='C\:/Windows/Fonts'
```

Run ffmpeg with `cwd` set to the project folder and pass a relative path — the drive-letter colon breaks the filtergraph.

Burning an SRT directly, without ASS:

```
subtitles=subs.srt:force_style='Fontname=Arial,Fontsize=24,PrimaryColour=&H00FFFFFF,Outline=2'
```

## Audio

| Task | Filter |
|---|---|
| Normalise for social platforms | `loudnorm=I=-14:TP=-1.5:LRA=11` |
| Two-pass loudnorm (more accurate) | first `loudnorm=print_format=json`, then feed the measured values back |
| Fades at cut points | `afade=t=in:st=0:d=0.03` + `afade=t=out:st=<end-0.03>:d=0.03` |
| Noise reduction | `afftdn=nf=-25` |
| Remove low-end rumble | `highpass=f=80` |
| Tame sibilance | `deesser` |
| Add background music | `[0:a][1:a]amix=inputs=2:duration=first:weights=1 0.15` |

The standard for Reels/TikTok is −14 LUFS. Quieter sounds amateurish; louder and the platform will turn it down itself.

## Encoding

Final:

```
-c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -profile:v high -level 4.1
-c:a aac -b:a 192k -ar 48000 -movflags +faststart
```

Intermediates: `-crf 16 -preset medium`, so re-encoding losses do not accumulate.

CRF: 16–18 for intermediates, 19–21 for the final, 23+ already shows artefacts on gradients.

Frame rate: 30 is plenty for a talking head and keeps the file smaller. 60 only makes sense with fast movement in frame.

## Inspection and verification

```bash
ffprobe -v error -show_format -show_streams -print_format json "IMG.MOV"
```

```bash
ffmpeg -hide_banner -i "IMG.MOV" -vf "select='gt(scene,0.25)',showinfo" -an -f null -
```

```bash
ffmpeg -y -i "IMG.MOV" -vf "fps=1/9,scale=360:-1" edit/work/f_%02d.jpg
```

```bash
ffmpeg -hide_banner -i "IMG.MOV" -af volumedetect -f null -
```

Stacking frames into a strip for visual review:

```bash
ffmpeg -y -i a.png -i b.png -i c.png -filter_complex "[0][1][2]hstack=inputs=3" row.png
```

Use `vstack` for a vertical strip and `xstack` for a grid.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/pipeline.md ===== -->

# Workflow

## Step 0. Get the source (only if it is not already a local file)

```bash
python edit/tools/download.py "https://youtu.be/xxxxxxxxxxx" edit
```

Lands at `edit/source.mp4` regardless of the site (yt-dlp handles YouTube, Vimeo, and hundreds of others). Grabs native quality, not a capped resolution — editing needs headroom for crop/zoom that a tool built only for *watching* a video does not. Skip this step entirely when the user already handed you a file.

## Step 1. Inspect the source

```bash
ffprobe -v error -show_format -show_streams -print_format json "IMG_XXXX.MOV"
```

Note the resolution, fps, duration, codecs and audio bitrate. A typical vertical iPhone clip is 1080×1920 (sometimes 1072×1920, which `scale` will fix) at 60 fps.

Find the cuts that already exist inside the source — it is good practice to align your edit points with them:

```bash
ffmpeg -hide_banner -i "IMG_XXXX.MOV" -vf "select='gt(scene,0.25)',showinfo" -an -f null -
```

Pull a contact sheet and **open the frames via Read**. Scale the sampling rate to the source's length instead of a fixed `fps=1/9` — a nine-minute raw recording at that rate is 60 frames (fine), but a fixed-length interview at forty-five minutes is 300 (not fine, and most of them will be near-duplicates of a static talking head):

```bash
# step (seconds between frames) ≈ duration / 24, floored at 3s and capped at 20s
ffmpeg -y -i "IMG_XXXX.MOV" -vf "fps=1/<step>,scale=360:-1" edit/work/f_%02d.jpg
```

For a short clip under a minute, just use `fps=1/3` directly — the formula above is for longer or unfamiliar-length source you have not eyeballed yet.

Do not look for "what the video is about" — look for specifics: where the subject moves, sits down, stands up, fixes their hair; where the light and background change. Those places break cuts, and you need to know about them **before** you build the EDL.

Check the audio level:

```bash
ffmpeg -hide_banner -i "IMG_XXXX.MOV" -af volumedetect -f null -
```

## Step 2. Transcribe

```bash
ffmpeg -y -i "IMG_XXXX.MOV" -vn -ac 1 -ar 16000 -c:a pcm_s16le edit/work/audio.wav
```

Windows:

```powershell
$env:HF_HUB_DISABLE_XET="1"; $env:HF_HOME="D:\ai-models\hf"; $env:WHISPER_MODEL="large-v3-turbo"; $env:WHISPER_LANG="en"; python edit\tools\transcribe.py edit\work\audio.wav edit
```

macOS / Linux:

```bash
HF_HUB_DISABLE_XET=1 WHISPER_MODEL=large-v3-turbo WHISPER_LANG=en python3 edit/tools/transcribe.py edit/work/audio.wav edit
```

Set `WHISPER_LANG` to the language actually spoken, or leave it unset for auto-detection. The first run downloads the model — run it in the background and use the time for grading and overlay design.

No GPU, no 4 GB to spare, or this is a one-off machine you will not use again? Skip the model download entirely:

```bash
GROQ_API_KEY=... WHISPER_LANG=en python edit/tools/transcribe_cloud.py edit/work/audio.wav edit
```

Produces the same `transcript.json`/`transcript.srt`, so every later step is unaffected. Trade-off: no true per-word confidence (the API doesn't return one), so `dump_words.py`'s `p` column is a per-segment approximation — proofread by reading the whole transcript, not just the low-confidence words.

## Step 3. Proofread the text

```bash
python edit/tools/dump_words.py edit/transcript.json
```

Look at words with confidence `p` below 0.7, then read the whole thing. **Also open `transcript.json` directly and check the first and last segment by eye** — Whisper occasionally hallucinates a fabricated line over silence (classically a fake subtitler credit on Russian audio) that can carry a deceptively normal confidence score. Both transcription scripts print `HALLUCINATION SUSPECTED, DROPPED [...]` when they catch one automatically, but that filter is not airtight — see [troubleshooting.md #17](troubleshooting.md). Collect fixes in `edit/corrections.json` — the key is the word index, an empty string deletes the word:

```json
{
  "_note": "Recognition fixes: word index -> correct text. Empty string removes the word.",
  "22": "",
  "26": "burnout",
  "77": "unrealised",
  "105": "In"
}
```

Usual casualties: compound words fused together, prefixes swapped, proper nouns mangled. Expect around ten fixes per minute of speech with `small`, one or two with `large-v3`.

## Step 4. Agree on the concept

If the user has not specified a format, ask **in a single pass** — do not run a questionnaire: platform and length limit, the topic and what should go into graphics, brand colours and logo if any. Then pick a format from [storyboard.md](storyboard.md) and show the block structure before rendering anything.

## Step 5. The EDL is the edit

```bash
python edit/tools/pauses.py edit/transcript.json 0.28
```

Create `edit/edl.json`:

```json
{
  "source": "D:\\path\\to\\IMG_XXXX.MOV",
  "segments": [
    { "start": 0.00,  "end": 2.11,  "zoom": 1.00,  "t": "first line — note to self" },
    { "start": 2.36,  "end": 6.28,  "zoom": 1.045, "t": "second line" }
  ]
}
```

On Windows escape the backslashes in `source`: `D:\\video\\file.MOV`.

Cutting rules:

- **Cut pauses, not ideas.** In talking-head content every sentence carries meaning; aggressive cutting destroys the logic.
- **Cut at the end of a phrase.** Cutting on a stopwatch ("every 10 seconds") slices ideas in half.
- **Leave 0.2–0.3 s of each pause.**
- **Never touch dramatic pauses** — after a question, before a conclusion.
- **Alternate `zoom`** between neighbouring segments (1.00 / 1.05 / 1.09). Maximum on the climax.
- **Do not cut where the subject is moving.** If the cut is unavoidable, cover it with an infographic card.
- **Check that a segment does not end inside a scene change** in the source: if the scene changes 0.1 s before your cut, two frames of the next scene will flash in the output.

For reference: 73 seconds of talking-head monologue yields about 5 seconds of pauses to remove without losing a single idea.

```bash
python edit/tools/build.py base
```

Verify the cuts — pull frames either side of each one, stack them, open via Read:

```bash
ffmpeg -y -ss 6.10 -i edit/work/base.mp4 -frames:v 1 -vf "scale=300:-1" edit/work/cut1.png
```

```bash
ffmpeg -y -i edit/work/cut1.png -i edit/work/cut2.png -i edit/work/cut3.png -filter_complex "[0][1][2]hstack=inputs=3" edit/work/row.png
```

## Step 6. Subtitles

```bash
python edit/tools/make_ass.py edit/transcript.json edit/edl.json edit/subs.ass edit/corrections.json
```

The script re-times every word onto the post-cut timeline and separates events so lines cannot overlap.

## Step 7. Infographics

Write `edit/overlays.json` — a single file holding the CSS, the card markup and the timing. Template in `assets/templates/overlays.json`; techniques and palette in [design-system.md](design-system.md).

```bash
python edit/tools/render_overlays.py edit/overlays.json edit/overlays
```

## Step 8. Assembly and acceptance

```bash
python edit/tools/build.py final
```

Pull a frame on every card, stack them into rows of six with `hstack`, open via Read. Then the checklist:

- [ ] No card covers the speaker's eyes
- [ ] Subtitles stay inside the frame and never overlap each other
- [ ] Subtitle text has been proofread
- [ ] No flashes of the wrong scene on cuts, no clicks in the audio
- [ ] The change of framing is noticeable but not jarring — the cut reads as a deliberate choice
- [ ] There is at least one stretch with no graphics
- [ ] Technical parameters are correct:

```bash
ffprobe -v error -show_entries format=duration,size:stream=width,height,r_frame_rate -of default=nw=1 edit/out/final.mp4
```

```bash
ffmpeg -hide_banner -i edit/out/final.mp4 -af volumedetect -f null -
```

Expect 1080×1920, `+faststart`, and a mean around −18 dB after `loudnorm` to −14 LUFS.

Deliver the file with SendUserFile.

## What to rebuild after a change

```bash
python edit/tools/build.py base && python edit/tools/build.py final
```

| Changed | Rebuild |
|---|---|
| `edl.json` (cuts, zoom) | `base` → `make_ass.py` → `final` |
| `GRADE` in `build.py` | `base` → `final` |
| `overlays.json` | `render_overlays.py` → `final` |
| `corrections.json` | `make_ass.py` → `final` |

`final` is fast, `base` is noticeably slower. That is why graphics and subtitles can be iterated freely without touching the cut — the two-stage split exists precisely for this.

## Batch: several videos from one source

One transcript, several EDLs. Keep `edl-hook.json`, `edl-full.json`, `edl-teaser.json` and build each into its own output, swapping the filename in `build.py` or copying the chosen EDL over `edl.json` before building. The transcript and `corrections.json` are reused as they are.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/remotion.md ===== -->

# Remotion — animated graphics layer

[Remotion](https://www.remotion.dev) renders React components to video. It does not replace this pipeline; it slots into it as a third graphics tier.

## Install

```bash
claude plugin marketplace add remotion-dev/claude-code-plugin
```

```bash
claude plugin install remotion@remotion
```

Restart Claude Code afterwards. The plugin exposes skills named `remotion:remotion-*` — a router plus one skill per topic (create, markup, captions, render, studio, multimedia, interactivity, maps, saas, docs, upgrade). Load them the same way as any other skill; `remotion:remotion-best-practices` is the entry point.

**On Windows the install can fail** with `No ED25519 host key is known for github.com`. The plugin clones over SSH, and the OpenSSH shipped with Windows is too old for GitHub's current key exchange, so `ssh-keyscan` cannot fetch the host key either. Get the keys over HTTPS instead:

```powershell
$meta = Invoke-RestMethod https://api.github.com/meta
foreach ($k in $meta.ssh_keys) { Add-Content "$env:USERPROFILE\.ssh\known_hosts" "github.com $k" -Encoding ascii }
```

**Licence:** free for individuals and small teams, paid for companies above a certain headcount. Check <https://remotion.pro> before shipping commercial work.

## The three graphics tiers

| Tier | Tool | Cost | Use for |
|---|---|---|---|
| Static | HTML/CSS → headless Chrome → PNG | instant | cards, badges, lower thirds, final QR frame |
| **Animated** | **Remotion → transparent video** | slow, needs Node | counters, staged reveals, spring motion, karaoke captions with real animation |
| Composite | ffmpeg | fast | cutting, grading, layering, audio |

Reach for Remotion only when the motion itself carries meaning. A card that fades in does not need React — `render_overlays.py` already does that for free. A number that counts from 0 to 200, a bar that fills, text that assembles word by word with spring physics: that is where it pays.

## How it plugs in

Render the graphics **with an alpha channel**, then treat the result as just another overlay input to ffmpeg.

```bash
npx remotion render --image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444 MyOverlay overlay.mov
```

WebM is smaller if size matters:

```bash
npx remotion render --image-format=png --pixel-format=yuva420p --codec=vp9 MyOverlay overlay.webm
```

Then in the filtergraph, exactly like a PNG but without `-loop 1`:

```
-i overlay.mov
[1:v]format=rgba,setpts=PTS-STARTPTS+6.35/TB[o1];
[0:v][o1]overlay=0:0:eof_action=pass:repeatlast=0:enable='between(t,6.35,9.85)'[b1]
```

Keep the composition size identical to the reel (1080×1920) and the fps identical (30), or the overlay will drift.

## Batch: one composition, many reels

This is the real reason to bring Remotion into a ten-reel project. Define the graphics once, pass different props per reel:

```bash
npx remotion render MyOverlay out/1a.mov --props='{"headline":"200 VPN blocked","accent":"#7DDA58"}'
```

Drive it from `project.json` in a loop and the entire graphics layer for ten reels regenerates from one component. Changing the brand colour becomes a one-line edit instead of ten.

## Captions

`@remotion/captions` has `createTikTokStyleCaptions()`, which groups word-level timings into pages and exposes per-token `fromMs`/`toMs` for highlighting the active word. It consumes the same word-level data this pipeline already produces — `work/vo/<id>/transcript.json` maps onto the `Caption` format with a trivial rename.

Worth it when you want the words to animate (scale, spring, colour sweep). Not worth it for plain highlighted captions: `make_ass.py` already does those, burns them in one ffmpeg pass, and costs no Node install.

## When not to use it

- **The reel is a screencast with cards.** ffmpeg plus Chrome PNGs is faster end to end and has no build step.
- **You need it now.** First render pulls a headless browser and renders frame by frame — much slower than an ffmpeg overlay pass.
- **The project must run on a machine without Node.**

The honest split: this pipeline stays the backbone, Remotion is what you add when a client asks for motion the CSS layer cannot fake.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/setup.md ===== -->

# Setting up the workstation

Goal: on a machine that has nothing but Claude Code, get a working editing environment. Takes about ten minutes, eight of which are downloading the speech recognition model.

## 1. What is already there

Windows (PowerShell):

```powershell
foreach ($t in 'ffmpeg','ffprobe','python','node') { $c = Get-Command $t -ErrorAction SilentlyContinue; if ($c) { "$t => $($c.Source)" } else { "$t => MISSING" } }
```

macOS / Linux:

```bash
for t in ffmpeg ffprobe python3 node; do command -v $t >/dev/null && echo "$t => $(command -v $t)" || echo "$t => MISSING"; done
```

Chrome (needed to render the infographics):

```powershell
foreach ($p in "C:\Program Files\Google\Chrome\Application\chrome.exe","C:\Program Files (x86)\Google\Chrome\Application\chrome.exe","$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") { if (Test-Path $p) { "CHROME: $p" } }
```

And free space on the system drive — at least 4 GB is needed for the model:

```powershell
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{n='FreeGB';e={[math]::Round($_.Free/1GB,1)}} | Format-Table -AutoSize
```

## 2. Windows

Install one package at a time and check the result:

```powershell
winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
```

```powershell
winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
```

```powershell
winget install --id Google.Chrome -e --accept-source-agreements --accept-package-agreements
```

**Restart the terminal afterwards** — otherwise PATH will not pick the new binaries up.

If `winget` is unavailable, download ffmpeg manually from <https://www.gyan.dev/ffmpeg/builds/> — you need the **full build**; unpack it and add `bin` to PATH.

## 3. macOS

```bash
brew install ffmpeg python@3.12
```

```bash
brew install --cask google-chrome
```

## 4. Verify the ffmpeg build

Stripped-down builds are missing the filters this pipeline needs:

```powershell
ffmpeg -hide_banner -filters | Select-String -Pattern "drawtext|subtitles|curves|colorbalance|lut3d|overlay |zoompan|xfade|vidstab|loudnorm"
```

```bash
ffmpeg -hide_banner -filters | grep -E "drawtext|subtitles|curves|colorbalance|lut3d|overlay |zoompan|xfade|vidstab|loudnorm"
```

`subtitles` (that is libass) and `lut3d` are the critical ones. Without them half the pipeline will not run — install a full build.

## 5. Speech recognition

```bash
pip install faster-whisper
```

Pulls in `ctranslate2`, `onnxruntime` and `tokenizers` — roughly 200 MB. The model itself is downloaded separately on first run.

**Set this environment variable before the first run:**

```
HF_HUB_DISABLE_XET=1
```

Without it the model download from Hugging Face stalls after a few megabytes — the xet protocol simply does not work on some networks. Details and the other traps are in troubleshooting.md.

Choosing a model:

| Model | Size | Quality |
|---|---|---|
| `small` | 0.5 GB | acceptable; will need manual proofreading |
| `medium` | 1.5 GB | good |
| `large-v3-turbo` | 1.6 GB | close to large-v3 but noticeably faster — **the sweet spot** |
| `large-v3` | 3.1 GB | best |

If the system drive is tight, move the cache:

```
HF_HOME=D:\ai-models\hf
```

**Alternative: skip the local model entirely.** `transcribe_cloud.py` gets the same word-level output from Groq's (free tier) or OpenAI's Whisper API — no download, no disk space, works on a machine with no GPU. Get a key at <https://console.groq.com/keys>, then either export it or drop it in a `.env` file next to the audio:

```
GROQ_API_KEY=gsk_...
```

Trade-off: no per-word confidence score, and audio over ~24 MB (compressed) gets chunked and sent to the API in pieces rather than staying on your machine. Fine for a one-off edit; use local `transcribe.py` for anything recurring or privacy-sensitive.

## 5b. Optional: pulling source footage from a URL

If the footage lives at a URL rather than on disk (a share link, an unlisted upload, a recording someone sent), `download.py` needs `yt-dlp`:

```powershell
winget install --id yt-dlp.yt-dlp -e --accept-source-agreements --accept-package-agreements
```

```bash
brew install yt-dlp        # macOS
pip install -U yt-dlp      # any OS, fallback
```

Skip this entirely if the user always hands you a local file.

## 6. Project layout

```powershell
New-Item -ItemType Directory -Force "edit\tools","edit\work","edit\overlays","edit\out" | Out-Null
```

Copy the six scripts from this skill's `assets/tools/` into `edit/tools/`, and the templates from `assets/templates/` into `edit/`.

## 7. Acceptance test

```bash
ffmpeg -version
```

```bash
python -c "import faster_whisper; print('faster-whisper ok')"
```

Test the overlay renderer — create `edit/work/test.json`:

```json
{
  "css": ".t{position:absolute;left:70px;top:800px;right:70px;background:rgba(20,16,12,.88);border-radius:36px;padding:46px;color:#FFF6EC;font-size:60px;font-weight:700}",
  "items": [{ "id": "test", "html": "<div class='t'>Hello, overlay</div>" }]
}
```

```bash
python edit/tools/render_overlays.py edit/work/test.json edit/work
```

`edit/work/test.png` should appear — 1080×1920, transparent background, one card. Open it via Read. If the background is white rather than transparent, the `--default-background-color=00000000` flag went missing.

## 8. Optional third-party tools

**None of these are required.** They just save time:

**claude-real-video** — one command does the whole source breakdown: scene detection, frame de-duplication, transcript, HTML viewer. Replaces the "inspect the source" step entirely:

```bash
pip install "claude-real-video[fast]"
```

```bash
crv "IMG_XXXX.MOV" -o edit/crv --lang en --grid
```

**claude-video** (`/watch`) — a plugin that lets Claude look at video frame by frame. Needs a Groq or OpenAI key:

```bash
npx skills add bradautomates/claude-video -g
```

**digitalsamba/claude-code-video-toolkit** — a toolkit for generative video (Remotion, AI voice-over, scene generation, cloud GPU). Overkill for editing shot footage; useful when a video is assembled from code rather than from a camera. Worth borrowing its transition library and its `brands/` idea — a brand profile holding palette and fonts.

MCP servers are not needed for editing — everything runs as local commands.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/storyboard.md ===== -->

# Storyboarding and video formats

## Why storyboard at all

The temptation after transcribing is to jump straight into `overlays.json` and start laying out cards. Don't: you end up with a pile of panels and no rhythm. Map the video out in panels first — it is cheap, it edits as plain text, and it can be shown to the user before anything renders.

A **panel** is the state of the screen over a stretch of time: what is in frame, what the text says, what graphics are up. A one-minute video is 12–20 panels.

Order: transcript → semantic blocks → panels inside blocks → `overlays.json`. One block is one idea, usually 5–15 seconds and 1–3 panels.

## Panel types

| Type | On screen | When |
|---|---|---|
| **Clean speaker** | just the person and subtitles | connective tissue, transitions between ideas, breathing room |
| **Hook title** | large headline on top + scrim | first 3–6 seconds, the opening question |
| **Thesis card** | panel above the face, kicker + 1–2 lines | a key claim |
| **Rebuttal** | same, with a word struck through | "it isn't laziness", myth-busting |
| **List** | 2–4 bullets appearing one at a time | enumeration, mechanism |
| **Split / diagram** | two columns with a relation between them | contrast, before/after, innate vs acquired |
| **Pull quote** | large centred text, no panel | the climax, the strongest line |
| **Big number** | one huge figure + caption | statistics, duration, quantity |
| **CTA** | panel with an icon and an action | the ending |

Limitation of this pipeline: a panel is a PNG overlay on top of live footage. Full-screen inserts of other video and picture-in-picture circles are not available unless you have a second source. If you truly need one, it becomes another ffmpeg input rather than an overlay.

## The "thesis breakdown" format

Validated on a talking-head monologue, 73 s → 68 s. Works for any expert content.

| Share of runtime | Block | Panel |
|---|---|---|
| 0–8 % | Hook | Hook title with a question |
| 8–13 % | Rebuttal | Card with a struck-through word |
| 13–23 % | Cause | Thesis card |
| 23–38 % | Mechanism | Two-column diagram, second column appears separately |
| 38–54 % | Breakdown | List, bullets appearing one at a time |
| 54–64 % | Turn | **Clean speaker** — breathing room |
| 64–77 % | Consequences | Two-bullet list |
| 77–86 % | Climax | Pull quote + maximum zoom |
| 86–100 % | Ending | Two CTA panels back to back |

## Other formats

**"The list"** — "5 signs that…". Hook → numbered points, each with its own card and its own punch-in → conclusion. The easiest to assemble and trivially re-cut into separate clips.

**"The story"** — setup → problem → turning point → outcome. Minimal graphics, only subtitles and 2–3 accents: the story carries itself and cards smother it.

**"The case study"** — question → what was done → the number → how to repeat it. The key panel is the big number: one large figure filling the screen.

**"Reply to a comment"** — a screenshot of the question for the first 3 seconds, then the talking head. The screenshot is laid out as just another card in `overlays.json`.

## How to build the storyboard

1. Split the transcript into semantic blocks and write down their boundaries in source seconds.
2. Assign a panel type to each block. **Never repeat the same type back to back** — a list after a list reads as one long wall of text.
3. Convert the timings to the final timeline (the cut shifts everything left; see below).
4. Show the user the storyboard as a table: time, type, text. Changes are free at this stage and expensive after rendering.
5. Build the first panel, check it on a still frame, and only then produce the rest. Otherwise a positioning mistake will repeat itself twelve times.

## Converting timings

After cutting, time in the finished video no longer matches the source. The shift for a segment is:

```
offset_i = final_segment_start − source_segment_start
```

A word spoken at 44.81 in the source lands at 41.76 in the final cut when `offset = −3.05`. `make_ass.py` does this conversion for subtitles automatically; **for overlays you do it yourself** — write out the cumulative segment boundaries right after building `base` and keep them at hand.

To print the actual boundaries:

```bash
python -c "import json;s=json.load(open('edit/edl.json',encoding='utf-8'))['segments'];t=0
for i,x in enumerate(s):
    d=x['end']-x['start'];print(f\"seg{i+1}: {t:6.2f}-{t+d:6.2f}  (source {x['start']}-{x['end']}, shift {t-x['start']:+.2f})\");t+=d"
```

## Rhythm

- A panel lives **no less than 2 and no more than 8 seconds**. Less and it cannot be read; more and it becomes wallpaper.
- Leave 0.3–1 s of clean frame between panels, otherwise they smear into each other.
- For a one-minute video: 8–12 panels and at least one 4–6 second stretch with no graphics at all.
- Bullets appearing one at a time: two cards with identical markup, the extra bullet hidden by `opacity:0` in the first and revealed and highlighted in the second. Placed back to back, so the bullet "arrives" while nothing else moves.

## One take, many videos

A single source yields several different pieces with no reshoot: the full version, a 15-second teaser made of the hook and the climax, a separate clip per list item. The transcript and the proofreading are reused; only the EDL and the storyboard change. The visual style changes the same way — palette and typography live in one CSS block inside `overlays.json`, so restyling is a single-file edit rather than a rebuild.

## The generative branch

There is an approach where, after cutting, the pieces are sent to a video model (Google Flow / Veo) together with the storyboard and a prompt along the lines of "edit exactly to this storyboard, smooth transitions, leave the original audio untouched", and ffmpeg only stitches the results. It produces imagery that was never shot, but it requires paid access, manual work in someone else's UI, and it gives up frame-level control.

When it is worth it: you need visuals that do not exist in the footage, or you want to try a dozen radically different styles quickly. Otherwise the local pipeline is more predictable and edits as text. If the user wants that branch, the storyboard built from this file is exactly what gets fed to the model.

---

<!-- ===== SOURCE FILE: videoediting-claude-skill/skill/videoediting/references/troubleshooting.md ===== -->

# Known failures

Every one of these was hit on a real build. Read before your first ffmpeg run — it will save hours.

## 1. Model download stalls after a few megabytes

Hugging Face fetches files over the xet protocol by default, and on some networks it simply does not work: the download starts and then freezes. The process stays alive and reports no error.

```
HF_HUB_DISABLE_XET=1
```

With this variable the speed is normal, around 2–3 MB/s. Set it **always**.

Diagnosis: if the cache folder has not grown for two minutes, this is it — not a slow connection.

```powershell
"{0:N0} MB" -f ((Get-ChildItem "D:\ai-models\hf" -Recurse -File | Measure-Object Length -Sum).Sum/1MB)
```

## 2. Out of space on the system drive

`large-v3` is 3.1 GB and lands in `C:\Users\<name>\.cache\huggingface` by default. With no room the download dies with `os error 112` after several minutes of waiting.

```
HF_HOME=D:\ai-models\hf
```

Check free space **before** starting, not after. If less than 4 GB is free and there is nowhere to move the cache, use `small` and proofread through `corrections.json`.

## 3. `drawtext` fails with "Fontconfig error: Cannot load default config file"

ffmpeg on Windows has no fontconfig setup, so `drawtext` needs an explicit font file:

```
drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='...'
```

The `subtitles` filter (libass) works fine regardless — which is why all text in this pipeline goes through ASS rather than `drawtext`.

## 4. `subtitles=` breaks on paths containing a colon

Inside a filtergraph the colon separates parameters, so `subtitles=D:/path/subs.ass` parses as garbage:

```
Unable to parse "original_size" option value "/path/subs.ass" as image size
```

Fix: run ffmpeg with `cwd` set to the project folder and pass the relative path `subs.ass`. Non-ASCII characters in the path are not a problem. `build.py` already does this via `run(..., cwd=ROOT)`.

## 5. "Cannot allocate memory" when compositing overlays

`-loop 1 -i overlay.png` creates an **infinite** video stream. A dozen such inputs and ffmpeg consumes all available memory.

```
-loop 1 -framerate 30 -t 3.5 -i card.png
...,setpts=PTS-STARTPTS+6.35/TB[o1]
```

Bound the length with `-t`, position it in time with `setpts`.

## 6. `concat` fails with code −22

```
Could not open encoder before EOF
Task finished with error code: -22 (Invalid argument)
```

Every input to concat must match exactly. Append to each video segment:

```
setsar=1,format=yuv420p
```

And to each audio segment:

```
aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo
```

## 7. Subtitles overlapping each other

If an event has not ended before the next one starts, libass draws both lines on top of each other. `make_ass.py` handles this in a post-processing pass that clips each event's end to the next event's start — do not remove it.

Check:

```bash
python -c "
ev=[l for l in open('edit/subs.ass',encoding='utf-8-sig') if l.startswith('Dialogue')]
sec=lambda t:(lambda h,m,s:int(h)*3600+int(m)*60+float(s))(*t.split(':'))
bad=0;prev=0
for l in ev:
    p=l.split(',',4)
    if sec(p[1])<prev-0.001: bad+=1
    prev=sec(p[2])
print(len(ev),'events, overlaps:',bad)"
```

## 8. Subtitles running off the edge of the frame

With `WrapStyle: 2` a long line does not wrap, it simply leaves the screen. Keep `WrapStyle: 0`, the size at 72 or below with three words per line, and `MarginL/R` around 70.

## 9. PowerShell mangles decimal numbers

Under a non-English locale `$t = 5.95` becomes `5,95` when interpolated into a string, and ffmpeg does not understand that timecode — the file is silently never created.

```powershell
$times = @("5.95","6.10")   # strings, not numbers
```

## 10. PNG transparency is lost

Chrome paints a white background by default. Both pieces are required: the `--default-background-color=00000000` flag and `background:transparent` on `html, body` in the CSS.

## 11. A flash of the wrong scene on a cut

If an EDL segment ends inside a scene change in the source (the scene changes at 62.30 and the segment ends at 62.36), two frames of the next scene will flash in the output. Cross-check EDL boundaries against the scene list from `select='gt(scene,0.25)'`.

## 12. Clicks in the audio at cut points

A waveform truncated away from zero crossing produces a click. Fixed by 30 ms fades on each segment edge — the `AFADE` constant in `build.py`. Below 20 ms the click survives; above 50 ms the audio audibly dips.

## 13. Motion in frame at a cut point

Not an ffmpeg bug but a property of the material: the subject stands up, sits down or fixes their hair exactly where the cut lands, so the frame is smeared. Options, in order of effort: move the cut point; cover the moment with an infographic card; add a 0.3 s `xfade` (which shifts every subsequent timing).

This is exactly why the contact sheet must be reviewed **before** the EDL is built.

## 14. Speech recognised, but the text is wrong

Normal behaviour for `small`: compound words fuse, prefixes swap, inflections drift. Do not try to fix it by switching models mid-flight — proofread through `corrections.json` by word index. For a minute of speech that is about ten fixes and five minutes of work.

## 15. `transcribe_cloud.py` exits with "API error 413" or hangs on upload

413 means the compressed chunk still exceeds the provider's limit — check that `ffmpeg` actually produced the 64 kbps mono re-encode (`_upload_*.mp3` briefly appears in the output dir; if `ffmpeg` itself failed the script would have already exited, so this points at an unusually long single chunk). A hang on upload for several minutes with no output is normal for a long file on a slow connection — the compressed audio for an hour of speech is still only ~30 MB.

A 401 means the key is wrong or unset in the shell that actually runs the script — `.env` is only read from the audio file's folder and the current directory, not `~/.config`.

## 16. `download.py` fails or produces the wrong file

"yt-dlp not found" — installed but not on PATH after install; restart the terminal, same as ffmpeg in setup.md.

A private link, a geo-blocked video, or a login-walled page fails with yt-dlp's own error message printed to stderr — there is no workaround inside this pipeline; get a direct file instead.

If `source.mp4` exists from a previous run, the script skips the download and reports the old file — pass `--force` when the URL content actually changed.

## 17. A fabricated line appears in the subtitles that nobody said

The tell: a phrase like "Субтитры создал DimaTorzhok" (or "Subtitles by ...", "thanks for watching, don't forget to subscribe", any other YouTube-outro-shaped sentence) sitting over a stretch of the video where the speaker is silent or has already stopped talking — usually right at the end of the clip, sometimes at the start.

This is Whisper hallucinating, not a bug in the recognised speech. Both `large-v3` and `large-v3-turbo` were trained partly on YouTube's own auto-captions, which are full of community-subtitler credit lines and outro boilerplate; fed a stretch of silence or room tone, the model sometimes free-associates one of those instead of reporting "no speech." It does this on both the local (`transcribe.py`) and cloud (`transcribe_cloud.py`) path, because it is the same family of model either way.

Both scripts now guard against it and print `HALLUCINATION SUSPECTED, DROPPED [...]` when they catch one — that line in the console output is not an error, it is the safety net working. It is not airtight: a fluently-hallucinated line can score confident enough on both `no_speech_prob` and `avg_logprob` to slip through. **Always read the first and last segment of `transcript.json` yourself** before building subtitles — this is the one blind spot proofreading-by-confidence-score (Step 3) does not cover, because the fabricated text can carry a perfectly normal-looking confidence.

If one slips through anyway: remove it from `transcript.json` (or null it out via `corrections.json` by word index) and rebuild subtitles — do not just delete it from the finished `.srt`, or it will come back the next time anything upstream is rebuilt.
