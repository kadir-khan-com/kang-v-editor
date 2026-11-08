# Licence + citation audit — creative_layer_2026-11-06_v2

Audited: 2026-11-06 (IST). Package: `kang/incoming/creative_layer_2026-11-06_v2/` (not modified).
Machine-readable: `licence_audit.json` (46 rows: 44 harvest files + QwenLM + browser-use/video-use) and `citation_audit.json` (40 rules).

**How I checked**
- **Licences:** I made one GitHub API call per repo, but the unauthenticated limit ran out after 26 calls. 18 repos came back 403. For every repo, the real check was a `git clone --depth 1`: I read the root LICENSE file, every nested LICENSE*, and any `license:` lines in SKILL.md front matter.
- **Repo status:** "Last activity" is the API `pushed_at` when I got it, otherwise the date of the clone's HEAD commit. The API only gave archived flags for the 26 repos it answered.
- **Citations:** For each rule I opened the harvest file and the matching upstream file in the clone. For the science rules I also opened Zacks et al. 2010 (Frontiers, full text) and Tim Smith's *Alexander Nevsky* chapter (Birkbeck PDF).

---

## 1. Licence verdicts

| Verdict | Count |
|---|---|
| OK (MIT / Apache-2.0) | 34 |
| OK, but must credit expocut.com | 1 (expocut) |
| IDEA_ONLY (ideas only, no text) | 8 (all `notes_*` files) |
| UNVERIFIED | 1 (pifferologo, repo 404) |

The licence claimed in each harvest-file header matches what I found, apart from the points below.

### Points that change something
1. **`github_pifferologo_ai-agent-video-editor.md`: UNVERIFIED.** The repo is gone (HTTP 404, and clone asks for credentials).
   - 122 of the 149 long lines in the harvest appear word-for-word in **browser-use/video-use `SKILL.md`**. That repo exists, is **MIT** ("Copyright (c) 2026 Browser Use") and had its last commit on 2026-10-08.
   - **Fix:** re-cite these 14 rules to `https://github.com/browser-use/video-use`: R-085, R-086, R-133, R-195, R-196, R-197, R-198, R-199, R-256, R-257, R-258, R-259, R-260, R-261. Then the MIT licence is verifiable.
2. **`notes_eacp1991_premiere-agent.md`: the repo is a fork of `Kemerd/premiere-agent`, whose licence is PolyForm Noncommercial 1.0.0.** That is an explicit non-commercial licence, which is stronger than "no licence". IDEA_ONLY stands.
   - Some of its text (for example the 30–200 ms padding rule) comes from MIT video-use. Those ideas can be cited to video-use instead.
3. **`notes_ADAM-0S_wayland-m3ta-0s.md`: the repo is a fork of `FerroxLabs/wayland` (AGPL-3.0).**
   - The skill's front matter says `license: Apache-2.0, author: foundry-skills`.
   - A search found no separate Apache-licensed source for it, so the repo's AGPL-3.0 licence governs. IDEA_ONLY.
4. **`notes_mmmnhat_agent-skills.md`: mixed.** The repo has no LICENSE file.
   - `skills/clean-cut/SKILL.md` and `skills/video-transform/SKILL.md` say `license: MIT` in their own front matter.
   - comedy-timing, pacing-editor and visioncut carry no licence at all. So R-277…R-283 stay IDEA_ONLY.
   - clean-cut content could be argued MIT on that self-declaration alone, but the claim is weak.
5. **expocut:** the repo LICENSE is MIT, but 17 skill files say "Free to use and redistribute with attribution to expocut.com". Credit expocut.com wherever its content is used.
   - R-201 relies only on expocut. R-095 cites it alongside other sources.
6. **MuhammadAsad809:** the GitHub API says NOASSERTION. The LICENSE is MIT text with the last liability sentence cut off, but the permission grant is intact, so I treated it as MIT (OK).
7. **koptsev63:** the `trailer-bridge` SKILL.md calls itself a "PAID PACK ($19)". It sits inside the MIT repo with no licence of its own, and MONETIZATION.md says the code is MIT. OK, flagged for awareness only.
8. **Archived repos:** Francesco149/slopstudio and Maciejdziuba/youtube-skills (API `archived=true`). LobzyJay has been renamed (API 301); the clone still works.
9. **Other confirmations:**
   - chvndler: README says ISC, LICENSE file is MIT. Both are permissive.
   - kmilo: front matter says MIT for code and text, CC0 for the bundled assets.
   - tryskilly: both extracted skills are Apache-2.0.
   - TerminalSkills: 1,110 skill front-matter entries say Apache-2.0.

### No subfolder licence that differs from the repo, except
- mmmnhat (two skills self-declare MIT in a repo with no licence),
- expocut (skill-level attribution clause),
- ADAM-0S (front matter says Apache, repo is AGPL),
- koptsev63 `skills/watch` (its own MIT; same licence as the repo).

---

## 2. Discrepancy: QwenLM/Qwen-MM-Plugins

**The package's claim is wrong.** INDEX entry 5 says the repo has "no technique content". It does.
- **The skill exists:** `src/capabilities/video-edit/skill/SKILL.md` describes itself as an "editing director" skill for real footage. It covers selection, pacing, beat-sync, sound and looks.
- **It has numeric pacing rules:** `craft/pacing-rhythm.md` (125 lines) includes:
  - shot length 0.5–2 s for fast-cut and 3–8 s for slow-cut,
  - narrated pieces cut every 4–6 s, with no shot longer than ~7 s,
  - a "comfort budget" of at least 2.6–3.0 s between camera changes,
  - the opening hook landing inside 1.5 s,
  - cuts on word boundaries with 30–200 ms padding.
- **More craft files:** `audio-first-cutting.md`, `music-beat-sync.md`, `transitions.md`, `sound-mix.md`, `footage-grading.md`, `camera-rig.md`.
- **Licence:** Apache-2.0 (root LICENSE). The skill folder has no licence of its own. The bundled fonts are MIT and OFL. Last commit 2026-11-01. **It qualifies and was never harvested.**

---

## 3. Citation spot check (40 rules)

| Tag | Sampled | SUPPORTED | PARTIAL | MISLABELLED_EVIDENCE | NOT_FOUND |
|---|---|---|---|---|---|
| 🟢 | 10 (all) | 1 | 2 | 7 | 0 |
| 🟡 | 15 | 10 | 2 | 3 | 0 |
| 🟠 | 15 | 14 | 1 | 0 | 0 |
| **Total** | **40** | **25** | **5** | **10** | **0** |

**Every number I checked was found in its cited source.** The problems are about what the numbers are claimed to prove, not about invented numbers.

### 🟢 (9 of 10 are not clean)
Only **R-089** (Mayer coherence/redundancy, cited via kmilo) holds up as 🟢.

**Zacks rules (R-055, R-057, R-177, R-178).** The study details in the harvest are correct: n=24, *The Red Balloon*, and situation changes mediating the boundary response. But the rules are design prescriptions the paper never tested. The harvester applied the right standard to the Cutting rules (finding 🟢, rule 🟡) but not here.
- **R-178 goes against the paper:** it says a mid-event cut "forces a model update". Zacks 2010 reports that "cuts in and of themselves were not associated with increases in segmentation".

**Tim Smith rules (R-126, R-140, R-232).** Smith's own chapter says the match-on-action and continuity analyses "are observational and based on hypotheses … derived from post-hoc analysis". The replicated result is gaze clustering in general, not these cutting rules. They should be 🟡.

**Other 🟢 rules:**
- **R-088:** the strict "exact noun or nothing" part is a mktkit house rule, so it is 🟠 content under a 🟢 tag.
- **R-135:** the 4–5 s figure is in kmilo, but kmilo calls it "a reference, not a target" and says talking-head YouTube cuts faster. The rule adds "don't go much faster", which the source contradicts.

### 🟡
- **R-035:** "payoff in the last 15–25%" comes from slopstudio's desk-research document (YouTube official + MrBeast/Paddy), not from the measured 5-video corpus. Should be 🟠.
- **R-171:** the "70–80% retention at end screen" figure is an unsourced bullet in an AI-written MrBeast profile. Should be 🟠.
- **R-422:** the transition percentages are a house budget built in reaction to one film. Should be 🟠.
- **R-001 (PARTIAL):** the 5 s check is applied to long-form too, but the YouTube guidance it cites is about the first 30 s.
- **R-173 (PARTIAL):** "3–6 s" is the harvester's own band, not a Cutting number. The rule's "why" also mixes up the 2010 study (150 films) with the 2011 figures (160 films).

### 🟠 (all fine except one)
- **R-338 (PARTIAL):** the source rule is scoped to teasers; the rule applies it to every sequence.
- **R-440:** comes from Blackmagic's official Fairlight manual, so 🟠 is conservative.

### Systemic finding (outside the sample, but grounded in the source text)
slopstudio's SKILL.md explicitly marks only some numbers as "measured":
- words and cuts in the first 30 s,
- the 2.8–7.5 cuts/min range,
- flat per-minute pacing,
- 160–195 WPM.

Everything else in that file comes from its desk-research document. Yet the package tags **R-033, R-034, R-036, R-037, R-043, R-044, R-164, R-165** as "measured reference corpus". These are very likely mislabelled the same way as R-035. Two examples:
- the APV 40–55% band comes from vendor runtime bands in `docs/research/llm-video-tooling-2026-07.md`,
- the Shorts rules come from AGENT_TOOLING.

I did not score these individually.

The "measured" corpus behind the slopstudio 🟡 rules is n=5. Its data file (`../slopstudio-projects/.../SYNTHESIS.md`) is outside the public repo, so it cannot be checked.

---

## 4. Rules relying ONLY on IDEA_ONLY sources (reword or drop): 32

| Source | Rules |
|---|---|
| ADAM-0S (AGPL) | R-262, R-263, R-264, R-265, R-267, R-268, R-269, R-270, R-271 |
| eacp1991 (fork of PolyForm-NC) | R-273, R-274, R-275, R-276 |
| mmmnhat (no licence) | R-277, R-278, R-279, R-280, R-281, R-282, R-283 |
| appariciojunior (CC BY-NC) | R-373, R-392, R-419, R-459, R-462 |
| SamuelAde001 (no licence) | R-386, R-387, R-404, R-405 |
| edwinponcious12 (no licence) | R-388 |
| AdamGarceau (no licence) | R-451, R-460 |

- **Rewording:** the rule text is already a Hinglish paraphrase. A 7-word overlap check against the upstream texts found only **R-405**, which reuses a short list of terms ("duplicate takes, misspeaks, garbled audio, flash frames, redundancy"). That overlap is trivially small; reword it anyway.
- **R-275 can move to a licensed source:** the 30–200 ms margin idea also exists in MIT browser-use/video-use.
- **Mixed (an IDEA_ONLY source plus a qualifying one; the qualifying one carries the rule):** R-266, R-272, R-372, R-379, R-402, R-403.

**Related lists:**
- **Re-cite to browser-use/video-use** (pifferologo-only, licence UNVERIFIED): R-085, R-086, R-133, R-195–R-199, R-256–R-261. R-194 cites pifferologo plus blazerior and needs no change.
- **expocut-only, needs credit to expocut.com:** R-201.

---

## Not done / limits
- I did not re-verify the INDEX entries that were not harvested (Dreydrey9000, OpenChatCut, Kaestral-pro, Andrea13235, yunpeng1998, GuanYixuan, samuelgursky, hetpatel-11, leancoderkavy, yumehiko). The exception is QwenLM, as asked.
- I did not open these primary sources myself: Mayer 2008, Guo 2014, Cutting 2010/2011, the BBC and Netflix guides. My verdicts on those rules rest on the cited skill text, and the notes say so.
- The Zacks 2010 and Smith chapter checks are against the primary texts.
- Clones were kept in `/tmp/ac/cl` (not in the project) and will not persist.
