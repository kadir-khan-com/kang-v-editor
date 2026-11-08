# STEP 4 — Python Rules Engine (Worker + Critic)

User ke design ka aakhri step: **engine Claude nahi hai.** Ye saf Python (sirf
stdlib, koi LLM/API call nahi) hai jo Step 2 ke rules ko Step 3 ke ORDER par
chalata hai.

**Round 2 update (editor round ke baad):** rules ab **463** hain (pehle 261),
jinme **153 machine-checkable** hain. ORDER_ADDENDUM ke 14 faisle (A1–A14)
bhi engine + profiles me utar aaye hain — destination-wise loudness, fast
talking-head ka alternating punch-in, overshoot ki context table, ducker ki
teen maps, auto-first-pass gate. Profiles ab **7** hain.

- **Worker** — har machine-checkable rule ko video ke beats par evaluate karta
  hai. Profile ke defaults (ORDER ke faisle) rule ke raw numbers ko override
  karte hain.
- **Critic** — har rule ka PASS/FAIL, layer-wise score (Kahani / Samajh /
  Rhythm / Style), overall score, aur **human flags** deta hai.
- **Takraav** — jab do rules ulte faisle dein, jeetne wala ORDER ki seedhi se
  tay hota hai (layer > evidence > profile > kam-hastakshep) aur report ke
  `resolutions` me saaf likhta hai: kaun jeeta, kaun hara, kis aadhar par.

## Files

| File | Kya hai |
|---|---|
| `engine.py` | Worker + critic (ek file, alag functions) |
| `profiles.json` | ORDER Section 5 + ADDENDUM ke 7 profiles ke numeric defaults |
| `test_engine.py` | stdlib unittest — 31 tests (16 purane + 15 addendum ke naye) |
| `demo/demo_long.json` | Sample beats: long_explainer, jaan-boojh kar 4 khamiyan |
| `demo/demo_shorts.json` | Sample beats: shorts, 2 khamiyan + 1 emotion beat |
| `demo/*.report.json/.md` | Dono demos par engine ke taaza reports |
| `demo/*.report.v1.*` | Round-1 (261 rules) wale purane reports — tulna ke liye backup |

## Kaise chalaye

```bash
python3 engine.py <beats.json> --profile <name> --out <dir>
python3 engine.py demo/demo_long.json --out demo     # demo report banega
python3 test_engine.py                               # tests
```

Bina koi argument diye chalao to usage dikhega (exit code 2).
`--profile` na do to `meta.profile` use hoga; wo bhi na ho to `long_explainer`.
Output: `<out>/<beats-file-naam>.report.json` + `.report.md` (Hinglish).

## Profiles (profiles.json)

| Profile | Max visual gap | Interrupt hadd | Captions | Loudness | Khaas |
|---|---|---|---|---|---|
| `long_explainer` | 5 s (hook window 3 s) | ≥1 re-hook / 120 s | 42 chars | −14 LUFS | flat pacing, pause model #6, hook 9–24 shabd, payoff 55–85% |
| `long_entertainment` | 5 s | ≥1 / 60 s | 42 chars | −14 LUFS | punch-in motivated; 30–60 s interrupt band optional |
| `shorts` | 3 s | — (cadence hi sab) | 32 chars, 1–3 shabd chunks | −14 LUFS | hook <12 shabd (sakht), duration windows platform se (YouTube/Reels 15–30, TikTok 15–45, educational 60–90), payoff seconds me (15–25 s) |
| `talking_reel` | 3–7 s band (limit 7) | hook repeat ON (sirf yahan) | 32 chars × 2 | −14 LUFS (house −16 uplabdh) | punches ≤10/min, B-roll exactness sakht |
| `podcast` | — (audio pehle) | — | 42 chars | **−16 LUFS/LKFS** | speaker handoff 400–600 ms; **narration-led: duck −12 dB** (A8) |
| `fast_talking_head` | 5 s | — | 42 chars | −14 LUFS | **alternating punch-in 100↔112% allowed** (A4), cap ≤10/min; kabhi 112% se upar nahi |
| `broadcast` | 5 s | ≥1 / 120 s | 42 chars | **−24 LUFS** (destination: broadcast) | music absolute dBFS map (A8); Netflix jaana ho to meta `destination: "netflix"` (−27 / TP −2) |

Har profile me ye sab bhi hai: music band 18–25 dB under voice (#11), punch-in
min gap 4 s (#5), pause model #6 (cut threshold ≥400 ms, remainder 0.2–0.45 s,
edge padding 30–200 ms, handoff 0.4–0.6 s), hook limits #17, WPM planning
150 / delivery 160–195 (#19), thumbnail hard cap 4 shabd · target 3 (#15),
title ≤100 chars · full-CAPS ≤1 shabd (#16/#23).

**ADDENDUM ke naye profile defaults (sab profiles me):**

- `loudness_destinations` table (A7): youtube −14±1, social −14±1,
  podcast −18 (band −20..−16), broadcast −24±1, netflix −27±1 + true-peak
  hadd −2 dBTP. Meta/profile ka `destination` field tay karta hai kaunsi
  pankti chalegi — destination table profile ke `lufs_target` se upar hai.
- `motion_class`: `"brand"` (A5 overshoot table ki default pankti);
  meta se `premium` / `character` override ho sakta hai.
- `ducker_depth_default_db`: [2.7, 5] (A8); narration-led (podcast) me
  `duck_db: -12`.
- `auto_first_pass`: `false` (A1) — smart-cut >1 s wala rule (R-282) sirf
  tab chalega jab profile ya meta me ye flag true ho.

## Beats schema (input)

```json
{
  "meta": {
    "profile": "long_explainer", "platform": "youtube", "duration_s": 400,
    "lufs": -14, "music_db_under_voice": 20, "wpm": 175,
    "title": "...", "title_chars": 24, "thumbnail_words": 3
  },
  "beats": [
    {"id": "b1", "start_s": 0, "end_s": 8, "kind": "hook",
     "text": "...", "visual_change": true, "open_loop_open": true}
  ]
}
```

- `kind`: `hook | speech | broll | graphic | pause | payoff | sponsor | transition`
- Optional beat fields (jo ho, usi par check chalega): `punch_in`, `motivated`,
  `caption_chars`, `caption_words`, `open_loop_open`, `open_loop_close`,
  `dramatic_pause`, `emotion_peak`, `relevant` (B-roll exactness), `rehook`,
  `proof`, `promises_artifact`, `tease`, `cta`, `title_card`,
  `explanation_card`, `chapter_start`, `speaker_change`, `gap_before_s`,
  `handoff`, `silence_cut`, `fast`, `sfx`, `lead_s`, `act`, `x_pct`/`y_pct`,
  `inside_safe_zone`
- Round-2 ke naye optional beat fields: `scale_pct` (punch-in scale),
  `overshoot_pct`, `follow_through_overshoot_pct`, `exaggeration_pct`,
  `follow_through_frames`, `stagger_frames`, `attack_frames`,
  `edge_silence_ms`, `speech_cut_distance_ms`, `lut_intensity_pct`,
  `highlighted_words`, `sfx_stack`, `reaction_s`, `breathing_shot`,
  `decorative` (transition), `hero_title`, `comedy_incident`, `comedy_cut`,
  `manual_boost_db`, `piece` / kind `shot`
- Optional meta fields: `hook_score`, `apv_percent`,
  `end_screen_retention_percent`, `retention_drop_percent`, `font_px`,
  `description_chars`, `background_music_db`, `cover_words`,
  `title_caps_words`, `clip_duration_s`, `chapters`, `promised_artifact`,
  `video_type`
- Round-2 ke naye optional meta fields: `destination`
  (youtube/social/podcast/broadcast/netflix), `true_peak_db`, `sfx_lufs`,
  `ducker_depth_db`, `dehum_db`, `voice_above_music_db`,
  `music_bed_relative_lufs`, `motion_class` (premium/brand/character),
  `auto_first_pass`, `voiceover` (false = bina-VO film), `cover_title_words`,
  `visual_styles`, `bgm_cues` + `bgm_unique_pct`, `pause_removal_threshold_s`,
  `min_silence_cut_s`, `motion_piece`
- **Jo field nahi hai, wo check "data nahi — skip" hai. FAIL kabhi nahi.**
  Skip critic ke score me ginna hi nahi jata.

## ORDER ke faisle engine me kahan hain

- **Override** (profile raw number ko badalta hai): max_visual_gap (cadence
  family R-134/158/160/164/221 → profile ka ek number, #2) · caption chars
  format se (#13) · LUFS destination se (#12) · interrupt interval
  R-155/R-181 → profile hadd 120/60 s (#1) · phrase gap → pause model
  remainder band 0.2–0.45 s (#6) · thumbnail cap 4, 5-wali hadd reject (#15) ·
  payoff band long-form 55–85%, Shorts par seconds 15–25 s (#22) · music band
  profile se (#11) · R-038 (sponsor pehle payoff ke baad) ko ORDER #9 se
  machine roop diya gaya.
- **Gating** (rule is profile/format par lagu hi nahi): short-form hook rules
  (R-053/054/111/121/227) sirf shorts/talking_reel · spoken hook ≤12
  (R-030/R-072) sirf short-form, long-form par 9–24 band (R-180) · cold-open
  counts (R-032/R-159) sirf long-form · ASL (R-173) fast formats par ·
  marketing B-roll cadence (R-167) short formats par · cadence rules ka
  format gate (R-134/R-164) · fast-section rules (R-158/R-221) sirf pehle
  30 s / `fast` beats par.
- **Takraav (resolutions)**: (a) cadence vs **relevance gate R-088** —
  Samajh > Rhythm, gate hamesha jeetega; jo B-roll `relevant:false` hai wo
  finding bhi banta hai. (b) cadence punch-in vs **motivated-only R-200** —
  ORDER ka khaas faisla #5 aam seedhi se upar: cadence ki demand unmotivated
  punch-in ko justify nahi karti.
- **Dramatic pause** (ORDER #7): >1 s ki khamoshi agar `dramatic_pause` hai
  to FAIL nahi — human flag. Bina-wajah ki >1 s khamoshi FAIL hai.

## ORDER_ADDENDUM (A1–A14) engine me kahan hai — sar

| Faisla | Engine me roop |
|---|---|
| A1 pause model | Unified model hi default; **R-282 (smart-cut >1 s) sirf `auto_first_pass` par** — warna gate-skip. 250 ms = perceptual floor (threshold rules R-274/R-415 meta field mile to check) |
| A2 do padding | Edge padding (30–200 ms) aur jumla-saans (250/350 ms) alag fields — dono edit-level hain, isliye dono `padding_range_ms` not_evaluable me, naam alag se |
| A3 samay ki hadd-ein | Hook ASL 1.6 s sirf hook section; visual gap 5 s/3 s waisa hi; sliver hadd 0.5 s shorts me beats-as-pieces (R-349) |
| A4 alternating punch-in | `fast_talking_head` profile: scale 112 wale pattern punches par **R-200 finding/resolution nahi**; R-296 (scale band =112) sirf wahi profile me evaluate hota hai |
| A5 overshoot table | `motion_class` (meta > profile > brand): premium 1.5–3% (R-313), brand follow-through 10–20% (R-322), character exaggeration 20–50% (R-287) — galat class par rule skip |
| A6 ms normalization | Saare naye checks ke range keys (`min_s/max_s/min_db/min_lufs/min_pct`, hook ka `max_s`) `norm_check()` se ek roop (value/min/max) me badal jate hain |
| A7 loudness destinations | Destination table (upar dekho); Netflix par true-peak −2 dBTP bhi check (meta `true_peak_db`); R-271 sirf broadcast/netflix par |
| A8 teen audio maps | Relative dB-under-voice = default map; ducker depth meta `ducker_depth_db` par cap 5 dB (R-440), narration-led duck −12 profile me; **R-334 SFX −16 LUFS asset-level hai** — master LUFS se kabhi pass/fail nahi |
| A9 LUT band | Default cap **55%**; 70 tak sirf profile `strong_look` par, warna fail; strong-look band me human flag |
| A10 bitrate | Beats se naap nahi banta — koi evaluator nahi (meta me bitrate field aaye to aage ka kaam) |
| A11 comedy samay | Comedy beats ki lambai duration_range se (incident kul 8–14 s, single beat 4–5 s) — `comedy_incident`/`comedy_cut` flags se |
| A12 CapCut cover | Cover title words count_range se (R-446, 1–5 shabd); thumbnail ka faisla (≤3 target, cap 4) alag hi raha |
| A13 kahani > rhythm | Meta-rule 1 waisa ka waisa — koi badlav nahi |
| A14 cross-references | Sirf record — engine par asar nahi |

**Naye check-kinds (round 2 me evaluator bane):** `min_gap_ms` (cut edge ki
sacchi khamoshi ≥60 ms — `edge_silence_ms`; boli se cut ki doori ≥30 ms —
`speech_cut_distance_ms`), `frame_range` (follow-through/stagger/attack
frames), `ratio_range` (sabse lamba : sabse chhota shot, beats proxy se),
`min_per_min` (bina-VO film me caption cues ≥4/min — sirf jab
`meta.voiceover: false` ho). Saath hi purane kinds ke naye `what` roop:
duration_range (transition/talking-head/climax/comedy/motion/text beats,
B-roll hold 1.2–3.0 s, title card, hero title hold), count_range (highlighted
words, cover title, visual styles, decorative transition runs, stacked SFX,
chapter breathing shots), db_range ke field-less roop (ducker, de-hum, music
bed, voice-above-music, manual boost), percent_range ke generic field roop
(split-edit share, anticipation %, grain, skin saturation, zoom scale…).
`max_per_act` ab NOT_EVALUABLE nahi hai — `act` field mile to ginati hoti
hai, warna imaandaar skip.

## Critic aur human flags

- Report `summary` me: kul rules (463), machine-checkable (153), evaluate hue,
  PASS/FAIL/skip ginati, overall score %, aur charon layer ke alag score.
- `human_flags`: check=null wale **310 rules** me se jo is video ke beats par
  lagu hote hain (rule ke naam/`when` ke signal shabd — hook, payoff, sponsor,
  open loop, dramatic, emotion — usi tarah ke beats par), har emotion/payoff/
  dramatic beat par ORDER §3 ka generic flag bhi.
- **Emotion par engine kabhi PASS/FAIL nahi deta — sirf flag.** Sundarta aur
  emotion insaan ki aankh ka kaam hai (user ki seema, ORDER §3). Insaan ka
  veto engine ke har faisle se upar hai.

## Demo scores — round 1 vs round 2

| Demo | Round 1 (261 rules) | Round 2 (463 rules) |
|---|---|---|
| `demo_long` (long_explainer) | 79.3% (29 evaluated, 23 pass / 6 fail) | **76.5%** (34 evaluated, 26 pass / 8 fail) |
| `demo_shorts` (shorts) | 87.1% (31 evaluated, 27 pass / 4 fail) | **87.2%** (39 evaluated, 34 pass / 5 fail) |

Purane rules ke saare verdicts dono demos me **bilkul waise ke waise** hain —
farak sirf naye evaluate hue rules ka hai. Long me 2 naye fail: R-338 (shot
ratio — demo ke lambe segment-beats proxy par band se bahar) aur R-432
(B-roll hold 1.2–3.0 s — demo ke B-roll *segments* 20 s/70 s ke hain; rule
shot-level hold naapta hai, beats ko shot proxy mana gaya hai, ye seema
finding me likhi aati hai). Shorts me R-432 hi ekmatra naya fail; baaki 7
naye evaluated rules pass hain (R-338, R-349, R-359, R-398, R-400, R-442,
R-457). Naye rules ka bada hissa demos par imaandaari se **skip** hai —
unke fields (ms gaps, frames, overshoot %) sample beats me hain hi nahi.

## Imaandari: not_evaluable check-kinds

Ye kinds beats-data se evaluate hi nahi ho sakte (engine inhe skip karta hai,
wajah ke saath):

| Kind | Kyun not_evaluable |
|---|---|
| `fade_ms` | Segment boundary par 30 ms audio fade — edit-level micro data, beats schema me hota hi nahi |
| `padding_range_ms` | Cut edge padding 30–200 ms **aur** jumla-saans 250/350 ms (A2: dono alag hain, dono edit-level) — beats me nahi |

Round 2 ke baad yahi do kinds bache hain. `max_per_act` is list se **hat
gaya** hai: `act` field mile to evaluator chalta hai, na mile to khud skip
karta hai (dead-code wala purana bandh bhi theek ho gaya).

Baaki kinds ke **kuch `what` roop** bhi tabhi chalte hain jab unka optional
field maujud ho (warna skip, fail nahi): `safe_zone_pct` (overlay position),
`min_score` (hook_score), `min_font_px`, `max_lead_s` (graphic ka lead_s),
analytics wale (`percent_range` ke APV/end-screen roop, `min_drop_percent`)
— ye publish ke baad ke data hain; `duration_range_s` ke join_fade/crossfade/
panel roop edit-level hain. A10 ka bitrate band (1080p 10–24 Mbps, 4K 35–68)
bhi isi shreni me hai — beats/meta me bitrate field hi nahi, isliye koi
evaluator nahi bana.
Ek khaas note: R-123 (retention refresh trigger) ek review-trigger hai,
video ki galti nahi — engine use kabhi FAIL nahi karta, sirf note karta hai.

Aur do imandaar seemayein:

- Visual gap ka matlab: `visual_change=true` wala beat = us beat ke andar
  badlav hota hai (editor ki annotation). Engine frame-by-frame naapta nahi.
- Words-first-30s ki ginati overlap ke hisaab se proportional hai (andaz),
  aur ASL me beats ko shot ka proxy mana gaya hai.
