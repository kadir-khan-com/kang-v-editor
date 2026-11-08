# ChaiWithJai/davinci-resolve-claude-skills

- **Repo:** ChaiWithJai/davinci-resolve-claude-skills — DaVinci Resolve 20 ke liye 11 Claude/Codex skills
- **Link:** https://github.com/ChaiWithJai/davinci-resolve-claude-skills
- **Licence:** MIT (repo page par verify; LICENSE file root me hai)
- **Activity:** 32 stars · 4 forks · sirf 2 commits · repo bana 2026-05-16 (repo page, 2026-11-06) — naya repo, lekin content Blackmagic ki official Resolve 20 training PDFs par dogfood kiya gaya hai
- **Content map:** 11 job-wise skills — setup, project template, screen-recording cut (60 min → 8 min tight demo), webcam color grade, podcast audio cleanup (ducking samet), titles/lower-thirds, multi-platform export, troubleshooting, computer-use training, social-editor (semantic cuts, B-roll, captions, Resolve handoff), folder autocutter. Neeche saare SKILL.md full hain + social-editor ke technique references (editing-qa, reels-eval-benchmark, qedc-trace-learnings, resolve-automation). Kuch skills ke saath Python scripts bhi hain (auto_silence_cut.py, multi_platform_render.py) jo Resolve scripting API chalate hain — scripts code hain, technique SKILL.md me hai. Repo ke docs/wiki (Blackmagic PDFs ke summaries) is file me NAHI liye — skills hi asal harvest hain.

---

# DaVinci Resolve Claude Skills

Claude/Codex skills for DaVinci Resolve 20. Built for creators, operators, developers, and educators who need publishable video, not another pile of editing notes.

The repo is organized around real jobs to be done: cut the story, repair the audio, keep the speaker in frame, add captions people can read on a phone, source useful B-roll, and hand the result back as an editable Resolve timeline.

If you found this from Twitter: this is an open skill library for teaching AI agents professional post-production workflows with evidence, not vibes.

If you came from Jai's content: this is the operating system behind turning raw workshop footage into Instagram Reels, Shorts, and YouTube videos that explain the offer clearly and feel worth watching.

## What is in the box

Eleven skills, each solving a specific job:

| Skill | Job to be done |
|---|---|
| `davinci-resolve-setup` | Install Resolve correctly, set up media drives, configure backups before your first edit |
| `davinci-resolve-devrel-project-template` | Set up a reusable project — bins, timeline, render presets, color preset — once, reuse forever |
| `davinci-resolve-cut-screen-recording` | Turn a 60-minute screen recording into an 8-minute tight demo (kills ums, dead air, mistakes) |
| `davinci-resolve-color-grade-webcam` | Make webcam or interview footage look broadcast-quality (skin tones, exposure, balance) |
| `davinci-resolve-audio-cleanup-podcast` | Clean podcast/interview audio — denoise, de-hum, dialogue level, music duck under voice |
| `davinci-resolve-titles-and-lower-thirds` | Branded titles and animated lower-thirds without leaving Resolve |
| `davinci-resolve-export-multi-platform` | Export the same edit for YouTube (16:9), LinkedIn (square), Shorts (9:16), plus automate it |
| `davinci-resolve-troubleshooting` | Diagnose the 5 most common "why is X broken" moments |
| `davinci-resolve-computer-use-training` | Work through Blackmagic lesson homework with Computer Use, record evidence, and turn UI lessons into better production skills |
| `davinci-resolve-social-editor` | Build speaker-led social edits with semantic cuts, B-roll, captions, audio checks, and Resolve handoff |
| `social-video-folder-autocutter` | Turn a hard-drive folder into repeatable Instagram/YouTube cut briefs, B-roll plans, and eval artifacts |

See `docs/jtbd-map.md` for the mapping from jobs to skills.

## The two-layer reference model

Each skill points at two layers of reference material:

1. **Deep wikis (`docs/wiki/`)** — working summaries the agent reads as context. One per Blackmagic PDF, plus a master index. These cover chapter structure, key concepts, workflows, shortcuts, and common pitfalls. Per-chapter page ranges are listed at the end of each notes block.

2. **PDF page ranges** — the ground truth. Blackmagic publishes six free training PDFs for Resolve 20, totaling around 1,800 pages. Download them from Blackmagic and keep them locally; skills cite specific page ranges as a reset mechanism.

The flow:

- Agent reads the wiki as working memory before answering.
- If the user pushes back, the agent reads the cited PDF page range to reset its mental model — then re-answers.
- The agent does not invent technique; it summarizes what the PDFs say.

This is the core design idea. Wikis are fast context. PDFs are the truth layer when context drifts.

## Installation

### Option 1: Copy each skill directory to `~/.claude/skills/`

```bash
git clone https://github.com/ChaiWithJai/davinci-resolve-claude-skills.git
cp -R davinci-resolve-claude-skills/skills/* ~/.claude/skills/
```

Claude Code picks up skills in `~/.claude/skills/` automatically.

### Option 2: Symlink the whole skills directory

```bash
git clone https://github.com/ChaiWithJai/davinci-resolve-claude-skills.git
cd davinci-resolve-claude-skills
for skill in skills/*/; do
  name=$(basename "$skill")
  ln -s "$(pwd)/$skill" "$HOME/.claude/skills/$name"
done
```

Symlinking lets you `git pull` updates without re-copying.

### Option 3: Project-local skills

If you want the skills available only inside one repo, put them in `<repo>/.claude/skills/` instead of `~/.claude/skills/`.

## How to use

The skills auto-trigger when their description matches what you are asking for. For example:

- "My screen recording is too long, help me cut it down" → triggers `davinci-resolve-cut-screen-recording`
- "How do I make my webcam look better" → triggers `davinci-resolve-color-grade-webcam`
- "The music in my podcast is drowning out the host" → triggers `davinci-resolve-audio-cleanup-podcast`
- "Export my edit for LinkedIn and YouTube" → triggers `davinci-resolve-export-multi-platform`
- "Make this folder into an Instagram Reel and YouTube cut" → triggers `social-video-folder-autocutter`
- "Fix the jump cuts, audio, captions, B-roll, and Resolve handoff" → triggers `davinci-resolve-social-editor`

You can also reference a skill explicitly: "use the davinci-resolve-color-grade-webcam skill on this footage."

## Production Standard

The current bar is not "a video exists." The bar is:

- the story is coherent enough for a stranger to understand,
- warm traffic immediately knows why the workshop matters,
- dialogue is clean and dominant on phone speakers,
- captions are burned in, timed to actual speech, and proofread,
- B-roll proves claims or covers cuts instead of decorating the frame,
- the color grade is bright, vibrant, and skin-tone safe,
- the Resolve artifact remains layered enough for a human editor to take over.

The strongest loop we learned is simple: when a cut is close, preserve the liked picture edit and fix the exact defect. For the latest Chai With Jai pass, that meant a caption-only finishing pass from word-level speech timing, followed by phone-safe still and loudness verification.

## Python automation

Several skills include Python scripts that drive Resolve through its external scripting API or prepare verified edit artifacts:

- `skills/davinci-resolve-cut-screen-recording/scripts/auto_silence_cut.py`
- `skills/davinci-resolve-export-multi-platform/scripts/multi_platform_render.py`
- `skills/davinci-resolve-computer-use-training/scripts/`
- `skills/davinci-resolve-social-editor/scripts/`
- `skills/social-video-folder-autocutter/scripts/`

To run these scripts you must enable external scripting in Resolve:

1. DaVinci Resolve > Preferences > System > General
2. Set External scripting using to **Local** (or **Network** if running remotely)
3. Click Save

Then either:

- Run from inside Resolve: Workspace > Console > Py3
- Or run from your shell:

  ```bash
  # macOS
  export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
  export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
  export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
  python3 skills/davinci-resolve-cut-screen-recording/scripts/auto_silence_cut.py
  ```

Resolve must be open with a project loaded. The scripts attach to the running Resolve instance via `DaVinciResolveScript.scriptapp("Resolve")`.

## Source documentation

The wikis under `docs/wiki/` summarize the six Blackmagic Design DaVinci Resolve 20 training PDFs:

- *The Beginner's Guide to DaVinci Resolve 20* (Roberts, Hall — 2025)
- *The Editor's Guide to DaVinci Resolve 20* (Roberts — 2025)
- *The Colorist Guide to DaVinci Resolve 20* (Fissoun — 2025)
- *The Fairlight Audio Guide to DaVinci Resolve 20* (Plummer — 2025)
- *The Visual Effects Guide to DaVinci Resolve 20* (Allen, Gallardo, Scoppettuolo — 2025)
- *Advanced Visual Effects in DaVinci Resolve 20* (Allen, Scoppettuolo — 2025)

Download the PDFs free from `https://www.blackmagicdesign.com/products/davinciresolve/training`.

The Python scripting API is documented in `DaVinci Resolve/Developer/Scripting/README.txt` shipped with the application installer.

## Contributing

Open issues and PRs welcome. Please:

- Cite specific PDF page numbers for any new technical claims
- Keep `description:` frontmatter focused on triggering conditions, not workflow summaries
- Add a `Verification` section to every new skill
- If you add a Python script, mark untested API calls clearly

## License

MIT. See `LICENSE`.

## About

Built by Jai Bhagat. More at chaiwithjai.com.

---

## FILE: skills/davinci-resolve-audio-cleanup-podcast/SKILL.md

---
name: davinci-resolve-audio-cleanup-podcast
description: Use when a user has podcast, interview, or talking-head audio that needs cleanup — denoise, de-hum, level dialogue, and duck music under voice. Triggering symptoms include phrases like "podcast audio is noisy", "background hum in interview", "music too loud under voice", "level out my voiceover", "fix my podcast", or any DaVinci Resolve Fairlight audio cleanup question.
---

# DaVinci Resolve — clean podcast and interview audio

## Overview

The four-step podcast audio cleanup chain: **EQ out rumble -> kill any hum -> denoise -> level -> duck music**. Done in this order. The principle: address frequency problems before dynamic problems. EQ is surgical; noise reduction is destructive. Use the surgical tool first so the destructive tool has less to do.

## When to use

Symptoms:
- Recording has background hum (electrical 50/60 Hz interference)
- Air conditioning, refrigerator, or traffic noise floor under dialogue
- Voice levels vary from clip to clip (loud intros, quiet thoughtful moments)
- Music score drowns out the host when they start talking
- Sibilance ("ess" sounds) too harsh

When NOT to use:
- Multi-mic interview where you need to gate each mic separately — that needs the Track-level Dynamics workflow per mic (Fairlight Audio Post pp. 373-375).
- Audio is destroyed (clipped, severe wind noise, water damage) — there is a limit to what cleanup can do. Re-record if possible.
- You need surround/Atmos mixing — different chapter (Fairlight Audio Post pp. 643+).

## Quick reference — the cleanup chain in order

### Phase -1 — source audit before cleanup

Before applying effects, audit every candidate audio source. Do not assume the named lav/boom file is best. Check:

- duration matches picture
- silence percentage
- integrated LUFS
- true peak
- clipping risk
- audible room tone/hum
- whether the track is actually silent

For multi-camera workshop folders, keep the selected dialogue on `A1`, the processed dialogue on `A2`, music/ambience on `A3`, and SFX/bumpers on `A4`. If the external mic peaks near `0 dBFS`, preserve it as source but create a processed duplicate with conservative limiting/leveling before delivery.

| Step | Tool | When to use | Where |
|---|---|---|---|
| 1. EQ rumble | **Clip EQ** (Inspector > Equalizer) | Always — every dialogue clip has sub-100Hz garbage | Inspector panel, audio clip selected |
| 2. De-Hummer | **Fairlight FX > De-Hummer** | Power line buzz (50 Hz Europe, 60 Hz US) | Drag from Effects Library onto clip |
| 3. Gate the noise floor | **Mixer > Dynamics > Gate** | Air conditioner / room tone audible between sentences | Mixer track dynamics panel |
| 4. Noise Reduction | **Fairlight FX > Noise Reduction** | Stubborn broadband noise that survives steps 1-3 | Drag from Effects Library onto clip or track |
| 5. AI Dialogue Leveler | **Inspector > AI Dialogue Leveler** (Studio) or manual keyframes | Voice gets loud/quiet within a sentence | Inspector Track FX section |
| 6. Ducker | **Track FX > Ducker** | Music too loud under dialogue | Inspector on the music track |

## Steps

### Phase 0 — Switch to Fairlight, set up your monitoring

1. Press **Shift-7** to switch to the Fairlight page.
2. Open the Mixer (Toolbar > Mixer button).
3. Put on headphones. You will hear problems on headphones that you will miss on laptop speakers.

### Step 1 — Clip EQ: cut everything below 80 Hz (always)

This is non-negotiable. Every voice recording has rumble, HVAC, traffic, and breath plosives under 80 Hz that contribute nothing to intelligibility but eat up headroom.

1. Select a dialogue clip in the timeline.
2. Open the **Inspector** (top right of the interface, then Audio tab).
3. Scroll down to **Equalizer**. Turn it ON (the radio button next to "Equalizer").
4. By default, Bands 2-5 are enabled. Set **Band 2** to **Low Shelf** (the first icon in the Band Filter Type dropdown).
5. Drag the Band 2 handle in the graph **down to -70 dB** and **right until the shelf reaches the 80-100 Hz line**.
6. Repeat for every dialogue clip — or **copy attributes** from this clip to all others (Cmd-C on the clip, select others, Edit > Paste Attributes, check Equalizer only, Apply).

Fairlight Audio Post pp. 368-372 walks through this with the same EQ controls.

### Step 2 — De-Hummer for any electrical hum

If you hear a constant tone behind the voice — usually a low buzz at 50 Hz or 60 Hz from poor cable shielding or a ground loop — use the De-Hummer.

1. Open the **Effects Library** (top-left button on Fairlight page).
2. Under **Audio FX > Fairlight FX**, find **De-Hummer**.
3. Drag De-Hummer onto the affected clip in the timeline.
4. In the De-Hummer window, click **60 Hz** (or 50 Hz if you are in Europe / Asia / Africa).
5. Drag the **Amount** knob right until the hum disappears. Typical setting: `-20 to -30 dB`.
6. Adjust the **Slope** knob slightly right if you still hear harmonics (multiples of 60 Hz — 120, 180, 240).
7. Click the **Bypass** switch at the top to A/B compare. The Bypass switch is red when the filter is on.

Fairlight Audio Post pp. 376-380 covers this exactly. The trick is that the De-Hummer is a *notch filter* — it removes specific frequencies without affecting nearby ones, unlike EQ.

### Step 3 — Gate the noise floor (track-level dynamics)

If there is a low-level hiss, computer fan, or AC noise that is *audible between sentences but masked when the voice is playing*, a gate kills it.

1. In the **Mixer**, find the dialogue track's channel strip.
2. Double-click the **Dynamics** section to open the Dynamics panel.
3. Click the **Gate** button to enable.
4. Start with these settings:
   - **Threshold**: -35 dB (default)
   - **Range**: -18 dB (start conservative)
   - **Attack**: 1.4 ms
   - **Hold**: 0 ms
   - **Release**: 93 ms
5. Play back the track. The Gain Reduction meter should activate only between sentences (when no voice). If the gate cuts off the start of words, raise the threshold (less negative). If it cuts off breaths or quiet sentence endings, lower the range.

The exact starting values come from Fairlight Audio Post pp. 373-375.

### Step 4 — Noise Reduction (when steps 1-3 are not enough)

Some recordings have broadband noise (general "hisssss") that EQ cannot remove and the gate would chop up too aggressively. Use the Fairlight FX Noise Reduction.

1. From the Effects Library > **Audio FX > Fairlight FX**, drag **Noise Reduction** onto the affected clip.
2. The Noise Reduction panel opens. You have two modes:
   - **Manual** (default) — you "teach" the plug-in what the noise sounds like
   - **Auto Speech Mode** — algorithm separates speech from noise automatically
3. **For Auto Speech Mode**: just enable it. Adjust the **Dry/Wet** slider (default 80%). Lower it if voices start sounding "underwater."
4. **For Manual mode**:
   a. Find a section of the clip with *only noise* (silent gap, ideally at the start before anyone speaks).
   b. Click **Learn** to enable noise-profile capture.
   c. Play the noise-only section.
   d. Click **Learn** again to stop. The plug-in has now "learned" the noise.
   e. Play back the full clip — noise should drop dramatically.

Fairlight Audio Post pp. 381-383 covers both modes. Studio version only — free Resolve does not have the Noise Reduction plug-in. Free users: use a more aggressive Clip EQ (step 1) combined with the Gate (step 3).

### Step 5 — AI Dialogue Leveler (Studio) or manual keyframes (Free)

Voices have natural dynamic range — a person gets quieter as they finish a sentence. The leveler evens this out.

**Studio approach** (one click):

1. Select the dialogue clip.
2. In the Inspector > **Track FX** section, enable **AI Dialogue Leveler**.
3. That is it. Adjust the strength slider if it sounds too "compressed."

**Free Resolve approach** (manual keyframes):

1. In the Edit page, Option-click (Mac) / Alt-click (Windows) the volume bar in an audio clip to add keyframes.
2. Add a keyframe before a quiet section, another keyframe after.
3. Drag the volume bar between keyframes up (typically +3 to +6 dB) to boost the quiet section.

Beginner's Guide pp. 150-153 covers the manual keyframe workflow with screenshots.

### Step 6 — Duck the music under dialogue

If you have music underneath voice and the music swallows the voice, use the Ducker.

1. Select the **MUSIC** track (or the music clip).
2. In the Inspector > **Track FX** section, enable **Ducker**.
3. In the Ducker controls:
   - **Source 1** dropdown: set to your dialogue track (e.g. DIALOGUE).
   - **Duck Level**: start at **2.7** dB (the default — a subtle duck).
   - If you have multiple dialogue tracks (host + guest), click the **+** to add Source 2 and Source 3.
4. Play back. Watch the Ducker Graph — when dialogue plays, the music level dips automatically.
5. If the duck is too dramatic, lower Duck Level. If you cannot hear the voice over music, raise Duck Level.

Fairlight Audio Post pp. 552-558 covers Ducker in depth, including the warning that **Duck Level > 5 dB sounds amateurish** because the audience perceives the dip.

## Common mistakes

- **Applying Noise Reduction first, then EQ** -> wrong order. EQ out the obvious frequencies first so the Noise Reduction has less to remove and is less destructive. **(This is the misconception this skill addresses head-on.)** Fairlight Audio Post p. 368-372 establishes EQ before p. 381-383 noise reduction for this reason.
- **Setting the Gate threshold too high** -> it cuts off the start of each word. Listen carefully and back the threshold off.
- **Cranking the Ducker Duck Level above 5 dB** -> the audience hears the level swing and it feels artificial. Stay subtle.
- **Forgetting that the Bypass switch is RED when ACTIVE** -> the convention is inverted from what you might expect. Red = filter is engaged.
- **Trying to fix wind noise** -> the Fairlight FX cannot meaningfully fix wind. Re-record or use iZotope RX externally.

## Verification

You succeeded if all of the following are true:

1. Listening on headphones at moderate volume, you cannot hear hum, hiss, or AC noise between sentences.
2. The loudness meter (top right of Fairlight) reads between -16 and -20 LUFS over the entire timeline (this is podcast-standard loudness).
3. Voice clips peak at around -9 dBFS to -3 dBFS but never clip (red).
4. Music plays at full volume when there is no voice, ducks audibly but smoothly when voice starts, returns to full when voice ends.
5. Bypassing the Clip EQ on the dialogue clip makes the audio sound noticeably "boomier" and worse — the EQ is doing something audible.

## Transfer

Now try this on a 3-person podcast where each person has their own mic (so three separate dialogue tracks). The cleanup chain is the same per track, but the Ducker setup changes: in the music track's Ducker, add Source 1, 2, and 3 pointing at each of the three dialogue tracks. The music will duck when *any* of the three is speaking. If two people talk over each other, the duck does not stack — you get the same -2.7 dB dip whether one or three voices are active.

## Working reference

- `docs/wiki/fairlight-audio-post.md#lesson-6--audio-repairs-pp-367-415` (full cleanup chain — primary)
- `docs/wiki/fairlight-audio-post.md#lesson-9--mixing-and-sweetening-pp-535-612` (Ducker setup)
- `docs/wiki/beginners-guide.md#lesson-3--audio-editing-and-quick-export-pp-141-179` (free Resolve fallback — manual keyframes + Fairlight FX)
- `docs/wiki/editors-guide.md#lesson-8--audio-editing-pp-475-543` (AI Dialogue Leveler reference)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (audio symptom rows — hum, hiss, ducker)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports remaining hum, hiss, robotic ducking, or that the chain order was different, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 368-372 (Clip EQ for low-frequency reduction)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 373-375 (Dynamics Gate, gating low-level noise)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 376-380 (De-Hummer for power line hum)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 381-389 (Noise Reduction — manual and Auto Speech Mode)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 552-558 (Ducker — Duck Level cap at 5 dB)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 142-158 (manual keyframes + Fairlight FX for free Resolve)
- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 514 (AI Dialogue Leveler one-click voice leveling)

---

## FILE: skills/davinci-resolve-color-grade-webcam/SKILL.md

---
name: davinci-resolve-color-grade-webcam
description: Use when a user wants webcam, interview, or talking-head footage to look broadcast-quality — corrects exposure, white balance, skin tones, and overall color. Triggering symptoms include phrases like "my webcam footage looks dull", "skin tones look orange/green", "wash out background", "make the face pop", "match shots from two cameras", or any DaVinci Resolve color page question for talking-head content.
---

# DaVinci Resolve — color grade webcam and talking-head footage

## Overview

Three primary corrections + one secondary on a skin-tone qualifier = footage that looks like it cost money. The core principle: **read the waveform scope, do not trust your laptop screen.** Laptop displays are uncalibrated; the scope tells you objectively whether the shadows are crushed or the highlights are clipped.

## When to use

Symptoms:
- Webcam footage looks dull, flat, or washed out
- Skin looks orange / green / too red
- Two cameras (e.g. your face cam and a co-host's) do not match
- Want a consistent "look" across episodes
- The phrase "make it look more professional"

When NOT to use:
- You are shooting RAW (.braw, .ari, .r3d) — that needs the **HDR Wheels** workflow (Colorist Guide pp. 393-406).
- You need to fix a green-screen shot — that is Fusion territory (Fusion VFX Guide ch. 5).
- The footage is already graded and you want to *match* it to a reference — that is a shot-matching workflow (Colorist Guide pp. 46-71).

## Quick reference

The grade is a 4-node tree on the Color page:

| Node | Job | Primary tool |
|---|---|---|
| **Node 1: Normalize** | Set black and white points using the waveform | Lift + Gain master wheels |
| **Node 2: Balance** | Neutralize color cast | Lift + Gain *color* wheels |
| **Node 3: Contrast** | Add midtone punch | Contrast + Pivot at the top of the Primaries palette |
| **Node 4: Skin tones** | Refine just the face | HSL Qualifier + a power window |

## Steps

### Prep — switch to the Color page and bring up the scopes

1. Press **Shift-6** to go to the Color page.
2. Click the **Scopes** palette button (right side of the page).
3. Set the scope dropdown to **Waveform** (this shows luminance and color channels stacked).
4. Select your first webcam clip in the thumbnail strip at the top.

The waveform is your truth source. Everything you do below should be visually verified on it.

### Node 1 — Normalize (set black and white points)

1. Confirm the **Primaries — Color Wheels** palette is active in the left panel.
2. Find the **Lift** wheel (leftmost). The horizontal slider below it is the **Lift master wheel**.
3. Drag the Lift master wheel left until the darkest area of the waveform sits just above the 0 line (around 5-10 % luminance, which is approximately the 64 line on a 1023-line scope).
   - For webcam footage shot in a normal room, this typically means dragging Lift down to around `-0.02 to -0.05`.
4. Find the **Gain** wheel (rightmost). Drag its master wheel until skin-tone highlights sit between 50-75% of the scope height.
   - Watch the highest peaks — you want them at roughly the 768 line on the 1023 scale.
5. Find the **Gamma** wheel (middle). Drag its master wheel right to brighten midtones so the face is well-lit but not blown out.
6. At the top of the Primaries palette, adjust **Contrast** to `1.1 - 1.2` and **Pivot** to `0.3` for a punchier mid-range.

Colorist Guide pp. 11-15 walks through this in detail.

### Node 2 — Balance (neutralize the color cast)

1. Right-click the node in the **Nodes** panel > **Add Node > Add Serial** to add Node 2.
2. Look at the waveform — the RGB channels should overlap (white trace) for neutral areas of the image. If you see a band of one color riding above the others, that is the cast.
3. Use the **Lift** *color wheel* (drag the center dot, not the master wheel) to push the shadows toward the *complementary* color of any cast you see.
   - If the shadows are too red (a common webcam issue from indoor lighting), drag Lift toward cyan.
   - If the shadows are too blue (daylight through a window), drag Lift toward yellow.
4. Do the same with the **Gain** *color wheel* for the highlights.
5. Use Resolve's **Qualifier Focus** trick: from the Scopes palette options menu, enable **Display Qualifier Focus**. Hover the mouse over a neutral area in the viewer (a white wall, a piece of paper) — the scope shows the RGB values under your cursor. Aim to get those three values to overlap (= neutral).

Colorist Guide pp. 16-19 covers this exact workflow.

### Node 3 — Contrast (already partially done in Node 1)

If you set Contrast in Node 1, you can skip this node. Some colorists prefer a dedicated contrast node so they can disable it independently. Up to you.

### Node 4 — Skin tone refinement (HSL Qualifier + Power Window)

This is the secret sauce. Even a perfectly balanced face benefits from a tiny saturation boost and slight warmth on the skin only.

1. Add Node 4 (right-click Node 3 > Add Serial).
2. In the left palette, switch from Primaries to **Qualifier**.
3. Set the qualifier mode to **HSL** (default).
4. Click the **eyedropper** in the Qualifier palette, then click on a clean patch of skin in the viewer.
5. Refine the selection by adjusting the Hue / Saturation / Luminance range sliders. Toggle the **Highlight** button (top of the viewer) to see the matte — you want only the skin selected.
6. Switch back to **Primaries**. Any adjustment now only affects the qualified skin.
7. Push **Gain color wheel** slightly toward orange (warmer skin). Increase **Saturation** to ~60 (default is 50).
8. To prevent the qualifier from triggering on background objects with skin-tone colors (wooden furniture, beige walls), add a **Power Window** in the Window palette > Linear or Circle shape > draw it loosely around the face. The qualifier + window combine — only skin *inside the window* gets the boost.

Colorist Guide pp. 118-138 covers the full skin-tone refinement workflow (Enhancing Skin Tones with Face Refinement uses the Studio-only AI face detector; the manual qualifier + window approach works on free Resolve).

### Save the node tree as a PowerGrade so you can reuse it

1. Right-click in the Gallery panel (bottom-left of Color page) > **Add to PowerGrade**.
2. Name the still `WEBCAM_LOOK_v1`.
3. To apply to a future clip: select the new clip, right-click the saved still in the Gallery > **Apply Grade**.

Colorist Guide pp. 246-250 covers saving grades for reuse.

## Common mistakes

- **Adjusting by eye on an uncalibrated laptop screen** -> the colors you see on a MacBook are not the colors your audience sees on their phone, TV, or monitor. Always check the waveform. The waveform does not lie.
- **Cranking Saturation to 70+** -> faces start to look orange and fake. Stay under 60. The Saturation control is in the Primaries palette options at the bottom.
- **Skipping Node 1 normalization and going straight to creative grading** -> you are stacking creative choices on top of broken footage. Always normalize first.
- **Using the same grade on footage shot under different lighting** -> a "WebcamLook" grade tuned for tungsten room lights will look wrong under daylight. Either re-grade per scene, or use the **Color Match** feature (Colorist Guide pp. 52-69) to use a color chart as reference.
- **Forgetting to disable the qualifier highlight after refining** -> the matte preview stays on and you cannot see your real adjustments. Press the Highlight button at the top of the viewer to toggle it off.

## Verification

You succeeded if all of the following are true:

1. **Scope check**: the waveform trace fills most of the 0-1023 range. The darkest part sits near 50-100 (not 0). The brightest part sits near 700-900 (not 1023, unless you have intentional specular highlights).
2. **RGB overlap check**: in a neutral area (white wall, paper), the R, G, B traces overlap to form a white trace.
3. **Skin check**: faces are not pulled toward orange / green / red.
4. **Before/after check**: press **Cmd-D** (or Ctrl-D) to toggle the grade on and off. The "after" should look noticeably more dimensional than the "before."
5. The saved PowerGrade still is in your Gallery and applies cleanly to a different clip.

## Transfer

Now try this: apply the same grade to a clip shot under daylight (natural window light). The Lift wheel adjustment will likely be smaller because daylight already pushes shadows toward blue. The Temp slider at the top of the Primaries palette may need to come down (cooler). Skin-tone qualifier should still work — but the Power Window may need to be redrawn if the face is at a different position in the frame.

## Working reference

- `docs/wiki/colorist-guide.md#lesson-1--balancing-footage-pp-3-43` (primary grading with wheels, scope reading — primary)
- `docs/wiki/colorist-guide.md#lesson-3--correcting-and-enhancing-isolated-areas-pp-73-139` (qualifier + window for skin tones)
- `docs/wiki/colorist-guide.md#lesson-6--managing-grades-across-clips-and-timelines-pp-225-259` (PowerGrade save/reuse)
- `docs/wiki/beginners-guide.md#lesson-4--performing-primary-color-corrections-pp-189-245` (gentle starter workflow)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (skin-tone and shot-match symptom rows)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports that skin tones still look orange/green, the grade is washed out, or RGB doesn't overlap on neutral patches, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 11-19 (Primary Grading with Color Wheels, normalization workflow)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 16-19 (Balancing Colors with Master Wheels, RGB overlap trick)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 118-138 (Skin-tone refinement, qualifier + window workflow)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 246-250 (Saving Still Templates for Other Projects — PowerGrade)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 12-15 (Setting Tonal Range with Master Wheels, scope reading)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 189-245 (Primary Color Corrections — alternative starter workflow)

---

## FILE: skills/davinci-resolve-computer-use-training/SKILL.md

---
name: davinci-resolve-computer-use-training
description: Use when the user wants Codex to learn DaVinci Resolve through Blackmagic Design lesson homework, operate the Resolve UI with Computer Use, validate skills against real Resolve behavior, or build a capstone workflow that turns local/T7 media into Instagram and YouTube cuts.
---

# DaVinci Resolve Computer Use Training

Use this skill for lesson-by-lesson Resolve practice and for improving Resolve skills from observed UI behavior.

## Automation Priority

Default to DaVinci Resolve's supported scripting and preset systems before UI automation:

1. Use the official Resolve Python/Lua scripting API for project setup, media import, timeline construction, markers, render queue work, preset import/export, and verification.
2. Use installed Workspace scripts, render presets, burn-in presets, layout presets, Fusion macros/templates, PowerGrades/LUTs, and reusable project templates for batteries-included repeatability.
3. Use Computer Use for UI homework, screenshot evidence, manual HITL validation, and controls the scripting API cannot expose.
4. Use external tools such as `ffprobe`, `ffmpeg`, Whisper/Gemini, Rust/Python edit planners, and audio/video analyzers around Resolve; materialize final decisions back into editable Resolve timelines.

Before any lesson or production edit, run or emulate `scripts/resolve_doctor.py` to confirm process state, scripting paths, Resolve version, current project/timeline, current page, database, and timeline start frame.

Use `bin/resolve-kit` for repeatable local execution:

- `resolve-kit doctor`
- `resolve-kit install`
- `resolve-kit stage-folder <folder>`
- `resolve-kit validate --project <name> --timeline <name>`
- `resolve-kit capstone <folder>`

## Core Loop

For every lesson:

1. Read the lesson map entry and the cited PDF page range.
2. Create a homework card with objective, required media/project, UI pages, expected artifact, and validation checks.
3. Use Resolve scripting for setup, inspection, and repeatable verification. Use Computer Use for the UI steps when the point is specifically to learn Resolve operation or validate HITL controls.
4. Capture evidence: screenshot/state notes, project/timeline name, exported file path, markers, and any logs.
5. Record failure modes: inaccessible control, wrong page, missing media, UI ambiguity, scripting mismatch, render/export failure, or quality failure.
6. Update the relevant production skill if the lesson teaches a durable workflow or catches a bad assumption.

## Computer Use Rules

- Start each UI session with `get_app_state` for DaVinci Resolve.
- Prefer accessibility element clicks. Use coordinates only when the Resolve canvas/tool surface exposes no useful element.
- After each meaningful action, call `get_app_state` or use the action result to verify the UI changed.
- Do not use UI automation for long repeated setup if Resolve scripting can do it more reliably. Use scripts to stage projects, then Computer Use to learn/edit/verify the interaction.
- If `list_apps` or `get_app_state` times out, do not claim the UI lesson is complete. Verify the Resolve process and scripting API, record the bridge failure in the lesson journal, and only use scripting to stage a practice artifact or inspect the project.
- Resolve scripting API availability varies by install. Prefer project timeline lookup by index when name-based lookup is unavailable, save through `ProjectManager.SaveProject`, and always use `timeline.GetStartFrame()` when placing clips so media appears at Resolve's `01:00:00:00` timeline origin.
- Keep a per-lesson journal in `training_runs/<book>/<lesson>/journal.md`.
- Keep screenshots or stills in the same folder when possible.

## Resolve Scripting Rules

- Use the local SDK paths from `references/resolve-automation-stack.md`.
- Always set `RESOLVE_SCRIPT_API`, `RESOLVE_SCRIPT_LIB`, and `PYTHONPATH`/`sys.path` before importing `DaVinciResolveScript`.
- Keep reusable scripts installable under the user's Resolve Scripts folder so they can be invoked from Workspace > Scripts.
- Prefer importing render, burn-in, layout, Fusion macro, and project-template assets over recreating equivalent state through UI clicks.
- Save through `ProjectManager.SaveProject()`.
- Validate by reading the project/timeline back through the API after writing.
- Never flatten the handoff unless the user asks for a flat render only; preserve layered tracks, markers, disabled repair/reference tracks, captions, and B-roll.

## Homework Card Schema

Each lesson should produce a JSON or Markdown card with:

- `book`
- `lesson_number`
- `lesson_title`
- `pdf_pages`
- `target_resolve_pages`
- `homework_objective`
- `source_media_needed`
- `ui_actions_to_learn`
- `automation_candidates`
- `expected_artifact`
- `validation_checks`
- `skill_updates`

## Skill Validation

When validating `davinci-resolve-claude-skills`:

- Check whether a skill cites the correct PDF lesson/page range.
- Check whether it has a verification section.
- Check whether it distinguishes UI-only steps from scripting API steps.
- Check whether Studio-only features are clearly marked.
- Check whether it handles failures discovered by prior video-editing traces: bad audio, missing captions, flattened timelines, frame offsets, stale media pool items, subject out of frame, and transcript-only jump cuts.

## Capstone Contract

The capstone must prove the full workflow:

- Input: any local or T7 folder with camera/audio/media assets.
- Output 1: Instagram vertical cut, target up to 3 minutes, speaker-first, burned-in captions, B-roll, audio in social loudness range.
- Output 2: YouTube/long-form 16:9 cut, up to 12 minutes, coherent story, clean audio, graded visuals.
- Resolve handoff: layered editable timelines, disabled repair/reference tracks, markers, edit decisions, B-roll plan, captions, and render verification.
- Website bridge: markdown or copy block for `chaiwithjai.com/workshops` using the video story.

## Anti-Reward-Hacking Gate

Never count a Loom upload, flat render, generated preview, or seed timeline as the capstone. Those are distribution or scaffolding artifacts only.

Never count shared screenshots across all lessons as lesson completion. Page visibility proves only that the app opened. It does not prove the class/homework concept was performed.

Before calling homework or capstone complete, produce an auditable proof bundle:

- `homework_coverage_matrix.md/json` covering every mapped workbook lesson.
- Per-lesson `homework_card.json`, `journal.md`, and `validation_report.md`.
- A clear status for each lesson:
  - `manual_ui_verified` only when Computer Use or human UI evidence proves the Resolve UI homework was performed.
  - `manual_ui_screenshot_verified` when Resolve's supported scripting/menus navigate the live app and macOS screenshots prove the UI state, because Computer Use is known to time out against Resolve on this machine.
  - `script_api_verified` when Resolve scripting created and read back the artifact.
  - `capstone_applied_script_verified_ui_blocked` when the lesson was applied to the capstone through scripting but Computer Use timed out.
  - `not_started` when there is no proof.
- Capstone acceptance report tying lesson groups to concrete Resolve timelines, source clips, captions, audio checks, color/visual checks, renders, and website copy.

If Computer Use times out, do not say the UI homework is complete. Record the timeout and continue with supported Resolve scripting for practical progress.

## DeepWiki Benchmark Gate

Before saying a capstone follows the classes, benchmark it against the local DeepWiki at the repo DeepWiki under `docs/wiki/` and fail it honestly when the artifact lacks the workbook competency.

Required capstone competency groups:

- Editing: semantic A-roll spine, B-roll over jumps, multicam/synced angle strategy, subject-safe vertical reframing, proofread captions.
- Fairlight: source/processed/music/SFX lanes, cleanup order proof (`Clip EQ -> De-Hummer -> Gate -> Noise Reduction -> Leveler`), music ducking below dialogue, LUFS/dBTP verification.
- Color: scope-based primary correction, named node order (`Normalize -> Balance -> Enhance -> Skin/Secondaries`), shot matching across cameras, vibrant but non-crushed delivery.
- Fusion/graphics: Text+ or Fusion caption/lower-third system, reusable macro/template for titles/bumper, editable graphics on separate tracks.
- Delivery: separate Instagram and YouTube timelines, presets/validation, project export, and human-editable handoff.

Status rules:

- `PASS` only when the Resolve artifact or exported audit proves the competency.
- `PARTIAL` only when the competency exists but lacks workbook-grade proof or editability.
- `FAIL` when the artifact uses a flat/rendered shortcut, screenshot-only proof, or omits the workflow.

Write the benchmark to `resolve_kit/status/deepwiki_capstone_benchmark_*.md/json` and let it drive the next repair pass. A capstone under 85/100 is not publish-ready and must not be described as class-complete.

## Source Workbook Benchmark Gate

The DeepWiki is not enough when the user asks whether the work follows the classes. The source-workbook benchmark must run against all 52 mapped workbook lessons using `references/resolve20-homework-map.md` and local PDF text exported from the Blackmagic workbooks, or the configured `RESOLVE_PDF_TEXT_DIR`.

Rules:

- Score every mapped lesson as `PASS`, `PARTIAL`, or `FAIL`.
- `PASS` requires workbook-grade/native Resolve evidence for that lesson's actual tool or workflow.
- `PARTIAL` is allowed only for adjacent production evidence that does not prove the native workbook workflow.
- `FAIL` is required for omitted lessons, pre-rendered shortcuts, screenshots that only show page visibility, or features represented by assets instead of Resolve workflows.
- If the source-workbook score is under 85/100, do not call the homework or capstone complete.
- If the user asked to do all homework, advanced/irrelevant lessons still fail unless there is a separate lesson artifact proving them; do not mark them N/A just because they are unnecessary for the capstone.

Write the source-workbook benchmark to `resolve_kit/status/source_workbook_capstone_benchmark_*.md/json` and report the score before attempting any further hillclimb.

## Workbook-Derived Quality Bar

Across the 52 mapped lessons, carry these checks into every production capstone:

- Editing: cut on semantic beats, preserve audio continuity, use B-roll to cover jumps, and expose markers for HITL review.
- Audio: select the best source by audit and listening, clean rumble/hum/noise before leveling, duck music under speech, and verify loudness.
- Color: balance and match cameras before stylizing; for Chai With Jai, target vibrant broadcast/documentary color without crushed shadows.
- Fusion/graphics: captions, titles, lower thirds, bumpers, and reference overlays must stay editable on separate tracks.
- Delivery: produce separate Instagram and YouTube timelines, validate aspect ratio, safe zones, captions, audio, and render playback.
- Automation: prefer Resolve API, macros, presets, and templates; use Computer Use for UI proof only.

## References

- `references/resolve20-homework-map.md` for the full book/lesson map.
- `references/computer-use-journal-template.md` for per-lesson journals.
- `references/resolve-automation-stack.md` for the supported Resolve scripting, preset, macro, and Computer Use hierarchy.

---

## FILE: skills/davinci-resolve-computer-use-training/references/computer-use-journal-template.md

# Computer Use Journal Template

```markdown
# {Book} Lesson {N}: {Title}

## Objective

## Setup

- Project:
- Timeline:
- Media:
- PDF pages:

## UI Actions Practiced

1.

## Evidence

- Screenshots:
- Exports:
- Resolve project/timeline:

## Validation

- Expected:
- Observed:
- Pass/fail:

## Failure Modes

## Skill Updates

## Next Lesson Notes
```

---

## FILE: skills/davinci-resolve-computer-use-training/references/resolve-automation-stack.md

# Resolve Automation Stack

Use DaVinci Resolve's supported automation surfaces in this order.

## 1. Resolve Scripting API

Default to the official Python/Lua scripting API for repeatable operations:

- project/database inspection
- bin creation and media import
- timeline creation and clip placement
- marker creation
- page switching with `resolve.OpenPage(pageName)`
- layout preset import/export
- render preset import/export
- burn-in preset import/export
- render queue setup and render status polling
- project export/archive

Local SDK paths on macOS:

```bash
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

The official SDK README and examples are installed at:

- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/README.txt`
- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples`
- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/DaVinciResolveScript.py`

Resolve must be running unless deliberately launched in `-nogui` mode. For normal HITL editing, keep the UI running.

## 2. Installed Workspace Scripts

For actions the user may invoke manually, install scripts into Resolve's Workspace > Scripts menu.

macOS locations:

- All users: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts`
- Current user: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts`

Use subfolders by surface:

- `Utility` for all pages
- `Edit`, `Color`, `Deliver`, etc. for page-specific scripts
- `Deliver` scripts also appear under render jobs

Preferred skill pattern:

1. Generate/edit a script in the skills repo.
2. Copy or symlink it into the user Scripts folder.
3. Verify Resolve sees it after restart or script refresh.
4. Keep a command-line entrypoint for automation and a menu entrypoint for HITL.

## 3. Presets, Templates, and Macros

Use Resolve-native assets for reusable production looks:

- Layout presets for consistent UI state.
- Render presets for Instagram, YouTube, review proxies, and archive outputs.
- Burn-in presets for timecode/debug overlays.
- Fusion macros/templates for lower thirds, caption styles, bumpers, motion graphics, and branded overlays.
- PowerGrade/LUT/still workflows for repeatable color look, while avoiding hard-coded destructive grades when a timeline should stay editable.

Skill outputs should prefer importing/installing these reusable assets over recreating UI state by clicking.

## 4. Computer Use

Use Computer Use only for UI learning, verification, and operations the scripting API cannot expose.

Examples:

- proving that a lesson control exists and can be operated
- validating visible UI state with screenshots
- testing manual HITL workflow
- adjusting plugin panels or modal controls that are not scriptable

If Computer Use fails but scripting succeeds, continue with scripting only and record the UI bridge failure. Do not mark UI homework complete.

## 5. External Analysis and Rendering Helpers

Use external tools around Resolve, not instead of it:

- `ffprobe`/`ffmpeg` for media probing, rough loudness checks, proxy generation, and render verification
- Whisper/Gemini/LLM evaluators for transcript/story/quality review
- Rust/Python planners for edit-decision graphs
- Resolve scripting to materialize the planner output into editable timelines

The production handoff target is always a layered Resolve artifact unless the user explicitly asks for a flat render only.

## Required Preflight

Before any Resolve skill edits a project:

1. Confirm Resolve process is running.
2. Confirm scripting API connection.
3. Capture Resolve version, current page, current project, current timeline, database info, and scripting paths.
4. Confirm timeline start frame before placing clips.
5. Confirm target media paths exist and are not AppleDouble `._*` sidecar files.
6. If using Computer Use, call `get_app_state` once and record success/failure separately from scripting readiness.

---

## FILE: skills/davinci-resolve-computer-use-training/references/resolve-sdk-notes.md

# Resolve SDK Notes

These notes are from the locally installed Resolve 20 scripting SDK README dated May 7, 2025.

## Supported Invocation

- Python and Lua scripts are supported.
- Resolve must be running for normal external scripting.
- Scripts can be run from the Fusion console, from the command line, or from Resolve's Workspace > Scripts menu.
- External scripting access is controlled in Resolve Preferences. Use local access for Codex workflows unless a network workflow is explicitly required.

## Local macOS Environment

```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

## Script Menu Install Paths

```text
/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
```

Place scripts under:

- `Utility` for all pages
- page folders such as `Edit`, `Color`, or `Deliver` for page-specific actions
- `Deliver` when render-job menu availability is useful

## APIs We Should Prefer

- `resolve.OpenPage("media" | "cut" | "edit" | "fusion" | "color" | "fairlight" | "deliver")`
- `resolve.GetCurrentPage()`
- `resolve.LoadLayoutPreset`, `SaveLayoutPreset`, `ImportLayoutPreset`, `ExportLayoutPreset`
- `resolve.ImportRenderPreset`, `ExportRenderPreset`
- `resolve.ImportBurnInPreset`, `ExportBurnInPreset`
- `ProjectManager.CreateProject`, `LoadProject`, `SaveProject`, `ExportProject`, `ArchiveProject`
- `Project.GetCurrentTimeline`, `GetTimelineByIndex`, `SetCurrentTimeline`
- `Project.SetRenderSettings`, `AddRenderJob`, `StartRendering`, `GetRenderJobStatus`
- `MediaStorage.AddItemListToMediaPool`
- `MediaPool.CreateEmptyTimeline`, `AppendToTimeline`, `CreateTimelineFromClips`
- `Timeline.InsertFusionTitleIntoTimeline`, `InsertFusionCompositionIntoTimeline`, `InsertFusionGeneratorIntoTimeline`
- `TimelineItem.ImportFusionComp`, `ExportFusionComp`, `LoadBurnInPreset`

## Practical Implication

Most production work should be script-first. UI automation is for proving manual workflows, catching screenshots, and operating non-scriptable controls.

---

## FILE: skills/davinci-resolve-computer-use-training/references/resolve20-homework-map.md

# Resolve 20 Homework Map

Ground truth PDFs are local under the configured local workbook download directory, such as `~/Downloads/`. The repo wikis are fast summaries; use the PDFs when UI behavior or page ranges matter.

## Beginner's Guide

| Lesson | Title | Pages | Homework Goal |
|---:|---|---|---|
| 1 | Editing a Rough Cut | 1-67 | Import/relink media, build a timeline from soundbites, add B-roll/music, pace an interview. |
| 2 | Finessing the Rough Cut | 69-139 | Practice timeline backups, trim modes, replace edit, simple effects, logo, closing titles. |
| 3 | Audio Editing and Quick Export | 141-179 | Normalize/dialogue cleanup, fades, music mix, voiceover, quick export. |
| 4 | Performing Primary Color Corrections | 189-245 | Use scopes, Lift/Gamma/Gain, nodes, automatic adjustments, camera matching, curves, HDR wheels. |
| 5 | Making Secondary Adjustments | 247-293 | Use windows, outside nodes, HSL curves, Color Warper, Qualifier, tracker, Color Slice. |
| 6 | Finishing and Management | 295-333 | Apply Color-page Resolve FX, find ungraded clips, copy grades, stills, grades, LUTs. |
| 7 | Project Setup and Preferences | 335-415 | Project setup, audio sync, metadata, Smart Bins, subclips, preferences, shortcuts. |
| 8 | An Introduction to Fairlight | 425-491 | Track formats, Dialogue Leveler, EQ, SFX, scrollers, soundtrack mix, music ducking. |
| 9 | An Introduction to Fusion | 499-541 | Fusion comp, nodes, Merge, Text+, keyframes, simple compositing. |
| 10 | Delivery and Media Management | 543-599 | Vertical timelines, reframing, Deliver settings, audio standards, presets, queue, archive/backup. |

## Editor's Guide

| Lesson | Title | Pages | Homework Goal |
|---:|---|---|---|
| 1 | Building the Rough Cut | 1-73 | Assemble soundbites, subclips, B-roll, music, logo using deeper edit workflow. |
| 2 | Refining the Rough Cut | 75-147 | Roll/slip/ripple/slide trims, replace edits, titles, review workflow. |
| 3 | Cutting a Dramatic Scene | 149-195 | Takes, reverse shots, Match Frame, pickups, Take Selector, split edits, dynamic trimming. |
| 4 | Multicamera Editing | 197-243 | Multicam interview/music workflow, real-time angle switching, flattening and adjustment. |
| 5 | Project Organization | 245-321 | Project settings, importing, sync, metadata, Smart Bins, Analyze Clips for People, Power Bins. |
| 6 | AI Workflows | 323-387 | Proxies, AI transcription, transcription edit, Remove Silent Portions, IntelliScript, AI Music Editor. |
| 7 | Edit Page Effects | 389-473 | Traveling mattes, speed changes, freeze frames, 3D Keyer, Transform FX, Video Collage. |
| 8 | Audio Editing | 475-543 | SFX, Foley sync, VO, clip balance, Dialogue Leveler, EQ, music mix. |
| 9 | Delivering Projects | 545-617 | AAF, aspect ratios, Smart Reframe, subtitles, custom presets, multi-project render, media management. |

## Colorist Guide

| Lesson | Title | Pages | Homework Goal |
|---:|---|---|---|
| 1 | Balancing Footage | 3-43 | Archive open, backups, primary grade, curves, color/log wheels. |
| 2 | Creating Color Continuity | 45-71 | Shot matching strategy, flags/filters, stills, manual match. |
| 3 | Correcting and Enhancing Isolated Areas | 73-139 | Windows, sharpening, skies, color warper, Face Refinement, skin tones. |
| 4 | Conforming an XML Timeline | 143-179 | XML import, offline reference sync, conform, maximize dynamic range. |
| 5 | Mastering Node Trees | 181-223 | Node order, parallel/layer mixers, external mattes. |
| 6 | Managing Grades Across Clips and Timelines | 225-259 | Versions, append grades/nodes, templates, PowerGrades, ColorTrace. |
| 7 | Using Groups | 263-341 | Scene Cut Detection, groups, pre/clip/post group levels, tracking, LUTs, timeline-level grades. |
| 8 | Adjusting Image Properties | 343-379 | Timeline resolutions, sizing, keyframes, noise reduction, render cache. |
| 9 | Setting Up Raw Projects | 381-409 | Raw project/clip settings, HDR wheels, raw render cache. |
| 10 | Delivering Projects | 411-447 | Lightbox, client review, render workflow, custom renders, DCP, advanced settings. |

## Fairlight Audio Post

| Lesson | Title | Pages | Homework Goal |
|---:|---|---|---|
| 1 | Building a Soundtrack | 1-79 | Audio-only project, clips, tracks, markers, trimming, balancing, panning. |
| 2 | Editing Dialogue Tracks | 81-159 | Multichannel prep, checkerboard edit, mono channels, VO takes, layers, AI speech-to-text. |
| 3 | Editing Sound Effects and Music | 161-244 | Markers, Focus Mode, Sound Library, sync points, scrollers, beat edits, nested timelines, music. |
| 4 | Recording Voiceover, ADR, and the Foley Sampler | 247-310 | Mic setup, patching, VO/ADR, cue lists, oscillator, Foley Sampler. |
| 5 | Balancing Clips and Panning Tracks | 313-364 | Dialogue levels, auto-leveling, panning, pan tracking. |
| 6 | Audio Repairs with Native Processing and Plug-Ins | 367-415 | Gate, Clip EQ, De-Hummer, Noise Reduction, click removal, time stretch. |
| 7 | Using Fairlight FX and Processing for Creative Sound Design | 417-472 | Futzing, presets, modulation, pitch/time, doubling. |
| 8 | Simplifying the Mix with Groups, Busses, and Nested Timelines | 475-533 | Link groups, track groups, busses, aux echo, nested timelines, timeline templates. |
| 9 | Mixing and Sweetening the Soundtrack | 535-612 | Reference tracks, submixes, Ducker, automation, compression, sidechain, EQ, AI Processing. |
| 10 | Finishing and Delivering Tracks | 615-640 | Loudness monitoring, bouncing mixes, stems, stereo/5.1 delivery. |
| 11 | Exploring Immersive Audio Integration | 643-724 | Ambisonics and Dolby Atmos basics. |

## Fusion Visual Effects

| Lesson | Title | Pages | Homework Goal |
|---:|---|---|---|
| 1 | Getting Started: Learning the Fusion Page | 1-30 | Fusion interface, nodes, masks, secondary correction, keyframes, vignette. |
| 2 | Compositing Split Screens | 31-57 | Edit page layers, tracking, matte drawing, nudging, camera motion. |
| 3 | Replacing a Sky | 59-85 | Resolution handling, Darken Apply Mode, keys, alpha, sky tracking. |
| 4 | Replacing Signs and Screens | 87-109 | Planar Tracker, Clone Tool, PSD layers, mattes, Planar Transform. |
| 5 | Compositing Green-Screen Content | 111-137 | Clean plate, Delta Keyer, roto mattes, background alignment, color correction. |
| 6 | Addendum: Creating Title Animations | 139-167 | Text+ styling, Fusion title animation, Follower modifier, timing, template save. |
| 7 | Addendum: Animating with Keyframes and Modifiers | 169-191 | Motion paths, alpha, parameter linking, acceleration, random modifiers, motion blur. |

## Advanced Visual Effects

| Lesson | Title | Pages | Homework Goal |
|---:|---|---|---|
| 1 | Creating a 3D Scene | 1-39 | 3D space, navigation, 3D text, camera, lights, 2D render. |
| 2 | Exploring a Green-Screen Workflow | 41-83 | VFX color management, denoise, key, spill, 3D windshield reflection. |
| 3 | Creating a Rainy Day | 85-127 | 2D/3D merge, sky replacement, Magic Mask, reflections, particles, finish. |
| 4 | 3D Camera Tracking | 129-159 | Masking, camera tracker, solve, export scene, place objects, match color/light. |
| 5 | Compositing 3D with USD | 161-199 | USD import, shaders, render, animation, lights, Z-depth, finish. |

---

## FILE: skills/davinci-resolve-cut-screen-recording/SKILL.md

---
name: davinci-resolve-cut-screen-recording
description: Use when a user has a long screen recording, tutorial, conference talk, or demo recording and needs to cut it down to a tight watchable version — removes dead air, mistakes, "ums", and silences. Triggering symptoms include phrases like "raw recording is too long", "edit out the bad takes", "fix the ums", "remove silences", "rough cut my demo", or any DaVinci Resolve cutting question for long-form content.
---

# DaVinci Resolve — cut a long screen recording into a tight demo

## Overview

The fastest way to turn a 60-minute screen recording into an 8-minute watchable demo. Uses Resolve's **AI Transcription** plus **Remove Silent Portions** to do 80% of the work automatically, then refines manually. The core principle: do not waste your time scrubbing a waveform when Resolve can find the dead air for you.

## When to use

Symptoms:
- You recorded a 30-90 minute demo, talk, or tutorial and need to ship a tight version
- You said "um" too many times
- There are long pauses between sentences where you were thinking
- You did 2-3 takes of the same explanation and need to pick the best one
- Phrases like "raw recording is too long", "remove silences", "fix the ums"

When NOT to use:
- Multi-camera interview / talk-show — that needs the Multicam workflow (Editor's Guide ch. 4).
- Tight musical edits to a beat (rhythmic cuts) — use the Cut page manually.
- The recording is already under 10 minutes — manual editing is faster than this skill.

## Quick reference

| Tool | What it does | Where |
|---|---|---|
| **AI Transcription** | Generates word-level transcript with speaker detection | Right-click clip > Audio Transcription > Transcribe With Speaker Detection |
| **Remove Silent Portions** | Auto-deletes silent ranges from the timeline | Transcription window > Options menu (...) > Remove Silent Portions |
| **Editing from transcript** | Click a word, press F12, the clip lands in the timeline at that word | Transcription window > Append (F12) / Insert (Shift-F12) buttons |
| **Subframe audio editing** | Edit audio at sub-frame precision for tight cuts | Cmd-B for Razor, then trim by mouse |

## Steps

### Phase 1 — Set up and transcribe (3 minutes)

1. Switch to the Edit page (Shift-4).
2. In the Media Pool, drag your screen recording into a bin (e.g. `01 — Footage`).
3. Right-click the clip > **Audio Transcription > Transcribe With Speaker Detection**. (This is Studio-only; if you have free Resolve, use the manual Cut workflow below.)
4. Wait — about 1 minute per 10 minutes of audio. The AI Transcription window opens automatically when done.

If you have free Resolve (not Studio), AI Transcription is unavailable. Use the Cut page approach: import the clip, drag to the timeline, use the **mouse-scrub-and-mark-In/Out** workflow on the Cut page (Beginner's Guide pp. 1-67 covers this).

### Phase 2 — Create the rough cut from the transcript (10-15 minutes)

1. Create a new bin called `TIMELINES` and a new timeline inside it called `ROUGH_CUT`. Audio Track Type = Mono if your recording is mono voice.
2. With the Transcription window open, click on any word — the playhead jumps to that timecode in the source viewer.
3. Use **J / K / L** to scrub backward/stop/forward through the transcript.
4. To add a soundbite to the timeline:
   - Click and drag through the words you want to keep — this sets In and Out points automatically.
   - Press **Shift-F12** to **Append** the marked range to the timeline end.
   - Or press **F12** to **Insert** at the playhead.
5. Search the transcript for keywords — type a word in the Search field at the top of the Transcription window to jump to every instance.
6. Build the rough cut by appending each good soundbite one by one. Aim for ~2x your target length (a 16-minute rough cut for an 8-minute final).

Editor's Guide pp. 352-358 covers this workflow in depth.

### Phase 3 — Auto-remove silent portions (1 minute)

1. In the Transcription window, click the **Timeline** button (top-left of the Transcription window) to switch from clip-mode to timeline-mode. The window now shows the transcript for everything on the timeline, with silent gaps marked as `(...)`.
2. Click the Options menu (three dots `...`) > **Remove Silent Portions**.
3. The silent ranges are ripple-deleted from the timeline. Your 16-minute rough cut is suddenly 12 minutes.

Editor's Guide p. 358 shows this exact step.

### Phase 4 — Refine the edits manually (10-20 minutes)

The AI cuts are crude — they leave breaths cut off or pauses that feel unnatural. Walk the playhead through each edit point.

1. Press **N** to disable snapping (so you can trim by mouse at sub-frame precision).
2. Press **Shift-S** to enable audio scrubbing (you can hear what you are passing over).
3. At each cut: hover the cut point, click and drag the edge to extend or pull in by a few frames.
4. Use **Shift-,** / **Shift-.** to nudge an edit by 5 frames forward/back.

The audio subframe editing tip is on Editor's Guide p. 496.

### Phase 5 — Cut the obvious mistakes (5 minutes)

1. Play through end-to-end at 1.5x speed.
2. When you hear a mistake / dead air / re-take, press **I** for In-point.
3. Find the end of the mistake, press **O** for Out-point.
4. Press **Shift-Delete** to ripple-delete the marked region.
5. Continue. This pass should remove 1-3 minutes more.

You should be at or near your target length. Save the project.

## Python automation (rough silence detection on existing timeline)

For a long talk you have already imported, this script walks the active timeline, finds audio clips, and prints their durations so you can quickly identify long silent gaps to manually remove. It is **not** a substitute for AI Transcription's Remove Silent Portions — it is a helper for when you need to script a multi-clip operation.

The script uses the official DaVinci Resolve scripting API documented in `DaVinci Resolve/Developer/Scripting/README.txt` and the public Reference Manual.

```python
# scripts/auto_silence_cut.py
# Marks silent regions on the active timeline by inspecting clip start/end frames.
# Run from inside Resolve via Workspace > Console > Py3, or from terminal after
# setting RESOLVE_SCRIPT_API / RESOLVE_SCRIPT_LIB / PYTHONPATH (see README.md).
```

See `scripts/auto_silence_cut.py` for the full script. The script is conservative — it does not actually delete anything. It prints clip-level timecode reports so you can verify before running destructive edits.

## Common mistakes

- **Trusting the AI Transcription's accuracy** -> it gets technical terms, brand names, and acronyms wrong. Always proofread before treating it as a script. Editor's Guide pp. 346-348 documents the Search + Replace workflow for fixing systematic errors (e.g. "Oregon" -> "Organ" misrecognition).
- **Cutting on the Cut page when this is a single long clip** -> the Cut page is optimized for fast assembly from many small clips. For one long recording, the transcript-driven workflow on the Edit page is faster.
- **Forgetting to disable snapping when fine-trimming** -> snapping forces your cuts to align with existing edits and frame boundaries. Press N to toggle it off for fine work, on for assembly.
- **Doing the entire pass at 1x playback speed** -> 1.5x or 2x is faster and your ear can still spot rough cuts. Use the L key twice to enable 2x playback.

## Verification

You succeeded if all of the following are true:

1. The timeline duration matches your target (or is within 30 seconds of it).
2. Playing back the timeline end-to-end, you cannot hear any cut edits — the audio flows smoothly.
3. Every "um" / "uh" / long pause has been removed or trimmed.
4. The audio levels look broadly even on the meters (no clip is much louder than another — though the next skill, `davinci-resolve-audio-cleanup-podcast`, handles the actual leveling).
5. You can hand the timeline to a teammate and they cannot tell which cuts were AI-driven vs manual.

## Transfer

Now try this on a 20-minute conference talk recording. Watch the silence-detection threshold — large auditoriums often have ambient room noise above -30 dB, so Resolve's Remove Silent Portions might not detect actual pauses. In that case, you may need to manually search for the "(silent)" markers in the transcript and remove them by hand, or apply a quick noise-reduction pass first (see `davinci-resolve-audio-cleanup-podcast`) so the noise floor drops below the silence-detection threshold.

## Working reference

- `docs/wiki/editors-guide.md#lesson-6--ai-workflows-pp-323-387` (AI Transcription, Remove Silent Portions — primary)
- `docs/wiki/beginners-guide.md#lesson-1--editing-a-rough-cut-pp-1-67` (Cut/Edit page basics for free Resolve users)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (transcription pitfall rows)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports that transcription edits land on the wrong word, breaths are cut weirdly, or Remove Silent Portions misses pauses, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 341-361 (Lesson 6 — full AI Transcription workflow)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 352-358 (Editing Using Transcription — append/insert/F12 semantics)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 358-360 (Editing Transcribed Clips in the Timeline — Remove Silent Portions)
- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 496 (Subframe Audio Editing)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 1-67 (Cut/Edit page basics — fallback workflow for free Resolve, no AI Transcription)

---

## FILE: skills/davinci-resolve-devrel-project-template/SKILL.md

---
name: davinci-resolve-devrel-project-template
description: Use when a user wants a reusable DaVinci Resolve project structure for shipping DevRel videos repeatedly — sets up bins, timeline, render presets, and a color preset so future videos start with one click instead of one hour. Triggering symptoms include phrases like "set up a Resolve template", "reusable project structure", "every video starts from scratch", "save my Resolve setup as a preset", or "DevRel video workflow."
---

# DaVinci Resolve — reusable DevRel project template

## Overview

A pre-configured Resolve project that you duplicate for every new video. It contains: a sensible bin hierarchy, a 1080p / 23.976 fps timeline, three render presets (YouTube 16:9, LinkedIn 1:1, Shorts 9:16), a starter color node tree, and a 100-track Fairlight timeline preset. Saved once, reused forever.

## When to use

Symptoms:
- You ship a new video every 1-4 weeks for the same channel/audience
- You catch yourself recreating the same bin structure every time
- You want render queue presets that match your platforms' specs
- A teammate keeps asking "what render settings do you use for X"

When NOT to use:
- You only ship one or two videos a year (the setup cost is not worth it).
- You are editing a one-off feature film (different structural needs).

## Quick reference

| Asset | What is in it |
|---|---|
| Bin structure | `01 — Footage`, `02 — Audio`, `03 — Music`, `04 — Graphics`, `05 — SFX`, `06 — VO`, `07 — Timelines`, `08 — Exports` |
| Master timeline | 1920x1080, 23.976 fps, 5-track audio (Dialogue / VO / SFX / Music / Bus) |
| Render presets | YouTube 1080p H.264, LinkedIn Square 1080x1080, Shorts 1080x1920 |
| Color preset | "Webcam Look" PowerGrade — see `davinci-resolve-color-grade-webcam` for what is in it |
| Fairlight preset | Saved 5-track configuration in Presets Library |

## Steps

### 1. Create the empty project that becomes the template

1. In the Project Manager, click **New Project**.
2. Name it `DEVREL_TEMPLATE_v1`.
3. Double-click to open it.

### 2. Build the bin hierarchy in the Media Pool

1. Press Shift-4 to go to the Edit page (or click Edit at the bottom).
2. Open the Media Pool (top-left button).
3. Right-click the **Master** bin > **New Bin**. Name it `01 — Footage`.
4. Repeat for: `02 — Audio`, `03 — Music`, `04 — Graphics`, `05 — SFX`, `06 — VO`, `07 — Timelines`, `08 — Exports`.

The numeric prefixes force the bins to sort in workflow order. See `templates/devrel-bin-structure.txt` in this skill for a copy-pasteable list.

### 3. Build a Power Bin that survives across projects

Standard bins are project-scoped. **Power Bins** are project-library-scoped — perfect for music stings, brand logos, animated graphics you reuse.

1. **View menu > Show Power Bins**.
2. In the Power Bins panel, right-click > **New Bin**. Name it `BRAND ASSETS`.
3. Drag your logo PNG/SVG and any reusable music files in. Future projects in the same library will see this bin.

Editor's Guide p. 317 covers Power Bins in detail.

### 4. Create the master timeline

1. **File > New Timeline** (Cmd-N / Ctrl-N).
2. Uncheck **Use Project Settings**.
3. Set:
   - Timeline name: `MASTER_TIMELINE`
   - Start Timecode: `01:00:00:00` (standard broadcast convention)
   - Video tracks: 3 (V1: main, V2: titles, V3: B-roll/overlays)
   - Audio tracks: 5 (Stereo on all)
   - Resolution: 1920x1080
   - Frame rate: 23.976 (or 29.97 if your audience is North American TV-trained, or 25 if you are in Europe)
4. Create. Move the new timeline to the `07 — Timelines` bin.

### 5. Name and color-code the audio tracks

1. Double-click the **Audio 1** track name and rename to `DIALOGUE`. Right-click the track header > color > Teal.
2. Repeat:
   - Audio 2: `VO` (Violet)
   - Audio 3: `SFX` (Orange)
   - Audio 4: `MUSIC` (Olive)
   - Audio 5: `BUS` (Gray — this is your scratch/safety track)
3. Right-click any track > **Lock Track** if you want to prevent accidental edits later.

This naming is loosely based on the structure shown in Fairlight Audio Post pp. 527-528 for documentary projects.

### 6. Save the Fairlight timeline configuration as a preset

This is the magic: the entire timeline structure (tracks, busses, names) can be saved as a Fairlight Configuration Preset and applied to any future new timeline.

1. Press Shift-7 to switch to the Fairlight page.
2. **Fairlight menu > Presets Library**.
3. Change **Filter by** dropdown to **Fairlight Configuration Presets**.
4. Click **Save New**. In the dialog, click **Create New**.
5. Name it `DEVREL_5_TRACK_TEMPLATE`. Click **OK**.

Now any new timeline created in this project (or any project in the same library) can opt into this preset via the **Use Fairlight Preset** checkbox when creating.

Fairlight Audio Post pp. 530-531 documents this workflow.

### 7. Build the three render presets — YouTube, LinkedIn, Shorts

Each preset reuses the same source timeline but with different reframing and dimensions. See the dedicated skill `davinci-resolve-export-multi-platform` for the full workflow including AI Smart Reframe. Here is the short version for getting the presets saved into the template:

1. Press Shift-8 to switch to the Deliver page.
2. In **Render Settings**, click **H.264 Master**.
3. Set **File Name** field to `%timeline_name` (variable). Click the variable dropdown if you want `%timestamp` appended.
4. Set Resolution: 1920x1080, Frame Rate: Timeline Resolution.
5. **Audio tab > Audio Normalization > Optimize to standard > Standard: YouTube**. This bakes in YouTube's -14 LUFS standard.
6. Click the Options menu (`...`) at the top of Render Settings > **Save As New Preset**.
7. Name: `DEVREL_YOUTUBE_1080`. Check **Add to quick export**. Save.
8. Repeat for LinkedIn (1080x1080, audio standard = streaming) and Shorts (1080x1920, audio standard = streaming).

Editor's Guide pp. 577-580 documents this exact workflow including the YouTube audio normalization standard at -14 LKFS / -1.0 dBTP.

### 8. Save the project as a template

Resolve does not have a true "save as template" command — the workflow is to **duplicate** the project for each new edit.

1. Close the project (File > Close Current Project, or just go back to Project Manager).
2. In Project Manager, right-click `DEVREL_TEMPLATE_v1` > **Duplicate**.
3. Rename the duplicate to `2026-05-WhateverVideo`.
4. Open the duplicate, replace media, edit. Your template stays clean.

You can also **Export Project Archive** (right-click in Project Manager) to ship the template as a `.dra` file to teammates.

## Common mistakes

- **Treating Smart Bins like Folder Bins** -> Smart Bins are dynamic queries (e.g. "all clips tagged 'interview'"). They are not folders. Use regular bins for hierarchy and Smart Bins for filtering. Editor's Guide p. 302.
- **Forgetting that Power Bins span projects** -> If you delete a clip from a Power Bin while editing one project, it disappears from every project that uses that Power Bin. Be careful.
- **Picking the wrong frame rate** -> Once a timeline has clips in it, changing the frame rate causes retiming. Decide upfront. 23.976 is the cinematic standard; use 29.97 if your audience watches your videos on a North-American TV; use 25 if you are in Europe.
- **Saving the YouTube render preset without enabling audio normalization** -> your audio will be inconsistent across uploads. Always enable Optimize to standard.

## Verification

You succeeded if all of the following are true:

1. Project Manager shows `DEVREL_TEMPLATE_v1` and you can right-click > Duplicate it.
2. Opening the template shows the eight numbered bins in the Media Pool.
3. The Quick Export menu (Edit page > top-right cloud icon) shows your `DEVREL_YOUTUBE_1080`, `DEVREL_LINKEDIN_1080`, `DEVREL_SHORTS_1080` presets.
4. Creating a new timeline with **Use Fairlight Preset** checked offers `DEVREL_5_TRACK_TEMPLATE` in the dropdown.
5. The duplicate project (your actual working project) has empty bins but identical structure.

## Transfer

Now try this: ship one real video using the duplicated project. After you have shipped, go back to the template and add anything you wished was there (a specific lower-third graphic, an SFX bin you reused, an additional render preset for Twitter/X). Version-bump the template to `DEVREL_TEMPLATE_v2`. Templates compound — each iteration shortens future setup time.

## Working reference

- `docs/wiki/editors-guide.md#lesson-5--project-organization-pp-245-321` (bins, Smart Bins, Power Bins — primary)
- `docs/wiki/editors-guide.md#lesson-9--delivering-projects-pp-545-617` (render presets workflow)
- `docs/wiki/fairlight-audio-post.md#lesson-8--busses-and-nested-timelines-pp-475-533` (Fairlight timeline preset)
- `docs/wiki/master.md#shared-glossary-terms-that-appear-across-multiple-pdfs` (bin vs Smart Bin vs Power Bin definitions)

## When the agent's work isn't matching expectations (context-rot reset)

If the user pushes back on the template structure, bin types, render presets, or Fairlight preset workflow, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 246-321 (Lesson 5 — Project Organization, full bin/metadata workflow)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 317-321 (Power Bins — specifically the library-scoping behavior)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 577-580 (Creating a Custom Render Preset)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 246-253 (Creating a New Project and Project Settings)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 525-532 (Creating a Timeline Template)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 530-532 (Saving a Timeline Configuration in the Presets Library)

---

## FILE: skills/davinci-resolve-export-multi-platform/SKILL.md

---
name: davinci-resolve-export-multi-platform
description: Use when a user needs to export the same DaVinci Resolve edit for multiple platforms — YouTube (16:9), LinkedIn (square 1:1), Reels/Shorts/TikTok (9:16) — with correct dimensions, loudness, and optionally batch automation. Triggering symptoms include phrases like "export for YouTube and LinkedIn", "make a vertical version", "9:16 from my 16:9 edit", "render the same edit three times", "batch render", "generate captions", or any DaVinci Resolve Deliver/render question.
---

# DaVinci Resolve — export the same edit for YouTube, LinkedIn, and Shorts

## Overview

One source edit, three platform-specific exports, optionally automated with Python. The core principle: **let Resolve's AI Smart Reframe do the reframing for you** — do not manually keyframe Position for every clip when you change aspect ratio. Then save custom render presets so the next video is a one-click affair.

This skill also covers two merged JTBDs: **auto-generating subtitles** and **batch-rendering with the Python API**.

## When to use

Symptoms:
- Need to ship the same video to YouTube + LinkedIn + Reels/Shorts/TikTok
- Need a vertical version of an existing 16:9 edit
- Need to add captions/subtitles to your video
- Want to automate "render this and that and the other" with a script
- Have multiple timelines to render in series and do not want to babysit Resolve

When NOT to use:
- One-off rendering of a single platform — use Quick Export (Edit page top-right cloud icon).
- DCP (digital cinema) export — separate Colorist Guide workflow (pp. 431-447).

## Quick reference

| Target | Resolution | Audio standard | Codec |
|---|---|---|---|
| YouTube (long-form) | 1920x1080 (or 3840x2160) | YouTube (-14 LUFS) | H.264 or H.265 |
| LinkedIn (feed) | 1080x1080 (square) | Streaming (-16 LUFS) | H.264 |
| Reels / Shorts / TikTok | 1080x1920 (vertical) | Streaming (-16 LUFS) | H.264 |

For HITL Resolve handoffs, create separate timelines before rendering:

- `Instagram Semantic Cut` or equivalent for vertical social.
- `YouTube Semantic Cut` or equivalent for horizontal long form.
- V1/V2/V3 for source picture layers.
- V4 for burned-caption/title graphics.
- A1/A2 for source and processed dialogue.
- A3/A4 for music, SFX, bumpers.

Do not treat an SRT file as enough when the user asked for burned-in Netflix-style captions. Captions must be visible in the video frame and editable as a layer or template until final render.

## Steps

### Phase 1 — Reframe your 16:9 source for vertical and square versions

Editor's Guide pp. 569-575 covers AI Smart Reframe.

1. Press **Shift-4** to go to the Edit page.
2. Right-click your master timeline in the Media Pool > **Duplicate Timeline**. Name the duplicate `MASTER_TIMELINE_VERTICAL`.
3. Open the duplicate. In the timeline, click the **Timeline Resolution** dropdown (top of the viewer) > custom > set to `1080x1920` (vertical).
4. Resolve will warn that clips will be cropped. Click OK.
5. Select all clips. Right-click > **Smart Reframe** (Studio only — for free Resolve, use manual keyframes via the **Position** parameter in the Inspector).
6. In the Smart Reframe dialog, choose **Object of Interest: Auto** and click **Reframe**. Resolve adds keyframes that keep the main subject in frame even as the aspect ratio crops the edges.
7. Scrub through and check — if a clip drifted (e.g. the AI followed the wrong person), select that clip and either:
   - Reset Position keyframes and use the **Reference Point** mode to manually click the subject
   - Or set Position X manually via the Inspector
8. Repeat for `MASTER_TIMELINE_SQUARE` at `1080x1080`.

Editor's Guide pp. 572-575 covers the Reference Point fallback when AI Smart Reframe picks the wrong subject.

### Phase 2 — Add captions with AI-generated subtitles

Editor's Guide pp. 586-590 covers Create Subtitles from Audio.

1. With your timeline open, choose **Timeline menu > AI Tools > Create Subtitles from Audio**.
2. In the dialog:
   - **Language**: Auto (or specific language)
   - **Caption Preset**: Subtitle Default
   - **Maximum**: 42 characters per line
   - **Lines**: Single (or Double if you have very long sentences)
   - **Gap Between Subtitles**: 0 frames
3. Click **Create**. Resolve transcribes and adds a Subtitle track to your timeline.
4. **Fix the inevitable errors** — playback the timeline, double-click any subtitle clip in the Subtitle track to edit the text. The AI gets technical terms, brand names, and acronyms wrong constantly.
5. To export subtitles as an SRT file, right-click the Subtitle track > **Export Subtitles** > choose SRT format.

### Phase 3 — Build the three render presets

Editor's Guide pp. 577-580 covers Save As New Preset.

1. Press **Shift-8** to switch to the **Deliver** page.
2. In Render Settings, click **H.264 Master**.
3. Configure:
   - **File Name**: type `%timeline_name` then choose the Timeline Name variable from the dropdown
   - **Location**: browse to your `08 — Exports` folder
   - **Render**: Single clip
   - **Video tab**: Format = MP4, Codec = H.264, Resolution = Timeline Resolution (this picks up the current timeline's dimensions)
   - **Audio tab > Export Audio**: ON, Codec AAC, Bit Rate 320 Kb/s
   - **Audio tab > Audio Normalization**: enable **Normalize Audio** > **Optimize to standard** > Standard = **YouTube** (-14 LUFS, -1.0 dBTP)
4. Click the Options menu (`...`) at top of Render Settings > **Save As New Preset**.
5. Name: `DEVREL_YOUTUBE_1080`. Check **Add to quick export**. Save.
6. Repeat for **LinkedIn** (1080x1080, audio standard = Streaming) and **Shorts** (1080x1920, audio standard = Streaming).

### Phase 4 — Queue and render all three

1. Open your **YouTube** timeline > Deliver page > select `DEVREL_YOUTUBE_1080` preset > click **Add to Render Queue**.
2. Switch to your **LinkedIn** timeline > Deliver page > select `DEVREL_LINKEDIN_1080` preset > **Add to Render Queue**.
3. Switch to your **Shorts** timeline > Deliver page > select `DEVREL_SHORTS_1080` preset > **Add to Render Queue**.
4. In the Render Queue panel (right side), click **Render All**.
5. Walk away. Resolve renders all three serially.

## Python automation — batch render multiple timelines

This is the merged "batch render with Python API" JTBD. The script below assumes Resolve is running, a project is open, and you have already saved render presets named `DEVREL_YOUTUBE_1080`, `DEVREL_LINKEDIN_1080`, `DEVREL_SHORTS_1080`. The script walks every timeline in the project and adds a render job for each preset that matches the timeline's aspect ratio.

See `scripts/multi_platform_render.py` for the full script.

The script uses the official DaVinci Resolve scripting API as documented in `DaVinci Resolve/Developer/Scripting/README.txt`:

```python
Resolve.GetProjectManager()
ProjectManager.GetCurrentProject()
Project.GetTimelineByIndex(idx)
Project.GetTimelineCount()
Project.LoadRenderPreset(preset_name)
Project.SetRenderSettings(settings_dict)
Project.AddRenderJob()
Project.StartRendering()
Project.IsRenderingInProgress()
```

These methods are real and documented. The script has been written defensively — it prints what it would do before doing it, and it confirms via stdin before starting the actual render.

## Common mistakes

- **Manually keyframing Position to vertical-frame every clip** -> there is a button for that. Use AI Smart Reframe (Studio) or at minimum the per-clip Reframe button in the Inspector. (Editor's Guide pp. 572-575.) **(This is the misconception this skill addresses head-on.)**
- **Saving the YouTube preset without enabling audio normalization** -> your videos will be inconsistent across uploads. Always enable Optimize to standard.
- **Forgetting that AI Smart Reframe is Studio-only** -> free Resolve has manual Position keyframes only. Either upgrade or accept manual reframing.
- **Trusting AI-generated subtitles without proofreading** -> always playback and fix. They will mangle product names, acronyms, and technical jargon.
- **Rendering all three timelines at once on a single GPU** -> Resolve renders serially anyway. There is no penalty for queueing all three; do not start three Resolve instances.

## Verification

You succeeded if all of the following are true:

1. Your `08 — Exports` folder contains three MP4 files: one 1920x1080, one 1080x1080, one 1080x1920.
2. Each file plays cleanly when dragged into VLC / QuickTime.
3. The vertical version keeps the main subject in frame for the entire duration (no awkward background-only stretches).
4. Subtitles burn in correctly on platforms that auto-display them, or are exported as `.srt` for upload alongside the MP4.
5. Audio loudness measured by a third-party LUFS meter (e.g. YouLean Loudness Meter, free) reads -14 LUFS ±1 for the YouTube file.

## Transfer

Now try this: add a fourth target — Twitter / X video at 1920x1080 but capped at 2:20 duration. Build a Twitter timeline that is a shorter cut of your master (use the trim workflow from `davinci-resolve-cut-screen-recording`). Save a new `DEVREL_TWITTER_1080` render preset. Add it to the Python script. You now have a one-script, four-platform export pipeline.

## Working reference

- `docs/wiki/editors-guide.md#lesson-9--delivering-projects-pp-545-617` (full Deliver chapter — primary)
- `docs/wiki/editors-guide.md#lesson-9--delivering-projects-pp-545-617` (AI Smart Reframe specifics inside the chapter notes)
- `docs/wiki/master.md#shared-glossary-terms-that-appear-across-multiple-pdfs` (LUFS / dBTP / AI Smart Reframe glossary)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (Smart Reframe + render failure rows)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports Smart Reframe drift, render failures, missing subtitles, or wrong loudness on delivered files, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 545-617 (Lesson 9 — Delivering Projects, full chapter)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 569-575 (AI Smart Reframe — Object of Interest vs Reference Point modes)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 577-580 (Creating a Custom Render Preset)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 586-590 (Generating Subtitles from Audio)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 597-617 (Customizing Deliver Presets, Verifying the Exported Files)
- DaVinci Resolve Scripting API: `DaVinci Resolve/Developer/Scripting/README.txt` (shipped with installer)

---

## FILE: skills/davinci-resolve-setup/SKILL.md

---
name: davinci-resolve-setup
description: Use when a user is installing DaVinci Resolve for the first time, switching machines, configuring a media drive for video editing, or asking about backup/proxy settings. Triggering symptoms include phrases like "just installed Resolve", "set up DaVinci Resolve", "drop frames during playback", "where should my media live", "how do I configure backups", or any DaVinci Resolve installation/preferences question.
---

# DaVinci Resolve — first-time setup for content creators

## Overview

One-time configuration for DaVinci Resolve 20 so it does not bite you later. Three things matter: the install source, the media drive, and the backup settings. Everything else can be configured per-project.

## When to use

Symptoms:
- Just downloaded DaVinci Resolve and want to know what to configure first
- Bought a new external drive and need to point Resolve at it
- Playback drops frames or shows a red GPU indicator
- Want to enable automatic project backups before doing real work

When NOT to use:
- Resolve is already running fine and you have an existing project — skip to `davinci-resolve-devrel-project-template`.
- You only need to enable Python scripting — that is a one-liner in Preferences > System > General (set External scripting to Local).

## Quick reference

| Decision | Right answer | Why |
|---|---|---|
| Install source | blackmagicdesign.com, NOT Mac App Store | App Store version sandboxes the file system |
| Free vs Studio | Free is fine for 99% of DevRel | Studio adds noise reduction, AI Smart Reframe, neural engine features |
| Media drive | Fastest external SSD you have | Read >500 MB/s minimum for 4K |
| Backup interval | 10 minutes / 24 hours / 180 days | Survives editor crash, daily mistake, six-month regret |
| Render cache location | Internal SSD, not media drive | Reduces read/write contention |

## Steps

### 1. Install from blackmagicdesign.com (not the App Store)

1. Open a browser, go to `https://www.blackmagicdesign.com/products/davinciresolve`.
2. Click Download.
3. Choose your OS (macOS, Windows, Linux). On macOS, do **not** install via the Mac App Store — it sandboxes the filesystem and breaks several workflows like the Blackmagic Proxy Generator.
4. Run the installer. Restart if prompted.

### 2. Test your media drive speed before you commit to it

1. Download **Blackmagic Disk Speed Test** (free, separate app). On macOS it is on the App Store. On Windows it is included with the Desktop Video installer.
2. Run it pointed at the drive you plan to use for media.
3. Look at the "Will It Work?" table. Confirm green checkmarks for the codecs and resolutions you actually shoot (typically H.265 at 1080p/4K, or Blackmagic RAW if you shoot on a Blackmagic camera).
4. If the drive cannot sustain reads above ~500 MB/s for your codec at your resolution, you will get dropped-frame playback. Buy a faster drive or generate proxies (covered in `davinci-resolve-devrel-project-template`).

### 3. First launch — set the media folders

1. Launch DaVinci Resolve. Skip the welcome screen.
2. Click **DaVinci Resolve > Preferences** (macOS) or **DaVinci Resolve > Preferences** (Windows).
3. Switch to the **System** tab at the top.
4. Click **Media Storage** in the left sidebar.
5. Click the **+** button and add your media drive. This tells Resolve where to look for media by default.
6. Click **Save**.

### 4. Enable Live Save and project backups

This is the single most important step. Resolve does NOT save by default, and you will lose work.

1. **DaVinci Resolve > Preferences > User > Project Save and Load**.
2. Confirm **Live Save** is checked. This auto-saves on every change.
3. Check **Project backups**.
4. Set the intervals:
   - Backups every **10** minutes (6 backups per hour)
   - Hourly backups for the past **24** hours
   - Daily backups for the past **180** days (six months)
5. Click **Browse** for **Backup location** and pick a folder on your internal SSD (not the media drive — you want backups in a different place than your media in case the media drive dies).
6. Check **Timeline backups** too (this backs up `.drt` files which are smaller and recoverable independently).
7. Click **Save**.

These intervals are loosely based on the Colorist Guide's project backup recommendations.

### 5. Set the working folders for the project media cache

1. **DaVinci Resolve > Project Settings** (or **File > Project Settings**, or press Shift-9).
2. **Master Settings** > scroll to **Working Folders**.
3. Set:
   - **Cache files location** — internal SSD (fast)
   - **Proxy generation location** — internal SSD or media drive (your call)
   - **Project media location** — typically same as Cache files, on your internal SSD
4. Save.

### 6. Enable external scripting (optional, but you will want it later)

1. **DaVinci Resolve > Preferences > System > General**.
2. Set **External scripting using** to **Local**.
3. Save. Restart Resolve.

This lets you run Python scripts against Resolve from your terminal — used by `davinci-resolve-cut-screen-recording` and `davinci-resolve-export-multi-platform`.

## Common mistakes

- **Installed via Mac App Store** -> uninstall and reinstall from blackmagicdesign.com. The App Store version cannot reach external drives reliably and the Blackmagic Proxy Generator is missing.
- **Media drive is USB 2.0** -> you will not be able to play back even 1080p H.264 reliably. Move to USB 3 / Thunderbolt / NVMe.
- **Backup location set to the media drive** -> backups die with the media drive. Use the internal SSD.
- **Live Save unchecked** -> you will lose hours of work the first time Resolve crashes.

## Verification

You succeeded if all of the following are true:

1. Resolve launches without complaining about a missing license or installer signature.
2. You can drag a video file from your media drive into the Media Pool without Resolve marking it offline.
3. The frame-rate indicator at the top of the source viewer stays **green** during playback (not red).
4. The path under DaVinci Resolve > Preferences > User > Project Save and Load > Backup location shows a folder on your internal SSD.
5. You can find `.drp` files (project backups) appearing in the backup folder after 10 minutes of editing.

## Transfer

Now try this: import a clip from a *different* drive than the one you configured. Resolve should still find it (since the file lives at an absolute path). Then disconnect that drive and reopen the project — note how Resolve flags those clips as offline and offers **Relink** in the Media Pool. That is the workflow you will use the first time a colleague hands you a project file without media.

## Working reference

- `docs/wiki/beginners-guide.md` (install, system requirements, Quick Setup)
- `docs/wiki/colorist-guide.md#front-matter--project-backups-pp-6-7` (Live Save and project backups, primary)
- `docs/wiki/editors-guide.md#lesson-6--ai-workflows-pp-323-387` (Disk Speed Test, proxies)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (cross-cutting symptom map)

## When the agent's work isn't matching expectations (context-rot reset)

If the user pushes back on a recommendation (install path, backup interval, drive speed, scripting toggle), read these PDF page ranges to reset:

- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. xiv-xxiv (Getting Started, system requirements, download instructions)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. xii-xxiv (Getting Started — Editor's perspective on initial setup)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 324-337 (Generating Proxy Files; Blackmagic Disk Speed Test; drive speed considerations)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 6-7 (Setting Up Project Backups, Live Save settings)

---

## FILE: skills/davinci-resolve-setup/references/pdf-pages.md

# Source page references for `davinci-resolve-setup`

| Section in SKILL.md | PDF | Pages | Topic |
|---|---|---|---|
| Install from blackmagicdesign.com | Beginner's Guide | xiv-xv | Download Resolve / installation instructions |
| Test media drive speed | Editor's Guide | 326 | Is Your Drive Fast Enough? (Blackmagic Disk Speed Test) |
| First launch — media folders | Editor's Guide | xiv-xxiv | Getting Started (general orientation) |
| Live Save + project backups | Colorist Guide | 6-7 | Setting Up Project Backups |
| Working folders | Beginner's Guide | 396-407 | Preferences chapter |
| Enable external scripting | Beginner's Guide | 396-407 | Preferences chapter (System > General) |

The Blackmagic Disk Speed Test app is referenced explicitly on Editor's Guide p. 326 with download links for both macOS App Store and the Windows Desktop Video installer.

The Live Save defaults (10 min / 2 hr / 2 day) are the Resolve installer defaults; the more aggressive 10 min / 24 hr / 180 day numbers in this skill are from Colorist Guide p. 6 step 7 ("Increase the daily backups to 180 days").

---

## FILE: skills/davinci-resolve-social-editor/SKILL.md

---
name: davinci-resolve-social-editor
description: Plan, analyze, and build professional DaVinci Resolve social edits from multicam video/audio folders, podcast/interview footage, vertical 9:16 deliverables, branded social promos, burned-in captions, B-roll/overlay coverage, Resolve timelines, FCPXML/EDL handoff, or FFmpeg preview renders. Use when Codex must avoid jump cuts, preserve narrative coherence, keep the speaker in frame, balance dialogue/music, create reviewable edit decisions, or automate Resolve media/timeline setup.
---

# DaVinci Resolve Social Editor

## Core Rule

Do not cut from transcript text alone. Build a story-first edit plan, then prove it with media analysis, frame checks, audio checks, and a Resolve-ready review artifact.

The failure mode to avoid is a technically valid cut that is semantically broken: sentence fragments, jump cuts, subject out of frame, captions that do not match, or music competing with speech.

## Required Workflow

1. **Ingest and audit**
   - Scan media with `scripts/probe_media.py <project-root> --out <manifest.json>`.
   - Identify camera ISOs, HQ audio, existing Resolve projects, brand images, and prior renders.
   - Detect unusable tracks early: silent WAVs, black cameras, missing audio, mismatched duration, or odd frame rates.

2. **Sync and source strategy**
   - Prefer Resolve multicam/sync-bin or waveform sync for real edits.
   - If scripting outside Resolve, treat FFmpeg preview renders as review proxies, not the final edit model.
   - If HQ audio is silent or unusable, explicitly fall back to embedded camera audio and say so.
   - For repeat hard-drive folder inputs, use the `social-video-folder-autocutter` skill first to create the format plan, then return here for Resolve implementation.

3. **Story plan before cutting**
   - Produce a short `story_plan.md` before rendering:
     - Hook/agenda: “tell them what you will tell them.”
     - Body beats: the complete ideas in order.
     - Recap/CTA: “tell them what you told them.”
   - Use transcript timestamps only to locate source ranges. Never cut mid-idea just to hit a duration.
   - Prefer longer coherent blocks over many word-boundary edits.

4. **Edit decision list**
   - Create a human-readable `edit_decisions.csv` or JSON with:
     - source file, in/out, selected camera angle, reason for cut, story beat, transition type, crop/framing notes, audio source.
   - Every hard cut needs a rationale: new beat, angle change, gesture emphasis, B-roll, title card, or intentional stylistic hit.
   - If the same camera/crop appears on both sides of a cut, use B-roll, a punch-in/punch-out, or dissolve. Do not create visible jump cuts.

5. **B-roll plan and coverage**
   - Treat B-roll as visual evidence, not filler. For each cutaway, record the claim it proves, the story beat it supports, and the edit problem it solves.
   - Build a `broll_plan.json`/CSV before placing B-roll with: beat, spoken line/context, source clip, source in/out, shot type, reason, placement, duration, and whether it covers a jump cut.
   - Prefer a sequence grammar: establishing/wide for context, medium for action, close-up/detail for proof. A single random stock insert is weaker than a planned sequence of coverage.
   - Use authentic or context-matched moments where available. If using stock, reject clips that feel metaphorical but do not visually match the claim, audience, event, or brand world.
   - Use project-native B-roll first: whiteboards, room details, hands, laptops, forms, audience, signage, tea/desk objects, and event/workshop artifacts. These should beat generic stock whenever they prove the speaker's exact claim.
   - Use Coverr as the default free stock B-roll source when native coverage is missing. Every downloaded asset must have a `broll_asset_manifest.json` row with query, source URL, license/attribution note, local path, selected segment, intended beat, and rejection notes for alternates.
   - Build search queries from the story plan, not from generic keywords. Example mappings: "AI falls short" -> `laptop frustration`, "Business Model Canvas" -> `business planning whiteboard`, "small room of entrepreneurs" -> `workshop collaboration`, "free/donation based" -> `community event`.
   - Hold B-roll long enough to read on mobile, usually `1.2s-3.0s`, but avoid covering crucial face/emotion beats unless the A-roll cut is broken.
   - Place B-roll on complete semantic beats: after a phrase lands, at breaths, on new ideas, or over obvious jump cuts. Do not interrupt the sentence fragment that carries the message.
   - Match visual direction and energy when cutting back to A-roll. Avoid disorienting motion, unreadable crops, or unrelated locations that make the viewer ask why they are seeing it.
   - Use full-opacity cutaways or clearly designed picture-in-picture. Low-opacity B-roll over faces is a last-resort texture and must pass still inspection.
   - If the user likes the cut and only wants improvements, do not rebuild the spine just to add B-roll. Add a limited B-roll pass over obvious jump cuts/proof beats, then regenerate captions and verify.

6. **Frame safety**
   - The speaker must remain visible during spoken sections.
   - Reject black or blank camera angles during ingest; do not leave them available for automatic angle selection.
   - Reject any region where the speaker face/body is absent unless covered by intentional B-roll, branded card, graphic, screenshot, or cutaway.
   - For vertical output, keep eyes near the upper third and keep captions out of the face/mouth region and social UI danger zones.
   - Generate verification stills at representative timestamps before final answer.

7. **Audio**
   - Voice is primary. Music is texture.
   - Treat audio as the emotional spine of the edit, not an afterthought filter pass. Build the sequence around the best dialogue stem, then add music, foley, transitions, and picture changes around that spine.
   - Run `scripts/audio_quality_audit.py` before choosing the dialogue source and keep the JSON report with the edit artifacts.
   - Audit channel balance before processing. If a lav/recorder track has one weak channel and one usable channel, duplicate the good channel to centered dual-mono before compression, denoise, music ducking, captions, or Resolve handoff. Do not treat broken stereo as a publish mix.
   - Keep repair/reference audio disabled by default. A bad original camera WAV must not remain enabled underneath a clean dialogue stem.
   - Use ducking/sidechain or very conservative music gain. Do not rely on a fixed loud bed.
   - Run a loudness check. Target social dialogue around `-14` to `-16 LUFS integrated` with true peak below `-1 dBTP`.
   - If music is present, verify it does not mask speech during dense spoken sections.
   - For creator-business and workshop videos, define the audio treatment before rendering:
     - dialogue repair/EQ/compression/limiter,
     - music bed selection and ducking depth,
     - foley/SFX moments,
     - L-cut/J-cut moments,
     - target LUFS and true peak.
   - Add tactile brand foley only when motivated by the visual or transition, such as tea cup, marker, keyboard, paper, or a soft UI tick. Random sound effects are worse than silence.

8. **Color and branding**
   - For PBS/60 Minutes style, use a clean documentary grade: neutral skin, moderate contrast, lifted mids, restrained saturation, no crunchy LUT.
   - Treat logos as brand bugs or title/end cards. Do not cover the speaker’s face.
   - If keying white backgrounds from logos, inspect stills for halos or accidental transparency issues.

8a. **Named Style Target**
   - Before building graphics, captions, music, or B-roll, name the target creator style and write a one-paragraph style brief. Do not render a "generic professional" video.
   - Prefer asset-led production over hand-rolled visual effects when the quality bar is YouTube-native or paid-social-native. Use proven Resolve templates, licensed music/SFX, and style packs before drawing custom FFmpeg overlays from scratch.
   - Before hand-rolling lower-thirds, captions, transitions, or callouts, search for existing local/project assets and known Resolve template sources such as Mixkit, Motion Array, Envato Elements, The Modern Filmmaker, or the user's installed PowerBins/templates.
   - Never use unlicensed music, SFX, templates, or stock footage. If paid assets require account access or purchase, produce an acquisition manifest and ask for access rather than substituting weak generated approximations.
   - Use benchmark-derived style languages, then adapt them rather than copying a creator exactly:
     - `Creator Business Systems` from Deya/Modern Millie: clean, bright, business workflow, key-term overlays, screenshots, calm music.
     - `Evidence-First Productivity Educator` from Ali Abdaal/Vanessa Lau: fast value contract, proof stack, numbered agenda, screen evidence, close vocal.
     - `Guided Session Retention` from MadFit/Chloe Ting/Caroline Girvan: progress/timer, high-key clarity, rhythmic pacing, next-step previews.
     - `Tactile Documentary Teacher` for Chai With Jai: speaker-led authority, whiteboard/canvas evidence, warm studio, tea/keyboard/marker foley, restrained premium graphics.
   - For a Deya-informed workshop/business cut, run a hard style comparison before polishing:
     - camera grammar: main face angle, context angle, evidence angle, screen/slide insert,
     - designed visual system: title cards, checklist/roadmap, key-term overlays, screenshot proof, CTA screen,
     - retention mechanics: no more than 6-9 seconds of uninterrupted A-roll without a visual reset,
     - audio personality: close clean voice, calm music, tasteful UI/desk/tea/marker foley,
     - workflow proof: show the actual framework, page, form, canvas, or artifact being discussed.
   - If the comparison shows the edit is only a captioned podcast cut, stop polishing and rebuild from a storyboard with visual assets first.
   - Score style fidelity separately from technical correctness. A video can pass export checks and still fail because it looks programmatic.
   - For a "5K-view quality bar", require an asset manifest covering visual templates, music bed, foley/SFX, fonts, captions, and color look. If the asset manifest is empty, do not claim premium production value.

9. **Resolve handoff**
   - Prefer creating/importing into a Resolve project/timeline for review:
     - bins: `Video ISO`, `HQ Audio`, `Brand`, `Renders`, `Review`.
     - timelines: one editable timeline and one rendered-master timeline.
   - A flattened rendered master is not an editable deliverable by itself. For user-facing Resolve handoff, create a layered source timeline whenever possible:
     - original camera cuts on their own video track,
     - original dialogue/audio cuts on a repair track,
     - clean dialogue mix on a separate enabled track,
     - original repair audio disabled by default,
     - music, SFX, captions, graphics, B-roll, and master reference on separate named tracks.
   - For HITL review, include a disabled master/reference render on its own track, plus markers for every known benchmark failure. The human editor should be able to compare the source-layer edit against the reference without leaving Resolve.
   - Name tracks by their actual enabled state. Disabled reference, repair, or prior-master tracks must say `DISABLED` in the track name so the user does not mistake them for active publish layers.
   - Add markers for story beats, jump-cut risks, B-roll needs, graphics, and HITL review steps.
   - Run `scripts/resolve_timeline_audit.py` after timeline creation. A Resolve timeline is not usable if clips were inserted before the visible timeline start frame, even when the API reports track counts.
   - After a hillclimb rebuild, verify timeline item source paths, not just clip names. Resolve media pools can contain same-named clips from older cuts; basename reuse can silently attach a stale v1 segment or source repair file to a new v2 timeline.
   - Prefer fresh/versioned bins or force-imported media for each build when source paths matter. Do not reuse a media pool item by name unless its `File Path` matches the intended artifact exactly.
   - If using PNG captions, verify they have alpha transparency. Full-frame black caption PNGs are a blocking bug.
   - If Resolve scripting is unavailable, provide FCPXML/EDL/CSV plus preview render and instructions.
   - Version project exports or outputs; never overwrite the user’s original `.drp`.

10. **Verification before final**
   - Run `scripts/verify_social_export.py <render.mp4> --out-dir <review-dir>`.
   - For captioned social exports, create a burned-in caption review with `scripts/caption_burnin_pipeline.py`. Do not claim captions are done from an SRT/PNG asset alone.
   - Run or record the four-lane benchmark before calling a social edit publishable: video editing craft, creative direction, visual multimodal, and audio multimodal. A strong visual score cannot override failing audio or cut-craft scores.
   - For YouTube/retention-oriented cuts, benchmark against creator videos by observable retention mechanics, not generic polish: first-5-second promise clarity, beat density, pattern-interrupt cadence, evidence B-roll, caption readability, phone mix, CTA placement, and whether each section earns the next minute.
   - Add an `audio desirability` lane to the benchmark with the highest weight for speaker-led educational content. Viewers may forgive imperfect picture, but weak dialogue, muddy EQ, unducked music, or lifeless sound design should block publishing.
   - If a benchmark render adds new hook/CTA graphics on top of an older master, inspect the CTA frame specifically. Baked captions plus a new lower-third can collide even when automated validators pass.
   - For FFmpeg renders with still-image overlays or looped music, hard-cap output duration with `-t` and/or `-shortest`; otherwise a looped logo/music bed can silently extend the render past the edit.
   - Inspect at least opening, first body beat, middle, CTA, and closing frames.
   - Treat multimodal evaluator timestamps as approximate, not authoritative. If Gemini or another critic flags framing, captions, ghosting, or missing speaker presence, extract stills at the cited timestamp and nearby frames before changing the edit. Document any validated false positive in the hillclimb notes.
   - On repeated hillclimbs, prefer replacing fragmented word-boundary cuts with fewer complete semantic blocks before adding more transitions. Smooth audio and coherent story are higher priority than maximal angle switching.
   - Keep attention graphics sparse. QR codes, logos, and event metadata belong in the CTA/details beats, not across the entire edit, and must not compete with the speaker or captions.
   - Avoid video crossfades on talking-head source clips unless the overlap is visually inspected at the transition. In vertical social crops, even short dissolves can read as ghosting/compositing errors; use hard picture cuts with audio crossfades, J-cuts, L-cuts, punch-ins, or B-roll instead.
   - Treat B-roll as intentional coverage, not decoration. For weak talking-head moments or jump-cut repair, use full-opacity cutaways or clearly designed picture-in-picture; do not use low-opacity B-roll overlays that create double-exposed faces, muddy captions, or unclear subject focus.
   - For speaker-led educational reels, do not replace the speaker with a static whiteboard, slide, or prop shot for more than a few seconds. If the user says the speaker is not “in the cuts,” rebuild around speaker-first A-roll and use board/prop content as quick inserts, picture-in-picture, captions, or text overlays.
   - A graphic overlay can pass text-readability QA and still fail the edit if it hides the speaker's face during an A-roll moment. For warm-traffic creator promos, full-screen or large proof cards are allowed only when intentionally functioning as B-roll/title-card coverage; otherwise keep the face/mouth visible and move graphics to side panels, upper corners, or short insert beats.
   - Avoid split-board treatments that duplicate the same board in multiple panels or expose upside-down/irrelevant board writing. If a whiteboard has mixed orientations, crop to the upright claim only or keep it as a brief insert.
   - Avoid duplicate titles from both baked video filters and ASS/top caption layers. Each beat should have one top label and one spoken caption lane at most.
   - When changing vertical crop scale or y-position, force `setsar=1`/square pixels before concatenation and inspect individual stills rather than only very wide contact sheets, which can be misleading in desktop preview.
   - Do not post-process punch-in crops after text/caption compositing unless every overlay lives inside the crop-safe center. Apply punch-ins before graphics/captions, or re-render captions after the motion pass. V10-style late crop passes can make the video feel more dynamic while cutting off title/callout text.
   - If a multimodal evaluator keeps calling the mix "dry" despite technical LUFS passing, treat the music/SFX as perceptually inaudible or too generic. Add an explicit music audibility check against dialogue-only sections, and inspect waveform/spectrogram deltas before claiming a scored audio-effects fix.
   - Do not let "visible effects" become generic flash bars or programmatic rectangles. If the benchmark asks for Mixkit/Fusion-style effects, the pass needs animated title templates, keyframed in/out motion, shadows/blur/separation, and Resolve-editable layers, not just baked FFmpeg drawboxes.
   - Caption placement must be checked against both the speaker's mouth/chin and the bottom social UI safe zone. Prefer short phrase captions with a dark plate and selective brand-color highlights; do not make captions so high that they compete with the face.
   - For near-final caption fixes, use the "caption-only finishing pass": extract dialogue from the approved cut, run word-level transcription, burn short spoken phrase captions, correct only high-confidence domain terms, inspect stills, and rerun social export verification. Do not change picture/audio unless the user asks.
   - Final response must mention:
     - output path,
     - duration/resolution/fps,
     - whether Resolve timeline was updated,
     - known limitations or any checks not performed.

11. **Capstone honesty**
   - Do not count a Loom upload, flat render, or seed timeline as a capstone.
   - A capstone needs an acceptance report with source folder, story plan, edit decisions, layered Resolve validation, export verification, homework/skill evidence when requested, and remaining gaps.
   - If the user asked for workbook homework, every lesson must have a coverage row and per-lesson evidence artifact. If Computer Use times out, mark it `ui_blocked`; do not imply manual UI completion.
   - If the editable Resolve timeline has empty caption/audio/music tracks while the render contains those features baked in, call that out as a handoff limitation.
   - A useful HITL handoff can include both publish timelines and layered repair timelines: publish timelines hold the exact verified master, while repair timelines hold original camera/audio cuts, processed segment spine, and a disabled master reference. Label this clearly so the user knows which timeline to export and which timeline to edit.

## Performance Guidance

Use a two-tier pipeline:

- **Fast analysis/planning:** ffprobe, scene thumbnails, transcript timestamps, rough EDL, low-res proxies.
- **Final render/review:** Resolve timeline, FFmpeg render, or FCPXML/EDL handoff after the plan passes.

For heavy automation or repeat projects, read `references/rust-video-stack.md`. Use Rust for the planner/orchestration layer, but keep FFmpeg/GStreamer/Resolve as the media engines.

## Useful Commands

```bash
python3 skills/davinci-resolve-social-editor/scripts/probe_media.py \
  /path/to/project --out /path/to/project/output/media_manifest.json
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/verify_social_export.py \
  /path/to/render.mp4 --out-dir /path/to/project/output/review
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/resolve_timeline_audit.py \
  --project "Project Name" --timeline "Timeline Name" --out /path/to/project/output/resolve_timeline_audit.json
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/audio_quality_audit.py \
  /path/to/audio-or-project-folder --out /path/to/project/output/audio_quality_audit.json
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/caption_burnin_pipeline.py \
  --srt /path/to/reviewed.srt --ass-out /path/to/netflix_captions.ass \
  --video /path/to/review.mp4 --out /path/to/review_burned_captions.mp4
```

## References

- `references/editing-qa.md`: quality gates for story, jump cuts, frame safety, captions, and audio.
- `references/resolve-automation.md`: Resolve scripting, bins, multicam, FCPXML/EDL, and timeline handoff.
- `references/rust-video-stack.md`: Rust/FFmpeg/GStreamer/OpenCV/Whisper architecture for performant video analysis and rough cuts.
- `references/acceptance-gate.json`: machine-readable gates for layered Resolve handoff, audio, captions, and creative QA.
- `references/reels-eval-benchmark.md`: four-lane Instagram Reels benchmark and failure-to-tool mapping.

---

## FILE: skills/davinci-resolve-social-editor/references/editing-qa.md

# Editing QA Gates

Use these gates before delivering a social edit.

## Story Coherence

The cut must have a visible structure:

1. Hook/agenda: the viewer knows what the event/video is about.
2. Body: complete ideas in an order that can be followed without external context.
3. Recap/CTA: the viewer remembers the promise and knows what to do.

Reject cuts that:

- Start after necessary context.
- Stitch unrelated transcript snippets together.
- Cut out the setup needed to understand a later claim.
- End without repeating the main value proposition.

## Jump-Cut Prevention

Each cut must satisfy at least one:

- new camera angle,
- new crop scale,
- B-roll/graphic/brand card covers the seam,
- crossfade or dip for a section boundary,
- motivated hard cut on emphasis,
- natural pause or sentence boundary.

Avoid same-camera hard cuts across removed words or pauses. If unavoidable, create a punch-in/punch-out or cover with B-roll.

For Instagram Reels, treat same-camera, same-scale consecutive cuts as a benchmark failure. Alternate crop scale, X/Y position, or use B-roll/graphics so the viewer reads the seam as intentional.

## Frame Safety

For speaker-led social video:

- Speaker visible during spoken sections.
- Blank/black camera angles are removed from the selectable angle pool.
- Face not hidden by large logos, captions, or overlays.
- Eyes close to upper third when possible.
- Captions do not cover mouth/face.
- Bottom caption area stays clear of Instagram UI where practical.

Review stills at opening, every major beat, and closing.

## Caption QA

- Proper names must be verified manually.
- Captions should summarize cleanly when the transcript is messy.
- Do not burn in captions from an unreviewed transcript.
- If speeding up a burned-in render, captions remain visually baked; regenerate from source when text changes.
- A caption deliverable is not complete until there is a burned-in review render or visible Resolve caption layer.
- Netflix-style social captions should use large white bold sans text, black outline or translucent black box, bottom-safe placement, and two lines maximum.
- Run `scripts/caption_burnin_pipeline.py` for review renders when Resolve subtitle burn-in is not being exported directly.

## Audio QA

Voice is primary.

- Music should be ducked or mixed low enough that speech remains intelligible.
- Use `loudnorm`, `acompressor`, and/or `sidechaincompress`.
- Check LUFS and true peak. General social dialogue should land around `-16` to `-14 LUFS`; Instagram Reels candidates should target about `-14 LUFS`, with an acceptable gate of `-15` to `-13 LUFS`.
- Listen to dense speech sections, not only intro/outro.
- Run `scripts/audio_quality_audit.py` on HQ audio, embedded camera audio, and any cleaned stems before committing to a source.
- Keep a ranked source report with the edit artifacts; if the chosen source is not the top-ranked source, explain why.
- Treat LUFS as a gate, not a full answer. A pass still needs a human listen check for room tone, pumping, music masking, clipping, and noise-reduction artifacts.

## Render Runtime QA

- Still-image overlays and looped audio must not control final duration.
- Use an explicit duration cap or shortest-stream behavior when a render graph contains looped logos, brand cards, or beds.
- Verify output duration against the edit decision list before importing to Resolve.

## Color QA

For broadcast/documentary style:

- Neutral skin tones.
- Moderate contrast.
- Lifted mids if the set is dark.
- Restrained saturation.
- No heavy vignette or crunchy 90s LUT unless explicitly requested.

---

## FILE: skills/davinci-resolve-social-editor/references/qedc-trace-learnings.md

# QEDC Trace Learnings

Use these findings when future video-editing threads resemble the QEDC workstream.

## Repeated Failure Loops

- User feedback around jump cuts, story coherence, framing, music levels, and captions must become explicit acceptance gates immediately.
- A flat render imported into Resolve is not a usable DaVinci deliverable when the user expects source layers.
- Transcript timestamps locate material; they do not define cuts. Cut on complete ideas, pauses, camera continuity, and B-roll coverage.
- Resolve API success is not enough. Audit `timeline.GetStartFrame()` and reject clips placed before the visible start frame.
- Audio source choice needs a ranked artifact. Silent MIC tracks and weak camera WAVs must be detected before cutting.
- Captions need a visible deliverable. SRT/ASS files alone are not enough; there must be a transparent overlay, Resolve subtitle layer, or burned-in review render.

## New Default Gates

- Story plan before render.
- Audio quality audit before source selection.
- Critic/pro-editor review before final Resolve build.
- Layered Resolve timeline audit before claiming handoff complete.
- Burned-in or transparent Netflix-style captions before social review.
- Repair/original camera audio disabled when clean dialogue is present.

## Tooling Implications

- `resolve_timeline_audit.py` catches invisible timeline and layer/handoff issues.
- `audio_quality_audit.py` catches silent/weak sources and creates a ranking artifact.
- `caption_burnin_pipeline.py` creates reviewable caption renders.
- Project-specific caption PNGs must be alpha-transparent, not full-frame black images.

---

## FILE: skills/davinci-resolve-social-editor/references/reels-eval-benchmark.md

# Instagram Reels Evaluation Benchmark

Use this benchmark when producing speaker-led Instagram Reels, Shorts, or TikTok-style cuts from interview/podcast/event footage.

## Four Evaluators

1. **Video editing craft**
   - Checks semantic beat integrity, cut smoothness, motivated transitions, visual variety, punch-ins, B-roll coverage, J-cuts, L-cuts, and whether the edit respects complete phrases.
   - Blocking failures: same-camera jump cuts without crop/angle change, clipped words, mid-thought cuts, absent split edits on dense A-roll, and unmotivated visual discontinuities.

2. **Creative direction**
   - Checks hook, audience clarity, value proposition, narrative arc, CTA, brand tone, social-native pacing, retention design, and whether on-screen text is public-facing.
   - Blocking failures: internal labels such as `THE HOOK`, weak first three seconds, no clear event promise, no CTA, and draft-looking graphics.

3. **Visual multimodal**
   - Checks native 9:16 framing, speaker frame safety, caption readability, caption safe zone, color/vibrance, graphic design, phone readability, and visual continuity.
   - Blocking failures: speaker out of frame during speech, captions under Instagram UI, dark grade, face covered by logo/graphic, black frames, or unreadable text.

4. **Audio multimodal**
   - Checks dialogue intelligibility, loudness, true peak, edit smoothness, room-tone continuity, noise/reverb control, music masking, and phone competitiveness.
   - Blocking failures: audible pops/clicks, room-tone jumps at cuts, music above dialogue, integrated loudness outside the target range, or clipped/peaked dialogue.

## Targets

- Instagram Reels dialogue loudness: approximately `-14 LUFS integrated`, acceptable range `-15` to `-13 LUFS`.
- True peak: below `-1 dBTP`.
- Audio edit smoothing: 2-4 frame constant-power fades or equivalent room-tone bridge at every dialogue edit.
- Captions: Netflix-style, two-line maximum, above the bottom social UI danger zone.
- Talking speed: 1.1x for speaker-led short-form when intelligibility remains strong.

## HITL Resolve Artifact Requirements

The Resolve timeline is the product, not just the preview render. A usable HITL artifact should include:

- enabled source-layer picture edit,
- enabled clean dialogue/master mix,
- disabled original repair audio,
- optional disabled music/SFX tracks,
- editable captions or caption reference,
- disabled master/reference render,
- track names that explain intent,
- visible timeline start-frame audit,
- markers at every benchmark failure and every human decision point.

## Failure-To-Tool Mapping

- Jump cuts: punch-in/punch-out, angle change, B-roll, J-cut/L-cut, or deliberate transition.
- Clipped words: expand source range, remove partial word, or rebuild the sentence selection.
- Room-tone jumps: constant-power crossfades, continuous room tone bed, denoise, and compression.
- Too quiet for social: loudness normalize to `-14 LUFS`, limit below `-1 dBTP`.
- Draft graphics: remove internal labels; use viewer-facing event promise, CTA, date/time, and brand elements.
- Good visual but failing craft/audio: do not publish; create a repair timeline with exact markers.

---

## FILE: skills/davinci-resolve-social-editor/references/resolve-automation.md

# Resolve Automation Notes

## Resolve Connection

Python scripting normally uses:

```python
sys.path.append('/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp('Resolve')
```

If `resolve` is false, launch Resolve and retry. If `dvr.scriptapp('Resolve')` hangs instead of returning, kill the attempt after a short timeout and switch to an in-Resolve script-menu handoff:

1. Copy the automation script into `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Edit/`.
2. Run it from Resolve's `Workspace > Scripts` menu after saving the current project.
3. Report that the script was installed but do not claim the timeline import succeeded until Resolve visibly creates the project/timeline or the script returns a project/timeline.

Do not claim a Resolve timeline was created unless the API call returns a project/timeline or the GUI has been verified.

## Project Setup

For social vertical edits:

- Timeline resolution: `1080x1920`
- Frame rate: match source unless user requests otherwise.
- Bins:
  - `Video ISO`
  - `HQ Audio`
  - `Brand`
  - `Renders`
  - `Review`

Import original media and rendered masters. Keep the original `.drp` untouched; create versioned projects/timelines.

## Multicam and Sync

Preferred Resolve-native workflow:

1. Import camera ISOs and HQ audio.
2. Use waveform sync / multicam clip / sync bin when audio tracks are usable.
3. Build an editable timeline with multicam angle switches.
4. Use proxies for speed if camera files are heavy.

If Resolve scripting cannot create the full multicam setup reliably, generate:

- `edit_decisions.csv`
- rough preview render
- optional FCPXML/EDL
- imported rendered-master timeline

## FCPXML/EDL Handoff

Use interchange files when the final creative work should be adjusted manually in Resolve. The planner should output source paths, in/out timestamps, track placement, transitions, and markers.

## Timeline Markers

Add markers or a companion CSV for:

- story beats,
- known weak cuts,
- B-roll needs,
- caption/name verification,
- audio/music check points.

## Layered Social Timeline Standard

Do not stop at an imported rendered master when the user expects to keep editing in Resolve. Build a layered timeline with named tracks:

- `V1 ORIGINAL CAMERA CUTS`
- `V2 BUMPER / B-ROLL COVER`
- `V3 GRAPHICS / TITLE CARDS`
- `V4 CAPTIONS / LOGO`
- `V5 MASTER REFERENCE` disabled by default
- `A1 CLEAN DIALOGUE MIX`
- `A2 ORIGINAL DIALOGUE CUTS` disabled or muted by default for repair
- `A3 MUSIC BED`
- `A4 BUMPER / SFX`

Use `AppendToTimeline([{clipInfo}])` with `mediaType`, `trackIndex`, and `recordFrame` to place original media on the intended tracks. Verify with `GetTrackCount()` and `GetItemListInTrack()` after script execution; the GUI can be zoomed or collapsed and may not visibly show all tracks.

## Visible Start Frame Audit

Resolve timelines commonly start at `01:00:00:00`, which is frame `86400` at 24 fps. When using `AppendToTimeline` with `recordFrame`, the value is an absolute timeline frame, not a zero-based offset from the edit start. Insertions at frame `0` can exist before the visible timeline start, causing the API to report clips while the Edit page appears empty or black.

Always compute:

```python
record_frame = timeline.GetStartFrame() + edit_offset_frames
```

After building a timeline, run `scripts/resolve_timeline_audit.py` and reject timelines where any clip starts before `timeline.GetStartFrame()`.

---

## FILE: skills/davinci-resolve-social-editor/references/rust-video-stack.md

# Rust Video Stack

Use Rust as the reliable planning/orchestration layer, not as a replacement for proven media engines.

## Practical Stack

- Rust CLI: project scanning, manifests, scoring, edit decision graph, reproducible plans.
- FFmpeg/libav: decode, trim, concat, filters, loudness, render, mux.
- GStreamer/GStreamer Editing Services: real timeline model, transitions, preview pipelines.
- Whisper/whisper.cpp/Candle Whisper: timestamps and rough transcript.
- PySceneDetect or scene detection stage: visual boundaries.
- OpenCV Rust / CV models: face/subject tracking, crop safety, motion quality.
- Symphonia/Rubato/dasp/hound: native Rust audio decode/resample/DSP analysis.
- Resolve Python/Lua scripting: project/timeline setup and review handoff.

## Planner Model

The missing piece is the edit planner:

```text
raw media
-> media manifest
-> transcript with timestamps
-> semantic segments
-> story beat candidates
-> visual continuity scoring
-> subject framing scoring
-> audio/music scoring
-> edit decision list
-> Resolve/FCPXML/EDL timeline
-> preview render
-> verification artifacts
```

## Cut Eligibility

No cut unless:

1. The idea/sentence boundary is complete.
2. The visual scene is stable or intentionally covered.
3. Speaker face/body remains trackable, or B-roll/graphics cover it.
4. The edit has a transition strategy: angle change, punch-in, B-roll, crossfade, title card, or motivated hard cut.
5. Audio remains continuous or the cut is intentionally masked.

## Suggested Rust Data Types

```rust
struct FrameSafetyScore {
    subject_visible: bool,
    face_centered: f32,
    headroom_ok: bool,
    body_cutoff_risk: f32,
    motion_blur: f32,
}

struct EditDecision {
    source_path: String,
    source_in: f64,
    source_out: f64,
    camera_angle: String,
    story_beat: String,
    transition: String,
    crop: Option<CropWindow>,
    audio_source: String,
    rationale: String,
}
```

## Crate Candidates

- `ffmpeg-next`, `rsmpeg`, `rusty_ffmpeg`, `ez-ffmpeg`: FFmpeg bindings.
- `gstreamer`, `gstreamer-editing-services`: timeline/preview pipeline.
- `symphonia`: safe Rust demux/decode and metadata.
- `rubato`, `dasp`, `hound`: resampling, DSP, WAV.
- `opencv`: face/body/crop analysis.
- `candle`: local ML inference.

Keep the Rust planner deterministic and artifact-heavy. Let humans review EDL/FCPXML/Resolve timelines before final export.

---

## FILE: skills/davinci-resolve-titles-and-lower-thirds/SKILL.md

---
name: davinci-resolve-titles-and-lower-thirds
description: Use when a user needs branded titles, animated lower-thirds, or a logo intro for their video — uses Resolve's Text+ node and Fusion's animation modifiers to create reusable title templates. Triggering symptoms include phrases like "add a name lower third", "animated logo intro", "title card with gradient", "save title as a template", "introduce a guest", or any DaVinci Resolve title/text question.
---

# DaVinci Resolve — branded titles and animated lower-thirds

## Overview

Build animated lower-thirds and title cards using the **Text+** node, then save them as templates that drop into any future timeline. The core principle: the basic **Text** generator is fine for static titles; for anything that needs to animate or look polished, use **Text+** which is Fusion-backed and far more powerful.

## When to use

Symptoms:
- Need to label a person in an interview ("FULL NAME / TITLE")
- Want an animated logo reveal at the start of a video
- Need a chapter divider title card with a gradient or animation
- Want to reuse the same title style across many videos
- The phrase "make it look like a real broadcast"

When NOT to use:
- You need 3D titles or particle effects — use the full Fusion 3D workflow (Advanced VFX Guide pp. 14-19).
- You only need a one-off static slide of text — the basic Text generator (Effects Library > Titles > Text) is faster.

## Quick reference

| Goal | Tool | Where it lives |
|---|---|---|
| Static caption (one line, no animation) | Basic Text generator | Effects Library > Titles > Text |
| Lower-third (name + role, animated) | **Text+** template | Effects Library > Titles > Text+ |
| Animated logo reveal | **Text+** + Follower modifier OR Fusion comp | Effects Library > Titles > Text+ |
| Reusable across projects | Save as Template | Right-click the Fusion comp > Save As Macro |

## Steps

### Build a lower-third using Text+

This is the workflow from Fusion VFX Guide pp. 140-145.

1. On the **Edit** page, position the playhead where you want the lower-third to appear.
2. Open the **Effects Library** (top-left button) > **Titles** category.
3. Drag the **Text+** template onto V2 (above your main video clip) at the playhead.
4. Select the Text+ clip in the timeline.
5. Open the **Inspector** (top right).

### Style the text

1. In the **Styled Text** field, replace `Custom Title` with the person's name in CAPS — e.g. `FULL NAME`.
2. Press **Return** to add a second line. Type their role/title — e.g. `Senior Developer Advocate`.
3. Set **Font**: pick a clean sans-serif. The Resolve PDFs use **Open Sans** at **Extrabold** weight, which is a safe default.
4. Set **Size** to around `0.1` (Text+ uses a 0-1 scale where 1 is the screen height).
5. Scroll down to **H Anchor** (horizontal anchor) and click the **Left** button so text aligns left.

### Position the text

1. Click the **Layout** tab at the top of the Inspector.
2. Adjust **Center X** and **Center Y** to position the text in the lower-third (left side). Typical values: X = `0.1`, Y = `-0.3` (negative Y is below center).
3. Or — from the overlay menu in the lower-left of the viewer, choose **Fusion Overlay** to drag the text directly in the viewer using onscreen handles.

### Add a gradient (the polished broadcast look)

1. Click the **Shading** tab in the Inspector.
2. Under **Type**, choose **Gradient**.
3. The first (white) color stop in the gradient bar sets the lower color of the gradient. Click it, then open the color swatch and pick a light teal.
4. Click the white color stop on the right end. Open the swatch and pick a pale yellow.
5. Scroll down to **Mapping Angle** and drag to `-90` so the gradient runs horizontally across each character.
6. From the **Mapping Level** menu, choose **Line** so the gradient spans the whole word, not each letter individually.

Fusion VFX Guide pp. 142-145 covers this gradient workflow with screenshots.

### Animate the lower-third (slide in from the left)

1. Position the playhead at the start of the Text+ clip.
2. Click the **Layout** tab > find **Center X**.
3. Click the small diamond next to Center X to add a keyframe at the current position.
4. Set Center X to `-1.5` (off-screen left).
5. Move the playhead forward 12 frames (about 0.5 seconds at 24 fps).
6. Set Center X back to `0.1` (your final position). A second keyframe is created automatically.
7. Resolve interpolates between the two keyframes. The lower-third slides in from the left over 12 frames.
8. To smooth the motion: right-click the Center X parameter > **Edit Spline** to open the Spline Editor and convert the keyframes to ease in/out curves.

### Save the lower-third as a template

This is what makes it reusable.

1. With the Text+ clip selected, click the **Fusion** button at the bottom (or press Shift-5) to enter the Fusion page.
2. You will see one node called `Template` (or `Text1`).
3. Right-click the Text+ node > **Save As Macro**.
4. Enter a name like `DEVREL_LOWER_THIRD_v1`.
5. The macro is saved to your local templates folder and shows up in the Effects Library > Titles category for any future project.

Fusion VFX Guide pp. 163-167 covers the Save As Template workflow.

### Use it on the next video

1. New project, new video. Drag your saved template from Effects Library > Titles onto V2 above the speaker's clip.
2. Update the Styled Text in the Inspector with the new name and title.
3. Done — the same animation, gradient, and position carry over.

### Build an animated logo reveal (the merged JTBD)

For a logo intro: same Text+ tooling, slightly different recipe.

1. Add a Text+ clip and replace the text with your brand name (or use a plain Text generator for typography-only logos).
2. Alternatively, drag your logo PNG/SVG from the Media Pool onto V2 — go to the **Fusion** page to compose it with animated background elements (animated shapes, particle systems).
3. For a simple "text appears one letter at a time" reveal: in the Text+ Inspector, set the **Follower** modifier on the Styled Text parameter — see Fusion VFX Guide pp. 153-157 for the Follower modifier workflow.

The Follower walks across each character and applies an animation to that character with a configurable delay between characters. Set the delay to 2 frames per character for a typewriter feel.

## Common mistakes

- **Using the basic Text generator and then trying to animate it** -> the basic Text generator does not expose animation properties cleanly. For anything animated, start with Text+. **(This is the misconception this skill addresses head-on.)**
- **Working in the Inspector and ignoring the on-screen handles** -> the Fusion Overlay (lower-left of viewer > overlay menu > Fusion Overlay) gives you direct manipulation. Faster than typing numbers.
- **Saving the template before perfecting the animation** -> save your template only when you are happy with the timing. Each saved template is hard to update without recreating from scratch.
- **Picking ornate or thin fonts** -> they fall apart at YouTube's compression. Stick to medium-to-bold sans-serif fonts. Open Sans Extrabold (used in the Resolve PDFs) is a safe default.

## Verification

You succeeded if all of the following are true:

1. The lower-third clip on V2 plays back smoothly with the slide-in animation.
2. The gradient on the text is visible — not flat single-color.
3. The saved template appears in the Effects Library > Titles category.
4. Dragging the saved template into a fresh timeline produces the same lower-third with the same animation.
5. Updating the Styled Text on the new instance does not break the animation or gradient.

## Transfer

Now try this: build a *closing* lower-third that slides out (the reverse animation). The keyframe recipe inverts — start at `0.1` (visible) and animate to `1.5` (off-screen right). Save as `DEVREL_LOWER_THIRD_OUT_v1`. Now you have a matched pair you can drop in for the in/out moments of every guest introduction.

## Working reference

- `docs/wiki/fusion-visual-effects.md#lesson-6--creating-title-animations-addendum-pp-139-167` (Text+, gradients, animation, macros — primary)
- `docs/wiki/beginners-guide.md#lesson-2--finessing-the-rough-cut-pp-69-139` (Adding the Logo, Adding the Closing Titles — beginner-tier alt path)
- `docs/wiki/master.md#shared-glossary-terms-that-appear-across-multiple-pdfs` (Text+ / Macro glossary)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (lower-third drift row)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports gradients not appearing, the Follower modifier not animating, or the saved macro missing from Effects Library, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 139-167 (Addendum: Creating Title Animations — complete workflow)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 140-145 (Styling Text in the Edit Page)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 142-145 (Gradient shading — Mapping Level / Mapping Angle)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 145-149 (Moving Text to the Fusion Page)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 153-157 (Follower modifier — for logo reveals)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 163-167 (Saving a Template / Macro)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 122-130 (Adding the Logo, Adding the Closing Titles)

---

## FILE: skills/davinci-resolve-troubleshooting/SKILL.md

---
name: davinci-resolve-troubleshooting
description: Use when DaVinci Resolve is broken in some specific way — red playback indicator, missing media, clips offline, audio out of sync, GPU/render crashes, or render queue stuck. Triggering symptoms include phrases like "Resolve is dropping frames", "media offline", "clips show red diagonal", "audio drifts", "Resolve crashes when rendering", "GPU error", or any DaVinci Resolve "why is X broken" question.
---

# DaVinci Resolve — troubleshoot the 5 most common breakage modes

## Overview

A diagnostic protocol for the five problems that account for ~90% of DaVinci Resolve support questions: dropped-frame playback, missing media, audio sync drift, render crashes, and render queue stalls. The principle: **diagnose before you fix**. Treat the red indicator as data, not a verdict.

## When to use

Symptoms:
- Red GPU/playback indicator during playback
- Clips show a red diagonal slash (offline media)
- Audio drifts out of sync over time
- Resolve crashes mid-render or after a few minutes of rendering
- Render queue says "complete" but the output file is missing or 0 bytes
- "Why is X broken in Resolve" — any of these.

When NOT to use:
- Resolve will not launch at all — that is an install issue (see `davinci-resolve-setup`).
- You are getting a license error — contact Blackmagic support.
- The problem is creative ("I do not like how my edit looks") — not a troubleshooting problem.

## Quick reference — the five diagnostic flows

| Symptom | First check | Then |
|---|---|---|
| Red playback indicator | Run Blackmagic Disk Speed Test on your media drive | If drive is fast enough, generate proxies |
| Clips offline (red diagonal) | Right-click clip > Relink Media | Or change source folder for the bin |
| Audio out of sync | Confirm timeline frame rate matches source frame rate | Use Auto-Sync (waveform or timecode) |
| Crashes during render | Reduce render parallelism, disable hardware acceleration | Check Console for the exact error |
| Render queue stalled at 0% | Check disk space on output drive | Check Custom Export filename for invalid chars |

## Steps — diagnostic flow per problem

### Problem 1: Red playback indicator (dropped frames)

The indicator at the top of the source/timeline viewers turns red when Resolve cannot sustain real-time playback.

**Step 1.1** — Identify the bottleneck. Is it the **drive** or the **GPU**?

- Open **DaVinci Resolve > Preferences > System > Memory and GPU**. Check GPU usage during playback.
- If GPU is below 80% during playback, the bottleneck is the **drive** (read speed).
- If GPU is pinned at 100%, the bottleneck is the **GPU** (rare for talking-head content; common for 4K + heavy color grading).

**Step 1.2** — If the drive is the bottleneck, run Blackmagic Disk Speed Test:

- Free app, install from Mac App Store (macOS) or Desktop Video installer (Windows).
- Point it at your media drive. Look at the "Will It Work?" table. Confirm green checkmarks for your codec at your resolution and frame rate.
- If the drive cannot sustain the required read speed, you have two options:
  1. Move media to a faster drive (NVMe SSD, Thunderbolt).
  2. Generate proxies (see step 1.3).

Editor's Guide p. 326 details Blackmagic Disk Speed Test usage.

**Step 1.3** — Generate proxies if you cannot upgrade the drive.

- In the Media Pool, right-click your clips > **Generate Proxy Media**.
- Choose a proxy format: **H.264 Half-Res 1080p** is a good default for editing.
- Wait for proxies to generate.
- Switch the **Proxy Handling** menu at the top of the viewer to **Prefer Proxies**.
- Playback should now be green.

**Step 1.4** — Before delivery, switch back to camera originals:

- **Proxy Handling > Prefer Camera Originals**. Resolve renders from the high-quality sources, not the proxies.

Editor's Guide pp. 324-337 covers the full proxy workflow including the Blackmagic Proxy Generator separate app.

**The misconception this addresses**: "Red indicator means my computer is too slow." Often it means the drive is too slow, not the GPU. Diagnose first.

### Problem 2: Clips offline (red diagonal slash)

A red diagonal across a clip thumbnail in the Media Pool or timeline means Resolve cannot find the source file at the path it was indexed at.

**Step 2.1** — Determine if it is one clip or all clips.

- If **all clips** in a bin are offline, the source folder has moved or the drive is unmounted.
- If **one or two clips** are offline, those specific files have been moved/renamed.

**Step 2.2** — For all clips offline (typical case: project moved to a new machine):

- Right-click the affected bin > **Change Source Folder**.
- Browse to the actual current location of the media on this machine.
- Click Change. All clips in the bin re-link in one operation.

Editor's Guide p. 336 shows Clip Operations > Change Source Folder.

**Step 2.3** — For individual offline clips:

- Right-click the clip > **Relink Selected Clips**.
- Browse to the file. Resolve relinks just that clip.

**Step 2.4** — If the file genuinely no longer exists:

- Check your backup folder (`davinci-resolve-setup` covers the backup folder location).
- Or check `~/.Trash` / Recycle Bin if you may have deleted it.
- If the file is truly gone, you may need to re-shoot or re-export from the source.

### Problem 3: Audio drifts out of sync

The audio is in sync at the start but drifts over time (e.g. 1 second off after 10 minutes).

**Step 3.1** — Confirm the source clip frame rate matches the timeline frame rate.

- Right-click the source clip in the Media Pool > **Clip Attributes**.
- Note the clip's Frame Rate.
- File > Project Settings > Master Settings > **Timeline frame rate**. Confirm it matches.
- If they differ (e.g. clip is 29.97 fps but timeline is 24 fps), Resolve will interpret the audio differently. This is the most common cause of drift.

**Step 3.2** — Check audio sample rate.

- Clip Attributes > Sample Rate (typically 48000 Hz).
- Project Settings > Master Settings > Sample Rate. Match them.

**Step 3.3** — If video and audio were recorded separately (dual-system audio), re-sync them.

- In the Media Pool, select the video and audio clips together.
- Right-click > **Auto Sync Audio**.
- Choose **Based on Waveform** (works without timecode) or **Based on Timecode** (faster if both have matching timecode).
- Resolve aligns the two clips into a single synced clip.

Editor's Guide pp. 267-277 covers the audio sync workflow.

**Step 3.4** — For drift caused by drifting hardware clocks (e.g. external audio recorder vs camera):

- Use the **Stretch** parameter on the audio clip in the Inspector to slow/speed by tiny amounts (0.5% or less).
- Or split the audio into multiple sections and re-sync each section.

### Problem 4: Resolve crashes during render

**Step 4.1** — Check the Console for the actual error.

- **Workspace > Console** opens the Console panel.
- Look at the last messages before the crash. Common causes:
  - "Out of memory" — reduce render frame rate or close other apps
  - "GPU error" — disable hardware decoding (see 4.2)
  - "File system error" — disk full or drive disconnected

**Step 4.2** — Disable hardware acceleration if you see GPU errors.

- **Preferences > Decode Options** > uncheck **Decode H.264/H.265 using hardware acceleration**.
- This is slower but more stable, especially on older or mixed-GPU systems.

**Step 4.3** — Reduce render concurrency.

- Some Resolve crashes during render are caused by trying to use both GPUs (in a dual-GPU machine).
- **Preferences > System > Memory and GPU** > set GPU processing mode to **CUDA** or **Metal** explicitly (not Auto).
- Restart Resolve.

**Step 4.4** — Free disk space.

- Renders need 2-3x the source file size as scratch during processing.
- Check that both your media drive and your output drive have at least 50 GB free.

### Problem 5: Render queue stalls at 0%

A render shows "Render in Progress" but the file size on disk does not grow.

**Step 5.1** — Check the output filename for invalid characters.

- macOS file systems do not allow `:` in filenames. Windows does not allow `< > : " / \ | ? *`.
- If your render preset has `%timeline_name` and your timeline name contains a colon or slash, the render will silently fail.
- Rename the timeline first, or change the Custom Export filename to use plain characters.

**Step 5.2** — Confirm the output folder exists and is writable.

- Check the **Location** field in Render Settings. Browse to it manually in Finder/Explorer.
- If it does not exist, create it.
- If it exists but is owned by another user, change permissions or pick a different location.

**Step 5.3** — Reduce the render frame range.

- If a specific clip is corrupted, the render hangs on that frame.
- In Render Settings, change **Render** from "Entire Timeline" to "In/Out Range" and set an Out point before the suspected bad frame.
- If that completes, walk forward by a few seconds at a time to find the problem frame.

**Step 5.4** — Restart Resolve.

- If all the above fail, kill Resolve (Force Quit on macOS, Task Manager on Windows) and reopen the project. Render queue often stalls after a long session and a restart clears it.

## Common mistakes

- **Assuming red indicator = old computer** -> often it is the drive, not the GPU. Diagnose with Blackmagic Disk Speed Test first. **(This is the misconception this skill addresses head-on.)**
- **Re-importing offline clips instead of relinking** -> you lose all your edits if you re-import. Always relink.
- **Letting Resolve auto-select GPU in dual-GPU systems** -> manually set it to CUDA or Metal explicitly. Auto can cause crashes.
- **Naming timelines with colons or slashes** -> renders silently fail. Stick to alphanumerics, underscores, dashes.

## Verification

You succeeded if all of the following are true:

1. Playback indicator is green during a 30-second play-through of your timeline.
2. Every clip in your Media Pool has a thumbnail (not a red diagonal).
3. Audio waveform aligns with video action throughout the timeline (clap on the slate matches the slate visual; mouth movements match speech).
4. Render completes and the output file is the expected size and duration.
5. You can identify which of the 5 problems applied (or no problem applied) by name.

## Transfer

Now try this when you encounter a *new* breakage mode — say, a Fusion comp that will not render correctly. Apply the same diagnostic protocol: (1) identify the symptom precisely, (2) check the Console for an actual error message, (3) reduce scope (render just that one Fusion comp segment) to isolate the cause, (4) test a fix on a copy before applying to the project. This problem-solving discipline scales beyond the five cases above.

## Working reference

- `docs/wiki/editors-guide.md#lesson-6--ai-workflows-pp-323-387` (Disk Speed Test, proxies, relink workflows — primary)
- `docs/wiki/editors-guide.md#lesson-5--project-organization-pp-245-321` (audio sync, frame-rate matching)
- `docs/wiki/colorist-guide.md#lesson-8--adjusting-image-properties-pp-343-379` (Render Cache for Color-page playback)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (every troubleshooting symptom row maps here)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports the diagnostic flow didn't fix the symptom (red playback returns, clips still offline, render still fails), read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 326 (Is Your Drive Fast Enough? — Blackmagic Disk Speed Test)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 324-340 (Generating Proxy Files — complete workflow including Blackmagic Proxy Generator)
- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 336 (Change Source Folder for bulk relink)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 267-277 (Syncing Audio to Video and Channel Configuration)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 597-617 (Customizing Deliver Presets, render failure causes)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 6-8 (Relinking the Media Files)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 350-364 (Syncing Audio to Video)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 369-377 (Optimizing Performance with Render Cache — for color page playback)

---

## FILE: skills/social-video-folder-autocutter/SKILL.md

---
name: social-video-folder-autocutter
description: Plan repeatable hard-drive folder-to-video pipelines for speaker-led multicam content, including 9:16 Reels/Shorts up to 3 minutes at 1.1x talking speed and 16:9 long-form 3-7 minute cuts, with Resolve handoff, Editframe asset generation, audio/caption gates, and narrative beat planning.
---

# Social Video Folder Autocutter

Use this before editing when the user wants a repeatable pipeline from a folder of camera/audio files into social or long-form cuts.

## Output Profiles

- **Vertical social:** `1080x1920`, 9:16, up to 3 minutes, default 1.1x speed for speaker-led sections, Netflix-style captions, source layers preserved in Resolve.
- **Horizontal long-form:** `1920x1080`, 16:9, 3-7 minutes, default normal speed, lower thirds/captions optional, source layers preserved in Resolve.

## Required Pipeline

1. Scan the folder:
   - run the DaVinci skill `probe_media.py`;
   - run `audio_quality_audit.py`;
   - identify camera ISOs, HQ audio, intro/bumper, brand files, old renders, and existing Resolve exports.
2. Make a story plan:
   - hook/agenda,
   - body beats,
   - recap/CTA,
   - rejected or risky segments.
3. Build edit decisions:
   - source file, in/out, angle, reason, transition, crop, audio source, caption text.
   - reject word-boundary-only cuts.
4. Build a B-roll coverage plan:
   - assign B-roll only where it proves a claim, establishes the event world, covers a jump cut, compresses time, or gives the audience an emotional/visual release.
   - tag every B-roll candidate as `wide`, `medium`, `close-up`, `insert/detail`, `environment`, `screen/product`, or `human moment`.
   - prefer wide/medium/close-up sequences over isolated filler shots.
   - require source page/licensing metadata for stock footage and store it with the manifest.
   - reject low-opacity overlays over faces unless the user explicitly asks for texture; default to full-opacity cutaways or designed picture-in-picture.
   - On warm-traffic educational reels, use B-roll sparingly as proof/coverage. Keep the speaker on screen for trust-building beats, and reserve stock inserts for claims about work, learning, planning, community, or tool use.
   - If the speaker is physically demonstrating a concept, prioritize that performance over generic B-roll. Use the board/prop as a quick visual aid, not a long replacement for the speaker.
   - Reject static whiteboard/slide replacements longer than `3s-5s` unless the user explicitly asks for a screen-recording style lesson. For Instagram, the speaker should remain visible across spoken educational beats.
   - Keep B-roll source URLs/license notes in the plan, and keep raw B-roll sources disabled on a separate Resolve track for HITL replacement.
   - Use Coverr as the default free B-roll source when the project lacks enough native visual evidence. Store search query, source URL, creator/source attribution, license URL, download path, and rejection reason for any candidate not used.
   - Coverr licensing/API notes must be recorded with the manifest: free downloads require attribution credit unless the account/license says otherwise; API usage requires clickable Coverr attribution; do not use Coverr assets for AI training/datasets or to build a competing stock/video service.
   - For Chai With Jai workshop promos, default search intents should include: `small business owner`, `entrepreneur workshop`, `business planning`, `whiteboard`, `team collaboration`, `laptop work`, `coffee meeting`, `Jersey City`, `AI technology`, `coding`, `marketing campaign`, and `community event`.
   - Prefer Coverr clips that can function as visual evidence for a spoken claim. Reject generic city lights, abstract technology, slow lifestyle filler, or anything with identifiable brands/trademarks unless the usage is clearly safe.
5. Generate review artifacts:
   - low-res proxy or stills for critic review,
   - audio ranking JSON,
   - caption preview,
   - Resolve/FCPXML/EDL plan.
6. Build the real handoff:
   - Resolve layered timeline for final editing,
   - original repair audio disabled,
   - clean dialogue and music separated,
   - graphics/captions/B-roll on separate tracks,
   - timeline audit passes.

## Winning Instagram Reels Loop

Use this loop when a prior cut is close and the user says it is nearly postable:

1. **Preserve the liked picture cut.** Do not re-edit the spine unless the user asks. Export or locate a picture spine without burned captions when possible.
2. **Caption from actual speech timing.** Extract dialogue from the liked cut, run Whisper word-level transcription, and build short burned-in phrase captions. Correct only high-confidence domain terms such as names, event titles, dates, and obvious ASR artifacts.
3. **Keep caption text spoken-first.** Do not replace spoken captions with topic cards. Topic cards may remain as a separate top lane, but the lower caption lane must match what the speaker says.
4. **Verify phone-safe stills.** Inspect opening, mid-body, B-roll/whiteboard, CTA, and closing frames. Captions must avoid the speaker's mouth/chin and Instagram's bottom UI region.
5. **Verify audio.** Target `-14` to `-16 LUFS` integrated, true peak below `-1 dBTP`, with music ducked under speech.
6. **Only then hillclimb B-roll.** Add B-roll where it solves a specific edit problem: jump cut coverage, proof of a claim, visual explanation, location/event context, or emotional reset.

## Required Output Artifacts For Repeat Use

For each folder cut, create or update:

- `story_plan.md`
- `edit_decisions.csv` or `.json`
- `broll_plan.json`
- `broll_asset_manifest.json`
- `caption_chunks.txt`
- `captions.ass` or Resolve caption track
- `verification_report.json`
- Resolve timeline or handoff report

## Editframe Role

Use Editframe in parallel for motion assets, not as the primary NLE when the user expects Resolve source layers.

Good uses:

- animated branded bumpers,
- Netflix-style/word-highlight caption assets,
- lower thirds,
- waveform/title cards,
- social-safe graphic overlays,
- fast HTML/React review proxies.

Avoid using Editframe as the only deliverable for source-camera editing unless the user explicitly wants a rendered web-video output. Editframe renders can be imported back into Resolve as V3/V4 graphics or bumper layers.

## Handoff Contract

Never call the job done unless these artifacts exist:

- media manifest,
- story plan,
- edit decisions,
- audio quality audit,
- caption artifact or burned-in review,
- layered Resolve timeline or interchange file,
- timeline audit report.

## Useful Command

```bash
python3 skills/social-video-folder-autocutter/scripts/create_folder_cut_brief.py \
  /path/to/project-folder --out /path/to/project-folder/output/folder_cut_brief.json
```

Then use `davinci-resolve-social-editor` for the Resolve build.
