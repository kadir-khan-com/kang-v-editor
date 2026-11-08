# Rules Part D2 — DaVinci Resolve + CapCut sources se naye rules

Step 2 ka cluster D2: editor-specific round (DaVinci Resolve + CapCut) ke sources se bane rules.
Purane 261 rules ke saath merge parent karega; jahan number purane defaults se takrate hain, woh `conflict_note` me saaf likha hai.

**Kul rules: 106**

Layer hisaab: kahani 17 · samajh 19 · rhythm 28 · style 42

Evidence hisaab: 🟢 0 · 🟡 3 · 🟠 103

Check wale rules (machine-map sakne wale): 28 · Bina check (human flag): 78

Conflict_note wale rules: 11

## KAHANI (kahani / story)

### D2-001 — Chapter ka 5-beat spine

- **Kab:** Har chapter (travel/long-form) ki planning aur review par
- **Kya:** Har chapter me paanchon beat hon: context, movement, lived-in texture, destination payoff, aftertaste/handoff. Jo beat gayab ho, use pehle footage se repair karo — effects ya BGM hit se kabhi nahi
- **Kyun:** Chapter sirf jagah ki list ban jata hai to viewer ko safar mehsoos nahi hota; movement aur texture hi kahani ko aage badhate hain
- **Kitni baar / haden:** Har chapter = 5/5 beats; missing beat = structure kaam, effect ka kaam nahi
- **Evidence:** 🟠 — Ek travel-studio skill ka house structure contract; koi measured corpus nahi
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-002 — Opening: 40s me vaada, 60s me saboot

- **Kab:** Video ke pehle minute me, khaas taur par travel/long-form opening me
- **Kya:** Pehle 40 second me asli destination/route footage par viewer promise rakho; pehle 60 second ke andar readable destination proof do (aerial, skyline, coast ya landmark)
- **Kyun:** Pehla minute hi decide karta hai ki viewer rukega ya jayega; vaada bina saboot ke clickbait lagta hai
- **Kitni baar / haden:** Promise ≤40s; destination proof ≤60s
- **Evidence:** 🟠 — House opening contract; koi platform data nahi
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "hook_within_s", "max_s": 60, "what": "destination proof"}`

### D2-003 — Pehle 3 minute: arrival aur texture, payoff se pehle

- **Kab:** Opening ke baad pehle chapter tak ke hisse me
- **Kya:** Minute 3 se pehle practical arrival dikhao (station, hotel, street) aur pehle chapter payoff se pehle lived-in texture rakho; pehla handoff movement/street/hotel/food/weather/signage bridge se ho, hard reset se nahi
- **Kyun:** Viewer ko pehle jagah par 'pahuncha' hua mehsoos hona chahiye, tabhi payoff ka matlab banta hai
- **Kitni baar / haden:** Arrival <3:00; texture hamesha pehle payoff se pehle
- **Evidence:** 🟠 — House opening contract
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-004 — Long-form ki ghadi: 20-minute wali shape

- **Kab:** Long-form travel film (target ~20 min) ki structure planning me
- **Kya:** Shape rakho: opening route promise 35–60s, 4–6 main chapters har ek 2.5–5 minute, transitions 15–45s, ending 45–75s callback/aftertaste ke saath. 1–2 minute ki short-video pacing long-form par default nahi
- **Kyun:** Lambi film ko saans aur route chahiye; short pacing se 20 minute ki film thaka deti hai
- **Kitni baar / haden:** Opening 35–60s; chapter 2.5–5 min; transition 15–45s; ending 45–75s
- **Evidence:** 🟠 — Ek reference-style (Bilibili long-form travel) se liya house target; measured nahi
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-005 — Har chapter ko barabar time nahi

- **Kab:** Chapter durations tay karte waqt
- **Kya:** Jis chapter ke paas strong footage, rich human moments, saaf local texture ya zyada route-matlab hai, use zyada time do; kamzor chapter sirf bridge ki bhumika me chhota rahe
- **Kyun:** Barabar time dene se film calendar jaisi lagti hai, kahani jaisi nahi
- **Kitni baar / haden:** koi fixed ratio nahi; strong chapter > bridge chapter hamesha
- **Evidence:** 🟠 — House structure niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-006 — Payoff-se-payoff jump = slideshow

- **Kab:** Chapter boundaries aur bade jagah-badal par
- **Kya:** Ek payoff shot ke seedha dusre payoff shot par mat jao — beech me movement/texture support rakho. Aftertaste hamesha chapter ke AAKHIR me rakho, shuru me nahi
- **Kyun:** Sirf 'best shots' jodne se tourist slideshow banta hai; beech ka safar hi film hai
- **Kitni baar / haden:** Har chapter boundary par ≥1 movement/texture support shot
- **Evidence:** 🟠 — House scene-flow contract
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-007 — Route task-chain hamesha samajh aaye

- **Kab:** Departure/arrival jaise practical chapters (hotel→airport→flight) me
- **Kya:** Chain ko padhne layak rakho: leave → handoff → travel → arrive → process → threshold → new state. Viewer ko har pal current jagah, current action aur agli manzil pata ho. Action continuity (haath, samaan, darwaze, signs, chalne ki disha) effect continuity se zyada mazboot join hai
- **Kyun:** Practical safar ki kahani kaam ke steps se banti hai; ek step gayab ho to viewer kho jata hai
- **Kitni baar / haden:** Har phase ke paas ≥1 pehchan wala anchor shot
- **Evidence:** 🟠 — Ek 6:13 homeward film ki poori review se nikali grammar (non-copying profile)
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-008 — Ending nayi state par, 3–6s thehrao ke saath

- **Kab:** Video/chapter ke aakhiri shot par
- **Kya:** Ending wahan rakho jahan traveller kisi nayi state me pahunch jaye (seat, window, arrival); uske baad suitable footage ho to 3–6 second stable aftertaste hold rakho. Chalte hue movement ke beech abrupt cut se khatam mat karo
- **Kyun:** Badli hui halat par rukna hi band hone ka ehsaas deta hai
- **Kitni baar / haden:** Final hold 3–6s (footage ho to)
- **Evidence:** 🟠 — Usi homeward review se; house niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "duration_range_s", "min_s": 3, "max_s": 6, "what": "ending aftertaste hold"}`

### D2-009 — Story plan cutting se pehle; beech-idea cut kabhi nahi

- **Kab:** Koi bhi talking-head/social edit shuru karne se pehle
- **Kya:** Pehle story plan likho: hook/agenda → body beats → recap/CTA ('jo bologe wo batao, batao, phir bataya hua dohrao'). Duration ghataane ke liye idea ko beech se kabhi mat kaato; word-boundary edits ki jagah lambe coherent blocks ko tarjeeh do
- **Kyun:** Plan bina kaatne se achhe hisse kat jate hain aur baat adhoori reh jati hai
- **Kitni baar / haden:** Har video = 1 story plan pehle; mid-idea cut = 0
- **Evidence:** 🟠 — Editor ke production standard se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-010 — Narration sparse rakho, khamoshi ko kaam karne do

- **Kab:** Long-form travel narration likhte waqt
- **Kya:** Spoken paragraphs sparse rakho; 20-minute film me voiceover kul chand minute hi ho sakta hai. 20–60 second ke hisse aise chhodo jahan sirf source audio, BGM aur visuals film ko aage le jayein. Jo dikh raha hai use bolkar mat samjhao
- **Kyun:** Har cheez bol dene se film lecture ban jati hai; nazara khud bhi bolta hai
- **Kitni baar / haden:** Quiet stretches 20–60s; narration kabhi wall-to-wall nahi
- **Evidence:** 🟠 — House narration style
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-011 — Reference se seekho, copy nahi; route par imaandari

- **Kab:** Kisi reference film ko style guide banate waqt
- **Kya:** Reference se pacing, structure aur rhythm seekho — uske titles, narration lines, music ya footage copy kabhi nahi. Location pakka na ho to narration/plan me confidence bhasa rakho: confirmed / visually likely / route scaffold only / needs human review
- **Kyun:** Copy ki hui pehchan pakdi jati hai aur galat location film ki sachchai tod deta hai
- **Kitni baar / haden:** Copy = 0; har uncertain location par confidence label
- **Evidence:** 🟠 — House non-copying + route-honesty contract
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-012 — Footage selection selective rakho, local pehle

- **Kab:** Pehli assembly se pehle footage chunte waqt
- **Kya:** Clip sirf isliye timeline me nahi aata ki woh exist karta hai. Pehle local footage, stock baad me. Kisi clip ko final reject karne se pehle full-duration, in-motion review karo — filename/metadata sirf review ke hints hain, faisla nahi
- **Kyun:** Sab kuch daal dene se film bhari ho jati hai; aur bina dekhe reject karne se best moment haath se jata hai
- **Kitni baar / haden:** Har final reject = full in-motion review ke baad hi
- **Evidence:** 🟠 — House footage-select contract (temporal scan ka ~99.5% coverage bar usi skill ke acceptance criteria me hai)
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-013 — Kharaab-par-unique clip, saaf generic scenic se upar

- **Kab:** Do clips me se ek chunna pade to
- **Kya:** Technically imperfect lekin unique story/emotion wala clip saaf lekin generic scenic shot se upar rank karo
- **Kyun:** Viewer ko perfection nahi, pal yaad rehta hai
- **Kitni baar / haden:** Tie-break rule: story/emotion > technical saafai
- **Evidence:** 🟠 — House selection niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-014 — Shot tiers aur function ka badlav

- **Kab:** Creator cut / clip classification me
- **Kya:** Har clip ko tier do: Hero / Main / Texture-bridge / Utility / Reject. Ek hi function wale do adjacent clips ke beech alag function wala clip daalo
- **Kyun:** Ek hi kaam ke shots lagatar aane se film ek-ras (monotone) ho jati hai
- **Kitni baar / haden:** Adjacent same-function pair = 0 (beech me alag function)
- **Evidence:** 🟠 — House creator-cut contract
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-015 — B-roll = saboot, sajawat nahi

- **Kab:** Cutaway/B-roll lagate waqt
- **Kya:** Har B-roll ke saath uska claim/beat/problem note karo — woh kis baat ka saboot hai ya kis cut ko dhak raha hai. B-roll pehle dhoondo aur WATCH karo, phir action/story ke hisaab se kaato; filler ke liye kabhi nahi
- **Kyun:** Bina-kaam ka B-roll viewer ko turant 'stock' lagta hai aur bharosa todta hai
- **Kitni baar / haden:** Har cutaway = 1 documented purpose
- **Evidence:** 🟠 — Do alag editor sources ka ek hi niyam (production standard + vlog workflow note)
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md, notes_appariciojunior_video-editor-skills.md (note)

### D2-016 — Rough cut me editor-notes aur punchlines bachaao

- **Kab:** Rough cut me retakes/dead air saaf karte waqt
- **Kya:** Speaker ki khud ki 'notes-to-editor' wali baatein aur punchlines ko galti se mat kaato — ye hamesha protect list me rakho
- **Kyun:** Ye woh hisse hain jo creator ne jaan-bujh kar rakhe hain; kaatna = kahani ka nuksaan
- **Kitni baar / haden:** Protect list = har rough cut se pehle tay
- **Evidence:** 🟠 — Note source: editor workflow apne shabdon me
- **Sources:** notes_appariciojunior_video-editor-skills.md (note)

### D2-017 — Screencast: shuru 15–30s 'kya aur kyun', aakhir me uplabdhi

- **Kab:** Screen-recording/tutorial videos me
- **Kya:** Pehle 15–30 second me batao kya bana rahe hain aur kyun. Aakhir me accomplishment/diff summary do — video beech safar me khatam mat karo
- **Kyun:** Viewer ko manzil pehle pata ho to beech ke steps sehne layak ho jate hain
- **Kitni baar / haden:** Opening context 15–30s; closing summary hamesha
- **Evidence:** 🟠 — Ek screencast editor ki house style
- **Sources:** github_matthull_my-skills.md
- **Check:** `{"kind": "duration_range_s", "min_s": 15, "max_s": 30, "what": "screencast opening context"}`

## SAMAJH (samajh aana / clarity)

### D2-018 — Captions sirf darshak ke liye

- **Kab:** Final SRT/TXT narration lines likhte waqt
- **Kya:** Har caption line audience ke liye ho: travel narration, route context, emotion ya visual observation. Workflow state wali baatein captions me KABHI nahi — 'QA pass', 'V14', 'Resolve', 'SRT', 'ye fix ho gaya' jaisi editor-bhasha block hai
- **Kyun:** Ek bhi andar-ki-baat wala caption poori film ko machine-bani hui ghoshit kar deta hai
- **Kitni baar / haden:** Editor-facing caption = 0
- **Evidence:** 🟠 — House caption contract
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-019 — Title zones me subtitles band

- **Kab:** Opening/chapter/ending title windows me
- **Kya:** Title chal raha ho to us window me rendered subtitle overlay suppress ya trim karo, jab tak user khaas taur par captions-over-title na maange. Scenic/title windows BGM-led rakho
- **Kyun:** Title aur caption ek saath ladte hain — dono padhne mushkil ho jate hain
- **Kitni baar / haden:** Title-zone subtitle overlap = 0
- **Evidence:** 🟠 — House subtitle-overlay contract
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-020 — Bina-voiceover film me captions hi kahani

- **Kab:** Jab voiceover na ho aur TXT/SRT hi narrative layer ho
- **Kya:** Captions itne dense rakho ki route, emotion aur visual imaandari carry kar sakein — planning target kam se kam 4 cues/minute rakho (slow reference profile justify kare to hi kam)
- **Kyun:** Awaaz na ho to kam captions wala hissa khaali aur khoya hua lagta hai
- **Kitni baar / haden:** ≥4 cues/minute planning target
- **Evidence:** 🟠 — House caption-density target
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "min_per_min", "min": 4, "what": "caption cues (no-VO film)"}`

### D2-021 — Caption highlight: line me sirf 1–3 shabd

- **Kab:** Word-highlight/karaoke style captions banate waqt
- **Kya:** Har caption line me sirf 1–3 important shabd highlight karo. Hierarchy: action verbs > numbers > emotional words. Filler/modifier shabd ('this', 'my', 'completely') kabhi highlight nahi
- **Kyun:** Sab kuch highlight = kuch bhi highlight nahi; aankh ko ek hi jagah rukna chahiye
- **Kitni baar / haden:** 1–3 highlighted words per line
- **Evidence:** 🟠 — CapCut director brain ki caption intelligence
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "count_range", "min": 1, "max": 3, "what": "highlighted words per caption line"}`

### D2-022 — Captions: pehle proofread, aakhir me finishing pass

- **Kab:** Caption workflow ke dono sire par
- **Kya:** Captions ko import karne se PEHLE saaf aur proofread karo (single-line default). Caption-only finishing pass sirf approved cut par chalao — word-level timing check karo aur sirf high-confidence domain terms fix karo
- **Kyun:** Gande captions import karke theek karna doguna kaam hai; aur cut badalne ke baad caption pass bekaar ho jata hai
- **Kitni baar / haden:** Proofread = import se pehle; finishing pass = sirf approved cut par
- **Evidence:** 🟠 — Do sources: vlog workflow note + Resolve production standard
- **Sources:** notes_appariciojunior_video-editor-skills.md (note), github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-023 — Burned-in captions dikhne wala layer ho

- **Kab:** Caption delivery check par
- **Kya:** Sirf SRT file deliverable nahi hai — burned-in captions timeline me ek visible layer ke roop me hone chahiye aur final render me dikhne ka saboot ho
- **Kyun:** File hai lekin render me caption nahi — ye sabse chhupa hua delivery fail hai
- **Kitni baar / haden:** Har delivery = rendered caption ka visual saboot
- **Evidence:** 🟠 — Production standard ki QA shart
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-024 — Vertical: aankhein upar-wale third me, captions surakshit jagah

- **Kab:** Vertical (9:16) framing aur caption placement me
- **Kya:** Speaker ki aankhein frame ke upper third ke aas-paas rakho. Captions ko chehra/munh aur platform UI ke danger zones se bahar rakho; key lines proofread karo
- **Kyun:** UI ke neeche daba caption = na padha gaya caption
- **Kitni baar / haden:** Caption kabhi face/mouth/UI-safe-zone ke bahar nahi
- **Evidence:** 🟠 — Do sources: Resolve social editor + CapCut mobile workflow
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md, github_pockebot_openpocket.md

### D2-025 — Bolne wala dikhe; B-roll emotion ko na dhake

- **Kab:** Talking-head par B-roll lagate waqt
- **Kya:** Spoken sections ke dauran speaker visible rakho. Crucial face/emotion beats par B-roll mat lagao — cutaway phrase land hone ke baad, saans par ya naye idea par rakho
- **Kyun:** Jazbaat chehre par hote hain; galat jagah cutaway usi pal ko chura leta hai
- **Kitni baar / haden:** Emotion beats par B-roll = 0
- **Evidence:** 🟠 — Production standard se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-026 — Screencast samajh: intent bolo, action nahi

- **Kab:** Screen-recording narration aur annotations me
- **Kya:** Har interaction se pehle context do; fast-forward hisse me khaas taur par narration rakho. Jo prompt text screen par poora na dikhe, use caption karo. Annotations phase ka label dein. Narration 'main ye click kar raha hoon' ki jagah intent bataye
- **Kyun:** Bina intent ke screen sirf harkat hai; viewer ko 'kyun' chahiye
- **Kitni baar / haden:** Har interaction = pehle intent line
- **Evidence:** 🟠 — Screencast editor ki house style
- **Sources:** github_matthull_my-skills.md

### D2-027 — Narration ka har daava saboot se bandha ho

- **Kab:** Narration/caption lines likhte waqt
- **Kya:** Har claim actual route evidence ya user-confirmed context se bandha ho. Jo cheez screen par khud dikh rahi hai use bolkar repeat mat karo
- **Kyun:** Bina saboot ke daave aur dikhi cheez ki commentary — dono bharosa ghataate hain
- **Kitni baar / haden:** Unverified claim = 0
- **Evidence:** 🟠 — House narration niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-028 — Title/lower-third: timing aur font ki discipline

- **Kab:** Animated titles aur lower-thirds banate waqt
- **Kya:** Lower-third slide-in ~12 frames rakho (~0.5s @24fps); typewriter follower delay 2 frames per character. Font medium-to-bold sans rakho (Open Sans Extrabold jaisa default). Timing perfect hone ke baad hi use macro/template me save karo. Animated title ke liye Text+ istemaal karo, basic Text nahi
- **Kyun:** Dheere-dheere ghusne wala lower-third purana lagta hai; halka font mobile par ghul jata hai
- **Kitni baar / haden:** Slide-in 12 frames; follower delay 2 frames/char
- **Evidence:** 🟠 — Resolve titles workflow se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-029 — Marker discipline: EDL se, rang-tiers ke saath

- **Kab:** Resolve me review markers lagate waqt
- **Kya:** Markers EDL ke through lagao (Resolve FCP7 XML ke clip colours ignore karta hai). Colour tiers fixed rakho: A = Red, flash frames = Fuchsia, B = Yellow, C = Blue, notes/re-record = Green
- **Kyun:** Marker ka rang hi team ki bhasha hai; rang badla to matlab badla
- **Kitni baar / haden:** 5 tiers, hamesha yahi mapping
- **Evidence:** 🟠 — Note source: dusre editor ke workflow apne shabdon me
- **Sources:** notes_SamuelAde001_second-brain.md (note)

### D2-030 — Pehle mapo (measure), phir raay do

- **Kab:** Kisi bhi editorial faisle se pehle
- **Kya:** Pacing/audio/structure par pehle scripts se numbers nikalo, editorial opinion uske baad do
- **Kyun:** Bina map ke raाय andaz hai; numbers behes khatam karte hain
- **Kitni baar / haden:** Har bada faisla = pehle ek measured report
- **Evidence:** 🟠 — Note source
- **Sources:** notes_SamuelAde001_second-brain.md (note)

### D2-031 — HOW aur WHAT alag rakho: preset pehle padho

- **Kab:** Koi bhi edit lane chalane se pehle
- **Kya:** Pehle WHAT padho — preset: look, numbers, done ki definition. Phir HOW chalao — lane ke steps. Dono ko mix mat karo
- **Kyun:** Bina 'done kya hai' jaane steps chalana = ghumte rehna
- **Kitni baar / haden:** Har kaam = pehle preset read, phir execution
- **Evidence:** 🟠 — Note source
- **Sources:** notes_edwinponcious12_video.md (note)

### D2-032 — Do-stage soch: pehle creative, phir tool

- **Kab:** AI/editor se edit plan banwate waqt
- **Kya:** Stage 1 me tool/catalog ka zikr kiye bina pure creative analysis karo (pacing, emotion, energy, weak spots). Stage 2 me hi suggestions ko asal tool/asset names se ground karo
- **Kyun:** Catalog pehle dikha do to soch catalog ke andar hi band ho jati hai; aur bina grounding ke plan chalaya nahi ja sakta
- **Kitni baar / haden:** Har plan = 2 stages, isi kram me
- **Evidence:** 🟠 — CapCut director ka core design niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-033 — Har edit ka 'kyun' aur weak spots saaf likho

- **Kab:** Edit plan/review dete waqt
- **Kya:** Har action ke saath uski wajah likho. Dead air, pacing drops jaise weak spots chhupao mat — explicitly flag karo. Subjective choices par 2–3 alternatives do taaki editor control me rahe
- **Kyun:** 'Kyun' bina ka plan order hai; kyun ke saath woh direction hai
- **Kitni baar / haden:** Actions bina why = 0; weak spots sab flag
- **Evidence:** 🟠 — CapCut director ke output niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-034 — Handoff ke liye layered timeline

- **Kab:** Timeline kisi insaan ko saumpte waqt
- **Kya:** Timeline layered rakho: disabled/backup tracks ka naam 'DISABLED' rakho, taaki agla editor bina puche samajh jaye ki kya live hai aur kya rakha hua hai
- **Kyun:** Gandi timeline dusre ke liye band kamra hai
- **Kitni baar / haden:** Har handoff = naam-daar layers
- **Evidence:** 🟠 — Production standard se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-035 — Pehli-pass ki taqseem: insaan = taste, agent = mazdoori

- **Kab:** AI agent ke saath edit ka kaam baant-te waqt
- **Kya:** Insaan taste aur film-sense ke faisle rakhe; agent transcribe/log/detect jaise labour kare. Agent raw footage kabhi modify nahi karta — woh sirf ADD karta hai
- **Kyun:** Taste machine ko dena aur mazdoori insaan karna — ulta batenwara kaam kharab karta hai
- **Kitni baar / haden:** Division = har project ki shuruaat me tay
- **Evidence:** 🟠 — Note source
- **Sources:** notes_appariciojunior_video-editor-skills.md (note)

### D2-036 — Creative azadi: template nahi, video ki energy

- **Kab:** Har naye video ki analysis par
- **Kya:** Har video ko independently analyze karo. Rigid genre rules ('funny hai to X karo') default mat banao. Video ki unique energy hai to usi par lean karo, safe defaults par nahi
- **Kyun:** Template-har-video ek jaisi film banata hai; energy har video ki alag hoti hai
- **Kitni baar / haden:** Genre-template default = 0
- **Evidence:** 🟠 — CapCut director ka creative-freedom rule
- **Sources:** github_tashisleepy_capcut-ai-director.md

## RHYTHM (lay / pacing)

### D2-037 — Travel shot-lengths: reference se calibrate

- **Kab:** Long-form travel pacing set karte waqt
- **Kya:** Ek poori tarah review ki hui homeward travel film ke measured numbers ko calibration anchor rakho: average shot ~10.4s, median ~10.1s, p10 ~3.1s, p90 ~17.9s. Apni film ke avg/median shot lengths in reference-calibrated ranges ke andar rakho
- **Kyun:** Long-form travel ki saans short-video se bilkul alag hai; bina anchor ke pacing ya to sust ya to bechain ho jati hai
- **Kitni baar / haden:** Anchor: avg ≈10.4s, median ≈10.1s, p90 ≈17.9s (ek film ka map)
- **Evidence:** 🟡 — Ek asli film ke 36 shots/35 boundaries ka poora human-reviewed map — measured, par sirf 1 film
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-038 — Pacing ki marammat footage se, effects se nahi

- **Kab:** Rhythm recut / pacing repair me
- **Kya:** Do galtiyan block karo: recut ke baad bache lambe non-scenic raw holds, aur micro-clips ki accidental flicker runs. Dono ki marammat footage badal/chun kar karo — effect daal kar kabhi nahi
- **Kyun:** Effect pacing ki bimari ko dhakta hai, theek nahi karta; viewer ko dhokha mehsoos hota hai
- **Kitni baar / haden:** Long raw holds = 0; flicker runs = 0
- **Evidence:** 🟠 — House pacing-watchability contract
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-039 — Har bade chapter me kam se kam ek saans-wala shot

- **Kab:** Chapter rhythm review par
- **Kya:** Har substantial chapter me kam se kam ek breathing/payoff/aftertaste shot rakho
- **Kyun:** Bina saans ke chapter ghutan hai; ek thehra shot poore chapter ko wazan deta hai
- **Kitni baar / haden:** ≥1 breathing shot per substantial chapter
- **Evidence:** 🟠 — House pacing contract
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "count_range", "min": 1, "what": "breathing/payoff shot per chapter"}`

### D2-040 — Visual rhythm ka pattern: establish → detail → reaction → widen

- **Kab:** Long-form ke andar shot sequence banate waqt
- **Kya:** Pattern dohrao: jagah ko establish karo (aerial/skyline/map/title) → street-level detail me ghuso → human reaction/food/transit/weather/waiting dikhao → jaane se pehle phir widen karo → geography, awaaz ya motion se transition karo
- **Kyun:** Ye upar-neeche ki lehar hi documentary-vlog rhythm hai; sirf beauty shots se film so jati hai
- **Kitni baar / haden:** Har place-block = kam se kam ek poora pattern cycle
- **Evidence:** 🟠 — House visual-rhythm style
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-041 — Visual change gap 3s se zyada (short-form) = pattern interrupt

- **Kab:** Short-form/social edit me jahan 3 second se zyada koi visual change nahi
- **Kya:** Pattern interrupt lagao — bareek se mote kram me: zoom (105–110%) → cut → caption overlay → motion (pan/shake) → effect overlay. Sabse halka kaam kare wahi chuno
- **Kyun:** 3 second bina badlav ke short-form me dhyaan marr jata hai
- **Kitni baar / haden:** Max visual gap 3s (short-form profile)
- **Evidence:** 🟠 — CapCut director ke attention niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "max_visual_gap_s", "value": 3, "scope": "short-form"}`
- **⚠️ Takraav:** TAKRAAV: purane ORDER default me long-form max visual gap 5s hai (Shorts 3s). Ye 3s wala niyam short-form/social ke liye hai — long-form par 5s wala hi rahe; profile se lagu karo, dono ko ek mat samjho.

### D2-042 — Platform ke hisaab se pacing table

- **Kab:** Platform tay hote hi edit shuru karne se pehle
- **Kya:** Pacing platform se lo: TikTok/Reels/Shorts — change har 1–3s, hook 1s me; YouTube short-form — change 2–3s, hook 3s; YouTube long-form — change 3–5s; LinkedIn — change 4–6s, saaf aur minimal
- **Kyun:** Ek hi pacing har platform par ya to sust hai ya bechain
- **Kitni baar / haden:** Table upar wali; hook: TikTok 1s / YT-SF 3s
- **Evidence:** 🟠 — CapCut director ke platform-optimization niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-043 — Hook me dead air = retention ki maut

- **Kab:** Video ki shuruaat (khaas taur par hook section ~pehle 4s) me
- **Kya:** Shuru ki silence/dead air kaato — hook action ya baat se shuru ho, khaamoshi se nahi
- **Kyun:** Pehle 2 second ki dead air sabse zyada viewers girati hai
- **Kitni baar / haden:** Initial dead air = 0; hook window ~4s
- **Evidence:** 🟠 — CapCut director ke hook niyam; purane Shorts hook ≤2.5s niyam se milta-julta
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "hook_within_s", "max_s": 2, "what": "shuru ki dead air"}`

### D2-044 — Pause ke niyam (talking head): 0.5s / 1.0s / dramatic chhoot

- **Kab:** Talking-head edit me pauses dekhte waqt
- **Kya:** Pause >0.5s ho to jump cut ka sujhav do; pause >1.0s ho to weak spot flag karo. Lekin 0.3–0.5s ke brief pauses dramatic maksad ke liye reh sakte hain
- **Kyun:** Har pause kaat dene se boli robot jaisi ho jati hai; lambe pause rakhe to viewer bore hota hai
- **Kitni baar / haden:** >0.5s = cut sujhav; >1.0s = flag; 0.3–0.5s dramatic = rakho
- **Evidence:** 🟠 — CapCut director ke silence-detection niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **⚠️ Takraav:** TAKRAAV: purana unified pause model ≥400ms ko cut zone, 150–400ms ko usable aur <150ms ko unsafe kehta hai. Ye source 500ms threshold rakhta hai aur 300–500ms dramatic pause ko surakshit maanta hai. Merge par faisla: threshold 400ms vs 500ms — profile (talking-head social = 0.5s wala; Kang pipeline = purana model) se tay karna bacha hai.

### D2-045 — Smart-cut: >1s silence aur duplicate takes pehle pass me bahar

- **Kab:** Auto/smart-cut pehla pass chalate waqt
- **Kya:** Subtitle gaps >1s wali silences aur duplicate takes auto-remove karo. Chalane se PEHLE project ka duplicate/backup zaroor banao (auto-backup nahi hota)
- **Kyun:** Pehla pass haath se karna sabse dheema kaam hai; machine ko wahi do jo bina taste ke ho sakta hai
- **Kitni baar / haden:** Threshold: silence gap >1s; duplicates = sab bahar
- **Evidence:** 🟠 — CapCut smart-cut + note source ke retake-removal workflow ka sangam
- **Sources:** github_tashisleepy_capcut-ai-director.md, notes_AdamGarceau_resolve-toolkit.md (note)
- **⚠️ Takraav:** TAKRAAV: purana pause model ≥400ms ko hi cut zone kehta hai — >1s wala threshold usse zyada conservative hai. Ye sirf AUTO pehle pass ke liye hai (haath ka fine pass purane model par hi rahe), isliye takraav pass-wise sulajh sakta hai.

### D2-046 — Cut sirf silence ya word-boundary par; mid-sentence kabhi nahi

- **Kab:** Tighten/cut pass me har cut lagate waqt
- **Kya:** Cut hamesha silence ke andar ya word boundary par rakho — sentence ke beech me kabhi nahi. Shorts aur longform ke liye alag tighten profiles rakho
- **Kyun:** Beech-vaakya cut boli ko kaatta hai aur viewer ko jhatka lagta hai
- **Kitni baar / haden:** Mid-sentence cuts = 0
- **Evidence:** 🟠 — Note source (dr-tighten) + production standard ke coherent-block niyam
- **Sources:** notes_AdamGarceau_resolve-toolkit.md (note), github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-047 — Do-phase discipline: CUT pass → re-cut → TRANSCRIPT pass

- **Kab:** Poore edit ka kram tay karte waqt
- **Kya:** Pehle CUT pass (picture lock ki taraf), phir editor ka re-cut, uske BAAD transcript pass. Purani subtitles ke upar transcript pass chalana bekaar hai — transcript hamesha final cut ke baad bane
- **Kyun:** Galat kram = do baar kaam; transcript pehle banaya to har cut use tod dega
- **Kitni baar / haden:** Kram fixed: cut → re-cut → transcript
- **Evidence:** 🟠 — Note source
- **Sources:** notes_SamuelAde001_second-brain.md (note)

### D2-048 — Phase-1 ki shikar-list

- **Kab:** Pehle (hunt) pass me footage dekhte waqt
- **Kya:** Sirf ye cheezen dhoondo aur mark karo: duplicate takes, misspeaks, garbled audio, flash frames, redundancy, aur script ke missing sections
- **Kyun:** Pehla pass sab kuch ek saath theek karne nikle to kuch theek nahi hota
- **Kitni baar / haden:** 6 item ki list; is se bahar ka kaam phase-2 ka
- **Evidence:** 🟠 — Note source
- **Sources:** notes_SamuelAde001_second-brain.md (note)

### D2-049 — Screen-recording cut workflow: transcript pehle, rough 2x, 1.5x par galti-pass

- **Kab:** Screen-recording/talking video ka rough cut banate waqt
- **Kya:** Transcript-first kaato: AI transcription + silent-portion removal ~80% kaam kar deta hai. Rough cut ka target final length ka ~2x rakho (8 min final → ~16 min rough). Refine pass me snapping OFF, audio scrubbing ON, 5-frame nudges. Aakhiri mistake pass 1.5x playback par ripple-delete ke saath chalao (aur 1–3 minute nikalta hai). Verify: koi audible cut edit na sune, saare ums/pauses gaye hon
- **Kyun:** Dekh-dekh kar kaatna sabse dheema hai; transcript se kaatna tez aur pakka hai
- **Kitni baar / haden:** Rough ≈ 2x final; mistake pass 1.5x playback
- **Evidence:** 🟠 — Resolve screen-recording workflow se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-050 — Silence detection ki shart: room noise pehle theek karo

- **Kab:** Auto silence removal chalane se pehle
- **Kya:** Room noise −30 dB se upar ho to silence detection toot jata hai — pehle noise reduction karo ya haath se kaato
- **Kyun:** Shor ko tool khaamoshi samajh nahi pata; galat detection = galat cuts
- **Kitni baar / haden:** Room noise >−30 dB = pehle NR/manual
- **Evidence:** 🟠 — Workflow ki vyavharik shart
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-051 — Screencast speed map: sust hissa delete nahi, tez karo

- **Kab:** Screencast ke boring hisse handle karte waqt
- **Kya:** Boring hisse ko delete karne ki jagah speed up karo taaki poora workflow dikhta rahe. Normal speed = prompts, output review, test results, key decisions. 4x–8x = generation, lambe reads, scrolling. Poora cut = false starts, re-prompts, apni typos. Speed% = (original duration / target audio duration) x 100
- **Kyun:** Delete karne se viewer ko 'beech me kya hua' ka shaq rehta hai; tez karne se poora safar dikhta hai
- **Kitni baar / haden:** 4x–8x sust hisso par; key moments hamesha 1x
- **Evidence:** 🟠 — Screencast editor ki house style
- **Sources:** github_matthull_my-skills.md

### D2-052 — Talking speed 1.1x (samajh bani rahe to)

- **Kab:** Speaker-led short-form me
- **Kya:** Speaker ki speed 1.1x rakho — sirf tab jab intelligibility poori bani rahe
- **Kyun:** Halki tez boli energy deti hai bina nakli lage
- **Kitni baar / haden:** 1.1x; samajh ghate to wapas 1.0x
- **Evidence:** 🟠 — Production standard se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-053 — A-roll reset: 6–9s se zyada bina reset ke nahi (talking-head social)

- **Kab:** Talking-head social edit (Deya-style retention) me
- **Kya:** 6–9 second se zyada uninterrupted A-roll mat chalne do — beech me visual reset do (B-roll, punch-in, angle ya title)
- **Kyun:** Ek hi frame par thahri boli dhyaan ko sust kar deti hai
- **Kitni baar / haden:** A-roll bina reset ≤6–9s
- **Evidence:** 🟠 — Ek retention creator (Deya) ki style ko production standard ne apnaya
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **⚠️ Takraav:** TAKRAAV (halka): purana max visual gap default 5s hai. Ye 6–9s wala window sirf 'A-roll reset' ki had hai (speaker frame par lagatar rehne ki), aam visual-change gap se alag mapna — dono ek saath chal sakte hain: visual change 5s ke andar, A-roll reset 9s ke andar.

### D2-054 — BPM ke hisaab se cut frequency

- **Kab:** Music-led edit me cut rhythm tay karte waqt
- **Kya:** Cut frequency BPM se lo: 60 BPM → har 4 beats (~4s, ~8 cuts/30s, cinematic); 100 BPM → har 2 beats (~17 cuts/30s); 120 BPM → har 1–2 beats (20–30 cuts/30s); 140 BPM → har beat (~35 cuts/30s). Ambient/bina-BPM music par beat-cut bilkul nahi — cuts visual narrative se motivate hon, 5–15s ke holds aam hain
- **Kyun:** Music ki gati aur cut ki gati alag chale to video do hisso me tootta lagta hai
- **Kitni baar / haden:** Upar wali table; formula: beat frames = 1800/BPM @30fps
- **Evidence:** 🟠 — CapCut KF-07 ka BPM-to-cut map (house table, measured nahi)
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-055 — Cuts beat par; 2–3 frame aage-peeche ka khel

- **Kab:** Beat-synced cuts lagate waqt
- **Kya:** Default: cut theek beat par (kick/snare). Aage ki kheench (anticipation) chahiye to cut beat se 2–3 frames PEHLE; wazan chahiye to 2–3 frames BAAD. Off-beat cuts sirf syncopated/groovy feel ke liye jaan-bujh kar
- **Kyun:** Beat par cut 'lock' mehsoos hota hai; jaan-bujh kar off-beat usi lock ko tod kar jaan deta hai — galti se off-beat sirf galti lagta hai
- **Kitni baar / haden:** Offset sirf ±2–3 frames, jaan-bujh kar
- **Evidence:** 🟠 — KF-07 beat-sync guide
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-056 — Bade phase-change cuts BGM phrase par; har beat par nahi

- **Kab:** Route/phase badlav ke cuts par (travel film)
- **Kya:** Ahem route-phase badlav phrase boundary ya saaf BGM hit par kaato. Har beat par cut mat karo — beat grid sirf bade palon ke liye hai
- **Kyun:** Har beat kaatne se film gana ban jati hai, safar nahi
- **Kitni baar / haden:** Phrase-level cuts sirf bade badlav par
- **Evidence:** 🟠 — Homeward profile + BGM phrase system
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-057 — Build-up → drop: edit ka accelerator

- **Kab:** Music me build-up/riser aur drop wale hisse me
- **Kya:** Pre-drop/riser par cut frequency tez karo, visual density har 2 beats badhao, speed ramps se time sikodo. Drop par sabse sakht cuts, hero shot/reveal rakho. Breakdown par dheere ho jao — lambe holds, viewer ko saans
- **Kyun:** Sangeet jo chadhaw-utaw deta hai, edit use follow na kare to drop fizool jata hai
- **Kitni baar / haden:** Har drop = 1 hero pal; breakdown = jaan-bujh kar dheema
- **Evidence:** 🟠 — KF-07 ki song-structure map
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-058 — Music entry chorus/drop se; climax drop par sync

- **Kab:** Video ke liye music ka hissa chunte waqt
- **Kya:** Cold open/hook par music chorus ya drop se shuru karo — track ke intro se kabhi nahi. Value-delivery hisse me instrumental/low-vocal section rakho taaki narration saans le. Climax/reveal ko drop ya chorus peak se sync karo
- **Kyun:** Track ka intro sabse sust hissa hota hai; hook wahan rakha = video shuru hote hi marr gaya
- **Kitni baar / haden:** Frame 1 = chorus/drop; climax = drop peak par
- **Evidence:** 🟠 — KF-07 music entry points
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-059 — BGM variety: 35% unique, 6 cues me repeat nahi

- **Kab:** Lambe film ke BGM cues (≥20) plan karte waqt
- **Kya:** Unique songs kam se kam max(12, cue_count x 0.35) rakho; koi gaana pichhle 6 cues ke andar repeat nahi. Lambe hero passages ko calm → lift → climax wala arc do
- **Kyun:** Wahi dhun baar-baar sunai de to film chhoti aur sasti lagti hai
- **Kitni baar / haden:** Unique ≥ max(12, 35%); repeat window = 6 cues
- **Evidence:** 🟠 — Travel-studio ka BGM catalog niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "percent_range", "min_pct": 35, "what": "unique BGM songs (≥20 cues par)"}`

### D2-060 — Muted-audio desert 18s se zyada nahi; scenic BGM coverage poora

- **Kab:** Scenic/BGM-led windows ki audio planning me
- **Kya:** Bina awaaz ke hisse (muted desert) ~18s se zyada na rakho. Drone/pure-scenic windows me BGM coverage ratio ~0.995 rakho
- **Kyun:** Lambi khaamoshi scenic hisse ko 'rendering adhoori' jaisa bana deti hai
- **Kitni baar / haden:** Muted desert ≤~18s; scenic coverage ≈99.5%
- **Evidence:** 🟠 — House scenic audio policy
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-061 — Speed-ramp ko beat se baandho

- **Kab:** Speed ramps lagate waqt
- **Kya:** Riser ke dauran 30–50% slow-mo rakho aur drop wale frame par 100% par snap karo. Whip-pan ke liye 400% speed sirf 6 frames, beat ke theek center me
- **Kyun:** Ramp bina beat ke geli-geli lagti hai; beat par wahi ramp prahar (hit) ban jata hai
- **Kitni baar / haden:** Slow-mo 30–50% riser par; whip 400% x 6 frames
- **Evidence:** 🟠 — KF-07 ramp-sync table
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-062 — Vlog silence cuts me chhote pads (saans) rakho

- **Kab:** Vlog ke silence cuts par
- **Kya:** Silences kaato lekin cut edges par chhote pads chhodo taaki boli saans leti lage; scene edges par bhi thodi room rakho. Jump cut ko naram karne ke liye halka zoom punch-in kaam aata hai
- **Kyun:** Zero-pad cuts vlog ko machine-gun bana dete hain; saans hi asli-boli ka saboot hai
- **Kitni baar / haden:** Har silence cut = chhota pad; scene edge = halki room
- **Evidence:** 🟠 — Note source; purane remainder 0.2–0.45s model se bhavna milta hai, numbers yahan qualitative
- **Sources:** notes_appariciojunior_video-editor-skills.md (note)
- **⚠️ Takraav:** Purane unified pause model ka remainder 0.2–0.45s is niyam se takrata nahi — ye usi 'saans' ko vlog context me kehta hai, par exact ms nahi deta.

### D2-063 — CapCut edit ka kram: ratio → structure → timing → transitions → text

- **Kab:** CapCut mobile edit shuru karte waqt
- **Kya:** Pehle aspect ratio confirm karo. Structural edit (trim/split/delete) speed/timing se pehle. Transitions tab jab boundaries stable ho jayein. Text/stickers timing fix hone ke baad
- **Kyun:** Galat kram me har baad wala step pehle wale ko tod deta hai
- **Kitni baar / haden:** 5 steps, yahi kram
- **Evidence:** 🟠 — CapCut mobile workflow (openpocket) se
- **Sources:** github_pockebot_openpocket.md

### D2-064 — AutoCut tabhi kabul jab intent se mile

- **Kab:** Auto-generated cut ka result dekhte waqt
- **Kya:** AutoCut ka output sirf tab accept karo jab pacing/cuts tumhare intent se milte hon. Na mile to baar-baar regenerate karne ki jagah manual edit par switch karo
- **Kyun:** Baar-baar regeneration samay khaata hai aur result waisa ka waisa rehta hai
- **Kitni baar / haden:** Intent-match nahi = manual, dobara generate nahi
- **Evidence:** 🟠 — CapCut mobile workflow
- **Sources:** github_pockebot_openpocket.md

## STYLE (style / effect / audio / rang)

### D2-065 — Transition mix ka budget (travel/POV)

- **Kab:** Poore film ke transition mix ki yojna/review par
- **Kya:** Mix rakho: clean cut / action match / direction match / hidden cut = 55–70%; physical bridge ya short dissolve = 15–30%; motion accent = zyada se zyada 18%, kabhi do adjacent nahi, ek family ko dohrane se pehle kam se kam 5 stable boundaries
- **Kyun:** Ek hi effect ki 77% repetition (reference film ki asli kamzori) poore film ko template bana deti hai
- **Kitni baar / haden:** Motion accent ≤18%; adjacent = 0; family repeat gap ≥5 boundaries
- **Evidence:** 🟡 — Reference film ke map par 27/35 boundaries ek hi transition the — usi kamzori ke ulta banaya house budget; percentages house hain, kamzori measured hai
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "percent_range", "max_pct": 18, "what": "motion accent transitions ka hissa"}`

### D2-066 — Motion accent ki 4 shartein, warna downgrade

- **Kab:** Koi motion transition (whip/zoom/slice type) lagane se pehle
- **Kya:** Accent tabhi jab: dono taraf real movement ho, route-phase ki wajah ho, BGM hit saath ho, aur kam se kam 0.8s ki stable landing footage ho. Ek bhi shart kamzor ho to clean match cut ya dissolve par downgrade karo. Accent ko hero title, subtitle collision ya voice-leak ke upar kabhi mat rakho
- **Kyun:** Bina zameen ke accent girta hai — viewer ko effect nahi, jhatka dikhta hai
- **Kitni baar / haden:** 4/4 shartein; landing ≥0.8s stable
- **Evidence:** 🟠 — Homeward transition policy
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "duration_range_s", "min_s": 0.8, "what": "motion accent ke baad stable landing"}`

### D2-067 — Hard-reject transitions ki list

- **Kab:** Transition chunne ke har pal
- **Kya:** Ye kabhi nahi: bina story-purpose ke random spin, flash, glitch, shake ya template transition; route jump ko sirf title card se dhakna; do static shots ke beech whip. Spin/zoom/flash/slice ko do kamzor unrelated shots chhupane ke liye kabhi nahi
- **Kyun:** Chhupane wala effect sabse pehle pakda jata hai
- **Kitni baar / haden:** Reject list = 0 exceptions
- **Evidence:** 🟠 — Transition grammar ke hard rejections
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-068 — Pair grammar: har jodi ka apna transition

- **Kab:** Har adjacent clip-pair ke liye transition tay karte waqt
- **Kya:** Pair ke hisaab se chuno: action continuity = straight cut; shape/direction/water/road/window/skyline ka mel = match cut; time/weather/day-night/aftertaste = short dissolve; whip/rotation sirf jab dono taraf route-motion energy ho (rotation durlabh); speed-ramp sirf real movement par. Agar pair ke paas physical bridge evidence nahi hai to faisla 'pehle bridge insert karo' hai — effect-ready nahi
- **Kyun:** Har jodi ki fiziks alag hai; ek formula sab par lagana hi template-bazi hai
- **Kitni baar / haden:** Har pair = 1 grammar-based faisla + fallback
- **Evidence:** 🟠 — Transition grammar engine
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-069 — Cadence: sajawati runs 4 se kam, koi style raja nahi

- **Kab:** Poore film ki transition cadence dekhte waqt
- **Kya:** Decorative transitions ki lagatar runs 4 se kam rakho; koi ek transition style poore film par dominate na kare
- **Kyun:** Ek style ka raaj = dekhne wale ko pattern dikhne lagta hai, kahani nahi
- **Kitni baar / haden:** Decorative run <4; dominance = kisi ek style ka varchasva nahi
- **Evidence:** 🟠 — Transition cadence/motif niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "count_range", "max": 3, "what": "lagatar decorative transitions ki run"}`

### D2-070 — Effects ki haden (CapCut director)

- **Kab:** Kisi bhi social edit me effects lagate waqt
- **Kya:** Haden: transitions zyada se zyada 2 per 10s; video effects 2 per 5s; zooms 1 per 5s; caption changes 1 per 3s; screen par ek saath stickers zyada se zyada 2
- **Kyun:** Had bina ke effects ek dusre ko kha jate hain — asar sab ka, yaad koi nahi
- **Kitni baar / haden:** 2 transitions/10s; 2 effects/5s; 1 zoom/5s; 1 caption change/3s; ≤2 stickers
- **Evidence:** 🟠 — CapCut director ke maximum effect limits
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "max_per_min", "value": 12, "what": "transitions (2 per 10s)"}`

### D2-071 — Emphasis zoom: 105–110%, 6–15 frames, ease-out

- **Kab:** Speaker kisi baat par zor de to
- **Kya:** Zoom 105–110% tak rakho, duration 6–15 frames, easing ease-out. Zoom hamesha bolne wale ke stress point par lage
- **Kyun:** Chhota, tez-nikalne wala zoom aankh ko 'sunno!' kehta hai; bada dheema zoom natak ban jata hai
- **Kitni baar / haden:** 105–110%; 6–15 frames; ease-out
- **Evidence:** 🟠 — CapCut director ke zoom niyam (hook examples me 108–110% bhi aaya hai)
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "percent_range", "min_pct": 105, "max_pct": 110, "what": "emphasis zoom scale"}`

### D2-072 — Ek video, zyada se zyada 2 visual styles

- **Kab:** Style tay karte waqt aur poore edit ke dauran
- **Kya:** Ek video me 2 se zyada visual styles mix mat karo. Transition ek hi family se rakho. Filter/color grade poori film me consistent rakho
- **Kyun:** Har scene alag duniya lage to film bikhar jati hai
- **Kitni baar / haden:** ≤2 styles; 1 transition family; 1 grade
- **Evidence:** 🟠 — Style consistency niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "count_range", "max": 2, "what": "visual styles per video"}`

### D2-073 — Cuts > transitions; har cut ka rationale

- **Kab:** Har edit decision par
- **Kya:** Clean editing ko effects par tarjeeh do — cut invisible hota hai, transition dhyaan kheenchta hai. Har hard cut ke paas rationale ho: nayi beat, angle change, gesture, B-roll, title card ya stylistic hit. Har effect ko apni jagah kamani hogi
- **Kyun:** 'Bas aise hi' wala cut viewer ko turant mehsoos hota hai
- **Kitni baar / haden:** Rationale-less cuts/effects = 0
- **Evidence:** 🟠 — Do sources ka sangam: director philosophy + production standard
- **Sources:** github_tashisleepy_capcut-ai-director.md, github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-074 — Dikhne wala jump cut dhako; talking-head par video crossfade nahi

- **Kab:** Same camera + same crop ke dono taraf jump cut dikhe to
- **Kya:** Use B-roll, punch-in ya dissolve se dhako. Talking-head video par crossfade kabhi nahi (ghosting hota hai) — picture par hard cut, aur audio par crossfade / J-cut / L-cut ka naram-pan do
- **Kyun:** Ghosting sabse sasta lagta hai; awaaz ka naram-pan cut ko chhupa deta hai
- **Kitni baar / haden:** Video crossfade on talking head = 0
- **Evidence:** 🟠 — Production standard se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-075 — B-roll grammar: wide → medium → close-up; hold 1.2–3.0s

- **Kab:** B-roll sequence banate waqt
- **Kya:** Sequence grammar rakho: wide → medium → close-up. Har B-roll shot 1.2–3.0s hold karo (mobile par padhne layak). Cutaway complete semantic beat par rakho — phrase land hone ke baad, saans par, ya naye idea par
- **Kyun:** Chhota B-roll jhalak hai, bada B-roll rukawat; kram bina sequence random hai
- **Kitni baar / haden:** Hold 1.2–3.0s
- **Evidence:** 🟠 — Production standard se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "duration_range_s", "min_s": 1.2, "max_s": 3.0, "what": "B-roll hold"}`

### D2-076 — Punch-in graphics/captions se pehle

- **Kab:** Punch-in zoom aur graphics dono ek hi edit me hon to
- **Kya:** Punch-ins graphics/captions compositing se PEHLE lagao — warna text bhi zoom ke saath hilta hai
- **Kyun:** Kram ulta ho to saaf dikhne wala technical nishan reh jata hai
- **Kitni baar / haden:** Kram fixed: punch-in → graphics/captions
- **Evidence:** 🟠 — Production standard se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-077 — Title reveal shant rakho

- **Kab:** Title/place-card reveals par
- **Kya:** Reveal sirf: short fade, tiny scale settle, ya gentle dissolve. Glitch, random spin, flash, shake, particle, logo-reveal ya generic template-pack effects reject karo. Route transitions understated rakho — map line, ambient street insert, station/vehicle movement, ya colour/motion match cut
- **Kyun:** Shor machane wala title saste pack ki pehchan hai
- **Kitni baar / haden:** Allowed reveals = 3 qismein hi
- **Evidence:** 🟠 — Effect-motion plan ke niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-078 — Ending ka ilaaj: music-tail fade, thehra hua aakhir

- **Kab:** Video ke aakhiri seconds me
- **Kya:** Ending par music-tail fade aur scenic breathing room do; slow zoom-out + fade (~15 frames) se band karo. Abrupt end kabhi nahi
- **Kyun:** Achanak khatam hua video adhoora lagta hai, khatam hua nahi
- **Kitni baar / haden:** Outro fade ~15 frames; abrupt end = 0
- **Evidence:** 🟠 — Do sources: travel effect plan + CapCut director ending niyam
- **Sources:** github_junwen853_travel-video-studio-skill.md, github_tashisleepy_capcut-ai-director.md

### D2-079 — Ek hi hero title, asli footage par, 6–12s ke andar

- **Kab:** Opening title lagate waqt
- **Kya:** Sirf EK saaf hero title, high-recognition asli footage ke upar, pehle 6–12 second ke andar. Dusra title, date, route/debug text ya ghosted duplicate kabhi nahi. Title ko kam se kam 1.2s tak bina competing viewer-text ke rehne do
- **Kyun:** Do title = koi title nahi; khaali card par title = footage par bharosa nahi
- **Kitni baar / haden:** Titles = 1; window 6–12s; clean hold ≥1.2s
- **Evidence:** 🟠 — Opening + homeward title contracts
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "duration_range_s", "min_s": 1.2, "what": "hero title ka clean (bina competing text) hold"}`

### D2-080 — Cover/hero-title formula: 1–5 shabd, pehchan wali background

- **Kab:** Cover/hero title design karte waqt
- **Kya:** High-recognition scenic background + oversized destination title (1–5 shabd) + neeche chhota designed subtitle + high-contrast (yellow/orange/white) type. Route/date/project clutter kabhi nahi
- **Kyun:** Cover ka kaam ek nazar me jagah bechna hai, itinerary batana nahi
- **Kitni baar / haden:** Title 1–5 shabd
- **Evidence:** 🟠 — Ek reference channel (Parallel World) ke cover formula se
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "count_range", "min": 1, "max": 5, "what": "cover title ke shabd"}`
- **⚠️ Takraav:** TAKRAAV: purana thumbnail niyam target ≤3 shabd, hard cap 4 kehta hai. Ye source 1–5 shabd deta hai. Cover (video hero title) aur thumbnail ko alag maanna sulah ho sakti hai; merge par user/engine faisla kare.

### D2-081 — Dialogue chain ka kram: EQ → de-hum → gate → NR → level → duck

- **Kab:** Dialogue/podcast audio saaf karte waqt
- **Kya:** Chain is kram me chalao: EQ → de-hummer → gate → noise reduction → level → ducking. Frequency ki problems dynamics se pehle; noise reduction destructive hai isliye der se. Manual NR ka dry/wet default 80% rakho. Hot external mic (0 dBFS ke paas) ho to use source rakho aur processed duplicate conservative limiting ke saath banao
- **Kyun:** Galat kram me har step pichhle step ki galti ko bada karta hai
- **Kitni baar / haden:** 6 steps, yahi kram; NR dry/wet ≈80%
- **Evidence:** 🟠 — Resolve audio-cleanup (podcast) workflow
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-082 — Dialogue EQ/de-hum/gate ke starting numbers

- **Kab:** Dialogue cleanup ki shuruaat par
- **Kya:** Har dialogue clip par 80 Hz se neeche kaato (shelf jo 80–100 Hz tak −70 dB chhoo jaye). De-hummer 50/60 Hz par, amount −20 se −30 dB. Gate ke starting values: threshold −35 dB, range −18 dB, attack 1.4 ms, hold 0, release 93 ms — gate sirf sentences ke beech kaam kare
- **Kyun:** Neeche ka shor (rumble/hum) har dialogue ki saafai kha jata hai; ye numbers surakshit shuruaat hain
- **Kitni baar / haden:** HPF <80 Hz; de-hum −20..−30 dB; gate −35/−18 dB, 1.4 ms / 93 ms
- **Evidence:** 🟠 — Usi cleanup workflow ke diye starting values
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "db_range", "min_db": -30, "max_db": -20, "what": "de-hum amount"}`

### D2-083 — Ducker: shuruaat 2.7 dB, 5 dB se zyada = amateur

- **Kab:** Music ko voice ke neeche duck karte waqt (dialogue chain)
- **Kya:** Ducker 2.7 dB se shuru karo. 5 dB se zyada ducking amateurish lagti hai — audience ko dip sunai dene lagta hai
- **Kyun:** Ducking mehsoos nahi honi chahiye, sirf voice saaf honi chahiye
- **Kitni baar / haden:** Start 2.7 dB; hard had 5 dB
- **Evidence:** 🟠 — Podcast cleanup workflow
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "db_range", "max_db": 5, "what": "ducker depth (dialogue chain)"}`
- **⚠️ Takraav:** TAKRAAV: purana ORDER default 'music voice se 18–25 dB neeche' bed-LEVEL ki baat hai; ye 2.7 dB DUCKER ki depth hai (kitna ghatao) — donon alag map hain, takraav asal me map ka hai. Lekin isi cluster ka KF-07 duck −12 dB (D2 style rule 'Narration duck landmarks') is 2.7–5 dB se sach me takrata hai — context farq: ye podcast dialogue-chain ka ducker hai, woh CapCut music-bed duck hai. Merge par profile-wise chuna jaye.

### D2-084 — Podcast loudness verify: −16..−20 LUFS, peaks −9..−3 dBFS

- **Kab:** Podcast/dialogue delivery se pehle verify karte waqt
- **Kya:** Integrated loudness −16 se −20 LUFS ke beech rakho; voice peaks −9 se −3 dBFS; clip kabhi nahi
- **Kyun:** Podcast sunne wala lamba sunta hai — thakane wali loudness ya clipping turant chhod deta hai
- **Kitni baar / haden:** −16..−20 LUFS; peaks −9..−3 dBFS; clips = 0
- **Evidence:** 🟠 — Podcast verification checklist
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "lufs_target", "min_lufs": -20, "max_lufs": -16, "profile": "podcast dialogue"}`
- **⚠️ Takraav:** Note: purana podcast profile −16 LUFS deta hai. Ye range −16..−20 hai — dialogue-only podcast ke liye neeche tak ijazat deta hai. Takraav halka; profile me range likh kar sulajh sakta hai.

### D2-085 — Short-form dialogue: −14..−16 LUFS, true peak <−1 dBTP

- **Kab:** Talking-head short-form ke final mix par
- **Kya:** Dialogue target −14 se −16 LUFS integrated rakho; true peak −1 dBTP se neeche. Music hamesha ducked/conservative — fixed loud bed kabhi nahi; dialogue edits par 2–4 frame constant-power audio fades rakho
- **Kyun:** Platform normalization is range ko inaam deta hai; zyada loud = neeche daba diya jayega
- **Kitni baar / haden:** −14..−16 LUFS; TP <−1 dBTP
- **Evidence:** 🟠 — Social-editor ke audio targets (usi source ke QA gate me Reels −15..−13 LUFS bhi aaya hai — range overlap hai, platform profile se final ho)
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "lufs_target", "min_lufs": -16, "max_lufs": -14, "profile": "talking-head short-form"}`

### D2-086 — Narration duck landmarks: −12 dB, 10f/15f fades

- **Kab:** Narration ke aane-jaane par music automation me
- **Kya:** Narration shuru ho to music −12 dB tak duck karo (~10 frame fade me); narration khatam ho to 0 dB par wapas lao (~15 frame fade me). Documentary me music hamesha speech ke neeche −12 dB. End card par music 2s me −inf tak fade karo
- **Kyun:** Achanak ghata-badha music dhyaan khinchta hai; landmark fades use invisible karte hain
- **Kitni baar / haden:** Duck −12 dB; in-fade ~10f; out-fade ~15f; end fade 2s
- **Evidence:** 🟠 — KF-07 volume automation landmarks
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **⚠️ Takraav:** TAKRAAV: purana default bed music ko voice se 18–25 dB neeche rakhta hai; −12 dB usse kam gehra hai. Aur ChaiWithJai ke ducker (2.7 dB start, >5 dB amateur) se bhi takrata hai. Teeno alag contexts ke numbers hain (bed level / CapCut duck / podcast ducker) — merge par har profile ka ek number tay karna hoga.

### D2-087 — Music bed narration ke neeche: −24..−18 LUFS relative

- **Kab:** Travel film me voiceover ke neeche music bed rakhte waqt
- **Kya:** Music ko narration ke neeche lagbhag −24 se −18 LUFS relative bed par rakho; clipping kabhi nahi; chapter badlav ke aas-paas chhote fades do
- **Kyun:** Bed mehsoos ho, sune nahi — voice hamesha aage
- **Kitni baar / haden:** Bed −24..−18 LUFS relative
- **Evidence:** 🟠 — Travel-studio audio QA target
- **Sources:** github_junwen853_travel-video-studio-skill.md
- **Check:** `{"kind": "db_range", "min_db": -24, "max_db": -18, "what": "music bed narration ke relative (LUFS)"}`
- **⚠️ Takraav:** Purane 18–25 dB under-voice default ke qareeb hai, lekin ye LUFS-relative me mapta hai (dB me nahi) — map farq note karo. Isi cluster ke −12 dB duck (KF-07) se takraav upar wale rule me darj hai.

### D2-088 — SFX volume ki seedhi (hierarchy)

- **Kab:** SFX aur music ka balance set karte waqt
- **Kya:** Seedhi rakho (music = 0 dB reference): voice/dialogue music se +3..+6 dB upar; primary SFX 0..+3 dB upar; ambient bed −12..−18 dB neeche; UI sounds (click/pop/ding) −6..−3 dB neeche
- **Kyun:** Har layer ki apni aukaat fix ho to mix kabhi keechad (mud) nahi banta
- **Kitni baar / haden:** Voice +3..+6; SFX 0..+3; ambient −12..−18; UI −6..−3 (music ke relative dB)
- **Evidence:** 🟠 — KF-07 SFX layering rules
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "db_range", "min_db": 3, "max_db": 6, "what": "voice music se upar (dB)"}`

### D2-089 — SFX ki haden: 3 stack, duration-match, comedy sirf meme/viral

- **Kab:** SFX lagate waqt
- **Kya:** Ek frame par 3 se zyada SFX stack mat karo (primary + tail + ambient hi kaafi). SFX ki duration transition ki duration se match kare — peak transition ke beech me, tail aakhir me. Comedy SFX (vine boom, fail horn, airhorn) sirf Meme/Viral modes me; Cinematic/Documentary/Aesthetic/Minimal me inki jagah zero hai
- **Kyun:** Teen se zyada awaazein ek saath = shor; galat mode ka comedy SFX poore mood ko maar deta hai
- **Kitni baar / haden:** Stack ≤3; comedy SFX sirf 2 modes me
- **Evidence:** 🟠 — KF-07 SFX rules
- **Sources:** github_tashisleepy_capcut-ai-director.md
- **Check:** `{"kind": "count_range", "max": 3, "what": "ek frame par stacked SFX"}`

### D2-090 — Audio edges hamesha fade; hard start/stop kabhi nahi

- **Kab:** Har audio clip ke sire par
- **Kya:** Har audio clip ke edges par fade lagao — kabhi hard start/stop nahi. Dissolve/fade par SFX ki jagah kuch nahi ya halka swell; music use carry karta hai
- **Kyun:** Hard audio edges click/pop dete hain jo sabse saste lagte hain
- **Kitni baar / haden:** Bina-fade audio edges = 0
- **Evidence:** 🟠 — KF-07 audio workflow + director niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md

### D2-091 — SFX density mode ke hisaab se; foley sirf motivated

- **Kab:** Sound design ki ghanata (density) tay karte waqt
- **Kya:** Density mode se lo: Viral — SFX har 1–2s; Cinematic — har 5–15s; Documentary — sirf functional; Meme — maximum. Foley sirf tab jab motivated ho — random SFX khaamoshi se bhi bura hai
- **Kyun:** Har mode ki apni awaaz ki bhasha hai; ek density sab par = koi pehchan nahi
- **Kitni baar / haden:** Viral 1–2s; Cinematic 5–15s; Documentary functional only
- **Evidence:** 🟠 — KF-07 mode blueprints + production standard ka foley niyam
- **Sources:** github_tashisleepy_capcut-ai-director.md, github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-092 — Scenic audio policy: loud BGM sirf muted picture par

- **Kab:** Scenic/BGM-led windows ki audio policy me
- **Kya:** Loud BGM sirf muted picture ke upar chalao. Jahan audible speech hai (face-to-camera ya transcript-backed) woh hamesha sunai de. Frustration/conflict/sensitive/dry windows par BGM forbidden rakho. TTS sirf muted-picture windows par chalao
- **Kyun:** Jazbaati pal par bajta khush music ya bolne par chadha BGM — dono film ko jhootha bana dete hain
- **Kitni baar / haden:** Speech windows me BGM-over-voice = 0; sensitive windows me BGM = 0
- **Evidence:** 🟠 — House audio-scene policy
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-093 — BGM asli named music ho; hum/tone/placeholder = block

- **Kab:** BGM select/final karne se pehle
- **Kya:** Final bed hamesha asal, named aur traceable music ho — sine tone, hum, buzz, silence ya procedural placeholder kabhi final nahi. Har asset ki license ledger me verify ho aur Content-ID risk check ho; bina verify kiye 'usable' kabhi mat kaho
- **Kyun:** Tone-bed technical pass ho sakta hai lekin film ko marr deta hai; license bina ka asset baad me claim laata hai
- **Kitni baar / haden:** Placeholder beds = 0; har asset = verified license row
- **Evidence:** 🟠 — BGM musicality + asset ledger contracts
- **Sources:** github_junwen853_travel-video-studio-skill.md

### D2-094 — VO finish master peak −6 dBFS

- **Kab:** Voiceover finish/master karte waqt
- **Kya:** VO finish master ka peak −6 dBFS rakho
- **Kyun:** Neeche rakha peak aage ke processing ke liye headroom deta hai
- **Kitni baar / haden:** Peak = −6 dBFS
- **Evidence:** 🟠 — Note source ke VO-finish preset se
- **Sources:** notes_AdamGarceau_resolve-toolkit.md (note)
- **⚠️ Takraav:** TAKRAAV (map ka): purane targets LUFS-integrated me hain (−14/−16 LUFS). Ye −6 dBFS PEAK hai, integrated loudness nahi — dono ek saath lagu nahi hote. Ye VO production-stage ka number hai, delivery loudness purane LUFS rules se hi tay ho.

### D2-095 — Quiet sections ko haath se +3..+6 dB boost

- **Kab:** Cleanup chain ke baad bache dhime hisso par
- **Kya:** Jo hisse gate/NR ke baad bhi dhime reh jayein, unhe haath se +3..+6 dB boost karo
- **Kyun:** Auto chain ausat ko theek karta hai; sabse dhime pal haath se hi uthte hain
- **Kitni baar / haden:** Boost +3..+6 dB sirf quiet sections par
- **Evidence:** 🟠 — Podcast cleanup workflow
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "db_range", "min_db": 3, "max_db": 6, "what": "quiet section manual boost"}`

### D2-096 — Rang ka kram: normalize pehle, creative grade baad me

- **Kab:** Webcam/talking-head colour grade karte waqt
- **Kya:** Waveform scope padho, laptop screen ko nahi. Node kram: (1) Normalize — blacks ~5–10% (1023 scale par ~64), highlights ~768, contrast 1.1–1.2, pivot 0.3; (2) Balance — neutrals par RGB overlap; (3) Contrast; (4) Skin — HSL qualifier + power window. Creative grade hamesha normalize ke BAAD
- **Kyun:** Galat base par bani grade har nayi roshni me toot jati hai
- **Kitni baar / haden:** 4 nodes, yahi kram
- **Evidence:** 🟠 — Resolve color-grade (webcam) workflow
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-097 — Skin saturation ~60, 70+ kabhi nahi

- **Kab:** Skin tone theek karte waqt
- **Kya:** Skin saturation ~60 ke aas-paas rakho — 70 ya usse upar kabhi nahi. Skin ko warm gain do aur qualifier + power window se alag sambhalo
- **Kyun:** 70+ saturation par chehra narangi-pakoda ho jata hai
- **Kitni baar / haden:** Skin sat ≈60; >70 = block
- **Evidence:** 🟠 — Usi colour workflow se
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "percent_range", "target": 60, "max_pct": 70, "what": "skin saturation"}`

### D2-098 — Grade ko PowerGrade bana kar rakho; har roshni ka alag grade

- **Kab:** Grade mukammal hote hi
- **Kya:** Final grade ko PowerGrade/preset bana kar save karo taaki reuse ho. Har nayi lighting setup ke liye phir se grade karo — purana grade nayi roshni par zabardasti mat lagao
- **Kyun:** Roshni badli to rang ke sawaal badle; copy-paste grade aadhi jagah galat hota hai
- **Kitni baar / haden:** Har setup = apna grade; save hamesha
- **Evidence:** 🟠 — Colour workflow
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md

### D2-099 — Audio track layout: A1–A4 aur stack ka kram

- **Kab:** Multicam/podcast ya bade edit ki timeline sajate waqt
- **Kya:** Tracks aise rakho: A1 selected dialogue, A2 processed dialogue, A3 music/ambience, A4 SFX/bumpers. Aam stack ka kram neeche se upar: ambient/room tone → music → SFX → voice sabse upar
- **Kyun:** Bikhre tracks par mix kabhi dobara nahi milta; sajawat hi aadha mix hai
- **Kitni baar / haden:** 4 tracks fixed bhumika; stack kram fixed
- **Evidence:** 🟠 — Do sources: podcast track layout + KF-07 stacking order
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md, github_tashisleepy_capcut-ai-director.md

### D2-100 — Delivery verify bahari meter se; platform exports tay

- **Kab:** Final export aur delivery check par
- **Kya:** Loudness ko bahari meter se verify karo: YouTube −14 ±1 LUFS. Platform exports: YouTube 1920x1080 −14 LUFS; LinkedIn 1080x1080 −16 LUFS; vertical 1080x1920 −16 LUFS. Manual position keyframes ki jagah AI Smart Reframe ko tarjeeh do (vertical ke liye)
- **Kyun:** Editor ke andar ka meter jhooth bol sakta hai; bahari map hi saboot hai
- **Kitni baar / haden:** YT −14 ±1 LUFS verified
- **Evidence:** 🟡 — YouTube ka −14 LUFS platform normalization spec maana gaya number hai; baaki platform numbers source ke house targets hain
- **Sources:** github_ChaiWithJai_davinci-resolve-claude-skills.md
- **Check:** `{"kind": "lufs_target", "value": -14, "tolerance": 1, "platform": "YouTube"}`

### D2-101 — Share se pehle silent-track check

- **Kab:** Koi bhi video share/export se pehle
- **Kya:** Audio ka mean_volume check karo: −80 dB se neeche matlab track silent/muted hai — share mat karo, pehle theek karo
- **Kyun:** Muted track wala export sabse sharminda karne wali galti hai aur sabse aasan pakdi jati hai
- **Kitni baar / haden:** Mean volume ≤−80 dB = block
- **Evidence:** 🟠 — Screencast workflow ki pre-share check
- **Sources:** github_matthull_my-skills.md

### D2-102 — Export: quality rakho, file size par nazar (25 GB trap)

- **Kab:** Final export settings tay karte waqt
- **Kya:** Quality barkarar rakho lekin file size hamesha dekho — bina dekhe export 25 GB jaise trap me phans sakta hai
- **Kyun:** Upload/share par size hi sabse pehli rukawat banta hai
- **Kitni baar / haden:** Har export = size check ke saath
- **Evidence:** 🟠 — Note source
- **Sources:** notes_appariciojunior_video-editor-skills.md (note)

### D2-103 — Podcast punch-in active speaker par switch kare

- **Kab:** Multicam podcast edit me
- **Kya:** Punch-in/camera switch hamesha us speaker par ho jo bol raha hai (pitch-based speaker pehchan se madad lo)
- **Kyun:** Galat chehre par kata hua jawaab viewer ko gumrah karta hai
- **Kitni baar / haden:** Switch = active speaker par hi
- **Evidence:** 🟠 — Note source
- **Sources:** notes_AdamGarceau_resolve-toolkit.md (note)

### D2-104 — Filters/retouch mamuli (moderate) rakho

- **Kab:** CapCut mobile me filters/effects/retouch lagate waqt
- **Kya:** Filters aur effects conservative rakho; portrait retouch moderate aur natural rakho — chehra plastic na lage
- **Kyun:** Zyada retouch pehle frame me pakda jata hai aur bharosa todta hai
- **Kitni baar / haden:** Retouch = moderate/natural hamesha
- **Evidence:** 🟠 — CapCut mobile workflow
- **Sources:** github_pockebot_openpocket.md

### D2-105 — Motion overlays bole gaye shabdon ke saath timed

- **Kab:** Motion graphics/overlays lagate waqt
- **Kya:** Overlays ko un shabdon ke saath time karo jinke baare me woh hain. Face aur caption wale hisse hamesha clear rakho
- **Kyun:** Der se aaya overlay purani khabar hai; chehre par aaya overlay rukawat
- **Kitni baar / haden:** Overlay timing = shabd ke saath; face/caption zone clear
- **Evidence:** 🟠 — Note source
- **Sources:** notes_appariciojunior_video-editor-skills.md (note)

### D2-106 — Travel delivery master: 4K 60fps, ≥60 Mbps

- **Kab:** Travel footage (DJI/action/phone) ki master delivery par
- **Kya:** Master target rakho: 4K, 59.94/60fps, kam se kam 60 Mbps — jab source footage is kabil ho
- **Kyun:** Neeche ka master baad me har platform par kamzor padta hai
- **Kitni baar / haden:** 4K 60fps ≥60 Mbps (source allow kare to)
- **Evidence:** 🟠 — Travel-studio ka Definition of Done
- **Sources:** github_junwen853_travel-video-studio-skill.md

## ⚠️ Takraav ki list (purane 261 rules / ORDER defaults se)

- **D2-041 (Visual change gap 3s se zyada (short-form) = pattern interrupt):** TAKRAAV: purane ORDER default me long-form max visual gap 5s hai (Shorts 3s). Ye 3s wala niyam short-form/social ke liye hai — long-form par 5s wala hi rahe; profile se lagu karo, dono ko ek mat samjho.
- **D2-044 (Pause ke niyam (talking head): 0.5s / 1.0s / dramatic chhoot):** TAKRAAV: purana unified pause model ≥400ms ko cut zone, 150–400ms ko usable aur <150ms ko unsafe kehta hai. Ye source 500ms threshold rakhta hai aur 300–500ms dramatic pause ko surakshit maanta hai. Merge par faisla: threshold 400ms vs 500ms — profile (talking-head social = 0.5s wala; Kang pipeline = purana model) se tay karna bacha hai.
- **D2-045 (Smart-cut: >1s silence aur duplicate takes pehle pass me bahar):** TAKRAAV: purana pause model ≥400ms ko hi cut zone kehta hai — >1s wala threshold usse zyada conservative hai. Ye sirf AUTO pehle pass ke liye hai (haath ka fine pass purane model par hi rahe), isliye takraav pass-wise sulajh sakta hai.
- **D2-053 (A-roll reset: 6–9s se zyada bina reset ke nahi (talking-head social)):** TAKRAAV (halka): purana max visual gap default 5s hai. Ye 6–9s wala window sirf 'A-roll reset' ki had hai (speaker frame par lagatar rehne ki), aam visual-change gap se alag mapna — dono ek saath chal sakte hain: visual change 5s ke andar, A-roll reset 9s ke andar.
- **D2-062 (Vlog silence cuts me chhote pads (saans) rakho):** Purane unified pause model ka remainder 0.2–0.45s is niyam se takrata nahi — ye usi 'saans' ko vlog context me kehta hai, par exact ms nahi deta.
- **D2-080 (Cover/hero-title formula: 1–5 shabd, pehchan wali background):** TAKRAAV: purana thumbnail niyam target ≤3 shabd, hard cap 4 kehta hai. Ye source 1–5 shabd deta hai. Cover (video hero title) aur thumbnail ko alag maanna sulah ho sakti hai; merge par user/engine faisla kare.
- **D2-083 (Ducker: shuruaat 2.7 dB, 5 dB se zyada = amateur):** TAKRAAV: purana ORDER default 'music voice se 18–25 dB neeche' bed-LEVEL ki baat hai; ye 2.7 dB DUCKER ki depth hai (kitna ghatao) — donon alag map hain, takraav asal me map ka hai. Lekin isi cluster ka KF-07 duck −12 dB (D2 style rule 'Narration duck landmarks') is 2.7–5 dB se sach me takrata hai — context farq: ye podcast dialogue-chain ka ducker hai, woh CapCut music-bed duck hai. Merge par profile-wise chuna jaye.
- **D2-084 (Podcast loudness verify: −16..−20 LUFS, peaks −9..−3 dBFS):** Note: purana podcast profile −16 LUFS deta hai. Ye range −16..−20 hai — dialogue-only podcast ke liye neeche tak ijazat deta hai. Takraav halka; profile me range likh kar sulajh sakta hai.
- **D2-086 (Narration duck landmarks: −12 dB, 10f/15f fades):** TAKRAAV: purana default bed music ko voice se 18–25 dB neeche rakhta hai; −12 dB usse kam gehra hai. Aur ChaiWithJai ke ducker (2.7 dB start, >5 dB amateur) se bhi takrata hai. Teeno alag contexts ke numbers hain (bed level / CapCut duck / podcast ducker) — merge par har profile ka ek number tay karna hoga.
- **D2-087 (Music bed narration ke neeche: −24..−18 LUFS relative):** Purane 18–25 dB under-voice default ke qareeb hai, lekin ye LUFS-relative me mapta hai (dB me nahi) — map farq note karo. Isi cluster ke −12 dB duck (KF-07) se takraav upar wale rule me darj hai.
- **D2-094 (VO finish master peak −6 dBFS):** TAKRAAV (map ka): purane targets LUFS-integrated me hain (−14/−16 LUFS). Ye −6 dBFS PEAK hai, integrated loudness nahi — dono ek saath lagu nahi hote. Ye VO production-stage ka number hai, delivery loudness purane LUFS rules se hi tay ho.

## 🚫 Chhodi hui tool-operation content (rule NAHI bani)

Neeche wali content shudh API/operation/catalog thi — editing ka faisla nahi — isliye rule nahi bani. Ginti lines ke hisaab se takreeban hai:

- **github_TerminalSkills_skills.md — poora file (~225 lines):** Resolve API/automation calls hi hain; editorial rule 0.
- **ChaiWithJai file ke hisse (~1,000 lines):** computer-use-training (~466), resolve-automation/rust API references (~177), troubleshooting (~226), setup/install (~134).
- **junwen853 file ke hisse (~960 lines):** davinci-resolve-api reference (~152), capcut-jianying-draft-automation (~209), aur references ke andar ke bash/script command blocks + smoke-test ops prose (~600).
- **tashisleepy file ke hisse (~3,410 lines):** PART B platform/UI reference (~441), PART C (~212), KF-01 UI navigation (~543), KF-05 ka catalog hissa — ART style/template/panel lists (~550), KF-09 effect-metadata naam-lists (~1,452), KF-10 AI-stylize catalog (~212). Sirf technique wale KF (brain PART A, KF-05 ke caption niyam, KF-07 audio) se rules bani.
- **Notes ke tool-hisse (4 items):** Fusion node-wiring trap (AdamGarceau note), Resolve traps — 1080-on-4K 400% crop / alpha premultiply / adjustment-layer substitute (edwinponcious12 note), EDL-replay ki timeline mechanics (SamuelAde001 note), AI Smart Reframe ki operation-tarjeeh (ChaiWithJai).
- **Junwen ke locale-specific font naam (Japan fonts ki list):** catalog maana gaya, rule nahi.

**Kul chhoda hua: takreeban 5,600 lines (kul extraction ~12,200 lines ka ~46%) + notes ke 4 tool-items.**
