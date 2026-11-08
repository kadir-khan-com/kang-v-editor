# Source: agent-video-editor — skill "editing-videos" (v2.0.0)

- **Source name:** kmilo93sd/agent-video-editor — the `editing-videos` Claude skill
- **Repo link:** https://github.com/kmilo93sd/agent-video-editor
- **Licence:** MIT. The cloned repo `LICENSE` file is the MIT License (Copyright (c) 2026 kmilo93sd), matching the earlier verified pass. The skill frontmatter refines it: "MIT (code and text); CC0-1.0 (audio in library/ and graphics in graphics/)".
- **Content map (one line):** 10 hard rules → sourced pacing table by video type (shot-change + silence values per type) → hook & retention guide → graphics/on-screen-text timing & caption rules → audio levels, ducking math & mastering targets → color order of work → thumbnail/title/description rules → how to apply the craft in NLEs/ffmpeg/Remotion/HyperFrames → media-licensing rules → universal pre-publish review checklist → 5 per-type recipes (talking head, vlog, podcast/interview, Shorts-from-long-form, narrated screen tutorial incl. synthetic-voice and HyperFrames generator docs) → meme-use policy.
- **Extraction method:** `git clone --depth 1` on 2026-11-05; every technique-bearing file reproduced **verbatim** below, each under its repo-relative path. Almost every number in this source carries a provenance tag: **official** (platform/vendor docs), **study**, **creator** (practice without public data) or **house** (learned reviewing real cuts).
- **Not reproduced (no technique content):** `CONTRIBUTING.md` (contribution process); `skills/editing-videos/library/LICENSES.md` and `skills/editing-videos/graphics/LICENSES.md` (per-asset licence/provenance ledgers for the bundled CC0 sound/graphics kits); `catalog.json` files and `search.mjs`/`verify.mjs` scripts (data/code for the bundled libraries, described in SKILL.md's index).

---

## Extracted content (verbatim, by source file)


---

## 📄 SOURCE FILE: `skills/editing-videos/SKILL.md` (verbatim)

---
name: editing-videos
description: >
  Gives an editor's judgment, with sourced numbers, for cutting and pacing, J and L cuts, jump cuts, b-roll,
  hooks and retention, captions, on-screen text and graphics, zoom and punch-in, audio levels in LUFS, music
  ducking, sound effects, basic color, thumbnails, titles, chapters and licensing. Use it when planning,
  scripting, editing, reviewing or publishing any video for YouTube, Shorts, Reels or TikTok: a talking
  head, a vlog, a podcast or interview, a screen tutorial, an explainer or a vertical clip from a long video,
  or when looking for royalty-free sound effects, music, animated graphics or a meme to recreate. Works with
  any tool (Premiere Pro, DaVinci Resolve, Final Cut Pro, CapCut, ffmpeg, Remotion, HyperFrames). Ships
  recipes per video type, a review checklist, a CC0 sound library, a CC0 graphics kit for HyperFrames, a
  meme reference with Content ID risk, and tested templates for narrated screen tutorials.
license: MIT (code and text); CC0-1.0 (audio in library/ and graphics in graphics/)
compatibility: >
  The editing craft needs nothing. The narrated screen tutorial templates need Node 20 or later and ffmpeg
  on the PATH, Playwright for recording, an ElevenLabs key for the voice, and HyperFrames for editing and
  rendering. The search tools of the sound library, the graphics kit and the meme reference need Node.
metadata:
  author: kmilo93sd
  version: "2.0.0"
  repository: https://github.com/kmilo93sd/agent-video-editor
---

# Editing videos

This skill gives an editor's judgment: when to cut, how long a shot or a caption lasts, how loud the music
goes, when a graphic helps and when it gets in the way. Every number says where it comes from: **official**
(platform or vendor docs), **study**, **creator** (practice without public data) or **house** (learned
reviewing real cuts). It is organized in two layers:

1. **The core** (this file, `references/` and `review-checklist.md`): craft that holds for any video and
   any tool.
2. **Recipes** (`recipes/`): what changes for one type of video. Load only the one that matches.

It does not replace the tool. On mechanics (file formats, APIs, a renderer's contract), the tool's own docs
or skills rule; on editorial matters, this skill does. `references/tools.md` maps the craft onto each tool.

## Process

| # | Step | What happens | Read |
|---|---|---|---|
| 1 | **Brief** | Video type, audience, platform and format (16:9 or 9:16), length, tool available. Pick the recipe | "Pick your recipe" below |
| 2 | **Story** | The promise (title and thumbnail idea) and a hook that delivers it in the first seconds; sections or chapters | `references/hook-and-retention.md` |
| 3 | **Assembly** | Select the best takes and order them; cut dead time; nothing is polished yet | `references/pacing-and-cuts.md`, the recipe |
| 4 | **Rhythm** | Shot length for the type, J and L cuts, jump cuts, b-roll, punch-ins | `references/pacing-and-cuts.md` |
| 5 | **Graphics and text** | Graphics only where they explain; text anchored to speech; captions | `references/graphics-and-text.md`, `graphics/`, `memes/` |
| 6 | **Audio** | Clean the dialogue, room tone, music under the voice, sound effects, then the master | `references/audio-and-sfx.md`, `library/` |
| 7 | **Color** | Exposure, white balance, matching shots; a look only after | `references/color.md` |
| 8 | **Review** | The recipe's checklist, then the core checklist, with frames and headphones | `review-checklist.md` |
| 9 | **Export** | Only with the person's approval: format, loudness master, check the file | `references/audio-and-sfx.md`, `references/tools.md` |
| 10 | **Publishing** | Title, thumbnail, description, chapters, captions, credits | `references/thumbnail-title-description.md`, `references/licenses.md` |

If the agent cannot touch the editor, it still does steps 1–8 as decisions: an edit decision list, a marker
list, caption files and instructions with numbers (`references/tools.md`).

## Hard rules (any video, any tool)

1. **Every cut has a reason**: it removes dead time, changes the information, or follows an action. Never
   in the middle of a word.
2. **Deliver the promise early.** What the title and thumbnail promise is seen or said in the first
   seconds; no logo intro or greeting before it.
3. **The voice is never fighting anything.** Music 18–25 dB under it and ducked, sound effects under it and
   never on a key word, room tone under every gap.
4. **Master once, to the destination**: -14 LUFS integrated and ≤ -1 dBTP for YouTube; -16 LKFS ± 1 for a
   podcast feed. Measured, not guessed.
5. **A graphic is never empty.** It enters at most 0.5 s before its word, has content within 1 s, and each
   element enters ≤ 0.6 s from when the voice names it **[house]**.
6. **Text stays long enough to read**: `max(1.5 s; words × 0.33 s + 0.5 s)`; captions ≤ 42 characters per
   line, ≤ 2 lines, ≥ 20 frames each.
7. **Zoom and punch-in only when motivated** by what is said, sharp, and never across a cut.
8. **Shots match**: exposure, white balance and levels consistent within a scene.
9. **Only licensed media**: CC0, the YouTube Audio Library, or a written license that allows commercial use.
   Nothing NC, nothing "found on YouTube". New sounds for the library leave their evidence in
   `library/LICENSES.md`. Graphics come from `graphics/` (CC0) or carry a recorded license. No copyrighted
   meme images, clips or sounds without a license: recreate the joke instead (`memes/README.md`).
10. **No invented numbers.** If no source supports a figure, say so and decide by the content.
11. **Nothing is rendered or published without approval**, and no cut is shown without passing its
    recipe's checklist and `review-checklist.md`.

## Pick your recipe

| The video is… | Recipe | What it adds to the core |
|---|---|---|
| One person talking to camera | [`recipes/talking-head.md`](recipes/talking-head.md) | Removing filler, softening jump cuts, punch-ins, b-roll on what is said |
| A day, a trip, an event | [`recipes/vlog.md`](recipes/vlog.md) | Finding the story, cold open, sequences, wind and location audio, matching cameras |
| A conversation with several cameras | [`recipes/podcast-to-youtube.md`](recipes/podcast-to-youtube.md) | Sync, cutting between angles, open mics, podcast master, chapters per topic |
| Vertical clips from a long video | [`recipes/shorts-from-long-form.md`](recipes/shorts-from-long-form.md) | Picking the moment, reframing to 9:16, burned-in captions, loops |
| A narrated software tutorial (screen recording) | [`recipes/narrated-screen-tutorial.md`](recipes/narrated-screen-tutorial.md) | The screen leads, honest speed, demo data, synthetic voice, chapter cards; tested templates (Playwright, ElevenLabs, HyperFrames) |
| Something else (explainer, essay, review…) | none | Use the core: the pacing table has a row per type; borrow from the closest recipe |

## Pacing at a glance

The full table, with the source of each number, is in `references/pacing-and-cuts.md`.

| Type | What is seen changes | Silence between phrases |
|---|---|---|
| Talking head | Every 2–5 s (creator) | 200–400 ms (creator) |
| Vlog | On events; film averages ≈ 4–5 s per shot (study) | Natural, with room tone |
| Explainer | First interrupt at 25–35 s, then every 2–3 min (creator) | 200–400 ms (creator) |
| Screen tutorial | When the action changes; shots ≥ 5 s (house) | ≥ 0.4 s (house) |
| Podcast / interview | On speaker changes and reactions; no source for a frequency | Natural pauses kept |
| Short / Reel / TikTok | Every 2–3 s; something new every 5–7 s (creator) | 200–300 ms (creator) |

## Audio at a glance

- **Master**: -14 LUFS, ≤ -1 dBTP for YouTube; upload AAC at 48 kHz.
- **Music** 18–25 dB under the voice, ducked 6–12 dB while someone talks.
- **Sound effects** 12–24 dB under the voice, one per on-screen event, the transient 2–4 frames before it.
- **Gains from measured levels**: `gain = 10^((voice_lufs - under_voice - sound_lufs)/20)`, capped at 1.

## CC0 sound library

`library/` ships 128 CC0 files, each measured in LUFS and true peak: 113 sound effects (mono WAV, 48 kHz,
-22 LUFS) and 15 music tracks (stereo MP3, 48 kHz, -16 LUFS). Categories: transition 18, click 12, appear
12, notification 11, success 7, error 5, typing 9, impact 5, stinger 14, office 17, ambience 3, music 15.
Paths below are relative to this skill's folder (for example `~/.claude/skills/editing-videos/`).

```bash
node library/search.mjs                          # categories
node library/search.mjs --category transition
node library/search.mjs whoosh --paths           # paths to copy
node library/search.mjs pop --voice -17          # with the gain for a voice at -17 LUFS
```

`--voice` puts effects 15 dB under the voice, music 20 dB and ambience 30 dB. Copy the files into the video
project; do not link them from outside it. Licenses and sources: `library/LICENSES.md` and
`references/licenses.md`. After adding a sound, run `node library/verify.mjs`.

## Graphics kit (CC0)

`graphics/` has 26 drop-in graphics for HyperFrames: arrows, circles and highlight rings, underlines and
scribbles, a spotlight, a cursor click ripple, callouts and tooltips, a lower third, keyboard-key chips, a
step counter, a progress bar, a countdown, a checkmark and a cross, a before/after split, chapter cards, an
end-screen layout, light-leak and grain overlays, and a generic like-and-subscribe prompt. Each is an HTML
snippet (plus an SVG for the shapes): a timed `.clip`, colors and sizes in `--gfx-*` custom properties, and a
`gfx.<name>(tl, el, opts)` function that adds seekable tweens to the composition's timeline. Anchor `at` to
the word that names the target; `catalog.json` gives each asset's duration and when not to use it.

```bash
node graphics/search.mjs                         # categories
node graphics/search.mjs --category arrows
node graphics/search.mjs shortcut --paths        # paths to copy
```

Open `graphics/preview.html` to see them all animate. After adding one, run `node graphics/build-preview.mjs`
and `node graphics/check.mjs`.

## Memes

`memes/catalog.json` is a reference of 59 memes and meme formats, with no media: what each one means, when
it fits in a tutorial, how long it stays on screen, how to recreate it with `graphics/`, who owns the
original and its Content ID risk. Recreate the joke or license the original; never use a meme's music. Read
`memes/README.md` first.

```bash
node memes/search.mjs fail --risk low
```

## Index

| File | What it covers |
|---|---|
| `references/pacing-and-cuts.md` | Pacing table by video type with sources; what a cut is for; shot length; J and L cuts; jump cuts; b-roll; transitions; segmentation |
| `references/hook-and-retention.md` | How YouTube measures retention; the hook by type; open loops; chapters; end screen and closing |
| `references/graphics-and-text.md` | When to use a graphic; anchored and never empty; text duration; captions and subtitles; zoom and punch-in; entrances; safe zones; legibility |
| `references/audio-and-sfx.md` | Target levels; dialogue cleanup; room tone; music and ducking; computing gains; sound effects; mastering |
| `references/color.md` | Order of work; LUTs as a starting point; matching shots; SDR and HDR delivery |
| `references/thumbnail-title-description.md` | Thumbnail spec and practices, A/B tests, title, description, hashtags, chapters |
| `references/licenses.md` | Music, SFX and footage sources for a monetized channel; fair use; Content ID |
| `references/tools.md` | Applying the craft in an NLE (EDL, markers, captions, instructions), ffmpeg, Remotion and HyperFrames |
| `review-checklist.md` | The universal review: measured, by eye, by ear, before publishing |
| `recipes/talking-head.md` | Talking-head recipe and checklist |
| `recipes/vlog.md` | Vlog recipe and checklist |
| `recipes/podcast-to-youtube.md` | Podcast and interview (multicam) recipe and checklist |
| `recipes/shorts-from-long-form.md` | Vertical clips from long videos: recipe and checklist |
| `recipes/narrated-screen-tutorial.md` | Narrated screen tutorial recipe, its house rules, process and checklist |
| `recipes/narrated-screen-tutorial/voice.md` | Script and synthetic voice for the tutorial: phonetic acronyms (Spanish narration), ElevenLabs, LUFS per chapter, whisper |
| `recipes/narrated-screen-tutorial/hyperframes-generator.md` | The tutorial edit in HyperFrames: skills per step, rules in the contract, the generator and its checks, pitfalls, review loop |
| `recipes/narrated-screen-tutorial/templates/` | Tested templates for that pipeline; each has `--help` |
| `library/` | CC0 sounds: `catalog.json`, `search.mjs`, `verify.mjs`, `LICENSES.md`, `sfx/`, `music/`, `tools/synthesize.py` |
| `graphics/` | CC0 HyperFrames graphics: `catalog.json`, `search.mjs`, `preview.html`, `check.mjs`, `LICENSES.md`, one folder per category |
| `memes/` | Meme reference with no media: `README.md` (read first), `catalog.json`, `search.mjs` |


---

## 📄 SOURCE FILE: `README.md` (verbatim)

<p align="center">
  <img src="assets/banner.svg" alt="agent-video-editor: a YouTube editor's judgment, for any AI agent" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/code-MIT-2ea44f"></a>
  <a href="skills/editing-videos/library/LICENSES.md"><img alt="CC0 audio" src="https://img.shields.io/badge/audio-CC0%201.0-5b8def"></a>
  <a href="skills/editing-videos/graphics/LICENSES.md"><img alt="CC0 graphics" src="https://img.shields.io/badge/graphics-CC0%201.0-5b8def"></a>
  <a href="https://agentskills.io/specification"><img alt="Agent Skills format" src="https://img.shields.io/badge/format-Agent%20Skills-f5b83d"></a>
  <a href="https://github.com/heygen-com/hyperframes"><img alt="Integrates HyperFrames" src="https://img.shields.io/badge/integrates-HyperFrames-8b7cf6"></a>
  <img alt="Language: English" src="https://img.shields.io/badge/language-English-lightgrey">
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#what-it-does">What it does</a> ·
  <a href="#the-rules">The rules</a> ·
  <a href="#audio-library">Audio library</a> ·
  <a href="#graphics-kit-and-meme-reference">Graphics and memes</a> ·
  <a href="#structure">Structure</a> ·
  <a href="#contributing">Contributing</a>
</p>

---

An AI agent can already cut footage, run ffmpeg, generate a voice and assemble a timeline. What it lacks is
an editor's judgment: when to cut, how much silence a phrase can take, when a graphic helps and when it gets
in the way, how loud the music should be. Without that, a vlog drags through every shot that was filmed, a
talking head keeps every "um", a Short spends its first three seconds on a logo, and a tutorial's graphics sit
empty while the voice talks about something else.

**agent-video-editor** is a skill that gives it that judgment, with numbers and sources: pacing per video
type, hooks, J and L cuts, captions, audio levels, color, thumbnails and licensing. It adds a recipe per type
of video (talking head, vlog, podcast, Shorts from long form, narrated screen tutorial), a CC0 library of
sounds and music, a CC0 kit of animated graphics, a meme reference with its Content ID risk, and tested
templates that **fail if the edit breaks a rule**.

It works with any agent that reads skills in the [`SKILL.md`](https://agentskills.io/specification) format
(Claude Code, Codex, Cursor, Gemini CLI and others) and with any editor: Premiere Pro, DaVinci Resolve, Final
Cut Pro, CapCut, ffmpeg, Remotion or HyperFrames.

## Install

**With [`skills`](https://github.com/vercel-labs/skills)**, for any compatible agent:

```bash
npx skills add kmilo93sd/agent-video-editor
```

**As a Claude Code plugin:**

```text
/plugin marketplace add kmilo93sd/agent-video-editor
/plugin install agent-video-editor@agent-video-editor
```

**By hand:** copy `skills/editing-videos/` into your agent's skills folder (in Claude Code,
`~/.claude/skills/`).

Then ask the agent things like:

> Here is the footage from my weekend trip to Lisbon. Find the story, give me a cold open and an edit list
> for a 10-minute vlog.

> Tighten this talking-head take: remove the filler, soften the jump cuts and tell me where a punch-in helps.

> Cut three Shorts from this podcast episode, with captions that fit 9:16 and a hook in the first second.

> Check the pacing of this software tutorial, then find a soft whoosh and a calm music bed and tell me how
> loud they go under the voice.

## What it does

The skill has two layers and three asset kits. The **core** is editing craft that holds for any video and
any tool; the **recipes** add what changes for one type of video, and the agent loads only the one it needs.
The **sound library**, the **graphics kit** and the **meme reference** are searched from the command line and
copied into the project.

| Core | |
|---|---|
| **Pacing with sources** | What a cut is for, shot length, J and L cuts, jump cuts, b-roll and transitions, with a pacing table for talking heads, vlogs, explainers, screen tutorials, podcasts and Shorts. Every number says where it comes from: official documentation, study, creator practice or our own experience. |
| **Hook and retention** | The first 30 s as YouTube measures them, a hook per video type, chapters, end screens. |
| **Graphics, text and captions** | Graphics anchored to the word that names them and never empty, reading time for text, caption timing and layout, zoom and punch-in, safe zones. |
| **Audio with levels** | Dialogue cleanup, room tone, music under the voice and ducking, sound effects, and masters for YouTube and podcast feeds, in LUFS and dB. |
| **Basic color** | Exposure, white balance and matching shots, LUTs as a starting point, SDR and HDR delivery. |
| **Publishing and licensing** | Thumbnail, title, description and chapters to YouTube's specification; which music, sound effects and footage are safe for a monetized channel. |
| **Any tool** | How to apply it in Premiere Pro, DaVinci Resolve, Final Cut Pro or CapCut (edit decision lists, markers, caption files, instructions with numbers), in ffmpeg, in Remotion or in HyperFrames. |
| **Review before showing** | A checklist of what is measured, what is seen and what is heard before a cut is shown. |

| Recipes | |
|---|---|
| **Talking head** | Removing filler, softening jump cuts, punch-ins, b-roll on what is said. |
| **Vlog** | Finding the story in the footage, cold open, wind and location audio, matching cameras. |
| **Podcast to YouTube** | Multicam sync, cutting between angles, open mics, a separate podcast master, chapters per topic. |
| **Shorts from long form** | Picking the moment, reframing to 9:16, burned-in captions, loops. |
| **Narrated screen tutorial** | The pipeline the skill was born from: Playwright recording, a synthetic ElevenLabs voice and a HyperFrames edit generator that **fails if the edit breaks a rule**, with tested templates. |

| Assets | |
|---|---|
| **Sound library** | 128 CC0 sounds and music tracks, measured in LUFS, with a search tool that computes how loud each one goes under your voice. |
| **Graphics kit** | 26 CC0 animated graphics for HyperFrames: arrows, highlights, callouts, lower third, progress, chapter cards, end screen and more. |
| **Meme reference** | 59 memes and meme formats: what they mean, when they fit, how to recreate them without the original, and their Content ID risk. No media. |

## The rules

<p align="center">
  <img src="assets/rules.svg" alt="The editing rules on a timeline: J-cut, fade, anchored graphic, continuous voice, zoom and music under the voice" width="100%">
</p>

The core's hard rules, for any video:

1. **Every cut has a reason**: it removes dead time, changes the information or follows an action.
2. **Deliver the promise early**: what the title and thumbnail promise shows up in the first seconds.
3. **The voice never fights anything**: music 18–25 dB under it and ducked, room tone under every gap.
4. **Master once, to the destination**: -14 LUFS and -1 dBTP for YouTube, -16 LKFS for a podcast feed.
5. **A graphic is never empty.** It enters at most 0.5 s before its word, has content within the first
   second, and each element appears 0.6 s or less from when the voice names it.
6. **Text stays long enough to read**, and captions follow subtitle timing (42 characters per line, 2
   lines, 20 frames minimum).
7. **Zoom and punch-in only when motivated**, and never across a cut.
8. **Shots match** in exposure, white balance and level.
9. **Only media with a clear license** (CC0, the YouTube Audio Library, or a written commercial-use
   license).
10. **No invented numbers**, and nothing rendered or published without approval.

Each recipe adds its own. The narrated screen tutorial, for example, adds that the screen leads and the
voice adapts, that speed is 1× except typing at 1.5× at most, shots of 5 s or more, zooms of up to 1.10, and
fake demo data only; its generator fails if the clip goes back, returns to a clip it already left, or leaves
more than 6 s without voice.

## Audio library

128 **CC0 1.0** files, with no attribution required and fit for monetized videos: 113 sound effects (mono WAV,
48 kHz, -22 LUFS) and 15 music tracks (stereo MP3, 48 kHz, -16 LUFS). Each one comes with its duration, its
loudness and true peak, and what it is for.

| Category | Files | Examples |
|---|---:|---|
| Transition | 18 | soft whoosh, page turn, risers, reverse cymbal, downlifter, glitch |
| Click | 12 | mouse click, tap, toggle, hover, select |
| Appear | 12 | pop, modal open and close, panel expand, drag and drop |
| Notification | 11 | notification, question, bell, alert, beeps, countdown |
| Success | 7 | success, chime, check mark |
| Error | 5 | soft errors, buzz |
| Typing | 9 | key press, keyboard typing (1 to 6 s), scroll |
| Impact | 5 | soft impact, dry thud, light wood |
| Stinger | 14 | win jingles, fanfare, intro and outro, serious, energetic |
| Office | 17 | coins, cash register, paper, pencil, book, stamp, calculator, clock |
| Ambience | 3 | room tone, office air conditioning, busy office (loops) |
| Music | 15 | ambient and emotional piano, lofi, acoustic, funky house, orchestral, tension |

```bash
node skills/editing-videos/library/search.mjs whoosh
node skills/editing-videos/library/search.mjs --category music --paths
node skills/editing-videos/library/search.mjs pop --voice -17
```

With `--voice`, the tool prints each sound's volume for a voice at that level: effects 15 dB under it, music
20 dB and ambience 30 dB. The origin of each file (Kenney, OpenGameArt or generated here, with the script that
makes them), with its page and the license text, is in
[`LICENSES.md`](skills/editing-videos/library/LICENSES.md).

## Graphics kit and meme reference

**Graphics kit.** 26 CC0 graphics for HyperFrames: arrows, hand-drawn circles and highlight rings, underlines
and scribbles, a spotlight, a cursor click ripple, callouts and tooltips, a lower third, keyboard-key chips, a
step counter, a progress bar, a countdown, a checkmark and a cross, a before/after split, chapter cards, an
end-screen layout, light-leak and grain overlays, and a generic like-and-subscribe prompt. Each one is an HTML
snippet with its timing, colors in CSS custom properties and a function that adds seekable tweens to the
composition's timeline. Open [`preview.html`](skills/editing-videos/graphics/preview.html) to see them all
animate.

```bash
node skills/editing-videos/graphics/search.mjs --category arrows
node skills/editing-videos/graphics/search.mjs chapter --paths
```

**Meme reference.** 59 memes and meme formats that work in tutorials and explainers, with what each one means,
when it fits, how long it stays on screen, how to recreate it with the graphics kit, who owns the original
and how likely it is to trigger Content ID. It ships no meme media on purpose: recreate the joke or license
the original. See [`memes/README.md`](skills/editing-videos/memes/README.md).

```bash
node skills/editing-videos/memes/search.mjs fail --risk low
```

## Structure

```text
skills/editing-videos/
├── SKILL.md                    entry point: process, core rules, pick your recipe, index
├── review-checklist.md         the universal review before showing a cut
├── references/                 the core: pacing and cuts, hook and retention, graphics and captions,
│                               audio, color, thumbnail and title, licenses, tools
├── recipes/                    one file per video type, loaded only when needed
│   ├── talking-head.md
│   ├── vlog.md
│   ├── podcast-to-youtube.md
│   ├── shorts-from-long-form.md
│   ├── narrated-screen-tutorial.md
│   └── narrated-screen-tutorial/
│       ├── voice.md            synthetic voice and script
│       ├── hyperframes-generator.md
│       └── templates/          recording, voice, verification, illustrations, edit and contact sheet
├── library/                    CC0 sounds and music: catalog, search, verify, licenses
│   ├── sfx/
│   ├── music/
│   └── tools/synthesize.py     reproduces the sounds generated for the library
├── graphics/                   CC0 HyperFrames graphics: catalog, search, preview, check, licenses
├── memes/                      meme reference (no media): catalog, search, README
└── evals/                      cases with what the agent should answer
```

The skill follows the [Agent Skills specification](https://agentskills.io/specification) and
[Anthropic's best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
the description says what it does and when to use it, SKILL.md stays under 500 lines, detail is loaded only
when needed, references are one level deep, and long files have a table of contents.

### Template requirements

The core and the general recipes need nothing: they work for planning, editing or reviewing a video made
with any tool. Only the narrated screen tutorial templates need:

- Node 20 or later and `ffmpeg` on the PATH.
- Voice: an ElevenLabs key and the `voice_id` in a `.env`, passed with `--env`. The templates do not search
  upwards for keys or copy them.
- Recording: Playwright. Editing and rendering: [HyperFrames](https://github.com/heygen-com/hyperframes) and
  its skills.

The search tools of the sound library, the graphics kit and the meme reference need Node. Rebuilding the
library's synthesized sounds with `library/tools/synthesize.py` needs Python with numpy, and `ffmpeg`.

## Language

The skill is written in English, and its editing guidance does not depend on the language of the video.
The voice recipe of the narrated screen tutorial
([`voice.md`](skills/editing-videos/recipes/narrated-screen-tutorial/voice.md)) covers Spanish narration:
its rules for spelled-out acronyms and phonetic spellings, and their examples, are in Spanish.

## Contributing

Contributions are welcome. Before opening a PR, read [CONTRIBUTING.md](CONTRIBUTING.md) and validate the
skill:

```bash
npx skills-ref validate ./skills/editing-videos
```

## License

- Code and text: [MIT](LICENSE).
- Sounds in `library/`: CC0 1.0, with each one's source in
  [`LICENSES.md`](skills/editing-videos/library/LICENSES.md).
- Graphics in `graphics/`: CC0 1.0, see [`LICENSES.md`](skills/editing-videos/graphics/LICENSES.md).
- The meme reference ships no meme media; the originals belong to their owners.


---

## 📄 SOURCE FILE: `skills/editing-videos/references/pacing-and-cuts.md` (verbatim)

# Pacing and cuts

Every number carries its source in brackets; the list is at the end. When sources disagree, each one's range
is shown, without averaging. Source types:

- **official**: platform or vendor documentation;
- **study**: published research;
- **creator**: blogs or analyses by creators or tools, useful but without public data behind them;
- **house**: a rule learned by reviewing real cuts. Here only the ones that hold for any video; the ones
  tied to one kind of video live in its recipe.

## Contents

- [Pacing table by video type](#pacing-table-by-video-type)
- [What a cut is for](#what-a-cut-is-for)
- [Shot length](#shot-length)
- [J and L cuts](#j-and-l-cuts)
- [Jump cuts: when they are fine](#jump-cuts-when-they-are-fine)
- [B-roll](#b-roll)
- [Transitions](#transitions)
- [Length and segmentation](#length-and-segmentation)
- [Sources](#sources)

## Pacing table by video type

"Change" means anything that renews what is seen: a cut, a punch-in, b-roll, a graphic or text. Where a
cell says "no serious source", decide by the content and say so.

| Type | How often what is seen changes | Shot length | Silence between phrases | Transitions | Recipe |
|---|---|---|---|---|---|
| **Talking head** | 2–5 s per shot, with jump cuts and punch-ins **[Ali Abdaal via blogs, creator]**; first 3 min every 10–15 s **[air.io, creator]** | No floor from a serious source; one idea per shot | 200–400 ms **[Syllaby, creator]**; Descript's gap shortener targets ~250 ms **[Descript, official for the tool]** | Hard cuts; a dissolve only for a change of topic | [`talking-head.md`](../recipes/talking-head.md) |
| **Vlog** | Driven by events, not a clock; film averages ≈ 4–5 s per shot **[Cutting 2011, study, film]** | Hold establishing shots long enough to read the place; no serious source for a number | Natural, with room tone under any gap | Cuts; match cuts and dissolves for time or place changes **[StudioBinder]** | [`vlog.md`](../recipes/vlog.md) |
| **Explainer** (voice over graphics or b-roll) | First interrupt at 25–35 s, then every 2–3 min **[air.io, creator]**; a "micro-hook" every 30–60 s **[TubeBuddy, creator]** or every 60–90 s **[vidIQ, creator]** | Film ≈ 4–5 s **[Cutting 2011]** | 200–400 ms **[Syllaby]** | Premiere's default dissolve is 1 s **[Adobe, official]** | none yet; use the core |
| **Screen tutorial** | When the action changes, not by the clock **[house]** | ≥ 5 s **[house]** | ≥ 0.4 s **[house]** | Hard cut within a step; a title card between steps | [`narrated-screen-tutorial.md`](../recipes/narrated-screen-tutorial.md) |
| **Podcast / interview** | Cut on speaker changes and meaningful reactions, not on a timer. No serious source for a frequency | Wide shot to re-establish, close-ups while someone talks; no serious source for numbers | Keep the conversation's natural pauses; cut only dead air and false starts | Hard cuts between angles | [`podcast-to-youtube.md`](../recipes/podcast-to-youtube.md) |
| **Short / Reel / TikTok** | 2–3 s per shot **[OpusClip, creator]**; something new every 5–7 s **[MrBeast analysis, creator]**; the first 3 s decide **[TikTok via blogs, creator]** | ~2 s floor if it carries text; 4 s max **[OpusClip, creator]** | 200–300 ms **[Syllaby]** | Hard cut, or 0.2–0.4 s | [`shorts-from-long-form.md`](../recipes/shorts-from-long-form.md) |

On-screen text has its own floor in every type: `max(1.5 s; words × 0.33 s + 0.5 s)`
(`graphics-and-text.md`). A shot carrying text never ends before its text can be read.

## What a cut is for

A cut is justified when it does at least one of these **[house]**:

1. **Removes dead time**: a pause, a false start, a wait, a repeated take. YouTube recommends planning cuts
   from the script and using jump cuts to remove filler **[YT-editing, official]**.
2. **Changes the information**: a new angle, the thing being talked about, a reaction.
3. **Follows the action**: cut on movement (a door opening, a hand reaching), so the motion hides the cut.

A cut that does none of these is noise. Never cut in the middle of a word, and avoid cutting in the middle
of a movement unless you are cutting on that action.

## Shot length

- **Average shot length in current film ≈ 4–5 s** **[Cutting 2011, study, film]**. It is a reference, not a
  target: dialogue scenes hold longer, action shorter.
- **Talking-head YouTube runs faster, 2–5 s per shot** **[Ali Abdaal via blogs, creator]**, because each
  cut removes a pause or adds a punch-in.
- **Verticals are faster again**: 2–3 s per shot, 4 s max **[OpusClip, creator]**.
- **Varied pacing, not even.** Alternate quick runs with a longer hold where the key point lands. For
  animation, the slowest move in a scene lasts about 3× the fastest **[hyperframes-creative/motion-principles]**.
- **The floor is legibility**: a shot must last as long as its text and its key detail take to read.

## J and L cuts

- **J cut**: the audio of the next shot starts before its picture. **L cut**: the audio of the current shot
  continues over the next picture **[TechSmith]**.
- Use them to soften a change of scene or speaker: in an interview, hear the answer start on the asker's
  face (J), or keep the speaker's last words over b-roll (L).
- Typical offset: a few frames to a couple of seconds. There is no serious source for a number; judge by
  whether the overlap is noticed.
- They matter most in interviews, vlogs and explainers. In a screen tutorial the voice should name what is
  already on screen, so they are rare there.

## Jump cuts: when they are fine

A jump cut is a cut between two shots of the same subject from (nearly) the same framing, so the subject
seems to jump. In film grammar it is an error; on YouTube it is an accepted way to remove filler from a
single-camera talking head **[YT-editing, official]**.

- **Fine**: one person talking to camera, removing pauses and fluffs; a deliberate time-lapse feel in a
  vlog.
- **Soften it** when it feels harsh: alternate a punch-in (scale 110–120 % or a crop from a higher
  resolution source) on every other cut, or cover the cut with b-roll **[creator practice]**.
- **Not fine**: in an interview or a multicam edit, where a real angle change is available; or when the cut
  leaves the subject in mid-gesture.

## B-roll

- **It shows what is being said.** Each b-roll shot illustrates the phrase on top of it; decorative b-roll
  that explains nothing distracts (coherence principle) **[Mayer, study]**.
- **Enter and leave on phrases**, not mid-word; an L cut out of b-roll back to the speaker reads naturally.
- **Hold a b-roll shot until its content is read**: a product close-up, a sign, a screen. A short insert
  that cannot be read is worse than none.
- **It covers jump cuts** and continuity errors.
- **License every clip** (`licenses.md`).

## Transitions

- **Cut = continuity.** **Dissolve = passage of time or a change of place or topic.** **Fade to black = end
  of a block** **[StudioBinder]**.
- Premiere's default dissolve lasts 1 s **[Adobe, official]**.
- UI-style graphic motion enters in ~225 ms and exits in ~195 ms; over 400 ms feels slow in an interface
  **[Material Design, official, for interfaces]**. In video, text has to be seen entering, so the core uses
  0.3–0.6 s (`graphics-and-text.md`).
- Flashy transitions (spins, glitches) on every cut age a video fast. Keep them for a deliberate style.

## Length and segmentation

- In 6.9 million edX sessions, videos under 6 minutes retained much better, and people came back to jump to
  the part they needed **[Guo 2014, study]**. On YouTube that maps to chapters (`hook-and-retention.md`).
- After publishing, the retention report shows where people leave; a dip at a specific moment says what to
  cut or re-edit **[YT-moments, official]**.

## Sources

- **[house]**: rules learned reviewing real cuts; see each recipe for the ones specific to a video type.
- **[Cutting 2011]**: Cutting, Brunick & DeLong, "How act structure sculpts shot lengths and shot transitions in Hollywood film", *Projections* 5(1). https://www.researchgate.net/publication/236964224_On_Shot_Lengths_and_Film_Acts_A_Revised_View
- **[Guo 2014]**: Guo, Kim & Rubin, "How video production affects student engagement", L@S 2014. https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf
- **[Mayer]**: Mayer (2008), *American Psychologist* 63(8). https://doi.org/10.1037/0003-066X.63.8.760
- **[YT-editing]**: YouTube Help, "Video editing tips". https://support.google.com/youtube/answer/11221953
- **[YT-moments]**: YouTube Help, "Measure key moments for audience retention". https://support.google.com/youtube/answer/9314415
- **[Adobe]**: Premiere Pro, default transition duration. https://helpx.adobe.com/premiere/desktop/add-video-effects/apply-video-transitions/change-transition-duration-using-the-effect-controls-panel.html
- **[Material Design]**: "Duration & easing". https://m1.material.io/motion/duration-easing.html
- **[StudioBinder]**: "What is a dissolve". https://www.studiobinder.com/blog/what-is-a-dissolve-in-film-definition/
- **[TechSmith]**: "How to edit videos: L-cuts and J-cuts". https://www.techsmith.com/blog/how-to-edit-videos-l-cuts-and-j-cuts/
- **[Descript]**: "Shorten word gaps". https://help.descript.com/hc/en-us/articles/10164807277453-Shorten-word-gaps
- **[Syllaby]**: "Voiceover pacing". https://syllaby.io/blog/voiceover-pacing-silence-trimming-retention-editing/
- **[air.io]**: https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8
- **[TubeBuddy]**: https://www.tubebuddy.com/blog/youtube-viewer-retention-to-increase-watch-time/
- **[vidIQ]**: https://vidiq.com/blog/post/audience-retention-secrets-youtube/
- **[OpusClip]**: https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
- **[MrBeast analysis]**: https://www.a4bcreative.com/post/the-pattern-interrupt-edit-how-to-keep-viewers-hooked-for-the-full-60-seconds
- **[Ali Abdaal via blogs]**: https://techbullion.com/an-ultimate-guide-to-ali-abdaal-video-editing-style-and-methods/
- **[TikTok via blogs]**: https://www.teleprompter.com/blog/tiktok-3-second-rule
- **[hyperframes-creative/motion-principles]**: the HyperFrames creative skill's motion principles (`hyperframes-creative/references/motion-principles.md`); the ratio holds for any animation tool.


---

## 📄 SOURCE FILE: `skills/editing-videos/references/hook-and-retention.md` (verbatim)

# Hook, retention, intro and outro

Sources in brackets; list at the end. **Official** = YouTube Help. **Creator** = blogs by tools or
creators, useful but without public data to back them.

## How YouTube measures retention (official)

- **Intro** is the percentage of the audience still watching after the **first 30 s** **[YT-moments]**.
- **Spikes**: parts that were rewatched or shared. **Dips**: parts that were skipped or where people
  stopped watching **[YT-moments]**.
- Key moments appear for videos of **≥ 60 s and ≥ 100 views** **[YT-moments]**.
- YouTube gives two levers for the intro **[YT-moments]**:
  1. make the thumbnail and title reflect the actual content;
  2. try different styles in the first 30 s.

After publishing, check the retention report. A dip at a specific moment shows what to cut or re-edit.

## The hook (first 5–30 s)

1. **Deliver the promise first.** What the title and thumbnail promise is seen or stated in the first
   seconds: the result, the most striking moment, the question the video answers. That is YouTube's lever 1
   **[YT-moments]**. By type:
   - talking head: the claim or the payoff in the first sentence;
   - vlog: the best moment of the day as a cold open, then back to the start;
   - tutorial: the end state on screen;
   - podcast clip: the strongest line of the conversation;
   - Short: the payoff or the setup of the payoff in the first frame.
2. **No logo intro, no greeting, no "in this video we'll see".** The logo goes on a card over content, not
   in a separate shot. TubeBuddy asks for the hook within the first 5 s **[TubeBuddy-hacks, creator]**; for
   Shorts, the first 3 s decide **[TikTok via blogs, creator]**.
3. **Be concrete.** Say who it is for and what they will get, with specifics (names, numbers, the actual
   thing), not generic promises like "it's that easy" or "from start to finish".
4. About half the audience is lost in the first minute **[TubeBuddy-hacks, creator]**. There is no official
   figure; take it as an order of magnitude.

## Keeping attention after the hook

- Renew what is seen at the pace of the video type (table in `pacing-and-cuts.md`). YouTube publishes no
  frequency for pattern interrupts; the figures there are creator practice.
- **Open loops**: announce something that pays off later ("the third one surprised me") and pay it off.
- **Cut tangents**, not just pauses: a dip in the retention graph usually sits on a stretch that does not
  move the video forward.

## Chapters (official)

YouTube's rules for chapters to work **[YT-chapters]**:

- the first timestamp is `00:00`;
- at least **3** timestamps, in ascending order;
- each chapter lasts **≥ 10 s**.

Automatic chapters are enabled on new uploads, but not every video gets them. For any long video
(tutorial, podcast, explainer, long vlog) write them by hand in the description, from the edit's real
times, not measured by eye. People jump to the part they need, and markers make that easier **[Guo 2014,
study; NN/g]**. A visible marker in the video (a title card or a lower third with the section name) helps
viewers who land mid-video.

## End screen and closing (official)

- The end screen takes up the **last 5–20 s**; the video needs to be **≥ 25 s**; up to **4 elements** in
  16:9 **[YT-end-screens]**.
- Leave those 5–20 s with a background and no important text where the elements will go. Otherwise the
  elements cover the content.
- The closing says where to go next (the next video, the guide, the full episode) in one sentence, without
  a long recap. Long sign-offs are where retention drops.
- End screens are not available on videos set as made for kids **[YT-end-screens]**. A Short does not rely on one: its loop is the closing ([`shorts-from-long-form.md`](../recipes/shorts-from-long-form.md)).

## Sources

- **[YT-moments]**: YouTube Help, "Measure key moments for audience retention". https://support.google.com/youtube/answer/9314415
- **[YT-chapters]**: YouTube Help, "Video chapters". https://support.google.com/youtube/answer/9884579
- **[YT-end-screens]**: YouTube Help, "Add end screens to videos". https://support.google.com/youtube/answer/6388789
- **[Guo 2014]**: https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf
- **[NN/g]**: https://www.nngroup.com/articles/instructional-video-guidelines/
- **[TubeBuddy-hacks]**: https://www.tubebuddy.com/blog/youtube-audience-retention-hacks-that-work/
- **[TikTok via blogs]**: https://www.teleprompter.com/blog/tiktok-3-second-rule


---

## 📄 SOURCE FILE: `skills/editing-videos/references/graphics-and-text.md` (verbatim)

# Graphics, on-screen text and captions

When to add a graphic or text, how long it lasts, how it enters, how to caption, and how it reads on a
phone. The tool that draws it does not matter: the numbers hold in an NLE's titler, in ffmpeg, in Remotion or
in HyperFrames (`tools.md`). Sources at the end.

## Contents

- [When to use a graphic](#when-to-use-a-graphic)
- [Anchored to speech, never empty](#anchored-to-speech-never-empty)
- [How long on-screen text lasts](#how-long-on-screen-text-lasts)
- [Captions and subtitles](#captions-and-subtitles)
- [Zoom and punch-in](#zoom-and-punch-in)
- [Entrances and exits](#entrances-and-exits)
- [Safe zones](#safe-zones)
- [Legibility on a phone](#legibility-on-a-phone)
- [Brand consistency](#brand-consistency)
- [Sources](#sources)

## When to use a graphic

1. **To show what the camera cannot**: a concept, a comparison, a number, a timeline, a map. Words with
   images teach more than words alone **[Mayer, study]**.
2. **To mark structure**: a section title, a lower third with a name, a step counter.
3. **Never decorative.** If the graphic can be removed without losing anything, it is not needed
   **[Mayer: coherence]**.
4. **Do not repeat the voice in text.** Narration plus the same text on screen teaches worse than narration
   alone (redundancy) **[Mayer]**. Text for what is not said: a name, a number, a key term, a link.
   Captions are the exception: they are an accessibility layer, not a graphic.

## Anchored to speech, never empty

A graphic that sits empty waiting for the voice reads as a mistake. In the first cut of the reference
tutorial a journal entry graphic sat for about 5 s as an empty frame. The rules that came out of it hold for
any narrated video **[house]**:

| Rule | Number |
|---|---|
| The graphic enters before the word that introduces it | **at most 0.5 s** before |
| Its first element with content appears | **within the first second** |
| Each row or element enters when the voice names it | **≤ 0.6 s** from its word |
| No card, table or frame stays without content | **for more than 1 s** |
| It stays after its last phrase | ~1.2 s, then leaves |

Elements enter **anchored to the words that name them** (from a transcript with word timings), not with an
even stagger: an even stagger brings in elements the voice has not named yet. Any tool that gives word
timestamps works: whisper, the NLE's transcript, a TTS alignment.

## How long on-screen text lasts

- **0.33 s per word** (160–180 words/min) **[BBC]**, or **20 characters/s** for adults and 17 for children
  **[Netflix-style]**.
- Minimum **20 frames (≈ 0.83 s)** per event **[Netflix-timing]**.
- Practical formula: `duration = max(1.5 s; words × 0.33 s + 0.5 s)`. The extra half second is for finding
  the text before reading it **[derived from BBC; the extra is house]**.
- A label that goes with the voice enters with its word and stays **until 0.6 s after it has been said, and
  never less than the formula above** **[house]**.

## Captions and subtitles

**Why:** many people watch without sound, and captions are what makes a video accessible **[NN/g]**.
YouTube's automatic captions can misrepresent speech because of accents, dialects or background noise, so
review them before publishing **[YT-auto-captions]**.

**Delivery formats:** YouTube accepts uploaded caption files, including SubRip (`.srt`), WebVTT (`.vtt`),
SubViewer (`.sbv`) and TTML **[YT-caption-formats]**. An uploaded file is searchable and switchable; burned-in
captions are neither, but they are the norm on Shorts, Reels and TikTok, where the style is part of the edit.

**Timing and layout** (closed captions, standard style) **[Netflix-style; Netflix-timing]**:

| What | Value |
|---|---|
| Characters per line | **≤ 42** |
| Lines | **≤ 2** |
| Reading speed | ≤ 20 characters/s for adults, ≤ 17 for children |
| Minimum duration | 20 frames (≈ 0.83 s) |
| Gap between events | at least 2 frames; either 2 frames or ≥ 0.5 s |
| After the speech ends | the caption stays ~0.5 s if nothing follows |
| Shot changes | start on the cut if speech starts within 0.5 s of it; end on the cut if within 0.5 s; cross a cut only if the speech does |
| Line breaks | after punctuation, before conjunctions or prepositions; never split an article from its noun or a first name from a last name |

**Burned-in social captions** (Shorts, Reels, TikTok) **[creator practice]**:

- 1–5 words per page, timed to the words, often highlighting the active word;
- large, bold sans-serif with an outline or a box for contrast over any background;
- placed above the platform's bottom UI and away from the right-hand buttons (see Safe zones);
- every page still respects the 20-frame minimum.

## Zoom and punch-in

- **Motivated by what is said**: the zoom goes to the detail the voice names, or punches in to stress a
  line. A zoom that points at nothing is noise **[house]**.
- **A zoom never crosses a cut**: it starts and ends within one shot **[house]**.
- **One at a time.** Space them out; Envision suggests 5–7 s between screencast zooms **[Envision,
  creator]**. Constant zooming reads as nervous.
- **Punch-in on a talking head**: a cut to 110–120 % on every other jump cut, or a crop from a higher
  resolution recording, so the image stays sharp **[creator practice]**. Beyond the source's resolution it
  gets soft.
- **Slow push-in** (a scale that creeps over seconds) for emotion or emphasis; a **hard punch-in** for a
  joke or a beat. How far and how fast depends on the type; screen recordings need much less (see
  [`narrated-screen-tutorial.md`](../recipes/narrated-screen-tutorial.md)).

## Entrances and exits

- **In UI**, Material Design uses 225 ms to enter, 195 ms to exit and 375 ms for large transitions, and
  warns that over 400 ms feels slow **[Material Design]**. That is for interfaces.
- **In video**, the text has to be seen entering **[house]**:
  - 0.35–0.6 s for cards and headlines, eased out, no bounce;
  - 0.3 s for rows;
  - 0.25 s for exits.
- **Vary speed on purpose**: the slowest animation in a scene lasts about 3× the fastest
  **[motion-principles]**.
- **No bounce or elastic on serious content**; a soft overshoot only on a call to action **[house]**.
- A short entrance with a 20–40 px offset plus opacity. Nothing that spins, bounces or zooms from 0.

## Safe zones

- Visible content inside the **90 % action-safe** (5 % margin per side) and text and key content inside the
  **80 % title-safe** (10 % per side). These are Premiere's default safe margins **[Adobe-safe]**.
- **Last 5–20 s** of a YouTube video: keep clear the area where end screen elements will go
  **[YT-end-screens]**.
- **Vertical (9:16)**: the platform's UI covers the bottom (caption, channel name) and the right side
  (buttons). Keep captions and key content in the central area and check in the platform's own preview. No
  official percentages could be verified; do not invent them.
- Lower thirds and badges stay clear of the player's progress bar.

## Legibility on a phone

- Body text **≥ 40–60 px tall at 1080p**; titles ~50 % larger **[legibility.info]**.
- Contrast **≥ 4.5:1** for normal text (WCAG AA) **[WebAIM]**. Over video, put text on a solid or scrimmed
  card, or give it an outline.
- At most one idea per card. If more than ~12 words have to be read while the voice talks about something
  else, voice and text compete **[Mayer]**.
- There is no official YouTube figure for the share of views from phones. Third-party figures (60–70 %)
  could not be verified; design for phones anyway.

## Brand consistency

- One skin across intro, cards, graphics, captions and closing: same palette, typography, radius, shadow
  and animation curve. Define it once (a style sheet, an NLE template, a design file) and reuse it.
- The brand appears where there is no content to show; footage does not need a frame around it.

## Sources

- **[house]**: rules learned reviewing real cuts; the never-empty rules come from the reference tutorial.
- **[Mayer]**: Mayer (2008), *American Psychologist* 63(8). https://doi.org/10.1037/0003-066X.63.8.760
- **[BBC]**: BBC Subtitle Guidelines, 160–180 words/min, read through https://www.clevercast.com/bbc-subtitling-guidelines/ because the BBC page did not load.
- **[Netflix-style]**: Netflix, "English (USA) Timed Text Style Guide" (42 characters per line, 2 lines, 20/17 cps, line breaks). https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977
- **[Netflix-timing]**: Netflix, "Subtitle Timing Guidelines" (20 frames minimum, 2-frame gaps, shot changes). https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394
- **[YT-auto-captions]**: YouTube Help, "Use automatic captioning". https://support.google.com/youtube/answer/6373554
- **[YT-caption-formats]**: YouTube Help, "Supported subtitle and closed caption files". https://support.google.com/youtube/answer/2734698
- **[NN/g]**: https://www.nngroup.com/articles/instructional-video-guidelines/
- **[Material Design]**: https://m1.material.io/motion/duration-easing.html
- **[Adobe-safe]**: Premiere Pro's default safe margins (action 10 %, title 20 % of the frame in total), also used by the HyperFrames preview (`hyperframes-studio` § 4).
- **[Envision]**: https://www.envision.everspringpartners.com/build/best-practices-for-screencast
- **[legibility.info]**: https://legibility.info/rules-for-text-in-videos
- **[WebAIM]**: https://webaim.org/articles/contrast/
- **[YT-end-screens]**: https://support.google.com/youtube/answer/6388789
- **[motion-principles]**: `hyperframes-creative/references/motion-principles.md`; the ratio holds in any animation tool.


---

## 📄 SOURCE FILE: `skills/editing-videos/references/audio-and-sfx.md` (verbatim)

# Audio: levels, music, ducking, SFX and mastering

Viewers forgive a soft image before they forgive bad audio. This file has the targets and the craft, in
any tool; how to apply them in a specific one is in `tools.md`. The skill's own sound library
([`../library/`](../library/)) ships CC0 sound effects and music, already measured. Sources at the end.

## Contents

- [Target levels](#target-levels)
- [Cleaning the dialogue](#cleaning-the-dialogue)
- [Room tone](#room-tone)
- [Music under the voice](#music-under-the-voice)
- [Computing a gain from measured levels](#computing-a-gain-from-measured-levels)
- [Sound effects: when to use them and when not to](#sound-effects-when-to-use-them-and-when-not-to)
- [Mastering for YouTube](#mastering-for-youtube)
- [Sources](#sources)

## Target levels

| What | Target | Source |
|---|---|---|
| Video master for YouTube | **-14 LUFS integrated**, **true peak ≤ -1 dBTP** | YouTube turns down what is louder than ~-14 LUFS and does not turn up what is quieter; it does not publish this in its Help, it is measured in "Stats for nerds" **[Frame.io; Pure Audio Insight, creator]** |
| Podcast feed (Apple Podcasts) | **-16 LKFS ± 1 dB**, true peak ≤ -1 dBFS | **[Apple Podcasts, official]** |
| Distribution of spoken content (reference) | -18 LUFS | AES TD1008 for "speech-only" **[AES TD1008 via Production Advice]** |
| Voice alone during the edit | -16 LUFS, LRA 4–8 LU | **[Sweetwater; Pure Audio Insight, creator]** |
| Background music under the voice | **18–25 dB under the voice** (voice at -16: music at -34/-41 LUFS) | **[Pure Audio Insight, creator]** |
| Music ducking while there is voice | 6–12 dB typical; Auphonic applies 18 dB by default; attack 10–50 ms, release 250–700 ms | **[Zella; Auphonic, official]** |
| Sound effects under the voice | 12–24 dB under the voice | **[Storyblocks, creator]** |
| Upload audio | AAC-LC (or Opus), **48 kHz**, 384 kbps stereo | **[YT-encoding, official]** |

**Why -14 and not louder:** going louder gains nothing, YouTube turns it down anyway. Staying well under
-14 does lose something: the video sounds quieter than its neighbors.

## Cleaning the dialogue

Order matters; each step works better on the output of the previous one **[creator practice]**:

1. **Pick the best source.** A lav or a close mic beats the camera mic; in multicam, choose one mic per
   speaker and mute the rest while they are not talking, to avoid echo and phasing.
2. **Noise reduction**, gently. Too much makes the voice sound underwater; leave some air.
3. **High-pass** around 80 Hz to remove rumble and handling noise (a common starting point, not a rule).
4. **EQ** for clarity, **compression** for even levels, a **de-esser** if sibilance hurts.
5. **Level** each clip so the voice sits steady across the video; then master once at the end.

Remove clicks, breaths that are louder than the words, and mouth noise only when they distract: a voice
with every breath removed sounds robotic.

## Room tone

Room tone is the ambient sound of the location with nobody talking. Record **at least 30–60 s** of it at
each location **[StudioBinder, creator]**, with the same mic and settings.

- Lay it under every gap left by a cut, so silences do not drop to digital silence (which sounds like a
  dropout).
- Use it to cover a removed cough or noise, and as the bed of a J or L cut.
- No room tone? Copy the cleanest quiet stretch from the recording itself.

## Music under the voice

- **A brief decision, not filler.** Background music that adds nothing hurts comprehension (coherence)
  **[Mayer, study]**. Use it for mood, energy or structure, and drop it where it competes.
- **Level:** 18–25 dB under the voice **[Pure Audio Insight]**.
- **Ducking:** dip the music while someone talks, 6–12 dB with soft attack and release **[Zella]**. Either
  with keyframes, an NLE's auto-ducking, a sidechain compressor, or a spectral carve that dips only the bands
  the voice uses (`tools.md`).
- **Melody-free beds** under long talking; music with vocals fights speech.
- **Edit music on its phrases**: cut or loop on a bar line, and end on a real ending or a fade, not
  mid-note. Hit the downbeat on a key cut when the music is foregrounded.
- **License it** (`licenses.md`).

## Computing a gain from measured levels

When you know the loudness of the voice and of a sound, compute the gain instead of guessing:

```
gain = 10 ^ ((voice_lufs - under_voice - sound_lufs) / 20)    capped at 1
```

- `under_voice`: 15 dB for sound effects by default (within the 12–24 dB range), ~20 dB for music, and
  ~30 dB for an ambience bed or room tone, which should be felt rather than heard **[house]**.
- Example: voice at -17, a pop at -23.7 → `10^((-17 - 15 + 23.7)/20)` = 0.38.
- If it comes out above 1, the sound is too quiet for that use: pick another one rather than amplifying.
- The library's `catalog.json` stores each file's LUFS, and `node library/search.mjs <term> --voice
  <voice_lufs>` prints the gain for each match, with those three defaults ([`../library/`](../library/)). Its music comes at
  -16 LUFS and its effects and ambience at -22 LUFS.

## Sound effects: when to use them and when not to

**Yes**, sparingly, when the sound confirms something that happens on screen:

| Moment | Effect in the library | Note |
|---|---|---|
| A section title card enters | `whoosh-soft` or `page-turn`, plus `impact-soft-1` as it settles | One per card |
| A graphic or card enters | `slide-1` / `slide-2` | Alternate so it does not repeat |
| An element appears when the voice names it | `pop-1` / `pop-2` | About 18–20 dB under the voice, and not on every element if there are more than 4 |
| A total adds up, a goal is reached | `success-1` | Rarely |
| An error shown on purpose | `error-1` | Soft, never looped |
| Animated typing in a graphic | `typing-clicks-3s` or `keyboard-typing-3s`, trimmed | Not over real recorded typing |
| Closing or final pull-back | `sweep-long` or `downlifter-2s` | |
| Build into a reveal (vlog, Short, intro) | `riser-short-2s`, ending on the visual change | Not under speech |
| A scene with no other room sound | `ambience-room-tone-30s` | ~30 dB under the voice |

The names are files in [`../library/`](../library/); `search.mjs` lists them by category.

- **Place the transient 2–4 frames before the visual change**, so the peak lines up with what is seen
  **[Storyblocks, creator]**. Trim any silence at the start of the file first.
- In vlogs and Shorts, effects carry more of the style (whooshes on transitions, risers before a reveal);
  the limits below still apply.

**No:**

- a whoosh on every continuity cut: those cuts should be invisible;
- the same sound more than 3 times in a row: the repetition is noticeable and tiring **[Storyblocks,
  creator]**;
- effects louder than the voice, or on top of a key word (a number, a name);
- sounds over real recorded sounds that already do the job (a real click, a real door).

## Mastering for YouTube

Master once, on the final mix, not per clip.

- **Target:** -14 LUFS integrated, true peak ≤ -1 dBTP. For a podcast feed, -16 LKFS ± 1 **[Apple
  Podcasts]**. If the same audio goes to both, make two masters.
- **Upload format:** AAC-LC, 48 kHz, 384 kbps stereo, in an MP4 with Fast Start **[YT-encoding]**.
- With ffmpeg, two `loudnorm` passes, copying the video without re-encoding:

```bash
ffmpeg -hide_banner -i render.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2> measure.txt
# read input_i, input_tp, input_lra, input_thresh and target_offset from the JSON at the end of measure.txt
ffmpeg -i render.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" -c:a aac -b:a 384k -ar 48000 final.mp4
```

- The `loudnorm` report goes to **stderr**, not stdout: reading stdout gives nothing.
- Verify with `ffmpeg -i final.mp4 -af ebur128=peak=true -f null -`: I close to the target, true peak ≤ -1.
- In an NLE: a loudness meter on the master bus (Premiere, Resolve and Final Cut each ship one) and
  a true-peak limiter last in the chain.

## Sources

- **[Frame.io]**: "Loudness for YouTube". https://workflow.frame.io/guide/loudness-for-youtube
- **[Pure Audio Insight]**: https://pureaudioinsight.com/blogs/content-production/perfect-youtube-audio-levels-creators-technical-guide
- **[Apple Podcasts]**: "Audio requirements" (-16 dB LKFS ± 1 dB, true peak ≤ -1 dB FS). https://podcasters.apple.com/support/893-audio-requirements
- **[AES TD1008 via Production Advice]**: https://productionadvice.co.uk/td1008/
- **[Sweetwater]**: https://www.sweetwater.com/insync/how-to-master-audio-for-youtube/
- **[Zella]**: https://zellahq.com/blog/music-ducking-explained/
- **[Auphonic]**: https://auphonic.com/help/web/multitrack.html
- **[Storyblocks]**: https://www.storyblocks.com/resources/blog/pump-youtube-videos-stock-sfx
- **[StudioBinder]**: "What is room tone". https://www.studiobinder.com/blog/what-is-room-tone/
- **[YT-encoding]**: YouTube Help, "Recommended upload encoding settings". https://support.google.com/youtube/answer/1722171
- **[Mayer]**: https://doi.org/10.1037/0003-066X.63.8.760
- **ffmpeg loudnorm**: https://ffmpeg.org/ffmpeg-filters.html#loudnorm; two passes: https://dev.to/masonwritescode/two-pass-loudness-normalization-with-ffmpeg-loudnorm-the-right-way-1nm3


---

## 📄 SOURCE FILE: `skills/editing-videos/references/color.md` (verbatim)

# Basic color

The goal of basic color in a YouTube video is not a look: it is **correct exposure, neutral white balance
and shots that match**. A look comes after, if at all. This file gives the order of work and the checks;
it gives no target numbers for skin or exposure, because none could be sourced well enough. Read the scopes,
not the screen.

## Order of work

1. **Normalize the footage.** Log or wide-gamut footage looks flat on purpose. Convert it to the delivery
   space first (a color space transform or the camera maker's conversion LUT), then correct.
2. **Exposure.** Set black and white points so nothing important is crushed or clipped, and the subject's
   face sits where it reads naturally. Check with the waveform, not by eye: a laptop screen in a bright room
   lies.
3. **White balance.** Neutral things (a white wall, a grey shirt, paper) should sit with R, G and B together
   on the parade. Skin should look like skin; the vectorscope's skin-tone line is a reference for hue, not a
   target for every face.
4. **Match shots.** Pick a hero shot per scene and match the others to it: same brightness of the face, same
   white balance, same contrast. In multicam, match every angle to one reference camera.
5. **Look (optional).** A creative LUT or a grade, applied the same way to every shot, with its strength
   dialed down if it pushes skin off.

## LUTs: a starting point, not a grade

- A **conversion LUT** (log to Rec.709) is technical: it belongs to the camera and profile it was made for.
  Use the right one, then correct exposure and balance after or before it as your tool's node or layer order
  requires.
- A **creative LUT** is a look. Applied on footage that is not normalized and balanced first, it amplifies
  the errors.
- Never stack LUTs blindly, and never trust one LUT for footage from different cameras.

## Consistency is the priority

- Viewers notice a jump in skin color or brightness between two cuts of the same scene more than a slightly
  imperfect grade. Match first.
- Lock camera settings while recording (manual white balance, exposure and ISO) so each clip does not drift
  on its own. Auto white balance under mixed light changes mid-shot.
- Screen recordings and graphics need no grade: leave them untouched so text stays crisp and colors
  match the brand.

## Delivery

- **SDR for YouTube is BT.709** **[YT-encoding, official]**. Export with the color space tagged so players do
  not guess.
- **HDR** needs HDR metadata in the file (PQ or HLG transfer, Rec. 2020 primaries); viewers on non-HDR
  devices see an SDR conversion, which you can guide with a LUT **[YT-HDR, official]**. If you are not sure
  you need HDR, deliver SDR.
- Check the export on a phone before publishing: most dark scenes that "looked fine" on the monitor get
  crushed there.

## Sources

- **[YT-encoding]**: YouTube Help, "Recommended upload encoding settings" (BT.709 for SDR). https://support.google.com/youtube/answer/1722171
- **[YT-HDR]**: YouTube Help, "Upload High Dynamic Range (HDR) videos". https://support.google.com/youtube/answer/7126552
- For scopes and node order in a given tool, its own manual: DaVinci Resolve Reference Manual (Color page), Adobe Premiere Pro's Lumetri Color and Lumetri Scopes help, Final Cut Pro's color correction help.


---

## 📄 SOURCE FILE: `skills/editing-videos/references/thumbnail-title-description.md` (verbatim)

# Thumbnail, title and description

**Official** = YouTube Help. **Creator** = widespread practice without public YouTube data. Sources at the
end.

## Thumbnail

**Specification (official)** **[YT-thumbnails]**:

- videos in 16:9, up to 3840×2160 and a minimum width of 640 px; Shorts in 9:16;
- JPG or PNG;
- up to 2 MB when uploaded from a phone and 50 MB from a computer;
- the account has to be verified.

Practical recommendation: export at **1920×1080 JPG under 2 MB**, which works for both paths.

**Practices:**

1. **What is promised is seen in the video.** The thumbnail and title must reflect what the first 30 s show.
   It is the first thing YouTube recommends for the intro **[YT-moments]**.
   - A misleading thumbnail violates the spam and deceptive practices policies **[YT-spam]**.
2. **Few words: 1–5, ideally 3–4**, in a heavy sans-serif, legible at ~180 px wide **[Snappa, creator]**.
   Do not repeat the title: complement it.
3. **One dominant subject and high contrast**; 2–3 elements at most **[GrowthOS, creator]**.
   - The subject is what the video delivers: the face with the reaction, the place, the product, the
     result of a tutorial, enlarged and cropped.
   - A face with a clear expression tends to raise CTR **[Snappa, creator]**, but there is no official
     figure.
4. **Bottom-right corner clear**: the video's duration goes there **[Pixelbatch, creator]**.
5. **Consistent brand skin** across the videos in a series (same typography and accent). That way the series
   is recognizable in the feed.
6. **Test.** YouTube allows **A/B tests of up to 3 titles and/or thumbnails**; the winner is the one with
   **more watch time**, not more clicks **[YT-AB]**. To judge a new thumbnail, YouTube suggests looking at
   the CTR for the first 24 hours in Home and Suggested **[YT-thumbnail-practices]**.

To produce the thumbnail: export a sharp frame of the key moment (any NLE's "export frame", or
`ffmpeg -ss <t> -i video.mp4 -frames:v 1 frame.png`) as a base, or shoot a dedicated photo, then add text and
branding in an image editor or a design tool.

## Title

- **Limit: 100 characters** **[YT-limits]**. Lists cut it off around 60–70; the important part goes in the
  first ~60 **[utilhq, creator]**.
- **Search or curiosity.** A video people search for (a tutorial, a review, a how-to) starts with what
  they would type: "How to …", "<product> review". A video people discover in the feed (a vlog, a story)
  leads with the curiosity or the stakes. Either way, the important words go first.
- No sustained capitals or clickbait: the title promises exactly what the video teaches.

## Description

- **Limit: 5,000 characters** **[YT-limits]**. What is visible before "Show more" is the first ~150
  **[utilhq, creator]**: that is where what the video teaches and the link to the written guide go.
- **Chapters**: a list of timestamps from `00:00`, at least 3, each ≥ 10 s **[YT-chapters]**. They are
  copied from the edit's real times (markers exported from the NLE, or a timeline file the tool writes),
  not measured by eye.
- **Hashtags**: YouTube shows up to 3 next to the title, and if there are **more than 60 it ignores all of
  them** **[YT-hashtags]**. Use 2–5 relevant ones.
- **Audio credits**: if music from the YouTube Audio Library with a Creative Commons license was used, the
  credit goes in the description **[YT-audio-library]**. The skill's own library is CC0: it requires no
  credit.
- **Corrections**: a `Correction:` line with the timestamp and the explanation, without re-uploading the
  video **[YT-limits]**.

## Sources

- **[YT-thumbnails]**: "Add video thumbnails". https://support.google.com/youtube/answer/72431
- **[YT-AB]**: "A/B test titles & thumbnails". https://support.google.com/youtube/answer/16391400
- **[YT-thumbnail-practices]**: https://support.google.com/youtube/answer/12340300
- **[YT-moments]**: https://support.google.com/youtube/answer/9314415
- **[YT-chapters]**: https://support.google.com/youtube/answer/9884579
- **[YT-hashtags]**: https://support.google.com/youtube/answer/6390658
- **[YT-limits]**: "Edit video settings". https://support.google.com/youtube/answer/57407
- **[YT-audio-library]**: https://support.google.com/youtube/answer/3376882
- **[YT-spam]**: "Spam, deceptive practices & scams policies". https://support.google.com/youtube/answer/2801973
- **[Snappa]**: https://snappa.com/blog/youtube-thumbnail-best-practices/
- **[GrowthOS]**: https://growthos.in/blog/youtube-thumbnail-best-practices
- **[Pixelbatch]**: https://pixelbatch.io/blog/youtube-thumbnail-size-guide
- **[utilhq]**: https://utilhq.com/articles/youtube-character-limits-seo-guide/


---

## 📄 SOURCE FILE: `skills/editing-videos/references/tools.md` (verbatim)

# Applying the craft in your tool

The craft in this skill does not depend on a tool. This file maps it onto what the agent actually has:
an NLE that a person drives, ffmpeg, Remotion or HyperFrames. When a tool's own rules clash with this skill,
the tool wins on mechanics (file formats, APIs, rendering) and this skill wins on editorial matters
(pacing, levels, when to use a graphic). Say so in the delivery.

## Contents

- [Which route fits](#which-route-fits)
- [NLEs: Premiere Pro, DaVinci Resolve, Final Cut Pro, CapCut](#nles-premiere-pro-davinci-resolve-final-cut-pro-capcut)
- [ffmpeg](#ffmpeg)
- [Remotion](#remotion)
- [HyperFrames](#hyperframes)
- [The same rule in each tool](#the-same-rule-in-each-tool)
- [Sources](#sources)

## Which route fits

| The agent has | It can produce | Best for |
|---|---|---|
| Only the person's NLE (no API access) | An edit decision list, a marker list, caption files and step-by-step instructions | Most YouTubers: the person keeps editing in their tool |
| A shell with ffmpeg | The finished file: trims, concatenation, crops, captions burned in, audio mix and master | Shorts from long videos, podcasts, quick talking-head cuts, any batch job |
| A Node project with Remotion | React compositions rendered to video | Videos built from data, templates, animated captions |
| HyperFrames and its skills | HTML compositions rendered to video, with lint and checks | Narrated explainers and tutorials, motion graphics; the reference pipeline in [`narrated-screen-tutorial.md`](../recipes/narrated-screen-tutorial.md) |

Whatever the route, the review is the same: [`../review-checklist.md`](../review-checklist.md).

## NLEs: Premiere Pro, DaVinci Resolve, Final Cut Pro, CapCut

The agent usually cannot click in the NLE, but it can do most of the thinking: read a transcript, decide
the cuts, and hand back something the NLE imports.

**What to hand back:**

1. **An edit decision list (EDL, CMX3600).** Premiere and Resolve import it as a timeline. One event per
   line: event number, reel, track, transition, source in, source out, record in, record out, all in
   timecode at the project's frame rate (24 fps in this example).

   ```text
   TITLE: talking-head-cut-v1
   FCM: NON-DROP FRAME

   001  A001     V     C        00:00:04:12 00:00:11:03 00:00:00:00 00:00:06:15
   * FROM CLIP NAME: A001.mov
   002  A001     V     C        00:00:13:20 00:00:21:00 00:00:06:15 00:00:12:19
   * FROM CLIP NAME: A001.mov
   ```

   EDLs carry cuts and simple dissolves, not effects, text or audio mixes. Check the frame rate and whether
   the footage is drop-frame before writing timecode.
2. **A marker list** (timecode + note) for what the person should do by hand: "punch-in to 115 % here",
   "b-roll of the street from 02:14 to 02:19", "duck music 10 dB under this line".
3. **Caption files** (`.srt` or `.vtt`): every NLE imports them, and YouTube accepts them directly.
4. **Instructions per step**, in the NLE's vocabulary, with numbers: "Essential Sound › Music › Ducking,
   reduce by 12 dB", not "lower the music a bit".

**Things that differ by NLE:**

- **Premiere Pro**: Text-Based Editing (cut by deleting transcript text), Essential Sound with auto-ducking,
  Lumetri scopes, multicam source sequences.
- **DaVinci Resolve**: the Cut and Edit pages for editing, Color page with scopes and color management,
  Fairlight for audio; multicam clips; a scripting API for automation where available.
- **Final Cut Pro**: magnetic timeline, multicam clips with an angle editor, roles for audio stems.
  FCPXML is its interchange format.
- **CapCut**: auto captions and templates aimed at vertical; good for Shorts, limited for long edits.

Feature names and menus change between versions. When giving instructions, say which version you assume,
and prefer telling the person the target (a level in LUFS, a duration in frames) over a menu path.

## ffmpeg

Enough for a whole edit when the edit is mostly cuts. Re-encode when you need frame accuracy: `-c copy`
only cuts on keyframes.

```bash
# Trim a segment, frame-accurate (re-encodes)
ffmpeg -ss 00:01:04.40 -to 00:01:31.00 -i in.mp4 -c:v libx264 -crf 18 -c:a aac -b:a 384k -ar 48000 seg01.mp4

# Join segments with the same codec settings (list.txt: one "file 'segNN.mp4'" per line)
ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4

# 16:9 to 9:16, centered crop, then scale to 1080x1920
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy vertical.mp4

# Burn captions from an .srt into the picture
ffmpeg -i vertical.mp4 -vf "subtitles=captions.srt" -c:a copy captioned.mp4

# Music ducked under the voice with a sidechain compressor
ffmpeg -i voice.wav -i music.wav -filter_complex \
  "[0:a]asplit=2[vo][sc];[1:a]volume=0.1[bed];[bed][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=500[duck];[vo][duck]amix=inputs=2:duration=first:normalize=0[mix]" \
  -map "[mix]" mix.wav

# Export one frame for a thumbnail base
ffmpeg -ss 00:02:14 -i in.mp4 -frames:v 1 frame.png
```

- The centered crop is a start: for a person who moves, crop per shot on the subject (see
  [`shorts-from-long-form.md`](../recipes/shorts-from-long-form.md)).
- `volume=0.1` is about -20 dB; compute it from measured levels instead (`audio-and-sfx.md`).
- Master the final file with the two-pass `loudnorm` in `audio-and-sfx.md`.
- Measure before deciding: `ffmpeg -i in.mp4 -af ebur128=peak=true -f null -` for loudness,
  `silencedetect` to find pauses worth cutting.

## Remotion

A React component per scene, rendered frame by frame **[Remotion]**.

- **Cuts and trims**: `<Sequence from durationInFrames>` places a piece on the timeline; `<OffthreadVideo>`
  or `<Video>` with `trimBefore` and `durationInFrames` picks the part of the source.
- **Ducking and fades**: `volume` accepts a function of the frame, so a fade or a dip under the voice is an
  `interpolate()` over frames.
- **Captions**: `@remotion/captions` parses `.srt` (`parseSrt`) and groups word timings into pages
  (`createTikTokStyleCaptions`), which fits the social caption style in `graphics-and-text.md`.
- **Never-empty graphics**: drive each element's entrance from the word timings, not from a fixed stagger.
- Master the rendered file with ffmpeg afterwards.

## HyperFrames

HTML compositions with `data-*` timing attributes, rendered deterministically, with its own skills for
each job **[HyperFrames skills]**. Load order:

| Step | Skill | What for |
|---|---|---|
| Entry | `hyperframes` | Always first: reads the project state, writes `BRIEF.md` or runs its `workflow` |
| Workflow | `general-video` (or the one the brief names) | Owns the deliverable end to end: plan, storyboard, build, review |
| Contract | `hyperframes-core` | Before writing HTML: `data-start`, `data-duration`, `data-media-start`, tracks, sub-compositions, determinism; recipes in `references/creator-editing-recipes.md` |
| Direction | `hyperframes-creative` | Brand skin (`frame.md` / `design.md`), narration, beat plan |
| Media | `media-use` | Resolve music, SFX, images and icons; transcribe; TTS |
| Motion | `hyperframes-animation`, `hyperframes-keyframes` | Animation rules and blueprints; zoom and punch-in on an inner wrapper |
| Blocks | `hyperframes-registry` | Before hand-drawing anything with a name (chart, terminal window, transition) |
| Mix | `hyperframes-audio` | Fades, voiceover carve of the music, automation, buses |
| Review and render | `hyperframes-cli` | `lint`, `check`, `snapshot`, `preview`, `render` |
| Notes on a built cut | `hyperframes-studio` | Questions and adjustments with the person; safe zones |

How the narrated tutorial pipeline uses it (a generator that writes the compositions and fails on broken
rules) is in [`hyperframes-generator.md`](../recipes/narrated-screen-tutorial/hyperframes-generator.md).

## The same rule in each tool

| Rule | NLE | ffmpeg | Remotion | HyperFrames |
|---|---|---|---|---|
| Cut out a pause | Delete the gap / ripple delete; EDL event boundaries | Trim segments and concatenate | Two `<Sequence>` pieces with different `trimBefore` | Two `<video>` pieces with different `data-media-start` |
| J or L cut | Unlink audio and extend it under the next shot | Offset the audio segments against the video ones | Audio `<Sequence>` starting before or ending after the video one | `<audio>` with its own `data-start` and `data-duration` |
| Punch-in | Scale 110–120 % on the clip | `crop` + `scale` on that segment | `transform: scale()` on a wrapper | Tween on an inner wrapper, never on the `.clip` |
| Music under voice | Auto-ducking or volume keyframes | `sidechaincompress` | `volume` as a function of the frame | `scripts/carve.mjs` from `hyperframes-audio` |
| Captions | Import `.srt`, style in the captions track | `subtitles=` filter | `@remotion/captions` | A caption track per `hyperframes-studio` |
| Master to -14 LUFS | Loudness meter + limiter on the master | Two-pass `loudnorm` | Render, then ffmpeg | Render, then ffmpeg |

## Sources

- **[Remotion]**: Remotion docs, `<Audio>` and `<OffthreadVideo>` (`trimBefore`, `durationInFrames`, `volume` as a function), and `@remotion/captions` (`parseSrt`, `createTikTokStyleCaptions`). https://www.remotion.dev/docs/
- **[HyperFrames skills]**: `hyperframes/SKILL.md`, `general-video/SKILL.md`, `hyperframes-core`, `hyperframes-audio` ("Voiceover carve"), `hyperframes-cli`, `hyperframes-studio` § 4. https://github.com/heygen-com/hyperframes
- **ffmpeg filters**: https://ffmpeg.org/ffmpeg-filters.html (`subtitles`, `crop`, `sidechaincompress`, `amix`, `loudnorm`, `ebur128`, `silencedetect`).
- **CMX3600 EDL**: the event format (event, reel, track, transition, source in/out, record in/out) is the one Premiere and Resolve import; check your NLE's import options for frame rate and reel names.


---

## 📄 SOURCE FILE: `skills/editing-videos/references/licenses.md` (verbatim)

# Licenses: music, sound effects and footage

What can be used in a monetized video without attribution and without Content ID surprises. The skill's own
library ([`../library/`](../library/)) is 100 % CC0 and its evidence is in
[`../library/LICENSES.md`](../library/LICENSES.md). Sources at the end.

## Contents

- [Audio: summary by source](#audio-summary-by-source)
- [Stock footage and images](#stock-footage-and-images)
- [Other people's clips and fair use](#other-peoples-clips-and-fair-use)
- [Rules](#rules)
- [Sources](#sources)

## Audio: summary by source

| Source | License | Attribution | Commercial use | Download | Content ID risk |
|---|---|---|---|---|---|
| **Kenney.nl** (audio) | CC0 | No ("would be nice but is not mandatory") | Yes | Direct zip, no account | Low |
| **OpenGameArt.org**, filtering for CC0 | CC0 (per piece; the site has other licenses too) | No | Yes | Direct, no account | Low, not zero |
| **Freesound.org** | Per sound: CC0, CC BY or CC BY-NC | CC0 no; CC BY yes; **CC BY-NC does not work** for a monetized channel | Only CC0 and CC BY | **Account required** to download; the API requires a key | Low for CC0 |
| **Sonniss GDC Game Audio Bundle** | Its own royalty-free license | No | Yes | Direct, no sign-up; ~7.5 GB | Low |
| **YouTube Audio Library** | YouTube's own; some tracks CC BY | Only the CC BY ones (credit in the description) | Yes, on YouTube | From YouTube Studio | None: YouTube says they are not claimed |
| **Pixabay** (music and sound effects) | Pixabay Content License | No | Yes, except selling it on its own | Direct | **High for music**: some authors register it in Content ID |
| **Incompetech** (Kevin MacLeod) | CC BY 4.0, **not CC0** | **Yes, required** | Yes | Direct | Low |

Detail for each row, with verbatim quotes:

- **Kenney**: every pack page says "License: Creative Commons CC0". The `License.txt` says "You may use
  these assets in personal and commercial projects. Credit … would be nice but is not mandatory."
  **[Kenney]**
- **Freesound**:
  - "To download a sound, first make sure you are logged into your registered account."
  - "For 'attribution' you should always mention the original creators."
  - "'Noncommercial' … you can't earn any money with the piece of work you create!" **[Freesound]**
  - The API requires its own credential (a token or, for some resources, OAuth2) **[Freesound-API]**, and
    downloading from the website requires an account. That is why it was not used for this library. It
    remains an option: create an account, filter by CC0 license and record each sound here.
- **Sonniss**:
  - "Everything is royalty-free and commercially usable."
  - "No attribution is required."
  - It forbids using the sounds to train AI and reselling them on their own **[Sonniss]**.
  - Useful when a specific effect is missing; it was not included because of its size.
- **YouTube Audio Library**:
  - "Copyright-safe music and sound effects downloaded from the Audio Library won't be claimed by a rights
    holder through the Content ID system."
  - "If you're using a track with a Creative Commons license, you must credit the artist in your video's
    description." **[YT-audio-library]**
  - The page only talks about use on YouTube: **do not use it for videos that also go to other networks**.
- **Pixabay**: the license allows use without attribution **[Pixabay-license]**. Its own FAQ acknowledges
  that some contributors "upload their tracks to Pixabay for free use but also register them with Content ID"
  **[Pixabay-FAQ]**. That is why **Pixabay music is not used unless you are willing to dispute claims**.
  - Careful: the sound effects `media-use` ships for use without a HeyGen credential come from Pixabay
    (`media-use/audio/assets/sfx/CREDITS.md`). For sound effects the risk is lower than for music, but they
    are not CC0.

## Stock footage and images

| Source | License | Attribution | Commercial use | Watch out for |
|---|---|---|---|---|
| **Pexels** (photos and video) | Pexels License | "Attribution is not required" | Yes, "free to use" | Identifiable people may not appear in a bad light; do not imply that a person or brand endorses you **[Pexels]** |
| **Pixabay** (photos and video) | Pixabay Content License | No | Yes | Do not sell or distribute the content on a standalone basis **[Pixabay-license]** |
| **Paid stock** (Storyblocks, Artgrid, Envato…) | Per the subscription | Per the license | Usually, while subscribed or per download | Read whether the license survives cancelling the subscription |
| **Your own footage** | Yours | No | Yes | Music playing in the background of a recording is still someone else's: it can trigger Content ID |

Footage with recognizable people, logos or private property can need a release beyond the copyright
license. The license covers the file, not everything in it.

## Other people's clips and fair use

- Fair use is decided case by case on four factors (purpose, nature of the work, amount used, effect on the
  market). **Giving credit does not turn a copy into fair use**, and there are no "magic words": a "no infringement intended" line does not protect you automatically
  **[YT-fair-use]**.
- Commentary, criticism and teaching that transform the clip have the best case; reposting it with music on
  top does not.
- Fair use is a US doctrine; other countries have narrower exceptions. When in doubt, do not use it.

## Rules

1. **On a monetized channel, only CC0, the YouTube Audio Library, or a license that explicitly says
   "commercial use without attribution"**, for audio and for footage. Nothing "NC", nothing without a
   written license, nothing "found on YouTube".
2. **Before adding a sound to the library**:
   - read the license on the pack's or the sound's page, not on an aggregator;
   - save the URL and the text in [`../library/LICENSES.md`](../library/LICENSES.md);
   - if the license is doubtful or cannot be found, it does not go in.
3. **CC BY works, but requires credit** in the description ("'Title' by Author, CC BY 4.0, link"). Note it in
   the brief so it is not forgotten at publishing time.
4. **Content ID does not look at the license.** A claim on CC0 or licensed material is a system error, not a
   violation. It is disputed in YouTube Studio with:
   - the link to the track's page;
   - the link to its license.
   A claim affects that video's monetization, not the channel's standing **[Pixabay-FAQ]**.
5. **Do not register free music in Content ID** under your own name: it is not yours and it causes claims
   against third parties **[Pixabay-FAQ]**.

## Sources

- **[Kenney]**: https://kenney.nl/assets/ui-audio (and the rest of the packs in `../library/LICENSES.md`)
- **[Freesound]**: https://freesound.org/help/faq/
- **[Freesound-API]**: https://freesound.org/docs/api/authentication.html
- **[Sonniss]**: https://gdc.sonniss.com/
- **[YT-audio-library]**: https://support.google.com/youtube/answer/3376882
- **[Pixabay-license]**: https://pixabay.com/service/license-summary/
- **[Pixabay-FAQ]**: https://pixabay.com/service/faq/
- **[Incompetech]**: https://incompetech.com/music/royalty-free/faq.html
- **[OpenGameArt]**: https://opengameart.org/content/faq
- **[Pexels]**: https://www.pexels.com/license/
- **[YT-fair-use]**: YouTube Help, "Fair use on YouTube". https://support.google.com/youtube/answer/9783148
- **CC0**: https://creativecommons.org/publicdomain/zero/1.0/


---

## 📄 SOURCE FILE: `skills/editing-videos/review-checklist.md` (verbatim)

# Review checklist before showing a cut

A cut is not shown until it passes this list and the checklist of its recipe (in `recipes/`). Check by
looking at frames and listening, not by imagining from the timeline or the code. Numbers and their sources
are in `references/`.

## 1. Measured

- [ ] **Loudness** of the final mix: -14 LUFS integrated, true peak ≤ -1 dBTP for YouTube (a separate
  master at -16 LKFS ± 1 for a podcast feed). Measured, not estimated: `ffmpeg -i final.mp4 -af
  ebur128=peak=true -f null -` or the NLE's loudness meter.
- [ ] **Duration** of the export matches the timeline; no black frames or silence at the head or tail.
- [ ] **Format**: the delivery resolution and frame rate, 9:16 for Shorts, SDR tagged as BT.709, audio at
  48 kHz.
- [ ] **Chapters** (long videos): from `00:00`, at least 3, ascending, each ≥ 10 s, taken from the edit's
  real times.
- [ ] **Captions**: no event shorter than 20 frames; ≤ 42 characters per line and ≤ 2 lines for standard
  captions; reading speed ≤ 20 characters/s.

## 2. By eye

Sample frames at the moments that matter (each graphic, each cut, the hook, the end) instead of scrubbing
the whole video; for a graphic, every 0.5 s from when it enters until it leaves.

- [ ] **Hook**: the first seconds show or say what the title and thumbnail promise; no greeting or logo
  intro first.
- [ ] **Cuts**: none in the middle of a word or an unmotivated movement; jump cuts are deliberate and
  softened where needed; nothing seen twice by mistake.
- [ ] **Graphics**: no frame with an empty box, table or card; elements appear when the voice names them;
  nothing stays long after its last phrase.
- [ ] **On-screen text**: lasts at least `max(1.5 s; words × 0.33 s + 0.5 s)`; contrast ≥ 4.5:1; ≥ 40 px
  tall at 1080p; inside title-safe (80 %), and in vertical, clear of the platform's UI.
- [ ] **Zoom and punch-in**: motivated by what is said, sharp (within the source's resolution), never
  across a cut.
- [ ] **Color**: exposure and white balance consistent between shots of the same scene; skin looks like
  skin; checked on a phone screen as well.
- [ ] **B-roll and footage**: each insert illustrates the phrase under it; all of it licensed.
- [ ] **Privacy**: no personal data that should not be there (addresses, documents, notifications,
  bystanders who should be blurred).
- [ ] **Last 5–20 s** of a YouTube video: free space for the end screen.

## 3. By ear (with headphones)

- [ ] The voice is intelligible everywhere and does not jump in level between sections or speakers.
- [ ] No cut drops to digital silence; room tone covers the gaps.
- [ ] The music does not compete with the voice (18–25 dB under, ducked) and ends on a phrase or a fade.
- [ ] Sound effects confirm something on screen, sit under the voice, do not cover a key word, and do not
  repeat more than 3 times in a row.
- [ ] No clicks, pops, echo from open mics or audible edits.

## 4. Before publishing (only with the person's approval)

- [ ] The render or export was approved after a preview; nothing is rendered or published without it.
- [ ] Watch the whole export at 1×, straight through, once. It does not replace the above: it confirms it.
- [ ] Every track, effect and clip has a license that allows this use, and CC BY credits are in the
  description (`references/licenses.md`).
- [ ] Title, thumbnail, description, chapters and captions ready
  (`references/thumbnail-title-description.md`).


---

## 📄 SOURCE FILE: `skills/editing-videos/recipes/talking-head.md` (verbatim)

# Recipe: talking head

One person talking to camera: commentary, advice, an essay, a reaction. The editing problem is that a
single static shot of a face gets tiring fast, and a recording is full of pauses, false starts and
repeats. The edit removes them and renews the image without breaking the person's rhythm. Sources at the end
of the file; the general numbers are in the core references.

## Structure

1. **Cold open (5–15 s):** the claim, the question or the payoff, in the person's best take of it. No
   greeting, no logo intro **[TubeBuddy-hacks, creator]** (`../references/hook-and-retention.md`).
2. **Context:** why it matters and what the viewer will get, in one or two sentences.
3. **Body in sections**, each opening with a line that works as a mini-hook. For videos past a few
   minutes, a section title or lower third per section, and the same names as YouTube chapters
   **[YT-chapters]**.
4. **Payoff and close:** the conclusion, then one sentence about where to go next, leaving the last
   5–20 s for the end screen **[YT-end-screens]**.

## Pacing and cuts

- **Shots of 2–5 s** in the typical YouTube style **[Ali Abdaal via blogs, creator]**, faster in the first
  minutes **[air.io, creator]**. A calmer essay can hold longer; the rule is that every cut removes something
  or adds something (`../references/pacing-and-cuts.md`).
- **Cut the pauses, keep the breath.** Gaps between phrases of 200–400 ms **[Syllaby, creator]**. Cutting to
  zero makes the person sound breathless and the jump cuts pile up.
- **Keep the best take** of each sentence and remove the others; listen for the one with the clearest
  emphasis, not the first or the last.
- **Jump cuts are fine here**: YouTube itself recommends them to remove filler **[YT-editing, official]**.
  Soften them by alternating framing: a punch-in to 110–120 % on every other cut, or a crop from a 4K source
  in a 1080p timeline so the punch-in stays sharp **[creator practice]**.
- **Cut on the eyes and the sentence, not on the gesture**: avoid cutting in the middle of a hand movement
  or a blink.
- **Punch in for emphasis**: a hard punch-in on the punchline or the key word; a slow push-in for a serious
  moment. Not on every cut.
- **B-roll, graphics and text** where the words name something that can be shown: a product, a place, a
  number, a quote on screen. Each insert illustrates the phrase under it; no decorative stock
  (`../references/graphics-and-text.md`).

## Audio

- **The voice is the video.** Clean it in order: noise reduction, high-pass, EQ, compression, de-ess
  (`../references/audio-and-sfx.md`).
- **Room tone under every cut** where the background noise would otherwise jump. Record 30–60 s of it
  **[StudioBinder, creator]**.
- **Music**, if any, 18–25 dB under the voice and ducked **[Pure Audio Insight, creator]**; melody-free under
  talking. Many talking-head channels use music only in the intro and section breaks.
- **Sound effects** on punch-ins and text pops at most, from [`../library/`](../library/) or a licensed
  source; never on every cut.
- **Master** to -14 LUFS, true peak ≤ -1 dBTP.

## Captions

- Upload a caption file (`.srt` or `.vtt`) or review YouTube's automatic captions, which can misrepresent
  speech **[YT-auto-captions]**.
- Burned-in captions are optional on long-form; if used, keep them short and clear of the end screen area.
- Text on screen for what is not said aloud: names, numbers, sources, links.

## Common mistakes

- Leaving the "um, so, basically" openings and the repeated takes: the edit's main job is removing them.
- Cutting every gap to zero, so the person never breathes.
- Punch-ins on every cut, or punch-ins that go past the source's resolution and get soft.
- Jump cuts that leave the head in a different position mid-sentence, so the cut is felt.
- Color and exposure drifting through the recording (daylight changing through a window); match the shots
  (`../references/color.md`).
- Background music that competes with the voice.

## Checklist for this recipe

Run it before the core [`../review-checklist.md`](../review-checklist.md).

- [ ] The first sentence delivers the promise of the title and thumbnail; no greeting first.
- [ ] No repeated takes, false starts or filler left; no gap cut to zero.
- [ ] Jump cuts alternate framing or are covered; none lands in mid-gesture or mid-blink.
- [ ] Punch-ins stay sharp (within the source's resolution) and are motivated by what is said.
- [ ] Room tone has no jumps at the cuts.
- [ ] Every b-roll or graphic illustrates the phrase under it, and is licensed.
- [ ] Skin tone and exposure are consistent from start to end.
- [ ] Sections have chapters in the description and, if long, on-screen titles.

## Sources

- **[YT-editing]**: YouTube Help, "Video editing tips". https://support.google.com/youtube/answer/11221953
- **[YT-chapters]**: https://support.google.com/youtube/answer/9884579
- **[YT-end-screens]**: https://support.google.com/youtube/answer/6388789
- **[YT-auto-captions]**: https://support.google.com/youtube/answer/6373554
- **[Ali Abdaal via blogs]**: https://techbullion.com/an-ultimate-guide-to-ali-abdaal-video-editing-style-and-methods/
- **[air.io]**: https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8
- **[Syllaby]**: https://syllaby.io/blog/voiceover-pacing-silence-trimming-retention-editing/
- **[TubeBuddy-hacks]**: https://www.tubebuddy.com/blog/youtube-audience-retention-hacks-that-work/
- **[StudioBinder]**: https://www.studiobinder.com/blog/what-is-room-tone/
- **[Pure Audio Insight]**: https://pureaudioinsight.com/blogs/content-production/perfect-youtube-audio-levels-creators-technical-guide
- **[creator practice]**: widespread practice among YouTube editors, with no single source; treat as a starting point.


---

## 📄 SOURCE FILE: `skills/editing-videos/recipes/vlog.md` (verbatim)

# Recipe: vlog

A day, a trip, an event, told with handheld footage, pieces to camera and the sound of the place. The
editing problem is the opposite of a tutorial: there is far too much footage, and the story has to be found
in it. Sources at the end of the file.

## Structure

1. **Cold open:** the best or most surprising moment of the video in a few seconds, before any
   introduction. It is the promise of the thumbnail (`../references/hook-and-retention.md`).
2. **Setup:** where we are, what is going to happen, what is at stake. A piece to camera works well.
3. **The story in beats**, each with a small question that the next scene answers ("will we make it?",
   "what's inside?"). Cut everything that does not move the story, however pretty.
4. **Payoff:** how it ended, said or shown, then a short close and the end screen in the last 5–20 s
   **[YT-end-screens]**.

For long vlogs, chapters named after the places or moments **[YT-chapters]**.

## Pacing and cuts

- **Events set the pace, not a clock.** There is no serious source for a shot length in vlogs; film averages
  ≈ 4–5 s per shot **[Cutting 2011, study]** and is a fair reference for b-roll sequences.
- **Establishing shots** (the place, the sign, the street) long enough to read where we are, then closer
  shots.
- **Sequences of 3–5 shots** for an action (wide, medium, detail) read better than one long handheld take.
- **Cut on action**: someone opens a door in one shot and walks through it in the next.
- **Time jumps**: a jump cut, a quick montage with music, or a dissolve for a longer passage of time
  **[StudioBinder]** (`../references/pacing-and-cuts.md`).
- **J and L cuts** carry the voice or the ambient sound across a change of place, so the cut feels natural
  **[TechSmith]**.
- **Speed ramps and time-lapses** for travel and waiting; hold real time for the moments that matter.

## Audio

- **Dialogue first.** Pieces to camera recorded outdoors need a windscreen (a furry cover on the mic);
  wind noise cannot be fully removed in the edit **[creator practice]**. A lav or a shotgun mic beats the
  camera's built-in mic.
- **Ambient sound is part of the story**: keep the sound of the place under the b-roll at a low level
  instead of muting it; add room tone or ambience under cuts so the background does not jump.
- **Music** sets the mood of each section and can change between sections. Under speech, 18–25 dB under the
  voice and ducked **[Pure Audio Insight, creator]**; in montages without speech it can lead.
- **Cut music on its phrases** and use the downbeats for key cuts in montages.
- **Music heard in the location** (a café, a shop, a street performer) can trigger Content ID even if it was
  just playing in the background. Mute or cover it (`../references/licenses.md`).
- **Master** to -14 LUFS, true peak ≤ -1 dBTP (`../references/audio-and-sfx.md`).

## Color

- Footage from different cameras and times of day has to be matched: same white balance and skin tone in
  each scene (`../references/color.md`).
- Phone footage and action cameras have their own color; match them to the main camera, not the other way.
- A consistent look across the video is part of the channel's identity; keep it subtle enough that skin
  still looks like skin.

## Captions and text

- Upload or review captions for the speech **[YT-auto-captions]**.
- Text on screen for places, names, prices, times: what the viewer would ask "where is this?".
- Burned-in captions only for short spoken bits, or when the video will be cut into Shorts.

## Privacy

- People in the background did not agree to be in the video: blur faces and license plates when they are
  identifiable and the focus, and never show addresses, documents or screens with personal data **[house]**.

## Common mistakes

- Keeping everything that was filmed: long, aimless walking shots and repeated views of the same place.
- A cold open that is not in the video, or that gives away the end without making people want to see how.
- Wind noise on the pieces to camera.
- The background music from a location left in, causing a claim.
- Music too loud under speech, or one track for the whole video.
- Shaky footage left in where a stabilizer or a different shot would do.
- Mismatched color between phone and camera footage.

## Checklist for this recipe

Run it before the core [`../review-checklist.md`](../review-checklist.md).

- [ ] The cold open shows a moment that is in the video and is the thumbnail's promise.
- [ ] Every scene moves the story; no scene repeats what a previous one already showed.
- [ ] Places are established before the detail shots.
- [ ] Pieces to camera are intelligible, with no wind noise and no music fighting them.
- [ ] No unlicensed music from locations; all added music and footage is licensed.
- [ ] Phone and camera footage match in color and exposure.
- [ ] No identifiable bystander, plate or personal data that should be blurred.
- [ ] Chapters in the description for long vlogs; end screen space free.

## Sources

- **[Cutting 2011]**: https://www.researchgate.net/publication/236964224_On_Shot_Lengths_and_Film_Acts_A_Revised_View
- **[StudioBinder]**: "What is a dissolve". https://www.studiobinder.com/blog/what-is-a-dissolve-in-film-definition/
- **[TechSmith]**: https://www.techsmith.com/blog/how-to-edit-videos-l-cuts-and-j-cuts/
- **[Pure Audio Insight]**: https://pureaudioinsight.com/blogs/content-production/perfect-youtube-audio-levels-creators-technical-guide
- **[YT-chapters]**: https://support.google.com/youtube/answer/9884579
- **[YT-end-screens]**: https://support.google.com/youtube/answer/6388789
- **[YT-auto-captions]**: https://support.google.com/youtube/answer/6373554
- **[creator practice]**: widespread practice among vloggers and sound recordists, with no single source.
- **[house]**: a rule of this skill; no published source.


---

## 📄 SOURCE FILE: `skills/editing-videos/recipes/podcast-to-youtube.md` (verbatim)

# Recipe: podcast or interview to YouTube (multicam)

Two or more people talking, recorded with several cameras and one mic per person. The editing problem is to
make a long conversation watchable: always show who matters at that moment, keep the audio clean when people
talk over each other, and give viewers a way to jump around. Sources at the end of the file.

## Contents

- [Before editing: sync and audio](#before-editing-sync-and-audio)
- [Structure](#structure)
- [Cutting between cameras](#cutting-between-cameras)
- [Trimming the conversation](#trimming-the-conversation)
- [Audio](#audio)
- [Captions and chapters](#captions-and-chapters)
- [Clips for Shorts](#clips-for-shorts)
- [Common mistakes](#common-mistakes)
- [Checklist for this recipe](#checklist-for-this-recipe)
- [Sources](#sources)

## Before editing: sync and audio

1. **Sync every camera and mic** to one timeline. NLEs build multicam clips synced by timecode or by audio;
   a clap or a slate at the start makes audio sync reliable. Check sync at the start, middle and end: some
   cameras drift over long recordings.
2. **One mic per person** is the source of the dialogue. Camera audio is only for syncing.
3. **Clean each mic track** (noise reduction, high-pass, EQ, compression) before cutting, then level the
   speakers to each other (`../references/audio-and-sfx.md`).

## Structure

1. **Cold open (15–60 s):** the strongest exchange of the episode, cut tight, before the intro. It is the
   promise of the title and thumbnail **[YT-moments]** (`../references/hook-and-retention.md`).
2. **Short intro:** who is talking and about what, in one or two sentences. No long branded intro.
3. **The conversation in topics.** Each topic is a chapter **[YT-chapters]**.
4. **Close** and end screen in the last 5–20 s **[YT-end-screens]**.

## Cutting between cameras

There is no serious source for how often to switch angles; cut on the conversation, not on a timer.

- **Show who is talking**, in a close-up, for most of their turn.
- **Cut on the speaker change**, ideally a beat after the new person starts (an L cut of the previous
  speaker's last words over the new face, or a J cut that lets us hear the answer start on the asker)
  **[TechSmith]**.
- **Reactions are content**: a laugh, a surprised face, a nod at the key line. Cut to them when they say
  something; not for every "mm-hm".
- **The wide shot** re-establishes the room: at the start, after a topic change, during fast cross-talk
  where a close-up would cut too often.
- **Long monologues**: alternate close-up, a medium shot and the wide, or a punch-in, so one face is not on
  screen for minutes. B-roll or a graphic when the person names something that can be shown.
- **Eyelines**: in a two-camera setup, each person looks off-frame toward the other; keep the cameras on the
  same side so they look at each other across the cut.

## Trimming the conversation

- **Remove dead air, false starts, off-topic stretches and technical problems**, but keep the conversation's
  natural pauses and rhythm: an interview cut like a talking head stops sounding like a conversation.
- **Cuts in the audio** are covered by a camera change, so they do not show as jump cuts. That is the
  multicam edit's advantage: cut audio first, then choose the angle.
- **Do not change meaning.** Joining the start of one answer to the end of another can put words in
  someone's mouth.
- **Cross-talk**: keep both mics open while people overlap, then mute the one not speaking.

## Audio

- **Mute the mics of people who are not talking** (or gate them), so one mic does not pick up the other
  voice late and create an echo.
- **Level the speakers to each other**, so nobody is louder than the rest.
- **Room tone** under cuts so the background does not jump; record 30–60 s before starting **[StudioBinder,
  creator]**.
- **Music** only for the intro, outro and topic breaks; not under the conversation.
- **Masters**: -14 LUFS / -1 dBTP for YouTube; if the audio also goes to podcast feeds, a separate master at
  -16 LKFS ± 1, true peak ≤ -1 dBFS for Apple Podcasts **[Apple Podcasts]**. AES TD1008 suggests -18 LUFS
  for speech-only streaming **[AES TD1008 via Production Advice]**.
- **Ads**: a podcast delivered to YouTube by RSS cannot contain ads, and sponsored segments have to be
  declared **[YT-podcast-RSS]**.

## Captions and chapters

- **Chapters are essential** for a long conversation: one per topic, from `00:00`, at least 3, each ≥ 10 s
  **[YT-chapters]**. Name them after the topic, not "Part 2".
- **Captions**: review or upload a caption file **[YT-auto-captions]**. With several people, mark speaker
  changes (a dash or the speaker's name) when it is not obvious who talks.
- **Lower thirds** with each person's name and role the first time they appear, and again after a long
  break.

## Clips for Shorts

The strongest moments become Shorts: see [`shorts-from-long-form.md`](shorts-from-long-form.md). Mark them
while editing (a marker at each candidate moment) so they do not have to be found again.

## Common mistakes

- A long intro before anything interesting happens.
- Angle changes on a timer, or cutting to every "mm-hm".
- Out-of-sync cameras: lips and words drifting late in the episode.
- Echo from all mics open at once.
- Speakers at different levels.
- Cuts that change what someone meant.
- No chapters on a one-hour video.

## Checklist for this recipe

Run it before the core [`../review-checklist.md`](../review-checklist.md).

- [ ] Sync checked at the start, middle and end of the episode.
- [ ] The cold open is a real exchange from the episode that matches the title and thumbnail.
- [ ] Whoever talks is on screen; reactions shown only when they add something.
- [ ] No echo: mics of people who are not talking are muted or gated.
- [ ] Speakers at the same level; YouTube master at -14 LUFS / -1 dBTP; a separate podcast master if needed.
- [ ] No cut changes what someone meant.
- [ ] Chapters per topic in the description; names on lower thirds.
- [ ] Candidate Short moments marked.

## Sources

- **[YT-moments]**: https://support.google.com/youtube/answer/9314415
- **[YT-chapters]**: https://support.google.com/youtube/answer/9884579
- **[YT-end-screens]**: https://support.google.com/youtube/answer/6388789
- **[YT-auto-captions]**: https://support.google.com/youtube/answer/6373554
- **[YT-podcast-RSS]**: YouTube Help, delivering podcasts to YouTube with RSS ("podcast content you upload to YouTube cannot contain advertisements"). https://support.google.com/youtube/answer/13525207
- **[Apple Podcasts]**: "Audio requirements". https://podcasters.apple.com/support/893-audio-requirements
- **[AES TD1008 via Production Advice]**: https://productionadvice.co.uk/td1008/
- **[TechSmith]**: https://www.techsmith.com/blog/how-to-edit-videos-l-cuts-and-j-cuts/
- **[StudioBinder]**: https://www.studiobinder.com/blog/what-is-room-tone/


---

## 📄 SOURCE FILE: `skills/editing-videos/recipes/shorts-from-long-form.md` (verbatim)

# Recipe: Shorts, Reels and TikToks from a long video

Turning a horizontal long video (a podcast, a talking head, a vlog, a tutorial) into vertical clips. The
editing problem is that a moment that works inside a long video often does not stand alone: it needs its own
hook, its own payoff and a frame rebuilt for a phone. Sources at the end of the file.

## Contents

- [Platform specs](#platform-specs)
- [Picking the moment](#picking-the-moment)
- [Reframing to 9:16](#reframing-to-916)
- [Pacing and cuts](#pacing-and-cuts)
- [Captions](#captions)
- [Audio](#audio)
- [Common mistakes](#common-mistakes)
- [Checklist for this recipe](#checklist-for-this-recipe)
- [Sources](#sources)

## Platform specs

| Platform | Length | Format | Source |
|---|---|---|---|
| **YouTube Shorts** | Up to **3 minutes** | Square or vertical; a wider ratio such as 16:9 is treated as a regular video | **[YT-Shorts, official]** |
| **Instagram Reels**, **TikTok** | Limits change often | 9:16, 1080×1920 is the common delivery | Check the platform's current help page before publishing; no figure verified here |

YouTube lets creators make Shorts from their own videos **[YT-Shorts]**, but a dedicated edit usually
works better than a raw excerpt.

## Picking the moment

- **A complete idea in itself**: a claim and its proof, a question and its answer, a story with an end. If
  it needs the context of the long video, it does not work.
- **Strong first line.** The first 3 s decide whether people swipe **[TikTok via blogs, creator]**. If the
  best line is in the middle, open with it and then go back to the setup, or cut the setup.
- **Let the idea set the length**, not the platform's maximum: a clip ends when its idea pays off. No
  length figure is given here because none could be sourced well.
- Mark candidates while editing the long video, so they do not have to be found again.

## Reframing to 9:16

- **Crop on the subject, shot by shot**, not one fixed center crop: the face or the action stays in the
  upper-middle of the frame.
- **Two speakers**: cut between them (one per frame) or stack them (one above the other) when the reaction
  matters.
- **Screens and wide shots** do not survive a 9:16 crop: show the relevant part enlarged, or put the
  horizontal shot in the middle with captions above and below.
- **Record in higher resolution** (4K) when you know clips will be cut, so the crop stays sharp.
- Tools: any NLE's auto-reframe, or `crop`+`scale` in ffmpeg per segment (`../references/tools.md`).

## Pacing and cuts

- **Faster than long-form**: 2–3 s per shot, 4 s max, and something new (a cut, a punch-in, text, a sound)
  every 5–7 s **[OpusClip; MrBeast analysis, creator]** (`../references/pacing-and-cuts.md`).
- **Cut every pause**; gaps of 200–300 ms **[Syllaby, creator]**.
- **Remove references to the long video** ("as I said before", "in the next part").
- **Make it loop**: an ending that leads back to the start makes rewatching natural. Do not count on an end
  screen; a verbal pointer to the full video, if any, goes in one short line.

## Captions

Most people watch these with the sound off or low, so captions are part of the edit, burned in **[creator
practice]** (`../references/graphics-and-text.md`):

- **1–5 words per caption page**, timed to the words, the active word highlighted;
- big, bold sans-serif with an outline or box; consistent style across the channel's clips;
- placed in the center or upper-center area, **above the platform's bottom UI and away from the right-side
  buttons**; check in the platform's preview, since no official safe-zone percentages were verified here;
- **reviewed word by word**: automatic transcription errors look much worse when burned in;
- every page lasts at least 20 frames **[Netflix-timing]**.

## Audio

- **Voice clear and present**; phones play through small speakers.
- **Music** under speech 18–25 dB under the voice **[Pure Audio Insight, creator]**, or leading in sections
  without speech.
- **Sound effects** carry more of the style here (whooshes, pops, risers), within the limits in
  `../references/audio-and-sfx.md`.
- **Master** to -14 LUFS, true peak ≤ -1 dBTP; platforms normalize, so louder gains nothing.
- **Licensed music only**: music from a platform's in-app library may not be cleared for use elsewhere
  (`../references/licenses.md`).

## Common mistakes

- An excerpt that starts mid-thought and needs the long video to make sense.
- A fixed center crop that cuts off the speaker or shows an empty middle between two people.
- Captions under the platform's UI, or with transcription errors.
- A slow first 3 seconds (an intro, a "so…").
- The same clip posted to every platform with another platform's watermark.
- Keeping 16:9 when the clip was meant to be a Short: YouTube treats wide ratios as regular videos
  **[YT-Shorts]**.

## Checklist for this recipe

Run it before the core [`../review-checklist.md`](../review-checklist.md).

- [ ] The clip makes sense without the long video, and ends on a payoff or a loop.
- [ ] The first 3 s carry the hook; no intro or filler.
- [ ] 9:16 (or square) at 1080×1920; the subject framed shot by shot, sharp after the crop.
- [ ] Within 3 minutes for YouTube Shorts; the current limits checked for the other platforms.
- [ ] Captions burned in, reviewed word by word, clear of the platform's UI.
- [ ] No references to the long video's other parts; no pauses left.
- [ ] Music and effects licensed for every platform the clip goes to.

## Sources

- **[YT-Shorts]**: YouTube Help, Shorts length and format ("up to three minutes", "a square or vertical aspect ratio"; "Create YouTube Shorts from your videos"). https://support.google.com/youtube/answer/15424877
- **[Netflix-timing]**: https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394
- **[OpusClip]**: https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
- **[MrBeast analysis]**: https://www.a4bcreative.com/post/the-pattern-interrupt-edit-how-to-keep-viewers-hooked-for-the-full-60-seconds
- **[TikTok via blogs]**: https://www.teleprompter.com/blog/tiktok-3-second-rule
- **[Syllaby]**: https://syllaby.io/blog/voiceover-pacing-silence-trimming-retention-editing/
- **[Pure Audio Insight]**: https://pureaudioinsight.com/blogs/content-production/perfect-youtube-audio-levels-creators-technical-guide
- **[creator practice]**: widespread practice for short-form editing, with no single source.


---

## 📄 SOURCE FILE: `skills/editing-videos/recipes/narrated-screen-tutorial.md` (verbatim)

# Recipe: narrated screen tutorial

A software tutorial where the viewer **repeats the flow with the app open next to it**. Everything here
follows from that: people don't understand that fast. This recipe is also the reference pipeline the skill
was born from, and it ships tested templates for it:

- recording with Playwright;
- a synthetic voice (ElevenLabs) generated per chapter with word alignment;
- an edit generated from data with HyperFrames, which **fails if a rule is broken**.

The craft rules (sections 1–4) apply whatever the tools. If you record with OBS or Screen Studio and cut in
Premiere or Resolve, follow them and skip the template commands. Sources at the end; `[house]` means a rule
learned reviewing real cuts of this kind of video (see "Why the house rules win").

## Contents

- [1. Hard rules for this recipe](#1-hard-rules-for-this-recipe)
- [2. Process with the reference pipeline](#2-process-with-the-reference-pipeline)
- [3. Recording](#3-recording)
- [4. Editing](#4-editing)
- [5. Hook, chapters and structure](#5-hook-chapters-and-structure)
- [6. Audio in a tutorial](#6-audio-in-a-tutorial)
- [7. Why the house rules win](#7-why-the-house-rules-win)
- [8. Checklist for this recipe](#8-checklist-for-this-recipe)
- [Sources](#sources)

Supporting files, loaded only when that step comes up:

| File | When |
|---|---|
| [`narrated-screen-tutorial/voice.md`](narrated-screen-tutorial/voice.md) | Writing the script for a synthetic voice, generating it with ElevenLabs, LUFS per chapter, verifying with whisper |
| [`narrated-screen-tutorial/hyperframes-generator.md`](narrated-screen-tutorial/hyperframes-generator.md) | Building the edit with the HyperFrames generator: the data schema, tracks, its checks, pitfalls and the review loop |
| `narrated-screen-tutorial/templates/` | `record.example.mjs`, `gen-voice.mjs`, `verify-voice.mjs`, `gen-illustrations.mjs`, `gen-video.example.mjs` + `edit-engine.mjs`, `contact-sheet.mjs`, and examples of `chapters.mjs` and `illustrations.mjs`. Copied to the video project's root (`gen-video.example.mjs` as `gen-video.mjs`, `record.example.mjs` as `record.mjs`); each one has `--help` |

## 1. Hard rules for this recipe

These come on top of the core rules in `SKILL.md`.

1. **The screen leads and the voice adapts.** The clip never goes back or repeats a second, and never
   returns to a clip it already left. Each phrase comes in when what it describes happens; if the phrase
   lasts longer than the action, the result is frozen at the right second **[house]**.
2. **Speed: 1× for navigation, clicks and results; typing at 1.5× at most.** Whatever is left over is
   removed with a clean cut, not sped up further **[house]**.
3. **Shots of ≥ 5 s**, and never a cut in the middle of an app animation (a modal opening, a loading
   state) **[house]**.
4. **A form is never visibly cut.** Waits where no pixel changes are cut; the typing itself is shown, at
   1.5× at most **[house]**. Seeing a form get typed twice, or jump half-filled, confuses more than any
   silence.
5. **Zoom only on the detail the voice names**: up to 1.10, ≥ 1.5 s to zoom in, one every two phrases,
   always within a single shot **[house]**.
6. **Fake demo data only**: a fictional company and people, a local environment, never a production
   mirror, even if the data "looks" like test data. The labels the voice names match what the screen shows
   **[house]**.
7. **≥ 0.4 s between phrases**; a warning at 3 s without voice and a hard cap at 6 s, unless the screen
   shows a self-explanatory action **[house]**.
8. **Synthetic voice:** acronyms and numbers written as they are pronounced, verified with whisper; never
   re-encoded; keys and the voice id only in the `.env`. Detail in `voice.md`.
9. **Chapter cards**: each chapter opens with a 3 s title card ("Step 2 of 5"); hard cuts inside a
   chapter **[house]**.

## 2. Process with the reference pipeline

| # | Step | What happens | Where |
|---|---|---|---|
| 1 | **Brief** | Audience, destination, length, chapters, voice, music or not, brand skin. With HyperFrames, go through the `hyperframes` skill: it writes `BRIEF.md`, and a narrated tutorial goes to `general-video` | `hyperframes-generator.md` § 1 |
| 2 | **Script** | By chapter, with what is on screen in brackets. Demo data, no stock phrases, acronyms and numbers written as pronounced in the `vo` field. Hook: the result first | `voice.md`, § 5 here |
| 3 | **Recording** | `record.mjs` (Playwright) on the demo company: 1920×1080, one clip per block, marks by text, H.264 `.mp4`. On Windows, with `node` | § 3 here |
| 4 | **Voice** | `gen-voice.mjs`: one take per chapter with alignment, LUFS per chapter, verified anchors; then whisper and `verify-voice.mjs` | `voice.md` |
| 5 | **Edit** | `gen-video.mjs` (from `gen-video.example.mjs` + `edit-engine.mjs`) generates the compositions from the script, the marks and the alignment, and fails if a rule is broken. Graphics for concepts, illustrations with `gen-illustrations.mjs`, sound effects from [`library/`](../library/) | `hyperframes-generator.md` |
| 6 | **Review** | The generator's checks, `npx hyperframes check`, snapshots every 0.5 s on graphics, `contact-sheet.mjs`, listen with headphones; then the core checklist | § 8 here, [`../review-checklist.md`](../review-checklist.md) |
| 7 | **Render** | Only with approval. `draft` → `looks` → `delivery`, with `--video-frame-format png`. Master to -14 LUFS / -1 dBTP | `hyperframes-generator.md` § 5 |
| 8 | **Publishing** | Title with the search query first, thumbnail that shows the result, chapters from `data/timeline.json`, a linked written guide | [`../references/thumbnail-title-description.md`](../references/thumbnail-title-description.md) |

## 3. Recording

1. **Demo data, never real data** (rule 6).
2. **1920×1080 full-bleed** and text legible on a phone. Record with the browser or app zoom at 125–150 %
   when the UI is dense **[Envision; legibility.info]**. If something looks small in the recording, it cannot
   be read on a phone: fix it before recording, not with zoom in the edit.
3. **Playwright with marks**, with `templates/record.example.mjs` copied into the project.
   - Set `viewport` and `recordVideo.size` to 1920×1080. Without that, Playwright records at 800×450 and
     rescales without warning.
   - Each action writes a `12.34s opens Banking` line to `<clip>.marks.txt`, measured from when the page is
     created, which is when the video starts.
   - The generator finds marks by text, not by second. When a clip is re-recorded with the same file name,
     the edit readjusts itself, and fails saying which mark is gone **[house]**.
   - Playwright records `.webm` at a low bitrate. The template converts it to H.264 `.mp4` (CRF 14, 15-frame
     GOP): it looks sharper when zoomed and the preview seeks well.
4. **On Windows, Chromium and Playwright are run with `node`, not with `bun`** **[house: pitfall already
   hit]**.
5. **Cursor with a purpose.** Move it only to go to the next click and keep it still while the voice
   explains. If the cursor looks small at 1080p, enlarge it (≥ 20 px visible) **[Envision]**.
6. **Real typing, at human speed.** Record with a per-key `delay`; in the edit it can go up to 1.5× at most.
7. **One clip per action block**, not one clip per video. Re-recording a step does not force re-recording
   everything.

## 4. Editing

1. **The screen leads.** Voice per phrase, placed when what it describes happens. If the action lasts
   longer than the phrase, the screen plays on its own; if the phrase lasts longer, the result is frozen.
   This is temporal contiguity: word and image together, not one after the other **[Mayer, study]**.
2. **Freeze instead of repeating.** The frozen frame is taken from the exact second the clip is at.
   **Pitfall already hit:** a freeze taken from before the modal finished opening makes the modal seem to
   open and close.
3. **Remove dead time** (loading, waiting, searching for a button) with clean cuts, not speed-ups. Screen
   Studio and similar tools speed typing up 2–5× **[Screen Studio, creator]**; it was tried on a real cut and
   could not be followed **[house]**.
4. **Guide the eye with framing, not arrows.** The recording's cursor already marks the click. Screencast
   tools suggest zooms of 1.5×–4× entering in 100–500 ms **[Envision, creator]**; that makes viewers who
   follow on another screen dizzy, so this recipe uses 1.10 (rule 5).
5. **On-screen text only for what is typed or searched for**: an expanded acronym, a menu path, a key. Do
   not duplicate in text what the voice says (redundancy principle) **[Mayer, study]**.
6. **Graphics and illustrations for what the screen does not show** (how a journal entry is built, what a
   contribution is), then the data in the app: the graphic explains, the screen proves the app does it
   **[house; Mayer: multimedia principle]**. Context illustrations with `gen-illustrations.mjs`, always
   without text inside the image.
7. **J and L cuts** are rarely used: the voice should name what is already on screen. Where they help is on
   the way out of a chapter card, with a 0.6 s breath before the first phrase **[house]**.
8. **Nothing decorative.** Animation, music or b-roll that explains nothing distracts (coherence principle)
   **[Mayer, study]**.

## 5. Hook, chapters and structure

- **Hook of 10–20 s** that shows the end state first (the closed report, the confirmed month) and says what
  will be achieved with which data **[house]**. No logo intro: the logo goes on a card over the result.
- **Chapters**: a 3 s title card per chapter, its content entering in 0.55 s, plus an **edge badge** with
  the step's name for viewers who land mid-video. In tutorials people rewatch and jump to the part they
  need, and large text at transitions helps **[Guo 2014, study]**.
- **Blocks under 6 min**; people watch 2–3 min of each video on average whatever its length **[Guo 2014,
  study]**. For a long process, NN/g recommends one video per step **[NN/g]**.
- **A written guide** with the same content and the video embedded, for people who cannot have sound on
  **[NN/g]**.

## 6. Audio in a tutorial

- **No music by default**: the viewer is listening to instructions, and music that adds nothing hurts
  learning **[house; Mayer: coherence]**. Music, if any, in the intro, the title cards and the closing.
- **No sound effect on the real recording's clicks**, and no whoosh on cuts within a chapter: those cuts are
  continuity, not transitions **[house]**.
- Sound effects on title cards, graphics and rows: see the table in
  [`../references/audio-and-sfx.md`](../references/audio-and-sfx.md), with files from
  [`../library/`](../library/).

## 7. Why the house rules win

Creator figures (2–3 s per shot, an interrupt every 5–7 s) come from entertainment and talking-head videos.
In a software tutorial the bottleneck is that the viewer **follows the action and repeats it**.

The first cut of the reference tutorial tied the screen to the voice: 45 shots in 5 minutes, with spans at
×3 and ×10, and it could not be followed. The rules above come from that review (4-Oct-2026). When an
external figure clashes with them, the house rule wins in this recipe, and that is stated.

## 8. Checklist for this recipe

Run it before the core [`review-checklist.md`](../review-checklist.md). With the reference pipeline, the
first block is automatic; with other tools, check the same things by hand.

**Automatic**

- [ ] `node gen-voice.mjs` with nothing pending: every anchor matches, none repeated; no chapter more than
  4 dB from the median.
- [ ] `node verify-voice.mjs NN tmp/trans-NN/transcript.json` read span by span for every new or regenerated
  chapter: no acronym read as a word, no number said differently, no swallowed word. It exits 1 on any
  difference and spelled-out acronyms always differ, so it is read, not used as a gate.
- [ ] `node gen-video.mjs` finishes with no broken rules: no going back or return to a clip; shots ≥ 5 s
  (except `short`); no span above ×1.5; ≥ 0.4 s between phrases and no silence > 6 s without
  `silenceJustified`; graphics anchored (≤ 0.5 s before, content within 1 s, each element ≤ 0.6 s from its
  word); zooms ≤ 1.10, ≥ 1.5 s in, one every two phrases, never across a cut; each freeze ± 0.1 s from the
  clip's second.
- [ ] `npx hyperframes check` with no errors (first pass with `--snapshots`).
- [ ] Script free of the blocklist phrases in `voice.md`.

**In `data/timeline.json`**

- [ ] `frozen` per shot: above ~6 s, the voice says more than the screen shows. Add a graphic, split the
  phrase or re-record.
- [ ] Chapter length: blocks under 6 min if possible.

**By eye, with snapshots** (how to take them: `hyperframes-generator.md` § 5)

- [ ] Freezes show the finished result, with no visible jump from the last moving frame.
- [ ] Title cards inside title-safe; the edge badge visible over product footage, hidden under graphics.
- [ ] The zoom lands on the detail the voice names, and UI text stays sharp at 1.10.
- [ ] Every name, ID and amount belongs to the demo company; buttons the voice names say the same on screen.
- [ ] No form is seen jumping half-filled.

**Listen**

- [ ] The voice does not get louder or quieter between chapters; acronyms sound spelled out.
- [ ] No click from the real recording has a sound effect on top.

## Sources

- **[house]**: rules from the reference tutorial, reviewed on 4-Oct-2026.
- **[Mayer]**: Mayer (2008), "Applying the science of learning", *American Psychologist* 63(8): multimedia, coherence, signaling, redundancy, temporal contiguity and segmenting principles. https://doi.org/10.1037/0003-066X.63.8.760
- **[Guo 2014]**: Guo, Kim & Rubin, "How video production affects student engagement", L@S 2014. https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf
- **[NN/g]**: "Instructional video guidelines". https://www.nngroup.com/articles/instructional-video-guidelines/
- **[Envision]**: "Best practices for screencast". https://www.envision.everspringpartners.com/build/best-practices-for-screencast
- **[legibility.info]**: https://legibility.info/rules-for-text-in-videos
- **[Screen Studio]**: "Speed up typing segments". https://screen.studio/guide/speed-up-typing-segments


---

## 📄 SOURCE FILE: `skills/editing-videos/recipes/narrated-screen-tutorial/voice.md` (verbatim)

# Narrated screen tutorial: synthetic voice and script

Part of the [narrated screen tutorial recipe](../narrated-screen-tutorial.md). How to write what is said and
how to get it out of ElevenLabs so it sounds natural and lines up with the screen. HyperFrames' general narration mechanics are in `hyperframes-creative/references/narration.md`.
This file covers what is specific to tutorials narrated in Chilean Spanish, so the voice examples below are
in Spanish.

## Contents

- [Writing the script](#writing-the-script)
- [Writing for synthesis](#writing-for-synthesis)
- [Generating with ElevenLabs](#generating-with-elevenlabs)
- [Measuring loudness per span (LUFS)](#measuring-loudness-per-span-lufs)
- [Verifying with whisper](#verifying-with-whisper)
- [Sources](#sources)

## Writing the script

1. **Speak like someone showing their screen, with the demo data.** "This bakery has eight employees", not
   "easily manage your team".
2. **No stock phrases or canned copy**: they sound like advertising and nobody believes them. Blocklist
   (extendable), searched for in the script before generating the voice:
   - «de principio a fin» (from start to finish), «en pocos clics» (in just a few clicks), «así de fácil»
     (it's that easy), «listo:» (done:);
   - «olvídate de» (forget about), «nunca fue tan fácil» (it's never been so easy), «te mostramos cómo»
     (we'll show you how);
   - «en este video vamos a ver» (in this video we'll see), «sin más preámbulo» (without further ado),
     «potencia» (power up), «revoluciona» (revolutionize).
   Running the text through the `humanizer` skill helps find others.
3. **Each phrase names what is seen at that moment.** If the phrase talks about something the screen does
   not show, a shot or a graphic is missing.
4. **Simple Chilean Spanish, not Argentine.** «Puedes», «tienes», not «podés». Compliance verbs with a
   person: the app calculates and suggests; the person using it reviews and confirms.
5. **Pace: 120–150 words per minute (2–2.5 per second) for technical content** **[speaking rate,
   creator]**.
   - HyperFrames takes 2.5 words per second as a natural pace and asks for pauses **[hyperframes-creative]**.
   - In recorded lectures, speaking fast and with enthusiasm retained more **[Guo 2014, study]**. In a
     tutorial, the screen's pace leads: the voice waits for the action, it does not rush it.
6. **One take per chapter, not per phrase.** Read in pieces, each break lands like a full stop and it sounds
   like a list. In a single take the voice flows and respects the commas **[house]**. Afterwards it is cut
   per phrase using the alignment.

## Writing for synthesis

ElevenLabs reads acronyms as words and numbers in its own way. In the `vo` field (what is read aloud) they
are written as they are pronounced; on screen they keep their normal spelling **[house]**.

| On screen | In `vo` | Why |
|---|---|---|
| SII | «ese i i» | it reads it as a word |
| ACHS | «a ce hache ese» | same |
| AFP | «a efe pe» | same |
| LRE | «ele erre e» | same |
| UF | «u efe» | it read it as «uff» |
| CSV, PDF | «ce ese uve», «pe de efe» | same |
| Previred | «Previ Red» | splits the syllables properly |
| RUT | «rut» | said as a word |
| 1,70 % | «uno coma setenta por ciento» | numbers are written out in words |
| art. 50 | «artículo cincuenta» | same |

The `vo` column is the Spanish spelling of each letter or number as a Spanish narrator would say it. Every
new acronym is tested and added to this table.

## Generating with ElevenLabs

Template: `templates/gen-voice.mjs`, copied to the project root, plus a `chapters.mjs` in the format of
`templates/chapters.example.mjs`. Run it from the root: `node gen-voice.mjs --help`.

- **Configuration by reference to the `.env`, without copying keys.** The scripts read the `.env` from
  `--env`, otherwise the one in `VIDEO_ENV_FILE`, otherwise the project's `./.env`. They do not search
  upwards, so they never pick up another app's file.
  - Variables: `ELEVENLABS_KEY` and the `voice_id` (in `ELEVENLABS_VOICE_ID`, or another name with
    `--voice-var`). Optional: `ELEVENLABS_MODEL_ID` (defaults to `eleven_multilingual_v2`),
    `VOICE_STABILITY`, `VOICE_SIMILARITY` and `VOICE_STYLE`.
  - Example, with the `.env` in another folder and the voice stored as `MY_VOICE_ID`:

    ```bash
    node gen-voice.mjs --env ../.env --voice-var MY_VOICE_ID
    node gen-illustrations.mjs --env ../.env
    ```
- **The voice is not resolved by name.**
  - A key scoped only to text-to-speech gets a 401 from `GET /v1/voices`.
  - Code that "resolves the name" falls back to the default voice, which is English and sounds like an
    American reading Spanish.
- **Settings for informative narration:** stability 0.55, similarity 0.8, style 0.05. With a high style the
  voice "acts" and figures come out with odd emphasis **[house]**.
- **Alignment:** request `/with-timestamps` and store the alignment of the **original** text (`alignment`,
  not `normalized_alignment`). The indices have to match the script, which is where anchors are searched.
- **Anchors:** each phrase and each visual element is anchored to a piece of text that appears **only once**
  in the chapter. `gen-voice.mjs` fails if an anchor is missing or repeated.
- **Regenerate per chapter only:** `node gen-voice.mjs 03 --redo`. Everything is not regenerated because
  one phrase changed.

## Measuring loudness per span (LUFS)

Each chapter is a separate call and comes out at its own level. Chained together, the voice sounds like it
rises and falls **[house]**. So:

1. `gen-voice.mjs` measures each chapter with `loudnorm` (integrated LUFS, ITU-R BS.1770) and writes
   `volumes.json`.
2. The reference is **the quietest chapter**: every gain ends up ≤ 1. It only attenuates, because
   amplifying raises the synthesis hiss and `data-volume` > 1 can clip.
3. **The mp3 is not re-encoded.** Re-encoding adds a few milliseconds of padding at the start and shifts the
   whole alignment. The correction is applied with `data-volume` on each `<audio>`.
4. If a chapter ends up **more than 4 dB from the median**, that chapter is regenerated. It is not allowed
   to drag the others along.
5. The video's final level (-14 LUFS for YouTube) is set **once, on the render** (see [`audio-and-sfx.md`](../../references/audio-and-sfx.md)).

## Verifying with whisper

Before editing, transcribe each chapter and compare it with the script:

```bash
npx hyperframes transcribe assets/voice/ch03.mp3 --engine whisper --model small --language es -d tmp/trans-03
node verify-voice.mjs 03 tmp/trans-03/transcript.json
```

- `transcribe` always writes `<dir>/transcript.json`: one `-d` per chapter, or the next one overwrites the
  previous one.
- `--engine whisper` pins the engine: with `auto`, if Parakeet is installed that one is used and `--model` is
  ignored.
- **Never use a `.en` model** (`small.en` is the CLI default): it silently translates Spanish into English
  **[media-use/transcribe]**.
- `verify-voice.mjs` lists the spans where what is heard differs from the script.
- Spelled-out acronyms will show up as differences (whisper writes «SII»): listen to those and confirm they
  do not sound like a word.
- What is an error: an acronym read as a word, a number said differently, a swallowed word.

## Sources

- **[house]**: corrections to the first cut of the reference tutorial (4-Oct-2026).
- **[hyperframes-creative]**: `~/.claude/skills/hyperframes-creative/references/narration.md`.
- **[media-use/transcribe]**: `~/.claude/skills/media-use/audio/references/transcribe.md`.
- **[Guo 2014]**: https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf
- **[speaking rate]**: https://thevoiceoverguy.com.au/words-to-minutes and https://goteleprompter.com/blog/words-per-minute-speaking-rate-guide/
- ElevenLabs, "Create speech with timing". https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps


---

## 📄 SOURCE FILE: `skills/editing-videos/recipes/narrated-screen-tutorial/hyperframes-generator.md` (verbatim)

# Narrated screen tutorial: the HyperFrames generator

Part of the [narrated screen tutorial recipe](../narrated-screen-tutorial.md). HyperFrames is one way to
build this kind of video, the one the templates here are tested with; the general map of HyperFrames skills,
and how the same rules look in an NLE, ffmpeg or Remotion, is in
[`../../references/tools.md`](../../references/tools.md).

The recipe decides **what** gets done and with which numbers; the HyperFrames skills decide **how** it is
written in their contract. HyperFrames wins on mechanics (attributes, determinism, CLI), the recipe on
editorial matters (pacing, speed, when to use a graphic). Say so in the delivery.

## Contents

- [1. Which HyperFrames skill to use at each step](#1-which-hyperframes-skill-to-use-at-each-step)
- [2. How each editorial rule is written in the contract](#2-how-each-editorial-rule-is-written-in-the-contract)
- [3. The generator pattern](#3-the-generator-pattern)
- [4. Pitfalls already hit](#4-pitfalls-already-hit)
- [5. Review loop with `npx hyperframes`](#5-review-loop-with-npx-hyperframes)
- [Sources](#sources)

## 1. Which HyperFrames skill to use at each step

Load order in a new or resumed project:

| Step | Skill | What for |
|---|---|---|
| 0. Entry | `hyperframes` | Always first. Runs `npx hyperframes usage --json`. Reads the project state. If there is a `BRIEF.md`, runs its `workflow`; if not, runs the interview and writes the brief. A long narrated tutorial falls under `general-video` |
| 0b. Install the workflow | `npx hyperframes skills update general-video` | Before reading the workflow. If it fails, show the error; do not continue from memory |
| 0c. Project | `npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=general-video` | Creates the folder, `hyperframes.json` and `package.json` with the pinned version. Add `"media": { "autoProxy": true }` |
| 1. Workflow | `general-video` | Owns the deliverable end to end: plan, storyboard, build, review |
| 2. Contract | `hyperframes-core` | **Before writing HTML**: `data-start`, `data-duration`, `data-media-start`, tracks, sub-compositions, determinism. Copyable recipes in `references/creator-editing-recipes.md` |
| 3. Direction | `hyperframes-creative` | `frame.md` / `design.md` (brand skin), narration, beat plan |
| 4. Media | `media-use` | Resolve BGM, SFX, images and icons; transcribe. TTS only if the brief does not set a brand voice |
| 5. Motion | `hyperframes-animation` | Animation rules, blueprints, transitions; `scripts/animation-map.mjs` to review the choreography |
| 5b. Camera | `hyperframes-keyframes` | Zoom, punch-in, reframing: always on an inner wrapper |
| 6. Blocks | `hyperframes-registry` | **Before hand-drawing** anything with a name (chart, terminal window, transition): `npx hyperframes catalog --query "<in English>" --json` |
| 7. Mix | `hyperframes-audio` | Fades, carving the music against the voice (`scripts/carve.mjs`), automation, buses |
| 8. Review and render | `hyperframes-cli` | `lint`, `check`, `snapshot`, `preview`, `render` |
| 9. Adjustments with the person | `hyperframes-studio` | Questions or notes on a cut that is already built (§ 0); track order and safe zones |

For requests that cross domains, the "Creator request" table in `hyperframes/SKILL.md` § 5 says what to load
together. Examples:

- a cut: `general-video` + `core`;
- a zoom: `+ keyframes`;
- a fade or ducking: `+ audio`.

### What `general-video` asks for and what covers it here

In a tutorial, the generator replaces the step of building scene by scene with subagents (the "frame
workers"). The artifacts the workflow expects are produced like this:

| `general-video` expects | In a tutorial with the generator |
|---|---|
| `STORYBOARD.md` with a `## Frame N` block per scene (`status`, `src:`, blueprint or rules citation, beat), even with `storyboard: no` | One block per chapter, with `src: compositions/chNN.html`. The rules citation points to `../narrated-screen-tutorial.md` and, for title cards and graphics, to the `hyperframes-animation` rules they use. The beat is the summary from `SCRIPT.md` |
| Per-scene packages and subagents that write `compositions/<frame>.html` | The generator writes every composition. No workers are dispatched |
| `compositions/<frame>.motion.json` | The generator writes one per chapter with graphics: `appearsBy` per row and `before` between rows. `check` verifies them |
| `audio_meta.json` from the `media-use` audio engine | Replaced by `gen-voice.mjs` (brand voice with alignment) and the library's `catalog.json`. If BGM or SFX from `media-use resolve` are used, that record still applies |
| Review with `animation-map.mjs` | Runs the same way on the generated compositions |
| Storyboard gates, final preview and render approval | Same. The generator does not skip them |

## 2. How each editorial rule is written in the contract

| Editorial rule | In HyperFrames |
|---|---|
| **Cutting and trimming a clip** | One `<video>` piece per span, with `data-start` (composition time), `data-duration` and `data-media-start` (second in the file). A forward jump in the clip is another piece. Recipes "Hard cut", "Trim in/out" and "Split / splice" |
| **Times inside a chapter** | Each chapter is a sub-composition, and its `data-start` values are local to it. Mark every `<video>`, `<img>` and `<audio>` with `data-hf-media-start-basis="local"`: without it, `lint` warns `nested_media_start_basis_ambiguous` |
| **No going back** | Inside a chapter, the `data-media-start` of each piece of a clip is ≥ the end of the previous one, and the edit never returns to a clip it already left. The generator checks this, not the CLI |
| **Speed** | Constant `data-playback-rate` per piece: `1` for navigation, clicks and results; **≤ 1.5** only for typing. Never a `rate` lane to rush a wait: the wait is cut. `source consumed = data-duration × rate` |
| **Freezing the result** | An `<img class="clip">` with the frame extracted **as PNG** at the exact second the clip is at (recipe "Freeze / hold"; a freeze in the middle of the file is preprocessed). As PNG, so that no compression jump between the video and the still frame is noticeable |
| **Voice per phrase over a single mp3** | One `<audio>` per phrase, all with the **same `src`**: `data-media-start` = start of the phrase in the mp3, `data-duration` = its length, `data-start` = when what it describes happens, `data-volume` = the chapter's gain, `data-audio-group="voice"`. No re-encoding. Every `<audio>` has an `id`: without an `id` the mixer ignores it and the render comes out silent |
| **Slow zoom on the detail** | Animate the **shot's wrapper** (`<div class="cam" id="p07">`, which wraps its pieces), **never the `.clip`** and **never the class** (`.cam` would zoom every shot). The wrapper has no `data-start`: `lint` rejects a video inside a timed element (`video_nested_in_timed_element`). `tl.set("#p07", {transformOrigin:"62% 40%"}, t)`, `tl.fromTo("#p07", {scale:1}, {scale:1.10, duration:1.6, ease:"sine.inOut", immediateRender:false}, t)`, and back to 1 in 0.9 s |
| **Title cards and graphics entering** | Tweens on inner elements of the `.clip` section (`fromTo` on `y` and `opacity`). The framework handles the `.clip`'s visibility, not a tween |
| **Fade or dissolve** | Two clips on different tracks that overlap, with opposite `opacity` envelopes on their wrappers and `volume` envelopes in `data-automation` (recipe "Crossfade"). Rarely used in a tutorial: hard cut within a step |
| **Level of each track** | `data-volume` = the track's fixed level. For changes over time, a `volume` lane in `data-automation`. **Never** a lane and a volume tween on the same track |
| **Music under the voice** | **Carve with the script**, not by writing attributes: `node <hyperframes-audio>/scripts/carve.mjs --comp compositions/chNN.html --bed <bed id>`. The `data-fx-carve` attribute only stores the configuration; what you hear is the `data-fx-chain` and the lanes the script writes. Requirements: `ffmpeg` and `npm i -D @hyperframes/core` in the project. The bed and the phrases have to be **in the same file**, because the script analyzes one. Always pass `--bed` with the bed's id: without it the script guesses the bed from ids and file names, and a guess can pick the wrong track. Do not adjust the bed's `data-volume` by hand afterwards: the carve writes its own gain. Confirm with `check` |
| **Sound effects** | With `media-use resolve --type sfx`, or copied from [`library/`](../../library/) to the project's `assets/sfx/`. Each one is an `<audio>` with an `id`, `data-start` on the event (2–4 frames before), a computed `data-volume` ([`audio-and-sfx.md`](../../references/audio-and-sfx.md)) and `data-audio-group="sfx"`, never in the voice group |
| **Safe zones** | Content within 90 % (action-safe) and text within 80 % (title-safe), the margins from `hyperframes-studio` § 4 |

### Levels in the project

- **Voice:** each phrase's `<audio>` takes its `data-volume` from `volumes.json`, never > 1 (see
  [`voice.md`](voice.md)). With those gains the whole voice sits at the level of the quietest chapter,
  recorded as `voice_lufs`; it usually lands between -18 and -14.
- **Sound effects and music:** `data-volume` is the gain formula in
  [`audio-and-sfx.md`](../../references/audio-and-sfx.md), computed from `voice_lufs`;
  `node library/search.mjs <term> --voice <voice_lufs>` prints it. `media-use` defaults to `volume: 0.35`
  for SFX and 0.12 for BGM **[media-use]**.
- **With carve**, leave the bed's `data-volume` at 1: the carve writes its own gain. Each voice phrase has
  `data-audio-group="voice"`, and that group carries no music or effects. Classic ducking (a `volume` lane)
  does not replace the carve, and a track has a volume lane or a volume tween, never both.

### Tracks (`data-track-index`)

One element type per track, so the timeline reads well in Studio (`hyperframes-studio`):

| Track | What goes there |
|---|---|
| 1 | product video pieces |
| 2 | freeze frames |
| 3 | graphics |
| 4 | chapter title cards |
| 5 | edge badge |
| 6 | labels |
| 10–19 | sound effects |
| 20 + n | voice for chapter n (one track per chapter; otherwise `lint` thinks the voices of two chapters overlap) |
| 40 | music |

## 3. The generator pattern

A tutorial several minutes long is not written by hand: the HTML is **generated** from data, so a clip can
be re-recorded or a phrase regenerated without redoing the edit.

```
chapters.mjs (script: what is read, with anchors)
   └─ gen-voice.mjs ───→ assets/voice/chNN.mp3 + chNN.json (alignment) + volumes.json + durations.json
record.mjs (Playwright)
   └─────────────────→ assets/clips/NN-*.webm → NN-*.mp4 (H.264) + NN-*.marks.txt
gen-video.mjs + edit-engine.mjs
   └─────────────────→ compositions/chNN.html + chNN.motion.json + index.html + data/timeline.json
                        (fails and writes nothing if a rule is broken)
```

**Templates** (copied to the project root):

- `templates/gen-video.example.mjs`: a complete, tested generator, with clean `lint` and `check` on
  synthetic data. Only the "what is specific to this video" section changes: `STEPS`, `EDIT`, `ZOOMS`,
  `GRAPHICS`.
- `templates/edit-engine.mjs`: the engine. `build()` places screen and voice on the chapter's clock,
  `review()` applies the rules, plus `markReader`, `splitPhrases`, `wordTime`, `freezeFrame` and
  `phraseHtml`. The input and output schema is documented in each function's comment.
- `templates/record.example.mjs`: Playwright at 1920×1080, with the marks measured from page creation and
  the conversion to H.264 with a short GOP.

**How a chapter is described** (`EDIT`):

```js
"01": [
  { clip: "01", spans: [t1(m("01", "opens Banking"), m("01", "picker open"))],
    phrases: [["In Banking", m("01", "opens Banking")]] },
  { clip: "01", spans: [t1(m("01", "file chosen"), m("01", "table loaded"), 1.5)],
    phrases: [["The file your bank exports", m("01", "file chosen")]] },
  { graphic: "transaction", phrases: ["Once you upload it"] },
],
```

- `m(clip, text)`: the second of the clip's mark that contains that text. Fails if it matches zero lines or
  more than one.
- `t1(from, to, speed)`: a contiguous span of the clip. Several spans in one segment have to be
  contiguous; a forward jump is another segment (a cut).
- A phrase with a second comes in when the clip reaches that point. If the previous one is still playing,
  the clip freezes until it ends. A phrase without a second follows the previous one.
- `short: true` allows a shot shorter than 5 s; `waitForVoice: false` lets the phrase keep playing over the
  next shot.
- A graphic declares its rows with each one's anchor. The generator works out when each row enters, passes
  it to `review()` and writes the `.motion.json`.

**What `review()` receives**: `[{ ch, shots, phrases, zooms }]`.

- Clip shots: `{ id, type: "clip", clip, source: [from, to], start, end, short, speeds,
  freezes: [{ second, expected }] }`. That is what `build()` returns, plus the `id`.
- Graphics: `{ id, type: "graphic", start, end, wordAt, entries: [{ what, at, wordTime }] }`.
- Zooms: `{ scale, inDur, start, end, shot }`.
- Phrases: the ones from `build()`; `silenceJustified: true` lets a long gap before that phrase through.

**Checks** (if any fails, it exits with an error and writes nothing):

| Check | Default threshold (`RULES`) |
|---|---|
| No going back or returning to an earlier clip | 0 s repeated |
| Minimum shot | 5 s (except `short`) |
| Maximum speed of a span | ×1.5 |
| Gap between phrases | ≥ 0.4 s |
| Silence without voice | warning > 3 s; fails > 6 s unless `silenceJustified` |
| Graphic before its word | ≤ 0.5 s (and not later than 0.6 s) |
| Graphic without content | ≤ 1 s |
| Element anchored to its word | ≤ 0.6 s away |
| Zoom | ≤ 1.10, ≥ 1.5 s to zoom in, at least two phrases since the previous zoom, fits entirely in its shot |
| Freeze from the right second | ≤ 0.1 s off the clip's second |
| Unique anchor, present and in order | `gen-voice.mjs` before paying for synthesis, and `splitPhrases` |

`data/timeline.json` stores the global times of each chapter (with its `timestamp` for the description), of
each phrase and of each shot. Also the `frozen` time of each shot and the `firstContent` of each graphic:
those are the seconds to look at in the review.

## 4. Pitfalls already hit

- **Freeze from the wrong second.** If the still frame comes from before an animation finishes (a modal
  opening), the modal seems to open and close. `freezeFrame` extracts at `t - 0.04 s` from the second the
  clip is at, and near the end of the file it uses `-sseof`. `review()` compares the second.
- **Windows: Chromium and Playwright are run with `node`, not with `bun`.** The `playwright` version has to
  match the Chromium installed in the `ms-playwright` folder of Playwright's cache. If not,
  `npx playwright install chromium`.
- **Playwright clips (`.webm` VP8/VP9).** They are not edited directly: `autoProxy` only makes a copy if
  Chrome says it cannot play the format, and with VP9 it usually says it can; the preview stutters when
  seeking. `record.mjs` leaves an H.264 `.mp4` with a 15-frame GOP, and the edit uses that one. Render with
  `--video-frame-format png`, as the CLI recommends for screen recordings.
- **The voice is regenerated only per chapter** (`node gen-voice.mjs 05 --redo`) and measured in LUFS. The
  mp3 is never re-encoded: it shifts the alignment.
- **The `loudnorm` report goes to stderr.** Reading stdout gives nothing, and the measurement is lost without
  an error.
- **An anchor repeated within the chapter** makes the visual come in at the wrong occurrence. Anchors have
  to be unique; if not, make them longer.
- **An `<audio>` without an `id`** is not picked up by the mixer: the render comes out silent. `lint` flags
  it as `media_missing_id`.
- **An even `stagger` on a graphic's rows** brings in rows the voice has not named yet. Each row is anchored
  to its word.
- **The edge badge gets covered by the video** if it does not have a `z-index` above the shots: `check`
  flags it as `text_occluded`.

## 5. Review loop with `npx hyperframes`

Use the version pinned in the project's `package.json`, and check once whether it is out of date
(`hyperframes/SKILL.md`, "Keep the project's CLI current").

1. `node gen-video.mjs`: it has to finish with no broken rules.
2. `npx hyperframes lint` while iterating.
3. `npx hyperframes check` as the final gate. **Do not chain `lint` before it**: `check` includes it. On the
   first full pass, add `--snapshots`.
4. **Snapshots every 0.5 s on each graphic**, with the times from `data/timeline.json`:

   ```bash
   npx hyperframes snapshot --at 258.0,258.5,259.0,259.5,260.0 --no-end --describe false -o tmp/snap-p13
   ```

   - `--no-end` keeps it from adding the final frame.
   - `--describe false` keeps it from calling Gemini, which costs money and runs by default if
     `GEMINI_API_KEY` is in the environment.
   - `-o` takes the images out of the project: `snapshots/` mixes old runs with the ones from `check`.
5. **Contact sheet** per group: `node contact-sheet.mjs tmp/snap-p13` writes `sheet-1.jpg`, `sheet-2.jpg`… (12 frames each, read by rows). Look at the sheets, not 20 loose images. One image per group and per phase, not one per frame:
   every attached image makes the context more expensive **[hyperframes/production-loop]**.
6. `npx hyperframes preview --background`: give the URL to the person and ask whether they will review it or
   it should be rendered.
7. **Render only with approval**, and with `--video-frame-format png`:
   - `--quality draft` while iterating;
   - `looks` for the first real render;
   - `delivery` for the final delivery.
   Then, the loudness master on the file ([`audio-and-sfx.md`](../../references/audio-and-sfx.md)), and `ffprobe` to confirm that the duration
   matches the root `data-duration`.

## Sources

- `~/.claude/skills/hyperframes/SKILL.md` (§ 1 state, § 2 routes, § 5 skills by need) and `references/production-loop.md`.
- `~/.claude/skills/general-video/SKILL.md` (plan, `STORYBOARD.md`, workers, `.motion.json`).
- `~/.claude/skills/hyperframes-core/references/creator-editing-recipes.md` and `variables-and-media.md`.
- `~/.claude/skills/hyperframes-audio/SKILL.md` ("Voiceover carve", "One bus for many tracks").
- `~/.claude/skills/hyperframes-cli/SKILL.md` and `references/lint-validate-inspect.md`; `npx hyperframes snapshot --help` and `render --help` (0.8.123).
- `~/.claude/skills/hyperframes-studio/SKILL.md` § 4.
- **[media-use]**: `~/.claude/skills/media-use/audio/references/{sfx,bgm}.md`.


---

## 📄 SOURCE FILE: `skills/editing-videos/memes/README.md` (verbatim)

# Meme reference catalog

`catalog.json` lists 59 well-known memes and video-editing meme formats that work in tutorials and
explainers. For each one it says what it means, when it fits, how long it stays on screen, how to make an
original version, where it came from, who likely owns it, and how likely it is to trigger Content ID.

**This folder ships no meme media**: no images, no GIFs, no clips, no sounds. That is deliberate.

```bash
node search.mjs                     # formats and risk levels, with counts
node search.mjs fail                # search by name, meaning or use
node search.mjs --format sound      # only sounds
node search.mjs --risk low --json   # full entries, filtered by Content ID risk
```

## Why the media isn't here

Almost every meme is a piece of someone else's work: a TV still, a film frame, a stock photo, a webcomic,
another creator's video, a song. Being famous doesn't make it free. Two problems follow:

- **Redistributing it in a public repository** means copying and sharing work we don't own or license.
  A repo is not a meme page.
- **Putting it in a monetized YouTube video** can trigger a Content ID claim (the owner takes the ad
  revenue, or blocks the video in some countries), a manual claim, or a takedown. A takedown is a copyright
  strike, and three active strikes get a channel terminated.

Content ID compares uploads against reference files that rights holders submit. In practice it matches
audio and video, so songs, sound effects from shows or games, and clips carry the highest risk. A still
image is unlikely to be matched automatically, but its owner can still file a manual claim. That is what the
`content_id_risk` field measures: the chance of an automated match **if you use the original media**. It is
not a legal opinion, and `low` does not mean "allowed".

## Fair use is not a safe harbor

- **Fair use is a US doctrine** (17 U.S.C. section 107). A court weighs four factors case by case: the
  purpose of the use (commentary, criticism, parody and transformation weigh in favor; commercial use weighs
  against), the nature of the work, how much of it you use, and the effect on its market. Nobody can tell
  you in advance that a use is fair.
- **Other countries use different and usually narrower rules.** Many have "fair dealing" or a closed list of
  exceptions (quotation, parody, caricature or pastiche where the law includes them). Your audience and
  your residence may put you under one of those, not under US fair use.
- **Content ID doesn't evaluate fair use.** The match and the claim happen automatically. You can dispute,
  and the dispute can take weeks, during which the claimant may collect the revenue. If the claimant rejects
  the dispute, the next step can be a takedown and a strike.
- **Monetized videos have it harder.** Commercial use counts against fair use, and a meme used as a quick
  joke in a tutorial is rarely commentary on the meme itself, which is the strongest kind of fair use.
- Brand logos and trade dress (a platform's button, an OS dialog, a game's title font) add trademark issues
  on top of copyright.

This README is not legal advice. When the money or the channel matters, ask a lawyer in your jurisdiction.

## The recommended approach

1. **Recreate the joke, not the image.** Most memes are a structure: two options (one rejected), a plan
   that fails at step four, a freeze frame with a narrator, a fake-dramatic zoom. The structure is not
   copyrightable; the picture is. Each entry's `how_to_recreate` describes an original version built with
   `graphics/` (arrows, checkmark and cross, callouts, chapter cards, split layouts) or plain HyperFrames:
   your text, your shapes, your voice, CC0 sounds from [`../library/`](../library/).
2. **Or license the original.** Some are licensable: stock photos (Distracted Boyfriend, Hide the Pain
   Harold) can be bought from the stock agency, and some creators license their work directly. Where a
   licensing route is known, `sourcing` lists it. Keep the license with the project, like the audio
   licenses in [`../library/LICENSES.md`](../library/LICENSES.md).
3. **Use Know Your Meme for context, not for files.** It documents origin and history; the images it hosts
   are not licensed for your video.
4. **Never use the meme's music.** Songs ("Roundabout", "Astronomia", "Never Gonna Give You Up", the Curb
   theme) are the most reliable Content ID matches there are. Use an original or CC0 sting.
5. **Check the tone.** `tone_warnings` flags memes that are dated, mean-spirited, tied to a real person or a
   political figure, or about real tragedies. In a tutorial, a meme should land in two or three seconds and
   never at the viewer's expense.

## How the catalog fits the skill

- A meme is an interrupt: it follows the same rhythm and text rules as any graphic. It enters with the word
  it reacts to, stays for `timing_s`, and any text on it lasts at least
  `max(1.5 s, words x 0.33 s + 0.5 s)`.
- Zoom punch-ins stay within the skill's 1.10 limit and happen inside one shot.
- A sound gag counts as a sound effect: one per event, about 15 dB under the voice, never on top of the
  recording's real clicks.
- At most one or two per video. A tutorial is not a meme compilation.

## Accuracy

Origins, owners and dates were checked against Know Your Meme, Wikipedia and the creators' own
statements on 4 October 2026. Where a fact could not be verified, the entry says `unknown` or attributes
the claim ("per KYM"). If you correct an entry, cite the source in the commit.
