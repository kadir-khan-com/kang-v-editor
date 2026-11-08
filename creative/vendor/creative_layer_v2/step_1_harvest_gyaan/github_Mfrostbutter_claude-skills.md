# Mfrostbutter/claude-skills — After Effects ExtendScript skill (from a personal skills collection)
- Repo: Mfrostbutter/claude-skills
- Link: https://github.com/Mfrostbutter/claude-skills
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 1 star, 38 commits (repo page, 2026-11-06)
- Last commit (from local clone git log): 2026-10-29
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Personal multi-topic skills collection; extracted here is ONLY skills/after-effects-extendscript/ — SKILL.md (ES3 rules, matchName cheatsheet, sourceRectAtTime pattern, typing/blink expressions), reference/audio-sync.md (ffmpeg silencedetect audio-sync recipe) and assets/helpers.jsx (helper library that ships with the skill). All other skills in the repo (langgraph, figma, n8n, video-walkthrough etc.) are out of scope.

---

## 📄 SOURCE FILE: `skills/after-effects-extendscript/SKILL.md` (verbatim)

---
name: after-effects-extendscript
description: >-
  Build and edit After Effects motion graphics from scratch with ExtendScript
  (.jsx) — comps, text, typing-on effects, expression-driven tracking, keyframes
  with easy-ease, shape/polystar elements (sparkles, glints), and timed audio.
  Use whenever the task is to author or change an AE script, build a title /
  splash / lower-third / logo animation, sync animation to a sound effect, or
  drive layers by expression. Encodes the hard-won rules: ExtendScript is ES3
  (no const/let/arrow/template-literals), the property matchname cheatsheet, the
  sourceRectAtTime layout+tracking pattern, Source Text typing expressions,
  per-dimension KeyframeEase, server-side font resolution with graceful
  fallback, AE-can't-import-Opus (convert with ffmpeg), and the ffmpeg
  silencedetect → audio-sync recipe.
---

# After Effects via ExtendScript (.jsx)

After Effects is scripted with **ExtendScript** against the AE scripting DOM (`app`, `comp`, layers, properties). A `.jsx` builds a comp deterministically and is fully parameterized — the right tool for repeatable, brand-locked motion (intros, titles, logo animations) where you want a `CONFIG` block instead of hand-keyframing.

There is **no AE MCP**. You write the script; the user runs it in AE and renders/previews to verify. Treat the render (a frame or clip the user shares) as the feedback loop — build, ask for a render, read it, fix, repeat. There is also no automated screenshot; favor a `CONFIG` block + an end-of-run `alert()` summary so the user can self-tune.

## Run + verify model

- Run: AE → `File > Scripts > Run Script File...` → pick the `.jsx`. No project/comp setup needed if the script builds its own.
- Syntax-check locally before handing off: `node` rejects the `.jsx` extension, so `cp script.jsx _check.js && node --check _check.js && rm _check.js`. This catches parse errors; it does NOT validate AE DOM calls.
- Headless render (optional): `aerender` CLI can render a comp for an automated check, but it needs AE installed and is heavy — default to the user previewing.

## ExtendScript is ES3 — write accordingly

- `var` only. **No** `const`/`let`, arrow functions, template literals, destructuring, or `for...of`. Use function declarations, `for` loops, and string concatenation. `===`, `try/catch`, `Array.push` are fine; avoid `Array.forEach`/`map` (spotty).
- Wrap mutations in `app.beginUndoGroup("...")` / `app.endUndoGroup()`, and the whole body in `try/catch` ending with an `alert()` so failures surface.
- Build expression strings by concatenation and inject CONFIG numbers/strings at build time (expressions can't read your CONFIG). Escape injected strings (`'"' + s.replace(/"/g,'\\"') + '"'`). Newlines in expression source: `\r`.

## Core principles

1. **Anchor at the origin, then measure.** For text layout set `Anchor Point = [0,0]` (baseline-left), then `layer.sourceRectAtTime(0, false)` → `{left, top, width, height}` relative to that anchor. Left-edge placement: `position.x = desiredLeft - rect.left`; baseline `position.y = baselineY`. Vertical-center off the tallest glyph: `baselineY = compH/2 - (rect.top + rect.height/2)`. The same `sourceRectAtTime` convention holds in expressions, so build-time layout and expression-time tracking agree.
2. **Prefer expressions over keyframes for anything derived.** Typing-on, edge-tracking, blinking — all are one expression and need no rebuild when strings change.
3. **CONFIG at the top.** Every tunable (strings, fonts, colors as hex, sizes, timings) in one object. Colors: store hex, convert to 0–1 RGB. This is what makes the script reusable and brand-switchable.
4. **Verify state before reading children.** `app.project` always exists. For multi-page/precomp work, set the active item before reading its layers.

## Property matchname cheatsheet

Use matchnames (stable across locales), not display names:

- Transform: `ADBE Transform Group` → `ADBE Anchor Point`, `ADBE Position`, `ADBE Scale`, `ADBE Rotate Z` (2D rotation), `ADBE Opacity`.
- Text source: `layer.property("ADBE Text Properties").property("ADBE Text Document")` — `.value` is a `TextDocument`; mutate it then `setValue(doc)`. Put a typing expression on this property's `.expression`.
- Shape layer: `ADBE Root Vectors Group` → `addProperty("ADBE Vector Group")` → `.property("ADBE Vectors Group")` → `addProperty("ADBE Vector Shape - Star")` (or `...- Rect`, `...- Ellipse`) + `addProperty("ADBE Vector Graphic - Fill")`. Fill color via `.property("ADBE Vector Fill Color").setValue([r,g,b,1])`.
- Polystar: `ADBE Vector Star Type` (1 = star, 2 = polygon), `ADBE Vector Star Points`, `ADBE Vector Star Outer Radius`, `ADBE Vector Star Inner Radius`, and the **misspelled** `ADBE Vector Star Outer Roundess` / `ADBE Vector Star Inner Roundess` (wrap in try/catch). A 4-point star with inner radius ≈ 0.16×outer = a sparkle/glint.

## TextDocument gotchas

- Set `applyFill=true` + `fillColor=[r,g,b]`, `applyStroke=false`, `justification` (use `ParagraphJustification.LEFT_JUSTIFY` for left-anchored growth), then `text`, then `setValue(doc)`.
- AE style names use spaces: `"Semi Bold"`, `"Extra Bold"` — not `"SemiBold"`.

## Fonts: PostScript names + graceful fallback

`TextDocument.font` wants a **PostScript name**, not a family name. Resolve family→PS via `app.fonts.getFontsByFamilyNameAndStyleName(family, style)` or by scanning `app.fonts.allFonts` when that API exists; otherwise trust your first guess (AE substitutes a missing font rather than erroring). Pattern: `resolvePS(family, style, guessList, fallbackPS)` returning a PS name; fallbacks like `Consolas` (mono) / `ArialMT` (sans). See `assets/helpers.jsx`.

**AE renders only SYSTEM-installed fonts.** A brand's *web* font (e.g. one loaded via a Google Fonts `@import` in a webapp) is invisible to AE — it silently falls back (you'll see `Arial-BoldMT` in the build alert). To actually match an in-app wordmark, install the font on the OS first. Windows per-user install (no admin), then **restart AE**: copy the static `.ttf`s to `%LOCALAPPDATA%\Microsoft\Windows\Fonts` and add `HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts` values like `"Inter Bold (TrueType)"` = the full font path. Have the script's alert print the resolved PS name and warn if the family didn't resolve, so a silent substitution is caught.

## Keyframes + easy-ease

Set values with `prop.setValueAtTime(t, v)`, then per key: `setInterpolationTypeAtKey(i, BEZIER, BEZIER)` and `setTemporalEaseAtKey(i, easeIn, easeOut)` where each ease array has **one `new KeyframeEase(0, 33)` per value dimension** — 1 for opacity/rotation, 2 for `Scale [x,y]`. **Exception: spatial properties (Position) take a SINGLE element regardless of dimensionality** — passing 2 to a keyframed Position throws `Unable to call "setTemporalEaseAtKey" ... Value array does not have 1 elements`. Gate on `prop.isSpatial` (use 1) vs `prop.value.length`. Wrong length throws. `easeAll(prop)` in `assets/helpers.jsx` handles this.

## Patterns

- **Typing-on:** Source Text expression `n=(time<ts)?0:Math.floor((time-ts)/iv)+1; s.substr(0,n)`. Measure the full string first for layout, then apply the expression.
- **Edge tracking:** drive a follower's `position.x` off the typed layer's `sourceRectAtTime` so a closing bracket / caret tracks the growing text. See `reference/audio-sync.md` and `assets/helpers.jsx` (`edgeTrackExpr`).
- **Blink:** opacity expression gated to a window: `(time<ts||time>te)?0:(Math.floor((time-ts)*hz*2)%2===0?100:0)`.
- **Sparkle/glint:** a polystar that scales `0→peak→0`, slow-rotates, and flashes opacity, timed to a beat (e.g. a ding). `makeSparkle` + `animSparkle` in helpers.
- **Audio sync:** see **`reference/audio-sync.md`** — convert non-WAV with ffmpeg, extract onsets with `silencedetect`, import + `layer.startTime`, lock the typing interval to the recording.

## Portability + render

- Resolve bundled assets relative to the script: `(new File($.fileName)).parent.fsName + "/sfx/"`. Bundle SFX/images next to the `.jsx`.
- Transparent background = **no solid layer** (comps are transparent by default). Render with an alpha codec (ProRes 4444 / PNG sequence) and **Audio Output On**.

## Committing AE scripts (secret scanners)

High-entropy asset filename literals (e.g. `keystrokes-14.wav`) inside a `.jsx` can trip a secret scanner's `generic-api-key` rule. Path-allowlist the script in your scanner config rather than renaming the asset.

## Keep a canonical example

Maintain one CONFIG-driven reference script in your repo and point new work at it. A good intro/splash reference exercises the whole toolkit in one file: transparent 1920×1080 / 30fps, a two-tone-capable wordmark, expression typing + an edge-tracked bracket + a blinking caret, timed keystroke/enter/ding SFX locked to the typing, and a polystar sparkle on the ding. When the code and this skill disagree, the code wins — update the skill.

---

## 📄 SOURCE FILE: `skills/after-effects-extendscript/reference/audio-sync.md` (verbatim)

# Syncing AE animation to a sound effect

The goal: visuals land exactly on the audio transients (e.g. one keystroke per typed character, a sparkle on a ding).

## Sourcing SFX on demand (ElevenLabs)

When there is no recording to use, generate the effect from the ElevenLabs **text-to-sound-effects** API.

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/sound-generation" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"smooth cinematic UI whoosh transition, soft airy swoosh, clean modern tech","duration_seconds":1.3,"prompt_influence":0.45}' \
  -o whoosh.mp3
```

- `duration_seconds` 0.5–30; `prompt_influence` 0–1 (~0.45 follows the prompt without going harsh). Response is `audio/mpeg`. On error the body is JSON, not audio — `head -c 4 file | grep '{'` to detect.
- AE imports MP3, but convert to WAV to keep the pipeline uniform and loudness-matched: `ffmpeg -i whoosh.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 whoosh.wav`.
- Prompt patterns that land: transitions → "smooth/fast digital swoosh transition, airy, crisp, futuristic"; confirmations → "clean soft UI chime, single bright digital bell, premium tech, short". Keep prompts short and concrete.
- Generate **2–3 variants per slot** (vary the prompt), audition, wire the winner, keep the rest in `sfx/options/`. Same `duration_seconds` yields the same MP3 byte size for different takes — that is NOT a duplicate; confirm with `md5sum`.
- **The API key is a secret.** Read `ELEVENLABS_API_KEY` from your environment or a secrets manager; never write it to a tracked file, and scrub any temp copy after use.

## 1. Make it importable

After Effects imports **WAV / AIFF / MP3 / AAC (m4a)**. It does **not** import Opus (`.opus`) or FLAC. Convert first:

```bash
ffmpeg -i in.opus -ar 48000 -ac 2 -c:a pcm_s16le out.wav
```

## 2. Find the transient onsets

Each `silence_end` reported by `silencedetect` is the start of a sound (a keystroke, a hit, a ding):

```bash
ffmpeg -hide_banner -nostats -i sound.wav \
  -af "silencedetect=noise=-38dB:d=0.035" -f null - 2>&1 | grep silence_
```

- Lower `noise` (e.g. `-45dB`) to catch quieter hits; raise it to ignore room noise.
- Lower `d` (min silence, e.g. `0.02`) to split fast adjacent hits; raise it to merge.
- A long `silence_end → next silence_start` span is a sustained sound (a ding/bell), not a click.

Record the in-file onset of each event you'll align to (first hit, last hit, enter, ding) — these become CONFIG constants.

## 3. Import + place in the script

```javascript
function importAudio(path) {
  var f = new File(path);
  if (!f.exists) return null;
  try { return app.project.importFile(new ImportOptions(f)); } catch (e) { return null; }
}
var item = importAudio(dir + "sound.wav");
if (item) {
  var L = comp.layers.add(item);   // audio-only footage adds as an AV layer
  L.name = "sfx";
  L.startTime = eventTime - onsetInFile;   // shift so the in-file onset lands on eventTime
}
```

`layer.startTime` shifts the whole clip; a negative value is allowed (only the part inside the comp plays).

## 4. Lock the animation to the recording

When the visual cadence should match the audio (e.g. one keystroke per typed character):

- Align the first transient to the first visual event: `startTime = typeStart - firstHitInFile`.
- Derive the per-step interval from the recording instead of guessing:
  `typeInterval = (lastHitInFile - firstHitInFile) / (stepCount - 1)`.
- With the `+1` reveal (`n = floor((t-ts)/iv)+1`), step _i_ shows at `ts + (i-1)*iv`, so the first and last steps line up with the first and last transients and the interior drift is imperceptible across a fast burst.

This couples the take to the step count: a keystroke recording with 14 hits matches a 14-character string. If the string length changes, re-record or disable the lock.

## 5. Place dependent beats by their in-file offset

A second sound's later transient is positioned relative to where you anchored it:

```
enter stroke aligned to the "]" pop  =>  startTime = popTime - enterHitInFile
ding rings at                            dingTime = popTime - enterHitInFile + dingInFile
```

Use `dingTime` to trigger a visual (a sparkle, a flash) exactly on the ding.

## 6. Render

Enable **Audio Output On** in Output Module settings, or the rendered file is silent. For a transparent background use an alpha codec (ProRes 4444 / PNG sequence) — audio still muxes into ProRes; for a PNG sequence render audio separately or use a movie format.

---

## 📄 SOURCE FILE: `skills/after-effects-extendscript/assets/helpers.jsx` (verbatim)

/* after-effects-extendscript · reusable helper block.
 * Paste the helpers you need into your script. ExtendScript is ES3:
 * var only, no const/let/arrow/template-literals. Every helper takes an
 * explicit parent/comp so it works inside any comp.
 */

// ---- color ----
function hexToRgb(hex) {
  hex = String(hex).replace(/^#/, "");
  if (hex.length === 3) hex = hex.charAt(0)+hex.charAt(0)+hex.charAt(1)+hex.charAt(1)+hex.charAt(2)+hex.charAt(2);
  return [parseInt(hex.substr(0,2),16)/255, parseInt(hex.substr(2,2),16)/255, parseInt(hex.substr(4,2),16)/255];
}

// ---- expression-string quoting (inject a JS string literal into an expression) ----
function q(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"'; }

// ---- font resolve: family -> installed PostScript name, graceful fallback ----
// guesses = candidate PS names; fallbackPS used only if the font API is present and nothing matched.
function resolvePS(family, style, guesses, fallbackPS) {
  try {
    if (app.fonts && app.fonts.getFontsByFamilyNameAndStyleName) {
      var arr = app.fonts.getFontsByFamilyNameAndStyleName(family, style || "Regular");
      if (arr && arr.length) return arr[0].postScriptName;
    }
    if (app.fonts && app.fonts.allFonts) {
      var all = app.fonts.allFonts, i, g;
      for (i = 0; i < all.length; i++) { if (all[i].familyName === family) return all[i].postScriptName; }
      for (g = 0; g < guesses.length; g++) {
        for (i = 0; i < all.length; i++) { if (all[i].postScriptName === guesses[g]) return guesses[g]; }
      }
      return fallbackPS;
    }
  } catch (e) {}
  return guesses[0];   // no font API: trust the primary guess (AE substitutes if missing)
}

// ---- point text, styled, anchored at baseline-left origin [0,0] ----
function makeText(comp, name, str, fontPS, size, rgb) {
  var layer = comp.layers.addText(str);
  layer.name = name;
  var td = layer.property("ADBE Text Properties").property("ADBE Text Document");
  var doc = td.value;
  doc.fontSize = size;
  try { doc.font = fontPS; } catch (e) {}
  doc.applyFill = true; doc.fillColor = rgb; doc.applyStroke = false;
  doc.justification = ParagraphJustification.LEFT_JUSTIFY;
  doc.text = str;
  td.setValue(doc);
  layer.property("ADBE Transform Group").property("ADBE Anchor Point").setValue([0, 0]);
  return layer;
}

// rect relative to the anchor (set anchor [0,0] first); left edge in comp = position.x + rect.left
function rectOf(layer) { return layer.sourceRectAtTime(0, false); }

function setPos(layer, x, y) { layer.property("ADBE Transform Group").property("ADBE Position").setValue([x, y]); }
function opacProp(layer)    { return layer.property("ADBE Transform Group").property("ADBE Opacity"); }
function posProp(layer)     { return layer.property("ADBE Transform Group").property("ADBE Position"); }

// ---- easy-ease every key of a property (1D or multi-D) ----
function easeAll(prop) {
  // spatial props (Position) take ONE temporal-ease element regardless of
  // dimensionality; non-spatial multi-D props (Scale [x,y]) take one per dimension.
  // Passing 2 to a Position keyframe throws "Value array does not have 1 elements".
  var spatial = false; try { spatial = prop.isSpatial; } catch (e) {}
  var dim = spatial ? 1 : ((prop.value instanceof Array) ? prop.value.length : 1);
  for (var i = 1; i <= prop.numKeys; i++) {
    prop.setInterpolationTypeAtKey(i, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
    var ein = [], eout = [], d;
    for (d = 0; d < dim; d++) { ein.push(new KeyframeEase(0, 33)); eout.push(new KeyframeEase(0, 33)); }
    prop.setTemporalEaseAtKey(i, ein, eout);
  }
}

// opacity keyframes + easy-ease. keys = [[t,val],...]
function opacityKeys(layer, keys) {
  var op = opacProp(layer), i;
  for (i = 0; i < keys.length; i++) op.setValueAtTime(keys[i][0], keys[i][1]);
  easeAll(op);
}

// ---- typing-on Source Text expression (apply AFTER measuring full text for layout) ----
// reveal +1 form: char i shows at ts+(i-1)*iv
function typingExpr(str, typeStart, interval) {
  return 'var s = ' + q(str) + ';\r' +
         'var ts = ' + typeStart + ';\r' +
         'var iv = ' + interval + ';\r' +
         'var n = (time < ts) ? 0 : Math.floor((time - ts) / iv) + 1;\r' +
         'if (n < 0) n = 0;\r' +
         'if (n > s.length) n = s.length;\r' +
         's.substr(0, n);';
}

// ---- track a follower's x to the right edge of another text layer (gap px) ----
function edgeTrackExpr(targetLayerName, gap) {
  return 'var W = thisComp.layer(' + q(targetLayerName) + ');\r' +
         'var wr = W.sourceRectAtTime(time, false);\r' +
         'var sr = sourceRectAtTime(time, false);\r' +
         'var x = W.position[0] + wr.left + wr.width + ' + gap + ' - sr.left;\r' +
         '[x, value[1]];';
}

// ---- 4-point sparkle (polystar) centered at (cx,cy) ----
function makeSparkle(comp, name, cx, cy, outerR, rgb) {
  var s = comp.layers.addShape(); s.name = name;
  var gc = s.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group").property("ADBE Vectors Group");
  var star = gc.addProperty("ADBE Vector Shape - Star");
  star.property("ADBE Vector Star Type").setValue(1);
  star.property("ADBE Vector Star Points").setValue(4);
  star.property("ADBE Vector Star Outer Radius").setValue(outerR);
  star.property("ADBE Vector Star Inner Radius").setValue(outerR * 0.16);
  try { star.property("ADBE Vector Star Outer Roundess").setValue(0); } catch (e) {}
  try { star.property("ADBE Vector Star Inner Roundess").setValue(0); } catch (e) {}
  gc.addProperty("ADBE Vector Graphic - Fill").property("ADBE Vector Fill Color").setValue([rgb[0], rgb[1], rgb[2], 1]);
  s.property("ADBE Transform Group").property("ADBE Anchor Point").setValue([0, 0]);
  setPos(s, cx, cy);
  return s;
}

// pop a sparkle on a beat: scale 0->peak->0, slow turn, opacity flash
function animSparkle(layer, dt, mul) {
  mul = mul || 1;
  var tg = layer.property("ADBE Transform Group");
  var sc = tg.property("ADBE Scale"), ro = tg.property("ADBE Rotate Z"), op = tg.property("ADBE Opacity");
  var peak = 135 * mul;
  sc.setValueAtTime(dt, [0,0]); sc.setValueAtTime(dt + 0.13, [peak, peak]); sc.setValueAtTime(dt + 0.50, [0,0]);
  ro.setValueAtTime(dt, -25);   ro.setValueAtTime(dt + 0.50, 40);
  op.setValueAtTime(dt, 0);     op.setValueAtTime(dt + 0.07, 100); op.setValueAtTime(dt + 0.45, 0);
  easeAll(sc); easeAll(ro); easeAll(op);
}

// ---- import audio/footage (returns null if missing) ----
function importAudio(path) {
  var f = new File(path);
  if (!f.exists) return null;
  try { return app.project.importFile(new ImportOptions(f)); } catch (e) { return null; }
}

// ---- assets next to the running script ----
function scriptDir() { try { return (new File($.fileName)).parent.fsName + "/"; } catch (e) { return ""; } }
