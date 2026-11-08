# Jakeschincariol/youtube-agent-skill — YouTube Agent Skill (11 skills)
- Repo: Jakeschincariol/youtube-agent-skill
- Link: https://github.com/Jakeschincariol/youtube-agent-skill
- Licence: MIT License (MIT) — verified on repo page + LICENSE file in clone
- Popularity: 4,664 stars, 1,420 forks (repo page, 2026-11-05)
- Last commit (from local clone git log): 2026-09-16
- Extracted: 2026-11-05, Round 2 harvest — clone --depth 1, technique files verbatim below (numbers/thresholds/checklists intact).
- Notes: Established maker pack (same author's linkedin-agent-skill family). 11 skills: yt-script (21 hook formulas in hooks.json + hookscore.py 5-property scorer calibrated on 74 real hooks), yt-package (title/thumbnail linter), yt-edit (deadair.py edit decision list), yt-retention (retention.py curve reader), yt-viral (swipe.py outlier ranking), yt-shorts, yt-seo, yt-chapters (chapters.py), yt-plan, yt-comment, yt-audit. ALL files under skills/ included verbatim, including the Python tools because their thresholds ARE the technique.


---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-audit/SKILL.md ===== -->

---
name: yt-audit
description: >-
  Audit a YouTube channel end to end - packaging, consistency, the first
  fifteen seconds, and what to fix first. Use for "audit my channel", "why
  isn't my channel growing", "review my videos", or a pasted channel URL.
---

# yt-audit

An audit that lists twenty problems is a way of avoiding the one that matters. This ends in ONE fix.

## Before you write

1. Read `~/.claude/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## What to look at, in this order

1. **The last ten titles, as a set.** Read them as a list, the way the channel page shows them. Do
   they promise different things? Run them through `../yt-package/title.py`. A channel where every
   title is the same shape has a format problem, not a title problem.
2. **The thumbnails, at feed size.** Shrink them. What survives? If three of them are unreadable at
   that size, that is the fix and nothing else matters yet.
3. **The first fifteen seconds of the three most recent.** Transcribe them and score with
   `../yt-script/hookscore.py`. This is where most channels lose.
4. **Upload rhythm.** Not frequency - CONSISTENCY. Six videos in one week and then nothing for a
   month is worse than one a fortnight forever.
5. **The retention shape**, if they can export it. `/yt-retention`.

## What to hand back

- The single biggest fix, named, with what to do this week.
- Three things that are already working, so they do not break them. Be specific; "your energy is
  good" is not an observation.
- What NOT to do yet, and why.

Never open an audit with praise you do not mean, and never end one with a list of twenty things.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-chapters/SKILL.md ===== -->

---
name: yt-chapters
description: >-
  Write YouTube chapters from a transcript, validated against YouTube's own
  rules so they actually render. Use for "add chapters", "timestamps",
  "break this video into sections".
---

# yt-chapters

```bash
python3 chapters.py transcript.srt --target 8
```

## The rules, which are not optional

A chapter list that breaks any of these silently does not become chapters at all - the block just
sits in the description doing nothing:

- The first entry must be **00:00**.
- There must be **at least three**.
- Each must be **at least 10 seconds** long.

The tool checks all three and tells you when a list is invalid rather than letting you paste it.

## Retitle every line

`chapters.py` finds the BOUNDARIES well - it scores the pauses you actually took by how much the
vocabulary shifts across them. The titles it emits are the topic words, and they are a draft. A
chapter called "Thumbnails Titles Packaging" is a placeholder. Rewrite each one as the promise of
that section, in the user's voice, three to five words.

Chapters are also a retention diagnostic: if a section cannot be named in five words, it is two
sections or it is filler.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-chapters/chapters.py ===== -->

#!/usr/bin/env python3
"""chapters.py - YouTube chapters from a timestamped transcript.

    python3 chapters.py transcript.srt            # or .vtt / whisper .json
    python3 chapters.py transcript.srt --target 8 --json

Prints a description block you can paste straight under a video. YouTube's own rules, enforced here
rather than assumed: the list must start at 00:00, needs at least three entries, and each chapter
must be at least 10 seconds long. A block that breaks any of those silently does not become
chapters, which is why this checks instead of trusting.

Boundaries come from the gaps - the pauses you actually took between sections - scored by how long
the pause was and how much the vocabulary changes across it. It is a first draft you retitle, not a
summariser.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
from deadair import load, parse_ts  # noqa: E402  (same parser, one implementation)

STOP = set("the a an of for to in on and or is are was were be been with this that it as at by from "
           "you your i my we our they them he she but so if then than there here what which who how "
           "when where why not no yes do does did just really very like about into over out up down "
           "can could will would should have has had get got make made go going went one two".split())

def keywords(text):
    return {w for w in re.findall(r"[a-z']{4,}", text.lower()) if w not in STOP}

def mmss(t):
    t = int(t); h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    target = int(a[a.index("--target") + 1]) if "--target" in a else 7
    a = [x for x in a if not x.startswith("--") and not x.isdigit()]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if len(cues) < 6: print("too few cues to chapter"); sys.exit(1)
    dur = cues[-1][1]
    cand = []
    for i in range(1, len(cues)):
        gap = cues[i][0] - cues[i - 1][1]
        before = " ".join(c[2] for c in cues[max(0, i - 12):i])
        after = " ".join(c[2] for c in cues[i:i + 12])
        kb, ka = keywords(before), keywords(after)
        shift = 1 - (len(kb & ka) / len(kb | ka)) if (kb | ka) else 0
        cand.append((gap * 1.6 + shift * 3.2, cues[i][0], i))
    cand.sort(reverse=True)
    picked, MIN = [0.0], 10.0
    for _, t, i in cand:
        if len(picked) >= target: break
        if all(abs(t - p) >= MIN for p in picked) and dur - t >= MIN:
            picked.append(t)
    picked.sort()
    chapters = []
    for n, t in enumerate(picked):
        end = picked[n + 1] if n + 1 < len(picked) else dur
        text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end)
        kw = [w for w in keywords(text)]
        kw.sort(key=lambda w: -text.lower().count(w))
        title = " ".join(w.capitalize() for w in kw[:3]) or "Section"
        chapters.append({"start": round(t, 2), "label": mmss(t), "draft_title": title,
                         "seconds": round(end - t, 2)})
    ok = len(chapters) >= 3 and chapters[0]["start"] == 0 and all(c["seconds"] >= MIN for c in chapters)
    if as_json:
        print(json.dumps({"valid": ok, "chapters": chapters}, indent=1)); return
    print()
    for c in chapters: print(f"  {c['label']} {c['draft_title']}")
    print(f"\n  {len(chapters)} chapters"
          f"{'' if ok else '  -- INVALID: YouTube needs 3+, a 00:00 first entry and 10s minimum each'}")
    print("  Retitle every line before pasting. These are the topic words, not your words.\n")

if __name__ == "__main__":
    main()

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-comment/SKILL.md ===== -->

---
name: yt-comment
description: >-
  Draft replies to YouTube comments in the creator's voice, triaged by which
  ones are worth answering. Use for "reply to my comments", "handle the
  comment section", "someone asked X", or a pasted comment thread.
---

# yt-comment

The comment section is a retention surface, not a chore. Replies in the first few hours are what
decide whether a thread becomes a conversation other people read.

## Before you write

1. Read `~/.claude/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## Triage first, always

Sort what the user pastes into four piles and say how many are in each before writing anything:

1. **Questions** - answer them. These are your next video's topics, so note the repeats.
2. **Corrections** - if they are right, say so plainly and thank them. Never argue a fact you
   cannot check.
3. **Praise** - reply to a few, briefly, with something specific from their comment. A wall of
   identical "thank you!" replies reads as automated because it is.
4. **Bait** - do not reply. Say so and move on. Never write a comeback, however deserved.

## Writing the reply

- Under 30 words. A long reply in a comment thread is a blog post nobody asked for.
- Answer the actual question in the first sentence.
- One question back, only when it is real.
- No emoji unless the user's own replies use them. Check their voice file.
- Never promise a video you have not agreed to make.

## The heart and the pin

Say which ONE comment to pin and why. Pin the question the most people also have, not the nicest
one. Heart generously - it costs nothing and it is visible.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-edit/SKILL.md ===== -->

---
name: yt-edit
description: >-
  Turn a raw recording's transcript into an edit decision list - dead air,
  filler cues and retakes, with timecodes. Use for "edit this", "cut the
  dead space", "tighten this video", "I rambled", or any request to shorten
  footage from a transcript.
---

# yt-edit

An edit decision list from a timestamped transcript. It prints the cuts. You apply them.

```bash
python3 deadair.py transcript.srt              # srt, vtt or whisper json
python3 deadair.py transcript.srt --floor 0.35 --json
```

No transcript yet? Ask for one, or produce one first - `whisper`, `faster-whisper`, or the caption
track YouTube generates on an unlisted upload all work. Do not guess at timings.

## What it finds

- **DEAD** - gaps longer than the floor, trimmed from the MIDDLE so both sides keep a breath.
  Cutting flush against speech is what makes a tightened take sound gasping.
- **FILLER** - cues that are nothing but "um", "so yeah", "basically".
- **REPEAT** - a sentence restarted. Compared against the last cue that was actually speech, not
  the literal previous cue, because most retakes have an "um" between the two attempts.

## What it will not do

It does not touch media. It has no opinion about your B-roll. A 40% cut on the report is a 40% cut
of SPEECH, and if the video has a long silent demo in it that number is wrong - check the report
against the footage before you trust the runtime at the bottom.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-edit/deadair.py ===== -->

#!/usr/bin/env python3
"""deadair.py - an edit decision list from a timestamped transcript.

    python3 deadair.py transcript.srt            # or .vtt, or whisper .json
    python3 deadair.py transcript.srt --floor 0.35 --json

Finds three things and prints the cuts as a list you can act on, newest problem first:
  DEAD    gaps between spoken cues longer than the floor
  FILLER  cues that are only filler ("um", "so yeah", "basically")
  REPEAT  a sentence restarted - the second take of the same opening

WHAT IT DOES NOT DO. It does not cut the file. It prints an EDL, the total it would remove, and the
runtime you would land on, and you apply it in whatever editor you use. Nothing here touches media.
"""
import json, os, re, sys

FILLER_ONLY = re.compile(r"^[\s,.-]*((um+|uh+|er+|ah+|so|okay|ok|right|yeah|like|anyway|basically|"
                         r"actually|you know|i mean|let me see|hold on)[\s,.-]*)+$", re.I)

def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])

def load(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".json"):
        d = json.loads(raw)
        segs = d.get("segments", d if isinstance(d, list) else [])
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
    cues, cur = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())
    return [(a, b, " ".join(t)) for a, b, t in cues if t]

def norm(t): return re.sub(r"[^a-z ]", "", t.lower()).split()

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    floor = float(a[a.index("--floor") + 1]) if "--floor" in a else 0.45
    a = [x for x in a if not x.startswith("--") and not re.match(r"^[\d.]+$", x)]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if not cues: print("no cues found - is this an srt, vtt or whisper json?"); sys.exit(1)
    dur = cues[-1][1]
    cuts = []
    for i, (s, e, t) in enumerate(cues):
        if FILLER_ONLY.match(t):
            cuts.append({"kind": "FILLER", "start": s, "end": e, "why": t.strip()[:48]})
        if i:
            gap = s - cues[i - 1][1]
            if gap > floor:
                keep = floor / 2
                cuts.append({"kind": "DEAD", "start": round(cues[i - 1][1] + keep, 3),
                             "end": round(s - keep, 3), "why": f"{gap:.2f}s gap"})
        # A restart is compared against the last cue that was actually SPEECH. Comparing against
        # the literal previous cue misses every retake with an "um" between the two attempts, which
        # is most of them.
        if t.strip() and not FILLER_ONLY.match(t):
            j = i - 1
            while j >= 0 and (FILLER_ONLY.match(cues[j][2]) or not cues[j][2].strip()): j -= 1
            if j >= 0:
                a1, b1 = norm(cues[j][2])[:5], norm(t)[:5]
                if len(a1) >= 3 and a1 == b1:
                    cuts.append({"kind": "REPEAT", "start": cues[j][0], "end": cues[j][1],
                                 "why": f'restart of "{" ".join(a1)}"'})
    cuts = [c for c in cuts if c["end"] > c["start"]]
    cuts.sort(key=lambda c: c["start"])
    removed = sum(c["end"] - c["start"] for c in cuts)
    if as_json:
        print(json.dumps({"source": a[0], "duration": dur, "cuts": cuts,
                          "removed": round(removed, 3), "out": round(dur - removed, 3)}, indent=1)); return
    print(f"\n  {a[0]}   {dur:.2f}s in, {len(cues)} cues, dead-air floor {floor}s\n")
    for c in cuts:
        print(f"    {c['kind']:<7} {c['start']:8.2f} -> {c['end']:8.2f}   {c['end']-c['start']:5.2f}s   {c['why']}")
    print(f"\n  {len(cuts)} cuts, {removed:.2f}s removed, {dur - removed:.2f}s out "
          f"({removed / dur * 100:.1f}% shorter)\n")

if __name__ == "__main__":
    main()

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-package/SKILL.md ===== -->

---
name: yt-package
description: >-
  Write and lint the title and thumbnail for a YouTube video as one pairing,
  checking truncation, duplication and vagueness before publish. Use for
  "title ideas", "what should I call this", "thumbnail text", "my CTR is
  bad", packaging, or any request to rename or repackage an existing video.
---

# yt-package

The title and the thumbnail are ONE unit. Writing them separately is why most packaging fails: the
thumbnail repeats the title, and half the click surface says the same thing twice.

```bash
python3 title.py --title "..." --thumb "AI RAN IT"
python3 title.py titles.txt            # one per line, ranked
```

## Before you write

1. Read `~/.claude/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## Rules the tool enforces, and why

- **60 characters** is where desktop search truncates, **40** is a mobile home feed. Both are
  reported because they fail differently: a desktop cut loses the tail, a mobile cut can lose the
  subject.
- **The thumbnail must not repeat the title.** Different words, same promise.
- **Three words maximum on the thumbnail.** At feed size a fourth word is a grey smear.
- **A number, a name or a date** beats every adjective available to you.
- **Two all-caps words is the ceiling** before a title reads as spam.

## Write ten, keep two

Generate ten titles, run them all through `title.py`, show the user the top three with their scores
and the specific issue on each. For the winner, write the thumbnail brief: the expression, the
framing, the three words, and what the background has to do to hold contrast at feed size.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-package/title.py ===== -->

#!/usr/bin/env python3
"""title.py - lint a YouTube title and thumbnail pairing before you publish it.

    python3 title.py --title "..." --thumb "AI RAN IT"
    python3 title.py titles.txt            # one per line, ranked
    python3 title.py --title "..." --json

The pairing is the unit, not the title. A title that repeats the thumbnail text wastes half the
click surface, and that is the single most common mistake this checks for.

Length: YouTube truncates around 60 characters on desktop search and around 40 on a mobile home
feed. Both limits are reported because they are different failures - a desktop truncation loses the
tail, a mobile one can lose the subject.
"""
import json, re, sys, os

DESKTOP, MOBILE, HARD = 60, 40, 100
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","ultimate","best","powerful",
         "secret","revolutionary","mindblowing","epic","perfect","complete","everything"}
STOP = {"the","a","an","of","for","to","in","on","and","or","is","are","with","your","you","my","i",
        "this","that","it","how","what","why"}

def words(t): return re.findall(r"[a-z0-9']+", t.lower())

def check(title, thumb=None):
    t = title.strip()
    n = len(t)
    issues, good = [], []
    if n > HARD: issues.append(("length", f"{n} characters - YouTube's hard limit is {HARD}"))
    elif n > DESKTOP: issues.append(("length", f"{n} characters - desktop search cuts near {DESKTOP}"))
    else: good.append(f"{n} characters, inside the {DESKTOP}-character desktop cut")
    if n > MOBILE:
        head = t[:MOBILE].rsplit(" ", 1)[0]
        issues.append(("mobile", f'a mobile feed shows about "{head}..." - check the subject survives'))
    caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
    if len(caps) > 2: issues.append(("shouting", f"{len(caps)} all-caps words - two is the ceiling before it reads as spam"))
    elif caps: good.append(f"{len(caps)} all-caps word for emphasis")
    v = [w for w in words(t) if w in VAGUE]
    if v: issues.append(("vague", f"{', '.join(sorted(set(v)))} - swap for a number, a name or a date"))
    nums = re.findall(r"\d[\d,.]*%?", t)
    if nums: good.append(f"carries a concrete figure ({', '.join(nums[:3])})")
    else: issues.append(("no-number", "no number, date or name - the most reliable single fix"))
    if t.endswith("?"): good.append("open question in the title")
    front = [w for w in words(t)[:3] if w not in STOP]
    if not front: issues.append(("front-load", "the first three words are all filler - move the subject forward"))
    if thumb:
        tw, hw = set(words(t)) - STOP, set(words(thumb)) - STOP
        shared = tw & hw
        if shared:
            issues.append(("duplicate", f"thumbnail repeats the title on {', '.join(sorted(shared))} - "
                                        "the thumbnail should say what the title does not"))
        else:
            good.append("thumbnail and title carry different words")
        if len(words(thumb)) > 4:
            issues.append(("thumb-length", f"{len(words(thumb))} words on the thumbnail - three is the ceiling at feed size"))
    score = max(0, min(100, 100 - 14 * len(issues) + 4 * len(good)))
    return {"title": t, "chars": n, "score": score, "issues": issues, "good": good}

def show(r):
    print(f'\n  "{r["title"]}"')
    print(f"  {r['chars']} chars   score {r['score']}/100")
    for k, m in r["issues"]: print(f"    x  {k:<12} {m}")
    for m in r["good"]:      print(f"    ok              {m}")

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    thumb = a[a.index("--thumb") + 1] if "--thumb" in a else None
    if "--title" in a:
        rows = [check(a[a.index("--title") + 1], thumb)]
    elif a and os.path.exists(a[0]):
        rows = [check(l, thumb) for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1)
    rows.sort(key=lambda r: -r["score"])
    if as_json: print(json.dumps(rows, indent=1)); return
    for r in rows: show(r)
    print()

if __name__ == "__main__":
    main()

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-plan/SKILL.md ===== -->

---
name: yt-plan
description: >-
  Plan a week or a month of YouTube uploads - what to post, when, and in
  what order, sized to the creator's actual capacity. Use for "plan my
  week", "content calendar", "what should I post", "I have no idea what to
  make next".
---

# yt-plan

A plan that does not fit the week is a list of regrets. Ask two questions before writing anything:
**how many hours do you actually have**, and **what is already half-made**.

## Before you write

1. Read `~/.claude/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The shape of a week

- **One anchor.** The video the week is for. It gets the most time and it goes out on the day the
  channel's own analytics say is best - ask for that, do not assume Tuesday.
- **One cheap one.** Built from something that exists: a clip, a reaction, a follow-up to the
  comment that got the most replies last week.
- **Shorts from the anchor.** Three, cut from the long video, not written separately. `/yt-shorts`
  finds them.

Three uploads on a seven-day week, not seven. A plan that posts daily is not a plan anyone
recognises, and the empty days are what make the filled ones survive a bad week.

## What to hand back

A table: day, format, working title, the one sentence it promises, and what already exists for it.
Then the honest line at the bottom - how many hours this costs, and what to drop first if the week
goes wrong.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-retention/SKILL.md ===== -->

---
name: yt-retention
description: >-
  Read a YouTube Studio audience-retention export and find where viewers
  actually leave, then say what to change. Use for "why do people stop
  watching", "my retention is bad", a pasted retention chart or CSV, or "fix
  my pacing".
---

# yt-retention

The retention graph is the only honest feedback YouTube gives you. Almost nobody exports it.

```bash
python3 retention.py retention.csv --duration 600
python3 retention.py retention.csv --transcript transcript.srt
```

Getting the file: Studio -> a video -> Analytics -> Engagement -> the audience-retention chart ->
the download icon -> "Audience retention".

## Three different problems

- **HOOK LEAK** - what is lost in the first 30 seconds. Under 25% is healthy. This is always the
  first thing to fix and it is always the first fifteen seconds of script, never the edit.
- **CLIFFS** - single steep drops. A cliff is a moment: a topic change with no signposting, a
  sponsor read, a long setup. With `--transcript` the tool prints what was being said there, which
  is what makes the report actionable instead of interesting.
- **SLIDE** - the steady bleed across the middle. A flat slide is pacing. The fix is cutting, not
  rewriting.

## What to hand back

Name the single biggest leak and one change for it. Not a list of five. Then, only if asked, the
rest. And if the hook leak is healthy and the slide is flat, say the video is fine and the problem
is packaging - send them to `/yt-package`.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-retention/retention.py ===== -->

#!/usr/bin/env python3
"""retention.py - read a YouTube Studio audience-retention export and find the leaks.

    python3 retention.py retention.csv
    python3 retention.py retention.csv --transcript transcript.srt   # names what was said at each drop
    python3 retention.py retention.csv --json

Get the file from Studio: Analytics -> a video -> Engagement -> the audience-retention chart ->
the download icon -> "Audience retention". Two columns, a position (percent or seconds) and a
percentage still watching.

It reports three things, because they are three different problems with three different fixes:
  HOOK LEAK    what you lost in the first 30 seconds
  CLIFFS       single steep drops - a specific moment people left at
  SLIDE        the steady bleed rate across the flat middle

With --transcript it prints what you were saying at each cliff, which is the only version of this
report you can act on without scrubbing the video yourself.
"""
import csv, json, os, re, sys

def load_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        for r in csv.reader(fh):
            nums = []
            for c in r:
                c = c.strip().replace("%", "").replace(",", "")
                try: nums.append(float(c))
                except ValueError: nums.append(None)
            vals = [n for n in nums if n is not None]
            if len(vals) >= 2: rows.append((vals[0], vals[1]))
    return rows

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    tr = a[a.index("--transcript") + 1] if "--transcript" in a else None
    files = [x for x in a if not x.startswith("--") and x != tr]
    if not files or not os.path.exists(files[0]): print(__doc__); sys.exit(1)
    rows = load_csv(files[0])
    if len(rows) < 8: print("could not read at least 8 data points from that csv"); sys.exit(1)
    xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
    pct_axis = max(xs) <= 100.5
    dur = None
    if "--duration" in a: dur = float(a[a.index("--duration") + 1])
    def at(x): return (x / 100.0 * dur) if (pct_axis and dur) else x
    start = ys[0] or 100.0
    # HOOK: the first 30 seconds, or the first 10% when the axis is a percentage and we have no duration
    cutoff = 30.0 if not pct_axis else (30.0 / dur * 100 if dur else 10.0)
    hook_end = min((y for x, y in rows if x <= cutoff), default=start)
    hook_leak = start - hook_end
    drops = []
    for i in range(1, len(rows)):
        d = ys[i - 1] - ys[i]
        span = xs[i] - xs[i - 1] or 1
        drops.append((d / span, xs[i - 1], xs[i], d))
    drops.sort(reverse=True)
    cliffs = [{"from": round(a1, 2), "to": round(b1, 2), "lost": round(d, 2),
               "at_seconds": round(at(a1), 1) if (not pct_axis or dur) else None}
              for _, a1, b1, d in drops[:5] if d > 0.8]
    mid = [d for d, x0, _, _ in [(r[0], r[1], r[2], r[3]) for r in drops] if x0 > cutoff]
    slide = sum(mid) / len(mid) if mid else 0
    said = {}
    if tr and os.path.exists(tr):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
        from deadair import load as load_cues
        cues = load_cues(tr)
        for c in cliffs:
            if c["at_seconds"] is None: continue
            t = c["at_seconds"]
            near = [q[2] for q in cues if q[0] <= t + 4 and q[1] >= t - 4]
            said[str(c["from"])] = " ".join(near)[:140]
    out = {"points": len(rows), "start": start, "hook_leak": round(hook_leak, 2),
           "end": ys[-1], "cliffs": cliffs, "slide_per_unit": round(slide, 3), "said": said}
    if as_json: print(json.dumps(out, indent=1)); return
    print(f"\n  {files[0]}   {len(rows)} points   {ys[0]:.1f}% -> {ys[-1]:.1f}%\n")
    verdict = "healthy" if hook_leak < 25 else "leaking" if hook_leak < 40 else "severe"
    print(f"  HOOK LEAK   {hook_leak:.1f}% lost in the opening   [{verdict}]")
    print(f"              under 25 is healthy for this length. Fix the first line before anything else.\n")
    print("  CLIFFS      the moments people actually left")
    for c in cliffs:
        where = f"{c['at_seconds']:.0f}s" if c["at_seconds"] is not None else f"{c['from']}"
        print(f"    -{c['lost']:5.1f}%  at {where:>8}" + (f"   \"{said.get(str(c['from']),'')}\"" if said else ""))
    if not cliffs: print("    none steeper than 0.8% - the loss is all slide, not moments")
    print(f"\n  SLIDE       {slide:.3f}% per unit across the middle")
    print( "              a flat slide is pacing, not content. Cut the middle, do not rewrite it.\n")

if __name__ == "__main__":
    main()

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-script/SKILL.md ===== -->

---
name: yt-script
description: >-
  Write a YouTube video script from a raw idea - hook options off 21
  formulas, scored, then the full spoken script with the retention beats
  marked. Use whenever the user wants a video script, a hook, an opening
  line, "what should I say", "write my next video", or is about to record
  and does not have the first fifteen seconds yet.
---

# yt-script

One idea into a script somebody finishes.

Two tools live in this folder and both actually run. Use them. Do not eyeball the hook.

```bash
python3 hookscore.py hooks.txt              # rank your hook options
python3 hookscore.py --hook "one line"      # score a single one
```

## Before you write

1. Read `~/.claude/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The shape

**The first 15 seconds is the whole job.** It does three things or the video leaks: confirm the
click the title promised, open a question the viewer cannot close, and prove the payoff exists.

1. **Hook.** Write FIVE against [the 21 formulas](hooks.json), run them through `hookscore.py`,
   keep the top two, and show the user both with their scores. Never hand over one hook.
2. **The turn** (0:15-0:45). Say what the video is going to do, in one sentence, and start doing it.
   No channel intro, no "before we get started", no subscribe pitch. Those are the single most
   common cause of the 0:30 cliff.
3. **The body.** One idea per beat. Mark each beat with what is ON SCREEN, not just what is said -
   a talking head with nothing to look at is a podcast.
4. **The payoff.** Deliver the thing the hook promised, explicitly, and say that you are delivering
   it: "that is the prompt, it is in the description".
5. **The close.** One ask. Not three.

## What to hand back

- the two best hooks with their scored panels
- the script, beat by beat, with `[ON SCREEN: ...]` on every beat
- the runtime estimate at 150 words per minute
- one line naming which formula the winning hook used and why it fits this idea

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-script/hooks.json ===== -->

{
 "version": "1.0",
 "note": "21 hook formulas for YouTube. A YouTube hook is the first 15 seconds and it does three jobs: confirm the click the title promised, raise a question the viewer cannot close, and prove the payoff exists. A hook that only does the third is a summary and it leaks. Every formula here carries the shape, a worked example, the failure mode, and the patterns hookscore.py classifies transcribed speech against.",
 "rules": [
  "Confirm the title in the first sentence. A hook that ignores its own title is why people leave at 0:08.",
  "One idea. A hook carrying two promises keeps neither.",
  "Specific beats big. '400 to 200,000 in seven months' outperforms 'massive growth'.",
  "Show the artifact inside 20 seconds if you promised one.",
  "Never open with who you are. The subscribe pitch has not been earned yet."
 ],
 "hooks": [
  {
   "id": "the-statistic",
   "name": "The Statistic",
   "shape": "A number the viewer did not know, stated flat, then the consequence.",
   "example": "97% of the people who start a channel quit before video 30. Here is what the other 3% do differently.",
   "fails_when": "Dies if the number is vague or unverifiable. Say the source out loud.",
   "match": [
    "\\b\\d+(\\.\\d+)?\\s?%",
    "\\b\\d+ (out of|in) \\d+\\b",
    "\\b\\d{2,}(,\\d{3})+\\b"
   ]
  },
  {
   "id": "someone-elses-result",
   "name": "Someone Else's Result",
   "shape": "A named person's outcome, then the mechanism.",
   "example": "This channel went from 400 subscribers to 200,000 in seven months on one format. I mapped it.",
   "fails_when": "Do not invent the number. If you cannot name the channel, use a different formula.",
   "match": [
    "\\bthis (channel|guy|creator|account)\\b",
    "\\bwent from .* to\\b",
    "\\bin (a|one|two|three|\\d+) (week|month|year)s?\\b"
   ]
  },
  {
   "id": "the-mistake",
   "name": "The Mistake",
   "shape": "Name the error the viewer is probably making right now.",
   "example": "Your first 30 seconds are why nobody finishes your videos. It is not the topic.",
   "fails_when": "Only works if the mistake is common and the viewer can check it in one second.",
   "match": [
    "\\byou('re| are) (probably |still )?(doing|making)\\b",
    "\\bthe (mistake|reason) (everyone|most people|nobody)\\b",
    "\\bstop (doing )?\\b"
   ]
  },
  {
   "id": "contrarian-flip",
   "name": "Contrarian Flip",
   "shape": "State the accepted advice, then reject it.",
   "example": "Everyone says post daily. I posted once a week for a year and tripled the channel.",
   "fails_when": "Needs evidence in the next 15 seconds or it reads as contrarian for its own sake.",
   "match": [
    "\\beveryone (says|thinks|tells you)\\b",
    "\\bis (actually )?wrong\\b",
    "\\bnobody (tells|talks about)\\b"
   ]
  },
  {
   "id": "the-reveal",
   "name": "The Reveal",
   "shape": "Promise a specific thing will be shown, then show it.",
   "example": "I am going to show you the exact prompt, on screen, that wrote this video.",
   "fails_when": "You have to actually show it, early. A reveal at 8:00 is a retention cliff at 1:00.",
   "match": [
    "\\bI('m| am) going to show you\\b",
    "\\bhere('s| is) (the|exactly)\\b",
    "\\bon screen\\b"
   ]
  },
  {
   "id": "the-superlative",
   "name": "The Superlative",
   "shape": "The single best/worst/fastest of a category.",
   "example": "This is the fastest way to turn one long video into thirty Shorts.",
   "fails_when": "Superlatives are cheap. Earn it by naming what it beat.",
   "match": [
    "\\bthe (best|worst|fastest|easiest|only)\\b",
    "\\bnumber one\\b"
   ]
  },
  {
   "id": "the-clock",
   "name": "The Clock",
   "shape": "Bound the payoff in time.",
   "example": "In the next six minutes you will have a working title, thumbnail and script for your next video.",
   "fails_when": "The clock has to be true. Overrun it and the next video's hook is not believed.",
   "match": [
    "\\bin (the next )?\\d+ (seconds|minutes|hours)\\b",
    "\\bby the end of this video\\b",
    "\\bunder \\d+\\b"
   ]
  },
  {
   "id": "i-tried-it",
   "name": "I Tried It",
   "shape": "First-person experiment with a stated cost.",
   "example": "I let an AI run my channel for 30 days. I did not touch the uploads.",
   "fails_when": "Needs a real cost - time, money, risk - or there is no stake.",
   "match": [
    "\\bI (tried|spent|tested|let|gave)\\b",
    "\\bfor \\d+ (days|weeks|months)\\b",
    "\\bso you don'?t have to\\b"
   ]
  },
  {
   "id": "the-question",
   "name": "The Question",
   "shape": "Ask the exact question the viewer typed into search.",
   "example": "Why do your videos die at 30 seconds when the topic is fine?",
   "fails_when": "Must be the viewer's question, not yours. Pull it from your own comments.",
   "match": [
    "^(why|how|what|when|should|can|do|does|is)\\b",
    "\\?\\s*$"
   ]
  },
  {
   "id": "the-before-after",
   "name": "Before and After",
   "shape": "Two states, one cut between them.",
   "example": "This was my thumbnail. This is my thumbnail now. Same video, four times the click-through.",
   "fails_when": "Only works with a visual. Do not use it on a talking-head-only video.",
   "match": [
    "\\bbefore\\b.*\\bafter\\b",
    "\\bthis was\\b.*\\bthis is\\b",
    "\\bused to\\b"
   ]
  },
  {
   "id": "the-teardown",
   "name": "The Teardown",
   "shape": "Take a real thing apart in public.",
   "example": "I pulled the nine most-viewed AI videos of the month and broke down what the titles share.",
   "fails_when": "Name what you pulled and how many. A teardown of one example is an anecdote.",
   "match": [
    "\\b(broke|break|breaking) (it )?down\\b",
    "\\bteardown\\b",
    "\\banalys(ed|ed|is|e)\\b",
    "\\bI pulled\\b"
   ]
  },
  {
   "id": "the-stack",
   "name": "The Stack",
   "shape": "Two named tools combined into one outcome.",
   "example": "Claude plus your YouTube Studio export gives you next week's upload schedule in one prompt.",
   "fails_when": "Both tools must be nameable and the outcome must need both.",
   "match": [
    "\\b\\w+ (plus|\\+) \\w+\\b",
    "\\bcombine\\b",
    "\\btogether\\b"
   ]
  },
  {
   "id": "the-warning",
   "name": "The Warning",
   "shape": "A cost the viewer is about to pay.",
   "example": "Do not upload another video until you check this one setting.",
   "fails_when": "If the cost is small the hook is a lie. Reserve it.",
   "match": [
    "\\bdo not\\b",
    "\\bdon'?t (upload|post|publish|start)\\b",
    "\\bbefore you\\b",
    "\\bstop\\b"
   ]
  },
  {
   "id": "the-list",
   "name": "The List",
   "shape": "A counted set, with the count in the first line.",
   "example": "Seven things I would do differently if I started a channel in 2026.",
   "fails_when": "The count must be exact and every item must be different in kind.",
   "match": [
    "^\\d+ \\w+",
    "\\b(here are|these are) \\d+\\b"
   ]
  },
  {
   "id": "the-receipt",
   "name": "The Receipt",
   "shape": "Show the artifact first, explain second.",
   "example": "This is the analytics page. This video did 40% of the channel's watch time. Here is why.",
   "fails_when": "Requires a real screenshot. A described receipt is not a receipt.",
   "match": [
    "\\bthis is (the|my)\\b",
    "\\bscreenshot\\b",
    "\\bproof\\b",
    "\\breceipts?\\b"
   ]
  },
  {
   "id": "the-insider",
   "name": "The Insider",
   "shape": "Information from inside a system.",
   "example": "YouTube tells you which videos are underperforming. Almost nobody opens the report.",
   "fails_when": "Do not claim insider access you do not have.",
   "match": [
    "\\b(nobody|almost nobody|most people) (knows?|opens?|uses?)\\b",
    "\\bhidden\\b",
    "\\bburied\\b"
   ]
  },
  {
   "id": "the-impossible",
   "name": "The Impossible Claim",
   "shape": "State something that sounds untrue, then prove it.",
   "example": "You can write, title, thumbnail and schedule a week of videos without opening a single editor.",
   "fails_when": "The proof has to start within 20 seconds or it reads as clickbait.",
   "match": [
    "\\bwithout\\b",
    "\\bnever\\b",
    "\\bin one\\b",
    "\\bzero\\b"
   ]
  },
  {
   "id": "the-comparison",
   "name": "The Comparison",
   "shape": "Two named options, one winner.",
   "example": "I wrote the same video three ways. One of them held 62% and the other two did not.",
   "fails_when": "Say the losing option out loud. A comparison with no loser is an advert.",
   "match": [
    "\\bvs\\.?\\b",
    "\\bversus\\b",
    "\\bwhich (one )?(is|wins)\\b",
    "\\bsame .* (three|two) ways\\b"
   ]
  },
  {
   "id": "the-origin",
   "name": "The Origin",
   "shape": "Where a result actually came from.",
   "example": "Every video on this channel starts in the same 12-line file. Here it is.",
   "fails_when": "Works once per channel. It is a reveal about you, and you only have one.",
   "match": [
    "\\bevery (video|post) .* starts\\b",
    "\\bit all (starts|started)\\b",
    "\\bthe (real )?reason\\b"
   ]
  },
  {
   "id": "the-deadline",
   "name": "The Deadline",
   "shape": "Something is changing on a date.",
   "example": "The old description format stops mattering this month. Here is what replaces it.",
   "fails_when": "Only use with a real, checkable date. This is the fastest formula to lose trust with.",
   "match": [
    "\\b(this|next) (week|month|year)\\b",
    "\\bis changing\\b",
    "\\bno longer\\b",
    "\\bas of\\b"
   ]
  },
  {
   "id": "the-direct-address",
   "name": "The Direct Address",
   "shape": "Name the exact viewer in the first six words.",
   "example": "If you have under a thousand subscribers, this is the only video you need this week.",
   "fails_when": "Narrow beats broad. 'If you make videos' addresses nobody.",
   "match": [
    "^if you\\b",
    "\\bfor (anyone|everyone|people) who\\b",
    "\\byou specifically\\b"
   ]
  }
 ]
}

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-script/hookscore.py ===== -->

#!/usr/bin/env python3
"""hookscore.py - score a YouTube hook before you waste a take on it.

Five properties, 0-100 each, and a verdict that is 60% the mean and 40% the weakest one. The
weakest-link weighting is deliberate: a hook with four strong properties and one dead one is a hook
that leaks at the dead one, and averaging hides that.

    python3 hookscore.py hooks.txt            # one hook per line, ranked
    python3 hookscore.py --hook "one line"    # score a single hook
    python3 hookscore.py --json hooks.txt     # machine-readable

WHAT THIS CAN AND CANNOT TELL YOU. Measured against 74 real short-form hooks (first 15 seconds of
auto-captions, top-8 and bottom-8 by views across five channels): it separates deliberately bad
hooks from real ones well, and it separates a creator's own hits from their own misses barely at
all. Treat a low score as a reason to look again, never a high score as a promise.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "hooks.json")))["hooks"]

FILLER = {"basically","actually","literally","just","really","very","so","kind","sort","like",
          "guys","hey","welcome","today","video","subscribe","channel"}
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","game","changer","secret",
         "powerful","ultimate","best","revolutionary","mind","blowing","unbelievable"}
CONCRETE = re.compile(r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)\b", re.I)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE = re.compile(r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead)\b", re.I)
CURIOSITY = re.compile(r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually)\b", re.I)

def words(t): return re.findall(r"[a-z0-9'%$.]+", t.lower())

def specificity(t):
    w = words(t)
    if not w: return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    # proper nouns that are not sentence-initial read as named things
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))

def address(t):
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    return max(0, min(100, 26 + n * 20 + first))

def stakes(t):
    n = len(STAKE.findall(t))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))

def curiosity(t):
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    # a hook that resolves itself has no gap left
    closed = -18 if re.search(r"\b(because|so that|which means)\b", t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))

def brevity(t):
    n = len(words(t))
    if n == 0: return 0
    # 9-24 words is the band a spoken hook lands in at ~150wpm inside 10 seconds
    if 9 <= n <= 24: return 100
    if n < 9:  return max(30, 100 - (9 - n) * 11)
    return max(10, 100 - (n - 24) * 7)

PROPS = [("SPECIFICITY", specificity), ("ADDRESS", address), ("STAKES", stakes),
         ("CURIOSITY", curiosity), ("BREVITY", brevity)]

def classify(t):
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, t, re.I))
        if n > hits: best, hits = f, n
    return (best["name"] if best else "Unclassified"), hits

def score(t):
    parts = {n: fn(t) for n, fn in PROPS}
    vals = list(parts.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    name, hits = classify(t)
    return parts, verdict, name, hits

def band(v): return "STRONG" if v >= 72 else "WORKABLE" if v >= 55 else "WEAK"

def report(t, parts, verdict, name, hits):
    print(f"\n  {t.strip()}")
    print(f"  {'-' * min(72, max(20, len(t.strip())))}")
    for k, v in parts.items():
        print(f"    {k:<12} {v:3d}  {'#' * (v // 5)}")
    print(f"    {'VERDICT':<12} {verdict:3d}  {band(verdict)}")
    print(f"    formula      {name}" + (f"  ({hits} pattern{'s' if hits != 1 else ''} matched)" if hits else "  (no formula matched - that is usually a summary, not a hook)"))
    low = min(parts, key=parts.get)
    print(f"    weakest      {low} - {FIX[low]}")

FIX = {
 "SPECIFICITY": "swap one adjective for a number, a name or a date",
 "ADDRESS": "say 'you' in the first six words",
 "STAKES": "name what it costs them to keep doing it the current way",
 "CURIOSITY": "cut the half of the sentence that answers itself",
 "BREVITY": "9 to 24 words. Read it out loud and stop where you run out of breath",
}

def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        lines = [l for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1 if not a else 0)
    out = []
    for t in lines:
        parts, verdict, name, hits = score(t)
        out.append({"hook": t.strip(), "properties": parts, "verdict": verdict,
                    "band": band(verdict), "formula": name, "matched": hits})
    out.sort(key=lambda r: -r["verdict"])
    if as_json:
        print(json.dumps([{k: v for k, v in r.items() if k != "matched"} for r in out], indent=1)); return
    for r in out:
        report(r["hook"], r["properties"], r["verdict"], r["formula"], r["matched"])
    if len(out) > 1:
        print(f"\n  winner: {out[0]['hook'].strip()}  ({out[0]['verdict']}, {out[0]['band']})\n")

if __name__ == "__main__":
    main()

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-seo/SKILL.md ===== -->

---
name: yt-seo
description: >-
  Write the description, tags and search-facing text for a YouTube video,
  aimed at the query a real person types. Use for "write my description",
  "tags", "SEO", "help this video get found", "nobody is finding this".
---

# yt-seo

Search is a smaller lever than packaging and a bigger one than people think for evergreen videos.
For a video aimed at the subscriber feed, say so and spend the effort on `/yt-package` instead.

## Before you write

1. Read `~/.claude/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The description

- **The first two lines are the only ones anyone reads.** They show above "...more" and they are
  the search snippet. Say what the video gives them, in the words they would have typed.
- Then the link or the resource, if there is one, so it is above the fold.
- Then chapters (`/yt-chapters` writes them).
- Then the long version: what is covered, who it is for, what it assumes.

## Tags, honestly

Tags are a weak signal and YouTube has said so. Use them for disambiguation - spellings, the tool
names, the abbreviations people actually type - and stop. Fifteen is plenty. A wall of tags is not
a strategy and stuffing unrelated ones is against the terms.

## The query test

Before handing anything over, write the three search queries this video should win, and check the
title and first two description lines contain the words in those queries. If they do not, the
problem is the title, not the description.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-shorts/SKILL.md ===== -->

---
name: yt-shorts
description: >-
  Find the Shorts hiding inside a long video and write them, using the
  transcript to pick self-contained moments. Use for "cut this into shorts",
  "clip this", "repurpose this video", "what should I clip".
---

# yt-shorts

A Short cut out of a long video is not a clip of the best moment. It is a moment that **survives
without the video around it**, which is a much smaller set.

## Picking

Read the transcript and find spans of 20-55 seconds where all three are true:

1. It opens on a complete thought. If the first sentence needs the previous minute, it is not a Short.
2. There is a turn in it - a claim, then something that complicates or proves it.
3. It ends on a line, not a trail-off.

Rank the candidates and show the user the top five with their timecodes and first line, so they can
reject one without reading the whole transcript.

## Writing each one

- **A NEW first line.** The long video's line assumes context this viewer does not have. Write the
  replacement and run it through `../yt-script/hookscore.py`.
- **On-screen text for the first two seconds**, different words from the spoken line.
- **A loop point**: what the last line sets up so the first line answers it.
- Vertical framing note - what gets cropped out of a 16:9 frame and whether that matters.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-viral/SKILL.md ===== -->

---
name: yt-viral
description: >-
  Find what is actually working in the user's niche on YouTube and rank it
  by how far each video beat its own channel, then name the formula. Use for
  "what's working right now", "find viral videos in my niche", "why did this
  blow up", competitor research, or a swipe file.
---

# yt-viral

Raw view counts rank channel size, not ideas. This ranks by **multiple over each channel's own
median**, which is the only version of the question that is about the video.

```bash
python3 swipe.py collected.json --min 2.0
```

## Collecting the input

You need at least **four videos per channel** or a median means nothing, and the tool will skip the
channel and tell you it did. Collect them however the user prefers - `yt-dlp --flat-playlist -J`
against a channel URL is the fastest, the public page works, a manual list works.

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

**Read, do not scrape.** Public listings only, never a logged-in session, never the user's own
account credentials.

## Reading the output

The multiple is the signal. The formula line is a judgement about the TITLE, matched against
[the 21 formulas](../yt-script/hooks.json) - it is not a claim about why the video worked, and you
should say so when you present it.

What to hand back: the top five with their multiples, the formula each used, and the ONE structural
thing they share. Then the harder line - which of those the user could actually make this week, in
their voice, with what they have.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

---

<!-- ===== SOURCE FILE: youtube-agent-skill/skills/yt-viral/swipe.py ===== -->

#!/usr/bin/env python3
"""swipe.py - rank collected videos by how far each beat its OWN channel, then name the formula.

    python3 swipe.py collected.json
    python3 swipe.py collected.json --min 2.0 --json

Input is a list you collected - one object per video:

    [{"channel":"Some Channel","title":"...","views":412000,"url":"...","duration":613}, ...]

Raw view counts rank channel size, not ideas. A 400k video on a 2M-subscriber channel is a normal
Tuesday; a 400k video on a channel whose median is 30k is the thing worth studying. So every video
is scored as a MULTIPLE OF ITS OWN CHANNEL'S MEDIAN, which needs at least four videos per channel
to mean anything - the tool says so rather than quietly ranking on noise.

The formula comes from skills/yt-script/hooks.json, matched against the TITLE. It is a judgement
about the words on screen, not a claim about why the video worked.
"""
import json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "..", "yt-script", "hooks.json")))["hooks"]

def classify(title):
    scored = []
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, title, re.I))
        if n: scored.append((n, f["name"]))
    scored.sort(reverse=True)
    return scored[0][1] if scored else "Unclassified"

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    lo = float(a[a.index("--min") + 1]) if "--min" in a else 1.5
    files = [x for x in a if not x.startswith("--") and not re.match(r"^[\d.]+$", x)]
    if not files or not os.path.exists(files[0]): print(__doc__); sys.exit(1)
    rows = json.load(open(files[0]))
    if isinstance(rows, dict): rows = rows.get("videos", [])
    by = {}
    for r in rows: by.setdefault(r.get("channel", "?"), []).append(r)
    out, thin = [], []
    for ch, vids in by.items():
        views = [float(v.get("views", 0) or 0) for v in vids]
        med = statistics.median(views) if views else 0
        if len(vids) < 4:
            thin.append((ch, len(vids)))
            continue
        for v in vids:
            m = (float(v.get("views", 0) or 0) / med) if med else 0
            out.append({"channel": ch, "title": v.get("title", ""), "views": int(v.get("views", 0) or 0),
                        "median": int(med), "multiple": round(m, 2),
                        "formula": classify(v.get("title", "")), "url": v.get("url", "")})
    out = [r for r in out if r["multiple"] >= lo]
    out.sort(key=lambda r: -r["multiple"])
    if as_json: print(json.dumps({"outliers": out, "skipped_thin_channels": thin}, indent=1)); return
    print(f"\n  {len(rows)} videos across {len(by)} channels, outliers at {lo}x or better\n")
    for r in out[:25]:
        print(f"    {r['multiple']:5.2f}x  {r['views']:>9,}  vs {r['median']:>9,} median   {r['channel'][:22]:<22} {r['title'][:52]}")
        print(f"            {r['formula']}")
    if not out: print("    nothing cleared the threshold - collect more per channel or lower --min")
    if thin:
        print(f"\n  skipped {len(thin)} channel(s) with under 4 videos collected - a median off one or")
        print( "  two videos is not a median: " + ", ".join(f"{c} ({n})" for c, n in thin[:6]))
    counts = {}
    for r in out: counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    if counts:
        print("\n  formulas among the outliers")
        for f, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"    {n:2d}x  {f}")
    print()

if __name__ == "__main__":
    main()
