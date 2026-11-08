# Rules Part D1 — After Effects + Premiere (naye editor sources)

Step 2 ka chautha hissa. Sources: Step 1 ke AE/Premiere extractions (15 files) + licence-bahar sources ke notes (4 files).
Khaas chhaan-bin: sirf EDITING KE FAISLE rule bane hain — shudh tool-operation (API/ExtendScript/bridge commands) chhod di gayi hai (neeche ginti dekho).

**Kul: 96 rules** — Kahani 10 · Samajh 13 · Rhythm 27 · Style 46 · Saboot: 🟠 96 (saare craft/house/parampara numbers hain; is cluster me koi 🟢/🟡 measured study nahi mili) · Machine-checkable (check ke saath): 42

Do jaan-boojh ke GAYAB items: (1) koptsev63 ka Murch Rule-of-Six varnan purane science harvest me pehle se hai — duplicate nahi kiya. (2) ADAM-0S ka ducking 6–12 dB purane R-103 se bilkul milta hai, eacp1991 ka word-boundary cut purane R-195/C-090 se, aur LUFS −14/−16 purane targets se — inke naye rules nahi bane; sirf NAYE band (−24/−27) D1-010 me aaye hain.

## KAHANI (Kya — kahani, vaada, pal)

**D1-002 — Match cut — katne wale do shots me ek rishta rakho** 🟠
- Kab: Do shots ke beech cut lage aur seedha cut kamzor lage
- Kya: Match cut ki 4 kismo me se ek rakho — graphic (shape), movement, sound, ya idea/concept match
- Kyun: Bina rishte ka cut darshak ko jhatka deta hai; match se do alag shots ek soch ban jate hain
- Kitni baar: Har kamzor cut par kam se kam ek match prakar
- Check: —
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)

**D1-016 — Comedy incident ki 4-act ghadi** 🟠
- Kab: Koi comedy incident/mazaak wala pal kata jaye
- Kya: Incident ko ek lagatar 4-act ghatna ki tarah kaato: Premise/Setup 2.0–3.5 s (max 4.0) → Escalation 1.5–3.0 s (max 3.5) → Punchline/Climax 1.5–2.5 s (max 3.0) → Aftermath/Reaction 2.0–4.0 s (max 4.5); kul lambai 8–14 s (zyada se zyada 15 s)
- Kyun: Comedy ka samay hi uski jaan hai — setup chhota to prediction nahi banti, reaction chhota to hasi nahi uthti
- Kitni baar: Har comedy incident par ye ghadi
- Check: {"kind": "duration_range_s", "what": "comedy_incident_total", "min": 8, "max": 14}
- Source: notes_mmmnhat_agent-skills.md (note)
- ⚠️ Takraav/sambandh: koptsev63 ki pacing table comedy beat ko 4–5 s kehti hai (D1-075) — wo ek shot/beat ki baat hai, ye poore incident (4 acts) ki; dono ka paimana alag hai, Step 3 addendum me saaf ho

**D1-017 — Reaction ko bachao — punchline ke baad kam se kam 1.5 s** 🟠
- Kab: Comedy/action ke climax ke baad ka hissa kata jaye
- Kya: Vaardaat ke baad kam se kam 1.5 s ka reaction rakho; OUT sirf tab lo jab reaction settle ho jaye; reaction ko beech me kaatna sakht mana hai
- Kyun: Darshak ki hasi/ehsaas reaction me hi poora hota hai — use kaatna matlab punchline ko aadha karna
- Kitni baar: Har climax ke baad, bina apvaad
- Check: {"kind": "min_gap_s", "what": "reaction_after_event", "value": 1.5}
- Source: notes_mmmnhat_agent-skills.md (note)

**D1-018 — Ek incident = ek hi lagatar cut; lambi scene me climax window** 🟠
- Kab: Comedy incident ya isolated scene ka hissa chunna ho
- Kya: Ek incident ko ek hi lagatar cut rakho (4–11 s). Agar isolated scene 9 s se lambi ho to window climax ke aas-paas rakho: peak se 4 s pehle se peak ke 3.5 s baad tak. Bahut tang window (sirf peak −1.5 s) kabhi mat lo — premise mar jayegi
- Kyun: Beech se kaata incident apna setup kho deta hai; climax window me poori chhoti kahani bachti hai
- Kitni baar: Har incident/scene-isolation par
- Check: {"kind": "duration_range_s", "what": "comedy_single_cut", "min": 4, "max": 11}
- Source: notes_mmmnhat_agent-skills.md (note)

**D1-022 — Chhote target par W-curve reordering** 🟠
- Kab: 30 s jaise chhote target ke liye clips sajane hon
- Kya: Clips ko chronological kram ki jagah retention curve (W-curve) ke hisaab se dobara sajao — ya tez chronological fast-cut rakho; beech ka aadha-adhura kram nahi
- Kyun: Chhoti video me har second ko darshak ko pakadna hai; seedha chronological kram sabse mazboot pal ko beech me dubo deta hai
- Kitni baar: Har short-target compilation par
- Check: —
- Source: notes_mmmnhat_agent-skills.md (note)

**D1-029 — Selects pehle, master baad me** 🟠
- Kab: Kisi naye project ki edit shuru ho (Premiere/AE dono)
- Kya: Pehle bins/labels/markers ke saath ek selects sequence banao; structural beats aur shot ke maksad par markers lagao; master sequence uske baad hi banao
- Kyun: Seedha master banane se chunav aur banawat ek dusre me ghul jate hain aur galti mehngi padti hai
- Kitni baar: Har project me ek baar, shuruaat me
- Check: —
- Source: github_MuhammadAsad809_AI-EDITING-SKILL.md

**D1-045 — Motion piece = beats ki shrinkhala, ek lambi animation nahi** 🟠
- Kab: 10–15 s ka koi motion piece/intro/title sequence bane
- Kya: Use 3–6 alag beats ki shrinkhala ki tarah banao — har beat visual roop se padhne layak, ek hi visual system ke andar; final lockup ko padhne layak samay do
- Kyun: Ek lambi behlti animation me koi pal yaad nahi rehta; beats ki shrinkhala hi chhoti kahani banti hai
- Kitni baar: Har 10–15 s motion piece par 3–6 beats
- Check: {"kind": "duration_range_s", "what": "motion_sequence", "min": 10, "max": 15}
- Source: github_SebastianBoehler_autoresearch_after_effects_finetune.md

**D1-080 — Idea cut jaan-boojh ke — jahaan matlab takkar se bane** 🟠
- Kab: Documentary/teaser/montage me do shots jodne hon
- Kya: Wahan idea cuts lagao jahan do shots ki takkar se teesra matlab banta hai; narrative/continuity wali jagah par continuity cuts rakho — dono ko jaan-boojh ke alag rakho, galti se mishrit nahi
- Kyun: Idea cut hi montage ki jaan hai; galat jagah laga idea cut sirf gadbad lagta hai
- Kitni baar: Montage/teaser hisso me jaan-boojh ke
- Check: —
- Source: github_koptsev63_premiere-claude-bridge.md

**D1-081 — Decisive moment — out-point us par ya uske just baad** 🟠
- Kab: Har clip ka out-point tay ho
- Kya: Pehle clip ka decisive frame pehchano (jahan pal apne matlab par pahunchta hai); out-point ko usi par ya uske just baad rakho — usse pehle kabhi nahi
- Kyun: Decisive pal se pehle kaata clip apni baat aadhi keh kar ruk jata hai
- Kitni baar: Har clip par
- Check: —
- Source: github_koptsev63_premiere-claude-bridge.md

**D1-090 — Repeated take me sirf ek — aakhri complete take** 🟠
- Kab: Ek hi passage ke kai takes/repeats hon
- Kya: Direction/setup wali chatter hamesha kaato; repeated passages me bilkul ek hi take rakho — aakhri complete take
- Kyun: Do aadhe takes jodne se behtar ek poora take hai; chatter kahani ko sirf dheema karti hai
- Kitni baar: Har repeated passage par
- Check: —
- Source: github_ZeusSheen_ppro-agent-bridge.md

## SAMAJH AANA (Saaf sunai/dikhai, bina dhakka)

**D1-007 — Dialogue cleanup ka kram aur numbers** 🟠
- Kab: Dialogue/voice track saaf karna ho
- Kya: Isi kram me: normalize (peaks −12..−6 dBFS) → high-pass filter 80–100 Hz → room-tone noise print se de-noise → de-ess 4–8 kHz → halki compression 2:1–3:1
- Kyun: Galat kram me safai awaaz ko patla/kritrim kar deti hai; ye kram pehle badi gadbad, phir bareeki sambhalta hai aur baat saaf sunai deti hai
- Kitni baar: Har dialogue track par ek baar, mix se pehle
- Check: {"kind": "db_range", "field": "dialogue_peak_dbfs", "min": -12, "max": -6}
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)

**D1-008 — Har edit point par chhota audio crossfade** 🟠
- Kab: Koi bhi audio cut lage
- Kya: Har edit point par 2–4 frames ka audio crossfade lagao
- Kyun: Bina crossfade ke cut par click/pop sunai deta hai jo darshak ko baat se bahar kheenchta hai
- Kitni baar: Har audio edit point par, bina apvaad
- Check: —
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)
- ⚠️ Takraav/sambandh: ZeusSheen ka 2-frame fade rule (D1-089) isi baat ka khaas roop hai — sangat hai, takraav nahi

**D1-012 — Cut ke dono taraf kam se kam 60 ms asli khamoshi** 🟠
- Kab: Speech par cut lage (word-boundary par)
- Kya: Har cut edge ke dono taraf kam se kam 60 ms ki asli (true) khamoshi chhodo taaki audio crossfade saans le sake
- Kyun: Khamoshi ke bina laga cut shabd ke kinare ko kaat deta hai aur click deta hai; 60 ms crossfade ki saans hai
- Kitni baar: Har speech cut par
- Check: {"kind": "min_gap_ms", "what": "cut_edge_true_silence", "value": 60}
- Source: notes_eacp1991_premiere-agent.md (note)

**D1-019 — Zero frame bleed — padosi scene ka ek frame bhi nahi** 🟠
- Kab: Compilation/scene isolation me cut edges tay hon
- Kya: Kisi bhi cut edge par padosi scene ka 1–2 frame bhi bleed na ho. Compilation rips ke kinaro par chipke hue pichle/agle clip ke 2–5 s ko isolation me (±0.08 s safety ke saath) poora hatao
- Kyun: Ek bhi ajnabee frame darshak ko jhatka deta hai aur edit ko kaccha dikhata hai
- Kitni baar: Har cut edge par, bina apvaad
- Check: —
- Source: notes_mmmnhat_agent-skills.md (note)

**D1-028 — Staging ki takneek — aankh ko ek hi jagah le jao** 🟠
- Kab: Frame me main subject ko ubharna ho
- Kya: Depth of field/blur se background ko peeche rakho, vignette lagao, secondary elements ki opacity ghatao, aur main subject ko sabse zyada roshan rakho
- Kyun: Aankh sabse saaf/roshan cheez par jati hai — staging se darshak wahi dekhta hai jo dikhana hai
- Kitni baar: Har ahem frame/scene par
- Check: —
- Source: github_dylantarre_animation-principles.md
- ⚠️ Takraav/sambandh: Dhyaan-anushaasan wale merged rule (D1-057) se sambandhit hai — ye usi baat ke haath ke upaay hain

**D1-036 — B-roll dialogue ke upar — A1 ko kaate bina** 🟠
- Kab: B-roll schedule karna ho
- Kya: Track banawat rakho: V1 = A-roll, V2 = B-roll, V3 = overlays/text; A1 = dialogue, A2 = SFX, A3 = music. B-roll ko transitions aur key points ke upar rakho lekin A1 dialogue ko kabhi mat kaato
- Kyun: B-roll ka kaam baat ko dikhana hai, kaatna nahi; dialogue ki nirantarta hi samajh ki neev hai
- Kitni baar: Har edit me yehi track anushaasan
- Check: —
- Source: github_vamshicreates_premiere-editing-dna.md

**D1-050 — Text zones hamesha saaf — microcopy ka bandobast** 🟠
- Kab: Frame me text/copy ke saath decorative elements hon
- Kya: Decorative systems ko copy ke peeche ya kinare par rakho, text ke paas clutter kabhi nahi; aur chhota gray microcopy mat rakho — secondary text bhi padhne layak size/rang me ho
- Kyun: Text ke paas ki bheed padhna rok deti hai; na-padha-jane-wala text sirf shor hai
- Kitni baar: Har text-wale frame par
- Check: —
- Source: github_SebastianBoehler_autoresearch_after_effects_finetune.md

**D1-057 — Dhyaan ka anushaasan — ek frame, zyada se zyada do maang** 🟠
- Kab: Frame ki composition/motion tay ho
- Kya: Ek frame me do se zyada cheezein ek saath dhyaan na maangein; har frame me kam se kam ek crisp/sharp element rakho; aur jaan-boojh ke near-stillness (lagbhag sthirta) ke pal bhi rakho — sab kuchh har samay hilna zaroori nahi
- Kyun: Har hilti cheez chillaye to koi nahi sunai deta; sthirta ke pal hi harkat ko matlab dete hain
- Kitni baar: Har frame/scene par
- Check: —
- Source: github_Maciejdziuba_youtube-skills.md, github_LobzyJay_motion-design-with-claude.md
- ⚠️ Takraav/sambandh: dylantarre ki staging takneek (D1-028) isi anushaasan ko pane ke upaay deti hai — takraav nahi

**D1-083 — Black card ke neeche room tone — khamoshi kabhi nahi** 🟠
- Kab: Video me koi black card/blank aaye
- Kya: Black card ke neeche hamesha room tone rakho; poori khamoshi (silence) kabhi mat rakho
- Kyun: Asli khamoshi darshak ko 'video ruk gaya/band ho gaya' jaisa ehsaas deti hai; room tone use zinda rakhta hai
- Kitni baar: Har black card par
- Check: —
- Source: github_koptsev63_premiere-claude-bridge.md
- ⚠️ Takraav/sambandh: Paheli lage to: 'a talking cut is never silent' wala usi skill ka usool bhi yahi disha deta hai

**D1-086 — 30 ms ke andar speech = CLIPPED (shabd kata mana jayega)** 🟠
- Kab: Koi cut speech ke paas gire
- Kya: Agar cut se 30 ms ke andar speech hai to use defect mano — shabd kata hua hai; cut ko hamesha asli pause ke beech me rakho
- Kyun: Shabd ke kinare ka kataav sunne me sabse pehle pakda jata hai — yehi sabse sasti galti hai
- Kitni baar: Har cut par check
- Check: {"kind": "min_gap_ms", "what": "speech_to_cut_distance", "value": 30}
- Source: github_ZeusSheen_ppro-agent-bridge.md
- ⚠️ Takraav/sambandh: eacp1991 ka 60 ms crossfade niyam (D1-012) isse sakht hai — dono sangat disha me hain: 30 ms = kataav ki hadd, 60 ms = saaf cut ki shart

**D1-087 — Room tone ka jump 6 dB se zyada = defect** 🟠
- Kab: Do hisso ke beech cut lage
- Kya: Cut ke dono taraf ke room tone me 6 dB se zyada ka jump defect hai (LEVEL_JUMP) — room tone ka mel rakho, warna cut kaan ko sunai dega bhale dikhai na de
- Kyun: Kaan background ke badlav ko tasveer ke badlav se pehle pakadta hai
- Kitni baar: Har cut par
- Check: {"kind": "db_range", "field": "room_tone_jump_db", "min": 0, "max": 6}
- Source: github_ZeusSheen_ppro-agent-bridge.md

**D1-089 — Click hatana ho to aakhri 2 frames fade karo** 🟠
- Kab: Cut par click sunai de aur outgoing shabd soft decay par khatm ho raha ho
- Kya: Shabd ko kaatne ki jagah outgoing audio ke aakhri 2 frames par fade lagao — click jayega, shabd bachega
- Kyun: Click ka ilaaj shabd kaatna nahi hai; 2-frame fade sabse halka aur surakshit ilaaj hai
- Kitni baar: Har click wale cut par
- Check: —
- Source: github_ZeusSheen_ppro-agent-bridge.md
- ⚠️ Takraav/sambandh: ADAM-0S ka 2–4 frame crossfade niyam (D1-008) isi ka vistarit roop hai — sangat

**D1-091 — Bina-wajah ka A/V cut mismatch = defect** 🟠
- Kab: Video (V1) aur audio (A1) ke cut points alag jagah par hon
- Kya: Agar A/V cuts kuch frames idhar-udhar hain aur uski koi wajah nahi hai to use defect mano — cuts ek hi jagah par rakho
- Kyun: Bina wajah ka mismatch edit ko bikharra hua dikhata hai; jaan-boojh ka offset hi split edit kehlata hai
- Kitni baar: Har cut par
- Check: —
- Source: github_ZeusSheen_ppro-agent-bridge.md
- ⚠️ Takraav/sambandh: ADAM-0S ke split-edit niyam (D1-001) se takraav NAHI hai — wahan offset jaan-boojh ka aur 6–12 frames ka hota hai; ye sirf bina-wajah ke chhote mismatch ki baat hai

## RHYTHM (Ghadi, lay, pacing)

**D1-001 — Split edit default — audio/video ek point par na kaato** 🟠
- Kab: Dialogue/interview editing me koi bhi cut lage
- Kya: Audio aur video ke cut points ko 6–12 frames offset rakho: J-cut (agle scene ki awaaz pehle) anticipation/transition ke liye, L-cut (pichli awaaz nayi tasveer par) reaction/emotional carry-over ke liye
- Kyun: Seedha cut baatcheet me jarring lagta hai; split edit se baat ka pravah aur ehsaas cut ke paar beh jata hai
- Kitni baar: Dialogue me lagbhag 80% cuts split edits hone chahiye (source ka daava)
- Check: {"kind": "percent_range", "what": "split_edit_share_pct", "min": 70, "max": 100}
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)

**D1-004 — Rhythm editing — cut ko kisi taal par rakho** 🟠
- Kab: Sequence ki cutting ki lay tay karni ho
- Kya: Cuts ko in chaar taal me se kisi ek par rakho: music ke beats, tension ke saath badhti speed (emotional rhythm), shaant hisso me saans ki gati (breathing rhythm), ya bolne wale ki cadence
- Kyun: Bina taal ke cuts yaad nahi rehte; taal hi pacing ko ehsaas banati hai
- Kitni baar: Poore sequence me ek chuni hui taal consistent
- Check: —
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)

**D1-013 — Pause-removal ki perceptual floor — 250 ms** 🟠
- Kab: Khamoshi hatane (silence removal) ka threshold tay karna ho
- Kya: Threshold 250 ms se neeche kabhi mat rakho: boli hui connected speech me shabdon ke beech 30–200 ms ke articulation gaps hote hi hain — ye dead air nahi, awaaz ka hissa hai. Asli editorial pause (saans, hichkichahat, soch) lagbhag 250–300 ms se shuru hota hai; ladder 800 ms se 250 ms tak hi rakho
- Kyun: 250 ms se neeche ka threshold ek jumle ko ek-shabd wale tukdo me kaat dega — video saaf nahi, kata-kata lagega
- Kitni baar: Har silence-removal pass par floor 250 ms
- Check: {"kind": "min_gap_s", "what": "pause_removal_threshold", "value": 0.25}
- Source: notes_eacp1991_premiere-agent.md (note)
- ⚠️ Takraav/sambandh: SEEDHA TAKRAAV purane pause model se: purana model (ORDER #6) silence ≥400 ms = cut zone kehta hai; eacp1991 250 ms ko floor aur 250–300 ms ko editorial pause ki shuruaat manta hai — cut threshold 400 vs 250 ka faisla Step 3 addendum me hona chahiye

**D1-014 — Lead/trail margins — ASR drift ko soak karo** 🟠
- Kab: Transcript/word timings se cut points banein
- Kya: Cut se pehle lead margin rakho jo ASR ki aam 50–100 ms drift ko soak kare aur sunne wale ko shabd se pehle saans ki jagah de; margins ki working window 30–200 ms rakho (Calm preset me 500 ms tak ja sakti hai)
- Kyun: Word timings hamesha thode idhar-udhar hote hain; bina margin ke cut shabd ke kinare par girta hai
- Kitni baar: Har transcript-based cut par
- Check: {"kind": "padding_range_ms", "what": "lead_trail_margin", "min": 30, "max": 200}
- Source: notes_eacp1991_premiere-agent.md (note)
- ⚠️ Takraav/sambandh: Purana padding model bhi 30–200 ms window kehta hai (sangat hai), lekin Calm preset ka 500 ms us window se bahar hai — preset-wise apvaad Step 3 addendum me tay ho. ZeusSheen ke sentence padding (0.25/0.35 s, D1-085) se bhi sambandh hai — wo isse bade hain

**D1-015 — Pacing preset bina confirm kiye edit shuru mat karo** 🟠
- Kab: Kisi naye video/session ki editing shuru ho
- Kya: Pehle pacing preset tay karo — Calm / Measured / Paced (default) / Energetic / Jumpy — aur har preset ko chaar numbers me kholo: kitni lambi khamoshi hatani hai, kitni chhoti baat rakhne layak hai, lead margin, trail margin
- Kyun: Bina preset ke har cut ka faisla alag mood me hota hai aur video ki lay beech me badal jati hai
- Kitni baar: Har session/video me ek baar, shuruaat me
- Check: —
- Source: notes_eacp1991_premiere-agent.md (note)

**D1-021 — 1 second ya lambi khamoshi hamesha kategi** 🟠
- Kab: Pause removal/cleanup ka pass chale
- Kya: 1 second ya usse lambi bina-wajah ki khamoshi hamesha kaato
- Kyun: Ek second ki khamoshi video ko ruka hua mehsoos karati hai — retention wahi girta hai
- Kitni baar: Har cleanup pass me, bina apvaad
- Check: {"kind": "max_silence_s", "value": 1.0}
- Source: notes_mmmnhat_agent-skills.md (note)
- ⚠️ Takraav/sambandh: Yahi suite 10 ms tak ke chhote pauses kaatne ki kshamata bhi rakhti hai — wo sakhti eacp1991 ke 250 ms perceptual floor (D1-013) aur purane 400 ms threshold se seedha takraati hai; kshamata ko default mat bano — faisla Step 3 addendum me

**D1-023 — Animation timing ki frame-ghadi (Disney ghadi)** 🟠
- Kab: Kisi element ki animation ki lambai (frames me) tay karni ho
- Kya: Frames se ehsaas chuno: 2–4 frames = snappy/instant, 6–8 = quick/energetic, 12–15 = normal pace, 20–30 = slow/heavy, 40+ = dramatic/weighted
- Kyun: Frames hi animation ki bhasha hai — galat ghadi par halki cheez bhaari aur bhaari cheez khilona lagti hai
- Kitni baar: Har animation ki duration tay karte waqt
- Check: —
- Source: github_dylantarre_animation-principles.md
- ⚠️ Takraav/sambandh: LobzyJay ki ms-ghadi (D1-059) isse sangat hai: <150 ms instant, 150–250 halka, 250–500 standard, 500 ms–1 s bhaari, >1 s cinematic — 30 fps par dono takreeban milte hain

**D1-032 — Editing DNA naapo — andaz se style copy mat karo** 🟠
- Kab: Kisi editor/brand ki style copy karni ho ya apni house style tay karni ho
- Kya: Purane approved edits ko naap kar DNA nikalo: ASL (average shot length), pehle 5 s ka Hook ASL, cuts per minute, silence threshold, min silence, cut padding, SFX/music ke dB offsets — style ko shabdon me nahi, numbers me pakdo
- Kyun: Style ka andaz har baar badalta hai; naape hue numbers hi style ko dohrane layak banate hain
- Kitni baar: Har nayi style/brand ke liye ek baar; phir wahi numbers har video par
- Check: —
- Source: github_vamshicreates_premiere-editing-dna.md

**D1-033 — House pacing ka udaharan — Hook ASL 1.6 s, Body ASL 2.8 s** 🟠
- Kab: Tez house style ki pacing ka starting point chahiye
- Kya: Udaharan DNA ke numbers se shuru karo: Hook ASL 1.6 s (pehle 5 s; scene-detect threshold gt(scene, 0.26)) aur Body ASL 2.8 s; phir apne corpus se inhe badlo
- Kyun: Ek kaam karke dikhaya gaya house number bina-naap ke andaz se behtar shuruaat deta hai
- Kitni baar: Pacing ka reference point; har video par sakhti se nahi
- Check: —
- Source: github_vamshicreates_premiere-editing-dna.md
- ⚠️ Takraav/sambandh: koptsev63 ki film/teaser pacing table (D1-075) isse bahut dheemi hai (hooks 4–6 s) — farak format ka hai (short-form house style vs film/teaser); Step 3 addendum me format-wise pacing saaf ho

**D1-034 — Silence cutting ka house DNA — −35 dB, 0.28 s, padding 0.08 s** 🟠
- Kab: Silence-based cutting/auto-cut chalana ho
- Kya: House settings: silence detect threshold −35 dB, kaatne layak kam se kam khamoshi 0.28 s, har cut ke aas-paas padding 0.08 s (80 ms)
- Kyun: Ye teen numbers milkar tay karte hain ki kataav kitna tez aur kitna saaf hoga
- Kitni baar: Har auto-cut pass par yehi DNA (jab tak naya naapa na jaye)
- Check: {"kind": "min_gap_s", "what": "min_silence_to_cut", "value": 0.28}
- Source: github_vamshicreates_premiere-editing-dna.md
- ⚠️ Takraav/sambandh: TAKRAAV: min silence 0.28 s purane pause model (≥400 ms cut zone, ORDER #6) aur eacp1991 ke 250 ms floor (D1-013) ke beech me hai — teen alag thresholds (250/280/400) ka ek faisla Step 3 addendum me. Padding 0.08 s (80 ms) purane 30–200 ms window ke andar hai — sangat

**D1-038 — Element entrance ki ghadi — 0.4–1.2 s** 🟠
- Kab: Koi text/object/graphic screen par aaye
- Kya: Har element ke entrance ko 0.4–1.2 s ke beech rakho — isse tez par hichki, isse dheere par susti; aur final state ko padhne layak der tak rukne do
- Kyun: Entrance ki ghadi hi element ka wajan batati hai; padhne ki rukawat ke bina aaya-gaya element register nahi hota
- Kitni baar: Har entrance par
- Check: {"kind": "duration_range_s", "what": "element_entrance", "min": 0.4, "max": 1.2}
- Source: github_justajazz_ae-mcp-bridge.md
- ⚠️ Takraav/sambandh: ishu86 ke bands (D1-092: UI 0.3–0.5 s, text reveal 0.8–1.2 s) is range se aadhe overlap karte hain — element ke prakar se band chunna Step 3 addendum me saaf ho

**D1-044 — Stagger — 2–5 frames ki lay, padhne ki disha me** 🟠
- Kab: Kai related elements (letters, cards, list items, sections) ek ke baad ek aayein
- Kya: Elements ke beech 2–5 frames ka stagger rakho (text layers par 3–5 frames); stagger hamesha har element ki apni duration ka 10–20% rakho aur poori cascade ko ~24 frames ke andar band rakho. Samay me: letters ke liye tight 20–50 ms, lists/cards/words ke liye 50–100 ms, sections ke liye 100–200 ms. Kram padhne ki disha me rakho (upar se neeche, baayein se daayein); exits par stagger ulta chalao
- Kyun: Ek saath aate elements ek dhakka lagte hain; sahi stagger se aankh ek lay me poori list padh leti hai
- Kitni baar: Har multi-element reveal par
- Check: {"kind": "frame_range", "what": "stagger", "min": 2, "max": 5}
- Source: github_justajazz_ae-mcp-bridge.md, github_SebastianBoehler_autoresearch_after_effects_finetune.md, github_Maciejdziuba_youtube-skills.md, github_LobzyJay_motion-design-with-claude.md
- ⚠️ Takraav/sambandh: Naap ki ikai sources me alag hai — koi frames deta hai, LobzyJay ms bands (20–200 ms) deta hai; 30 fps par dono takreeban milte hain, lekin fps badalne par frames wala band hi pakdo — Step 3 addendum me ikai tay ho

**D1-046 — Attack tez, settle lamba — 2–4 frame attacks** 🟠
- Kab: Koi transition/move apne sabse tez hisse par ho
- Kya: Attacks ko 2–4 frames me rakho aur settles ko usse hamesha lamba; ladkhadaata hua (sloppy) beech ka hissa kahin na ho
- Kyun: Tez attack urja deta hai, lamba settle wajan aur aitbaar — ulta karne par motion sust aur nakli lagta hai
- Kitni baar: Har bade move/transition par
- Check: {"kind": "frame_range", "what": "attack_frames", "min": 2, "max": 4}
- Source: github_SebastianBoehler_autoresearch_after_effects_finetune.md

**D1-049 — Motion piece me nirnayak transition har 1.5–3 s** 🟠
- Kab: 10–15 s ka motion piece chal raha ho
- Kya: Har 1.5–3 s par ek nirnayak (decisive) transition rakho — isse lamba sukha antaral piece ko thanda kar deta hai
- Kyun: Motion piece ki urja transition ki lay se banti hai; lambi khamoshi wahan susti hai
- Kitni baar: Poore piece me, har 1.5–3 s
- Check: {"kind": "max_visual_gap_s", "value": 3}
- Source: github_SebastianBoehler_autoresearch_after_effects_finetune.md
- ⚠️ Takraav/sambandh: Purana default max visual gap 5 s (ORDER #2, talking video ke liye) isse dheema hai — ye 1.5–3 s ki lay SIRF motion-graphics pieces ke liye hai; Step 3 addendum me context alag saaf ho

**D1-054 — Exit hamesha entrance se tez — 0.6–0.8 guna** 🟠
- Kab: Koi element screen se jaye (exit animation)
- Kya: Exit ki duration entrance ki 0.6–0.8 guna rakho aur exit par accelerate karke jao (ease-in) — dheere float karke kabhi mat ruko
- Kyun: Jaane wali cheez par darshak ka dhyaan pehle hi ja chuka hota hai; dheema exit susti aur anakalpan lagta hai
- Kitni baar: Har exit animation par
- Check: {"kind": "percent_range", "what": "exit_vs_entrance_duration_pct", "min": 60, "max": 80}
- Source: github_Maciejdziuba_youtube-skills.md, github_LobzyJay_motion-design-with-claude.md

**D1-055 — Timing table 30 fps par — kaunsi harkat kitni lambi** 🟠
- Kab: Motion element ki duration tay karni ho
- Kya: 30 fps par ye table rakho: opacity fade 5–8 frames (150–270 ms), chhota entrance 8–12 frames (250–400 ms), object/product entrance 12–18 frames (400–600 ms), exit 6–10 frames (200–330 ms), scene transition 15–24 frames (500–800 ms), hero camera move 24–45 frames (800–1500 ms)
- Kyun: Bina table ke har duration andaz banti hai aur poori piece ki lay bikhar jati hai
- Kitni baar: Har motion element ki duration par
- Check: {"kind": "duration_range_s", "what": "scene_transition", "min": 0.5, "max": 0.8}
- Source: github_Maciejdziuba_youtube-skills.md
- ⚠️ Takraav/sambandh: ishu86 transitions ko 0.5–1.5 s kehta hai (D1-093) — upari hadd par farak (0.8 vs 1.5 s); dhyaan do dono ke neeche ke band (0.5 s) milte hain. justajazz ke entrance band (D1-038) se bhi aadha overlap hai

**D1-059 — Duration hi wajan hai — ms ki ghadi** 🟠
- Kab: Kisi bhi animation ki lambai (ms me) tay karni ho
- Kya: Wajan ke hisaab se ghadi chuno: <150 ms = instant/mechanical, 150–250 ms = halka/UI, 250–500 ms = standard brand motion, 500 ms–1 s = bhaari/editorial, >1 s = cinematic (ya bas bahut dheema). Har cheez ko ek hi ~300 ms par mat chalao — sab kuchh ek jaisi ghadi par chalana cheezon ko wajan-rahit bana deta hai
- Kyun: Aankh lambai se hi wajan padhti hai — ek ghadi sab par matlab koi ghadi kisi par nahi
- Kitni baar: Har animation duration par
- Check: —
- Source: github_LobzyJay_motion-design-with-claude.md
- ⚠️ Takraav/sambandh: ishu86 ke bands (D1-092: UI 0.3–0.5 s) is ghadi ke 'standard brand' hisse me padte hain — UI ko yahan halka (150–250 ms) kaha gaya hai; chhota farak Step 3 addendum me tay ho

**D1-063 — Sequential reveal metronome jaisa na ho** 🟠
- Kab: Kai cheezein ek ke baad ek reveal hon (timings ki shrinkhala)
- Kya: Reveals ke beech ke antar barabar mat rakho (200/400/600/800 ms jaisa metronome galat hai) — lay ko tod-tor kar rakho (jaise 0/180/340/550 ms)
- Kyun: Barabar antar machine jaisa lagta hai; tooti hui lay hi insaani taal aur dilchaspi deti hai
- Kitni baar: Har sequential reveal par
- Check: —
- Source: github_LobzyJay_motion-design-with-claude.md
- ⚠️ Takraav/sambandh: Stagger (D1-044) se takraav nahi — stagger ELEMENTS ke beech ka offset hai, ye bade reveals ke beech ke antar ki lay hai

**D1-072 — Visuals ko audio transients par bithao** 🟠
- Kab: Music/audio ke saath animation sync karni ho
- Kya: Har visual event ko audio ke asal transient (hit/beat) par bithao; kadam-ka-antarr (step interval) recording se naapo — (aakhri hit − pehli hit) / (steps − 1) — aur pehle transient ko pehla visual event banao; BPM ka andaz mat lagao
- Kyun: Sync ka ehsaas naape hue transients se hi aata hai; andaz wala sync hamesha thoda off lagta hai
- Kitni baar: Har audio-sync wali animation par
- Check: —
- Source: github_Mfrostbutter_claude-skills.md

**D1-075 — Shot ki lambai beat ke prakar se — film/teaser ghadi** 🟠
- Kab: Film/teaser/documentary ki pacing tay ho
- Kya: Beat ke hisaab se shot rakho: establishing/breath 5–8 s, hook/opening reveal 4–6 s, comedy beat 4–5 s, rhythmic action montage 2–4 s prati shot, interview/talking head 5–7 s (5 s se kam par baat kati hui lagti hai), title card 3–5 s (zor se padho + 1 s)
- Kyun: Har beat ki apni saans hoti hai — sab par ek ghadi chalana hi pacing ko marta hai
- Kitni baar: Har shot ka chunav isi ghadi se
- Check: {"kind": "duration_range_s", "what": "talking_head_shot", "min": 5, "max": 7}
- Source: github_koptsev63_premiere-claude-bridge.md
- ⚠️ Takraav/sambandh: Short-form house pacing (D1-033: Hook ASL 1.6 s) se bahut dheema — ye film/teaser ki ghadi hai; format ke hisaab se chunav Step 3 addendum me. Title card 3–5 s ishu86 (D1-093) se bilkul milta hai — sangat

**D1-076 — Sabse bade pal ko sabse lambi ghadi do** 🟠
- Kab: Emotional climax/payoff/end title ka shot tay ho
- Kya: Cinematic/emotional center ko 6–8 s, climax/payoff reveal ko 6–10 s (ye rhythm ke aam niyamo ko override karta hai), aur end title ko 6–10 s rakho
- Kyun: Sabse ahem pal ko sabse zyada waqt hi kahani ka hisaab hai — wahan jaldi karna matlab payoff ko sasta karna
- Kitni baar: Har climax/payoff/end title par
- Check: {"kind": "duration_range_s", "what": "climax_shot", "min": 6, "max": 10}
- Source: github_koptsev63_premiere-claude-bridge.md
- ⚠️ Takraav/sambandh: Tez-pacing wale purane rules (jaise max gap/ASL wale) se disha ka takraav hai — source khud kehta hai ye beats rhythm rules ko override karte hain; ORDER ki kahani-sabse-upar wali seedhi bhi yahi kehti hai

**D1-077 — Lambai ka ratio — sabse lamba shot sabse chhote ka 2–4 guna** 🟠
- Kab: Kisi teaser/sequence ki shot lambaiyan tay hon
- Kya: Sabse lambe shot ko sabse chhote ke 2–4 guna ke andar rakho; chaar lagatar shots ek hi lambai ke kabhi mat rakho; aur teen sabse ahem emotional beats ko hi teen sabse lambe shots banao
- Kyun: Ek-jaisi lambai lay ko sust karti hai; lambai ka utaar-chadhaav hi ehsaas ki seedhi hai
- Kitni baar: Poore sequence par laagoo
- Check: {"kind": "ratio_range", "what": "longest_to_shortest_shot", "min": 2, "max": 4}
- Source: github_koptsev63_premiere-claude-bridge.md

**D1-078 — Blink cut point — soch ke aakhir par kaato** 🟠
- Kab: Dialogue/performance me cut point chunna ho
- Kya: Cut ko soch ke aakhir par rakho; actor ki palak jhapakne (blink) wala frame cut-point ka swabhavik ummeedvaar hai — palak band hote hi cut chhupta hai
- Kyun: Insaan soch badalte waqt palak jhapakta hai — wahi pal darshak ke liye bhi cut ki swabhavik jagah hai
- Kitni baar: Har performance cut par pehla ummeedvaar yahi
- Check: —
- Source: github_koptsev63_premiere-claude-bridge.md
- ⚠️ Takraav/sambandh: Purane Murch/science rules se takraav nahi — unhi ka vyavharik roop hai

**D1-085 — Jumla-cut ki padding — 0.25 s pehle, 0.35 s baad** 🟠
- Kab: Rough cut me jumlo (sentences) ke hisse kaate jayein
- Kya: Har hisse ko pehle shabd se lagbhag 0.25 s pehle shuru karo aur aakhri shabd ke lagbhag 0.35 s baad khatm karo — hamesha asal source pause ke ANDAR rehkar; pause ke beech me kabhi mat kaato; agar chhota pause do hisso me bantna pade to 60% outgoing tail ko do. ASR timestamps ko ±0.2 s ki galti ke saath lo
- Kyun: Ye saans ki jagah hi bol ko insaani rakhti hai; kas kar kaata jumla ghuta hua lagta hai
- Kitni baar: Har sentence-level cut par
- Check: {"kind": "padding_range_ms", "what": "sentence_cut_padding", "min": 250, "max": 350}
- Source: github_ZeusSheen_ppro-agent-bridge.md
- ⚠️ Takraav/sambandh: TAKRAAV purane padding model se: purana edge padding 30–200 ms hai (frame-edge suraksha ke liye); ye 250/350 ms jumla-star ki saans hai — dono ki jagah alag hai lekin numbers takraate dikhte hain; Step 3 addendum me dono ki paribhasha alag saaf ho. eacp1991 ke margins (D1-014, 30–200 ms) se bhi yahi sambandh hai

**D1-088 — 0.5 s se chhota tukda = SLIVER — mat rakho** 🟠
- Kab: Cut ke baad koi bahut chhota tukda bane
- Kya: 0.5 s se chhote tukde ko hamesha hatao ya padosi me milao — sirf tab rakho jab wo music/SFX ke neeche jaan-boojh ka rakha fragment ho
- Kyun: Aadhe second ka tukda darshak ko sirf jhatka deta hai, koi matlab nahi
- Kitni baar: Har cut ke baad check
- Check: {"kind": "min_gap_s", "what": "min_piece_duration", "value": 0.5}
- Source: github_ZeusSheen_ppro-agent-bridge.md
- ⚠️ Takraav/sambandh: Shorts/teaser ke jaan-boojh ke tez tukdo (jaise mmmnhat ke <1.5 s teaser shots) se takraav sambhav hai — apvaad sirf jaan-boojh ke fragments ke liye hai, Step 3 addendum me saaf ho

**D1-092 — Chhote elements ki ghadi — UI 0.3–0.5 s, text reveal 0.8–1.2 s** 🟠
- Kab: Chhote motion elements (UI, text, logo/CTA) ki duration tay ho
- Kya: Bands rakho: UI elements 0.3–0.5 s, text reveals 0.8–1.2 s (kuch guidelines 0.5–1.5 s tak jati hain), logo/CTA reveal overshoot ke saath 0.4–0.6 s
- Kyun: Har prakar ke element ki apni padhne ki ghadi hai — UI ko text jitna aur text ko UI jitna samay dena dono galat hai
- Kitni baar: Har chhote element ki duration par
- Check: {"kind": "duration_range_s", "what": "text_reveal", "min": 0.8, "max": 1.2}
- Source: github_ishu86_after-effects-mcp.md
- ⚠️ Takraav/sambandh: justajazz ka aam entrance band 0.4–1.2 s (D1-038) inse overlap karta hai; LobzyJay ki ms-ghadi (D1-059) UI ko 150–250 ms kehti hai — 0.3–0.5 s usse dheema hai; element-prakar wise faisla Step 3 addendum me

**D1-093 — Bade pieces ki ghadi — logo 1–3 s, title card 3–5 s, loop 2–4 s** 🟠
- Kab: Poora logo animation, title card, transition ya ambient loop bane
- Kya: Bands rakho: poora logo animation 1–3 s, title cards 3–5 s, transitions 0.5–1.5 s, ambient loops 2–4 s
- Kyun: Bade pieces ko chhoto ki ghadi dene se wo ghate hue lagte hain, aur ulta karne se sust
- Kitni baar: Har bade piece ki duration par
- Check: {"kind": "duration_range_s", "what": "title_card", "min": 3, "max": 5}
- Source: github_ishu86_after-effects-mcp.md
- ⚠️ Takraav/sambandh: Title card 3–5 s koptsev63 (D1-075) se bilkul milta hai — sangat. Transitions 0.5–1.5 s ki upari hadd Maciejdziuba ke 0.5–0.8 s (D1-055) se takraati hai — neeche ka band (0.5) dono me ek hai

## STYLE / EFFECT (Sajawat, motion, rang, awaaz ki sajawat)

**D1-003 — Invisible cut ko harkat/roshni ke peeche chhupao** 🟠
- Kab: Cut dikhai de raha ho lekin kahani me seam nahi dikhana
- Kya: Cut ko whip pan, frame cross karte object, light flash ya rack-focus blur ke peeche chhupao
- Kyun: Darshak ki aankh harkat/roshni ke saath beh jati hai aur seam ghayab ho jata hai
- Kitni baar: Har dikhne wale problem cut par
- Check: —
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)
- ⚠️ Takraav/sambandh: koptsev63 ke misdirection rule (D1-079) se sambandhit hai — wo khaas taur par movement/sound spike ki baat karta hai; takraav nahi

**D1-005 — Grade ka kram aur LUT ki matra** 🟠
- Kab: Colour grade lagana ho (Premiere Lumetri ya Resolve nodes)
- Kya: Kram rakho: Basic/Primary correction (scopes se black/white point, white balance) → Creative (LUT/Look hamesha kam intensity par) → Curves → Wheels/Secondary → skin-tone protection. Creative LUT ki intensity 50–70% rakho; Rec709 material par blend ≤55% rakho
- Kyun: Poori taakat ka LUT rang bigaad deta hai; sahi kram se correction aur look alag-alag control me rehte hain
- Kitni baar: Har grade par; LUT intensity 50–70% (Rec709 par ≤55%)
- Check: {"kind": "percent_range", "what": "creative_lut_intensity_pct", "min": 50, "max": 70}
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note), github_koptsev63_premiere-claude-bridge.md
- ⚠️ Takraav/sambandh: Andar ka halka takraav: ADAM-0S 50–70% kehta hai, koptsev63 Rec709 par ≤55% ki hadd deta hai — sangat hissa 50–55%; Step 3 addendum me material-wise hadd tay ho

**D1-006 — Pehle hero shot grade karo, phir baaki ko milao** 🟠
- Kab: Ek scene ke kai shots ka grade match karna ho
- Kya: Pehle scene ka ek hero shot grade karke uska still bachao; phir har shot ko waveform (exposure), parade (balance), histogram (contrast), vectorscope (skin line) se usi still se milao
- Kyun: Har shot ko alag se grade karne se scene ke andar rang badalta rehta hai; hero shot se mel consistency deta hai
- Kitni baar: Har scene par ek hero shot pehle
- Check: —
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)

**D1-009 — Mix levels ki seedhi (dBFS)** 🟠
- Kab: Final mix ke levels tay karne hon
- Kya: Seedhi rakho: dialogue −12..−6 dBFS (sabse upar), dialogue ke neeche music −18..−24, bina dialogue ke featured music −12..−6, SFX −18..−6 (content ke hisaab se), ambience bed −24..−18
- Kyun: Levels ki seedhi hi tay karti hai ki kya sunai dega aur kya sirf mehsoos hoga; ulta-pulta mix baat dabaa deta hai
- Kitni baar: Poore mix me ye seedhi barkarar
- Check: {"kind": "db_range", "field": "music_under_dialogue_dbfs", "min": -24, "max": -18}
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)
- ⚠️ Takraav/sambandh: Purana niyam (ORDER #11) music ko voice ke RELATIVE 18–25 dB neeche kehta hai; ye band ABSOLUTE dBFS hai (−18..−24) — sankhya milti-julti hai lekin naap ka aadhar alag hai; Step 3 addendum me basis ek karna hoga

**D1-010 — Broadcast/Netflix loudness ke naye band** 🟠
- Kab: Delivery broadcast TV ya Netflix/cinema ke liye ho
- Kya: Integrated loudness destination ke hisaab se rakho: broadcast TV −24 LUFS, Netflix/cinema −27 LUFS (Netflix par true peak max −2 dBTP)
- Kyun: Har platform ki loudness shart alag hai; YouTube wala −14 wahan chalega nahi aur file reject/normalize hogi
- Kitni baar: Har delivery par destination-wise ek target
- Check: {"kind": "lufs_target", "value": -24, "tolerance": 1}
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note)
- ⚠️ Takraav/sambandh: Purane rules sirf −14 (YouTube) aur −16 (podcast/house) band dete hain — ye −24/−27 wale band naye hain; Step 3 addendum me destination-wise poori table banni chahiye (YouTube −14 / podcast −16 / broadcast −24 / Netflix −27)

**D1-011 — Delivery bitrate ki hadd (quality bachane ke liye)** 🟠
- Kab: Final export ki quality tay karni ho
- Kya: VBR 2-pass rakho; bitrate ke band: 1080p par lagbhag 10–24 Mbps, 4K par 35–68 Mbps, vertical (Reels/TikTok 1080×1920, 30 fps) 10–15 Mbps; master hamesha ProRes 422/DNxHR HQ jaisi quality me rakho
- Kyun: Bahut kam bitrate par saaf edit bhi keechad (muddy) dikhta hai — quality ka faisla export par bhi hota hai
- Kitni baar: Har delivery export par
- Check: —
- Source: notes_ADAM-0S_wayland-m3ta-0s.md (note), github_iart-ai_motion-design-skills.md
- ⚠️ Takraav/sambandh: Sources ke beech farak: ADAM-0S 1080p 16–24 Mbps / 4K 45–68 Mbps kehta hai; iart-ai H.264 delivery 1080p ~10–16 Mbps / 4K ~35–50 Mbps kehta hai — aam sangat hissa 16 Mbps (1080p) ke aas-paas hai; Step 3 addendum me ek band tay ho

**D1-020 — Climax par music ko −12 dB tak duck karo** 🟠
- Kab: Kisi scene ka climax/action peak aaye
- Kya: Background music ko climax moments par −12 dB tak auto-duck karo, aur climax SFX (punch/impact) ko apni alag jagah (track) par rakho taaki wo music se na lade
- Kyun: Climax par music aur asar ek saath chillayein to dono marte hain; duck se pal ki taakat saaf uthti hai
- Kitni baar: Har climax/action peak par
- Check: {"kind": "db_range", "field": "music_climax_duck_db", "min": -12, "max": -12}
- Source: notes_mmmnhat_agent-skills.md (note)
- ⚠️ Takraav/sambandh: Purana ducking niyam (R-103) dialogue ke neeche 6–12 dB duck kehta hai — ye climax par −12 dB ki khaas hadd hai; sangat disha, alag mauqa — Step 3 addendum me dono ki jagah saaf ho

**D1-024 — Anticipation ki bani-banai banawat (frames)** 🟠
- Kab: Koi bada action animate ho (jump, launch, reveal)
- Kya: Timeline ko aise banao: 0–10 frames wind-up (crouch/pull back) → 10–12 frames transition → 12–30 frames main action → 30–40 frames settle. Wind-up ke keyframes par easy ease rakho
- Kyun: Bina taiyaari ke action achanak teleport lagta hai; wind-up aankh ko aane wale zor ke liye taiyaar karta hai
- Kitni baar: Har bade action par; chhote UI moves par anupaat se chhota
- Check: —
- Source: github_dylantarre_animation-principles.md
- ⚠️ Takraav/sambandh: LobzyJay anticipation ko main action ka 20–30% kehta hai (D1-060) — ye 40-frame banawat me wind-up ~25% hi banta hai; sangat hai, paimana alag (absolute frames vs %) — Step 3 addendum me ek bhasha tay ho

**D1-025 — Follow-through — child elements ko 2–5 frames peeche rakho** 🟠
- Kab: Multi-part element (character, lockup, card system) rukta/move karta ho
- Kya: Child layers ke keyframes ko 2–5 frames offset rakho (ya ~0.05 s ka time-delay) taaki hisse ek saath na ruk kar ek ke baad ek settle hon
- Kyun: Sab kuchh ek hi frame par rukna nakli lagta hai; peeche chalte hisse wajan aur zindagi dete hain
- Kitni baar: Har multi-part motion par
- Check: {"kind": "frame_range", "what": "follow_through_offset_frames", "min": 2, "max": 5}
- Source: github_dylantarre_animation-principles.md
- ⚠️ Takraav/sambandh: Stagger wale merged rule (D1-044) se sambandhit hai — ye khaas taur par rukne/settle hone ki follow-through hai

**D1-026 — Exaggeration — asal se 20–50% aage** 🟠
- Kab: Character/brand animation me koi action padhne layak banana ho
- Kya: Values ko realistic se 20–50% aage badhao — bade scales, chaudi rotations, zyada dramatic timing
- Kyun: Camera/screen par asal jitna hi dikhana feeka padta hai; thoda badha hua hi saaf padhta hai
- Kitni baar: Character/brand motion par; product UI par nahi (wahan D1-052 dekho)
- Check: {"kind": "percent_range", "what": "exaggeration_pct", "min": 20, "max": 50}
- Source: github_dylantarre_animation-principles.md
- ⚠️ Takraav/sambandh: BADA TAKRAAV overshoot ki matra par: Maciejdziuba premium UI/product ke liye overshoot sirf 1.5–3% kehta hai (D1-052), LobzyJay follow-through ko move-distance ka 10–20% kehta hai (D1-061), aur LobzyJay ka pop example 110% (10% overshoot) hai — teen alag duniyayein (character animation / brand motion / premium UI); Step 3 addendum me context-wise faisla zaroori

**D1-027 — Squash & stretch me volume constant rakho** 🟠
- Kab: Koi object dabta/kheenchta (squash-stretch) ho
- Kya: Jab Y compress ho to X ko ulta expand karo — X × Y lagbhag constant rakho taaki object ka volume bana rahe
- Kyun: Bina volume-bachat ke deformation object ko phula hua ya pichka hua khilona bana deta hai
- Kitni baar: Har squash-stretch wale move par
- Check: —
- Source: github_dylantarre_animation-principles.md

**D1-030 — Effect-heavy kaam alag rakho, intensity revise ho sake** 🟠
- Kab: Koi bhaari effect/compositing lagana ho
- Kya: Effect-heavy kaam adjustment layers ya nests par rakho taaki uski intensity baad me revise ho sake; aur hamesha sabse chhota native tool chuno jo kaam kare
- Kyun: Clip par seedha chipka effect badalna mushkil hota hai; alag parat par rakha effect ek slider se kam-zyada ho sakta hai
- Kitni baar: Har bhaari effect par
- Check: —
- Source: github_MuhammadAsad809_AI-EDITING-SKILL.md

**D1-031 — AE sirf zaroori shots ke liye — editorial structure ka badal nahi** 🟠
- Kab: Koi shot After Effects me bhejna ho
- Kya: AE ko tracked graphics/compositing/typography ke liye rakho, editorial structure ke badle ke roop me nahi; sirf wahi shots bhejo jinhe zaroorat ho, handles bachakar bhejo, aur color management + motion blur wahan verify karo
- Kyun: Har shot ko AE me ghumana samay aur structure dono kharab karta hai; kataav (editing) NLE me hi rehta hai
- Kitni baar: Har AE round-trip par
- Check: —
- Source: github_MuhammadAsad809_AI-EDITING-SKILL.md

**D1-035 — Punch-in alternating — har dusre cut par 100% ↔ 112%** 🟠
- Kab: Talking-head/A-roll me jaan-boojh ki house style ke tor par punch-in lagana ho
- Kya: Har dusre cut par scale badlo: ek cut 100%, agla 112% — isi alternating lay me poora video
- Kyun: Regular lay wala punch-in style ki pehchan ban jata hai aur static frame me harkat deta hai
- Kitni baar: Har dusre cut par, poore video me consistent
- Check: {"kind": "percent_range", "what": "punch_in_scale_pct", "min": 112, "max": 112}
- Source: github_vamshicreates_premiere-editing-dna.md
- ⚠️ Takraav/sambandh: SEEDHA TAKRAAV purane faisle se (ORDER #5): punch-in sirf motivated, ≤10/min, gaps ≥4 s. Ye house style bina-wajah har dusre cut par punch-in karta hai — Body ASL 2.8 s par har dusra cut ≈ 10–11 baar/min banta hai, yaani purani hadd ke bilkul kinare/par. Step 3 addendum me house-style apvaad tay ho

**D1-037 — House mix offsets — SFX −9 dB, music bed −20 dB** 🟠
- Kab: House style me final mix ke offsets tay karne hon
- Kya: Dialogue ko 0 dB reference rakho; SFX uske −9 dB par, music bed −20 dB par (dialogue ke neeche ducked)
- Kyun: Reference ke saapeksh offsets har video me ek jaisi awaaz ki pehchan banate hain
- Kitni baar: Poore mix me constant
- Check: {"kind": "db_range", "field": "music_bed_db_under_voice", "min": -20, "max": -20}
- Source: github_vamshicreates_premiere-editing-dna.md
- ⚠️ Takraav/sambandh: Music −20 dB purane relative band (18–25 dB neeche, ORDER #11) ke andar hai — takraav nahi. Lekin ADAM-0S ki absolute dBFS seedhi (D1-009) se naap ka aadhar alag hai — dono ko ek table me rakhna Step 3 addendum ka kaam

**D1-039 — Timing ki hierarchy — ahem pehle, container pehle, focal aakhir me** 🟠
- Kab: Koi lockup/scene kai elements ke saath animate ho
- Kya: Kram rakho: sabse ahem element (primary mark/logo) pehle ya 50 ms ki head-start ke saath aaye; container apne content se pehle move kare; baaki uske baad lay me aayein (jaise wordmark +80 ms, tagline uske +200 ms baad); sabse sajawati element sabse aakhir me aur sabse dheere land kare; focal element sabse aakhir ya sabse strong land kare
- Kyun: Jo pehle/strong land karta hai wahi aankh ka malik banta hai — hierarchy ka ulta matlab dhyaan ka ulta
- Kitni baar: Har multi-element entrance par
- Check: —
- Source: github_justajazz_ae-mcp-bridge.md, github_LobzyJay_motion-design-with-claude.md

**D1-040 — Overshoot me poora object react kare** 🟠
- Kab: Koi element overshoot ke saath land kare
- Kya: Overshoot sirf ek dimension (jaise height) par mat rakho — poori cheez react kare (width, scale, position sab saath), aur element apni momentum ko aage carry-through kare
- Kyun: Aadha react karta object rubber ka khilona lagta hai; poora react karta object wajan wala lagta hai
- Kitni baar: Har overshoot landing par
- Check: —
- Source: github_justajazz_ae-mcp-bridge.md
- ⚠️ Takraav/sambandh: Overshoot ki MATRA par takraav D1-052/D1-061/D1-026 me darj hai — ye rule sirf react karne ke DHANG ki baat karta hai

**D1-041 — Ek object ki saari properties ek hi frame par finish hon** 🟠
- Kab: Ek hi object ki kai properties (position/scale/opacity) animate hon
- Kya: Un sabko ek hi frame par khatm karo — sync me; aur saath aane wale text/group ko ek saath treat karo, tukdo me nahi
- Kyun: Alag-alag frame par rukti properties object ko bikhra hua aur animation ko adhura dikhati hain
- Kitni baar: Har multi-property animation par
- Check: —
- Source: github_justajazz_ae-mcp-bridge.md
- ⚠️ Takraav/sambandh: Follow-through (D1-025) iska ulta nahi hai — wahan alag-alag OBJECTS offset hote hain, yahan EK object ki properties sync hoti hain

**D1-042 — Number counter ki ghadi — 0.3 s ruk, 1.2 s ginti** 🟠
- Kab: Koi number/statistic animate hokar gina jaye
- Kya: Counter ko 0.3 s ki delay ke baad shuru karo aur 1.2 s me ease ke saath target value tak pahunchao
- Kyun: Turant shuru hua counter nazar se chook jata hai; bina ease ki ginti machine jaisi lagti hai
- Kitni baar: Har animated counter par
- Check: —
- Source: github_justajazz_ae-mcp-bridge.md

**D1-043 — Motion blur — har moving layer par, shutter 180 default** 🟠
- Kab: Koi layer/element move kare (AE/motion work)
- Kya: Motion blur har moving layer par ON rakho. Shutter angle ka default 180° (natural); crisp UI ke liye 90–120°, tez sweeps ke liye 200–300°; samples ~32. Blur ki matra velocity ke anupaat me rakho — jo element frame me sirf kuch pixels hi hilta hai us par blur OFF
- Kyun: Bina blur ke tez motion strobe karta hai; zyada blur chhoti harkat ko keechad bana deta hai
- Kitni baar: Har moving layer par; shutter context ke hisaab se
- Check: —
- Source: github_justajazz_ae-mcp-bridge.md, github_Maciejdziuba_youtube-skills.md

**D1-047 — Transition me hard cut pehle, crossfade aakhir me** 🟠
- Kab: Motion piece me scenes/beats ke beech transition chunna ho
- Kya: Hard cuts, matte wipes, shutters aur element-led transitions ko pehle chuno; crossfade ko default mat bano
- Kyun: Crossfade sabse kamzor aur sabse zyada istemal hone wala transition hai — nirnayak transition hi piece ko professional deta hai
- Kitni baar: Har transition par pehle nirnayak vikalp socho
- Check: —
- Source: github_SebastianBoehler_autoresearch_after_effects_finetune.md

**D1-048 — Ek piece, ek hi dominant visual grammar** 🟠
- Kab: Motion piece ka visual system tay ho
- Kya: Poore piece me ek hi dominant visual grammar rakho (ek hi bhasha: type-led, ya shape-led, ya image-led); beech me dusri bhasha mat ghusao
- Kyun: Har scene nayi bhasha bole to piece bikhar jata hai; ek grammar hi pehchan aur aitbaar banati hai
- Kitni baar: Har piece par ek grammar
- Check: —
- Source: github_SebastianBoehler_autoresearch_after_effects_finetune.md

**D1-051 — Amateur lage to pehle element count ghatao** 🟠
- Kab: Koi motion scene banana par bhi amateur/sasta lage
- Kya: Pehla ilaaj hamesha dikhne wale elements ki ginti ghatana hai; aur final lockup ko beech ke scenes se simple aur zyada confident rakho
- Kyun: Zyada elements = zyada shor; sadgi hi mehenga dikhne ka sabse sasta raaz hai
- Kitni baar: Har amateur lagne wale scene par, effects badhane se pehle
- Check: —
- Source: github_SebastianBoehler_autoresearch_after_effects_finetune.md

**D1-052 — Premium UI/product overshoot — sirf 1.5–3%** 🟠
- Kab: Premium/product/UI motion me element land kare
- Kya: Overshoot ko sirf 1.5–3% rakho; damped settle ka namuna: 100 → 102 → 99.5 → 100 (frames 3/2/2 me)
- Kyun: Is duniya me zyada overshoot sasta padhta hai — premium ka matlab hai asar dikhe bina mehnat dikhe
- Kitni baar: Har premium UI/product landing par
- Check: {"kind": "percent_range", "what": "overshoot_pct_premium", "min": 1.5, "max": 3}
- Source: github_Maciejdziuba_youtube-skills.md
- ⚠️ Takraav/sambandh: BADA TEEN-TARAFA TAKRAAV: dylantarre character animation ke liye exaggeration +20–50% kehta hai (D1-026); LobzyJay brand motion ke liye follow-through overshoot move-distance ka 10–20% aur pop 110% kehta hai (D1-061/D1-065); ye 1.5–3% SIRF premium UI/product ke liye hai. Step 3 addendum me context-wise table zaroori: UI/product 1.5–3% / brand 10–20% / character 20–50%

**D1-053 — Easing kabhi symmetric nahi — asymmetric influence hi premium hai** 🟠
- Kab: Kisi bhi move ke keyframes par easing lagani ho
- Kya: Keyframe influence ko jaan-boojh ke asymmetric rakho: premium ease-out ke liye key1 out ~12 / key2 in ~84; weighted hero in-out 38/78; pass-through 20 / 54-54 / 88; floor impact par 0.5/0.5 (bilkul cushioning nahi); apex/hang par 90/90. Aam taur par entrance par pehle key ka out-influence kam aur dusre ka in-influence zyada (mazboot ease-out ~80, halka ~33) rakho. Default Easy Ease (~33) ya symmetric 50/50 ko aakhri haal mat samjho
- Kyun: Symmetric/default easing hi amateur ki sabse pehchanne layak nishani hai; asymmetric curve hi wajan aur maksad deti hai
- Kitni baar: Har keyframed move par
- Check: —
- Source: github_Maciejdziuba_youtube-skills.md, github_LobzyJay_motion-design-with-claude.md, github_Mfrostbutter_claude-skills.md
- ⚠️ Takraav/sambandh: LobzyJay ki chetaavni: easing ke numbers koi jaadu nahi — galat maksad par sahi number bhi bekaar hai; pehle faisla (entrance hai ya exit, halka hai ya bhaari), phir number

**D1-056 — Shadow ki teen paratein — kabhi pure black nahi** 🟠
- Kab: Kisi element ko realistic shadow deni ho
- Kya: Shadow ko teen blurred copies se banao: contact (blur ~9, opacity ~21%), occlusion (blur ~22, opacity ~11%), ambient (blur ~64, opacity ~5%). Blur radius offset ka 2–3 guna rakho; vertical squash 30–40% rakho; shadow ka rang kabhi pure black nahi — halka cool dark violet/neutral rakho
- Kyun: Ek hi hard shadow nakli lagti hai; teen naram paratein aur rang-daar andhera hi asal roshni jaisa padhta hai
- Kitni baar: Har realistic shadow par
- Check: —
- Source: github_Maciejdziuba_youtube-skills.md

**D1-058 — Glow/bloom ka hisaab — stack aur frame ka hissa** 🟠
- Kab: Kisi element ko glow/bloom dena ho
- Kya: Glow ko blurred copies ke stack se banao (jaise blur 4px/42%, 22px/17%, 92px/6% — radius dugna to opacity aadhi); bloom ko frame ke sirf 5–20% hisse tak rakho; glass/translucent cheezon par glow ke liye Screen mode rakho, Add nahi
- Kyun: Poora frame chamke to kuchh nahi chamakta; seemit bloom hi mehnga aur jaan-boojh ka lagta hai
- Kitni baar: Har glow ke istemal par
- Check: {"kind": "percent_range", "what": "bloom_frame_coverage_pct", "min": 5, "max": 20}
- Source: github_Maciejdziuba_youtube-skills.md

**D1-060 — Anticipation — main action ka 20–30%** 🟠
- Kab: Koi badi harkat (move/launch/jump) animate ho
- Kya: Anticipation ko main action ki duration ka 20–30% rakho (jaise 400 ms ke move se pehle 80–120 ms ki taiyaari); uski matra chhoti rakho — ~300 px ke move se pehle ulta disha me sirf ~15–25 px ka kheenchav
- Kyun: Bina taiyaari ki harkat teleport lagti hai; zyada taiyaari use sust bana deti hai
- Kitni baar: Har badi harkat se pehle
- Check: {"kind": "percent_range", "what": "anticipation_vs_action_pct", "min": 20, "max": 30}
- Source: github_LobzyJay_motion-design-with-claude.md
- ⚠️ Takraav/sambandh: dylantarre ki frame-banawat (D1-024) me wind-up ~40-frame action ka ~25% banta hai — sangat; paimana alag hai (absolute frames vs pratishat)

**D1-061 — Follow-through overshoot — move-distance ka 10–20%** 🟠
- Kab: Brand motion me element apni jagah par land kare
- Kya: Landing par element ko target se aage move-distance ka 10–20% tak overshoot karao, phir use main duration ke 20–40% samay me settle karo; overshoot wala keyframe target ke 3–5 frames aage rakho; secondary elements ke aakhri keyframes primary ke 3–6 frames baad land hon
- Kyun: Thoda sa aage nikal kar wapas aana hi harkat ko zinda aur wajan-daar banata hai
- Kitni baar: Har badi landing par
- Check: {"kind": "percent_range", "what": "follow_through_overshoot_pct_of_distance", "min": 10, "max": 20}
- Source: github_LobzyJay_motion-design-with-claude.md
- ⚠️ Takraav/sambandh: Overshoot ke teen-taraffa takraav ka hissa (D1-052 me poora varnan): ye 10–20% brand motion ke liye hai; premium UI 1.5–3%, character exaggeration 20–50% — Step 3 addendum me context table bane

**D1-062 — Inertial bounce ke tuned defaults** 🟠
- Kab: Landing ke baad element ko natural bounce/settle dena ho
- Kya: Damped oscillation ke defaults se shuru karo: amp 0.04–0.12 (default ~0.08), freq 2.0–4.0 (default ~2.0–2.5), decay 4–8 (UI) / 2–4 (naram material) / default ~5; bounce ka asar pehle 1 s ke andar hi khatm ho jana chahiye (t < 1 s)
- Kyun: Andaz se lagaya bounce ya to hilta hi nahi ya jelly ban jata hai; ye defaults production me ghise hue hain
- Kitni baar: Har bounce/settle par starting point
- Check: —
- Source: github_LobzyJay_motion-design-with-claude.md, github_iart-ai_motion-design-skills.md, github_chvndler_aeft.jsx.md

**D1-064 — Midpoint check — transition ka beech wala frame bhi design ho** 🟠
- Kab: Koi bhi transition bane
- Kya: Transition ke 50% wale frame ko alag se dekho — wo kisi jaan-boojh ke design state jaisa lagna chahiye, do states ke beech ka dhundhla saump nahi
- Kyun: Darshak beech ke frame ko bhi dekhta hai; bekaar midpoint poori transition ko sasta kar deta hai
- Kitni baar: Har transition par ek baar check
- Check: —
- Source: github_LobzyJay_motion-design-with-claude.md

**D1-065 — Pop ka snap — 0 se 110%, phir 100%** 🟠
- Kab: Kisi element ko pop ke saath land karana ho
- Kya: Scale ko 0 se shuru karke 0.25 s par 110% tak le jao, phir 0.4 s par 100% par settle karo
- Kyun: Thoda sa overshoot karke rukna hi pop ko padhne layak aur mazedaar banata hai
- Kitni baar: Har pop-style landing par
- Check: {"kind": "duration_range_s", "what": "pop_total", "min": 0.4, "max": 0.4}
- Source: github_LobzyJay_motion-design-with-claude.md
- ⚠️ Takraav/sambandh: Iska 10% overshoot Maciejdziuba ke premium band (1.5–3%, D1-052) se takraata hai — ye brand/marketing pop ke liye hai, premium UI ke liye nahi; context table Step 3 addendum me

**D1-066 — Exit ka raasta = entry ka ulta raasta** 🟠
- Kab: Koi element jis raaste se aaya tha usi se wapas jaye
- Kya: Exit path ko entry path ka ulta rakho — jo neeche se aaya wo neeche hi jaye; alag raaste se gayab hona teleport jaisa lagta hai
- Kyun: Aankh cheez ko usi raaste par dhoondhti hai jahan se wo aayi thi; raasta badalna = cheez ka badal jana
- Kitni baar: Har exit par jahan entry bhi dikhi ho
- Check: —
- Source: github_LobzyJay_motion-design-with-claude.md

**D1-067 — Zoom aur pan ek saath kabhi nahi** 🟠
- Kab: Camera jaisi harkat (scale + position) design ho
- Kya: Ek hi harkat me zoom aur pan dono mat chalao — pehle ek, phir dusra
- Kyun: Dono saath chalein to frame behka hua aur sasta lagta hai; aankh kisi ek ko bhi follow nahi kar pati
- Kitni baar: Har camera-style move par
- Check: —
- Source: github_LobzyJay_motion-design-with-claude.md

**D1-068 — Camera move ki matra — push-in 2–6%, drift seemit** 🟠
- Kab: Koi camera jaisi harkat (push/drift/rotation) design ho
- Kya: Matra seemit rakho: push-in 1–1.5 s me kul 2–6% zoom; lateral drift 1–2 s me 20–80 px; rotation 0.5–2° (jaan-boojh ke reveal par hi 3–5°); product shots ke liye lambi focal length jaisa ehsaas (70–120 mm ke barabar)
- Kyun: Camera ki harkat mehsoos honi chahiye, dikhni nahi — zyada matra hi use sasta bana deti hai
- Kitni baar: Har camera move par
- Check: {"kind": "percent_range", "what": "push_in_pct", "min": 2, "max": 6}
- Source: github_Maciejdziuba_youtube-skills.md

**D1-069 — Camera hamesha subject se dheema — 1.5–2.5 guna lambi ghadi** 🟠
- Kab: Subject aur camera dono move karein
- Kya: Camera ki movement ki duration object ki duration ki 1.5–2.5 guna rakho; ek section me ek hi jaan-boojh ka camera idea rakho (push, ya track, ya orbit, ya parallax — sab nahi); bina maksad ka perpetual drift kabhi nahi
- Kyun: Tez camera harkat ko kha jata hai; dheema camera use wajan deta hai aur bhatkav mita deta hai
- Kitni baar: Har camera + subject wale scene par
- Check: —
- Source: github_Maciejdziuba_youtube-skills.md

**D1-070 — Finish ki parat — halka grain, near-black background** 🟠
- Kab: Motion piece ka final polish/render ho
- Kya: Project ko 16 bpc par rakho (32 bpc nahi — koi fayda nahi, sirf bojh); adjustment layer par 1.5–2% mono noise grain lagao (banding chhupta hai, premium texture aata hai); backgrounds ko near-black rakho, pure black (0,0,0) kabhi nahi
- Kyun: Banding aur khaali kaala rang hi do sabse aam 'sasta' nishaan hain; grain aur near-black dono ko ek saath sambhalte hain
- Kitni baar: Har final render se pehle
- Check: {"kind": "percent_range", "what": "grain_noise_pct", "min": 1.5, "max": 2}
- Source: github_Maciejdziuba_youtube-skills.md

**D1-071 — Accent pop ki ghadi — chamak 0.13 s me peak** 🟠
- Kab: Chhota accent (sparkle/glint/star) pop karna ho
- Kya: Pop ki ghadi rakho: scale 0 se shuru, lagbhag +0.13 s par peak (~135%) par, +0.50 s tak wapas 0; opacity flash +0.07 s tak 100 par aur +0.45 s tak khatm
- Kyun: Accent ka kaam ek pal ki chamak hai — dheema pop dhyaan kheench kar bojh ban jata hai
- Kitni baar: Har chhote accent pop par
- Check: —
- Source: github_Mfrostbutter_claude-skills.md

**D1-073 — Generated SFX ko pehle normalize karo — I=−16 LUFS** 🟠
- Kab: AI/generated SFX ko edit me milana ho
- Kya: Generated SFX samples ko pehle loudnorm I=−16 LUFS : TP=−1.5 dB : LRA=11 par laakar phir pipeline me milao
- Kyun: Bina normalize kiye generated awaazein har baar alag zor par aati hain aur mix bikhar jata hai
- Kitni baar: Har generated SFX asset par, milane se pehle
- Check: {"kind": "lufs_target", "value": -16, "tolerance": 1}
- Source: github_Mfrostbutter_claude-skills.md
- ⚠️ Takraav/sambandh: Ye ASSET-level normalization hai, final master ka loudness target nahi — purana master target −14 LUFS (YouTube) isse alag cheez hai; Step 3 addendum me asset vs master ka farak saaf likha jaye

**D1-074 — Wiggle hamesha maksad ke saath** 🟠
- Kab: Kisi layer par wiggle/ambient harkat lagani ho
- Kya: Wiggle ko maksad ke hisaab se chuno: ambient drift ke liye wiggle(0.5, 8), mechanical jitter ke liye wiggle(24, 2); bina-socha wiggle(5, 20) jaisa raw wiggle mat lagao — wo harkat nahi, shor hai
- Kyun: Har harkat ka matlab hona chahiye; matlab-rahit harkat frame ko sasta aur bechain karti hai
- Kitni baar: Har wiggle ke istemal par
- Check: —
- Source: github_LobzyJay_motion-design-with-claude.md

**D1-079 — Misdirection — cut ko harkat ya awaaz ke dhakke peeche chhupao** 🟠
- Kab: Koi cut zyada dikh raha ho
- Kya: Cut point par achanak harkat ya sound spike (darwaza band, taali jaisi tez awaaz) rakho — darshak ka dhyaan wahan jayega aur cut ghayab ho jayega
- Kyun: Aankh aur kaan hamesha sabse tez nayi cheez ke peeche bhagte hain — usi pal me seam ghul jati hai
- Kitni baar: Har dikhne wale cut par
- Check: —
- Source: github_koptsev63_premiere-claude-bridge.md
- ⚠️ Takraav/sambandh: ADAM-0S ke invisible-cut upaayo (D1-003) se sambandhit — ye sirf cut-point wale dhakke ki baat karta hai

**D1-082 — Stabilize sirf outliers ko — blanket kabhi nahi** 🟠
- Kab: Handheld footage ko stabilize karna ho
- Kya: Sirf un shots ko stabilize karo jo baakio ke muqable me zyada hilte hain (relative outliers); poori film par blanket stabilization kabhi mat chalao
- Kyun: Zyada safai jaan-boojh ki handheld urja ko maar deti hai — documentary ka sach hi us harkat me hai
- Kitni baar: Har stabilization faisle par
- Check: —
- Source: github_koptsev63_premiere-claude-bridge.md

**D1-084 — End card fade ke baad, black par** 🟠
- Kab: End card/title lagana ho
- Kya: End card ko fade ke BAAD, black ke upar rakho — aakhri frame ke upar title chipkana galat hai
- Kyun: Aakhri frame par chipka title dono ko kharab karta hai; black par saaf card hi khatma deta hai
- Kitni baar: Har end card par
- Check: —
- Source: github_koptsev63_premiere-claude-bridge.md

**D1-094 — Spring presets — mood ke hisaab se spring chuno** 🟠
- Kab: Spring-based motion ka ehsaas tay karna ho
- Kya: Mood se spring chuno: gentle/soft = stiffness 80, damping 20 (koi overshoot nahi); default = 100/10 (halka overshoot); wobbly/playful = 150/8 (zyada overshoot); stiff/snappy = 200/20; slow/heavy = mass 3 ke saath 100/15; visual bounce chahiye to 200/5; tez UI feedback = mass 0.5 ke saath 300/20
- Kyun: Spring ke numbers hi ehsaas hain — ek hi spring har mood par chalana sab ko ek jaisa bana deta hai
- Kitni baar: Har spring animation par mood ke hisaab se ek preset
- Check: —
- Source: github_ishu86_after-effects-mcp.md
- ⚠️ Takraav/sambandh: Inertial bounce wale defaults (D1-062) se sambandhit hai — wahan damped oscillation AE expressions me hai, yahan spring physics ke presets hain; takraav nahi

**D1-095 — Parallax ki gehrai — 0.2 / 0.5 / 1.0** 🟠
- Kab: Parallax/depth wala scene bane
- Kya: Ek hi controller ko animate karo aur layers ko uske ansh (fraction) do: door ka background 0.2, midground 0.5, foreground 1.0
- Kyun: Har layer ko alag se animate karna bikharav hai; ek controller ke fractions se gehrai khud-ba-khud sahi banti hai
- Kitni baar: Har parallax scene par
- Check: —
- Source: github_ishu86_after-effects-mcp.md

**D1-096 — Aakhri frame murda na baithe — slow push-in rakho** 🟠
- Kab: Koi reveal/logo animation apne end frame par ruke
- Kya: End frame par halka slow push-in rakho taaki final frame zinda lage, murda still na lage
- Kyun: Bilkul ruka hua aakhri frame video ko khatm nahi, atak gaya mehsoos karata hai
- Kitni baar: Har reveal ke end frame par
- Check: —
- Source: github_ishu86_after-effects-mcp.md
- ⚠️ Takraav/sambandh: Maciejdziuba ke perpetual-drift mana karne (D1-069) se halka tanav hai — ye sirf END frame par halka push-in hai, poore scene ka drift nahi

---

## Chhodi gayi tool-operation content (gintee)

**Ek line me ginti:** 19 source files me se 3 files lagbhag poori ki poori tool-operation/how-to nikli aur unse 0 rules bane (github_aedev-tools_adobe-agent-skills.md — 5,506 lines ExtendScript/DOM reference; notes_dvschultz_adobe-hut.md — UXP/plugin-dev reference; github_tryskilly_skilly.md — beginner curriculum); baaki 16 files me bhi kul milakar anumanan aadhe se zyada content (lagbhag 55–65%) tool-operation/reference/code/process tha jo chhod diya gaya.

- github_ishu86_after-effects-mcp.md: MCP tool schemas, prompt templates aur TypeScript preset CODE (bounce/wiggle/glitch/particle) — sirf timing bands, spring presets, parallax aur push-in ke numbers rule bane.
- github_chvndler_aeft.jsx.md: lagbhag 90% expression code — sirf bounce defaults (D1-062) aur expo-ease ki disha craft bani.
- github_Mfrostbutter_claude-skills.md: lagbhag 85% ExtendScript/matchName/JSON tables — craft kernels sirf sparkle timing, AV-sync aur SFX loudnorm.
- github_iart-ai_motion-design-skills.md: export codec tables ka bada hissa, performance checklist, file hygiene, MCP tool docs — craft sirf bounce params aur bitrate band.
- github_SebastianBoehler_autoresearch_after_effects_finetune.md: fal-ai/ES3 API patterns, job schema, render pipeline — tool-operation.
- github_LobzyJay_motion-design-with-claude.md: scripting patterns, operational canon, limits/render sections; effects-catalog ke look parameters Maciejdziuba ke shadow/glow rules (D1-056/D1-058) se dohraate the.
- github_justajazz_ae-mcp-bridge.md: MCP implementation aur aam reasoning frameworks — sirf animation craft kernels.
- github_ZeusSheen_ppro-agent-bridge.md: command reference, config gates, hook scripts, report formats — sirf defect thresholds aur rough-cut numbers.
- github_koptsev63_premiere-claude-bridge.md: pipeline checkpoints (ingest/manifest/naming) process hai; Murch varnan duplicate nahi kiya.
- notes_ADAM-0S_wayland-m3ta-0s.md (note): proxy workflow aur render-queue settings — workflow/tool.
- notes_mmmnhat_agent-skills.md (note): quarter-frame seek takneek, harness ki khaamiyon ki fehrist, teaser shots <1.5 s ki kamzor observation — rule nahi bani.
- github_MuhammadAsad809_AI-EDITING-SKILL.md: file/path sanction lists jaise pipeline hisse — sirf teen workflow-discipline rules.
- github_vamshicreates_premiere-editing-dna.md: Auto-Cut ke commands/pipeline steps — sirf DNA numbers.
- github_dylantarre_animation-principles.md: principles ke saath ke expression code snippets — sirf frame counts aur usool.
