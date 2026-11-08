# dylantarre/animation-principles — Animation Principles (After Effects tool sheet)
- Repo: dylantarre/animation-principles
- Link: https://github.com/dylantarre/animation-principles
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 142 stars, 17 forks, only 2 commits, ~859 catalog installs (repo page, 2026-11-06)
- Last commit (from local clone git log): 2025-12-30
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: The repo is a 144-skill animation-principles catalog (Disney 12 principles organised by tool/framework); extracted here is ONLY the After Effects sheet — skills/09-by-tool-framework/after-effects/SKILL.md — which converts the 12 principles into AE frame counts: timing table (2–4 frames snappy … 40+ dramatic), anticipation ranges (0–10 / 10–12 / 12–30 / 30–40 frames), exaggeration +20–50%. The other 143 skills are for other tools/frameworks, out of this round's scope.

---

## 📄 SOURCE FILE: `skills/09-by-tool-framework/after-effects/SKILL.md` (verbatim)

---
name: after-effects
description: Use when implementing Disney's 12 animation principles in Adobe After Effects
---

# After Effects Animation Principles

Implement all 12 Disney animation principles using After Effects' powerful animation tools.

## 1. Squash and Stretch

```javascript
// Expression for automatic squash/stretch
s = transform.scale[1];
x = 100 + (100 - s) * 0.5;
[x, s]
```

Or manually:
- Keyframe Scale X and Y inversely
- When Y compresses, X expands
- Maintain volume (X * Y ≈ constant)

## 2. Anticipation

Timeline structure:
- **0-10f**: Wind-up (crouch, pull back)
- **10-12f**: Transition
- **12-30f**: Main action
- **30-40f**: Settle

Use Easy Ease on anticipation keyframes for smooth wind-up.

## 3. Staging

Techniques:
- Use depth of field (Camera > Depth of Field)
- Apply blur to background layers
- Use vignettes to direct focus
- Adjust opacity of secondary elements
- Light the main subject brighter

## 4. Straight Ahead / Pose to Pose

**Pose to Pose (recommended):**
1. Set keyframes at key poses
2. Fill in breakdowns
3. Use Graph Editor to adjust timing

**Straight Ahead:**
- Animate frame-by-frame
- Use Onion Skin (Layer > Onion Skin)

## 5. Follow Through and Overlapping Action

```javascript
// Delay expression for child layers
thisComp.layer("Parent").transform.position.valueAtTime(time - 0.05)
```

Or:
- Offset child keyframes by 2-5 frames
- Use parenting with delayed wiggle
- Apply spring expression to end values

## 6. Slow In and Slow Out

- Select keyframes > F9 (Easy Ease)
- Graph Editor > Adjust bezier handles
- Steeper curve = faster movement
- Flatter curve = slower movement

```javascript
// Custom ease expression
ease(time, inPoint, outPoint, startValue, endValue)
```

## 7. Arc

Techniques:
- Draw motion path with Pen tool
- Use Position property's bezier handles
- Layer > Transform > Auto-Orient
- Apply path from shape layer to position

## 8. Secondary Action

- Animate main action first
- Add secondary on separate layer/property
- Offset timing slightly
- Secondary should complement, not compete

Example: Character waves → Hair follows → Clothing shifts

## 9. Timing

| Frames | Feel |
|--------|------|
| 2-4 | Snappy, instant |
| 6-8 | Quick, energetic |
| 12-15 | Normal pace |
| 20-30 | Slow, heavy |
| 40+ | Dramatic, weighted |

Adjust composition frame rate for overall feel (24fps cinematic, 30fps smooth).

## 10. Exaggeration

```javascript
// Overshoot expression
amp = 15;
freq = 3;
decay = 5;
t = time - key(numKeys).time;
if (t > 0) {
  value + amp * Math.sin(t * freq * Math.PI * 2) / Math.exp(t * decay);
} else {
  value;
}
```

Push values 20-50% beyond realistic:
- Larger scales
- Wider rotations
- More dramatic timing

## 11. Solid Drawing

- Use 3D layers for depth
- Apply cameras with perspective
- Animate Z position
- Use light and shadow
- Consider volume in all poses

## 12. Appeal

Design principles:
- Clear silhouettes at every pose
- Smooth curves over sharp angles
- Consistent character proportions
- Pleasing timing patterns
- Clean, readable motion paths

## Essential Expressions

```javascript
// Wiggle
wiggle(frequency, amplitude)

// Loop
loopOut("cycle")

// Time remap
timeRemap = linear(time, 0, duration, 0, 1)

// Bounce
n = 0;
if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) n--;
}
if (n == 0) t = 0;
else t = time - key(n).time;
amp = 80; freq = 3; decay = 8;
value + amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
```

## Export Options

- **Lottie**: Bodymovin plugin → JSON
- **GIF**: Media Encoder
- **Video**: H.264, ProRes
- **Sprite Sheet**: Scripts > Render Sprite Sheet
