# tashisleepy/capcut-ai-director

- **Repo:** tashisleepy/capcut-ai-director — CapCut Desktop Pro ke liye AI Editing Director (agent + 380KB knowledge base + MCP server)
- **Link:** https://github.com/tashisleepy/capcut-ai-director
- **Licence:** MIT (repo page par verify; LICENSE file root me hai)
- **Activity:** 3 stars · 1 fork · 3 commits · repo bana 2026-04-04 (repo page, 2026-11-06) — chhota repo, lekin CapCut-specific technique knowledge is round me sabse ghana yahi mila
- **Content map:** Two-stage directing system (Stage 1 pure creative analysis: pacing/emotion/energy; Stage 2 CapCut asset-grounding), frame-based timecode HH:MM:SS:FF, Creative Modes (Viral/Cinematic/Documentary/Meme/Aesthetic/Minimal — intensity 1-5 ke saath), smart-cut niyam (silence gaps >1s), hook/body ke timestamped plan examples. Neeche: README, agents/capcut-director.md, brain (director ka poora creative system), dono examples, aur knowledge-base ke technique-wale files — KF-01 (UI navigation/workflow), KF-05 (text/captions), KF-07 (audio & music intelligence — mixing), KF-09 (top-150 effect metadata with use guidance), KF-10 (AI stylize).
- **Na liye gaye catalog files (asset name lists, technique nahi):** KF-02 all-effects (3,467 effects, 85KB), KF-03 transitions (2,225), KF-04 filters (600+), KF-06 stickers (50+ categories), KF-08 animations — ye sirf naam/category catalogs hain; counts README/brain me darj hain.

---

# capcut-ai-director

**The first AI editing director for CapCut Desktop Pro.** Upload a video. Get frame-accurate, timestamped editing instructions with real CapCut asset names. No vague advice. No hallucinations. Surgical precision.

---

## What This Does

You film. AI directs. You execute.

Instead of "add some transitions here," you get:

```
00:00:05:00
Action: Add Flash transition (duration: 00:00:00:06)
Path: Left panel → Transitions → Trending → Flash
Why: Beat drop in background audio. Flash aligns with energy spike
```

### Before vs After

| Traditional AI Feedback | capcut-ai-director |
|---|---|
| "The opening is slow, add some pacing" | "00:00:00:00-00:00:02:00: Cut initial silence. Dead air kills retention in first 2s" |
| "Use a transition between these shots" | "00:00:05:00: Add Flash transition (6 frames). Left panel → Transitions → Trending → Flash" |
| "Add captions for emphasis" | "00:00:02:00: Add caption 'This changed everything'. Style: Bold Impact. KF-05 Bold Impact template #7" |
| "Color grade to match mood" | "00:00:08:15: Apply AI Stylize with Preset ID: warm-cinematic-35. Strength: 0.7" |

---

## Quick Demo

**Input:** Your video file (any length, any format CapCut supports)

**Output:** Timestamped editing plan across three stages

```markdown
VIDEO EDIT PLAN
Platform: TikTok
Intensity: 4
Mode: Viral
Frame Rate: 30fps

═══════════════════════════════════════════

HOOK SECTION (00:00:00:00-00:00:04:00)

00:00:00:00-00:00:02:00
Action: Cut initial 2-second silence
Navigation: Right panel → Timeline → select segment → Delete
Why: Dead air kills retention in first 2 seconds

00:00:02:00
Action: Add text overlay - "Watch to the end"
Style: KF-05 #12 Bold Impact White
Duration: 00:00:00:20 (duration on screen)
Position: Center of frame
Why: Anchors viewer attention before hook payload

00:00:02:15
Action: Add zoom animation
Effect: Zoom-In
Amount: 108%
Duration: 00:00:00:12
Easing: Ease-Out
Why: Emphasis on speaker's vocal inflection.visual punch

═══════════════════════════════════════════

BODY SECTION (00:00:04:00-00:00:12:00)

00:00:05:00
Action: Add transition before dialogue shift
Type: Flash transition (KF-03 #14)
Duration: 00:00:00:06
Navigation: Left panel → Transitions → Trending → Flash
Why: Audio beat drop at this moment.Flash snaps with energy

...
```

Every timestamp. Every asset. Every "why."

---

## Architecture

```
USER VIDEO
    ↓
┌─────────────────────────────┐
│ Stage 1: Free Analysis      │
│ (Gemini multimodal)         │
│ - Scene detection           │
│ - Speech/emotion/beats      │
│ - Silence & attention       │
└────────────┬────────────────┘
             ↓
    Creative brief (no CapCut)
             ↓
┌─────────────────────────────┐
│ Stage 2: Asset Grounding    │
│ (KF-01 through KF-10        │
│  injected into prompt)      │
│ - 3,467 effects             │
│ - 2,225 transitions         │
│ - 600+ filters              │
│ - 200+ text templates       │
│ - 50+ sticker categories    │
│ - 10 Knowledge Files        │
└────────────┬────────────────┘
             ↓
    FRAME-ACCURATE EDITING PLAN
    (with exact asset names &
     navigation paths)
```

**Two-stage prompting** separates free creative thinking from grounded execution. Stage 1 prevents the asset catalog from constraining ideas; Stage 2 ensures every suggestion uses real CapCut tools.

---

## Installation

### Requirements
- Claude Code, Claude Desktop, Cursor, or VS Code
- Python 3.10+
- CapCut Desktop Pro installed (for opening/executing plans)

### Step 1: Clone the repo
```bash
git clone https://github.com/tashisleepy/capcut-ai-director.git
cd capcut-ai-director
```

### Step 2: Set up the MCP server
```bash
cd mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Step 3: Configure Claude Code / Claude Desktop

Add to your `claude_desktop_config.json` (Mac: `~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "capcut-director": {
      "command": "/path/to/capcut-ai-director/mcp-server/venv/bin/python",
      "args": ["-m", "smartcut.server"]
    }
  }
}
```

**Windows path example:**
```json
"command": "C:\\Users\\YourName\\capcut-ai-director\\mcp-server\\venv\\Scripts\\python.exe"
```

### Step 4: Restart Claude Code or Claude Desktop

The `capcut-director` MCP server is now available. Claude can now:
- List your CapCut projects
- Open and inspect projects
- Smart-cut (silence + duplicate removal)

---

## Usage

### In Claude Code / Claude Desktop

**Direct the edit of a video:**
```
I just filmed a product demo. Can you direct the edit for TikTok?
Use viral intensity (4/5), and assume 30fps.
My CapCut file is "Product Demo - Take 3".
```

**Result:** Timestamped editing plan with every action, path, and reason.

### Available MCP Tools

| Tool | Use | Example |
|------|-----|---------|
| `list_capcut_projects` | See your drafts | "Show me my CapCut projects" |
| `open_capcut_project` | Inspect a project | "Open 'My Vlog' project" |
| `smart_cut_project` | Auto-cut silences + duplicates | "Smart cut 'Podcast #5'" |

---

## Knowledge Base

**380 KB of structured CapCut intelligence** across 10 Knowledge Files:

| KF | Content | Count |
|---|---|---|
| KF-01 | Core UI Navigation (left panel, right panel, timeline controls) | 538 lines |
| KF-02 | All Effects (name, icon, category, use case) | 4,042 lines |
| KF-03 | Transitions (all 2,225 variations with metadata) | 2,393 lines |
| KF-04 | Filters (600+ with names & previews) | 186 lines |
| KF-05 | Text & Captions (200+ templates, fonts, styles) | 744 lines |
| KF-06 | Stickers (50+ categories, naming convention) | 651 lines |
| KF-07 | Audio & Music Intelligence (Suno integration, mixing tips) | 1,123 lines |
| KF-08 | Animations (preset names, easing, duration) | 586 lines |
| KF-09 | Effect Metadata (top 150 effects, advanced settings) | 1,447 lines |
| KF-10 | AI Stylize (presets, strength settings, mood matching) | 211 lines |

**Total:** ~13,000 lines of actionable CapCut knowledge.

---

## Creative Modes

Choose your edit style. AI adapts intensity and asset selection accordingly.

| Mode | Vibe | Best For | Intensity | Example Output |
|------|------|----------|-----------|---|
| **Viral** | Fast cuts, hooks, rapid fire | TikTok, Reels, YouTube Shorts | 4-5 | Flash + zoom + captions every 2s |
| **Cinematic** | Smooth transitions, color grading, depth | Brand films, product launches, vlogs | 2-3 | Slow dissolves, subtle color grades, 12-frame transitions |
| **Documentary** | Pacing, lower thirds, voiceover emphasis | Explainers, interviews, podcasts | 2-3 | Silence cuts, text overlays, subtle zoom |
| **Meme** | Jump cuts, speed ramps, sound effects | Comedy, reaction, trending audio | 5 | Hard cuts, 2-4 frame transitions, rapid captions |
| **Aesthetic** | Color-first, filters, minimal movement | Fashion, luxury, interior, mood content | 1-2 | AI Stylize preset, one slow zoom, minimal transitions |
| **Minimal** | Clean, breathing room, intentional pauses | Conferences, slow-burn storytelling, ASMR | 1 | Hard cuts only, no effects, text only when necessary |

---

## Examples

### Example 1: TikTok Product Demo (Viral, Intensity 4)

**Command:**
```
Direct the edit for my product demo "iPhone Case Unboxing".
Platform: TikTok
Mode: Viral
Intensity: 4
Frame rate: 30fps
```

**Output snippet:**
```
HOOK (00:00:00:00–00:00:03:00)

00:00:00:00–00:00:01:00
Action: Cut silence (B-roll of hand moving to box)
Why: Hook must start with action, not dead air

00:00:01:00
Action: Add text "This case is INSANE"
Style: KF-05 #8 (Bold Impact, white outline)
Duration: 00:00:00:18
Why: Establish value claim before unboxing

00:00:01:15
Action: Zoom to 110% over 00:00:00:12 (12 frames)
Easing: Ease-Out
Why: Vocal stress on "INSANE".zoom reinforces emphasis

00:00:02:00
Action: Hard cut to close-up of case
Transition: None
Why: Action change + audio beat.hard cut is cleanest
```

### Example 2: LinkedIn Thought Leadership (Cinematic, Intensity 2)

**Command:**
```
I'm talking about the future of AI (2:14 video).
Platform: LinkedIn
Mode: Cinematic
Intensity: 2
Frame rate: 30fps
```

**Output snippet:**
```
INTRO (00:00:00:00–00:00:10:00)

00:00:00:00–00:00:02:00
Action: Slow dissolve from black to speaker
Transition: Dissolve (KF-03 #45)
Duration: 00:00:01:00
Why: Cinematic entrance.builds anticipation

00:00:02:15
Action: Add lower-third graphic "AI transformation"
Style: KF-05 #3 (Corporate, sans-serif, left-aligned)
Duration: video length (stays on screen)
Why: Professional context + speaker intro

00:00:05:00
Action: Apply AI Stylize."warm corporate"
Preset: KF-10 #2 (warm-professional-40)
Strength: 0.65
Why: Color grade supports "optimistic future" narrative
```

---

## MCP Tools

The backing MCP server provides three core tools:

### `list_capcut_projects`
Lists all CapCut projects in your drafts folder.
```
INPUT: (none)
OUTPUT: [
  { name: "Product Demo - Take 3", path: "...", created: "2026-04-01" },
  { name: "Podcast #5", path: "...", created: "2026-03-28" },
  ...
]
```

### `open_capcut_project`
Opens and inspects a CapCut project. Returns video segments, text, audio, effects currently applied.
```
INPUT: { project_name: "Product Demo - Take 3" }
OUTPUT: {
  segments: [...],
  text_elements: [...],
  audio_tracks: [...],
  applied_effects: [...]
}
```

### `smart_cut_project`
Auto-removes silences (gaps > 1s between subtitles) and duplicate takes.
Requires auto-generated subtitles in CapCut (Text → Auto Captions).
```
INPUT: { project_name: "Podcast #5" }
OUTPUT: { removed_ranges: [...], duplicates_removed: [...] }
```

---

## Timecode Format

All editing instructions use CapCut's native **frame-based timecode**: `HH:MM:SS:FF`

| Example | Meaning |
|---------|---------|
| `00:00:00:00` | Frame 0 |
| `00:00:00:15` | Frame 15 (0.5 sec at 30fps) |
| `00:00:01:00` | Frame 0 of second 1 (exactly 1.0 sec) |
| `00:00:10:00` | 10 seconds |
| `00:01:00:00` | 1 minute |

**Range example:** `00:00:01:00-00:00:03:15` = from 1.0s to 3.5s

**At 30fps, valid frames are 00–29.** Frame 30 doesn't exist; it rolls to 00:00:01:00.

Why frame-accurate? Because the CapCut timeline displays frames. Direct timecode matching = zero conversion errors.

---

## Pricing & Commercial Use

**MIT License** - free for personal and commercial use. Fork, modify, deploy.

---

## Contributing

Issues, feature requests, and PRs welcome.

**For knowledge file updates** (new effects, transitions, filters added to CapCut):
1. Submit PR updating relevant KF file
2. Include CapCut version tested
3. Include screenshot evidence of new asset in CapCut UI

**For mode additions** (new creative styles beyond Viral/Cinematic/etc):
1. Define the intensity curve and asset selection rules
2. Include 3 example outputs
3. PR against `brain/capcut-ai-director-brain.md`

---

## Credits

- **Brain architecture:** [Tashi](https://github.com/tashisleepy)
- **CapCut UI mapping:** 101 screen recordings + 193 panel screenshots + expert review feedback
- **Knowledge files:** Community contributors + CapCut desktop research
- **Two-stage prompting:** Inspired by frontier AI directing work in commercial production

---

## License

MIT

---

## FILE: agents/capcut-director.md

# CapCut AI Editing Director

## Role
You are Tashi's CapCut AI Editing Director. You combine two powers:
1. **CapCut MCP** - direct read/write access to CapCut Desktop Pro projects (timelines, subtitles, segments, smart-cut)
2. **CapCut Knowledge Base** - 10 knowledge files covering every CapCut asset (3,467 effects, 2,225 transitions, 600+ filters, 200+ text templates, animations, stickers, audio, AI stylize)

You analyze footage, generate surgical timestamped editing instructions using real CapCut asset names, and execute automated cuts (silence removal, duplicate detection) directly on the project files.

## System Architecture

```
USER: "edit my latest CapCut project"
  |
  v
STEP 1: Read project via MCP (list_capcut_projects -> open_capcut_project)
  |
  v
STEP 2: Analyze footage structure (segments, subtitles, timing, gaps)
  |
  v
STEP 3: Stage 1 - Pure creative analysis (pacing, emotion, energy, weak spots)
  |
  v
STEP 4: Stage 2 - Ground suggestions in CapCut KB (exact asset names from KF-01 through KF-10)
  |
  v
STEP 5: Output timestamped editing instructions in HH:MM:SS:FF format
  |
  v
STEP 6: Execute automated cuts if requested (smart_cut_project via MCP)
```

## Two-Stage Prompting (Core Design)

**Stage 1 - Pure Free Analysis** (no CapCut mentioned)
Analyze pacing, emotion, energy, color, movement, audio, story. No constraints. No asset names. Let creative thinking run free.

**Stage 2 - Grounded Suggestions** (CapCut KB injected)
Feed Stage 1 analysis + CapCut catalog into suggestions. Every suggestion MUST reference exact asset names from the Knowledge Base. Zero hallucinated tools.

This separation prevents the catalog from constraining creative thinking while ensuring every output is actionable with real CapCut assets.

## Timecode Format (Critical)

CapCut uses frame-based timecode: `HH:MM:SS:FF` (not decimal seconds)
- 30fps default: frames 00-29, then second increments
- `00:00:02:15` = 2 seconds and 15 frames (2.5 seconds)
- There is NO frame 30 - after :29 the second increments
- Always check project frame rate (24/30/60fps)

## Output Format

```
VIDEO EDIT PLAN
Platform: [TikTok / YouTube / Instagram / General]
Intensity: [1-5]
Mode: [Editing Instructions / Viral Optimization / Cinematic / Minimal Clean]
Frame Rate: 30fps

HOOK SECTION (00:00:00:00-00:00:04:00)

00:00:00:00-00:00:02:00
Action: [specific action]
Find it: [exact CapCut panel path from KB]
Why: [reason]

[... continues per section]

EDITING REVIEW
Pacing: [assessment]
Hook strength: [assessment]
Weak spots flagged: [count]
```

## Rules
- Every action gets a CapCut-native timecode (HH:MM:SS:FF)
- Every action gets a "Why" explanation
- Every CapCut asset reference includes the panel navigation path ("Left panel -> Transitions -> Trending -> Shaky Inhale")
- Subjective choices get 2-3 alternatives
- Weak spots (dead air, pacing drops) flagged explicitly
- Instructions grouped by section (Hook / Body / Ending)
- Highlight moments called out with star marker

## Attention Rules
- Visual change gap > 3 seconds -> suggest pattern interrupt
- Pause > 0.5s in talking-head -> suggest jump cut
- Pause > 1.0s -> flag as weak spot
- Max 1 zoom per 5 seconds
- Max 2 transitions per 10 seconds
- Cuts > transitions (invisible editing is professional editing)
- Less is more - every edit must have a reason

## Creative Modes
| Mode | Description |
|------|------------|
| Cinematic | Film-style, slow pacing, dramatic lighting |
| Viral | Fast cuts, captions, pattern interrupts every 2-3s |
| Documentary | Slower pacing, lower thirds, clean |
| Meme | Jump cuts, zooms, sound effects, chaos |
| Aesthetic | Color-focused, smooth, dreamy |
| Minimal | Clean cuts only, professional |

If no mode specified, analyze the video and decide.

## Intensity Levels
1. Minimal - clean cuts, no effects
2. Cinematic - subtle color, gentle zooms
3. Social Media - captions, moderate effects
4. Viral - fast-paced, heavy captions, motion
5. Chaos - maximum effects, meme energy

## Knowledge Base Reference
Load these from the repo's `knowledge-base/` directory as needed:
- `KF-01-core-ui-navigation.md` - UI panels, shortcuts, navigation paths
- `KF-02-all-effects.md` - 3,467 video effects + body effects (85 KB)
- `KF-03-transitions.md` - 2,225 transitions, 13 categories (41 KB)
- `KF-04-filters.md` - 600+ filters, 14 categories (20 KB)
- `KF-05-text-captions.md` - 200+ text templates (33 KB)
- `KF-06-stickers.md` - 50+ sticker categories (29 KB)
- `KF-07-audio-music-intelligence.md` - Audio, sound effects, music (50 KB)
- `KF-08-animations-complete.md` - All animation presets (34 KB)
- `KF-09-effect-metadata-top150.md` - Top 150 effects with full metadata (55 KB)
- `KF-10-ai-stylize.md` - AI style transfer presets (6 KB)

## MCP Tools Available
When the capcut-smartcut MCP is connected:
- `list_capcut_projects` - list all CapCut projects on disk
- `open_capcut_project` - read project structure, segments, subtitles
- `smart_cut_project` - auto-remove silences and duplicate takes

## Workflow

1. **"List my projects"** -> call list_capcut_projects, show names + durations
2. **"Open [project]"** -> call open_capcut_project, analyze structure
3. **"Edit this"** -> Two-stage analysis, load relevant KFs, output edit plan
4. **"Smart cut this"** -> call smart_cut_project to auto-remove silences/duplicates
5. **"Make it viral"** -> Viral mode analysis with platform-specific optimization
6. **"What effects should I use?"** -> Load KF-02/KF-09, recommend based on content

## Important
- NEVER hallucinate CapCut asset names. Only reference assets from the KF files.
- ALWAYS use HH:MM:SS:FF timecodes, never decimal seconds.
- ALWAYS include navigation paths so the editor can find assets quickly.
- Duplicate your project in CapCut BEFORE running smart_cut (no auto-backup).
- When analyzing video files directly, use FFmpeg to extract frames/audio for analysis.

---

## FILE: brain/capcut-ai-director-brain.md

# CapCut Desktop Pro — AI Editing Director Brain File

> **Platform:** CapCut Desktop Pro (Mac, dark theme)
> **Product identity:** Upload your video and get professional editing instructions generated by AI.
> **What it is:** An AI editing director that watches footage and delivers surgical, timestamped editing instructions grounded in real CapCut Desktop Pro assets.
> **What it is NOT:** A video editor. It does not perform edits. It tells you exactly what to do, where, and why.
> **Last updated:** 2026-03-10
> **Sources:** Screen recordings (hires-v1: 30 frames + hires-v2: 71 frames = 101 frames) + 193 panel screenshots + three rounds of expert feedback
> **Knowledge Files:** KF-01 through KF-10

---

# PART A — DIRECTING SYSTEM

## 1. SYSTEM ARCHITECTURE

```
USER VIDEO
↓
Gemini multimodal analysis (Stage 1 — pure creative)
↓
Scene segmentation
Speech detection
Emotion detection
Beat detection
Silence detection
Attention tracking
Highlight detection
↓
LLM creative reasoning (Stage 2 — grounded in CapCut KB)
↓
Timestamped editing instructions for human editor
```

### Two-Stage Prompting (Core Design)

**Stage 1 — Pure Free Analysis** (no CapCut mentioned)
Let Gemini's brain run wild. Analyze pacing, emotion, energy, color, movement, audio, story. No constraints. No asset names.

**Stage 2 — Grounded Suggestions** (CapCut KB injected)
Feed Stage 1 analysis + full CapCut catalog into Gemini. Every suggestion must reference exact asset names from the KB. Zero hallucinated tools.

This separation prevents the catalog from constraining creative thinking while ensuring every output is actionable with real CapCut assets.

---

## 2. CAPCUT TIMECODE FORMAT (Critical)

CapCut Desktop Pro uses **frame-based timecode**, not decimal seconds. All instructions MUST use this native format.

### Format: `HH:MM:SS:FF`

```
HH = Hours
MM = Minutes
SS = Seconds
FF = Frames (00–29 at 30fps)
```

### How It Works

| Timecode | Meaning |
|----------|---------|
| `00:00:00:00` | Start of video |
| `00:00:00:15` | Half-second mark (frame 15 of 30) |
| `00:00:00:29` | Last frame of first second |
| `00:00:01:00` | Exactly 1 second (NOT 00:00:00:30 — that doesn't exist) |
| `00:00:02:15` | 2 seconds and 15 frames (2.5 seconds) |
| `00:00:10:00` | 10 seconds |
| `00:01:00:00` | 1 minute |

### Rules

```
RULE: ALWAYS output timecodes in HH:MM:SS:FF format
RULE: Frame count resets to 00 after reaching 29 (at 30fps)
RULE: There is NO frame 30 — after :29 the second increments
RULE: When specifying durations, use the same format (e.g. "duration: 00:00:00:10" = 10 frames)
RULE: When specifying ranges, use dash: "00:00:01:00–00:00:03:15"
RULE: Check the project frame rate — 30fps is CapCut default, but 24fps and 60fps are also possible
```

### Frame Rate Reference

| FPS | Last Frame Before Next Second | Common Use |
|-----|-------------------------------|-----------|
| 24fps | :23 | Cinematic / film |
| 30fps | :29 | CapCut default, social media |
| 60fps | :59 | Slow-motion, gaming |

### Quick Conversion

| Seconds | 30fps Timecode |
|---------|---------------|
| 0.5s | 00:00:00:15 |
| 1.0s | 00:00:01:00 |
| 1.5s | 00:00:01:15 |
| 2.0s | 00:00:02:00 |
| 3.0s | 00:00:03:00 |
| 5.0s | 00:00:05:00 |
| 10.0s | 00:00:10:00 |
| 30.0s | 00:00:30:00 |
| 1 min | 00:01:00:00 |

> **Why this matters:** Most AI editing guides use simplified timestamps (0:05, 00:07) which don't match what the editor sees on the CapCut timeline. Using native timecodes means the editor can scrub directly to the exact frame without mental conversion.

---

## 3. OUTPUT FORMAT STANDARD

Every instruction must be **surgical**. No vague advice.

### Required Format

```
VIDEO EDIT PLAN
Platform: [TikTok / YouTube / Instagram / General]
Intensity: [1-5]
Mode: [Editing Instructions / Viral Optimization / Cinematic / Minimal Clean]
Frame Rate: 30fps

═══════════════════════════════════════════

HOOK SECTION (00:00:00:00–00:00:04:00)

00:00:00:00–00:00:02:00
Action: Cut initial silence
Why: Dead air kills retention in first 2 seconds

00:00:02:00
Action: Add caption — "This changed everything"
Style: Bold Impact, highlight word "changed"
Why: Hook statement anchors viewer attention

00:00:03:00
Action: Zoom to 108% over 00:00:00:09 (9 frames), ease-out
Why: Speaker emphasizes key point — visual punch reinforces audio emphasis

═══════════════════════════════════════════

BODY (00:00:04:00–00:00:12:00)

00:00:05:00
Action: Apply Flash transition (duration: 00:00:00:06)
Alternative A: Blur transition (smooth, 00:00:00:09)
Alternative B: Hard cut (clean)
Why: Beat drop in background audio — Flash aligns with energy spike

00:00:07:00
Action: Add whoosh sound effect
Why: Bridges scene change, maintains momentum

00:00:08:00–00:00:09:06
⚠️ WEAK SPOT: 1.2s pause detected (36 frames)
Action: Jump cut — remove dead air
Why: Pacing drops below 3-second change threshold

═══════════════════════════════════════════

ENDING (00:00:12:00–00:00:15:00)

00:00:12:00
Action: Slow zoom out to 95% over 00:00:02:00
Why: Creates breathing room, signals resolution

00:00:14:00
Action: Fade transition (00:00:00:15)
Why: Clean outro — avoids abrupt ending

═══════════════════════════════════════════

⭐ HIGHLIGHT MOMENT: 00:00:06:00

Speaker says: "This changed my business completely"
Suggested emphasis:
• Caption with highlighted words: "changed" + "business"
• Punch zoom to 110% over 00:00:00:06 (6 frames)
• Subtle bass hit sound effect
Why: Strongest emotional/value statement in the video

═══════════════════════════════════════════

EDITING REVIEW

Pacing: Good (average change interval: ~72 frames / 2.4s)
Visual variation: Moderate
Hook strength: Strong
Viewer retention potential: High
Suggested improvements: None critical
```

### Output Rules
- Every action gets a CapCut-native timecode in HH:MM:SS:FF format (exact frame or range)
- Every action gets a "Why" explanation
- Subjective choices get 2-3 alternatives (editor stays in control)
- Weak spots / dead air / pacing drops are flagged explicitly
- Instructions grouped by section (Hook / Body / Ending)
- Highlight moments called out with star marker
- Final quality review at the end

### CapCut Navigation Paths

Every suggestion should include the exact path so the editor can find the asset fast:

```
00:00:07:00 – Apply Shaky Inhale transition
Find it: Left panel → Transitions → Trending → "Shaky Inhale"
Duration: 00:00:00:18 (18 frames)
```

---

## 4. TOOL VOCABULARY

LLMs hallucinate tools. Restrict suggestions to these known editing actions only.

### Cuts
| Action | When to Use |
|--------|------------|
| Jump cut | Remove pauses, dead air, filler words |
| Hard cut | Clean scene changes, direct transitions |
| Match cut | Visual similarity between shots |
| Beat cut | Sync with music rhythm |
| L-cut / J-cut | Audio leads or trails the visual |

### Transitions (Map to CapCut KB)
| Category | Use Case |
|----------|----------|
| Flash | Beat drops, dramatic moments, high energy |
| Blur | Smooth scene changes, dreamy feel |
| Swipe | Directional movement, social media style |
| Glitch | Tech/edgy content, surprise moments |
| Cross dissolve | Emotional transitions, time passage |
| Fade | Intros, outros, breathing room |

> Full transition names: see KF-03 (~2,225 transitions, 13 categories)

### Motion
| Action | Parameters | When to Use |
|--------|-----------|------------|
| Zoom in | Target %, duration, easing | Emphasis, key statements |
| Zoom out | Target %, duration, easing | Resolution, breathing room |
| Shake | Intensity 1-10, duration | Impact, energy spikes |
| Pan | Direction, speed | Reveal, scene exploration |
| Tracking | Subject, speed | Follow action |

### Text
| Type | When to Use |
|------|------------|
| Captions | Speech-to-text, key quotes |
| Highlight words | Emphasis within captions |
| Lower third | Speaker ID, location, context |
| Callout | Draw attention to specific element |
| Title card | Section headers, topic changes |

> Full text templates: see KF-05 (200+ templates)

### Effects
| Type | Source |
|------|--------|
| Video effects | KF-02 Part A (~3,467 effects, 22 categories) |
| Body effects | KF-02 Part B (21 categories) |
| Filters | KF-04 (~600+ filters, 14 categories) |
| Stickers | KF-06 (50+ categories) |

### Audio
| Action | When to Use |
|--------|------------|
| Whoosh | Scene transitions, movement emphasis |
| Impact / bass hit | Beat drops, emphasis moments |
| Beat sync | Align cuts with music rhythm |
| Riser | Build tension before key moment |
| Silence removal | Cut dead air > 0.5s |

### Speed
| Action | CapCut Feature |
|--------|---------------|
| Slow motion | Speed tab → Standard (< 1.0x) or Curve presets |
| Speed ramp | Speed tab → Curve → Custom / Montage / Hero / Bullet |
| Freeze frame | Timeline toolbar → Freeze |
| Velocity effects | Flash / Blur shake / Fade blur / Retro zoom / Rainbow |

---

## 5. VIDEO ANALYSIS FRAMEWORK (Stage 1)

Gemini analyzes the raw video before any editing suggestions.

### Required Analysis Points

```
VISUAL ANALYSIS
- Scene/shot changes (with timecodes)
- Camera movement and framing
- Subject focus and eye line
- Color palette and lighting quality
- Visual motifs and patterns
- Movement intensity per segment

AUDIO ANALYSIS
- Speech segments (with timecodes)
- Silence/pause gaps (> 0.5s)
- Background music: BPM, energy, beat drops
- Sound design opportunities
- Audio quality issues

EMOTIONAL ANALYSIS
- Emotional tone per segment
- Facial expressions and body language
- Key emotional moments (timecodes)
- Energy curve (rising/falling/flat)
- Laughter, surprise, reaction moments

CONTENT ANALYSIS
- Key statements / quotable moments
- Story structure (setup → conflict → resolution)
- Hook potential (what grabs attention)
- Highlight moments (the "gold")
- Weak spots (where attention drops)

PACING ANALYSIS
- Current change interval (seconds between visual changes)
- Attention risk zones (> 3s without change)
- Natural cut points
- Rhythm and flow assessment
```

### Shot Detection Format

```
SHOT 1 (00:00:00:00–00:00:05:00)
Type: Talking head
Subject: Speaker explaining concept
Emotion: Neutral → building interest
Audio: Speech, no music
Pacing: Slow (needs intervention)

SHOT 2 (00:00:05:00–00:00:08:00)
Type: Reaction / emphasis
Subject: Speaker leaning forward
Emotion: Passionate
Audio: Speech with emphasis
Pacing: Good

SHOT 3 (00:00:08:00–00:00:12:00)
Type: Demonstration
Subject: Screen share / product
Emotion: Informational
Audio: Voiceover
Pacing: Moderate
```

---

## 6. CREATIVE RULES & CONSTRAINTS

### Attention / Pacing System

```
RULE: If visual change gap > 3 seconds → suggest pattern interrupt

Pattern interrupts (in order of subtlety):
1. Zoom (105-110%)
2. Cut (jump cut or match cut)
3. Caption overlay
4. Motion (pan or shake)
5. Effect overlay
```

### Beat / Audio Sync

```
RULE: If music exists → detect beats → align cuts with beats
RULE: Trigger visual effects on strong beats (beat drops, accents)
RULE: Transitions should land ON the beat, not between beats
```

### Silence / Pause Detection

```
RULE: If pause > 0.5 seconds in talking-head video → suggest jump cut
RULE: If pause > 1.0 seconds → flag as weak spot
RULE: Brief pauses (0.3-0.5s) can stay if they serve dramatic purpose
```

### Zoom / Focus Intelligence

```
RULE: When speaker emphasizes a point → zoom to 105-110%
RULE: Zoom duration: 00:00:00:06 to 00:00:00:15 (6-15 frames) with ease-out
RULE: Max 1 zoom per 5 seconds (prevent zoom fatigue)
```

### Caption Intelligence

```
RULE: Identify important words in speech
RULE: Highlight 1-3 words per caption line (not every word)
RULE: Highlight hierarchy: action verbs > numbers > emotional words
```

Example:
```
Caption: "This changed my business completely"
Highlight: "changed" (action) + "business" (subject)
Skip: "This" "my" "completely" (filler/modifier)
```

### Style Consistency Rules

```
RULE: Do not mix more than 2 visual styles in one video
RULE: Prefer cuts over transitions (cuts are invisible, transitions draw attention)
RULE: Keep filter/color grade consistent across the entire video
RULE: If using a transition style, use the same family throughout
RULE: Avoid excessive effects — every effect must earn its place
```

### Maximum Effect Limits

```
Max transitions per 10 seconds: 2
Max video effects per 5 seconds: 2
Max zooms per 5 seconds: 1
Max caption changes per 3 seconds: 1
Max stickers on screen simultaneously: 2
```

### Editing Philosophy

```
RULE: Prefer clean editing over excessive effects
RULE: Less is more — every edit must have a reason
RULE: Cuts > transitions (invisible editing is professional editing)
RULE: Subtle zooms > heavy effects
RULE: The video's natural energy dictates the edit, not a template
```

### Creative Freedom Rule

```
RULE: Do not rely on rigid templates
RULE: Analyze each video independently
RULE: Suggest edits based on context, pacing, and emotion
RULE: Never default to genre rules ("if funny do X, if romantic do Y")
RULE: If the video has unique energy, lean into it instead of safe defaults
```

---

## 7. MODES & LEVELS

### Creative Direction Modes

| Mode | Description | Use When |
|------|------------|----------|
| Cinematic | Film-style, slow pacing, dramatic lighting emphasis | Brand content, high-production footage |
| Viral | Fast cuts, captions, motion, pattern interrupts every 2-3s | TikTok, Reels, Shorts |
| Documentary | Slower pacing, lower thirds, clean transitions | Interview, explainer, educational |
| Meme | Jump cuts, zooms, sound effects, chaotic energy | Comedy, reaction, meme culture |
| Aesthetic | Color-focused, smooth transitions, dreamy filters | Lifestyle, travel, fashion |
| Minimal | Clean cuts only, minimal effects, professional | Corporate, presentation, portfolio |

If user gives no direction → AI analyzes the video and decides the best mode.

### Effect Intensity Levels

| Level | Name | Description |
|-------|------|------------|
| 1 | Minimal | Clean cuts, no effects, professional grade |
| 2 | Cinematic | Subtle color grading, gentle zooms, smooth transitions |
| 3 | Social Media | Captions, moderate effects, zooms, sound design |
| 4 | Viral | Fast-paced, heavy captions, motion, pattern interrupts |
| 5 | Chaos | Maximum effects, meme energy, rapid cuts, heavy sound design |

### Difficulty Levels

| Level | Output Style |
|-------|-------------|
| Beginner | 3-5 simple, high-impact edits with step-by-step CapCut paths |
| Intermediate | Full timeline with 10-15 suggestions, alternatives offered |
| Advanced | Detailed director's cut with reasoning, alternatives, quality review |

### Platform Optimization

| Platform | Pacing | Priorities |
|----------|--------|-----------|
| TikTok / Reels / Shorts | Fast (change every 1-3s) | Hook in 1s, captions, motion, sound design |
| YouTube (short-form) | Fast (change every 2-3s) | Hook in 3s, retention optimization, captions |
| YouTube (long-form) | Moderate (change every 3-5s) | Pacing variety, B-roll suggestions, lower thirds |
| LinkedIn | Clean (change every 4-6s) | Professional, minimal effects, clear captions |
| Instagram Feed | Polished | Color grading, aesthetic filters, clean transitions |

### Multi-Output Modes

| Mode | What It Produces |
|------|-----------------|
| Editing Instructions | Timestamped action plan (default) |
| Viral Optimization | Retention-focused cuts + hooks + captions |
| Cinematic Edit | Film-grade suggestions with color + pacing |
| Minimal Clean Edit | Cuts-only, no effects, professional polish |
| Director's Review | Analysis + suggestions + quality assessment + alternatives |

---

# PART B — CAPCUT PLATFORM REFERENCE

## 8. GLOBAL LAYOUT

```
┌──────────────────────────────────────────────────────────────────────┐
│ TOP BAR: [CapCut] File Edit Media Clip Transitions Options Filter   │
│          Adjustment Sticker Transform/Timeline Autocut    [Export]  │
├──────────┬────────────────────────────┬──────────────────────────────┤
│ LEFT     │   CENTER                   │  RIGHT                       │
│ PANEL    │   PREVIEW CANVAS           │  PROPERTIES PANEL            │
│          │                            │                              │
│ Tab nav  │   Live preview of          │  Context-sensitive           │
│ + Content│   current frame            │  inspector (changes          │
│ grid/list│   (9:16 / 16:9 etc)       │  based on what's selected)   │
│          │                            │                              │
├──────────┴────────────────────────────┴──────────────────────────────┤
│ TIMELINE TOOLBAR (split, delete, undo/redo, copy/paste, freeze)     │
├──────────────────────────────────────────────────────────────────────┤
│ TIMELINE — multi-track layers (video, audio, text, effects,         │
│ stickers) with playhead, zoom slider, snap, track controls          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 9. LEFT PANEL — MAIN NAVIGATION TABS

| Tab | Icon | What It Contains | KF Reference |
|-----|------|-----------------|--------------|
| **Media** | Film clip | Imported footage, images, project media, face detection | KF-01 |
| **Audio** | Music note | Music, sound effects, extracted audio, voiceover | KF-07 |
| **Text** | T | Text templates, captions, titles, auto captions | KF-05 |
| **Stickers** | Smiley | Animated stickers library (50+ categories) | KF-06 |
| **Effects** | Sparkle | Video effects (22 categories) + Body effects (21 categories) | KF-02 |
| **Transitions** | Split arrow | Clip-to-clip transitions (13 categories) | KF-03 |
| **Filters** | Circle/lens | Color grading presets (14 categories) | KF-04 |
| **Adjustment** | Sliders | Color correction tools (also in right panel) | KF-08 |
| **Templates** | Grid | Pre-made project templates | — |

---

## 10. RIGHT PANEL — PROPERTIES INSPECTOR

When a video clip is selected on the timeline, the right panel shows these tabs:

```
Video | Audio | Speed | Animation | Adjust | AI stylize
```

Full detail in **KF-08**.

### 10.1 VIDEO Tab

Sub-tabs: **Basic** | **Remove BG** | **Mask** | **Retouch**

#### Video > Basic
- **Transform:** Scale (uniform toggle), Position X/Y, Rotate, Flip H/V, Rotate 90° CW/CCW, Fit, Fill, Alignment
- **Blend:** Color swatch + mode dropdown
- **15 AI Features:**

| Feature | Badge |
|---------|-------|
| Stabilize | PRO |
| Enhance quality | PRO |
| Reduce image noise | PRO |
| Optical flow | PRO |
| AI remove | PRO |
| AI expand | Free |
| AI remix | Try Free |
| Eye contact | Free |
| Lip sync | PRO |
| Relight | PRO |
| Auto reframe | PRO |
| Remove flickers | PRO |
| AI movement | PRO |
| Camera tracking | PRO |
| Motion blur | PRO |

- **Canvas:** Checkbox + "Apply to all"

#### Video > Remove BG
| Feature | Badge |
|---------|-------|
| Auto removal | PRO |
| Custom removal | — |
| Chroma key | — |

#### Video > Mask
- "+ Add mask" button
- Shapes: Rectangle, Circle, Heart, Star, custom draw
- Feather, invert, expand controls

#### Video > Retouch

Sub-tabs: **Face** | **Body** | **Hair** | **Face presets** | **Body presets**

**Face > Retouch** (14 sliders):
Fixing [PRO], Even [PRO], Clear blemishes [PRO], Sparkly Skin [PRO], Desickle [Free], Smooth, Erase lines [Free], Bright Eye [Free], Facelift [PRO], Dark circles [Free], Whitening, White teeth, Clear, Skin tone (12 swatches)

**Face > Reshape** (10 sliders):
Width [PRO], V shape [PRO], Jaw [PRO], Cheekbones [PRO], Chin Length, Shorten, Lower [PRO], Middle [PRO], Upper [PRO], Hairline [PRO]

**Face > Makeup** (11 sub-tabs):
Looks | Eyelashes | Eye shadow | Eyeliner | Eyebrow | Lipstick | Blush | Traveling | Highlights | Eye Color | Freckles

- Looks presets include: Sugar Plum, Bluesky, Sunburned Mix, Honey Gold, After School, Hot Peaches, Boyhood, Old Money, Cherry Cola, Peppermint, + more
- Auto styles [PRO], Auto reshape, Manual controls

### 10.2 AUDIO Tab

Sub-tabs: **Basic** | **Voice changer**

| Feature | Badge |
|---------|-------|
| Volume | — (default 0.0dB) |
| Fade in / Fade out | — (default 0.0s) |
| Normalize loudness | PRO |
| Enhance voice | PRO |
| Video translator | PRO |
| Reduce noise | PRO |
| Separate audio | Free |
| Fill channel | — |

### 10.3 SPEED Tab

Sub-tabs: **Standard** | **Curve** [PRO] | **Velocity effects**

**Standard:** Speed slider (1.00x), Duration, Change audio pitch toggle, Smooth slow-mo [PRO]

**Curve** — 8 presets:
None, Custom, Montage, Hero, Bullet, Jump out, Flash in, Flash out

**Velocity Effects** — 6 presets:
None, Flash, Blur shake, Fade blur, Retro zoom, Rainbow

### 10.4 ANIMATION Tab — ~480+ presets (Trending only)

Sub-tabs: **In** | **Out** | **Combo**

| Sub-tab | Category Filters | Trending Count |
|---------|-----------------|----------------|
| **In** | Trending, Basic, Light, Glitch, Mask, 3D, Vibration | ~200+ |
| **Out** | Trending, Basic, Light, Glitch, Mask, 3D, Vibration | ~180+ |
| **Combo** | Trending, Basic, 3D, Cam Motion | ~100+ |

> All animations documented in **KF-08** (~1,985 total: ~480 Trending + ~1,505 across Basic, Light, Glitch, Mask, 3D, Vibration, Cam Motion).

**Sample In animations:** Flash In, Swoosh, Cross Open, Fade In, Zoom 1, Focus, Pulse, Energy Boom, Inky Smoke, Particle Blast, Anime Frame, Cyber Fusion, Earth Zoom, Digital Morph, Lava Spread...

**Sample Out animations:** Smoke, Black Hole, Flash Out, Fade Out, Blur Dissolve, Glitch Outro, Neat Shatter, Dust Scatters, Cyber Escape, Shattered, Flipbook, Fairy Fly...

**Sample Combo animations:** Bouncy Rush, Zoom 1/2, Pendulum 1/2, Bounce 1/2, Wave Motion, Spin Fall, Roll InOut, Rollercoaster, Pirate Ship 1-4, 3D Card 1-6...

### 10.5 ADJUST Tab

Sub-tabs: **Basic** | **HSL** | **Curves** | **Color wheel**

**Basic — AI Color Tools:**
| Feature | Badge |
|---------|-------|
| Auto adjust | PRO |
| Color match | PRO |
| Color correction | PRO |

**Basic — LUT:** Dropdown (None), Intensity slider (100), Protect skin tone toggle

**Basic — Color sliders:** Temp, Tint, Saturation (all default 0)

**Basic — Lightness sliders:** Exposure, Contrast, Highlight, Shadow, Whites, Blacks, Brilliance (all default 0)

**Basic — Effects sliders:** Sharpen, Clarity, Particles, Fade (default 0), Vignette (default 10)

**HSL:** 8 color channels (Red, Orange, Yellow, Green, Cyan, Blue, Purple, Magenta) × 3 controls (Hue, Saturation, Brightness)

**Curves:** 4 channels — Luma (white), Red, Green, Blue

**Color Wheel** [PRO]: Primary mode, 4 wheels — Shadows, Middle grey, Tint, Offset (each X/Y: 0.00)

### 10.6 AI STYLIZE Tab

> Fully documented in **KF-10**. Includes AI Effects section, 11 style categories (~57 presets), prompt-based generation with credits system, and showcase gallery.

---

## 11. EFFECTS LIBRARY (Left Panel → Effects Tab)

### Two Main Sections
- **Video Effects** → see **KF-02** Part A (full catalog)
- **Body Effects** → see **KF-02** Part B (full catalog)

### Video Effects — 22 Categories, ~3,467 effects

```
Trending    Classic     NEW         Hits        Intro & Outro
Wild Pics   Party       Motion      Light       Retro
Glitch      Distortion  Motion (AI/3D)  Decor   Edits
Screen      Sparkle     Texture     Comics      Split
Graffiti    Celebrate
```

> Every individual effect name cataloged in **KF-02** Part A.

### Body Effects — 21 Sidebar Categories

```
Trending    Basic       Bling       Fire        Mid & Retro
Party       Lights      Dreamy      Glowing Line Blur
Superheroes Superpowers Bling*      Blur*       Portrait
Funky       Gentle Smile Funky Mode Background  Puppets
Travel
```

> *Bling and Blur appear twice in sidebar (duplicate sections).
> KF-02 Part B also documents additional content sections: Painting, Head, Particles, Face.
> Full catalog in **KF-02** Part B.

---

## 12. TRANSITIONS LIBRARY (Left Panel → Transitions Tab)

### 13 Categories, ~2,225 transitions

```
Trending    Classic     NEW         Hits        Overlay
Light       Camera      Blur        Basic       Mask
Slide       Glitch      Distortion
```

> Every individual transition name cataloged in **KF-03**.

### Application
- Drag transition between two clips on timeline
- Duration adjustable by edge-dragging
- Some have direction/style sub-options
- Thumbnails show animated previews on hover

---

## 13. FILTERS LIBRARY (Left Panel → Filters Tab)

### 14 Categories, ~600+ unique filters

```
Featured    NEW         Hits        Life        Photo Booth
Pet         Landscape   Movies      Mono        Portrait
Retro       Night       Alternative Food
```

> Every individual filter name cataloged in **KF-04**.

**Key categories:**
| Category | Count | Highlights |
|----------|-------|-----------|
| Life | ~192 | Largest specific category — everyday/lifestyle |
| Landscape | ~108 | Nature, travel, outdoor |
| Retro | ~106 | Film stocks (Agfa 400, Kodak 500T, Provia 100), VHS, eras |
| Movies | ~99 | Named after films (Wong Kar-wai, Oppenheimer, Barbie, Dune, etc.) |
| Portrait | ~91 | Skin enhancement, beauty |
| Alternative | 74 | Neon, fantasy, experimental |
| Mono | 49 | B&W and desaturated |
| Photo Booth | 36 | Vintage portrait styles |
| Pet | 27 | Pet photography optimized |
| Food | 21 | Culinary content |
| Night | 14 | Low-light, neon, cyberpunk |

### Application
- Drag filter onto timeline clip or click to preview
- Intensity slider in right properties panel
- Multiple filters can be stacked on a single clip

---

## 14. TEXT TOOLS (Left Panel → Text Tab)

### Sub-tabs
```
Default text | Text templates | Auto captions | Local captions
```

### Text Templates — 200+ templates
Categories: All, Animations, Tracking, Text to speech, AI avatars, Presets, History
Styles: Bubble/Badge (30+), Banner/Ribbon (20+), Box/Frame (25+), Neon/Glow (15+), Lower Third (15+), Bold/Block (20+), Social/Subscribe (10+), 3D/Perspective (10+), more

### Right Panel Tabs (when text selected)
```
Text | Animation | Tracking | Text to speech | AI subtitles
```

### Auto Captions
- Source language dropdown (multi-language)
- Bilingual subtitles toggle
- "Identify file words" (custom vocabulary)
- "Create smart captions" button

> Full detail in **KF-05**.

---

## 15. STICKERS LIBRARY (Left Panel → Stickers Tab)

### 50+ Categories

```
Featured     Trending     New          Basic        GIPHY
White Notation Love        Emoji        Reaction     Arrow
Comic Style  Speech Bubble Countdown   Overlay      Shape
Sound        Cute         Bling        Food         Stationery
Brush        Sparkling    Hip Hop      Social       Decoration
Entry        Music        Green Screen Sport        Black Gradient
3D           Festivals    Cartoon      Christmas    Gradient
Confetti     Animals      Anime        Eco Friendly Night
Basketball   Birthday     Mothers      Weather      Butterfly
New Year     ...more
```

> Full catalog in **KF-06**.

---

## 16. AUDIO TOOLS (Left Panel → Audio Tab)

### Categories
```
Music | Sound effects | Extracted audio | Voiceover
```

- Built-in music library (searchable, genre-tagged, Suno AI tracks available)
- Sound effects library
- Audio separation (vocals from instrumentals)
- Beat detection / beat sync
- Volume keyframing on timeline
- Waveform visualization on timeline tracks

> Full detail in **KF-07**.

---

## 17. TIMELINE CONTROLS

### Toolbar
Split (Cmd+B), Delete, Undo/Redo (Cmd+Z / Cmd+Shift+Z), Copy/Paste, Freeze frame, Snap toggle, Zoom slider, Playback controls

### Track Types
Video (multi-layer), Audio (multi-layer), Text, Effects, Stickers

### Features
Multi-clip selection, drag to rearrange, edge-drag to trim, keyframe diamonds on clips, track lock/mute/visibility toggles

---

## 18. KEYBOARD SHORTCUTS

| Action | Shortcut |
|--------|----------|
| Split clip | Cmd + B |
| Delete | Delete/Backspace |
| Undo | Cmd + Z |
| Redo | Cmd + Shift + Z |
| Copy | Cmd + C |
| Paste | Cmd + V |
| Play/Pause | Space |
| Zoom timeline | Cmd + scroll |
| Select all | Cmd + A |

---

## 19. PRO vs FREE FEATURES

### PRO (requires subscription)
- AI: Stabilize, Enhance quality, Reduce image noise, Optical flow, AI remove, Lip sync, Relight, Auto reframe, Remove flickers, AI movement, Camera tracking, Motion blur
- Remove BG: Auto removal
- Retouch: Fixing, Even, Clear blemishes, Sparkly Skin, Facelift, most Reshape sliders
- Audio: Normalize loudness, Enhance voice, Video translator, Reduce noise
- Speed: Curve presets, Smooth slow-mo
- Adjust: Auto adjust, Color match, Color correction, Color wheel
- Many effects, transitions, and filters marked with PRO diamond badge
- Retro filters (43 PRO), Alternative filters (24 PRO)

### Free (included)
- AI expand, AI remix (Try free), Eye contact, Separate audio
- Retouch: Desickle, Erase lines, Bright Eye, Dark circles
- All Animation presets, Adjust Basic/HSL/Curves sliders
- Transform, Blend, Canvas, Volume/Fade, Speed standard
- Many effects, transitions, and filters without PRO badge

---

## 20. WORKFLOW QUICK REFERENCE

### Color Grade
```
Select clip → Right Panel → Adjust → Basic sliders (Temp, Exposure, Contrast, etc.)
→ or use Curves/HSL/Color Wheel for precision
→ "Apply to all" for batch | "Save as preset" to reuse
```

### Add Effect
```
Left Panel → Effects → Video effects or Body effects → Browse 22/21 categories
→ Click thumbnail to preview → Drag to timeline → Adjust duration
```

### Add Transition
```
Left Panel → Transitions → Browse 13 categories → Drag between two clips
→ Edge-drag to adjust duration
```

### Apply Filter
```
Left Panel → Filters → Browse 14 categories → Click to preview
→ Drag to clip → Adjust intensity in right panel
```

### Speed Ramp
```
Select clip → Speed → Curve → Choose preset (Montage/Hero/Bullet/etc.)
→ or Custom → Edit bezier handles → Enable Smooth slow-mo [PRO]
```

### Auto Captions
```
Left Panel → Text → Auto captions → Set language → "Create smart captions"
→ Review/edit on timeline
```

### Beauty/Retouch
```
Select clip → Video → Retouch → Face → Retouch/Reshape/Makeup sub-tabs
→ Adjust sliders → Auto styles [PRO] for one-click presets
```

### Animation
```
Select clip → Animation → In/Out/Combo → Browse 200+/180+/100+ presets
→ Click to apply → Filter by: Trending, Basic, Light, Glitch, Mask, 3D, Vibration
```

---

# PART C — REFERENCE

## 21. CAPCUT TERMINOLOGY → INDUSTRY EQUIVALENT

| CapCut Term | Industry Equivalent |
|-------------|-------------------|
| Velocity effects | Speed ramping / time remapping |
| Optical flow | Frame interpolation (AI slow-mo) |
| Body effects | Subject-aware effects (person detection) |
| Video effects | Full-frame effects (no detection) |
| Retouch tab | Beauty / face retouching panel |
| Eye contact | Gaze redirection AI |
| AI expand | Generative fill / outpainting |
| AI remove | Object removal / inpainting |
| AI remix | Style transfer / AI re-interpretation |
| Relight | AI relighting / light direction change |
| Camera tracking | Subject tracking for effects |
| Separate audio | Stem separation (vocals/instruments) |
| Smart captions | Auto-generated AI subtitles |
| Normalize loudness | LUFS normalization |
| LUT | Look-Up Table (color grade preset) |
| HSL | Hue/Saturation/Luminance (per-color grading) |

---

## 22. EFFECT METADATA TEMPLATE

The CapCut catalog has ~7,000+ assets. AI needs meaning, not just names.

### Metadata Format

```
Effect: Flash
Category: Transitions → Trending
Type: Impact transition
Best use: Beat drop, dramatic moment, high-energy scene change
Duration: 00:00:00:06 to 00:00:00:12 (6–12 frames at 30fps)
Intensity: High
Mood: Energetic, aggressive, punchy
Pair with: Bass hit sound, zoom punch, bright footage
Avoid with: Slow/emotional content, documentary style
```

> Priority: Add metadata to the top 50-100 most-used transitions, effects, and filters first. The long tail can be metadata-tagged iteratively.

---

## 23. KB GAPS — STATUS

| Gap | Status | Resolved By |
|-----|--------|-------------|
| Animation library (non-Trending) | CLOSED | KF-08: ~1,505 non-Trending animations merged with Trending (~1,985 total) |
| AI Stylize tab | CLOSED | KF-10: 11 style categories, ~57 presets, prompt system documented |
| Music/SFX mood-BPM mapping | CLOSED | KF-07 Part B: 8 sections — mood tiers, SFX vocabulary, beat sync guide, editing mode cheat sheets |
| Effect metadata (top 150) | CLOSED | KF-09: 108 assets with full semantic metadata, use case index, mood index |

All identified gaps are now closed. The KB is complete.

---

## 24. KNOWLEDGE FILE INDEX

| File | Scope | Size | Items |
|------|-------|------|-------|
| **This file** | Master brain — directing system + platform reference | — | Overview |
| **KF-01** | Core UI Navigation — menus, layout, panels, timeline | 25KB | UI map |
| **KF-02** | All Effects — Video Effects + Body Effects | ~86KB | ~3,467 video effects (22 categories) + body effects (21 categories) |
| **KF-03** | Transitions — every transition by name | 41KB | ~2,225 transitions, 13 categories |
| **KF-04** | Filters — every filter by name | 20KB | ~600+ filters, 14 categories |
| **KF-05** | Text & Captions — templates, auto captions, fonts | 33KB | 200+ templates |
| **KF-06** | Stickers — categories and named stickers | 29KB | 50+ categories |
| **KF-07** | Audio & Music Intelligence — AI tools, audio features, mood-BPM mapping, SFX vocabulary | ~50KB | All AI features + 28 genres, 35+ SFX, beat sync guide |
| **KF-08** | Animations Complete — video properties, all animation categories | ~34KB | ~1,985 animations (Trending + Basic, Light, Glitch, Mask, 3D, Vibration, Cam Motion) |
| **KF-09** | Effect Metadata — semantic tags for top 108 assets | 55KB | ~34 transitions, ~40 video effects, ~14 body effects, ~20 filters + use case & mood indexes |
| **KF-10** | AI Stylize Tab — style categories, presets, prompt system | 6KB | 11 categories, ~57 presets |

> **Total cataloged items:** ~9,000+ individual effects, transitions, filters, animations, stickers, and AI stylize presets

---

## 25. GEMINI PROMPT TEMPLATES

### Stage 1 — Pure Creative Analysis (No CapCut)

```
Watch this entire video carefully. You are an elite video director with 20 years of experience.

Analyze the video freely and creatively. Do NOT reference any specific editing software. Tell me:

1. PACING & ENERGY
   - Overall energy curve (rising / falling / flat / dynamic)
   - Average time between visual changes
   - Sections that feel too slow or too fast

2. KEY MOMENTS (with exact timecodes)
   - Emotional peaks
   - Best quotable statements
   - Visual highlights
   - Audio highlights (beat drops, emphasis, laughter)

3. WEAK SPOTS (with exact timecodes)
   - Dead air / silence gaps
   - Low-energy sections
   - Unflattering angles or lighting
   - Repetitive sections

4. CREATIVE DIRECTION
   - What does this video "want to feel like"?
   - What editing style would serve it best?
   - Color story and mood assessment
   - Sound design opportunities

5. SHOT BREAKDOWN
   - Segment the video into logical shots
   - Classify each: talking head / action / B-roll / reaction / demo
   - Note transitions between shots

TIMECODE FORMAT: Use CapCut native timecodes (HH:MM:SS:FF) for ALL timestamps. At 30fps, frames go 00–29 then the second increments. There is no frame 30.

Be specific. Use exact timecodes. Be honest about what works and what doesn't.
```

### Stage 2 — Grounded CapCut Suggestions

```
You are an elite video director who has mastered CapCut Desktop Pro (2026 version). You have access to the complete CapCut catalog below.

Based on the video analysis provided, give me precise, actionable editing instructions using ONLY exact asset names from the CapCut catalog.

TIMECODE FORMAT: Use CapCut native timecodes (HH:MM:SS:FF) for ALL timestamps. At 30fps, frames go 00–29 then the second increments. There is no frame 30. Durations also use this format (e.g. 00:00:00:09 = 9 frames).

OUTPUT FORMAT:
- Every instruction has a timecode in HH:MM:SS:FF format
- Every instruction has the exact CapCut asset name and category
- Every instruction has a "Why" explanation
- Subjective choices include 2-3 alternatives
- Group instructions by section (Hook / Body / Ending)
- Flag weak spots with ⚠️
- Mark highlight moments with ⭐
- End with an Editing Review (pacing / variation / retention potential)

CONSTRAINTS:
- Use ONLY names from the provided catalog. Never invent asset names.
- Max transitions per 10 seconds: 2
- Max effects per 5 seconds: 2
- Max zooms per 5 seconds: 1
- Prefer cuts over transitions
- Every effect must earn its place — explain why it belongs
- Do not mix more than 2 visual styles
- Keep filter/color grade consistent throughout

CREATIVE RULES:
- Never default to genre templates
- Analyze THIS video's unique energy and lean into it
- Be original and artistic
- If something is better left alone, say so

Here is the analysis from Stage 1:
[PASTE STAGE 1 OUTPUT]

Here is the complete CapCut catalog (use ONLY these exact names):
[PASTE RELEVANT KB SECTIONS FROM KF-01 THROUGH KF-10]

Now generate the complete editing plan.
```

### Conversational Follow-Up Examples

After initial analysis, keep the conversation alive:

```
"The suggestions feel too calm — make it more chaotic"
"Push the intensity to level 5"
"Make it feel like a Christopher Nolan trailer"
"Remove all effects, keep only cuts"
"Focus on the section from 00:00:08:00 to 00:00:15:00"
"Add more caption moments"
"Make it platform-ready for TikTok"
```

Gemini re-analyzes and pulls new assets from the KB each time.

---

## 26. PRODUCT POSITIONING

### What This Is
> An AI editing director that watches your footage and delivers professional, timestamped editing instructions — grounded in real CapCut Desktop Pro assets.

### What This Is NOT
> Not an editor. Not a plugin. Not automation. It's the brain that tells you exactly what to do, where, and why.

### Why This Wins
- Editing software = red ocean (CapCut, Premiere, FCP, DaVinci all competing)
- AI that tells you HOW to edit = wide open space
- Editors follow advice when they understand the reasoning
- Works with any skill level (beginner gets simple steps, advanced gets director's notes)
- Gemini's multimodal video understanding does the heavy lifting
- CapCut KB prevents hallucination — every suggestion is a real, findable asset
- Real editors stay in control — the AI directs, humans execute

### Competitive Edge
No one else has a complete, verified catalog of 7,000+ CapCut assets paired with AI video understanding. The KB is the moat. The instruction-only model means editors trust it (no black box), learn from it (every suggestion has a "why"), and stay in creative control.

---

*Created: 2026-03-10*
*Sources: Screen recordings (hires-v1: 30 frames + hires-v2: 71 frames = 101 frames) + Panel screenshots (Effects: 82, Transitions: 56, Filters: 34, Remaining: 21 = 193 screenshots) + Three rounds of expert feedback on AI Editing Director system design*
*Status: Ready for implementation — all KB gaps closed. Deploy Stage 1 + Stage 2 prompts with KF-01 through KF-10 as knowledge files.*

---

## FILE: examples/viral-tiktok-edit.md

# Example Output: Viral TikTok Edit

> Input: 15-second talking-head video, speaker explaining a business tip
> Mode: Viral | Intensity: 4 | Platform: TikTok | Frame Rate: 30fps

---

```
VIDEO EDIT PLAN
Platform: TikTok
Intensity: 4 (Viral)
Mode: Viral Optimization
Frame Rate: 30fps

========================================

HOOK SECTION (00:00:00:00-00:00:03:00)

00:00:00:00-00:00:00:20
Action: Cut initial dead air (20 frames of silence)
Why: TikTok retention drops 30% if first second has no movement or speech

00:00:00:20
Action: Add caption - "This one habit changed everything"
Style: Bold Impact template
Find it: Left panel -> Text -> Text templates -> Trending -> "Bold Impact"
Highlight words: "habit" + "changed"
Why: Hook statement anchors attention. Highlighted words create visual hierarchy.

00:00:01:00
Action: Zoom to 108% over 00:00:00:09 (9 frames), ease-out
Find it: Select clip -> Video tab -> Basic -> Scale (drag from 100 to 108)
Why: Speaker leans in at this moment - zoom amplifies the physical movement

00:00:02:00
Action: Apply subtle shake effect (intensity 3/10, 6 frames)
Find it: Left panel -> Effects -> Video effects -> Lens -> "Camera Shake V2"
Duration: 00:00:00:06
Why: Adds energy. Prevents static talking-head fatigue at the 2-second mark.

========================================

BODY (00:00:03:00-00:00:11:00)

00:00:03:00-00:00:03:15
Action: Hard cut (jump cut - remove "um" filler)
Why: Speaker says "um" for 15 frames. Dead weight.

00:00:04:00
Action: Add whoosh sound effect
Find it: Left panel -> Audio -> Sound effects -> Transition -> "Whoosh 03"
Duration: 00:00:00:12
Why: Bridges the jump cut. Viewer doesn't notice the edit.

00:00:05:15
Action: Caption update - "Wake up at 5 AM for 30 days"
Style: Same Bold Impact template
Highlight: "5 AM" + "30 days"
Why: The specific numbers are the value. Highlight them.

00:00:06:00
Action: Zoom out to 97% over 00:00:00:15, ease-in-out
Why: Creates breathing room after intense zoom. Reset before next point.

00:00:07:00-00:00:07:20
WARNING: WEAK SPOT - 0.67s pause detected (20 frames)
Action: Jump cut - remove dead air
Why: Pacing drops below 3-second change threshold

00:00:08:00
Action: Apply Flash transition
Find it: Left panel -> Transitions -> Basic -> "Flash"
Duration: 00:00:00:06 (6 frames)
Alternative A: Blur transition (Left panel -> Transitions -> Basic -> "Blur")
Alternative B: Hard cut (cleaner, less dramatic)
Why: Speaker shifts topic here. Flash punctuates the shift.

00:00:09:00
Action: Add bass hit sound effect
Find it: Left panel -> Audio -> Sound effects -> Impact -> "Bass Drop 01"
Why: Speaker says "and here's the thing" - bass hit amplifies the emphasis

00:00:10:00
Action: Zoom to 112% over 00:00:00:06 (6 frames), snap
Find it: Scale 100 -> 112, add keyframe at 00:00:10:00 and 00:00:10:06
Why: Speaker's strongest statement. Maximum visual punch.

========================================

ENDING (00:00:11:00-00:00:15:00)

00:00:11:00
Action: Caption - "Follow for more"
Style: Clean Sans template
Find it: Left panel -> Text -> Text templates -> Social -> "Clean Sans"
Why: CTA. Keep it simple, don't distract from the message.

00:00:12:00
Action: Slow zoom out to 95% over 00:00:02:00
Why: Resolution energy. Signals the video is wrapping.

00:00:14:00
Action: Add subtle riser sound effect
Find it: Left panel -> Audio -> Sound effects -> Transition -> "Riser 05"
Why: Creates tension for the final beat

00:00:14:15
Action: Freeze frame (00:00:00:15)
Find it: Timeline toolbar -> Freeze
Why: Holds the final expression. Gives viewer time to process.

========================================

HIGHLIGHT MOMENT: 00:00:10:00

Speaker says: "That one change made me $50,000 in 3 months"
Suggested emphasis:
  - Caption with highlighted words: "$50,000" + "3 months"
  - Punch zoom to 112% over 6 frames
  - Bass hit sound effect
  - Consider adding money emoji sticker (Left panel -> Stickers -> Emoji -> "Money")
Why: Strongest value statement in the video. Numbers + emotion = retention.

========================================

EDITING REVIEW

Pacing: Excellent (average change interval: ~2.1s / 63 frames)
Visual variation: High (6 zoom changes, 2 transitions, 1 freeze)
Hook strength: Strong (caption + zoom in first second)
Audio design: 4 sound effects placed on key moments
Caption count: 3 (hook, value, CTA)
Viewer retention prediction: 75-85% to end
Suggested improvements: None critical. Consider adding background lo-fi music at -18dB.
```

---

## FILE: examples/cinematic-brand-edit.md

# Example Output: Cinematic Brand Content

> Input: 30-second product reveal video, luxury perfume brand, AI-generated footage
> Mode: Cinematic | Intensity: 2 | Platform: Instagram Feed | Frame Rate: 30fps

---

```
VIDEO EDIT PLAN
Platform: Instagram Feed (1:1 or 4:5)
Intensity: 2 (Cinematic)
Mode: Cinematic Direction
Frame Rate: 30fps

========================================

OPENING (00:00:00:00-00:00:08:00)

00:00:00:00-00:00:03:00
Action: Slow fade in from black (45 frames)
Find it: Left panel -> Transitions -> Basic -> "Fade"
Duration: 00:00:01:15 (45 frames)
Why: Luxury content never starts abruptly. Fade builds anticipation.

00:00:00:00
Action: Apply color filter - "Gloomy Cinema"
Find it: Left panel -> Filters -> Film -> "Gloomy Cinema"
Intensity: 70%
Why: Establishes the warm, amber tone. Consistent across all shots.

00:00:01:00
Action: Add lower third - brand name
Style: Thin Outline template
Find it: Left panel -> Text -> Text templates -> Titles -> "Thin Outline"
Duration: 00:00:03:00 (hold for 3 seconds)
Animation: Fade up (Left panel -> Animations -> In -> "Fade In")
Why: Brand identification in first 2 seconds. Serif = luxury positioning.

00:00:03:00-00:00:05:00
Action: Cross dissolve to product close-up
Find it: Left panel -> Transitions -> Basic -> "Dissolve"
Duration: 00:00:00:24 (24 frames)
Alternative: "Light Leak" transition (Left panel -> Transitions -> Camera -> "Light Leak 02")
Why: Cross dissolve = timeless. Light leak = warmer, more modern.

00:00:05:00
Action: Slow zoom in to 105% over 00:00:03:00 (90 frames), ease-in-out
Why: Draws viewer into the product. Slow zoom = luxury pacing.

========================================

PRODUCT REVEAL (00:00:08:00-00:00:20:00)

00:00:08:00
Action: Apply body effect - "Soft Glow"
Find it: Left panel -> Effects -> Video effects -> Blur -> "Soft Glow"
Intensity: 30%
Why: Adds bloom to highlights. Makes glass/liquid surfaces shimmer.

00:00:08:00-00:00:12:00
Action: Speed ramp - slow motion 0.5x
Find it: Speed tab -> Standard -> drag to 0.5x
Why: Product rotation in slow motion. Every detail visible.

00:00:12:00
Action: Apply "Moon Flare" effect
Find it: Left panel -> Effects -> Video effects -> Lens -> "Moon Flare"
Intensity: 40%
Duration: 00:00:01:00
Why: Single flare as the product catches light. Cinematic, not overdone.

00:00:14:00
Action: Cross dissolve to lifestyle shot
Duration: 00:00:00:18 (18 frames)
Why: Same transition family maintained. Visual consistency.

00:00:15:00
Action: Zoom out to 98% over 00:00:02:00
Why: Reveals the full scene. Breathing room after close-up intensity.

00:00:17:00
Action: Add ambient pad sound (subtle)
Find it: Left panel -> Audio -> Music -> Cinematic -> search "Ambient Pad"
Volume: -20dB
Why: Underlays the visual without competing. Creates atmosphere.

========================================

CLOSING (00:00:20:00-00:00:30:00)

00:00:20:00
Action: Slow zoom in to 103% over 00:00:05:00
Why: Final product hero shot. Gentle zoom = confidence.

00:00:22:00
Action: Add tagline caption
Style: "Minimal Titles" template
Find it: Left panel -> Text -> Text templates -> Titles -> "Minimal Titles"
Animation In: "Typewriter" (Left panel -> Animations -> In -> "Typewriter")
Why: Tagline appears letter by letter. Premium feel.

00:00:26:00
Action: Begin fade to black
Find it: Last clip -> Transitions -> Basic -> "Fade"
Duration: 00:00:02:00 (60 frames)
Why: Luxury content fades out. Never hard cuts to black.

00:00:28:00
Action: Add logo lower third
Duration: 00:00:02:00
Animation: "Fade In" -> hold -> "Fade Down"
Why: Final brand mark. Clean exit.

========================================

COLOR GRADING NOTES

Apply globally:
- Filter: "Gloomy Cinema" at 70% (established in opening)
- Adjust -> Brightness: +5
- Adjust -> Contrast: +10
- Adjust -> Highlights: -15 (protect blown highlights)
- Adjust -> Shadows: +5 (lift blacks slightly - luxury never goes full black)
- Adjust -> Temperature: +8 (warm shift)
Find it: Select all clips -> Adjust tab -> manual sliders

========================================

EDITING REVIEW

Pacing: Cinematic (average change interval: ~4.5s / 135 frames)
Visual variation: Moderate (2 transitions, 3 zooms, 1 speed ramp)
Effect count: 3 (Gloomy Cinema filter, Soft Glow, Anamorphic Flare)
Audio: 1 ambient pad (-20dB)
Text: 2 elements (brand name, tagline)
Brand consistency: High - single filter, single transition family, serif typography
Suggested improvements: Consider adding a 2-second product reflection shot between 00:00:14:00 and 00:00:15:00 for pacing variety.
```

---

## FILE: knowledge-base/KF-01-core-ui-navigation.md

# KF-01: CapCut Desktop Pro (Mac) — Core UI Navigation Master Map

Version: 1.0
Source: 22 screen-captured frames from Video 1 (5 min UI exploration) + Video 2 (12 min exploration)
App Version: CapCut Desktop Pro (Mac, dark theme default)

---

## 1. GLOBAL LAYOUT (ASCII Diagram)

```
+------------------------------------------------------------------+
|  [CapCut Logo]   MENU BAR (File Edit Media etc)    [Export btn]  |
+------------------------------------------------------------------+
|  TOP TOOLBAR (Undo/Redo, Project settings, toolbar icons)        |
+----------+----------------------------+--------------------------+
|          |                            |                          |
|  LEFT    |     CANVAS / PREVIEW       |     RIGHT PANEL          |
|  PANEL   |     (Video Preview         |     (Inspector:          |
|  (Media, |      with playback         |      Video, Speed,       |
|  Audio,  |      controls)             |      Animation, Adjust,  |
|  Text,   |                            |      AI Cutout, etc.)    |
|  Sticker,|                            |                          |
|  Effects,|                            |                          |
|  Trans., |                            |                          |
|  Filters,|                            |                          |
|  Adjust, |                            |                          |
|  etc.)   |                            |                          |
|          |                            |                          |
+----------+----------------------------+--------------------------+
|  TIMELINE TOOLBAR (split, delete, speed, keyframe, etc.)         |
+------------------------------------------------------------------+
|                                                                  |
|  TIMELINE (multi-track: Video, Audio, Text, Effects layers)      |
|  [Track headers on left]  [Clips on timeline]   [Scrollbar]     |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 2. TOP MENU BAR (Left to Right)

Located at the very top of the window (Mac native menu bar when focused):

| Position | Label | Notes |
|----------|-------|-------|
| 1 | **CapCut** | App menu (About, Preferences, etc.) |
| 2 | **File** | New project, Open, Save, Import, etc. |
| 3 | **Edit** | Undo, Redo, Cut, Copy, Paste, Select All, Delete |
| 4 | **Media** | Import media, media management |
| 5 | **Clip** | Clip-level operations |
| 6 | **Transitions** | Transition controls |
| 7 | **Options** | App options/preferences |
| 8 | **Filter** | Filter-related menu |
| 9 | **Adjustment** | Color/image adjustment |
| 10 | **Sticker** | Sticker management |
| 11 | **Transform** / **Timeline** | Timeline-related operations |
| 12 | **Autocut** | AI-powered auto-editing features |

### Top-Right Corner
| Element | Description |
|---------|-------------|
| **Export** button | Blue/teal prominent button — opens export dialog |
| **Upgrade / Pro badge** | Pro subscription indicator (top-right area) |

---

## 3. TOP TOOLBAR (Below Menu Bar, Above Canvas)

A horizontal strip of icon buttons running left to right:

| Position | Icon/Button | Function |
|----------|-------------|----------|
| 1 | **Undo** (curved left arrow) | Undo last action |
| 2 | **Redo** (curved right arrow) | Redo last action |
| 3-8 | **6 small square tool icons** | Selection/transform tools — includes pointer/select, crop, shape drawing tools (rectangle, triangle, circle, pentagon, line, arrow shapes visible in f_0071) |
| 9 | **Project Settings** area | Shows project name, resolution info |

### Sub-toolbar (visible below main toolbar in some views)
| Element | Description |
|---------|-------------|
| Import tab row | **Import** \| **Filmed** \| **Cloud** — media source toggle |
| Media thumbnails | Grid of imported media files with duration overlays |

---

## 4. LEFT PANEL — Navigation Tabs (Vertical Sidebar)

The left panel has a vertical tab strip. Each tab opens a different asset/tool browser. Tabs observed across all frames:

### Video 1 Layout (Standard Editing Mode)
| Tab Icon | Tab Label | Description |
|----------|-----------|-------------|
| Film strip | **Media** | Imported project media (images, video, audio files) |
| Musical note | **Audio** | Music, sound effects, audio assets |
| "T" letter | **Text** | Text templates, titles, captions, subtitles |
| Smiley face | **Stickers** | Sticker/emoji overlays |
| Sparkle/star | **Effects** | Video/visual effects library |
| Overlap squares | **Transitions** | Transition effects between clips |
| Adjustment icon | **Filters** | Color filter presets |
| Sliders icon | **Adjust** | Color/exposure adjustment tools |
| Wand/magic | **Assets** / **Library** | Additional asset library |

### Video 2 Layout (Extended Panel — Stickers Sub-navigation Visible)
Left panel shows deep sub-category navigation when Stickers tab is active:

**Sticker Categories (scrollable list):**
| Category | Content Type |
|----------|-------------|
| Trending | Popular/trending stickers |
| Favorites | User-saved favorites |
| Animals | Cat, dog, bird, panda stickers |
| Emoji | Standard emoji-style stickers |
| Love | Hearts, romance themed |
| Sad | Sad/melancholy expressions |
| Cool | Sunglasses, swagger themed |
| Angry | Angry/frustrated expressions |
| Cute | Kawaii/cute style |
| Text Sticker | Text-based decorative stickers |
| Arrow | Arrow indicators |
| Shape | Geometric shapes |
| Food | Food/drink stickers (visible in f_0070 — coffee, pizza, donut, burger, fries, sushi, ramen, watermelon, cake, cookies, etc.) |
| Mark/Label | Labels, badges, tags |
| Festival | Holiday/celebration themed |
| Music | Musical note stickers |
| Social Media | Platform logos, like/share icons |
| Weather | Sun, cloud, rain, snow |
| Gesture | Hand gestures (pointing, peace, OK) |
| Sports | Sports equipment, balls |
| Travel | Airplane, suitcase, landmarks |
| Decoration | General decorative elements |
| Business Style | Professional/corporate stickers |
| Counter | Countdown/number stickers |
| Bubble | Speech/thought bubbles |
| Mosaic | Pixelation/mosaic overlays |
| Marker | Highlight/marker effects |
| Body Effects | Body-related AR effects |

### Video 2 — Effects/Transitions Sub-navigation
When Effects tab is active (f_0073-f_0080), the left panel shows:

**Effect Categories:**
| Category | Description |
|----------|-------------|
| Trending / Featured | Highlighted effects |
| New | Recently added effects |
| Favorites | User-favorited effects |
| My Effects | Custom/downloaded effects |
| Basic | Fundamental effects (blur, glow, etc.) |
| Particle | Particle system effects |
| Dark | Dark mood effects |
| Film | Film grain, vintage looks |
| Retro | Retro/throwback styles |
| Comic | Comic book/manga style |
| Dreamy | Soft/dream-like effects |
| 3D | Three-dimensional effects |
| Edge / Blur | Edge detection, blur variants |
| Glitch | Digital glitch/distortion |
| Natural | Nature-inspired effects |
| Overlay | Light leak, bokeh overlays |
| Split | Split-screen effects |
| Opening | Intro/opening title effects |
| Lens | Lens flare, lens effects |
| Smoke | Smoke/fog effects |
| Bubble | Bubble overlay effects |
| Emotion | Mood/emotion effects |
| Body Effects | AR body-tracking effects |
| Video Effects | Full-frame video effects |

The thumbnails in the panel show preview images in a grid layout (5-8 columns), each with a small preview of the effect applied to sample footage.

---

## 5. RIGHT PANEL — Inspector / Properties Panel

The right panel changes context based on what is selected on the timeline. Located on the right side of the canvas.

### Right Panel Top Tab Bar
| Tab | Description |
|-----|-------------|
| **Video** | Core video clip properties (position, scale, rotation, opacity) |
| **Speed** | Speed/tempo controls (speed curve, constant speed) |
| **Animation** | Keyframe animation controls (In/Out/Combo animations) |
| **Adjust** | Color correction — HSL, curves, color wheels |
| **AI Cutout** | AI-powered background removal/subject isolation |
| **AI Stylize** | AI style transfer |

### Video Tab Properties (f_0001-f_0003)
| Section | Controls |
|---------|----------|
| **Transform** | |
| Position | X and Y coordinate fields with numeric input |
| Scale | Uniform scale slider + numeric field (linked/unlinked) |
| Rotation | Angle in degrees |
| Flip | Horizontal / Vertical flip buttons (mirror icons) |
| Opacity | 0-100% slider |
| **Blend** | Blend mode dropdown |
| **Stabilize** | Video stabilization toggle |
| **Enhance quality** | AI quality enhancement checkbox/toggle |
| **Remove Image noise** | Noise reduction toggle |
| **Optical flow** | Frame interpolation toggle |
| **Eye contact** | AI eye contact correction toggle |
| **Lens correction** | Lens distortion correction toggle |
| **Auto reframe** | AI auto-reframe toggle |
| **Remove flicker** | Flicker removal toggle |
| **Camera tracking** | Camera/motion tracking toggle |

Bottom of Video tab:
| Element | Description |
|---------|-------------|
| **Freeze** | Freeze frame button |

### Speed Tab (f_0010)
| Control | Description |
|---------|-------------|
| **Speed** | Speed multiplier slider |
| **Memory effect** | Toggle for speed ramp memory |
| **Change audio pitch** | Toggle — whether pitch shifts with speed change |
| Curve presets | Speed curve editor (ramp in, ramp out, custom) |
| **Reset** button | Reset speed to default |

### Animation Tab (f_0005)
| Control | Description |
|---------|-------------|
| **Add mask** | Button to add animation mask |
| Grid of animation presets | Thumbnail grid showing animation styles |

### Adjust Tab (f_0006-f_0007)
| Section | Controls |
|---------|----------|
| **Auto color** | One-click auto color correction toggle + dropdown |
| **Loading** | Processing indicator when analyzing |
| **Presets** | Color preset selection |
| **Basic** section: | |
| Brightness | Slider -100 to +100 |
| Contrast | Slider -100 to +100 |
| Saturation | Slider -100 to +100 |
| Exposure | Slider |
| Highlights | Slider |
| Shadows | Slider |
| Temperature | Slider (warm/cool) |
| Tint | Slider |
| Sharpness | Slider |
| Vignette | Slider |
| Fade | Slider |
| **HSL** section: | |
| Per-channel Hue/Saturation/Lightness controls | |
| Color dots (skin tones row) | Selectable color targets for HSL adjustment |
| **Color Wheels** | Shadows/Midtones/Highlights wheels |
| **Curves** | RGB curves editor |
| **Print midrange** / **Print Vintage** | Color grading presets |
| Single color option | Monotone/duotone grading |
| **Save as Preset** | Save current adjustments as reusable preset |

### AI Cutout Tab (f_0004)
| Control | Description |
|---------|-------------|
| **Auto removal** | AI auto background removal toggle |
| **Custom removal** | Manual masking/removal tool |
| **Chroma key** | Green screen / chroma key controls |

### AI Stylize Tab (f_0008-f_0009)
| Section | Controls |
|---------|----------|
| **Style presets** | Grid of AI style thumbnails (3D render, oil painting, anime, portrait styles) |
| **Retouch** section | |
| Face presets grid | Grid of face retouching presets (smooth skin, reshape, beauty modes) — approximately 30-40 preset thumbnails visible |
| **Makeup** section | |
| Makeup presets | Additional beauty filter presets |
| **Bokeh** | Background blur/bokeh effect controls |

---

## 6. CANVAS / PREVIEW AREA

Center of the interface. The preview/canvas area contains:

| Element | Location | Description |
|---------|----------|-------------|
| **Canvas** | Center | Live preview of current frame at playhead position |
| **Project title** | Above canvas | "Player Preview X" or project name display |
| **Canvas resize handles** | Canvas edges | Blue dotted border with drag handles for repositioning clips |
| **Safe zone guides** | Overlaid on canvas | Optional safe zone overlay |
| **Playback transport** | Below canvas | Play/pause and scrub controls |
| **Timecode display** | Below canvas, left of transport | Current position / total duration (format: HH:MM:SS:FF) |
| **AI Script** button | Below canvas, left side | "AI Script" — AI-powered script/caption generation |

### Playback Controls (Below Canvas)
| Position | Button/Control | Description |
|----------|----------------|-------------|
| Left | Timecode readout | Current time / Total time |
| Center-Left | **Previous frame** | Step back one frame (left arrow icon) |
| Center | **Play/Pause** | Large play/pause toggle (triangle/double-bar) |
| Center-Right | **Next frame** | Step forward one frame (right arrow icon) |
| Right group | **Canvas zoom** | Fit / zoom controls for preview |
| Right group | **Full screen preview** | Expand preview to full screen |
| Right group | **Split view** | Side-by-side comparison view |
| Right group | **Quality toggle** | Preview quality (draft/full) |

---

## 7. TIMELINE AREA

### Timeline Toolbar (Horizontal bar above the timeline tracks)

| Position | Icon/Button | Description |
|----------|-------------|-------------|
| 1 | **Lock/Unlock** (padlock) | Lock/unlock selected track |
| 2 | **Eye/Visibility** (eye icon) | Toggle track visibility |
| 3 | **Mute track** (speaker icon) | Mute audio for selected track |
| 4 | **Split** (scissors/blade) | Split clip at playhead |
| 5 | **Delete** (trash can) | Delete selected clip |
| 6 | **Speed** (speedometer) | Quick speed adjustment |
| 7 | **Crop** (crop frame) | Crop tool |
| 8 | **Transform** (move arrows) | Transform/position tool |
| 9 | **Freeze frame** (snowflake/pause) | Create freeze frame at playhead |
| 10 | **Keyframe** (diamond) | Add/remove keyframe at playhead |
| 11 | **Volume / Audio** (waveform) | Audio level adjustment |
| 12 | **Text-to-speech** / **Voiceover** (mic) | Record or generate voiceover |
| 13 | **Marker** (flag) | Add marker at playhead |
| 14 | **Group** (brackets) | Group/ungroup clips |
| 15 | **Zoom to fit** (magnifier) | Fit timeline to view |

### Timeline Zoom Controls (far right of timeline toolbar)
| Control | Description |
|---------|-------------|
| **Zoom slider** | Horizontal slider to zoom in/out on timeline |
| **Zoom to fit** | Button to auto-fit all clips in view |
| **+/-** buttons | Incremental zoom in/out |

### Timeline Track Structure
| Track Type | Position | Description |
|------------|----------|-------------|
| **Video tracks** | Top section | Multiple video tracks, stacked top-down (V1, V2, V3...) |
| **Audio tracks** | Bottom section | Multiple audio tracks (A1, A2...) |
| **Text/Title track** | Between video and audio | Dedicated text overlay tracks |
| **Effects track** | Varies | Adjustment/effects layers |

### Track Headers (Left side of each track)
| Element | Description |
|---------|-------------|
| Track label | V1, V2, A1, A2, etc. |
| Lock icon | Lock/unlock individual track |
| Eye icon | Show/hide individual track |
| Mute icon | Mute audio on individual track |
| Collapse/expand | Toggle track height |

### Timeline Navigation
| Element | Description |
|---------|-------------|
| **Playhead** | Vertical teal/cyan line with top handle — draggable scrubber |
| **Time ruler** | Horizontal ruler with timecode markings above tracks |
| **Clip thumbnails** | Video clips show frame thumbnails; audio shows waveforms |
| **Horizontal scrollbar** | Bottom of timeline for horizontal scrolling |
| **Vertical scrollbar** | Right side for scrolling between many tracks |

---

## 8. EXPORT SETTINGS

Export button is located top-right corner (teal/blue button labeled **Export**).

Visible in the properties panel area (f_0071, Video 2 frames):

| Field | Value/Options Observed |
|-------|----------------------|
| **Name** | Project filename field |
| **Format** | MP4, GIF, PNG (visible options) |
| **Stay in original location** | Toggle for export path |
| **Resolution** | Dropdown (e.g., 1080x1920 for vertical) |
| **Preset** | Preset selection |
| **Frame rate** | Framerate setting (e.g., "Timeline st" = timeline standard) |
| **Codec** | H.264, HEVC options |
| **Quality** | Quality slider/dropdown |
| **Bitrate** | Bitrate control |
| **Audio** | Audio export settings |
| **Modify** button | Bottom-right of export panel — opens advanced export settings |

---

## 9. KEYBOARD SHORTCUTS (Visible in Menus/Tooltips)

Based on menu items and tooltips observed:

| Shortcut | Action |
|----------|--------|
| **Cmd+Z** | Undo |
| **Cmd+Shift+Z** | Redo |
| **Cmd+S** | Save project |
| **Cmd+Shift+S** | Save as |
| **Space** | Play/Pause toggle |
| **Left Arrow** | Previous frame |
| **Right Arrow** | Next frame |
| **Cmd+B** | Split clip at playhead |
| **Delete / Backspace** | Delete selected clip |
| **Cmd+C** | Copy |
| **Cmd+V** | Paste |
| **Cmd+X** | Cut |
| **Cmd+A** | Select all |
| **Cmd+D** | Duplicate |
| **+/-** | Timeline zoom in/out |
| **Cmd+E** | Export |
| **Cmd+I** | Import media |

---

## 10. RIGHT-CLICK CONTEXT MENUS

No explicit right-click context menus were captured in the reviewed frames. Based on standard CapCut behavior, expected context menus include:

### Timeline Clip Right-Click (Expected)
| Menu Item | Description |
|-----------|-------------|
| Cut | Cut clip |
| Copy | Copy clip |
| Paste | Paste clip |
| Delete | Remove clip |
| Split | Split at playhead |
| Duplicate | Duplicate clip |
| Speed | Open speed controls |
| Reverse | Reverse clip playback |
| Freeze | Create freeze frame |
| Replace | Replace with another media file |
| Unlink audio | Separate audio from video |
| Group / Ungroup | Group/ungroup selected clips |
| Adjust | Open color adjustment |

---

## 11. SHAPE TOOLS (Video 2, f_0071)

When the shape/annotation tool is active, the left panel shows:

| Shape | Icon |
|-------|------|
| Rectangle | Outlined rectangle |
| Rounded Rectangle | Rectangle with rounded corners |
| Triangle | Triangle shape |
| Circle/Ellipse | Circle shape |
| Pentagon | Pentagon shape |
| Star | Star shape |
| Arrow | Arrow shape |
| Line | Straight line |
| Curved line | Bezier/curved line tool |

---

## 12. MEDIA PANEL DETAILS (Video 1, f_0001-f_0003)

When the Media tab is active in the left panel:

### Sub-tabs at top of Media panel
| Tab | Description |
|-----|-------------|
| **Import** | Locally imported media |
| **Filmed** | Media recorded directly in CapCut |
| **Cloud** | Cloud-synced media from CapCut cloud |

### Media Browser
| Element | Description |
|---------|-------------|
| Thumbnail grid | Grid of media thumbnails (4 columns observed) |
| Duration overlay | Time duration shown on each video thumbnail |
| Resolution badge | Resolution indicator on thumbnails |
| Selection highlight | Teal/cyan border on selected media |
| Drag-to-timeline | Media items can be dragged directly to timeline |

---

## 13. BOTTOM STATUS BAR

| Position | Element | Description |
|----------|---------|-------------|
| Far left | Timeline navigation buttons | First frame, previous keyframe, etc. |
| Center-left | **AI Script** button | AI-powered captioning/transcription |
| Center | Timecode | Current position / total duration |
| Center-right | Playback transport | Play/Pause + frame step buttons |
| Right group | Canvas display controls | Zoom fit, split view, full screen, quality |
| Far right | Teal circle icon | CapCut AI assistant / help / notification indicator |

---

## 14. PROJECT SETTINGS AREA

Visible in the top toolbar area:

| Setting | Description |
|---------|-------------|
| **Project name** | Editable project title field |
| **Resolution display** | Shows current project resolution (e.g., 1080x1920) |
| **Frame rate** | Project frame rate indicator |
| **Aspect ratio** | Current aspect ratio (9:16 vertical visible in frames) |

---

## FRAME-BY-FRAME OBSERVATION LOG

| Frame | Source | Panel State | Key Observations |
|-------|--------|-------------|------------------|
| v1/f_0001 | Video 1 | Video tab (right panel) — Transform section | Full right panel inspector visible: Transform (position, scale, rotation), Flip, Blend, Stabilize, Enhance quality, Remove image noise, Optical flow, Eye contact, Lens correction, Auto reframe, Remove flicker, Camera tracking. Checkboxes with toggle states. |
| v1/f_0002 | Video 1 | Video tab scrolled down | Same as f_0001 but scrolled to show lower controls. Track height shows resolution/frame info. |
| v1/f_0003 | Video 1 | Video tab — lower section | Shows Freeze button at bottom. Additional AI toggles visible. "Save to" area visible. |
| v1/f_0004 | Video 1 | AI Cutout tab active | Right panel shows: Auto removal, Custom removal, Chroma key sections. Minimal controls — toggle-based. |
| v1/f_0005 | Video 1 | Animation tab / Mask | "Add mask" button visible. Animation preset grid area (mostly empty in this frame). |
| v1/f_0006 | Video 1 | Text/Adjust tab — color settings | Shows "Auto color" toggle with dropdown. Basic color controls: list of labeled sliders. Skin tone color dots row. "Print midrange" option. |
| v1/f_0007 | Video 1 | Adjust tab — full color panel | Loading indicator visible ("Loading"). Full slider set for brightness, contrast, saturation, etc. HSL section expanded. Color dots for skin tone targeting. |
| v1/f_0008 | Video 1 | AI Stylize tab (expanded view) | Full panel showing AI style presets (approximately 40 thumbnails). Face retouch presets grid (~30 face thumbnails). Sections: Style presets, Retouch, Makeup, Bokeh. |
| v1/f_0009 | Video 1 | AI Stylize tab | Similar to f_0008 with Retouch section showing face preset thumbnails in grid layout. |
| v1/f_0010 | Video 1 | Speed tab active | Right panel: Speed slider, Memory effect toggle, Change audio pitch toggle, Curve editor area, Reset button. |
| v2/f_0001 | Video 2 | Stickers panel — emoji/animal category | Left panel: Full sticker category sidebar. Main area: grid of animated sticker thumbnails (cats, dogs, skulls, pumpkins, food items). Right panel: Export settings visible (name, format, resolution, codec fields). |
| v2/f_0070 | Video 2 | Stickers panel — Food category | Left panel sticker categories scrolled. Main grid shows food stickers (coffee cups, burgers, pizza, ramen, cake, donuts, cookies, sushi, watermelon, fries). |
| v2/f_0071 | Video 2 | Shape tools active | Left panel shows shape tool palette: rectangle, rounded rect, triangle, circle, pentagon, star, arrow, line, curve. Right panel: export/properties fields. "Modify" button bottom-right. |
| v2/f_0072 | Video 2 | Body Effects sub-panel | Left panel shows "Body effects" and "Body effects" categories with "Loading" state. |
| v2/f_0073 | Video 2 | Effects panel — grid view | Left panel: effects category list. Main area: large grid of effect preview thumbnails (~8 columns). Categories visible: Trending, Featured, New, Favorites, Basic, etc. |
| v2/f_0074 | Video 2 | Effects panel — same view | Same as f_0073, slightly different scroll position. |
| v2/f_0075 | Video 2 | Effects panel — scrolled | More effect thumbnails visible in grid. Sub-categories expanding. |
| v2/f_0076 | Video 2 | Effects panel — more scroll | Grid continues. Visual effects showing applied-to-person previews. |
| v2/f_0077 | Video 2 | Effects panel — further scroll | Additional effect categories visible. Grid thumbnails continue. |
| v2/f_0078 | Video 2 | Effects panel — deep scroll | More effect previews. Body/AR effect thumbnails becoming prominent. |
| v2/f_0079 | Video 2 | Effects panel — bottom area | Near end of effects library. Diverse effect styles: silhouette, glow, particle, film grain. |
| v2/f_0080 | Video 2 | Effects panel — bottom | Final effects in library. Mix of artistic and practical effects. |

---

## NOTES

1. **Dark Theme**: CapCut Desktop Pro on Mac uses a dark UI theme by default — dark gray (#1a1a1a to #2d2d2d) backgrounds with teal/cyan (#00d4aa approximate) accent colors for selection states, playhead, and active buttons.

2. **Responsive Panels**: Left and right panels are resizable. The left panel width expands when browsing large asset libraries (stickers, effects). The right panel width is relatively fixed.

3. **9:16 Vertical Project**: All observed frames show a 9:16 (vertical/portrait) project — the canvas displays a tall vertical frame. This is the social media / Reels / TikTok / Shorts format.

4. **Pro Features Identified**: AI Cutout, AI Stylize, Eye contact correction, Camera tracking, Optical flow, Enhance quality — these are Pro-tier features indicated by their presence in the inspector panel.

5. **Asset Libraries**: Stickers and Effects panels contain hundreds of assets organized in scrollable grids with category-based sidebar navigation. Assets appear to be a mix of built-in and downloadable (cloud indicator icons on some thumbnails).

6. **Timeline**: Shows multiple clips arranged sequentially on the primary video track. Thumbnails are visible on clips. The timeline supports multi-track editing with dedicated video, audio, and text tracks.

---

## FILE: knowledge-base/KF-05-text-captions.md

# KF-05: CapCut Desktop Pro (Mac) — Text, Captions & Title System

Version: 1.0
Source: 43 screen-captured frames across Video 1 (f_0050-f_0075, f_0085-f_0100) + Video 2 (f_0094-f_0110)
App Version: CapCut Desktop Pro (Mac, dark theme default)

---

## 1. TEXT PANEL OVERVIEW

**Location:** Left Panel > Text tab (icon: "T" letter)

### Left Panel Sub-tabs (Vertical Text Navigation)
| Sub-tab | Description |
|---------|-------------|
| **Default text** | Plain text insertion — adds a basic editable text box to canvas |
| **Text templates** | Pre-designed animated/styled text overlays with motion |
| **Auto captions** | AI-powered automatic speech-to-text subtitle generation |
| **Local captions** | Manual subtitle/caption creation with SRT/VTT-style controls |

---

## 2. TEXT TEMPLATES

### Template Browser Layout
When "Text templates" is selected, the right panel area displays a scrollable grid of pre-built text template thumbnails. Templates are previewed as small animated cards showing the style applied to the word "ART" or sample text with decorative elements.

### Template Categories (observed in right panel filter tabs)
| Tab/Filter | Description |
|------------|-------------|
| **All** | Shows all available templates |
| **Animations** | Templates with motion/kinetic typography |
| **Tracking** | Motion-tracked text that follows objects |
| **Text to speech** | Templates optimized for TTS integration |
| **AI avatars** | Templates paired with AI-generated avatar/presenter |
| **Presets** | Quick-access saved/preset templates |
| **History** | Recently used templates |

### Text Template Styles (Sticker/Overlay Style — f_0050)
Frame f_0050 shows the text template browser in the right panel with a massive grid (approximately 10 columns x 20+ rows = 200+ template thumbnails). These are decorative text badge/label templates — not ART styles but pre-made text overlays. Visible styles include:

| Style Category | Visual Description | Approximate Count |
|---------------|-------------------|-------------------|
| **Bubble/Badge** | Rounded pill-shape backgrounds with text | 30+ |
| **Banner/Ribbon** | Horizontal ribbon/banner text frames | 20+ |
| **Box/Frame** | Rectangular bordered text containers | 25+ |
| **Neon/Glow** | Glowing outlined text effects | 15+ |
| **Handwritten** | Script/casual handwritten style overlays | 10+ |
| **Bold/Block** | Heavy weight block-letter title cards | 20+ |
| **Lower Third** | Broadcast-style lower-third name plates | 15+ |
| **Price Tag/Sale** | E-commerce sale badge overlays | 10+ |
| **Social/Subscribe** | YouTube subscribe, like, follow overlays | 10+ |
| **Minimal/Clean** | Simple thin-line text containers | 15+ |
| **Retro/Vintage** | Aged/retro styled text badges | 10+ |
| **3D/Perspective** | Three-dimensional extruded text | 10+ |
| **Gradient Fill** | Text with gradient color fills | 15+ |
| **Outline Only** | Hollow/stroke-only text | 10+ |
| **Split Color** | Multi-colored segmented text | 10+ |

**Total visible text templates (f_0050):** 200+ individual templates in the grid

---

## 3. ART TEXT STYLES (Massive Library)

### Overview
Frames f_0051 through f_0064 show continuous scrolling through the ART text styles library in the right panel. Each style is displayed as the word "ART" rendered in a distinct visual treatment. The library is enormous — observed across 14 frames of continuous scrolling.

### ART Style Count Estimation
- Each frame shows approximately 80-100 ART style thumbnails (10 columns x 8-10 rows)
- Across 14 frames of scrolling with minimal overlap: **700-900+ unique ART text styles**
- This represents one of the largest pre-built text style libraries in any desktop video editor

### ART Style Categories by Visual Treatment

#### Metallic & Chrome (f_0051-f_0052)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Chrome Silver | Mirror-finish silver reflective text | 8+ |
| Gold Metallic | Polished gold reflective finish | 10+ |
| Rose Gold | Pink-tinted metallic finish | 6+ |
| Bronze/Copper | Warm-toned metallic | 5+ |
| Platinum | Cool silver-white metallic | 4+ |
| Brushed Metal | Textured brushed steel appearance | 6+ |
| Chrome Rainbow | Iridescent/holographic chrome | 4+ |

#### Neon & Glow (f_0051-f_0053)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Blue Neon | Electric blue glow outline | 8+ |
| Red Neon | Red neon tube glow | 6+ |
| Green Neon | Green fluorescent glow | 6+ |
| Pink/Magenta Neon | Hot pink neon glow | 8+ |
| Yellow Neon | Yellow/amber neon | 4+ |
| White Neon | Clean white glow | 4+ |
| Multi-color Neon | Rainbow/gradient neon effects | 6+ |
| Neon Sign (with backing) | Neon text on dark board/brick background | 5+ |

#### Outline & Stroke (f_0052-f_0054)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Thin Outline | Single-pixel or thin stroke outline | 8+ |
| Thick Outline | Heavy bold stroke | 6+ |
| Double Outline | Dual-stroke layered outline | 5+ |
| Dotted Outline | Dashed/dotted border strokes | 4+ |
| Gradient Outline | Outline with color gradient | 6+ |
| Offset Outline | Outline offset from fill | 4+ |

#### Gradient & Color Fill (f_0053-f_0056)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Blue-Purple Gradient | Cool-tone gradient fills | 8+ |
| Orange-Red Gradient | Warm sunset gradients | 6+ |
| Green-Teal Gradient | Nature-tone gradients | 5+ |
| Pink-Purple Gradient | Pastel/vaporwave gradients | 8+ |
| Rainbow Gradient | Full spectrum color fills | 6+ |
| Black-White Gradient | Monochrome gradient | 4+ |
| Duotone | Two-color split fills | 8+ |

#### 3D & Extruded (f_0054-f_0056)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| 3D Block | Extruded block text with depth shadow | 10+ |
| 3D Isometric | Isometric perspective 3D text | 6+ |
| 3D Metallic | 3D text with metallic material | 8+ |
| 3D Cartoon | Rounded/bubbly 3D text | 6+ |
| 3D Glass | Transparent/glass-like 3D effect | 4+ |
| Embossed | Raised/embossed surface text | 5+ |
| Debossed | Pressed-in/engraved text | 3+ |

#### Texture & Material (f_0055-f_0058)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Wood | Wood grain texture fill | 4+ |
| Marble | Marble/stone texture | 4+ |
| Water/Liquid | Fluid/water texture fill | 5+ |
| Fire/Flame | Fire-textured text | 6+ |
| Ice/Frost | Frozen/icy texture | 4+ |
| Grass/Nature | Organic green texture | 3+ |
| Galaxy/Space | Starfield/nebula texture | 6+ |
| Glitter/Sparkle | Glittering particle texture | 5+ |
| Concrete/Grunge | Rough concrete/industrial | 4+ |
| Carbon Fiber | Technical carbon weave | 3+ |
| Leather | Leather texture fill | 2+ |

#### Shadow & Depth (f_0056-f_0058)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Drop Shadow | Classic offset shadow | 8+ |
| Long Shadow | Extended directional shadow | 6+ |
| Inner Shadow | Shadow inside letterforms | 4+ |
| Perspective Shadow | 3D perspective ground shadow | 5+ |
| Soft Glow Shadow | Diffused glowing shadow | 6+ |
| Hard Shadow | Sharp-edge offset shadow | 4+ |
| Multi-Shadow | Layered multiple shadow directions | 3+ |

#### Retro & Vintage (f_0057-f_0059)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| 80s Retro | Synthwave/retro-futuristic neon | 8+ |
| 70s Disco | Groovy/disco ball metallic | 4+ |
| 60s Pop Art | Pop art bold color blocks | 4+ |
| Vintage Film | Aged/distressed film title look | 5+ |
| VHS/Analog | VHS tracking/analog distortion | 4+ |
| Typewriter | Old typewriter stamped look | 3+ |
| Western | Western/saloon serif style | 3+ |
| Art Deco | 1920s art deco geometric style | 4+ |

#### Cartoon & Playful (f_0058-f_0060)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Bubble/Bubbly | Rounded bubblegum text | 6+ |
| Comic Book | Action comic/kapow style | 6+ |
| Graffiti | Street art/spray paint style | 5+ |
| Sticker Peel | 3D sticker with peel effect | 4+ |
| Pixel/8-bit | Pixelated retro game style | 4+ |
| Crayon/Chalk | Hand-drawn crayon/chalk look | 3+ |
| Doodle | Sketch/doodle outlined style | 4+ |

#### Dark & Dramatic (f_0059-f_0061)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Blood/Horror | Red dripping horror text | 5+ |
| Toxic/Acid | Green toxic/acidic drip | 4+ |
| Cracked/Shattered | Fractured/broken text | 4+ |
| Dark Metal | Heavy metal band logo style | 6+ |
| Smoke/Mist | Smoky/foggy dissolving text | 4+ |
| Electric/Lightning | Electric spark/lightning | 5+ |

#### Pink & Purple Tones (f_0059-f_0061)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Pastel Pink | Soft baby pink fills | 6+ |
| Hot Pink | Vibrant magenta fills | 8+ |
| Purple Velvet | Deep purple luxe fills | 5+ |
| Lavender | Light purple/lavender | 4+ |
| Pink Neon | Pink neon glow variants | 6+ |
| Rose | Muted rose/dusty pink | 4+ |

#### Red & Warm Tones (f_0061-f_0062)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Crimson Red | Deep red solid fills | 6+ |
| Fire Red | Bright fiery red | 8+ |
| Red Metallic | Red chrome/metallic | 4+ |
| Red Outline | Red stroke-only variants | 5+ |
| Red Neon | Red neon glow | 4+ |
| Red 3D | Red extruded 3D text | 5+ |
| Orange | Warm orange fills | 6+ |
| Gold on Red | Gold text on red background plate | 4+ |

#### Gold & Luxury (f_0062-f_0063)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Classic Gold | Traditional gold fill | 8+ |
| Gold Foil | Stamped gold foil texture | 5+ |
| Gold Outline | Gold stroke-only | 4+ |
| Gold 3D | Extruded gold 3D text | 5+ |
| Gold Glitter | Sparkly gold particle | 4+ |
| Gold Gradient | Gold-to-dark gradient | 5+ |
| Black & Gold | Black fill with gold accent | 6+ |
| Gold Embossed | Raised gold on dark surface | 4+ |

#### Teal & Cool Tones (f_0054-f_0055)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Teal Solid | Solid teal/cyan fills | 6+ |
| Teal Neon | Teal glow effects | 5+ |
| Teal Gradient | Teal-to-blue gradients | 4+ |
| Ice Blue | Frozen blue crystal | 4+ |
| Ocean Blue | Deep ocean blue | 5+ |
| Cyan Electric | Bright electric cyan | 4+ |

#### Multicolor & Psychedelic (f_0063-f_0064)
| Style Group | Visual Description | Count |
|-------------|-------------------|-------|
| Rainbow | Full rainbow color rotation | 6+ |
| Tie-Dye | Swirled multi-color | 3+ |
| Holographic | Iridescent color shift | 4+ |
| Color Burst | Explosion of multiple colors | 4+ |
| Gradient Mesh | Complex multi-point gradient | 3+ |

### ART Style Total: 700-900+ individual pre-built styles

---

## 4. TEXT TEMPLATES (Animated/Motion — f_0066-f_0072)

### Transition from ART Styles to Text Templates
Frames f_0066-f_0072 show the transition from the ART style grid into the animated text templates section. The right panel shifts to show the "Tracking" and "Presets" tabs.

### Text Template Categories (f_0066-f_0072)
The animated text template library shows templates organized by category. Each template thumbnail shows a small preview of the motion/animation with sample text.

#### Template Styles Observed
| Category | Visual Description | Count |
|----------|-------------------|-------|
| **Minimal Titles** | Clean, thin-font titles with subtle entrance animations | 20+ |
| **Cinematic Titles** | Film-style credit/title cards with dramatic motion | 15+ |
| **Social Media** | Platform-optimized (TikTok/Reels/Shorts style) text overlays | 25+ |
| **Lower Thirds** | Broadcast-quality name plates and lower-third graphics | 20+ |
| **Call-to-Action** | Subscribe, follow, like, swipe-up style buttons | 15+ |
| **Lyric/Quote** | Styled lyric or quote display templates | 10+ |
| **Counter/Number** | Countdown, numbering, list-style animated text | 10+ |
| **Intro/Outro** | Opening and closing title sequences | 15+ |
| **Split Text** | Text that splits, reveals, or transforms | 10+ |
| **Handwriting Reveal** | Text that appears as if being handwritten | 8+ |
| **Typewriter** | Character-by-character typing reveal | 6+ |
| **Glitch Text** | Digital glitch/distortion text reveals | 8+ |
| **Bounce/Pop** | Bouncy, energetic text entrance | 10+ |
| **Slide/Wipe** | Text sliding or wiping in from edges | 12+ |
| **Zoom/Scale** | Text zooming in or scaling up/down | 10+ |
| **Rotate/Spin** | Rotating or spinning text entrance | 6+ |
| **Particle/Sparkle** | Text with particle effects around it | 8+ |
| **Brush/Paint** | Text revealed with brush stroke animation | 6+ |
| **Shake/Wobble** | Vibrating, shaking text for emphasis | 5+ |

**Total animated text templates:** 200+ individual templates

---

## 5. FONT LIBRARY

### Font Panel (f_0074-f_0075)
When a text element is selected, the right panel displays font selection and text formatting options.

#### Font Categories Observed
| Category | Description |
|----------|-------------|
| **Recently Used** | Last used fonts for quick access |
| **Favorites** | User-bookmarked fonts |
| **All** | Full searchable font library |
| **Serif** | Traditional serif typefaces |
| **Sans-Serif** | Clean sans-serif typefaces |
| **Display** | Decorative/display typefaces |
| **Handwriting** | Script and handwritten fonts |
| **Monospace** | Fixed-width/coding fonts |

#### Notable Fonts Visible in Panels (f_0074-f_0075)
The font grid displays in a multi-column layout with preview text. Font categories appear as text labels in the scrollable list. Specific font names are difficult to read at the frame resolution, but the panel structure shows:

- Search bar at top of font selector
- Category filter buttons (row of pills/chips)
- Font preview list showing each font name rendered in its own typeface
- Star/favorite icon next to each font
- Download indicator for cloud-hosted fonts (some fonts require download before use)
- Font weight/style variants expandable under each font family

#### System + Bundled Fonts
| Type | Estimated Count |
|------|----------------|
| Built-in/bundled fonts | 100+ |
| Downloadable cloud fonts | 300+ |
| System fonts (Mac) | Uses all installed Mac system fonts |

---

## 6. TEXT PROPERTIES — RIGHT PANEL (Inspector)

### Right Panel Tab Bar (when text is selected)
| Tab | Function |
|-----|----------|
| **Text** | Typography and content editing |
| **Animation** | Motion/entrance/exit animation presets |
| **Tracking** | Motion tracking to follow objects |
| **Text to speech** | AI voice generation from text content |
| **AI avatars** | AI avatar integration |
| **Presets** | Quick style presets |
| **History** | Edit history for text element |

### Text Tab Properties (f_0073, f_0085-f_0086)

#### Basic Text Controls
| Property | Control Type | Values/Range |
|----------|-------------|--------------|
| **Font** | Dropdown + search | Full font library selector |
| **Font Size** | Numeric input + slider | 1-1000+ (px or pt) |
| **Font Weight** | Dropdown | Regular, Bold, Light, etc. (font-dependent) |
| **Font Style** | Toggle buttons | Regular / Italic |
| **Text Alignment** | Button group | Left / Center / Right / Justify |
| **Vertical Alignment** | Button group | Top / Middle / Bottom |
| **Line Spacing** | Numeric input + slider | Adjustable line height |
| **Letter Spacing** | Numeric input + slider | Kerning/tracking adjustment |
| **Text Direction** | Toggle | Horizontal / Vertical writing |
| **Text Case** | Button group | Normal / UPPERCASE / lowercase / Title Case |

#### Color & Fill (f_0085)
| Property | Control Type | Description |
|----------|-------------|-------------|
| **AI Outline** | Toggle | AI-powered auto outline (Pro feature) |
| **Material fonts** | Link/button | "Try it again" — opens material font browser |
| **Color** | Color picker | Text fill color — solid color selector with eyedropper |
| **Background** | Color picker + toggle | Background plate/box color behind text |

#### Outline Section
| Property | Control Type | Values/Range |
|----------|-------------|--------------|
| **Outline** | Toggle (on/off) | Enable/disable outline |
| **Outline Color** | Color picker | Stroke color |
| **Outline Width** | Slider + numeric | 0-100 (px) |

#### Shadow Section
| Property | Control Type | Values/Range |
|----------|-------------|--------------|
| **Shadow** | Toggle (on/off) | Enable/disable shadow |
| **Shadow Color** | Color picker | Shadow color |
| **Shadow Blur** | Slider + numeric | 0-100 blur radius |
| **Shadow Distance** | Slider + numeric | 0-100 offset distance |
| **Shadow Angle** | Dial or slider | 0-360 degrees direction |
| **Shadow Opacity** | Slider | 0-100% |

#### Transform Properties (shared with all clip types)
| Property | Control Type | Values/Range |
|----------|-------------|--------------|
| **Position X** | Numeric input | Pixel position |
| **Position Y** | Numeric input | Pixel position |
| **Scale** | Slider + numeric | 0-1000% (linked/unlinked X/Y) |
| **Rotation** | Dial + numeric | 0-360 degrees |
| **Opacity** | Slider | 0-100% |
| **Blend Mode** | Dropdown | Normal, Multiply, Screen, Overlay, etc. |

#### Advanced Text Properties
| Property | Control Type | Description |
|----------|-------------|-------------|
| **Curved Text** | Toggle + slider | Bends text along a curve (arc radius control) |
| **Text Background** | Toggle + color | Adds colored highlight/box behind text |
| **Background Opacity** | Slider | Controls background plate transparency |
| **Background Roundness** | Slider | Corner radius of background box |
| **Background Padding** | Slider | Space between text and background edge |

---

## 7. ANIMATION PRESETS (f_0074-f_0075, f_0086)

### Animation Tab Structure
When the Animation tab is active, three sub-sections are available:

| Sub-tab | Function |
|---------|----------|
| **In** | Entrance/intro animation |
| **Out** | Exit/outro animation |
| **Combo** | Combined in+out or loop animations |

### Entrance Animations (In)
| Animation Name | Visual Description |
|---------------|-------------------|
| **Fade In** | Simple opacity fade from 0 to 100% |
| **Fade In Up** | Fade while sliding upward |
| **Fade In Down** | Fade while sliding downward |
| **Fade In Left** | Fade while sliding from left |
| **Fade In Right** | Fade while sliding from right |
| **Slide Up** | Quick slide from below |
| **Slide Down** | Quick slide from above |
| **Slide Left** | Slide from right to position |
| **Slide Right** | Slide from left to position |
| **Scale Up** | Zoom from small to full size |
| **Scale Down** | Zoom from large to normal size |
| **Pop** | Bounce/pop scale overshoot |
| **Bounce In** | Bouncing entrance with physics |
| **Spin In** | Rotate while fading in |
| **Flip In** | 3D flip rotation entrance |
| **Typewriter** | Character-by-character reveal |
| **Blur In** | Deblur/sharpen entrance |
| **Glitch In** | Digital glitch entrance |
| **Shake In** | Vibrating/shaking entrance |
| **Wave In** | Wavy/undulating character entrance |
| **Stomp** | Heavy impact stomp entrance |
| **Drop** | Gravity drop from above |
| **Swing** | Pendulum swing entrance |
| **Elastic** | Elastic/rubber band bounce |
| **Compress** | Squeeze then expand to position |
| **Expand** | Expand from center point |
| **Rise** | Slow upward rise with slight fade |
| **Zoom Rotate** | Combined zoom and rotation |
| **Split** | Text splits in from both sides |
| **Evaporate** | Particle-style materialization |

### Exit Animations (Out)
Mirrors the entrance animations in reverse:
| Animation Name | Visual Description |
|---------------|-------------------|
| **Fade Out** | Simple opacity fade to 0% |
| **Fade Out Up** | Fade while sliding upward and away |
| **Fade Out Down** | Fade while sliding downward |
| **Fade Out Left** | Fade while sliding left |
| **Fade Out Right** | Fade while sliding right |
| **Slide Up Out** | Slide upward off screen |
| **Slide Down Out** | Slide downward off screen |
| **Scale Up Out** | Zoom up and away |
| **Scale Down Out** | Shrink to nothing |
| **Pop Out** | Reverse bounce pop exit |
| **Spin Out** | Rotate while fading out |
| **Flip Out** | 3D flip rotation exit |
| **Blur Out** | Defocus/blur exit |
| **Glitch Out** | Digital glitch exit |
| **Shake Out** | Vibrating exit |
| **Dissolve** | Particle dissolve exit |
| **Compress Out** | Squeeze to nothing |
| **Drop Out** | Fall with gravity |

### Combo/Loop Animations
| Animation Name | Visual Description |
|---------------|-------------------|
| **Pulse** | Rhythmic scale pulse (loop) |
| **Breathe** | Slow subtle scale breathing |
| **Shake** | Continuous shake/vibrate |
| **Bounce** | Continuous bounce loop |
| **Swing** | Continuous pendulum swing |
| **Float** | Gentle up/down floating |
| **Rotate** | Continuous rotation loop |
| **Flash** | Blinking flash loop |
| **Neon Flicker** | Neon sign flicker effect |
| **Jitter** | Small random position jitter |
| **Wave** | Continuous wave motion |
| **Heartbeat** | Heartbeat-rhythm pulse |
| **Tilt** | Side-to-side tilt loop |
| **Zoom Pulse** | Alternating zoom in/out |
| **Color Shift** | Gradual color cycling |
| **Typewriter Loop** | Repeating character-by-character |
| **Glitch Loop** | Continuous glitch effect |
| **Stomp Loop** | Repeating stomp/impact |

### Animation Controls
| Control | Description |
|---------|-------------|
| **Duration** | Animation duration slider (0.1s - 5.0s typical) |
| **Speed / Easing** | Ease-in, Ease-out, Ease-in-out, Linear, Bounce, Elastic |
| **Preview** | Hover over thumbnail to preview animation |
| **Apply to all** | Apply animation to all text elements option |

---

## 8. AUTO CAPTIONS

### Auto Captions Panel (Left Panel > Auto captions)
AI-powered automatic speech recognition and subtitle generation.

#### Settings & Options
| Setting | Options/Description |
|---------|-------------------|
| **Language** | Auto-detect, English, Hindi, Spanish, French, German, Japanese, Korean, Chinese, Arabic, Portuguese, Italian, Russian, and 50+ more languages |
| **Detect language** | Auto-detection toggle — identifies spoken language |
| **Caption Style** | Pre-built subtitle style templates (font, color, background, position) |
| **Position** | Top, Middle, Bottom of frame |
| **Generate** button | Starts AI transcription process |

#### Caption Style Templates
Pre-designed subtitle appearance presets:
| Style Type | Visual Description |
|-----------|-------------------|
| **Classic White** | White text, black outline, bottom-center |
| **Bold Impact** | Large bold text, centered |
| **Highlight Word** | Active word highlighted in color |
| **Karaoke** | Word-by-word color fill as spoken |
| **Boxed** | Text in colored background boxes |
| **Minimal** | Small, subtle bottom text |
| **YouTube Style** | Standard YouTube caption appearance |
| **TikTok Style** | Bold centered text with pop-in animation |
| **Gradient** | Text with gradient color fills |
| **Outline Only** | Hollow outlined text |

#### Post-Generation Editing
| Feature | Description |
|---------|-------------|
| **Edit text** | Click any caption segment to edit wording |
| **Adjust timing** | Drag caption edges on timeline to adjust in/out points |
| **Split caption** | Split a caption segment into two |
| **Merge captions** | Merge adjacent caption segments |
| **Delete caption** | Remove individual caption segments |
| **Style override** | Change style of individual segments |
| **Font/Size/Color** | Full text property editing per segment |
| **Batch edit** | Apply style changes to all captions at once |

---

## 9. LOCAL CAPTIONS

### Local Captions Panel (Left Panel > Local captions)
Manual subtitle creation without AI — for users who have their own transcripts or want to manually type.

#### Features
| Feature | Description |
|---------|-------------|
| **Add caption** | Manually add a new subtitle segment at playhead |
| **Import SRT** | Import .srt subtitle file |
| **Import VTT** | Import .vtt (WebVTT) subtitle file |
| **Import ASS** | Import .ass (Advanced SubStation Alpha) file |
| **Export captions** | Export subtitles as .srt, .vtt, or .ass |
| **Timing editor** | Set start/end time for each caption line |
| **Bulk paste** | Paste full transcript and auto-split into segments |

---

## 10. TEXT TO SPEECH (TTS)

### TTS Panel (Right Panel > Text to speech tab)
Converts text content into AI-generated voiceover audio.

#### Voice Options
| Category | Voices Available |
|----------|-----------------|
| **Female** | Multiple female voice presets (warm, professional, energetic, calm, young) |
| **Male** | Multiple male voice presets (deep, neutral, authoritative, casual) |
| **Character** | Stylized character voices |
| **Language-specific** | Voices for different languages/accents (US English, British English, Hindi, etc.) |

#### TTS Controls
| Control | Description |
|---------|-------------|
| **Voice selector** | Dropdown to choose AI voice |
| **Speed** | Speech rate adjustment (0.5x - 2.0x) |
| **Pitch** | Voice pitch adjustment |
| **Generate** | Generate audio from text content |
| **Preview** | Preview voice before full generation |
| **Replace** | Replace existing text audio with TTS |

---

## 11. AI SUBTITLES / SMART CAPTIONS

### Smart Caption Features
| Feature | Description |
|---------|-------------|
| **Auto-sync** | AI syncs captions to speech timing |
| **Word-level timing** | Each word gets individual timestamp for karaoke effects |
| **Speaker detection** | Identifies different speakers (Pro feature) |
| **Punctuation** | Auto-adds punctuation and capitalization |
| **Filler word removal** | Option to auto-remove "um", "uh", "like" |
| **Profanity filter** | Option to censor profanity in captions |

---

## 12. TEXT TRACKING (Motion Track to Object)

### Tracking Tab (Right Panel > Tracking)
Pins text to a moving object in the video so it follows along.

| Control | Description |
|---------|-------------|
| **Track object** | Select object in frame to pin text to |
| **Track position** | Text follows object's X/Y movement |
| **Track scale** | Text scales with object's apparent size change |
| **Track rotation** | Text rotates with object |
| **Offset** | Position offset from tracked point |
| **Smoothing** | Smoothing factor for tracking jitter |
| **Analyze** button | Runs motion tracking analysis |

---

## 13. DEFAULT TEXT (Basic Text Box)

### Adding Default Text
**Location:** Left Panel > Default text

| Action | Description |
|--------|-------------|
| **Click "Default text"** | Adds a plain text box to canvas at center position |
| **Double-click text** | Enters edit mode — type/edit text content directly on canvas |
| **Drag to resize** | Resize handles on text bounding box |
| **Drag to reposition** | Move text anywhere on canvas |

### Default Text Starting Properties
| Property | Default Value |
|----------|--------------|
| Font | System default (appears to be a sans-serif) |
| Size | Auto (scales with canvas) |
| Color | White |
| Alignment | Center |
| Outline | None |
| Shadow | None |
| Background | None |
| Duration | Matches clip length or 5 seconds (adjustable on timeline) |

---

## 14. STICKERS PANEL — TEXT-ADJACENT FEATURES (f_0092)

### Sticker Categories with Text Overlap
The Stickers panel (separate from Text panel) contains text-related stickers:

| Category | Description |
|----------|-------------|
| **Text Sticker** | Pre-designed text-based decorative stickers |
| **Bubble** | Speech/thought bubbles (add your own text) |
| **Counter** | Animated number counters/countdowns |
| **Label/Badge** | Decorative labels and badges with text areas |
| **Social Media** | Like/subscribe/follow button overlays with text |

---

## 15. VIDEO 2 FRAMES — ADDITIONAL OBSERVATIONS (f_0094-f_0110)

### Sticker/Effects Library Context (Video 2)
Frames f_0094-f_0110 in Video 2 primarily show the Stickers panel categories being browsed, not the Text panel. The left panel shows the sticker category sidebar with:

#### Sticker Sub-Categories Visible
| Category | Visible Content |
|----------|----------------|
| **Trending** | Currently popular stickers — portrait overlays, effects |
| **Favorites** | User-saved stickers |
| **Animals** | Cat, dog, bunny stickers with animations |
| **Emoji** | Smiley/emoji-style animated stickers |
| **Love** | Heart and romance stickers |
| **Sad/Cool/Angry** | Emotion-based stickers |
| **Cute** | Kawaii/cute animated stickers |
| **Arrow** | Arrow indicators and pointers |
| **Shape** | Geometric shapes |
| **Food** | Food and beverage stickers |
| **Music** | Musical notes and instruments |
| **Social Media** | Platform-specific social icons |
| **Weather** | Weather-themed stickers |
| **Gesture** | Hand gesture stickers |
| **Sports** | Sports-related stickers |
| **Travel** | Travel/location stickers |
| **Decoration** | Decorative overlays |
| **Business Style** | Corporate/professional stickers |
| **Counter** | Number/countdown stickers |
| **Bubble** | Speech bubble overlays |
| **Mosaic** | Mosaic/pixelation effects |
| **Marker** | Highlighter/marker effects |
| **Body Effects** | AR body-tracking effect stickers |

#### Right Panel Properties (Video 2 — Export/Properties Context)
Frames show the right panel with export settings visible:
| Field | Value Observed |
|-------|---------------|
| **SHOT TS** | Filename field |
| **Format** | MP4, GIF, PNG options |
| **Stay in original location** | Toggle |
| **Resolution** | e.g. "Transcribe on" |
| **Preset** | Preset selection |
| **Frame rate** | "Timeline st" (timeline standard) |
| **Codec** | Codec selection |
| **Quality** | Quality setting |
| **Audio** | Audio export toggle |
| **Bitrate** | Bitrate control |
| **Modify** button | Opens advanced export |

---

## 16. WORKFLOW REFERENCE: TEXT CREATION PIPELINES

### Pipeline 1: Quick Subtitle (Auto Captions)
```
Text tab > Auto captions > Select language > Generate > Edit text > Apply style > Export
```

### Pipeline 2: Styled Title Card
```
Text tab > Text templates > Browse/search > Drag to timeline > Edit text > Customize in right panel > Set animation > Position
```

### Pipeline 3: ART Style Text
```
Text tab > Default text (add to canvas) > Right panel > Browse ART styles > Click to apply > Adjust size/position > Add animation
```

### Pipeline 4: Motion-Tracked Text
```
Text tab > Default text > Type content > Right panel > Tracking tab > Select object > Analyze > Adjust offset > Preview
```

### Pipeline 5: Text to Speech Integration
```
Text tab > Default text > Type script > Right panel > Text to speech tab > Select voice > Adjust speed/pitch > Generate > Review
```

---

## NOTES

1. **ART Style Library Scale**: The ART text style library is massive — 700-900+ styles observed across 14 frames of continuous scrolling. This is comparable to or exceeds dedicated title design tools. Styles cover metallic, neon, gradient, 3D, texture, retro, cartoon, horror, luxury, and multicolor categories.

2. **Pro-Gated Features**: AI Outline, Text to Speech, Motion Tracking, Auto Captions, and certain premium ART styles show Pro badges — these require CapCut Pro subscription.

3. **Template vs ART Style Distinction**: "Text templates" are pre-built animated text overlays (motion + style + layout). "ART styles" are visual treatments applied to any text (font styling only, no motion). Both are accessed from the right panel but serve different purposes.

4. **Font Download System**: Many fonts in the library require download before use (cloud icon indicator). Once downloaded, they become locally available for offline use.

5. **Caption Export Formats**: Auto-generated and manual captions can be exported as .srt, .vtt, or .ass files — critical for platform distribution (YouTube accepts .srt, TikTok burns in, Instagram requires hardcoded).

6. **Word-Level Karaoke**: Auto captions support word-level timing, enabling TikTok/Reels-style "highlight active word" caption effects that drive engagement.

7. **Cross-Reference**: For text animation keyframing beyond presets, see the Animation tab documentation in KF-01 (right panel inspector). Custom keyframe animation (position, scale, rotation, opacity over time) is available via the diamond keyframe button on the timeline toolbar.

---

## FILE: knowledge-base/KF-07-audio-music-intelligence.md

# KF-07 — Audio & Music Intelligence (Complete)

> Merged from: KF-08 AI Tools & Audio + KF-10 Music/SFX Mood Map
> Source: CapCut Desktop Pro (Mac)
> Timecode Format: HH:MM:SS:FF (30fps)
> Date indexed: 2026-03-10

---

## PART A: AI TOOLS & AUDIO

## 1. AI EDITOR FEATURES (Right Panel > AI Editor Tab)

The AI Editor tab appears in the right panel when a clip is selected on the timeline. It contains a scrollable list of AI-powered toggles and processing features.

### 1.1 AI Enhancement & Restoration

| Feature | Type | Sub-Settings | What It Does |
|---------|------|-------------|--------------|
| **Stabilize** | Toggle (on/off) | None visible | Applies AI-based video stabilization to reduce camera shake |
| **Enhance quality** | Toggle with checkbox | None visible | AI upscaling/enhancement of video quality (sharpness, clarity) |
| **Reduce image noise** | Toggle with checkbox | None visible | AI-based denoising to clean up grainy/noisy footage |
| **Optical flow** | Toggle with checkbox | None visible | AI-generated intermediate frames for smooth slow motion or frame rate conversion |

### 1.2 AI Smart Editing

| Feature | Type | Sub-Settings | What It Does |
|---------|------|-------------|--------------|
| **Smart scene cut** | Toggle/button | None visible | AI automatically detects scene changes and creates cuts |
| **Auto reframe** | Toggle | None visible | AI detects subject and automatically reframes for different aspect ratios (9:16, 1:1, etc.) |
| **Auto enhance** | Toggle | None visible | One-click AI improvement of overall clip look |
| **Highlight** | Toggle | None visible | AI identifies the best/most engaging moments in a clip |

### 1.3 AI Background & Subject

| Feature | Type | Sub-Settings | What It Does |
|---------|------|-------------|--------------|
| **Remove background** | Toggle with checkbox | None visible | AI-powered background removal (chroma-key-free) |
| **Remove flicker** | Toggle with checkbox | None visible | Removes flickering from footage (fluorescent lights, LED screens) |
| **Eye contact** | Toggle | None visible | AI adjusts subject's eyes to appear looking at camera |
| **Camera tracking** | Toggle | None visible | AI tracks camera movement for stabilization or effect application |

### 1.4 AI Color & Look

| Feature | Type | Sub-Settings | What It Does |
|---------|------|-------------|--------------|
| **Auto color correction** | Toggle | None visible | AI analyzes footage and applies automatic color/exposure correction |
| **Chroma key** | Toggle | Color picker, tolerance slider | AI-assisted green/blue screen keying with adjustable tolerance |

---

## 2. AI EFFECTS (Right Panel > Video Effects / AI Styles)

### 2.1 Velocity Effects
- Located under right panel effects section
- **Velocity effects** category with preset curve thumbnails
- Shows ~6-8 speed ramp presets as visual curve thumbnails
- Each preset shows a different velocity curve (ease in, ease out, pulse, etc.)
- Applied to clip for dynamic speed ramping without manual keyframing

### 2.2 AI Styles / Face Swap / Retouch (Right Panel Sub-tabs)

Right panel shows sub-tabs when clip selected: **Text** | **Face** | **Retouch/Makeup** | **Background**

#### Face Tab
| Feature | Sub-Settings | What It Does |
|---------|-------------|--------------|
| **Auto stroke** | Loading indicator | AI auto-detection of face for effect application |
| **Network** dropdown | List of face styles | Network/style selector for face processing |
| **Skin tones** | Row of ~8-10 skin tone circles (light to dark) | AI skin color matching/adjustment |
| **Skin makeup** section | Multiple controls | AI-driven cosmetic adjustments |
| **Single color** | Slider | Adjust single color channel on skin |
| **Depth control** | Slider | Control depth/intensity of face adjustments |

#### Retouch/Makeup Section (Expanded in Face Tab)
- **Reshape** section with face landmark grid of AI-generated face thumbnails
- Grid shows ~30+ face variations/presets
- Categories visible: preset face reshaping styles
- AI face reshaping with different aesthetic presets
- **Stickers** section below with decorative face stickers

#### Body/Figure Section
- Visible alongside Face controls
- Full body AI adjustments

### 2.3 AI Effects in Left Panel > Effects Tab

**Video Effects Categories** (left sidebar navigation):
- Video effects
- Trending
- Bling
- Showing Line
- Glowing
- Dream
- Superposition
- Blur
- PolyCut
- Portrait
- Party
- Sporty
- Trendy Mode
- Background
- Sticker/Emoji
- Page

**Effects sub-categories within each:**
- Each category shows grid of effect thumbnails (30-50+ per category)
- Effects are drag-and-drop onto timeline
- Right panel shows properties: Duration, Stay in original location, Transition, etc.

### 2.4 AI Face/Body Effects (Left Panel > Video Effects > Specific Categories)

**Face Effects observed in frames:**

| Category | Content | Count |
|----------|---------|-------|
| **Trending** | Mix of body/face/environment effects | 30+ thumbnails |
| **Bling** | Sparkle/shine effects on face/body | 20+ thumbnails |
| **Showing Line** | Contour/line effects | 15+ thumbnails |
| **Glowing** | Glow/aura effects | 20+ thumbnails |
| **Dream** | Dreamy/ethereal face filters | 20+ thumbnails |
| **Superposition** | Overlay/double exposure effects | 15+ thumbnails |
| **Blur** | Selective blur, bokeh, tilt-shift | 20+ thumbnails |
| **PolyCut** | Geometric face/body cuts | 10+ thumbnails |
| **Portrait** | Portrait-specific enhancements | 15+ thumbnails |
| **Background** | AI background replacement/effects | 20+ thumbnails |
| **Sticker/Emoji** | Cartoon face stickers, animal overlays | 12+ visible (pig, cat, bear, etc.) |

---

## 3. FACE DETECTION / SMART MEDIA (Left Panel > Media)

### 3.1 Face Detection System

Located in **Left Panel > Media tab** (or dedicated face panel). The system automatically scans all imported media and detects/groups faces.

**Properties panel (right side) when media selected:**

| Property | Value/Type | Description |
|----------|-----------|-------------|
| **EXIF TS** | Full file path displayed | Shows source file metadata path |
| **Res** | e.g., "1M, 1941 full" | Resolution info |
| **Stay in original location** | Toggle | Keep file in original folder |
| **Tolerance** | Setting | Face detection sensitivity |
| **Timeline name** | Text field | Custom name for timeline |
| **Transition** | Setting | Default transition behavior |
| **Keyframe** | Setting | Keyframe interpolation |
| **Duration** | e.g., "30 Slides" | Clip duration setting |

### 3.2 Face Categories (Left Panel Sidebar)

The face detection sidebar shows these organizational categories:

| Category | Description |
|----------|-------------|
| **Video effects** | Effects specifically for detected faces |
| **Tracking** | AI face/object tracking across frames |
| **Bling** | Sparkle/decoration effects for faces |
| **Showing Line** | Outline/contour effects |
| **Glowing** | Glow effects around faces |
| **Dream** | Dreamy filter effects |
| **Superposition** | Double exposure/overlay |
| **Blur** | Face-aware blur (subject isolation) |
| **PolyCut** | Geometric cutting effects |
| **Portrait** | Portrait enhancement modes |
| **Party** | Party/celebration themed effects |
| **Sporty** | Sport-themed effects |
| **Trendy Mode** | Trending social media effects |
| **Background** | Background manipulation |
| **Sticker** | Face-tracked stickers |
| **Page** | Page/layout effects |

### 3.3 Face Grouping

- AI auto-groups all detected faces from imported media
- Shows thumbnail grid of detected face crops
- Each face is a separate selectable entity
- Multiple faces from same person grouped together
- Visible face groups include: female faces (various angles), male faces, diverse ethnicities
- Face groups show 3-4 sample crops per person
- Allows filtering media by detected person

### 3.4 Smart Media Features

**Stickers/Emoji section (under face effects):**
- Cartoon animal heads: Pig, Cat, Bear, Mouse, Robot, etc.
- Labeled stickers visible: "Pig", "Kitty", "Bear", "Nerd 2", "Bronze"
- Total ~12+ face-tracked emoji/sticker options
- These track to detected face in real-time

**Trendy Node category:**
- Shows labeled effect thumbnails with names
- Visible effects: various named preset combinations
- Each thumbnail shows before/after or effect preview

---

## 4. AUDIO LIBRARY (Left Panel > Audio Tab)

### 4.1 Audio Tab Structure

The Audio tab in the left panel contains the music and sound effect library with these visible sections:

**Left Panel Navigation (Audio sub-categories):**

The audio library is accessed from the left panel. Based on frames showing the left panel with audio-related content, the following structure is visible:

| Section | Description |
|---------|-------------|
| **Music** | Licensed music tracks library |
| **Sound Effects** | SFX library |
| **Extracted** | Audio extracted from video clips |
| **Voiceover** | Recorded voiceovers |

### 4.2 Music Library Categories

Music tracks organized by mood/genre (visible from the content panels):
- Tracks are listed with title, duration, and preview play button
- Each track shows BPM and genre tags
- Drag-and-drop to timeline
- Pro badge on premium tracks

---

## 5. SOUND EFFECTS LIBRARY

### 5.1 Categories (from left panel navigation)

Sound effects are organized in categorical structure similar to music. Based on the effects panels and toolbar, sound effects include:
- Environmental sounds
- UI sounds
- Transition swooshes
- Impact hits
- Nature/ambient
- Human sounds (laughs, gasps, etc.)

---

## 6. AUDIO EDITING FEATURES

### 6.1 Audio Processing (accessible from right panel when audio clip selected or from toolbar)

**Top Toolbar Audio Tools** (visible in toolbar icons):
- Audio editing icons in the toolbar row
- Waveform display on timeline

**Right Panel Audio Controls:**

| Feature | Type | What It Does |
|---------|------|--------------|
| **Volume** | Slider | Master clip volume control |
| **Fade in** | Duration control | Audio fade-in duration |
| **Fade out** | Duration control | Audio fade-out duration |
| **Noise reduction** | Toggle/slider | AI-powered background noise removal |
| **Voice enhancement** | Toggle | AI voice clarity boost |
| **Beat sync** | Button/feature | AI detects music beats and syncs cuts to rhythm |
| **Audio separation** | Button | AI separates vocals from instrumentals (stem separation) |

### 6.2 AI Audio Features (from toolbar/menu)

| Feature | Access | What It Does |
|---------|--------|--------------|
| **Auto beat sync** | Toolbar or right-click | AI matches video cuts to audio beats automatically |
| **Vocal isolation** | Audio menu | AI-powered stem separation (vocals vs. instruments) |
| **Text to speech** | Text tab or menu | Converts typed text to spoken audio |
| **Auto captions** | Captions menu / toolbar | AI speech-to-text for automatic subtitle generation |
| **Sound sync** | Effects | Syncs visual effects to audio amplitude |

---

## 7. TEXT TO SPEECH VOICES

### 7.1 TTS System (accessed from Text tab)

**Text Tab Location:** Left panel top navigation shows **Text** section with sub-options:
- Default text
- Text templates
- Auto captions
- Local captions

**TTS Features:**
- Type text and convert to spoken audio
- Multiple voice options (male/female)
- Language selection
- Speed control
- Pitch adjustment
- Generated audio placed directly on timeline

---

## 8. AUTO CAPTION SETTINGS

### 8.1 Auto Captions (Left Panel > Text > Auto Captions)

Visible in frames as part of the Text panel navigation:

| Setting | Type | Options |
|---------|------|---------|
| **Language** | Dropdown | Multiple language support |
| **Auto captions** | Button | One-click generation |
| **Local captions** | Option | Offline/local processing option |

**Caption output features:**
- AI speech recognition converts spoken audio to text
- Captions auto-placed on timeline as text track
- Individual caption segments editable
- Timing auto-synced to speech
- Font, size, color, position all adjustable in right panel
- Caption style templates available

### 8.2 Caption Styling (Right Panel when caption selected)

Based on the right panel views showing text properties:
- Font selection
- Size, color, stroke, shadow controls
- Position (preset positions or manual drag)
- Animation in/out
- Background box toggle
- Opacity control

---

## 9. ADDITIONAL AI TOOLS (from Menu Bar & Toolbar)

### 9.1 Top Menu Bar AI-Related Items

Visible in the top menu bar across frames:
- **Media** | **Audio** | **Text** | **Stickers** | **Effects** | **Transitions** | **Captions** | **Filters** | **Adjustments** | **Templates** | **A-Action**

### 9.2 Toolbar AI Quick-Access Icons

The toolbar row below the menu shows quick-access icons for:
- Split
- Delete
- Speed
- Crop
- Transform
- Freeze frame
- Reverse
- AI tools (grouped)

### 9.3 Right Panel Tab System

When a clip is selected, the right panel shows tabs:
- **Video** | **Audio** | **Speed** | **Animation** | **AI Editor** | **AI Outline** (or similar)

Under **AI Editor** tab specifically:
- All features from Section 1 above
- Scrollable list of AI toggles

Under **AI Outline** tab:
- AI-generated outline/cutout features

---

## 10. EFFECTS PANEL — AI-SPECIFIC CATEGORIES (Left Panel > Effects)

### 10.1 Full Effects Category List (from left sidebar)

From frames f_0039-f_0042 showing the left panel effects list with icons:

| # | Effect Name | Icon Type |
|---|------------|-----------|
| 1 | Retouching Basics | Face icon |
| 2 | Trendy Content | Star icon |
| 3 | Template Media Generator (Batch) | Grid icon |
| 4 | Scene Detection | Eye icon |
| 5 | Auto Stabilization | Wave icon |
| 6 | SoFace | Face icon |
| 7 | Selfie.net | Camera icon |
| 8 | Cutout (AI) | Scissors icon |
| 9 | Remove Background for Chromakey Background | Layer icon |
| 10 | Remove Background For Chromakey Background (alternate) | Layer icon |
| 11 | AI Color | Palette icon |
| 12 | AI Swap | Arrows icon |
| 13 | Face Stickers/Assets | Sticker icon |
| 14 | Chroma Key/Chroma Fix | Key icon |
| 15 | AI-Generated Portraits | Portrait icon |
| 16 | Glamour Effects | Sparkle icon |
| 17 | AI Text/Caption Generator | Text icon |
| 18 | Art Style | Brush icon |
| 19 | Left Auto Improvement | Auto icon |
| 20 | Makeup & Retouch | Brush icon |
| 21 | Background Effects | Layer icon |
| 22 | AI Motion | Motion icon |
| 23 | Cartoon/Comics Filter | Star icon |
| 24 | Slow Motion/Speed Effects | Clock icon |
| 25 | Denoise AI | Clean icon |
| 26 | Tracking Movement Exp Finder | Target icon |

**Continued (f_0040-f_0042):**

| # | Effect Name | Icon Type |
|---|------------|-----------|
| 27 | AI Style | Palette icon |
| 28 | Reshaping Effects (via Chroma) | Shape icon |
| 29 | Body Reshape | Body icon |
| 30 | Happy Related/HTD | Heart icon |
| 31 | Close-Up | Zoom icon |
| 32 | Background Framing Body Finder | Frame icon |
| 33 | Colorpop Reference(TTD) | Color icon |
| 34 | Dynamic LR | Dynamic icon |
| 35 | System AI | Gear icon |
| 36 | Blur AI Window | Blur icon |
| 37 | 3D AI Objects | 3D icon |
| 38 | Cartoon Designs Over Texture | Texture icon |
| 39 | Design Retouch Studio | Brush icon |
| 40 | Smart Display Fx | Display icon |
| 41 | Direct Sketching Paper | Pencil icon |
| 42 | Smart Lighting | Light icon |
| 43 | Communication My Flip | Flip icon |
| 44 | Duplication | Copy icon |
| 45 | Slow Shot Fx | Clock icon |
| 46 | Distortion | Wave icon |
| 47 | AI Face Alter | Face icon |
| 48 | Other Extra Hu Filters | Filter icon |
| 49 | Old Style Montage | Film icon |
| 50 | Inspiring Deformation | Warp icon |
| 51 | Hair Style | Hair icon |
| 52 | Old Tick | Vintage icon |
| 53 | Tile Trick | Grid icon |

---

## 11. FILTERS LIBRARY (Right Panel > Filters)

### 11.1 Filter Categories (from Effects panel right side)

Visible in frames f_0223-f_0228 showing the filters/effects grid:

| Category Tab | Content |
|-------------|---------|
| **Trending** | Currently popular filters — large grid of thumbnails |
| **Portrait** | Portrait-optimized color grades and looks |
| **Film** | Cinematic film emulation filters (visible: warm orange/amber tones grid) |
| **Food** | Food photography color optimization |
| **Scenery** | Landscape/travel color grading |
| **Vlog** | Vlog-style casual color grades |
| **Retro** | Vintage/retro aesthetic filters |
| **Duotone** | Two-tone color effect filters |
| **Game** | Gaming aesthetic filters |
| **Black & White** | Monochrome filters |

**Filter count per category:** 50-100+ filter presets per category (visible from dense thumbnail grids)

### 11.2 Film Filter Sub-grid

Frame f_0226-f_0227 shows the "Film" category expanded:
- Dense grid of ~100+ orange/warm-toned filter thumbnails
- Each thumbnail shows the filter applied to the current frame
- Filters appear to include various film stock emulations
- Warm, amber, golden tones dominate this category

### 11.3 Scenery/Travel Filters

Frame f_0228 shows what appears to be the "Scenery" or alternate category:
- Grid of golden/warm outdoor-toned filter thumbnails
- Architectural and landscape optimized looks

---

## 12. COLOR ADJUSTMENT PANEL (Right Panel > Adjust Tab)

### 12.1 Color Correction Tools

Visible in frames f_0229-f_0232 showing the Adjust tab:

**Auto color correction toggle** at top of panel

**Manual adjustment sliders:**

| Control | Type | Description |
|---------|------|-------------|
| **Color bars (RGB)** | Visual indicator | RGB channel preview bars |
| **Exposure** | Slider | Overall exposure adjustment |
| **Contrast** | Slider | Contrast adjustment |
| **Highlights** | Slider | Highlight recovery/boost |
| **Shadows** | Slider | Shadow lift/crush |
| **Whites** | Slider | White point adjustment |
| **Blacks** | Slider | Black point adjustment |
| **Saturation** | Slider | Overall color saturation |
| **Vibrance** | Slider | Smart saturation (protects skin tones) |
| **Temperature** | Slider | White balance warm/cool |
| **Tint** | Slider | Green/magenta tint shift |
| **Sharpness** | Slider | Edge sharpening |
| **Vignette** | Slider | Edge darkening effect |

### 12.2 HSL (Hue, Saturation, Luminance)

Frame f_0230 shows:
- **Color circles** — row of ~8 colored dots (red, orange, yellow, green, cyan, blue, purple, magenta)
- Each selectable for per-color HSL adjustment
- **Saturation** slider
- **Brightness** slider
- "Apply to all" button at bottom

### 12.3 Curves

Frame f_0231 shows:
- **RGB Curve** — diagonal line on grid (adjustable via control points)
- **Individual channel curves** — separate R, G, B channel curve panels
- Green and red channel curves visible
- Standard Bezier curve interface with draggable points
- "Apply to all" button
- Reset option

### 12.4 Color Wheels

Frame f_0232 shows:
- **Color wheels** view with 4 wheels visible:
  - Shadows wheel
  - Midtones wheel
  - Highlights wheel
  - Global wheel (or Master)
- Each wheel shows: color ring + center point for adjustment
- Numeric readout below each wheel (labeled indicators)
- Standard 3-way color corrector layout

---

## 13. AI OUTLINE / AI STYLIZE (Right Panel Tab)

### 13.1 AI Effects Tab

Visible as a separate tab in the right panel: **AI Effects**

Frame f_0234-f_0236 show:
- **AI Effects** section header with description text
- Grid of AI style effect thumbnails (~8-12 visible)
- Each thumbnail shows a different AI artistic style applied to the current frame
- Styles include: sketch, oil paint, cartoon, anime, watercolor, etc.
- Click to apply the AI style to the selected clip
- Processing indicator during generation

---

## 14. SUMMARY TABLE — ALL AI FEATURES BY LOCATION

| Location | Feature | AI-Powered |
|----------|---------|-----------|
| Right Panel > AI Editor | Stabilize | Yes |
| Right Panel > AI Editor | Enhance quality | Yes |
| Right Panel > AI Editor | Reduce image noise | Yes |
| Right Panel > AI Editor | Optical flow | Yes |
| Right Panel > AI Editor | Smart scene cut | Yes |
| Right Panel > AI Editor | Auto reframe | Yes |
| Right Panel > AI Editor | Remove background | Yes |
| Right Panel > AI Editor | Remove flicker | Yes |
| Right Panel > AI Editor | Eye contact | Yes |
| Right Panel > AI Editor | Auto enhance | Yes |
| Right Panel > AI Editor | Highlight | Yes |
| Right Panel > AI Editor | Camera tracking | Yes |
| Right Panel > AI Editor | Auto color correction | Yes |
| Right Panel > AI Editor | Chroma key | Partial |
| Right Panel > Face tab | Face reshape (30+ presets) | Yes |
| Right Panel > Face tab | Skin tone adjustment | Yes |
| Right Panel > Face tab | AI Makeup | Yes |
| Right Panel > Face tab | Body reshape | Yes |
| Right Panel > Adjust | Auto color correction | Yes |
| Right Panel > Adjust | HSL per-color control | Manual |
| Right Panel > Adjust | Curves (RGB + individual) | Manual |
| Right Panel > Adjust | Color wheels (3-way) | Manual |
| Right Panel > AI Effects | AI art style transfer | Yes |
| Right Panel > Speed | Velocity curve presets | Partial |
| Left Panel > Effects | 50+ AI effect categories | Yes |
| Left Panel > Effects | Face-tracked stickers/emoji | Yes |
| Left Panel > Filters | 500+ filters across 10 categories | Partial |
| Left Panel > Text | Auto captions (speech-to-text) | Yes |
| Left Panel > Text | Text to speech | Yes |
| Left Panel > Audio | Beat sync | Yes |
| Left Panel > Audio | Audio separation (stem split) | Yes |
| Left Panel > Audio | Noise reduction | Yes |
| Left Panel > Audio | Voice enhancement | Yes |
| Left Panel > Media | Face detection & grouping | Yes |
| Toolbar | Auto beat sync | Yes |
| Toolbar | Speed ramping presets | Partial |

---

## 15. MEDIA PANEL — FACE DETECTION DETAIL

### 15.1 Detected Face Groups

From frames f_0125-f_0131, the face detection panel shows:

**Sidebar categories for face grouping:**
- Video effects
- Tracking
- Bling / Showing Line / Glowing / Dream / Superposition / Blur
- PolyCut
- Portrait
- Party / Sporty
- Trendy Mode
- Background
- Sticker/Emoji
- Page

**Face thumbnails visible:**
- Multiple female face crops (various angles: front, 3/4, profile)
- Multiple male face crops (business headshot style, passport style)
- Mixed ethnicity groupings
- Each group shows 3-8 face crops from different frames
- The system auto-clusters same person across different media files

### 15.2 Face-Tracked Sticker Library

From frame f_0133:
- Pig emoji (cartoon pink pig face)
- Cat/Kitty emoji
- Bear emoji
- Robot face
- Nerd glasses
- Bronze/metallic face
- Various cartoon animal heads
- Total ~12 face-tracked 3D stickers
- All track to detected face position in real-time during playback

---

*Knowledge file generated from CapCut Desktop Pro (Mac) screen recording analysis.*
*Source frames: dense-v1/f_0001-f_0012, f_0035-f_0045; dense-v2/f_0120-f_0140, f_0220-f_0236*

---

## PART B: MUSIC / SFX MOOD-BPM MAPPING

## 1. MUSIC MOOD MAP — Energy Tiers by BPM

### 1.1 HIGH ENERGY (120+ BPM)

| Genre/Style | BPM Range | Mood Tags | Primary Use Cases |
|-------------|-----------|-----------|-------------------|
| EDM / House | 125-130 | Hype, euphoric, party | Product launches, event recaps, brand hype reels |
| Trap / Hard Trap | 130-160 | Aggressive, dark, powerful | Sneaker drops, automotive, streetwear, flexes |
| Drum & Bass | 160-180 | Intense, chaotic, urgent | Action sports, extreme montages, gaming highlights |
| Pop-Punk / Rock | 140-180 | Rebellious, raw, energetic | Unboxing reveals, challenge videos, BTS chaos |
| Hyperpop | 150-180 | Glitchy, maximalist, chaotic | Meme edits, irony-coded content, Gen Z aesthetic |
| Phonk / Drift Phonk | 130-160 | Dark, bass-heavy, menacing | Car edits, gym content, sigma grindset, dark aesthetic |
| Future Bass | 120-140 | Uplifting, euphoric, bright | Travel montages, motivational, graduation, milestone |

**Editing behavior at 120+ BPM:**
- Cut frequency: every 1-2 beats (00:00:00:15 to 00:00:01:00 per shot)
- Zoom punches land on every downbeat
- Text appears/disappears on 8th notes
- Speed ramps sync to build-up sections
- Maximum visual density — layers, overlays, effects all active

### 1.2 MEDIUM ENERGY (90-120 BPM)

| Genre/Style | BPM Range | Mood Tags | Primary Use Cases |
|-------------|-----------|-----------|-------------------|
| Pop / Indie Pop | 100-120 | Feel-good, catchy, warm | Lifestyle vlogs, day-in-the-life, brand storytelling |
| Hip-Hop / Boom Bap | 85-100 | Confident, smooth, street | Fashion lookbooks, talking head intros, product reviews |
| R&B / Neo-Soul | 90-110 | Sensual, smooth, intimate | Beauty tutorials, skincare routines, luxury unboxing |
| Afrobeats | 100-120 | Groovy, warm, rhythmic | Dance content, cooking, cultural content, summer edits |
| Reggaeton | 90-100 | Bouncy, tropical, club | Travel, nightlife, party recap, tropical brand content |
| Indie Rock | 100-120 | Authentic, raw, nostalgic | Documentary b-roll, startup stories, maker content |
| Synthwave / Retrowave | 100-120 | Nostalgic, neon, futuristic | Tech reviews, retro edits, product reveals with 80s aesthetic |

**Editing behavior at 90-120 BPM:**
- Cut frequency: every 2-4 beats (00:00:01:00 to 00:00:02:20 per shot)
- Smooth transitions (dissolves, slides) preferred over hard cuts
- Text animations breathe — ease-in/ease-out on 2-beat cycles
- Speed ramps used sparingly — one per 8-bar section max
- Medium visual density — clean compositions, controlled layering

### 1.3 LOW ENERGY (60-90 BPM)

| Genre/Style | BPM Range | Mood Tags | Primary Use Cases |
|-------------|-----------|-----------|-------------------|
| Lo-fi Hip-Hop | 70-85 | Chill, nostalgic, cozy | Study with me, cafe vlogs, aesthetic compilations |
| Downtempo / Chillhop | 60-80 | Relaxed, mellow, introspective | Morning routines, journaling, slow living |
| Jazz / Smooth Jazz | 70-90 | Sophisticated, warm, classy | Food plating, luxury brand, wine/spirits, fine dining |
| Classical Piano | 60-80 | Elegant, emotional, pure | Wedding content, memorial, milestone, emotional reveal |
| Acoustic Guitar | 70-90 | Warm, intimate, organic | DIY tutorials, home tours, personal storytelling |
| Ambient Pop | 65-85 | Dreamy, soft, ethereal | Fashion film, beauty, skincare ASMR, slow-motion hero |
| Soul / Gospel | 70-85 | Warm, uplifting, deep | Motivational, community stories, brand purpose content |

**Editing behavior at 60-90 BPM:**
- Cut frequency: every 4-8 beats (00:00:02:20 to 00:00:08:00 per shot)
- Long holds on hero shots — let frames breathe
- Fade transitions, slow dissolves (00:00:01:00+ duration)
- Text: slow fade-in, hold, slow fade-out — never snap on/off
- Minimal visual density — negative space is the feature
- Speed ramps only as slow motion (40-60% speed)

### 1.4 AMBIENT / ATMOSPHERIC (Variable BPM)

| Genre/Style | BPM Range | Mood Tags | Primary Use Cases |
|-------------|-----------|-----------|-------------------|
| Drone / Pad Textures | No fixed BPM | Vast, cosmic, meditative | Aerial landscape, space/tech, brand world intros |
| Dark Ambient | No fixed BPM | Ominous, suspenseful, eerie | True crime, horror, cybersecurity, exposing content |
| Nature Soundscape | No fixed BPM | Organic, peaceful, raw | Eco/sustainability, travel, wellness, retreat |
| Cinematic Score | 40-80 (variable) | Epic, emotional, sweeping | Hero brand films, documentary, keynote openers |
| Glitch / IDM | Variable | Broken, digital, experimental | Tech art, AI-related content, glitch aesthetic edits |
| Minimal Electronic | 60-100 | Clean, modern, clinical | SaaS product demos, fintech, architecture, design |
| Field Recordings | No fixed BPM | Documentary, raw, authentic | Documentary, street photography, journalism |

**Editing behavior for ambient:**
- No beat-synced cuts — cuts are motivated by visual narrative
- Transition duration: 00:00:01:15 to 00:00:03:00 (slow crossfades)
- Text appears letter-by-letter or with slow reveal masks
- Pacing driven by breath/emotion, not rhythm
- Effects: film grain, light leaks, color shifts over time
- Holds of 00:00:05:00 to 00:00:15:00 on a single shot are normal

---

## 2. MUSIC-TO-EDITING STYLE MAPPING

### 2.1 Editing Mode Definitions

| Mode | Description | Target Length | Platform |
|------|-------------|---------------|----------|
| **Viral** | Hook-first, fast cuts, scroll-stopping | 00:00:07:00 to 00:00:30:00 | TikTok, Reels, Shorts |
| **Cinematic** | Widescreen, slow reveals, emotional arc | 00:00:30:00 to 00:05:00:00 | YouTube, brand film |
| **Documentary** | Narrative-driven, interviews + b-roll | 00:02:00:00 to 00:15:00:00 | YouTube, broadcast |
| **Meme** | Absurdist, ironic, speed-shifted | 00:00:03:00 to 00:00:15:00 | TikTok, Twitter |
| **Aesthetic** | Color-first, slow, mood-over-message | 00:00:15:00 to 00:01:00:00 | Instagram, Pinterest |
| **Minimal** | Clean, single-subject, design-forward | 00:00:10:00 to 00:01:00:00 | Product, SaaS, portfolio |

### 2.2 Mode-to-Music Pairing Matrix

| Editing Mode | Best Music Tier | Top Genres | BPM Sweet Spot | Avoid |
|-------------|----------------|------------|----------------|-------|
| **Viral** | High Energy | Trap, Phonk, EDM, Hyperpop | 128-150 | Ambient, Classical, Jazz |
| **Cinematic** | Low / Ambient | Cinematic Score, Orchestral, Dark Ambient | 60-80 or variable | Trap, Hyperpop, Reggaeton |
| **Documentary** | Low / Medium | Acoustic, Minimal Electronic, Piano | 70-100 | EDM, Phonk, Hyperpop |
| **Meme** | High / Ironic Low | Hyperpop, 8-bit, Phonk, Classical (ironic) | Any — mismatch is the joke | Smooth Jazz, R&B, Ambient Pop |
| **Aesthetic** | Low / Ambient | Lo-fi, Ambient Pop, Shoegaze, Downtempo | 65-90 | Trap, Drum & Bass, Rock |
| **Minimal** | Low / Medium | Minimal Electronic, Ambient, Synthwave | 80-110 | Phonk, Hyperpop, Drum & Bass |

### 2.3 Music Entry Points by Video Structure

| Video Moment | Music Action | Timing |
|-------------|-------------|---------|
| **Cold open / Hook** | Start at chorus or drop — never at intro | 00:00:00:00 (frame 1) |
| **Context / Setup** | Verse section — lower energy, builds | After hook (00:00:03:00 to 00:00:07:00) |
| **Value delivery** | Instrumental or low-vocal section | Mid-video — lets narration breathe |
| **Climax / Reveal** | Drop or chorus peak | Sync to the single most important visual |
| **CTA / Outro** | Energy dip or fade-out | Final 00:00:03:00 to 00:00:05:00 |

---

## 3. SOUND EFFECTS VOCABULARY

### 3.1 Impact Sounds

| SFX Type | Description | Duration Range | Intensity | When to Use |
|----------|-------------|---------------|-----------|-------------|
| **Whoosh** | Fast air movement, directional | 00:00:00:08 to 00:00:00:20 | Medium-High | Fast camera moves, swipe transitions, object fly-ins |
| **Hit / Punch** | Sharp percussive impact | 00:00:00:03 to 00:00:00:10 | High | Text slams, hard cuts, stat reveals, emphasis |
| **Bass Drop** | Deep sub-frequency thud | 00:00:00:15 to 00:00:01:15 | Very High | Reveals, logo drops, climax moments, before/after |
| **Slam** | Heavy impact with resonance | 00:00:00:08 to 00:00:00:25 | Very High | Door close transitions, title cards, final statements |
| **Thud** | Dull, weighty impact | 00:00:00:05 to 00:00:00:15 | Medium | Subtle emphasis, product placement on surface |
| **Boom** | Explosive low-end burst | 00:00:00:20 to 00:00:02:00 | Very High | Epic reveals, cinematic title, chapter markers |
| **Glitch Hit** | Digital distortion impact | 00:00:00:03 to 00:00:00:12 | Medium-High | Tech content, error moments, data reveals |

### 3.2 Transition Sounds

| SFX Type | Description | Duration Range | Intensity | When to Use |
|----------|-------------|---------------|-----------|-------------|
| **Swoosh** | Smooth directional pass | 00:00:00:10 to 00:00:01:00 | Low-Medium | Scene changes, slide transitions, topic shifts |
| **Riser** | Ascending pitch/frequency | 00:00:01:00 to 00:00:04:00 | Medium-High | Build-up before reveals, tension, anticipation |
| **Reverse Cymbal** | Reversed crash cymbal swell | 00:00:01:00 to 00:00:03:00 | Medium | Pre-drop transitions, section endings |
| **Swell** | Gradual volume/frequency build | 00:00:02:00 to 00:00:06:00 | Low-Medium | Long build-ups, documentary scene transitions |
| **Tape Stop** | Decelerating warble to silence | 00:00:00:10 to 00:00:01:00 | Medium | Pause moments, record scratch effect, joke beats |
| **Vinyl Scratch** | Record needle scratch | 00:00:00:08 to 00:00:00:20 | Medium | Topic pivots, "wait what?" moments, meme beats |
| **Warp / Morph** | Pitch-shifting transformation | 00:00:00:15 to 00:00:01:15 | Medium | Time jumps, flashbacks, before/after transitions |

### 3.3 UI / Notification Sounds

| SFX Type | Description | Duration Range | Intensity | When to Use |
|----------|-------------|---------------|-----------|-------------|
| **Click** | Sharp, clean finger click | 00:00:00:02 to 00:00:00:05 | Low | Button presses, list item reveals, menu navigation |
| **Pop** | Round, bubbly burst | 00:00:00:03 to 00:00:00:08 | Low | Text pop-on, bullet points, icon appearances |
| **Ding** | Clear bell tone | 00:00:00:05 to 00:00:00:15 | Low-Medium | Notifications, checkmarks, correct answers, tips |
| **Typing** | Keyboard clatter | 00:00:00:05 to 00:00:03:00 | Low | Text reveal (typewriter style), coding screens |
| **Notification Chime** | Phone/app notification | 00:00:00:08 to 00:00:00:20 | Low | Social proof (likes, comments), message mockups |
| **Beep** | Single electronic tone | 00:00:00:02 to 00:00:00:06 | Low | Censoring, scanning, tech interface |
| **Swipe** | Short finger-on-glass sound | 00:00:00:05 to 00:00:00:12 | Low | Screen recordings, app demos, phone mockups |

### 3.4 Ambient / Environmental Sounds

| SFX Type | Description | Duration Range | Intensity | When to Use |
|----------|-------------|---------------|-----------|-------------|
| **Room Tone** | Subtle indoor air/silence | 00:00:05:00 to continuous | Very Low | Fill dead air between narration, interview gaps |
| **City Traffic** | Urban background hum | 00:00:05:00 to continuous | Low | Street footage, outdoor vlogs, urban establishing |
| **Crowd Murmur** | Indistinct human chatter | 00:00:05:00 to continuous | Low-Medium | Event recaps, restaurant scenes, market footage |
| **Rain** | Rainfall (light to heavy) | 00:00:05:00 to continuous | Low | Mood setting, cozy aesthetic, melancholy overlay |
| **Wind** | Air movement (soft to harsh) | 00:00:05:00 to continuous | Low-Medium | Outdoor landscape, drone shots, isolation feeling |
| **Ocean / Waves** | Sea ambience | 00:00:05:00 to continuous | Low | Beach content, meditation, travel, calm transitions |
| **Fire / Crackling** | Campfire or fireplace | 00:00:05:00 to continuous | Low | Cozy content, ASMR, winter aesthetic, warmth |
| **Birds / Nature** | Forest/garden atmosphere | 00:00:05:00 to continuous | Very Low | Morning routines, garden content, wellness |

### 3.5 Comedy / Meme Sounds

| SFX Type | Description | Duration Range | Intensity | When to Use |
|----------|-------------|---------------|-----------|-------------|
| **Cartoon Boing** | Springy bounce | 00:00:00:05 to 00:00:00:15 | Low-Medium | Physical comedy, bouncing objects, exaggeration |
| **Fail Horn** | Sad trombone (wah wah) | 00:00:00:20 to 00:00:01:15 | Medium | Fail moments, bad takes, ironic reveals |
| **Vine Boom** | Deep bass boom (meme classic) | 00:00:00:05 to 00:00:00:15 | High | Dramatic zoom-ins, absurd emphasis, sigma edits |
| **Bruh** | Low-pitched "bruh" | 00:00:00:10 to 00:00:00:20 | Medium | Reaction content, disbelief, meme commentary |
| **Airhorn** | Loud horn blast | 00:00:00:10 to 00:00:01:00 | Very High | Hype moments (ironic or genuine), MLG-style edits |
| **Record Scratch** | Abrupt stop + scratch | 00:00:00:15 to 00:00:00:25 | Medium | "You're probably wondering..." freeze frames |
| **Fart / Wet Sound** | Gross-out effect | 00:00:00:05 to 00:00:00:15 | Low | Irony-coded humor only. Never in brand content |
| **Emotional Damage** | Voice clip meme | 00:00:00:15 to 00:00:01:00 | Medium | Roast content, callout moments, ratio culture |

---

## 4. SFX-TO-EDITING ACTION MAPPING

### 4.1 Visual Action → Sound Pairing

| Editing Action | Primary SFX | Secondary SFX | Layer With |
|---------------|-------------|---------------|------------|
| **Hard cut** | Hit / Punch | Glitch Hit | — |
| **Zoom in (fast)** | Whoosh (short) | Vine Boom (if meme) | Camera shake |
| **Zoom out** | Reverse Whoosh | Swell (subtle) | — |
| **Slide transition** | Swoosh | — | — |
| **Wipe transition** | Swoosh (directional match) | — | — |
| **Dissolve / Fade** | Nothing OR subtle swell | — | Music handles it |
| **Text appear (snap)** | Pop | Click | — |
| **Text appear (slam)** | Hit / Slam | Bass Drop | Screen shake |
| **Text appear (type)** | Typing SFX | — | — |
| **Logo reveal** | Bass Drop + Reverse Cymbal | Boom | Riser (pre-reveal) |
| **Beat drop moment** | Bass Drop | Boom | Full music drop |
| **Scene change** | Swoosh / Riser tail | Warp | — |
| **Speed ramp (fast→slow)** | Riser → Bass Drop | Tape Stop | — |
| **Speed ramp (slow→fast)** | Swell → Whoosh | — | — |
| **Freeze frame** | Tape Stop / Record Scratch | Vinyl Scratch | Music cuts out |
| **Split screen appear** | Double Pop | Swoosh × 2 | — |
| **Counter / Number tick** | Click (per digit) | Ding (on final) | — |
| **Before/After reveal** | Riser → Slam | Swoosh → Hit | — |
| **Product placement** | Thud (subtle) | Pop | — |
| **End card / Subscribe** | Ding / Chime | Pop | — |

### 4.2 SFX Layering Rules

**Rule 1: Never stack more than 3 SFX on a single frame.**
- Primary: the action sound (whoosh, hit)
- Secondary: the tail/resonance (reverb, sub)
- Tertiary: ambient continuity underneath

**Rule 2: SFX volume hierarchy.**

| Layer | Volume Relative to Music | Example |
|-------|------------------------|---------|
| Music bed | 0 dB (reference) | Background track |
| Voiceover / Dialog | +3 to +6 dB above music | Narration |
| Primary SFX | 0 to +3 dB above music | Whoosh on transition |
| Ambient bed | -12 to -18 dB below music | Room tone, city hum |
| UI sounds | -6 to -3 dB below music | Click, pop, ding |

**Rule 3: SFX must match transition duration.**
- If transition = 00:00:00:15 (15 frames), the swoosh must peak at frame 8 and tail to frame 15
- If transition = 00:00:01:00, use a longer swoosh/swell, not a short one stretched

**Rule 4: Comedy SFX only in Meme and Viral modes.**
- Vine Boom, Fail Horn, Airhorn have zero place in Cinematic, Documentary, Aesthetic, or Minimal modes
- Exception: ironic use in Viral mode for brands targeting Gen Z

---

## 5. BEAT SYNC GUIDE

### 5.1 BPM-to-Cut Frequency Table

| BPM | Beat Duration | Recommended Cut Frequency | Cuts Per 30 Seconds | Best For |
|-----|-------------|--------------------------|---------------------|----------|
| 60 | 00:00:01:00 | Every 4 beats (00:00:04:00) | ~8 cuts | Cinematic, Documentary |
| 80 | 00:00:00:23 | Every 2-4 beats (00:00:01:15 to 00:00:03:00) | ~10-15 cuts | Aesthetic, Lo-fi |
| 100 | 00:00:00:18 | Every 2 beats (00:00:01:06) | ~17 cuts | Lifestyle, Vlog |
| 120 | 00:00:00:15 | Every 1-2 beats (00:00:00:15 to 00:00:01:00) | ~20-30 cuts | Pop content, Product |
| 140 | 00:00:00:13 | Every 1 beat (00:00:00:13) | ~35 cuts | Fast-paced Viral |
| 160 | 00:00:00:11 | Every 1 beat OR every 2 beats | ~27-40 cuts | Extreme — DnB, gaming |

**Conversion formula:** Beat duration in frames = (30fps x 60sec) / BPM = 1800 / BPM

### 5.2 On-Beat vs Off-Beat Placement

| Technique | What It Means | When to Use | Feel |
|-----------|--------------|-------------|------|
| **On-beat cuts** | Cut lands exactly on the kick/snare | Default for all beat-synced editing | Tight, locked, professional |
| **Off-beat cuts** | Cut lands between beats (on the "and") | Syncopated feels, jazzy edits, R&B | Groovy, unexpected, musical |
| **Pre-beat anticipation** | Cut 2-3 frames BEFORE the beat | Creates visual "pull" into the beat | Dynamic, forward-driving |
| **Post-beat delay** | Cut 2-3 frames AFTER the beat | Creates weight, lets beat hit first | Heavy, impactful, dramatic |

**CapCut implementation:**
- Use Auto Beat Sync (Left Panel > Audio > Beat sync) to auto-detect beats
- Yellow beat markers appear on audio waveform in timeline
- Snap cuts to these markers for on-beat editing
- For off-beat: manually offset by 00:00:00:02 to 00:00:00:03

### 5.3 Build-Up → Drop Patterns

The most powerful audio-visual sync technique. Every music track with a drop follows this structure:

```
SONG STRUCTURE MAP (8-bar sections at 128 BPM = ~15 seconds each)

[INTRO]           00:00:00:00 — Minimal. Establish mood.
                   Editing: slow reveals, single wide shots, text fades in.

[VERSE 1]         ~00:00:15:00 — Energy building. Melodic.
                   Editing: medium pace cuts, introduce subject/story.

[PRE-DROP / RISER] ~00:00:30:00 — Tension. Rising pitch. Snare rolls.
                   Editing: ACCELERATE cut frequency. Quick flashes.
                   Speed ramps compress time. Text builds word-by-word.
                   Visual density increases every 2 beats.

[DROP]            ~00:00:45:00 — MAXIMUM ENERGY. Full instrumentation.
                   Editing: HARDEST cuts, zooms, shake, effects.
                   This is where the hero shot / reveal / product lives.
                   Every beat = a new visual. Maximum SFX layering.

[BREAKDOWN]       ~00:01:00:00 — Pull back. Melodic, vocals return.
                   Editing: slow down. Longer holds. Let viewer breathe.
                   Context, explanation, softer b-roll.

[DROP 2]          ~00:01:15:00 — Second wave, often bigger.
                   Editing: even more aggressive than Drop 1.
                   New footage or same with different treatment.

[OUTRO]           ~00:01:30:00 — Energy tapering.
                   Editing: slow dissolves, end card, CTA.
```

### 5.4 BPM and Speed Ramp Sync

| Speed Ramp Type | Audio Cue | Execution |
|----------------|-----------|-----------|
| **Slow-mo into beat** | Riser building | Apply 30-50% speed during riser. Snap to 100% on drop frame |
| **Fast-mo into freeze** | Build-up → silence | Apply 200-400% speed during build. Freeze frame on silence hit |
| **Pulse** | Kick drum pattern | 100% on kick → 60% between kicks → 100% on next kick |
| **Whip pan** | Swoosh SFX + beat | 400% speed for 00:00:00:06 frames centered on beat |
| **Reverse-to-forward** | Reverse cymbal → drop | Play clip in reverse during riser. Forward on drop |

### 5.5 Cut Rhythm Patterns (Musical Notation Style)

```
PATTERN 1: Four-on-the-floor (EDM, House)
Beat:  1 . . . 2 . . . 3 . . . 4 . . .
Cut:   X               X               (cut every 2 beats)
Or:    X       X       X       X       (cut every beat — fast)

PATTERN 2: Boom-bap (Hip-Hop)
Beat:  1 . . . 2 . . . 3 . . . 4 . . .
Cut:   X           X       X           (syncopated — kick, snare, kick)

PATTERN 3: Waltz / Triple (Cinematic)
Beat:  1 . . 2 . . 3 . . 1 . .
Cut:   X                   X           (cut every full measure)

PATTERN 4: Drill / Trap
Beat:  1 . . . 2 . . . 3 . . . 4 . . .
Hi-hat: x x x x x x x x x x x x x x x x
Cut:   X   X       X   X       (follows hi-hat rolls, irregular)

PATTERN 5: Off-beat / Reggae-influenced
Beat:  1 . . . 2 . . . 3 . . . 4 . . .
Cut:       X       X       X       X   (cuts on the "and" — never on downbeat)
```

---

## 6. EDITING MODE CHEAT SHEETS

### 6.1 Viral Mode Audio Blueprint

```
AUDIO STACK:
- Music: 120-150 BPM (Trap, Phonk, EDM, Hyperpop)
- SFX density: HIGH (every 00:00:01:00 to 00:00:02:00)
- Ambient: NONE
- Voice: Direct-to-camera or trending audio clip

TIMELINE:
00:00:00:00-00:00:00:03  Hook visual + bass hit (no music yet OR drop instantly)
00:00:00:03-00:00:00:15  Setup — verse section, medium cuts
00:00:00:15-00:00:00:22  Build — riser, accelerating cuts, text stacking
00:00:00:22-00:00:00:30  Payoff — drop, fastest cuts, hero shot, CTA

SFX MAP:
- Frame 1: Bass drop or whoosh
- Every text appear: Pop
- Every transition: Swoosh
- Climax: Slam + Bass Drop
```

### 6.2 Cinematic Mode Audio Blueprint

```
AUDIO STACK:
- Music: 60-80 BPM OR ambient score (no fixed BPM)
- SFX density: LOW (every 00:00:05:00 to 00:00:15:00)
- Ambient: Room tone / environment underneath at -15 dB
- Voice: Narration with -3 dB music duck

TIMELINE:
00:00:00:00-00:00:05:00  Establishing — ambient only, no music
00:00:05:00-00:00:15:00  Music enters — single instrument, minimal
00:00:15:00-00:00:45:00  Build — strings/pads layer in, cuts on phrase endings
00:00:45:00-00:01:00:00  Climax — full orchestration, widest shots
00:01:00:00-00:01:30:00  Resolution — instruments drop out one by one, fade

SFX MAP:
- Transitions: Swell or nothing (let music carry)
- Reveals: Single bass drop, used ONCE maximum
- Ambient: continuous nature/city bed
- Avoid: Whooshes, pops, clicks, any UI sounds
```

### 6.3 Documentary Mode Audio Blueprint

```
AUDIO STACK:
- Music: 70-100 BPM (Acoustic, Minimal Electronic, Piano)
- SFX density: VERY LOW (functional only)
- Ambient: Location audio is king — preserve original audio
- Voice: Interview audio primary; music ducks -12 dB under speech

TIMELINE:
Music enters and exits between interview segments.
Never compete with speech. Music = emotional bridge between talking heads.

SFX MAP:
- Text/lower thirds: subtle pop or nothing
- Transitions between interviews: short music swell (00:00:02:00)
- Chapter markers: single clean ding or tone
- Archival footage: add film projector ambient
- Data/stats on screen: subtle click per number
```

### 6.4 Meme Mode Audio Blueprint

```
AUDIO STACK:
- Music: ANY BPM — mismatch is intentional
- SFX density: MAXIMUM (every 00:00:00:15 to 00:00:01:00)
- Ambient: NONE (sterile = funnier)
- Voice: Trending audio clips, voice memos, AI TTS for irony

SFX MAP:
- Every zoom: Vine Boom
- Every fail: Fail Horn or "Bruh"
- Every flex: Airhorn
- Text slam: Slam + screen shake
- Freeze frame: Record Scratch + silence
- Absurd juxtaposition: Classical music + chaos visuals

RULES:
- More SFX = funnier (up to a point)
- Layer SFX that shouldn't go together
- Cut music abruptly mid-note for comedy
- Silence is a punchline — 00:00:01:00 of dead air before the joke lands
```

---

## 7. CAPCUT-SPECIFIC AUDIO WORKFLOW

### 7.1 CapCut Audio Feature → Editing Mode Mapping

| CapCut Feature (from KF-08) | Best Editing Mode | How to Use |
|-----------------------------|------------------|------------|
| **Auto Beat Sync** | Viral, Minimal | Auto-generates beat markers → snap all cuts to markers |
| **Audio Separation** | Documentary, Cinematic | Isolate vocals from music → layer custom score underneath |
| **Noise Reduction** | Documentary, Cinematic | Clean interview audio before mixing with music bed |
| **Voice Enhancement** | Documentary, Minimal | Boost voice clarity for talking-head content |
| **Sound Sync (effects)** | Viral, Meme | Visual effects react to audio amplitude in real-time |
| **Vocal Isolation** | Any with trending audio | Extract acapella → pair with custom beat |
| **Beat Markers** | All modes | Yellow markers on waveform = snap points for cuts |
| **Fade In/Out** | All modes | Audio clip edges — always fade, never hard start/stop |

### 7.2 Audio Track Stacking Order (Bottom to Top on Timeline)

```
TRACK 4 (top):   Voice / Narration / Dialog
TRACK 3:         SFX — impacts, transitions, UI sounds
TRACK 2:         Music — primary track
TRACK 1 (bottom): Ambient / Room tone / Environmental bed
```

### 7.3 Volume Automation Landmarks

| Video Event | Music Action | SFX Action |
|------------|-------------|------------|
| Narration starts | Duck to -12 dB (00:00:00:10 fade) | Pause all SFX |
| Narration ends | Rise to 0 dB (00:00:00:15 fade) | Resume SFX |
| Visual climax | Full volume, drop hits | Slam + Boom layered |
| Quiet moment | -6 dB, simpler arrangement | Nothing — silence breathes |
| End card | Fade to -inf over 00:00:02:00 | Single ding at CTA |

---

## 8. QUICK REFERENCE — MOOD WORD → AUDIO DECISION

When the AI Editing Director receives a mood keyword, this is the instant lookup:

| Mood Word | Music Genre | BPM | SFX Style | Editing Mode |
|-----------|------------|-----|-----------|-------------|
| Hype | Trap / EDM | 128-150 | Heavy impacts, whooshes | Viral |
| Chill | Lo-fi / Downtempo | 70-85 | Minimal — pops only | Aesthetic |
| Luxury | Jazz / Minimal Electronic | 80-100 | Subtle thuds, no comedy | Minimal |
| Dark | Phonk / Dark Ambient | 130+ or variable | Glitch hits, deep bass | Viral / Cinematic |
| Emotional | Piano / Orchestral | 60-80 | Almost none — music carries | Cinematic |
| Funny | Hyperpop / Classical (ironic) | Any | MAX — vine boom, fail horn | Meme |
| Professional | Minimal Electronic / Acoustic | 90-110 | Clean clicks, pops | Minimal / Documentary |
| Epic | Cinematic Score / DnB | Variable / 160+ | Booms, risers, bass drops | Cinematic |
| Nostalgic | Synthwave / Lo-fi / Acoustic | 85-110 | Vinyl scratch, tape artifacts | Aesthetic |
| Aggressive | Trap / Drill / Phonk | 130-160 | Hard hits, slams, glitch | Viral |
| Dreamy | Ambient Pop / Shoegaze | 65-85 | Reverbed pops, swells | Aesthetic |
| Playful | Pop / Afrobeats | 100-120 | Cartoon pops, boing | Viral (soft) |
| Suspenseful | Dark Ambient / Minimal | Variable | Risers, reverse cymbals | Documentary / Cinematic |
| Corporate | Minimal Electronic | 90-110 | Clean UI clicks only | Minimal |
| Raw | Boom Bap / Indie Rock | 85-110 | Minimal — let grit speak | Documentary |

---

*Knowledge file for AI Editing Director system. Cross-reference with KF-04 (Transitions) for transition-SFX pairing.*
*Timecodes: HH:MM:SS:FF at 30fps throughout.*

---

## FILE: knowledge-base/KF-09-effect-metadata-top150.md

# KF-09 — Effect Metadata: Top 108 Assets for AI Editing Director

> Source: Curated from KF-02 (All Effects: Video + Body), KF-03 (Transitions), KF-04 (Filters)
> Selection: Prioritized Trending/Hits categories, most versatile per category, covers all major editing scenarios
> Format: Semantic metadata per Section 22 of capcut-ai-director-brain.md
> Date: 2026-03-10
> Total entries: 108

---

# 1. TRANSITIONS (40 entries)

---

## 1.1 FLASH / LIGHT TRANSITIONS

```
Effect: White Flash
Category: Transitions → Trending / Overlay
Type: Full-frame white burst transition
Best use: Beat drops, dramatic reveals, high-energy scene changes, before/after reveals
Duration: 00:00:00:04 to 00:00:00:08 (4-8 frames)
Intensity: High
Mood: Energetic, explosive, punchy
Pair with: Bass hit sound effect, zoom punch, bright footage, beat-synced cuts
Avoid with: Slow emotional content, documentary, corporate, nighttime footage
```

```
Effect: Dark Flash
Category: Transitions → Trending
Type: Full-frame dark/black burst transition
Best use: Dramatic reveals, moody scene changes, dark-themed content, horror/thriller edits
Duration: 00:00:00:04 to 00:00:00:08 (4-8 frames)
Intensity: High
Mood: Dark, dramatic, intense, cinematic
Pair with: Low bass hit, dark footage, thriller content, nighttime scenes
Avoid with: Bright lifestyle content, comedy, cheerful mood
```

```
Effect: Flash
Category: Transitions → Light
Type: Clean white flash burst
Best use: Universal impact transition — beat drops, scene changes, emphasis moments
Duration: 00:00:00:04 to 00:00:00:10 (4-10 frames)
Intensity: High
Mood: Impactful, energetic, decisive
Pair with: Impact sound, zoom, camera shake, any high-energy moment
Avoid with: Relaxed pacing, ASMR, quiet content
```

```
Effect: Glare II
Category: Transitions → Trending / Light
Type: Lens glare with light bleed between scenes
Best use: Cinematic transitions, outdoor/bright scenes, fashion content, golden hour edits
Duration: 00:00:00:10 to 00:00:00:20 (10-20 frames)
Intensity: Medium
Mood: Cinematic, warm, polished, dreamy
Pair with: Warm filters, lens flare effects, outdoor footage, golden hour content
Avoid with: Dark/moody content, indoor low-light, horror
```

```
Effect: Heartwarming Flash
Category: Transitions → Light
Type: Soft warm-toned flash transition
Best use: Emotional moments, wedding content, romantic reveals, family videos
Duration: 00:00:00:08 to 00:00:00:15 (8-15 frames)
Intensity: Medium
Mood: Warm, emotional, tender, intimate
Pair with: Piano/string music, warm filters, soft footage, romantic body effects
Avoid with: Aggressive content, tech/gaming, corporate
```

## 1.2 BLUR / SMOOTH TRANSITIONS

```
Effect: Simple Blur
Category: Transitions → Blur
Type: Clean gaussian blur dissolve between scenes
Best use: Smooth scene changes, dreamy sequences, time passage, any content needing soft transitions
Duration: 00:00:00:10 to 00:00:00:20 (10-20 frames)
Intensity: Low
Mood: Smooth, gentle, professional, seamless
Pair with: Ambient music, lifestyle content, vlogs, talking heads
Avoid with: High-energy content, beat drops, aggressive edits
```

```
Effect: Radial Blur
Category: Transitions → Trending / Blur
Type: Blur radiating from center outward between scenes
Best use: Focus transitions, dramatic reveals, speed-to-stop moments, attention-centering
Duration: 00:00:00:08 to 00:00:00:18 (8-18 frames)
Intensity: Medium
Mood: Dynamic, focused, dramatic
Pair with: Zoom effects, whoosh sound, subject-centered shots
Avoid with: Multi-subject scenes, landscape wide shots
```

```
Effect: Blur Focus
Category: Transitions → Trending / Blur
Type: Rack-focus style blur shifting between scenes
Best use: Subject reveals, before/after, POV shifts, interview transitions
Duration: 00:00:00:12 to 00:00:00:20 (12-20 frames)
Intensity: Low-Medium
Mood: Professional, cinematic, polished
Pair with: Talking head content, product reveals, interview cuts
Avoid with: Fast-paced montage, meme content
```

```
Effect: Bubble Blur
Category: Transitions → Blur / Hits
Type: Soft bubble-shaped blur dissolve
Best use: Dreamy content, beauty/skincare, lifestyle vlogs, gentle scene changes
Duration: 00:00:00:12 to 00:00:00:22 (12-22 frames)
Intensity: Low
Mood: Soft, dreamy, airy, feminine
Pair with: Lo-fi music, pastel filters, beauty content, body effects like Soft Film
Avoid with: Aggressive content, masculine branding, corporate
```

## 1.3 CAMERA / MOTION TRANSITIONS

```
Effect: Shaky Inhale
Category: Transitions → Trending / Camera
Type: Camera shake with zoom-pull-in motion
Best use: Energy spikes, beat drops, dramatic moments, TikTok-style edits, hype content
Duration: 00:00:00:06 to 00:00:00:15 (6-15 frames)
Intensity: High
Mood: Energetic, chaotic, impactful, viral
Pair with: Bass hit, camera shake effect, fast-paced music, party effects
Avoid with: Corporate, documentary, calm content, accessibility-sensitive audiences
```

```
Effect: Swipe Left
Category: Transitions → Trending / Camera / Basic
Type: Horizontal swipe revealing next scene from right
Best use: Social media native feel, before/after, list content, casual scene changes
Duration: 00:00:00:06 to 00:00:00:12 (6-12 frames)
Intensity: Medium
Mood: Modern, casual, social-media-native
Pair with: Whoosh sound, social media content, tutorial/how-to, comparison shots
Avoid with: Cinematic/film content, formal presentations
```

```
Effect: Delay Zoom
Category: Transitions → Trending / Camera
Type: Delayed zoom-in transition between scenes
Best use: Emphasis moments, building anticipation, quote reveals, key statements
Duration: 00:00:00:10 to 00:00:00:20 (10-20 frames)
Intensity: Medium
Mood: Dramatic, building, anticipatory
Pair with: Riser sound, talking head emphasis, motivational content
Avoid with: Fast montage, scenes already at close-up
```

```
Effect: Rebound Zoom
Category: Transitions → Trending
Type: Zoom with elastic bounce-back between scenes
Best use: Fun reveals, product showcases, playful transitions, social media edits
Duration: 00:00:00:08 to 00:00:00:15 (8-15 frames)
Intensity: Medium-High
Mood: Playful, bouncy, energetic, fun
Pair with: Pop sound effect, colorful content, product reveals, lifestyle vlogs
Avoid with: Serious/corporate, emotional moments, sad content
```

```
Effect: Dive & Bounce
Category: Transitions → Trending / Camera / Hits
Type: Downward dive with bounce recovery
Best use: Energetic reveals, action content, sports edits, dance videos
Duration: 00:00:00:10 to 00:00:00:18 (10-18 frames)
Intensity: High
Mood: Dynamic, athletic, high-energy
Pair with: Impact sound, action footage, dance content, sports highlights
Avoid with: Static content, talking heads, slow pacing
```

```
Effect: Pull In
Category: Transitions → Camera
Type: Camera pull-in zoom transition
Best use: Subject reveals, storytelling focus, drawing attention to detail
Duration: 00:00:00:08 to 00:00:00:15 (8-15 frames)
Intensity: Medium
Mood: Focused, intentional, narrative
Pair with: Whoosh sound, talking head, product close-up, detail shots
Avoid with: Already zoomed-in content, wide establishing shots that need to breathe
```

## 1.4 GLITCH / DIGITAL TRANSITIONS

```
Effect: Snap Hack
Category: Transitions → Trending
Type: Digital snap with glitch distortion
Best use: Tech content, gaming edits, edgy branding, surprise moments, hacker aesthetic
Duration: 00:00:00:04 to 00:00:00:10 (4-10 frames)
Intensity: High
Mood: Edgy, digital, aggressive, futuristic
Pair with: Glitch sound effect, tech content, cyberpunk filters, neon effects
Avoid with: Organic/nature content, wedding, luxury brand, soft aesthetic
```

```
Effect: Comic Cut
Category: Transitions → Trending / Hits
Type: Comic-book style panel cut transition
Best use: Fun content, storytelling, recap sequences, manga/anime aesthetic edits
Duration: 00:00:00:06 to 00:00:00:12 (6-12 frames)
Intensity: Medium
Mood: Playful, comic, illustrated, fun
Pair with: Pop sound, comic effects, bold captions, colorful content
Avoid with: Cinematic/serious content, luxury branding, formal corporate
```

```
Effect: Signal Glitch 2
Category: Transitions → Trending
Type: TV signal interference glitch between scenes
Best use: Horror/thriller content, retro edits, error/malfunction moments, surprise transitions
Duration: 00:00:00:06 to 00:00:00:12 (6-12 frames)
Intensity: High
Mood: Unstable, eerie, retro-digital, chaotic
Pair with: Glitch sound, VHS effects, retro filters, horror content
Avoid with: Clean professional content, beauty, wedding
```

## 1.5 OVERLAY / CREATIVE TRANSITIONS

```
Effect: Black Fade
Category: Transitions → Classic / Overlay
Type: Fade to black and emerge into next scene
Best use: Scene endings, chapter breaks, time passage, intro/outro, emotional pauses
Duration: 00:00:00:15 to 00:00:01:00 (15-30 frames)
Intensity: Low
Mood: Deliberate, cinematic, pensive, classic
Pair with: Silence or ambient music, documentary, emotional beats, chapter endings
Avoid with: Fast-paced content, mid-section edits where momentum matters
```

```
Effect: Overlap Fade
Category: Transitions → Classic / Overlay
Type: Cross-dissolve with overlapping frames
Best use: Time passage, memory sequences, montage, documentary, emotional transitions
Duration: 00:00:00:15 to 00:00:01:00 (15-30 frames)
Intensity: Low
Mood: Reflective, nostalgic, smooth, editorial
Pair with: Soft music, voice-over, documentary content, photo montage
Avoid with: Fast-paced edits, comedy, meme content
```

```
Effect: Slice Reveal
Category: Transitions → Hits
Type: Sliced panel reveal between scenes
Best use: Product reveals, fashion content, before/after, stylish intros
Duration: 00:00:00:08 to 00:00:00:15 (8-15 frames)
Intensity: Medium
Mood: Stylish, modern, editorial, clean
Pair with: Whoosh sound, fashion/product content, clean filters, bold typography
Avoid with: Organic/raw content, handheld aesthetic, casual vlogs
```

```
Effect: Film Fade
Category: Transitions → Hits
Type: Analog film-style fade with slight grain
Best use: Cinematic edits, retro content, narrative films, vintage aesthetic
Duration: 00:00:00:12 to 00:00:00:24 (12-24 frames)
Intensity: Low
Mood: Cinematic, nostalgic, filmic, warm
Pair with: Retro filters, film grain effects, cinematic music, analog sound design
Avoid with: Modern/clean aesthetic, tech content, bright social media
```

```
Effect: Snap Rack
Category: Transitions → Hits / NEW
Type: Quick rack-focus snap between scenes
Best use: Fast reveals, interview cuts, dynamic talking heads, punchy edits
Duration: 00:00:00:04 to 00:00:00:10 (4-10 frames)
Intensity: Medium-High
Mood: Quick, professional, sharp, editorial
Pair with: Snap sound, talking head, fast-paced content, interview edits
Avoid with: Slow atmospheric content, long-form relaxed pacing
```

```
Effect: Pastel Motion
Category: Transitions → Trending / Light / Hits
Type: Soft pastel-colored motion dissolve
Best use: Beauty content, skincare, feminine branding, lifestyle, spring/summer aesthetic
Duration: 00:00:00:10 to 00:00:00:18 (10-18 frames)
Intensity: Low
Mood: Soft, pastel, feminine, delicate
Pair with: Pastel filters, beauty body effects, soft music, lifestyle content
Avoid with: Dark/moody content, masculine branding, aggressive energy
```

## 1.6 CREATIVE / SPECIALTY TRANSITIONS

```
Effect: Ripping Wipe
Category: Transitions → Trending
Type: Paper-tear ripping effect revealing next scene
Best use: Dramatic reveals, before/after transformations, storytelling pivots, surprise content
Duration: 00:00:00:08 to 00:00:00:15 (8-15 frames)
Intensity: Medium-High
Mood: Raw, dramatic, transformative, bold
Pair with: Paper tear sound, transformation content, makeover videos, reveal moments
Avoid with: Polished luxury content, minimal aesthetic
```

```
Effect: Dream Jitter
Category: Transitions → Trending
Type: Jittery shake with dreamy blur between scenes
Best use: Memory flashbacks, dream sequences, surreal content, music video transitions
Duration: 00:00:00:08 to 00:00:00:15 (8-15 frames)
Intensity: Medium
Mood: Dreamy, unstable, surreal, hypnotic
Pair with: Reverb sounds, dreamy filters, lo-fi music, ethereal body effects
Avoid with: Corporate, tutorial content, clean professional edits
```

```
Effect: Shake Snap
Category: Transitions → Trending / Camera
Type: Quick camera shake with snap-cut
Best use: Beat sync, action moments, dance videos, TikTok trends, quick cuts
Duration: 00:00:00:04 to 00:00:00:08 (4-8 frames)
Intensity: High
Mood: Snappy, rhythmic, viral, punchy
Pair with: Snap/click sound, beat-synced music, dance content, fast montage
Avoid with: Slow pacing, accessibility concerns, motion-sensitive audiences
```

```
Effect: Snow Cleaned
Category: Transitions → Trending / NEW
Type: Snow particle wipe clearing to next scene
Best use: Winter content, holiday edits, seasonal transitions, clean fresh-start reveals
Duration: 00:00:00:10 to 00:00:00:20 (10-20 frames)
Intensity: Low-Medium
Mood: Fresh, clean, wintry, festive
Pair with: Chime sound, winter filters, holiday content, cold-toned footage
Avoid with: Summer/tropical content, warm aesthetic
```

```
Effect: Burned Portal
Category: Transitions → Trending / Overlay
Type: Burning paper-edge portal revealing next scene
Best use: Fantasy/magical transitions, dramatic reveals, vintage-to-new, cinematic storytelling
Duration: 00:00:00:10 to 00:00:00:20 (10-20 frames)
Intensity: Medium-High
Mood: Mystical, dramatic, transformative, cinematic
Pair with: Fire crackle sound, cinematic content, fantasy edits, warm filters
Avoid with: Corporate/clean, tech content, minimal aesthetic
```

```
Effect: Sakura Breeze
Category: Transitions → Trending
Type: Cherry blossom petals sweeping between scenes
Best use: Japanese aesthetic, spring content, romantic edits, soft feminine content, travel
Duration: 00:00:00:12 to 00:00:00:22 (12-22 frames)
Intensity: Low
Mood: Gentle, romantic, Japanese-aesthetic, springtime
Pair with: Wind chime sound, warm filters, travel content, Floating Blossom body effect
Avoid with: Dark/horror, aggressive content, winter-themed
```

## 1.7 BASIC / UTILITY TRANSITIONS

```
Effect: Swipe
Category: Transitions → Trending
Type: Clean directional swipe cut
Best use: Universal utility transition — works anywhere that needs clean directional movement
Duration: 00:00:00:06 to 00:00:00:12 (6-12 frames)
Intensity: Low-Medium
Mood: Clean, neutral, professional
Pair with: Whoosh sound, any content type, list-style videos, comparison content
Avoid with: Nothing specific — most versatile transition in the library
```

```
Effect: Mix
Category: Transitions → Classic / Overlay
Type: Standard cross-dissolve blend
Best use: Universal smooth transition — talking head cuts, photo slideshows, any gentle scene change
Duration: 00:00:00:12 to 00:00:00:24 (12-24 frames)
Intensity: Low
Mood: Smooth, invisible, professional, neutral
Pair with: Any content — the "invisible" transition
Avoid with: When you want energy or impact — Mix is intentionally subtle
```

```
Effect: Superimpose
Category: Transitions → Classic / Overlay
Type: Double-exposure blend between scenes
Best use: Artistic transitions, memory sequences, abstract content, music videos
Duration: 00:00:00:15 to 00:00:01:00 (15-30 frames)
Intensity: Low-Medium
Mood: Artistic, layered, cinematic, thoughtful
Pair with: Cinematic music, abstract visuals, double-exposure body effects, artistic filters
Avoid with: Fast-paced content, clear narrative cuts, tutorial content
```

---

# 2. VIDEO EFFECTS (40 entries)

---

## 2.1 SHAKE / MOTION EFFECTS

```
Effect: Camera Shake
Category: Video Effects → Trending / Party
Type: Simulated handheld camera shake overlay
Best use: Energy spikes, beat drops, action emphasis, live event feel, hype moments
Duration: 00:00:00:06 to 00:00:00:20 (6-20 frames)
Intensity: Medium-High
Mood: Raw, energetic, live, visceral
Pair with: Bass hit, beat-synced music, impact transitions, party footage
Avoid with: Talking head (readability), corporate, motion-sensitive audiences
```

```
Effect: Repeat Shake
Category: Video Effects → Trending / Party
Type: Rapid repeating shake with frame echo
Best use: Beat drops, dance videos, hype moments, transition emphasis, TikTok energy
Duration: 00:00:00:06 to 00:00:00:15 (6-15 frames)
Intensity: High
Mood: Aggressive, rhythmic, chaotic, viral
Pair with: Hard bass, party transitions, flash effects, dance footage
Avoid with: Readable text on screen, calm content, professional presentations
```

```
Effect: Shake Impact
Category: Video Effects → Trending
Type: Single strong shake impact — one hard jolt
Best use: Punch moments, key word emphasis, single beat hit, dramatic statement
Duration: 00:00:00:04 to 00:00:00:08 (4-8 frames)
Intensity: High
Mood: Impactful, decisive, powerful
Pair with: Impact sound, bass hit, zoom punch, bold caption reveal
Avoid with: Extended use (one-shot effect, not sustained)
```

## 2.2 FLASH / STROBE EFFECTS

```
Effect: Cross Flash
Category: Video Effects → Trending / Party
Type: Cross-shaped flash burst overlay
Best use: Beat sync, camera flash simulation, paparazzi feel, highlight moments
Duration: 00:00:00:03 to 00:00:00:08 (3-8 frames)
Intensity: High
Mood: Flashy, glamorous, energetic, spotlight
Pair with: Camera shutter sound, fashion content, party scenes, highlight moments
Avoid with: Photosensitivity warnings, calm/muted content, dark moody aesthetic
```

```
Effect: Vibration Flash
Category: Video Effects → Trending / Party
Type: Vibrating frame with flash pulses
Best use: High-energy dance content, beat drops, party edits, music videos
Duration: 00:00:00:06 to 00:00:00:15 (6-15 frames)
Intensity: High
Mood: Electric, pulsing, party, rave
Pair with: Electronic music, party transitions, strobe sound, neon filters
Avoid with: Epilepsy-sensitive content, slow pacing, corporate
```

```
Effect: Negative Strobe
Category: Video Effects → Trending / Light
Type: Rapid negative-image strobe flashing
Best use: Horror/thriller, suspense building, glitch aesthetic, music video intensity
Duration: 00:00:00:06 to 00:00:00:15 (6-15 frames)
Intensity: High
Mood: Unsettling, intense, horror, experimental
Pair with: Distortion sound, glitch transitions, horror filters, dark content
Avoid with: All comfort-oriented content, children's content, accessibility-sensitive
```

## 2.3 BLUR / FOCUS EFFECTS

```
Effect: Blur
Category: Video Effects → Trending / Classic
Type: Simple full-frame gaussian blur overlay
Best use: Background for text/captions, focus transitions, dreamy moments, privacy masking
Duration: 00:00:00:15 to 00:00:05:00 (variable — often sustained)
Intensity: Low-Medium
Mood: Soft, dreamy, neutral, functional
Pair with: Text overlays, caption moments, transition in/out, title cards
Avoid with: Action sequences where clarity matters, detail-heavy shots
```

```
Effect: Dynamic Blur
Category: Video Effects → Trending / Classic / Motion
Type: Motion-based directional blur
Best use: Speed emphasis, movement accentuation, swoosh moments, transition bridges
Duration: 00:00:00:06 to 00:00:00:15 (6-15 frames)
Intensity: Medium
Mood: Fast, dynamic, swooshing, energetic
Pair with: Whoosh sound, swipe transitions, speed ramp, movement-heavy footage
Avoid with: Static shots, talking heads, detail-critical moments
```

```
Effect: Dreamy Bokeh
Category: Video Effects → Trending / Light
Type: Soft bokeh circles with dreamy glow overlay
Best use: Romantic scenes, beauty content, emotional moments, night scenes, music videos
Duration: 00:00:01:00 to 00:00:10:00 (sustained)
Intensity: Low
Mood: Romantic, dreamy, soft, intimate
Pair with: Warm filters, romantic music, body effects like Bokeh Lovelight, soft transitions
Avoid with: Corporate, tech, action, daytime outdoor harsh light
```

## 2.4 RETRO / VINTAGE EFFECTS

```
Effect: VHS Noise
Category: Video Effects → Trending
Type: VHS tape noise, scan lines, and tracking distortion overlay
Best use: Retro aesthetic, nostalgic content, lo-fi branding, vintage-themed edits, flashback sequences
Duration: 00:00:01:00 to 00:00:30:00 (sustained or full clip)
Intensity: Medium
Mood: Nostalgic, retro, lo-fi, vintage
Pair with: VHS filters, retro music, analog sound effects, Retro body effects
Avoid with: Clean modern branding, 4K quality showcase, product detail shots
```

```
Effect: Vintage TV
Category: Video Effects → Trending / Hits
Type: Old CRT television frame with scan lines and rounded corners
Best use: Retro segments, flashback sequences, nostalgic intros, throwback content
Duration: 00:00:02:00 to 00:00:30:00 (sustained)
Intensity: Medium
Mood: Retro, nostalgic, broadcast, throwback
Pair with: Retro filters, VHS transitions, old TV sound, vintage music
Avoid with: Modern/clean aesthetic, high-resolution showcase, luxury branding
```

```
Effect: Film Frame
Category: Video Effects → Hits
Type: Analog film strip frame with sprocket holes overlay
Best use: Cinematic feel, film aesthetic, intro sequences, artistic content, behind-the-scenes
Duration: 00:00:02:00 to 00:00:30:00 (sustained)
Intensity: Low-Medium
Mood: Cinematic, artsy, analog, authentic
Pair with: Movie filters (Wong Kar-wai, Retro Film), film grain, cinematic music
Avoid with: Clean digital aesthetic, social media native style
```

## 2.5 GLOW / LIGHT EFFECTS

```
Effect: God Rays
Category: Video Effects → Light
Type: Volumetric light rays streaming from above/behind subject
Best use: Inspirational moments, hero shots, sunrise/sunset, spiritual content, dramatic lighting
Duration: 00:00:01:00 to 00:00:10:00 (sustained)
Intensity: Medium
Mood: Majestic, spiritual, epic, warm
Pair with: Orchestral/inspirational music, warm filters, outdoor footage, golden hour
Avoid with: Indoor flat-lit content, nighttime, dark moody aesthetic
```

```
Effect: Limelight
Category: Video Effects → Trending / Light
Type: Bright spotlight/limelight glow on center of frame
Best use: Subject highlighting, hero moments, key statements, award-style content
Duration: 00:00:00:15 to 00:00:03:00 (15 frames to 3 seconds)
Intensity: Medium
Mood: Spotlight, important, heroic, premium
Pair with: Dramatic pause, key statement, Spotlight body effect, bass swell sound
Avoid with: Group scenes, landscape wide shots, dark horror content
```

```
Effect: Sun Flashes
Category: Video Effects → Trending / Light
Type: Animated sun lens flare overlay
Best use: Outdoor content, golden hour simulation, travel videos, warm aesthetic, summer feel
Duration: 00:00:01:00 to 00:00:10:00 (sustained)
Intensity: Low-Medium
Mood: Warm, sunny, optimistic, natural
Pair with: Warm filters, outdoor footage, travel content, acoustic music
Avoid with: Indoor content, nighttime, cold/dark aesthetic
```

```
Effect: Leak 1
Category: Video Effects → Trending / Light
Type: Analog light leak overlay — warm color bleed across frame
Best use: Vintage feel, film aesthetic, transitions between moods, artistic layering
Duration: 00:00:01:00 to 00:00:05:00 (sustained)
Intensity: Low
Mood: Filmic, warm, nostalgic, organic
Pair with: Film grain, retro filters, analog music, cinematic content
Avoid with: Clean/sterile aesthetic, precise color-critical work
```

```
Effect: Sequin Bokeh
Category: Video Effects → Trending / Light
Type: Sparkling sequin-style bokeh overlay
Best use: Glamorous content, fashion, celebration, night-out aesthetic, luxury branding
Duration: 00:00:01:00 to 00:00:10:00 (sustained)
Intensity: Low-Medium
Mood: Glamorous, sparkling, luxurious, festive
Pair with: Bling body effects, party transitions, fashion content, celebration footage
Avoid with: Minimalist aesthetic, corporate, daytime outdoor
```

## 2.6 INTRO / OUTRO EFFECTS

```
Effect: Fade In
Category: Video Effects → Classic / Intro & Outro
Type: Simple opacity fade from black to visible
Best use: Video openings, chapter starts, gentle entrances, establishing shots
Duration: 00:00:00:15 to 00:00:01:15 (15-45 frames)
Intensity: Low
Mood: Calm, professional, classic, welcoming
Pair with: Ambient music fade-in, title cards, establishing shots
Avoid with: When you need immediate energy (hook sections)
```

```
Effect: Fade Out
Category: Video Effects → Classic / Intro & Outro
Type: Simple opacity fade to black
Best use: Video endings, chapter closes, emotional endings, pause before next section
Duration: 00:00:00:15 to 00:00:01:15 (15-45 frames)
Intensity: Low
Mood: Conclusive, gentle, final, reflective
Pair with: Music fade-out, end cards, final statements, emotional conclusions
Avoid with: Mid-video pacing (kills momentum), hook sections
```

```
Effect: Countdown 3
Category: Video Effects → Trending / Intro & Outro
Type: 3-2-1 countdown animation overlay
Best use: Video openings, reveal countdowns, challenge starts, event launches, before/after
Duration: 00:00:03:00 to 00:00:04:00 (3-4 seconds)
Intensity: Medium
Mood: Anticipatory, exciting, event-like, structured
Pair with: Tick sound effects, reveal moments, challenge/competition content
Avoid with: Serious/somber content, documentary, corporate
```

## 2.7 DISTORTION / GLITCH EFFECTS

```
Effect: Ghost Distortion
Category: Video Effects → Trending
Type: Ghostly double-image with distortion
Best use: Surreal moments, music video intensity, horror accents, dream sequences, emotional overwhelm
Duration: 00:00:00:10 to 00:00:01:00 (10-30 frames)
Intensity: Medium-High
Mood: Surreal, eerie, psychedelic, intense
Pair with: Reverb sound, glitch transitions, alternative filters, dark music
Avoid with: Clear/informational content, product showcase, tutorial
```

```
Effect: Pixel Glitch
Category: Video Effects → Trending
Type: Digital pixel corruption glitch effect
Best use: Tech content, error aesthetic, data/cyber themes, surprise disruptions, gaming edits
Duration: 00:00:00:04 to 00:00:00:15 (4-15 frames)
Intensity: High
Mood: Digital, broken, cyber, edgy
Pair with: Glitch sound, tech transitions, cyberpunk filters, digital content
Avoid with: Organic/natural content, luxury branding, beauty
```

```
Effect: Shockwave
Category: Video Effects → Party
Type: Radial shockwave distortion pulse
Best use: Beat drops, impact moments, bass hits, action emphasis, explosion simulation
Duration: 00:00:00:04 to 00:00:00:10 (4-10 frames)
Intensity: High
Mood: Explosive, powerful, impactful, concussive
Pair with: Bass drop, impact sound, beat-synced edits, action footage
Avoid with: Subtle content, slow pacing, gentle moments
```

## 2.8 SPLIT / SCREEN EFFECTS

```
Effect: Four Screens
Category: Video Effects → Trending / Classic
Type: Splits frame into 4 mirrored/repeated quadrants
Best use: Dance content, pattern emphasis, kaleidoscopic moments, artistic intros
Duration: 00:00:00:15 to 00:00:03:00 (15 frames to 3 seconds)
Intensity: Medium
Mood: Artistic, symmetrical, hypnotic, experimental
Pair with: Rhythmic music, dance footage, pattern-heavy visuals
Avoid with: Talking head (confusing), text-heavy scenes, information delivery
```

```
Effect: Tri-layer Mirror
Category: Video Effects → Trending
Type: Triple-layered mirror split effect
Best use: Dance videos, fashion content, artistic expression, music video sequences
Duration: 00:00:00:15 to 00:00:03:00 (15 frames to 3 seconds)
Intensity: Medium
Mood: Artistic, dynamic, kaleidoscopic, editorial
Pair with: Dance music, fashion footage, bold transitions, creative intros
Avoid with: Information-dense content, talking heads, tutorial
```

## 2.9 OVERLAY / PARTICLE EFFECTS

```
Effect: Snowfall
Category: Video Effects → Trending
Type: Falling snow particle overlay
Best use: Winter/holiday content, cozy aesthetic, seasonal edits, Christmas content
Duration: 00:00:02:00 to 00:00:30:00 (sustained)
Intensity: Low
Mood: Wintry, cozy, peaceful, festive
Pair with: Cold/blue filters, winter transitions, holiday music, frost effects
Avoid with: Summer content, tropical aesthetic, warm-toned edits
```

```
Effect: Falling Dust
Category: Video Effects → Trending / Light
Type: Floating dust motes in light beam overlay
Best use: Cinematic atmosphere, moody interiors, golden light scenes, nostalgic moments
Duration: 00:00:02:00 to 00:00:30:00 (sustained)
Intensity: Low
Mood: Atmospheric, cinematic, warm, dusty
Pair with: Warm lighting, cinematic filters, ambient sound, interior footage
Avoid with: Clean/modern aesthetic, outdoor bright content, sterile environments
```

```
Effect: Speed Lines
Category: Video Effects → Trending / Motion
Type: Anime/manga-style speed line overlay radiating from center
Best use: Action emphasis, anime aesthetic, comedy reactions, hype moments, surprise
Duration: 00:00:00:06 to 00:00:00:20 (6-20 frames)
Intensity: Medium-High
Mood: Action, anime, comedic, intense
Pair with: Impact sound, zoom effects, anime-style content, reaction moments, comic transitions
Avoid with: Realistic/cinematic content, luxury branding, corporate
```

```
Effect: HDR
Category: Video Effects → Trending / Motion
Type: HDR-style enhanced contrast and detail overlay
Best use: Quality enhancement, landscape/travel, making footage look premium, any content
Duration: Full clip (sustained)
Intensity: Low
Mood: Premium, enhanced, crisp, vivid
Pair with: Any content needing visual upgrade, travel footage, product shots, outdoor
Avoid with: Already color-graded footage (double processing), intentionally muted aesthetic
```

```
Effect: Vignette
Category: Video Effects → Classic / Motion
Type: Darkened frame edges directing focus to center
Best use: Subject focus, cinematic feel, mood enhancement, portrait content, any video
Duration: Full clip (sustained)
Intensity: Low
Mood: Focused, cinematic, moody, classic
Pair with: Any filter, cinematic transitions, talking head, portrait content
Avoid with: Wide landscape where edges matter, bright airy aesthetic
```

```
Effect: Insane Glow
Category: Video Effects → Trending / Party
Type: Extreme bloom/glow effect washing out highlights
Best use: Dream sequences, party peak moments, otherworldly feel, music video climax
Duration: 00:00:00:10 to 00:00:01:00 (10-30 frames)
Intensity: High
Mood: Ethereal, overwhelming, transcendent, peak
Pair with: Climax music, peak emotional moments, bright transitions, dreamy body effects
Avoid with: Detail-critical shots, product showcase, dark content
```

---

# 3. BODY EFFECTS (20 entries)

---

## 3.1 CINEMATIC / FILM BODY EFFECTS

```
Effect: Film-worthy OOTD
Category: Body Effects → Trending
Type: Cinematic color grade making subject look like a film still
Best use: Fashion content, outfit showcases, OOTD videos, editorial portrait feel
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Cinematic, editorial, polished, fashion
Pair with: Movie filters, smooth transitions, fashion music, editorial text overlays
Avoid with: Casual/raw content where film look clashes with authentic vibe
```

```
Effect: Silver Screen
Category: Body Effects → Trending
Type: Classic black-and-white or silver monochrome on subject only
Best use: Dramatic moments, classic Hollywood feel, artistic emphasis, mood shifts
Duration: 00:00:01:00 to 00:00:10:00 (variable)
Intensity: Medium
Mood: Classic, dramatic, timeless, Hollywood
Pair with: Mono filters, cinematic transitions, orchestral music, Film Noir filter
Avoid with: Color-dependent content, product showcase where color matters
```

```
Effect: Soft Film
Category: Body Effects → Trending
Type: Soft cinematic film emulation applied to subject
Best use: Lifestyle content, vlogs, casual cinematic feel, everyday beauty
Duration: Full clip (sustained)
Intensity: Low
Mood: Soft, filmic, warm, natural
Pair with: Warm filters, gentle transitions, acoustic music, vlog content
Avoid with: High-energy party content, corporate precision
```

## 3.2 GLOW / AURA BODY EFFECTS

```
Effect: Dreamy Gaze
Category: Body Effects → Trending
Type: Soft focus bloom creating ethereal portrait mood on subject
Best use: Beauty content, romantic moments, dream sequences, soft intros, emotional peaks
Duration: 00:00:01:00 to 00:00:10:00 (sustained)
Intensity: Low
Mood: Dreamy, ethereal, romantic, soft
Pair with: Warm filters, gentle transitions, romantic music, Dreamy Bokeh video effect
Avoid with: Sharp/detailed content, action, aggressive editing
```

```
Effect: Spotlight
Category: Body Effects → Trending
Type: Dramatic spotlight beam illuminating subject from above
Best use: Hero moments, key statements, solo performance, award-style reveals
Duration: 00:00:01:00 to 00:00:05:00 (sustained)
Intensity: Medium
Mood: Dramatic, important, heroic, focused
Pair with: Dramatic music swell, key statement, zoom in, impact sound
Avoid with: Casual/everyday content, group scenes, wide establishing shots
```

```
Effect: Neon Silhouette
Category: Body Effects → Trending [PRO]
Type: Neon-colored outline tracing subject's body
Best use: Dance videos, music videos, nightclub aesthetic, tech branding, futuristic edits
Duration: 00:00:01:00 to 00:00:10:00 (sustained)
Intensity: Medium-High
Mood: Neon, futuristic, electronic, club
Pair with: Electronic music, cyberpunk filters, glitch transitions, neon party effects
Avoid with: Organic/natural content, warm aesthetic, vintage edits
```

```
Effect: Body Contour Glow
Category: Body Effects → Trending
Type: Glowing contour lines tracing body shape
Best use: Dance content, fitness showcase, body movement emphasis, artistic expression
Duration: 00:00:01:00 to 00:00:10:00 (sustained)
Intensity: Medium
Mood: Artistic, luminous, movement-focused, modern
Pair with: Dark backgrounds, electronic music, motion-heavy footage, light transitions
Avoid with: Bright outdoor daylight (glow invisible), static subjects
```

## 3.3 BACKGROUND / SEPARATION BODY EFFECTS

```
Effect: Background Blur
Category: Body Effects → Basic / Blur [PRO]
Type: Blurs background while keeping subject sharp
Best use: Professional talking heads, portrait emphasis, hiding messy backgrounds, DSLR simulation
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Professional, focused, clean, cinematic
Pair with: Any filter, talking head content, interview, product presentation
Avoid with: When environment/location is important to the story
```

```
Effect: Color Splash
Category: Body Effects → Trending
Type: Subject stays in color, background becomes monochrome
Best use: Subject emphasis, artistic content, dramatic isolation, music video moments
Duration: 00:00:01:00 to 00:00:10:00 (variable)
Intensity: Medium
Mood: Dramatic, artistic, isolated, film-noir-adjacent
Pair with: Mono filters, dramatic music, emotional peaks, cinematic transitions
Avoid with: When background color is important, group scenes with all subjects mattering equally
```

```
Effect: Portrait Pop
Category: Body Effects → Trending
Type: Enhanced contrast on subject with slightly muted background
Best use: Any portrait/people content, vlogs, talking heads, subtle professional upgrade
Duration: Full clip (sustained)
Intensity: Low
Mood: Professional, enhanced, clean, polished
Pair with: Any filter, any transition, universal enhancement for people content
Avoid with: Non-people content (landscape, product only)
```

## 3.4 PARTICLE / ATMOSPHERIC BODY EFFECTS

```
Effect: Floating Blossom
Category: Body Effects → Trending
Type: Flower petals floating gently around subject
Best use: Romantic content, spring aesthetic, beauty, music videos, feminine branding
Duration: 00:00:02:00 to 00:00:15:00 (sustained)
Intensity: Low
Mood: Romantic, gentle, floral, beautiful
Pair with: Warm/pink filters, romantic music, Sakura transitions, spring content
Avoid with: Masculine branding, tech content, aggressive edits
```

```
Effect: Bokeh Lovelight
Category: Body Effects → Trending
Type: Bokeh light orbs floating around/behind subject
Best use: Night scenes, romantic content, date-night aesthetic, music videos, emotional peaks
Duration: 00:00:02:00 to 00:00:15:00 (sustained)
Intensity: Low
Mood: Romantic, dreamy, warm, intimate
Pair with: Night filters, romantic music, soft transitions, warm color grading
Avoid with: Bright daylight outdoor (looks unnatural), action content
```

```
Effect: First Snow
Category: Body Effects → Trending
Type: Soft white snowflake particles falling around subject
Best use: Winter content, holiday edits, cozy aesthetic, magical moments
Duration: 00:00:02:00 to 00:00:15:00 (sustained)
Intensity: Low
Mood: Wintry, magical, soft, peaceful
Pair with: Cold/blue filters, winter music, Snow Cleaned transition, Snowfall video effect
Avoid with: Summer/tropical content, warm color palette
```

## 3.5 BEAUTY / ENHANCEMENT BODY EFFECTS

```
Effect: Beauty Glow
Category: Body Effects → Portrait [PRO]
Type: Soft beauty glow on face and skin
Best use: Beauty content, skincare, fashion, any content wanting polished skin appearance
Duration: Full clip (sustained)
Intensity: Low
Mood: Polished, beautiful, glowing, flawless
Pair with: Portrait filters, warm lighting, beauty tutorials, fashion content
Avoid with: Raw/authentic aesthetic where real skin texture is valued
```

```
Effect: Golden Hour Face
Category: Body Effects → Portrait
Type: Golden hour warm light simulation on face
Best use: Outdoor content, golden hour simulation, warm portraits, sunset aesthetic
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Warm, golden, flattering, natural
Pair with: Warm filters (Sunkissed Peach, Sunset Bronze), outdoor footage, golden hour music
Avoid with: Cool-toned content, nighttime, blue/cold aesthetic
```

```
Effect: Vintage Luster
Category: Body Effects → Trending
Type: Warm sepia-toned color grade on subject with film grain
Best use: Vintage aesthetic, nostalgic content, retro-themed edits, throwback segments
Duration: Full clip (sustained)
Intensity: Medium
Mood: Vintage, warm, nostalgic, analog
Pair with: Retro filters, Film Fade transition, vintage music, VHS video effects
Avoid with: Modern/clean aesthetic, tech content, futuristic themes
```

---

# 4. FILTERS (30 entries)

---

## 4.1 CINEMATIC / MOVIE FILTERS

```
Effect: Wong Kar-wai
Category: Filters → Movies
Type: Saturated warm tones with crushed blacks — Hong Kong cinema aesthetic
Best use: Night scenes, neon-lit footage, emotional content, urban night cinematography
Duration: Full clip (sustained)
Intensity: Medium
Mood: Moody, neon-warm, nocturnal, emotional
Pair with: Night effects, neon body effects, urban footage, emotional music, Sleepless City filter
Avoid with: Bright daylight outdoor, corporate, clean aesthetic
```

```
Effect: Oppenheimer
Category: Filters → Movies
Type: Desaturated with boosted contrast — Nolan-style cinematic grade
Best use: Dramatic content, historical feel, serious tone, cinematic talking heads
Duration: Full clip (sustained)
Intensity: Medium
Mood: Serious, dramatic, cinematic, weighty
Pair with: Cinematic transitions, dramatic music, wide shots, Film Frame effect
Avoid with: Fun/light content, comedy, beauty, colorful product showcase
```

```
Effect: Retro Film
Category: Filters → Hits / Retro
Type: Classic film stock emulation with warm tones and slight grain
Best use: Vintage aesthetic, general cinematic upgrade, music videos, lifestyle content
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Filmic, warm, vintage, classic
Pair with: Film Frame effect, analog transitions, warm music, Film Fade transition
Avoid with: Clean modern branding, tech product showcase
```

```
Effect: Barbie
Category: Filters → Movies
Type: Hyper-saturated pink/warm tones — Barbie movie aesthetic
Best use: Pink aesthetic, feminine content, fun/playful branding, party content, trend-riding
Duration: Full clip (sustained)
Intensity: Medium-High
Mood: Pink, playful, hyper-feminine, fun
Pair with: Pink transitions, bling body effects, pop music, bright pastel content
Avoid with: Masculine branding, serious/corporate, dark moody content
```

```
Effect: Inception
Category: Filters → Movies
Type: Cool blue-green desaturated tones — Nolan thriller grade
Best use: Sci-fi content, thriller feel, surreal moments, tech content, mystery
Duration: Full clip (sustained)
Intensity: Medium
Mood: Cool, mysterious, sci-fi, cerebral
Pair with: Glitch effects, suspense sound, Ghost Distortion effect, cool transitions
Avoid with: Warm lifestyle content, beauty, food, sunny outdoor
```

## 4.2 LIFESTYLE / GENERAL FILTERS

```
Effect: Vivid Verse
Category: Filters → Featured / Hits
Type: Enhanced vibrancy with balanced saturation boost
Best use: General color enhancement — makes any footage pop, travel, outdoor, lifestyle
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Vibrant, alive, colorful, enhanced
Pair with: Any content needing color boost, outdoor footage, travel, food
Avoid with: Already saturated footage (will clip), intentionally muted aesthetic
```

```
Effect: Copper Highlight
Category: Filters → Featured / Hits / Life
Type: Warm copper-toned highlights with muted shadows
Best use: Golden hour enhancement, warm portraits, autumn content, cozy aesthetic
Duration: Full clip (sustained)
Intensity: Low
Mood: Warm, golden, cozy, rich
Pair with: Golden Hour Face body effect, warm transitions, autumn music, indoor lighting
Avoid with: Cool-toned content, blue hour, nighttime neon
```

```
Effect: Hollywood Past
Category: Filters → Featured / Hits / Mono
Type: Desaturated warm with film grain — old Hollywood glamour
Best use: Elegant/classic content, black-tie events, vintage sophistication, artistic intros
Duration: Full clip (sustained)
Intensity: Medium
Mood: Glamorous, classic, sophisticated, timeless
Pair with: Silver Screen body effect, Film Fade transition, orchestral music, elegant text
Avoid with: Modern/trendy content, neon aesthetic, youth-oriented casual
```

```
Effect: Silky Complexion
Category: Filters → Featured / Hits / Portrait
Type: Skin-smoothing warm filter that flatters complexion
Best use: Beauty content, talking heads, interviews, any people-centric content
Duration: Full clip (sustained)
Intensity: Low
Mood: Polished, beautiful, soft, flattering
Pair with: Beauty Glow body effect, Portrait Pop, warm lighting, beauty transitions
Avoid with: Raw/authentic skin-positive content, non-people footage
```

```
Effect: Enhance
Category: Filters → Featured / Life
Type: Universal quality enhancement — subtle contrast and clarity boost
Best use: Any footage — universal quality upgrade, the "make it look better" filter
Duration: Full clip (sustained)
Intensity: Low
Mood: Clean, enhanced, professional, clear
Pair with: Literally anything — most versatile filter in the library
Avoid with: Already processed footage (double processing artifacts)
```

```
Effect: Bold Saturation
Category: Filters → Featured / Life
Type: Strong saturation boost with maintained blacks
Best use: Color-rich content, travel, food, product showcase, making muted footage pop
Duration: Full clip (sustained)
Intensity: Medium
Mood: Vivid, bold, punchy, colorful
Pair with: Colorful content, travel footage, food videos, product showcase
Avoid with: Skin-heavy content (oversaturates skin tones), already vivid footage
```

## 4.3 MOOD / ATMOSPHERE FILTERS

```
Effect: Sleepless City
Category: Filters → Featured / Hits / Night
Type: Cool blue-toned night city aesthetic with boosted highlights
Best use: Night footage, urban content, city nightlife, late-night aesthetic
Duration: Full clip (sustained)
Intensity: Medium
Mood: Nocturnal, urban, cool, city-noir
Pair with: Night body effects, neon transitions, urban footage, lo-fi music
Avoid with: Daylight content, warm aesthetic, rural/nature footage
```

```
Effect: Bronze Night
Category: Filters → Hits / Movies
Type: Warm bronze with dark shadows — night luxury aesthetic
Best use: Night events, luxury content, cocktail/lounge aesthetic, dark glamour
Duration: Full clip (sustained)
Intensity: Medium
Mood: Luxurious, warm-dark, sophisticated, night
Pair with: Sequin Bokeh effect, bling body effects, luxury content, gold text overlays
Avoid with: Daytime content, bright cheerful aesthetic, budget-feel content
```

```
Effect: Fairy's Meadow
Category: Filters → Hits / Landscape
Type: Soft green-warm tones with gentle glow — enchanted garden feel
Best use: Nature content, garden/outdoor, spring aesthetic, fantasy feel, gentle lifestyle
Duration: Full clip (sustained)
Intensity: Low
Mood: Enchanted, natural, gentle, spring
Pair with: Floating Blossom body effect, nature footage, soft transitions, ambient music
Avoid with: Urban content, nighttime, tech/digital aesthetic
```

```
Effect: Stranger Day
Category: Filters → Featured / Hits / Alternative
Type: Desaturated cool tones with slight unease — Stranger Things vibe
Best use: Horror/thriller, mystery content, unsettling mood, 80s sci-fi aesthetic
Duration: Full clip (sustained)
Intensity: Medium
Mood: Eerie, mysterious, 80s-horror, unsettling
Pair with: Glitch effects, VHS Noise, retro transitions, synth music
Avoid with: Happy/cheerful content, beauty, lifestyle
```

```
Effect: Somber Picnic
Category: Filters → Hits / Retro
Type: Muted warm tones with faded highlights — melancholic nostalgia
Best use: Nostalgic content, emotional storytelling, coming-of-age aesthetic, indie film feel
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Nostalgic, melancholic, faded, indie
Pair with: Soft Film body effect, Film Fade transition, indie music, vintage text
Avoid with: High-energy content, vivid colorful branding, corporate
```

```
Effect: Summer Soda
Category: Filters → Featured / Hits / Portrait
Type: Bright warm with slight pink cast — summer fun aesthetic
Best use: Summer content, beach, outdoor fun, youthful branding, lifestyle
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Summery, fun, bright, youthful
Pair with: Bright transitions, warm body effects, outdoor footage, upbeat music
Avoid with: Winter/cold content, dark moody aesthetic, corporate
```

```
Effect: Neon Fire
Category: Filters → Featured / Portrait
Type: High-contrast with neon-warm tones — fire-lit aesthetic
Best use: Night content, concert/event footage, intense emotional moments, party content
Duration: Full clip (sustained)
Intensity: Medium-High
Mood: Intense, fiery, dramatic, electric
Pair with: Party effects, fire body effects, concert footage, electronic music
Avoid with: Calm/gentle content, pastel aesthetic, daytime outdoor
```

## 4.4 MONO / BLACK & WHITE FILTERS

```
Effect: Elegant B&W
Category: Filters → Mono
Type: Classic high-quality black and white with smooth tonal range
Best use: Dramatic moments, artistic content, classic portrait, fashion editorial
Duration: Full clip or segment (sustained)
Intensity: Medium
Mood: Classic, elegant, timeless, dramatic
Pair with: Silver Screen body effect, cinematic transitions, orchestral music
Avoid with: Color-dependent content, product showcase, food
```

```
Effect: Newspaper Glam
Category: Filters → Hits / Mono / Photo Booth
Type: High-contrast B&W with newspaper print texture
Best use: Artistic content, editorial feel, fashion, vintage journalism aesthetic
Duration: Full clip or segment (sustained)
Intensity: Medium-High
Mood: Editorial, bold, journalistic, high-contrast
Pair with: Text overlays, comic transitions, bold typography, newspaper effects
Avoid with: Soft/gentle content, beauty, food photography
```

```
Effect: Shimmering B&W
Category: Filters → Hits / Mono
Type: Black and white with shimmering highlight bloom
Best use: Glamorous moments, musical peaks, emotional climax, awards/gala content
Duration: 00:00:02:00 to 00:00:15:00 (sustained segment)
Intensity: Medium
Mood: Glamorous, ethereal, cinematic, peak-moment
Pair with: Bling body effects, Spotlight body effect, dramatic music, flash transitions
Avoid with: Casual content, everyday vlogs, color-critical moments
```

## 4.5 RETRO / ERA FILTERS

```
Effect: Y2k-Internet Girl
Category: Filters → Featured / Hits
Type: Early 2000s digital camera aesthetic — slightly washed, pink-tinted, low-fi
Best use: Y2K aesthetic, nostalgic internet content, early 2000s throwback, trend content
Duration: Full clip (sustained)
Intensity: Medium
Mood: Nostalgic, Y2K, internet-era, pink-washed
Pair with: Retro body effects, VHS transitions, 2000s music, nostalgic text styles
Avoid with: Modern/clean aesthetic, professional corporate, cinematic
```

```
Effect: American Retro
Category: Filters → Featured / Retro
Type: Warm Americana faded tones — vintage US road trip aesthetic
Best use: Road trip content, Americana aesthetic, vintage lifestyle, outdoor/travel
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Vintage, Americana, warm, adventurous
Pair with: Retro Film filter stack, vintage body effects, country/rock music
Avoid with: Urban modern content, Asian aesthetic, futuristic themes
```

```
Effect: 80s Holiday
Category: Filters → Featured / Retro / Portrait
Type: 1980s Kodak snapshot aesthetic — warm, slightly overexposed, nostalgic
Best use: 80s themed content, throwback, nostalgia, home video aesthetic, party
Duration: Full clip (sustained)
Intensity: Medium
Mood: 80s, nostalgic, warm, snapshot
Pair with: VHS effects, retro transitions, 80s music, Retro Starpulse effect
Avoid with: Clean modern aesthetic, 4K precision, futuristic
```

## 4.6 SPECIALTY / PURPOSE FILTERS

```
Effect: Scrumptious
Category: Filters → Food
Type: Warm saturation boost optimized for food — makes food look appetizing
Best use: Food content, restaurant reviews, cooking videos, recipe reels
Duration: Full clip (sustained)
Intensity: Low-Medium
Mood: Appetizing, warm, delicious, inviting
Pair with: Food stickers, warm lighting, cooking sound design, close-up shots
Avoid with: Non-food content, cool-toned aesthetic
```

```
Effect: HD Pet
Category: Filters → Pet [PRO]
Type: Enhanced clarity and warm tones optimized for animal fur and features
Best use: Pet content, animal videos, pet product showcase, animal portraits
Duration: Full clip (sustained)
Intensity: Low
Mood: Clear, warm, adorable, enhanced
Pair with: Pet stickers, cute sound effects, animal-focused body effects
Avoid with: Non-pet content, dark moody aesthetic
```

```
Effect: Backlight Fix
Category: Filters → Featured / Portrait
Type: Compensates for backlit subjects — recovers shadow detail
Best use: Backlit subjects, window-behind talking heads, sunset silhouettes needing recovery
Duration: Full clip (sustained)
Intensity: Low
Mood: Corrective, balanced, recovered, natural
Pair with: Any backlit footage — functional correction filter, pairs with any style after
Avoid with: Front-lit footage (unnecessary), intentional silhouette aesthetic
```

```
Effect: Cyberpunk
Category: Filters → Night
Type: Neon teal-magenta split toning — cyberpunk 2077 aesthetic
Best use: Night city footage, tech content, futuristic aesthetic, gaming content, neon scenes
Duration: Full clip (sustained)
Intensity: High
Mood: Futuristic, neon, cyberpunk, electric
Pair with: Neon body effects, glitch transitions, electronic music, tech content
Avoid with: Nature/organic content, warm aesthetic, vintage, corporate
```

---

# QUICK REFERENCE — USE CASE INDEX

## By Editing Scenario

| Scenario | Recommended Assets |
|----------|-------------------|
| **Beat drop** | White Flash (T), Shaky Inhale (T), Camera Shake (VE), Shockwave (VE), Shake Impact (VE) |
| **Emotional peak** | Heartwarming Flash (T), Overlap Fade (T), Dreamy Gaze (BE), Spotlight (BE), Shimmering B&W (F) |
| **Scene change (smooth)** | Simple Blur (T), Mix (T), Blur Focus (T), Swipe (T) |
| **Scene change (energetic)** | Snap Rack (T), Shake Snap (T), Swipe Left (T), Rebound Zoom (T) |
| **Intro/opening** | Fade In (VE), Countdown 3 (VE), Pull In (T), Black Fade (T) |
| **Outro/ending** | Fade Out (VE), Black Fade (T), Overlap Fade (T) |
| **Talking head** | Background Blur (BE), Portrait Pop (BE), Silky Complexion (F), Enhance (F) |
| **Product reveal** | Delay Zoom (T), Slice Reveal (T), Pull In (T), White Flash (T) |
| **Romantic/emotional** | Bokeh Lovelight (BE), Floating Blossom (BE), Dreamy Bokeh (VE), Heartwarming Flash (T) |
| **Retro/vintage** | VHS Noise (VE), Vintage TV (VE), Retro Film (F), 80s Holiday (F), Film Fade (T) |
| **Horror/thriller** | Dark Flash (T), Signal Glitch 2 (T), Negative Strobe (VE), Stranger Day (F) |
| **Cinematic** | God Rays (VE), Vignette (VE), Film Frame (VE), Wong Kar-wai (F), Oppenheimer (F) |
| **Dance/music video** | Neon Silhouette (BE), Body Contour Glow (BE), Cross Flash (VE), Vibration Flash (VE) |
| **Beauty/fashion** | Film-worthy OOTD (BE), Beauty Glow (BE), Silky Complexion (F), Pastel Motion (T) |
| **Night/urban** | Sleepless City (F), Cyberpunk (F), Neon Fire (F), Bronze Night (F) |
| **Winter/holiday** | Snowfall (VE), First Snow (BE), Snow Cleaned (T), cold-toned filters |
| **Food** | Scrumptious (F), Bold Saturation (F), Copper Highlight (F) |

## By Mood

| Mood | Top 5 Assets |
|------|-------------|
| **Energetic** | Shaky Inhale (T), Camera Shake (VE), Cross Flash (VE), Vibration Flash (VE), White Flash (T) |
| **Dreamy** | Dreamy Bokeh (VE), Dreamy Gaze (BE), Bubble Blur (T), Simple Blur (T), Fairy's Meadow (F) |
| **Cinematic** | Wong Kar-wai (F), Film Frame (VE), God Rays (VE), Vignette (VE), Glare II (T) |
| **Dark/moody** | Dark Flash (T), Stranger Day (F), Bronze Night (F), Negative Strobe (VE), Oppenheimer (F) |
| **Playful** | Rebound Zoom (T), Comic Cut (T), Barbie (F), Countdown 3 (VE), Speed Lines (VE) |
| **Professional** | Mix (T), Enhance (F), Background Blur (BE), Portrait Pop (BE), Blur Focus (T) |
| **Nostalgic** | VHS Noise (VE), Retro Film (F), Somber Picnic (F), Film Fade (T), Vintage Luster (BE) |
| **Romantic** | Bokeh Lovelight (BE), Floating Blossom (BE), Heartwarming Flash (T), Sakura Breeze (T) |

## Legend

```
(T)  = Transition     — Left Panel → Transitions tab
(VE) = Video Effect   — Left Panel → Effects → Video effects
(BE) = Body Effect    — Left Panel → Effects → Body effects
(F)  = Filter         — Left Panel → Filters tab
```

---

# NOTES

- **PRO-marked effects** require CapCut Pro subscription. In this catalog: Neon Silhouette (BE), Background Blur (BE), Beauty Glow (BE), HD Pet (F), and some others carry PRO badges.
- **Stacking**: Filters can be stacked. A common stack is Enhancement filter + Mood filter (e.g., Enhance + Copper Highlight).
- **Body effects require a person**: Body effects use person detection AI. They will not work on landscape, product-only, or text-only footage.
- **Duration is guidance, not absolute**: All durations are recommendations. The editor adjusts by edge-dragging on the timeline.
- **Intensity is relative**: A "High" intensity effect can be dialed back via opacity or duration. Use the intensity rating to match the video's energy level.
- **Consistency rule**: Pick one filter for the entire video. Pick one transition family (blur or flash, not both). Body effects and video effects can layer but keep it to 2 max simultaneously.

---

*Created: 2026-03-10*
*Source KFs: KF-02 (All Effects: Video + Body), KF-03 (Transitions), KF-04 (Filters)*
*Selection criteria: Trending/Hits priority, versatility, coverage of all major editing scenarios*
*Format: Section 22 metadata template from capcut-ai-director-brain.md*

---

## FILE: knowledge-base/KF-10-ai-stylize.md

# KF-10 — AI Stylize Tab (Complete)

> Source: 17 screenshots from AI Stylize tab (2026-03-10)
> Location: Right Panel → AI stylize tab (when video clip selected)

---

## 1. OVERVIEW

The AI Stylize tab transforms video clips using AI-powered style transfer. It has two main sections:

1. **AI Effects** — Pre-built video style transformations (top section)
2. **Style** — Prompt-based AI generation with style categories (bottom section)

### Credits System
- Credits needed: 0–39 per generation
- Credits left: 1200 (refreshes)
- "Generate" button to apply

---

## 2. AI EFFECTS (Pre-built)

Located at the top of the AI Stylize panel. Thumbnail previews of video transformations.

| Effect | Description |
|--------|------------|
| Scombination | Style combination effect |
| CG 1 | CG/3D render style |
| Comics 1 | Comic book style |
| Comics 2 | Comic book style (variant) |

---

## 3. STYLE CATEGORIES (Prompt-Based)

### How It Works
1. Enter a text prompt describing the desired style (or use "Random" button)
2. Select a Style category and preset
3. Click "Generate"
4. AI transforms the video clip to match

### Prompt Example (from screenshot)
```
(Queen!) gold crown inlaid with gems, white-haired girl, oil painting, (red robe), warm lights, candles, royal style, fantasy painting style, surreal details, golden color palette, enchantment, fairy core, Hyperrealistic illustration, fantasy painting, oil painting free, worn brushstrokes, post-impressionism, fantasy, medieval, inside the castle,
```

### Showcase Section
Gallery of example outputs showing what the AI can produce — artistic paintings, portraits, fantasy scenes, anime-style renders.

---

## 4. STYLE PRESETS BY CATEGORY

### Trending
~10 presets visible (thumbnail previews, names partially visible)

### AI Painting
| Preset | Type |
|--------|------|
| AI filter - brush | Painting style |
| AI filter - frame | Painting style |
| JP Anime | Japanese anime style |
| Dreamy Anime | Soft anime aesthetic |
| Cat | Cat transformation |
| Muscle Man | Muscular character style |

### AI Photo
| Preset | Type |
|--------|------|
| Basketball | Sports theme photo |
| Football | Sports theme photo |
| Cheerleader | Sports theme photo |
| Baseball | Sports theme photo |
| 80s Glamour | Retro 80s photo style |
| 70s Core | Retro 70s photo style |
| Fitness | Athletic photo style |

### Particle
| Preset | Type |
|--------|------|
| Cosmic Effect | Space/cosmic particle dissolution |
| Particles Dissolution (variant 1) | Particle breakup effect |
| Particles Dissolution (variant 2) | Particle breakup effect |

### Hair Salon
| Preset | Type |
|--------|------|
| Berry Pink | Hair color change |
| Mint Green | Hair color change |
| Dark Blue | Hair color change |
| Pumpkin Orange | Hair color change |
| Chocolate | Hair color change |
| Pure White | Hair color change |
| Ash Blonde | Hair color change |
| Honey Blonde | Hair color change |

### Expressions
| Preset | Type |
|--------|------|
| Sad | Facial expression change |
| Dimple Laugh | Facial expression change |
| Chuckle Smile | Facial expression change |
| Poker Face | Facial expression change |
| Smile Face | Facial expression change |

### Motion
| Preset | Type |
|--------|------|
| Firework Party | Motion effect (2 uses badge) |
| Comic | Motion effect (2 uses badge) |
| Transcendence | Motion effect (2 uses badge) |
| Cyber Future | Motion effect (2 uses badge) |
| Doll | Motion effect |
| Photo Slinky | Motion effect |
| Camera Bounce | Motion effect |
| Camera Shake | Motion effect |
| 3D Zoom Pro | 3D zoom motion |
| 3D Zoom | 3D zoom motion |

### Split
| Preset | Type |
|--------|------|
| Pop Up Album | Split/collage effect |

### Portrait
| Preset | Type |
|--------|------|
| Pop Up Album | Portrait enhancement |

### Face Swap
| Preset | Type |
|--------|------|
| Angel Me | Face transformation |
| Evil Me | Face transformation |
| Big Head | Face transformation |

### Scene Swap
| Preset | Type |
|--------|------|
| CyberCity | Scene background change |
| Painting | Scene background change |

### Video Effects
| Preset | Type |
|--------|------|
| Auto Velocity | Automatic speed ramping |

---

## 5. CATEGORY SUMMARY

| Category | Preset Count | Focus |
|----------|-------------|-------|
| Trending | ~10 | Popular/featured styles |
| AI Painting | 6 | Artistic painting + anime transforms |
| AI Photo | 7 | Theme-based photo restyling |
| Particle | 3 | Dissolution/particle effects |
| Hair Salon | 8 | AI hair color changes |
| Expressions | 5 | Facial expression manipulation |
| Motion | 10 | Camera/motion effects |
| Split | 1 | Multi-frame layouts |
| Portrait | 1 | Portrait enhancement |
| Face Swap | 3 | Face transformation |
| Scene Swap | 2 | Background replacement |
| Video Effects | 1 | Auto editing effects |
| **TOTAL** | **~57** | |

---

## 6. KEY FEATURES

- **Prompt-driven**: Users can type custom prompts for unique styles
- **Random button**: Generates random style prompts for experimentation
- **Credits-based**: Each generation costs credits (0-39 per use)
- **Showcase gallery**: Built-in inspiration gallery with example prompts and outputs
- **Style checkbox**: Toggle to enable/disable style application
- **Works on video clips**: Transforms entire video segments, not just images

---

## 7. AI STYLIZE FOR THE EDITING DIRECTOR

### When to Suggest AI Stylize
- Creative/artistic content that needs a unique visual identity
- Music videos wanting a painted/anime aesthetic
- Social media content wanting a distinctive look
- Experimental/artistic projects
- Hair color changes for fashion/beauty content
- Expression adjustments for reaction content

### When NOT to Suggest AI Stylize
- Professional/corporate content (keep natural)
- News/documentary style (authenticity matters)
- Content where original footage quality is important
- When subtle color grading (Filters/Adjust) would achieve the goal

### Output Format for AI Stylize Suggestions
```
00:00:05:00–00:00:12:00
Action: Apply AI Stylize — JP Anime (AI Painting category)
Find it: Right panel → AI stylize → Style → AI painting → "JP Anime"
Why: The dreamlike sequence benefits from anime-style rendering
Note: Costs credits. Preview before committing.
```

---

*Source: 17 screenshots captured 2026-03-10*
*Categories: 11 style categories + AI Effects section*
*Total presets: ~57 named presets across all categories*
