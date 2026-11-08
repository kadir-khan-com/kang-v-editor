# justajazz/ae-mcp-bridge — AE MCP Bridge (bundled after-effects-motion skill extracted)
- Repo: justajazz/ae-mcp-bridge
- Link: https://github.com/justajazz/ae-mcp-bridge
- Licence: MIT License (MIT) — LICENSE file verified in clone (the bridge ports tools from TheLlamainator/after-effects-mcp, itself MIT per the README)
- Popularity: 1 star, 6 commits (repo page, 2026-11-06)
- Last commit (from local clone git log): 2026-10-09
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: The repo is an MCP bridge (34 tools) for working inside After Effects — the bridge is a tool and is NOT extracted. Extracted here is only its optional bundled skill, skills/after-effects-motion/ — SKILL.md + RECIPES.md — which carries the bridge's motion-design guidelines (asymmetric easing, bounce, text animators, stagger, track mattes, motion blur, and the build→review loop) as agent-facing craft instructions.

---

## 📄 SOURCE FILE: `skills/after-effects-motion/SKILL.md` (verbatim)

---
name: after-effects-motion
description: "After Effects work through the after-effects MCP tools (ae_*) - building a design, animating it, reviewing motion, recreating a reference image, or scripting AE."
---

# After Effects through the bridge

The bridge exposes `ae_*` tools. The motion-design rules live in one place, the `ae_guidelines` tool; this skill is
the working loop around them. Recipes for common moves: [RECIPES.md](RECIPES.md).

## Loop

1. **Orient.** Call `ae_health`. When the user points at something ("this", "the selected layer"), call
   `ae_get_selection`; otherwise `ae_list_project`. Done when you know the target composition and the layers by name.
2. **Load the rules.** Call `ae_guidelines` once per session, before the first design or animation step.
3. **Build the still.** Create or edit with the dedicated tools; give every layer a meaningful name. Check with
   `ae_capture_frame` (add `compareWith` when recreating a reference). Done when the frame matches the brief and the
   user has seen it: agree on the still before animating.
4. **Animate.** Use the recipes; reach for `ae_run_jsx` only for what no tool covers, passing data through `args`.
5. **Review the motion.** Call `ae_capture_frames` over the animated range: 6-12 frames, denser around overshoots
   and overlaps. Walk the review checklist below against the sheet, fix, capture again. Done when every checklist
   item passes on a fresh sheet. Then offer `ae_render_preview` so the user can watch it.
6. **Report.** Say what changed and that each call is one Ctrl+Z; mention the project is unsaved and save only
   when the user asks (`ae_save_project`).

A result with `status: "running"` is still executing in After Effects: collect it with `ae_get_result` (with
`waitMs`) and send nothing new until it returns.

## Review checklist

Read each item off the storyboard frames:

- **Containment**: content stays inside its container while the container opens; clip it with a track matte
  (`ae_set_layer` `trackMatte`, `matteVisible: true` for the container).
- **Hierarchy**: the container moves first, its content follows, the focal element lands last or strongest.
- **Stagger**: related elements arrive a few frames apart, in reading order.
- **Easing**: entrances start fast and land softly; nothing starts from a dead stop unless intended.
- **Overshoot**: momentum carries through it, and the whole object reacts (width or scale too, not only height).
- **Sync**: properties of one object finish on the same frame.
- **Text**: letters overlap in a wave (rampUp) or lines arrive whole; offsets and blur suit the font size.
- **Motion blur**: on for every moving layer.
- **Timing**: entrances 0.4-1.2 s per element; the final state holds long enough to read.
- **Typography and spacing**: one type scale for secondary labels, even padding inside cards.

---

## 📄 SOURCE FILE: `skills/after-effects-motion/RECIPES.md` (verbatim)

# Recipes

Concrete tool calls for common moves. Paths use names; names, matchNames and 1-based indices all work.

## Card that opens with a bounce

A rounded rectangle shape layer `Card` (`ae_create_layer` type `shape`, shape `rectangle`, `roundness`).
Animate the **path size**, so corners keep their radius:

1. `ae_set_keyframes` on `Contents/Group 1/Contents/Rectangle Path 1/Size`:
   keys `[{time: 0, value: [W, 0], ease: "easyOut", influence: 20}, {time: 0.4, value: [W, H], ease: "linear"}]`.
   The landing key arrives with speed: the bounce expression turns that speed into the overshoot.
2. `ae_set_expression` on the same property with the inertial-bounce snippet from `ae_guidelines`.
3. For a whole-object feel add a small `Transform/Scale` bounce, or bounce the width as well.

## Text reveal

- Words or characters: `ae_add_text_animator` with defaults (soft wave, offsets position [0, 40], opacity 0, blur 16).
- Lines: `basedOn: "lines"` (square selector, strong ease).
- Several text layers: one call with `layers: [...]` and `stagger: 3-5`.
- Same animator on more layers later: `ae_copy_animation` from the first layer, `property: "Text/Animators/MCP Reveal"`,
  `to: [...]`, `stagger`.

## Number counter

`ae_set_expression` on `Source Text`:

```js
var t0 = inPoint + 0.3, t1 = t0 + 1.2, target = 8412;
var v = Math.round(ease(time, t0, t1, 0, target));
v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
```

## Content clipped by its card

`ae_set_layer` on the content layer: `trackMatte: "Card"`, `matteVisible: true`. Place the content directly above
the card in the layer stack.

## Motion blur

`ae_set_layer` `motionBlur: true` on every moving layer (this also turns on the composition switch);
`ae_set_comp` `shutterAngle: 180` for a natural amount.

## Recreate a reference

1. `ae_create_comp` with the reference's size.
2. Build shapes and text, measuring positions from the reference.
3. `ae_capture_frame` with `compareWith: "<path to the reference>"`; fix differences in spacing, sizes, colors.

## Markers on the beat

`ae_analyze_audio` with `comp`, `layer` (the music layer) and `addMarkers: true`; tune `threshold` (0.5-0.8) and
`minGap` (seconds) until the markers match the beats. Use the marker times as key times.

## Copy a look

`ae_copy_animation` copies effects (`Effects/Drop Shadow`), masks and single properties (`Transform/Position`) with
their keys; `ae_apply_preset` applies a saved `.ffx` (find it with `ae_list_presets`).
