# INDEX — Licence bina wale / istemal ke liye NAHI nikale gaye sources

**⚠️ Saaf baat pehle: is list ke kisi bhi source ka content istemal ke liye NAHI nikala gaya hai — na is folder me, na kahin aur. Ye file sirf ek record hai ki ye sources exist karte hain, aur har ek ke saath wajah likhi hai ki unka content kyun nahi liya gaya. Sirf MIT/Apache wale sources ka gyaan hi harvest karke istemal hua hai.**

Reason har entry ke saath hai. (Source: GitHub harvest, 2026-11-05 — `~/workspace/research_notes/creative-harvest-github.md`.)

**📌 Addendum (2026-11-06, editor-specific round — user ka naya nirdesh):** Upar wali chetaavni entries 1–6 (2026-11-05 round) ke liye jaisi thi waisi hi hai. 2026-11-06 se niyam me ek badlav hai: non-qualifying sources ka **verbatim content ab bhi NAHI** liya jata, lekin unki techniques/ideas/numbers ka ek chhota sar **apne shabdon me** ek alag file `notes_<owner>_<repo>.md` me rakha jata hai (ideas aur numbers par copyright nahi hota; source ka asal text/code copy nahi hota). Neeche entries 7–10 ke saath aisi notes files bani hain. Entries 11–13 licence se qualify karte hain lekin tool-only/schema-only hain — unme technique content hai hi nahi, isliye na extraction hua na note bana.

---

## 1. Dreydrey9000/claude-skills — "Clipper Skill" (Viral Editz)
- **Wajah:** Repo me **koi licence hai hi nahi** (licence re-check me phir confirm hua). Bina licence ke content istemal/copy karna allowed nahi mana jata.
- Link: https://github.com/Dreydrey9000/claude-skills (`video-editing/clipper-skill/SKILL.md`)
- Note: Content (timestamp-wise editing directions, CUB test) kaam ka laga tha, lekin licence na hone ki wajah se content NAHI nikala gaya.

## 2. OpenChatCut-V2 — `youtube-retention-editing` skill
- **Wajah:** Licence **AGPL-3.0** hai — user ka bar sirf MIT/Apache hai, AGPL qualify nahi karta.
- Ek-line factual note (sirf note, content nahi): is skill ka priority order hai — retention > clean cuts > comprehension > rhythm. Iske aage ka koi content nahi nikala gaya.

## 3. prabindersinghh/Kaestral-pro — `skills/retention-editing`
- **Wajah:** Licence **GPL-3.0** hai ("GNU General Public License v3.0"; README: "Free and open-source. GPLv3.") — MIT/Apache bar par qualify nahi karta.
- Link: https://github.com/prabindersinghh/Kaestral-pro/blob/HEAD/skills/retention-editing/SKILL.md
- Note: Cadence targets aur toolkit padhne layak the, lekin istemal licence par atka — content NAHI nikala gaya.

## 4. Andrea13235/Retention
- **Wajah:** **Custom licence** hai — GitHub ise "Other (NOASSERTION)" dikhata hai; MIT/Apache nahi hai, isliye qualify nahi karta.
- Design-idea note (sirf note, data/content nahi): is repo ka measured dataset pattern — **85 viral videos, 13,487 cut events** — ek *design idea* ke taur par note hai (apna measured corpus banane ka tareeka). Uska data ya content istemal NAHI hua.

## 5. QwenLM/Qwen-MM-Plugins — `video-edit` capability
- **Wajah:** Licence to **Apache-2.0** hai (qualify karta hai), lekin ye **generation/execution tooling** hai ("Generates images, video and audio, and runs editing workflows over them") — isme technique/retention knowledge hai hi nahi jo nikala ja sake. README me koi hook/pacing/cadence niyam nahi mile.
- Link: https://github.com/QwenLM/Qwen-MM-Plugins
- Note: "Qwen video-edit" naam ki koi technique-rules wali skill GitHub par mili hi nahi; ye usi naam ka sabse kareebi Apache source hai, isliye record me hai.

## 6. yunpeng1998/Qwen-Video-Edit (near-match)
- **Wajah:** Ye ek AI video-editing **model** hai ("Instruction-Based Video Editing by Repurposing an Image Editing Model") — technique skill nahi hai; aur iski apni licence README me **UNVERIFIED** rahi (koi licence line nahi mili).
- Link: https://github.com/yunpeng1998/Qwen-Video-Edit
- Note: Naam ki samaanta ki wajah se record me hai; content nikalne layak technique knowledge isme hai hi nahi.

---

## Editor round (DaVinci/CapCut)

(2026-11-06 ko DaVinci Resolve + CapCut ke liye khaas khoj hui. Neeche ke sources ya to licence ki wajah se qualify nahi hue, ya licence theek hone par bhi sirf tool/library nikale — technique knowledge nahi. Inka content istemal ke liye NAHI nikala gaya; upar wali saaf baat in par bhi lagu hai.)

### E1. appariciojunior/video-editor-skills
- **Wajah:** Licence **CC BY-NC 4.0** hai (commercial use mana hai) — user ka bar sirf MIT/Apache hai, qualify nahi karta.
- Link: https://github.com/appariciojunior/video-editor-skills
- Note: Content is round ka sabse relevant DaVinci first-pass editing tha — transcript cuts, vlog-pacing (silence/pads/pause rules), broll, music-and-sound (ducking), captions, motion-overlays, youtube-export — lekin licence NC hai, isliye content NAHI nikala gaya. (Agentgid ki Nov 2026 check ke mutabiq ~370 stars.)

### E2. AdamGarceau/resolve-toolkit
- **Wajah:** Repo me **koi licence hai hi nahi** — root me LICENSE file nahi aur repo details me licence blank hai.
- Link: https://github.com/AdamGarceau/resolve-toolkit
- Note: Skills me asal technique thi (perfect-cuts, dr-tighten ke shorts/longform profiles, podcast-punch-in, dr-snap-captions, resolve-vo-finish −6 dBFS peak, Fusion title pack) — lekin licence na hone se content NAHI nikala gaya.

### E3. SamuelAde001/second-brain — `video-edit-pass` skill
- **Wajah:** Personal vault repo hai, **koi licence nahi** (root me LICENSE nahi).
- Link: https://github.com/SamuelAde001/second-brain (skill: `.claude/skills/video-edit-pass/`)
- Note: DaVinci Resolve ke liye two-phase edit-assist technique thi (SRT + timeline XML se duplicate takes/misspeaks/flash frames pakadna, colour-coded marker EDL) — licence bina, content NAHI nikala gaya.

### E4. edwinponcious12/video — `davinci-resolve` skill
- **Wajah:** Repo me **koi licence nahi** (LICENSE file nahi, repo details me licence blank).
- Link: https://github.com/edwinponcious12/video
- Note: Skill khud kehta hai "This skill carries HOW, never WHAT" — MCP se Resolve timeline par EDL replay karne ki mechanics zyada thi, technique kam; licence bhi nahi, content NAHI nikala gaya.

### E5. GuanYixuan/pyJianYingDraft
- **Wajah:** Licence **Apache-2.0 hai (qualify karta hai)**, lekin ye CapCut/JianYing ke liye **draft-file generation library/tool** hai — draft JSON banane ka API hai, andar editing craft/technique knowledge nahi hai jo nikala ja sake.
- Link: https://github.com/GuanYixuan/pyJianYingDraft (repo page, 2026-11-06: 4,814 stars · 726 forks · 2024-07 se active)
- Note: Isi wajah se upar wali entry 5 (Qwen-MM-Plugins) jaisa hi muamla hai — licence theek, technique gayab. Iski sibling pyCapCut ka bhi yahi haal hai.

### E6. samuelgursky/davinci-resolve-mcp
- **Wajah:** Licence **MIT hai**, lekin ye sirf ek **MCP tool server** hai jo Resolve scripting API ko agent ke liye kholta hai — project khud kehta hai ki ye cut quality judge nahi karta, takes nahi chunta; technique knowledge isme hai hi nahi.
- Link: https://github.com/samuelgursky/davinci-resolve-mcp
- Note: Tool ke taur par mashhoor hai, lekin is harvest ka moyad technique hai, tool nahi — content NAHI nikala gaya.

## 7. ADAM-0S/wayland-m3ta-0s — `video-editing-master` skill (Premiere Pro + DaVinci Resolve)
- **Wajah:** Repo ka licence **AGPL-3.0** hai — MIT/Apache bar par qualify nahi karta. Dilchasp inconsistency: skill ki frontmatter khud ko "Apache-2.0" kehti hai, lekin repo ka LICENSE AGPL-3.0 hai; repo licence hi maana gaya.
- Link: https://github.com/ADAM-0S/wayland-m3ta-0s (skill: `src/process/resources/skills-library/bodies/skills/design-creative/video-editing-master/SKILL.md`)
- Note: Skill ka craft asal me pakka tha (split-edit offsets, Lumetri order, audio levels, loudness standards) — isliye 2026-11-06 ke naye nirdesh ke tahat apne shabdon me note bana hai: `notes_ADAM-0S_wayland-m3ta-0s.md`. Verbatim content NAHI liya gaya. (1 star, 729 commits, repo page 2026-11-06.)

## 8. eacp1991/premiere-agent — Premiere Agent (SKILL.md + references)
- **Wajah:** Repo me **koi licence hai hi nahi** (repo page par bhi nahi, clone me bhi koi LICENSE file nahi mili). Ye ek fork hai.
- Link: https://github.com/eacp1991/premiere-agent
- Note: SKILL.md (~85 KB) me asal production-correctness craft tha — word-boundary cut rule, pacing presets (Calm/Measured/Paced/Energetic/Jumpy) ke margins, 250 ms perceptual floor. Apne shabdon me note: `notes_eacp1991_premiere-agent.md`. Verbatim content NAHI liya gaya. (0 stars, 120 commits, repo page 2026-11-06.)

## 9. mmmnhat/agent-skills — "VisionCut" editorial suite (Premiere Pro MCP skills)
- **Wajah:** Repo me **koi licence hai hi nahi** (repo page par licence line nahi, clone me bhi LICENSE nahi mili).
- Link: https://github.com/mmmnhat/agent-skills
- Note: Suite ki technique asal thi — pacing-editor ka 5-track layout aur −12 dB climax ducking, comedy-timing ki 4-act durations, clean-cut ki frame-accuracy tarkeebein. Apne shabdon me note: `notes_mmmnhat_agent-skills.md`. Verbatim content NAHI liya gaya. (0 stars, 46 commits, repo page 2026-11-06.)

## 10. dvschultz/adobe-hut — Adobe UXP/ExtendScript knowledge base (.claude skills + agents)
- **Wajah:** **Koi licence nahi mila** (repo page ki details me licence line nahi, clone me bhi LICENSE nahi). Upar se iska vishay plugin development ke APIs hain, editing craft nahi.
- Link: https://github.com/dvschultz/adobe-hut
- Note: AE expression/scripting aur Premiere UXP ke ~50 skill files + expert agents hain — sab API reference. Pehchan ke liye apne shabdon me chhota note: `notes_dvschultz_adobe-hut.md`. Verbatim content NAHI liya gaya. (24 stars, 129 commits, repo 2013 se, repo page 2026-11-06.)

## 11. hetpatel-11/Adobe_Premiere_Pro_MCP — Premiere Pro MCP server (is round ka sabse bada Premiere repo)
- **Wajah:** Licence **MIT hai (qualify karta hai)**, lekin ye ek shudh **tool server** hai (283 tools); iske saath bandhi `skills/premiere-pro-mcp` skill sirf tool ko install/verify/surakshit istemal sikhata hai — editing technique isme hai hi nahi. Qwen-MM-Plugins (entry 5) wala hi ilaaj: record me hai, extraction nahi.
- Link: https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP
- Note: 824 stars, 153 forks, 173 commits (repo page, 2026-11-06) — Premiere side ki khoj me popularity ke hisaab se ye sabse upar tha, lekin popularity tool ki hai, technique ki nahi.

## 12. leancoderkavy/premiere-pro-mcp — Premiere Pro MCP server (npm)
- **Wajah:** Iske apne README ke mutabiq **MIT** hai, lekin ye bhi ek **tool server** hai (436 tools, npm package `premiere-pro-mcp`) — technique content nahi, isliye extraction nahi.
- Link: https://github.com/leancoderkavy/premiere-pro-mcp
- Note: Entry 11 ke saath koptsev63 ke README me bhi iska zikr "hundreds of typed tools" wale bade servers me aata hai. Isi family ke aur variants (0xTrip/adobe_premiere_pro_mcp, compimprove/adobe-premiere-mcp) bhi khoj me dikhe — sab tool servers/forks hain; unki licence alag se verify nahi ki gayi kyunki category hi tool hai.

## 13. yumehiko/ae-agent-skills — After Effects declarative/CLI agent skills (Japanese)
- **Wajah:** Licence **MIT hai (qualify karta hai)**, lekin dono skills (aftereffects-declarative, aftereffects-cli) lekhak ke **apne hi tool** ko chalane ki vidhi hain — declarative wali skill ka "scene design rules" hissa asal me uske apni JSON scene-schema ke niyam hain (upsert keys, keyframeMode, propertyPath conventions). Transferable AE craft nahi hai; entry 11 wala hi ilaaj.
- Link: https://github.com/yumehiko/ae-agent-skills
- Note: 38 stars, 61 commits, 18 releases (repo page, 2026-11-06); skills Japanese me hain. Agar aage kabhi is declarative workflow ko apnana ho to repo kaam ka hai — lekin harvest ke liye isme editor-technique nahi mili.
