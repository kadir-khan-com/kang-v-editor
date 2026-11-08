# LobzyJay/motion-design-with-claude — Motion Design with Claude (After Effects specialist pack)
- Repo: LobzyJay/motion-design-with-claude (GitHub now displays the name "motion-design-with-claude-and-codex"; the clone URL above still resolves)
- Link: https://github.com/LobzyJay/motion-design-with-claude
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 37 stars, 9 forks, 10 commits (repo page, 2026-11-06)
- Last commit (from local clone git log): 2026-09-23
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Extracted: (1) skills/aftereffects-motion/ — the AE specialist: SKILL.md + all 10 references (ExtendScript scripting patterns, expressions, effects catalog, animation & keyframes, text animators, shape layers, operational canon, limits & pitfalls, render output, higgsfield bridge); (2) skills/motion-design/ — the foundation craft skill the AE skill stands on: SKILL.md + 12 principles, easing taxonomy, timing & spacing, defaults-to-avoid, composition-for-motion; (3) skills/motion-design-critique/ — SKILL.md + AE diagnostics + visual diagnostics (the critique loop). Excluded: skills/blender-motion/ and the critique pack's blender-diagnostics.md (Blender — out of this round's scope).

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/SKILL.md` (verbatim)

---
name: aftereffects-motion
description: Use this skill whenever Adobe After Effects is the working tool. Triggers on "After Effects", "AE", ".aep", "ExtendScript", "JSX", "composition", "comp", "keyframe in AE", "AE expression", "render queue", "wiggle", "loopOut", "Trim Paths", or any AE-driven motion graphics task. Also triggers when the user is mid-session with the AE MCP bridge active (mcp-bridge-auto.jsx), or mentions "Higgsfield", "remove background", "reframe", "upscale", "Draw to Edit", or "generate footage" in an AE context. Pair with motion-design (foundation skill) for principles, timing, and taste. AE MCP server: TheLlamainator/after-effects-mcp. Optional Higgsfield Bridge MCP: bridge.higgsfield.ai/mcp.
---

# After Effects Motion

You are driving Adobe After Effects through `TheLlamainator/after-effects-mcp`, and optionally the Higgsfield Bridge. The user is a working designer. They want results that look hand-built, not script-built.

## What you are not

- Not a tutorial bot. Don't explain how AE works unless asked.
- Not an effects-stack maximalist. Restraint reads as taste. Piling effects reads as a beginner.
- Not in control of the viewport. You see only what the user screenshots. Ask for one when uncertain.
- Not allowed to use AE defaults as the answer. Default linear easing, default wiggle, default keyframe interpolation are all signals that you stopped thinking.

## Three modes (pick one before acting)

You operate in one of three execution modes. Decide which before any work.

**Mode A. Live MCP commands.** Single calls: add a layer, set a keyframe, read a property. Slow (3 to 5 seconds per call, sometimes more). Use for small tweaks, scene inspection, iterative adjustments.

**Mode B. JSX scripts.** Write a `.jsx` file. User runs it once via File > Scripts > Run Script File. Fast (under 2 seconds inside AE). Use for anything multi-keyframe, anything with 10+ operations, anything the user might want to re-run later. Most real builds are Mode B.

**Mode C. Higgsfield Bridge.** Generated plates and clips, Remove Background, Reframe, Upscale, Draw to Edit. Spends credits. Never use it for motion builds; those stay in Mode B. See `references/higgsfield-bridge.md`.

Heuristic: if the task is more than 5 MCP calls, write a JSX. Don't ask. See `references/operational-canon.md`.

## Hard rules

1. Easing is a design decision. Never leave it linear unless the brief explicitly demands it (countdowns, machine readouts, type-on effects).
2. Don't animate every layer at once. Stagger and offset. Hierarchy through timing.
3. `wiggle(5, 20)` slapped on Position is not a motion design choice. If you reach for wiggle, justify it or build something more specific. See `references/expressions.md`.
4. Idempotent scripts only. Every JSX you write starts with cleanup logic so it's safe to re-run. See `references/scripting-patterns.md`.
5. If the user has manually adjusted the comp, dump state before changing anything. See `references/scripting-patterns.md` (state dump pattern).
6. Save before you run a destructive script. Tell the user: "Cmd+S first, then run." AE's Undo cannot reliably undo script operations.
7. Mode C spends the user's credits. Say what you'll run on which layer, wait for a yes. Dump state after every bridge operation, before any JSX touches the comp.

## When to load which reference

| Situation | Load |
|---|---|
| Session start, planning a build | `references/operational-canon.md` |
| Before scoping what's possible | `references/limits-and-pitfalls.md` |
| Reaching for `wiggle`, `loopOut`, `valueAtTime`, time-driven motion, inertial bounce | `references/expressions.md` |
| Before writing any JSX | `references/scripting-patterns.md` |
| Setting keyframes, interpolation, velocity, or time remap by hand | `references/animation-and-keyframes.md` |
| Applying or keyframing an effect | `references/effects-catalog.md` |
| Working with shape layers / Trim Paths | `references/shape-layers.md` |
| Animating text reveals or titles | `references/text-animators.md` |
| Setting up render/output | `references/render-output.md` |
| Higgsfield generation, keying, reframing, upscaling | `references/higgsfield-bridge.md` |

Lazy-load. Don't load everything up front.

## The iteration loop

1. User describes goal. Reference image if available.
2. Ask one clarifying question only if blocking.
3. Build (Mode A or B).
4. User runs / previews / screenshots.
5. User sends screenshot back. You diagnose and patch.
6. Repeat.

The screenshot is your only view. Treat the user as your eyes.

## Voice

Direct. No hedging. No "I'll go ahead and...". Tell them what you're about to do, then do it. When you're unsure, say so plainly and ask for the one thing you need.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/animation-and-keyframes.md` (verbatim)

# Animation and Keyframes

Keyframe creation, interpolation, and velocity control via ExtendScript. Load before any keyframe-level build. For the JSX object model and idempotent script template, see `references/scripting-patterns.md`. For expression-driven motion, see `references/expressions.md`.

---

## Two dimensions: temporal and spatial

AE keyframes carry two independent kinds of interpolation. Confusing them is the most common reason scripted motion looks wrong.

| Dimension | Controls | Where you see it |
|---|---|---|
| Temporal | When the value changes (easing, velocity) | Graph editor (speed/value graph) |
| Spatial | The path a position value travels | Comp view (motion path curve) |

Temporal interpolation applies to every animatable property. Spatial interpolation applies only to multi-dimensional spatial properties (Position, Anchor Point, effect point controls). Setting Position to BEZIER temporally does not smooth the path; you set spatial tangents separately.

---

## Interpolation types

```js
KeyframeInterpolationType.LINEAR     // constant velocity, no ease
KeyframeInterpolationType.BEZIER     // manual handle control, in and out
KeyframeInterpolationType.HOLD       // value snaps, no transition
KeyframeInterpolationType.EASY_EASE  // symmetric ease in and out (F9 in UI)
```

Set interpolation after the keyframes exist:

```js
var prop = comp.layer("Card").property("Transform").property("Position");
prop.setValueAtTime(0, [960, 700]);
prop.setValueAtTime(0.6, [960, 540]);

// in, out
prop.setInterpolationTypeAtKey(1, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
prop.setInterpolationTypeAtKey(2, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
```

HOLD is for snaps, cuts, and mechanical on/off states (a counter ticking, a strobe, a hard cut between poses). Never use it for motion that should read as smooth. LINEAR is for countdowns, machine readouts, and constant-rate loops only. Everything else gets BEZIER with deliberate velocity, per the foundation skill's easing rules.

---

## Velocity: the part most scripts skip

`setInterpolationTypeAtKey` only sets the handle type. It does not set the curve shape. A BEZIER keyframe with default handles is barely different from EASY_EASE. To shape real velocity, set temporal ease with `KeyframeEase` objects.

```js
// KeyframeEase(speed, influence)
//   speed: value units per second at the keyframe (usually 0 to stop motion)
//   influence: 0.1 to 100 percent, how far the handle reaches toward the next key
var easeOut = new KeyframeEase(0, 80);   // strong ease out: long influence, parks at 0 speed
var easeMild = new KeyframeEase(0, 33);  // gentle ease (AE default influence is ~16.7)

var prop = comp.layer("Card").property("Transform").property("Position");
// setTemporalEaseAtKey(keyIndex, [inEase per dimension], [outEase per dimension])
// Position is 2D, so pass an array of two eases for each side.
prop.setTemporalEaseAtKey(1, [easeMild, easeMild], [easeOut, easeOut]);
prop.setTemporalEaseAtKey(2, [easeOut, easeOut], [easeMild, easeMild]);
```

For a 1D property (Opacity, Rotation), pass a single-element array:

```js
var op = comp.layer("Card").property("Transform").property("Opacity");
op.setValueAtTime(0, 0);
op.setValueAtTime(0.4, 100);
op.setTemporalEaseAtKey(2, [new KeyframeEase(0, 70)], [new KeyframeEase(0, 70)]);
```

Rule of thumb for entrances: low influence on the outgoing handle of the first key, high influence on the incoming handle of the second key. That is an ease-out: fast departure, soft arrival.

---

## Spatial tangents (motion path shape)

Position keys travel in a straight line until you give them spatial tangents. Tangents are offsets in comp pixels, measured from the keyframe.

```js
var pos = comp.layer("Card").property("Transform").property("Position");
// setSpatialTangentsAtKey(keyIndex, inTangent[x,y], outTangent[x,y])
pos.setSpatialTangentsAtKey(1, [0, 0], [120, 0]);   // leaves moving right
pos.setSpatialTangentsAtKey(2, [120, 0], [0, 0]);   // arrives from the left, curved
```

To force a straight path (no overshoot arc), set both tangents to `[0, 0]` or use `setSpatialContinuousAtKey(keyIndex, false)`.

For an overshoot landing, add a third key past the target and pull the middle key's tangent through it. Do not fake overshoot with extra easing; it reads as mush.

---

## Hold-at-peak and snaps

```js
var scale = comp.layer("Pop").property("Transform").property("Scale");
scale.setValueAtTime(0.0, [0, 0]);
scale.setValueAtTime(0.25, [110, 110]); // overshoot
scale.setValueAtTime(0.4, [100, 100]);  // settle
// snap a strobe off with HOLD:
var op = comp.layer("Strobe").property("Transform").property("Opacity");
op.setValueAtTime(0.0, 100);
op.setInterpolationTypeAtKey(1, KeyframeInterpolationType.HOLD);
op.setValueAtTime(0.1, 0);
```

---

## Roving keyframes

Roving keys let middle position keys float in time so velocity stays smooth across the whole path (good for camera moves and continuous travel). Set the rove flag on interior keys only; the first and last key cannot rove.

```js
var pos = comp.layer("Camera Rig").property("Transform").property("Position");
// keys 2..(n-1) can rove
for (var k = 2; k < pos.numKeys; k++) {
    pos.setRovingAtKey(k, true);
}
```

---

## Time remapping

`timeRemapEnabled` exposes a Time Remap property you keyframe to freeze, reverse, ramp, or stutter a layer's internal time. Useful for hold-at-peak on nested comps and footage.

```js
var layer = comp.layer("PrecompLoop");
layer.timeRemapEnabled = true;
var tr = layer.property("Time Remap");
tr.setValueAtTime(0, 0);      // start of source
tr.setValueAtTime(1, 0.5);    // play first half over 1s
tr.setValueAtTime(1.5, 0.5);  // freeze for 0.5s
tr.setValueAtTime(2.5, 1.0);  // finish
tr.setInterpolationTypeAtKey(3, KeyframeInterpolationType.HOLD); // clean freeze
```

---

## Reading keyframes back

Before patching motion the user adjusted by hand, read the existing keys instead of guessing.

```js
var prop = comp.layer("Card").property("Transform").property("Position");
for (var k = 1; k <= prop.numKeys; k++) {
    var t = prop.keyTime(k);
    var v = prop.keyValue(k);
    // inspect prop.keyInTemporalEase(k), prop.keyInInterpolationType(k) for ease state
}
```

If the comp state may have diverged from what you know, run the state dump in `references/scripting-patterns.md` rather than assuming.

---

## Common mistakes

- Setting BEZIER but not setting `setTemporalEaseAtKey`. The motion stays near-linear and reads cheap.
- Treating Position like a 1D property. It needs an array of eases per side, and separate spatial tangents.
- Using EASY_EASE on entrances. Symmetric ease fights the eye on the way in. Entrances want ease-out, exits want ease-in.
- HOLD on motion that should be smooth, or BEZIER on a strobe that should snap.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/effects-catalog.md` (verbatim)

<!-- INCOMPLETE: expand iteratively, add new effects as they come up in real sessions -->

# Effects Catalog

The model gets effect parameter names wrong because UI names and ExtendScript names don't match. This file is the ground truth for the most-used effects.

Format: Display name (what you see in AE) | ExtendScript name (`addProperty()` argument) | Parameters

---

## Gaussian Blur

Display: **Gaussian Blur**
ExtendScript: `"ADBE Gaussian Blur 2"`

| UI name | ExtendScript name |
|---|---|
| Blurriness | `"Blurriness"` |
| Blur Dimensions | `"Blur Dimensions"` |
| Repeat Edge Pixels | `"Repeat Edge Pixels"` |

```js
var blur = layer.property("Effects").addProperty("ADBE Gaussian Blur 2");
blur.property("Blurriness").setValue(20);
```

---

## Fast Box Blur

Display: **Fast Box Blur**
ExtendScript: `"ADBE Box Blur2"`

| UI name | ExtendScript name |
|---|---|
| Blur Radius | `"Blur Radius"` |
| Iterations | `"Iterations"` |
| Blur Dimensions | `"Blur Dimensions"` |
| Repeat Edge Pixels | `"Repeat Edge Pixels"` |

---

## Drop Shadow

Display: **Drop Shadow**
ExtendScript: `"ADBE Drop Shadow"`

| UI name | ExtendScript name |
|---|---|
| Shadow Color | `"Shadow Color"` |
| Opacity | `"Opacity"` |
| Direction | `"Direction"` |
| Distance | `"Distance"` |
| Softness | `"Softness"` |
| Shadow Only | `"Shadow Only"` |

```js
var shadow = layer.property("Effects").addProperty("ADBE Drop Shadow");
shadow.property("Distance").setValue(10);
shadow.property("Softness").setValue(20);
shadow.property("Opacity").setValue(60);
```

---

## Hue/Saturation

Display: **Hue/Saturation**
ExtendScript: `"ADBE HUE SATURATION"`

| UI name | ExtendScript name |
|---|---|
| Channel Control | `"Channel Control"` |
| Master Hue | `"Master Hue"` |
| Master Saturation | `"Master Saturation"` |
| Master Lightness | `"Master Lightness"` |
| Colorize | `"Colorize"` |
| Colorize Hue | `"Colorize Hue"` |
| Colorize Saturation | `"Colorize Saturation"` |
| Colorize Lightness | `"Colorize Lightness"` |

---

## Levels

Display: **Levels**
ExtendScript: `"ADBE Levels"`

| UI name | ExtendScript name |
|---|---|
| Channel | `"Channel"` |
| Input Black | `"Input Black"` |
| Input White | `"Input White"` |
| Gamma | `"Gamma"` |
| Output Black | `"Output Black"` |
| Output White | `"Output White"` |

---

## Curves

Display: **Curves**
ExtendScript: `"ADBE CurvesCustom"`

Note: Setting Curves values via ExtendScript is complex (custom point data). In practice, use Levels for brightness/contrast adjustments via script and Curves for manual tweaks in the UI.

---

## Tint

Display: **Tint**
ExtendScript: `"ADBE Tint"`

| UI name | ExtendScript name |
|---|---|
| Map Black To | `"Map Black To"` |
| Map White To | `"Map White To"` |
| Amount to Tint | `"Amount to Tint"` |

```js
var tint = layer.property("Effects").addProperty("ADBE Tint");
tint.property("Map Black To").setValue([0, 0, 0, 1]);    // black
tint.property("Map White To").setValue([1, 0.5, 0, 1]);  // orange
tint.property("Amount to Tint").setValue(100);
```

---

## Glow

Display: **Glow**
ExtendScript: `"ADBE Glo2"`

| UI name | ExtendScript name |
|---|---|
| Glow Threshold | `"Glow Threshold"` |
| Glow Radius | `"Glow Radius"` |
| Glow Intensity | `"Glow Intensity"` |
| Composite Original | `"Composite Original"` |
| Glow Colors | `"Glow Colors"` |
| Glow Color Loops | `"Glow Color Loops"` |
| Glow Dimensions | `"Glow Dimensions"` |

---

## Trim Paths

Not an effect, a shape layer property. MCP cannot access this. JSX only.

```js
// accessing Trim Paths on a shape layer
var shapeLayer = comp.layer("ShapeLayer");
var contents = shapeLayer.property("Contents");
var group = contents.property("Group 1");         // your shape group name
var trimPaths = group.property("Trim Paths 1");   // your trim paths name

trimPaths.property("Start").setValueAtTime(0, 0);
trimPaths.property("End").setValueAtTime(0, 0);
trimPaths.property("End").setValueAtTime(1.5, 100);
trimPaths.property("End").setInterpolationTypeAtKey(1, KeyframeInterpolationType.EASY_EASE);
trimPaths.property("End").setInterpolationTypeAtKey(2, KeyframeInterpolationType.EASY_EASE);
```

---

## Set Matte

Display: **Set Matte**
ExtendScript: `"ADBE Set Matte3"`

| UI name | ExtendScript name |
|---|---|
| Take Matte From Layer | `"Take Matte From Layer"` |
| Use For Matte | `"Use For Matte"` |
| Invert Matte | `"Invert Matte"` |
| If Layer Sizes Differ | `"If Layer Sizes Differ"` |
| Composite Matte with Original | `"Composite Matte with Original"` |
| Premultiply Matte Layer | `"Premultiply Matte Layer"` |

---

## Color Balance (HLS)

Display: **Color Balance (HLS)**
ExtendScript: `"ADBE Color Balance (HLS)"`

| UI name | ExtendScript name |
|---|---|
| Hue | `"Hue"` |
| Lightness | `"Lightness"` |
| Saturation | `"Saturation"` |

---

## Lumetri Color

Display: **Lumetri Color**
ExtendScript: `"ADBE lumetri"`

Lumetri has many nested parameters. Most useful for grading via script are Temperature and Tint under Basic Correction:

```js
var lumetri = layer.property("Effects").addProperty("ADBE lumetri");
// Basic correction params are nested under "Basic Correction"
var basic = lumetri.property("Basic Correction");
basic.property("Temperature").setValue(15);    // warm push
basic.property("Tint").setValue(-5);
```

Note: Lumetri's internal naming is inconsistent. Verify param names against the AE UI when setting up.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/expressions.md` (verbatim)

# Expressions

Load when you reach for `wiggle`, `loopOut`, `valueAtTime`, or any time-driven motion. These are the patterns worth knowing. Not a complete reference.

---

## Inertial bounce and overshoot

Dan Ebberts' canonical math. Use this, not a cheap wiggle. Apply to Position, Scale, or Rotation after a settle keyframe.

```js
// Inertial Bounce (post-overshoot settle)
// Apply to the property you want to bounce after its final keyframe
n = 0;
if (numKeys > 0) {
    n = nearestKey(time).index;
    if (key(n).time > time) n--;
}
if (n == 0) {
    t = 0;
} else {
    t = time - key(n).time;
}

if (n > 0 && t < 1) {
    v = velocityAtTime(key(n).time - .001);
    amp = .08;
    freq = 2.5;
    decay = 6.0;
    value + v * amp * Math.sin(freq * 2 * Math.PI * t) / Math.exp(decay * t)
} else {
    value
}
```

Tuning:
- `amp` (amplitude): how far past the target it overshoots. 0.04-0.12 is the useful range.
- `freq` (frequency): oscillation speed. 2.0-4.0 covers most motion graphics use cases.
- `decay`: how fast it settles. Higher = faster decay. 4-8 for UI motion, 2-4 for softer material.

This expression reads the velocity at the last keyframe and decays it. The keyframe value IS the resting target. Don't add a bounce keyframe manually and then add this. Just end at the final value.

---

## loopOut and loopIn

Four modes worth knowing:

```js
loopOut("cycle")       // exact loop from first to last keyframe
loopOut("pingpong")    // forward then backward, seamless
loopOut("offset")      // repeats but offsets by the last-first keyframe delta each cycle
loopOut("continue")    // keeps going at the velocity of the last keyframe (no loop, just continues)
```

Same modes apply to `loopIn`.

Loop a bounce:
```js
loopOut("pingpong")
```

Drift that never repeats exactly:
```js
loopOut("offset")
```

Spin forever from last keyframe velocity:
```js
loopOut("continue")
```

Most useful for:
- Looping icons, badges, badges
- Ambient motion that runs in the background of a longer piece
- Loading states

---

## valueAtTime for stagger and offset

Delay one layer's value by reading another layer's earlier value:

```js
// reads this layer's own value 0.15s ago
// creates a natural lag/echo
thisComp.layer(thisLayer.index).transform.position.valueAtTime(time - 0.15)
```

Delay a property based on another layer:
```js
// reads the "Source" layer's position with a 0.2s delay
thisComp.layer("Source").transform.position.valueAtTime(time - 0.2)
```

Good for:
- Trail effects (position ghost following a lead layer)
- Organic text cascades that don't feel mechanical
- Character rig layers following a root

---

## time and time-driven motion

`time` is always the current composition time in seconds.

Linear value over time:
```js
time * 180   // rotates 180 degrees per second
```

Oscillation with Math.sin:
```js
amplitude = 30;
frequency = 0.5;   // cycles per second
offset = 0;
amplitude * Math.sin(2 * Math.PI * frequency * time + offset)
```

Ramp from 0 to a target value over a fixed duration:
```js
startTime = 0;
duration = 2;
targetValue = 500;
linear(time, startTime, startTime + duration, 0, targetValue)
```

---

## linear() and ease() for remapping

Map time or any value to a range, with or without easing.

```js
// linear(t, tMin, tMax, value1, value2)
// no easing, straight interpolation
linear(time, 0, 3, [0, 540], [960, 540])  // position slides over 3 seconds

// ease(t, tMin, tMax, value1, value2)
// smooth ease-in-out between value1 and value2
ease(time, 0.5, 2.5, 0, 100)  // opacity eases in over 2 seconds

// easeIn and easeOut are also available
easeIn(time, 0, 1, 0, 100)   // starts slow, ends fast
easeOut(time, 0, 1, 0, 100)  // starts fast, ends slow
```

---

## Wiggle done right

Raw `wiggle` on Position with defaults is the fastest way to signal you didn't think. If you reach for wiggle, have a reason.

Default you should not use:
```js
wiggle(5, 20)   // 5 cycles/sec, 20px amplitude. It's just noise.
```

Wiggle with intent:
```js
// slow, large drift, ambient camera-like movement
wiggle(0.5, 8)

// fast, small, mechanical jitter
wiggle(24, 2)

// time-limited wiggle (only during a window, settles after)
amp = 15;
freq = 3;
decay = 2;
n = 0;
if (numKeys > 0) n = nearestKey(time).index;
if (n > 0) {
    t = time - key(n).time;
    amp * Math.exp(-decay * t) * Math.sin(freq * 2 * Math.PI * t) + value
} else {
    value
}
```

Seeded wiggle (two layers that move together):
```js
seedRandom(42, true);  // true = time-independent seed
wiggle(2, 10)
```

Position wiggle in 2D only (don't wiggle Z on a 2D layer):
```js
w = wiggle(1.5, 12);
[w[0], w[1]]
```

---

## Parenting via expressions

Inherit a parent's position without creating an AE parent link (useful when you need additional offset):

```js
// follow "Parent" layer's position with a 20px vertical offset
thisComp.layer("Parent").transform.position + [0, 20]
```

Match rotation:
```js
thisComp.layer("Parent").transform.rotation
```

This is not the same as AE's built-in parent. Use it when you need the parent to exist independently or when you need the relationship to be value-driven, not hierarchy-driven.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/scripting-patterns.md` (verbatim)

# Scripting Patterns

ExtendScript object model and reusable patterns. Load before writing any JSX.

---

## Object model

```
app.project                         → the open AE project
app.project.activeItem              → the currently active comp (CompItem)
app.project.item(index)             → access any item by index (1-based)
comp.layer(name)                    → layer by name (string)
comp.layer(index)                   → layer by index (1-based)
layer.property("Transform")         → the Transform property group
layer.property("Transform").property("Position")     → position
layer.property("Transform").property("Scale")        → scale
layer.property("Transform").property("Rotation")     → rotation
layer.property("Transform").property("Opacity")      → opacity
layer.property("Transform").property("Anchor Point") → anchor point
```

Shape layer contents (Trim Paths, etc.):
```
layer.property("Contents")
layer.property("Contents").property("Group 1")
layer.property("Contents").property("Group 1").property("Trim Paths 1")
```

Effects:
```
layer.property("Effects").property("Gaussian Blur")
layer.property("Effects").property("Gaussian Blur").property("Blurriness")
```

---

## Idempotent JSX template

Every JSX you write must start with cleanup logic. If the script is re-run, it rebuilds cleanly rather than stacking duplicates.

```js
// cleanup-and-rebuild template
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    alert("No active comp. Open a composition first.");
} else {
    app.beginUndoGroup("My Script v1");

    // --- CLEANUP: remove layers this script manages ---
    var managedLayers = ["LockupBG", "LockupText", "LockupIcon"];
    for (var i = comp.numLayers; i >= 1; i--) {
        for (var j = 0; j < managedLayers.length; j++) {
            if (comp.layer(i).name === managedLayers[j]) {
                comp.layer(i).remove();
                break;
            }
        }
    }

    // --- BUILD ---
    // ... your layer/keyframe work here ...

    app.endUndoGroup();
    alert("Done. Preview with 0 on numpad.");
}
```

Rules for idempotent scripts:
- Name layers you create. Check for those names at cleanup time.
- Never assume a layer exists; check `comp.numLayers` before indexing.
- Wrap everything in `beginUndoGroup` / `endUndoGroup`.

---

## Setting keyframes with interpolation

```js
var prop = comp.layer("MyLayer").property("Transform").property("Position");

// set keyframes
prop.setValueAtTime(0, [960, 540]);          // frame 0
prop.setValueAtTime(1.5, [960, 200]);        // 1.5s in

// set interpolation type (after setting keyframes)
prop.setInterpolationTypeAtKey(1, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
prop.setInterpolationTypeAtKey(2, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);

// common interpolation types
// KeyframeInterpolationType.LINEAR
// KeyframeInterpolationType.BEZIER
// KeyframeInterpolationType.HOLD
// KeyframeInterpolationType.EASY_EASE (sets both in/out to ease)
```

After setting BEZIER interpolation, set spatial tangents for clean curves:
```js
// spatialTangent = [xIn, yIn, xOut, yOut] (rough values, adjust to taste)
prop.setSpatialTangentsAtKey(1, [0, 0], [0, -50]);
prop.setSpatialTangentsAtKey(2, [0, 50], [0, 0]);
```

Easy ease shortcut:
```js
prop.setInterpolationTypeAtKey(1, KeyframeInterpolationType.EASY_EASE);
prop.setInterpolationTypeAtKey(2, KeyframeInterpolationType.EASY_EASE);
```

---

## Batch keyframe pattern

When setting many layers to stagger, loop and offset:

```js
var layers = ["Word1", "Word2", "Word3", "Word4"];
var stagger = 0.08; // seconds between each
var duration = 0.4; // animation duration per element

for (var i = 0; i < layers.length; i++) {
    var layer = comp.layer(layers[i]);
    var startTime = i * stagger;
    var endTime = startTime + duration;
    var prop = layer.property("Transform").property("Opacity");

    prop.setValueAtTime(startTime, 0);
    prop.setValueAtTime(endTime, 100);
    prop.setInterpolationTypeAtKey(1 + (i * 2), KeyframeInterpolationType.EASY_EASE);
    prop.setInterpolationTypeAtKey(2 + (i * 2), KeyframeInterpolationType.EASY_EASE);
}
```

---

## Adding and applying effects

```js
var layer = comp.layer("MyLayer");
var effect = layer.property("Effects").addProperty("ADBE Gaussian Blur 2"); // use internal name
effect.property("Blurriness").setValue(20);
```

Internal names differ from display names. See `references/effects-catalog.md` for the mapping.

---

## State dump diagnostic script

Run this when the comp state has diverged from what you know. Save the output, read it back via MCP.

```js
// _dump_state.jsx, run this to capture current comp state
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    alert("No active comp.");
} else {
    var output = {
        compName: comp.name,
        duration: comp.duration,
        frameRate: comp.frameRate,
        width: comp.width,
        height: comp.height,
        layers: []
    };

    for (var i = 1; i <= comp.numLayers; i++) {
        var layer = comp.layer(i);
        var layerData = {
            index: i,
            name: layer.name,
            type: layer.matchName,
            inPoint: layer.inPoint,
            outPoint: layer.outPoint,
            startTime: layer.startTime,
            enabled: layer.enabled,
            solo: layer.solo,
            locked: layer.locked,
            threeDLayer: layer.threeDLayer,
            properties: {}
        };

        // dump Transform properties
        var transform = layer.property("Transform");
        var transformProps = ["Position", "Scale", "Rotation", "Opacity", "Anchor Point"];
        for (var j = 0; j < transformProps.length; j++) {
            var p = transform.property(transformProps[j]);
            if (p) {
                layerData.properties[transformProps[j]] = {
                    value: p.value,
                    numKeys: p.numKeys
                };
                if (p.numKeys > 0) {
                    var keys = [];
                    for (var k = 1; k <= p.numKeys; k++) {
                        keys.push({
                            time: p.keyTime(k),
                            value: p.keyValue(k)
                        });
                    }
                    layerData.properties[transformProps[j]].keys = keys;
                }
            }
        }

        output.layers.push(layerData);
    }

    // write to file
    var outputPath = Folder.desktop + "/ae_dump_state.json";
    var file = new File(outputPath);
    file.open("w");
    file.write(JSON.stringify(output, null, 2));
    file.close();
    alert("Dumped to: " + outputPath);
}
```

After the user runs it, read `ae_dump_state.json` from the desktop via MCP or ask them to paste the content.

---

## try/catch around risky operations

ExtendScript doesn't bubble errors cleanly. Wrap risky operations:

```js
try {
    var layer = comp.layer("MightNotExist");
    layer.property("Transform").property("Opacity").setValue(100);
} catch (e) {
    alert("Error: " + e.toString());
}
```

---

## Naming conventions

Scripts you write should follow this pattern:
- `structural_build.jsx`, creates the full animation structure
- `lockup_reveal_v2.jsx`, versioned variant
- `colorize_dark.jsx`, variant by purpose
- `_dump_state.jsx`, leading underscore for utility/diagnostic scripts
- `_cleanup.jsx`, cleanup utility

Never name scripts by date ("script_may26.jsx"). Name by what they do.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/text-animators.md` (verbatim)

# Text Animators

Per-character, per-word, and per-line text animation via ExtendScript. Load when animating titles, reveals, or any type that moves as a system rather than as a single block. For the JSX object model and idempotent template, see `references/scripting-patterns.md`. For keyframe and easing detail, see `references/animation-and-keyframes.md`.

Text animators beat duplicating one layer per character. For a title with 10+ characters or words, animators are faster to build, faster to retime, and the only sane way to stagger a reveal.

---

## Property tree

The path is deep and exact. Get it wrong and the script throws.

```
layer.property("Source Text")                                   // the text content (TextDocument)
layer.property("Text")                                          // text group
layer.property("Text").property("Animators")                    // animator container
  .addProperty("ADBE Text Animator")                            // one animator group
    .property("Properties")                                     // the animated values live here
      .addProperty("ADBE Text Opacity")                         // opacity
      .addProperty("ADBE Text Position 3D")                     // position (use 3D matchName even for 2D)
      .addProperty("ADBE Text Scale 3D")                        // scale
      .addProperty("ADBE Text Rotation")                        // rotation
    // selector lives at the animator level:
  .property("Selectors").addProperty("ADBE Text Selector")      // Range Selector
```

Internal matchNames matter. Display names will not resolve through `addProperty`.

---

## Setting the text content

```js
var layer = comp.layer("Title");
var srcText = layer.property("Source Text");
var td = srcText.value;          // TextDocument
td.text = "MOTION";
td.fontSize = 120;
td.fillColor = [1, 1, 1];
td.justification = ParagraphJustification.CENTER_JUSTIFY;
srcText.setValue(td);            // must set back; editing the copy does nothing alone
```

---

## The Range Selector is the reveal engine

A Range Selector picks which characters the animator affects. You animate its Start or End, and the animated values sweep across the text. The Selector's Advanced group controls how the effect distributes (per character, word, or line) and the shape of the falloff.

```js
var animator = layer.property("Text").property("Animators").addProperty("ADBE Text Animator");
var sel = animator.property("Selectors").addProperty("ADBE Text Selector");

// Range start/end are 0..100 percent of the text
var selEnd = sel.property("ADBE Text Percent End");
selEnd.setValueAtTime(0, 0);
selEnd.setValueAtTime(0.8, 100); // sweep the selection across the whole title

// distribute per character (default), per word, or per line:
sel.property("ADBE Text Range Type2").setValue(1); // 1 = Characters, 2 = Words, 3 = Lines
```

Common selector properties (matchNames):

| Property | matchName | Use |
|---|---|---|
| Start | `ADBE Text Percent Start` | reveal from the end |
| End | `ADBE Text Percent End` | reveal from the start |
| Offset | `ADBE Text Percent Offset` | slide the whole selection window |
| Units | `ADBE Text Range Units` | percent vs index |
| Based on | `ADBE Text Range Type2` | characters / words / lines |

---

## Per-character fade-up reveal

The workhorse title reveal: each character fades and rises into place, staggered.

```js
// idempotent: clears prior animators this script manages before rebuilding
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    alert("No active comp.");
} else {
    app.beginUndoGroup("Text fade-up reveal v1");
    var layer = comp.layer("Title");
    var animators = layer.property("Text").property("Animators");

    // cleanup: remove animators named by this script
    for (var i = animators.numProperties; i >= 1; i--) {
        if (animators.property(i).name === "FadeUp") animators.property(i).remove();
    }

    var anim = animators.addProperty("ADBE Text Animator");
    anim.name = "FadeUp";
    var props = anim.property("Properties");
    props.addProperty("ADBE Text Opacity").setValue(0);          // start invisible
    props.addProperty("ADBE Text Position 3D").setValue([0, 40, 0]); // start 40px low

    var sel = anim.property("Selectors").addProperty("ADBE Text Selector");
    var end = sel.property("ADBE Text Percent End");
    end.setValueAtTime(0, 0);
    end.setValueAtTime(0.9, 100);
    end.setInterpolationTypeAtKey(2, KeyframeInterpolationType.BEZIER);
    end.setTemporalEaseAtKey(2, [new KeyframeEase(0, 75)], [new KeyframeEase(0, 75)]);

    // smooth the per-character handoff
    var adv = sel.property("Advanced");
    adv.property("ADBE Text Range Shape").setValue(4); // 4 = Smooth ramp

    app.endUndoGroup();
}
```

Slide-in and scale-in are the same structure: swap the animated property. Position `[80, 0, 0]` for a horizontal slide, Scale `[0, 0, 0]` for a scale-in. Stack two animated properties in one animator for combined moves (fade + rise).

---

## Wiggly Selector

For organic, non-uniform character motion (jitter, hand-lettered feel), add a Wiggly Selector instead of animating a Range Selector. It needs no keyframes; it modulates over time on its own.

```js
var wiggly = anim.property("Selectors").addProperty("ADBE Text Wiggly Selector");
wiggly.property("ADBE Text Temporal Wiggle Max Amount").setValue(100);
wiggly.property("ADBE Text Temporal Wiggle Min Amount").setValue(-100);
wiggly.property("ADBE Text Temporal Freq").setValue(2); // wiggles per second
```

Use this sparingly. Default wiggle on text is as much a beginner tell as `wiggle(5,20)` on Position. Justify it or build a deliberate stagger instead.

---

## Retiming a reveal

The whole reveal is driven by one or two selector keyframes. To make it faster, move the End keyframe earlier; to add hold, push it later. You never touch individual characters. That is the entire reason to use animators.

---

## Common mistakes

- Adding animated properties to the animator root instead of its `Properties` group. They will not animate.
- Using `ADBE Text Position` (does not exist); the matchName is `ADBE Text Position 3D` even in a 2D comp.
- Forgetting `setValue(td)` after editing a TextDocument copy.
- Leaving the Range Shape as Square, which makes characters pop in groups instead of flowing. Set Smooth for a clean sweep.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/shape-layers.md` (verbatim)

# Shape Layers

Building and animating shape layers via ExtendScript. Load when working with vector shapes, Trim Paths, strokes, or the Repeater. For the JSX object model and idempotent template, see `references/scripting-patterns.md`. For keyframe and easing detail, see `references/animation-and-keyframes.md`.

Shape layers are the primary vector animation surface in AE. MCP cannot reach into shape contents; all shape work is JSX.

---

## The Contents tree

Everything lives under `Contents`, nested by group. The tree is the thing people get wrong.

```
layer ("ADBE Vector Layer")
  Contents ("ADBE Root Vectors Group")
    Group ("ADBE Vector Group")
      Contents ("ADBE Vectors Group")        // the group's own contents
        Path     ("ADBE Vector Shape - Group")
        Stroke   ("ADBE Vector Graphic - Stroke")
        Fill     ("ADBE Vector Graphic - Fill")
        Trim     ("ADBE Vector Filter - Trim")
        Repeater ("ADBE Vector Filter - Repeater")
      Transform  ("ADBE Vector Transform Group")  // the group's transform, not the layer's
```

Order matters. A stroke listed above a fill draws on top of it. Trim Paths and Repeater are modifiers; they affect everything above them in the same group.

---

## Creating a shape layer from script

```js
var comp = app.project.activeItem;
app.beginUndoGroup("Build shape v1");

// cleanup if re-run
for (var i = comp.numLayers; i >= 1; i--) {
    if (comp.layer(i).name === "Ring") comp.layer(i).remove();
}

var shapeLayer = comp.layers.addShape();
shapeLayer.name = "Ring";
var contents = shapeLayer.property("Contents");

var group = contents.addProperty("ADBE Vector Group");
group.name = "RingGroup";
var groupContents = group.property("ADBE Vectors Group");

// an ellipse primitive
var ellipse = groupContents.addProperty("ADBE Vector Shape - Ellipse");
ellipse.property("ADBE Vector Ellipse Size").setValue([400, 400]);

// stroke, no fill
var stroke = groupContents.addProperty("ADBE Vector Graphic - Stroke");
stroke.property("ADBE Vector Stroke Color").setValue([1, 1, 1, 1]);
stroke.property("ADBE Vector Stroke Width").setValue(12);

app.endUndoGroup();
```

For a custom path instead of a primitive, build a `Shape` object and set it on `ADBE Vector Shape - Group`:

```js
var pathGroup = groupContents.addProperty("ADBE Vector Shape - Group");
var myShape = new Shape();
myShape.vertices = [[0, 0], [200, 0], [200, 200], [0, 200]];
myShape.closed = true;
pathGroup.property("ADBE Vector Shape").setValue(myShape);
```

---

## Trim Paths (the line-draw workhorse)

Trim Paths is the standard way to draw on a stroke, build progress rings, and reveal outlines. It is a group-level modifier, not a layer property.

```js
var trim = groupContents.addProperty("ADBE Vector Filter - Trim");
var end = trim.property("ADBE Vector Trim End");   // 0..100 percent
end.setValueAtTime(0, 0);
end.setValueAtTime(1.2, 100);
end.setInterpolationTypeAtKey(1, KeyframeInterpolationType.BEZIER);
end.setInterpolationTypeAtKey(2, KeyframeInterpolationType.BEZIER);
end.setTemporalEaseAtKey(2, [new KeyframeEase(0, 80)], [new KeyframeEase(0, 80)]);

// offset rotates the start point around the path; animate it for a chasing dash
trim.property("ADBE Vector Trim Offset").setValue(0);
```

Trim properties: `ADBE Vector Trim Start`, `ADBE Vector Trim End`, `ADBE Vector Trim Offset`. To draw out then retract, animate End up and Start up behind it. For a progress ring, animate End alone and start the path at 12 o'clock with Offset.

---

## Stroke and Fill keyframing

Stroke and Fill are group-level graphic properties. Keyframe them exactly like Transform properties.

```js
var fill = groupContents.addProperty("ADBE Vector Graphic - Fill");
var color = fill.property("ADBE Vector Fill Color");
color.setValueAtTime(0, [0.1, 0.1, 0.1, 1]);
color.setValueAtTime(0.5, [0.9, 0.2, 0.3, 1]);

var width = stroke.property("ADBE Vector Stroke Width");
width.setValueAtTime(0, 0);
width.setValueAtTime(0.4, 12); // stroke grows in
```

Dashes live under the stroke's `ADBE Vector Stroke Dashes` group (add a `ADBE Vector Stroke Dash 1` property). Animate the dash offset for marching-ants and chase effects.

---

## Repeater (grids, radials, bursts)

The Repeater duplicates everything above it in the group with a compounding transform. It is the fastest way to a grid, a radial burst, or a row of ticks.

```js
var rep = groupContents.addProperty("ADBE Vector Filter - Repeater");
rep.property("ADBE Vector Repeater Copies").setValue(12);
var repTransform = rep.property("ADBE Vector Repeater Transform");
repTransform.property("ADBE Vector Repeater Position").setValue([0, 0]);
repTransform.property("ADBE Vector Repeater Rotation").setValue(30); // 12 copies x 30deg = full circle
// stagger opacity across copies for a fade-in burst:
repTransform.property("ADBE Vector Repeater Opacity Start").setValue(100);
repTransform.property("ADBE Vector Repeater Opacity End").setValue(0);
```

Animate Copies for a count-up, or animate the Repeater's Offset to march the pattern. To stagger the copies in time you pair the Repeater with an expression or split into separate layers; the Repeater itself cannot offset copies temporally.

---

## Scripting against a hand-built shape layer

Hand-built layers default to generic names ("Shape 1", "Group 1"), and the tree may not match what you expect. Do not assume. Dump the contents tree first:

```js
function dumpContents(propGroup, indent) {
    indent = indent || "";
    var out = "";
    for (var i = 1; i <= propGroup.numProperties; i++) {
        var p = propGroup.property(i);
        out += indent + p.name + "  [" + p.matchName + "]\n";
        if (p.numProperties && p.numProperties > 0) {
            out += dumpContents(p, indent + "  ");
        }
    }
    return out;
}
var layer = app.project.activeItem.layer("Shape Layer 1");
alert(dumpContents(layer.property("Contents")));
```

Read the real names back, then target them exactly.

---

## Common mistakes

- Adding modifiers (Trim, Repeater) at the layer level instead of inside the group's `ADBE Vectors Group`. They do nothing there.
- Confusing the group's own Transform (`ADBE Vector Transform Group`) with the layer Transform. Animating the wrong one moves the wrong thing.
- Assuming primitive names. A "rectangle" the user drew might be a custom path, not `ADBE Vector Shape - Rect`. Dump first.
- Stroke drawn under fill, so the line-draw is hidden. Reorder so stroke sits above fill in the group.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/operational-canon.md` (verbatim)

# Operational Canon

How a session actually runs. Load at session start.

## Bridge setup (user-side, once per session)

The MCP server only works if the AE-side bridge is active. If the user isn't getting responses, this is usually why.

1. Open the AE project (`.aep`).
2. Window menu > `mcp-bridge-auto.jsx`. A floating panel appears.
3. Tick the **Auto-run commands** checkbox in that panel.
4. Leave it open for the whole session.

If you make an MCP call and nothing happens, the panel is closed or the checkbox is off. Tell the user to reopen `Window > mcp-bridge-auto.jsx` and tick the box again.

## Choose Mode A or Mode B before acting

Mode A. Live MCP commands. Each tool call is one operation in AE. Round-trip is 3-5 seconds. Good for:

- Inspecting a comp (list layers, get a property value)
- One-off changes (add a Gaussian Blur to layer 1)
- Iterative adjustments while the user is watching

Mode B. JSX scripts. You write a `.jsx` file and the user runs it once via `File > Scripts > Run Script File...`. Good for:

- Building entire animations (50+ keyframes at once)
- Complex effects, masks, time remaps
- Anything you might re-run later
- Anything that would otherwise be 10+ MCP roundtrips

If a build is more than 5 MCP calls, switch to JSX. Don't ask.

The user can re-run a JSX file as many times as needed (as long as you wrote it idempotently, which you must, see `scripting-patterns.md`).

## The iteration loop in detail

1. **User describes the goal.** Plain language is fine. They will sometimes drop a reference image. Treat reference images as design direction, not pixel-exact targets, unless they say otherwise.

2. **Ask one blocking question, if any.** Examples of blocking: target duration unclear, target framerate/comp size unknown, source asset path missing. Don't ask design-taste questions ("should the easing be soft or sharp?"); make a call and let them push back.

3. **Build.** If JSX, save the file to the user's project folder (ask for the path once and remember it for the session). Recommended name pattern: `<purpose>_<vN>.jsx`, e.g. `lockup_reveal_v3.jsx`.

4. **Tell the user exactly what to do next.** If JSX, say: "Save your project (Cmd+S), then run `File > Scripts > Run Script File... > lockup_reveal_v3.jsx`." If Mode A, the work happens live.

5. **User previews.** They hit `0` on the numpad for RAM preview. They report what's wrong or what's right, ideally with a screenshot at a specific timestamp.

6. **You diagnose from the screenshot + their description, then patch.** Patches that touch what the user has changed manually need a state dump first (see below).

## Screenshot-driven debugging

Your only view of AE is what the user screenshots. When something looks wrong:

- Ask for a screenshot **at a specific time** (e.g. "screenshot at 2.5s with the comp panel visible at 100% zoom").
- If timing is the question, ask for two screenshots (start and end of the problematic range).
- If layering is the question, ask for the timeline panel screenshot too, not just the comp panel.

Treat the user as your eyes. They will know what's wrong before you do.

## State dump pattern

If the user has manually adjusted properties or added layers since your last script, your model of the comp is stale. Don't push changes blind. Write a one-shot diagnostic script that dumps the current comp state to JSON, ask the user to run it, then read the JSON file back via the MCP. Then patch.

The state dump script lives in `scripting-patterns.md` as a template. Common name: `_dump_state.jsx`.

## File organisation

Recommend the user keep a per-project folder:

```
~/Documents/<Project>/
├── <Project>.aep
├── structural_build.jsx
├── lockup_reveal.jsx
├── colorize_variants.jsx
└── _dump_state.jsx
```

When you write a new script, save it into that folder by default. Name it for what it does, not when it was made.

## Save discipline

Before running any non-trivial JSX, the user must save. Always say "Cmd+S first, then run." AE's Undo (Cmd+Z) is unreliable on script operations. If a script destroys work and AE didn't undo cleanly, the most recent save is the only recovery.

## Common commands the user might paste back at you

Worth recognising so you can respond fast:

| User says... | They mean... |
|---|---|
| "rerun the script" | Re-execute the JSX you wrote, no changes needed |
| "dump state" | Run `_dump_state.jsx` |
| "patch the timing" | Change keyframe times, not the structural script |
| "restart this section" | Throw away current approach, propose new one |
| "0 on numpad" | RAM preview (just FYI, no action needed) |

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/limits-and-pitfalls.md` (verbatim)

# Limits and Pitfalls

What the AE MCP can and cannot do. Read before scoping any build.

---

## Hard limits: MCP cannot do these

**Trim Paths and shape-layer interiors.** The MCP has no access to shape layer contents. Trim Paths, stroke/fill toggles on shapes, any property inside a shape group, all JSX-only. If the user asks for a Trim Paths animation, write JSX. Do not attempt via MCP.

**3D Layer switch.** Enabling the 3D Layer flag on a layer (`layer.threeDLayer`) is not accessible via MCP. Either tell the user to do it manually or handle it via JSX.

**Render and export.** Claude cannot trigger renders or exports. The user runs the Render Queue themselves. Your job ends at "set this up to render." Don't imply otherwise.

**Viewport vision.** Claude has no live view of the AE comp. The only way to see the current state is a user screenshot. Ask for one at a specific time when you need it, "screenshot at 2.5s with the comp panel visible at 100% zoom."

---

## ExtendScript quirks (ES3, not modern JS)

AE's scripting engine runs ExtendScript, which is roughly ES3. It does not understand modern syntax.

**No `const` or `let`.** Use `var` only.

```js
// breaks
const x = 5;
let y = 10;

// correct
var x = 5;
var y = 10;
```

**No arrow functions.**

```js
// breaks
var result = items.map(i => i.name);

// correct
var result = [];
for (var i = 0; i < items.length; i++) {
    result.push(items[i].name);
}
```

**No template literals.**

```js
// breaks
var msg = `Layer: ${name}`;

// correct
var msg = "Layer: " + name;
```

**`Array.indexOf` not always available.** Check before using, or write a manual loop.

```js
// safe fallback
function indexOf(arr, val) {
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] === val) return i;
    }
    return -1;
}
```

**No `try/catch` on property access (no optional chaining either).** Always check for null before accessing nested properties.

---

## Bridge requirements

The AE MCP only works when:

1. The `mcp-bridge-auto.jsx` panel is open (Window menu).
2. The **Auto-run commands** checkbox is ticked.
3. The panel stays open the entire session.

If the user closes the panel mid-session, all subsequent MCP calls will silently fail or hang. When this happens, tell them: "Reopen `Window > mcp-bridge-auto.jsx` and tick Auto-run commands."

---

## Undo is unreliable after JSX

AE's Undo (Cmd+Z) cannot reliably undo script operations. If a script runs and trashes something, Undo may not recover it. Before any non-trivial script, always say: "Cmd+S first, then run." The most recent save is the real undo.

---

## State staleness

If the user has moved keyframes, adjusted values, or added layers manually since your last script ran, your model of the comp is stale. Do not write a patch script based on stale assumptions. Write a state dump first, read the result, then patch.

---

## Performance: MCP is slow

Each MCP call takes 3-5 seconds. Ten calls = 30-50 seconds of dead time. If a build takes more than 5 MCP calls, switch to JSX. Don't ask. This isn't a preference; it's respect for the user's time.

---

## What MCP can do (for reference)

- `setLayerKeyframe`: sets position, scale, rotation, opacity keyframes
- `setLayerExpression`: attaches expression strings to properties
- `apply-effect`: applies effects by effect name
- `set-effect-keyframe`: keyframes effect parameters
- `run-script` with predefined scripts: `getProjectInfo`, `getLayerInfo`, `listCompositions`

Anything not on this list either requires JSX or is not possible at all.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/render-output.md` (verbatim)

# Render and Output

Render Queue setup, output modules, and codec choices via ExtendScript. Load when preparing a render or auditing output settings. For the JSX object model, see `references/scripting-patterns.md`.

Claude never triggers the render. The user always presses the button. Your job is to set the queue up correctly and audit it before they do.

---

## What Claude can and cannot do

| Can | Cannot |
|---|---|
| Add a comp to the Render Queue | Start the render (it is a user action) |
| Set render settings and output module | Reliably render H.264 from older AE without AME |
| Set the output file path | Render faster than the machine allows |
| Read and audit all current settings | See the rendered result without a screenshot |

RAM preview (numpad 0) is not a render. It caches to RAM for real-time playback only. The Render Queue writes to disk.

---

## Adding a comp to the queue

```js
var comp = app.project.activeItem;
app.beginUndoGroup("Queue render v1");

var rq = app.project.renderQueue;
var rqItem = rq.items.add(comp);          // returns the RenderQueueItem
rqItem.timeSpanStart = 0;                 // render the whole comp
rqItem.timeSpanDuration = comp.duration;

app.endUndoGroup();
```

To audit instead of add, read existing items:

```js
var rq = app.project.renderQueue;
for (var i = 1; i <= rq.numItems; i++) {
    var item = rq.item(i);
    // item.status, item.comp.name, item.timeSpanDuration
    var om = item.outputModule(1);
    // om.file (output path), om.name (template)
}
```

---

## Render settings vs output module

Two separate things. Render Settings controls resolution, frame rate, and quality of the render itself. The Output Module controls the file format and codec written to disk.

```js
// apply a saved Render Settings template by name
rqItem.applyTemplate("Best Settings");

// apply a saved Output Module template by name
rqItem.outputModule(1).applyTemplate("ProRes 422 HQ");

// set the output path
rqItem.outputModule(1).file = new File("~/Desktop/render/shot_01.mov");
```

Template names must already exist in the project's render settings/output module presets. If a named template is missing, `applyTemplate` throws. Wrap it in try/catch and tell the user which template to create.

---

## Codec choice by delivery

| Delivery | Format | Why |
|---|---|---|
| Final master, handoff with alpha | ProRes 4444 | 12-bit, alpha channel, near-lossless |
| Final master, no alpha | ProRes 422 HQ | broadcast standard, manageable size |
| Frame-accurate iteration, safest | PNG sequence | per-frame, resumable, no codec artifacts |
| Web / client review | H.264 (.mp4) | small, plays everywhere |

Hard rule: do not render H.264 directly from AE for a final master if quality matters. Render ProRes or a PNG sequence, then transcode to H.264 in Adobe Media Encoder. Direct H.264 from the AE queue is lower quality and, in current versions, routed through AME anyway.

---

## Adobe Media Encoder handoff

For H.264 and most delivery codecs, send to AME instead of the AE queue:

```js
// queues the active comp in Adobe Media Encoder (AME must be installed)
app.project.renderQueue.queueInAME(false); // false = do not start immediately
```

The user picks the preset and starts the render in AME. This keeps AE free and gives better H.264 output.

---

## Pre-render audit (run before they hit Render)

Before any final render, confirm:

1. Resolution and frame rate match the comp's intent (`comp.width`, `comp.height`, `comp.frameRate`).
2. Time span is the whole comp, not a stray work-area trim (`rqItem.timeSpanStart`, `rqItem.timeSpanDuration`).
3. Output module codec matches the delivery (see table above).
4. Output path exists and is writable; the filename is descriptive, not `Comp 1.mov`.
5. No solo'd or hidden layers that should be visible (cross-check with `references/limits-and-pitfalls.md` and a state dump).

Then tell the user: "Cmd+S first. Settings are confirmed. Hit Render (or Start Queue in AME)."

---

## Common mistakes

- Rendering with the work area trimmed by accident, so the output is half the comp. Set `timeSpanDuration` explicitly.
- Applying an output module template that does not exist in the project. Confirm the preset name first.
- Rendering H.264 as a master, then wondering why the gradients band. Render ProRes or PNG, transcode after.
- Forgetting that the queue writes over an existing file silently if the path matches. Version the filename.

---

## 📄 SOURCE FILE: `skills/aftereffects-motion/references/higgsfield-bridge.md` (verbatim)

# Higgsfield Bridge (After Effects)

Mode C. How to run the Higgsfield AE plugin through its MCP bridge alongside the AE MCP and JSX. Load when the user mentions Higgsfield, generated footage, background removal, reframing, upscaling, or Draw to Edit.

---

## Bridge setup (user-side, once per machine)

Requirements: After Effects 2024 (24.0) or newer, macOS (Apple Silicon or Intel) or Windows 10/11 64-bit, internet, a Higgsfield account with credits. One installer covers AE and Premiere Pro.

**macOS**
1. Download the .dmg from `higgsfield.ai/plugins/after-effects`.
2. Open it, drag Higgsfield to Applications, double-click to launch once.
3. In AE: Window > Extensions > Higgsfield AI. Sign in.

**Windows**
1. Install the free ZXP Installer from aescripts.
2. Drag the Higgsfield .zxp onto it.
3. In AE: Window > Extensions > Higgsfield AI. Sign in.

Then register the bridge with the agent (see README). Name it `HiggsfieldBridge`. URL: `https://bridge.higgsfield.ai/mcp`. Authenticate once when the agent asks.

Keep the Higgsfield panel open and signed in for the session. The AE MCP bridge (`mcp-bridge-auto.jsx`) stays open too if you want Mode A.

Verification prompt:
> "Use the aftereffects-motion skill. Check the Higgsfield Bridge is connected and list the comps in my project."

---

## Three modes

| Task | Mode |
|---|---|
| Read a property, nudge one keyframe, inspect the comp | A. AE MCP |
| Any multi-keyframe build, anything re-runnable | B. JSX |
| Shape layers, Trim Paths, text animators | B. JSX |
| Generate a plate, background, overlay, or title card image | C. Bridge |
| Generate a video clip onto the timeline | C. Bridge |
| Key a subject without green screen | C. Bridge: Remove Background |
| Deliver 9:16, 1:1, 4:3, 3:4, 21:9 from a 16:9 master | C. Bridge: Reframe |
| Paint out an object or add an element on a frame | C. Bridge: Draw to Edit |
| Push footage to 4K or 8K | C. Bridge: Upscale |
| Prompt-based change to existing footage | C. Bridge: Edit Video |

The bridge can also write layers, keyframes, and expressions. Don't use it for that. Motion builds stay in Mode B: a JSX file is reproducible, idempotent, and reviewable. A bridge build is none of those. The only exception is when the user explicitly asks the bridge to build it.

---

## Credit discipline

Generation, Remove Background, Reframe, Upscale, and Edit Video all spend Higgsfield credits (unless the model is on the user's Unlimited list; you can't see that).

1. Say what you're about to run, on which layer, at what output: "Remove Background on `Talent_A.mov`, full duration. Spends credits. Go?"
2. Wait for a yes. One operation per yes.
3. Trim the work area or precomp to the used range before processing footage. Don't upscale or key frames that never make the cut.
4. No variants unless asked.
5. If an operation fails, report it once and ask before retrying.

---

## After every bridge operation: dump state

Generated or processed media lands in the project and usually on the timeline. You don't know where until you look.

1. Run the state dump from `scripting-patterns.md` (or a Mode A read of the active comp).
2. List what was added: new footage items, new layers, their index, in and out points.
3. Rename new layers to the comp's naming convention. Prefix `HF_` if there isn't one.
4. Park generated footage in a project folder (`HF Generations`). Idempotent JSX pattern:

```js
(function () {
    var FOLDER = "HF Generations";
    var proj = app.project;
    if (!proj) { alert("No project open."); return; }

    app.beginUndoGroup("Collect HF generations");
    try {
        var folder = null;
        for (var i = 1; i <= proj.numItems; i++) {
            var it = proj.item(i);
            if (it instanceof FolderItem && it.name === FOLDER) { folder = it; break; }
        }
        if (!folder) folder = proj.items.addFolder(FOLDER);

        // names come from the state dump, never guessed
        var names = ["HF_plate_01.mp4", "HF_bg_sky.png"];
        var missing = [];
        for (var n = 0; n < names.length; n++) {
            var found = false;
            for (var j = 1; j <= proj.numItems; j++) {
                var item = proj.item(j);
                if (item.name === names[n] && !(item instanceof FolderItem)) {
                    item.parentFolder = folder;
                    found = true;
                    break;
                }
            }
            if (!found) missing.push(names[n]);
        }
        if (missing.length) alert("Not found: " + missing.join(", "));
    } catch (e) {
        alert("Collect failed: " + e.toString());
    } finally {
        app.endUndoGroup();
    }
})();
```

5. Only then run any JSX that touches the comp. A JSX written against a pre-bridge state dump can target the wrong layer index.

---

## Using generated media well

- Generated footage is a plate, not the design. Motion, timing, and hierarchy still come from you and the foundation skill.
- Match frame rate. Check the generated clip's fps against the comp before building on it. Interpret Footage if it's off; never let AE frame-blend silently.
- Remove Background output carries alpha. Check edges at 200% on a hair or motion-blur frame before approving. Ask for a screenshot at a specific time.
- Reframe tracks the subject. It doesn't know your type safe areas. Check titles and lower thirds in every aspect ratio after reframing.
- Upscale before grading and effects, not after.

---

## Supercomputer and ChatGPT routes

Higgsfield's Supercomputer detects the plugin with no bridge setup. ChatGPT has its own Higgsfield plugin with a `/use-after-effects` command. Same rules apply there: credits confirmed, JSX for motion builds, state dump after every operation.

---

## Limits

- Cloud only. No offline mode. The panel must be signed in.
- AE 2023 and older are unsupported.
- Generation time scales with resolution and duration. Don't promise turnaround.
- The bridge sees the project, not the viewer. You still need a user screenshot to judge the result.
- Commercial rights depend on the user's Higgsfield plan. Flag it once if the work is for a client.

---

## 📄 SOURCE FILE: `skills/motion-design/SKILL.md` (verbatim)

---
name: motion-design
description: Use this skill whenever motion, animation, timing, easing, or composition over time is the subject. Triggers on "animate", "motion", "easing", "timing", "keyframe", "transition", "stagger", "loop", "bounce", "overshoot", "follow-through", "anticipation", "12 principles", "motion hierarchy", "composition for motion". Does NOT trigger on still design, static layout, color theory, or typography in isolation. Pair with aftereffects-motion or blender-motion when a tool is named. Load this first; specialists layer on top.
---

# Motion Design

You are advising on motion as a design discipline. The user is a working designer. They want output that reads as craft, not as software defaults applied.

## What you are not

- Not a tutorial. Don't explain what a keyframe is.
- Not a neutral reference. Motion is full of defaults that signal no decision was made. Name them and steer away.
- Not a generalist. "Add some animation" is not a brief. Push for specificity: what moves, when, at what pace, for what reason.

## The fundamental split

**Timing** is when things happen. **Spacing** is how values distribute between those moments.

Both are decisions. Neither has a correct default. Linear easing and uniform timing are the absence of a decision, not a neutral one.

## Hard rules

1. Easing is a design decision. Ease-out for entrances. Ease-in for exits. Custom bezier for anything with a strong mood. Linear only for countdowns, machine readouts, or mechanical metaphors.
2. Nothing moves simultaneously unless that simultaneity is the point. Stagger. Offset. Build hierarchy through timing.
3. Anticipation and follow-through are not optional polish. They are what separates motion that feels physical from motion that feels like a slide transition.
4. Duration communicates weight. Fast is light. Slow is heavy. If everything is 300ms, nothing has weight.
5. Restraint reads as taste. One thing moving well beats five things moving adequately.
6. If a motion could be removed and the design would work fine, remove it.

## When to load which reference

| Situation | Load |
|---|---|
| Discussing any animation principle | `references/12-principles.md` |
| Choosing or critiquing easing | `references/easing-taxonomy.md` |
| Talking about duration, stagger, or pacing | `references/timing-and-spacing.md` |
| Designing for motion in a frame | `references/composition-for-motion.md` |
| Output feels robotic or default | `references/defaults-to-avoid.md` |

Lazy-load. Don't load all references up front.

## The critique loop

When reviewing motion:
1. Identify what each element is doing and why.
2. Name what reads as a default. Be direct.
3. Propose a specific alternative with values, not vague direction.

"The easing feels off" is not useful. "The entrance is ease-in-out when it should be ease-out, it's fighting the eye as it enters the frame" is useful.

## Voice

Direct. Designer-to-designer. Name the problem and give the fix. No hedging. No summaries.

---

## 📄 SOURCE FILE: `skills/motion-design/references/12-principles.md` (verbatim)

# 12 Principles of Animation

The Disney canon, distilled for applied motion design. Each principle is a decision tool, not a technique to tick off.

---

## 1. Squash and Stretch

**What it is:** Objects deform in the direction of motion and recover on impact. Volume stays constant.

**When to use:** Physical objects under force: bouncing, impact, weight landing. For UI and brand motion, a subtle version on logos and icons adds life without going cartoon. Scale on one axis while counter-scaling the other.

**Common mistake:** Applying it uniformly across all elements. A typographic headline does not squash and stretch. A bouncing badge does.

---

## 2. Anticipation

**What it is:** A brief motion in the opposite direction before the main action. A character crouches before jumping. A UI element pulls back slightly before launching.

**When to use:** Before any large fast move. It primes the eye and makes the main action read as intentional force rather than sudden teleportation.

**Common mistake:** Skipping it entirely. Most software-default animations have no anticipation. That's why they feel mechanical.

---

## 3. Staging

**What it is:** Every moment in time has one clear read. The audience's eye goes exactly where you need it, not wherever happens to be moving.

**When to use:** Always. In a frame, nothing competes for attention during a transition. If two things move simultaneously, one of them is wrong.

**Common mistake:** Animating all elements at once to "save time." Hierarchy through timing is the solution. See `timing-and-spacing.md`.

---

## 4. Straight Ahead vs. Pose-to-Pose

**What it is:** Two approaches to building an animation. Straight ahead: animate from first frame to last without planning. Pose-to-pose: define the key moments (poses), then fill in between.

**When to use:** In motion design (not character animation), pose-to-pose is almost always right. Define the start state, the peak, and the end state. Then control the spacing between them with easing. Straight ahead works for organic, unpredictable motion (fire, water, particles).

**Common mistake:** Treating this as a character animation concept with no application to motion graphics. It directly maps to keyframe-first vs. procedural-first thinking.

---

## 5. Follow-Through and Overlapping Action

**What it is:** Parts of an object continue to move after the main body stops (follow-through). Different parts of an object move at different rates (overlapping action).

**When to use:** Any multi-part element. A wordmark where letters continue to settle after the lockup lands. A logo where secondary elements lag the primary. Without this, everything stops at exactly the same frame and reads as a grid of simultaneity.

**Common mistake:** All layers hitting their final keyframe at the same time. Every layer in your stack should have a slightly different end point.

---

## 6. Slow In and Slow Out

**What it is:** Motion accelerates at the start and decelerates at the end. The spacing of frames is denser at the beginning and end, sparser in the middle.

**When to use:** This is easing. Always, with intent. See `easing-taxonomy.md` for when to apply which variant.

**Common mistake:** Linear easing. The model's default. The first thing to fix on any AI-generated animation.

---

## 7. Arcs

**What it is:** Natural motion follows curved paths, not straight lines. Eyes, limbs, and pendulums move in arcs. So do elements with physical metaphors.

**When to use:** Position animation where a straight-line path looks mechanical. Set spatial tangent handles in AE to curve the motion path. In Blender, edit the F-curve in the graph editor for curved paths.

**Common mistake:** Ignoring spatial handles entirely and letting AE default to straight-line paths between keyframes.

---

## 8. Secondary Action

**What it is:** A supporting motion that reinforces the main action. A character thinking while walking. A badge pulsing while a modal enters.

**When to use:** When the main animation is long enough to warrant a sub-element providing rhythm or context. Subtle. If the secondary action is more interesting than the primary, something is wrong.

**Common mistake:** Adding secondary action that competes with the primary. If the user's eye follows the secondary, it's staging, not secondary action.

---

## 9. Timing

**What it is:** The number of frames an action takes. More frames = slower, heavier. Fewer frames = faster, lighter. Timing communicates weight and urgency.

**When to use:** Always calibrated to the physical metaphor. A heavy logo should enter slower than a light notification. A system alert should feel faster than an onboarding reveal.

**Common mistake:** Every element at 300ms because it "looks smooth." Duration is a design variable, not a constant.

---

## 10. Exaggeration

**What it is:** Pushing the motion past what would be physically realistic to make it read clearly. Overshoot past the target. Anticipation that's a beat longer than strictly necessary.

**When to use:** Brand and marketing motion, where charm is the goal. Less applicable to product UI where subtlety is expected. The right amount is: more than you think, less than cartoon.

**Common mistake:** Restraint mistaken for quality. Subtle motion isn't always better. Sometimes it just reads as tentative.

---

## 11. Solid Drawing (Solid Design in motion context)

**What it is:** In character animation, understanding 3D form. In motion design: keeping the design coherent as it moves. A logo that looks good in its final position should look intentional at every frame of its entrance.

**When to use:** Always check midpoint frames. At 50% through an animation, the frame should be designerly, not a blur of things in transit.

**Common mistake:** Only checking start and end states. A reveal that looks fine at 0 and 100 can look broken at frame 12.

---

## 12. Appeal

**What it is:** The quality that makes motion feel alive and worth watching. Charisma, not complexity. A simple motion with perfect timing and easing has more appeal than a complex one with defaults.

**When to use:** As a final check. After all other principles are applied, ask: does this motion feel like it was made by someone with taste, or like it was generated by a default setting?

**Common mistake:** Conflating appeal with detail. Adding more effects does not add appeal. Sharpening timing and easing does.

---

## 📄 SOURCE FILE: `skills/motion-design/references/easing-taxonomy.md` (verbatim)

# Easing Taxonomy

Not a list of curve shapes. A decision framework: which easing for which situation, and why.

---

## The decision tree

```
Is this an entrance (something appearing or arriving)?    → ease-out
Is this an exit (something leaving or disappearing)?      → ease-in
Is this a loop or a transition between two held states?   → ease-in-out
Is this a countdown, machine, or mechanical readout?      → linear
Does the brief have a specific mood (snap, spring, drag)? → custom bezier
```

If none of the above fit, the motion has not been scoped clearly enough. Get a clearer brief before choosing easing.

---

## Ease-out (deceleration)

**When:** Entrances. Elements entering the frame or arriving at their final position.

**Why:** Ease-out mirrors how physical objects move when arriving. Fast at the beginning, settling into position. It front-loads the energy so the eye catches the element immediately.

**AE convention:** In the graph editor, the value starts fast and slows at the end. Set the outgoing velocity high, incoming velocity near zero.

**bpy convention:** In the NLA/Graph Editor, use `EASE_OUT` interpolation or set handles so the right handle of the starting keyframe is positioned up-and-close and the left handle of the ending keyframe is positioned far-and-flat.

---

## Ease-in (acceleration)

**When:** Exits. Elements leaving the frame or transitioning away.

**Why:** Ease-in mirrors an object picking up speed as it leaves. Slow departure, fast exit. Without this, exits feel like elements getting yanked out of frame.

**AE convention:** Outgoing velocity near zero, incoming velocity high.

**bpy:** Left handle of ending keyframe positioned up-and-close, right handle of starting keyframe positioned far-and-flat.

**Caution:** Do not use ease-in for entrances. A slow-start entrance fights the eye; the viewer sees nothing happening, then suddenly the element is there.

---

## Ease-in-out (symmetric)

**When:** Loops. Transitions between two resting states where both ends deserve equal pacing. Breathing animations. Background ambient motion.

**Why:** Neither end is arrival or departure; both are held states. Symmetric easing gives them equal weight.

**AE:** F9 (Easy Ease) applies symmetric ease-in-out. It's a reasonable starting point; adjust velocity handles for the specific mood.

**bpy:** `BEZIER` interpolation with symmetric handles on both keyframes.

**Caution:** Ease-in-out on entrances and exits gives motion a "floating" quality that reads as weightless or ungrounded. Sometimes that's the brief. Usually it isn't.

---

## Linear

**When:** Countdowns and timers (the clock metaphor demands it). Progress bars with precise correspondence to elapsed time. Mechanical readouts. Type-on effects where each character appears at a uniform rate. Data visualization that encodes time.

**Why:** Linear easing communicates precision and mechanism. It's the only appropriate default for things that must feel like a machine.

**Common mistake:** Linear as a starting point because it's the default. Linear should be a deliberate choice, not the absence of a choice.

---

## Custom bezier

**When:** Any motion with a specific physical metaphor that none of the above cover cleanly. Springs. Snaps. Material drag. Overshoot followed by settle.

**AE:** Drag the velocity handles in the graph editor. A snap looks like: very fast in the middle, tight handles on both ends. A spring looks like: ease-out followed by a small ease-back past the target (overshoot), then forward again (settle). For overshoot without expressions, use an extra keyframe past the target, then a final keyframe at the target.

**bpy:** Edit the F-curve handles directly in the Graph Editor. `FREE` handle type gives full control. Use the Noise F-Curve modifier sparingly for organic drift.

**Reference curves for common moods:**

| Mood | Description |
|---|---|
| Snap | Near-linear with very fast peak velocity, tight settle at end |
| Bounce settle | Ease-out, slight overshoot, settle, better done with inertial expression in AE; explicit keyframes in bpy |
| Heavy drag | Slow, weighted entrance, very shallow start, steep middle, near-flat end |
| Elastic | Overshoot in both directions before settling, use expressions in AE; F-curve modifier in bpy |

---

## Bezier control point conventions

**After Effects (graph editor):**
- The horizontal axis is time; the vertical axis is value.
- The handles control velocity: a handle pulled far horizontally = slow velocity at that keyframe. A handle pulled close = fast velocity.
- Spatial handles (comp view) control the motion path curve. These are separate from temporal handles.
- Temporal and spatial handles are independent. Adjusting one does not affect the other.

**Blender (Graph Editor):**
- Same axis convention: horizontal = time (frames), vertical = value.
- Handle types: `AUTO` (default, smooth), `AUTO_CLAMPED` (smooth, won't overshoot), `VECTOR` (straight linear segments), `FREE` (manual), `ALIGNED` (moves both handles together).
- For most motion graphics: start with `AUTO_CLAMPED`, switch to `FREE` where precise velocity control is needed.
- In Python (`bpy`): set `keyframe_points[i].handle_left_type = 'FREE'` and set `handle_left` and `handle_right` coordinates explicitly.

---

## Common easing errors to name on sight

| What you see | What it means | Fix |
|---|---|---|
| Linear entrance or exit | Default, no decision made | Ease-out on entrance, ease-in on exit |
| Ease-in-out on an entrance | Floaty start, element isn't clearly arriving | Switch to ease-out |
| Everything the same easing | Easing was applied globally, not per-element | Per-element easing based on function |
| Fast ease-out overshoot that doesn't settle | Overshoot without decay | Add follow-through keyframe or inertial expression |
| Perfectly symmetric bounce | Keyframe ping-pong, not physics | Decay the bounce, each cycle should be shorter than the last |

---

## 📄 SOURCE FILE: `skills/motion-design/references/timing-and-spacing.md` (verbatim)

# Timing and Spacing

Two different things. Conflating them is where most motion decisions go wrong.

---

## The distinction

**Timing** is when things happen. The start frame of a move. The moment a beat lands.

**Spacing** is how values are distributed between those moments. Dense spacing near a keyframe = slow. Sparse spacing = fast. This is easing. Timing and spacing are independent variables.

You can have good timing (moves land on the right beats) with bad spacing (linear between keyframes, no weight). You can have good spacing (perfect ease-out) with bad timing (everything moves at once, nothing reads).

Both have to be right.

---

## Duration as a design variable

Duration encodes weight. This is not a metaphor, it is how viewers read physicality in motion.

| Duration | What it reads as |
|---|---|
| Under 150ms | Instant, mechanical, system-level |
| 150–250ms | Light, responsive, UI-scale |
| 250–500ms | Standard, intentional, most brand motion |
| 500ms–1s | Heavy, deliberate, editorial |
| Over 1s | Cinematic, slow-motion, or simply too slow |

A large heavy logo entering at 200ms reads as wrong. A light notification badge at 800ms reads as broken. Match duration to the physical metaphor of the element.

---

## Stagger

Stagger is the offset between elements that should move as a group but not simultaneously. It is the primary tool for creating hierarchy through timing.

Without stagger: everything moves at once, the eye has no path, nothing reads as primary.

With stagger: the first element moving establishes a direction, subsequent elements confirm it, the sequence reads as intentional order.

**Stagger values for motion graphics:**

| Context | Stagger range |
|---|---|
| Tight (letters, tightly related elements) | 20–50ms |
| Standard (list items, cards, words) | 50–100ms |
| Loose (sections, large elements with visual separation) | 100–200ms |

Stagger direction matters. Top-to-bottom or left-to-right stagger reinforces reading direction. Starting from the visual center and radiating outward works for reveals. Reverse stagger (last-to-first) for exits.

---

## Offset

Offset is stagger applied to follow-through: when parts of a multi-element object settle at different times.

In a text lockup: the primary word settles, then the secondary line settles 80ms later, then a supporting badge settles 80ms after that. No single element defines the endpoint, the stack lands in sequence.

Offset is not the same as delay. Delay postpones a move entirely. Offset lets the whole group start moving together but arrive at different times.

---

## Anticipation timing

Anticipation is brief. Rule: anticipation should be 20–30% of the main action duration.

If a main move is 400ms, anticipation is 80–120ms. Longer than that and the anticipation becomes the animation; shorter and it disappears.

Anticipation magnitude: small. An anticipation that travels 20px before a move that travels 300px is correct. An anticipation that travels 80px for the same move is a cartoon.

---

## Follow-through timing

Follow-through is also brief. Elements that continue past their target should overshoot by 10–20% of the main move distance, then settle in 20–40% of the main action duration.

Main move: 300px over 400ms. Overshoot: 30–60px. Settle: 80–160ms.

If the follow-through takes longer than the main action, the motion reads as a bounce animation, not a settle.

---

## Hierarchy through timing: the rule

The primary element moves first. Supporting elements follow. Decorative elements follow last.

In a logo reveal:
1. Primary mark (50ms head start)
2. Wordmark (stagger from mark, 80ms offset)
3. Tagline (200ms after wordmark starts)
4. Background texture or ambient elements (last, slowest)

If any element in the hierarchy draws the eye before the primary mark does, it is either moving too early or moving too fast. Fix the timing first; don't fix it by slowing everything down uniformly.

---

## Rhythm

When an animation has multiple sequential beats, they should feel rhythmic: not metronomic (exactly equal intervals), but musically paced (like a sentence with natural cadence).

A sequence of reveals at exactly 200ms, 400ms, 600ms, 800ms is a metronome. It reads as software, not craft.

A sequence at 0ms, 180ms, 340ms, 550ms has phrasing. Elements cluster slightly, breathe slightly. That's rhythm.

There is no formula for rhythm. The test is: does the timing map onto a phrase you can speak aloud at a natural cadence? If yes, it has rhythm.

---

## 📄 SOURCE FILE: `skills/motion-design/references/defaults-to-avoid.md` (verbatim)

# Defaults to Avoid

The tells that mark motion as auto-generated or unconsidered. Name them when you see them. Replace them with decisions.

---

## Linear easing

**What it looks like:** Value changes at a perfectly constant rate from start to end. No acceleration, no deceleration.

**Why it's wrong:** Nothing in the physical world moves linearly. Linear motion reads as mechanical or digital in a way that breaks immersion in brand and product motion.

**Fix:** Ease-out for entrances. Ease-in for exits. Custom bezier for specific moods. Reserve linear for countdowns and machines, things that are supposed to feel mechanical.

---

## Everything moves at once

**What it looks like:** All elements in a scene start animating on the same frame and end on the same frame. The whole screen changes simultaneously.

**Why it's wrong:** The eye has nowhere to go. There is no visual sentence, just noise. The designer has handed off timing decisions to the software.

**Fix:** Stagger. Define the primary element, animate it first. Secondary elements follow with 50–100ms offset. Decorative elements follow last. See `timing-and-spacing.md`.

---

## Equal-duration everything

**What it looks like:** Every animation in the comp is 300ms (or 250ms, or 400ms, pick a number). A logo reveal, a text fade, and a background element all take the same amount of time.

**Why it's wrong:** Duration encodes weight. When every element has the same duration, no element has more weight than any other. The motion has no hierarchy.

**Fix:** Match duration to the physical metaphor and visual weight of each element. Heavy elements take longer. Light elements take less time.

---

## Default wiggle on Position

**What it looks like:** `wiggle(5, 20)` applied to a layer's position to add "organic movement." The result is random jitter with no relationship to the motion happening around it.

**Why it's wrong:** Wiggle with defaults communicates that you wanted organic motion but didn't design it. It's a placeholder used as a finish.

**Fix:** If you need ambient drift, use a slow, low-amplitude wiggle (`wiggle(0.5, 6)`) that is almost invisible. If you need controlled oscillation, use `Math.sin` with explicit frequency and amplitude. If you need post-action vibration, use a decaying oscillation expression, not raw wiggle. See `expressions.md` in the aftereffects-motion skill.

---

## No anticipation

**What it looks like:** A large fast element appears to move from rest with no wind-up. The motion starts abruptly at the in-keyframe.

**Why it's wrong:** Without anticipation, fast moves read as sudden and jarring. The eye hasn't been prepared for where the motion is going.

**Fix:** Add an anticipation keyframe before the main action. Duration: 20–30% of the main action. Distance: 10–20px in the opposite direction. Then into the main action at full force.

---

## No follow-through

**What it looks like:** Every element stops dead at its final keyframe. The whole comp "lands" at one frame and freezes.

**Why it's wrong:** Physical objects with momentum don't stop cleanly. The absence of follow-through is what makes motion graphics look like PowerPoint.

**Fix:** Allow elements to slightly overshoot their target, then settle. See `timing-and-spacing.md` for follow-through timing rules. Use an inertial bounce expression in AE for automatic settle.

---

## Symmetric bounce

**What it looks like:** An element bounces with equal height on each bounce. The animation loops perfectly.

**Why it's wrong:** This is a ping-pong between two keyframes. Physical bounces decay, each bounce is smaller than the last. A symmetric bounce reads as a toggle, not physics.

**Fix:** Add decay. Each cycle should be shorter in both duration and amplitude. If you want a loop, use a looping expression on a decaying pattern, not a keyframe ping-pong.

---

## Every layer on the same timeline marker

**What it looks like:** All layers in the comp start at frame 0. The whole scene builds from one moment with no pre-positioning or staggered entry.

**Why it's wrong:** This is the default state when you drop layers into AE without thinking about flow. It compounds the "everything moves at once" problem.

**Fix:** Position layer in-points across time deliberately. Layers that enter later should start later. Background elements can start at frame 0 if they establish the space; foreground elements should enter after the space is set.

---

## 2-second default duration

**What it looks like:** Comp duration is 2s and the animation roughly fills it end-to-end because that was the comp length. Or everything is 2s because AE's default layer duration is 2 seconds.

**Why it's wrong:** Duration should come from the brief, the platform, and the motion's physical metaphor, not from AE's default layer length.

**Fix:** Set comp duration based on what the motion needs. Edit layer in-points and out-points intentionally. Never let a default duration make a timing decision.

---

## Opacity as the only entrance mechanic

**What it looks like:** Every element fades in. The reveal is accomplished entirely by opacity keyframes from 0 to 100.

**Why it's wrong:** A pure fade communicates nothing about where an element came from or how it relates to the rest of the design. It is the absence of a motion decision.

**Fix:** Pair opacity with a position or scale move. The fade provides the transition; the position or scale provides the direction and weight. Exceptions: very subtle, background-level elements where a fade is correct because the element should not draw attention.

---

## Generic "glowing" or "lens flare" punctuation

**What it looks like:** A glow effect, lens flare, or streak applied at the moment an element arrives to "add energy."

**Why it's wrong:** These are stock motion graphic punctuation marks. They read as the designer not knowing how to make the motion itself carry energy.

**Fix:** If the motion needs energy, the motion itself should provide it. Faster entrance, higher initial velocity, more decisive easing. Effects are decoration; timing and easing are the work.

---

## 📄 SOURCE FILE: `skills/motion-design/references/composition-for-motion.md` (verbatim)

# Composition for Motion

Static composition rules apply to motion, but the frame changes over time. That changes everything.

---

## The moving frame problem

In a still design, the composition is fixed. The viewer's eye can scan at will.

In motion, the composition at frame 0 is different from frame 60 and frame 120. The designer is responsible for every frame in between, not just the start and end states. A transition that passes through a compositionally broken midpoint is a broken transition.

Check the midpoint. Always.

---

## Negative space over time

Static design uses negative space to create breathing room and direct the eye.

In motion, negative space is dynamic. An element moving into a corner compresses the negative space in that corner. An element scaling up can fill negative space that was deliberately there at the start state.

Rules:
- Plan where negative space will be at each key moment in the animation.
- Avoid midpoints where negative space is distributed accidentally (e.g. two elements in opposite corners, equidistant from center, creating dead symmetry during a transition).
- Entering elements should move from a dead zone (outside frame, or an area of planned negative space) toward the point of highest compositional interest.

---

## Entry and exit paths

Where an element comes from communicates intent.

| Entry direction | Reads as |
|---|---|
| From bottom | Rising, elevation, growth |
| From top | Dropping, falling, authority |
| From leading edge (left in left-to-right reading) | Forward, arrival, natural reading direction |
| From trailing edge (right) | Retreat, secondary, or deliberate reversal of expectation |
| Scale from center | Materializing, emerging, zoom focus |
| Scale from a functional point | Connected to that point (a button that expands into a panel) |
| Fade only | System-level, no physical metaphor intended |

Exit paths should be the inverse of the entry, unless the narrative demands otherwise. An element that entered from the bottom should exit toward the bottom. Breaking this reads as teleportation.

---

## Focal hierarchy in motion

In a still design, focal hierarchy is set by size, color, contrast, and position.

In motion, timing is an additional hierarchy signal. The first thing to move draws the eye. The fastest thing to move draws the eye. Use both deliberately.

If the wrong element is drawing first attention, either:
- Delay its movement so the primary element moves first, or
- Slow it down so the primary element is faster and more decisive.

---

## Reading direction and motion direction

Motion that travels in the same direction as the reading language (left-to-right) feels natural and progressive. Motion that travels against it can feel like retreat or reversal.

Use directional rules to reinforce narrative:
- Forward motion (left-to-right) for advancement, next steps, progress.
- Backward motion (right-to-left) for going back, undo, history.
- Vertical motion for hierarchy shifts (deeper = downward, elevated = upward).
- Scale changes (grow) for gaining importance; scale changes (shrink) for receding.

Mixing directional metaphors in the same sequence creates confusion. Pick a direction for each spatial relationship and hold it across the piece.

---

## Anchoring

Elements should feel anchored to the design grid, not floating independently.

When multiple elements move: if they all have a relationship to a common axis or anchor point, have them reference it. A lockup that reveals outward from the logo center feels grounded. A lockup where each element flies in from a random direction feels like clip art.

In practice: define your center of composition before building. Everything moves toward or away from that anchor, not arbitrarily.

---

## The frame edge

Screen edges are walls. Motion toward an edge is directional. Motion away from an edge is an arrival.

Elements that exit off-frame feel like they've moved to another place. Elements that disappear in place feel like they've ended. Choose which you want based on whether the element is leaving the scene permanently or temporarily.

Elements that stop exactly at the frame edge (cropped composition) should stay there with purpose. A random crop that happens to land at the edge reads as a mistake.

---

## Camera in motion design

Even in 2D work, the camera can move. Zooms and pans in AE are not camera moves; they are scale and position changes on a composition. But they read as camera moves to the viewer.

Zoom into a subject: increases intimacy, makes it feel significant.
Zoom out: reveals context, suggests the viewer is gaining perspective.
Pan: follows a subject, or reveals what was off-screen.

Do not zoom and pan simultaneously unless you are intentionally simulating a camera with drift. Random simultaneous zoom-pan reads as instability, not dynamism.

---

## 📄 SOURCE FILE: `skills/motion-design-critique/SKILL.md` (verbatim)

---
name: motion-design-critique
description: Use this skill when something has gone wrong, looks wrong, or needs a second opinion. Triggers on: "something looks off", "this doesn't look right", "why is this happening", "script error", "render artifact", "the timing feels wrong", "animation looks robotic", "AE error", "bpy error", "Blender crashed", "nothing is moving", "wrong position", "wrong keyframe", "expression error", "the material looks fake", "shadows are wrong", "why does this look cheap", "critique this", "review this", "what's wrong with". Also triggers when the user is stuck and doesn't know why. Works with or without MCP attached.
---

# Motion Design Critique

You are a senior motion designer doing a diagnostic. Something is wrong. Your job is to find it and fix it, not to soften the feedback.

## What you are not

- Not a sympathetic listener. Don't validate the problem, fix it.
- Not vague. "The easing feels off" is not useful. Name the specific parameter, the specific frame, the specific value. Give the fix.
- Not a tutorial. The user is a designer. They want the diagnosis and the patch, not a lesson.
- Not guessing. If you don't have enough information to diagnose, ask for the one thing you need: a screenshot at a specific time, an error message, a state dump, the script that ran. One question, not five.

## Diagnostic modes

**Mode 1. Visual critique.** The output looks wrong. The user has a screenshot or a description.
Load `references/visual-diagnostics.md`. Identify the specific problem. Give the fix.

**Mode 2. Script / expression error.** A JSX script or bpy script threw an error. The user has an error message.
Load `references/ae-diagnostics.md` (for AE) or `references/blender-diagnostics.md` (for Blender). Find the error pattern. Give the patch.

**Mode 3. Motion quality review.** The animation runs but feels wrong: robotic, default, weightless, overly mechanical.
Load `references/visual-diagnostics.md`. Run through the defaults-to-avoid checklist. Name every problem you see. Rank by impact. Fix the highest-impact ones first.

**Mode 4. Render problem.** The render output has artifacts, wrong colors, missing objects, or unexpected results.
Load `references/blender-diagnostics.md`. Run the pre-render checklist against what the user describes.

## Hard rules

1. One diagnosis at a time. Fix the highest-impact problem. Don't hand the user a list of ten things to change simultaneously.
2. Screenshots are primary evidence. Ask for one before guessing. Specify the timestamp and what panels to include.
3. State dumps are better than speculation. If the script state might have diverged from what you know, ask for a state dump before patching.
4. Every patch must be idempotent. A diagnostic script that fixes something should be safe to re-run.
5. Save before patching. Always say "Cmd+S first" before any AE script. In Blender, tell the user to save before running a destructive bpy operation.

## What good diagnosis looks like

Bad: "The timing seems a bit off, you might want to adjust the easing."

Good: "The entrance is using ease-in-out when it should be ease-out. The slow start at the beginning is fighting the eye as the element enters the frame. Set the outgoing velocity handle on the first keyframe to ~80% and bring the incoming handle on the second keyframe flat. That removes the slow start without changing the settle."

Name the problem. Name the location. Give the value. Give the fix.

## When to load which reference

| Situation | Load |
|---|---|
| Motion looks robotic, default, or unconvincing | `references/visual-diagnostics.md` |
| AE script error, expression error, MCP not responding | `references/ae-diagnostics.md` |
| Blender bpy error, render artifact, material wrong, MCP issue | `references/blender-diagnostics.md` |
| Higgsfield Bridge not responding, generated asset wrong | Higgsfield section of `ae-diagnostics.md` or `blender-diagnostics.md` |

---

## 📄 SOURCE FILE: `skills/motion-design-critique/references/ae-diagnostics.md` (verbatim)

# AE Diagnostics

Script errors, expression errors, MCP failures, and common AE states that go wrong. Read the error message first, then find the matching pattern below.

---

## Script errors (JSX)

### "undefined is not an object" / "Cannot read property of null"

The script is trying to access a layer, property, or comp that doesn't exist.

Common causes:
- `comp.layer("SomeName")` where "SomeName" is not the exact layer name (case-sensitive, space-sensitive).
- `app.project.activeItem` returns null because no comp is open or selected.
- A shape group name has changed since the script was written.

Fix:
```js
// safe layer access
var layer = null;
for (var i = 1; i <= comp.numLayers; i++) {
    if (comp.layer(i).name === "ExactLayerName") {
        layer = comp.layer(i);
        break;
    }
}
if (!layer) { alert("Layer not found."); }
```

Run a state dump (`_dump_state.jsx`) to get the exact layer names as AE sees them. See `aftereffects-motion/references/scripting-patterns.md`.

---

### "KeyframeInterpolationType is not defined"

Using `KeyframeInterpolationType.BEZIER` before AE has loaded the enum. This sometimes happens at the top of a script before `app` is fully initialized.

Fix: move all `KeyframeInterpolationType` usage inside a function body, or wrap in a short wait:
```js
app.beginUndoGroup("MyScript");
// ... all your code here, including KeyframeInterpolationType usage
app.endUndoGroup();
```

---

### "After Effects error: can't add keyframe to locked property"

The property is locked (padlock icon on the layer or property) or the layer is shy.

Fix: unlock the layer before scripting:
```js
comp.layer("LayerName").locked = false;
```

---

### "Expression disabled" / expression turns red in AE

The expression has a syntax error or references a property that doesn't exist.

Ask the user to paste the exact expression text and the red error tooltip. Common causes:

| Error | Cause | Fix |
|---|---|---|
| `thisComp.layer("X")` errors | Layer renamed or deleted | Update the layer name reference |
| `comp is not defined` | Using `comp` outside an expression context | Use `thisComp` inside expressions |
| `Error: index out of range` | `numKeys` is 0 but expression accesses `key(1)` | Add a null check: `if (numKeys > 0)` |
| `undefined` value | Property path is wrong | Check `layer.transform.position` vs `layer.property("Transform").property("Position")` |

---

### Script runs but nothing changes

Most common cause: the script ran on the wrong comp or the wrong layer.

Diagnostic:
```js
alert("Active item: " + (app.project.activeItem ? app.project.activeItem.name : "none"));
```

If the active item is wrong, the user needs to click into the correct comp in the Project panel before running the script.

Second cause: the script changed values but at time 0, and the playhead is parked at a different time. The value is set; it just isn't visible at the current time.

---

### Script stacks duplicates on re-run

The script is not idempotent. It is adding layers or effects without checking if they already exist.

Fix: every script that creates named layers must have cleanup logic at the top that removes those layers before re-creating them. See the idempotent template in `aftereffects-motion/references/scripting-patterns.md`.

---

## MCP failures

### MCP calls hang or return no response

The bridge panel is closed or the checkbox is unticked.

Fix: tell the user to reopen `Window > mcp-bridge-auto.jsx` in AE and tick "Auto-run commands."

If the panel is open and ticked but still hanging: AE may be busy (rendering, running a long preview, blocked by an alert dialog). Check the AE window for any dialog or modal that needs dismissing.

---

### MCP returns success but AE didn't change

The bridge ran the command in a different comp than expected, or the command targeted a layer by index and the layer order changed.

Fix: always target layers by name, not by index. After any operation the user might have done manually (reordering layers, renaming), run a state dump before assuming the current structure matches what the script expects.

---

### `run-script` predefined script returns stale data

`getLayerInfo` and `getProjectInfo` return a snapshot. If the user modified the comp since the last call, the data is stale.

Fix: call the state dump script and read the fresh JSON. Do not patch based on data from a prior `getLayerInfo` call if the user has touched the comp.

---

## Higgsfield Bridge failures

### Bridge tools missing or calls fail with an auth error

The bridge isn't registered or the sign-in expired.

Fix: confirm `HiggsfieldBridge` shows in the agent's MCP list (`claude mcp list` or `codex mcp list`). Re-authenticate (`/mcp` in Claude Code, `codex mcp login HiggsfieldBridge` in Codex).

---

### Bridge connects but nothing lands in AE

The Higgsfield panel is closed or signed out, or AE is older than 2024 (24.0).

Fix: Window > Extensions > Higgsfield AI, sign in, keep the panel open. If AE is 2023 or older, the plugin won't run. There is no workaround.

---

### Generation fails partway or returns nothing

Usually out of credits or hitting a plan rate limit. Ask the user to check their balance in the panel. Don't retry in a loop; one retry after a yes.

---

### JSX targets the wrong layer after a bridge operation

The bridge added layers and shifted the stack. The script was written against a pre-bridge state.

Fix: state dump, then rewrite the JSX to target layers by name. See `aftereffects-motion/references/higgsfield-bridge.md`.

---

### Remove Background edges chatter or fringe

Check at 200% on a hair or motion-blur frame. If the key is soft, a Refine Soft Matte pass on the keyed layer usually beats regenerating. Regenerate only if the subject is lost on whole frames.

---

## Render and playback issues

### RAM preview is slow / choppy

AE is not fully caching to RAM before playing. This is a performance issue, not an animation problem.

Tell the user: "Hit 0 on numpad to start RAM preview. Wait until the green bar fills the timeline range before it plays back. The first pass caches; the second plays at full framerate."

This is not a script fix. Do not try to resolve this via MCP.

---

### Final render output looks different from comp preview

Common causes:
- Color profile mismatch: comp is sRGB, output module is set to a different profile.
- Effects using GPU acceleration in preview, falling back to software in render.
- Draft quality was on during preview.

Ask the user: "Did you render as PNG sequence or H.264 directly from AE?" If H.264: "H.264 rendered from AE has lossy color. Render as PNG sequence and compare a single frame before calling it a render artifact."

---

### Script ran, AE crashed on undo

AE's Undo is unreliable after script operations. If the user is reporting that Cmd+Z crashed or trashed their project after a script ran:

"AE's Undo can't reliably reverse all script operations. The safest recovery is your most recent save. Always Cmd+S before running any non-trivial script. Going forward, scripts from this workflow will always remind you to save first."

There is no code fix for this. It is a known AE limitation. See `aftereffects-motion/references/limits-and-pitfalls.md`.

---

## 📄 SOURCE FILE: `skills/motion-design-critique/references/visual-diagnostics.md` (verbatim)

# Visual Diagnostics

For when the animation runs but looks wrong. Work through this list from top to bottom. Stop at the first match and fix it before moving to the next.

---

## Diagnostic checklist

**1. Is easing linear?**
Check the first and last keyframes of every moving property. If the interpolation is linear, that is the problem. Linear easing reads as mechanical and artificial in any motion graphics context that isn't a machine or countdown.
Fix: ease-out on entrances, ease-in on exits, ease-in-out on loops.

**2. Is everything moving at once?**
If all layers start and end their animation on the same frames, there is no hierarchy. The eye has no entry point.
Fix: stagger by 50–100ms between elements. Primary element first, secondary follows, decorative last. See `motion-design/references/timing-and-spacing.md`.

**3. Does everything have the same duration?**
If a heavy logo and a light caption both animate over 300ms, the motion has no weight differentiation.
Fix: heavy elements take longer (400–600ms). Light elements take less (150–250ms). Duration encodes weight.

**4. Is there anticipation before fast moves?**
A fast entrance with no wind-up reads as a sudden pop. If the move is aggressive (high velocity, large displacement), it needs anticipation.
Fix: add a keyframe 80–120ms before the main action, displaced 15–25px in the opposite direction of travel. Then into the main move.

**5. Is there follow-through after the settle?**
All elements stopping on the exact same frame reads like a PowerPoint slide change.
Fix: offset the final keyframe of secondary and decorative elements by 3–6 frames after the primary lands. Or add a slight overshoot keyframe 3–5 frames past the target, then settle back.

**6. Does the animation pass through a broken midpoint?**
At 50% through any transition, take a screenshot. Does the frame look like a deliberate design state, or like elements in transit to somewhere else? If the midpoint looks accidental, the motion path or easing needs adjustment.
Fix: check spatial handles (AE) or F-curve handles (Blender). The motion path between keyframes should be clean.

**7. Is wiggle being used without purpose?**
Raw `wiggle(5, 20)` on a Position property reads as "I added organic motion without designing it."
Fix: either justify the wiggle (slow ambient drift: `wiggle(0.5, 6)`) or replace it with a specific motion decision. See `aftereffects-motion/references/expressions.md`.

**8. Is the motion too slow or too fast for the visual weight?**
A small, light UI element animating over 1 second reads as broken. A heavy logo animating over 80ms reads as a glitch.
Fix: see timing table in `motion-design/references/timing-and-spacing.md`.

**9. Is the easing symmetric when it should be asymmetric?**
A bouncing element that bounces with equal height each time is a ping-pong between keyframes, not physics. Each bounce should be shorter than the last.
Fix: in AE, use the inertial bounce expression from `aftereffects-motion/references/expressions.md`. In Blender, add a Noise F-curve modifier with decay, or manually reduce amplitude per cycle.

**10. Is opacity the only entrance mechanic?**
A pure fade-in communicates nothing about where the element came from. It is the absence of a motion decision.
Fix: pair opacity with a position or scale move. The fade is the transition vehicle; the position or scale provides the direction and weight.

---

## How to request more information

If the above checklist doesn't identify the problem from a description alone, ask for:

- A screenshot at the specific timestamp where it looks wrong (e.g. "screenshot at 1.5s with comp panel at 100% zoom").
- If timing is the question: two screenshots, one at the start of the problematic range and one at the end.
- If layering is the question: a timeline screenshot showing layer in/out points and keyframe positions.
- If the problem is motion path: a comp screenshot with motion paths visible (View > Show Layer Controls).

One request. Be specific about what you need and why.

---

## Common describes and their translations

| The user says | What it actually means |
|---|---|
| "Looks robotic" | Linear easing, simultaneous animation, or no anticipation/follow-through |
| "Looks cheap" | Default easing, no weight differentiation, or opacity-only entrances |
| "Too fast" | Duration too short for the visual weight of the element |
| "Too floaty" | Ease-in-out on an entrance (slow start fights the eye); or overshoot without decay |
| "Looks like a slideshow" | No stagger, everything moves at once, no follow-through |
| "Feels flat" | No depth cues: no stagger, no size differentiation, no motion path arcs |
| "Doesn't feel premium" | Default easing, missing anticipation, or wiggle without purpose |
| "The bounce looks fake" | Symmetric bounce, needs decay per cycle |
| "Letters look the same" | Stagger too large or too small, or same easing on every character |
| "The settle looks off" | Overshoot too large, or decay too slow, adjust amplitude and decay rate |
