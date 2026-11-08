# chvndler/aeft.jsx — After Effects expressions & scripts library
- Repo: chvndler/aeft.jsx
- Link: https://github.com/chvndler/aeft.jsx
- Licence: MIT License (MIT) — LICENSE file in clone is the MIT text (verified in clone; GitHub metadata also says MIT). ⚠️ Internal inconsistency in the source: the README's licence line says "ISC (see LICENSE)" although the LICENSE it points to is MIT — recorded here so the mismatch is not hidden; the operative LICENSE file is MIT, so the repo qualifies under the MIT/Apache bar.
- Popularity: 4 stars (repo page, 2026-11-06); created 2021-12-16
- Last commit (from local clone git log): 2026-07-27
- Extracted: 2026-11-06, Editor-specific harvest round Part 1 (After Effects + Premiere Pro) — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Extracted: README.md + src/expressions/README.md (the intent-wise map) + every expression snippet under src/expressions/ (velocity-driven decay controllers, expo-ease between keys, typewriter, counters, date/time, layout spacing, layer-effect color). Expressions are copy-paste craft snippets — the technique content of this repo. NOT extracted: src/scripts/ ScriptUI utility panels and src/lib/aequery.js (a general ExtendScript query library — machinery), listed here by name only.

---

## 📄 SOURCE FILE: `README.md` (verbatim)

# aeft.jsx

Public repository of Adobe After Effects expressions and scripts.

## Overview

This project keeps AE snippets organized like a lightweight codebase:

- `src/expressions` for copy/paste expressions
- `src/scripts` for full ScriptUI or utility scripts
- `src/lib` for shared script helpers and templates

The expressions folder is now organized by intent, and each file contains one snippet for easier discovery.

## Project Structure

```text
src/
├── expressions/
│   ├── README.md
│   ├── color/
│   ├── controllers/
│   │   └── velocity-driven/
│   ├── counters/
│   ├── datetime/
│   ├── keyframes/
│   ├── layout/
│   └── text/
├── lib/
└── scripts/
    └── composition/
```

## Usage

### Expressions

1. Open a file from `src/expressions`.
2. Copy its contents.
3. Paste into an After Effects expression field.
4. Adjust layer/control names called out in comments.

### Scripts

- Run `.jsx` scripts from `File > Scripts > Run Script File...`
- Or place them in your After Effects Scripts directory.

## Formatting

- Run `yarn pretty` to format all `.js`/`.jsx` source files with Prettier.

## License

ISC (see `LICENSE`).

---

## 📄 SOURCE FILE: `src/expressions/README.md` (verbatim)

# Expressions Index

Expression snippets are organized by intent. Each file contains a single reusable expression so copy/paste usage is straightforward.

## color

- `color/layer-effect-color.js` — reads a Color Control from a target layer.

## controllers/velocity-driven

- `controllers/velocity-driven/velocity-decay-basic.js` — static velocity wobble settings.
- `controllers/velocity-driven/velocity-decay-controlled.js` — velocity wobble driven by slider controls on `VELOCITY_CTRL`.

## counters

- `counters/roll-with-velocity.js` — vertical rolling number effect.
- `counters/three-digit-padding.js` — 3-digit zero padding for numeric displays.

## datetime

- `datetime/current-date-dd-mm-yyyy.js` — date format `DD/MM/YYYY`.
- `datetime/current-date-long.js` — date format `Weekday, Month Day`.
- `datetime/current-time-12h.js` — time format `h:mm AM/PM`.
- `datetime/current-time-12h-seconds.js` — time format `h:mm:ss AM/PM`.
- `datetime/current-time-24h.js` — time format `HH:mm`.
- `datetime/current-time-manual-12h.js` — manual 12-hour conversion with zero-padded minutes.

## keyframes

- `keyframes/expo-ease-between-keys-basic.js` — compact exponential in/out interpolation.
- `keyframes/expo-ease-between-keys-modular.js` — same easing behavior with helper functions for maintainability.

## layout

- `layout/menu-spacing-control.js` — automatic horizontal spacing for text rows using `sourceRectAtTime`.

## text

- `text/typewriter-basic.js` — character reveal over time (`Chars Per Second` slider).

---

## 📄 SOURCE FILE: `src/expressions/color/layer-effect-color.js` (verbatim)

// Pulls a Color Control value from a named layer/effect.
thisComp.layer("TOP_NAV_CTRL").effect("Background Color")("Color");

// Generic example:
// thisComp.layer('NULL_LAYER_NAME').effect('Effect_Name')('Color');

---

## 📄 SOURCE FILE: `src/expressions/controllers/velocity-driven/velocity-decay-basic.js` (verbatim)

// Velocity-driven damped oscillation after each keyframe.
var amp = 0.08;
var freq = 2.0;
var decay = 5.0;
var n = 0;
var timeMax = 4;

if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) {
    n--;
  }
}

var elapsed = n === 0 ? 0 : time - key(n).time;

if (n > 0 && elapsed < timeMax) {
  var velocity = velocityAtTime(key(n).time - thisComp.frameDuration / 10);
  value +
    (velocity * amp * Math.sin(freq * elapsed * 2 * Math.PI)) /
      Math.exp(decay * elapsed);
} else {
  value;
}

---

## 📄 SOURCE FILE: `src/expressions/controllers/velocity-driven/velocity-decay-controlled.js` (verbatim)

var ctrlLayer = thisComp.layer("VELOCITY_CTRL");

// VELOCITY-DRIVEN DECAY WOBBLE
// Apply to any keyframed property (Position, Scale, Rotation).
//
// Controls on VELOCITY_CTRL (slider names):
// - amp
// - freq
// - decay
// - time_max

function ctrl(name, fallback) {
  try {
    return ctrlLayer.effect(name)("Slider").value;
  } catch (e) {
    return fallback;
  }
}

var amp = ctrl("amp", 0.08);
var freq = ctrl("freq", 2.0);
var decay = ctrl("decay", 5.0);
var timeMax = ctrl("time_max", 2.0);

var n = 0;
if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) {
    n--;
  }
}

var elapsed = n === 0 ? 0 : time - key(n).time;

if (n > 0 && elapsed < timeMax) {
  var velocity = velocityAtTime(key(n).time - thisComp.frameDuration / 10);
  value +
    (velocity * amp * Math.sin(freq * elapsed * 2 * Math.PI)) /
      Math.exp(decay * elapsed);
} else {
  value;
}

---

## 📄 SOURCE FILE: `src/expressions/counters/roll-with-velocity.js` (verbatim)

// Vertical rolling counter driven by slider delta per frame.
var slider = effect("Number")("Slider");
var current = slider.value;
var previous = slider.valueAtTime(time - thisComp.frameDuration);
var offset =
  (previous - current) *
  (thisComp.height * 0.5 - ((time * 10000) % thisComp.height));

[0, offset];

---

## 📄 SOURCE FILE: `src/expressions/counters/three-digit-padding.js` (verbatim)

// Forces a slider value to render with 3 leading zeroes.
var digits = effect("Slider Control")("Slider").value.toFixed(0);
(digits.length < 3 ? (digits.length < 2 ? "00" : "0") : "") + digits;

---

## 📄 SOURCE FILE: `src/expressions/datetime/current-date-dd-mm-yyyy.js` (verbatim)

// Render current date as DD/MM/YYYY.
var now = new Date();
now.getDate() + "/" + (now.getMonth() + 1) + "/" + now.getFullYear();

---

## 📄 SOURCE FILE: `src/expressions/datetime/current-date-long.js` (verbatim)

// Render current date as: Thursday, December 21.
var now = new Date();
now.toLocaleDateString("en-US", {
  weekday: "long",
  month: "long",
  day: "numeric",
});

---

## 📄 SOURCE FILE: `src/expressions/datetime/current-time-12h-seconds.js` (verbatim)

// Render current time as: 12:00:00 PM.
var now = new Date();
now.toLocaleTimeString("en-US", {
  hour: "numeric",
  minute: "2-digit",
  second: "2-digit",
});

---

## 📄 SOURCE FILE: `src/expressions/datetime/current-time-12h.js` (verbatim)

// Render current time as: 12:00 PM.
var now = new Date();
now.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });

---

## 📄 SOURCE FILE: `src/expressions/datetime/current-time-24h.js` (verbatim)

// Render current time as: 12:00.
var now = new Date();
now.toLocaleTimeString("en-US", {
  hour: "numeric",
  minute: "2-digit",
  hour12: false,
});

---

## 📄 SOURCE FILE: `src/expressions/datetime/current-time-manual-12h.js` (verbatim)

// Render current time manually as X:MM (12h clock, no AM/PM).
var now = new Date();
var hours = now.getHours();
var minutes = now.getMinutes();
var minutePadded = minutes < 10 ? "0" + minutes : "" + minutes;

if (hours > 12) {
  hours -= 12;
} else if (hours === 0) {
  hours = 12;
}

hours + ":" + minutePadded;

---

## 📄 SOURCE FILE: `src/expressions/keyframes/expo-ease-between-keys-basic.js` (verbatim)

/**
 * Exponential ease between surrounding keyframes.
 * Works on 1D/2D/3D properties.
 */

function keyflowInOut(t, b, c, d) {
  var correction = 0.000976563;
  var eased;

  if ((t /= d / 2) < 1) {
    eased = Math.pow(2, 10 * (t - 1)) - correction;
  } else {
    eased = -Math.pow(2, -10 * (t - 1)) + 2 + correction;
  }

  return b + (eased / 2) * c;
}

function keyEase() {
  var n = 0;
  if (numKeys > 0) {
    n = nearestKey(time).index;
    if (key(n).time > time) {
      n--;
    }
  }

  var key1;
  var key2;
  try {
    key1 = key(n);
    key2 = key(n + 1);
  } catch (e) {
    return null;
  }

  var dim = 1;
  try {
    key(1)[1];
    dim = 2;
    key(1)[2];
    dim = 3;
  } catch (e2) {}

  var localT = time - key1.time;
  var duration = key2.time - key1.time;

  var startX = key1[0];
  var changeX = key2[0] - key1[0];

  var startY;
  var changeY;
  var startZ;
  var changeZ;

  if (dim >= 2) {
    startY = key1[1];
    changeY = key2[1] - key1[1];

    if (dim >= 3) {
      startZ = key1[2];
      changeZ = key2[2] - key1[2];
    }
  }

  if (time < key1.time || time > key2.time) {
    return value;
  }

  var value1 = keyflowInOut(localT, startX, changeX, duration);
  if (dim === 1) {
    return value1;
  }

  var value2 = keyflowInOut(localT, startY, changeY, duration);
  if (dim === 2) {
    return [value1, value2];
  }

  var value3 = keyflowInOut(localT, startZ, changeZ, duration);
  return [value1, value2, value3];
}

keyEase() || value;

---

## 📄 SOURCE FILE: `src/expressions/keyframes/expo-ease-between-keys-modular.js` (verbatim)

/**
 * Exponential ease between surrounding keyframes.
 * Modular variant with dedicated helper functions.
 */

function easeInOutExpo(t, b, c, d) {
  var correction = 1 / 1024;
  var eased;

  if (d === 0) {
    return b;
  }

  t /= d / 2;
  if (t < 1) {
    eased = Math.pow(2, 10 * (t - 1)) - correction;
  } else {
    eased = -Math.pow(2, -10 * (t - 1)) + 2 + correction;
  }

  return b + eased * 0.5 * c;
}

function getDimFromKey(prop) {
  try {
    prop.key(1)[2];
    return 3;
  } catch (e3) {
    try {
      prop.key(1)[1];
      return 2;
    } catch (e2) {
      return 1;
    }
  }
}

function currentKeySegment(prop, currentTime) {
  if (prop.numKeys < 2) {
    return null;
  }

  var n = prop.nearestKey(currentTime).index;
  if (prop.key(n).time > currentTime) {
    n--;
  }

  if (n < 1 || n >= prop.numKeys) {
    return null;
  }

  return { k1: prop.key(n), k2: prop.key(n + 1) };
}

function easeBetweenKeysExpo(prop, currentTime) {
  var seg = currentKeySegment(prop, currentTime);
  if (!seg) {
    return null;
  }

  var k1 = seg.k1;
  var k2 = seg.k2;
  if (currentTime < k1.time || currentTime > k2.time) {
    return null;
  }

  var localT = currentTime - k1.time;
  var duration = k2.time - k1.time;
  var dim = getDimFromKey(prop);

  if (dim === 1) {
    var start = k1[0];
    var change = k2[0] - k1[0];
    return easeInOutExpo(localT, start, change, duration);
  }

  if (dim === 2) {
    var startX = k1[0];
    var changeX = k2[0] - k1[0];
    var startY = k1[1];
    var changeY = k2[1] - k1[1];
    return [
      easeInOutExpo(localT, startX, changeX, duration),
      easeInOutExpo(localT, startY, changeY, duration),
    ];
  }

  var sx = k1[0];
  var cx = k2[0] - k1[0];
  var sy = k1[1];
  var cy = k2[1] - k1[1];
  var sz = k1[2];
  var cz = k2[2] - k1[2];
  return [
    easeInOutExpo(localT, sx, cx, duration),
    easeInOutExpo(localT, sy, cy, duration),
    easeInOutExpo(localT, sz, cz, duration),
  ];
}

easeBetweenKeysExpo(thisProperty, time) || value;

---

## 📄 SOURCE FILE: `src/expressions/layout/menu-spacing-control.js` (verbatim)

// X Position expression:
// Equal gaps using the right edge of the previous text layer.
// Requires a "Spacing" slider on layer "MENU_CTRL".
// Assumes the row starts at layer 1 and text layers are consecutive.

var gap = thisComp.layer("MENU_CTRL").effect("Spacing")("Slider");
var first = thisComp.layer(1);

function widthScaled(layer) {
  var rect = layer.sourceRectAtTime(time, false);
  return rect.width * (layer.transform.scale[0] / 100);
}

function centerOffset(layer) {
  var rect = layer.sourceRectAtTime(time, false);
  return (-rect.left + rect.width / 2) * (layer.transform.scale[0] / 100);
}

function rightOffset(layer) {
  var rect = layer.sourceRectAtTime(time, false);
  return (-rect.left + rect.width) * (layer.transform.scale[0] / 100);
}

var firstLeft = first.transform.xPosition - centerOffset(first);
var firstRight = first.transform.xPosition + rightOffset(first);

if (index === first.index) {
  firstLeft + centerOffset(thisLayer);
} else {
  var totalPrev = 0;
  for (var i = first.index + 1; i < index; i++) {
    totalPrev += widthScaled(thisComp.layer(i));
  }

  var left = firstRight + totalPrev + (index - first.index) * gap;
  left + centerOffset(thisLayer);
}

---

## 📄 SOURCE FILE: `src/expressions/text/typewriter-basic.js` (verbatim)

// Source Text expression:
// Reveals characters over time using a slider.
var charsPerSecond = effect("Chars Per Second")("Slider");
var count = Math.max(0, Math.floor(time * charsPerSecond));
value.substr(0, count);
