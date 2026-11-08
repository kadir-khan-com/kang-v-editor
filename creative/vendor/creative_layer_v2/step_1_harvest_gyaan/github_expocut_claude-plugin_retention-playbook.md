# Source: ExpoCut — "expocut-retention-playbook" skill

- **Source name:** expocut/claude-plugin, skill at `plugins/expocut/skills/expocut-retention-playbook/` (v3.0.0)
- **Repo link:** https://github.com/expocut/claude-plugin

> ⚠️ **LICENCE NOTE — two different terms apply; read both:**
> 1. **Repo level:** the cloned repo's `LICENSE` file is the **MIT License** (Copyright (c) 2026 ExpoCut).
> 2. **Skill level:** this playbook's own `SKILL.md` frontmatter declares: `license: Free to use and redistribute with attribution to expocut.com.`
> The skill text itself therefore carries an **attribution condition** (credit expocut.com) even though the repository is MIT. Until the maintainer clarifies, treat the playbook content as **free to use WITH attribution to expocut.com**, not as plain MIT.

- **Content map (one line):** A short-form (TikTok/Reels/Shorts) retention playbook for the ExpoCut phone editor: hook window (0–1s pattern interrupt + 4–7-word text hook + audio spike; sound-off legibility to 3s; explicit promise at 3–5s; 5 reusable hook formats) → cadence rule (visible change every 3–5s; 0.5–1s for trend/entertainment) → snap punch-ins as hold keyframes (scale 1.0↔1.1, timeline milliseconds) → per-platform duration table with completion/retention thresholds → per-platform safe-zone percentages plus a numeric safe-box check → optimisation-signal ranking (completion > sends > likes) → cover-frame rules → a filmstrip/canvas verify loop → full MCP tool-signature list with key parameters → 2 worked recipes (25s talking-head pass; 12s loop reel) → pitfalls.
- **Extraction method:** `git clone --depth 1` on 2026-11-05; the skill's `SKILL.md` and its `references/tools.md` reproduced **verbatim** below. The playbook explicitly says: "Do not use for long-form YouTube pacing beyond the basics."

---

## Extracted content (verbatim, by source file)


---

## 📄 SOURCE FILE: `plugins/expocut/skills/expocut-retention-playbook/SKILL.md` (verbatim)

---
name: expocut-retention-playbook
description: "Retention editing for TikTok, Instagram Reels and YouTube Shorts inside ExpoCut through the in-app MCP server: the first-second hook (open mid-action, a four to seven word text hook, an audio spike), a visible change every three to five seconds, snap punch-ins as hold keyframes at real timeline milliseconds, duration targets per platform, text kept inside platform safe zones checked with describe_canvas and the capture_canvas grid, seamless loop endings, a cover frame, and a preview_filmstrip verify loop. Use when the user wants a video to perform, go viral, hold attention, asks about hooks, retention, watch time, completion rate, the best length for a platform, where text is safe from the app UI, why viewers swipe away, or wants a cover frame. It decides what to change and when, then calls the executing skills (expocut-video-creating, expocut-social-speed-edit, expocut-audio-post, expocut-kinetic-captions). Do not use for long-form YouTube pacing beyond the basics."
license: Free to use and redistribute with attribution to expocut.com.
compatibility: Works standalone as guidance; becomes hands-on when paired with the ExpoCut in-app MCP server (private/loopback network only).
metadata:
  author: ExpoCut (expotechin.com)
  version: "3.0.0"
  homepage: https://expocut.com/skill.html
---

# The retention playbook

You are the retention editor. The scroll decision happens in about 1.5 seconds, so everything
below serves the first second first. You change the live project on the user's phone; keep a
checkpoint before a pass, verify with cheap text readouts before spending images, and let the
user decide on removals.

## When to use / hand off

Use this skill to decide what to change and when: hook, cadence, punch-ins, duration, safe
zones, loop, cover frame. It executes the simple calls itself and hands the rest off:

- cuts, trims, titles, stock, music, export: expocut-video-creating and expocut-editor-ops
- speed ramps, cut-level transitions between two clips, zoom punches at scale: expocut-social-speed-edit
- beat detection, silence removal, ducking, loudness: expocut-audio-post
- captions and word-by-word text (most viewers watch muted): expocut-kinetic-captions
- keyframe easing beyond a snap, motion paths: expocut-motion-graphics

## Before you start

- Ask which platform and whether the piece is entertainment or educational; that sets the target
  length (table below) and the safe zone.
- `get_active_project`, then `get_canvas_info` for `totalDurationSec` and the aspect, and
  `list_layers` for ids and timings (seconds). Never guess an id.
- `save_history_checkpoint { label: "before retention pass" }` so the whole pass can be reverted
  with `undo_to_checkpoint { id }`.
- Units: cut tools take seconds; `keyframe_add` takes `timeMs` in milliseconds on the project
  timeline (a punch-in at 4 s is `timeMs: 4000`, and `timeMs: 4` lands at 4 ms).

## Core workflow

### 1. The hook window

- 0 to 1 s: a pattern interrupt (hard cut mid-action, whip pan, snap zoom), a four to seven word
  text hook, and an audio spike. Start mid-motion, never on an intro card.
- 0 to 3 s: the hook has to work with sound off. Text, not narration, carries it.
- 3 to 5 s: state the explicit promise ("3 edits that double watch time").
- Hook formats that keep working: bold or contrarian claim, open question, result first (show the
  payoff frame at t=0, then the process), numbered promise, direct callout ("if you edit on your phone").

Execution:

```
trim_layer { layerId: "video_…", mediaOffsetSec: 3.2, startTimeSec: 0 }          // skip the wind-up, open mid-action
add_text_layer { text: "3 edits that double watch time", fontSize: 64, fontWeight: "800", textColor: "#FFFFFF", fontFamily: "din-condensed", textAlign: "center", y: 18, startTime: 0, duration: 2.5, transitionIn: "slideUp", transitionInDuration: 0.25, textStrokeColor: "#000000", textStrokeWidth: 3, textAutoFit: { maxSize: 64, minSize: 40, maxLines: 2 } }
stock_search_music { query: "whoosh", category: "sfx", maxDuration: 2 }
add_stock_music_layer { soundId: 123456, startTime: 0, duration: 1, volume: 0.9 }  // example id
set_layer_transition { layerId: "video_…", in: { id: "whippan", durationSec: 0.3 } }
```

If the strongest moment sits later in the clip, `split_layer { layerId, atSec: 6 }` and move the
second half to the front with `trim_layer { layerId: "video_…second", startTimeSec: 0 }`, or let
expocut-social-speed-edit rebuild the order.

### 2. Cadence: change something every 3 to 5 seconds

- Baseline for short-form: a visible change (cut, B-roll, text pop, zoom, angle) at least every
  3 to 5 s. Trend and entertainment cuts run 0.5 to 1 s; educational content can hold 4 to 5 s.
- Talking head: cut at sentence boundaries. Run `auto_remove_silence { layerId: "video_…", thresholdDb: -40, minSilenceMs: 500, paddingMs: 80 }`
  first (it rebuilds the layer into trimmed segments; take the checkpoint before it), then punch
  in on every second or third cut.
- Music-led: cut on beats; expocut-audio-post owns `beat_cut_from_drums`.

A snap punch-in is two hold keyframes, not a ramp; `interp` describes the curve leaving the
keyframe, so a hold on the 1.0 key keeps the frame still until it jumps:

```
keyframe_add { layerId: "video_…", property: "transform.scale", timeMs: 0, value: 1.0, interp: { type: "hold" } }
keyframe_add { layerId: "video_…", property: "transform.scale", timeMs: 4000, value: 1.1, interp: { type: "hold" } }
keyframe_add { layerId: "video_…", property: "transform.scale", timeMs: 8000, value: 1.0, interp: { type: "hold" } }
```

Alternate 1.0 and 1.1 at each chosen cut. For a settle instead of a snap, ease back:
`keyframe_add { layerId: "video_…", property: "transform.scale", timeMs: 4000, value: 1.1, interp: { type: "preset", name: "easeOut" } }`
followed by a 1.0 key 400 ms later. Times are project-timeline milliseconds, so a clip that
starts at 12 s gets keys at 12000 and up; a text layer cannot host scale keys for a video.

### 3. Durations that fit distribution

| platform | sweet spot | note |
| --- | --- | --- |
| TikTok | 21 to 34 s entertainment; 60 to 90 s educational | completion is the first signal; over 50 percent completion earns pushes |
| Shorts | 15 to 30 s | roughly 65 percent retention needed under 30 s; loops count as watch time |
| Reels | 7 to 15 s punchy; 30 to 60 s value | watch time and sends outrank likes |

Under 15 s, build a seamless loop: make the last shot match the opening shot and end mid-motion.
`trim_layer { layerId: "video_…last", durationSec: 2.6 }` so the final frame resembles the first,
and never add a "thanks for watching" outro to short-form.

### 4. Safe zones

Platform UI covers the edges. In canvas percent (measured on 1080 x 1920, valid for any 9:16 size):

- TikTok: top 10, bottom 18, right 12. Reels: top 13, bottom 21, right 14. Shorts: top 10, bottom 21, right 12.
- Universal cross-platform zone: x from 9 to 91, y from 14 to 86. Practical rule: hook text at
  y 15 to 22; captions and CTAs no lower than y 78; nothing important in the right 14 percent.

Check numerically before spending an image: `describe_canvas { timeSec: 0.5 }` returns each visible
layer's box as `{ x, y, w, h }` in percent; text is safe when `y >= 14`, `y + h <= 79` and
`x + w <= 86`. Then confirm visually with `capture_canvas { timeSec: 0.5, grid: true }` (10 percent
grid) and fix with `update_layer { id: "text_…", patch: { position: { x: 0, y: 18 } } }` or a
smaller `fontSize` through `update_text`.

### 5. Signals to optimise

1. Completion and watch time, everywhere.
2. Sends per reach (DM shares) on Instagram: frame content as "send this to someone who".
3. Likes are the weakest signal; never trade the first two for them.

Plan the cover: one readable three to five word frame. `render_still { timeSec: 0.4, format: "png" }`
writes it to a file for the Shorts thumbnail; Reels covers must survive a centred 1:1 crop, so keep
that frame's text inside x 22 to 78.

### 6. Verify

```
preview_filmstrip { fromSec: 0, toSec: 3, frames: 6 }        // would you stop scrolling? is the hook readable in frame 0?
preview_filmstrip { fromSec: 0, toSec: 30, frames: 12 }      // any 5 s window with nothing changing is a swipe risk
describe_canvas { timeSec: 0.5 }                              // safe-zone numbers
capture_canvas { timeSec: 0.5, grid: true }                   // safe-zone eyes
```

Both filmstrip calls need the editor on screen and cost one image per frame; use the
`describe_canvas` readout first when you only need placement.

## Tools you will use

| tool | what for | key params (units) |
| --- | --- | --- |
| trim_layer | open mid-action, shorten, move a clip | layerId*, mediaOffsetSec, durationSec, startTimeSec (s) |
| split_layer | cut a clip at a moment | layerId*, atSec (s, relative to the layer start) |
| add_text_layer | the text hook | text*, fontSize, fontWeight, y (percent), startTime, duration (s), transitionIn (list_transitions id), textStrokeColor/Width, textAutoFit |
| update_text / update_layer | resize or move the hook | layerId + text fields; id + patch { position } |
| set_layer_transition | pattern interrupt on one clip | layerId*, in { id: "whippan" or "flash" or "zoomBlur", durationSec } |
| keyframe_add | snap punch-in | layerId*, property "transform.scale", timeMs (ms, timeline), value, interp { type: "hold" } |
| keyframe_clear | remove a punch-in track | layerId*, property |
| auto_remove_silence | sentence-boundary cuts on a talking head | layerId*, thresholdDb, minSilenceMs, paddingMs |
| stock_search_music / add_stock_music_layer | whoosh or riser at t=0 | query, category "sfx", maxDuration; soundId, startTime, duration, volume |
| describe_canvas / capture_canvas | safe-zone numbers / grid picture | timeSec; grid: true |
| preview_filmstrip | hook and cadence review | fromSec, toSec, frames 1..12 |
| render_still | cover frame file | timeSec, format png/jpg |
| get_canvas_info / list_layers | length, aspect, ids | none |
| save_history_checkpoint / undo_to_checkpoint | revert the whole pass | label; id |

## Recipes

### 1. Talking-head retention pass (Shorts, 25 s target)

```
save_history_checkpoint { label: "before retention pass" }
list_layers                                                       // video_… is the talking head
auto_remove_silence { layerId: "video_…", thresholdDb: -40, minSilenceMs: 450, paddingMs: 80 }
list_layers                                                       // re-read: segments are new ids with new startTimes
add_text_layer { text: "Stop exporting at 480p", fontSize: 60, fontWeight: "800", textColor: "#FFFFFF", fontFamily: "din-condensed", y: 17, startTime: 0, duration: 2.2, transitionIn: "slideUp", transitionInDuration: 0.25, textStrokeColor: "#000000", textStrokeWidth: 3 }
keyframe_add { layerId: "video_…seg2", property: "transform.scale", timeMs: 5200, value: 1.1, interp: { type: "hold" } }
keyframe_add { layerId: "video_…seg3", property: "transform.scale", timeMs: 10800, value: 1.0, interp: { type: "hold" } }
describe_canvas { timeSec: 0.4 }
preview_filmstrip { fromSec: 0, toSec: 25, frames: 10 }
```

Captions for the muted majority come next from expocut-kinetic-captions. Keyframe times are
timeline milliseconds, so use each segment's own startTime (from `list_layers`, in seconds, times 1000).

### 2. Twelve-second loop reel (Reels)

```
get_canvas_info
trim_layer { layerId: "video_…open", mediaOffsetSec: 1.4, durationSec: 4 }      // start on the action
trim_layer { layerId: "video_…close", durationSec: 3.2 }                        // end on a frame that matches the opener
set_layer_transition { layerId: "video_…mid", in: { id: "whippan", durationSec: 0.3 } }
add_text_layer { text: "Send this to your co-founder", fontSize: 56, fontWeight: "700", textColor: "#FFFFFF", y: 20, startTime: 0, duration: 3, transitionIn: "fadeIn", transitionInDuration: 0.2 }
render_still { timeSec: 0.3, format: "png" }                                     // cover
preview_filmstrip { fromSec: 0, toSec: 12, frames: 8 }
```

End mid-motion; do not fade to black. The last frame and the first frame should read as one shot.

## Pitfalls

- `keyframe_add` takes milliseconds on the project timeline. Seconds in `timeMs` place every
  key inside the first few milliseconds and the punch-in never shows.
- `interp` is the curve leaving that keyframe. A hold on the 1.1 key keeps the punch until the
  next key; a linear (default) 1.1 key ramps into whatever follows.
- `auto_remove_silence` replaces the layer with trimmed segments; re-run `list_layers` before
  touching ids, and take a checkpoint first.
- `add_text_layer` ignores `x` while `fullWidth` is true (the default). Use `y` for the safe zone
  and `textAlign` for horizontal placement; `verticalAnchor` and `y` are alternatives, not a pair.
- `preview_filmstrip` and `capture_canvas` need the editor on screen; `describe_canvas` does not.
- Safe-zone percentages assume a 9:16 canvas; for 1:1 or 16:9 keep text inside the middle 80
  percent and re-check with `describe_canvas`.
- Cut-level transitions between two clips use `set_junction_transition`, whose ids differ from
  `list_transitions`; leave those to expocut-social-speed-edit. `set_layer_transition` on the
  incoming layer is the executable shortcut used above.

## Reference

- Executing skills: expocut-video-creating, expocut-social-speed-edit, expocut-audio-post,
  expocut-kinetic-captions, expocut-motion-graphics, expocut-editor-ops.
- Full tool list and conventions: https://expocut.com/mcp.html


---

## 📄 SOURCE FILE: `plugins/expocut/skills/expocut-retention-playbook/references/tools.md` (verbatim)

# Tool signatures used by expocut-retention-playbook

<!-- generated from the live MCP registry by apps/mobile/src/mcp/__tests__/skillsParity.test.ts; do not edit by hand -->

Exact names, parameters and enums of every tool this skill mentions. `*` marks a required parameter.
Time arguments named startTime / duration / *Sec are seconds; keyframe timeMs is milliseconds.

## add_stock_music_layer

Download a Freesound clip and add it as an audio layer in the active project. Pass either soundId (recommended — picks the best preview MP3) or a direct preview url. Layer duration defaults to the full clip length reported by Freesound. Uses preview-hq-mp3 (no OAuth required); original-quality download needs OAuth2 which the app does not configure.

| param | type | notes |
| --- | --- | --- |
| soundId | number |  |
| url | string |  |
| startTime | number |  |
| duration | number |  |
| volume | number | 0..1 layer volume |
| fadeInMs | number |  |
| fadeOutMs | number |  |

## add_text_layer

Add a text layer. Defaults to fullWidth=true + textAlign="center" so the text auto-fits the canvas regardless of aspect ratio (9:16, 16:9, 1:1) — perfect for title cards. x/y are the TOP-LEFT corner of the text block in canvas % (fullWidth pins x=0). Use verticalAnchor="top|center|bottom" instead of computing y: it places the block top at 12 %, the glyph centre at 50 %, or the block bottom at 88 % on any aspect. startTime/duration are seconds. Use transitionIn/Out (e.g. "fade", "scale") for entrance/exit animations.

| param | type | notes |
| --- | --- | --- |
| text\* | string |  |
| fontSize | number |  |
| fontFamily | string |  |
| fontWeight | string | e.g. "400", "700", "bold" |
| fontItalic | boolean |  |
| textColor | string | #RRGGBB |
| textAlign | string | one of: `left`, `center`, `right`, `justify` |
| fullWidth | boolean | Default true. Layer spans full canvas width; textAlign places the glyphs. |
| verticalAnchor | string | one of: `top`, `center`, `bottom` — Convenience for y. Use this OR y, not both. |
| x | number | Top-left x percent 0..100. Ignored when fullWidth=true. |
| y | number | Top-left y percent 0..100. |
| scale | number |  |
| rotation | number | degrees |
| opacity | number | 0..1 |
| letterSpacing | number | pt tracking; 2–3 for luxe caps labels |
| textTransform | string | one of: `none`, `uppercase`, `lowercase`, `capitalize` |
| lineHeight | number | multiplier, e.g. 1.2 |
| startTime | number | seconds |
| duration | number | seconds |
| fadeInMs | number |  |
| fadeOutMs | number |  |
| transitionIn | string |  |
| transitionOut | string |  |
| transitionInDuration | number | seconds |
| transitionOutDuration | number | seconds |
| textShadowColor | string |  |
| textShadowBlur | number |  |
| textStrokeColor | string |  |
| textStrokeWidth | number |  |
| textAutoFit | object | Shrink-to-fit. Resolver picks the largest fontSize ≤ maxSize that fits the text within maxLines lines, never below minSize. |

## auto_remove_silence

Auto-edit: detect and ripple-delete the silent gaps in a video/audio clip, closing the timeline so the result is one tight cut. Non-destructive to the media file (rebuilds the timeline layer into trimmed segments). thresholdDb (default -40), minSilenceMs (shortest gap to cut, default 500), paddingMs (silence kept around speech, default 80).

| param | type | notes |
| --- | --- | --- |
| layerId\* | string |  |
| thresholdDb | number |  |
| minSilenceMs | number |  |
| paddingMs | number |  |

## beat_cut_from_drums

Detect onsets on the isolated DRUM stem and return cut times (ms) to place cuts/transitions. Requires the clip to be separated first.

| param | type | notes |
| --- | --- | --- |
| sourceLayerId\* | string |  |
| sensitivity | number | Higher = fewer cuts. Default 1.5. |
| maxCuts | number | Cap to the N strongest cuts. |

## capture_canvas

Capture the editor canvas to a PNG (or JPG) at a given frame and return it as an MCP image block, so you can SEE the project state — layer placement, colors, overlap, final composition. The leading text block is SELF-DESCRIBING for debugging: it reports the captured time, project canvas size (aspectRatio + resolution), total length, layer/track counts, and — most useful — the list of layers actually VISIBLE at that frame (sorted top-most first, each with its computed bounding box in canvas %), so an empty/wrong frame is immediately explainable. DEBUG VIEWS: xray=true dims the composition and draws labeled layer bounding boxes on top; outlinesOnly=true hides content entirely (borders only); grid=true overlays a 10%-step coordinate grid with % labels to pin-point positions — all composable with timeSec. Requires the editor mounted on the active project (Library → tap the project). timeSec scrubs the playhead first; maxWidth defaults to 512 (cap 1024). ANDROID CAVEAT: this capture is a software view-snapshot, which does NOT include camera-based 3D — a layer with rotationX/rotationY renders FLAT here even though the real screen and the export both show the tilt. When that applies to the frame you asked for, the result carries a `warnings` entry naming the affected layers; use capture_export_frame to see the tilt. Do not read a flat capture as a tilt bug on Android.

| param | type | notes |
| --- | --- | --- |
| timeSec | number |  |
| maxWidth | number |  |
| format | string | one of: `png`, `jpg` |
| quality | number |  |
| xray | boolean |  |
| outlinesOnly | boolean |  |
| grid | boolean |  |

## describe_canvas

Describe — as structured TEXT, no image — exactly what is composited at a given frame. Returns, for the requested time (default = current playhead): every VISIBLE layer sorted top-most first, each with its resolved bounding box in canvas % (x/y/w/h, top-left anchored; approx=true when the size is estimated), paint order (lower trackIndex paints on top), opacity and type; plus how many layers are hidden, scheduled outside this frame, or non-visual (audio never paints and is never listed). This is the cheap, mount-free companion to capture_canvas — use it to reason about layout, overlap and z-order without spending an image. timeSec scrubs the described frame only.

| param | type | notes |
| --- | --- | --- |
| timeSec | number |  |

## get_active_project

Return the currently-open project id, layer count, and export settings.

No parameters.

## get_canvas_info

Return the canvas/preview context in one cheap call (no image, editor need not be mounted): aspectRatio + numeric aspect, pixel width/height (from the stored resolution, else the 1080p preset — resolutionAssumed=true), the editor canvas size in points, layerBaseWidthPct / layerBaseHeightPct (how big an unsized layer lands, as % of the canvas), fps, format, quality, total duration (ms + sec), estimated frame count, layer/track counts, current playhead, isPlaying and the selected layer id. Use this to understand the frame size, the default layer size and the timeline length before placing layers or capturing.

No parameters.

## keyframe_add

Add or replace a scalar keyframe on a layer. Accepts image, text, shape, and video layers for the common transform/opacity/fx/border/mask/color surface. Call list_keyframe_properties to see the full property catalog and which layer types each applies to. The easing curve (interp) is optional; default is linear.

| param | type | notes |
| --- | --- | --- |
| layerId\* | string |  |
| property\* | string | one of: `transform.x`, `transform.y`, `transform.scale`, `transform.scaleX`, `transform.scaleY`, `transform.rotation`, `transform.rotationX`, `transform.rotationY`, `transform.anchorX`, `transform.anchorY`, `opacity`, `color.hueShift`, `color.saturation`, `color.brightness`, `color.contrast`, `color.intensity`, `fx.blur`, `fx.intensity`, `mask.rect.x`, `mask.rect.y`, `mask.rect.width`, `mask.rect.height`, `mask.feather`, `mask.expansion`, `mask.rotation`, `mask.bandWidth`, `mask.gradientSoftness`, `secondaryEffect.intensity`, `audio.volume`, `filter.id`, `filter.intensity`, `transition.inIntensity`, `transition.outIntensity`, `border.width`, `border.glowIntensity`, `border.cornerRadius`, `text.color.r`, `text.color.g`, `text.color.b`, `text.stroke.color.r`, `text.stroke.color.g`, `text.stroke.color.b`, `text.stroke.width`, `border.color.r`, `border.color.g`, `border.color.b`, `x`, `y`, `scale`, `scaleX`, `scaleY`, `rotation`, `rotationX`, `rotationY`, `anchorX`, `anchorY` — Animatable scalar property. Full dot-path (transform.scale) or shorthand (scale) accepted. |
| timeMs\* | number | Time on the timeline in milliseconds. |
| value\* | number | Numeric value at this keyframe. |
| interp | object | Easing leaving this keyframe. Shape: { type: "hold" \| "linear" } \| { type: "bezier", x1, y1, x2, y2 } \| { type: "preset", name: "ease" \| "easeIn" \| "easeOut" \| "easeInOut" \| "bounce" \| "elastic" \| "spring" }. Default linear. |

## keyframe_clear

Clear all keyframes on a layer. Pass a property to clear only that track. This is the "remove animation" path — equivalent to the editor's Reset button.

| param | type | notes |
| --- | --- | --- |
| layerId\* | string |  |
| property | string |  |

## list_layers

List all layers in the active project. Returns a compact summary per layer.

No parameters.

## list_transitions

List all entrance/exit transitions (fadeIn, slideUp, lightCinematic, …). Use the returned id at creation time with add_text_layer / add_shape_layer transitionIn or transitionOut, or on an existing layer with set_layer_transition. Shader-category ids are cover-and-reveal GPU transitions. Durations are in seconds.

No parameters.

## preview_filmstrip

Capture a STRIP of evenly-spaced frames across a time range and return them as labeled MCP image blocks — so you can SEE motion, a transition or pacing instead of one still. Args: fromSec (default 0), toSec (default project end), frames (1..12, default 6), maxWidth (64..512, default 320), format ("jpg" default / "png"), quality. The leading text block lists each frame index and time. Requires the editor mounted on the active project (same as capture_canvas). For a single high-detail frame use capture_canvas instead.

| param | type | notes |
| --- | --- | --- |
| fromSec | number |  |
| toSec | number |  |
| frames | number |  |
| maxWidth | number |  |
| format | string | one of: `png`, `jpg` |
| quality | number |  |

## render_still

Render the current frame to an image FILE on disk and return its file:// uri (plus width/height/atMs). Unlike capture_canvas (which returns an inline preview image for you to look at), this writes a reusable file — e.g. a poster/thumbnail, or a frame to re-import with add_image_layer. timeSec scrubs the playhead first; maxWidth defaults to the canvas pixel width (cap 2160). Requires the editor mounted on the active project.

| param | type | notes |
| --- | --- | --- |
| timeSec | number |  |
| maxWidth | number |  |
| format | string | one of: `png`, `jpg` |
| quality | number |  |

## save_history_checkpoint

Push a session-scoped checkpoint of the editor state onto the undo stack. Returns the checkpoint id. Use undo() to revert to the previous checkpoint or undo_to_checkpoint({id}) for direct jump.

| param | type | notes |
| --- | --- | --- |
| label | string |  |

## set_junction_transition

Put a transition on the CUT between two adjacent clips (the joiner), or change the one already there. Address the cut by the pair of layers that meet at it — call list_junctions first to find them. effectId comes from list_transitions (e.g. wipe.iris, slide.push-left, distort.warp, dissolve.cross). durationSec is clamped to what the cut can actually hold at the chosen alignment. params carries the family options, and is the ONLY route to several of them: wipe.iris takes originX / originY (0..1, where the circle grows from; 0.5/0.5 = centre) and bulge (0..1 rim refraction — a water-droplet lens riding the advancing edge); the distort family takes blur, blurAniso (0 = even blur, 1 = a directional streak), blurAngle (degrees) and blurStreak; wipes take angle / softness / borderWidth; dissolve.film takes gamma. Unknown params are ignored, out-of-range values are clamped.

| param | type | notes |
| --- | --- | --- |
| fromLayerId\* | string | Outgoing clip — the one that ends at the cut. |
| toLayerId\* | string | Incoming clip — the one that starts at the cut. |
| effectId\* | string | Transition id from list_transitions. |
| durationSec | number | Clamped to the cut's capacity. Default 1s. |
| alignment | string | one of: `center`, `start`, `end` |
| ease | string | one of: `none`, `in`, `out`, `inOut`, `custom` |
| reverse | boolean | Play the effect backwards. |
| endRatio | number | Progress reached on the final frame, 0..1. Below 1 the incoming clip never fully resolves. |
| params | object | Family options — see the description. |

## set_layer_transition

Set or change the entrance (in) / exit (out) transition on an EXISTING layer. Each role takes a transition id from list_transitions plus optional durationSec/easing/intensity/blur. Classic and Shader-category ids are mutually exclusive per role — picking one clears the other automatically. For Shader-category ids (liquidwipe, slicewipe, …) you can also "Customize" the look via preset (a named preset like "Pink Boards" / "Cyan Shards") and shaderParams (fxParams such as fillColors / angle / transparentBg / revealOnly / useTexture — see get_effect_schema). Pass {id:null} (or "none") to clear a role. Provide at least one of in/out.

| param | type | notes |
| --- | --- | --- |
| layerId\* | string |  |
| in | object |  |
| out | object |  |

## split_layer

Cut a layer into two halves at atSec (relative to the layer's startTime). The first half keeps the original id; the second half is a fresh layer with its mediaOffset advanced by atSec so it continues playing the source seamlessly. Both halves keep all styling, effects, color settings.

| param | type | notes |
| --- | --- | --- |
| layerId\* | string |  |
| atSec\* | number |  |

## stock_search_music

Search Freesound for music / audio clips. Returns id, name, username, duration (seconds), tags, waveform url, and a preview url for each result. Use the returned id with add_stock_music_layer to drop the sound onto the timeline. category buckets: music | sfx | ambient | vocals | nature | electronic | cinematic | all. minDuration / maxDuration are post-filtered client-side. Default sort downloads_desc (most popular first).

| param | type | notes |
| --- | --- | --- |
| query | string |  |
| category | string | one of: `all`, `music`, `sfx`, `ambient`, `vocals`, `nature`, `electronic`, `cinematic` |
| page | number |  |
| perPage | number | Default 15 |
| sort | string | one of: `score`, `duration_desc`, `duration_asc`, `created_desc`, `created_asc`, `downloads_desc`, `downloads_asc`, `rating_desc`, `rating_asc` |
| minDuration | number | seconds |
| maxDuration | number | seconds |

## trim_layer

Trim a video/audio (or any) layer. mediaOffsetSec moves the in-point into the source media; durationSec sets how long the clip plays for on the timeline; startTimeSec moves where on the timeline the clip starts. Pass any subset — omitted fields stay put.

| param | type | notes |
| --- | --- | --- |
| layerId\* | string |  |
| mediaOffsetSec | number |  |
| durationSec | number |  |
| startTimeSec | number |  |

## undo_to_checkpoint

Jump directly to a specific checkpoint by id.

| param | type | notes |
| --- | --- | --- |
| id\* | string |  |

## update_layer

Merge a partial patch into the layer with the given id. Use this for tweaks like changing position, opacity, scale, fontSize, transitionIn etc. without rebuilding the layer. rotationX / rotationY tilt the layer out of plane in degrees (0 = flat, clamped to ±75) — that is the card-in-3D-space move; plain `rotation` remains the in-plane spin. Supported on every visual layer type that can rotate at all — image, video, base video, text, shape, shape-widget, collage and Lottie — on canvas and at export. Android adds transcript and lower-third; on iOS those two carry no layer rotation in the encoder at all, so they stay flat there.

| param | type | notes |
| --- | --- | --- |
| id\* | string |  |
| patch\* | object |  |

## update_text

Edit the core properties of an EXISTING text layer (the Edit Text ▸ Text tab): text content, fontSize (pt), lineHeight (multiplier), fontWeight ("400"/"700"/"bold"), fontItalic, textTransform (none/uppercase/lowercase/capitalize = the Abc/ABC/abc case toggles), textAlign (left/center/right/justify), letterSpacing (pt), textColor (#RRGGBB), opacity (0..1). Only the fields you pass change. For the one-tap look presets use set_text_style; for the font use set_text_font.

| param | type | notes |
| --- | --- | --- |
| layerId\* | string |  |
| text | string |  |
| fontSize | number |  |
| lineHeight | number |  |
| fontWeight | string | e.g. "400", "700", "bold" |
| fontItalic | boolean |  |
| textTransform | string | one of: `none`, `uppercase`, `lowercase`, `capitalize` |
| textAlign | string | one of: `left`, `center`, `right`, `justify` |
| letterSpacing | number |  |
| textColor | string | #RRGGBB |
| opacity | number | 0..1 |
