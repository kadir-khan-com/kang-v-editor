# iart-ai/motion-design-skills — Motion Design Skills (After Effects skill)
- Repo: iart-ai/motion-design-skills
- Link: https://github.com/iart-ai/motion-design-skills
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 201 stars, 35 forks, 21 commits (repo page, 2026-11-06)
- Last commit (from local clone git log): 2026-06-22
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Skill pack (9 skills); extracted here is ONLY the After Effects skill — SKILL.md (routing hub: expressions & rigging, MOGRT/Essential Graphics, export recipes, performance triage, project hygiene) + all 5 references, including the expression-library cookbook (wiggle / loopOut / inertial bounce / seedRandom / valueAtTime patterns). The pack's animation-principles skill is editor-agnostic (a separate AE principles file from dylantarre is in this round); beat-sync-editing / remotion-video / logo-animation etc. are out of this round's editor scope. 3 small utility scripts in skills/after-effects/scripts/ (sequential-offset, batch-rename, apply-effect-to-layers) are machinery — listed here, not extracted.

---

## 📄 SOURCE FILE: `skills/after-effects/SKILL.md` (verbatim)

---
name: after-effects
description: This skill should be used when the user asks anything about Adobe After Effects — to "write an After Effects expression", "make a wiggle / loopOut / inertial bounce", "rig a control with a slider / null", "build a MOGRT / Essential Graphics template", "export AE to Lottie or Media Encoder"; OR to "export from After Effects", "export with transparency / an alpha channel", "fix a black background on export", "choose ProRes vs H.264", "which codec / what bitrate for 1080p / 4K", "stop H.264 disappearing from the Render Queue"; OR when "After Effects is slow / laggy / crashing / froze", "RAM preview won't play in real time", "AE is using all my memory / render takes forever", "how do I speed up After Effects"; OR to "organize my After Effects project", "relink missing footage", "fix broken links after moving files", "set a folder structure / naming conventions", "batch rename layers", or "write an ExtendScript / .jsx script". Covers expressions & rigging, export recipes, performance triage, and project hygiene.
version: 0.1.0
---

# After Effects

After Effects is GUI software, so this skill delivers knowledge and ready-to-paste assets — expressions, rig setups, export checklists, diagnostic flows, naming schemes, and ExtendScript — rather than a rendered file. It is a hub covering four domains; route to the matching reference for depth and complete recipes.

## Routing

| If the user wants to… | Go to |
|---|---|
| Write/debug an expression, rig sliders & nulls, build a MOGRT, export to Lottie | `references/expressions.md` (deep cookbook in `references/expression-library.md`) |
| Choose a codec/container, export with alpha, fix a black background, set bitrate, recover H.264 | `references/export-recipes.md` |
| Fix slow/laggy previews, slow renders, crashes, freezes, out-of-memory | `references/performance-triage.md` |
| Organize the project, relink missing footage, set naming/folders, batch-automate with .jsx | `references/project-hygiene.md` |

The `.jsx` automation scripts live in `scripts/`.

## Expressions & rigging

Expressions are JavaScript evaluated on the property they are pasted on; `value` is that property's value, `time` is comp time in seconds, and `index`, `thisLayer`, `thisComp` are in scope. An expression overrides keyframes unless it incorporates `value`.

```js
wiggle(2, 30);            // 2 wiggles/sec, amplitude 30 (property units)
loopOut("cycle");         // repeat keyframed range forever; "pingpong" / "offset" / "continue"
seedRandom(index, true);  // stable-but-unique per layer (timeless) before random()/wiggle()
thisComp.layer("Lead").transform.position.valueAtTime(time - 0.2 * index);  // staggered echo
```

Inertial bounce (overshoot/settle after the last keyframe) and the full loop/wiggle/rigging set are in `references/expressions.md`.

Rig controllable motion: add a null with **Slider / Checkbox / Color / Angle / Point** control effects, then reference them and parent transforms to drive many layers from one.

```js
ctrl = thisComp.layer("Controls");
amt  = ctrl.effect("Intensity")("Slider");   // Checkbox → 1/0, Color → [r,g,b,a]
value * amt;
```

Expose those controls via **Window → Essential Graphics** and **Export Motion Graphics Template** (.mogrt) for Premiere/AE editors.

## Export recipes

Two engines, and choosing wrong is the root of most export confusion:
- **Render Queue (RQ)** — masters/intermediates: ProRes, image sequences, lossless, alpha.
- **Adobe Media Encoder (AME)** — delivery: H.264 MP4, H.265, social presets.

Since AE CC 2014/2015 the native **H.264 output module was removed from the RQ** — make MP4s in AME, not the RQ. **H.264/MP4 cannot store alpha**, so a transparent comp exported to H.264 always fills with black; that is the classic "black background" complaint and not a bug. For transparency use **ProRes 4444**, a **PNG/TIFF sequence**, or **HEVC-alpha (Safari) + VP9/WebM-alpha (Chrome)**, with Output Module **Channels: RGB + Alpha**.

Quick targets: editor handoff → **ProRes 422 HQ**; master/grade or alpha → **ProRes 4444**; web/social/client → **H.264 via AME**, VBR 2-pass (~10–16 Mbps 1080p, ~35–45 Mbps 4K). Full matrix, social specs, and step-by-step alpha exports in `references/export-recipes.md`.

## Performance triage

Work top-down by symptom, cheapest fix first, and stop when it clears. Most settings are in `Edit > Preferences` (Win) / `After Effects > Settings` (Mac).

- **Slow previews:** Half/Third resolution → enable **Multi-Frame Rendering** → raise RAM allocation (leave ~6 GB for OS) → Adaptive fast previews → purge cache → Disk Cache on SSD/NVMe → solo heavy layers/effects → HW-accelerated decode → proxy heavy comps.
- **Slow renders:** confirm MFR on → RQ for masters / AME for delivery → HW decode H.264 → pre-render slow precomps → cheaper effects → transcode long-GOP to ProRes.
- **Crashes/freezes:** purge + empty disk cache → update **NVIDIA Studio** (not Game-Ready) drivers → reset prefs (`Ctrl/Cmd+Alt+Shift` on launch) → pull third-party plugins → free disk space → disable MFR if MFR-specific → roll back AE after a bad update.

MFR needs several GB RAM per active core. Ordered flows, exact preference paths, and the proxy workflow are in `references/performance-triage.md`.

## Project hygiene

Keep projects organized, portable, and automatable.

- **Folders:** numeric-prefixed bins (`01_Comps`, `02_Precomps`, `03_Footage`, …, `99_Old`) for stable sort order.
- **Naming:** `PROJECT_section_descriptor_v01`; precomps `PRE_`; rename solids/nulls to their role (`CTRL_master`); no spaces/special chars for farm/cross-OS safety.
- **Broken links:** AE references footage by path, so moving files breaks links. Double-click a missing item → **Replace Footage > File** and AE relinks the whole folder at once; enumerate with `File > Dependencies > Find Missing Footage`. **Always hand off projects via `File > Dependencies > Collect Files`**, never a bare `.aep`.
- **ExtendScript (.jsx):** wrap batches in `app.beginUndoGroup(...) / app.endUndoGroup()`; apply effects by **matchName** (e.g. `"ADBE Gaussian Blur 2"`), not the display name. Ready scripts: `scripts/batch-rename.jsx`, `scripts/sequential-offset.jsx`, `scripts/apply-effect-to-layers.jsx`.

Full naming scheme, label-color system, relink/Collect-Files/Reduce workflows, and scripting setup in `references/project-hygiene.md`.

## Reference files

- `references/expressions.md` — expressions, rigging, MOGRT, Lottie/Media Encoder basics.
- `references/expression-library.md` — deeper expression cookbook: tuned inertial bounce, all loop variants, advanced wiggle, valueAtTime echoes, seedRandom grids, full rigging + coordinate spaces, MOGRT and Lottie/Bodymovin steps, Media Encoder presets.
- `references/export-recipes.md` — full codec/alpha/bitrate matrix, per-platform social specs, step-by-step transparency exports, AME preset cautions.
- `references/performance-triage.md` — ordered preview/render/crash flows, preference paths and values, MFR/GPU/disk-cache tuning, pre-render & proxy workflow.
- `references/project-hygiene.md` — folder template, naming and label systems, relink/Collect Files/Reduce details, scripting setup.
- `scripts/batch-rename.jsx`, `scripts/sequential-offset.jsx`, `scripts/apply-effect-to-layers.jsx` — ExtendScript automations.
</content>

---

## 📄 SOURCE FILE: `skills/after-effects/references/expressions.md` (verbatim)

# Expressions, Rigging & MOGRT

After Effects is GUI software, so this delivers knowledge: ready-to-paste JavaScript expressions, rigging setups that make motion controllable, and template/export pipelines. Expressions read on the property they are pasted on; `value` is that property's keyframed/static value, `time` is the composition time in seconds, and `index`, `thisLayer`, `thisComp` are in scope.

For a deeper cookbook (tuned inertial bounce, every loop variant, advanced per-axis wiggle, `valueAtTime` echoes, `seedRandom` grids, full rigging walkthrough, Essential Graphics → MOGRT steps, Lottie/Bodymovin + Media Encoder presets), see `expression-library.md`.

## Core expressions

### Inertial bounce (overshoot after the last keyframe)

Paste on a Position, Scale, or Rotation property. It continues the velocity at the final keyframe into a damped sine — the classic "settle" motion.

```js
amp = 0.08;   // overshoot amount
freq = 2.5;   // oscillations per second
decay = 6.0;  // how fast it settles
n = 0;
if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) n--;
}
if (n > 0) {
  t = time - key(n).time;
  v = velocityAtTime(key(n).time - 0.001);
  value + v * (amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t));
} else {
  value;
}
```

### Looping

```js
loopOut("cycle");        // repeat keyframed range forever
loopOut("pingpong");     // bounce back and forth
loopOut("offset");       // continue, accumulating (e.g. continuous travel)
loopOut("continue");     // extend final velocity linearly
loopOut("cycle", 2);     // loop only the last 2 keyframes
loopIn("cycle");         // mirror, before the first keyframe
```

### Wiggle and stable randomness

```js
wiggle(2, 30);              // 2 wiggles/sec, amplitude 30 (units match the property)
seedRandom(index, true);   // unique-but-stable per layer; timeless=true
random(0, 100);            // stable after seedRandom
wiggle(freq, amp, octaves=1, amp_mult=0.5, t=time);  // full signature
```

`seedRandom(index, true)` before `random()` or `wiggle()` makes each layer differ but stay constant across renders — essential for grids of layers that must not flicker.

### Time remap & value-at-time

```js
// Sample another property/layer at a shifted time (echo/trailing motion)
delay = 0.2 * index;
thisComp.layer("Lead").transform.position.valueAtTime(time - delay);

// Speed up a precomp via time remap
linear(time, 0, thisComp.duration, 0, 6);  // 6s source mapped over comp duration
```

## Rigging

Make motion controllable instead of hand-keyed:

1. Add a null/control layer (often a "Controls" layer). Add **Slider Control**, **Checkbox Control**, **Color Control**, **Angle Control**, or **Point Control** effects to it.
2. Reference them with the pick-whip or by path:

```js
ctrl = thisComp.layer("Controls");
amt  = ctrl.effect("Intensity")("Slider");      // Slider Control → ADBE Slider Control-0001
on   = ctrl.effect("Enable")("Checkbox");       // Checkbox: 1 or 0
col  = ctrl.effect("Tint")("Color");

if (on == 1) value * amt else value;
```

3. Parent transforms to a null so one move drives many layers. Use `toComp`/`fromComp` to convert coordinate spaces when layers are parented or in different comps.

```js
// Stagger N layers off one master slider
master = thisComp.layer("Controls").effect("Reveal")("Slider");
delay  = 4 * index;     // 4 frames per layer
master.valueAtTime(time - framesToTime(delay));
```

## Essential Graphics / MOGRT

1. Open **Window → Essential Graphics**, pick the comp as the Master.
2. Drag the Slider/Checkbox/Color/Text source properties into the panel to expose them.
3. Group, rename, and set comment fields for editors.
4. **Export Motion Graphics Template** → a `.mogrt` usable in Premiere Pro / AE. Keep driving expressions referencing the exposed controls so editors change only the exposed params.

Set "Allow fonts to substitute" off and embed/package fonts where possible so the template renders consistently elsewhere.

## Export from expressions/template work

### To Lottie (Bodymovin / `@lottiefiles/bodymovin`)

- Stick to Lottie-supported features: shape layers, transforms, masks, track mattes, basic expressions converted to keyframes.
- Avoid blur-heavy effects, blend modes, 3D layers, and most native effects — they don't translate.
- Bake expressions to keyframes if the renderer is strict, or use the `expressions` flag in Bodymovin and test on the target player (web/iOS/Android renderers differ).
- Run **Bodymovin → Render** to produce `data.json` (+ optional images). Verify in a Lottie preview before handoff.

### To video (Media Encoder)

- **File → Export → Add to Adobe Media Encoder Queue** (or render queue for AE-native).
- Delivery: **H.264** (MP4), bitrate ~10–20 Mbps for 1080p, VBR 2-pass.
- Master/intermediate: **ProRes 422 HQ** (or ProRes 4444 when alpha is needed).
- Transparency: ProRes 4444 or PNG/QuickTime with an alpha channel; H.264 cannot carry alpha. (See `export-recipes.md` for the full codec/alpha/bitrate matrix.)

## Quick reference

| Goal | Expression |
|---|---|
| Loop keyframes | `loopOut("cycle")` |
| Continuous travel | `loopOut("offset")` |
| Subtle life | `wiggle(2, 20)` |
| Stable per-layer random | `seedRandom(index,true); random(...)` |
| Settle/overshoot | inertial bounce (above) |
| Echo another layer | `valueAtTime(time - delay)` |
| Read a slider | `effect("Name")("Slider")` |
| Frames ↔ seconds | `framesToTime(n)` / `timeToFrames(t)` |

## Gotchas

- An expression overrides keyframes on that property unless it incorporates `value`; start most expressions from `value`.
- `index` is the layer's stacking number — it changes if layers are reordered; prefer named lookups for stable rigs.
- Expression errors disable the expression and show a yellow banner; check the property's path names (effect names must match exactly, including duplicates' suffixes).
- Pre-compose for reuse; name layers; use shy/lock and guide layers for safe areas before handoff.
</content>
</invoke>

---

## 📄 SOURCE FILE: `skills/after-effects/references/expression-library.md` (verbatim)

# After Effects Expression Library, Rigging & Export

A deeper cookbook. All expressions are JavaScript (the modern AE expression engine). They evaluate on the property they are pasted on, where `value`, `time`, `index`, `thisLayer`, `thisComp` are in scope.

## Inertial bounce (parameterized)

```js
// Overshoot/settle after the most recent keyframe. Tune amp/freq/decay.
amp = 0.10;     // 0.05 = subtle, 0.2 = bouncy
freq = 3.0;     // oscillations per second
decay = 5.0;    // higher = settles faster

n = 0;
if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) n--;
}
if (n === 0) {
  value;
} else {
  t = time - key(n).time;
  v = velocityAtTime(key(n).time - thisComp.frameDuration / 10);
  value + v * amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t);
}
```

Inertial bounce works on multi-dimensional properties because `velocityAtTime` returns a vector; the arithmetic is per-component.

## Loop variants

```js
loopOut("cycle");          // A B C A B C ...
loopOut("pingpong");       // A B C B A B C ...
loopOut("offset");         // continues accumulating the delta each cycle
loopOut("continue");       // linear extension of the final velocity (no loop)
loopOut("cycle", 3);       // loop only the last 3 keyframes
loopIn("cycle", 2);        // loop the first 2 keyframes, backwards in time
loopOutDuration("cycle", 2); // loop the last 2 SECONDS of keyframes
```

Use `offset` for endless conveyor/scroll motion; `continue` for inertia past the last keyframe without oscillation.

## Wiggle — advanced

```js
// Full signature: wiggle(freq, amp, octaves, amp_mult, time)
wiggle(2, 30, 3, 0.5);     // 3 octaves adds finer detail

// Per-axis wiggle (different amplitude X vs Y)
x = wiggle(2, 50)[0];
y = wiggle(2, 10)[1];
[x, y];

// Wiggle only rotation while keeping keyframed position
wiggle(1, 5);              // on Rotation

// Smooth, looping ambient motion without true wiggle (loopable):
amp = 20; period = 4;      // seconds
[Math.sin(time / period * 2 * Math.PI) * amp,
 Math.cos(time / period * 2 * Math.PI) * amp] + value;
```

`wiggle` is non-looping noise; for seamless loops use periodic sin/cos as above.

## Stable randomness across a grid

```js
seedRandom(index, true);        // timeless=true → constant over time, varies per layer
startDelay = random(0, 0.5);    // each layer gets a stable random delay
opacity = ease(time, startDelay, startDelay + 0.4, 0, 100);
```

`seedRandom(index, false)` (timeless=false) lets `random()` vary over time — use for flicker; `true` for stable offsets.

## Time remap & valueAtTime echoes

```js
// Trailing/echo: sample the lead layer in the past, staggered by index
delay = 0.08 * (index - 1);
thisComp.layer("Lead").transform.position.valueAtTime(time - delay);

// Speed-ramp a time-remapped layer using easing on the source time
src = thisComp.layer("Source");
linear(time, 0, 2, 0, src.source.duration);   // play a 2s window of the source

// Sample own value in the past for motion smear / trail
valueAtTime(time - 0.1);
```

## Rigging walkthrough

### Control types and how to read them

```js
ctrl = thisComp.layer("Controls");
ctrl.effect("Intensity")("Slider");   // number
ctrl.effect("Visible")("Checkbox");   // 1 or 0
ctrl.effect("Brand")("Color");        // [r,g,b,a] 0..1
ctrl.effect("Spin")("Angle");         // degrees
ctrl.effect("Anchor")("Point");       // [x,y]
```

### One slider, staggered reveal across N layers

```js
// On each layer's Opacity:
master = thisComp.layer("Controls").effect("Reveal")("Slider"); // 0..100 driver
per = 6;                       // frames of stagger per layer
shift = framesToTime(per * (index - 1));
ease(master, 0, 100, 0, 100) * (time > shift ? 1 : 0);
```

### Coordinate-space conversions

```js
// Place this layer where another parented layer appears in comp space
target = thisComp.layer("Marker");
fromComp(target.toComp(target.anchorPoint));

// World position of a point on this layer
toComp([0, 0]);
```

`toComp` converts layer space → composition space; `fromComp` does the inverse. Use them whenever layers are parented or live in different (nested) comps.

### Linking many layers to a master null

1. Select all children → set Parent to the null.
2. Animate only the null; children inherit transform.
3. For non-transform links (effects, opacity), pick-whip to the control layer's effect.

## Essential Graphics / MOGRT export steps

1. **Window → Essential Graphics**, choose the master comp.
2. Drag exposed properties (Slider, Checkbox, Color, Text Source, Media replacement) into the panel.
3. Add **Group** headers, rename controls, fill comment fields for editors.
4. Use **Drop-Zone / Media Replacement** for swappable footage/logos.
5. Click **Export Motion Graphics Template**, choose destination (Local Templates Folder / Library / file). Toggle "Make fonts available" and check "Raster/vector" compatibility for Premiere.
6. Test in Premiere Pro's Essential Graphics → Browse panel.

Keep all motion driven by expressions referencing the exposed controls so editors only touch the exposed params; hide internal layers with shy.

## Lottie / Bodymovin export

Supported reliably:
- Shape layers, solids, transforms (position/scale/rotation/opacity/anchor).
- Masks and track mattes (alpha), parenting, basic gradients.
- Trim Paths, simple repeaters.
- Expressions: enable in Bodymovin settings, but verify on the target renderer — `lottie-web`, lottie-ios, and lottie-android differ in expression and effect support.

Not supported / risky (bake or avoid):
- Blend modes, most native Effects, layer blurs, 3D layers/cameras, time remapping, adjustment-layer effects.

Workflow:
1. Install Bodymovin extension; **Window → Extensions → Bodymovin**.
2. Select comp(s), set destination, choose Standard/Demo.
3. Settings: enable "Glyphs"/"Hidden", "Expressions" only if needed; "Assets" → export images or use base64.
4. Render `data.json`. Preview in a Lottie player; check file size and that masks/mattes survived.
5. For web, load with `lottie-web`:

```js
import lottie from 'lottie-web';
lottie.loadAnimation({
  container: document.getElementById('lottie'),
  renderer: 'svg',          // 'canvas' for heavy fills, better perf
  loop: true, autoplay: true,
  path: '/data.json',
});
```

## Media Encoder presets

| Use | Codec / format | Settings |
|---|---|---|
| Web/social delivery | H.264 (MP4) | VBR 2-pass, 1080p ~12–16 Mbps; 4K ~35–50 Mbps |
| Master/intermediate | ProRes 422 HQ (MOV) | full range, matched fps |
| With alpha | ProRes 4444 (MOV) | enable alpha channel |
| Lossless interchange | PNG sequence or ProRes 4444 | per-frame, alpha |
| GIF | via Media Encoder/Photoshop | reduce palette, dither, cap dimensions |

Tips:
- Match the comp frame rate; avoid frame-blending unless intentionally retiming.
- H.264 cannot store alpha — composite onto a background or use ProRes 4444 / PNG.
- For crisp text, render at the delivery resolution (don't upscale); set quality to maximum and use 2-pass VBR.

---

## 📄 SOURCE FILE: `skills/after-effects/references/export-recipes.md` (verbatim)

# Export Recipes — Codec, Container, Alpha, Bitrate

Pick the correct codec, container, alpha handling, and bitrate for a given delivery target, and avoid the classic failures: black backgrounds where transparency was expected, H.264 that vanished from the Render Queue, and bloated or muddy files.

## The two export engines

After Effects has two output paths. Choosing the wrong one is the root of most export confusion.

- **Render Queue (RQ)** — `Composition > Add to Render Queue`. Best for mastering/intermediate formats: ProRes, image sequences, lossless, alpha. Renders inside AE.
- **Adobe Media Encoder (AME)** — `Composition > Add to Adobe Media Encoder Queue` (or the RQ "Queue in AME" button). Best for delivery/compressed formats: H.264 MP4, H.265, social presets. Renders in a separate app so AE stays usable.

**Why H.264 disappeared from the Render Queue:** Since AE CC 2014/2015, Adobe removed the native H.264, H.264 Blu-ray, and MPEG-2 output modules from the RQ. To make an MP4, use AME — not the RQ. There is no setting to restore it in the RQ; that workflow is intentional.

## Decision tree

```
Need transparency (alpha) in the final file?
├─ YES, for an editor/compositor (NLE)      → ProRes 4444 (.mov), RGB+Alpha, RQ
│   └─ smaller, still alpha?                 → PNG sequence or TIFF sequence (RGB+Alpha)
├─ YES, for the web/browser                  → dual export:
│     • HEVC with alpha (.mov, Safari/iOS)
│     • VP9/WebM with alpha (Chrome/Firefox/Edge)
└─ NO alpha needed
    ├─ Final delivery / upload (YouTube, social, client review) → H.264 MP4 via AME
    ├─ Editorial / intermediate / grading       → ProRes 422 HQ or 422 (.mov), RQ
    ├─ Mastering / archival, highest fidelity    → ProRes 4444 or lossless / image seq
    └─ Tiny looping clip, limited colors         → GIF (via AME / Photoshop), or WebM
```

## Transparency — the black background problem

H.264/MP4 **cannot store an alpha channel**. Exporting a comp with transparent areas to H.264 always fills them with black (or white). This is the single most common export complaint and it is not a bug.

To actually keep transparency:

1. Use a format that supports alpha: **ProRes 4444**, **PNG/TIFF sequence**, **HEVC-with-alpha**, or **VP9/WebM-with-alpha**.
2. In the RQ Output Module, set **Channels: RGB + Alpha** and **Depth** to Millions of Colors+ (the "+" is the alpha).
3. Choose a matte type: **Premultiplied (Matted with color)** for most cases; **Straight (Unmatted)** if the compositor explicitly wants straight alpha. Straight alpha avoids dark/light fringing on edges when re-composited, but only some apps import it cleanly.

For web transparent video, no single file plays everywhere. Ship two and use the HTML `<video>` element with multiple `<source>` tags: HEVC-alpha for Safari/iOS, VP9/WebM-alpha for Chromium/Firefox.

## Bitrate guidance (H.264 via AME)

Set in AME Export Settings → Video → Bitrate Settings.

- **Encoding:** VBR, 2 pass (better quality per byte than CBR or 1-pass).
- **1080p30:** Target ~10–16 Mbps, Max ~20 Mbps.
- **1080p60:** Target ~16–24 Mbps.
- **4K30:** Target ~35–45 Mbps, Max ~55 Mbps.
- **4K60:** Target ~50–68 Mbps.
- Higher target/max for high-motion or grainy footage; lower for flat graphics/motion design.
- For uploading to YouTube/Vimeo, lean to the high end — the platform re-encodes, so feed it a clean, high-bitrate master rather than over-compressing twice.

## Quick reference

| Target | Engine | Codec / Container | Channels | Bitrate / Notes |
|---|---|---|---|---|
| YouTube / Vimeo upload | AME | H.264 .mp4 | RGB | VBR 2-pass, 1080p ~16 Mbps / 4K ~45 Mbps |
| Instagram / TikTok / Reels | AME | H.264 .mp4 | RGB | 1080×1920 or 1080×1080, ~10–14 Mbps |
| Client review | AME | H.264 .mp4 | RGB | VBR 2-pass ~10–16 Mbps |
| Editorial / hand to editor | RQ | ProRes 422 HQ .mov | RGB | Mezzanine; large but edit-friendly |
| Mastering / grading | RQ | ProRes 4444 .mov | RGB(+A) | Highest fidelity, optional alpha |
| Transparency → NLE | RQ | ProRes 4444 .mov | RGB+Alpha | Millions+; premultiplied usually |
| Transparency → frames | RQ | PNG or TIFF sequence | RGB+Alpha | Lossless per-frame, robust |
| Transparent web (Safari) | AME/RQ | HEVC w/ alpha .mov | RGB+Alpha | Pair with VP9 below |
| Transparent web (Chrome) | AME/3rd-party | VP9 / WebM w/ alpha | RGB+Alpha | `yuva420p` alpha mode |
| Looping clip, few colors | AME/PS | GIF or WebM | — | GIF = large/limited; prefer WebM |
| Archival lossless | RQ | Lossless / PNG seq | RGB(+A) | Huge files |

## Gotchas

- **H.264 in the RQ is gone** — use AME. Don't search for a missing module.
- **Black background = wrong codec.** Switching matte/straight settings won't help if the codec has no alpha. Change the codec first.
- **"Millions of Colors" has no alpha; "Millions of Colors+" does.** The `+` is the alpha channel in RQ Depth.
- **ProRes on Windows** is fully supported for export in modern AE; no extra codec install needed.
- **GIF is rarely the right answer** — large files, dithered color, no real alpha softness. Prefer WebM/VP9 or short H.264 loops.
- **Don't double-compress.** Master to ProRes/lossless, then make one H.264 from that — not H.264 from H.264.
- **AME "Match Source"** presets can silently downscale or drop the bitrate; verify resolution and bitrate before queuing.
- **Render multiple outputs efficiently:** in the RQ, one render item can have several Output Modules (e.g. ProRes master + PNG seq) from a single render pass.

---

# Codec & Export Matrix — Detailed Reference

## ProRes family — when to use which

| Variant | Use for | Alpha | Relative size |
|---|---|---|---|
| ProRes 422 Proxy | Offline edit, rough cuts | No | Smallest |
| ProRes 422 LT | Lightweight editorial | No | Small |
| ProRes 422 | General editorial | No | Medium |
| ProRes 422 HQ | High-quality editorial / delivery to editor | No | Large |
| ProRes 4444 | Mastering, grading, **transparency** | Yes | Larger |
| ProRes 4444 XQ | Highest fidelity, HDR, max-quality alpha | Yes | Largest |

Rule of thumb: hand an editor **422 HQ**; master/keep alpha with **4444**.

## Full target → settings matrix

| Delivery target | Engine | Container | Codec | Resolution | Channels / Depth | Bitrate / Quality | Audio |
|---|---|---|---|---|---|---|---|
| YouTube 1080p | AME | .mp4 | H.264 | 1920×1080 | RGB, 8-bit | VBR 2-pass, Tgt 16 / Max 20 Mbps | AAC 320 kbps 48 kHz |
| YouTube 4K | AME | .mp4 | H.264 | 3840×2160 | RGB, 8-bit | VBR 2-pass, Tgt 45 / Max 55 Mbps | AAC 384 kbps |
| Vimeo 1080p | AME | .mp4 | H.264 | 1920×1080 | RGB | VBR 2-pass, Tgt 20 Mbps | AAC 320 kbps |
| Instagram Feed | AME | .mp4 | H.264 | 1080×1080 or 1080×1350 | RGB | ~10–12 Mbps | AAC 128–256 kbps |
| Instagram Reels / TikTok | AME | .mp4 | H.264 | 1080×1920 | RGB | ~12–14 Mbps | AAC 256 kbps |
| X / Twitter | AME | .mp4 | H.264 | 1280×720 or 1080p | RGB | ~6–10 Mbps | AAC |
| Broadcast delivery | RQ | .mov | ProRes 422 HQ | as spec (often 1080i/p) | RGB, 10-bit | — | PCM 48 kHz |
| Editorial handoff | RQ | .mov | ProRes 422 HQ | comp size | RGB | — | PCM |
| Color grading master | RQ | .mov | ProRes 4444 | comp size | RGB, 12-bit | — | PCM |
| VFX plate / alpha to NLE | RQ | .mov | ProRes 4444 | comp size | RGB+Alpha, Millions+ | premultiplied | — |
| Compositing frames | RQ | seq | PNG or 16-bit TIFF | comp size | RGB+Alpha | lossless | — |
| EXR for VFX pipeline | RQ | seq | OpenEXR | comp size | RGB+Alpha, 32-bit float | linear/ACES | — |
| Transparent web (Apple) | AME or RQ | .mov | HEVC w/ alpha | comp size | RGB+Alpha | quality ~ 60–80% | optional |
| Transparent web (Chrome) | 3rd-party/ffmpeg | .webm | VP9 (yuva420p) | comp size | RGB+Alpha | CRF ~30 | optional |
| Animated icon / loop | AME or PS | .gif / .webm | GIF / VP9 | small | indexed / RGBA | minimize frames | — |

## Transparency — step by step

### ProRes 4444 with alpha (Render Queue)
1. `Composition > Add to Render Queue`.
2. Click the blue **Output Module** text.
3. Format: **QuickTime**. Click **Format Options** → Codec: **Apple ProRes 4444**.
4. **Channels: RGB + Alpha**. **Depth: Millions of Colors+**.
5. **Color: Premultiplied (Matted)** for most uses; choose **Straight (Unmatted)** only if the downstream app asks for straight alpha.
6. Set Output To path, then **Render**.

### PNG / TIFF sequence with alpha (Render Queue)
1. Add to RQ → Output Module.
2. Format: **PNG Sequence** (or **TIFF Sequence**).
3. **Channels: RGB + Alpha**, Depth **Millions of Colors+** (PNG) or 16-bit (TIFF).
4. Output To a **dedicated empty folder** — sequences write one file per frame.

### HEVC with alpha (Apple/Safari)
- In AME, choose **H.265 (HEVC)** and enable an alpha/transparency option where available, or use the QuickTime HEVC export with RGB+Alpha. Verify playback in Safari; Chrome will not show its alpha.

### VP9 / WebM with alpha (Chrome)
- AME does not reliably produce alpha WebM. Render a ProRes 4444 or PNG sequence from AE, then encode with ffmpeg:
  - `ffmpeg -i master.mov -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 out.webm`
  - `yuva420p` is the alpha-carrying pixel format; without it WebM has no transparency.

### HTML for cross-browser transparent video
```html
<video autoplay loop muted playsinline>
  <source src="clip.mov"  type="video/quicktime">   <!-- HEVC alpha, Safari/iOS -->
  <source src="clip.webm" type="video/webm">         <!-- VP9 alpha, Chrome/Firefox -->
</video>
```

## Alpha matte types explained
- **Straight (Unmatted):** color stored independent of alpha; cleanest edges when re-composited, but fewer apps import correctly.
- **Premultiplied (Matted with color):** color blended with a matte color (usually black). Most compatible; can show fringing if the wrong matte color is assumed downstream.
- When in doubt for NLE handoff, **premultiplied with black** is the safe default.

## AME preset cautions
- **Match Source – High bitrate** can downscale to the source clip rather than the comp; confirm output resolution.
- Always check **VBR 2-pass** is selected for final masters; presets sometimes default to 1-pass.
- Use **Render at Maximum Depth** and **Use Maximum Render Quality** for scaling-heavy comps (slower but cleaner).
- For social verticals, set the resolution explicitly — don't trust a 16:9 preset.

## Bitrate cheat sheet (H.264 VBR 2-pass)
| Resolution / fps | Target Mbps | Max Mbps |
|---|---|---|
| 720p30 | 5–8 | 10 |
| 1080p30 | 10–16 | 20 |
| 1080p60 | 16–24 | 30 |
| 4K30 | 35–45 | 55 |
| 4K60 | 50–68 | 80 |

---

## 📄 SOURCE FILE: `skills/after-effects/references/performance-triage.md` (verbatim)

# Performance Triage — Slow, Laggy, Crashing, Frozen

Diagnose slow previews, slow renders, freezes, and crashes in a fixed order, from cheapest fix to most invasive. Work top-down and stop when the symptom clears — most issues are solved in the first few steps.

Most fixes live in Preferences. Open `Edit > Preferences` (Windows) or `After Effects > Settings/Preferences` (macOS).

## First: identify the symptom

- **Slow / non-real-time previews (RAM preview)** → Flow A
- **Slow renders (final output)** → Flow B
- **Crashes / freezes / hangs** → Flow C

## Flow A — Slow previews (do in order)

1. **Set Resolution to Auto/Half/Third.** In the Composition viewer, change Resolution from Full to **Half** or **Third**. Adaptive/Draft resolution gives the biggest instant win.
2. **Enable Multi-Frame Rendering (MFR).** `Preferences > Memory & Performance > Enable Multi-Frame Rendering`. Uses all CPU cores for preview and render (AE 2022+). Confirm "CPUs reserved for other applications" isn't set too high.
3. **Check RAM allocation.** `Preferences > Memory & Performance`. Leave ~6 GB for the OS; give the rest to AE. Too little RAM = a tiny green preview bar.
4. **Set Fast Previews to Adaptive Resolution.** Viewer's lightning-bolt icon → **Adaptive Resolution** (degrades resolution only while interacting).
5. **Purge the cache.** `Edit > Purge > All Memory & Disk Cache`. Stale/full cache stalls previews.
6. **Verify the Disk Cache is on a fast drive.** `Preferences > Media & Disk Cache` → Enable Disk Cache, point it at a fast **SSD/NVMe**, give it 50–100+ GB. Never on a slow external HDD.
7. **Solo the offending layer/effect.** Toggle effects off (the fx switch) or solo layers to find the bottleneck. Heavy culprits: blurs, glows, Mocha/tracking, particles, expressions, large 3D, and many third-party plugins.
8. **Enable GPU / hardware-accelerated decoding.** `Preferences > Video Preview` (Mercury GPU) and `Preferences > Import > Hardware Accelerate H.264/HEVC decoding`. Helps long-GOP source footage.
9. **Pre-render or proxy heavy comps.** Pre-render a finished/slow precomp to ProRes and set it as a **proxy** (`File > Create Proxy`, or right-click footage → Set Proxy). Frees compute for the part being worked on.
10. **Trim the work area** to just the section in progress so RAM preview fills faster.

## Flow B — Slow renders (do in order)

1. **Confirm Multi-Frame Rendering is on** (`Memory & Performance`) — the single largest render speedup on multi-core CPUs.
2. **Render with the Render Queue for masters, AME for delivery** — and don't run heavy work in AE while AME renders.
3. **Enable hardware-accelerated decoding** for H.264/HEVC sources (`Preferences > Import`).
4. **Pre-render slow precomps** once and reuse them, instead of recomputing every frame. Heavy effect stacks, time-remapping, and 3rd-party renderers benefit most.
5. **Replace effects with cheaper equivalents** where possible (e.g., Fast Box Blur over Gaussian; native over plugin).
6. **Convert long-GOP source to an intermediate** (ProRes/DNxHR). Decoding H.264 every frame is slow; ProRes is cheap to read.
7. **Check the renderer:** `Composition > Composition Settings > 3D Renderer`. Classic 3D is fastest; Cinema 4D/Ray-traced renderers are far slower.
8. **Disk Cache on NVMe** so repeated frames aren't recomputed.
9. **Close other apps**, especially other Adobe apps and browsers, to free RAM/CPU for MFR.

## Flow C — Crashes / freezes / hangs (do in order)

1. **Purge cache** (`Edit > Purge > All`). A full/corrupt cache causes hangs.
2. **Clear the Disk Cache folder** in `Preferences > Media & Disk Cache > Empty Disk Cache`. Corrupt cache files cause crash-on-open.
3. **Update GPU drivers** (NVIDIA Studio driver / AMD). Outdated/Game-Ready drivers cause Mercury GPU crashes. As a test, switch Project renderer GPU→CPU (`File > Project Settings > Video Rendering and Effects: Mercury Software Only`).
4. **Reset Preferences:** hold `Ctrl+Alt+Shift` (Win) / `Cmd+Opt+Shift` (Mac) while launching AE. Corrupt prefs are a top crash cause.
5. **Disable third-party plugins** by temporarily moving them out of the plug-ins folder, then reintroduce to find the offender. Old plugins are a leading crash/freeze source after AE updates.
6. **Check Disk Cache and Output drives for free space.** A full scratch/cache disk causes freezes mid-render.
7. **Lower or disable MFR** if crashes appear only during multi-frame render — some plugins are not MFR-safe; reserve more CPUs or disable MFR for those projects.
8. **Roll back the AE version** if crashes started right after an update. Install a previous version via Creative Cloud (Other Versions) — many crash waves are version-specific regressions.
9. **Look for a single corrupt asset** — import comps one at a time, or replace footage, to isolate a bad file.

## Quick reference

| Symptom | First three moves |
|---|---|
| Choppy RAM preview | Half resolution → enable MFR → purge cache |
| Tiny green preview bar | Raise RAM allocation → SSD disk cache → trim work area |
| Slow final render | Enable MFR → HW decode H.264 → pre-render precomps |
| Crash on launch | Reset prefs (modifier keys) → empty disk cache → update GPU driver |
| Crash mid-render | Free disk space → disable/reserve CPUs for MFR → disable 3rd-party plugins |
| Started after update | Roll back AE version → update plugins → reset prefs |
| Laggy with footage | HW-accelerated decode → transcode to ProRes → proxy heavy comps |

## Gotchas

- **MFR needs RAM per core.** With many cores but little RAM, MFR can underperform or stall — aim for several GB per active core.
- **Game-Ready drivers crash AE.** Prefer the **Studio** driver branch on NVIDIA.
- **Disk Cache on an external HDD is worse than none** — it must be SSD/NVMe to help.
- **Plugins lag behind AE updates.** After a major AE upgrade, a sudden crash wave usually means a plugin needs updating or is not MFR-safe.
- **Purging clears the green bar.** Previews must rebuild afterward; that initial slowness is expected, not a new problem.
- **CPU/GPU effects are not equal.** A few GPU-accelerated effects are fast; mixing many CPU-only effects forces round-trips that kill preview speed.
- **Don't render in AE and AME simultaneously** on the same machine — they fight for cores and RAM.

---

# AE Performance — Detailed Diagnostics Reference

## Preference locations and recommended values

| Setting | Path | Recommended |
|---|---|---|
| RAM for AE | Preferences > Memory & Performance | Total RAM minus ~6 GB for OS |
| Multi-Frame Rendering | Memory & Performance > Enable MFR | On; reserve 0–2 CPUs for other apps |
| Disk Cache | Media & Disk Cache > Enable Disk Cache | On, SSD/NVMe, 50–150 GB |
| Conformed media cache | Media & Disk Cache | On SSD, separate from project if possible |
| HW decode (H.264/HEVC) | Import > Hardware Accelerate Decoding | On |
| Mercury GPU | Project Settings > Video Rendering and Effects | GPU (CPU as crash test) |
| Fast Previews | Viewer lightning icon | Adaptive Resolution |

## Multi-Frame Rendering (MFR) tuning
- Introduced in AE 2022 (22.x); renders multiple frames in parallel across CPU cores for both preview and final render.
- **RAM is the limiter.** Each rendering frame needs memory; with too little RAM, AE quietly reduces the cores it uses. Target several GB of free RAM per logical core you want active.
- "CPUs reserved for other applications" trades render speed for system responsiveness. Set 0–2 on a dedicated machine.
- Some legacy/3rd-party effects are **not MFR-safe** and can crash or render incorrectly under MFR. If a specific project crashes only with MFR on, disable MFR for that project or update the plugin.

## GPU and drivers
- Use the **NVIDIA Studio Driver** (not Game Ready) for stability with Adobe apps; keep AMD drivers current too.
- Mercury GPU acceleration speeds some effects and the renderer. If AE crashes on launch or while playing back, switch `Project Settings > Video Rendering and Effects` to **Mercury Software Only** to confirm GPU/driver fault, then update drivers.
- Hardware-accelerated **decoding** (separate from rendering) speeds reading H.264/HEVC source footage; enable in `Preferences > Import`.

## Disk cache sizing and placement
- Put the disk cache on the **fastest local drive** (internal NVMe ideal). Never on a slow USB HDD or a network drive.
- 50–150 GB is typical; more helps long projects retain cached frames between sessions.
- Symptoms of a bad cache: hangs on open, garbage frames, refusal to play. Fix via `Empty Disk Cache` and `Edit > Purge > All`.
- Keep the cache drive from filling up — a full cache/scratch disk causes mid-render freezes.

## Pre-render and proxy workflow
1. Identify a slow, finished precomp (heavy effects, particles, 3D, tracking).
2. Add it to the Render Queue and render to **ProRes 422/422 HQ** (or PNG sequence).
3. Right-click the footage/comp in the Project panel → **Set Proxy > File**, select the rendered file. A box icon shows the proxy is active.
4. Toggle the proxy off for final render if you want to re-render at full quality, or keep it if the pre-render is final.
5. Alternatively `File > Create Proxy > Movie/Still` to queue a proxy directly.
- Proxies let AE substitute a cheap-to-read file for an expensive comp/footage during editing.

## Heavy effect culprits (preview/render cost)
- Gaussian Blur, Camera Lens Blur, Glow → use Fast Box Blur where acceptable.
- Particle systems (Particular, Form), Element 3D, Plexus.
- Mocha tracking, Warp Stabilizer (analysis), motion tracking.
- Expressions that read many layers/time, especially per-frame heavy ones.
- Nested precomps with collapsed transformations and continuous rasterization.
- Ray-traced / Cinema 4D 3D renderer vs Classic 3D.

## Version-specific culprits
- After a **major AE update**, a sudden crash/slowdown wave usually traces to a third-party plugin not yet updated for that AE version — update plugins or remove them to test.
- If problems began immediately after updating AE, install the **previous version** from Creative Cloud → app → Other Versions, and report the regression.
- Reset corrupt preferences by holding `Ctrl+Alt+Shift` (Win) / `Cmd+Opt+Shift` (Mac) during launch; this resolves many post-update oddities.

## Isolation checklist for crashes
1. Reset preferences (modifier-key launch).
2. Empty disk cache + Purge All.
3. Update GPU driver (Studio branch).
4. Move 3rd-party plugins out, relaunch, reintroduce one at a time.
5. Switch Mercury to Software Only to rule out GPU.
6. Import comps/footage incrementally to find a corrupt asset.
7. Disable MFR for the project if crashes are MFR-specific.
8. Roll back AE version if the crash wave is version-correlated.

## When to pre-compose vs pre-render
- **Pre-compose** to organize and to apply an effect to a group — does not by itself speed anything up (it can even add overhead).
- **Pre-render** (render to a file + use as proxy/footage) when a precomp is finished and slow — this is the actual performance win.

---

## 📄 SOURCE FILE: `skills/after-effects/references/project-hygiene.md` (verbatim)

# Project Hygiene — Organize, Relink, ExtendScript

Keep AE projects organized, portable, and automatable: consistent naming, a clear folder/bin structure, label discipline, pre-comp discipline, reliable relinking when files move, and ExtendScript (.jsx) automation for repetitive tasks.

## Folder (bin) structure

Create folders in the Project panel (the folder icon at the bottom). A reliable layout:

```
01_Comps/         finished/active compositions
02_Precomps/      nested precomps
03_Footage/       imported video
04_Images/        stills, logos, textures
05_Audio/
06_Solids/        (AE's auto "Solids" folder — keep it here)
07_Assets_3D/
99_Old/           deprecated comps/layers, not deleted yet
```

Numeric prefixes force a stable sort order. After importing, immediately drag items into the right bin — `File > Reduce Project` and `File > Consolidate All Footage` help later, but discipline up front prevents chaos.

## Naming conventions

- **Comps:** `PROJECT_section_descriptor_v01` (e.g., `BRAND_intro_logoBuild_v03`). Version with zero-padded `v01`, `v02`.
- **Precomps:** prefix `PRE_` or suffix `_pre` so they're obvious in lists.
- **Layers:** rename solids/nulls to their role (`CTRL_master`, `BG_gradient`, `MATTE_text`). Never ship "Black Solid 12".
- **No spaces / special chars** in filenames destined for render farms or cross-OS sharing — use `_` and `-`.
- Keep names short but unique; long names truncate in the timeline.

## Label colors

Use the Label color (the swatch left of each Project/Timeline item) as a visual system. Pick a convention and apply it consistently, e.g.:
- Red = control/null layers
- Blue = footage
- Green = precomps
- Yellow = text
- Purple = adjustment/effects layers

Right-click an item → **Label** to set. Select multiple, then `Edit > Label > Select Label Group` to act on a whole color at once. Customize label names/colors in `Preferences > Labels`.

## Pre-comp discipline

- Pre-compose (`Layer > Pre-compose`, `Ctrl/Cmd+Shift+C`) to **group** related layers and to apply one effect to a group — not reflexively for everything.
- When pre-composing a single layer, choose **"Leave all attributes in"** vs **"Move all attributes into the new composition"** deliberately: "Move" carries transforms/effects inside; "Leave" keeps them on the outer layer.
- Name the precomp immediately and file it in `02_Precomps`.
- Avoid deep nesting beyond a few levels — it slows navigation and makes relinking/debugging painful.
- Match precomp duration and frame rate to need; an over-long precomp wastes cache.

## The "moved one file and everything broke" rescue

AE references footage by file path. Moving, renaming, or sending a project without its assets breaks links (shown as **colored bars / "Missing Footage"** placeholders).

### Fix options, in order
1. **Relink one, fix many:** double-click a missing item (or right-click → **Replace Footage > File**). Point it at the moved file; AE offers to relink *all* missing items from the same folder automatically. This single step usually fixes the whole project.
2. **Find Missing Footage:** `File > Dependencies > Find Missing Footage` lists every broken link to resolve.
3. **Replace Footage:** right-click footage → **Replace Footage > File** to swap an asset while keeping every use, effect, and keyframe intact.

### Prevent it: Collect Files
Before moving or sharing a project, use `File > Dependencies > Collect Files`. This copies the project plus every used asset into one new folder with relative structure, so links survive on any machine. Always hand off projects as a Collect Files package, not a bare `.aep`.

Related: `File > Dependencies > Consolidate All Footage` (merge duplicate imports), `Remove Unused Footage`, and `Reduce Project` (strip everything not used by selected comps) to slim a project before collecting.

## Batch automation with ExtendScript (.jsx)

AE scripts (ExtendScript / JSX) automate repetitive work. Run via `File > Scripts > Run Script File...`, or place in the **ScriptUI Panels** folder to dock as a panel. Always wrap edits in `app.beginUndoGroup("name") ... app.endUndoGroup()` so one Undo reverts the whole batch.

Common automations (full code in `../scripts/`):
- **Batch rename** selected layers with a base name + auto-increment (`../scripts/batch-rename.jsx`).
- **Sequential offset** — stagger selected layers in time by N frames each, a staggered "domino" start (`../scripts/sequential-offset.jsx`).
- **Apply an effect** (e.g., a Gaussian Blur, or any matchName) across all selected layers at once (`../scripts/apply-effect-to-layers.jsx`).

Minimal pattern:
```javascript
app.beginUndoGroup("My Batch Op");
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
  var sel = comp.selectedLayers;
  for (var i = 0; i < sel.length; i++) {
    // operate on sel[i]
  }
}
app.endUndoGroup();
```

## Quick reference

| Task | How |
|---|---|
| New bin | Folder icon at bottom of Project panel |
| Set label color | Right-click item → Label |
| Relink missing footage | Double-click item / Replace Footage > File |
| List broken links | File > Dependencies > Find Missing Footage |
| Package for handoff | File > Dependencies > Collect Files |
| Swap an asset everywhere | Replace Footage > File |
| Slim project | Reduce Project / Remove Unused Footage |
| Run a script | File > Scripts > Run Script File... |
| Pre-compose | Layer > Pre-compose (Ctrl/Cmd+Shift+C) |

## Gotchas

- **Collect Files before moving anything.** Moving the `.aep` alone always breaks links.
- **Relinking one item often relinks the rest** from the same folder — try that before fixing each by hand.
- **Replace Footage preserves effects/keyframes;** deleting + re-importing does not.
- **AE auto-creates a "Solids" folder** — don't scatter solids elsewhere or it regenerates duplicates.
- **Scripts need `app.beginUndoGroup`/`endUndoGroup`** or a batch becomes many separate undos.
- **Applying effects by name needs the `matchName`,** not the display name (e.g., `"ADBE Gaussian Blur 2"`), to be reliable across AE language versions.
- **Allow Scripts to Write Files** must be enabled in `Preferences > Scripting & Expressions` for scripts that save/render.
- **Deep precomp nesting** makes both performance and relinking worse — keep it shallow.

---

# AE Project Organization — Detailed Reference

## Full folder (bin) template
```
PROJECT.aep
├── 00_Output/        (final renders live next to project on disk)
01_Comps/             master & active comps
02_Precomps/          nested precomps (prefix PRE_)
03_Footage/           video clips
04_Images/            stills, logos, vector, textures
05_Audio/             music, VO, SFX
06_Solids/            AE auto-folder; leave it here
07_Assets_3D/         OBJ/C4D/3D model assets
08_Reference/         storyboards, briefs, temp ref
99_Old/               deprecated, kept until final
```
Numeric prefixes lock sort order. Keep the on-disk asset folders mirroring these bins so Collect Files stays clean.

## Naming scheme
| Item | Pattern | Example |
|---|---|---|
| Master comp | `PROJ_section_v##` | `BRAND_main_v04` |
| Sub/shot comp | `PROJ_section_shot_v##` | `BRAND_intro_logo_v02` |
| Precomp | `PRE_descriptor` | `PRE_textReveal` |
| Null/control | `CTRL_role` | `CTRL_master` |
| Solid/BG | `BG_role` | `BG_gradient` |
| Matte | `MATTE_role` | `MATTE_logoTrack` |
| Adjustment | `ADJ_role` | `ADJ_grade` |

Rules: zero-pad versions; no spaces/special characters for farm/cross-OS safety; keep unique and short.

## Label color system (example)
| Color | Meaning |
|---|---|
| Red | Control / null layers |
| Blue | Footage |
| Green | Precomps |
| Yellow | Text |
| Purple | Adjustment / effects |
| Orange | Audio |
| Gray | Disabled / old |

Set via right-click → Label. Customize names/colors in `Preferences > Labels`. Use `Edit > Label > Select Label Group` to select everything of one color.

## Relink / missing footage — full workflow
1. **Identify:** missing items show as colored bars with "Missing" placeholders; the Project panel marks them.
2. **Relink one to fix many:** right-click a missing item → **Replace Footage > File** (or double-click it). Choose the relocated file. AE prompts to relink all other missing files found in the same folder — accept to fix the batch at once.
3. **Enumerate:** `File > Dependencies > Find Missing Footage`, `Find Missing Fonts`, `Find Missing Effects` to locate every broken dependency.
4. **Swap assets:** **Replace Footage > File** swaps the source while preserving all layer instances, effects, masks, and keyframes.

## Collect Files (portable handoff)
- `File > Dependencies > Collect Files`.
- Options: Collect Source Files = **All**; enable **Reduce Project** to drop unused; optionally **Generate Report**.
- Produces a folder containing the `.aep` plus a `(Footage)` subfolder with every used asset, preserving relative links so the project opens anywhere.
- Always deliver/move projects as a Collect Files package, never a lone `.aep`.

## Slimming a project
- `File > Reduce Project` — removes all items not used by the currently selected comp(s). Destructive to unused items; save first.
- `File > Dependencies > Consolidate All Footage` — merges duplicate imports of the same file.
- `File > Dependencies > Remove Unused Footage` — drops footage no comp references.
- Run these before Collect Files to keep the package small.

## Scripting setup
- Enable `Preferences > Scripting & Expressions > Allow Scripts to Write Files and Access Network` for scripts that save or render.
- Run a script: `File > Scripts > Run Script File...`.
- Dock a panel script: place the `.jsx` in `(AE install)/Scripts/ScriptUI Panels/`, restart AE, open from the `Window` menu.
- Wrap every batch in `app.beginUndoGroup("...")` / `app.endUndoGroup()` so it undoes in one step.
- Apply effects by **matchName** (internal id like `"ADBE Gaussian Blur 2"`), not the localized display name, for cross-version reliability. Use `layer.property("ADBE Effect Parade").addProperty(matchName)`.

## Pre-comp discipline details
- "Leave all attributes in the new composition" keeps the outer layer's transform; "Move all attributes" pushes them inside the precomp. Choosing wrong shifts/rescales the result.
- Trim precomp duration to the content; over-long precomps waste RAM/disk cache.
- Name and file precomps immediately; never leave "Pre-comp 1".
- Keep nesting shallow (2–3 levels) for performance and easier relinking/debugging.

---
Keep the project tidy and named well and footage relinks without a fight. Built by **[iart.ai](https://iart.ai/?utm_source=github&utm_medium=readme&utm_campaign=motion-design-skills&utm_content=skill_footer&utm_term=after-effects)** — the AI motion agent for editable, on-brand motion graphics.
