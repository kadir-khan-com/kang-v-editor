# Step 2 — Rules, Part A (Cluster A)

Step 1 ke chaar bade sources se nikale gaye rules. Har rule: kab lagana hai, kya karna hai, kyun, kitni baar (numbers ke saath), evidence tag, aur source. Ek hi baat kai sources me aayi to merge karke saare sources likhe hain.

**Sources (is cluster ke):**
- `github_kmilo93sd_agent-video-editor.md`
- `github_Melvynx_video-agent-skills.md`
- `github_1610-advisory_mktkit.md`
- `github_expocut_claude-plugin_retention-playbook.md`

> ⚠️ **ExpoCut attribution:** Free to use and redistribute with attribution to expocut.com — ExpoCut se aaye rules (unke evidence_note me ye note dobara likha hai) is shart ke saath use/redistribute hote hain.

**Evidence tags:** 🟢 = peer-reviewed research · 🟡 = measured corpus / platform data · 🟠 = creator/editor opinion ya house rule

**Kul rules: 91** — kahani 27, samajh 23, rhythm 21, style 20 · Evidence: 🟢 3, 🟡 21, 🟠 67

---

## KAHANI — kahani aage badhe, vaada bache

### A-001 · Vaada sabse pehle 🟡
- **Kab:** Har video ki shuruaat par
- **Kya:** Title/thumbnail jo vaada kare, wahi cheez pehle seconds me dikhao ya bolo — result, sabse striking moment, ya woh sawal jiska jawab video hai
- **Kyun:** Viewer pehle seconds me faisla karta hai; YouTube ka official lever hai ki thumbnail/title asal content ko reflect kare aur intro wahi dikhaye
- **Kitni baar / limits:** Har video; long-form me pehle 5-30 s ke window me, Shorts me pehle frame/3 s me
- **Evidence:** 🟡 — YouTube official guidance (YT-moments, platform) + Melvynx ke measured outlier data; ExpoCut playbook bhi yahi kehta hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Machine check:** `{"kind": "hook_within_s", "value": 5}`

### A-002 · Intro, greeting, logo pehle nahi 🟠
- **Kab:** Video ke opening seconds me
- **Kya:** Logo intro, greeting ya 'in this video we'll see' se shuru mat karo; logo aaye to content ke upar card ki tarah aaye, alag shot me nahi
- **Kyun:** Pehle seconds vaade ke liye hain; intro pehle aane se audience wahi girti hai jahan video sabse kamzor hai
- **Kitni baar / limits:** Har video, bina apvaad
- **Evidence:** 🟠 — Creator practice (TubeBuddy/TikTok blogs) + kmilo aur Melvynx dono ke house rules; ExpoCut: 'never on an intro card'
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`

### A-003 · Cold open = sabse mazboot moment 🟠
- **Kab:** Video ki structure banate waqt
- **Kya:** Video ke best moment/line ko shuruaat me rakho (vlog ka best pal, podcast ki sabse mazboot exchange, tutorial ka end-state), phir context par wapas aao
- **Kyun:** Thanda, dheere chadhne wala start viewer ko rok nahi pata; best moment hi thumbnail ke vaade ko sach karta hai
- **Kitni baar / limits:** Talking head 5-15 s, podcast 15-60 s, tutorial hook 10-20 s (end-state pehle)
- **Evidence:** 🟠 — Creator practice (TubeBuddy-hacks aadi) — kmilo recipes ka standing structure rule
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-004 · Hook formula se, score 7+ ka gate 🟠
- **Kab:** Har script likhte waqt
- **Kya:** 3 hooks 3 alag formulas se likho (22 formulas ki library: pain, claim, number, mistake, story, promise, curiosity, proof, reaction), har hook ko 5-point rubric (Specific, Tension, Viewer, Fast, True) par 0-2 score karo, best rakho; sab 7/10 se kam hon to 3 aur likho
- **Kyun:** Ek hi andaz ka hook aksar kamzor hota hai; teen vikalp + score se mazboot hook chunna aasan aur dohraane layak hota hai
- **Kitni baar / limits:** Har script par 3 hooks; rakha hua hook ≥7/10
- **Evidence:** 🟠 — Melvynx studio-script ka creator system (rubric usi ka banaya hua, koi public data nahi)
- **Sources:** `github_Melvynx_video-agent-skills.md`
- **Machine check:** `{"kind": "min_score", "what": "hook_score", "value": 7, "scale": 10}`

### A-005 · On-screen hook chhota aur alag 🟠
- **Kab:** Short ki pehli 1-2 s me on-screen text lagate waqt
- **Kya:** Screen par hook 6-7 shabd se zyada nahi, ek accent word ke saath; woh spoken hook ki copy na ho, usme kuch jode (number, result, sawal)
- **Kyun:** Sound-off viewer ko screen wala hook hi rokta hai; bola hua dohraane se dusri jaankari ki jagah khali जाती hai
- **Kitni baar / limits:** Har short; Melvynx ≤6 shabd, ExpoCut 4-7 shabd
- **Evidence:** 🟠 — Melvynx house rule + ExpoCut playbook practice (ExpoCut: Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Machine check:** `{"kind": "max_words", "what": "on_screen_hook", "value": 7}`

### A-006 · Open loop kholo, aakhir se pehle band mat karo 🟠
- **Kab:** Script ki structure me
- **Kya:** Aage aane wali cheez announce karo ('teesri wali ne hairaan kar diya') aur uska payoff end ke paas do; har sentence usi ek vaade ko aage badhaye, detour nahi
- **Kyun:** Khula sawal viewer ko roke rakhta hai; jo hissa video ko aage nahi badhata, retention graph wahi girta hai
- **Kitni baar / limits:** Har video me kam se kam 1 open loop, payoff end se pehle nahi
- **Evidence:** 🟠 — Creator practice (kmilo hook-and-retention); Melvynx ke measured viral data me 'one promise, paid line after line' isko support karta hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-007 · Re-hook 40-60% par 🟡
- **Kab:** Script ke beech wale hisse me
- **Kya:** 40-60% ke aas-paas ek line rakho jo dhyaan restart kare: naya sawal, number, twist ('lekin isse theek nahi hua'), ya sabse mushkil hissa ('ye wala sab skip karte hain')
- **Kyun:** Beech me dhyaan girna sabse aam hai; ek naya gap wahi rokta hai jahan viewer jaane wala hota hai
- **Kitni baar / limits:** 25 s se lambi har script me 1 re-hook; 25 s se chhoti skip kar sakte ho
- **Evidence:** 🟡 — Melvynx ke niche-outlier measurements (apne studied accounts) me consistent pattern — measured data, peer-reviewed nahi
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-008 · Ek video = ek idea, ek vaada 🟠
- **Kab:** Topic aur script tay karte waqt
- **Kya:** Ek hi idea rakho; script me 'and also' aaye to woh dusri video hai; hook se ask tak ek hi promise chale
- **Kyun:** Do topics wala video dono me aadha rehta hai; ek vaada hi retention aur share dono banata hai
- **Kitni baar / limits:** Har video par
- **Evidence:** 🟠 — Melvynx script-rules ka house rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-009 · Topic pehle, script baad me (proven concept) 🟡
- **Kab:** Kuch bhi likhne se pehle, planning par
- **Kya:** Woh concept chuno jo niche me pehle over-perform kar chuka ho (account median ke x3+ outliers wala); kaam ka kram: topic > hook > structure; fresh news wala topic ho to use week me pehle rakho
- **Kyun:** Measured data kehta hai views topic se bante hain — same creator, same edit, topic badalte hi x1 se x100 ka farak
- **Kitni baar / limits:** Week ke 5 scripts me kam se kam 3 proven concept par
- **Evidence:** 🟡 — Melvynx ke outlier measurements (har studied niche me median ke muqable) — measured data
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-010 · Object 0 second par, hook me specific 🟡
- **Kab:** Short ke pehle frame aur pehli line par
- **Kya:** Jis cheez ke baare me video hai use pehle second me dikhao (naam baad me), aur pehli line me kam se kam ek specific rakho: number, bade brand ka naam, ya 'free'
- **Kyun:** Viewer 1 s me tay karta hai 'ye mere liye hai ya nahi'; creator ke baare me hook ya vague category x1 par reh jati hai
- **Kitni baar / limits:** Har short par
- **Evidence:** 🟡 — Melvynx viral research ke measured rules (every niche checked)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-011 · Proof 8 second ke andar 🟡
- **Kab:** Video ki shuruaat me
- **Kya:** 8 s ke andar proof dikha do — number, screen, ya receipt — taaki viewer ko baaki video par bharosa ho
- **Kyun:** Bina saboot ke vaada sirf daava lagta hai; jaldi proof aage ki baaton ko wazan deta hai
- **Kitni baar / limits:** Har script; viral data kehta hai 4-7 s sabse achha
- **Evidence:** 🟡 — Melvynx viral measurements (proof by 4-7 s) + script trigger rule (proof before 8 s)
- **Sources:** `github_Melvynx_video-agent-skills.md`
- **Machine check:** `{"kind": "proof_within_s", "value": 8}`

### A-012 · Triggers kam se kam 4, apni jagah par 🟠
- **Kab:** Script likhne ke baad check karte waqt
- **Kya:** Kam se kam 4 triggers sahi jagah rakho: curiosity gap (hook), self-recognition (hook/line 2), proof (8 s se pehle), enemy (problem par — tool/habit/myth, viewer kabhi nahi), pattern break (re-hook), specificity (fix me), loss/urgency (ask se pehle; fake scarcity kabhi nahi)
- **Kyun:** Script isiliye tikti hai kyunki har hissa sahi pal par ek lever kheenchta hai
- **Kitni baar / limits:** Har script me ≥4 triggers
- **Evidence:** 🟠 — Melvynx script-rules ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-013 · Funnel: darwaza bada, pivot 20-35% par 🟠
- **Kab:** Naye viewers tak pahunchne wali Teach/Opinion video par
- **Kya:** M ya L size ke topic se kholo (bridge 0-3 s: debate, bada naam, sabki roz ki scene), tension 3-10 s, pivot script ke 20-35% par niche ki taraf modo, pearl (sabse mazboot line) sabse pehle likho; bridge par 2 test: niche tak 15 s ke andar pahunche? kal ko is viewer ko offer chahiye hoga?
- **Kyun:** Sirf niche ke topic par video chhote test group me hi marti hai; bada darwaza sahi viewer ko andar laata hai
- **Kitni baar / limits:** Naye-reach wali videos par; pivot hamesha 20-35% band me
- **Evidence:** 🟠 — Melvynx funnel reference ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-014 · Divisive bridge ke kaide 🟠
- **Kab:** Funnel me behes wala bridge use karte waqt
- **Kya:** Niche ke pehchane debate par ek paksh lo, ek sentence me kaho aur use fairly defend karo (pehle opposite ki ek line, phir apni wajah + example); hamla idea/habit/tool par ho, kisi person ya viewer group par kabhi nahi; CTA soft rakho (proximity 0-1)
- **Kyun:** Behes sabse chauda darwaza hai, lekin galat nishana rage-bait ban jata hai aur sakht sale usi pal bharosa tod deta hai
- **Kitni baar / limits:** Divisive script me; bridge kabhi poori video nahi
- **Evidence:** 🟠 — Melvynx funnel reference ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-015 · Hook khule, sirf ek baar repeat ho 🟠
- **Kab:** Koi line hook bana kar cut ki shuruaat me rakho to
- **Kya:** Hook line cut ko khole aur poori edit me apne context me sirf ek baar repeat ho; dusri baar repeat kabhi nahi
- **Kyun:** Reviewer ki standing pasand: ek repeat context deta hai, dusra repeat defect mana gaya (pipeline ke apne itihaas me repeat bug do baar lauta)
- **Kitni baar / limits:** Har reel jisme hook prepend ho — repeat count theek 1
- **Evidence:** 🟠 — mktkit owner/reviewer ka house rule, QA gate (hook.once) se enforce hota hai
- **Sources:** `github_1610-advisory_mktkit.md`
- **⚠️ Takraav:** Ye sirf mktkit ka design rule hai; baaki teen sources me hook-repeat ka koi niyam nahi — aam taur par repeat ko galti hi mana jata hai, dusri pipeline me lagane se pehle socho

### A-016 · Chapters ke niyam 🟡
- **Kab:** Lambi video (tutorial, podcast, explainer, lamba vlog) publish karte waqt
- **Kya:** Pehla timestamp 00:00 ho, kam se kam 3 timestamps ascending order me, har chapter ≥10 s ka; timestamps edit ke asli times se lo, aankh se naap kar nahi
- **Kyun:** Viewer apne kaam ke hisse par seedha jump karta hai aur markers use wapas aana aasan karte hain (Guo 2014 me bhi yahi pattern)
- **Kitni baar / limits:** Har lambi video par
- **Evidence:** 🟡 — YouTube official chapters spec (platform rule)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "min_chapter_duration_s", "value": 10}`

### A-017 · End screen aur closing 🟡
- **Kab:** YouTube lambi video ke aakhir me
- **Kya:** Aakhri 5-20 s end screen ke liye khaali rakho (video ≥25 s ho, ≤4 elements aayenge, wahan zaroori text mat rakho); closing ek sentence me batao aage kahan jana hai — lambi recap nahi
- **Kyun:** End screen elements content ko dhak dete hain; lambe sign-off par hi retention sabse tez girti hai
- **Kitni baar / limits:** Har eligible YouTube video par
- **Evidence:** 🟡 — YouTube official end-screen spec (platform rule)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-018 · CTA ek line me, object ke saath 🟡
- **Kab:** Video ke aakhir me ask rakhte waqt
- **Kya:** Ek hi ask, ek line me, aur woh koi cheez de (repo, guide, prompt); Shorts me CTA card aakhri 2-3 s me; 'thanks for watching' ya bina exact shabd wala 'comment karo' nahi
- **Kyun:** CTA views nahi banata, comments/DMs banata hai — aur kai asks ek saath koi ask nahi banta
- **Kitni baar / limits:** Har video me 1 ask; Offer video ke alawa soft
- **Evidence:** 🟡 — Melvynx viral measurements (CTA reach nahi banata) + shorts-codes ka house rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-019 · Facts aur numbers invent mat karo 🟠
- **Kab:** Script ya video me koi number, naam ya result aaye to
- **Kya:** Number/naam/result sirf asal source se (creator ke diye hue facts); jo na mile use {{placeholder}} rakho aur 'bharna baki' me likho; koi figure bina source ke mat ghusao — source na ho to saaf kaho
- **Kyun:** Gadha hua number ek baar pakda jaye to poori channel ki baaton par bharosa jata hai
- **Kitni baar / limits:** Har script, har video
- **Evidence:** 🟠 — kmilo hard rule ('No invented numbers') + Melvynx facts rule — dono house/creator ethic
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-020 · Licensed media hi; meme recreate karo 🟠
- **Kab:** Music, SFX, footage ya meme use karte waqt
- **Kya:** Sirf CC0, YouTube Audio Library, ya commercial use ki written license wala media lo; NC ya 'YouTube par mila hua' kabhi nahi; meme ka original media/music mat uthao — joke ko apne graphics se recreate karo
- **Kyun:** Monetized channel par ek claim poori video (aur channel) ko mehenga pad sakta hai
- **Kitni baar / limits:** Har asset par; library me naya sound aaye to uska license evidence record karo
- **Evidence:** 🟠 — kmilo hard rule + licenses reference (house rule, legal risk par based)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-021 · Body ki banawat type ke hisaab se 🟠
- **Kab:** Script ka body likhte waqt
- **Kya:** Type-wise beats rakho — Teach: problem → kyun hota hai → fix (steps/ek move) → kya badlega; Proof: result+number → concretely kya kiya → copyable hissa → honest catch; Story: moment (mid-scene) → turn → ek line ka lesson; Opinion: position → opposite ko fairly → reason+example → kya karein; Talking head: cold open → context → sections (har section mini-hook se khule) → payoff
- **Kyun:** Har type ka viewer alag ummeed se aata hai; banawat wahi ummeed poori karti hai to beech me girawat nahi aati
- **Kitni baar / limits:** Har script par uske type ki banawat
- **Evidence:** 🟠 — Melvynx script-rules (body by type) + kmilo talking-head recipe structure
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`

### A-022 · Week ka mix aur offer ki doori 🟠
- **Kab:** Hafte ki scripts plan karte waqt
- **Kya:** Pehle mix banao (5 me lagbhag Teach 2, Proof 1, Story 1, Opinion 1, Offer ≤1); ek hi hook formula lagatar do baar nahi, ek hi type hafte me teen baar nahi; offer proximity ladder 0-3 rakho — rung 3 hafte me ≤1 aur woh bhi sabse mazboot value video ke baad
- **Kyun:** Ek hi tarah ki videos thakati hain aur har video me bechna bharosa khatm karta hai
- **Kitni baar / limits:** Har week ke plan par
- **Evidence:** 🟠 — Melvynx week-mix aur offer-proximity house rules
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-023 · Hit concept ko do hafte me repeat karo 🟡
- **Kab:** Apna koi concept x3+ over-perform kare to
- **Kya:** Use 2 hafte ke andar 2-3 naye hooks ya naye items ke saath repost karo, use 'luck' kehne se pehle
- **Kyun:** Jo shape ek baar median se kai guna gaya, woh recipe hai; dohraana hi use sabit karta hai
- **Kitni baar / limits:** Har x3+ hit par, 14 din ke andar
- **Evidence:** 🟡 — Melvynx viral measurements ka rule (apne studied accounts par)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-024 · Retention report padh kar seekho 🟡
- **Kab:** Video publish hone ke baad
- **Kya:** Retention report dekho: jis moment par dip hai wahi agli baar cut/sudhar ka candidate hai; spikes (rewatch/share wale hisse) pehchano aur unhe dohraane ki koshish karo
- **Kyun:** Graph jhooth nahi bolta — dip aksar usi hisse par hota hai jo video ko aage nahi badhata
- **Kitni baar / limits:** Har publish ke baad (key moments ≥60 s aur ≥100 views wali videos par milte hain)
- **Evidence:** 🟡 — YouTube official key-moments feature (platform data)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-025 · Script ki lines: ek saans, 4-15 shabd 🟠
- **Kab:** Script likhte waqt
- **Kya:** Ek line = ek sentence = ek saans, 4-15 shabd; abstract lines lagatar 3 nahi — teesri ko example bana do; ek viewer se baat karo ('you', 'you guys' nahi); chhote shabd, jo dost ko na kaho woh kato
- **Kyun:** Lambi, abstract lines bolne me bhi atakti hain aur sunne me bhi; ek-saans wali lines hi natural lagti hain
- **Kitni baar / limits:** Har script ki har line par
- **Evidence:** 🟠 — Melvynx script-rules ka house style
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-026 · AI wali banawat hatao (humanize) 🟠
- **Kab:** Script ya koi bhi text finalize karne se pehle
- **Kya:** AI ke nishan saaf karo: hype shabd (delve, unlock, game-changer jaisi khaali badi baatein) hatao ya number se badlo; preamble ('here's the thing') kato; recap ending hatao; engagement bait ('save this', 'tag someone') sirf asl ask se badlo; false contrast ('it's not X, it's Y') poori text me ≤1; tino-tino ki triads tod do
- **Kyun:** Chat-model jaisi banawat viewer ko turant 'ye asli insaan nahi' ka sanket deti hai aur bharosa girta hai
- **Kitni baar / limits:** Har script/text par aakhri pass
- **Evidence:** 🟠 — Melvynx ai-tells + humanize references ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-027 · Clip standalone banao (long se short) 🟠
- **Kab:** Lambi video se Short/Clip nikaalte waqt
- **Kya:** Clip aisi jagah se kato jo bina context samajh aaye: pehli line 'so', 'as I said', 'this' jaisi bahari sahara wali na ho; ek hi idea poora ho; end finished thought par ho; long video ke references ('pichle part me') hata do; end payoff ya loop par
- **Kyun:** Jo clip context maangta hai woh feed me akela khada nahi ho pata
- **Kitni baar / limits:** Har clip 20-60 s; Melvynx ka standalone score ≥7/10 (5 points × 0-2)
- **Evidence:** 🟠 — Melvynx clips skill ka scoring system + kmilo shorts recipe
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "duration_range_s", "what": "clip_from_long_form", "min": 20, "max": 60}`

## SAMAJH — clarity, galat-fehmi na ho, padhna aasan

### A-028 · B-roll exactness: bola wahi dikhe 🟢
- **Kab:** Voice jo naam le use dikhaya ja sakta ho to
- **Kya:** B-roll/punch wahi cheez literally dikhaye jo boli gayi (spoken noun phrase); exact asset na mile to speaker par hi raho — same-category ki tasveer (kisi bhi darwaze se 'hidden door') fallback nahi, defect hai; photo tabhi jab human-confirmed subject match kare, aur video hamesha photo se pehle
- **Kyun:** Alag ya sajawati visual dhyaan todta hai aur comprehension girata hai; exact visual baat ko pakka karta hai
- **Kitni baar / limits:** Har punch/B-roll par
- **Evidence:** 🟢 — Mayer (2008, peer-reviewed) ka coherence principle; mktkit ka owner rule ('exact or nothing', 2026-09-07) iska sakht roop hai — woh hissa 🟠
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`

### A-029 · Graphic sirf jab samjhaye 🟢
- **Kab:** Koi graphic ya on-screen text jodne se pehle
- **Kya:** Graphic sirf tab: (1) jo camera nahi dikha sakta woh dikhana ho (concept, comparison, number, timeline, map), ya (2) structure mark karna ho (section title, naam, step counter); jo graphic hatane se kuch na ghate woh hatao; voice ki baat ko text me mat dohrao — text woh ho jo bola nahi gaya (naam, number, key term)
- **Kyun:** Shabd + tasveer saath sikhati hai, lekin bekaar graphic aur dohra hua text dono seekhna aur samajh girate hain
- **Kitni baar / limits:** Har graphic par
- **Evidence:** 🟢 — Mayer (2008, peer-reviewed) — multimedia, coherence aur redundancy principles
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-030 · Graphic kabhi khaali nahi, word se bandha ho 🟠
- **Kab:** Koi card, table ya graphic screen par aaye to
- **Kya:** Graphic use shabd se zyada se zyada 0.5 s pehle enter kare jo use introduce karta hai; pehla content element 1 s ke andar aa jaye; har row/element us shabd ke ≤0.6 s ke andar enter kare jo use naam de; koi card 1 s se zyada khaali na rahe; aakhri phrase ke ~1.2 s baad graphic chala jaye; elements even stagger se nahi, shabdo se bandh kar aayein
- **Kyun:** Khaali frame intezaar karta hua graphic galti lagta hai aur viewer ka dhyaan wahi atakta hai
- **Kitni baar / limits:** Har graphic par
- **Evidence:** 🟠 — kmilo house rules (reference tutorial ke pehle cut ki review se bane)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "max_lead_s", "what": "graphic_before_its_word", "value": 0.5}`

### A-031 · On-screen text ka reading-time formula 🟡
- **Kab:** Koi bhi text screen par rahe to
- **Kya:** Text ki duration = max(1.5 s; words × 0.33 s + 0.5 s) rakho (0.33 s/shabd = 160-180 wpm padhne ki gati); jo label voice ke saath jata hai woh apne shabd ke saath enter kare aur bole jaane ke 0.6 s baad tak rahe — formula se kam kabhi nahi
- **Kyun:** Jaldi gayab text padha hi nahi jata; padhne se pehle use dhoondhne ka bhi samay lagta hai (+0.5 s isiliye)
- **Kitni baar / limits:** Har text event par
- **Evidence:** 🟡 — BBC subtitle guidelines (160-180 wpm) se derived; +0.5 s aur label wala hissa kmilo house
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "formula", "what": "on_screen_text_duration_s", "expr": "max(1.5, words*0.33+0.5)"}`

### A-032 · Captions ke standard specs 🟡
- **Kab:** Closed captions/subtitles banate waqt
- **Kya:** ≤42 characters per line, ≤2 lines; reading speed ≤20 characters/s (bachchon ke liye 17); har event ≥20 frames (≈0.83 s); events ke beech gap ≥2 frames; line break punctuation ke baad ya conjunction/preposition se pehle rakho — article ko noun se, pehle naam ko upnaam se kabhi mat todo
- **Kyun:** Ye duniya bhar ke broadcast specs hain — inse tez ya lambe captions padhe nahi jate
- **Kitni baar / limits:** Har caption event par
- **Evidence:** 🟡 — Netflix Timed Text Style Guide (platform/broadcast spec)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_1610-advisory_mktkit.md`
- **Machine check:** `{"kind": "max_chars", "what": "caption_line", "value": 42}`
- **⚠️ Takraav:** mktkit vertical (1080 px wide) ke liye 32 chars × 2 lines rakhta hai kyunki wahan 42 fit nahi hota (DCMP Captioning Key bhi 32 kehta hai) — vertical me 32, 16:9 standard captions me 42

### A-033 · Caption cue join cross na kare, shabd drop na ho 🟡
- **Kab:** Captions ko edit points ke saath rakhte waqt
- **Kya:** Cue kabhi edit join ko cross na kare (har spine boundary par cue split karo); rakha hua koi shabd caption se drop na ho; speech agar cut ke 0.5 s ke andar shuru/khatm ho to cue ko cut par hi rakho, cross sirf tab jab speech khud cross kare
- **Kyun:** Join ke paar latka caption galti dikhta hai; range ke aakhir ke chhote shabd clamp me gayab hona ek asal defect raha hai
- **Kitni baar / limits:** Har caption cue par
- **Evidence:** 🟡 — Netflix timing guide ke shot-change rules (platform spec) + mktkit ka engine-enforced house rule
- **Sources:** `github_1610-advisory_mktkit.md`, `github_kmilo93sd_agent-video-editor.md`

### A-034 · Burned-in social captions ka tareeka 🟠
- **Kab:** Shorts/Reels/TikTok ke liye captions burn karte waqt
- **Kya:** Captions word-timed rakho; chunk chhota rakho; bola ja raha shabd accent color/highlight me dikhao; badi bold sans-serif, outline ya box ke saath; har page ≥20 frames rahe; jab board wahi shabd dikha raha ho to captions hide karo; numbers ko digits me likho (shabdon me nahi); caption engine ke defaults: min cue 0.8 s, max cue 2.8 s
- **Kyun:** 80%+ viewers muted ya kam awaaz me dekhte hain — wahan captions hi awaaz hain
- **Kitni baar / limits:** Har short-form video par
- **Evidence:** 🟠 — Creator practice teeno sources me; muted-viewing wala aankda Melvynx shorts-codes ka (80%+)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_1610-advisory_mktkit.md`
- **⚠️ Takraav:** Chunk size par farak: Melvynx 1-3 words per chunk, kmilo 1-5 words per page — dono chalte hain, ek channel par ek hi style consistent rakho

### A-035 · Safe zones: text platform UI se bahar 🟡
- **Kab:** 9:16 video me text, captions ya CTA rakhte waqt
- **Kya:** Text aur key visuals platform UI bands ke bahar rakho. Universal 9:16 zone: x 9-91%, y 14-86%; hook text y 15-22%; captions/CTA y 78% se neeche nahi; right 14% me kuch zaroori nahi. Pixel hisaab (1080x1920, mktkit): IG/FB top 270 bottom 672, TikTok top 130 bottom 484, Shorts top 180 bottom 350 — kai platforms ke liye sabse sakht intersection lo aur caption MarginV = strictest bottom + 24 px. 1:1/16:9 me text beech ke 80% me rakho
- **Kyun:** UI ke neeche dabaa text padha hi nahi jata — ye retention nahi, seedha samajh ka nuksaan hai
- **Kitni baar / limits:** Har text placement par; check number se karo (text safe jab y ≥14, y+h ≤79, x+w ≤86)
- **Evidence:** 🟡 — mktkit ke specs Meta/TikTok sourced (platform specs); ExpoCut ke % vendor-measured (Free to use and redistribute with attribution to expocut.com); Melvynx ke px zones house-measured
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "safe_zone_pct", "x_min": 9, "x_max": 91, "y_min": 14, "y_max": 79}`
- **⚠️ Takraav:** Sources ke numbers format aur platform ke hisaab se alag hain: Melvynx px (top 220, bottom 420, right 140 from y900) ExpoCut ke % aur mktkit ke px se thode alag hain — target platforms ka sakht intersection hi surakshit raasta hai

### A-036 · Phone par padhai: size aur contrast 🟡
- **Kab:** Koi text screen par aaye to
- **Kya:** Body text 1080p par ≥40-60 px uncha rakho; contrast ≥4.5:1; video ke upar text ko solid/scrim card ya outline do; label fit karne ke liye font chhota mat karo — label ke shabd chhote karo
- **Kyun:** Chhota ya halka text phone par gayab ho jata hai; jo padha na jaye woh information nahi, shor hai
- **Kitni baar / limits:** Har text par; Melvynx ke floors: UI detail ≥34 px, labels 38-42 px, captions ~84 px
- **Evidence:** 🟡 — WCAG AA contrast 4.5:1 (WebAIM standard) + legibility.info; px floors creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`
- **Machine check:** `{"kind": "min_font_px", "what": "body_text_at_1080p", "value": 40}`

### A-037 · Boards illustrate karein, paraphrase nahi 🟠
- **Kab:** Short me board/visual element lagate waqt
- **Kya:** Board sirf woh dikhaye jo dikhaya ja sakta hai: number, command, folder, asli logo, before/after, asli screen; bola hua paraphrase karke board mat banao; board par 2-4 shabd se zyada text nahi; teen text-board lagatar nahi; har board theek us shabd par land kare jo use naam de
- **Kyun:** Jo board baat ko dohraata hai woh screen bharta hai, samajh nahi; jo dikhata hai woh baat ko pakka karta hai
- **Kitni baar / limits:** Har board par
- **Evidence:** 🟠 — Melvynx short-editing style.md ka house rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-038 · Tutorial me screen lead kare, voice follow 🟠
- **Kab:** Screen tutorial edit karte waqt
- **Kya:** Screen jo dikhaye voice wahi kahe, usi pal: phrase tab aaye jab uska action screen par ho; phrase action se lambi ho to result ko usi second par freeze karo; clip kabhi peeche na jaye, na kisi chhode hue clip par wapas aaye
- **Kyun:** Shabd aur tasveer ka saath (temporal contiguity) hi tutorial ko follow karne layak banata hai; aage-peeche hona sabse bada confusion hai
- **Kitni baar / limits:** Tutorial ki har phrase par
- **Evidence:** 🟠 — kmilo house rule (reference tutorial review se); peeche Mayer ka temporal contiguity principle (🟢) khada hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-039 · Tutorial chapter cards aur edge badge 🟠
- **Kab:** Tutorial ke chapter badlein to
- **Kya:** Har chapter 3 s ke title card se khule ('Step 2 of 5'), card ka content 0.55 s me enter kare; screen par step ke naam ka edge badge rakho taaki beech me land karne wale ko jagah samajh aaye; chapter ke andar hard cuts hi rakho
- **Kyun:** Tutorial viewers hisse dohraate aur jump karte hain; bade, saaf markers unhe sahi jagah pahunchaate hain
- **Kitni baar / limits:** Har chapter par
- **Evidence:** 🟠 — kmilo house rule; Guo 2014 (🟡) ka bade-text-at-transitions wala support
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "duration_range_s", "what": "chapter_title_card", "min": 3, "max": 3}`

### A-040 · Lower third pehli pehchan par 🟠
- **Kab:** Podcast/interview me koi vyakti pehli baar dikhe to
- **Kya:** Us vyakti ka naam aur role lower third me dikhao, aur lambe break ke baad dobara dikhao
- **Kyun:** Bina pehchan ke viewer baat ko sahi insaan se jod nahi pata
- **Kitni baar / limits:** Har naye speaker ki pehli appearance par
- **Evidence:** 🟠 — kmilo podcast recipe ka creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-041 · Auto captions review zaroor karo 🟡
- **Kab:** Publish se pehle captions finalize karte waqt
- **Kya:** YouTube ke auto captions ko bina review publish mat karo (accent, dialect, background noise se woh speech ko galat dikha sakte hain) — caption file upload karo ya auto wali sudharo; burned-in ho to word-by-word check karo; numbers hamesha video se verify karo
- **Kyun:** Galat caption samajh ko ulta kar deta hai, aur burn ho jaye to galti permanent dikhti hai
- **Kitni baar / limits:** Har video, publish se pehle
- **Evidence:** 🟡 — YouTube official auto-caption warning (platform) + Melvynx clips ki practical chetaavni
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-042 · Music awaaz se 18-25 dB neeche 🟠
- **Kab:** Bolne ke neeche music lage to
- **Kya:** Background music ko voice se 18-25 dB neeche rakho (voice -16 LUFS ho to music lagbhag -34/-41 LUFS)
- **Kyun:** Awaaz se ladta music seedha samajh khatm karta hai — viewer shabd pakadne me thakta hai
- **Kitni baar / limits:** Jahan bhi speech ke neeche music hai
- **Evidence:** 🟠 — Creator source (Pure Audio Insight) kmilo ki tagging me; koi peer-reviewed number nahi
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "db_range", "field": "music_db_under_voice", "min": 18, "max": 25}`
- **⚠️ Takraav:** Melvynx ke measured style-copy me ek creator ka beat ~12 dB under naapa gaya tha — woh us style ka naapa hua apvaad hai; aam niyam 18-25 dB hi hai, copy karna ho to original ko naapo (dekho A-091)

### A-043 · Ducking: bolte waqt music 6-12 dB dabao 🟠
- **Kab:** Speech ke neeche music chale to
- **Kya:** Jab koi bole to music ko 6-12 dB duck karo — soft attack 10-50 ms, release 250-700 ms (sidechain compressor, auto-ducking ya keyframes se); Melvynx ke mix defaults: bed -28 LUFS, duck ratio 0.5
- **Kyun:** Ducking se music rehta bhi hai aur shabd saaf bhi rehte hain; bina duck ke ya to music gayab ya awaaz dabti hai
- **Kitni baar / limits:** Poore talking hisse par
- **Evidence:** 🟠 — Creator sources (Zella; Auphonic ka official default 18 dB apne tool ke liye hai — isiliye range 6-12 creator wali rakhi)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-044 · SFX ke level aur jagah ke niyam 🟠
- **Kab:** Sound effect lagate waqt
- **Kya:** SFX voice se 12-24 dB neeche rakho; effect ka transient visual change se 2-4 frames pehle rakho taaki peak dikhne ke pal mile; key word (number, naam) ke upar effect kabhi nahi; ek hi sound lagatar 3 baar se zyada nahi; jo awaaz asal recording me pehle se kaam kar rahi hai (real click, darwaza) us par effect mat chadhao; gain ke default andaze: SFX ~15 dB, ambience ~30 dB under
- **Kyun:** Galat jagah ya zyada tez effect shabd ko kha jata hai; sahi jagah wala effect dikhne wali cheez ko pakka karta hai
- **Kitni baar / limits:** Har effect par
- **Evidence:** 🟠 — Creator sources (Storyblocks) + kmilo library ke house defaults
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-045 · Master loudness destination ke hisaab se 🟡
- **Kab:** Final master banate waqt
- **Kya:** Ek hi master, destination ke target par, naap kar (guess nahi): YouTube ke liye -14 LUFS integrated, true peak ≤-1 dBTP; podcast feed ke liye -16 LKFS ±1; dono jagah jana ho to do masters banao; loudnorm two-pass lagao (pehle measure, phir linear apply)
- **Kyun:** Zyada loud ghusane se kuch nahi milta (platform neeche kar dega), bahut kam rakho to padosi videos se halka sunai dega
- **Kitni baar / limits:** Har export par ek master; mktkit apni pipeline me -16 LUFS / -1.5 dBTP / LRA 11 rakhta hai
- **Evidence:** 🟡 — Apple Podcasts official spec + YouTube ke measured normalization behaviour + EBU R128 references — platform specs
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_1610-advisory_mktkit.md`
- **Machine check:** `{"kind": "lufs_target", "value": -14, "tolerance": 1}`
- **⚠️ Takraav:** YouTube target -14 LUFS (kmilo/Melvynx) vs mktkit ka house master -16 LUFS: dono apni jagah sahi hain — mktkit ka tark hai ki -16 wala master platform ke ~-14 normalization par bina limiting artifacts ke pahunchta hai; jo pipeline chuno, ek hi target rakho

### A-046 · Room tone har gap ke neeche 🟠
- **Kab:** Recording aur edit dono par
- **Kya:** Har location par 30-60 s ka room tone record karo; edit me har cut-gap ke neeche wahi bichao — awaaz kabhi digital silence par na gire; room tone na ho to recording ke sabse saaf khaali hisse se copy karo
- **Kyun:** Digital silence dropout jaisi lagti hai aur har cut par background ka jump sunai deta hai
- **Kitni baar / limits:** Har location, har gap
- **Evidence:** 🟠 — Creator source (StudioBinder) — kmilo ki tagging me creator
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-047 · Dialogue saaf karne ka kram 🟠
- **Kab:** Voice/dialogue clean karte waqt
- **Kya:** Isi kram me chalo: sabse achha source/mic chuno (jo na bole uske mics mute) → halki noise reduction → high-pass ~80 Hz → EQ (clarity) → compression → de-esser (zarurat ho to) → har clip ka level barabar → aakhir me ek master; har breath mat hatao, awaaz robotic ho jati hai
- **Kyun:** Har kadam pichle ke output par behtar kaam karta hai; ulta kram artefacts banata hai
- **Kitni baar / limits:** Har video ki dialogue processing par
- **Evidence:** 🟠 — Creator practice (kmilo audio reference)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-048 · Gain andaze se nahi, formula se 🟠
- **Kab:** Kisi sound ko voice ke neeche set karte waqt
- **Kya:** Gain hamesha naap kar nikalo: gain = 10^((voice_lufs − under − sound_lufs)/20), cap 1 par; 'under' ke defaults — SFX 15 dB, music ~20 dB, ambience/room tone ~30 dB; gain 1 se upar aaye to woh sound us kaam ke liye halka hai, dusra chuno, amplify mat karo
- **Kyun:** Andaze wale levels har video me badalte rehte hain; formula har baar wahi rishta deta hai
- **Kitni baar / limits:** Har sound placement par
- **Evidence:** 🟠 — kmilo house method (library ke measured catalog par chalta hai)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-049 · Podcast mics: jo na bole uska band 🟠
- **Kab:** Multicam podcast/interview edit karte waqt
- **Kya:** Jo vyakti nahi bol raha uska mic mute ya gate karo (dusri awaaz late pakad kar echo/phasing na bane); sab speakers ka level ek barabar rakho; music sirf intro, outro aur topic breaks me rakho, baat-cheet ke neeche nahi
- **Kyun:** Khule mics ka echo aur alag-alag levels hi podcast ko sabse zyada 'amateur' sunate hain
- **Kitni baar / limits:** Poore episode par
- **Evidence:** 🟠 — kmilo podcast recipe ka creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-050 · Join fades: cut par click na aaye 🟠
- **Kab:** Talking spine ke segments judte hon to
- **Kya:** Har kept segment ke join par 0.05-0.08 s ka audio fade rakho
- **Kyun:** Bina fade ke range joins click karte hain — chhoti awaaz, lekin har cut par sunne wale ko khichti hai
- **Kitni baar / limits:** Har join par
- **Evidence:** 🟠 — mktkit cut-video engine ka rule (reviewer catches se bana)
- **Sources:** `github_1610-advisory_mktkit.md`
- **Machine check:** `{"kind": "duration_range_s", "what": "join_fade", "min": 0.05, "max": 0.08}`

## RHYTHM — timing, pacing, cadence

### A-051 · Visual change ki cadence (short-form) 🟠
- **Kab:** Short-form (TikTok/Reels/Shorts) edit karte waqt
- **Kya:** Har kuch seconds me screen par kuch badal ho — baseline: 5 s ke andar kam se kam ek visual change (cut, punch-in, overlay, B-roll, text swap); ExpoCut ki kasauti: koi bhi 5 s ka window bina change ke = swipe risk
- **Kyun:** Short-form me rukti hui screen hi swipe ka sabse seedha karan hai
- **Kitni baar / limits:** Pacing offsets: Melvynx har 2-4 s, ExpoCut har 3-5 s, mktkit har 3-7 s (pehle 5 s me aur tight), trend/entertainment me cuts 0.5-1 s
- **Evidence:** 🟠 — Teeno sources creator playbook/house numbers hain (Free to use and redistribute with attribution to expocut.com — ExpoCut ka hissa)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "max_visual_gap_s", "value": 5}`
- **⚠️ Takraav:** Cadence ke numbers sources me alag hain — Melvynx 2-4 s, ExpoCut 3-5 s, mktkit 3-7 s; content type faisla kare (samjhane wala dheema, entertainment tez), lekin 5 s se upar kahin bharosa nahi

### A-052 · Film se pacing ka benchmark 🟢
- **Kab:** Kisi bhi format ka shot length sochte waqt
- **Kya:** Reference rakho: aaj ki filmein ~4-5 s average shot length par chalti hain; dialogue wale hisse isse lambe, action wale chhote; apne format ka pacing isi ke aas-paas napo, usse bad-zada tez mat karo
- **Kyun:** Ye das saal ke data ka pattern hai — viewer's aankh is cadence ki aadi hai
- **Kitni baar / limits:** Sirf benchmark; koi sakht target nahi
- **Evidence:** 🟢 — James Cutting (2011) — peer-reviewed film data (kmilo me 'study / official' tag)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **⚠️ Takraav:** Ye film ka naapa hua average hai, short-form ke liye target nahi — wahan cadence A-051 wali hi chalegi

### A-053 · Type ke hisaab se shot lambaai 🟠
- **Kab:** Har segment ka shot length tay karte waqt
- **Kya:** Talking head: 2-5 s per shot; verticals: 2-3 s per shot, 4 s se upar kabhi nahi, aur text wala shot kam se kam ~2 s; tutorial: shot ≥5 s; vlog: clock se nahi, event ke hisaab se kato (ek kaam = ek block)
- **Kyun:** Har format ki samajh-gati alag hai — tutorial ko sochne ka samay chahiye, vertical ko nahi
- **Kitni baar / limits:** Har shot par
- **Evidence:** 🟠 — kmilo creator reference (type-wise shot lengths)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-054 · Explainer ke pattern interrupts 🟠
- **Kab:** Lambe explainer/talking video me dhyaan bachana ho to
- **Kya:** Pehla pattern interrupt (angle, B-roll, graphic, zoom) 25-35 s ke andar laao, phir har 2-3 minute me ek; micro-hook (caption, question, tease) isse ghana rakho
- **Kyun:** Bina badlaav ke dhyaan sabse tez yahi girta hai — interrupt ek nayi shuruaat jaisa kaam karta hai
- **Kitni baar / limits:** Pehla ≤35 s par; phir 2-3 min ke antar par; micro-hook har 30-90 s
- **Evidence:** 🟠 — Creator source (air.io) kmilo me; micro-hook ke numbers TubeBuddy/vidIQ ke alag-alag reports hain
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **⚠️ Takraav:** Micro-hook interval par sources aapas me takrate hain — TubeBuddy 30-60 s kehta hai, vidIQ 60-90 s; dono creator reports hain, koi pakka number nahi

### A-055 · Phrases ke beech ka gap 🟠
- **Kab:** Dead air/silence hatate waqt
- **Kya:** Phrase gaps type ke hisaab se rakho: talking head 200-400 ms, Shorts 200-300 ms, tutorial ≥0.4 s (3 s bina voice = warning, 6 s = hard cap jab tak screen khud na samjhaye); saans ki jagah puri tarah zero mat karo — gap hamesha kuch rakho
- **Kyun:** Saans hi bolne ko insaani banati hai; gap type ke samajh-waqt ke barabar ho to edit natural lagta hai
- **Kitni baar / limits:** Har phrase boundary par
- **Evidence:** 🟠 — Creator/house numbers teeno sources se (kmilo, Melvynx pauses.json defaults, mktkit engine defaults)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_1610-advisory_mktkit.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Machine check:** `{"kind": "gap_range_ms", "what": "phrase_gap_talking_head", "min": 200, "max": 400}`
- **⚠️ Takraav:** Numbers style ke hisaab se bahut alag hain: Melvynx ka super-fast style sirf 30-80 ms saans rakhta hai (sentence .08, comma .05, word .03); mktkit engine defaults talking 0.40 s, manifest 0.85 s; ExpoCut silence removal me min gap 450-500 ms + 80 ms padding (Free to use and redistribute with attribution to expocut.com) — ek channel par ek style pakdo

### A-056 · Har cut ke paas reason ho 🟠
- **Kab:** Koi cut lagane se pehle
- **Kya:** Cut tabhi jab woh ek kaam kare: (1) dead time hataye, (2) information badle, ya (3) action ko follow kare; word ke beech me cut kabhi nahi
- **Kyun:** Bina reason ke cut viewer ko jhatka deta hai; reason wala cut dikhai hi nahi deta
- **Kitni baar / limits:** Har cut par
- **Evidence:** 🟠 — kmilo house rule (yeh editor test); YouTube official bhi 'cuts that do not serve a purpose confuse viewers' kehta hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-057 · Cut on action 🟠
- **Kab:** Movement ke beech cut aaye to
- **Kya:** Cut ko khud movement par rakho (darwaza khulna, haath uthna) — movement cut ko dhak deta hai; gesture ya blink ke beech me cut mat karo; classic tareeka: aankhon par ya sentence par cut
- **Kyun:** Aankh movement ko follow karti hai, isliye wahan cut chhup jata hai
- **Kitni baar / limits:** Har action cut par
- **Evidence:** 🟠 — kmilo editing reference ka creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-058 · J/L cuts scene badlaav naram karne ke liye 🟠
- **Kab:** Scene ya speaker badle aur transition kathin lage to
- **Kya:** Agli awaaz ko tasveer se pehle aane do (J cut) ya pichli awaaz ko tasveer badalne ke baad rehne do (L cut); offset kuch frames se ~2 s tak; tutorial me inka istemal kam
- **Kyun:** Awaaz ka nirantar flow scene ka badlaav mehsoos hi nahi hone deta
- **Kitni baar / limits:** Scene/speaker changes par zarurat ke hisaab se
- **Evidence:** 🟠 — Creator source (TechSmith) — offset ke liye koi pakka number source nahi deta
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-059 · Jump cuts ka sahi istemal 🟡
- **Kab:** Single-camera talking head se filler hatana ho to
- **Kya:** Jump cuts hi sahi tareeka hain; inhe naram karne ke liye alternate cut par punch-in ya B-roll cover lagao; interview/multicam me jab asli angle maujood hai to jump cut kabhi nahi; subject ko mid-gesture me pakde hue mat chhodo
- **Kyun:** YouTube khud tight talking head ke liye jump cuts ki salah deta hai; bina cover ke lagatar jump cuts kathin lagte hain
- **Kitni baar / limits:** Har take me filler positions par
- **Evidence:** 🟡 — YouTube official recommendation (platform) + kmilo creator refinements
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-060 · Pacing varied rakho, metronome nahi 🟠
- **Kab:** Poori edit ka rhythm banate waqt
- **Kya:** Tez hisso ke baad wohi lamba hold rakho jahan key point land karta hai; ek hi scene ke andar bhi sabse dheemi animation sabse tez ki ~3 guna ho sakti hai; har cheez ko ek hi gati par mat chalao
- **Kyun:** Ek-si gati thoda samay baad sunai/dikhai dena band ho jati hai; contrast hi dhyaan banata hai
- **Kitni baar / limits:** Har section par
- **Evidence:** 🟠 — kmilo creator rules + motion-principles reference
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-061 · Cuts music ki phrase par 🟠
- **Kab:** Music ke saath edit karte waqt
- **Kya:** Cuts aur loops music ki phrases par rakho, mid-note par nahi; video ka ant music ke asli ending ya saaf fade par ho; foreground music (music video/promo) me key cuts downbeat par rakho; music-led video me cuts beats par rakho
- **Kyun:** Phrase ke beech kata music bina bole hi galat lagta hai; phrase par kata hua mehsoos hi nahi hota
- **Kitni baar / limits:** Music wale har section par
- **Evidence:** 🟠 — Creator practice (kmilo music reference; ExpoCut ke music-beat cuts iske saath — Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_expocut_claude-plugin_retention-playbook.md`

### A-062 · Punch ki hadd: lambaai, doori, ginti 🟠
- **Kab:** Talking reel me visual punch (clip/still/board/super) lagate waqt
- **Kya:** Clip punch <3.0 s rakho (zyada lamba = woh cutaway ho gaya); still punch 3.5 s; super wala segment 3.5-4.0 s; do punches ke beech A-roll ≥3.0 s rakho, warna punches ko butt karo; punches ≤10/min; stills ≤2 per reel aur lagatar kabhi nahi; still apne noun ke 0.3 s ke andar shuru ho, clip punch ki window 0.8 s
- **Kyun:** Bina hadd ke punches poori reel ko shor bana dete hain aur punch ka matlab hi khatm ho jata hai
- **Kitni baar / limits:** Har reel par (yeh mktkit ke QA gates se enforce hote hain)
- **Evidence:** 🟠 — mktkit owner/reviewer ke khade kiye hue rules (asal reviewer catches se bane)
- **Sources:** `github_1610-advisory_mktkit.md`
- **Machine check:** `{"kind": "max_per_min", "what": "punch", "value": 10}`

### A-063 · B-roll ki ginti (paper-stage shorts) 🟠
- **Kab:** Short ke liye B-roll lagate waqt (Melvynx system)
- **Kya:** B-roll zyada se zyada har 8-15 s me ek, 2-5 s ka; do B-roll ke beech ~5 s creator screen par; clip tabhi jab image sentence se fit ho; achha hit na mile to board ya creator hi rakho, random clip kabhi nahi
- **Kyun:** Har doosri line par clip pura lagne ki jagah pura hi bekaar lagta hai; kam aur fit B-roll hi premium feel deta hai
- **Kitni baar / limits:** Har short par
- **Evidence:** 🟠 — Melvynx shorts broll house rules
- **Sources:** `github_Melvynx_video-agent-skills.md`
- **⚠️ Takraav:** mktkit ke punch system me punches 10/min (har ~6 s) tak ja sakte hain — woh talking-reel ka alag system hai; ye 8-15 s wali cadence paper-stage shorts ki hai; format ke hisaab se chuno, dono ko mat milao

### A-064 · Retakes aur false starts hatao 🟠
- **Kab:** Talking footage ki pehli safaai karte waqt
- **Kya:** Har line ka aakhra complete attempt rakho; false starts, half-words, 'uh', off-script awaazein ('wait, redo that') drop karo; chhupe retake ke nishan pehchano: 0.6 s se lamba koi shabd, bola hua phrase dohraaya, ya be-matlab shabd
- **Kyun:** Retake wali gandagi hi raw footage ko amateur banati hai; saaf spine ke bina koi style kaam nahi karta
- **Kitni baar / limits:** Har take par, style se pehle
- **Evidence:** 🟠 — Melvynx script-first pipeline ka house rule + kmilo retake rules
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`

### A-065 · Podcast me camera jo bole us par 🟠
- **Kab:** Multicam podcast/interview cut karte waqt
- **Kya:** Jo bol raha hai uska close-up rakho; speaker badle to badlaav ke ek beat baad cut karo; reaction shot sirf tab jab woh kuch kahe; wide shot shuruaat, topic change aur cross-talk ke liye rakho; timer par angle kabhi mat badlo; lambi monologue me close/medium/wide ya punch-in ghumao
- **Kyun:** Camera speaker ko follow kare to baat-cheet dekhna aasan hota hai; timer wale cuts nakli lagte hain
- **Kitni baar / limits:** Poore episode par; koi pakki frequency nahi — speaker changes hi trigger hain
- **Evidence:** 🟠 — kmilo podcast recipe; source khud kehta hai iske liye koi authoritative frequency number nahi hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-066 · Hard-out hamesha shabd ke end par 🟠
- **Kab:** Clip ya reel ka ant tay karte waqt
- **Kya:** Video ka end hamesha aakhri rakhe hue shabd ke END par rakho; ant kabhi SRT cue ke end se mat nikalo (wah aadha sentence late ho sakta hai)
- **Kyun:** Cue timing aur asli awaaz ka end alag hote hain — galat ant par video latka hua ya kata hua lagta hai
- **Kitni baar / limits:** Har edit ke ant par
- **Evidence:** 🟠 — mktkit cut-video engine ka rule (asal defect se bana)
- **Sources:** `github_1610-advisory_mktkit.md`

### A-067 · Tutorial shots aur speed 🟠
- **Kab:** Tutorial edit karte waqt
- **Kya:** Shots ≥5 s rakho; navigation, clicks aur results 1x par; typing zyada se zyada 1.5x; dead time ko speed se nahi, clean cut se hatao; app ki apni animation (modal khulna, loading) ke beech cut mat karo; form kabhi screen par kata hua mat dikhao (submit sirf clicked state me)
- **Kyun:** Tutorial ka kaam follow karwana hai — tez ya kata hua step viewer ko kho deta hai
- **Kitni baar / limits:** Har tutorial shot par
- **Evidence:** 🟠 — kmilo house rules (reference tutorial review se)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-068 · Bolne ki gati type ke hisaab se 🟠
- **Kab:** Script ki lambaai aur pace tay karte waqt
- **Kya:** Technical/tutorial narration 120-150 wpm rakho; short script ka default pace ~160 wpm; script ki lambaai shabdo ki ginti ko pace se bhaag de kar napo (bole hue runtime ke hisaab se likho)
- **Kyun:** Gati hi samajh ka samay deti hai; tez script bechne me bhi aur samjhane me bhi haarti hai
- **Kitni baar / limits:** Har script par
- **Evidence:** 🟠 — Creator practice (kmilo pacing + Melvynx script-length defaults)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-069 · Short ki lambaai ke targets 🟠
- **Kab:** Short-form video ki lambaai tay karte waqt
- **Kya:** Targets rakho lekin idea ko lambaai tay karne do, platform ki max ko nahi: TikTok entertainment 21-34 s (educational 60-90 s), Shorts 15-30 s, Reels 7-15 s punchy ya 30-60 s value; Melvynx ke naape hue hits 25-40 s aur 30-60 s aam range hai, 45 s se neeche completion behtar
- **Kyun:** Jo lambaai idea se zyada hai woh completion% gira kar video ko dabati hai
- **Kitni baar / limits:** Har short par
- **Evidence:** 🟠 — Creator guidance (ExpoCut playbook — Free to use and redistribute with attribution to expocut.com; Melvynx ke measured ranges)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`

### A-070 · Lambe content ko 6 min ke blocks me baanto 🟡
- **Kab:** Lamba educational content banate waqt
- **Kya:** Content ko 6 minute se chhote blocks/chapters me baanto; lambi process ho to ek step = ek video rakho
- **Kyun:** Measured data (6.9M sessions) me 6 minute ke baad engagement girna shuru hota hai — chhote blocks wale videos zyada dekhe jate hain
- **Kitni baar / limits:** Har lambe video ki planning par
- **Evidence:** 🟡 — Guo et al. 2014 — edX ke 6.9 million sessions ka measured study
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-071 · Verify loop: dikhane se pehle filmstrip check 🟠
- **Kab:** Render ya delivery se pehle
- **Kya:** Poori video ko filmstrip/contact sheet par check karo: pehle 3 s (hook frame 0 par padh sakte ho?), poori lambaai (koi 5 s window bina change ke to nahi?), text ke safe-zone numbers (y ≥14, y+h ≤79, x+w ≤86); mktkit ka machine QA gate pass karo; render se pehle stills par iterate karo — stills seconds me bante hain, renders minutes me
- **Kyun:** Jo galti sheet par dikh jati hai woh publish ke baad pakadne se sasti padti hai; aadha kaam yahi pakda jata hai
- **Kitni baar / limits:** Har render/delivery par
- **Evidence:** 🟠 — Teeno sources ke house QA workflows (ExpoCut SVR loop — Free to use and redistribute with attribution to expocut.com; mktkit gate; Melvynx stills rule)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`

## STYLE — look, effect, sajawat

### A-072 · Punch-in sirf motivated, hadd ke andar 🟠
- **Kab:** Talking video me zoom/punch-in lagane se pehle
- **Kya:** Zoom sirf us detail, reaction ya usi line par rakho jis par voice baat kar rahi hai; talking-head punch-in ka scale 110-120% rakho (source resolution ke andar hi, soft frame crop nahi); Melvynx ke naape hue limits: punch-in har ~4 s se zyada baar nahi, ≤1.15x, agle cut tak hold, ek hi shot me in aur out dono nahi; zoom cut ko kabhi cross na kare; screencast me do zooms ke beech 5-7 s ka gap
- **Kyun:** Bina wajah ka zoom sabse pehchani jaane wali amatuer harkat hai; wajah wala zoom dhyaan ko sahi jagah le jata hai
- **Kitni baar / limits:** Har punch-in par
- **Evidence:** 🟠 — Creator practice (kmilo; Envision ke screencast numbers) + Melvynx measured style-copy ke exact numbers
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Machine check:** `{"kind": "min_gap_s", "what": "punch_in", "value": 4}`
- **⚠️ Takraav:** ExpoCut cadence ke saath har 2nd ya 3rd cut par punch-in ki salah deta hai (Free to use and redistribute with attribution to expocut.com) — ye kmilo/Melvynx ke 'sirf motivated' niyam se takrata hai; entertainment short me cadence wali chal sakti hai, samjhane wale content me motivated wali hi surakshit hai

### A-073 · Snap punch-in ki technique 🟠
- **Kab:** Punch-in lagate waqt (ExpoCut tareeka)
- **Kya:** Zoom ko ramp mat karo — do hold keyframes lagao (jaise scale 1.0 se 1.1), cut par alternate karo; agar settle chahiye to easeOut key rakho aur 400 ms baad scale 1.0 wapas karo
- **Kyun:** Ramp wala zoom dheere-dheere ghista hua lagta hai; snap cut jaisa saaf lagta hai
- **Kitni baar / limits:** ExpoCut style wale har punch-in par
- **Evidence:** 🟠 — ExpoCut playbook ki technique (Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`

### A-074 · Entrances aur exits ki timing 🟠
- **Kab:** Koi element screen par aaye ya jaye to
- **Kya:** Cards/headlines 0.35-0.6 s ease-out me enter karein (bounce nahi), rows 0.3 s; exit hamesha entrance se chhota (0.25 s); elements 20-40 px offset aur opacity ke saath slide-in karein; Melvynx ka niyam: exit entrance se chhota rakho (.26 s smoothstep), theek 0 par khatm karo — spring wala exit ghost chhodta hai; springs kabhi overshoot na karein
- **Kyun:** Yahi chhoti timings 'professional' aur 'PPT jaisa' ke beech ka farak hain
- **Kitni baar / limits:** Har animated element par
- **Evidence:** 🟠 — kmilo motion reference (Material Design ke UI numbers 225/195 ms sirf reference ke roop me) + Melvynx reads ke measured exits
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-075 · Bounce, elastic aur emoji nahi 🟠
- **Kab:** Animation style ya visual language chunte waqt
- **Kya:** Serious content par bounce/elastic easing kabhi nahi (sirf halka overshoot promotional CTA par chal sakta hai); ye bilkul mat use karo: pulse, bounce, elastic, overshoot, glow, shake, spin, confetti; beat ko emoji se illustrate mat karo — motion design, asal logo ya typography use karo
- **Kyun:** Ye effects video ko sasta aur baccho jaisa dikhate hain; ek forbidden cheez poora premium feel tod deti hai
- **Kitni baar / limits:** Har project par (style system me band)
- **Evidence:** 🟠 — kmilo forbidden list + Melvynx motion rules — dono house style
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-076 · Ek moment, ek hi accent color 🟠
- **Kab:** Board ya graphic design karte waqt
- **Kya:** Kisi ek pal me screen par sirf ek accent color rakho; dusra accent kabhi na aaye
- **Kyun:** Do accents ek saath ladte hain aur design ka focus khatm ho jata hai
- **Kitni baar / limits:** Har frame par
- **Evidence:** 🟠 — Melvynx design system ka rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-077 · Har beat action, khadi tasveer nahi 🟠
- **Kab:** Koi beat banate waqt
- **Kya:** Har beat kuch karta hua ho — screenshot, still illustration, akela logo ya text card screen par 'baitha' rahe to woh beat redo hai; screenshot sirf reference hai — UI ko recreate karke animate karo
- **Kyun:** Ruki hui screen hi short ko marta hai; action hi premium motion ka ehsaas deta hai
- **Kitni baar / limits:** Har beat par
- **Evidence:** 🟠 — Melvynx short-editing style.md ka rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-078 · Hero then place; ek idea ek tableau 🟠
- **Kab:** Naya object screen par laate waqt
- **Kya:** Naya object pehle bada aur center me dikhao (scale 1.3-1.7), phir apni jagah (slot) me glide karo, aur agla item aane se pehle use land kar do; ek idea ke saare sentences ek hi tableau par badhte rahein — board har 1.5-2.5 s tabhi badlo jab speech ka idea badle; board ≥3 s hold ho to .025 ka slow push-in rakho
- **Kyun:** Bade pehle dikhne se aankh samajhti hai kya aa raha hai; tableau badalte rehne se viewer har baar nayi jagah seekhta hai
- **Kitni baar / limits:** Har naye object/idea par
- **Evidence:** 🟠 — Melvynx style.md hero-then-place aur tableau rules
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-079 · Asli logos hi, nakli kabhi nahi 🟠
- **Kab:** Screen par kisi tool/product ka naam aaye to
- **Kya:** Us tool ka asal logo/icon rakho (press kit, App Store listing ya official site se); letter glyph, emoji ya look-alike kabhi nahi; logo na mile to creator se file mango, khud mat banao
- **Kyun:** Nakli logo ek jhalak me pakda jata hai aur poori video ki credibility gira deta hai
- **Kitni baar / limits:** Har naam ke saath
- **Evidence:** 🟠 — Melvynx style.md logo rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-080 · Layout teen tarah ka ghumao 🟠
- **Kab:** Short ka layout banate waqt
- **Kya:** Teen views ghumao: split (paper/board upar, camera neeche — aam), paper-only (bada moment: key number ya screen), full camera (story, emotion, punchline, CTA — ≥5 s ke stretches); proof (paper) aur face (full camera) ko alternate karo taaki aankh ko aaram mile
- **Kyun:** Ek hi layout poori video me monotonous lagta hai; layout ka badlaav hi bina effect ke variety deta hai
- **Kitni baar / limits:** Har short par
- **Evidence:** 🟠 — Melvynx edit skill ke teen layouts
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-081 · Hook ka visual ek mini-story ho 🟠
- **Kab:** Hook ka visual design karte waqt
- **Kya:** Hook ka visual 2-3 acts ki mini-story ho — reversal ke saath, kai layers saath move karein, har keyword par impact (stamp + thud) aaye, aur payoff badge ki tarah land kare; ek object rakh kar use slide kar dena kaafi nahi
- **Kyun:** Hook ka visual hi pehle 2 s me 'ye alag hai' ka saboot hai; sust visual vaade ko khokhla kar deta hai
- **Kitni baar / limits:** Har hook par
- **Evidence:** 🟠 — Melvynx hook-design reference (house craft)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-082 · Music bed emotion se chuno, dohrao mat 🟠
- **Kab:** Short ke liye music bed chunte waqt
- **Kya:** Bed ko hook ke emotion se chuno; busy ya dynamic track voice ke neeche kabhi mat rakho (aise tracks test me reject ho chuke hain); pichle short me use hua bed is short me dobara mat use karo
- **Kyun:** Galat bed poori video ka mood ulta kar deta hai, aur dohraaya bed 'wahi purana' ka ehsaas deta hai
- **Kitni baar / limits:** Har short par nayi bed chuno
- **Evidence:** 🟠 — Melvynx music defaults aur test-rejected tracks ka house record
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-083 · Music ka offset payoff par land karana 🟠
- **Kab:** Track ko timeline par rakhte waqt
- **Kya:** Bade payoff ko track ke kisi mazboot pal par land karana ho to offset = c − P rakho (jaise full section payoff par aaye, usse pehle 10-20 s ka break pocket ho); full-camera emotional line ke liye offset = brk − E; aam default: offset = a point (10 s ki intro skip, pulse frame 1 se); offset + lambaai kabhi track ke 'out' pal se aage na jaye
- **Kyun:** Track ka sabse mazboot pal video ke sabse mazboot pal par mile to dono ek dusre ko uthate hain
- **Kitni baar / limits:** Har track placement par
- **Evidence:** 🟠 — Melvynx edit plan ke music rules (reads se naape gaye a/b/brk/c points)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-084 · Movement shor nahi, sirf payoff hits 🟠
- **Kab:** Sound design/hits lagate waqt
- **Kya:** Thud sirf number land/die hone par, pop sirf asal arrival par rakho; ek aam short me music ke alawa 2-4 sounds hi rakho; entrance clicks, whooshes aur risers copy ya add mat karo (riser bhi shor hai — sirf hit bache); bundled hit gains: impact-boom −8 dB, zhhh −6 dB, riser −12 dB (voice ke neeche)
- **Kyun:** Har harkat par awaaz lagane se awaaz ka matlab khatm ho jata hai; kam aur sahi jagah wale hits hi mehsoos hote hain
- **Kitni baar / limits:** Har short par 2-4 sounds (music se alag)
- **Evidence:** 🟠 — Melvynx style-steal learnings (galat copies ko reject karke bane house rules)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### A-085 · Color grade ka kram aur shot matching 🟠
- **Kab:** Color correction/grade karte waqt
- **Kya:** Isi kram me chalo: pehle normalize (log ko delivery color space me) → exposure scopes se set karo → white balance → scene ke saare shots ko hero shot se match karo (consistent grade hi sabse bada professional farak hai) → look/LUT aakhir me, sirf normalized footage par; skin tones ka red/green ka santulan mat bigado; screens aur graphics ko kabhi grade mat karo
- **Kyun:** Galat kram me grade karne se har shot alag lagta hai aur look footage ko tod deta hai
- **Kitni baar / limits:** Har project par
- **Evidence:** 🟠 — kmilo color reference (creator practice) + Melvynx grade system ka ek hi kram
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### A-086 · Transitions ke matlab 🟠
- **Kab:** Do shots ke beech transition chunte waqt
- **Kya:** Har transition ka apna matlab rakho: cut = nirantarta (continuity), dissolve = samay/jagah/topic ka badlaav, fade to black = ek block ka ant; Premiere ka default dissolve 1 s hai — use tabhi rakho jab badlaav asal me ho; flashy transitions (spin, glitch) har cut par kabhi nahi
- **Kyun:** Har cut par flashy transition dhyaan ko kahani se hata kar khud par le jata hai
- **Kitni baar / limits:** Har transition par
- **Evidence:** 🟠 — Creator source (StudioBinder) + Adobe official docs
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-087 · Thumbnail ke niyam 🟡
- **Kab:** YouTube thumbnail banate waqt
- **Kya:** File 1920×1080 JPG, 2 MB se kam; text 1-5 shabd (ideal 3-4) heavy sans-serif me, ~180 px par padh sakne wale; thumbnail title ko repeat na kare — use complement kare; ek hi dominant subject, 2-3 elements se zyada nahi; bottom-right corner khaali rakho (duration wahan aata hai); thumbnail jo vaada kare woh video ke pehle 30 s me milna chahiye
- **Kyun:** Mobile feed me thumbnail chhota dikhta hai — wahan padh sakne wala, ek-subject wala design hi click lata hai, aur jhootha vaada retention ko marta hai
- **Kitni baar / limits:** Har video par
- **Evidence:** 🟡 — YouTube official spec (1920×1080, <2 MB) + creator testing ke legibility numbers
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "max_words", "what": "thumbnail_text", "value": 5}`

### A-088 · Title ke niyam 🟡
- **Kab:** Video ka title likhte waqt
- **Kya:** Title 100 characters ke andar rakho, zaroori hissa pehle ~60 characters me; search video ke liye wohi shabd rakho jo log type karte hain, discovery video ke liye curiosity ya stakes pehle rakho; poora caps ya clickbait mat rakho
- **Kyun:** Lamba title feed me kat jata hai; galat iraade wala title galat viewer lata hai jo turant chala jata hai
- **Kitni baar / limits:** Har video par
- **Evidence:** 🟡 — YouTube official title limit (100 chars) + creator title-mapping practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Machine check:** `{"kind": "max_chars", "what": "title", "value": 100}`

### A-089 · Cover frame / title card 🟠
- **Kab:** Short/Reel ka cover banate waqt
- **Kya:** Cover par public-safe line ≤7 shabd me rakho (ExpoCut: frame 0 par padh sakne wala 3-5 shabd), center-anchored, ~2.0 s hold, 1-2 lines; Reels ke 1:1 center crop ke liye text x 22-78% ke andar rakho; cover frame video ke 0.3-0.4 s se render karo; test: cover dekh kar koi ajnabi topic bata sake
- **Kyun:** Cover hi grid me video ki pehchan hai — wahan se samajh na aaye to click bhi nahi aata
- **Kitni baar / limits:** Har short par
- **Evidence:** 🟠 — mktkit cover rules (public-safe gate) + ExpoCut frame-0 hook (Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_1610-advisory_mktkit.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Machine check:** `{"kind": "max_words", "what": "cover_title", "value": 7}`

### A-090 · Shorts reframe subject par rakho 🟠
- **Kab:** 16:9 footage ko vertical me badalte waqt
- **Kya:** Crop ko shot-by-shot subject par rakho — fixed center crop kabhi nahi; do speakers hon to dono ko sikoṛne ke bajaye unke beech cut karo ya stack karo; screen ya wide shot ka relevant hissa bada karke dikhao; clips nikalne ka plan ho to 4K me record karo
- **Kyun:** Center crop aksar subject ko hi kaat deta hai; subject-centered reframing hi vertical ko asal lagta hai
- **Kitni baar / limits:** Har reframed shot par
- **Evidence:** 🟠 — kmilo shorts recipe ka creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### A-091 · Style copy karna ho to pehle naapo 🟠
- **Kab:** Kisi creator ki editing style copy karne se pehle
- **Kya:** Pehle original ko naapo: cuts/sec (scene detection se), spectrogram se SFX aur hit ke pal, face screen ka kitna % hai, zoom jumps, music ki BPM aur voice ke neeche uski level — sirf frames dekh kar copy mat karo (wahan sound aur rhythm gayab rehte hain, aur copy isi liye nakli lagta hai); apne numbers original ke andar rakho (zyada jumps nahi, bada face nahi); result side-by-side compare karke hi dikhao
- **Kyun:** Do baar ki nakli copies (zyada zoom, bada face, har entrance par whoosh) isi sabak se bane rule hain — naap hi style ka asal DNA deti hai
- **Kitni baar / limits:** Har style-copy project se pehle
- **Evidence:** 🟠 — Melvynx steal skill ke learnings (rejected copies ke aadhar par)
- **Sources:** `github_Melvynx_video-agent-skills.md`
