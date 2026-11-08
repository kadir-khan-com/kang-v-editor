# KANG — gap research for the creative rulebook (2026-11-06)

Scope: Hindi narration-led travel/devotional vlogs made from still photos (Ken Burns / 2.5D), a few CC clips, text cards, route maps, Hinglish captions + pop words, 16:9 master + 9:16 reels. Audio not researched (deferred).

Input read: `kang/incoming/creative_layer_2026-11-06_v2/step_2_rules/rules.json` (463 rules: 10 🟢, 55 🟡, 398 🟠), `MASTER_RULES.md`, `step_3_order/ORDER.md`.
Output: `gap_rules_proposed.json` (33 rules, G-001…G-033, same schema incl. `part_ids`).

## 1. What was missing in the existing rulebook

Grep of rules.json showed almost nothing for our format:
- **Still photos / Ken Burns**: no rule on zoom size for stills, resolution headroom, hold time per still, or move variety. Only generic camera moves (R-329 is for 1–1.5 s UI push-ins).
- **Maps**: no map timing, labels or data/licence rules (only "map" as an example inside R-089, R-397).
- **Devotional / temple**: zero rules (no hits for mandir, deity, respect, dharm).
- **Hindi / Hinglish captions**: zero rules; caption speed rules are English/European numbers (R-131 = 17 cps).
- **16:9 graphics safe area**: missing (R-095 is 9:16 only).
- **Flashing / seizure safety**: missing.
- **Spelling consistency (names)**: missing.
- **Platform limits**: R-172 still says 60 s for Reels; Shorts/Reels are now 3 min.
- **Style pack (palette, one transition style, grade matching)**: already well covered (R-204, R-252, R-309, R-429, R-213, R-226, R-267, R-453). No new rule needed; see §8.

## 2. Sources opened (all opened on 2026-11-06)

| # | Source | Type / licence | Key fact used |
|---|---|---|---|
| 1 | YouTube Help – Video Chapters https://support.google.com/youtube/answer/9884579 | Official help | First timestamp 00:00, ≥3 timestamps ascending, chapter ≥10 s |
| 2 | YouTube Help – End screens https://support.google.com/youtube/answer/6388789 | Official help | Last 5–20 s, video ≥25 s, up to 4 elements (16:9) |
| 3 | YouTube Help – 3-minute Shorts https://support.google.com/youtube/answer/15424877 | Official help | Shorts up to 3 min (vertical/square, after 15 Oct 2024); >1 min Short with active Content ID claim is blocked globally |
| 4 | Instagram Creators blog https://creators.instagram.com/blog/the-latest-with-instagram | Official blog | Reels up to 3 min eligible for recommendation (Jan 2025, US first) |
| 5 | Meta Ads Guide – Reels video https://www.facebook.com/business/ads-guide/update/video/instagram-reels | Official (ads) | Keep 14% top, 35% bottom, 6% sides free of text/logos |
| 6 | Meta Business Help – safe zone https://www.facebook.com/business/help/980593475366490 | Official (ads) | Bottom 40% if disclaimers; same safe zone for 9:16 feed |
| 7 | Google – YouTube Shorts ads https://business.google.com/us/ad-solutions/youtube-ads/shorts-ads/ | Official (ads) | Avoid top 10%, bottom 25%, right 10% |
| 8 | Google Ads Help – vertical video https://support.google.com/google-ads/answer/9128498 | Official (ads) | Vertical video gets cropped/compressed in some player states; safe-zone image (pixel numbers are only in the image, not used) |
| 9 | EBU R 95 v1.1 https://tech.ebu.ch/docs/r/r095.pdf | Broadcast standard | Action safe 3.5%, graphics safe 5% each edge (16:9) |
| 10 | W3C WCAG 1.4.3 https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html | W3C, permissive | Text contrast ≥4.5:1; large text ≥3:1 |
| 11 | W3C WCAG 2.3.1 https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold.html | W3C, permissive | No more than 3 flashes in any 1 s |
| 12 | W3C WCAG 2.3.3 https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html | W3C, permissive | Parallax can trigger dizziness/nausea (vestibular) |
| 13 | BBC subtitle guidelines https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/ | Official broadcaster | 160–180 wpm, ≈0.3 s per word minimum; online 9:16 line ≤90% width |
| 14 | Netflix Hindi TTSG https://partnerhelp.netflixstudios.com/hc/en-us/articles/115003196707-Hindi-Timed-Text-Style-Guide | Official spec | 42 chars/line, 2 lines, **22 cps adults**, proper names not translated, redundant on-screen text dropped |
| 15 | Netflix General Requirements https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617 | Official spec | Min 5/6 s, max 7 s, line-break rules, position to avoid on-screen text, KNP consistency |
| 16 | Netflix Timing Guidelines https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394 | Official spec | Gap = 2 frames or ≥0.5 s (no 3–11 frames @24fps); snap to cuts within 0.5 s; linger 0.5 s after speech |
| 17 | Material Design 3 duration tokens https://m3.material.io/styles/motion/easing-and-duration/tokens-specs | Official design system | 50–200 ms short, 250–400 medium, 450–600 long, 700–1000 ms extra-long |
| 18 | Poynter – Ken Burns and his effect https://www.poynter.org/reporting-editing/2007/meaning-in-motion-ken-burns-and-his-effect/ | Journalism craft article | Move only for meaning; motion guides the eye and can change meaning; start wide→detail or tight→reveal |
| 19 | 43frames – Ken Burns numbers https://www.43frames.com/blog/ken-burns-effect | Vendor craft blog | 10–20% scale, 6–8 s per still, always ease, max zoom = source px ÷ timeline px, vary moves |
| 20 | PTE AV Studio manual – Ken Burns https://docs.pteavstudio.com/en-us/9.0/techniques/kenburns | Manual, **CC BY-NC-SA** → idea only, not copied | Resolution must cover deepest zoom; linear motion looks jerky |
| 21 | ClickPop – animated route maps https://clickpop.ai/guides/animated-map-route-videos | Vendor guide | Leg 1.5–3 s, overview 1.5–2 s, 0.5 s arrival pause, ≤4 labels, 10–16 px line, middle 60% in vertical, real data + attribution |
| 22 | Animaps – route lines & pauses https://animaps.ai/blog/curved-vs-straight-route-lines | Vendor guide | ≥2 s hold after each move, ~1 s per short label, 3–4 s final view |
| 23 | BBC Editorial Guidelines – stills https://www.bbc.co.uk/editorialguidelines/guidance/stills | Official editorial policy | Images that may offend religious groups need special care; captions must be factually correct; public-place images can still be private |
| 24 | Hindu American Foundation – use of Hindu images https://www.hinduamerican.org/projects/commercial-use-hindu-images-guide | Community advocacy guidance | Lists degrading uses; "significant material modification of a Deity" may offend |
| 25 | Devbhumi Dwarka photography guide https://www.devbhumidwarka.in/blog/dwarka-photography-guide | Independent local guide | No phones/photography in Dwarkadhish sanctum; exterior/ghat OK; ask before photographing pilgrims; blur unwilling faces |
| 26 | YouTube blog – Shorts deep dive https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive | Official blog (creator opinion) | "You have one second to hook someone" on Shorts |

No GitHub repos were used, so no GPL/NC text issue. PTE manual is NC → ideas only, in own words.

## 3. Findings by topic (short)

**3.1 Still-photo storytelling** — Move only for meaning (Burns). Practical numbers exist only in craft blogs: 10–20% scale, 4–8 s per still, always eased, one axis. Hard fact: max zoom = source px ÷ output px. Parallax is a known motion-sickness trigger (W3C) → ration it. No official "px per second" speed exists; scale % over clip length is the usable unit. → G-001…G-008.

**3.2 Text cards** — BBC: ≈0.3 s per word (backs R-091). Material tokens give official ms bands (backs R-202/R-299/R-353; R-299's 1.2 s top end is above Material's 1.0 s max). WCAG contrast 4.5:1 / 3:1 large (backs R-096). EBU 16:9 graphics safe 5%. Flash ≤3/s. → G-009, G-011, G-012, G-018, G-033.

**3.3 Maps** — Only vendor guides; they agree: one map beat when a new place/leg appears, 1.5–3 s per leg, ≥2 s holds, ≤4 labels, real data with attribution. → G-024…G-028 (all 🟠).

**3.4 Hindi/Hinglish captions** — Netflix Hindi: 42 chars, 2 lines, **22 cps** (R-131's 17 cps is a European number — Netflix pt-BR is 17). Netflix timing: 20 frames–7 s, 2-frame-or-0.5 s gaps, cut snapping. Name consistency via a key-names list. No official source on pop-word frequency — existing R-378/R-224 stay as they are. → G-013…G-017.

**3.5 Devotional sensitivity** — No India-specific official style guide found. BBC (religion care, accurate captions, privacy) and HAF (no degrading/modifying deity images) give principles; Dwarka sanctum photography ban from an independent local guide. Effect bans on murti frames are our inference (🟠) → human/devotee check. → G-019…G-023.

**3.6 Story structure** — Chapters and end-screen rules verified exactly as R-087/R-016 state → upgrade both to 🟢. Rest (cold open, loops, payoff) is already heavily covered (R-001…R-086); nothing new found worth adding. → G-032 (dup, for upgrade only).

**3.7 Reels/Shorts** — Limits now 3 min (YouTube, Instagram). Short >1 min with any Content ID claim = blocked. Official 9:16 safe zone numbers come from ad guidance (Meta 14/35/6; Google 10/25/10 right). Combined box x 6–90%, y 14–65%. "One second" hook is a creator opinion on the official blog. → G-010, G-029, G-030, G-031.

**3.8 Clean-modern style pack** — Already covered (see §8). Only new safety items: flash limit (G-011), contrast numbers (G-018).

## 4. Corrections to existing rules (important)

| Existing | Problem | Fix |
|---|---|---|
| R-095 (9:16 safe, y_max 79%) | Captions at ~78% sit inside Meta's 35% bottom band | Use G-010: x 6–90%, y 14–65% |
| R-254 / R-124 pixel insets | Smaller than official Meta/Google bands | Use G-010 |
| R-131 (≤17 cps) | European-language number; Netflix Hindi = 22 | G-013: 20 target, 22 max for Hinglish |
| R-172 (Reels "max 60 s") | Outdated as a limit (3 min now) | G-029; keep 15–60 s only as a target |
| R-432 / R-136 (holds 1.2–3 s) | Too short for narration stills in long-form | G-004: 4–8 s long-form, 2–3 s in reels |
| R-299 (entrance up to 1.2 s) | Above Material's 1.0 s max | Cap at 1.0 s (G-033) |
| R-200/R-296/R-428/R-422 (punch-ins, zooms, motion accents) | Unsafe on deity frames | G-020 overrides on deity-tagged beats |
| R-376 (captions off in title zones) | For narration video, losing speech captions hurts | G-017: move captions, switch off only for hero title |

## 5. Upgrades (existing rule now backed by an official source)

R-087 → 🟢 (YouTube chapters), R-016 → 🟢 (end screens), R-091 → 🟢 (BBC 0.3 s/word), R-092 → 🟢 (Netflix 42 chars, 2 lines, 20 frames, 2-frame gap), R-096 → 🟢 (WCAG 4.5:1), R-261/R-328 → 🟡 (ease + one axis, two sources).

## 6. Proposed rules — summary (full text in JSON)

| ID | Name | Layer | Evidence | Check | Duplicates / corrects |
|---|---|---|---|---|---|
| G-001 | Every photo move has a reason | style | 🟡 | – | extends R-205, R-220 |
| G-002 | Ken Burns 10–20% scale | style | 🟠 | ✓ | ≠ R-329/R-428 (different job) |
| G-003 | Never zoom past the pixels | style | 🟢 | ✓ | new |
| G-004 | Still on screen 4–8 s | rhythm | 🟠 | ✓ | conflicts R-432, R-136 |
| G-005 | Ease every move, one axis | style | 🟡 | – | dup R-261, R-328 |
| G-006 | Vary moves; ≤2 same in a row | style | 🟠 | ✓ | overlaps R-244, R-426 |
| G-007 | New place: wide first | kahani | 🟡 | – | dup R-397, R-432 |
| G-008 | Parallax rationed | style | 🟠 | ✓ | adds to R-356 |
| G-009 | 16:9 graphics safe 5% | samajh | 🟢 | ✓ | new |
| G-010 | 9:16 safe box x6–90 y14–65 | samajh | 🟢 | ✓ | corrects R-095, R-254, R-124 |
| G-011 | ≤3 flashes per second | style | 🟢 | ✓ | new |
| G-012 | Number cards: count then hold | samajh | 🟡 | ✓ | builds on R-303, R-091 |
| G-013 | Hinglish caption ≤20/22 cps | samajh | 🟢 | ✓ | corrects R-131; vs R-092 |
| G-014 | Netflix caption timing | samajh | 🟢 | ✓ | dup R-092, R-131 + adds |
| G-015 | Hindi-aware line breaks | samajh | 🟡 | – | refines R-092 |
| G-016 | One spelling glossary | samajh | 🟢 | ✓ | new |
| G-017 | Caption vs card: no clash | samajh | 🟡 | ✓ | softens R-376 |
| G-018 | Contrast 4.5:1 / 3:1 large | samajh | 🟢 | ✓ | upgrades R-096 |
| G-019 | No inside-sanctum images | kahani | 🟡 | – | extends R-019 |
| G-020 | Calm treatment of murti | style | 🟠 | ✓ | overrides R-200, R-296, R-428, R-422 |
| G-021 | Never cover/alter murti | style | 🟠 | ✓ | like R-246 |
| G-022 | Pilgrims' privacy | samajh | 🟡 | – | new |
| G-023 | Devotional words accurate/calm | kahani | 🟠 | – | narrows R-121 |
| G-024 | Map only when it helps | samajh | 🟠 | ✓ | applies R-089, R-364 |
| G-025 | Route draw 1.5–3 s/leg | rhythm | 🟠 | ✓ | fits R-199 |
| G-026 | Map holds ≥2 s | rhythm | 🟠 | ✓ | map version of R-091 |
| G-027 | Phone-readable map design | style | 🟠 | ✓ | fits R-252, R-318 |
| G-028 | Real map data, credited | kahani | 🟠 | – | extends R-018, R-019 |
| G-029 | Platform limits 3 min; Content ID >60 s | rhythm | 🟢 | ✓ | corrects R-172 |
| G-030 | Re-frame stills for 9:16 | style | 🟡 | ✓ | builds R-218, R-255 |
| G-031 | Short hook in first second | kahani | 🟡 | ✓ | dup R-111, R-001, R-005 |
| G-032 | Chapters + end screen (verified) | kahani | 🟢 | ✓ | exact dup R-087, R-016 (upgrade then drop) |
| G-033 | Motion duration bands | rhythm | 🟢 | ✓ | corroborates R-202/R-299/R-353 |

Counts: 33 rules — 🟢 11, 🟡 10, 🟠 12. 25 have a machine check. Truly new (no existing equivalent): G-003, G-008, G-009, G-011, G-016, G-019–G-023, G-024–G-028, G-029 (as limit), G-030. Pure duplicates kept only for upgrade: G-005, G-007, G-031, G-032.

## 7. ORDER.md suggestion

Devotional-respect rules (G-019…G-023) should win over any Style/Rhythm rule. Simplest: treat them as **Kahani-level** (an offended audience = story failure) or as a hard gate before the layer ladder, plus a human/devotee check flag (ORDER.md §3 already gives humans the veto).

## 8. Gaps I could not close (be honest)

- **No official numbers** for Ken Burns speed, still hold time, parallax depth, map timing, or pop-word frequency. All such numbers are 🟠 craft/vendor values.
- **No India-specific official guide** on depicting deities in video was found; devotional effect bans are inference.
- **Dwarka photo ban**: only an independent guide was opened; the district notification and police-case news appeared in search results but were not opened. Verify with the temple trust.
- **Organic Shorts/Reels safe zones**: no official organic numbers exist; the ad numbers are used as a conservative stand-in. Google's vertical pixel figures are only in an image (not used).
- **Hinglish (Roman) cps**: no source specific to Roman Hinglish; 22 cps is Netflix's Devanagari Hindi figure.
- **Colour/grade consistency for mixed-source stills**: no new official source opened; existing R-213/R-226/R-267/R-453 already cover normalise → match to hero → one look.
- **India map boundaries**: flagged in G-028 but not researched.
- Audio not researched, as instructed (G-029 only notes the Content ID block for >60 s Shorts for the later audio phase).
