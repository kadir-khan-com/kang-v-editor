# aedev-tools/adobe-agent-skills — Adobe Agent Skills (After Effects domain-knowledge rules)
- Repo: aedev-tools/adobe-agent-skills
- Link: https://github.com/aedev-tools/adobe-agent-skills
- Licence: Apache License 2.0 (Apache-2.0) — verified on repo page + LICENSE file in clone
- Popularity: 116 stars, 7 forks, 18 commits (repo page, 2026-11-06)
- Last commit (from local clone git log): 2026-03-02
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Extracted: the after-effects skill's SKILL.md + all 9 rules/ domain-knowledge files (ExtendScript fundamentals, keyframes & animation, expressions, effects, composition management, layer manipulation, assets/footage, batch operations, rendering) + references/ae-api-versions.md. The skill ships 41 prebuilt .jsx scripts under skills/after-effects/scripts/ (39 in scripts/ + 2 lib files: utils, json2; there is also a runner.sh) — those are implementations of the rules, listed here by name only, not extracted: active-state, anchor-point-mover, batch-comp-settings, batch-expression, batch-rename, blend-mode-set, comp-detail, comp-from-csv, copy-ease, easing-presets, explode-shape-layer, expression-errors, expression-replace, fit-to-comp, font-inventory, font-replace, incremental-save, label-layers, layer-detail, layer-sort, layer-stagger, null-from-layers, organize-project, project-audit, project-cleanup, project-overview, purge-cache, randomize-properties, relink-footage, render-queue-batch, reverse-keyframes, select-layers, smart-precompose, split-layer, srt-import, text-export-import, trim-comp-to-content, true-comp-duplicator, un-precompose.

---

## 📄 SOURCE FILE: `skills/after-effects/SKILL.md` (verbatim)

---
name: after-effects
description: >
  Automate Adobe After Effects via ExtendScript. Use when the user asks to
  create, modify, or query anything in an After Effects project — layers,
  keyframes, expressions, effects, compositions, assets, rendering, batch
  operations. Generates and executes JSX ExtendScript via osascript on macOS.
compatibility: Requires macOS with Adobe After Effects installed. Needs "Allow Scripts to Write Files and Access Network" enabled in AE Preferences > Scripting & Expressions.
allowed-tools: Bash(osascript *) Bash(chmod *) Bash(bash *) Read Write
metadata:
  author: aedev-tools
  version: "1.0"
---

## Overview

This skill automates After Effects by generating ExtendScript (.jsx) and executing it via osascript. It reads project state through query scripts, uses rule files for domain knowledge, and wraps all mutations in undo groups.

## First-Time Setup

1. Run `scripts/runner.sh` with any query script to detect the AE version
2. If multiple AE versions are installed, the user must choose one — runner.sh will prompt
3. Ensure AE Preferences > Scripting & Expressions > "Allow Scripts to Write Files and Access Network" is enabled

## Workflow

For every user request:

### Step 1: Gather context (auto-run, no confirmation needed)

Use `--background` for all query scripts — this skips `ae.activate()` so AE doesn't steal focus:

```bash
bash scripts/runner.sh --background scripts/active-state.jsx
```
Then read `/tmp/ae-assistant-result.json` for active comp, selected layers, CTI.

If this is the first interaction or the project context is unknown, also run:
```bash
bash scripts/runner.sh --background scripts/project-overview.jsx
```
This returns a **summary** by default: folder tree with counts, all comps listed, footage grouped by file type. NOT every individual file.

To drill into a specific folder:
```bash
bash scripts/runner.sh --background scripts/project-overview.jsx '{"mode": "folder", "folderName": "Images"}'
```

Only use full mode when you actually need every item listed:
```bash
bash scripts/runner.sh --background scripts/project-overview.jsx '{"mode": "full"}'
```

### Step 2: Drill down if needed (auto-run)

If the task targets a specific comp:
```bash
bash scripts/runner.sh --background scripts/comp-detail.jsx '{"compName": "Comp Name"}'
```

If the task targets specific layers:
```bash
bash scripts/runner.sh --background scripts/layer-detail.jsx '{"layerNames": ["Layer 1", "Layer 2"]}'
```

Omit `compName` to use the active comp. Omit `layerNames` to use selected layers.

#### Additional query scripts

**Expression errors** — scan for broken expressions:
```bash
bash scripts/runner.sh --background scripts/expression-errors.jsx
bash scripts/runner.sh --background scripts/expression-errors.jsx '{"compName": "Main Comp"}'
```

**Font inventory** — list all fonts used across the project:
```bash
bash scripts/runner.sh --background scripts/font-inventory.jsx
```

**Project audit** — comprehensive health check (unused footage, missing files, expression errors, duplicate solids, font issues, empty folders):
```bash
bash scripts/runner.sh --background scripts/project-audit.jsx
bash scripts/runner.sh --background scripts/project-audit.jsx '{"checks": ["unused", "missing", "expressions"]}'
```

### Step 3: Load domain knowledge

Read the relevant rule file from `rules/`. Always read `rules/extendscript-fundamentals.md` — it contains ES3 constraints that apply to every generated script.

| Task involves | Load rule file |
|---|---|
| Layers (create, move, parent, duplicate) | [rules/layer-manipulation.md](rules/layer-manipulation.md) |
| Keyframes, animation, easing | [rules/keyframes-animation.md](rules/keyframes-animation.md) |
| Expressions | [rules/expressions.md](rules/expressions.md) |
| Compositions (create, precompose, nest) | [rules/composition-management.md](rules/composition-management.md) |
| Effects and parameters | [rules/effects.md](rules/effects.md) |
| Import, footage, assets | [rules/assets-footage.md](rules/assets-footage.md) |
| Render queue, export | [rules/rendering.md](rules/rendering.md) |
| Bulk/batch operations | [rules/batch-operations.md](rules/batch-operations.md) |
| Version-specific features | [references/ae-api-versions.md](references/ae-api-versions.md) |

### Step 4: Generate the action script

**CRITICAL: Resolve the skill's real path first**

Before writing or executing any action script, resolve the skill's real (non-symlinked) path. ExtendScript `#include` cannot follow symlinks, so you MUST use the real filesystem path.

Run this once at the start of each session:
```bash
SKILL_SCRIPTS="$(readlink -f ~/.claude/skills/after-effects-assistant/scripts 2>/dev/null || readlink ~/.claude/skills/after-effects-assistant/scripts)"
echo "$SKILL_SCRIPTS"
```

Use the resolved path (`$SKILL_SCRIPTS`) for all subsequent Write and Bash commands in this session.

**Why this matters:**
- `~/.claude/skills/` is typically a symlink — ExtendScript `#include` fails through symlinks
- Writing to the real `scripts/` directory lets `#include "lib/json2.jsx"` resolve correctly
- The resolved path changes per machine, so never hardcode it

Every generated script MUST follow this template:

```jsx
#include "lib/json2.jsx"
#include "lib/utils.jsx"

(function() {
    app.beginUndoGroup("AE Assistant: <action description>");
    try {
        var args = readArgs();
        var comp = getActiveComp();
        if (!comp) return;

        // ... action code ...

        writeResult({ success: true, message: "<what was done>" });
    } catch (e) {
        try { writeResult({ error: e.toString(), line: e.line, fileName: e.fileName }); }
        catch(e2) { writeError(e.toString(), "line:" + e.line); }
    } finally {
        app.endUndoGroup();
    }
})();
```

#### utils.jsx helpers available for generated scripts

| Function | Purpose |
|----------|---------|
| `writeResult(obj)` | Write JSON result to `/tmp/ae-assistant-result.json` |
| `writeError(msg, detail)` | Last-resort error capture when JSON.stringify fails |
| `readArgs()` | Read args from `/tmp/ae-assistant-args.json` |
| `getLayerType(layer)` | Returns type string: "shape", "text", "null", "precomp", etc. |
| `getBlendModeName(mode)` | BlendingMode enum → string name |
| `getActiveComp()` | Returns active comp or writes error and returns null |
| `getSelectedOrAllLayers(comp)` | Selected layers array, or all layers if none selected |
| `hexToRGB(hex)` | `"#ff0000"` → `[1, 0, 0]` |
| `getCompByName(name)` | Find comp in project items by name |
| `walkProperties(group, leafFn, path)` | Recursive property tree walker — calls `leafFn(prop, path)` on leaves |
| `bubbleSort(arr, compareFn)` | ES3-compatible in-place sort |
| `framesToSeconds(frames, comp)` | Frame count → seconds via `comp.frameDuration` |
| `appendLog(message)` | Append to `~/.ae-assistant-extendscript.log` |

**Write the script using the Write tool, then execute with a short bash command:**

1. Use the **Write** tool to write the script to `$SKILL_SCRIPTS/ae-action.jsx` (the resolved real path)
2. Execute it with bash:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/ae-action.jsx"
```

**IMPORTANT:** Do NOT use `cat > file << 'SCRIPT'` heredocs — they put the entire script in the bash command, cluttering the permission prompt. Always use the Write tool for the script content, then a short bash command to run it.

### Step 5: Execute or confirm

**Auto-run** (no confirmation needed):
- All read-only queries (active-state, project-overview, comp-detail, layer-detail, expression-errors, font-inventory, project-audit)
- Non-destructive additions: adding a keyframe, adding an effect, creating a layer, creating a comp

**Confirm before running** (show the script and ask the user):
- Deleting layers or comps
- Removing keyframes
- Replacing footage
- Clearing expressions
- Render queue operations
- Project cleanup (removing unused items, consolidating solids)
- Any operation the user might not expect

### Built-in action scripts

Before generating a custom `ae-action.jsx`, check if a built-in script already handles the task. These are permanent, tested scripts with args-based behavior:

**True Comp Duplicator** — deep-clone a comp with independent sub-comps (confirm before running):
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/true-comp-duplicator.jsx" '{"compName": "Main Comp", "suffix": " COPY"}'
```

**Font Replace** — find and replace fonts across the project. Always dryRun first:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/font-replace.jsx" '{"find": "Helvetica", "replace": "Inter-Regular", "dryRun": true}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/font-replace.jsx" '{"find": "Helvetica", "replace": "Inter-Regular"}'
```

**Project Cleanup** — remove unused footage, consolidate duplicate solids, remove empty folders. Always dryRun first:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/project-cleanup.jsx" '{"dryRun": true}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/project-cleanup.jsx"
```

**Batch Rename** — rename layers, comps, or project items in bulk:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-rename.jsx" '{"target": "layers", "mode": "find-replace", "find": "Layer", "replace": "Element"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-rename.jsx" '{"target": "layers", "mode": "prefix", "prefix": "BG_"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-rename.jsx" '{"target": "layers", "mode": "sequence", "base": "Card", "start": 1}'
```

**Layer Stagger** — offset selected layers in time for cascade animations:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/layer-stagger.jsx" '{"offset": 0.1, "unit": "seconds", "direction": "forward"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/layer-stagger.jsx" '{"offset": 2, "unit": "frames"}'
```

**Expression Replace** — find/replace text in expressions project-wide. Always dryRun first:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/expression-replace.jsx" '{"find": "comp(\"Old\")", "replace": "comp(\"New\")", "dryRun": true}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/expression-replace.jsx" '{"find": "comp(\"Old\")", "replace": "comp(\"New\")"}'
```

**Organize Project** — auto-sort project panel items into folders by type:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/organize-project.jsx" '{"structure": "by-type"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/organize-project.jsx" '{"structure": "by-extension"}'
```

**Batch Comp Settings** — change fps, resolution, duration across multiple comps:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-comp-settings.jsx" '{"scope": "all", "fps": 25}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-comp-settings.jsx" '{"compNames": ["Comp 1", "Comp 2"], "width": 3840, "height": 2160}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-comp-settings.jsx" '{"scope": "nested", "fps": 30, "duration": 10}'
```

**Easing Presets** — apply professional easing or bounce/elastic expressions:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/easing-presets.jsx" '{"preset": "smooth"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/easing-presets.jsx" '{"preset": "snappy"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/easing-presets.jsx" '{"preset": "bounce"}'
```

**Anchor Point Mover** — reposition anchor point with visual position compensation:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/anchor-point-mover.jsx" '{"position": "center"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/anchor-point-mover.jsx" '{"position": "bottom-left"}'
```

**Reverse Keyframes** — reverse animation on selected properties:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/reverse-keyframes.jsx"
```

**Select Layers** — select layers by type, label, attribute, or name:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/select-layers.jsx" '{"type": "text"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/select-layers.jsx" '{"hasExpressions": true}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/select-layers.jsx" '{"nameContains": "BG"}'
```

**Layer Sort** — reorder layers in timeline by name, position, in-point, type, or label:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/layer-sort.jsx" '{"sortBy": "name", "order": "ascending"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/layer-sort.jsx" '{"sortBy": "position-y"}'
```

**Smart Precompose** — precompose with auto-trimmed duration:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/smart-precompose.jsx" '{"name": "My Precomp", "trimToContent": true}'
```

**Copy Ease** — copy easing from one keyframe and paste to others:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/copy-ease.jsx" '{"mode": "both"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/copy-ease.jsx" '{"sourceLayer": "Logo", "sourceProperty": "Position", "sourceKeyIndex": 2}'
```

**Relink Footage** — batch-relink missing footage from search directories. Always dryRun first:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/relink-footage.jsx" '{"searchPaths": ["/Volumes/Projects/footage"], "dryRun": true}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/relink-footage.jsx" '{"searchPaths": ["/Volumes/Projects/footage"]}'
```

**SRT Import** — create timed subtitle text layers from an SRT file:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/srt-import.jsx" '{"srtPath": "/path/to/subs.srt", "fontSize": 48}'
```

**Text Export/Import** — export all text to CSV, edit externally, reimport:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/text-export-import.jsx" '{"mode": "export", "csvPath": "/tmp/text.csv"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/text-export-import.jsx" '{"mode": "import", "csvPath": "/tmp/text.csv"}'
```

**Batch Expression** — apply, remove, enable, or disable expressions in bulk:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-expression.jsx" '{"property": "opacity", "expression": "wiggle(2, 10)", "mode": "apply"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-expression.jsx" '{"mode": "remove"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/batch-expression.jsx" '{"mode": "disable"}'
```

**Randomize Properties** — apply random values to transform properties:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/randomize-properties.jsx" '{"property": "rotation", "min": -15, "max": 15}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/randomize-properties.jsx" '{"property": "position", "minX": 0, "maxX": 1920, "minY": 0, "maxY": 1080}'
```

**Un-PreCompose** — extract layers from a precomp back into parent (confirm before running):
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/un-precompose.jsx" '{"precompLayerName": "Precomp 1"}'
```

**Comp from CSV** — generate comp variations from spreadsheet data (confirm before running):
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/comp-from-csv.jsx" '{"templateComp": "Lower Third", "csvPath": "/path/data.csv"}'
```

**Render Queue Batch** — add multiple comps to render queue (confirm before running):
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/render-queue-batch.jsx" '{"compNames": ["Final_16x9", "Final_9x16"], "outputPath": "~/Desktop/renders/"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/render-queue-batch.jsx" '{"scope": "folder", "folderName": "Finals"}'
```

**Explode Shape Layer** — split shape groups into individual layers:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/explode-shape-layer.jsx" '{"layerName": "AI Import"}'
```

**Incremental Save** — save project with auto-incrementing version number:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/incremental-save.jsx" '{"comment": "before revisions"}'
```

**Purge Cache** — clear memory caches, disk cache, and free resources. dryRun to check size first:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/purge-cache.jsx" '{"dryRun": true}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/purge-cache.jsx"
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/purge-cache.jsx" '{"memory": true, "disk": false}'
```

**Trim Comp to Content** — trim/extend comp duration to exactly fit layer content:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/trim-comp-to-content.jsx"
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/trim-comp-to-content.jsx" '{"padding": 0.5}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/trim-comp-to-content.jsx" '{"recursive": true}'
```

**Null from Layers** — create a null at each selected layer's position, auto-parent:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/null-from-layers.jsx"
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/null-from-layers.jsx" '{"naming": "custom", "prefix": "Driver"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/null-from-layers.jsx" '{"position": "comp-center"}'
```

**Fit to Comp** — scale selected layers to fit/fill comp dimensions:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/fit-to-comp.jsx" '{"mode": "fit"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/fit-to-comp.jsx" '{"mode": "fill"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/fit-to-comp.jsx" '{"mode": "stretch"}'
```

**Label Layers** — batch-set label colors on layers by type, name, or selection:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/label-layers.jsx" '{"label": 3, "target": "selected"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/label-layers.jsx" '{"label": 1, "target": "text"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/label-layers.jsx" '{"label": 5, "target": "all", "nameContains": "BG"}'
```

**Blend Mode Set** — set blending mode on selected layers:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/blend-mode-set.jsx" '{"mode": "SCREEN"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/blend-mode-set.jsx" '{"mode": "MULTIPLY"}'
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/blend-mode-set.jsx" '{"mode": "ADD"}'
```

**Split Layer** — split selected layers at CTI (confirm before running — modifies layer timing):
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/split-layer.jsx"
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/split-layer.jsx" '{"time": 2.5}'
```

### Step 6: Execute and read result

```bash
# Execute the action script (already written to $SKILL_SCRIPTS/ae-action.jsx in Step 4)
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/ae-action.jsx" '{"arg1": "value1"}'
```

Read `/tmp/ae-assistant-result.json` for the result.

### Debugging failures

If a script fails, check these in order:
1. **`~/.ae-assistant-log`** — runner.sh logs every execution, args, results, and errors here
2. **`/tmp/ae-assistant-error.txt`** — JXA-level errors (AE not responding, DoScriptFile failure)
3. **`~/.ae-assistant-extendscript.log`** — ExtendScript-level logs from `appendLog()` in utils.jsx
4. **AE Preferences** — Ensure "Allow Scripts to Write Files and Access Network" is enabled

When an error occurs, read `~/.ae-assistant-log` to understand what happened, fix the script, and retry.

## MUST

- ALWAYS wrap mutations in `app.beginUndoGroup()` / `app.endUndoGroup()`
- ALWAYS use matchNames for property access, not display names (display names are localized)
- ALWAYS use 1-based indexing for layers and project items
- ALWAYS write action scripts to `$SKILL_SCRIPTS/ae-action.jsx` (the resolved real path, NOT `/tmp/`)
- ALWAYS use relative `#include "lib/json2.jsx"` and `#include "lib/utils.jsx"` (NOT absolute paths)
- ALWAYS wrap in an IIFE to avoid global scope pollution
- ALWAYS use `var`, never `let` or `const` (ES3)
- ALWAYS write results to /tmp/ae-assistant-result.json via writeResult()
- ALWAYS use `getActiveComp()` to get the active comp (handles the null/CompItem check and writes error)
- ALWAYS use `--background` flag for query scripts to avoid focus-steal

## FORBIDDEN

- NEVER use ES5+ syntax: let, const, arrow functions, template literals, destructuring
- NEVER use Array.map, Array.filter, Array.reduce, Array.forEach (not in ES3)
- NEVER use JSON.parse or JSON.stringify without including json2.jsx
- NEVER write action scripts to `/tmp/` — ExtendScript `#include` can't resolve paths from there
- NEVER use absolute paths in `#include` — they break through symlinks
- NEVER hardcode layer indices — use names, selection, or iteration
- NEVER run destructive operations without user confirmation
- NEVER assume a comp is active without checking
- NEVER use `cat > file << 'SCRIPT'` heredocs to write scripts — use the Write tool instead, then execute with a short bash command

---

## 📄 SOURCE FILE: `skills/after-effects/rules/extendscript-fundamentals.md` (verbatim)

# ExtendScript Fundamentals

> **This rule file is REQUIRED for every interaction.** It defines the language constraints, DOM hierarchy, and patterns that apply to all generated ExtendScript code.

---

## ES3 Syntax Constraints

ExtendScript is based on **ECMAScript 3 (ES3)**. Modern JavaScript features do not exist.

### FORBIDDEN Syntax

FORBIDDEN: `let` and `const` declarations. Use `var` for all variable declarations.

```jsx
// WRONG - will cause a syntax error
let x = 10;
const y = 20;

// CORRECT
var x = 10;
var y = 20;
```

FORBIDDEN: Arrow functions. Use the `function` keyword for all function definitions.

```jsx
// WRONG - will cause a syntax error
var double = (x) => x * 2;
var greet = () => { return "hello"; };

// CORRECT
var double = function(x) { return x * 2; };
function greet() { return "hello"; }
```

FORBIDDEN: Template literals. Use string concatenation with `+`.

```jsx
// WRONG - will cause a syntax error
var msg = `Layer ${name} at position ${pos}`;

// CORRECT
var msg = "Layer " + name + " at position " + pos;
```

FORBIDDEN: Destructuring assignment.

```jsx
// WRONG - will cause a syntax error
var { name, index } = layer;
var [x, y] = position;

// CORRECT
var name = layer.name;
var index = layer.index;
var x = position[0];
var y = position[1];
```

FORBIDDEN: Default parameters.

```jsx
// WRONG - will cause a syntax error
function createLayer(name, width, height) {
    width = width || 1920;  // This pattern is OK as a workaround
}

// WRONG - will cause a syntax error
function createLayer(name, width = 1920, height = 1080) {}

// CORRECT
function createLayer(name, width, height) {
    if (width === undefined) width = 1920;
    if (height === undefined) height = 1080;
}
```

FORBIDDEN: Spread operator.

```jsx
// WRONG - will cause a syntax error
var merged = [...arr1, ...arr2];
doSomething(...args);

// CORRECT
var merged = arr1.concat(arr2);
```

FORBIDDEN: `for...of` loops.

```jsx
// WRONG - will cause a syntax error
for (var item of collection) {}

// CORRECT
for (var i = 0; i < collection.length; i++) {
    var item = collection[i];
}
```

FORBIDDEN: `class` declarations.

```jsx
// WRONG - will cause a syntax error
class MyThing {
    constructor(name) { this.name = name; }
}

// CORRECT
function MyThing(name) {
    this.name = name;
}
```

FORBIDDEN: `Array.prototype.forEach`, `Array.prototype.map`, `Array.prototype.filter`, `Array.prototype.reduce`. These do not exist in ES3. Use `for` loops for all iteration.

```jsx
// WRONG - will throw a runtime error (not a function)
layers.forEach(function(layer) { layer.enabled = false; });
var names = layers.map(function(l) { return l.name; });
var visible = layers.filter(function(l) { return l.enabled; });

// CORRECT
for (var i = 0; i < layers.length; i++) {
    layers[i].enabled = false;
}

var names = [];
for (var i = 0; i < layers.length; i++) {
    names.push(layers[i].name);
}

var visible = [];
for (var i = 0; i < layers.length; i++) {
    if (layers[i].enabled) {
        visible.push(layers[i]);
    }
}
```

FORBIDDEN: `Object.keys()`, `Object.values()`, `Object.entries()`. Use `for...in` with `hasOwnProperty`.

```jsx
// WRONG - will throw a runtime error
var keys = Object.keys(obj);

// CORRECT
var keys = [];
for (var key in obj) {
    if (obj.hasOwnProperty(key)) {
        keys.push(key);
    }
}
```

### Allowed ES3 Features

These standard constructs work in ExtendScript:

- `var` declarations
- `function` declarations and expressions
- `for`, `for...in`, `while`, `do...while` loops
- `if/else`, `switch/case`
- `try/catch/finally`
- `new`, `delete`, `typeof`, `instanceof`
- `Array`, `String`, `Number`, `Boolean`, `RegExp`, `Date`, `Math`
- `Array.prototype.push`, `.pop`, `.shift`, `.unshift`, `.splice`, `.slice`, `.concat`, `.join`, `.sort`, `.reverse`, `.indexOf` (ExtendScript adds indexOf)
- `String.prototype.indexOf`, `.lastIndexOf`, `.charAt`, `.substring`, `.slice`, `.split`, `.replace`, `.match`, `.search`, `.toLowerCase`, `.toUpperCase`
- `parseInt()`, `parseFloat()`, `isNaN()`, `isFinite()`
- Regular expressions via `new RegExp()` or `/pattern/` literals

---

## JSON Serialization

There is no native `JSON` object in ES3. Calling `JSON.parse()` or `JSON.stringify()` without including the polyfill will throw a runtime error.

MUST include `json2.jsx` before any JSON operation:

```jsx
#include "lib/json2.jsx"

// Now JSON.parse and JSON.stringify are available
var obj = JSON.parse(content);
var str = JSON.stringify(obj);
```

The `#include` directive path is relative to the script file location, not the working directory.

---

## After Effects DOM Hierarchy

The AE scripting object model follows this tree structure:

```
Application (app)
  |-- Project (app.project)
  |     |-- ItemCollection (app.project.items)
  |     |     |-- FolderItem
  |     |     |-- FootageItem
  |     |     |-- CompItem
  |     |     |     |-- LayerCollection (comp.layers)
  |     |     |           |-- AVLayer
  |     |     |           |     |-- TextLayer (extends AVLayer)
  |     |     |           |     |-- ShapeLayer (extends AVLayer)
  |     |     |           |-- CameraLayer
  |     |     |           |-- LightLayer
  |     |     |
  |     |     |     Each Layer has:
  |     |     |           |-- PropertyGroup ("ADBE Transform Group", etc.)
  |     |     |                 |-- Property ("ADBE Position", "ADBE Opacity", etc.)
  |     |
  |     |-- RenderQueue (app.project.renderQueue)
  |           |-- RQItemCollection (renderQueue.items)
  |                 |-- RenderQueueItem
  |                       |-- OutputModule (rqItem.outputModule(1))
```

Key access patterns:

```jsx
var project = app.project;
var comp = app.project.activeItem;          // Currently open comp (may be null)
var item = app.project.item(1);             // First item in project (1-based)
var layer = comp.layer(1);                  // Top layer in comp (1-based)
var prop = layer.property("ADBE Position"); // Access property by matchName
```

---

## Indexing Rules

### 1-Based Indexing (AE Collections)

MUST use 1-based indexing for all After Effects collections. The first item is at index 1, not 0.

```jsx
// Layers in a composition
var topLayer = comp.layer(1);              // First (top) layer
var lastLayer = comp.layer(comp.numLayers); // Last (bottom) layer

// Project items
var firstItem = app.project.item(1);
var lastItem = app.project.item(app.project.numItems);

// Folder items
var firstChild = folder.item(1);

// Effect properties
var firstEffect = effects.property(1);

// Properties within a group
var firstProp = group.property(1);
var count = group.numProperties;            // numProperties counts from 1

// Keyframes
var firstKeyTime = prop.keyTime(1);
var firstKeyValue = prop.keyValue(1);
```

### 0-Based Indexing (JavaScript Arrays)

Standard JavaScript arrays returned by AE are 0-based:

```jsx
// selectedLayers returns a JavaScript array
var sel = comp.selectedLayers;  // Standard JS array, 0-based
var firstSelected = sel[0];
var lastSelected = sel[sel.length - 1];

// selectedProperties returns a JavaScript array
var selProps = comp.selectedProperties;  // 0-based
var firstProp = selProps[0];
```

### Common Indexing Mistake

```jsx
// WRONG - index 0 does not exist in AE collections
var layer = comp.layer(0);        // throws error
var item = app.project.item(0);   // throws error

// WRONG - treating selectedLayers as 1-based
var first = comp.selectedLayers[1]; // skips the actual first element

// CORRECT
var layer = comp.layer(1);
var first = comp.selectedLayers[0];
```

### Iteration Patterns

```jsx
// Iterating AE collections (1-based)
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
}

for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
}

for (var i = 1; i <= group.numProperties; i++) {
    var prop = group.property(i);
}

// Iterating JavaScript arrays (0-based)
var sel = comp.selectedLayers;
for (var i = 0; i < sel.length; i++) {
    var layer = sel[i];
}
```

---

## Property Access via matchNames

MUST use matchNames (internal identifiers) instead of display names when accessing properties. Display names are localized and will break in non-English installations of After Effects.

```jsx
// WRONG - display names are localized, will fail in non-English AE
var pos = layer.property("Transform").property("Position");

// CORRECT - matchNames are stable across all languages
var pos = layer.property("ADBE Transform Group").property("ADBE Position");
```

### Common matchNames Reference

#### Transform Properties

| matchName | Display Name | Notes |
|---|---|---|
| `ADBE Transform Group` | Transform | Property group containing all transform props |
| `ADBE Anchor Point` | Anchor Point | Value: `[x, y]` or `[x, y, z]` for 3D layers |
| `ADBE Position` | Position | Value: `[x, y]` or `[x, y, z]` for 3D layers |
| `ADBE Position_0` | X Position | Only when dimensions are separated |
| `ADBE Position_1` | Y Position | Only when dimensions are separated |
| `ADBE Position_2` | Z Position | Only when dimensions are separated (3D) |
| `ADBE Scale` | Scale | Value: `[x, y]` or `[x, y, z]` as percentages (100 = 100%) |
| `ADBE Rotate Z` | Rotation | Value: degrees. Also called Z Rotation for 3D layers |
| `ADBE Rotate X` | X Rotation | Only on 3D layers |
| `ADBE Rotate Y` | Y Rotation | Only on 3D layers |
| `ADBE Orientation` | Orientation | Only on 3D layers. Value: `[x, y, z]` degrees |
| `ADBE Opacity` | Opacity | Value: 0-100 |

#### Layer Property Groups

| matchName | Display Name | Notes |
|---|---|---|
| `ADBE Effect Parade` | Effects | Container for all effects on a layer |
| `ADBE Mask Parade` | Masks | Container for all masks on a layer |
| `ADBE Text Properties` | Text | Text layer properties group |
| `ADBE Text Document` | Source Text | The text content property (child of Text Properties) |
| `ADBE Root Vectors Group` | Contents | Shape layer contents group |
| `ADBE Audio Group` | Audio | Audio properties group |
| `ADBE Marker` | Marker | Layer marker property |
| `ADBE Material Options Group` | Material Options | 3D material properties |
| `ADBE Layer Styles` | Layer Styles | Photoshop-style layer effects |

#### Accessing Transform Properties (Full Pattern)

```jsx
var xform = layer.property("ADBE Transform Group");
var position = xform.property("ADBE Position");
var scale = xform.property("ADBE Scale");
var rotation = xform.property("ADBE Rotate Z");
var opacity = xform.property("ADBE Opacity");
var anchorPoint = xform.property("ADBE Anchor Point");

// 3D layer additional properties
if (layer instanceof AVLayer && layer.threeDLayer) {
    var xRot = xform.property("ADBE Rotate X");
    var yRot = xform.property("ADBE Rotate Y");
    var orientation = xform.property("ADBE Orientation");
}

// Separated position dimensions
var posProp = xform.property("ADBE Position");
if (posProp.dimensionsSeparated) {
    var xPos = xform.property("ADBE Position_0");
    var yPos = xform.property("ADBE Position_1");
    var zPos = xform.property("ADBE Position_2"); // 3D only
}
```

#### Accessing Effects

```jsx
var effects = layer.property("ADBE Effect Parade");
if (effects && effects.numProperties > 0) {
    for (var i = 1; i <= effects.numProperties; i++) {
        var effect = effects.property(i);
        var effectName = effect.name;
        var effectMatchName = effect.matchName;
    }
}

// Add an effect by matchName
var blur = effects.addProperty("ADBE Gaussian Blur 2");
blur.property("ADBE Gaussian Blur 2-0001").setValue(10); // Blurriness parameter
```

#### Accessing Text Properties

```jsx
var textProp = layer.property("ADBE Text Properties").property("ADBE Text Document");
var textDoc = textProp.value;

// Read text properties
var content = textDoc.text;
var fontSize = textDoc.fontSize;
var fontName = textDoc.font;
var fillColor = textDoc.fillColor;    // [r, g, b] in 0-1 range

// Modify text
textDoc.text = "New text content";
textDoc.fontSize = 48;
textDoc.font = "ArialMT";
textDoc.fillColor = [1, 0, 0];       // Red
textProp.setValue(textDoc);
```

#### Accessing Shape Layer Contents

```jsx
var contents = layer.property("ADBE Root Vectors Group");
if (contents) {
    for (var i = 1; i <= contents.numProperties; i++) {
        var shapeGroup = contents.property(i);
        // Shape groups contain paths, fills, strokes, transforms
    }
}
```

---

## Type Checking

Use `instanceof` to determine item and layer types. This is the reliable way to branch logic based on what kind of object you have.

### Project Item Types

```jsx
var item = app.project.item(i);

if (item instanceof CompItem) {
    // Composition - has layers, duration, fps, etc.
} else if (item instanceof FolderItem) {
    // Folder - contains other items
} else if (item instanceof FootageItem) {
    // Footage - video, image, audio, solid, placeholder
}
```

### Layer Types

```jsx
var layer = comp.layer(i);

if (layer instanceof TextLayer) {
    // Text layer (extends AVLayer)
} else if (layer instanceof ShapeLayer) {
    // Shape layer (extends AVLayer)
} else if (layer instanceof CameraLayer) {
    // Camera layer - no source, no transform opacity
} else if (layer instanceof LightLayer) {
    // Light layer - no source, has light options
} else if (layer instanceof AVLayer) {
    // Audio/video layer - footage, solid, precomp, null, adjustment
    if (layer.nullLayer) {
        // Null object
    } else if (layer.adjustmentLayer) {
        // Adjustment layer
    } else if (layer.source instanceof CompItem) {
        // Pre-comp layer
    }
}
```

### Layer matchName Values

For more granular type detection, use `layer.matchName`:

| matchName | Layer Type |
|---|---|
| `ADBE AV Layer` | AVLayer (footage, solid, precomp, null, adjustment) |
| `ADBE Text Layer` | TextLayer |
| `ADBE Vector Layer` | ShapeLayer |
| `ADBE Camera Layer` | CameraLayer |
| `ADBE Light Layer` | LightLayer |

```jsx
switch (layer.matchName) {
    case "ADBE AV Layer":
        // General AV layer
        break;
    case "ADBE Text Layer":
        // Text layer
        break;
    case "ADBE Vector Layer":
        // Shape layer
        break;
    case "ADBE Camera Layer":
        // Camera
        break;
    case "ADBE Light Layer":
        // Light
        break;
}
```

### Active Item Check

MUST always verify the active item is a composition before using it:

```jsx
var comp = app.project.activeItem;

// WRONG - activeItem can be null, a FootageItem, or a FolderItem
comp.numLayers; // may throw

// CORRECT
if (!comp || !(comp instanceof CompItem)) {
    writeResult({ error: "No active composition" });
    return;
}
// Safe to use comp now
```

---

## File I/O Pattern

ExtendScript uses the `File` and `Folder` objects for filesystem operations.

### Reading a File

```jsx
var f = new File("/path/to/file.txt");
if (f.exists) {
    f.encoding = "UTF-8";
    f.open("r");
    var content = f.read();
    f.close();
} else {
    // File does not exist
}
```

### Writing a File

```jsx
var f = new File("/path/to/output.txt");
f.encoding = "UTF-8";
f.open("w");
f.write("content to write");
f.close();
```

### File Dialog (Interactive Only)

```jsx
// Open file dialog - ONLY for interactive scripts, never automated
var f = File.openDialog("Select a file", "*.jsx;*.json");
if (f) {
    // user selected a file
}

// Save file dialog
var f = File.saveDialog("Save as", "*.json");
```

### Folder Operations

```jsx
var dir = new Folder("/path/to/directory");
if (!dir.exists) {
    dir.create();
}

// List files in a folder
var files = dir.getFiles("*.jsx");
for (var i = 0; i < files.length; i++) {
    var fileName = files[i].name;
}
```

### Path Notes

- Use forward slashes `/` even on Windows (ExtendScript normalizes)
- `file.fsName` gives the platform-native path
- `file.fullName` gives the URI-style path
- `Folder.desktop` returns the desktop folder
- `Folder.temp` returns the system temp folder
- `$.fileName` returns the path of the currently executing script

---

## Undo Group Pattern

MUST wrap all mutation operations in an undo group. This allows the user to undo the entire operation with a single Cmd+Z.

```jsx
app.beginUndoGroup("AE Assistant: Descriptive Action Name");
try {
    // All mutation operations go here
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        writeResult({ error: "No active composition" });
        return;
    }

    // ... perform operations ...

    writeResult({ success: true, message: "Completed action description" });
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

Rules for undo groups:

- MUST call `app.endUndoGroup()` in the `finally` block so it runs even on error
- MUST use a descriptive name that tells the user what happened (appears in Edit > Undo)
- MUST NOT nest undo groups (AE ignores inner `beginUndoGroup` calls)
- Read-only queries do not need undo groups

---

## IIFE Pattern

MUST wrap all script code in an Immediately Invoked Function Expression (IIFE) to prevent global scope pollution. Without this, variables from one script execution could leak into subsequent runs.

```jsx
(function() {
    // All script code goes here
    // Variables declared with var are scoped to this function
    var comp = app.project.activeItem;
    // ...
})();
```

### Full Script Template

Combining the IIFE, undo group, and error handling patterns:

```jsx
#include "lib/json2.jsx"
#include "lib/utils.jsx"

(function() {
    app.beginUndoGroup("AE Assistant: Action Name");
    try {
        var args = readArgs();
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            writeResult({ error: "No active composition" });
            return;
        }

        // ... action code using args and comp ...

        writeResult({ success: true, message: "What was done" });
    } catch (e) {
        writeResult({ error: e.toString(), line: e.line });
    } finally {
        app.endUndoGroup();
    }
})();
```

---

## Common Gotchas

### TextDocument Properties Require an Associated Layer

Some `TextDocument` properties can only be set after the text layer exists. Setting them on a standalone `TextDocument` (before passing to `addText()`) throws: "Unable to set value as it is not associated with a layer."

```jsx
// WRONG - justification cannot be set before layer creation
var textDoc = new TextDocument("Hello");
textDoc.justification = ParagraphJustification.CENTER_JUSTIFY; // THROWS

// CORRECT - create layer first, then modify via property
var textLayer = comp.layers.addText("Hello");
var textProp = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
var textDoc = textProp.value;
textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
textDoc.fontSize = 48;
textProp.setValue(textDoc);
```

Safe before `addText()`: `text`, `fontSize`, `font`, `fillColor`, `strokeColor`, `applyFill`, `applyStroke`.
Must set after layer creation: `justification`, `boxText`, `boxTextSize`, `baselineShift`, `tracking`.

### Locked Layers Block All Modifications

Any write operation on a locked layer throws an error — including `moveToEnd()`, `moveToBeginning()`, property changes, and effect additions. Always unlock first:

```jsx
var wasLocked = layer.locked;
if (wasLocked) layer.locked = false;
// ... perform operations ...
if (wasLocked) layer.locked = true;
```

### layer.source Throws for Some Layer Types

Cameras, lights, and some null layers do not have a `.source` property. Accessing it throws an error.

```jsx
// WRONG - will throw for cameras and lights
var sourceName = layer.source.name;

// CORRECT
var sourceName = null;
try {
    if (layer.source) {
        sourceName = layer.source.name;
    }
} catch (e) {
    // Layer has no source (camera, light, or orphaned null)
}
```

### property.value Throws on Some Property Types

Certain properties (such as dropdown menus with no value set, or marker properties) throw when you access `.value`.

```jsx
// WRONG - may throw
var val = prop.value;

// CORRECT - wrap in try/catch when property type is uncertain
var val = null;
try {
    val = prop.value;
} catch (e) {
    // Property does not support .value or has no value
}
```

### alert() Blocks the AE User Interface

FORBIDDEN: Do not use `alert()` in automated scripts. It pops up a modal dialog and blocks AE until the user clicks OK, which defeats the purpose of automation.

```jsx
// FORBIDDEN in automated scripts
alert("Operation complete!");

// CORRECT - write results to file for the runner to read
writeResult({ success: true, message: "Operation complete" });
```

### $.writeln() for Debug Logging

`$.writeln()` writes to the ExtendScript Toolkit console. Useful during development but not for production output.

```jsx
// Debug logging (only for development)
$.writeln("Debug: layer count = " + comp.numLayers);

// Production output - use writeResult
writeResult({ layerCount: comp.numLayers });
```

### String Comparison Is Case-Sensitive

```jsx
// This will NOT match "My Layer" if the actual name is "my layer"
if (layer.name === "my layer") { }

// For case-insensitive comparison, normalize both sides
if (layer.name.toLowerCase() === "my layer") { }
```

### #include Paths Are Relative to the Script File

The `#include` directive resolves paths relative to the location of the `.jsx` file being executed, not the current working directory or the AE application.

```jsx
// If the script is at: /path/to/skills/scripts/action.jsx
// Then this resolves to: /path/to/skills/scripts/lib/json2.jsx
#include "lib/json2.jsx"

// Absolute paths also work
#include "/absolute/path/to/json2.jsx"
```

### app.project.activeItem Can Be Null or Non-Comp

`app.project.activeItem` returns whatever is currently active in the AE UI. This can be:
- `null` (nothing is active)
- A `CompItem` (a composition is open)
- A `FootageItem` (footage viewer is open)
- A `FolderItem` (a folder is selected in the project panel)

MUST check with `instanceof` before using as a composition:

```jsx
var item = app.project.activeItem;

// WRONG - item might be null or a non-comp
item.numLayers;

// CORRECT
if (item && item instanceof CompItem) {
    var comp = item;
    // Safe to use comp.numLayers, comp.layer(), etc.
}
```

### Collections Are 1-Based but .length Is Standard

AE collection objects use 1-based indexing, and their count properties (`.numLayers`, `.numProperties`, `.numItems`) start counting from 1.

```jsx
// A comp with 5 layers:
comp.numLayers;       // 5
comp.layer(1);        // First layer (top)
comp.layer(5);        // Last layer (bottom)
comp.layer(0);        // ERROR - no index 0
comp.layer(6);        // ERROR - out of range

// Correct iteration
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
}
```

### selectedLayers Returns a Standard JS Array (0-Based)

Unlike AE collections, `selectedLayers` and `selectedProperties` return regular JavaScript arrays with 0-based indexing.

```jsx
var sel = comp.selectedLayers;

// This is a standard JS array
sel.length;     // Number of selected layers
sel[0];         // First selected layer (0-based)
sel[1];         // Second selected layer

// Correct iteration (0-based)
for (var i = 0; i < sel.length; i++) {
    var layer = sel[i];
}

// WRONG - treating selectedLayers as 1-based
sel[1]; // This is the SECOND selected layer, not the first
```

### Modifying Collections During Iteration

Removing layers or items while iterating forward causes index shifting. MUST iterate in reverse when deleting.

```jsx
// WRONG - indices shift after each removal
for (var i = 1; i <= comp.numLayers; i++) {
    if (shouldDelete(comp.layer(i))) {
        comp.layer(i).remove(); // Next layer shifts down, gets skipped
    }
}

// CORRECT - iterate in reverse
for (var i = comp.numLayers; i >= 1; i--) {
    if (shouldDelete(comp.layer(i))) {
        comp.layer(i).remove(); // Safe, earlier indices unaffected
    }
}
```

### Property Existence Checks

Not all layers have all property groups. Always check before accessing sub-properties.

```jsx
// WRONG - shape layers have Contents, but text layers do not
var contents = layer.property("ADBE Root Vectors Group"); // null for non-shape layers
contents.numProperties; // throws if contents is null

// CORRECT
var contents = layer.property("ADBE Root Vectors Group");
if (contents && contents.numProperties > 0) {
    // Safe to iterate
}
```

### Numeric Precision

AE uses floating-point internally. Avoid exact equality comparisons on time values and property values.

```jsx
// WRONG - floating point comparison
if (comp.time === 2.5) { }

// CORRECT - compare with tolerance
var epsilon = 0.001;
if (Math.abs(comp.time - 2.5) < epsilon) { }
```

### Property Value Types Quick Reference

| Property | Value Type | Example |
|---|---|---|
| Position (2D) | Array `[x, y]` | `[960, 540]` |
| Position (3D) | Array `[x, y, z]` | `[960, 540, 0]` |
| Scale (2D) | Array `[x, y]` | `[100, 100]` (percentages) |
| Scale (3D) | Array `[x, y, z]` | `[100, 100, 100]` (percentages) |
| Rotation | Number | `45` (degrees) |
| Opacity | Number | `100` (0-100) |
| Color | Array `[r, g, b]` | `[1, 0, 0]` (0-1 range, this is red) |
| Anchor Point (2D) | Array `[x, y]` | `[0, 0]` |
| Anchor Point (3D) | Array `[x, y, z]` | `[0, 0, 0]` |
| Source Text | `TextDocument` object | Must use `.value` then modify, then `.setValue()` |
| Checkbox | Number | `0` or `1` |
| Slider | Number | Any float |
| Angle | Number | Degrees |
| Point (2D) | Array `[x, y]` | Normalized 0-1 for effect points |

---

## 📄 SOURCE FILE: `skills/after-effects/rules/keyframes-animation.md` (verbatim)

# Keyframes & Animation

> **Loaded when:** the task involves keyframes, animation, easing, interpolation, or temporal/spatial curves.

All code in this file is ES3-compatible ExtendScript. See `extendscript-fundamentals.md` for baseline syntax rules.

---

## Property Value Types Quick Reference

| Property | Type | Example Value | Notes |
|---|---|---|---|
| Position (2D) | Array | `[960, 540]` | Pixels from top-left |
| Position (3D) | Array | `[960, 540, 0]` | Z = depth |
| Scale | Array | `[100, 100]` or `[100, 100, 100]` | Percentages, not decimals |
| Rotation (Z) | Number | `45` | Degrees, single float |
| Rotation X/Y | Number | `0` | Only on 3D layers |
| Orientation | Array | `[0, 0, 0]` | 3D only, degrees |
| Opacity | Number | `50` | Range 0-100 |
| Color | Array | `[1, 0, 0, 1]` | RGBA, each 0.0-1.0 |
| Anchor Point | Array | `[0, 0]` or `[0, 0, 0]` | Pixels |

---

## Reading Keyframes

```jsx
var prop = layer.property("ADBE Transform Group").property("ADBE Position");

// Check whether the property is keyframed
var numKeys = prop.numKeys; // 0 means no keyframes (static value)

// Iterate all keyframes (1-based index)
for (var k = 1; k <= prop.numKeys; k++) {
    var time  = prop.keyTime(k);   // seconds as float
    var value = prop.keyValue(k);  // value at that keyframe
}

// Current value (at CTI for keyframed props, static value otherwise)
var currentValue = prop.value;

// Value at an arbitrary time
// Second arg: false = post-expression value, true = pre-expression value
var valAtTime = prop.valueAtTime(2.5, false);
```

### Nearest Keyframe

```jsx
// Returns the 1-based index of the keyframe closest to the given time
var idx = prop.nearestKeyIndex(1.5);
var nearestTime = prop.keyTime(idx);
```

---

## Setting Static (Non-Keyframed) Values

Use `setValue()` to assign a value without creating keyframes.

```jsx
layer.property("ADBE Transform Group").property("ADBE Opacity").setValue(50);
layer.property("ADBE Transform Group").property("ADBE Position").setValue([960, 540, 0]);
layer.property("ADBE Transform Group").property("ADBE Scale").setValue([100, 100, 100]);
layer.property("ADBE Transform Group").property("ADBE Rotate Z").setValue(45);
```

Convenience shortcuts when the property object is already resolved:

```jsx
var xf = layer.property("ADBE Transform Group");
xf.property("ADBE Opacity").setValue(50);
xf.property("ADBE Position").setValue([960, 540]);
xf.property("ADBE Scale").setValue([100, 100]);
```

---

## Setting Values at Times (Creates Keyframes)

```jsx
var prop = layer.property("ADBE Transform Group").property("ADBE Position");

// Each call creates (or updates) a keyframe at that time
prop.setValueAtTime(0, [960, 540]);
prop.setValueAtTime(2.5, [100, 100]);
```

---

## Batch Setting Keyframes

Set multiple keyframes in a single call. The two arrays must be the same length.

```jsx
var times  = [0, 1, 2, 3];
var values = [[0, 0], [100, 0], [100, 100], [0, 100]];
prop.setValuesAtTimes(times, values);
```

---

## Adding and Removing Keyframes

### Adding a Keyframe

```jsx
// addKey returns the 1-based index of the new keyframe
var keyIndex = prop.addKey(1.5);

// Then set its value
prop.setValueAtKey(keyIndex, [100, 200]);
```

### Removing Keyframes

```jsx
// MUST remove from highest index to lowest to avoid index shifting
for (var k = prop.numKeys; k >= 1; k--) {
    prop.removeKey(k);
}
```

### Removing a Single Keyframe by Time

```jsx
var idx = prop.nearestKeyIndex(1.5);
// Verify it is actually at the expected time before removing
if (Math.abs(prop.keyTime(idx) - 1.5) < 0.001) {
    prop.removeKey(idx);
}
```

---

## Interpolation Types

Three built-in types:

| Constant | Behaviour |
|---|---|
| `KeyframeInterpolationType.LINEAR` | Straight-line interpolation |
| `KeyframeInterpolationType.BEZIER` | Smooth curve (default for most props) |
| `KeyframeInterpolationType.HOLD`   | Value jumps instantly at next keyframe |

### Setting Interpolation

```jsx
prop.setInterpolationTypeAtKey(keyIndex,
    KeyframeInterpolationType.BEZIER,  // in-type
    KeyframeInterpolationType.BEZIER   // out-type
);
```

### Reading Interpolation

```jsx
var inType  = prop.keyInInterpolationType(keyIndex);
var outType = prop.keyOutInterpolationType(keyIndex);
```

---

## Temporal Ease

Temporal ease controls the speed curve between keyframes.

### KeyframeEase Constructor

```jsx
// new KeyframeEase(speed, influence)
//   speed     : velocity at the keyframe (0 = at rest)
//   influence : 0-100, how much the curve is affected (higher = more extreme)
var ease = new KeyframeEase(0, 33.33);
```

### Applying Temporal Ease

The number of `KeyframeEase` objects in each array MUST match the property dimensions:
- 1D property (Rotation, Opacity): arrays of 1
- 2D property (Position 2D, Scale 2D): arrays of 2
- 3D property (Position 3D, Scale 3D): arrays of 3

```jsx
// Example: 2D position — two KeyframeEase objects per array
var easeIn  = new KeyframeEase(0, 33.33);
var easeOut = new KeyframeEase(0, 33.33);

prop.setTemporalEaseAtKey(keyIndex,
    [easeIn, easeIn],    // inEase  (one per dimension)
    [easeOut, easeOut]    // outEase (one per dimension)
);
```

```jsx
// Example: 1D property (Opacity) — one KeyframeEase per array
var opacityProp = layer.property("ADBE Transform Group").property("ADBE Opacity");
var easeIn1D  = new KeyframeEase(0, 33.33);
var easeOut1D = new KeyframeEase(0, 33.33);
opacityProp.setTemporalEaseAtKey(keyIndex, [easeIn1D], [easeOut1D]);
```

```jsx
// Example: 3D position — three KeyframeEase objects per array
var ease3D = new KeyframeEase(0, 33.33);
prop.setTemporalEaseAtKey(keyIndex,
    [ease3D, ease3D, ease3D],
    [ease3D, ease3D, ease3D]
);
```

### Reading Temporal Ease

```jsx
var easeInArr  = prop.keyInTemporalEase(keyIndex);   // array of KeyframeEase
var easeOutArr = prop.keyOutTemporalEase(keyIndex);   // array of KeyframeEase

for (var i = 0; i < easeInArr.length; i++) {
    var speed     = easeInArr[i].speed;
    var influence = easeInArr[i].influence;
}
```

---

## Common Easing Presets

### Easy Ease (Smooth In and Out)

```jsx
var easeIn  = new KeyframeEase(0, 33.33);
var easeOut = new KeyframeEase(0, 33.33);
// Apply to a 2D property:
prop.setTemporalEaseAtKey(keyIndex, [easeIn, easeIn], [easeOut, easeOut]);
```

### Ease In Only (Slow Arrival / Decelerate)

```jsx
var easeIn  = new KeyframeEase(0, 75);
var easeOut = new KeyframeEase(0, 33.33);
prop.setTemporalEaseAtKey(keyIndex, [easeIn, easeIn], [easeOut, easeOut]);
```

### Ease Out Only (Slow Departure / Accelerate)

```jsx
var easeIn  = new KeyframeEase(0, 33.33);
var easeOut = new KeyframeEase(0, 75);
prop.setTemporalEaseAtKey(keyIndex, [easeIn, easeIn], [easeOut, easeOut]);
```

### Strong / Aggressive Ease

```jsx
var easeIn  = new KeyframeEase(0, 85);
var easeOut = new KeyframeEase(0, 85);
prop.setTemporalEaseAtKey(keyIndex, [easeIn, easeIn], [easeOut, easeOut]);
```

### Helper Function: Apply Easy Ease to All Keyframes

```jsx
function easyEaseAll(prop) {
    for (var k = 1; k <= prop.numKeys; k++) {
        var dims = prop.value instanceof Array ? prop.value.length : 1;
        var eIn  = [];
        var eOut = [];
        for (var d = 0; d < dims; d++) {
            eIn.push(new KeyframeEase(0, 33.33));
            eOut.push(new KeyframeEase(0, 33.33));
        }
        prop.setInterpolationTypeAtKey(k,
            KeyframeInterpolationType.BEZIER,
            KeyframeInterpolationType.BEZIER
        );
        prop.setTemporalEaseAtKey(k, eIn, eOut);
    }
}
```

---

## Spatial Tangents (Position-Like Properties Only)

Spatial tangents control the motion path shape in the Comp viewer. They apply only to spatial properties such as Position.

### Setting Spatial Tangents

```jsx
// inTangent and outTangent are offset vectors relative to the keyframe value
prop.setSpatialTangentsAtKey(keyIndex,
    [0, 0, 0],      // inTangent  — direction arriving at keyframe
    [100, 0, 0]     // outTangent — direction leaving keyframe
);
```

### Linear Spatial Motion (Straight Path)

```jsx
// Zero tangents = straight lines between keyframes
prop.setSpatialTangentsAtKey(keyIndex, [0, 0, 0], [0, 0, 0]);
```

### Auto Bezier and Continuous Spatial

```jsx
// Auto Bezier: AE calculates smooth tangents automatically
prop.setSpatialAutoBezierAtKey(keyIndex, true);

// Continuous: in and out tangents are locked together (smooth through point)
prop.setSpatialContinuousAtKey(keyIndex, true);
```

---

## Roving Keyframes

Roving keyframes let AE automatically adjust timing so that the speed along the motion path is smooth.

```jsx
prop.setRovingAtKey(keyIndex, true);
```

### Reading Roving State

```jsx
var isRoving = prop.keyRoving(keyIndex);
```

---

## Separated Dimensions

When Position dimensions are separated, you cannot access the unified Position property. Instead, access each axis independently.

### Check and Access

```jsx
var posProp = layer.property("ADBE Transform Group").property("ADBE Position");

if (posProp.dimensionsSeparated) {
    var xPos = layer.property("ADBE Transform Group").property("ADBE Position_0");
    var yPos = layer.property("ADBE Transform Group").property("ADBE Position_1");
    // For 3D layers:
    // var zPos = layer.property("ADBE Transform Group").property("ADBE Position_2");

    xPos.setValueAtTime(0, 0);
    xPos.setValueAtTime(1, 960);
    yPos.setValueAtTime(0, 0);
    yPos.setValueAtTime(1, 540);
} else {
    posProp.setValueAtTime(0, [0, 0]);
    posProp.setValueAtTime(1, [960, 540]);
}
```

### Enabling/Disabling Separation

```jsx
posProp.dimensionsSeparated = true;   // separate
posProp.dimensionsSeparated = false;  // reunify
```

---

## Complete Example: Animate a Layer Sliding In with Ease

```jsx
app.beginUndoGroup("AE Assistant: Slide in from left");
try {
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) throw new Error("No active comp");

    var layer = comp.selectedLayers[0];
    if (!layer) throw new Error("No layer selected");

    var pos = layer.property("ADBE Transform Group").property("ADBE Position");
    var opa = layer.property("ADBE Transform Group").property("ADBE Opacity");

    // Position: offscreen left -> center
    var startTime = comp.time;
    var endTime   = startTime + 1.0;
    pos.setValueAtTime(startTime, [-200, comp.height / 2]);
    pos.setValueAtTime(endTime, [comp.width / 2, comp.height / 2]);

    // Opacity: 0 -> 100
    opa.setValueAtTime(startTime, 0);
    opa.setValueAtTime(endTime, 100);

    // Apply ease out on first keyframe, ease in on second
    // Position (2D = 2 ease objects)
    var posKey1 = pos.nearestKeyIndex(startTime);
    var posKey2 = pos.nearestKeyIndex(endTime);
    pos.setTemporalEaseAtKey(posKey1,
        [new KeyframeEase(0, 33.33), new KeyframeEase(0, 33.33)],
        [new KeyframeEase(0, 75), new KeyframeEase(0, 75)]
    );
    pos.setTemporalEaseAtKey(posKey2,
        [new KeyframeEase(0, 75), new KeyframeEase(0, 75)],
        [new KeyframeEase(0, 33.33), new KeyframeEase(0, 33.33)]
    );

    // Opacity (1D = 1 ease object)
    var opaKey1 = opa.nearestKeyIndex(startTime);
    var opaKey2 = opa.nearestKeyIndex(endTime);
    opa.setTemporalEaseAtKey(opaKey1,
        [new KeyframeEase(0, 33.33)],
        [new KeyframeEase(0, 75)]
    );
    opa.setTemporalEaseAtKey(opaKey2,
        [new KeyframeEase(0, 75)],
        [new KeyframeEase(0, 33.33)]
    );

    // Make position path linear (straight line, no curve)
    pos.setSpatialTangentsAtKey(posKey1, [0, 0, 0], [0, 0, 0]);
    pos.setSpatialTangentsAtKey(posKey2, [0, 0, 0], [0, 0, 0]);

} catch (e) {
    alert("Error: " + e.toString());
} finally {
    app.endUndoGroup();
}
```

---

## Complete Example: Copy Keyframes Between Properties

```jsx
function copyKeyframes(srcProp, dstProp) {
    // Remove existing keyframes on destination (highest to lowest)
    for (var k = dstProp.numKeys; k >= 1; k--) {
        dstProp.removeKey(k);
    }

    // Copy from source
    if (srcProp.numKeys === 0) {
        // Static value — just copy the value
        dstProp.setValue(srcProp.value);
    } else {
        for (var i = 1; i <= srcProp.numKeys; i++) {
            var time  = srcProp.keyTime(i);
            var value = srcProp.keyValue(i);
            dstProp.setValueAtTime(time, value);

            var newIdx = dstProp.nearestKeyIndex(time);

            // Copy interpolation type
            dstProp.setInterpolationTypeAtKey(newIdx,
                srcProp.keyInInterpolationType(i),
                srcProp.keyOutInterpolationType(i)
            );

            // Copy temporal ease
            try {
                dstProp.setTemporalEaseAtKey(newIdx,
                    srcProp.keyInTemporalEase(i),
                    srcProp.keyOutTemporalEase(i)
                );
            } catch (e) { /* may fail for non-temporal properties */ }
        }
    }
}
```

---

## MUST

- **MUST** remove keyframes from highest index to lowest to avoid index shifting during removal.
- **MUST** match the number of `KeyframeEase` objects to the property dimensions (1 for 1D, 2 for 2D, 3 for 3D).
- **MUST** check `prop.numKeys` before accessing keyframe data via `keyTime()` or `keyValue()`.
- **MUST** use `setValueAtTime()` to add or modify keyframes on an already-keyframed property.
- **MUST** set interpolation type to `BEZIER` before applying temporal ease (ease has no effect on `LINEAR` or `HOLD` keyframes).
- **MUST** use 1-based indexing for all keyframe access (`keyTime(1)` is the first keyframe).
- **MUST** wrap keyframe operations in `app.beginUndoGroup()` / `app.endUndoGroup()`.

---

## FORBIDDEN

- **FORBIDDEN:** Using `setValue()` on a keyframed property -- this silently removes all keyframes and sets a static value. Use `setValueAtTime()` instead.
- **FORBIDDEN:** Setting roving on the first or last keyframe -- only interior keyframes can rove. AE will throw an error.
- **FORBIDDEN:** Removing keyframes in ascending index order within a loop -- indices shift downward after each removal, causing skipped or out-of-range keyframes.
- **FORBIDDEN:** Passing a single `KeyframeEase` object instead of an array to `setTemporalEaseAtKey()` -- it always requires arrays, even for 1D properties.
- **FORBIDDEN:** Using `setSpatialTangentsAtKey()` on non-spatial properties (e.g., Opacity, Rotation) -- it will throw an error.

---

## Gotchas

- `setTemporalEaseAtKey()` requires arrays of `KeyframeEase` matching the property dimensions (2 for 2D Position, 3 for 3D Position, 1 for Opacity or Rotation). Mismatched array length causes a runtime error.
- `prop.value` on a keyframed property returns the value at the **current time indicator**, not any specific keyframe. Use `prop.keyValue(k)` for a specific keyframe or `prop.valueAtTime(t, false)` for an arbitrary time.
- Keyframe indices are **1-based**. `keyTime(0)` will throw an error.
- `nearestKeyIndex(time)` returns the closest keyframe to the given time, not necessarily one at that exact time. Always verify with `keyTime()` if exact matching matters.
- `setValuesAtTimes()` does not return keyframe indices. If you need to set interpolation or ease on those keyframes, use `nearestKeyIndex()` after setting them.
- When dimensions are separated (`dimensionsSeparated === true`), the unified Position property becomes read-only. You must access `ADBE Position_0`, `ADBE Position_1`, (and `ADBE Position_2` for 3D) individually.
- `addKey()` returns the index of the new keyframe, but that index may change if you later add keyframes before it in time. Always use the index immediately or re-query with `nearestKeyIndex()`.
- Spatial tangent values are **offsets relative to the keyframe position**, not absolute coordinates. `[100, 0, 0]` means 100 pixels to the right of the keyframe value.
- `prop.isSpatial` can be checked to determine whether a property supports spatial tangents before calling `setSpatialTangentsAtKey()`.
- The `speed` parameter of `KeyframeEase` is the velocity at the keyframe. For most ease-in/ease-out presets, speed is `0` (at rest). Non-zero speed values create motion at the keyframe boundary.

---

## 📄 SOURCE FILE: `skills/after-effects/rules/expressions.md` (verbatim)

# Expressions

> **Loaded when:** the task involves expressions, expression controls, linking properties, wiggle, loopOut, loopIn, or dynamically driven values.

All code in this file is ES3-compatible ExtendScript. See `extendscript-fundamentals.md` for baseline syntax rules.

---

## Expression Language vs ExtendScript

Expressions and ExtendScript are **two separate runtimes**.

| | Expressions | ExtendScript |
|---|---|---|
| **Where they run** | Inside AE's expression engine, evaluated per-frame on a property | Inside AE's scripting engine, executed once as a script |
| **Language** | JavaScript-like (AE's own dialect, modern-ish) | ECMAScript 3 (ES3) |
| **Purpose** | Dynamically compute a property value each frame | Automate project-level tasks (create layers, set keyframes, etc.) |
| **Access to** | `thisComp`, `thisLayer`, `thisProperty`, `time`, `value` | `app`, `app.project`, `CompItem`, `Layer`, `Property` |

When you set an expression via ExtendScript, the expression text is **just a string**. ExtendScript does not parse or evaluate it. AE's expression engine evaluates it later at render time.

```jsx
// This ExtendScript line assigns a string to the expression property.
// The string "wiggle(3, 50)" is NOT executed in ExtendScript.
// AE's expression engine will evaluate it per-frame.
prop.expression = "wiggle(3, 50)";
```

---

## Setting an Expression

```jsx
var prop = layer.property("ADBE Transform Group").property("ADBE Position");

// Assign a simple expression
prop.expression = "time * 100";

// Assign a multi-line expression (use \n for newlines)
prop.expression = "var freq = 3;\nvar amp = 50;\nwiggle(freq, amp);";
```

---

## Enabling and Disabling an Expression

```jsx
// Enable the expression (AE evaluates it each frame)
prop.expressionEnabled = true;

// Disable the expression (AE ignores it, uses keyframed/static value)
prop.expressionEnabled = false;
```

Setting `prop.expression` to a non-empty string automatically enables the expression. Setting it to `""` clears and disables it.

---

## Reading an Expression

```jsx
// Returns the expression string, or "" if no expression is set
var exprText = prop.expression;

// Check whether an expression is present
if (prop.expression !== "") {
    // This property has an expression
}

// Check whether the expression is currently active
var isActive = prop.expressionEnabled;
```

---

## Checking for Expression Errors

```jsx
// Returns the error message string, or "" if no error
var err = prop.expressionError;

if (err !== "") {
    // Expression has an error — err contains the message
    $.writeln("Expression error on " + prop.name + ": " + err);
}
```

---

## Common Expression Patterns

These are **expression-language strings** that you assign to `prop.expression` from ExtendScript. They are not ExtendScript code.

### wiggle(freq, amp)

Generates random oscillation around the property's current value.

```jsx
// 3 wiggles per second, 50 pixels of amplitude
prop.expression = "wiggle(3, 50)";

// Wiggle only on X axis (for 2D/3D properties)
prop.expression = "var w = wiggle(3, 50);\n[w[0], value[1]];";
```

### loopOut(type) and loopIn(type)

Repeats keyframed animation beyond the last or before the first keyframe.

```jsx
// Cycle: repeats the keyframed pattern endlessly after the last keyframe
prop.expression = 'loopOut("cycle")';

// Ping-pong: plays forward, then backward, then forward, etc.
prop.expression = 'loopOut("pingpong")';

// Continue: extrapolates the last velocity forever
prop.expression = 'loopOut("continue")';

// Offset: repeats the pattern, but each cycle builds on the end value
prop.expression = 'loopOut("offset")';

// Loop before the first keyframe
prop.expression = 'loopIn("cycle")';

// Combine both directions
prop.expression = 'loopIn("cycle") + loopOut("cycle") - value';
```

### valueAtTime(t)

Reads the property's own value at an arbitrary time.

```jsx
// Time delay: read this property's value 0.5 seconds in the past
prop.expression = "valueAtTime(time - 0.5)";
```

### linear(t, tMin, tMax, valMin, valMax)

Linearly maps a value from one range to another.

```jsx
// Map time 0-2s to opacity 0-100
prop.expression = "linear(time, 0, 2, 0, 100)";

// Map a slider control (0-100) to scale (50-150)
prop.expression = 'var s = effect("Slider Control")("Slider");\nlinear(s, 0, 100, 50, 150);';
```

### ease(t, tMin, tMax, valMin, valMax)

Same as `linear()` but with smooth (eased) acceleration and deceleration at both ends.

```jsx
// Smooth ramp from 0 to 100 opacity over the first 2 seconds
prop.expression = "ease(time, 0, 2, 0, 100)";
```

Related functions: `easeIn()` (smooth start, linear end), `easeOut()` (linear start, smooth end).

### clamp(val, min, max)

Constrains a value to a range.

```jsx
// Keep opacity between 20 and 80 even if driven by another expression
prop.expression = "clamp(value, 20, 80)";

// Clamp wiggle so it never goes negative
prop.expression = "clamp(wiggle(2, 100), 0, 100)";
```

---

## Linking Properties Across Layers

Expression strings can reference other layers and properties using `thisComp.layer()`.

### Link to Another Layer's Transform

```jsx
// Follow another layer's position
prop.expression = 'thisComp.layer("Controller").transform.position';

// Follow another layer's rotation
prop.expression = 'thisComp.layer("Controller").transform.rotation';

// Follow another layer's opacity
prop.expression = 'thisComp.layer("Controller").transform.opacity';
```

### Link to an Effect Parameter

```jsx
// Read a slider value from another layer's effect
prop.expression = 'thisComp.layer("Controller").effect("Slider Control")("Slider")';

// Read from an effect on the same layer
prop.expression = 'effect("Slider Control")("Slider")';
```

### Link with an Offset

```jsx
// Follow another layer's position but offset by [100, 0]
prop.expression = 'thisComp.layer("Controller").transform.position + [100, 0]';

// Follow with a time delay
prop.expression = 'thisComp.layer("Controller").transform.position.valueAtTime(time - 0.1)';
```

---

## Expression Controls

Expression controls are effects that expose simple UI controls (sliders, checkboxes, colors, etc.) which expressions can reference. They hold no visual effect on their own; they exist purely as data sources for expressions.

### Adding Expression Controls via ExtendScript

```jsx
var effects = layer.property("ADBE Effect Parade");

// Slider Control — single float value
var slider = effects.addProperty("ADBE Slider Control");
slider.name = "Speed";
slider.property("ADBE Slider Control-0001").setValue(50);

// Checkbox Control — 0 or 1
var checkbox = effects.addProperty("ADBE Checkbox Control");
checkbox.name = "Enabled";
checkbox.property("ADBE Checkbox Control-0001").setValue(1);

// Color Control — [r, g, b, a] in 0-1 range
var colorCtrl = effects.addProperty("ADBE Color Control");
colorCtrl.name = "Tint Color";
colorCtrl.property("ADBE Color Control-0001").setValue([1, 0, 0, 1]);

// Point Control — [x, y] in pixels
var pointCtrl = effects.addProperty("ADBE Point Control");
pointCtrl.name = "Target Point";
pointCtrl.property("ADBE Point Control-0001").setValue([960, 540]);

// Layer Control — index of the target layer (integer)
var layerCtrl = effects.addProperty("ADBE Layer Control");
layerCtrl.name = "Reference Layer";
layerCtrl.property("ADBE Layer Control-0001").setValue(2); // layer index

// Dropdown Menu Control
var dropdown = effects.addProperty("ADBE Dropdown Control");
dropdown.name = "Mode";
// Dropdown items must be set via the property's setPropertyParameters method (AE 2020+)
// The value is the 1-based index of the selected item
dropdown.property("ADBE Dropdown Control-0001").setValue(1);
```

### Referencing Expression Controls in Expressions

```jsx
// Reference a slider on the same layer
prop.expression = 'effect("Speed")("Slider")';

// Reference a checkbox on the same layer
prop.expression = 'effect("Enabled")("Checkbox")';

// Reference a color control on the same layer
prop.expression = 'effect("Tint Color")("Color")';

// Reference a point control on the same layer
prop.expression = 'effect("Target Point")("Point")';

// Reference a layer control on the same layer
prop.expression = 'effect("Reference Layer")("Layer")';

// Reference a dropdown on the same layer
prop.expression = 'effect("Mode")("Menu")';

// Reference a control on a different layer
prop.expression = 'thisComp.layer("Controller").effect("Speed")("Slider")';
```

### Expression Control matchNames Reference

| Control Type | Effect matchName | Parameter matchName | Expression Reference |
|---|---|---|---|
| Slider Control | `ADBE Slider Control` | `ADBE Slider Control-0001` | `("Slider")` |
| Checkbox Control | `ADBE Checkbox Control` | `ADBE Checkbox Control-0001` | `("Checkbox")` |
| Color Control | `ADBE Color Control` | `ADBE Color Control-0001` | `("Color")` |
| Point Control | `ADBE Point Control` | `ADBE Point Control-0001` | `("Point")` |
| Layer Control | `ADBE Layer Control` | `ADBE Layer Control-0001` | `("Layer")` |
| Dropdown Menu Control | `ADBE Dropdown Control` | `ADBE Dropdown Control-0001` | `("Menu")` |

---

## Escaping Quotes in Expression Strings

When setting an expression from ExtendScript, the expression is a string literal. Quotes inside the expression must be escaped or alternated.

### Strategy 1: Alternate Quote Types

```jsx
// Expression uses double quotes, ExtendScript string uses single quotes
prop.expression = 'thisComp.layer("Controller").transform.position';

// Expression uses single quotes, ExtendScript string uses double quotes
prop.expression = "loopOut('cycle')";
```

### Strategy 2: Escape with Backslashes

```jsx
// Escape double quotes inside a double-quoted ExtendScript string
prop.expression = "thisComp.layer(\"Controller\").transform.position";

// Escape single quotes inside a single-quoted ExtendScript string
prop.expression = 'loopOut(\'cycle\')';
```

### Strategy 3: Build Strings with Concatenation

Use concatenation for complex expressions that mix variable data and quoted references.

```jsx
// Insert a layer name dynamically
var targetName = "Logo";
prop.expression = 'thisComp.layer("' + targetName + '").transform.position';

// Build a multi-line expression with a variable
var freq = 3;
var amp = 50;
prop.expression = "wiggle(" + freq + ", " + amp + ")";
```

---

## MUST

- **MUST** treat expression text as a plain string when working in ExtendScript. Do not attempt to call expression functions (`wiggle`, `loopOut`, etc.) directly in ExtendScript -- they do not exist there.
- **MUST** check `prop.expressionError` after setting an expression if you need to verify it compiled successfully. Expression errors are silent in ExtendScript.
- **MUST** use `prop.expressionEnabled = true` if you need to guarantee the expression is active. Setting `prop.expression` to a non-empty string enables it automatically, but re-enabling after a disable requires the explicit flag.
- **MUST** escape or alternate quotes when embedding quoted strings (layer names, effect names, loop types) inside an expression assigned from ExtendScript.
- **MUST** wrap expression-setting operations in `app.beginUndoGroup()` / `app.endUndoGroup()` so the user can undo them.
- **MUST** verify the property supports expressions before setting one. Not all properties are expressionable. Check with `prop.canSetExpression` (returns `true` if the property supports expressions).

---

## FORBIDDEN

- **FORBIDDEN:** Calling expression-engine functions (`wiggle()`, `loopOut()`, `thisComp`, `time`, `value`, etc.) directly in ExtendScript. These exist only inside AE's expression engine. In ExtendScript, they are undefined and will throw a `ReferenceError`.

```jsx
// WRONG — these are expression-engine globals, not ExtendScript globals
var w = wiggle(3, 50);       // ReferenceError
var t = time;                // ReferenceError
var v = thisComp.layer(1);   // ReferenceError

// CORRECT — pass them as a string to prop.expression
prop.expression = "wiggle(3, 50)";
```

- **FORBIDDEN:** Using `prop.setValue()` to try to set an expression. `setValue()` sets the property's static/keyframed value, not its expression. Use `prop.expression = "..."` to set an expression.

- **FORBIDDEN:** Assuming `prop.value` returns the pre-expression value. It returns the **post-expression** value (the final computed result). Use `prop.valueAtTime(t, true)` to get the pre-expression value.

- **FORBIDDEN:** Using template literals or ES6+ string syntax when building expression strings in ExtendScript. ExtendScript is ES3 -- use string concatenation with `+`.

```jsx
// WRONG — template literals do not exist in ES3
prop.expression = `wiggle(${freq}, ${amp})`;

// CORRECT
prop.expression = "wiggle(" + freq + ", " + amp + ")";
```

---

## Gotchas

- **Escape quotes properly when setting expressions from ExtendScript.** Expression strings often contain quoted layer names, effect names, or loop type arguments. Mismatched or unescaped quotes will produce a malformed string, and AE will report an expression error at render time. Always alternate quote types or escape inner quotes.

```jsx
// WRONG — unescaped double quotes inside double-quoted string
prop.expression = "thisComp.layer("Name").transform.position"; // syntax error

// CORRECT
prop.expression = 'thisComp.layer("Name").transform.position';
```

- **`prop.value` returns the post-expression value; `prop.valueAtTime(t, true)` returns pre-expression.** If an expression is active, `prop.value` gives you the result after the expression runs. To read the underlying keyframed or static value (before the expression modifies it), pass `true` as the second argument to `valueAtTime()`.

```jsx
// Post-expression value (what you see in the comp viewer)
var rendered = prop.value;

// Pre-expression value at time t (the raw keyframed/static value)
var raw = prop.valueAtTime(comp.time, true);
```

- **Expression errors do not throw in ExtendScript.** Setting a syntactically invalid expression via `prop.expression = "..."` does not throw an error in your ExtendScript code. The expression is stored as-is, and AE only reports the error when it tries to evaluate the expression at render time. You must explicitly check `prop.expressionError` to detect problems.

```jsx
prop.expression = "this is not valid javascript";
// No error thrown here — ExtendScript continues normally

// You must check manually:
if (prop.expressionError !== "") {
    // "this is not valid javascript" produced an error
    $.writeln("Expression error: " + prop.expressionError);
}
```

- **`prop.expressionError` may not update immediately.** AE evaluates expressions lazily. After setting an expression, you may need to force an evaluation (e.g., by reading `prop.value` or calling `prop.valueAtTime()`) before `prop.expressionError` reflects the current state.

- **Multi-line expressions require `\n` or string concatenation.** ExtendScript string literals cannot span multiple lines. Use `\n` for newlines inside the expression string, or concatenate multiple lines.

```jsx
// Using \n
prop.expression = "var s = effect(\"Speed\")(\"Slider\");\nwiggle(s, 50)";

// Using concatenation
prop.expression = 'var s = effect("Speed")("Slider");\n'
    + 'wiggle(s, 50)';
```

- **Expression controls must exist before an expression can reference them.** If you set an expression that references `effect("Speed")("Slider")` but the Slider Control effect named "Speed" has not been added to the layer yet, the expression will error. Always add the expression control first, then set the expression.

- **Layer Control returns a layer object in expressions, not an index.** In the expression engine, `effect("Reference Layer")("Layer")` returns a layer object you can chain methods on (e.g., `.transform.position`). But when setting the Layer Control's value via ExtendScript, you set it to the layer's **index** (an integer).

```jsx
// ExtendScript: set the layer control to point at layer index 3
layerCtrl.property("ADBE Layer Control-0001").setValue(3);

// Expression: use the layer control to get a position
prop.expression = 'effect("Reference Layer")("Layer").transform.position';
```

- **Dropdown Menu Control value is 1-based.** The first item in a dropdown is index 1, not 0. Setting it to 0 will produce an error.

---

## Complete Example: Add a Wiggle Expression to Position via ExtendScript

```jsx
app.beginUndoGroup("AE Assistant: Add wiggle expression to position");
try {
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        writeResult({ error: "No active composition" });
        return;
    }

    var layer = comp.selectedLayers[0];
    if (!layer) {
        writeResult({ error: "No layer selected" });
        return;
    }

    // Unlock if needed
    var wasLocked = layer.locked;
    if (wasLocked) {
        layer.locked = false;
    }

    // Add a Slider Control for frequency
    var effects = layer.property("ADBE Effect Parade");
    var freqSlider = effects.addProperty("ADBE Slider Control");
    freqSlider.name = "Wiggle Frequency";
    freqSlider.property("ADBE Slider Control-0001").setValue(3);

    // Add a Slider Control for amplitude
    var ampSlider = effects.addProperty("ADBE Slider Control");
    ampSlider.name = "Wiggle Amplitude";
    ampSlider.property("ADBE Slider Control-0001").setValue(50);

    // Get the position property
    var pos = layer.property("ADBE Transform Group").property("ADBE Position");

    // Verify the property supports expressions
    if (!pos.canSetExpression) {
        writeResult({ error: "Position property does not support expressions" });
        return;
    }

    // Build the expression string
    // The expression reads from the two slider controls on the same layer
    var expr = 'var freq = effect("Wiggle Frequency")("Slider");\n'
        + 'var amp = effect("Wiggle Amplitude")("Slider");\n'
        + 'wiggle(freq, amp);';

    // Set the expression (this also enables it automatically)
    pos.expression = expr;

    // Verify no expression error
    // Force evaluation by reading the value
    var testVal = pos.valueAtTime(0, false);
    var exprErr = pos.expressionError;

    if (exprErr !== "") {
        writeResult({
            error: "Expression error: " + exprErr,
            expression: expr
        });
        return;
    }

    // Re-lock if it was locked before
    if (wasLocked) {
        layer.locked = true;
    }

    writeResult({
        success: true,
        message: "Added wiggle expression to " + layer.name + " position",
        expression: expr,
        controls: ["Wiggle Frequency", "Wiggle Amplitude"]
    });
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## 📄 SOURCE FILE: `skills/after-effects/rules/effects.md` (verbatim)

# Effects

> **Loaded when:** the task involves adding, removing, configuring, or querying effects on layers in After Effects via ExtendScript.

All code in this file is ES3-compatible ExtendScript. See `extendscript-fundamentals.md` for baseline syntax rules.

---

## Effect Parade (The Effects Container)

Every layer has a property group called "ADBE Effect Parade" that holds all of its effects. This is the entry point for all effect operations.

```jsx
var effects = layer.property("ADBE Effect Parade");
var effectCount = effects.numProperties; // number of effects on the layer
```

---

## Adding Effects

MUST use `addProperty()` with the effect's **matchName** to add an effect.

```jsx
var effects = layer.property("ADBE Effect Parade");
var blur = effects.addProperty("ADBE Gaussian Blur 2");
```

The returned object is a `PropertyGroup` representing the newly added effect. You can immediately configure its parameters.

```jsx
var fill = effects.addProperty("ADBE Fill");
fill.property("ADBE Fill-0002").setValue([1, 0, 0]); // Color -> red
fill.property("ADBE Fill-0007").setValue(1);          // Opacity -> 100%
```

---

## Removing Effects

```jsx
var effect = layer.property("ADBE Effect Parade").property(1);
effect.remove();
```

When removing multiple effects in a loop, MUST iterate in **reverse order** to avoid index shifting:

```jsx
var effects = layer.property("ADBE Effect Parade");
for (var i = effects.numProperties; i >= 1; i--) {
    effects.property(i).remove();
}
```

---

## Accessing Effect Parameters

Effect parameters can be accessed by **1-based index** or by **matchName**.

### By Index

```jsx
var effect = layer.property("ADBE Effect Parade").property(1);

// Access the first parameter of the effect (1-based)
var firstParam = effect.property(1);
```

### By matchName

```jsx
var blur = layer.property("ADBE Effect Parade").property("ADBE Gaussian Blur 2");

// Blurriness parameter
var blurriness = blur.property("ADBE Gaussian Blur 2-0001");
```

### Iterating All Parameters

```jsx
var effect = layer.property("ADBE Effect Parade").property(1);
for (var p = 1; p <= effect.numProperties; p++) {
    var param = effect.property(p);
    var paramName = param.name;
    var paramMatchName = param.matchName;
    // param.value may throw on non-valued properties; wrap in try/catch
    try {
        var val = param.value;
    } catch (e) {
        // parameter does not expose a value (e.g., group headers)
    }
}
```

---

## Setting Effect Parameter Values

Use `setValue()` on the specific parameter property.

```jsx
var blur = layer.property("ADBE Effect Parade").property("ADBE Gaussian Blur 2");

// Set Blurriness to 10
blur.property("ADBE Gaussian Blur 2-0001").setValue(10);

// Set Blur Dimensions to "Horizontal and Vertical" (value 1)
blur.property("ADBE Gaussian Blur 2-0002").setValue(1);

// Set Repeat Edge Pixels checkbox on (value 1)
blur.property("ADBE Gaussian Blur 2-0003").setValue(1);
```

---

## Keyframing Effect Parameters

Effect parameters support the same keyframe API as any other AE property.

```jsx
var blurriness = blur.property("ADBE Gaussian Blur 2-0001");

// Set keyframes
blurriness.setValueAtTime(0, 0);
blurriness.setValueAtTime(1, 25);
blurriness.setValueAtTime(2, 0);

// Apply ease to keyframes
for (var k = 1; k <= blurriness.numKeys; k++) {
    blurriness.setInterpolationTypeAtKey(k,
        KeyframeInterpolationType.BEZIER,
        KeyframeInterpolationType.BEZIER
    );
    blurriness.setTemporalEaseAtKey(k,
        [new KeyframeEase(0, 33.33)],
        [new KeyframeEase(0, 33.33)]
    );
}
```

---

## Reading Effect Parameters and Keyframes

```jsx
var effect = layer.property("ADBE Effect Parade").property(1);

for (var p = 1; p <= effect.numProperties; p++) {
    var param = effect.property(p);

    try {
        if (param.numKeys > 0) {
            // Parameter is keyframed
            for (var k = 1; k <= param.numKeys; k++) {
                var time = param.keyTime(k);
                var value = param.keyValue(k);
            }
        } else {
            // Static value
            var value = param.value;
        }
    } catch (e) {
        // Some parameters (group headers, unsupported types) throw on .value
    }
}
```

---

## Enabling and Disabling Effects

```jsx
var effect = layer.property("ADBE Effect Parade").property(1);

// Disable effect (equivalent to clicking the "fx" toggle in the UI)
effect.enabled = false;

// Enable effect
effect.enabled = true;

// Check current state
var isEnabled = effect.enabled;
```

---

## Finding Effects by Name or matchName

There is no built-in search method. MUST iterate and compare.

### Find by Display Name

```jsx
function findEffectByName(layer, effectName) {
    var effects = layer.property("ADBE Effect Parade");
    for (var i = 1; i <= effects.numProperties; i++) {
        if (effects.property(i).name === effectName) {
            return effects.property(i);
        }
    }
    return null;
}

var blur = findEffectByName(layer, "Gaussian Blur");
```

### Find by matchName

```jsx
function findEffectByMatchName(layer, matchName) {
    var effects = layer.property("ADBE Effect Parade");
    for (var i = 1; i <= effects.numProperties; i++) {
        if (effects.property(i).matchName === matchName) {
            return effects.property(i);
        }
    }
    return null;
}

var blur = findEffectByMatchName(layer, "ADBE Gaussian Blur 2");
```

### Find All Effects of a Given Type

```jsx
function findAllEffectsByMatchName(layer, matchName) {
    var results = [];
    var effects = layer.property("ADBE Effect Parade");
    for (var i = 1; i <= effects.numProperties; i++) {
        if (effects.property(i).matchName === matchName) {
            results.push(effects.property(i));
        }
    }
    return results;
}
```

---

## Common Effect matchNames

| Effect | matchName |
|---|---|
| Gaussian Blur | `ADBE Gaussian Blur 2` |
| Fill | `ADBE Fill` |
| Tint | `ADBE Tint` |
| Levels | `ADBE Levels2` |
| Curves | `ADBE CurvesCustom` |
| Hue/Saturation | `ADBE HUE SATURATION` |
| Drop Shadow | `ADBE Drop Shadow` |
| Glow | `ADBE Glo2` |
| CC Toner | `CS Toner` |
| Tritone | `ADBE Tritone` |
| Opacity | `ADBE Opacity` |

### Discovering matchNames at Runtime

When you do not know the matchName for an effect, add it manually in AE and then read it back:

```jsx
var effects = layer.property("ADBE Effect Parade");
for (var i = 1; i <= effects.numProperties; i++) {
    var fx = effects.property(i);
    $.writeln("Effect: " + fx.name + " | matchName: " + fx.matchName);

    // Also dump parameter matchNames
    for (var p = 1; p <= fx.numProperties; p++) {
        $.writeln("  Param " + p + ": " + fx.property(p).name + " | " + fx.property(p).matchName);
    }
}
```

---

## MUST

- **MUST** use `matchName` (not display name) when calling `addProperty()`. Display names are localized and will fail in non-English AE installations.

```jsx
// WRONG - display name, will fail in non-English AE
effects.addProperty("Gaussian Blur");

// CORRECT - matchName, works in all locales
effects.addProperty("ADBE Gaussian Blur 2");
```

- **MUST** access the effect parade via `layer.property("ADBE Effect Parade")` before adding or querying effects.

- **MUST** use 1-based indexing for effects and their parameters. The first effect is `property(1)`, the first parameter within an effect is `property(1)`.

- **MUST** remove effects in reverse index order when removing multiple effects in a loop:

```jsx
for (var i = effects.numProperties; i >= 1; i--) {
    effects.property(i).remove();
}
```

- **MUST** wrap all effect mutation operations in an undo group:

```jsx
app.beginUndoGroup("AE Assistant: apply effects");
try {
    // ... effect operations ...
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

- **MUST** check that the layer exists and the comp is valid before manipulating effects:

```jsx
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    writeResult({ error: "No active composition" });
    return;
}
```

---

## FORBIDDEN

- **FORBIDDEN:** Passing a display name to `addProperty()`. It requires the internal matchName string. Display names are localized and unreliable.

```jsx
// FORBIDDEN
effects.addProperty("Gaussian Blur");
effects.addProperty("Fill");

// CORRECT
effects.addProperty("ADBE Gaussian Blur 2");
effects.addProperty("ADBE Fill");
```

- **FORBIDDEN:** Using `setValue()` on a keyframed effect parameter. This silently removes all keyframes and sets a static value. Use `setValueAtTime()` instead.

```jsx
// FORBIDDEN when blurriness already has keyframes
blurriness.setValue(10);

// CORRECT
blurriness.setValueAtTime(comp.time, 10);
```

- **FORBIDDEN:** Removing effects in forward index order within a loop. Indices shift downward after each removal, causing skipped effects or out-of-range errors.

- **FORBIDDEN:** Assuming an effect exists on a layer without checking first. Always verify before accessing:

```jsx
// FORBIDDEN
var blur = layer.property("ADBE Effect Parade").property("ADBE Gaussian Blur 2");
blur.property(1).setValue(10); // throws if blur is null

// CORRECT
var blur = layer.property("ADBE Effect Parade").property("ADBE Gaussian Blur 2");
if (blur) {
    blur.property("ADBE Gaussian Blur 2-0001").setValue(10);
}
```

- **FORBIDDEN:** Using ES5+ syntax (`let`, `const`, arrow functions, template literals, `forEach`, `map`, `filter`). All code must be ES3.

---

## Gotchas

- **`addProperty()` requires matchName, not display name.** The string you pass to `addProperty()` is the internal matchName (e.g., `"ADBE Gaussian Blur 2"`), not the name shown in the Effects menu (e.g., `"Gaussian Blur"`). Using the display name will throw an error or silently fail.

- **Effect parameter matchNames are effect-specific and not standardized across effects.** Each effect defines its own parameter matchNames. For Gaussian Blur, the blurriness parameter is `"ADBE Gaussian Blur 2-0001"`. For Fill, the color parameter is `"ADBE Fill-0002"`. There is no universal naming convention. Always discover parameter matchNames by inspecting the effect at runtime or consulting documentation.

- **Some effects have different matchNames across AE versions.** Adobe occasionally updates effect internals between major AE releases. An effect that works as `"ADBE Gaussian Blur"` in older versions uses `"ADBE Gaussian Blur 2"` in modern versions. Always test scripts against the target AE version. When writing portable scripts, wrap `addProperty()` in a try/catch and attempt fallback matchNames:

```jsx
var blur;
try {
    blur = effects.addProperty("ADBE Gaussian Blur 2");
} catch (e) {
    try {
        blur = effects.addProperty("ADBE Gaussian Blur");
    } catch (e2) {
        writeResult({ error: "Could not add Gaussian Blur effect" });
        return;
    }
}
```

- **`property()` by matchName returns `null` (not an error) when the effect is not present on the layer.** Always null-check the result before accessing sub-properties.

```jsx
var blur = effects.property("ADBE Gaussian Blur 2");
// blur is null if no Gaussian Blur is on the layer, NOT an error
if (blur === null) {
    // effect not found
}
```

- **Effect parameter `.value` can throw on some parameter types.** Group headers, dropdown menus with no value, and certain custom parameters do not support `.value`. Wrap in try/catch when iterating unknown parameters.

- **Duplicate effect names.** If a layer has multiple instances of the same effect (e.g., two Gaussian Blurs), `property("ADBE Gaussian Blur 2")` returns only the **first** match. Use index-based access or iterate to find all instances.

- **The `.name` property of an effect is the user-facing display name and can be renamed by the user.** After renaming, the original display name no longer matches. Use `.matchName` for reliable type identification:

```jsx
// User renamed "Gaussian Blur" to "My Blur"
effect.name;       // "My Blur"
effect.matchName;  // "ADBE Gaussian Blur 2" (always stable)
```

- **`effect.enabled` controls the effect toggle, not the layer visibility.** Setting `effect.enabled = false` is equivalent to clicking the effect's "fx" checkbox in the Timeline panel. The layer itself remains visible.

- **Effect order matters.** Effects are processed top-to-bottom (index 1 first). The order in which effects are added determines the visual result. There is no `moveProperty()` method to reorder effects after creation; you must remove and re-add them in the desired order.

---

## Complete Example: Add Gaussian Blur, Set Blurriness, Keyframe It

```jsx
app.beginUndoGroup("AE Assistant: Add and keyframe Gaussian Blur");
try {
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        writeResult({ error: "No active composition" });
        return;
    }

    // Get the first selected layer, or fall back to the top layer
    var layer = null;
    if (comp.selectedLayers.length > 0) {
        layer = comp.selectedLayers[0];
    } else if (comp.numLayers > 0) {
        layer = comp.layer(1);
    }
    if (!layer) {
        writeResult({ error: "No layers in composition" });
        return;
    }

    // Unlock the layer if locked
    var wasLocked = layer.locked;
    if (wasLocked) {
        layer.locked = false;
    }

    // Add Gaussian Blur effect
    var effects = layer.property("ADBE Effect Parade");
    var blur = effects.addProperty("ADBE Gaussian Blur 2");

    // Get the Blurriness parameter
    var blurriness = blur.property("ADBE Gaussian Blur 2-0001");

    // Keyframe Blurriness: 0 -> 25 -> 0 over 2 seconds
    var startTime = comp.time;
    blurriness.setValueAtTime(startTime, 0);
    blurriness.setValueAtTime(startTime + 1, 25);
    blurriness.setValueAtTime(startTime + 2, 0);

    // Apply easy ease to all keyframes
    for (var k = 1; k <= blurriness.numKeys; k++) {
        blurriness.setInterpolationTypeAtKey(k,
            KeyframeInterpolationType.BEZIER,
            KeyframeInterpolationType.BEZIER
        );
        blurriness.setTemporalEaseAtKey(k,
            [new KeyframeEase(0, 33.33)],
            [new KeyframeEase(0, 33.33)]
        );
    }

    // Re-lock layer if it was locked before
    if (wasLocked) {
        layer.locked = true;
    }

    writeResult({
        success: true,
        message: "Added Gaussian Blur to '" + layer.name + "' with keyframed blurriness (0 -> 25 -> 0 over 2s)",
        effectName: blur.name,
        effectMatchName: blur.matchName,
        keyframeCount: blurriness.numKeys
    });
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## 📄 SOURCE FILE: `skills/after-effects/rules/composition-management.md` (verbatim)

# Composition Management

> **Loaded when:** the task involves creating, configuring, precomposing, nesting, or finding compositions in After Effects via ExtendScript.

All code in this file is ES3-compatible ExtendScript. See `extendscript-fundamentals.md` for baseline syntax rules.

---

## Creating Compositions

```jsx
// app.project.items.addComp(name, width, height, pixelAspect, duration, fps)
// Returns a CompItem
var comp = app.project.items.addComp("Main Comp", 1920, 1080, 1, 10, 29.97);
```

All arguments are required:

| Argument | Type | Description |
|---|---|---|
| `name` | String | Composition name |
| `width` | Integer | Width in pixels |
| `height` | Integer | Height in pixels |
| `pixelAspect` | Number | Pixel aspect ratio (1 for square pixels) |
| `duration` | Number | Duration in seconds |
| `fps` | Number | Frame rate (e.g., 24, 29.97, 30, 60) |

---

## Composition Settings

### Dimensions and Timing

```jsx
// Read/write dimensions
comp.width = 1920;
comp.height = 1080;

// Duration in seconds
comp.duration = 30;

// Frame rate
comp.frameRate = 24;

// Pixel aspect ratio (1 = square pixels)
comp.pixelAspect = 1;
```

### Background Color

```jsx
// bgColor is [r, g, b] with each channel in the 0-1 range
comp.bgColor = [0, 0, 0];           // black
comp.bgColor = [0.1, 0.1, 0.15];    // dark blue-grey
```

### Nested Composition Overrides

```jsx
// When true, nested comps retain their own frame rate instead of inheriting the parent's
comp.preserveNestedFrameRate = true;

// When true, nested comps retain their own resolution instead of inheriting the parent's
comp.preserveNestedResolution = true;
```

---

## Work Area

The work area defines the region used by preview and render operations.

```jsx
// Work area start time in seconds
comp.workAreaStart = 2;

// Work area duration in seconds (not end time)
comp.workAreaDuration = 5;

// The work area spans from workAreaStart to workAreaStart + workAreaDuration
// In this example: 2s to 7s
```

---

## Display Start Time

Controls the timecode offset shown in the timeline. Does not affect actual layer timing.

```jsx
// Set the display start time in seconds
comp.displayStartTime = 3600;   // display timecode starts at 1:00:00:00

// displayStartFrame is read-only — it reflects displayStartTime as a frame number
var startFrame = comp.displayStartFrame;
```

---

## Motion Blur

```jsx
// Enable motion blur for the composition (layers must also have MB enabled individually)
comp.motionBlur = true;

// Shutter angle in degrees (0-720). Default is 180.
comp.shutterAngle = 180;

// Shutter phase in degrees (-360 to 360). Default is -90.
// Controls when the shutter opens relative to each frame
comp.shutterPhase = -90;
```

---

## Finding Compositions in the Project

Iterate `app.project.items` and check each item with `instanceof CompItem`.

```jsx
// Find all compositions
var comps = [];
for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
    if (item instanceof CompItem) {
        comps.push(item);
    }
}
```

### Find a Composition by Name

```jsx
function findCompByName(name) {
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof CompItem && item.name === name) {
            return item;
        }
    }
    return null;
}

var mainComp = findCompByName("Main Comp");
```

---

## Creating Compositions in Folders

Items are placed into folders by setting their `parentFolder` property. By default new items are created at the project root.

```jsx
// Create or find a folder
var folder = app.project.items.addFolder("Precomps");

// Create a comp and move it into the folder
var comp = app.project.items.addComp("Nested Comp", 1920, 1080, 1, 10, 24);
comp.parentFolder = folder;
```

### Find an Existing Folder by Name

```jsx
function findFolderByName(name) {
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof FolderItem && item.name === name) {
            return item;
        }
    }
    return null;
}

var precompsFolder = findFolderByName("Precomps");
if (!precompsFolder) {
    precompsFolder = app.project.items.addFolder("Precomps");
}
```

---

## Nesting Compositions

Add an existing `CompItem` as a layer inside another composition using `comp.layers.add()`.

```jsx
var mainComp = app.project.activeItem;
var nestedComp = findCompByName("Lower Third");

if (mainComp && mainComp instanceof CompItem && nestedComp) {
    var precompLayer = mainComp.layers.add(nestedComp);
    // precompLayer is an AVLayer whose source is nestedComp
}
```

---

## Precomposing Layers

```jsx
// comp.layers.precompose(layerIndices, name, moveAllAttributes)
// layerIndices  : Array of 1-based layer indices (must be contiguous)
// name          : String name for the new precomp
// moveAllAttributes : Boolean
//   true  = moves all attributes (effects, masks, transforms, keyframes) into the precomp
//   false = moves only the layers; attributes stay on the collapsed layer in the parent comp

var newComp = comp.layers.precompose([1, 2, 3], "BG Elements", true);
// newComp is the newly created CompItem
```

### moveAllAttributes Explained

| `moveAllAttributes` | Behaviour |
|---|---|
| `true` | All effects, masks, transforms, track mattes, and keyframes are moved into the new precomp. The resulting layer in the parent comp is clean. |
| `false` | Only the layer sources are moved into the new precomp. Effects, masks, and transforms remain on the collapsed layer in the parent comp. Only valid when precomposing a single layer. |

---

## Collecting Layer Indices for Precompose

`comp.selectedLayers` is a 0-based JavaScript array, but `precompose()` requires 1-based layer indices. Extract `.index` from each selected layer.

```jsx
var sel = comp.selectedLayers;
var indices = [];
for (var i = 0; i < sel.length; i++) {
    indices.push(sel[i].index);
}

// Sort ascending so they are in contiguous order
indices.sort(function(a, b) { return a - b; });
```

---

## MUST

- **MUST** wrap all composition creation and modification in an undo group:

```jsx
app.beginUndoGroup("AE Assistant: create composition");
try {
    // ... comp operations ...
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

- **MUST** verify the active item is a `CompItem` before accessing `comp.layers` or calling `precompose()`:

```jsx
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    writeResult({ error: "No active composition" });
    return;
}
```

- **MUST** supply all six arguments to `addComp()`. Omitting any argument throws an error.

- **MUST** use 1-based layer indices in the array passed to `precompose()`. Layer index 1 is the topmost layer.

- **MUST** sort layer indices when collecting them from `selectedLayers` for precompose, since selection order is not guaranteed to match layer stack order.

- **MUST** enable motion blur on individual layers (`layer.motionBlur = true`) in addition to the composition-level `comp.motionBlur = true`. Neither alone is sufficient.

---

## FORBIDDEN

- **FORBIDDEN:** Passing 0-based indices to `precompose()`. The method expects 1-based layer indices matching `layer.index`. Using 0-based array positions from `selectedLayers` will precompose the wrong layers or throw an out-of-range error.

```jsx
// WRONG -- using 0-based loop counter as the index
var sel = comp.selectedLayers;
var indices = [];
for (var i = 0; i < sel.length; i++) {
    indices.push(i);  // WRONG: this is the array position, not the layer index
}

// CORRECT -- use the layer's actual .index property
var sel = comp.selectedLayers;
var indices = [];
for (var i = 0; i < sel.length; i++) {
    indices.push(sel[i].index);  // CORRECT: 1-based layer index
}
```

- **FORBIDDEN:** Using `moveAllAttributes = false` when precomposing multiple layers. AE only supports `false` for single-layer precompose. Passing `false` with multiple indices throws an error.

- **FORBIDDEN:** Setting `comp.workAreaDuration` to 0 or a negative value. This causes undefined behavior.

- **FORBIDDEN:** Using ES5+ syntax. Use `var`, not `let`/`const`. Use string concatenation with `+`, not template literals.

---

## Gotchas

- **Precompose indices must be contiguous.** The array of layer indices passed to `precompose()` must form an unbroken range in the layer stack (e.g., `[2, 3, 4]`). Non-contiguous indices (e.g., `[1, 3, 5]`) will throw an error. If you need to precompose non-adjacent layers, move them to be adjacent first using `layer.moveBefore()` or `layer.moveAfter()`.

- **Precompose with `moveAllAttributes = true` moves everything.** Effects, masks, track mattes, transforms, expressions, and keyframes are all moved into the precomp. The resulting layer in the parent composition is a bare reference to the new precomp. This is usually what you want for a clean hand-off.

- **Precompose with `moveAllAttributes = false` keeps attributes on the parent layer.** Only the source layers are moved into the precomp. Effects, masks, and transforms stay on the collapsed layer in the parent comp. This is only valid for single-layer precompose.

- **`precompose()` returns a `CompItem`, not a layer.** The return value is the newly created composition in the project panel. To get the new precomp layer in the parent comp, find it by name or index after the call -- precompose replaces the original layers with a single new layer at the topmost original index.

- **`comp.workAreaDuration` is a duration, not an end time.** The work area ends at `comp.workAreaStart + comp.workAreaDuration`. Setting `workAreaDuration = 5` with `workAreaStart = 2` means the work area spans from 2s to 7s.

- **`comp.displayStartTime` only changes display timecode.** It shifts how frame numbers and timecodes appear in the UI. It does not change where layers sit on the timeline or affect `layer.inPoint`, `layer.startTime`, or `comp.workAreaStart`.

- **`comp.bgColor` uses the 0-1 range.** Like all AE color arrays, values are `[r, g, b]` where each channel is 0.0 to 1.0, not 0-255.

- **Adding a comp as a layer creates a live link.** Changes to the nested comp are immediately reflected in the parent. There is no "flattening" -- the nested comp layer is a live reference to the `CompItem`.

- **`selectedLayers` order vs. layer stack order.** `comp.selectedLayers` returns layers in selection order (the order the user clicked), which may not match the layer stack order. Always extract `.index` from each layer and sort the indices before passing to `precompose()`.

---

## Complete Example: Create a New Comp and Precompose Selected Layers

```jsx
app.beginUndoGroup("AE Assistant: precompose selected layers");
try {
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        writeResult({ error: "No active composition" });
        return;
    }

    var sel = comp.selectedLayers;
    if (sel.length === 0) {
        writeResult({ error: "No layers selected" });
        return;
    }

    // Collect 1-based layer indices and sort ascending
    var indices = [];
    for (var i = 0; i < sel.length; i++) {
        indices.push(sel[i].index);
    }
    indices.sort(function(a, b) { return a - b; });

    // Verify indices are contiguous
    for (var i = 1; i < indices.length; i++) {
        if (indices[i] !== indices[i - 1] + 1) {
            writeResult({
                error: "Selected layers are not contiguous in the layer stack. "
                     + "Indices: " + indices.join(", ")
            });
            return;
        }
    }

    // Create the precomp (moveAllAttributes = true)
    var precompName = "Precomp - " + sel[0].name;
    var newComp = comp.layers.precompose(indices, precompName, true);

    // Optionally organize: move the new precomp into a folder
    var folder = null;
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof FolderItem && item.name === "Precomps") {
            folder = item;
            break;
        }
    }
    if (!folder) {
        folder = app.project.items.addFolder("Precomps");
    }
    newComp.parentFolder = folder;

    writeResult({
        success: true,
        message: "Precomposed " + indices.length + " layers into \"" + precompName + "\"",
        precompName: newComp.name,
        precompId: newComp.id,
        layerCount: indices.length
    });
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## 📄 SOURCE FILE: `skills/after-effects/rules/layer-manipulation.md` (verbatim)

# Layer Manipulation

> Rule file for creating, deleting, duplicating, reordering, parenting, and configuring layers in After Effects via ExtendScript.

---

## Creating Layers

All layer creation methods live on `comp.layers` (a `LayerCollection`). Every method returns the newly created layer.

### Solid Layer

```jsx
// comp.layers.addSolid(color, name, width, height, pixelAspect)
// color is [r, g, b] with each channel in the 0-1 range
var solid = comp.layers.addSolid([1, 0, 0], "Red Solid", comp.width, comp.height, 1);
```

### Null Object

```jsx
// comp.layers.addNull(duration)
// duration is optional (defaults to comp duration)
var nullLayer = comp.layers.addNull();

// With explicit duration (in seconds)
var nullLayer = comp.layers.addNull(5);
```

### Shape Layer

```jsx
var shape = comp.layers.addShape();
```

### Text Layer

```jsx
// Pass a string directly
var text = comp.layers.addText("Hello");

// Or pass a TextDocument for more control
var textDoc = new TextDocument("Hello");
textDoc.fontSize = 72;
textDoc.font = "Arial";
textDoc.fillColor = [1, 1, 1];
var text = comp.layers.addText(textDoc);
```

**CRITICAL: Some TextDocument properties (like `justification`) can only be set AFTER the layer exists.** Set them by reading the source text property back from the layer, modifying it, and calling `setValue()`:

```jsx
// WRONG - justification on a standalone TextDocument throws
// "Unable to set value as it is not associated with a layer"
var textDoc = new TextDocument("Hello");
textDoc.justification = ParagraphJustification.CENTER_JUSTIFY; // ERROR

// CORRECT - set justification after creating the layer
var textLayer = comp.layers.addText("Hello");
var textProp = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
var textDoc = textProp.value;
textDoc.fontSize = 72;
textDoc.font = "Arial";
textDoc.fillColor = [1, 1, 1];
textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
textProp.setValue(textDoc);
```

Properties safe to set on standalone TextDocument (before addText): `text`, `fontSize`, `font`, `fillColor`, `strokeColor`, `strokeWidth`, `applyFill`, `applyStroke`.

Properties that MUST be set after layer creation (via setValue): `justification`, `baselineLocs`, `boxText`, `boxTextSize`, `baselineShift`, `tracking`.

### Camera

```jsx
// comp.layers.addCamera(name, centerPoint)
var cam = comp.layers.addCamera("Camera 1", [comp.width / 2, comp.height / 2]);
```

### Light

```jsx
// comp.layers.addLight(name, centerPoint)
var light = comp.layers.addLight("Light 1", [comp.width / 2, comp.height / 2]);
```

### Add Existing Footage or Composition as a Layer

```jsx
// comp.layers.add(item) — item is a FootageItem or CompItem from the project
var layer = comp.layers.add(footageItem);

// Example: find a project item by name and add it
var item = null;
for (var i = 1; i <= app.project.numItems; i++) {
    if (app.project.item(i).name === "logo.png") {
        item = app.project.item(i);
        break;
    }
}
if (item) {
    var layer = comp.layers.add(item);
}
```

---

## Deleting Layers

```jsx
layer.remove();
```

When deleting multiple layers in a loop, iterate in **reverse order** to avoid index shifting:

```jsx
// CORRECT: reverse iteration
for (var i = comp.numLayers; i >= 1; i--) {
    var layer = comp.layer(i);
    if (layer.name.indexOf("temp") === 0) {
        layer.remove();
    }
}
```

```jsx
// WRONG: forward iteration — indices shift after each removal
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    if (layer.name.indexOf("temp") === 0) {
        layer.remove(); // next layer now has this index, gets skipped
    }
}
```

---

## Duplicating Layers

```jsx
// duplicate() returns the new layer (inserted directly above the original)
var newLayer = layer.duplicate();
newLayer.name = "Copy of " + layer.name;
```

---

## Reordering Layers

Layer index 1 is the topmost layer in the comp. Moving a layer changes the indices of other layers.

```jsx
// Move layer directly above another layer
layer.moveBefore(otherLayer);

// Move layer directly below another layer
layer.moveAfter(otherLayer);

// Move layer to top of comp (index 1)
layer.moveToBeginning();

// Move layer to bottom of comp
layer.moveToEnd();
```

### Example: Move a layer to a specific index

```jsx
// Move "Logo" to index 3
var logo = comp.layer("Logo");
var targetLayer = comp.layer(3);
logo.moveAfter(targetLayer);
```

---

## Parenting

```jsx
// Set parent
layer.parent = otherLayer;

// Remove parent (unparent)
layer.parent = null;
```

### Example: Parent all selected layers to a null

```jsx
var nullCtrl = comp.layers.addNull();
nullCtrl.name = "Controller";
var sel = comp.selectedLayers;
for (var i = 0; i < sel.length; i++) {
    sel[i].parent = nullCtrl;
}
```

---

## Renaming

```jsx
layer.name = "New Name";
```

---

## Layer Flags

### Visibility, Lock, Solo, Shy

```jsx
layer.enabled = true;   // visibility (eye icon)
layer.enabled = false;

layer.locked = true;     // lock the layer
layer.locked = false;

layer.solo = true;       // solo the layer
layer.solo = false;

layer.shy = true;        // mark layer as shy
layer.shy = false;
```

### 3D Layer (AVLayer only)

```jsx
// Only works on AVLayer instances (solids, footage, shapes, text, nulls)
// Does NOT apply to cameras or lights (they are always 3D)
layer.threeDLayer = true;
layer.threeDLayer = false;
```

### Adjustment Layer (AVLayer only)

```jsx
layer.adjustmentLayer = true;
layer.adjustmentLayer = false;
```

### Guide Layer

```jsx
layer.guideLayer = true;
layer.guideLayer = false;
```

### Full Example: Create an Adjustment Layer

```jsx
var adj = comp.layers.addSolid([0, 0, 0], "Adjustment", comp.width, comp.height, 1);
adj.adjustmentLayer = true;
adj.name = "Color Correction";
```

---

## Timing

All time values are in **seconds** (floating point).

```jsx
// In point — when the layer becomes visible
layer.inPoint = 1.0;

// Out point — when the layer stops being visible
layer.outPoint = 5.0;

// Start time — shifts the layer's internal timeline
// Positive values delay the layer content; negative values pre-roll it
layer.startTime = 0.5;

// Stretch — time stretch factor as a percentage
// 100 = normal speed, 200 = half speed, 50 = double speed
layer.stretch = 100;
```

### Example: Trim a Layer to the Work Area

```jsx
layer.inPoint = comp.workAreaStart;
layer.outPoint = comp.workAreaStart + comp.workAreaDuration;
```

### Example: Offset a Layer to Start at the Current Time

```jsx
var offset = comp.time - layer.inPoint;
layer.startTime = layer.startTime + offset;
```

---

## Labels

```jsx
// label is an integer 0-16
// 0 = None, 1 = Red, 2 = Yellow, 3 = Aqua, 4 = Pink, 5 = Lavender,
// 6 = Peach, 7 = Sea Foam, 8 = Blue, 9 = Green, 10 = Purple,
// 11 = Orange, 12 = Brown, 13 = Fuchsia, 14 = Cyan, 15 = Sandstone, 16 = Dark Green
layer.label = 1;  // Red
layer.label = 8;  // Blue
layer.label = 0;  // None (remove label color)
```

---

## MUST

- **MUST** check `layer.locked` before modifying any layer property. Locked layers throw errors on write operations. Unlock first, make changes, then re-lock if needed:

```jsx
var wasLocked = layer.locked;
if (wasLocked) {
    layer.locked = false;
}

// ... modify the layer ...

if (wasLocked) {
    layer.locked = true;
}
```

- **MUST** wrap all layer modifications in an undo group:

```jsx
app.beginUndoGroup("AE Assistant: modify layers");
try {
    // ... layer operations ...
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

- **MUST** verify the comp exists and is a `CompItem` before accessing `comp.layers`:

```jsx
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    writeResult({ error: "No active composition" });
    return;
}
```

- **MUST** use 1-based indexing when accessing layers by index (`comp.layer(1)` is the first layer). The `selectedLayers` array is 0-based.

---

## FORBIDDEN

- **FORBIDDEN:** Accessing `layer.source` on cameras or lights without a try/catch. These layer types have no source and will throw:

```jsx
// WRONG — will throw on cameras and lights
var src = layer.source;

// CORRECT — guard with try/catch
try {
    var src = layer.source;
} catch (e) {
    // layer has no source (camera, light)
}

// ALSO CORRECT — check type first
if (layer instanceof AVLayer) {
    var src = layer.source;
}
```

- **FORBIDDEN:** Using `layer.threeDLayer` or `layer.adjustmentLayer` on CameraLayer or LightLayer. These properties only exist on AVLayer.

- **FORBIDDEN:** Using ES5+ syntax. Use `var`, not `let`/`const`. Use string concatenation with `+`, not template literals.

---

## Gotchas

- **Locked layers block ALL modifications:** `layer.moveToEnd()`, `layer.moveBefore()`, `layer.moveAfter()`, `layer.moveToBeginning()`, setting properties, adding effects — ALL throw errors on locked layers. Always check and temporarily unlock:

```jsx
var wasLocked = layer.locked;
if (wasLocked) layer.locked = false;
layer.moveToEnd();  // or any other operation
if (wasLocked) layer.locked = true;
```

- **Index shifting on move:** `layer.moveBefore()`, `layer.moveAfter()`, `layer.moveToBeginning()`, and `layer.moveToEnd()` change the indices of other layers. Never cache layer indices across move operations. Re-fetch layers by name or re-read indices after moving.

- **Index shifting on delete:** When deleting layers in a loop, always iterate in reverse (`for (var i = comp.numLayers; i >= 1; i--)`) to avoid skipping layers due to index shifting.

- **addSolid color range:** `addSolid` expects color values as `[r, g, b]` in the **0.0 to 1.0** range, not 0-255. To convert from 0-255: `[r/255, g/255, b/255]`.

```jsx
// Convert hex #FF6600 to AE color
var color = [0xFF / 255, 0x66 / 255, 0x00 / 255];  // [1.0, 0.4, 0.0]
var solid = comp.layers.addSolid(color, "Orange Solid", comp.width, comp.height, 1);
```

- **duplicate() position:** `layer.duplicate()` places the new layer directly above the original (at the same index, pushing the original down by one). The returned layer reference points to the new copy.

- **Parenting and transforms:** Setting `layer.parent` does not change the layer's visual position. AE recalculates the transform values to keep the layer in the same world-space position. If you want to preserve the raw transform values instead, save them before parenting and restore after.

- **Null layers are AVLayers:** Null objects are instances of AVLayer with `nullLayer === true`. They support `threeDLayer`, `parent`, and transform properties, but have no visual content.

- **selectedLayers is 0-based:** `comp.selectedLayers` returns a JavaScript array (0-based), while `comp.layer(index)` uses 1-based indexing. Do not confuse the two:

```jsx
// 0-based array
var sel = comp.selectedLayers;
for (var i = 0; i < sel.length; i++) {
    var layer = sel[i]; // direct layer reference, no index needed
}

// 1-based layer access
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
}
```

- **Camera and Light layers:** These are always 3D. They do not have `threeDLayer`, `adjustmentLayer`, or `guideLayer` properties. They are instances of `CameraLayer` and `LightLayer`, not `AVLayer`.

- **layer.stretch behavior:** Stretch is percentage-based. Setting `layer.stretch = 200` makes the layer play at half speed (doubled duration). Setting it to `50` doubles the playback speed (halved duration). Stretch affects `inPoint` and `outPoint` relative to `startTime`.

---

## Complete Example: Build a Layer Stack

```jsx
app.beginUndoGroup("AE Assistant: build layer stack");
try {
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        writeResult({ error: "No active composition" });
        return;
    }

    // Create a background solid
    var bg = comp.layers.addSolid(
        [0.1, 0.1, 0.15], "Background",
        comp.width, comp.height, 1
    );
    bg.moveToEnd();
    bg.locked = true;
    bg.label = 1; // Red

    // Create a null controller
    var ctrl = comp.layers.addNull();
    ctrl.name = "Master Controller";
    ctrl.threeDLayer = false;
    ctrl.label = 5; // Lavender

    // Create a text layer
    var textDoc = new TextDocument("Title");
    textDoc.fontSize = 120;
    textDoc.fillColor = [1, 1, 1];
    var title = comp.layers.addText(textDoc);
    title.name = "Title Text";
    title.parent = ctrl;
    title.label = 8; // Blue

    // Create a shape layer
    var shape = comp.layers.addShape();
    shape.name = "Underline";
    shape.parent = ctrl;
    shape.label = 8; // Blue

    // Trim all layers to 5 seconds
    var layers = [bg, ctrl, title, shape];
    for (var i = 0; i < layers.length; i++) {
        var wasLocked = layers[i].locked;
        if (wasLocked) layers[i].locked = false;
        layers[i].inPoint = 0;
        layers[i].outPoint = 5;
        if (wasLocked) layers[i].locked = true;
    }

    writeResult({
        success: true,
        message: "Created layer stack with 4 layers",
        layers: [bg.name, ctrl.name, title.name, shape.name]
    });
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## 📄 SOURCE FILE: `skills/after-effects/rules/assets-footage.md` (verbatim)

# Assets & Footage

> Rule file for importing, replacing, organizing, and inspecting assets and footage in After Effects via ExtendScript.

---

## Importing Files

Use `app.project.importFile()` with an `ImportOptions` object built from a `File` reference.

```jsx
var io = new ImportOptions(new File("/absolute/path/to/file.mov"));
var item = app.project.importFile(io);
```

The returned object is a `FootageItem` (for single files) or a `CompItem` (when importing as composition).

### ImportAsType

Control how the file is interpreted with `importOptions.importAs`:

```jsx
// Import as footage (default for single media files)
var io = new ImportOptions(new File("/path/to/clip.mov"));
io.importAs = ImportAsType.FOOTAGE;
var footage = app.project.importFile(io);

// Import as composition (e.g. layered PSD, AI file)
var io = new ImportOptions(new File("/path/to/design.psd"));
io.importAs = ImportAsType.COMP;
var comp = app.project.importFile(io);

// Import an After Effects project into the current project
var io = new ImportOptions(new File("/path/to/other_project.aep"));
io.importAs = ImportAsType.PROJECT;
app.project.importFile(io);
```

### Importing Image Sequences

Enable sequence detection and alphabetical ordering on the `ImportOptions` object:

```jsx
var io = new ImportOptions(new File("/path/to/sequence/frame_0001.png"));
io.sequence = true;
io.forceAlphabetical = true;
var seqItem = app.project.importFile(io);
```

The `File` object must point to the **first frame** of the sequence. After Effects infers the remaining frames from the filename pattern.

---

## Replacing Footage

### Replace with a Single File

```jsx
footageItem.replace(new File("/absolute/path/to/new_file.mov"));
```

### Replace with an Image Sequence

```jsx
// firstFrame: File object pointing to the first frame
// forceAlphabetical: boolean — true to sort frames alphabetically
footageItem.replaceWithSequence(new File("/path/to/new_seq/frame_0001.png"), true);
```

Both methods update every composition that references the footage item.

---

## Creating and Organizing Folders

### Creating Folders

```jsx
var folder = app.project.items.addFolder("Assets");
```

Folders are `FolderItem` objects in the project panel.

### Nested Folders

```jsx
var rootFolder = app.project.items.addFolder("Project Assets");
var subfolder = app.project.items.addFolder("Footage");
subfolder.parentFolder = rootFolder;
```

### Moving Items into Folders

Assign the `parentFolder` property to relocate any project item (footage, comp, solid, folder):

```jsx
item.parentFolder = folder;
```

### Example: Organize All Footage into a Folder

```jsx
var folder = app.project.items.addFolder("Footage");
for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
    if (item instanceof FootageItem && item.parentFolder === app.project.rootFolder) {
        item.parentFolder = folder;
    }
}
```

---

## Footage Properties

Every `FootageItem` exposes properties about its media:

```jsx
var item = app.project.item(1); // assumes a FootageItem

item.name;            // String — display name in the project panel
item.width;           // Number — pixel width (0 if no video stream)
item.height;          // Number — pixel height (0 if no video stream)
item.duration;        // Number — duration in seconds (0 for stills)
item.hasVideo;        // Boolean — true if the item contains a video stream
item.hasAudio;        // Boolean — true if the item contains an audio stream
item.footageMissing;  // Boolean — true if the source file cannot be found on disk
item.frameRate;       // Number — frames per second
item.time;            // Number — current time (rarely used on footage)
```

### The mainSource Property

`footageItem.mainSource` returns a source descriptor object. Its type tells you what kind of asset the footage item wraps:

```jsx
var src = footageItem.mainSource;

if (src instanceof FileSource) {
    // File-based footage — video, image, audio, sequence
    var filePath = src.file.fsName; // full OS path to the source file
}

if (src instanceof SolidSource) {
    // Solid — created via comp.layers.addSolid()
    var color = src.color; // [r, g, b] in 0-1 range
}

if (src instanceof PlaceholderSource) {
    // Placeholder — a stand-in for missing or not-yet-linked media
}
```

---

## Finding Footage by Name or Path

### By Name

```jsx
function findFootageByName(name) {
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof FootageItem && item.name === name) {
            return item;
        }
    }
    return null;
}
```

### By File Path

```jsx
function findFootageByPath(filePath) {
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof FootageItem && item.mainSource instanceof FileSource) {
            if (item.mainSource.file.fsName === filePath) {
                return item;
            }
        }
    }
    return null;
}
```

---

## Proxies

Proxies let you substitute a lighter file for preview without changing the final render source.

### Set a Proxy

```jsx
footageItem.setProxy(new File("/path/to/proxy_file.mov"));
```

### Remove a Proxy

```jsx
footageItem.setProxyToNone();
```

### Check Proxy Status

```jsx
if (footageItem.proxySource !== null) {
    // proxy is active
    var proxyPath = footageItem.proxySource.file.fsName;
}
```

---

## Interpret Footage

Interpretation settings live on `footageItem.mainSource`. After changing any interpretation property, call `footageItem.mainSource.guessAlphaMode()` or set values explicitly.

### Conform Frame Rate

```jsx
// Override the interpreted frame rate (does not re-encode)
footageItem.mainSource.conformFrameRate = 24;
```

### Alpha Mode

```jsx
// AlphaMode.IGNORE — treat as opaque
// AlphaMode.STRAIGHT — straight (unmatted) alpha
// AlphaMode.PREMULTIPLIED — premultiplied alpha
footageItem.mainSource.alphaMode = AlphaMode.PREMULTIPLIED;
```

### Field Separation

```jsx
// FieldSeparationType.OFF — progressive (no fields)
// FieldSeparationType.UPPER_FIELD_FIRST
// FieldSeparationType.LOWER_FIELD_FIRST
footageItem.mainSource.fieldSeparationType = FieldSeparationType.OFF;
```

---

## MUST

- **MUST** use absolute file paths when constructing `File` objects for import or replace. Relative paths resolve unpredictably and differ between macOS and Windows:

```jsx
// WRONG — relative path, will fail or resolve to the wrong location
var io = new ImportOptions(new File("footage/clip.mov"));

// CORRECT — absolute path
var io = new ImportOptions(new File("/Users/me/project/footage/clip.mov"));
```

- **MUST** verify that the file exists before importing. `ImportOptions` will throw if the file does not exist:

```jsx
var f = new File("/path/to/file.mov");
if (!f.exists) {
    writeResult({ error: "File not found: " + f.fsName });
    return;
}
var io = new ImportOptions(f);
var item = app.project.importFile(io);
```

- **MUST** wrap all import and project-structure operations in an undo group:

```jsx
app.beginUndoGroup("AE Assistant: import assets");
try {
    // ... import / organize operations ...
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

- **MUST** use 1-based indexing when iterating `app.project.items` or `app.project.numItems`. Index 0 does not exist:

```jsx
for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
}
```

- **MUST** check `instanceof FootageItem` before accessing footage-specific properties like `.mainSource`, `.hasVideo`, `.footageMissing`, etc. `CompItem` and `FolderItem` do not have these properties:

```jsx
var item = app.project.item(i);
if (item instanceof FootageItem) {
    var src = item.mainSource;
}
```

---

## FORBIDDEN

- **FORBIDDEN:** Using relative paths in `new File()` calls. Always provide a full absolute path. Relative paths are resolved from an unpredictable working directory and are not portable.

- **FORBIDDEN:** Using ES5+ syntax. Use `var`, not `let`/`const`. Use string concatenation with `+`, not template literals. Use `function` declarations, not arrow functions.

- **FORBIDDEN:** Calling `footageItem.mainSource.file` on a `SolidSource` or `PlaceholderSource`. Only `FileSource` has a `.file` property. Always check the source type first:

```jsx
// WRONG — throws if mainSource is not a FileSource
var path = footageItem.mainSource.file.fsName;

// CORRECT
if (footageItem.mainSource instanceof FileSource) {
    var path = footageItem.mainSource.file.fsName;
}
```

- **FORBIDDEN:** Importing files without error handling. `app.project.importFile()` throws when the file is missing, the format is unsupported, or import options are invalid. Always wrap in try/catch.

- **FORBIDDEN:** Assuming `importAs` is valid for all file types. Not every file supports every `ImportAsType`. For example, `ImportAsType.COMP` only works with layered formats (PSD, AI). Attempting an unsupported combination throws an error.

---

## Gotchas

- **Import paths must be absolute.** `new File("relative/path.mov")` resolves from ExtendScript's internal working directory, which is unpredictable and changes between sessions. Always build full paths. If you receive a relative path from the user, resolve it against a known base first.

- **macOS `File` paths use `/` separators.** On macOS, pass POSIX-style paths: `/Users/name/footage/clip.mov`. On Windows, use backslashes or forward slashes (both work): `C:/Users/name/footage/clip.mov`. The `File.fsName` property always returns the OS-native path format.

- **`importFile` can return either a `FootageItem` or a `CompItem`.** When `importAs` is `ImportAsType.COMP`, the return value is a `CompItem`. When importing a layered file as `COMP`, AE may also create a folder containing the individual layers as footage items. Do not assume the return type without checking.

- **Sequence import requires the first frame.** `ImportOptions.sequence = true` expects the `File` to point to the first numbered frame in the sequence. AE reads the filename pattern and finds subsequent frames automatically. If the first frame does not follow a recognized numbering pattern, the import fails silently or imports only that single frame.

- **`numItems` changes during loops that add items.** When importing files inside a loop over `app.project.numItems`, new items increment `numItems`. Cache the count before the loop or iterate backward to avoid processing newly added items:

```jsx
var count = app.project.numItems;
for (var i = 1; i <= count; i++) {
    // safe — count was captured before any imports
}
```

- **Replacing footage is destructive.** `footageItem.replace()` and `footageItem.replaceWithSequence()` permanently change the source for that item across all compositions. There is no built-in "unreplace" other than undo.

- **`footageMissing` is read-only.** You cannot set `footageMissing` to fix a broken link. Use `footageItem.replace(new File(correctPath))` to relink missing footage.

- **Proxy does not affect final render by default.** When rendering, AE uses the original source unless the render settings explicitly say "Use All Proxies." Setting a proxy only affects previews in the timeline.

- **`conformFrameRate` is not the same as source frame rate.** `mainSource.conformFrameRate` overrides the interpreted frame rate. Setting it to `0` resets to the file's native frame rate. The original frame rate of the file is not directly readable — `footageItem.frameRate` reflects the conformed (interpreted) rate.

---

## Complete Example: Import a File, Create a Folder, Move It In

```jsx
app.beginUndoGroup("AE Assistant: import and organize");
try {
    // 1. Define the file path and validate it exists
    var filePath = "/Users/me/project/footage/hero_shot.mov";
    var f = new File(filePath);
    if (!f.exists) {
        writeResult({ error: "File not found: " + f.fsName });
        return;
    }

    // 2. Import the file as footage
    var io = new ImportOptions(f);
    io.importAs = ImportAsType.FOOTAGE;
    var footageItem = app.project.importFile(io);

    // 3. Create a folder in the project panel
    var folder = app.project.items.addFolder("Imported Footage");

    // 4. Move the imported item into the folder
    footageItem.parentFolder = folder;

    // 5. Report results
    writeResult({
        success: true,
        message: "Imported and organized footage",
        item: {
            name: footageItem.name,
            width: footageItem.width,
            height: footageItem.height,
            duration: footageItem.duration,
            hasVideo: footageItem.hasVideo,
            hasAudio: footageItem.hasAudio,
            folder: folder.name
        }
    });
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## 📄 SOURCE FILE: `skills/after-effects/rules/batch-operations.md` (verbatim)

# Batch & Bulk Operations

> **Loaded when:** the task involves operating on multiple layers, multiple comps, batch rename, bulk effect application, or any repetitive operation across collections.

All code in this file is ES3-compatible ExtendScript. See `extendscript-fundamentals.md` for baseline syntax rules.

---

## Core Pattern: Iterate and Apply

Every batch operation follows the same shape: iterate a collection with a `for` loop, test each item against a condition, and apply the operation to items that match.

```jsx
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    if (condition(layer)) {
        // apply operation to layer
    }
}
```

AE collections (layers, project items, properties) are **1-based**. JavaScript arrays returned by AE (`selectedLayers`, `selectedProperties`) are **0-based**. Never mix the two indexing schemes.

---

## Filtering Layers

### By Type: `instanceof`

The most reliable way to filter layers by type. Check from most specific to least specific because `TextLayer` and `ShapeLayer` are subclasses of `AVLayer`.

```jsx
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);

    if (layer instanceof TextLayer) {
        // Text layers only
    } else if (layer instanceof ShapeLayer) {
        // Shape layers only
    } else if (layer instanceof CameraLayer) {
        // Cameras only
    } else if (layer instanceof LightLayer) {
        // Lights only
    } else if (layer instanceof AVLayer) {
        // Solids, footage, precomps, nulls, adjustment layers
    }
}
```

### By Type: `matchName`

An alternative when you need string-based dispatch (e.g. mapping types to handler functions).

| `layer.matchName` | Layer Type |
|---|---|
| `"ADBE AV Layer"` | AVLayer (footage, solid, precomp, null, adjustment) |
| `"ADBE Text Layer"` | TextLayer |
| `"ADBE Vector Layer"` | ShapeLayer |
| `"ADBE Camera Layer"` | CameraLayer |
| `"ADBE Light Layer"` | LightLayer |

```jsx
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    if (layer.matchName === "ADBE Vector Layer") {
        // Shape layer
    }
}
```

### By Subtype Flags: `nullLayer`, `adjustmentLayer`

Null objects and adjustment layers are both `AVLayer` instances. Use their boolean flags to distinguish them.

```jsx
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    if (layer instanceof AVLayer) {
        if (layer.nullLayer) {
            // Null object
        } else if (layer.adjustmentLayer) {
            // Adjustment layer
        }
    }
}
```

### By Name: String Matching

Use `String.prototype.indexOf` for prefix, suffix, and substring matching. Regex is available in ES3 but is unreliable for complex patterns in ExtendScript -- prefer explicit string methods.

```jsx
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    var name = layer.name;

    // Prefix match
    if (name.indexOf("bg_") === 0) {
        // layer name starts with "bg_"
    }

    // Suffix match
    var suffix = "_ref";
    if (name.indexOf(suffix, name.length - suffix.length) !== -1) {
        // layer name ends with "_ref"
    }

    // Contains match
    if (name.indexOf("hero") !== -1) {
        // layer name contains "hero" anywhere
    }

    // Case-insensitive match
    if (name.toLowerCase().indexOf("title") !== -1) {
        // matches "Title", "TITLE", "title", etc.
    }
}
```

---

## Operating on Selected Layers

`comp.selectedLayers` returns a standard JavaScript array (0-based). Use it to limit operations to what the user has manually selected.

```jsx
var sel = comp.selectedLayers;
if (sel.length === 0) {
    writeResult({ error: "No layers selected" });
    return;
}

for (var i = 0; i < sel.length; i++) {
    var layer = sel[i];
    // apply operation
}
```

---

## Batch Rename

Iterate layers and set the `.name` property.

```jsx
// Rename layers: replace a prefix
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    if (layer.name.indexOf("old_") === 0) {
        layer.name = "new_" + layer.name.substring(4);
    }
}
```

```jsx
// Rename layers: add a numbered suffix
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    layer.name = layer.name + " [" + i + "]";
}
```

---

## Batch Apply Effect

Add effects using `addProperty` on the layer's effects group (`"ADBE Effect Parade"`). Every effect is identified by its matchName.

```jsx
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    var effects = layer.property("ADBE Effect Parade");
    var blur = effects.addProperty("ADBE Gaussian Blur 2");
    blur.property("ADBE Gaussian Blur 2-0001").setValue(15); // Blurriness
}
```

```jsx
// Apply effect only to layers that don't already have it
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    var effects = layer.property("ADBE Effect Parade");
    var existing = effects.property("ADBE Gaussian Blur 2");
    if (!existing) {
        effects.addProperty("ADBE Gaussian Blur 2");
    }
}
```

---

## Batch Keyframe Copy

Read all keyframe data from a source property and write it to one or more target properties. This copies times, values, interpolation types, and temporal ease.

```jsx
function copyKeyframesToTargets(srcProp, targetProps) {
    for (var t = 0; t < targetProps.length; t++) {
        var dst = targetProps[t];

        // Clear existing keyframes (reverse order)
        for (var k = dst.numKeys; k >= 1; k--) {
            dst.removeKey(k);
        }

        if (srcProp.numKeys === 0) {
            // Static value -- copy directly
            dst.setValue(srcProp.value);
        } else {
            for (var k = 1; k <= srcProp.numKeys; k++) {
                var time = srcProp.keyTime(k);
                var value = srcProp.keyValue(k);
                dst.setValueAtTime(time, value);

                var newIdx = dst.nearestKeyIndex(time);

                // Copy interpolation type
                dst.setInterpolationTypeAtKey(newIdx,
                    srcProp.keyInInterpolationType(k),
                    srcProp.keyOutInterpolationType(k)
                );

                // Copy temporal ease
                try {
                    dst.setTemporalEaseAtKey(newIdx,
                        srcProp.keyInTemporalEase(k),
                        srcProp.keyOutTemporalEase(k)
                    );
                } catch (e) {
                    // Temporal ease not supported on this property type
                }
            }
        }
    }
}
```

### Usage: Copy Opacity Keyframes from First Selected Layer to All Others

```jsx
var sel = comp.selectedLayers;
if (sel.length < 2) {
    writeResult({ error: "Select at least 2 layers (source + targets)" });
    return;
}

var srcProp = sel[0].property("ADBE Transform Group").property("ADBE Opacity");
var targets = [];
for (var i = 1; i < sel.length; i++) {
    targets.push(sel[i].property("ADBE Transform Group").property("ADBE Opacity"));
}
copyKeyframesToTargets(srcProp, targets);
```

---

## Across Compositions

Iterate `app.project.items` (1-based) and check each item with `instanceof CompItem` to operate across all compositions in the project.

```jsx
for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
    if (item instanceof CompItem) {
        var comp = item;
        for (var j = 1; j <= comp.numLayers; j++) {
            var layer = comp.layer(j);
            // apply operation across every layer in every comp
        }
    }
}
```

### Filtering Comps by Name

```jsx
for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
    if (item instanceof CompItem && item.name.indexOf("FINAL_") === 0) {
        // Only comps whose name starts with "FINAL_"
    }
}
```

---

## Performance: Suppress Dialogs

For batch operations that touch many items, suppress modal dialogs that AE may pop up during the operation. This prevents the script from hanging on a dialog that requires user interaction.

```jsx
app.beginSuppressDialogs();
try {
    // batch operations here
} finally {
    app.endSuppressDialogs(false); // false = discard any suppressed alert text
}
```

Combined with the undo group pattern:

```jsx
app.beginUndoGroup("AE Assistant: batch operation");
app.beginSuppressDialogs();
try {
    // batch operations
} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endSuppressDialogs(false);
    app.endUndoGroup();
}
```

---

## MUST

- **MUST** wrap all batch mutation operations in `app.beginUndoGroup()` / `app.endUndoGroup()` so the entire batch can be undone with a single Ctrl+Z / Cmd+Z.

- **MUST** iterate in **reverse** when removing layers, removing keyframes, or performing any operation that changes collection length or indices:

```jsx
for (var i = comp.numLayers; i >= 1; i--) {
    var layer = comp.layer(i);
    if (shouldRemove(layer)) {
        layer.remove();
    }
}
```

- **MUST** check `layer.locked` before modifying a layer in a batch loop. Locked layers throw on write. Unlock first, modify, then re-lock:

```jsx
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    var wasLocked = layer.locked;
    if (wasLocked) layer.locked = false;

    // ... modify layer ...

    if (wasLocked) layer.locked = true;
}
```

- **MUST** verify the active item is a `CompItem` before operating on layers:

```jsx
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    writeResult({ error: "No active composition" });
    return;
}
```

- **MUST** use 1-based indexing for AE collections (`comp.layer(1)`, `app.project.item(1)`) and 0-based indexing for JavaScript arrays (`comp.selectedLayers[0]`).

- **MUST** balance every `app.beginSuppressDialogs()` with a matching `app.endSuppressDialogs()`. Place the end call in a `finally` block so it runs even on error.

- **MUST** check `instanceof` or `matchName` before accessing type-specific properties. Accessing `layer.nullLayer` on a `CameraLayer` or `LightLayer` will throw because those properties only exist on `AVLayer`.

---

## FORBIDDEN

- **FORBIDDEN:** Using `Array.prototype.forEach`, `.map`, `.filter`, or `.reduce`. These do not exist in ES3. Use `for` loops for all iteration.

```jsx
// WRONG -- runtime error: forEach is not a function
comp.selectedLayers.forEach(function(layer) { layer.enabled = false; });

// CORRECT
var sel = comp.selectedLayers;
for (var i = 0; i < sel.length; i++) {
    sel[i].enabled = false;
}
```

- **FORBIDDEN:** Forward iteration when deleting. Indices shift downward after each removal, causing layers to be skipped.

```jsx
// WRONG -- layers get skipped
for (var i = 1; i <= comp.numLayers; i++) {
    comp.layer(i).remove();
}

// CORRECT -- reverse iteration
for (var i = comp.numLayers; i >= 1; i--) {
    comp.layer(i).remove();
}
```

- **FORBIDDEN:** Using `let`, `const`, arrow functions, template literals, destructuring, or any ES5+ syntax. All code must be ES3.

- **FORBIDDEN:** Using `alert()` in batch scripts. A single `alert()` inside a loop over hundreds of layers will create hundreds of modal dialogs.

- **FORBIDDEN:** Calling `app.beginSuppressDialogs()` without a matching `app.endSuppressDialogs()`. Unbalanced calls leave AE in a broken state where all dialogs are permanently suppressed until restart.

---

## Gotchas

- **Reverse iteration on delete.** When removing layers in a loop, you MUST iterate from `comp.numLayers` down to `1`. Forward iteration causes index shifting: after removing layer 3, the old layer 4 becomes the new layer 3 and gets skipped on the next iteration.

```jsx
// Removing layers 3, 4, 5 in a forward loop:
// Remove layer 3 -> old layer 4 is now layer 3 -> i++ goes to 4 -> old layer 5 (now 4) is skipped

// CORRECT: reverse iteration avoids this entirely
for (var i = comp.numLayers; i >= 1; i--) {
    if (shouldRemove(comp.layer(i))) {
        comp.layer(i).remove();
    }
}
```

- **Index shifting during modification.** Any operation that changes a layer's index (moving, adding, duplicating, or deleting layers) invalidates cached indices for layers below the change point. If you must move or reorder layers inside a loop, either iterate in reverse or collect target layers by reference first, then operate on the collected references.

```jsx
// Safe: collect references first, then operate
var targets = [];
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    if (layer.name.indexOf("move_") === 0) {
        targets.push(layer);
    }
}
for (var i = 0; i < targets.length; i++) {
    targets[i].moveToEnd();
}
```

- **`beginSuppressDialogs` must be balanced.** Every `app.beginSuppressDialogs()` call must have a matching `app.endSuppressDialogs()`. If the script errors out between the two calls, dialogs remain suppressed for the rest of the AE session. Always use `try/finally`:

```jsx
app.beginSuppressDialogs();
try {
    // operations
} finally {
    app.endSuppressDialogs(false);
}
```

- **`selectedLayers` is a snapshot.** `comp.selectedLayers` returns an array at the moment it is called. If you change selection during the loop (e.g., by selecting/deselecting layers), the array does not update. Always capture it to a variable before iterating.

```jsx
var sel = comp.selectedLayers; // capture once
for (var i = 0; i < sel.length; i++) {
    // sel[i] is still valid even if selection changes during iteration
}
```

- **Regex is unreliable in ExtendScript.** Some regex features behave inconsistently or differently than in modern JavaScript. For batch name matching, prefer explicit string methods (`indexOf`, `substring`, `toLowerCase`) over regex.

- **Cross-comp iteration can be slow.** Iterating all layers in all comps in a large project can take significant time. Use `app.beginSuppressDialogs()` and consider adding a progress check or limiting the scope (e.g., filtering comps by name or folder).

- **`addProperty` on effects returns null if the matchName is wrong.** Double-check the effect matchName. There is no error thrown -- you get `null` back silently, and subsequent `.property()` calls on it will throw.

- **Locked layers in batch loops.** A single locked layer in the middle of a batch operation will throw an error and abort the entire script if not handled. Always check `layer.locked` before writing, or wrap individual layer operations in `try/catch`.

---

## Complete Example 1: Rename All Layers Matching a Pattern

Rename every layer whose name starts with `"Layer "` (the AE default) to a descriptive name with a zero-padded number.

```jsx
(function() {
    app.beginUndoGroup("AE Assistant: batch rename layers");
    try {
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            writeResult({ error: "No active composition" });
            return;
        }

        var prefix = "Layer ";
        var newPrefix = "Element";
        var renamed = 0;

        for (var i = 1; i <= comp.numLayers; i++) {
            var layer = comp.layer(i);
            if (layer.name.indexOf(prefix) === 0) {
                // Zero-pad the number to 3 digits
                var num = String(renamed + 1);
                while (num.length < 3) {
                    num = "0" + num;
                }
                layer.name = newPrefix + "_" + num;
                renamed++;
            }
        }

        writeResult({
            success: true,
            message: "Renamed " + renamed + " layers"
        });
    } catch (e) {
        writeResult({ error: e.toString(), line: e.line });
    } finally {
        app.endUndoGroup();
    }
})();
```

---

## Complete Example 2: Apply an Effect to All Selected Layers

Add a Gaussian Blur effect to every selected layer, setting Blurriness to 20 and the Repeat Edge Pixels option to on.

```jsx
(function() {
    app.beginUndoGroup("AE Assistant: batch apply Gaussian Blur");
    try {
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            writeResult({ error: "No active composition" });
            return;
        }

        var sel = comp.selectedLayers;
        if (sel.length === 0) {
            writeResult({ error: "No layers selected" });
            return;
        }

        var applied = 0;
        for (var i = 0; i < sel.length; i++) {
            var layer = sel[i];

            // Skip cameras and lights (they cannot have effects)
            if (layer instanceof CameraLayer || layer instanceof LightLayer) {
                continue;
            }

            var wasLocked = layer.locked;
            if (wasLocked) layer.locked = false;

            var effects = layer.property("ADBE Effect Parade");
            var blur = effects.addProperty("ADBE Gaussian Blur 2");
            if (blur) {
                blur.property("ADBE Gaussian Blur 2-0001").setValue(20); // Blurriness
                blur.property("ADBE Gaussian Blur 2-0002").setValue(1);  // Repeat Edge Pixels (on)
                applied++;
            }

            if (wasLocked) layer.locked = true;
        }

        writeResult({
            success: true,
            message: "Applied Gaussian Blur to " + applied + " layer" + (applied !== 1 ? "s" : "")
        });
    } catch (e) {
        writeResult({ error: e.toString(), line: e.line });
    } finally {
        app.endUndoGroup();
    }
})();
```

---

## Complete Example 3: Disable All Shape Layers in All Comps

Iterate every composition in the project and turn off visibility for every shape layer.

```jsx
(function() {
    app.beginUndoGroup("AE Assistant: disable all shape layers");
    app.beginSuppressDialogs();
    try {
        var disabledCount = 0;
        var compsProcessed = 0;

        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (!(item instanceof CompItem)) {
                continue;
            }

            var comp = item;
            compsProcessed++;

            for (var j = 1; j <= comp.numLayers; j++) {
                var layer = comp.layer(j);
                if (layer instanceof ShapeLayer) {
                    var wasLocked = layer.locked;
                    if (wasLocked) layer.locked = false;

                    layer.enabled = false;
                    disabledCount++;

                    if (wasLocked) layer.locked = true;
                }
            }
        }

        writeResult({
            success: true,
            message: "Disabled " + disabledCount + " shape layer" + (disabledCount !== 1 ? "s" : "") +
                     " across " + compsProcessed + " composition" + (compsProcessed !== 1 ? "s" : "")
        });
    } catch (e) {
        writeResult({ error: e.toString(), line: e.line });
    } finally {
        app.endSuppressDialogs(false);
        app.endUndoGroup();
    }
})();
```

---

## 📄 SOURCE FILE: `skills/after-effects/rules/rendering.md` (verbatim)

# Rendering & Render Queue

> **Loaded when:** the task involves rendering, the render queue, output modules, render settings, output paths, or render templates in After Effects via ExtendScript.

All code in this file is ES3-compatible ExtendScript. See `extendscript-fundamentals.md` for baseline syntax rules.

---

## Adding a Composition to the Render Queue

```jsx
// items.add(comp) returns a RenderQueueItem
var rqItem = app.project.renderQueue.items.add(comp);
```

The composition must be a valid `CompItem`. The new item is appended to the end of the render queue with a status of `RQItemStatus.QUEUED`.

```jsx
// Full pattern: validate comp, then add to queue
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    writeResult({ error: "No active composition" });
    return;
}
var rqItem = app.project.renderQueue.items.add(comp);
```

---

## Output Modules

Each render queue item has at least one output module. Access it with a 1-based index.

### Accessing the Default Output Module

```jsx
// outputModule(1) — first (default) output module, 1-based
var om = rqItem.outputModule(1);
```

### Adding Additional Output Modules

```jsx
// outputModules.add() appends a new output module to the item
var om2 = rqItem.outputModules.add();
```

This is useful for rendering multiple formats or to multiple destinations from a single queue item.

---

## Setting the Output File Path

```jsx
// om.file accepts a File object — path MUST include the file extension
om.file = new File("/path/to/output.mov");
```

```jsx
// Dynamic path using comp name
var outputPath = Folder.desktop.fsName + "/" + comp.name + ".mov";
om.file = new File(outputPath);
```

```jsx
// Windows-style paths work with forward slashes
om.file = new File("C:/Renders/project_output.mp4");
```

---

## Applying Templates

### Output Module Templates

Output module templates control the format, codec, channels, and encoding settings.

```jsx
// Apply a named output module template
om.applyTemplate(templateName);
```

```jsx
// Common built-in template names (vary by AE version and installed codecs)
om.applyTemplate("Lossless");
om.applyTemplate("Lossless with Alpha");
om.applyTemplate("H.264");
om.applyTemplate("TIFF Sequence with Alpha");
```

### Render Settings Templates

Render settings templates control resolution, frame rate, time span, and quality.

```jsx
// Apply a named render settings template
rqItem.applyTemplate(templateName);
```

```jsx
// Common built-in render settings template names
rqItem.applyTemplate("Best Settings");
rqItem.applyTemplate("Draft Settings");
rqItem.applyTemplate("Current Settings");
```

### Listing Available Templates

```jsx
// Output module templates — returns a JavaScript array of strings
var omTemplates = om.templates;
for (var i = 0; i < omTemplates.length; i++) {
    $.writeln("OM template: " + omTemplates[i]);
}

// Render settings templates — returns a JavaScript array of strings
var rsTemplates = rqItem.templates;
for (var i = 0; i < rsTemplates.length; i++) {
    $.writeln("RS template: " + rsTemplates[i]);
}
```

---

## Render Settings Properties

### Time Span

```jsx
// timeSpanStart — the start time of the render in seconds
rqItem.timeSpanStart = 0;

// timeSpanDuration — the total duration to render in seconds
rqItem.timeSpanDuration = 10;
```

```jsx
// Render only the first 5 seconds
rqItem.timeSpanStart = 0;
rqItem.timeSpanDuration = 5;

// Render from 2 seconds to 7 seconds
rqItem.timeSpanStart = 2;
rqItem.timeSpanDuration = 5;
```

### Skip Frames

```jsx
// skipFrames — number of frames to skip between rendered frames
// 0 = render every frame (default)
// 1 = render every other frame
// 2 = render every third frame
rqItem.skipFrames = 0;
```

---

## Starting a Render

```jsx
// render() starts rendering all QUEUED items in the render queue
// This call BLOCKS the script until all rendering is complete
app.project.renderQueue.render();
```

After `render()` returns, all items that were `QUEUED` will have updated statuses (typically `DONE`, `ERR_STOPPED`, or `USER_STOPPED`).

---

## Render Queue Item Status

The `rqItem.status` property is read-only and returns one of the `RQItemStatus` enum values.

| Status | Meaning |
|---|---|
| `RQItemStatus.QUEUED` | Ready to render |
| `RQItemStatus.RENDERING` | Currently rendering (only during a render call) |
| `RQItemStatus.DONE` | Render completed successfully |
| `RQItemStatus.UNQUEUED` | Removed from queue (will not render) |
| `RQItemStatus.NEEDS_OUTPUT` | Missing output module or output path |
| `RQItemStatus.WILL_CONTINUE` | Partially rendered, will continue on next render |
| `RQItemStatus.ERR_STOPPED` | Render stopped due to an error |
| `RQItemStatus.USER_STOPPED` | Render stopped by the user |

### Checking Status

```jsx
if (rqItem.status === RQItemStatus.QUEUED) {
    // Ready to render
}

if (rqItem.status === RQItemStatus.DONE) {
    // Finished successfully
}

if (rqItem.status === RQItemStatus.ERR_STOPPED) {
    // Render failed
}
```

---

## Inspecting the Render Queue

### Item Count

```jsx
var numItems = app.project.renderQueue.numItems;
```

### Iterating All Items (1-Based)

```jsx
var rq = app.project.renderQueue;
for (var i = 1; i <= rq.numItems; i++) {
    var item = rq.item(i);
    var compName = item.comp.name;
    var status = item.status;
}
```

### Counting Queued Items

```jsx
var queuedCount = 0;
var rq = app.project.renderQueue;
for (var i = 1; i <= rq.numItems; i++) {
    if (rq.item(i).status === RQItemStatus.QUEUED) {
        queuedCount++;
    }
}
```

---

## Removing / Unqueuing Items

Render queue items cannot be removed directly from the queue via scripting. To prevent an item from rendering, change its status to `UNQUEUED`.

```jsx
// Mark an item as unqueued so it will not render
rqItem.render = false;  // sets status to RQItemStatus.UNQUEUED
```

```jsx
// To re-queue a previously completed or unqueued item
// Only items with status UNQUEUED or DONE can be changed
rqItem.render = true;   // sets status to RQItemStatus.QUEUED
```

### Unqueue All Items

```jsx
var rq = app.project.renderQueue;
for (var i = 1; i <= rq.numItems; i++) {
    var item = rq.item(i);
    if (item.status !== RQItemStatus.RENDERING) {
        item.render = false;
    }
}
```

---

## MUST

- **MUST** verify the active item is a `CompItem` before adding it to the render queue:

```jsx
var comp = app.project.activeItem;
if (!comp || !(comp instanceof CompItem)) {
    writeResult({ error: "No active composition" });
    return;
}
```

- **MUST** include the file extension in the output path. AE uses the extension to determine the output format. Omitting it causes unpredictable behavior or errors:

```jsx
// WRONG — no extension
om.file = new File("/renders/output");

// CORRECT — includes extension
om.file = new File("/renders/output.mov");
```

- **MUST** set the output file path before rendering. A render queue item with no output path has status `RQItemStatus.NEEDS_OUTPUT` and will not render.

- **MUST** ensure at least one item in the render queue has status `RQItemStatus.QUEUED` before calling `render()`. Calling `render()` with no queued items does nothing but can cause confusion.

- **MUST** use 1-based indexing when accessing render queue items (`rq.item(1)`) and output modules (`rqItem.outputModule(1)`).

- **MUST** use ES3 syntax in all render queue scripts. No `let`, `const`, arrow functions, or template literals.

---

## FORBIDDEN

- **FORBIDDEN:** Calling `app.project.renderQueue.render()` without understanding that it blocks the entire script. No code after the `render()` call will execute until all queued items finish rendering. Do not place time-sensitive logic after `render()` expecting it to run concurrently.

```jsx
// WRONG — expecting this to run during rendering
app.project.renderQueue.render();
updateProgressUI(); // This runs AFTER render completes, not during

// CORRECT — set everything up before calling render
setupOutputPaths();
configureTemplates();
app.project.renderQueue.render();
// Now handle post-render logic
reportResults();
```

- **FORBIDDEN:** Using `alert()` in automated render scripts. It blocks the AE UI and halts the render process until dismissed. Use `writeResult()` instead.

- **FORBIDDEN:** Accessing `rqItem.outputModule(0)`. Output modules are 1-based. Index 0 does not exist and will throw an error.

- **FORBIDDEN:** Assuming template names are consistent across machines. Template availability depends on AE version, installed codecs, and user-defined presets. Always validate template names against the `templates` array or wrap `applyTemplate()` in a try/catch:

```jsx
// SAFE — wrap in try/catch in case the template does not exist
try {
    om.applyTemplate("H.264");
} catch (e) {
    // Template not available, fall back
    om.applyTemplate("Lossless");
}
```

- **FORBIDDEN:** Attempting to remove render queue items from the collection. There is no `remove()` method on render queue items. Use `rqItem.render = false` to unqueue them instead.

---

## Gotchas

- **`render()` blocks the script.** `app.project.renderQueue.render()` is synchronous and blocking. The script halts at that line until every `QUEUED` item in the render queue finishes rendering (or errors out, or the user cancels). Plan all setup -- output paths, templates, render settings -- before calling `render()`.

- **The render queue must have at least one QUEUED item.** If no items are queued, `render()` returns immediately without doing anything. Always verify at least one item has `RQItemStatus.QUEUED` before calling `render()` to avoid silent no-ops.

- **Output path must include the file extension.** AE infers the output format from the extension (`.mov`, `.avi`, `.mp4`, `.tif`, `.png`, etc.). Omitting the extension can cause the render to fail or produce an unusable file with no format association.

- **Template names are machine-specific.** The arrays returned by `om.templates` and `rqItem.templates` vary across installations. A template that exists on one machine may not exist on another. Never hard-code template names without a fallback.

- **Render queue items are 1-based.** `app.project.renderQueue.item(1)` is the first item. `app.project.renderQueue.item(0)` throws an error. Same applies to `rqItem.outputModule(1)`.

- **`rqItem.comp` is read-only.** You cannot reassign which composition a render queue item points to after creation. To change the comp, add a new render queue item and unqueue the old one.

- **Status is read-only.** You cannot set `rqItem.status` directly. Use `rqItem.render = true` to queue and `rqItem.render = false` to unqueue. The status property reflects the current state.

- **`timeSpanStart` and `timeSpanDuration` are in seconds.** These are floating-point values in seconds, not frames. Convert frames to seconds using `frameNumber / comp.frameRate`.

- **Adding output modules after applying templates.** If you add an output module with `rqItem.outputModules.add()`, it inherits default settings, not the settings of any previously configured output module. Apply templates and set paths on each output module individually.

- **Items with status `NEEDS_OUTPUT` will not render.** If you add a comp to the render queue but never assign an output path, the status remains `NEEDS_OUTPUT`. This item is silently skipped by `render()`.

---

## Complete Example: Add Active Comp to Render Queue with Template

```jsx
app.beginUndoGroup("AE Assistant: Add to render queue");
try {
    // Validate active comp
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        writeResult({ error: "No active composition" });
        return;
    }

    // Add to render queue
    var rqItem = app.project.renderQueue.items.add(comp);

    // Apply render settings template (with fallback)
    try {
        rqItem.applyTemplate("Best Settings");
    } catch (e) {
        // "Best Settings" not available, use first available template
        if (rqItem.templates.length > 0) {
            rqItem.applyTemplate(rqItem.templates[0]);
        }
    }

    // Get the default output module
    var om = rqItem.outputModule(1);

    // Apply output module template (with fallback)
    try {
        om.applyTemplate("Lossless");
    } catch (e) {
        // "Lossless" not available, use first available template
        if (om.templates.length > 0) {
            om.applyTemplate(om.templates[0]);
        }
    }

    // Set output path — desktop folder with comp name
    var outputFolder = Folder.desktop.fsName;
    var outputPath = outputFolder + "/" + comp.name + ".mov";
    om.file = new File(outputPath);

    // Verify the item is queued
    if (rqItem.status === RQItemStatus.QUEUED) {
        writeResult({
            success: true,
            message: "Added to render queue: " + comp.name,
            outputPath: outputPath
        });
    } else {
        writeResult({
            error: "Item status is " + rqItem.status + ", expected QUEUED"
        });
    }

} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## Complete Example: Batch Render Multiple Comps

```jsx
app.beginUndoGroup("AE Assistant: Batch render setup");
try {
    var outputFolder = Folder.desktop.fsName + "/Renders";
    var dir = new Folder(outputFolder);
    if (!dir.exists) {
        dir.create();
    }

    var compsAdded = [];

    // Find all compositions in the project and add them to the queue
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof CompItem) {
            var rqItem = app.project.renderQueue.items.add(item);
            var om = rqItem.outputModule(1);

            // Set output path with comp name and extension
            var outputPath = outputFolder + "/" + item.name + ".mov";
            om.file = new File(outputPath);

            compsAdded.push(item.name);
        }
    }

    if (compsAdded.length === 0) {
        writeResult({ error: "No compositions found in project" });
        return;
    }

    // Start rendering — this blocks until all items are done
    app.project.renderQueue.render();

    // Check results after render completes
    var results = [];
    var rq = app.project.renderQueue;
    for (var i = rq.numItems - compsAdded.length + 1; i <= rq.numItems; i++) {
        var rqItem = rq.item(i);
        results.push({
            comp: rqItem.comp.name,
            status: rqItem.status === RQItemStatus.DONE ? "DONE" : "FAILED"
        });
    }

    writeResult({
        success: true,
        message: "Batch render complete",
        results: results
    });

} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## Complete Example: Add Comp with Multiple Output Modules

```jsx
app.beginUndoGroup("AE Assistant: Multi-output render");
try {
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        writeResult({ error: "No active composition" });
        return;
    }

    var rqItem = app.project.renderQueue.items.add(comp);
    var outputFolder = Folder.desktop.fsName;

    // First output module — video file
    var om1 = rqItem.outputModule(1);
    try {
        om1.applyTemplate("Lossless");
    } catch (e) { /* fallback to defaults */ }
    om1.file = new File(outputFolder + "/" + comp.name + ".mov");

    // Second output module — image sequence
    var om2 = rqItem.outputModules.add();
    try {
        om2.applyTemplate("TIFF Sequence with Alpha");
    } catch (e) { /* fallback to defaults */ }
    om2.file = new File(outputFolder + "/" + comp.name + "_[#####].tif");

    writeResult({
        success: true,
        message: "Added " + comp.name + " with 2 output modules",
        outputs: [
            outputFolder + "/" + comp.name + ".mov",
            outputFolder + "/" + comp.name + "_[#####].tif"
        ]
    });

} catch (e) {
    writeResult({ error: e.toString(), line: e.line });
} finally {
    app.endUndoGroup();
}
```

---

## 📄 SOURCE FILE: `skills/after-effects/references/ae-api-versions.md` (verbatim)

# After Effects API Versions Reference

Mapping of After Effects versions to marketing names, years, API capabilities,
and scripting execution methods.

---

## Version-to-Year Mapping

| `app.version` Major | Marketing Name           | Year |
| -------------------- | ------------------------ | ---- |
| 16.x                 | After Effects CC 2019    | 2019 |
| 17.x                 | After Effects 2020       | 2020 |
| 18.x                 | After Effects 2021       | 2021 |
| 22.x                 | After Effects 2022       | 2022 |
| 23.x                 | After Effects 2023       | 2023 |
| 24.x                 | After Effects 2024       | 2024 |
| 25.x                 | After Effects 2025       | 2025 |

> **Note:** Versions 19, 20, and 21 were skipped. Adobe jumped directly from
> 18.x (2021) to 22.x (2022) to align the major version number with the
> calendar year.

---

## Version Detection Code

Use the following snippet in any ExtendScript context to determine the running
major version:

```jsx
var major = parseInt(app.version.split(".")[0], 10);
```

Example conditional usage:

```jsx
var major = parseInt(app.version.split(".")[0], 10);

if (major >= 24) {
    // AE 2024+ specific logic
} else if (major >= 22) {
    // AE 2022-2023 specific logic
} else {
    // AE 2021 and earlier
}
```

---

## Notable Scripting Additions by Version

### 17.x - After Effects 2020

- **JavaScript expression engine** introduced as an alternative to the legacy
  ExtendScript expression engine. Expressions can now run in a modern JS
  runtime, significantly improving evaluation performance.
- The legacy ExtendScript engine remains available and is the default for
  existing projects.

### 22.x - After Effects 2022

- **Multi-frame rendering API** - scripting hooks and awareness for the new
  multi-frame rendering pipeline. Scripts must account for thread-safety
  considerations when MFR is enabled.
- **`layer.id` property** - each layer now exposes a persistent unique `id`
  property that survives layer reordering, renaming, and duplication. This is
  the preferred way to reference layers programmatically instead of by index
  or name.

### 23.x - After Effects 2023

- **Properties panel scripting improvements** - enhanced access to the
  Properties panel, improving the ability to read and manipulate property
  groups and individual properties through scripts.

### 24.x - After Effects 2024

- **Layer tagging / labeling improvements** - expanded scripting control over
  layer labels and organizational tags, enabling better automated project
  organization workflows.
- **Text layer per-character 3D** - scripting support for per-character 3D
  transformations on text layers, allowing programmatic control of individual
  character positioning in 3D space.

### 25.x - After Effects 2025

- **Enhanced scripting for Motion Graphics templates** - improved API surface
  for creating, modifying, and exporting Motion Graphics templates (MOGRTs)
  via script, enabling more robust template automation pipelines.

---

## Execution Method by Version

### All Versions: AppleScript `DoScriptFile`

The traditional method for executing ExtendScript from an external process on
macOS:

```applescript
tell application "Adobe After Effects 2024"
    DoScriptFile "/path/to/script.jsx"
end tell
```

This works reliably through AE 2023 (23.x).

### 24.x and Later: JXA (`osascript -l JavaScript`)

Starting with After Effects 2024 (24.x), the AppleScript `DoScriptFile`
command became **unreliable**. The recommended approach for 24.x+ is to use
JavaScript for Automation (JXA) instead:

```bash
osascript -l JavaScript -e '
  var ae = Application("Adobe After Effects 2025");
  ae.doscriptfile("/path/to/script.jsx");
'
```

#### Choosing the Right Method

| AE Version | Recommended Method          | Notes                              |
| ---------- | --------------------------- | ---------------------------------- |
| 16.x-23.x  | AppleScript `DoScriptFile`  | Stable and well-tested             |
| 24.x+      | JXA via `osascript -l JavaScript` | AppleScript method is unreliable |

#### Version-Adaptive Execution Pattern

When building tools that must support multiple AE versions, detect the version
first and dispatch accordingly:

```bash
# Pseudocode for adaptive execution
ae_version=$(get_ae_major_version)
if [ "$ae_version" -ge 24 ]; then
    osascript -l JavaScript -e "Application('Adobe After Effects ...').doscriptfile('$script')"
else
    osascript -e "tell application \"Adobe After Effects ...\" to DoScriptFile \"$script\""
fi
```

---

## TODO

- TODO: Full command ID mapping per version
- TODO: Complete matchName changes between versions
- TODO: Deprecated APIs per version
- TODO: Document `app.executeCommand()` ID differences across versions
- TODO: Map `PropertyType` and `PropertyValueType` enum availability per version
- TODO: Document Windows execution methods (COM automation) per version
