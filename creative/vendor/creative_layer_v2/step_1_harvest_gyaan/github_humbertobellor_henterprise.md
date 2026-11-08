# Harvest — humbertobellor/henterprise (youtube-producer + video-content skills)

- **Repo:** humbertobellor/henterprise — a virtual agentic organization (16 departments, 143 skills) ported from cbrock84/headcount to Hermes Agent
- **Link:** https://github.com/humbertobellor/henterprise
- **Licence:** MIT License (MIT) — verified on repo page; LICENSE file present (© 2026 Chris Brock)
- **What it is (relevant part):** Two marketing-department skills by Chris Brock. `youtube-producer` = long-form YouTube: packaging-first, first-30-seconds rule, retention structure (seams/transitions), editing direction rules, and a retention-curve diagnosis order. `video-content` = short-form + long-form scripting/packaging companion with the same retention diagnosis. Principle-heavy rather than number-heavy, but the rules are sharp and directly convertible.
- **Activity:** Created 2026-09-09; 25 commits, 1 release/tag; latest commit on default branch 2026-10-27 (from clone HEAD `01d625e`) — recent and active.
- **Files extracted (full, verbatim):** `marketing/youtube-producer/SKILL.md`, `marketing/video-content/SKILL.md`

---


---

## Source file: `marketing/youtube-producer/SKILL.md`

---
name: youtube-producer
description: "Plans, packages, and scripts long-form video. Idea selection, titles and thumbnails, script structure, editing direction, and diagnosing why a video or channel underperforms. Use this for video ideas, packaging, scripting, a retention teardown, or channel strategy - including when someone describes a topic and wants it turned into something publishable. For short-form and cross-platform video, use video-content."
version: 1.0.0
author: Chris Brock (cbrock84), ported to Hermes Agent by Humberto Bello
license: MIT
platforms: [linux, macos, windows]
category: marketing
metadata:
  hermes:
    category: marketing
    tags: [marketing, youtube, long-form-video, retention, editing]
    related_skills: [video-content, visual-content, content-strategy, chief-content-officer]
---

# YouTube producer

Long-form video: idea selection, packaging, script structure, editing direction, and diagnosis. For
short-form and cross-platform video, use `enterprise/marketing/video-content`.

## When to Use

- Generating or selecting video ideas.
- Packaging — titles and thumbnails.
- Scripting.
- A retention teardown.
- Channel strategy, including turning a described topic into something publishable.

## Procedure

### Package before you produce

Title and thumbnail decide whether a video is watched at all. Design them first, as a test of the
idea: if you cannot package it compellingly, the idea is weak and you have found that out before
spending a week filming.

**Titles.** Specific over clever. Front-load the distinguishing word — titles truncate, and the
distinguishing word is usually last in a natural sentence. Curiosity only where the video genuinely
resolves it; unresolved curiosity trains people not to click next time.

**Thumbnails.** One subject, readable at phone-thumbnail size. High contrast, minimal text, real
faces outperform objects for most channels. Title and thumbnail must not say the same thing —
together they should say more than either alone.

Make three packaging options per idea and pick the one that would make *you* click while scrolling
past something else.

### Idea selection

The best ideas sit where audience demand, your unusual knowledge, and a packageable hook overlap.
Missing any one produces a predictable failure: no demand means nobody searches, no unusual
knowledge means it is generic, no hook means nobody clicks.

Check what already exists on the topic. Not to avoid it — a crowded topic proves demand — but to
find the angle nobody took.

### The first thirty seconds

Deliver the promise immediately. No channel intro, no "before we get started," no restating the
title. Show the outcome, state the surprising conclusion, or drop the viewer mid-action.

Then briefly say what the video covers, so the viewer knows the shape of the commitment they are
making.

### Retention structure

Retention is lost at seams, not in the middle of sections. Every transition needs an explicit reason
to continue — an open question, a promised payoff, a stated next step.

- **Chapter it.** Each section should work standalone and end pointing forward.
- **Vary pace deliberately.** A uniformly intense video is as tiring as a flat one.
- **Front-load value.** Withholding the good part until the end optimizes for a viewer who is no
  longer watching.
- **Place sponsor reads after the first payoff**, never before it.

### Visual direction and editing

Retention is as much editing as writing. The script sets what is said; the edit sets whether it is
watched.

- **Cut on the beat of meaning**, not on a timer. Rhythmic cutting for its own sake reads as noise.
- **Show, then say.** Where footage can carry the point, let it, and cut the sentence explaining it.
- **B-roll earns its place** by showing something the words cannot. Decorative b-roll is dead air
  with pictures.
- **Text on screen for anything numeric or named.** Viewers do not retain spoken numbers.
- **Remove every pause, restart, and filler word** in the first thirty seconds without exception.
  Later in the video, some breathing room is worth keeping — an unrelentingly tight edit is
  exhausting.
- **Change something visually** at each chapter transition. Transitions are where viewers leave, and
  a visual change is a cheap reason to stay.

Write editing notes into the script as you go — the shot, the on-screen text, the moment to cut
away. Deciding this in the edit costs far more time than deciding it while writing.

### Channel level

Consistency of promise matters more than consistency of schedule. A channel whose videos deliver
different kinds of value teaches the audience nothing about whether to click the next one.

Plan repurposing before filming — segments meant to stand alone as short-form get shot to stand
alone.

## Pitfalls

- Filming before packaging. The packaging is the test of the idea.
- Curiosity the video does not resolve.
- A thumbnail and title saying the same thing.
- Withholding the good part until the end, which optimizes for a viewer who has left.
- A sponsor read before the first payoff.
- Decorative b-roll — dead air with pictures.
- Deciding editing direction in the edit rather than while writing.
- Consistency of schedule without consistency of promise.

## Verification

Diagnose against the analytics, in this order:

- **Low click-through** — packaging. Title and thumbnail, not content.
- **High click-through, immediate drop** — the opening did not pay the promise, or the promise was
  unpayable.
- **Gradual decline** — normal. Judge the slope against your own baseline, not against absolutes.
- **A sharp cliff mid-video** — find the timestamp and watch it. Almost always a transition, a
  tangent, or a badly placed sponsor read.
- **Good retention, no growth** — the videos work but the packaging is not earning impressions, or
  the topics have no audience beyond existing subscribers.

## Related

- `enterprise/marketing/video-content` — short-form and cross-platform.
- `enterprise/marketing/visual-content` — thumbnail craft.
- `enterprise/marketing/content-strategy` — whether long-form video is the right format commitment.


---

## Source file: `marketing/video-content/SKILL.md`

---
name: video-content
description: "Plans and scripts video, and designs the packaging. Short-form and long-form, plus the titles, thumbnails, and openings that determine whether it gets watched. Use this to script a video, plan a series, fix retention or click-through problems, design thumbnail and title concepts, or turn written content into video."
version: 1.0.0
author: Chris Brock (cbrock84), ported to Hermes Agent by Humberto Bello
license: MIT
platforms: [linux, macos, windows]
category: marketing
metadata:
  hermes:
    category: marketing
    tags: [marketing, video, packaging, retention, short-form]
    related_skills: [youtube-producer, visual-content, content-strategy, chief-content-officer]
---

# Video content

Short-form and long-form video, and the packaging that decides whether either is watched. For
long-form channel strategy in depth, use `enterprise/marketing/youtube-producer`.

## When to Use

- Scripting a video.
- Planning a series.
- Fixing retention or click-through problems.
- Designing thumbnail and title concepts.
- Turning written content into video.

## Procedure

### Packaging is most of the outcome

A video nobody clicks has no retention curve. Title and thumbnail are not promotion of the video —
they are the promise the video must keep, and they should be designed before it is made. If you
cannot package it compellingly, the idea is weak; find that out before filming.

**Titles** — specific over clever. Curiosity that a real answer resolves, not a withheld one.
Front-load the distinguishing word, since titles truncate.

**Thumbnails** — one subject, readable at thumbnail size on a phone. High contrast. Text under about
four words, or none. Thumbnail and title must not say the same thing; together they should say more
than either alone.

### Openings

The first fifteen seconds decide the rest. Deliver the promise immediately — no channel intro, no
"before we get started," no restating the title.

Best openings show the outcome, state the surprising conclusion, or drop the viewer mid-action. Then
say what the video will cover, briefly, so they know the shape of the commitment.

### Structure by length

**Short-form** — one idea, opening frame that reads as motion, and a payoff before attention decays.
No setup. The loop matters: end where the beginning makes sense again.

**Long-form** — chapters that each work standalone, with an explicit reason to continue at every
seam. Retention is lost at transitions, not in the middle of sections. Vary pace deliberately; a
uniformly intense video is as tiring as a flat one.

### Repurposing

Plan derivatives before filming, not after. Segments intended to stand alone get shot to stand
alone. Extracting short-form from a video not built for it produces clips that need context they do
not have.

## Pitfalls

- Making the video before the packaging. If it cannot be packaged, the idea is weak.
- Curiosity the video does not resolve, which trains people not to click next time.
- A thumbnail that says the same thing as the title.
- Channel intros, "before we get started," and restating the title in the opening.
- A uniformly intense edit, which is as tiring as a flat one.
- Cutting short-form out of a video that was not built for it.

## Verification

Diagnose against the retention curve, not against impressions:

- **Low click-through** — packaging problem. Title and thumbnail, not content.
- **High click-through, early drop** — the opening did not pay the promise. Or the promise was
  unpayable.
- **Steady mid-video decline** — normal. Look at the slope against your own baseline, not absolutes.
- **Sharp mid-video cliff** — find the timestamp and watch it. It is almost always a transition, a
  tangent, or a sponsor read placed badly.

## Related

- `enterprise/marketing/youtube-producer` — long-form channel strategy and editing depth.
- `enterprise/marketing/visual-content` — thumbnail design.
- `enterprise/marketing/chief-content-officer` — where derivatives are planned at brief time.
