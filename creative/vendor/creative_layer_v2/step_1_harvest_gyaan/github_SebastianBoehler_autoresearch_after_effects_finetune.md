# SebastianBoehler/autoresearch_after_effects_finetune — After Effects Motion Scripting skill (inside an MLX finetune scaffold)
- Repo: SebastianBoehler/autoresearch_after_effects_finetune
- Link: https://github.com/SebastianBoehler/autoresearch_after_effects_finetune
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 0 stars, 7 commits (repo page, 2026-11-06)
- Last commit (from local clone git log): 2026-06-11
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: The repo is a scaffold for fine-tuning a model on AE scripting data; extracted here is ONLY its skill folder skills/after-effects-motion-scripting/ — SKILL.md + references/extendscript-api-patterns.md + references/motion-design-patterns.md + references/review-rubric.md (the sample quality bar: an AE sample "must look intentional"). The finetune machinery and the synthetic .jsx dataset templates under data/ are not extracted.

---

## 📄 SOURCE FILE: `skills/after-effects-motion-scripting/SKILL.md` (verbatim)

---
name: after-effects-motion-scripting
description: Create, review, and iterate Adobe After Effects ExtendScript JSX animation scripts and curated dataset samples. Use when writing AE scripts, improving motion-graphics trailer samples, using AE scripting APIs such as comps/layers/shapes/text/cameras/lights/effects/imports/markers/expressions, debugging AE JSX runtime errors, or benchmarking model outputs for professional motion design quality.
---

# After Effects Motion Scripting

## Workflow

1. Decide whether the script is self-contained or asset-backed.
   - Self-contained scripts must create all visuals procedurally.
   - Asset-backed scripts must use tiny local fixtures, not live URLs or absolute machine paths.
2. Storyboard before coding: 3-6 distinct beats, one visual system, fast deliberate transitions, readable title/subtitle/final lockup.
3. Write ES3-safe ExtendScript: `var` only, no `let`, `const`, classes, arrow functions, template strings, destructuring, `forEach`, or `map`.
4. Use stable AE handles: reacquire properties after adding shape operators if needed, and add Trim Paths/Repeaters before Stroke/Fill when AE reports invalid object handles.
5. Verify narrow first, then visually:
   - `node --check --input-type=commonjs < script.jsx`
   - repo dataset rebuild and source verifier when working in this repo
   - live AE execution/manual preview when judging visual quality

## Quality Bar

Do not accept a sample because it demonstrates APIs. A useful AE sample must also look intentional.

- Prefer one strong visual grammar over many unrelated elements.
- Use hairlines, masks, trim-path reveals, offset timing, camera/null drift, and fast cuts deliberately.
- Keep secondary text readable; avoid tiny gray microcopy.
- Avoid generic centered cards, random grids, arbitrary squares, and palette-only variations.
- Avoid overlap: reserve clear text zones and keep decorative systems behind or beside copy.
- Use asset-backed samples only when the referenced assets are visibly meaningful and good enough.

## API Coverage Targets

Use the smallest set that improves coverage for the sample:

- Project/comps: `app.project.items.addComp`, nested comps, precomps, save paths.
- Layers: solids, shape layers, text/box text, footage layers, nulls, cameras, lights.
- Shapes: paths, rectangles, ellipses, groups, Trim Paths, Repeaters, strokes/fills.
- Animation: `setValueAtTime`, `KeyframeEase`, markers, expressions, time remap when useful.
- Assets: `File`, `Folder`, `ImportOptions`, `app.project.importFile`, image sequences, audio, JSON/GeoJSON/CSV fixtures, `replaceSource`.
- Effects/materials: built-in effects by match name, blend modes, 3D material options, lights/camera depth.

## Runtime Rules

Read [references/extendscript-api-patterns.md](references/extendscript-api-patterns.md) when implementing or debugging JSX.

Read [references/motion-design-patterns.md](references/motion-design-patterns.md) when improving visual taste, pacing, transitions, or sample diversity.

Read [references/review-rubric.md](references/review-rubric.md) when comparing model outputs, deciding whether a sample is curated, or writing benchmark notes.

## Repo Integration

When adding samples in this repo:

- Put JSX in `data/synthetic/templates/`.
- Keep each file under 300 LOC.
- Put small owned fixtures in `data/synthetic/assets/`.
- Add one manifest row in `data/synthetic/manifest.json`.
- Rebuild `data/after_effects_synthetic_cases.jsonl` with `uv run python scripts/build_synthetic_dataset.py`.
- Verify with `uv run python -m after_effects_pipeline.cli verify-source --config configs/lfm25_8b_a1b_after_effects.json`.

---

## 📄 SOURCE FILE: `skills/after-effects-motion-scripting/references/extendscript-api-patterns.md` (verbatim)

# ExtendScript API Patterns

## Safe Language Subset

After Effects JSX is ExtendScript, not modern browser JavaScript.

- Use `var`, functions, arrays, and plain objects.
- Avoid `let`, `const`, classes, arrow functions, template strings, destructuring, `forEach`, and `map`.
- Avoid reserved words as identifiers.
- Wrap fragile API calls in targeted `try/catch`, but do not hide whole-script failures unless writing a harness.

## Project Skeleton

```jsx
app.beginUndoGroup("AEFT Sample Name");
(function () {
    if (!app.project) app.newProject();
    var comp = app.project.items.addComp("AEFT Sample Name", 1920, 1080, 1, 12, 30);
    comp.bgColor = [0.02, 0.03, 0.04];
    // create layers
})();
app.endUndoGroup();
```

## Easing Helper

Use a dimension-aware helper and tolerate AE rejecting temporal easing on some properties.

```jsx
function ease(prop, influence) {
    if (!prop || prop.numKeys < 2) return;
    var dims = 1;
    try {
        if (prop.propertyValueType === PropertyValueType.TwoD || prop.propertyValueType === PropertyValueType.TwoD_SPATIAL) dims = 2;
        if (prop.propertyValueType === PropertyValueType.ThreeD || prop.propertyValueType === PropertyValueType.ThreeD_SPATIAL) dims = 3;
    } catch (e) {}
    for (var k = 1; k <= prop.numKeys; k++) {
        var ei = [], eo = [];
        for (var d = 0; d < dims; d++) {
            ei.push(new KeyframeEase(0, influence));
            eo.push(new KeyframeEase(0, influence));
        }
        try { prop.setTemporalEaseAtKey(k, ei, eo); } catch (ignore) {}
    }
}
```

## Shape Operator Order

AE can invalidate object handles after adding operators to a shape group. Prefer:

1. Create group.
2. Add shape/path.
3. Add Trim Paths or Repeater and animate those properties.
4. Add Stroke/Fill.

If AE reports “object is invalid,” reacquire the property or move the operator creation earlier.

## Local Asset Resolver

Use local fixtures and support both direct script runs and repo harnesses.

```jsx
function asset(rel) {
    var roots = [];
    if ($.global.AEFT_ASSET_ROOT) roots.push($.global.AEFT_ASSET_ROOT);
    var here = new File($.fileName).parent;
    roots.push(here.parent.fsName + "/assets");
    roots.push(here.fsName + "/../assets");
    for (var i = 0; i < roots.length; i++) {
        var f = new File(roots[i] + "/" + rel);
        if (f.exists) return f;
    }
    throw new Error("Missing asset: " + rel);
}
```

## JSON Fallback

Some AE runtimes lack global `JSON`.

```jsx
function parseJsonText(txt) {
    if (typeof JSON !== "undefined" && JSON.parse) return JSON.parse(txt);
    return (new Function("return " + txt))();
}
```

Only use the fallback for trusted local fixtures committed with the sample.

## Import Patterns

- Single file: `app.project.importFile(new ImportOptions(asset("image.png")))`.
- Image sequence: create `ImportOptions` from the first numbered frame and set `opts.sequence = true`.
- Audio: import WAV/AIFF, add as layer, then drive markers/visuals from separate local beat JSON.
- Replacement: create a placeholder layer and call `replaceSource(footageItem, false)`.

---

## 📄 SOURCE FILE: `skills/after-effects-motion-scripting/references/motion-design-patterns.md` (verbatim)

# Motion Design Patterns

## Scene Structure

Use 10-15 seconds as a sequence of beats, not one long animation:

1. Cold open signal, flash, or blade wipe.
2. Main visual system reveal.
3. Detail or data moment.
4. Contrast transition.
5. Secondary visual system.
6. Final title lockup.

## Professional Timing

- Use 2-4 frame attacks and longer settles.
- Stagger related elements by 2-5 frames.
- Let lines draw with Trim Paths before labels appear.
- Prefer hard cuts, matte wipes, shutters, and element-led transitions over crossfades.
- Keep the comp moving subtly with null/camera scale drift or parallax.

## Visual Grammar

Choose one dominant grammar per sample:

- Editorial typography: strong grid, large type, shutter cuts.
- Instrument UI: hairlines, rulers, readouts, restrained color.
- Luxury 3D: camera, lights, rings, slow premium parallax.
- Business: calm hierarchy, chart draw-ons, precise spacing.
- Festival/music: beat cuts, strobes, stage sweeps, reactive bursts.
- Asset-backed product: the imported asset must be clearly visible and worth looking at.

## Common Failures

- “API checklist” visuals: many features, no coherent scene.
- Random squares or panels behind text.
- Dense grids overlaying titles.
- Centered cards that never transition.
- Low-quality generated assets used as hero visuals.
- Small thin gray text that cannot be read.

## Fix Strategy

When a sample looks amateur, reduce visible element count first. Build a stronger stage:

- define title zone, hero zone, and annotation zone
- remove decorative clutter near text
- make one motion motif repeat across scenes
- add a decisive transition every 1.5-3 seconds
- make the final lockup simpler and more confident than the middle scenes

---

## 📄 SOURCE FILE: `skills/after-effects-motion-scripting/references/review-rubric.md` (verbatim)

# Review Rubric

## Static Gate

A sample can enter manual review only if:

- JSX syntax passes.
- It creates the expected comp.
- Required API snippets are present.
- Forbidden APIs are absent: `app.quit`, `system.callSystem`, `fetch`, `XMLHttpRequest`.
- It stays under the repo line limit.

## Visual Gate

Reject or mark for rework when:

- the result looks like simple shapes placed on screen
- text overlaps or is hard to read
- scene changes are too slow, flat, or repetitive
- assets are low quality or do not justify being imported
- API coverage is visible but the trailer would not be useful as training taste data

## Benchmarking Models

Compare models on:

- execution validity in AE
- script compactness and ES3 compatibility
- API breadth used correctly
- motion grammar diversity
- text readability
- transitions and pacing
- final lockup quality
- amount of manual repair needed

## Current Repo Notes

- `pro_motion_trailer_intro.jsx` is a strong benchmark for fast editorial pacing and readable copy.
- `celestial_clockwork_luxury_trailer.jsx` is a broad API-coverage benchmark for cameras, lights, null rigs, 3D layers, Trim Paths, Repeaters, and text.
- `product_sequence_launch_trailer.jsx` is useful for import/sequence/replaceSource coverage, but it is not visually accepted yet. Replace its PNG fixtures with high-quality product graphics and redesign the full motion language before promoting it.
