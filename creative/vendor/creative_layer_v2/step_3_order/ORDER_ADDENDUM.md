# ORDER ADDENDUM — Editor round ke takraavon ke faisle

ORDER.md ke meta-niyam hi yahan lagu hain (Layer > Evidence > Profile > Kam-hastakshep).
Ye faisle CONFLICTS.md ke Addendum A1–A14 ke liye hain. Engine inhe profile defaults me lega.

**A1 · Pause thresholds (250/280/400/500 ms + smart-cut 1 s)**
Purana unified model hi default rahega (≥400 ms cut · 150–400 usable · <150 unsafe).
250 ms = *perceptual floor* — isse chhoti khamoshi viewer ko mehsoos hi nahi hoti, use kaatne ka retention fayda zero hai; ye floor model se takraata nahi, use samjhata hai. 280 ms usi usable band ke andar hai. Smart-cut ka >1 s wala threshold sirf **AUTO pehle pass** (machine rough-cut) ke liye hai — haath ke pass me 400 wala model. Calm profile ka remainder 500 ms tak ja sakta hai (pace profile ka faisla).

**A2 · Padding ki teen paribhashayein**
Takraav naam ka hai, kaam ka nahi. **Edge padding** (30–200 ms, technical — cut ke kinare ki suraksha) aur **jumla-saans** (250/350 ms, Calm par 500 ms — jumlo ke beech ki hawa) alag cheezein hain; dono rahenge, engine dono ko alag fields me naapega.

**A3 · Pacing ki ghadiyaan format-wise**
Hook ASL 1.6 s sirf hook section ki house-ghadi hai; film/teaser ki 4–6 s apni jagah. Visual gap ka purana faisla barkarar (long 5 s / Shorts 3 s). A-roll reset 6–9 s ek alag map hai (chehre par wapsi ka antar) — visual gap se takraav nahi, saath chalega. Sliver 0.5 s = Shorts me sabse chhota shot.

**A4 · Punch-in alternating 100%↔112%**
ORDER #5 barkarar: default **sirf motivated**, hadd ≤10/min. Alternating wala house style sirf **fast talking-head profile** me chalega — wahan bhi 112% se upar nahi aur hadd wahi ≤10/min.

**A5 · Overshoot ki matra — context table (faisla)**
Premium/UI motion: **1.5–3%** · Brand follow-through: **10–20%** (pop 110% tak) · Character exaggeration: **+20–50%**. Teeno sahi hain — content type tay karega kaunsi pankti lagu hai. Entertainment/dharmik content me default brand wali pankti se upar nahi jana hai.

**A6 · Animation timing ki ikaiyaan**
Engine ke andar saari timing **ms me normalize** hogi. Anticipation ka default **% of movement** (fps se azaad); frame-counts 24 fps ke hisaab se sirf reference. Entrance: UI elements 150–250 ms · aam overlays 0.3–0.5 s. Transition ki upari hadd default **0.8 s**; 1.5 s sirf cinematic profile me.

**A7 · Loudness destination table (ORDER #12 ka vistaar)**
YouTube/social **−14 LUFS** · Podcast **−16** (band −16..−20 tolerance ke saath) · Broadcast **−24 LUFS** · Netflix **−27 LUFS / TP −2**. Ek video, ek destination, ek target — pipeline me destination pehle tay hoga.

**A8 · Audio ke teen maps**
(i) **Relative dB under voice (18–25 dB)** = mixing ka default (voice-led content).
(ii) **Absolute dBFS seedhi** = broadcast delivery profile me hi.
(iii) **Ducker depth 2.7–5 dB** = subtle automation ka default; **−12 dB duck** = narration-led (podcast/interview) profile.
VO ka **−6 dBFS peak** ek production-stage check hai — peak aur integrated (LUFS) alag naap hain, dono saath chalenge, takraav nahi. SFX asset normalize −16 LUFS asset-level hai, master target nahi.

**A9 · Grade/LUT ki matra**
Default band **50–55%** (dono paksho ka sangat hissa). 70% tak sirf strong-look profile me, aur wo bhi human flag ke saath (grade sundarta se juda hai — seema).

**A10 · Delivery bitrate**
1080p: **10–24 Mbps** (YouTube upload ke liye upari hissa pasandeeda) · 4K: **35–68 Mbps**. Engine sirf range se bahar hone par flag karega; ek number thopna delivery ka kaam hai, creative rule ka nahi.

**A11 · Comedy timing**
Poora incident (setup→payoff) **8–14 s** aur ek beat **4–5 s** — alag ikaiyaan, dono chalenge. (Hamare travel/dharmik content me ye kam lagu hoga; record ke liye rakha hai.)

**A12 · Cover vs thumbnail**
Alag cheezein hain: CapCut **cover** (video ke andar ka title card) **1–5 shabd** chalega; **thumbnail** par purana faisla barkarar — target ≤3, hard cap 4.

**A13 · Kahani ki ghadi rhythm se upar**
Koi naya faisla nahi chahiye — ye ORDER ke meta-niyam 1 (Kahani > Rhythm) ka seedha istemal hai: sabse bade pal ko sabse lambi ghadi milegi, cadence ke numbers wahan khud jhukenge.

**A14 · Cross-references**
Sirf record — koi faisla nahi. Invisible-cut ↔ misdirection, staging ↔ dhyaan-anushaasan jaise rishte Step 4 ke aage ke versions me kaam aayenge.
