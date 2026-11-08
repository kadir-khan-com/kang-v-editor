# KANG — Science verification (creative_layer_2026-11-06_v2)

Date: 2026-11-06. Scope: the 4 science files in `step_1_harvest_gyaan/`, the 10 🟢 rules, and the 🟡 rules that cite science, in `step_2_rules/rules.json`. The package was read only, not changed.
New rules proposed from this work are in `science_rules_proposed.json` (same folder).

Status words: **VERIFIED** (the primary source I opened says it) · **CORRECTED** (the primary source says something different; the correct value is given) · **UNVERIFIABLE** (I could not open a primary source for it, so it stays unconfirmed).
I opened every source listed under "Sources opened". Nothing here is cited from a search snippet alone.

---

## 1. Headline findings (read this first)

1. **The "ASL 15 s → 3.5 s" figure is wrong as quoted.** Cutting et al. 2011 (i-Perception) says ASL went from **about 10 s (1930s–40s) to under 4 s after 2000**, across 160 films (1935–2010). The 15→3.5 figure comes from Tim Smith's paraphrase in a non-peer-reviewed dialogue. Cutting 2018 repeats it: about 10 s/shot in 1950 → about 4 s/shot in 2010.
2. **No evidence that 1/f pacing makes films better liked.** Cutting 2010 tested this: IMDb ratings did **not** correlate with 1/f slope (r = −.089, n.s.). The authors call 1/f an "emergent" result, not something editors aim for. The science file left this out.
3. **"A cut at an event boundary feels invisible" is wrong.** Smith & Henderson 2008 measured it: cuts *between* scenes were the **most** noticed (only 9.4% missed). Cuts *inside* a scene were missed far more often (25.1%, and 32.4% for match-action cuts). A boundary cut gets noticed, but viewers read it as meaningful. Schwan 2000 adds that cuts placed at breakpoints give **better recall**.
4. **"A mid-event cut reads as a jolt or error" is contradicted.** Zacks 2010: "Cuts in and of themselves did not produce increases in segmentation." Schwan 2000: viewers' segmentation was "largely unaffected by the occurrence of cuts." What *does* hurt memory is a big **break** (an ad break) placed mid-event (Boltz, as reported in the Zacks 2007 review). For a stills-based vlog this matters: many photo changes inside one event are fine.
5. **For a place change alone, the boundary is weak.** Magliano & Zacks 2011: action discontinuities had the biggest effect on segmentation; space and time changes had "minor effects." A new section should change the **goal or action**, which narration can do, and not just the place.
6. **Clutter is not an attention lever.** Cutting 2018: luminance, clutter and shot scale "seem not to be important to holding viewers' moment-to-moment attention." R-231's reason is not supported. Mayer's coherence principle supports decluttering *graphics*, not photo framing.
7. **Murch's weights are exactly right** (51/23/10/7/5/4) and so is the "slightly tongue-in-cheek" quote. They are opinion, as tagged.
8. **Our format ≠ Hollywood.** Every film finding comes from live-action Hollywood features with motion inside the shots. KANG is mostly stills, maps and cards with narration. Film shot-length numbers should be benchmarks, not checks. Multimedia-learning research (Mayer) and caption research fit our format better, and the new rules lean on them.

---

## 2. Claim table — science_james_cutting.md

| # | Claim in file | Status | Correct value / note | Source opened |
|---|---|---|---|---|
| C1 | Cutting, DeLong & Nothelfer 2010, *Psych Sci* 21(3) 432–439, 150 films 1935–2005 | VERIFIED | 10 films per year, every 5 years, 1935–2005 | jordandelong.com PDF |
| C2 | Shots per film 231 (*Seven Year Itch*) to 3,099 (*King Kong* 2005), mean ≈1,132 | VERIFIED | exact | same |
| C3 | Shot-length sequences moved toward 1/f; neighbouring shots more correlated | VERIFIED | AR index vs year r = .43–.45; slope steepening r = .19 (linear), .28 (polynomial) | same |
| C4 | "1/f causes better attention-holding is interpretation" | VERIFIED + ADD | Stronger than the file says: ratings did **not** track 1/f (r = −.089 n.s.); authors: 1/f is "emergent… not intentional" | same |
| C5 | ASL fell ≈15 s → ≈3.5 s across 160 films 1935–2010 (Cutting et al. 2011) | **CORRECTED** | Primary text: "ASLs of about 10 s in the 1930s and 1940s falling to below 4 s after 2000" (r = −.75). 15→3.5 is Smith's paraphrase. | PMC3485803; Smith–Christie dialogue PDF |
| C6 | Modern films: more motion, shorter scenes, fewer dissolves, more close-ups, less clutter, higher contrast | PARTLY VERIFIED | 2011 paper confirms shorter shots, more motion, **darker** (left out of the file), and shorter shots carrying more motion. The rest is from Wikipedia only. | PMC3485803; Wikipedia |
| C7 | 2018 follow-up: motion, sound amplitude, scene durations adapted to attention | VERIFIED + ADD | Cutting, DeLong & Brunick 2018 *CRPI*. Also says luminance, clutter and shot scale are **not** important for moment-to-moment attention. | PMC5849648 |
| C8 | 300+ films, 1915–2015 programme | VERIFIED (loosely) | 2018: "almost twice as many movies released over a century" | PMC5849648; Wikipedia |
| C9 | Climax pattern (shorter shots into the climax, longer after) — "search abstract only" | **VERIFIED now** | Cutting 2016 *CRPI* 1:30: shorter shots and more motion in the first part of the climax, then longer shots and less motion at its end. The setup has *lengthening* shots. | PMC5256470 |
| C10 | "Modern ASL band ≈3–6 s" (R-CUT-1) | OPINION | Not in any paper. Cutting gives ≈4 s (whole-film mean, Hollywood) | — |
| C11 | Footnote: a 90 s run of ~1 s shots "could not be sustained" | VERIFIED as authors' opinion | Not an experiment | jordandelong.com PDF |

## 3. Claim table — science_tim_smith.md

| # | Claim | Status | Correct value / note | Source opened |
|---|---|---|---|---|
| S1 | Smith 2012, AToCC, *Projections* 6(1) 1–27 | VERIFIED | | Birkbeck eprint 6679 PDF |
| S2 | The cut replaces a natural attention shift; match-action, matched exits, shot/reverse-shot, 180° explained by attention | VERIFIED (theory) | Theory paper, not an experiment | same |
| S3 | Attentional synchrony (Mital, Smith et al. 2011) | VERIFIED | *Cognitive Computation* 3:5–24 | Mital et al. PDF |
| S4 | Attention "pulled involuntarily" by motion, faces, speech | **CORRECTED** | Mital 2011: motion predicts gaze clustering, but "it is currently unclear whether this influence is involuntary or due to correlations with higher order factors" | Mital et al. PDF |
| S5 | Match-action timing: cut "just after" the action begins | CORRECTED (minor) | AToCC: cut "timed to coincide with the onset of the action" | AToCC PDF |
| S6 | Gaze clustering "replicated by numerous studies" (Stelmach first) | VERIFIED | Smith's own words in the *Alexander Nevsky* chapter | Birkbeck eprint 12587 PDF |
| S7 | Edit blindness (Smith & Henderson 2008), marked "secondary only" | **VERIFIED now** | *JEMR* 2(2):6. Missed cuts: between-scene 9.4%, gaze-match 10.9%, within-scene 25.1%, match-action 32.4%. "A quarter… increased to a third with sudden onset of motion." Blinks or saccades at cuts were negligible (~1%); most misses come from inattention. | bop.unibe.ch JEMR PDF |
| S8 | Bond/Bay: centre fixation, fatigue, habituation | VERIFIED as Smith's statement | Centre bias is from his eye-tracking ("Smith, in press"). "Fatigue/habituation/bored" is his interpretation, in a non-peer-reviewed dialogue. | Smith–Christie dialogue PDF |
| S9 | Points of high motion predict where and when synchrony happens | VERIFIED | Flicker and motion were the most predictive features | Mital et al. PDF |

## 4. Claim table — science_jeffrey_zacks.md

| # | Claim | Status | Correct value / note | Source opened |
|---|---|---|---|---|
| Z1 | Zacks, Speer, Swallow, Braver & Reynolds 2007, *Psych Bull* 133(2) 273–293, states EST | VERIFIED | | PMC2852534 |
| Z2 | Zacks, Speer, Swallow & Maley 2010, *Front Hum Neurosci* 4:168 | VERIFIED | | PMC2955413 |
| Z3 | n = 24, *The Red Balloon*, fMRI during passive viewing | VERIFIED | 24 participants (12 male, aged 19–28); 6 more excluded | same |
| Z4 | Boundary responses mediated by situation changes (characters, objects, location, goals, causes) | VERIFIED | Abstract wording matches | same |
| Z5 | "More simultaneous change = stronger boundary response" (mediation) | **CORRECTED** | It is a *behavioural* result: "the probability of segmenting during a 5-s interval increased with the number of situation changes." The mediation result is separate. | same |
| Z6 | (missing) Cuts alone | ADD | "Cuts in and of themselves did not produce increases in segmentation." | same |
| Z7 | Viewers agree on boundaries; boundaries are remembered better | VERIFIED | 2007 review: good agreement (Newtson 1976); "event boundaries are remembered better than non-boundaries" | PMC2852534 |
| Z8 | Zacks et al. 2001 fMRI | UNVERIFIABLE here | Cited inside the papers only; not opened | — |
| Z9 | Magliano & Zacks 2011 (asked to check) | VERIFIED + ADD | *Cog Sci* 35:1489–1517. Action discontinuities had the biggest effect; space/time had minor effects. With situation change controlled, cuts were *negatively* tied to boundaries. | PMC3208769 |
| Z10 | (new support) Boundary placement helps memory | ADD | Schwan, Garsoffky & Hesse 2000, n = 40: "Cuts accompanying a breakpoint lead to more detailed recall." Swallow, Zacks & Abrams 2009: objects present at boundaries are recognised better. | Springer abstract; PMC2819197 |

## 5. Claim table — science_walter_murch.md

| # | Claim | Status | Note | Source opened |
|---|---|---|---|---|
| M1 | Six criteria in order, weights 51/23/10/7/5/4 | VERIFIED | exact | Berkeley iSchool blog (verbatim pp. 17–20) |
| M2 | "Slightly tongue-in-cheek, but not completely" | VERIFIED | | same |
| M3 | Sacrifice from the bottom up; never give up emotion before story | VERIFIED | | same |
| M4 | Higher criteria hide lower problems, "but not vice versa" | VERIFIED | | same |
| M5 | Top three bound "like protons and neutrons" | VERIFIED | | same |
| M6 | "Never accept less when more is available" | VERIFIED | | same |
| M7 | Book: Silman-James 1995, pp. 17–20 | VERIFIED (as stated by the blog) | Page numbers per the blog | same |
| M8 | Cross-validation: eye-trace = Smith's synchrony | FAIR | Same idea, but the measured result (S7) shows gaze-match cuts were *not* the hardest to spot (10.9% missed) | JEMR PDF |
| M9 | (related, R-339) Blink as the natural cut point | NOT SUPPORTED as the reason cuts go unseen | Smith & Henderson 2008: blinks at cut moments ~1%; misses are mostly inattention. The blink idea stays 🟠 craft. | JEMR PDF |

Counts (39 rows): **VERIFIED 31** (including rows marked verified now / + add / fair / as stated) · **CORRECTED 5** (C5 ASL, S4 involuntary, S5 cut timing, Z5 mediation wording, M9 blink mechanism) · **PARTLY VERIFIED 1** (C6) · **OPINION, no source 1** (C10) · **UNVERIFIABLE 1** (Z8) · plus **4 missing facts added** (C4 ratings, C7 clutter, Z6 cuts alone, Z10 recall).

---

## 6. Green-tag (🟢) review — all 10

| Rule | Verdict | What changes |
|---|---|---|
| **R-055** Deliberate boundary = reset | 🟢 core, **reword** | Boundaries come from situation change (Zacks 2010), and memory updates there (Swallow 2009). "Attention reset button" is a metaphor and is not measured. Make the change a **goal or action** change (Magliano & Zacks: place/time alone is minor). See S-012. |
| **R-057** Chunk = one event | 🟢 **justified** | Add Schwan 2000 (breakpoint cuts → more detailed recall) and Boltz (breaks at non-boundaries hurt memory, via the 2007 review). |
| **R-088** B-roll exactness | **Overreach → 🟡** (core) / 🟠 (parts) | Mayer's coherence principle is about removing extra material. It does not say a same-category photo is a "defect." Temporal contiguity (d = 1.31) supports "show what is said, when it is said." "Exact or nothing" and "video always before photo" are house opinion (🟠). The evidence comes from short science lessons, not vlogs. |
| **R-089** Graphic only when it explains | 🟢 **justified** | Redundancy d = 0.72 (Mayer 2008). Adesope & Nesbit 2012: key terms beat verbatim text. Caveat: full same-language captions are a different case (see S-002). |
| **R-126** One attentional magnet per shot | **Overreach → 🟡** | Mital 2011 shows motion predicts clustering. "Two magnets break synchrony" was not tested in what I opened, and Mital says involuntariness is unclear. For stills, the magnets are faces, text and contrast; no study covers stills. |
| **R-135** Film pacing benchmark ~4–5 s | **Number corrected; rule → 🟡** | Cutting 2011/2018: about 4 s around 2010, under 4 s after 2000. The number is 🟢 as a measurement. Using it as a target for a stills vlog is not. Film shots carry motion; shorter modern shots carry more motion (Cutting 2011). |
| **R-140** Cut on action | 🟢 for live-action CC clips, **scope it** | Match-action cuts are the most missed (32.4%). Smith says time the cut to the action onset. The "never cut on a blink" clause is Murch, not data (🟠). Little use for stills. |
| **R-177** Cut at situation change | 🟢 action, **wrong "why"** | Placing cuts or breaks at situation changes is supported (Zacks 2010; Schwan 2000). The claim that the cut "feels invisible" is false: between-scene cuts were the most detected (9.4% missed). Rewrite the why as "the cut is noticed but read as meaningful, and recall improves." |
| **R-178** No mid-event cuts | **Overreach / partly contradicted → 🟡** | Cuts alone do not create boundaries (Zacks 2010; Schwan 2000), and within-scene continuity cuts often go unnoticed (25%). What is supported: don't place a big *break* (chapter card, music stop, long transition) mid-event. See S-011 and S-013. |
| **R-232** Eye-trace landing | **Overreach → 🟡** | This is AToCC theory plus film examples. No experiment I opened tested it as a rule. A simpler measured fact: for about 1.2 s after onset, gaze goes to screen centre (Smith & Henderson 2010 VSS abstract; central tendency in Mital et al. 2011). See S-017. |

**Score: 2 justified as-is (R-057, R-089) · 3 justified after rewording (R-055, R-140, R-177) · 5 should drop to 🟡 (R-088, R-126, R-135, R-178, R-232).**

### Hollywood → YouTube overreach (general)
- All Cutting, Smith and Zacks data comes from feature films, mostly live action, watched in a lab. None comes from YouTube, phones, Hindi audiences or still-photo edits.
- Mayer-type effects are biggest for low prior knowledge, complex material and **system-paced** media, and video is system-paced (Noetel et al. 2022). That makes them a better fit for KANG than film cinemetrics. They still come from short lessons with mostly college students, and they measure learning, not retention.

## 7. 🟡 rules that cite science

| Rule | Verdict |
|---|---|
| R-056 one dimension at a time | Keep 🟡. Fix the wording: more changes raise the *probability* of a boundary (behavioural), not "the mediation result." The "use sparingly" dose is still inference. |
| R-173 ASL 3–6 s (hard check) | Keep 🟡, but **do not run it as a hard check on long-form stills.** The band is opinion (Cutting gives ~4 s for films with motion). It also conflicts with R-394 (travel reference avg ~10.4 s). Make it profile-specific or a warning. |
| R-174 1/f waves | **Drop to 🟠.** Cutting 2010 tested liking (IMDb) and found no link. The authors call 1/f emergent, not a technique. |
| R-175 climax compression | Keep 🟡 and mark it **VERIFIED** (Cutting 2016 abstract). Add: shots lengthen at the *end* of the climax and through the setup. |
| R-176 speed ceiling | Keep 🟡. Add Lang et al. 1999 (fast pace + arousing content → less recognition and recall; peer-reviewed). "Fatigue/boredom" is Smith's opinion in a dialogue. |
| R-231 declutter frame | **Drop to 🟠** as an attention claim (Cutting 2018: clutter does not matter for moment-to-moment attention). Keep decluttering for graphics under coherence (S-010). |
| R-087 YouTube chapters (00:00, ≥3, ≥10 s) | **VERIFIED** on YouTube Help. The 3–5-word promise title is craft. |
| R-091 text time = words×0.33+0.5 | Base VERIFIED: BBC 160–180 wpm = 0.33–0.375 s/word; minimum ≈0.3 s/word. Note 0.33 s/word ≈ 180 wpm, the fast end. This is English guidance; Hindi needs a cps measure (S-003). |
| R-092 Netflix caption specs | English VERIFIED (42 chars, 2 lines, 20 cps adult / 17 kids, 5/6 s to 7 s). **For Hindi: 22 cps adult / 18 kids** (Netflix Hindi guide). The "2-frame gap" is not on the General Requirements page I opened (UNVERIFIED here). |
| R-153 6-minute blocks (Guo 2014) | VERIFIED: "median engagement time is at most 6 minutes, regardless of total video length," from 6.9M sessions. Scope: edX MOOC lectures, 2012, engagement time (not learning). Weak transfer to travel vlogs. |
| R-163 narration 160–195 wpm | Not science (creator corpus). BBC R&D (2015, English news clips): ~175 wpm "about right", ~230 "too fast", ~115 "too slow." The Dwarika measurement of 200 wpm is inside that. English wpm bands should not fail Hindi narration (S-022). |
| R-001 promise first | YouTube official (opened): "Intro" = % of viewers still watching after **30 s**; advice is to match the title/thumbnail and rework the first 30 s. YouTube does **not** state the 5 s threshold, so that part is creator data. |

---

## 8. New evidence found (summary; rules in the JSON)

**(a) Mayer multimedia principles**
- Mayer 2008 *Am Psychol* 63(8) 760–769: coherence d = 0.97 (13/14 tests); signaling 0.52 (6/6); redundancy 0.72 (5/5); spatial contiguity 1.12 (5/5); temporal contiguity 1.31 (8/8); segmenting 0.98 (3/3; *learner-paced*); pretraining 0.85 (5/5); modality 1.02 (17/17). Lab studies with short science lessons.
- Noetel et al. 2022 *Rev Educ Res* (29 reviews, 1,189 studies): spatial contiguity g = 0.63; temporal contiguity g = 0.78; signaling g = 0.43 (k = 209); removing seductive details g = 0.33, and **0.43 when the detail stays on screen vs 0.12 when transient**; segmenting g = 0.32/0.36; captions for second-language video g = 0.99. Good design matters more in system-paced media.
- Adesope & Nesbit 2012 (57 studies): adding text to audio helps (g = 0.29); adding audio to text does not (−0.04). The gain disappears when pictures or animation are present. **Key terms beat verbatim text.**
- Schneider et al. 2018 (signaling meta-analysis): g = 0.43 on learning (k = 209), as reported inside Noetel 2022. The split into retention/transfer seen in search snippets was not opened, so it is not used.

**(b) Captions / subtitles**
- Netflix Hindi TTSG: 42 chars/line, 2 lines, **22 cps adult**, 18 kids (SDH 25/20). Netflix general: 5/6 s to 7 s per event. Netflix counts spaces and punctuation in cps.
- BBC guidelines: 160–180 wpm (0.33–0.375 s/word). For 9:16 vertical, about **25 characters** per line equals 37 in 16:9.
- Szarkowska & Gerber-Morón 2018 *PLOS One* (n = 74, eye-tracking, 12/16/20 cps): viewers cope with fast subtitles; **slow subtitles caused more re-reading and less enjoyment.**
- BBC R&D 2015: the best subtitle speed is the speech speed; verbatim is preferred.
- India: Kothari & Bandyopadhyay 2014 *ITID* (n = 7,409, 5 Hindi states, 2002–2007): same-language subtitles on Hindi film songs → greater literacy gains. This is direct evidence for our audience.

**(c) Motion on stills (Ken Burns)** — **No direct study of Ken Burns on adults was found.** Closest evidence:
- Smith & Henderson 2010 (VSS abstract): gaze clusters more for dynamic than static versions of the same scene (15% vs 20% of the screen). The first ~1.2 s after onset goes to screen centre.
- Takacs & Bus 2016 *Front Psychol* (children, n = 39): motion matched to narration drew more fixation to the named detail and gave better story recall.
- Kumar, Viswanathan & Bapna 2026 *ISR* (children's YouTube, A/B ads): more background motion → higher view-rate. It shortened long look-aways and did not reduce attention to the content. Children only.

**(d) YouTube official** — Chapters rules (00:00, ≥3, ≥10 s) verified. The Retention help page defines "Intro" as the first 30 s and lists spikes, dips and top moments.

**(e) Pacing / load** — Lang et al. 1999 *JBEM*: fast pace + arousing content overloads processing and lowers recognition and recall. Guo 2014: median engagement ≤6 min.

**(f) Emotion / music** — skipped, as asked.

## 9. Gaps (honest)
- No study on Hindi/Hinglish caption cps for *same-language* captions on YouTube. The Netflix 22 cps is an industry spec for translated subtitles.
- No study on YouTube retention vs edit pace that I could open. Creator corpora stay 🟡.
- No adult study of Ken Burns moves (direction, speed, % zoom). R-329's 2–6% stays 🟠.
- Zacks 2001 and Boltz 1992 were cited through other papers only.

## Sources opened
- https://jordandelong.com/pubs/2010/AttentionEvolution.pdf
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/ (Cutting et al. 2011)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5256470/ (Cutting 2016)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5849648/ (Cutting et al. 2018)
- https://en.wikipedia.org/wiki/James_E._Cutting
- https://eprints.bbk.ac.uk/id/eprint/6679/1/6679.pdf (Smith 2012 AToCC)
- https://bop.unibe.ch/JEMR/article/download/2264/3460 (Smith & Henderson 2008)
- http://jhenderson.org/vclab/PDF_Pubs/MitalSmithHillHenderson_CC2011.pdf
- https://ualresearchonline.arts.ac.uk/id/eprint/21181/2/616c90e6-d98c-4117-bccf-74eaf857b1ae.pdf (Smith–Christie dialogue)
- https://eprints.bbk.ac.uk/id/eprint/12587/1/Alex_Nev_CogMediaTheory_2014_timjsmith_figs.pdf
- https://ualresearchonline.arts.ac.uk/id/eprint/21095/ (Smith & Henderson 2010 VSS abstract)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2852534/ (Zacks et al. 2007)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2955413/ (Zacks et al. 2010)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3208769/ (Magliano & Zacks 2011)
- https://link.springer.com/article/10.3758/BF03213801 (Schwan et al. 2000)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2819197/ (Swallow et al. 2009)
- https://blogs.ischool.berkeley.edu/i290-viznarr-s12/the-rule-of-six-walter-murch/
- https://jgregorymcverry.com/readings/mayerprinciplesofmultimedialearning2008.pdf (Mayer 2008)
- https://journals.sagepub.com/doi/10.3102/00346543211052329 (Noetel et al. 2022)
- https://psycnet.apa.org/journals/edu/104/1/250.html (Adesope & Nesbit 2012)
- https://partnerhelp.netflixstudios.com/hc/en-us/articles/115003196707-Hindi-Timed-Text-Style-Guide
- https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/
- https://www.bbc.co.uk/rd/blog/2015-09-how-fast-should-subtitles-be
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6007935/ (Szarkowska & Gerber-Morón 2018)
- https://itidjournal.org/index.php/itid/article/view/1307.html (Kothari & Bandyopadhyay 2014)
- https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01591/full (Takacs & Bus 2016)
- https://pubsonline.informs.org/doi/abs/10.1287/isre.2023.0718 (Kumar et al. 2026)
- https://support.google.com/youtube/answer/9884579 (Chapters)
- https://support.google.com/youtube/answer/9314415 (Retention key moments)
- https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf (Guo et al. 2014)
- https://www.tandfonline.com/doi/abs/10.1080/08838159909364504 (Lang et al. 1999)
- Schneider et al. 2018 and Alpizar et al. 2020 (signaling): only their numbers as reported inside Noetel 2022 are used.


---
## 10. Proposed rules
`science_rules_proposed.json` has 22 rules (S-001 to S-022): 9 🟢 and 13 🟡; 11 samajh, 4 rhythm, 4 style, 3 kahani; 8 with a machine check. Two check kinds are new and need engine support: `max_cps` and `must_align`. Each rule has a `relation_to_existing` field (NEW / DUPLICATES / MODIFIES / CORRECTS + rule ids). Thresholds that are editorial are marked as such in `evidence_note`.
