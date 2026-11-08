# CONFLICTS — Step 2 ke takraav (faisla Step 3 ka hai)

Teeno parts (A/B/C) ke saare conflict_notes aur ek-hi-baat-par-alag-numbers wale niyam yahan ikatthe hain.
**Is file me koi faisla NAHI liya gaya** — har takraav ke saath sirf ye likha hai ki faisla *kis aadhar par*
ho sakta hai (layer ka order, evidence tag, format long/short, platform, content type). Jeetne wala
Step 3 (Order) tay karega. Rule IDs naye unified wale hain (rules.json / MASTER_RULES.md wale);
saath me purana part-ID bhi diya hai taaki part-files me dhoondhna aasan ho.

> ⚠️ **ExpoCut attribution:** Free to use and redistribute with attribution to expocut.com — kuch takraavon me
> ExpoCut playbook ke numbers bhi ek paksh hain; wo isi shart ke saath aaye hain.

---

## 1. Pattern interrupt ki cadence — SABSE BADA TAKRAAV

**Rules:** R-155 (B-044) · R-156 (B-045) · R-181 (C-033) · R-137 (A-054) · R-182 (C-034)

| Paksh | Daava / number | Source |
|---|---|---|
| CraigHewitt cadence | Pattern interrupt har **15–30 s** | TheCraigHewitt retention-editing (🟠) |
| Slopstudio measured | Pacing **FLAT** rakho; interrupt sirf **~1 per ACT** (per minute nahi) — measured corpus (5 top explainers) me yahi mila | slopstudio retention-editing (🟡) |
| SkillMedev cadence | Pattern interrupt har **90–120 s** | SkillMedev youtube-script-writer (🟠) |
| Explainer micro-hooks | TubeBuddy **30–60 s** vs vidIQ **60–90 s** — dono creator reports, koi pakka number nahi | A-054 ke andar dono (🟠) |

Saath wala niyam R-182 (C-034): har **section break** par re-hook — ye waqt par nahi, placement (boundary) par lagta hai; upar wale teeno se sambandhit hai lekin logic alag hai.
**Faisla kis aadhar par ho sakta hai:** format/genre (explainer long-form vs entertainment) · evidence tag (🟡 measured corpus vs 🟠 creator cadence) · interrupt ki *kind* (waqt-based vs section-based).

## 2. Visual change ki cadence — short-form aur hook sections ke numbers

**Rules:** R-134 (A-051) · R-158 (B-047) · R-164 (B-053) · R-157 (B-046) · R-159 (B-048) · R-135 (A-052)

| Paksh | Number | Source |
|---|---|---|
| Melvynx style | Visual change har **2–4 s** | Melvynx (🟠) |
| ExpoCut playbook | Har **3–5 s** | ExpoCut (🟠, attribution note upar) |
| mktkit engine | Har **3–7 s** | mktkit (🟠) |
| Hook/fast sections | Har **3–5 s** (R-158) | CraigHewitt/Classicchins (🟠) |
| Shorts cuts | Har **2–4 s**, VVSA target 70–90% (R-164) | slopstudio Shorts data (🟡) |
| Visual floor | Cut-count nahi, **perceived motion**; gap ki chhat **15 s** (R-157) | slopstudio (🟡) |
| Measured cold open | Pehle 30 s me sirf **2–7 cuts** (R-159) — upar wali 3–5 s wali cadence (30 s me 6–10 changes) isse tez padti hai | slopstudio corpus (🟡) |

Savdhaani (R-135 / A-052): film ka naapa hua ASL benchmark short-form ka *target* nahi hai — wahan yahi cadence chalegi.
**Faisla kis aadhar par ho sakta hai:** content type (samjhane wala dheema, entertainment tez) · section (hook vs body) · format (Shorts vs long-form) · ek baat sab paksh mante hain: **5 s se upar ke static gap par kahin bharosa nahi**.

## 3. Cutting-speed ki ceiling vs tez cadence

**Rules:** R-176 (C-008) बनाम cadence wale saare rules (Section 1–2)

- Tim Smith ki research (🟢): hadd se tez cutting par aankh ko **re-fixation ka waqt** chahiye; speed ki ek ceiling hai jiske upar samajh girti hai.
- Dusri taraf cadence rules tez change mangte hain.
- C-008 ki apni note kehti hai: takraav ho to **ceiling jeetni chahiye** — lekin ye Step 3 confirm karega, yahan faisla nahi.

**Faisla kis aadhar par ho sakta hai:** evidence tag (🟢 peer-reviewed eye-tracking sabse pakka) · layer (ceiling Samajh ki hifazat karti hai, cadence Rhythm hai — Order me Samajh upar hai).

## 4. Mid-event flow ki hifazat vs deliberate interrupt

**Rules:** R-178 (C-010) बनाम R-181 (C-033) · R-182 (C-034)

- Zacks event segmentation (🟢): dimaag kahani ko events me baant ta hai; event ke **beech me be-wajah cut** flow todta hai (R-178).
- Pattern-interrupt rules jaan-boojh kar beech me todte hain.
- C-010 ki note: ye *satahi* takraav hai — interrupt ek **deliberate design** hona chahiye, aadat nahi.

**Faisla kis aadhar par ho sakta hai:** intention (design kiya hua interrupt vs aadat) · event boundary ki jagah (interrupt boundary par lage to dono jeette hain).

## 5. Punch-in: har 2nd/3rd cut par (cadence) vs sirf motivated

**Rules:** R-200 (A-072) · R-145 (A-062)

| Paksh | Daava | Source |
|---|---|---|
| ExpoCut cadence | Cadence ke saath har **2nd ya 3rd cut** par punch-in | ExpoCut (🟠, attribution note upar) |
| Motivated-only | Punch-in **sirf wajah ke saath**, hadd ke andar (gap ≥4 s) | kmilo/Melvynx (🟠) |
| Ginti ki hadd | Punches **≤10/min** (R-145) | mktkit (🟠) |

**Faisla kis aadhar par ho sakta hai:** content type (entertainment short me cadence wali chal sakti hai; samjhane wale content me motivated wali surakshit) · layer (punch-in Style hai — sabse neeche; Samajh/Rhythm se takraye to harega).

## 6. Pause / silence ke teen model — dead-air ka ek model final hona hai

**Rules:** R-184 (C-042) · R-191 (C-072) · R-196 (C-091) · R-197 (C-092) · R-198 (C-093) · R-138 (A-055)

| Model | Numbers | Source |
|---|---|---|
| Floor + beech-trim | Speech gap ki floor **0.45 s**; zyada hissa beech se kato, saansein bachao (R-184) | Jakeschincariol deadair (🟠) |
| Remainder model | Har pause ka **0.2–0.3 s** bacha kar rakho (R-191) | blazerior (🟠) |
| Cut-edge padding | Cut ke edge par **30–200 ms** padding window — ye pause ki lambai nahi, edge ki baat hai (R-196) | pifferologo (🟠) |
| Silence thresholds | **≥400 ms** = saaf cut · **150–400 ms** = usable · **<150 ms** = unsafe (R-197) | pifferologo (🟠) |
| Speaker handoff | Speaker badle to **400–600 ms** hawa (R-198) | pifferologo (🟠) |
| Phrase gaps (style-wise) | Talking-head aam **200–400 ms** · Melvynx super-fast style sirf **30–80 ms** (sentence .08, comma .05, word .03) · mktkit defaults talking **0.40 s**, manifest **0.85 s** · ExpoCut silence-removal min gap **450–500 ms + 80 ms padding** (R-138) | chaar sources (🟠) |

**Faisla kis aadhar par ho sakta hai:** teenon model ek saath rakhe ja sakte hain agar *layer* saaf ho (threshold = kab kato, remainder/floor = kitna bachao, padding = edge par) — ya ek model final hoga · channel ki style (super-fast vs aaram-daa) par ek hi style pakdo. **Numbers ki bhasha alag hai, isliye Step 3 ko teeno ko ek table me badalna hoga.**

## 7. Dead air beherahmi se kato vs jaan-boojh ka dramatic pause

**Rules:** R-162 (B-051) बनाम R-229 (B-071) · R-192 (C-073)

- R-162: bina-kaarann wali khamoshi/filler **beherahmi se kato** (max silence ~1 s).
- R-229: **1–2 s ki jaan-boojh wali khamoshi 'extremely powerful'** hai — speaker performance ka hissa (Filnik).
- R-192: **dramatic pause ko haath mat lagao** — dead-air rules ka ye jaan-boojh kiya exception hai; engine ko dramatic pause pehchanna hoga ya human flag lagega.

**Faisla kis aadhar par ho sakta hai:** intention — pause ke saath visual use uthata hai ya nahi (CraigHewitt khud yahi exception deta hai). Bina wajah ki khamoshi par koi takraav nahi: wo hamesha kategi.

## 8. B-roll ki cadence vs relevance gate

**Rules:** R-166 (B-055) · R-167 (B-056) · R-146 (A-063) बनाम gate: R-114 (B-032) · R-088 (A-028)

| Cadence paksh | Number | Source |
|---|---|---|
| Long-form (talking-head) | B-roll/screen-share ka gap **30–60 s** tak chal sakta hai | CraigHewitt (🟠) |
| Marketing video | B-roll har **5–10 s** | Classicchins (🟠) |
| Paper-stage shorts | Cadence **8–15 s** wali | A-063 cluster (🟠) |
| Talking-reel punches | Punches **10/min** (har ~6 s) tak — alag system | mktkit (🟠) |

Gate (dono taraf lagu): R-114 — B-roll ko **apni jagah kamani padegi** (relevance pehle; cadence ke liye sajawati B-roll mat dalo). R-088 — jo bola, wahi dikhe (exactness).
**Faisla kis aadhar par ho sakta hai:** format (lamba talking-head vs chhota marketing video vs talking-reel — number format se aata hai, dono ko mat milao) · layer (gate Samajh ka hai, cadence Rhythm ki — Order me Samajh upar, yani relevance cadence ko hara sakti hai).

## 9. Sponsor ki jagah: 20–33% container vs pehle payoff ke BAAD

**Rules:** R-037 (B-011) बनाम R-038 (B-012)

- R-037 (slopstudio, 🟡 measured): sponsor/tangent ko runtime ke **20–33%** wale container me rakho.
- R-038 (henterprise, 🟠): sponsor read **pehle payoff ke BAAD** hi aaye.
- Takraav tab pakka hota hai jab pehla payoff 33% ke baad aata ho — dono ek saath satisfy nahi honge.

**Faisla kis aadhar par ho sakta hai:** evidence tag (🟡 measured vs 🟠 opinion) · layer (payoff Kahani ka hai — vaada pehle pura ho, ye Kahani > baaki order se bhi judta hai) · video ki lambai/payoff ki asal jagah.

## 10. Constant escalation vs FLAT pacing

**Rules:** R-048 (B-022) बनाम R-156 (B-045)

- R-048 (henterprise): kahani ke **stakes/intensity ki constant escalation** + segments ke beech micro-cliffhanger.
- R-156 (slopstudio, 🟡): **cut/WPM ki pacing FLAT** rakho, escalation nahi.
- Note ki saaf baat: farak *lever* ka hai — ek kahani ke stakes ki baat hai, dusra cut-speed ki. Agar dono ek hi lever (cut speed) par lagu hon to takraav asal hoga.

**Faisla kis aadhar par ho sakta hai:** lever alag rakho (stakes badhao, speed flat) to dono jeet sakte hain · agar ek hi lever par aayein to evidence (🟡 measured) aur layer (Kahani ki escalation vs Rhythm ki flatness — Kahani upar hai) dekho.

## 11. Music ka level: voice se kitna neeche — aur naapa hua apvaad

**Rules:** R-102 (A-042) · R-225 (B-067) · R-103 (A-043) · apvaad: R-219 (A-091)

| Paksh | Number | Source |
|---|---|---|
| Relative niyam | Music voice se **18–25 dB neeche** (voice −16 LUFS ho to music ~−34/−41 LUFS) | kmilo (🟠) |
| Absolute levels | Music track **−20..−25 dB**, voice **−6..−10 dB** | Classicchins/CraigHewitt/Filnik (🟠) |
| Ducking | Bolte waqt music aur **6–12 dB** dabao (R-103) | kmilo (🟠) |
| ⚠️ Naapa hua apvaad | Ek creator ke style-copy me beat sirf **~12 dB under** naapa gaya — us style ka measured apvaad hai; copy karna ho to original ko naapo (R-219) | Melvynx measured (🟡) |

**Faisla kis aadhar par ho sakta hai:** measurement ki bhasha (relative dB-under-voice vs absolute track level — dono ko ek hi table me badalna hoga) · style-copy ka case aam niyam se alag (pehle naapo, phir copy karo).

## 12. Master loudness target: −14 LUFS vs −16 LUFS

**Rules:** R-105 (A-045) · R-248 (C-078)

| Paksh | Target | Source |
|---|---|---|
| YouTube/social standard | **−14 LUFS** integrated, TP ≤−1 dBTP | kmilo/Melvynx (🟡) |
| Social render (blazerior) | **−14 LUFS**, TP **−1.5**, LRA **11**, two-pass | blazerior (🟡) |
| mktkit house master | **−16 LUFS / −1.5 dBTP / LRA 11** — tark: −16 wala master platform ke ~−14 normalization par bina limiting artifacts ke pahunchta hai | mktkit (🟠) |
| Podcast feed | **−16 LKFS ±1** | A-045 ke andar (🟡) |

**Faisla kis aadhar par ho sakta hai:** destination/platform (YouTube vs podcast feed vs social) · pipeline consistency — jo pipeline chuno, **ek hi target** rakho.

## 13. Captions: 32 vs 42 characters, aur teen caption modes

**Rules:** R-092 (A-032) · R-094 (A-034) · R-247 (C-077) · R-131 (C-085) · R-259 (C-098)

| Baat | Numbers | Source |
|---|---|---|
| Standard captions | **≤42 chars/line**, ≤2 lines, reading speed **≤20 CPS** (bachche 17) | kmilo/mktkit + DCMP Captioning Key (🟡) |
| Vertical (1080 px) | **32 chars × 2 lines** — wahan 42 fit nahi hota (DCMP bhi 32 kehta hai) | mktkit (🟡) |
| Phrase captions | **~32–42 chars/line**, reading speed **≤~17 CPS** | SkillMedev (🟠) |
| Word-level subtitles | Line me **≤3 shabd** | blazerior (🟠) |
| Burned-in chunks | Melvynx **1–3 words/chunk** vs kmilo **1–5 words/page** | dono (🟠) |
| Tested chunking styles | **2-shabd** bold chunks wala style bhi tested hai (R-259) | pifferologo (🟠) |

**Faisla kis aadhar par ho sakta hai:** format (vertical par 32, 16:9 standard par 42) · mode (word-level highlight vs phrase captions — content ke hisaab se batega) · ek channel par **ek hi style consistent** rakho.

## 14. Safe-zone ke number sets — ek table final honi hai

**Rules:** R-095 (A-035) · R-246 (C-076) · R-254 (C-086)

- R-095: % adhar par safe box (x 9–91%, y 14–79%) + sources ke per-platform px numbers.
- R-246: blazerior ke pixel zones (card face ke upar, face PAR kabhi nahi).
- R-254: SkillMedev ke per-platform % insets (TikTok/Reels/Shorts).
- Teeno ek hi sach ke alag roop/number-set hain — numbers platform aur format ke hisaab se alag hain.

**Faisla kis aadhar par ho sakta hai:** target platforms ka **sakht intersection** hi surakshit raasta hai (A-035 ki note) · Step 3 me ek hi zone table final hogi.

## 15. Thumbnail text ki shabd-hadd: 2, 3, 4 ya 5?

**Rules:** R-215 (A-087) · R-119 (B-037) · R-240 (C-061) · R-239 (C-060)

| Paksh | Hadd | Source |
|---|---|---|
| kmilo niyam | **≤5 shabd** | kmilo (🟠) |
| MrBeast profile (sabse zyada views wale) | **0–2 shabd** target | Filnik ke MrBeast profile (🟠) |
| henterprise | **~4 shabd** hard cap ke aas-paas | henterprise (🟠) |
| Jake | **3 maximum** (tool 4 par flag karta hai) | Jakeschincariol (🟠) |
| serge | **≤4 shabd** | sergebulaev (🟠) |
| SkillMedev | **2–5, target 3, hard ceiling 5** | SkillMedev (🟠) |

Sab pakshon me surakshit beech: **target 3** — lekin ek number final karna Step 3 ka kaam hai.
**Faisla kis aadhar par ho sakta hai:** evidence (measured top-performer profiles vs aam craft niyam) · thumbnail ka kaam (ek focal point, sachhi emotion — R-239 sab mante hain).

## 16. Title me caps ki hadd

**Rule:** R-238 (C-059)

- Jake: all-caps ki ceiling **2 caps shabd**.
- serge: full-caps title **banned**; emphasized shabd **1 tak**.
- Note kehti hai sakht wala (serge) surakshit rahega — par aakhiri faisla Step 3 ka.

**Faisla kis aadhar par ho sakta hai:** surakshat pasand (sakht hadd) vs flexibility · clickbait-risk (Samajh/imaandari ka sawal bhi hai — vaada jhootha na ho).

## 17. Hook ki lambai aur hook ka window

**Rules:** R-180 (C-024) · R-072 (C-037) · R-030 (B-004) · R-061 (C-022)

| Baat | Numbers | Source |
|---|---|---|
| Long-form hook | **9–24 shabd** | Jake/SkillMedev cluster (🟠) |
| Shorts spoken hook | **<12 shabd** (sakht limit) | SkillMedev video-hook-writer (🟠) |
| Filled hook (sab platforms) | **<12 shabd** | viral-hooks-skill (🟠) |
| Hook ka window | Jake: hook **15 s** ka core · SkillMedev/serge: pehle **30 s** ki puri beat structure (R-061) | dono (🟠) |

Note (C-022): 15 s vs 30 s takraav nahi hai — 15 s hook ka *core* hai, 30 s *puri beat structure*; dono jude hue hain.
**Faisla kis aadhar par ho sakta hai:** format (Shorts par <12 wali sakht limit jeetegi; long-form par 9–24 wala band) · hook ki kind (spoken vs filled/text).

## 18. Short-form ki duration windows

**Rules:** R-152 (A-069) · R-172 (B-061) · R-073 (C-040) · R-026 (A-027)

| Paksh | Windows | Source |
|---|---|---|
| ExpoCut/Melvynx/kmilo | TikTok entertainment **21–34 s** (educational 60–90 s) · Shorts **15–30 s** · Reels **7–15 s** punchy ya **30–60 s** value · Melvynx ke naape hits **25–40 s** | teen sources (🟠) |
| Filnik playbook | Reels optimal **15–30 s** · TikTok optimal **15–45 s**, max 60 s | filnik (🟠) |
| Self-contained short | Moment **20–55 s** ka ho | SkillMedev cluster (🟠) |
| Long-form se clip | Clip **20–60 s** standalone | Melvynx/kmilo (🟠) |

**Faisla kis aadhar par ho sakta hai:** platform (Reels/TikTok/Shorts ke windows alag) · content type (entertainment vs educational) · idea ko lambaai tay karne do, platform ki max ko nahi — ye baat dono paksh mante hain.

## 19. Bolne ki gati (WPM) ke band

**Rules:** R-151 (A-068) · R-163 (B-052) · R-188 (C-047)

| Paksh | Band | Source |
|---|---|---|
| Measured narration | **160–195 WPM** (5-explainer corpus) | slopstudio (🟡) |
| Script budget | **150 WPM** par timing budget banao | SkillMedev (🟠) |
| Type-wise gati | Har content type ki apni gati (tutorial dheema, talking-head tez...) | kmilo (🟠) |

**Faisla kis aadhar par ho sakta hai:** content type (narration/explainer vs tutorial/demo) · evidence (🟡 measured band vs 🟠 budget number) · 150 budget aur 160–195 band ek saath chal sakte hain agar budget = planning, band = asal delivery.

## 20. ORDER KA SABSE BADA SAWAL: Emotion kahan baithega?

**Rules:** R-058 (C-014) · R-060 (C-020)

- **Murch ka Rule of Six (🟠, lekin sabse anubhavi craft parampara):** Emotion **51%** > Story 23% > Rhythm 10% > Eye-trace 7% > 2-D 5% > 3-D 4% — Emotion akela baaki paanchon ke kul se zyada; qurbani hamesha **neeche se upar** do (R-060).
- **User ka apna Order (is system ka design):** Kahani > Samajh aana > Rhythm > Style/Effect — aur **Emotion engine ke bahar hai, insaan ki aankh par** (system ki ghoshit seema: rules sundarta/emotion judge nahi kar sakte).
- Takraav: Murch Emotion ko Kahani se **strictly upar** rakhta hai; user ke order me emotion Kahani ke andar band/insaan ke paas hai.

**Faisla kis aadhar par ho sakta hai:** ye Step 3 ka **kendriya design faisla** hai — engine ke andar emotion ka koi proxy rakhein, ya use poori tarah insaan ki approval par chhodein. Dono pakshon ki taakat: Murch ka 51% anubhav ka wazan hai (🟠); user ka tark system ki seema ka hai (jo naapa nahi ja sakta wo rule nahi ban sakta).

## 21. Filler hatao vs bolne ki natural texture

**Rules:** R-185 (C-043) · R-162 (B-051)

- R-185: jo cue **sirf filler** ho ('um', 'uh' hi bhara ho) use hatao.
- Lekin dusre cluster ki measured baat (PandaStudio wali): bolne ki **natural texture** (halki saansein, aadhe jumle) bachane se bharosa banta hai — sab filler saaf karna delivery ko robotic bana sakta hai.
- C-043 ki note khud kehti hai: filler HATAO *sirf jab cue sirf filler ho* — yahi seema takraav ko ghata ti hai, par line kahan hai ye Step 3 tay karega.

**Faisla kis aadhar par ho sakta hai:** cue ki kind (sirf-filler vs texture wala) · Samajh (baat saaf ho) vs Kahani (bharosa/character bache).

## 22. Load-bearing turns ke percentages — har format par copy hon?

**Rule:** R-076 (C-053)

- Rule turns/payoffs ki jagah runtime ke percentages par rakhta hai (jaise payoff 55–85% par).
- Note ka sawal: ye percentages **seedha copy** karna Step 3 me tay hoga — short/mid-form par scale badal sakta hai (lambi video ke percentages chhoti par wahi matlab nahi rakhte).

**Faisla kis aadhar par ho sakta hai:** format/runtime (long-form ke % vs short-form ke seconds) · evidence (percentages kis corpus se aaye, wo corpus kitna lamba tha).

## 23. Title formulas ki niche-validity

**Rule:** R-237 (C-057)

- Corpus-validated formulas ko pehle rakho — lekin corpus me kuch formulas (Y2/Y4/Y6) **kamzor ya gayab** mile; Y4 aur Y6 business niche me essentially absent the.
- Ye formulas gear/tutorial niches me kaam kar sakte hain — lekin unhe 'proven' mat mano.

**Faisla kis aadhar par ho sakta hai:** niche (business vs gear/tutorial) · formula ka evidence usi niche ke corpus se aaya hai ya dusre se.

## 24. Hook repeat: sirf mktkit ka akela design rule

**Rule:** R-015 (A-015)

- mktkit: hook khule aur **sirf ek baar** repeat ho (design rule).
- Baaki teen clusters me hook-repeat ka **koi niyam nahi** — aam taur par repeat ko galti hi mana jata hai.
- Dusri pipeline me lagane se pehle sochna hoga — ye kisi measured data par nahi, ek system ke design par tika hai.

**Faisla kis aadhar par ho sakta hai:** pipeline ka design (loop-wale Shorts me repeat ka kaam hai, long-form me nahi) · format.

---

## 25. Sambandhit lekin TAKRAAV NAHI (cross-references — sirf record)

Ye notes takraav nahi, rishton ke ishare hain; Step 3/4 me kaam aayenge, isliye gayab na hon:

- **R-231 (C-004) frame declutter** ↔ **R-126 (C-007) ek shot = ek magnet** (🟢): declutter usi baat ka style-roop hai.
- **R-232 (C-006) eye-trace landing** ↔ **R-233 (C-017) Murch eye-trace (7%)**: ek hi baat — ek measured (🟢) roop me, ek craft (🟠) roop me.
- **R-057 (C-013) chunk = ek event** ↔ **R-087 chapters**: chapter bhi ek event hona chahiye — dono milte hain.
- **R-190 (C-071) cut phrase ke end par** ↔ **R-195 (C-090) shabd ke beech cut kabhi nahi**: pehla phrase-level craft hai, dusra word-level technical correctness — alag, takraav nahi.
- **R-249 (C-079) grade tulna karke** ↔ **R-258 (C-097) CDL se grade**: dono 'ek badlav, phir dekho' kehte hain — ek dusre ko mazboot karte hain.
- **R-253 (C-084) animation restraint (0.25 s fade)** ↔ **R-260/R-261 animation durations/easing**: takraav nahi — wahan information-cards ki baat hai, yahan simple overlays ki.
- **R-199 (C-101) animation ka payoff shabd par land kare** ↔ graphic-timing wale rules (shabd se pehle card): sambandh Step 3 dekhega.
- **R-086 (C-103) structural archetypes** ↔ **R-074 (C-050) paanch-beat spine**: overlap hai — spine demo-specific hai, archetypes general set hai.

---

*Kul: 24 takraav-vishay (Sections 1–24) + 1 cross-reference section. Har section ke rules rules.json me apne naye R-ID se milenge; purana part-ID MASTER_RULES.md ke har rule me 'Purana ID' me likha hai.*

---

## ADDENDUM — Editor round ke takraav (faisla ORDER addendum me hoga)

Merge Round 2 (2026-11-06) me jude D1 (After Effects + Premiere) aur D2 (DaVinci Resolve + CapCut) clusters ke
conflict_notes yahan vishay-wise ikatthe hain. **Is addendum me bhi koi faisla NAHI liya gaya** — har takraav ke
saath sirf aadhar likha hai (purana ORDER faisla / layer / format / profile / map ki paribhasha). Faisla
ORDER ke addendum me hoga. Rule IDs naye unified wale hain; part-ID band me diya hai.

### A1. Pause/silence thresholds — 250 / 280 / 400 / 500 ms aur smart-cut 1 s

**Rules:** R-274 (D1-013) · R-282 (D1-021) · R-295 (D1-034) · R-401 (D2-044) · R-402 (D2-045) · R-419 (D2-062) · purana model: ORDER #6

| Paksh | Number | Source |
|---|---|---|
| eacp1991 perceptual floor | **250 ms** floor; 250–300 ms = editorial pause ki shuruaat; is suite me 10 ms tak kaatne ki kshamata bhi hai (kshamata ≠ default) | R-274 (D1-013), R-282 (D1-021) (🟠) |
| vamshicreates house DNA | Min silence **0.28 s** (−35 dB par), padding 0.08 s (purane 30–200 ms window ke andar — sangat) | R-295 (D1-034) (🟠) |
| Purana unified model (ORDER #6) | Silence **≥400 ms** = cut zone · 150–400 ms usable · <150 ms unsafe | purane rules (🟠) |
| ChaiWithJai/appariciojunior (note) talking-head | Threshold **0.5 s**; **0.3–0.5 s dramatic pause surakshit** | R-401 (D2-044) (🟠) |
| CapCut smart-cut (auto pehla pass) | Sirf **>1 s** silence + duplicate takes bahar — jaan-boojh kar conservative | R-402 (D2-045) (🟠) |
| Vlog pads | Exact ms nahi; purane remainder **0.2–0.45 s** se takraav nahi | R-419 (D2-062) (🟠) |

**Faisla kis aadhar par ho sakta hai:** pass (auto pehla vs haath ka fine) · profile (talking-head social vs Kang pipeline) · dramatic pause ki suraksha sab paksh mante hain — sawal sirf threshold ke number ka hai.

### A2. Cut-edge padding aur crossfade — ek shabd, teen paribhashayein

**Rules:** R-275 (D1-014) · R-346 (D1-085) · R-269 (D1-008) · R-350 (D1-089) · R-273 (D1-012) · R-347 (D1-086) · purana padding: ORDER #6

- **Frame-edge padding (purana):** 30–200 ms — cut ke kinare ki suraksha. R-275 (D1-014) ke margins bhi yahi kehte hain (sangat), lekin usi rule ka Calm preset **500 ms** window se bahar hai — preset-wise apvaad ka sawal.
- **Jumla-star ki saans:** R-346 (D1-085) — jumla-cut par **0.25 s pehle / 0.35 s baad** padding; paribhasha alag (sentence-level breath) lekin numbers purane window se takraate dikhte hain.
- **Crossfade parivaar (sangat, takraav nahi):** har edit point par chhota crossfade (R-269 (D1-008)) · click hatane ko aakhri **2 frames** fade (R-350 (D1-089), usi ka khaas roop) · speech **30 ms** ke andar = CLIPPED hadd (R-347 (D1-086)) · **60 ms** crossfade = saaf cut ki sakht shart (R-273 (D1-012)) — disha ek hai: 30 ms kataav ki hadd, 60 ms saaf-cut ki shart.

**Faisla kis aadhar par ho sakta hai:** paribhasha alag saaf karna (edge suraksha vs jumla-saans vs click-fix) · preset (Calm) ko apvaad ghoshit karna ya nahi.

### A3. Pacing ki ghadi — format ke hisaab se alag duniyayein

**Rules:** R-294 (D1-033) · R-336 (D1-075) · R-398 (D2-041) · R-410 (D2-053) · R-310 (D1-049) · R-349 (D1-088) · purane: ORDER #1/#2

| Paksh | Number | Source |
|---|---|---|
| Short-form house DNA (Premiere) | Hook ASL **1.6 s**, Body ASL **2.8 s** | R-294 (D1-033) (🟠) |
| Film/teaser ghadi (koptsev63) | Hooks **4–6 s** — bahut dheemi | R-336 (D1-075) (🟠) |
| Short-form visual gap | **3 s** se zyada gap = pattern interrupt (purana Shorts default bhi 3 s — sangat; long-form **5 s** se takraav sirf lagu karne par) | R-398 (D2-041) (🟠) |
| A-roll reset (talking-head social) | **6–9 s** bina reset ke nahi — ye sirf speaker-frame ki hadd hai, aam visual gap se alag map | R-410 (D2-053) (🟠) |
| Motion-graphics piece | Nirnayak transition har **1.5–3 s** — sirf motion pieces ke liye | R-310 (D1-049) (🟠) |
| Sliver hadd | **0.5 s** se chhota tukda mat rakho — jaan-boojh ke tez teaser fragments (R-336 (D1-075) ke <1.5 s shots) apvaad ka sawal | R-349 (D1-088) (🟠) |

**Faisla kis aadhar par ho sakta hai:** format sabse bada aadhar hai (short-form house / film-teaser / talking-head / motion-graphics — chaaro ki ghadiyan alag hain aur sab apni jagah sahi ho sakti hain) · map ki paribhasha (ASL vs visual gap vs A-roll reset ek cheez nahi).

### A4. Punch-in: alternating house style vs motivated-only

**Rules:** R-296 (D1-035) बनाम purana faisla ORDER #5

- **House style (vamshicreates):** har dusre cut par **100% ↔ 112%** alternating punch-in, bina-wajah bhi. Body ASL 2.8 s par ye ≈ **10–11 baar/min** banta hai — purani hadd (≤10/min, gap ≥4 s) ke bilkul kinare ya par.
- **Purana faisla (ORDER #5):** punch-in **sirf motivated**, ≤10/min, gap ≥4 s; cadence-punch-in sirf entertainment-Shorts profile me.

**Faisla kis aadhar par ho sakta hai:** house-style ko profile-apvaad banana hai ya nahi · layer (punch-in Style hai — Samajh/Rhythm se takraye to harega, ye purana usool hai).

### A5. Overshoot / exaggeration ki matra — teen alag duniyayein

**Rules:** R-313 (D1-052) · R-322 (D1-061) · R-287 (D1-026) · R-326 (D1-065) · R-301 (D1-040)

| Context | Matra | Source |
|---|---|---|
| Premium UI / product | **1.5–3%** overshoot | R-313 (D1-052) (Maciejdziuba, 🟠) |
| Brand motion | Follow-through = move-distance ka **10–20%**; pop = **110%** (10% overshoot) | R-322 (D1-061), R-326 (D1-065) (LobzyJay, 🟠) |
| Character animation | Exaggeration asal se **+20–50%** | R-287 (D1-026) (dylantarre/Disney parampara, 🟠) |

Teeno apne context me sahi ho sakte hain — takraav tab hota hai jab ek hi number sab par lagu ho. R-301 (D1-040) (overshoot me poora object react kare) sirf DHANG ki baat hai, matra ki nahi — takraav se bahar.
**Faisla kis aadhar par ho sakta hai:** context-wise table (UI/product · brand · character) — ek universal number is takraav ko suljha nahi sakta.

### A6. Animation timing — ikai (frames vs ms), anticipation ke paimane, entrance bands

**Rules:** R-284 (D1-023) · R-320 (D1-059) · R-285 (D1-024) · R-321 (D1-060) · R-299 (D1-038) · R-353 (D1-092) · R-316 (D1-055) · R-354 (D1-093) · R-305 (D1-044) · R-286 (D1-025) · R-324 (D1-063) · R-314 (D1-053) · R-355 (D1-094)

- **Ikai ka sawal:** dylantarre ki frame-ghadi (30 fps par) aur LobzyJay ki ms-ghadi (<150 ms instant · 150–250 halka · 250–500 standard · 500 ms–1 s bhaari · >1 s cinematic) 30 fps par takreeban milti hain; **fps badle to kaunsi ikai pakdi jaye** — stagger (R-305 (D1-044): frames me 2–5 vs ms me 20–200) par bhi yahi sawal.
- **Anticipation ke do paimane (sangat):** frame-banawat me wind-up ~40-frame action ka ~25% (R-285 (D1-024)) vs seedha niyam main action ka **20–30%** (R-321 (D1-060)) — baat ek, bhasha do (absolute frames vs %).
- **Entrance bands ka overlap:** aam entrance **0.4–1.2 s** (R-299 (D1-038)) vs UI **0.3–0.5 s** / text reveal **0.8–1.2 s** (R-353 (D1-092)) vs ms-ghadi me UI **150–250 ms** (R-320 (D1-059)) — UI par 150–250 ms vs 0.3–0.5 s ka seedha farak hai.
- **Transitions ki upari hadd:** **0.5–0.8 s** (R-316 (D1-055)) vs **0.5–1.5 s** (R-354 (D1-093)) — neeche ka band (0.5 s) dono me ek hai. Title card **3–5 s** dono paksh mante hain (sangat).
- **Sambandh (takraav nahi):** follow-through child elements 2–5 frames peeche (R-286 (D1-025)) stagger parivaar se hai; sequential reveal metronome jaisa na ho (R-324 (D1-063)) bade reveals ke antar ki baat hai; easing asymmetric hi premium (R-314 (D1-053)) ke saath LobzyJay ki chetaavni — number se pehle maksad; spring presets (R-355 (D1-094)) inertial-bounce defaults se sambandhit.

**Faisla kis aadhar par ho sakta hai:** ikai ka ek faisla (fps-tied frames vs absolute ms) · element ke prakar se band (UI / text / logo / title) · anticipation ko % bhasha me ek karna.

### A7. Loudness — destination-wise poori table banni hai

**Rules:** R-271 (D1-010) · R-441 (D2-084) · purane: ORDER #12

- Purane band: YouTube/social **−14 LUFS**, podcast **−16 LUFS**, mktkit house −16.
- **Naye band (D1-010):** broadcast **−24 LUFS**, Netflix **−27 LUFS** — ye naye destinations hain, purano se takraav nahi, table adhuri thi.
- **Podcast range (halka takraav):** R-441 (D2-084) podcast ko **−16..−20 LUFS** ki range deta hai (peaks −9..−3 dBFS) — purana podcast profile ek point −16 hai; dialogue-only podcast ke liye neeche tak ijazat.

**Faisla kis aadhar par ho sakta hai:** destination/platform — ek table (YouTube −14 / podcast −16 ya range / broadcast −24 / Netflix −27) ORDER addendum me final hogi.

### A8. Audio levels ke maps aur ducking ke teen numbers

**Rules:** R-270 (D1-009) · R-298 (D1-037) · R-281 (D1-020) · R-334 (D1-073) · R-440 (D2-083) · R-443 (D2-086) · R-444 (D2-087) · R-451 (D2-094) · purane: ORDER #11, R-103

| Map / number | Kya hai | Source |
|---|---|---|
| Absolute dBFS seedhi | Music bed **−18..−24 dBFS** (absolute) — purana niyam RELATIVE (voice se 18–25 dB neeche) hai; sankhya milti-julti, naap ka aadhar alag | R-270 (D1-009) (🟠) |
| House mix offsets | SFX **−9 dB**, music bed **−20 dB** — music purane relative band ke andar (sangat), lekin aadhar phir absolute | R-298 (D1-037) (🟠) |
| Climax duck | Climax par music **−12 dB** tak duck — purana R-103 dialogue-duck 6–12 dB se sangat disha, alag mauqa | R-281 (D1-020) (🟠) |
| Podcast ducker depth | Shuruaat **2.7 dB**, **>5 dB = amateur** — ye ducker ki GEHRAI hai, bed level nahi | R-440 (D2-083) (🟠) |
| CapCut narration duck | **−12 dB** (10f/15f fades) — ducker-depth ke roop me 2.7–5 dB se seedha takraav; bed-level ke roop me purane 18–25 dB se kam gehra | R-443 (D2-086) (🟠) |
| Music bed LUFS-relative | Narration ke neeche **−24..−18 LUFS relative** — purane dB band ke qareeb, map LUFS ka | R-444 (D2-087) (🟠) |
| VO finish peak | **−6 dBFS PEAK** — production-stage ka number, LUFS-integrated delivery target se alag map; dono ek saath lagu nahi hote | R-451 (D2-094) (🟠, note) |
| SFX asset normalize | Generated SFX pehle **I=−16 LUFS** par normalize — ASSET level hai, master target (−14) se alag cheez | R-334 (D1-073) (🟠) |

**Faisla kis aadhar par ho sakta hai:** sabse pehle map ki paribhasha (bed LEVEL vs ducker DEPTH vs asset normalize vs delivery master — chaar alag cheezein ek table me saaf hon) · phir profile (podcast dialogue-chain / CapCut bed / aam YouTube).

### A9. Grade / LUT ki matra

**Rules:** R-266 (D1-005)

- ADAM-0S: LUT/grade intensity **50–70%** · koptsev63: Rec709 par **≤55%** ki hadd. Sangat hissa **50–55%** hai; sawal material-wise hadd ka hai (log/flat par zyada, Rec709 par kam).

**Faisla kis aadhar par ho sakta hai:** source material (Rec709 vs log/flat) · skin-tone suraksha (Samajh) upar, style ki matra neeche.

### A10. Delivery bitrate ke band

**Rules:** R-272 (D1-011)

- ADAM-0S: 1080p **16–24 Mbps** / 4K **45–68 Mbps** · iart-ai H.264 delivery: 1080p **~10–16 Mbps** / 4K **~35–50 Mbps**. Aam sangat hissa 1080p par 16 Mbps ke aas-paas.

**Faisla kis aadhar par ho sakta hai:** platform/destination aur codec (H.264 vs H.265) · quality-bachana Samajh hai, file-size Style/practical — ek band tay hona bacha hai.

### A11. Comedy timing ka paimana — incident vs beat

**Rules:** R-277 (D1-016) · R-336 (D1-075)

- VisionCut 4-act ghadi: poora comedy **incident 8–14 s** (Setup 2.0–3.5 → Escalation 1.5–3.0 → Punchline 1.5–2.5 → Reaction 2.0–4.0).
- koptsev63 pacing table: comedy **beat/shot 4–5 s**.
- Dono ka paimana alag hai (incident vs ek beat) — asal takraav tabhi hoga jab ek hi ghadi dono par lagu ho.

**Faisla kis aadhar par ho sakta hai:** paimane ki paribhasha saaf karna (incident-ghadi aur beat-ghadi alag-alag darj hon).

### A12. Cover / thumbnail ke shabd — 1–5 vs hadd 4

**Rules:** R-437 (D2-080) · purane: CONFLICTS #15, ORDER #15

- Purana faisla (ORDER #15): thumbnail text **target ≤3 shabd, hard cap 4**.
- CapCut cover/hero-title formula: **1–5 shabd** (pehchan wali background ke saath).
- Sulah ki disha note me hai: **cover (video ke andar ka hero title) aur thumbnail (bahar ki image) alag cheezein** ho sakti hain — faisla ORDER addendum ka.

**Faisla kis aadhar par ho sakta hai:** cheez ki paribhasha (cover vs thumbnail) · platform (CapCut/TikTok cover vs YouTube thumbnail).

### A13. Kahani ki ghadi rhythm ko override kare — disha ka note

**Rules:** R-337 (D1-076) · sambandhit: R-339 (D1-078)

- R-337 (D1-076): sabse bade pal ko sabse lambi ghadi do — tez-pacing wale rhythm rules (max gap/ASL) se disha ka tanav hai; source khud kehta hai ye beats rhythm ko override karte hain, aur ORDER ki seedhi (Kahani sabse upar) bhi yahi disha deti hai.
- R-339 (D1-078) (blink cut point — soch ke aakhir par kaato) purane Murch/science rules ka vyavharik roop hai, takraav nahi.

**Faisla kis aadhar par ho sakta hai:** layer ka order pehle se tay hai (Kahani > Rhythm) — sawal sirf ye hai ki engine/ORDER addendum is override ko kis hadd tak formal kare.

### A14. Sambandhit lekin TAKRAAV NAHI (editor round cross-references — sirf record)

- R-264 (D1-003) (invisible cut upaay) ↔ R-340 (D1-079) (misdirection — cut ko harkat/awaaz ke dhakke peeche): ek hi kala ke do hisse; D1-079 sirf cut-point wale dhakke ki baat hai.
- R-289 (D1-028) (staging takneek) ↔ R-318 (D1-057) (dhyaan ka anushaasan — ek frame, zyada se zyada do maang): staging usi anushaasan ko pane ke upaay hain.
- R-302 (D1-041) (ek object ki properties ek frame par finish) ↔ R-286 (D1-025) (follow-through me alag OBJECTS offset): ulta nahi — ek object ke andar sync, objects ke beech offset.
- R-352 (D1-091) (bina-wajah A/V mismatch = defect) ↔ R-262 (D1-001) (split edit default, jaan-boojh ka 6–12 frame offset): takraav nahi — wajah wala offset jaayaz, bina-wajah wala defect.
- R-344 (D1-083) (black card ke neeche room tone) usi skill ke 'talking cut kabhi silent nahi' usool ki disha me hai.
- R-357 (D1-096) (aakhri frame par slow push-in) ↔ D1-069 (perpetual-drift mana): halka tanav — ye sirf END frame ki baat hai, poore scene ke drift ki nahi.

---

*Addendum kul: 14 vishay (A1–A14) — 13 takraav/paribhasha-vishay + 1 cross-reference section. Inke jude rules rules.json me naye R-ID se milenge; part-ID MASTER_RULES.md ke har rule me 'Purana ID' me likha hai. Faisla ORDER ke addendum me hoga.*
