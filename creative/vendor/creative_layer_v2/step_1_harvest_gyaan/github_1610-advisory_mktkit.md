# Harvest — 1610-advisory/mktkit (cut-video + reel-qa skills)

- **Repo:** 1610-advisory/mktkit — "1610 Marketing Toolkit": run your marketing like an AI CMO (markdown + Python + CSV, in Claude Code)
- **Link:** https://github.com/1610-advisory/mktkit
- **Licence:** MIT License (MIT) — verified on repo page; LICENSE file present
- **What it is (relevant part):** The `cut-video` skill is a full talking-reel editing system ("the reel factory"): brief + word-level transcript → reel manifest → B-roll sourcing rules → ffmpeg render → machine QA gate → delivery. Its files encode unusually concrete, numbers-first editing rules: hook handling, punch-in durations, B-roll exactness law, caption timing/safe zones, loudness, platform specs with sources, a QA checklist, and an incident-to-fixture method for turning reviewer catches into code gates. The `reel-qa` skill is the standalone QA-gate entry.
- **Activity:** Created 2026-06-18; 63 commits, 2 tags; latest commit on default branch 2026-10-28 (from clone HEAD `2a69fe1`) — actively maintained, most recent activity of all finds in this round.
- **Files extracted (full, verbatim):** `.claude/skills/cut-video/SKILL.md`, `.claude/skills/cut-video/resources/platform-specs.md`, `.claude/skills/cut-video/CHECKLIST.md`, `.claude/skills/cut-video/REFERENCE.md`, `.claude/skills/reel-qa/SKILL.md`
- **Not extracted:** `cut-video/ONBOARDING.md` (setup/onboarding, not technique), the Python engine scripts and JSON schemas (implementation, not technique prose — see repo).

---


---

## Source file: `.claude/skills/cut-video/SKILL.md`

---
name: cut-video
description: >
  Cut a talking reel from an editor brief + word-level transcript to a
  phone-ready 1080x1920 file for Instagram Reels, YouTube Shorts, TikTok and
  Facebook Reels: fill a reel manifest, source B-roll that matches the spoken
  line, render through the engine, pass the machine QA gate, deliver a watch
  pack. Use when the user says "cut this reel", "edit the video", "in-house
  cut", "cut-video", "rough cut from the brief", "edit lab", "overnight cut",
  "execute the edit lab", "finish this reel", "render the talking cut", or
  runs the queue ("cut the next N"). This is the ffmpeg route: when the tool
  is not named, pick between it and resolve-reel with references/edit-route.md
  (batches and unattended runs point here; editable projects point to Resolve).
metadata:
  version: 2.2.0
---

# Cut Video: the reel factory

You turn a brief and a transcript into a finished vertical reel. **You decide what is said and what is shown. The scripts decide everything about ffmpeg.** Never run ffmpeg by hand for a deliverable and never edit a render with a one-off command: every defect that was fixed by a rule instead of a code gate came back (see `CHECKLIST.md`, "Why the gate is code").

This skill is model-agnostic and harness-agnostic: plain files, Python 3.10+, ffmpeg, Pillow. Optional extras (`open_clip` + `torch` for image search) degrade gracefully.

## Files in this skill

| Path | Role |
|---|---|
| `resources/reel-manifest.schema.json` | The contract. One JSON per reel: source, spine ranges, hook, cover, captions, punches, inserts, audio, render, qa. |
| `resources/manifest.example.json` | Filled example to copy. |
| `resources/style.example.json` | A business's house style (fonts, colors, LUT, eq, caption size). Pass with `--style`; the manifest wins on conflicts. |
| `resources/platform-specs.json` + `.md` | Safe zones, delivery specs, loudness, caption timing, pacing, with sources. |
| `CHECKLIST.md` | Definition of done, frame-review questions, the incident-to-fixture rule. |
| `REFERENCE.md` | Engine flags, orientation tree, traps. Read when a render misbehaves. |
| `scripts/render-reel.py` | Executes a manifest: preflight lint → spine → stills → pre-grade → finish → QA → RUNNOTES → deliver. Holds the render lock. |
| `scripts/qa-reel.py` | Machine QA gate: container, duration, loudness, black/frozen frames, caption safe zone and timing, banned words, hook-once, contact sheet. Exit 3 on FAIL. |
| `scripts/broll-index.py`, `scripts/broll-search.py` | Index a footage/photo library; rank candidates for a spoken line; write verified subjects back. |
| `scripts/regress.py` | Re-render the fixture reels and compare to gold. Run after any engine change. |
| `scripts/bench-reel.py` | Run the same note through several harnesses and models (pi with any provider, Claude Code, codex, grok, cursor) and compare manifests, QA, punches, cost and time in one report. Sibling skill `reel-bench`. |
| `scripts/cut-video.py`, `finish-reel.py`, `stills-to-broll.py` | Engines. render-reel.py calls them; you normally do not. |

Building the reel inside DaVinci Resolve instead (color-managed grade, look LUTs, look-review pages)? Sibling skill `resolve-reel`; it reuses this skill's caption, safe-zone and QA code.

**Pick the route before you cut.** Read `references/edit-route.md` (toolkit root): the business's `edit_route` preference, the hard limits (headless → ffmpeg; wordless montage → Resolve), and the task signals. Recommend one route with the reason; ask once only when it is unclear.

Client-specific inputs live in the **client's** repo, never here: LUT and crop recipe (`resources/video-pipeline/README.md`), fonts and colors (`knowledge/DESIGN.md`), a style profile, a banned-words list, fixtures.

## Mode

**Unattended is the default** when the user says edit lab, overnight, queue, or "cut the next N": render without asking. **Interactive**: stop after step 5 (dry run), show the manifest summary and the preflight table, wait for approval, then continue. Unattended never waits for "render it".

## Steps

1. **Orient.** Read the brief (deliverable name, duration window, public-safe cover line, hook quote + timecode, keep ranges with quoted words, hard-out, B-roll wishes, orientation notes). Read the client's video-pipeline README and design pack. Load the client style profile if one exists. Read `references/edit-craft.md` (toolkit root): the house edit rules for every business.
2. **Inputs.** Every referenced file must exist; the transcript JSON must have `segments[].words[]`. Missing words: transcribe to a local temp dir (word timestamps on), copy the JSON back. Missing file: stop and say which. Never substitute a clip.
3. **Fill the manifest** (copy `resources/manifest.example.json`). Ranges start and end on WORD boundaries from the JSON, each with a `quote` (first words … last words). `hard_out` = the end time of the last kept word, never an SRT cue end. **Hook rule:** if the take opens on the hook line, `mode: none`; if the hook is a later grab, `mode: prepend` with `lift_from_spine: false`: the hook opens the cut, then the whole edit plays through and the line repeats once in context (the reviewer's standing choice). `true` only when the brief asks for one play. Cover: public-safe, 7 words or fewer, the pack's display font. Captions on unless the brief says otherwise. Every punch gets a `line` (the spoken words it illustrates) and `dur` (clips under 3.0 s; stills 3.5 s; a punch carrying a `super` 3.5 to 4.0 s). `render.mode: proxy` while iterating.
4. **B-roll: exact or nothing, video first.** A punch must literally show the noun phrase spoken under it. The ladder: (1) an exact raw clip from ANY job in the index (the same job first, but an arched opening from another Acme Remodeling job is right for "arched opening" on this reel); a callback that needs the earlier line heard is an `insert`, not a punch. (2) An exact photo, only when no exact clip exists AND the index entry carries a human-confirmed subject that matches the line (`descriptions[].by == "human"`; search with `--confirmed-only` for stills). A model's own read of a photo is not enough to put a still on screen: the owner would rather have no photo than a near miss. (3) Nothing exact: stay on the speaker; a sit-down with no B-roll of its own usually ships with zero or one punch, and that is correct. A same-category picture (a hallway for "a hallway full of doors", any door for "hidden door", a closet slider for "pocket door") is a defect, not a fallback. Trade terms are literal: a pocket door disappears into the wall cavity; a bypass or barn slider on a track is not one; a hidden door is concealed in the wall's finish, not a dark door in matching trim. Search with `broll-search.py --index INDEX --lines-from-manifest reel.json --prefer-project JOB --sheet sheet.jpg`; look at the ONE sheet; for each pick write `broll[].line` (the words spoken) and `broll[].shows` (what the picture literally shows, named after looking: object, setting, material), copy `path` (and `src` for a clip), then `--confirm PATH --subject "<shows>"` so the library learns. Stills: at most two per reel, never back to back, 3.5 s, each starting within 0.3 s of the noun it shows. Check every still at full resolution for house numbers, addresses, or a client name. Never finished reels or another piece's A-roll as B-roll.
5. **Dry run.** `render-reel.py --manifest reel.json --dry-run`. Read the preflight table: quotes vs words near each boundary, hard-out on a word end, estimated duration vs window, unsourced punches. Fix the manifest until it is clean.
6. **Proxy render.** `render-reel.py --manifest reel.json --proxy [--style STYLE]`. The renderer takes the render lock, cuts the spine, builds stills, pre-grades mixed sources, finishes, runs the QA gate, writes RUNNOTES and a contact sheet. Read the verdict line and the sheet (one image, small frames). Answer the frame questions in `CHECKLIST.md`. Fix the manifest, re-render the proxy. Iterate on proxies, not finals.
7. **Final render.** Same command without `--proxy`. QA must be `pass`, or `warn` where every WARN is listed under "Known deviations" in RUNNOTES with a reason.
8. **Independent verify** (unattended path). A fresh context (a new agent or a cleared turn) sees ONLY the contact sheet, the cover line, the hook quote, the punch lines, and the CHECKLIST questions, and returns strict JSON per question. A "verified" produced without looking at the sheet does not count.
9. **Deliver.** `deliver.copy_to` puts the mp4, RUNNOTES and sheet in the review folder. Update the content note's revision history per the client repo's rules. Never publish, schedule, or mark approved.
10. **Close the loop.** File every reviewer note first: craft → `references/edit-craft.md`, this business's taste → its `reel-style.json` or `memory/` (sort table in edit-craft.md). A note that the machine missed becomes a QA check or a fixture BEFORE the fix counts as done. After any engine change run `regress.py --fixtures DIR --proxy`.

## Must

- Hook opens the cut and repeats once in the full edit, never more. Hard-out is a word end. Every punch is exact (it shows the noun phrase spoken under it), video before photo, and carries `line` and `shows`; a line with no exact asset stays on the speaker. Stills: two per reel at most, never consecutive, on the noun.
- Captions on, in the safe zone (the engine reads `platform-specs.json`). Cover public-safe, center-anchored.
- Loudness two-pass, 48 kHz. Join fades on talking spines.
- One encode at a time (the lock). Proxies for iteration, one final.
- QA frames small, one contact sheet; never read dozens of full-resolution frames into context.
- RUNNOTES beside every render; "Known deviations" honest.

## Must not

- Compose ffmpeg by hand for a deliverable, or bypass the engine with a "quick pre-grade".
- Wait for approval in unattended mode. Leave listed punches for "the NLE later".
- Overwrite a `_vN`. Write client names, addresses, drive names or real paths into this repo.
- Burn crew first names on screen.

## Queue mode

`/cut-video --next N` selects eligible content notes and runs steps 1 to 10 per note (details in the slash command). Cinematic or wordless pieces: not this skill; say so and stop.


---

## Source file: `.claude/skills/cut-video/resources/platform-specs.md`

# Platform specs: where the numbers come from

Companion to `platform-specs.json`. Every number in the JSON has a row here with its source and the date it was checked. When a platform changes its UI, update the JSON first, then this file, then re-run the fixtures (`regress.py`).

Rule of thumb: the pipeline publishes one 1080x1920 file to every platform, so text is placed inside the **intersection** of all targeted safe rectangles. qa-reel.py and finish-reel.py take the strictest value across the platforms named in the manifest.

## Safe zones (pixels from the edge that platform UI may cover)

| Platform | Top | Bottom | Left | Right | Source | Checked |
|---|---|---|---|---|---|---|
| Instagram Reels, Facebook Reels | 270 (14%) | 672 (35%) | 65 (6%) | 65 (6%) | Meta's 2026 unified 9:16 creative safe-zone guidance for Stories and Reels (14% top, 35% bottom, 6% sides); summarized by several agency guides, e.g. https://behaviour.digital/post/meta-reels-safe-zone-14-top-35-bottom-6-sides-the-2026-official-guide and https://kreatli.com/guides/instagram-reels-safe-zone | 2026-09-04 |
| TikTok | 130 | 484 | 60 | 140 | TikTok Ads creative best practices (keep key elements clear of the status area, caption and audio strip, and the right action rail): https://ads.tiktok.com/help/article/creative-best-practices ; pixel values are the conservative end of practitioner measurements | 2026-09-04 |
| YouTube Shorts | 180 | 350 | 60 | 120 | No official pixel spec. Practitioner consensus for the title and channel row at the bottom and the action rail at the right: https://kreatli.com/guides/safe-zone-guide | 2026-09-04 |

Consequences already built in:
- Dialogue captions default to `safe-lower`: bottom-center alignment with `MarginV = strictest bottom + 24` (694 px for Instagram + Shorts) and side margins of the strictest side band + 16. The old default, `MarginV 220`, put caption text under the Reels caption box on a real phone.
- The cover title is center-anchored, which is inside every safe rectangle.
- Supers sit below the top band.

## Delivery

| Item | Value | Why |
|---|---|---|
| Canvas | 1080x1920, 9:16 | Native vertical canvas for Reels, Shorts, TikTok |
| Codec | H.264 High, yuv420p, AAC 48 kHz, `+faststart` | Universally accepted upload format; 10-bit or 4:4:4 masters are transcoded badly or rejected |
| Frame rate | any of 23.976 to 60 | Platforms accept the common rates; the QA gate flags odd values |
| Minimum video bitrate | 6 Mb/s | Below this, platform re-encodes visibly soften fine texture (tile, brick, wood grain) |
| Max duration | Reels 90 s, Shorts 180 s, TikTok 600 s | Platform limits at the time of checking; the manifest window is always tighter |

## Loudness

| Item | Value | Source |
|---|---|---|
| Pipeline master target | -16 LUFS integrated, -1.5 dBTP, LRA target 11 | House standard for phone playback headroom. Platforms normalize downward toward roughly -14 LUFS; a -16 master arrives without limiting artifacts. |
| Two-pass loudnorm | measure with `print_format=json`, then apply `measured_*` + `linear=true` | The filter's author documents single-pass as the live mode that applies dynamic gain (audible pumping on dialogue): http://k.ylo.ph/2016/04/04/loudnorm.html |
| Keep LRA in the target | yes | ffmpeg's linear mode silently reverts to dynamic when the measured LRA exceeds the target LRA; verified locally on ffmpeg 8.1.1. The QA gate should read `normalization_type` from the second pass when available and flag `dynamic`. |
| Do not assert LRA on the delivered file | informational only | EBU R128 Supplement 1 (short-form programmes) states that Loudness Range limits shall not be specified for short content: https://tech.ebu.ch/docs/r/r128s1.pdf |
| Measurement | `ebur128=peak=true` on the delivered file | EBU Tech 3341/3343 measurement; ffmpeg filter reference: https://ffmpeg.org/ffmpeg-filters.html#ebur128-1 |

## Captions

| Item | Value | Source |
|---|---|---|
| Minimum cue | 0.83 s (20 frames) | Netflix Timed Text Style Guide, subtitle timing: https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines |
| Minimum gap between cues | 2 frames (0.067 s at 30 fps) | same |
| Reading speed | 20 characters per second maximum (adults) | Netflix English Timed Text Style Guide: https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide |
| Line length | 32 characters, 2 lines | Netflix allows 42 on a 16:9 frame; DCMP Captioning Key recommends 32 or fewer: https://dcmp.org/learn/597-captioning-key---text . On a 1080-wide frame at size 42 to 48 inside 65 to 140 px side margins, 32 is what fits. |
| Never cross an edit join | rule | A cue that spans a jump cut reads as a mistake; the engine splits cues at every `--spine-range` boundary |
| Never drop a kept word | rule | Short words at range ends were dropped by an earlier clamp; the engine now keeps the word and clamps its end |
| Escape handling | ASS `\N` is the line break; drawtext has no such escape | The literal backslash-N defect (2026-09-04) was in the cover drawtext; the cover now wraps via a textfile and rejects a backslash in the text |

## Punch-ins and pacing

| Item | Value | Why |
|---|---|---|
| Clip punch | under 3.0 s | House rule from the owner's reviews; longer clip punches read as a cutaway, not a punch |
| Still punch | 3.5 s default | Slow-push stills need the extra second to read (owner note 2026-09-04) |
| Punch carrying a super | 3.5 to 4.0 s | Text must be readable (owner note 2026-09-04) |
| Consecutive stills | 2 maximum | Three stills in a row reads as a montage, not a talking reel |
| A-roll between punches | 3.0 s minimum, or butt the punches | Shorter A-roll flashes read as a glitch (reviewer, 2026-09-24) |
| Visual change cadence | a visual change every 3 to 7 s, tighter in the first 5 s | Practitioner retention guidance for vertical short-form; not a standard, a budget the timeline should meet: https://www.strategia-x.com/blog/2026-07-01-vertical-video-retention-editing-playbook/ |
| Punches per minute | 10 maximum | Derived from the cadence rule and the 3.0 s minimum A-roll; a soft ceiling the QA gate can warn on |

Owner rule 2026-09-07: a punch must literally show the noun phrase spoken under it, or the reel stays on the speaker. Stills are the fallback to video: at most two per reel (`max_stills_per_reel: 2`), never two in a row (`max_consecutive_stills: 1`), and each still starts within 0.3 s of the spoken noun (`still_on_noun_s`). A photo pulls the viewer out of the moment; only an exact one earns it. Video punches use a looser 0.8 s window (`clip_on_noun_s`).

## Cover title

| Item | Value | Why |
|---|---|---|
| Words | 7 maximum | Readable in the 2.0 s hold at display size 72 |
| Line width | about 18 characters before wrapping to two lines | Display serif at 72 px on a 1080 canvas with side margins |
| Content | public-safe: never a client surname or address | Confidentiality rule; enforced by the banned-words list in QA |


---

## Source file: `.claude/skills/cut-video/CHECKLIST.md`

# Cut Video: definition of done and review questions

Companion to `SKILL.md`. Two audiences: the model that cuts (run this before calling a reel done) and the model or person that verifies (answer the frame questions from the contact sheet alone).

## Why the gate is code

Across the first nine working days of the in-house pipeline (about 35 renders, roughly 60 defect instances), every defect class that was fixed with a code gate stayed fixed: the frozen-punch check, the duration cap, the overwrite refusal. Every class fixed with a prose rule or a manual recipe came back at least once: the transpose direction (fixed in the engine, then re-introduced by a hand-built pre-grade step), the repeated hook (a rule existed; two repeats followed; since 2026-09-25 one repeat is the design, a second is the defect), the cover centering (fixed twice), the LUT on Rec.709 footage (three times). Half of all defects reached the reviewer. So: when a reviewer catches something, the fix is a check in `qa-reel.py`, a refusal in `render-reel.py`, or a fixture in `regress.py`, and only then a sentence in a document.

## Definition of done (the renderer and QA gate enforce most of this; you confirm the rest)

Machine-checked, from `qa-reel.py` (id in parentheses):

- [ ] 1080x1920, yuv420p, H.264 + AAC 48 kHz, faststart (`container.*`)
- [ ] Duration inside the brief window and under the platform maximum (`duration.*`)
- [ ] Integrated loudness at the manifest target ±1 LU, true peak under the platform ceiling, no silence gap over 0.8 s, no clipped tail (`audio.*`)
- [ ] No black run, no frozen frame outside a punch window (`video.*`)
- [ ] Captions inside the strictest platform safe zone, no cue under the minimum duration, no oversized cue (`captions.*`)
- [ ] Cover text 7 words or fewer, no literal escape characters (`text.cover_words`)
- [ ] No banned term (client surname, address) in cover, supers, captions, or punch lines (`text.banned_words`)
- [ ] Hook opens the cut; it repeats once in the full edit only when `lift_from_spine` is false, never twice (`hook.once`)
- [ ] Every punch has `verified: true` (`broll.verified`)

Confirmed by a look at the contact sheet (see the questions below):

- [ ] The person is upright and framed in every sampled frame, including the hook and the last frame
- [ ] The cover reads as one or two centered lines in the display font, in the brand color, over a frame that is not blown out
- [ ] Each punch is `exact`: the frame literally shows the noun phrase in its `line`, and `shows` names that object. Category matches are defects. No more than two stills, never two in a row, each on its noun. Lines with no exact asset stay on the speaker
- [ ] Captions are legible, not overlapping the cover or a super, and not touching the bottom band
- [ ] Grade: A-roll and punches match; nothing flat (log left ungraded) or crushed (a Rec.709 still put through the LUT)
- [ ] Nothing on screen names a client or shows a house number, mailbox, or address

Process:

- [ ] Rendered from the camera file through `render-reel.py`, not from an older spine, not by hand
- [ ] RUNNOTES beside the file: why this version exists, punch map with lines, color decisions, loudness, known deviations, provenance
- [ ] Proxy iterations done; exactly one final for this version number
- [ ] Revision history line appended in the client's content note; nothing published or scheduled

## Frame questions for the verifier

Given ONLY the contact sheet (first, cover at 1.0 s, hook end, each punch midpoint, each join, last), the cover line, the hook quote, and the punch lines. Answer each with `yes`, `no`, or `cannot tell`, plus the frame label and one sentence. Return JSON: `[{"q": "...", "answer": "yes|no|cannot tell", "frame": "punch2", "note": "..."}]`. Default to `no` when unsure; `cannot tell` is a request for a better frame, not a pass.

1. Is the person upright (head at the top, floor at the bottom) in the first, hook-end, and last frames?
2. Does the cover frame show the exact cover line, wrapped to at most two lines, centered, in a serif display face and the brand color?
3. For each punch frame, grade it: `exact` (the picture literally shows the noun phrase in `line`; name the object you see), `category` (the same kind of thing but not what the line names: a hallway for "a hallway full of doors", any door for "hidden door", a closet slider for "pocket door"), or `wrong` (something else). Trade terms are literal: a pocket door disappears into a wall cavity, a bypass or barn slider on a track does not; a hidden door is concealed in the wall's finish (slats, paneling), not a dark door in matching trim; an arched opening has no door slab. Only `exact` passes. A line with no punch is correct when no exact asset exists; say whether the run's own `shows` texts suggest one did.
4. Do any two punch frames show the same picture? Are there more than two stills, or two stills back to back?
5. Is any caption cut off, overlapping the cover or a super, or sitting inside the bottom third of the frame?
6. Does any frame look flat and desaturated (ungraded log) or crushed and orange (double-graded)?
7. Is there any readable text that is not ours: a house number, a street sign, a mailbox, a client's name, a crew member's first name burned in?
8. Does the last frame show the person mid-sentence (a hard-out that cut too early) or a blank/black frame (a hard-out that ran long)?
9. Is there a join frame where the background jumps in a way a punch should have covered?
10. Would a stranger scrolling past understand the topic from the cover frame alone?

A reel passes the verifier when every answer is `yes` for 1, 2, 3 (all punches), 10, and `no` for 4 to 9.

## Incident to fixture

When the reviewer finds a defect the pipeline did not flag:

1. Write one line in the client's `defects.csv` (class, date, reel, version, caught by, recurred).
2. Decide the gate: a `qa-reel.py` check (measurable on the file), a `render-reel.py` refusal (detectable from the manifest or inputs), or a fixture in the client's fixtures folder (needs real footage to reproduce).
3. Build the gate first; confirm it fails on the defective render; then fix the cause; confirm the gate passes.
4. Only then update SKILL.md or REFERENCE.md if wording must change.

## Review rounds

Label each delivered version in RUNNOTES as `Round: STRUCTURE` (line selection, order, hook, hard-out, punch subjects) or `Round: POLISH` (color, caption styling, cover wording, timing nudges). Reviewer notes about structure on a POLISH cut open a new STRUCTURE round. Ask the reviewer for notes in one shape: `mm:ss  what is wrong  what it should be`, one line each, and a final `SHIP` or `REVISE`.


---

## Source file: `.claude/skills/cut-video/REFERENCE.md`

# cut-video: engines, flags, traps

Companion to `SKILL.md`. Read when a render misbehaves or when you must call an engine directly. Normal work goes through `render-reel.py` and a manifest; the flag tables below are what the renderer drives for you.

## render-reel.py (the one command you run)

`render-reel.py --manifest reel.json [--proxy] [--style STYLE.json] [--version N] [--dry-run] [--strict] [--no-deliver] [--no-qa] [--lock-file PATH] [--work-dir DIR] [--keep-work] [--ledger PATH | --no-ledger]`

Exit codes: 0 rendered · 2 manifest or input problem (invalid manifest, missing file, transcript without words, unsourced punch, `--strict` preflight warning) · 3 a downstream script failed · 4 rendered but the QA gate reported FAIL (file exists; read the report) · 5 render lock timeout.

Order of work: validate against the schema → preflight (files, words, quote lint, hard-out is a word end, duration estimate) → version → color detection per clip (`signalstats` YMIN: about 31 to 33 in 8-bit means log, single digits means Rec.709; the renderer prints the value) → hook lift → hard out → spine (`cut-video.py --emit-json`) → joins from the spine timeline → stills (`stills-to-broll.py`) → pre-grade mixed sources → inserts → finish (`finish-reel.py`, flags feature-detected from `--help`) → QA (`qa-reel.py`) → RUNNOTES → deliver → one summary JSON line on stdout.

Files beside the output `<id>_<slug>_v<N>.mp4` (or `_v<N>-proxy.mp4`): `.reel.json` (resolved manifest with provenance), `-RUNNOTES.md`, `.ass` and `.srt` (captions), `.cover.jpg` (title frame for the thumbnail), `.timeline.json` (finish timeline: hook, punches, joins, captions, loudness), `.qa.json`, `.sheet.jpg`. Intermediates live in `.work/<id>_v<N>/` and are removed on success unless `--keep-work`.

The render lock (`~/.cache/reel-factory/render.lock` by default) serializes every encode on the machine. Two renderers never run at once; the second waits and says so. Parallel 4K encodes once pushed swap past 15 GB.

## Manifest semantics the renderer applies

- `version: "auto"` picks the next free `_vN`; proxies are `_vN-proxy` and never consume a final number. Nothing is ever overwritten.
- `hook.mode: prepend` with `lift_from_spine: false` (default) opens on the hook and keeps it in the spine, so the line repeats once in context. `true` removes the hook range from the spine (splitting the range it sits in) so the line plays once. A hook from a different file lifts nothing.
- `spine.hard_out` clamps the last range. It must be a word END from the JSON; the preflight lint warns when it is not.
- `joins: "auto"` = every coarse-range boundary on the output clock, read from the spine timeline. finish-reel covers each join with the nearest punch.
- `source.color: auto` and `broll[].color: auto` are measured per clip; stills are Rec.709 by definition. Log spine with log clips: `--lut` for everything. Log spine with any Rec.709 punch (stills, phone clips): the A-roll and hook keep the LUT in finish-reel, log B-roll clips are pre-graded in the work dir, and finish-reel runs with `--broll-no-lut --broll-no-eq` so Rec.709 punches are left alone. Rec.709 spine with log clips: log clips pre-graded, `--skip-lut`. The first model bench (2026-09-05) crushed the stills in all four runs before this rule; `qa-reel` now warns on a punch/A-roll saturation mismatch (`video.grade_mismatch`).
- `source.eq: "none"` → `--no-eq`. `broll[].eq: "none"` on every punch → `--broll-no-eq`.
- `broll[].kind: still` (or an image extension) → `stills-to-broll.py` first; `dur` defaults 3.5; with a `super` at least 3.5.
- `inserts[]`: the spine is split at `after_word_end`; part A (cover, hook), the insert (its own audio, optional super), part B (punches recomputed) are finished separately and concatenated with a re-encode.
- `render.mode: proxy` or `--proxy`: 540x960, hardware encoder when available, every other step unchanged. Iterate on proxies.

## cut-video.py (spine)

| Flag | Role |
|---|---|
| `--source` / `--json` / `--output` | Camera file, word-level JSON, spine mp4 |
| `--range start:end` | Repeat per keep region. **Sorted and merged if they overlap** (the hook trap below) |
| `--max-pause 0.40` · `--keep-tail 0.10` · `--keep-lead 0.05` | Engine defaults. Talking reels: 0.85 / 0.20 / 0.08 (the manifest defaults) |
| `--join-fade SEC` | Audio fade at every kept segment boundary (0.05 to 0.08). Range joins stop clicking |
| `--no-filler-removal` / `--no-pause-compression` | Off switches |
| `--emit-json PATH` | Spine timeline: `coarse_ranges[]` with `out_start/out_end`, `segments[]`, `removed_fillers[]`, `duration_s`. Does not change the render |
| `--force-8bit` | Do **not** use before the LUT. Grade in 10-bit; finish-reel delivers 8-bit |
| `--dry-run` | Print ffmpeg, do not render |

JSON must have `segments[].words[]` with `start`/`end`. Segment-only JSON is not enough.

## finish-reel.py (phone file)

Processing order is locked: extract hook → normalize A-roll (orient → LUT → eq → canvas) → normalize B-roll (orient → LUT → same eq) → `setpts` and overlay on the spine clock → concat hook in front → cover drawtext → dialogue captions (ASS) → loudness → encode.

| Flag | Role |
|---|---|
| `--spine` / `--output` | Input spine, final file |
| `--hook-source` + `--hook-range` / `--hook` | Cold-open clip extracted from the camera file, or a pre-cut clip |
| `--lut` / `--skip-lut` | 3D cube before eq and before text |
| `--eq` / `--no-eq` | A-roll match after LUT. Default `contrast=1.14:saturation=1.35:brightness=-0.015` |
| `--cover-text` · `--cover-seconds 2.0` · `--cover-anchor center|top` · `--cover-case as-is|upper|sentence` · `--cover-darken` | Title card. A backslash in the text is rejected (exit 2); the engine wraps via a textfile. `center` is the IG-safe default; darken dims one frame only |
| `--font` · `--font-color #F2EDE0` · `--font-size 72` | Cover type, absolute font path. Family and color come from the client pack |
| `--broll PATH:at=SEC:dur=SEC[:src=SEC][:kind=clip|still]` | Repeatable. `at` on the cut spine before hook prepend. Omit `src` for a mid-clip in-point |
| `--max-broll-dur 3.0` · `--min-aroll 3.0` · `--join SEC` · `--broll-no-eq` · `--broll-no-lut` | Punch cap; butt punches closer than 3.0 s; cover a spine concat with the nearest punch; B-roll skips the match eq; B-roll skips the LUT (A-roll and hook still take it) |
| `--super TEXT:at=SEC:dur=SEC` · `--super-size 44` | Upper-third annotation below the top safe band |
| `--transcript` + `--spine-range start:end` (repeat) | Burn dialogue captions from kept words only; cues never cross a join; kept words are never dropped |
| `--caption-font` · `--caption-size 42` · `--caption-style phrase|word` · `--caption-min-cue 0.8` · `--caption-max-cue 2.8` · `--caption-max-chars 32` · `--caption-max-lines 2` · `--no-captions` | Caption typography and grouping |
| `--caption-placement safe-lower|safe-center|custom` · `--caption-margin-v` · `--caption-margin-side` · `--platforms LIST` · `--platform-specs PATH` | Placement from the strictest platform safe zone: `safe-lower` = bottom-center with `MarginV = bottom band + 24` (694 px for Reels + Shorts) |
| `--ass-out PATH` | Keep the ASS beside the output (default `<output>.ass`); an SRT is written alongside |
| `--loudnorm-mode two-pass|single|off` · `--loudnorm-i -16` · `--loudnorm-tp -1.5` · `--loudnorm-lra 11` · `--denoise off|light` | Two-pass is the default: measure, then `linear=true`. Keep LRA in the target or linear mode reverts to dynamic. `light` = `afftdn` for phone mics only |
| `--proxy` · `--encoder auto|libx264|h264_videotoolbox` · `--threads N` | 540x960 preview with the hardware encoder; finals stay libx264 CRF 18 |
| `--emit-json PATH` | Finish timeline on the FINAL clock (hook, punches `at_final`, joins, captions, cover, loudness, encoder) |
| `--qa-dir DIR` · `--qa-max-px 540` | Frames: first, cover, hook end, three per punch window, last; exit 3 on a frozen punch. No frame larger than 540 px |
| `--orient auto|none|r5-portrait|landscape-punch|tall-spine` · `--rotate 90|180|270` | Per-clip orientation; `--rotate` only when the brief says so |
| `--width 1080 --height 1920 --crf 18 --preset fast` · `--force` · `--dry-run` | Delivery and safety |

## stills-to-broll.py

`--image IN --output OUT.mp4 [--dur 3.5] [--zoom 1.10] [--direction in|out] [--focus fx,fy] [--eq ...] [--engine auto|pil|zoompan]`. Pillow per-frame sub-pixel resample is the default; ffmpeg `zoompan` is the fallback because it steps on whole pixels and a slow push jitters (measured with `signalstats` YDIF). EXIF upright, 9:16 crop around the focus point, no audio.

## Orientation decision tree

Probe each clip. Do not trust a 4096x2160 container.

1. Display-matrix or `rotate` tag ±90 **and** width > height → `r5-portrait` with `-noautorotate`. **Transpose follows the matrix sign**: `+90` → `transpose=2`, `-90` → `transpose=1`. Then crop from the standing frame: `2160:3840:0:128` when the container was 4096 wide, else a centered 9:16 crop.
2. Already upright (height > width, no rotation): within 1% of 9:16 → scale only; taller → crop to 9:16 before scale.
3. True landscape that must become 9:16 → `landscape-punch`: `crop=ih*9/16:ih:(iw-ih*9/16)/2:0`.
4. Sideways B-cam with no flag → `--rotate` only when the brief says so.

Never hand-roll a pre-grade or pre-rotate outside the engine: that path re-introduced the upside-down hook once already. If a source needs handling the engine lacks, add it to the engine with a test.

## Traps

- **Hook merge.** `cut-video.py` merges overlapping ranges; a hook passed as a range disappears into the spine. The manifest handles this (`lift_from_spine`).
- **B-roll stills freeze.** Overlays must be `setpts` onto the spine clock or the last frame repeats. The engine does this; `--qa-dir` catches a regression.
- **LUT on Rec.709** double-grades orange. Measure, do not eyeball; the renderer prints YMIN per clip.
- **SRT cue end as hard-out** lands half a sentence late. Use the word end.
- **Full-resolution QA frames** in a model's context killed a session (70 frames, 52 MB). Frames are capped at 540 px; look at the one contact sheet.
- **Parallel encodes** blew swap. The lock serializes them.

## Naming

`<id>_<slug>_v<N>.mp4`, proxies `_v<N>-proxy.mp4`. Sidecars share the stem. Never overwrite a version; `finish-reel.py` exits 2 when `--output` exists unless `--force`, and the renderer never passes `--force`.

## Changelog

2.1.0: `bench-reel.py` and the `reel-bench` sibling skill: the same note through several harnesses and models, scored on manifest, QA, punches, stray writes, cost and time; `video.join_uncovered` QA check; preflight lint tokenizes quotes per spoken word; style files may carry `_` keys.
2.0.0: manifest-driven `render-reel.py` (preflight lint, hook lift, color measurement, mixed-source pre-grade, inserts, render lock, RUNNOTES, ledger, provenance, style profile); `qa-reel.py` gate with contact sheets; `broll-index.py` / `broll-search.py` (job-first ranking, captions from alt text, optional CLIP, write-back); `regress.py` fixtures; finish-reel two-pass loudness, safe-zone captions, caption timing, proxy encoder, SRT + cover frame, timeline JSON, 540 px QA frames; platform specs with sources; sibling skills `reel-qa`, `reel-broll`, `reel-regress`.
1.2.3: stills-to-broll sub-pixel engine; text punches hold 3.5 to 4 s.
1.2.2: `--max-broll-dur`, `--super`, `cut-video --join-fade`, insert recipe.
1.2.1: stills-to-broll.py; caption words clamped to range end.
1.2.0: upright tall-spine crop, wide-container hook crop, loudnorm stage, cover wrap via textfile, caption cues limited to kept words, mixed-grade recipe, hard-out from the word JSON.


---

## Source file: `.claude/skills/reel-qa/SKILL.md`

---
name: reel-qa
description: >
  Run the machine QA gate on any vertical short-form video and read the
  result: container and delivery specs, duration window, loudness and true
  peak, black or frozen frames, caption safe zone and timing, banned words,
  hook-once, plus one small contact sheet for a visual check. Use when the
  user says "QA this reel", "check this video before it ships", "is this
  safe for Reels/Shorts", "run the gate", "why did QA fail", or hands you an
  mp4 and asks whether it is ready to post.
metadata:
  version: 1.0.0
---

# Reel QA

A standalone entry to the QA gate that `cut-video` runs automatically. Use it on files that did not come out of the renderer (an editor's delivery, an older cut, a re-export) or to re-check one after a manual change.

Script: `../cut-video/scripts/qa-reel.py`. Specs it reads: `../cut-video/resources/platform-specs.json` (see `platform-specs.md` for sources). Review questions: `../cut-video/CHECKLIST.md`.

## Steps

1. Identify the file and, if they exist beside it, the manifest (`*.reel.json`), the finish timeline (`*.timeline.json`), and the captions (`*.ass`). Ask nothing if the file alone is given; the gate works with less and marks the rest `na`.
2. Run the gate, always with a contact sheet and small frames:

   ```
   python3 <skill>/scripts/qa-reel.py --video FILE.mp4 \
     [--manifest FILE.reel.json] [--platforms instagram_reels,youtube_shorts] \
     [--duration-window MIN,MAX] [--banned-words client/resources/public-safe-banned-words.txt] \
     --report FILE.qa.json --contact-sheet FILE.sheet.jpg --frames-dir ./qa-frames --max-px 540
   ```

   Exit 0 = pass (warnings allowed), 3 = at least one FAIL, 4 = warnings with `--strict`, 2 = bad input.
3. Read the report table (FAILs first) and then look at the ONE contact sheet. Answer the frame questions in `CHECKLIST.md` for the frames shown. Do not extract additional full-resolution frames into context; ask for a specific frame with `contact-sheet.py --video FILE --times T` at `--max-px 540` if one is needed.
4. Report: the verdict line, each FAIL with measured vs expected in one sentence, each WARN in one line, and the visual answers. State plainly what must change before the file can ship. For an editor's delivery, phrase the notes as timestamped requests (`mm:ss what is wrong, what it should be`).

## Interpreting common results

- `container.resolution` FAIL on a 540x960 file: it is a proxy, not a delivery; render the final.
- `captions.safe_zone` FAIL: caption bottom sits inside the platform UI band; re-render with `--caption-placement safe-lower` (the engine default) or move the burned captions up in the NLE.
- `audio.integrated_loudness` outside tolerance: normalize (two-pass loudnorm) rather than raising the gain by ear.
- `video.frozen_frames` WARN inside a punch: a static tripod shot or a still; fine. FAIL outside a punch: a real freeze, usually a B-roll overlay whose timestamps were not shifted onto the spine clock.
- `hook.once` WARN: the opening line appears again more often than designed (one repeat is expected when `lift_from_spine` is false); check whether the take says its hook twice.
- `text.banned_words` FAIL: a client name or address is on screen or in the caption text. The file cannot ship.

## Must not

- Call a file "verified" without the report AND a look at the sheet.
- Read more than one contact sheet or any frame larger than 540 px into context.
- Publish, schedule, or change a content note's status; this skill only reports.
