# Maciejdziuba/youtube-skills — After Effects Scripting skill (repo ARCHIVED)
- Repo: Maciejdziuba/youtube-skills
- Link: https://github.com/Maciejdziuba/youtube-skills
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 4 stars, 3 commits; repo is ARCHIVED on GitHub (read-only) (repo page, 2026-11-06)
- Last commit (from local clone git log): 2026-08-17
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Extracted: the after-effects-scripting/ skill — SKILL.md + references/motion-quality.md (numeric craft settings: easing, shadows, glows, motion blur) + references/api-gotchas.md (API traps, render-proof loop). The skill's helper library scripts/aelib.jsx and scripts/templates/build-template.jsx are implementations — listed here, not extracted.

---

## 📄 SOURCE FILE: `after-effects-scripting/SKILL.md` (verbatim)

---
name: after-effects-scripting
description: >-
  Drive a running After Effects instance directly from the shell to build, edit and render motion graphics — no MCP, plugin or panel required. Use whenever the user wants Claude to work inside After Effects: building animations, title sequences, logo stings, UI/product motion, data visualisations, or fixing an existing comp. Covers the osascript/ExtendScript bridge, a verified helper library, the render-proof iteration loop, After Effects API traps that cause silent failures, and the numeric craft settings (easing, shadows, glows, motion blur) that separate premium motion from amateur output. Triggers on After Effects, AE, ExtendScript, .aep, motion graphics, animation, comp, keyframes.
---

# After Effects, driven from the shell

After Effects exposes an AppleScript command, `DoScript`, that runs ExtendScript
inside the live application. That is the whole bridge. Nothing is installed, no
MCP server, no CEP panel.

```bash
osascript -e 'tell application "Adobe After Effects 2026" to DoScript "$.evalFile(\"/tmp/ae/build.jsx\")"'
```

## Before anything else

1. After Effects must be **open**, with a project.
2. `Preferences → Scripting & Expressions → Allow Scripts to Write Files and Access Network` must be **on**. Nothing works without it.
3. macOS may need Automation permission for your terminal (System Settings → Privacy & Security → Automation).
4. Confirm the bridge before building anything:

```bash
osascript -e 'tell application "Adobe After Effects 2026" to DoScript "var f=new File(\"/tmp/ae/ping.txt\"); f.open(\"w\"); f.write(\"alive \"+app.project.numItems); f.close();"'
```

Adjust the app name to the installed version. `DoScript` returning `1` instead of
`0` means AE is busy or blocked by a modal dialog — see *When it looks hung*.

## The loop — this is the skill

Never judge a change you have not looked at. The entire value of this workflow is
that you can see your own output and fix it, instead of guessing from a
description. One cycle:

1. Write `build.jsx` — idempotent: it wipes and rebuilds the comp every run.
2. Run it. Read `err.txt` and `prog.txt`.
3. Render proof frames, stitch a contact sheet, **open the image and look at it**.
4. Fix what you actually see. Repeat.

`scripts/ae-run.sh` does steps 2–3 in one command:

```bash
~/.claude/skills/after-effects-scripting/scripts/ae-run.sh /tmp/ae "MY COMP"
```

It prints `BUILD: OK` or the error with a line number, waits for AE to finish
flushing PNGs to disk, and prints the path of a timestamped contact sheet. Read
that image with your file-reading tool. Do not skip this step — every serious
mistake in a build is invisible in the code and obvious in the frame.

## Use the helper library

`scripts/aelib.jsx` wraps every match name and API trap listed below. Load it
first and you skip most of the discovery pain:

```javascript
$.evalFile("/Users/<you>/.claude/skills/after-effects-scripting/scripts/aelib.jsx");
```

`scripts/templates/build-template.jsx` is a working skeleton with the correct
order of operations. Copy it and fill in the middle.

Key calls: `AE.init(comp, logPath)`, `AE.park()` / `AE.unpark()`, `AE.wipe()`,
`AE.shape/grp/rect/ell/fill/stroke/trim`, `AE.blur/grad4/noise/fx`,
`AE.cOut/cWeight/cThru/easeKey/impact/hang/tint`, `AE.text/place/resolve`,
`AE.rig/parent/setRot/depth`, `AE.camera/poi`, `AE.order`, `AE.proofs`,
`AE.cleanup`.

## Five rules that save the most time

**Park the viewer before building.** If the comp you are scripting is open in a
viewer, AE re-renders it after every single change and a 100-layer build takes
minutes. It looks exactly like a hang. `AE.park()` opens a throwaway 64×64 comp
and drops the target to 1/8 resolution; `AE.unpark()` restores it. This one
change turned a five-minute stall into ten seconds.

**Set the layer order explicitly at the end.** AE inserts new layers next to the
current *selection*, not at the top. Creation order tells you nothing. Finish
every build with `AE.order([...names top to bottom...])`.

**Give every 3D layer its own Z.** Layers at identical Z sort unpredictably — a
background card will swallow your artwork at some times and not others. Fractions
apart is enough; `AE.depth(layers, 0, 0.1)`.

**Clean up orphaned items.** Every `addSolid` and `addNull` creates a project item
that survives deleting the layer. After thirty rebuilds a project accumulates
dozens of duplicates. Call `AE.cleanup()` at the end of every build.

**Wrap the build in try/catch and log progress.** An uncaught error pops a modal
dialog in AE, and that dialog blocks every subsequent `DoScript` call — which
reads as the bridge dying. `ae-run.sh` uses `eval()` on the file contents rather
than `$.evalFile` precisely so errors are catchable.

## When it looks hung

`DoScript` returns `1` and nothing happens. In order of likelihood:

1. **Viewer re-render** — you did not park the viewer. Wait, then park.
2. **Modal error dialog** — an earlier script threw. Dismiss it:
   `osascript -e 'tell application "Adobe After Effects 2026" to activate' -e 'delay 1' -e 'tell application "System Events" to keystroke return'`
3. **AE genuinely busy** — poll the ping until it returns `0`.

Check whether AE is computing or waiting: `top -l 2 -pid $(pgrep -x "After Effects") -stats pid,cpu,state`.

## Reading results back

ExtendScript has no `JSON`. Write results to a text file with a hand-rolled
serialiser and read it from the shell. `AE.log()` appends to a progress file — put
a marker after each section so a failure tells you where it stopped.

Two traps: concatenating an `Error` object into a string throws its own error and
masks the real one (`e.toString()` always). And `addProperty()` invalidates
property references you captured earlier — re-fetch with `AE.fx()` instead of
caching.

## Where to go next

- `references/api-gotchas.md` — the full list of match names, invalid property
  names, and API behaviours that fail silently or misleadingly. Read this before
  guessing any match name.
- `references/motion-quality.md` — the numbers that make output look expensive:
  easing influence values, layered shadow and bloom stacks, motion blur, bit
  depth, timing and stagger conventions. Read this before animating anything a
  human will judge on quality.

---

## 📄 SOURCE FILE: `after-effects-scripting/references/motion-quality.md` (verbatim)

# Making it look expensive — the numbers

Researched and then verified in production builds. These are the settings that
separate premium motion from output that reads as a default preset. Apply them by
default; deviate deliberately, not by omission.

## Easing — the single clearest tell

AE's `KeyframeEase(speed, influence)`: influence is handle **length**. High
influence flattens the curve near that key, so the property moves slowly there.

**Never put the same influence on both sides of every keyframe.** Symmetric 50/50
easing everywhere is the most recognisable amateur signature — everything floats
in and floats out with no attack.

| Feel | Curve | AE influence |
|---|---|---|
| Premium ease-out | `cubic-bezier(0.16, 1, 0.3, 1)` | key1 **out 12**, key2 **in 84** |
| Weighted in/out (hero moves) | — | key1 out 38, key2 in 78 |
| Pass-through (multi-point path) | — | first out 20, middles 54/54, last in 88 |
| Floor impact | — | **0.5 / 0.5** — zero cushioning |
| Apex / hang | — | 90 / 90 |
| Exit | `cubic-bezier(0.4, 0, 1, 1)` | accelerate away, do not float to a stop |

Exits run **0.6–0.8×** the entrance duration.

`AE.cOut()`, `AE.cWeight()`, `AE.cThru()`, `AE.impact()`, `AE.hang()` implement
these.

## Timing (30 fps — double for 60)

| Action | Frames | ms |
|---|---:|---:|
| Opacity fade | 5–8 | 150–270 |
| Small entrance | 8–12 | 250–400 |
| Object / product entrance | 12–18 | 400–600 |
| Exit | 6–10 | 200–330 |
| Scene transition | 15–24 | 500–800 |
| Hero camera move | 24–45 | 800–1500 |

**Stagger** repeated elements 2–4 frames (0.066–0.13 s). Keep stagger at 10–20%
of each element's own duration. Cap a full cascade at ~24 frames so it reads as
one event, not a queue.

**Overlap**: a child element (text inside a card) starts **2 frames** after its
container. As one element settles the next is already beginning.

**Overshoot: 1.5–3% only.** 8% reads as cheap. Damped settle 100 → 102 → 99.5 →
100 over 3/2/2 frames.

## Shadows — never one blurred ellipse

Real shadows are a tight contact component plus a broad ambient one. Stack three
at 1× / 2× / 4× blur, halving opacity each step:

| Layer | Blur | Opacity | Offset |
|---|---:|---:|---:|
| Contact | 9 | 21% | 0–3 |
| Occlusion | 22 | 11% | 3–12 |
| Ambient | 64 | 5% | 10–30 |

- Blur radius ≈ **2–3× the offset**.
- Squash vertically to **30–40%** height for a surface shadow.
- Colour: cool dark violet or neutral, **never pure black**.
- Drive opacity and blur off the object's height so the shadow opens up as it
  rises — that is what sells contact.

## Glows and bloom — never one Glow effect

AE's `ADBE Glo2` on light or pastel artwork blows it to flat white; every channel
sails past the threshold. Instead stack blurred copies of the artwork in Add mode:

| Layer | Blur | Opacity |
|---|---:|---:|
| Core | 4 | 42% |
| Mid | 22 | 17% |
| Wide | 92 | 6% |

Roughly halve opacity per doubled radius. Equal opacities produce a visible halo
ring. Keep the source crisp and blur only the duplicates. Bloom should touch
5–20% of the frame, not wash the silhouette.

**Glass and translucent panes use Screen, not Add.** Additive panes stack and
flood the frame, destroying a dark background. Glass transmits light; it does not
emit it.

## Motion blur

Comp settings: shutter angle **180°** natural, **90–120°** for crisp UI,
**200–300°** for fast sweeps. Samples **32**, adaptive limit **128**, shutter
phase **−90**.

Motion blur should be proportional to velocity — if an element moves a few pixels
per frame, turn it off. Excessive blur makes clean motion look soft, not
expensive.

## Colour and finish

- **16 bpc**, never 32 (see api-gotchas).
- Add **1.5–2% mono noise** on an adjustment layer as a finishing grain — it also
  hides residual banding.
- A subtle vignette: full-frame dark solid, inverted rounded mask, feather ~300.
- Keep backgrounds **near-black, never pure black**, with a coloured glow
  somewhere in frame.

## Camera and macro movement

- **One deliberate idea per section** — push, track, orbit or parallax. Not all
  four at once.
- Push-in **2–6% over 1–1.5 s**. Lateral drift **20–80 px over 1–2 s**.
- Long lens (**70–120 mm**) for restrained product perspective; `AE.camera(name, 85)`
  accepts millimetres.
- Rotation **0.5–2°**; reserve 3–5° for a deliberate reveal.
- Camera duration **1.5–2.5×** object duration — the camera is always the slower
  element.
- **No perpetual aimless drift.** Settle, then one purposeful slow push. A
  continuous sine on everything reads as a screensaver.

## Form and depth

- A flat gradient shape reads as a sticker. Add **form shading** inside its
  matte: a dark cool ellipse (Multiply, ~30%, large blur) at the lower right, and
  a white specular ellipse (~36%) at the upper left.
- Something should always be **slightly** out of focus — but soft-focus on
  everything is emptiness, not restraint. Keep at least one crisp element per
  frame for the eye to hold.
- Assign blur by distance from a focal plane so depth is legible.

## Composition discipline

- Never more than two things demanding attention at once.
- A lone thin bright line floating in soft light reads as a stray path, not as
  design. Either give it a form to belong to, or remove it.
- Leave real moments of near-stillness. They make the moves that follow land.

---

## 📄 SOURCE FILE: `after-effects-scripting/references/api-gotchas.md` (verbatim)

# After Effects scripting — traps that fail silently or misleadingly

Everything here was hit in real builds against After Effects 2026 on macOS.
Each one cost a broken render or a wasted cycle. Check here before guessing a
match name.

## Match names you will get wrong

| Thing | Wrong | Correct |
|---|---|---|
| Camera zoom | `ADBE Zoomval` | walk `ADBE Camera Options Group`, match `name === "Zoom"` |
| Camera point of interest | `ADBE Point of Interest` | `ADBE Anchor Point` (inside `ADBE Transform Group`) |
| Transform effect | `ADBE Transform` | `ADBE Geometry2` |
| Text animator position | `ADBE Text Position` | **rejected** — animate the layer position instead |
| Noise effect params | `Amount of Noise` | match by name prefix `"Amount"` — see `AE.noise()` |

Effect parameter match names are **not** in UI order. 4-Color Gradient's
"Positions & Colors" is `-0011` while Point 1 is `-0001`. Address effect params
by their **English name** (`e.property("Point 1")`), never by index or a guessed
suffix. To discover names, add the effect to a throwaway comp and dump
`name` / `matchName` for every child.

## Properties that do not exist where you expect

**`transform.rotation` on a 3D layer is undefined.** 3D layers have
`xRotation` / `yRotation` / `zRotation`. Use `AE.setRot()`.

**Spatial properties take exactly ONE `KeyframeEase`.** Position, Point of
Interest and Anchor Point reject a per-dimension array; Scale and Color want one
per dimension. `AE.easeKey()` tries N and falls back to 1.

**Time Remap goes hidden if you remove every key.** Add the new keys first, then
delete the stale ones, or every later `setValueAtTime` throws "property or a
parent property is hidden".

## Behaviours that silently corrupt a build

**New layers are inserted next to the selection, not at index 1.** Creation order
is meaningless. Always finish with an explicit `AE.order([...])`.

**3D layers at identical Z sort unpredictably.** The symptom is maddening: your
artwork renders correctly at one time and is invisible at another, with no
keyframe explaining it. Give each layer its own fractional Z.

**`layer.parent = x` preserves world position** and rewrites the child's position
values to compensate — so a child you just placed at `[0,0]` jumps to
`[-960,-540]`. Use `setParentWithJump()` (wrapped as `AE.parent()`) when you want
the child to keep the numbers you set.

**Parenting does not inherit opacity.** Fading a container leaves its child text
fully visible. Link the child's opacity with an expression.

**`addProperty()` invalidates earlier property references.** Capturing
`var r = rect(...)` then adding a fill to the same group makes `r` throw "Object
of type ... is invalid". Re-fetch by walking the group (`AE.fx()` does this for
effects).

**Cross-layer expressions bake in a "layer missing" error permanently** if the
referenced layer does not exist yet. Assign them in a deferred pass at the end of
the build.

**`sourceRectAtTime` returns the value at the time you ask for.** If the layer's
position is keyframed, reading `.value` gives you the pose at time 0, not the
settled one — which produces ghost duplicates offset from the original. Link with
an expression instead.

## Rendering

**`comp.saveFrameToPng` composites transparency over WHITE.** A precomp with
alpha renders as if on a white card. Always render the top-level comp for
judging.

**It returns before the bytes are on disk.** Reading immediately gives truncated
files. Wait until file sizes are stable for a few polls — `ae-run.sh` does this.
Diagnosing a "caching" problem that was really this race cost four cycles.

**Set `comp.resolutionFactor = [1,1]` for proofs** and back to `[8,8]` while
building.

**`app.purge(PurgeTarget.ALL_CACHES)`** before a proof render.

## Errors and dialogs

**Concatenating an `Error` into a string throws its own error** — "Object of type
Error found where a Number, Array, or Property is needed" — masking the real
failure. Always `e.toString()`.

**An uncaught error pops a modal dialog that blocks all further `DoScript`
calls.** The bridge appears dead. Run builds through `eval(fileContents)` inside
try/catch rather than `$.evalFile` so errors stay catchable.

**`app.onError`** can intercept errors AE would otherwise show, but it does not
catch everything — the try/catch wrapper is the reliable route.

## Colour and project settings

**Do not set `app.project.bitsPerChannel = 32`.** In AE 2026 it switches the
project into a linearized colour pipeline and every frame renders dramatically
darker. Use 16 — it removes gradient banding with no gamma surprise.

**Colour properties are 4-component `[r,g,b,a]`** in 0–1 floats. Shape fills
accept 3 or 4.

## Filesystem

**External volumes may be invisible to the shell** while AE reads them fine
(macOS TCC blocks removable volumes: `ls` → "Operation not permitted"). To
identify footage, render thumbnails through AE rather than using ffmpeg. Finder
via osascript can list the directory.

## Things that do work and are worth knowing

- **Path expressions**: `content("GRP").content("PATH").path.pointOnPath(t)` is
  arc-length parameterised, so an object can ride a Trim Paths reveal exactly with
  zero keyframe syncing.
- **Separated position dimensions**: `position.dimensionsSeparated = true` gives
  independent X/Y properties — the correct rig for a bounce (sharp on Y contacts,
  smooth on X) and it removes spatial-bezier corner rounding.
- **Shape path keyframes morph cleanly** between two paths with the same vertex
  count and matching vertex order. Build both from the same angular sequence.
- **Masks on a solid + a gradient effect** gives a gradient-filled shape with a
  feathered edge — the practical way to get gradient fills, since setting a shape
  Gradient Fill's colour ramp from script is not reliable.
- **A light sweep without a track matte**: duplicate the layer, set it to Add,
  and reveal it with a feathered mask whose *path* is keyframed across. (A
  Transform effect moves the already-masked result, not the mask — wrong.)
