# MASTER RULES — Step 2 (Parts A + B + C + Editor Round D1 + D2 ka unified sangrah)

Step 1 ke saare sources se nikale gaye editing rules, ek hi jagah, layer ke order me (Kahani > Samajh > Rhythm > Style/Effect). Har rule: kab lagana hai, kya karna hai, kyun, kitni baar (numbers ke saath), evidence tag, sources, aur ⚙️ nishan = machine se check ho sakta hai (check field rules.json me hai). Cross-cluster EXACT duplicates merge kiye gaye hain — unke part_ids do hain. **Editor round (Merge Round 2, 2026-11-06):** D1 (AE + Premiere, 96 rules) aur D2 (DaVinci + CapCut, 106 rules) ke 202 naye rules R-262 se R-463 tak jude hain — har naye rule ke heading me *(naya — editor round)* ka nishan hai; is round me koi naya EXACT duplicate nahi mila (0 merge). Editor round ke takraav CONFLICTS.md ke ADDENDUM me hain (faisla ORDER addendum me hoga). Numbers me farak wale takraav alag rakhe hain; unki list CONFLICTS.md me hai (faisla Step 3 ka hai).

> ⚠️ **ExpoCut attribution:** Free to use and redistribute with attribution to expocut.com — ExpoCut playbook (`github_expocut_claude-plugin_retention-playbook.md`) se aaye rules is shart ke saath use/redistribute hote hain.

**Evidence tags:** 🟢 = peer-reviewed research se sabit · 🟡 = measured corpus / platform data · 🟠 = creator/editor opinion ya house rule

## Summary

| Cheez | Ginti |
|---|---|
| **Kul rules (merge ke baad)** | **463** |
| Kul raw (A 91 + B 72 + C 103 = 266 · D1 96 + D2 106 = 202) | 468 |
| EXACT duplicates merge hue | 5 jode (saare Round 1 me; editor round me 0) |
| Layer: kahani | 113 |
| Layer: samajh | 79 |
| Layer: rhythm | 121 |
| Layer: style | 150 |
| Evidence 🟢 | 10 |
| Evidence 🟡 | 55 |
| Evidence 🟠 | 398 |
| ⚙️ Machine-checkable (check field hai) | 153 |
| Sirf insaan ki aankh/judgement | 310 |


---

## KAHANI — kahani aage badhe, vaada bache (sabse upar)

### R-001 — Vaada sabse pehle ⚙️
- **Purana ID:** A-001
- **Kab:** Har video ki shuruaat par
- **Kya:** Title/thumbnail jo vaada kare, wahi cheez pehle seconds me dikhao ya bolo — result, sabse striking moment, ya woh sawal jiska jawab video hai
- **Kyun:** Viewer pehle seconds me faisla karta hai; YouTube ka official lever hai ki thumbnail/title asal content ko reflect kare aur intro wahi dikhaye
- **Kitni baar:** Har video; long-form me pehle 5-30 s ke window me, Shorts me pehle frame/3 s me
- **Evidence:** 🟡 — YouTube official guidance (YT-moments, platform) + Melvynx ke measured outlier data; ExpoCut playbook bhi yahi kehta hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Check:** `{"kind": "hook_within_s", "value": 5}`

### R-002 — Intro, greeting, logo — hook se pehle kuch nahi
- **Purana ID:** A-002, C-021
- **Kab:** Kisi bhi video (long-form ya Short) ke opening seconds me
- **Kya:** Greeting ('Hey guys, welcome back'), channel intro, logo sting, subscribe pitch — kuch bhi hook se pehle mat rakho; pehli cheez viewer promise/payoff sune ya dekhe. Logo aaye to content ke upar card ki tarah aaye, alag shot me kabhi nahi
- **Kyun:** Pehle seconds vaade ke liye hain — greeting/intro unhi seconds ko khaali cheez par kharch karta hai jahan audience sabse zyada girti hai; subscribe pitch abhi earn hi nahi hua. Saare source clusters isey sabse aam opening galti mante hain
- **Kitni baar:** Har video ki shuruaat par, bina exception
- **Evidence:** 🟠 — Creator practice (TubeBuddy/TikTok blogs) + kmilo/Melvynx house rules + Jake/SkillMedev/serge ki shared craft rule; ExpoCut: 'never on an intro card' (Free to use and redistribute with attribution to expocut.com); koi measured study nahi
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`, `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`, `github_sergebulaev_youtube-skills.md`

### R-003 — Cold open = sabse mazboot moment
- **Purana ID:** A-003
- **Kab:** Video ki structure banate waqt
- **Kya:** Video ke best moment/line ko shuruaat me rakho (vlog ka best pal, podcast ki sabse mazboot exchange, tutorial ka end-state), phir context par wapas aao
- **Kyun:** Thanda, dheere chadhne wala start viewer ko rok nahi pata; best moment hi thumbnail ke vaade ko sach karta hai
- **Kitni baar:** Talking head 5-15 s, podcast 15-60 s, tutorial hook 10-20 s (end-state pehle)
- **Evidence:** 🟠 — Creator practice (TubeBuddy-hacks aadi) — kmilo recipes ka standing structure rule
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-004 — Hook formula se, score 7+ ka gate ⚙️
- **Purana ID:** A-004
- **Kab:** Har script likhte waqt
- **Kya:** 3 hooks 3 alag formulas se likho (22 formulas ki library: pain, claim, number, mistake, story, promise, curiosity, proof, reaction), har hook ko 5-point rubric (Specific, Tension, Viewer, Fast, True) par 0-2 score karo, best rakho; sab 7/10 se kam hon to 3 aur likho
- **Kyun:** Ek hi andaz ka hook aksar kamzor hota hai; teen vikalp + score se mazboot hook chunna aasan aur dohraane layak hota hai
- **Kitni baar:** Har script par 3 hooks; rakha hua hook ≥7/10
- **Evidence:** 🟠 — Melvynx studio-script ka creator system (rubric usi ka banaya hua, koi public data nahi)
- **Sources:** `github_Melvynx_video-agent-skills.md`
- **Check:** `{"kind": "min_score", "what": "hook_score", "value": 7, "scale": 10}`

### R-005 — On-screen hook chhota aur alag ⚙️
- **Purana ID:** A-005
- **Kab:** Short ki pehli 1-2 s me on-screen text lagate waqt
- **Kya:** Screen par hook 6-7 shabd se zyada nahi, ek accent word ke saath; woh spoken hook ki copy na ho, usme kuch jode (number, result, sawal)
- **Kyun:** Sound-off viewer ko screen wala hook hi rokta hai; bola hua dohraane se dusri jaankari ki jagah khali जाती hai
- **Kitni baar:** Har short; Melvynx ≤6 shabd, ExpoCut 4-7 shabd
- **Evidence:** 🟠 — Melvynx house rule + ExpoCut playbook practice (ExpoCut: Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Check:** `{"kind": "max_words", "what": "on_screen_hook", "value": 7}`

### R-006 — Open loop kholo, aakhir se pehle band mat karo
- **Purana ID:** A-006
- **Kab:** Script ki structure me
- **Kya:** Aage aane wali cheez announce karo ('teesri wali ne hairaan kar diya') aur uska payoff end ke paas do; har sentence usi ek vaade ko aage badhaye, detour nahi
- **Kyun:** Khula sawal viewer ko roke rakhta hai; jo hissa video ko aage nahi badhata, retention graph wahi girta hai
- **Kitni baar:** Har video me kam se kam 1 open loop, payoff end se pehle nahi
- **Evidence:** 🟠 — Creator practice (kmilo hook-and-retention); Melvynx ke measured viral data me 'one promise, paid line after line' isko support karta hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-007 — Re-hook 40-60% par
- **Purana ID:** A-007
- **Kab:** Script ke beech wale hisse me
- **Kya:** 40-60% ke aas-paas ek line rakho jo dhyaan restart kare: naya sawal, number, twist ('lekin isse theek nahi hua'), ya sabse mushkil hissa ('ye wala sab skip karte hain')
- **Kyun:** Beech me dhyaan girna sabse aam hai; ek naya gap wahi rokta hai jahan viewer jaane wala hota hai
- **Kitni baar:** 25 s se lambi har script me 1 re-hook; 25 s se chhoti skip kar sakte ho
- **Evidence:** 🟡 — Melvynx ke niche-outlier measurements (apne studied accounts) me consistent pattern — measured data, peer-reviewed nahi
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-008 — Ek video = ek idea, ek vaada
- **Purana ID:** A-008
- **Kab:** Topic aur script tay karte waqt
- **Kya:** Ek hi idea rakho; script me 'and also' aaye to woh dusri video hai; hook se ask tak ek hi promise chale
- **Kyun:** Do topics wala video dono me aadha rehta hai; ek vaada hi retention aur share dono banata hai
- **Kitni baar:** Har video par
- **Evidence:** 🟠 — Melvynx script-rules ka house rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-009 — Topic pehle, script baad me (proven concept)
- **Purana ID:** A-009
- **Kab:** Kuch bhi likhne se pehle, planning par
- **Kya:** Woh concept chuno jo niche me pehle over-perform kar chuka ho (account median ke x3+ outliers wala); kaam ka kram: topic > hook > structure; fresh news wala topic ho to use week me pehle rakho
- **Kyun:** Measured data kehta hai views topic se bante hain — same creator, same edit, topic badalte hi x1 se x100 ka farak
- **Kitni baar:** Week ke 5 scripts me kam se kam 3 proven concept par
- **Evidence:** 🟡 — Melvynx ke outlier measurements (har studied niche me median ke muqable) — measured data
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-010 — Object 0 second par, hook me specific
- **Purana ID:** A-010
- **Kab:** Short ke pehle frame aur pehli line par
- **Kya:** Jis cheez ke baare me video hai use pehle second me dikhao (naam baad me), aur pehli line me kam se kam ek specific rakho: number, bade brand ka naam, ya 'free'
- **Kyun:** Viewer 1 s me tay karta hai 'ye mere liye hai ya nahi'; creator ke baare me hook ya vague category x1 par reh jati hai
- **Kitni baar:** Har short par
- **Evidence:** 🟡 — Melvynx viral research ke measured rules (every niche checked)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-011 — Proof 8 second ke andar ⚙️
- **Purana ID:** A-011
- **Kab:** Video ki shuruaat me
- **Kya:** 8 s ke andar proof dikha do — number, screen, ya receipt — taaki viewer ko baaki video par bharosa ho
- **Kyun:** Bina saboot ke vaada sirf daava lagta hai; jaldi proof aage ki baaton ko wazan deta hai
- **Kitni baar:** Har script; viral data kehta hai 4-7 s sabse achha
- **Evidence:** 🟡 — Melvynx viral measurements (proof by 4-7 s) + script trigger rule (proof before 8 s)
- **Sources:** `github_Melvynx_video-agent-skills.md`
- **Check:** `{"kind": "proof_within_s", "value": 8}`

### R-012 — Triggers kam se kam 4, apni jagah par
- **Purana ID:** A-012
- **Kab:** Script likhne ke baad check karte waqt
- **Kya:** Kam se kam 4 triggers sahi jagah rakho: curiosity gap (hook), self-recognition (hook/line 2), proof (8 s se pehle), enemy (problem par — tool/habit/myth, viewer kabhi nahi), pattern break (re-hook), specificity (fix me), loss/urgency (ask se pehle; fake scarcity kabhi nahi)
- **Kyun:** Script isiliye tikti hai kyunki har hissa sahi pal par ek lever kheenchta hai
- **Kitni baar:** Har script me ≥4 triggers
- **Evidence:** 🟠 — Melvynx script-rules ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-013 — Funnel: darwaza bada, pivot 20-35% par
- **Purana ID:** A-013
- **Kab:** Naye viewers tak pahunchne wali Teach/Opinion video par
- **Kya:** M ya L size ke topic se kholo (bridge 0-3 s: debate, bada naam, sabki roz ki scene), tension 3-10 s, pivot script ke 20-35% par niche ki taraf modo, pearl (sabse mazboot line) sabse pehle likho; bridge par 2 test: niche tak 15 s ke andar pahunche? kal ko is viewer ko offer chahiye hoga?
- **Kyun:** Sirf niche ke topic par video chhote test group me hi marti hai; bada darwaza sahi viewer ko andar laata hai
- **Kitni baar:** Naye-reach wali videos par; pivot hamesha 20-35% band me
- **Evidence:** 🟠 — Melvynx funnel reference ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-014 — Divisive bridge ke kaide
- **Purana ID:** A-014
- **Kab:** Funnel me behes wala bridge use karte waqt
- **Kya:** Niche ke pehchane debate par ek paksh lo, ek sentence me kaho aur use fairly defend karo (pehle opposite ki ek line, phir apni wajah + example); hamla idea/habit/tool par ho, kisi person ya viewer group par kabhi nahi; CTA soft rakho (proximity 0-1)
- **Kyun:** Behes sabse chauda darwaza hai, lekin galat nishana rage-bait ban jata hai aur sakht sale usi pal bharosa tod deta hai
- **Kitni baar:** Divisive script me; bridge kabhi poori video nahi
- **Evidence:** 🟠 — Melvynx funnel reference ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-015 — Hook khule, sirf ek baar repeat ho
- **Purana ID:** A-015
- **Kab:** Koi line hook bana kar cut ki shuruaat me rakho to
- **Kya:** Hook line cut ko khole aur poori edit me apne context me sirf ek baar repeat ho; dusri baar repeat kabhi nahi
- **Kyun:** Reviewer ki standing pasand: ek repeat context deta hai, dusra repeat defect mana gaya (pipeline ke apne itihaas me repeat bug do baar lauta)
- **Kitni baar:** Har reel jisme hook prepend ho — repeat count theek 1
- **Evidence:** 🟠 — mktkit owner/reviewer ka house rule, QA gate (hook.once) se enforce hota hai
- **Sources:** `github_1610-advisory_mktkit.md`
- **Takraav note:** Ye sirf mktkit ka design rule hai; baaki teen sources me hook-repeat ka koi niyam nahi — aam taur par repeat ko galti hi mana jata hai, dusri pipeline me lagane se pehle socho (dekho CONFLICTS.md)

### R-016 — End screen aur closing
- **Purana ID:** A-017
- **Kab:** YouTube lambi video ke aakhir me
- **Kya:** Aakhri 5-20 s end screen ke liye khaali rakho (video ≥25 s ho, ≤4 elements aayenge, wahan zaroori text mat rakho); closing ek sentence me batao aage kahan jana hai — lambi recap nahi
- **Kyun:** End screen elements content ko dhak dete hain; lambe sign-off par hi retention sabse tez girti hai
- **Kitni baar:** Har eligible YouTube video par
- **Evidence:** 🟡 — YouTube official end-screen spec (platform rule)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-017 — CTA ek line me, object ke saath
- **Purana ID:** A-018
- **Kab:** Video ke aakhir me ask rakhte waqt
- **Kya:** Ek hi ask, ek line me, aur woh koi cheez de (repo, guide, prompt); Shorts me CTA card aakhri 2-3 s me; 'thanks for watching' ya bina exact shabd wala 'comment karo' nahi
- **Kyun:** CTA views nahi banata, comments/DMs banata hai — aur kai asks ek saath koi ask nahi banta
- **Kitni baar:** Har video me 1 ask; Offer video ke alawa soft
- **Evidence:** 🟡 — Melvynx viral measurements (CTA reach nahi banata) + shorts-codes ka house rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-018 — Facts aur numbers invent mat karo
- **Purana ID:** A-019
- **Kab:** Script ya video me koi number, naam ya result aaye to
- **Kya:** Number/naam/result sirf asal source se (creator ke diye hue facts); jo na mile use {{placeholder}} rakho aur 'bharna baki' me likho; koi figure bina source ke mat ghusao — source na ho to saaf kaho
- **Kyun:** Gadha hua number ek baar pakda jaye to poori channel ki baaton par bharosa jata hai
- **Kitni baar:** Har script, har video
- **Evidence:** 🟠 — kmilo hard rule ('No invented numbers') + Melvynx facts rule — dono house/creator ethic
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-019 — Licensed media hi; meme recreate karo
- **Purana ID:** A-020
- **Kab:** Music, SFX, footage ya meme use karte waqt
- **Kya:** Sirf CC0, YouTube Audio Library, ya commercial use ki written license wala media lo; NC ya 'YouTube par mila hua' kabhi nahi; meme ka original media/music mat uthao — joke ko apne graphics se recreate karo
- **Kyun:** Monetized channel par ek claim poori video (aur channel) ko mehenga pad sakta hai
- **Kitni baar:** Har asset par; library me naya sound aaye to uska license evidence record karo
- **Evidence:** 🟠 — kmilo hard rule + licenses reference (house rule, legal risk par based)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-020 — Body ki banawat type ke hisaab se
- **Purana ID:** A-021
- **Kab:** Script ka body likhte waqt
- **Kya:** Type-wise beats rakho — Teach: problem → kyun hota hai → fix (steps/ek move) → kya badlega; Proof: result+number → concretely kya kiya → copyable hissa → honest catch; Story: moment (mid-scene) → turn → ek line ka lesson; Opinion: position → opposite ko fairly → reason+example → kya karein; Talking head: cold open → context → sections (har section mini-hook se khule) → payoff
- **Kyun:** Har type ka viewer alag ummeed se aata hai; banawat wahi ummeed poori karti hai to beech me girawat nahi aati
- **Kitni baar:** Har script par uske type ki banawat
- **Evidence:** 🟠 — Melvynx script-rules (body by type) + kmilo talking-head recipe structure
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`

### R-021 — Week ka mix aur offer ki doori
- **Purana ID:** A-022
- **Kab:** Hafte ki scripts plan karte waqt
- **Kya:** Pehle mix banao (5 me lagbhag Teach 2, Proof 1, Story 1, Opinion 1, Offer ≤1); ek hi hook formula lagatar do baar nahi, ek hi type hafte me teen baar nahi; offer proximity ladder 0-3 rakho — rung 3 hafte me ≤1 aur woh bhi sabse mazboot value video ke baad
- **Kyun:** Ek hi tarah ki videos thakati hain aur har video me bechna bharosa khatm karta hai
- **Kitni baar:** Har week ke plan par
- **Evidence:** 🟠 — Melvynx week-mix aur offer-proximity house rules
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-022 — Hit concept ko do hafte me repeat karo
- **Purana ID:** A-023
- **Kab:** Apna koi concept x3+ over-perform kare to
- **Kya:** Use 2 hafte ke andar 2-3 naye hooks ya naye items ke saath repost karo, use 'luck' kehne se pehle
- **Kyun:** Jo shape ek baar median se kai guna gaya, woh recipe hai; dohraana hi use sabit karta hai
- **Kitni baar:** Har x3+ hit par, 14 din ke andar
- **Evidence:** 🟡 — Melvynx viral measurements ka rule (apne studied accounts par)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-023 — Retention report padh kar seekho
- **Purana ID:** A-024
- **Kab:** Video publish hone ke baad
- **Kya:** Retention report dekho: jis moment par dip hai wahi agli baar cut/sudhar ka candidate hai; spikes (rewatch/share wale hisse) pehchano aur unhe dohraane ki koshish karo
- **Kyun:** Graph jhooth nahi bolta — dip aksar usi hisse par hota hai jo video ko aage nahi badhata
- **Kitni baar:** Har publish ke baad (key moments ≥60 s aur ≥100 views wali videos par milte hain)
- **Evidence:** 🟡 — YouTube official key-moments feature (platform data)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-024 — Script ki lines: ek saans, 4-15 shabd
- **Purana ID:** A-025
- **Kab:** Script likhte waqt
- **Kya:** Ek line = ek sentence = ek saans, 4-15 shabd; abstract lines lagatar 3 nahi — teesri ko example bana do; ek viewer se baat karo ('you', 'you guys' nahi); chhote shabd, jo dost ko na kaho woh kato
- **Kyun:** Lambi, abstract lines bolne me bhi atakti hain aur sunne me bhi; ek-saans wali lines hi natural lagti hain
- **Kitni baar:** Har script ki har line par
- **Evidence:** 🟠 — Melvynx script-rules ka house style
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-025 — AI wali banawat hatao (humanize)
- **Purana ID:** A-026
- **Kab:** Script ya koi bhi text finalize karne se pehle
- **Kya:** AI ke nishan saaf karo: hype shabd (delve, unlock, game-changer jaisi khaali badi baatein) hatao ya number se badlo; preamble ('here's the thing') kato; recap ending hatao; engagement bait ('save this', 'tag someone') sirf asl ask se badlo; false contrast ('it's not X, it's Y') poori text me ≤1; tino-tino ki triads tod do
- **Kyun:** Chat-model jaisi banawat viewer ko turant 'ye asli insaan nahi' ka sanket deti hai aur bharosa girta hai
- **Kitni baar:** Har script/text par aakhri pass
- **Evidence:** 🟠 — Melvynx ai-tells + humanize references ka creator framework
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-026 — Clip standalone banao (long se short) ⚙️
- **Purana ID:** A-027
- **Kab:** Lambi video se Short/Clip nikaalte waqt
- **Kya:** Clip aisi jagah se kato jo bina context samajh aaye: pehli line 'so', 'as I said', 'this' jaisi bahari sahara wali na ho; ek hi idea poora ho; end finished thought par ho; long video ke references ('pichle part me') hata do; end payoff ya loop par
- **Kyun:** Jo clip context maangta hai woh feed me akela khada nahi ho pata
- **Kitni baar:** Har clip 20-60 s; Melvynx ka standalone score ≥7/10 (5 points × 0-2)
- **Evidence:** 🟠 — Melvynx clips skill ka scoring system + kmilo shorts recipe
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "duration_range_s", "what": "clip_from_long_form", "min": 20, "max": 60}`

### R-027 — Packaging pehle, production baad me
- **Purana ID:** B-001
- **Kab:** Har naye video idea par, script/shoot se pehle
- **Kya:** Title aur thumbnail pehle design karo — ye idea ka test hai; agar compelling package na bane to idea kamzor hai, pehle wahi fix karo
- **Kyun:** Jo video click hi nahi hoga uski retention curve hi nahi banti; kamzori sabse saste stage par pakdi jati hai
- **Kitni baar:** Har video par 1 baar, pre-production me; Henterprise: har idea ke 3 packaging options bana kar best chuno
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`, `github_humbertobellor_henterprise.md`

### R-028 — Title/thumbnail ka vaada video me sach me pura karo ⚙️
- **Purana ID:** B-002
- **Kab:** Opening aur payoff planning ke time
- **Kya:** Thumbnail/title ne jo promise kiya hai use video me literally pay karo; curiosity sirf wahan rakho jahan video use sach me resolve kare
- **Kyun:** Unpaid promise turant drop karata hai aur unresolved curiosity viewer ko next time click na karne ki training deti hai
- **Kitni baar:** Har video, har vaade par; long-form hook payoff ≤15s (shorts ≤2.5s) — dekho B-006/B-017
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers + producer practice
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`, `github_humbertobellor_henterprise.md`, `github_classicchins_compounding-marketing.md`
- **Check:** `{"kind": "hook_within_s", "value": 15}`

### R-029 — Hook ke 3 variants — category mix karke
- **Purana ID:** B-003
- **Kab:** Short-form script ke liye hook chunne se pehle
- **Kya:** 100 hook formulas ke 10 categories (appendix) se 3 candidate hooks banao: 1 stop-scroll category (negation / specificity / question) + 1 retention category (story / confession / emotional) + 1 free pick; har ek ke saath category label aur 'best for' note do
- **Kyun:** Pehla hook thumb rokta hai, dusra viewer ko 3 second ke aage rakhta hai; alag categories ke hooks aam taur par sabse strong hote hain
- **Kitni baar:** Har script par 3 variants; A/B test ya strongest fit ke liye
- **Evidence:** 🟠 — curated hook library / creator practice — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_rediumvex_viral-hooks-skill.md`

### R-030 — Filled hook 12 shabdon se chhota rakho ⚙️
- **Purana ID:** B-004
- **Kab:** Hook variant ko final karte waqt
- **Kya:** Bracket bhara hua hook <12 words me rakho aur platform ke hisaab se native banao (TikTok/IG casual, LinkedIn punchy-declarative, YouTube title-style search-friendly, X short-contrarian)
- **Kyun:** Lamba hook pehle seconds me samajh nahi aata; chhota hook turant land karta hai
- **Kitni baar:** Har hook, har baar
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_rediumvex_viral-hooks-skill.md`
- **Check:** `{"kind": "max_words_exclusive", "what": "filled_hook", "value": 12}`

### R-031 — First-5-seconds checklist pass karo ⚙️
- **Purana ID:** B-005
- **Kab:** Har video ke opening par, publish se pehle
- **Kya:** Check: visual interesting/unexpected ≤1s; hook line boli gayi ≤3s; viewer ko milega kya, iska promise ≤5s tak implicit saaf; logo cold-open NAHI; 'Hi, I'm X' preamble NAHI — punch se shuru karo
- **Kyun:** Source ke data ke hisaab se aadhe viewers pehle 10 seconds me drop hote hain; hook hi tay karta hai ki baaki video exist karega ya nahi
- **Kitni baar:** Har video ke pehle 5 seconds par, bina exception
- **Evidence:** 🟡 — Wistia/Vidyard platform data par based skill (aadhe viewers pehle 10s me drop)
- **Sources:** `github_classicchins_compounding-marketing.md`, `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "hook_within_s", "value": 5}`

### R-032 — Cold open = hook, branding baad me ⚙️
- **Purana ID:** B-006
- **Kab:** Long-form (10–55 min) video ki shuruaat par
- **Kya:** Mid-content se kholo (threat/countdown, absurd exact number, universal observation, ya question ladder); 'hi, I'm X' 0:15–1:00 par rakho. Pehle 30s measured band: 65–98 words, 2–7 cuts, zero throat-clearing
- **Kyun:** Measured corpus me top explainers aise hi khulte hain; branding pehle rakhne se promise late hota hai aur drop badhta hai
- **Kitni baar:** Har long-form opening; first-30s words 65–98, cuts 2–7
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "count_range", "what": "words_first_30s", "min": 65, "max": 98}`

### R-033 — Promise line jaldi bolo, payoff par verbatim dohrayo
- **Purana ID:** B-007
- **Kab:** Long-form script likhne/review karte waqt
- **Kya:** Payoff line ('X because Y') shuru me state karo, video me use earn karo, aur end ke paas use verbatim restate karo
- **Kyun:** Viewer ko pehle se pata hota hai ki wo kis cheez ka intezaar kar raha hai; verbatim callback payoff ko band (close) kar deta hai
- **Kitni baar:** Har long-form video me 1 promise line; checklist: stated early AND restated at payoff
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`

### R-034 — Har waqt ≥1 open loop zinda rakho ⚙️
- **Purana ID:** B-008
- **Kab:** Poore long-form video ke structure me
- **Kya:** Kam se kam ek open loop hamesha live rakho; loop 45 minute tak bhi chal sakta hai agar beech me re-tease ho aur payoff tease se ZYADA detail ke saath mile. Ek measured refrain (same benchmark artifact, har section naya number) permanently open loop ka kaam karta hai
- **Kyun:** Khula sawaal viewer ko band hone tak rokta hai; loop band hote hi nikalne ki wajah ban jati hai
- **Kitni baar:** Har pal ≥1 loop live; payoff hamesha tease se bada
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "min_open_loops_alive", "value": 1}`

### R-035 — Payoff ko aakhri 15–25% me rakho ⚙️
- **Purana ID:** B-009
- **Kab:** Long-form structure plan karte waqt
- **Kya:** Sabse bada payoff video ke last 15–25% hisse me rakho; beech wale loops uski taraf build karein, use jaldi close mat karo
- **Kyun:** Jaldi mila payoff baaki video ko dead weight bana deta hai (checklist me yahi violation flag hota hai)
- **Kitni baar:** Har long-form video ka main payoff 75–85% position ke aas-paas
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "percent_range", "what": "payoff_position_percent", "min": 75, "max": 85}`

### R-036 — Callback close + tez exit ⚙️
- **Purana ID:** B-010
- **Kab:** Long-form video ke end par
- **Kya:** Cold open ko echo karo (phrase/location/metaphor), CTA ko theme me buno (alag se ghusao mat), aur payoff ke ~30s ke andar video khatam kar do; bloopers end card ke baad
- **Kyun:** Callback kahani ko gol band karta hai; payoff ke baad lamba kheenchna end drop-off lata hai
- **Kitni baar:** Har long-form end; exit payoff ke ~30s ke andar
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "max_delay_s", "what": "exit_after_payoff", "value": 30}`

### R-037 — Sponsor/tangent ko container me rakho (20–33%) ⚙️
- **Purana ID:** B-011
- **Kab:** Long-form me sponsor ya tangent aane par
- **Kya:** Sponsor/tangent ko visually distinct container me rakho, joke segue se andar jao aur hard re-entry se bahar aao; placement runtime ke 20–33% hisse me
- **Kyun:** Measured corpus me containers aise hi chalte hain — viewer ko pata chalta hai ye alag hissa hai, aur re-entry kahani ko phir pakad leti hai
- **Kitni baar:** Har sponsor/tangent par; position 20–33% of runtime
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "percent_range", "what": "sponsor_container_position_percent", "min": 20, "max": 33}`
- **Takraav note:** Henterprise ka B-012 kehta hai sponsor read pehle payoff ke BAAD hi aaye. Agar pehla payoff 33% ke baad hai to dono rules ek saath satisfy mushkil honge — Step 3 (Order) me iska faisla hoga. (dekho CONFLICTS.md)

### R-038 — Sponsor read pehle payoff ke baad hi
- **Purana ID:** B-012
- **Kab:** Long-form me sponsor read place karte waqt
- **Kya:** Sponsor read ko hamesha pehle payoff ke baad rakho, kabhi usse pehle nahi
- **Kyun:** Vaada pura hone se pehle ad aana unpaid-promise jaisa lagta hai aur cliff bana sakta hai
- **Kitni baar:** Har sponsor read, bina exception
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`
- **Takraav note:** Slopstudio ka B-011 sponsor ko 20–33% band me rakhta hai (measured). Agar pehla payoff der se hai to dono takra sakte hain — Step 3 (Order) decide karega. (dekho CONFLICTS.md)

### R-039 — Har seam par aage dekhne ki wajah do
- **Purana ID:** B-013
- **Kab:** Long-form ke har section transition par
- **Kya:** Har transition/seam par explicit reason to continue rakho — ek open question, ek promised payoff, ya ek stated next step
- **Kyun:** Retention sections ke beech me nahi, seams (jod) par marti hai; bina wajah ke transition viewer ke liye exit point hai
- **Kitni baar:** Har transition par, bina exception
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`

### R-040 — Chapter standalone + aage ki taraf ishara
- **Purana ID:** B-014
- **Kab:** Long-form ko chapters me baant-te waqt
- **Kya:** Har section/chapter ko aisa banao ki wo akela bhi samajh aaye, aur uska end hamesha aage ki taraf point kare
- **Kyun:** Standalone chapters beech se ghusne wale viewer ko bhi pakadte hain; forward-pointing end seam ko majboot karta hai
- **Kitni baar:** Har chapter par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`

### R-041 — Value front-load karo, best part rok ke mat rakho
- **Purana ID:** B-015
- **Kab:** Long-form structure/value placement par
- **Kya:** Sabse achhi value jaldi do; 'achha part' end ke liye withhold mat karo
- **Kyun:** End tak rokna us viewer ke liye optimize karta hai jo tab tak ja chuka hota hai
- **Kitni baar:** Har video; khaas taur par pehle hisse me
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`

### R-042 — Short-form: ek idea, payoff jaldi, loop wala end
- **Purana ID:** B-016
- **Kab:** Short-form script banate waqt
- **Kya:** Ek hi idea rakho, koi setup nahi; opening frame motion jaisa padhe, aur payoff attention decay hone se pehle aa jaye. End wahan rakho jahan se beginning phir sense banaye (loop)
- **Kyun:** Short-form me dhyaan sabse tez girta hai; loop wala end rewatch ko badhata hai
- **Kitni baar:** Har short; duration = jitna lamba near-100% retention hold ho sake (B-053 dekho)
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`, `github_filnik_social-media-manager-AI.md`

### R-043 — Shorts me reverse structure: payoff pehle
- **Purana ID:** B-017
- **Kab:** Short banate waqt
- **Kya:** Pehle payoff dikhao, phir explain karo (reverse structure)
- **Kyun:** Result pehle dekhne se viewer explanation sunne ke liye rukta hai
- **Kitni baar:** Har short ki structure me
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`

### R-044 — Short ke pehle 3s + aakhri 3s pehle likho
- **Purana ID:** B-018
- **Kab:** Short script/edit shuru karte waqt
- **Kya:** Pehle first 3 seconds aur last 3 seconds author karo, phir beech bharo; end ko start se loop karo
- **Kyun:** Short ka faisla uske pehle aur aakhri palon me hota hai; loop rewatch ko support karta hai
- **Kitni baar:** Har short par
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`

### R-045 — BUTS chain: but = takraav, so = reaction
- **Purana ID:** B-019
- **Kab:** Short ki kahani aage badhane ke liye
- **Kya:** Har beat ko 'but' (naya conflict) ya 'so' (uski reaction) se jodo — kahani kabhi rukti hui mehsoos na ho
- **Kyun:** Lagatar conflict+reaction narrative tension banaye rakhta hai; viewer ko 'kahani khatam' mehsoos hi nahi hota (Hoyos ki method)
- **Kitni baar:** Har short ke har beat par
- **Evidence:** 🟠 — creator practice (Jenny Hoyos profile) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-046 — Foreshadowing hook: pehle second me result ka ishara
- **Purana ID:** B-020
- **Kab:** Short ki opening design karte waqt
- **Kya:** Pehle second me final result/comparison ka hint do, lekin reveal end ke liye rakho
- **Kyun:** Viewer ko end tak comparison dekhne ke liye rukna padta hai
- **Kitni baar:** Har suitable short ki opening me
- **Evidence:** 🟠 — creator practice (Jenny Hoyos profile) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-047 — End sabse tez emotion par rakho
- **Purana ID:** B-021
- **Kab:** Short/long video ke end par
- **Kya:** Video ko maximum emotion/climax ke pal par khatam karo; kamzor 'and so…' wala band mat karo
- **Kyun:** Viewer poori video ko aakhri pal ki emotion se judge karta hai (Hoyos); weak ending peeche ka saara kaam kharab karti hai
- **Kitni baar:** Har video ka aakhri beat
- **Evidence:** 🟠 — creator practice (Hoyos + MrBeast profiles) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-048 — Constant escalation + segment ke beech micro-cliffhanger
- **Purana ID:** B-022
- **Kab:** MrBeast-style long/short structure me
- **Kya:** Har segment pichle se intensity me aage badhe; segments ke beech internal cliff-hangers rakho aur sabse bada payoff (prize/challenge/result) shuru me hi visible karo
- **Kyun:** Badhti tension aur micro-suspense viewer ko agle segment tak kheenchti hai (MrBeast profile)
- **Kitni baar:** Har segment par
- **Evidence:** 🟠 — creator practice (MrBeast profile) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Takraav note:** Slopstudio ka B-045 kehta hai pacing FLAT rakho, escalation nahi. Farak: ye rule kahani ke stakes/intensity ki escalation hai, B-045 cut/WPM pacing ki. Agar dono ek hi lever (cut speed) par lagu hon to takraav hoga — Step 3 (Order) decide karega. (dekho CONFLICTS.md)

### R-049 — Content buckets: pehchan wali recurring series banao
- **Purana ID:** B-023
- **Kab:** Channel/shorts series planning me
- **Kya:** 3–4 recurring series (buckets) define karo — har bucket ek pehchan wala format; viewer ko pata ho ki use kya milega
- **Kyun:** Ek bucket pasand aane par viewer usi series ki baaki videos dekhta hai; pehchan expectation aur wapsi banati hai (Hoyos)
- **Kitni baar:** Channel level par; har nayi short kisi bucket me
- **Evidence:** 🟠 — creator practice (Jenny Hoyos profile) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-050 — Ek video = ek job
- **Purana ID:** B-024
- **Kab:** Video ka brief tay karte waqt
- **Kya:** Har video ka sirf EK job rakho (awareness / conversion / education / trust aadi); explainer+demo+testimonial+brand ko ek video me merge mat karo
- **Kyun:** Sab jobs ek saath karne wala video koi job achhe se nahi karta — wo documentary ban jata hai, asset nahi
- **Kitni baar:** Har video, brief stage par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`

### R-051 — Video type ke hisaab se beat template use karo
- **Purana ID:** B-025
- **Kab:** Script likhne se pehle type chunne par
- **Kya:** Explainer (60–90s): Problem→Agitate→Solution→How→Proof→CTA. Demo (2–5m): Hook→Use-case setup→Walkthrough (3–5 features)→Result→CTA. Testimonial (60–120s): Result hook→Before→Decision→After→Endorsement. UGC (15–30s): Hook (1s)→Reveal→Result→CTA. Thought leadership: Specific claim→Framework→Examples→Takeaway→CTA
- **Kyun:** Har type ki proven structure hoti hai; wing karne se pehle 15 seconds me 80% viewers kho sakte ho (source ka daava)
- **Kitni baar:** Har script, type ke hisaab se
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`

### R-052 — Short infotainment ka emotional arc (0–30s)
- **Purana ID:** B-026
- **Kab:** 15–30s infotainment short banate waqt
- **Kya:** Setup 0–5s = frustration/recognition ('ye to main hu'); Development 5–15s = ironic escalation (haal aur bhadke); Payoff 15–25s = smart solution/plot twist; CTA 25–30s = soft CTA
- **Kyun:** Pehchan → badhti absurdity → twist ka arc share/save wali reactions (solidarity, 'mujhe ye dikhana hai', 'ye nahi pata tha') ko trigger karta hai
- **Kitni baar:** Har infotainment short par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-053 — Direct-to-camera question hook ⚙️
- **Purana ID:** B-027
- **Kab:** Short ke pehle 3 seconds me
- **Kya:** Camera me dekh kar aisa sawal poochho jo target viewer ko turant engage kare (jaise 'How many X did you read this week?')
- **Kyun:** Seedha sawal viewer ko dialogue mode me dalta hai, passive rehne nahi deta
- **Kitni baar:** Hook ki ek technique ke roop me, suitable shorts me
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "hook_within_s", "value": 3}`

### R-054 — 'If…' scenario hook ⚙️
- **Purana ID:** B-028
- **Kab:** Short ke pehle 3 seconds me
- **Kya:** 'If…' se shuru karo jo target audience ignore na kar sake ('If you've also spent 3 weeks on…, this video is for you')
- **Kyun:** Apni sthiti ko pehchanne wala viewer turant rukta hai — ye usi ke liye bana lagta hai
- **Kitni baar:** Hook ki ek technique ke roop me, suitable shorts me
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "hook_within_s", "value": 3}`

### R-055 — Deliberate boundary = attention reset button
- **Purana ID:** C-011
- **Kab:** Dhyaan reset karna ho — naya section, reveal, topic change
- **Kya:** Us point par jaanboojh kar ek saaf situation change design karo (jagah, insaan, goal ya cause visibly badle) aur cut exactly usi par lagao — ek brain 'update' kharch ho raha hai, use wahan kharch karo jahan fresh start chahiye
- **Kyun:** Boundary par dimaag purana model band karke naya kholta hai — yahi natural fresh-start moment hai
- **Kitni baar:** Har section/reveal/topic-change par
- **Evidence:** 🟢 — Boundary responses situation changes se statistically mediated hain (Frontiers 2010 film study)
- **Sources:** `science_jeffrey_zacks.md`

### R-056 — Ek baar me ek hi dimension badlo
- **Purana ID:** C-012
- **Kab:** Boundary banana ho
- **Kya:** Place, people, goal, cause — ek baar me ek hi dimension badlo; chaaron ek saath badalna hard reset hai, wo climax ya naye chapter ke liye bachao, aadat mat banao
- **Kyun:** Zyada simultaneous situation change = zyada strong boundary response; roz-marra me ye disorientation banta hai
- **Kitni baar:** Har boundary par; hard reset sirf bade moments par
- **Evidence:** 🟡 — Mediation result 🟢 hai, lekin 'ek baar me ek, baaki bachao' wali dosage editorial inference hai
- **Sources:** `science_jeffrey_zacks.md`

### R-057 — Chunk = ek event
- **Purana ID:** C-013
- **Kab:** Content structure karte waqt — topics, steps, scenes, chapters
- **Kya:** Har chunk ko exactly ek event banao jiska saaf beginning aur end ho; adha-event ya do-event wala chunk mat banao
- **Kyun:** Viewer ki memory inhi event chunks me store hoti hai — ragged chunks matlab ragged recall
- **Kitni baar:** Har chunk/section par
- **Evidence:** 🟢 — Boundaries baad me yaad rehne wali cheezon ko predict karti hain — memory experiments ka result
- **Sources:** `science_jeffrey_zacks.md`
- **Takraav note:** Chapters wale rule (C-046) se milta hai — chapter bhi ek event hona chahiye (dekho CONFLICTS.md)

### R-058 — Murch 1 — Emotion sabse upar (51%)
- **Purana ID:** C-014
- **Kab:** Koi bhi cut chunna ho, khaaskar jahan criteria takrate hon
- **Kya:** Cut pehle is sawal se test karo: 'ye is moment ki emotion ke sach hai? audience ko kya mehsoos karana hai?' Emotion fail ho to cut reject/flag karo — EMOTION CHECK ENGINE KE BAHAR HAI: aise cut ko human check ke liye flag karo, engine khud emotion judge nahi karega
- **Kyun:** Murch ke hisaab se emotion akela (51%) baaki paanch criteria ke kul (49%) se zyada bhaari hai; emotion sahi ho to audience neeche ki khaamiyan notice hi nahi karti
- **Kitni baar:** Har cut par; emotion-veto ke roop me — technically perfect lekin emotion todne wala cut bhi reject
- **Evidence:** 🟠 — Ek master editor ki craft raay; Murch khud percentages ko 'slightly tongue-in-cheek' kehta hai — koi experiment nahi
- **Sources:** `science_walter_murch.md`
- **Takraav note:** User ke order (Kahani > Samajh > Rhythm > Style) me emotion Kahani ke andar band hai; Murch use Kahani se bhi upar rakhta hai — aur is system me emotion insaan ki aankh par hai, engine par nahi (dekho CONFLICTS.md)

### R-059 — Murch 2 — Story aage badhe (23%)
- **Purana ID:** C-015
- **Kab:** Cut ka faisla karte waqt
- **Kya:** Wahi cut rakho jo kahani ko aage badhaye; jo cut kahani ko roke ya ghumaye, use neeche ke criteria (rhythm/continuity) ke liye mat bachao
- **Kyun:** Story dusra sabse bhaari criterion hai; emotion ke baad yahi cut ki asal justification hai
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — Craft wisdom, measured nahi (Murch, In the Blink of an Eye)
- **Sources:** `science_walter_murch.md`

### R-060 — Murch meta — all-six pehle, qurbani neeche se upar
- **Purana ID:** C-020
- **Kab:** Do candidate cuts takrayein aur trade-off majboori ho
- **Kya:** Pehle wo cut dhundo jo chhah criteria pure kare; na mile to neeche se upar qurbani do: 3-D space pehle, phir 2-D plane, phir eye-trace, phir rhythm, phir story — emotion kabhi nahi. Upar wala criterion neeche wale ke liye kabhi mat chhodo
- **Kyun:** Hierarchy sirf forced trade-offs ke liye hai; Murch: 'never accept less when more is available'
- **Kitni baar:** Har conflicting cut decision par
- **Evidence:** 🟠 — Craft framework; percentages pedagogical device hain, measurements nahi
- **Sources:** `science_walter_murch.md`
- **Takraav note:** User ke apne Order (Kahani > Samajh aana > Rhythm > Style/Effect) se qareebi rishta hai, lekin ek farak: Murch Emotion ko Story se strictly upar rakhta hai, user ke order me emotion Kahani ke andar/insaan ke paas hai — Step 3 me ye faisla final hoga (dekho CONFLICTS.md)

### R-061 — Pehle 30 second ki beat structure ⚙️
- **Purana ID:** C-022
- **Kab:** Long-form video ka opening design karte waqt
- **Kya:** 0-3s: cold line/clip — promise ya peak moment, koi greeting nahi. 0:03-0:10 (der se der 0:10 tak): title ka promise apni awaaz me restate karo. 0:10-0:18: stakes/obstacle naam karke loop kholo. 0:18-0:28: watch-contract — 'by the end you will...'. 0:28-0:30: body me hard pivot. Pehle 15s me teeno kaam pure hon: click confirm, aisa sawaal jo viewer band na kar paye, payoff ke saboot ki jhalak. Main point ki setup 2-minute mark se pehle screen par ho
- **Kyun:** Pehle 30s retention cliff hai — sabse zyada viewers yahi jaate hain; promise confirm na ho to viewer 0:08 par nikal jata hai
- **Kitni baar:** Har long-form video par
- **Evidence:** 🟠 — Teenon sources ki beat timings aapas me milti hain (Jake 15s ke 3 kaam, SkillMedev 30s cliff, serge ki beat table) — craft consensus, controlled study nahi
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`
- **Check:** `{"kind": "hook_within_s", "value": 30}`
- **Takraav note:** Jake hook ko 15s kehta hai, SkillMedev/serge 30s — takraav nahi: 15s hook ka core hai, 30s puri beat structure; dono is rule me jode gaye hain (dekho CONFLICTS.md)

### R-062 — Hook ko score karo — weakest property fix karo
- **Purana ID:** C-023
- **Kab:** Hook finalize karne se pehle
- **Kya:** Har hook ko 5 properties par 0-100 score karo: Specificity, Address, Stakes, Curiosity, Brevity. Verdict = 60% mean + 40% sabse kamzor property. Sabse kamzor property ko fix karo (specificity kam = adjective hata ke number/naam/date; address kam = pehle 6 shabdon me 'you'; stakes kam = lagat naam karo; curiosity kam = khud jawab dene wala hissa kato; brevity kam = saans rukne wali jagah par roko). Low score = dobara dekho; high score = vaada kabhi mat samjho
- **Kyun:** Ek dead property wala hook usi property par leak karta hai; average use chhupa deta hai — isliye weakest-link weighting
- **Kitni baar:** Har hook par, recording se pehle
- **Evidence:** 🟡 — hookscore.py 74 real short-form hooks par calibrate hua (top-8/bottom-8 by views, 5 channels); kharab hooks ko asli se alag karta hai, lekin ek hi creator ke hits vs misses ko mushkil se alag karta hai — isliye 🟡, 🟢 nahi
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`

### R-063 — Hook variants banao, test karke chuno
- **Purana ID:** C-025
- **Kab:** Kisi video ka hook tay karte waqt
- **Kya:** Ek hook par mat ruko: long-form ke liye 5 hooks likho, score karke top 2 rakho aur dono dikhao; kam se kam 3 variants, har ek alag formula se, taaki A/B test ho sake aur pattern seekha ja sake. Sabse badhiya hook pehla draft lagbhag kabhi nahi hota
- **Kyun:** Variants ki tulna hi asli pasand batati hai; ek hook dena = andaza lagana
- **Kitni baar:** Har video par
- **Evidence:** 🟠 — Dono sources ki workflow rule; koi measurement nahi
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`

### R-064 — Cold-open payoff tease — result pehle, setup baad me ⚙️
- **Purana ID:** C-026
- **Kab:** Video me ek dramatic moment/result maujud ho (build, transformation, reveal)
- **Kya:** Sabse dramatic moment ya result ka 3-8 second ka flash sabse pehle dikhao, phir setup par cut karo — viewer wahan tak kaise pahunche, ye dekhne ke liye rukta hai. Tease kiya moment asal me video me hona chahiye aur intezaar ke layak bhi
- **Kyun:** Destination pehle dikhane se dheema hissa bik jata hai; setup par wapas cut hi khula loop hai
- **Kitni baar:** Har suitable video par ek baar, opening me
- **Evidence:** 🟠 — serge Y8 + Jake ke 'The Reveal' formula + SkillMedev Before/After — craft pattern
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`
- **Check:** `{"kind": "duration_range_s", "what": "cold_open_tease", "min": 3, "max": 8}`

### R-065 — Vaada imandari — title/hook ka promise pehle 30s me cash ho
- **Purana ID:** C-027
- **Kab:** Title, thumbnail aur hook finalize karte waqt
- **Kya:** Title/hook jo promise kare, video ka pehla hissa use imandari se pura kare — hook us payoff se zyada mat wada kare jo video de sakta hai. Inflate kiya hook ek view kharidta hai aur channel ka bharosa kharch karta hai; tez click-away ranking penalty hai
- **Kyun:** YouTube satisfied watch-time optimize karta hai: CTR x retention; over-promise wala click fast bounce me badalta hai aur modest title se zyada mehnga padta hai
- **Kitni baar:** Har video par
- **Evidence:** 🟡 — serge ke heuristics YouTube ke public Creator Insider statements par adharit synthesis hain; baaki do sources bhi yahi rule dete hain
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`

### R-066 — Promised artifact 20 second ke andar screen par ⚙️
- **Purana ID:** C-028
- **Kab:** Hook/title ne koi cheez dikhane ka vaada kiya ho (prompt, screenshot, result, tool)
- **Kya:** Wo artifact 20 second ke andar screen par dikhao. Reveal 8 minute par rakha to 1 minute par retention cliff pakka hai
- **Kyun:** Vaada kiya saboot jaldi na mile to hook clickbait padhta hai
- **Kitni baar:** Har promised artifact par
- **Evidence:** 🟠 — hooks.json ki rule; craft heuristic
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`
- **Check:** `{"kind": "artifact_within_s", "value": 20}`

### R-067 — Turn (0:15-0:45) — ek sentence me plan
- **Purana ID:** C-029
- **Kab:** Hook ke baad body shuru hone se pehle
- **Kya:** Ek sentence me batao video kya karne wala hai, aur karna shuru kar do. Channel intro, 'before we get started', subscribe pitch — kuch nahi; yehi 0:30 cliff ki sabse aam wajah hai
- **Kyun:** Viewer ko roadmap milta hai bina waqt kharch hue; throat-clearing sidha drop-off hai
- **Kitni baar:** Har long-form video par
- **Evidence:** 🟠 — yt-script ki structure rule
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`

### R-068 — Har beat: mini-hook + delivery + bridge (loop zinda) ⚙️
- **Purana ID:** C-031
- **Kab:** Long-form body ko 3-5 beats me structure karte waqt
- **Kya:** Har beat ke teen hisse rakho: shuruaat me mini-hook (is beat ka micro-promise), phir point ki delivery, phir bridge jo agle beat me ek loop khole. Kisi bhi pal kam se kam 1 open loop zinda rakho
- **Kyun:** Bina bridge ke beats 'and then' ki chain banti hai; khula loop hi viewer ko agle beat tak kheenchta hai
- **Kitni baar:** 3-5 beats per video; har pal ≥1 loop zinda
- **Evidence:** 🟠 — SkillMedev youtube-script-writer ki architecture rule
- **Sources:** `github_SkillMedev_skills.md`
- **Check:** `{"kind": "min_open_loops_alive", "value": 1}`

### R-069 — Midpoint par re-engagement trigger
- **Purana ID:** C-032
- **Kab:** Video ke beech wale beat par
- **Kya:** Beech me jaanboojh kar ek re-engagement trigger lagao — 'but here's the thing' jaisa mod ya stakes-raise — kyunki midpoint cliff ke baad dusra sabse bada drop-off hai
- **Kyun:** Unstructured body beech me ek-ek karke viewers kho deti hai; midpoint ka mod curve ko dobara uthata hai
- **Kitni baar:** Har long-form video me ek baar, midpoint par
- **Evidence:** 🟠 — SkillMedev ki craft claim; drop-off ranking ka koi cited dataset nahi
- **Sources:** `github_SkillMedev_skills.md`

### R-070 — Payoff over-deliver karo — bonus insight lazmi
- **Purana ID:** C-035
- **Kab:** Video ka ending/payoff likhte waqt
- **Kya:** Payoff hook ke vaade se zyada de: har beat ka takeaway ek sentence me recap karo, phir ek bonus insight do jo hook me zikr hi nahi tha. Yahi surplus santusht viewer ko subscriber banata hai aur end-screen retention uthata hai. Abrupt end mat karo — outro bhi retention signal hai
- **Kyun:** Promise se zyada milna hi 'satisfied watch' hai jise ranker optimize karta hai
- **Kitni baar:** Har video ke payoff par
- **Evidence:** 🟠 — SkillMedev ki payoff rule; Jake bhi payoff ko explicitly deliver karne ko kehta hai
- **Sources:** `github_SkillMedev_skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`

### R-071 — Ek hi CTA — ek hi ask
- **Purana ID:** C-036
- **Kab:** Video ke close par
- **Kya:** Sirf EK specific ask rakho, video ke topic se juda (jaise 'pricing script neeche link hai'). Subscribe-like-comment-bell ki string kabhi nahi; generic subscribe ask bhi nahi
- **Kyun:** Kai asks dhyaan baant dete hain; ek topic-specific ask convert karta hai
- **Kitni baar:** Har video me exactly 1
- **Evidence:** 🟠 — Teenon sources ki shared rule
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`, `github_sergebulaev_youtube-skills.md`

### R-072 — Shorts spoken hook 12 shabdon se kam ⚙️
- **Purana ID:** C-037
- **Kab:** Short/Reel/TikTok ka spoken hook likhte waqt
- **Kya:** Spoken hook line 12 shabdon ke neeche rakho — lambi line speaking pace par 3-second window se aage nikal jati hai. Line ek specific claim kare, vague nahi
- **Kyun:** Short-form me pehle 3 second hi poora audition hai; har shabd ko apni jagah kamani padti hai
- **Kitni baar:** Har short-form hook par
- **Evidence:** 🟠 — SkillMedev video-hook-writer ki hard limit
- **Sources:** `github_SkillMedev_skills.md`
- **Check:** `{"kind": "max_words", "what": "spoken_hook", "value": 12}`
- **Takraav note:** Long-form hook ke liye band 9-24 shabd hai (C-024); Shorts par ye sakht limit jeetegi (dekho CONFLICTS.md)

### R-073 — Short ke liye self-contained 20-55s moment ⚙️
- **Purana ID:** C-040
- **Kab:** Long video se Short kaatna ho
- **Kya:** Sirf wahi 20-55 second ka span chuno jo: (1) complete thought se khule (pehli line ko pichla minute na chahiye ho), (2) usme ek turn ho (claim, phir use complicate/prove karne wali cheez), (3) ek line par khatm ho, trail-off par nahi. Short ke liye NAYI pehli line likho (purani line context maangti hai jo is viewer ke paas nahi) aur score karo
- **Kyun:** 'Best moment' ka clip aksar context ke bina marta hai; survive wahi karta hai jo akele khada ho
- **Kitni baar:** Har candidate Short par teeno shartein lazmi
- **Evidence:** 🟠 — yt-shorts ki selection rule
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`
- **Check:** `{"kind": "duration_range_s", "what": "short_span", "min": 20, "max": 55}`

### R-074 — Paach-beat spine (demo/launch videos) ⚙️
- **Purana ID:** C-050
- **Kab:** Demo, announcement ya launch video plan karte waqt
- **Kya:** Paach beats is order me rakho: Hook (pehle 3s — result/tension/claim, logo NAHI) → Problem (ek concrete dard) → Reveal (cheez kaam karti hui) → Proof (asli number/before-after, invented metric kabhi nahi) → CTA (ek action, ek URL). Beat sirf wajah ke saath drop karo; hook ke baad order mat badlo. Lambi walkthrough me Reveal+Proof har feature par repeat hota hai, Hook/Problem/CTA ek hi rehte hain
- **Kyun:** Ye order viewer ke faisle ki seedhi hai: rukna, dard pehchanna, jawab dekhna, yakeen karna, kadam uthana
- **Kitni baar:** Har demo/launch video par
- **Evidence:** 🟠 — SkillMedev video-storyboard ki spine rule
- **Sources:** `github_SkillMedev_skills.md`
- **Check:** `{"kind": "hook_within_s", "value": 3}`

### R-075 — Scene order causality par — therefore/but, and-then nahi
- **Purana ID:** C-052
- **Kab:** Beats/scenes ka order tay karte waqt
- **Kya:** Har beat pichle se caused ho aur agle ko cause kare — 'therefore / but' ki chain banao. 'And then, and then' wali chain sagging story ki structural nishani hai; sag ko naye events jod kar mat sudharo, connectives dobara banao
- **Kyun:** Causality hi woh cheez hai jo sequence ko kahani banati hai; bina uske beech hamesha sag karega
- **Kitni baar:** Har beat transition par
- **Evidence:** 🟠 — SkillMedev story-structure-architect ki diagnostic rule (fiction se aayi, video structure par lagu)
- **Sources:** `github_SkillMedev_skills.md`

### R-076 — Load-bearing turns ki jagah (percentages)
- **Purana ID:** C-053
- **Kab:** Lambi kahani/format ki macro structure banate waqt
- **Kya:** Bade turns ko in hisson ke aas-paas rakho: inciting incident pehle 10-12% ke andar; first-act break / point of no return ~20-25%; midpoint ~50% (reversal jo stakes uthaye aur goal ko recontextualize kare — sirf time mark karne wala midpoint sag ki jad hai); all-is-lost ~75-80%; phir climax aur resolution. First-act break 30% ke paar ya midpoint 60% ki taraf sarka ho to interrogate karo
- **Kyun:** Ye jagahen darshak ki umeedon ki ghadi se mili hui hain; mod der se aaye to beech ka hissa dheela padta hai
- **Kitni baar:** Har lambi structure par
- **Evidence:** 🟠 — Percentages guides hain, law nahi — source khud kehta hai; screenwriting craft convention
- **Sources:** `github_SkillMedev_skills.md`
- **Takraav note:** Video par ye percentages seedha copy karna Step 3 me tay hoga — short/mid-form par ye scale badal sakta hai (dekho CONFLICTS.md)

### R-077 — Setups aur payoffs ka audit
- **Purana ID:** C-054
- **Kab:** Structure deliver/final karne se pehle
- **Kya:** Har payoff (twist, reveal, capability, object) ki list banao aur confirm karo wo pehle fairly plant hua hai — telegraph kiye bina. Har prominent setup ko dekho: ya payoff kare ya cut ho. Bina chalayi banduk (loaded gun) mat chhodo; bina plant kiya payoff kahin se mat lao. Coincidence protagonist ko museebat me daal sakta hai, use bacha kabhi nahi sakta
- **Kyun:** Unplanted payoff dhokha lagta hai, unpaid setup jhoothi ummeed; dono bharosa todte hain
- **Kitni baar:** Har structure par, delivery se pehle ek pass
- **Evidence:** 🟠 — story-structure-architect ki diagnostic checklist
- **Sources:** `github_SkillMedev_skills.md`

### R-078 — Tension curve — chadhai ke saath jaanboojh ki ghaatiyan
- **Purana ID:** C-055
- **Kab:** Poori video/kahani ki tension map karte waqt
- **Kya:** Tension ko beat-by-beat upar chadhate hue rakho, beech me saans ke liye deliberate valleys ke saath. Flatline = sag; shuru me hi max out = aage chadhne ki jagah nahi. Do paas wale beats ek hi intensity par hon to ek ko vary ya reorder karo; har bada turn pichle se zyada stakes uthaye
- **Kyun:** Curve hi viewer ki urja ka budget hai; ek-jaisi intensity aadat (habituation) ban jati hai
- **Kitni baar:** Har structure par ek diagnostic pass
- **Evidence:** 🟠 — story-structure-architect ki tension diagnostic; Cutting ke waves (C-002) se taal-mel hai lekin ye kahani-level par lagta hai, shot-level par nahi
- **Sources:** `github_SkillMedev_skills.md`

### R-079 — Thesis-breakdown format (runtime ke hisse)
- **Purana ID:** C-056
- **Kab:** Expert talking-head monologue ko format karte waqt
- **Kya:** Runtime ko in hisson me baanto: 0-8% Hook (sawaal wala hook title), 8-13% Rebuttal (kata hua shabd/mithak), 13-23% Cause (thesis card), 23-38% Mechanism (diagram), 38-54% Breakdown (ek-ek karke bullets), 54-64% Turn (saaf speaker — saans ki jagah), 64-77% Consequences, 77-86% Climax (pull quote + maximum zoom), 86-100% Ending (CTA). 73s ke monologue par validate hua format hai
- **Kyun:** Ye hissa-bandhwari viewer ko har charan par 'main kahan hu' ka jawab deti hai aur climax ke liye jagah bachati hai
- **Kitni baar:** Har thesis-style monologue par
- **Evidence:** 🟠 — blazerior storyboard ki ek video (73s→68s) par validated format table
- **Sources:** `github_blazerior_videoediting-claude-skill.md`

### R-080 — Hafte ka mix — cadence jo 12 hafte chal sake
- **Purana ID:** C-065
- **Kab:** Upload plan/calendar banate waqt
- **Kya:** Mix stage ke hisaab se rakho: New (0-1k) 1 long-form + 4-5 Shorts; Growing (1k-50k) 1 long-form + 3 Shorts; Established (50k+) 1-2 long-form + 2-3 Shorts. Cadence wahi chuno jo kam se kam 12 hafte nibh sake — consistency volume ko harati hai. Har slot pre-paired ho: format, title angle, thumbnail angle, hook formula, goal (CTR/retention/subscribe — hafta teeno me banta ho, ek hi note nahi), posting window. Shorts ka long-form library se through-line lazmi. Ek anchor video hafte ka kendr, ek cheap video maujud cheez se, Shorts anchor se katein. Week slip ho to Short chhodo, long-form kabhi nahi
- **Kyun:** Shorts reach laate hain, long-form watch-time aur wafadar subscriber; bina through-line ke dono audiences alag marte hain
- **Kitni baar:** Har hafte ke plan par; mix ka review har 4 hafte
- **Evidence:** 🟠 — serge planner/pillars + Jake yt-plan ki cadence rules; ratios 'reported' starting points hain
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`

### R-081 — Community posts — pehli line hook, ek hi ask
- **Purana ID:** C-066
- **Kab:** Uploads ke beech community tab par post karte waqt
- **Kya:** Pehli line poora hook carry kare (feed truncate karta hai). Ek post = ek clear ask (vote, ek specific comment, ya video dekho) — do asks response baant dete hain. Poll: 2-4 options, mutually exclusive, koi false dilemma nahi. Hafte me 2-4 posts kaafi; lagbhag aadhi posts aane wale/recent video se judi hon (tease ya follow-up). Engagement bait ('comment 1 for yes') banned
- **Kyun:** Community tab between-uploads ka touchpoint hai — channel ko garm rakhta hai aur agle video ke early signals seed karta hai
- **Kitni baar:** Hafte me 2-4; har post par ek ask
- **Evidence:** 🟠 — serge community-post-writer ki rules
- **Sources:** `github_sergebulaev_youtube-skills.md`

### R-082 — Comments se next video — 3+ baar wahi sawaal
- **Purana ID:** C-068
- **Kab:** Comments padh kar content ideas nikalte waqt
- **Kya:** Comments ko themes me baanto; jo alag sawaal 3 ya zyada baar aaye, wahi next-video candidate hai — use potential title ke roop me naam do. Ek baar aaya comment trend nahi hota. Repeat commenters (superfans) ko naam se reply karo. Critical-but-specific comments sabse kaam ke hain — unhe dabao mat, surface karo. Pin us sawaal ko karo jo sabse zyada logon ka hai, sabse pyaare wale ko nahi
- **Kyun:** Comment section retention surface bhi hai aur demand signal bhi; dohraya sawaal hi sabit demand hai
- **Kitni baar:** Har video ke comments par ek pass
- **Evidence:** 🟠 — serge audience-insights + Jake yt-comment ki triage rules
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`

### R-083 — Repurpose — spine nikalo, copy-paste kabhi nahi
- **Purana ID:** C-069
- **Kab:** Blog/thread/post ko YouTube surface me badalna ho
- **Kya:** Source ka shell utaaro aur ek claim/story/number (spine) nikalo. Payoff se lead karo — source ka hook lagbhag kabhi survive nahi karta, use dobara likho. Listicle/numbered thread description me chapters ban jata hai (ek item = ek chapter). Off-platform artifacts ('link in bio', hashtag walls, dusri jagah ke @-handles, 'as I posted on...') sab hatao. Source ke claim, facts aur numbers bilkul na badlo — delivery badalti hai, matlab nahi
- **Kyun:** Galat platform ka format YouTube par marta hai; shabdon ko nahi, point ko carry karna hi repurposing hai
- **Kitni baar:** Har repurpose par
- **Evidence:** 🟠 — serge repurposer ki native-fit rules
- **Sources:** `github_sergebulaev_youtube-skills.md`

### R-084 — Outlier research — channel ke apne median ka multiple
- **Purana ID:** C-070
- **Kab:** Niche me 'kya chal raha hai' research karte waqt
- **Kya:** Videos ko raw views se rank mat karo — har video ko uske APNE channel ke median views ke multiple se rank karo (default threshold 1.5x-2x). Jis channel ke 4 se kam videos jama hon, use skip karo — 1-2 videos ka median, median nahi hota. Har outlier ke title ka formula naam do, lekin yaad rakho: formula TITLE ke shabdon par judgement hai, video ke chalne ki wajah ka dawa nahi
- **Kyun:** Raw views channel ka size naapte hain, idea ko nahi; median-multiple hi video ke baare me sawal ka jawab deta hai
- **Kitni baar:** Har niche research par
- **Evidence:** 🟠 — swipe.py ki ranking method; statistical common sense, measured study nahi
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`

### R-085 — Peaks ki hifazat — laugh/punchline ke aage reaction tak
- **Purana ID:** C-094
- **Kab:** Comedy/emphasis wale beats cut karte waqt
- **Kya:** Hansi, punchline aur emphasis beats ko poora rakho; punchline ke aage reaction tak extend karo — hasi hi asal beat hai. Audio events ((laughs), (sighs), (applause)) beats ke signal hain, unke aage bhi badhao
- **Kyun:** Peak ko kaatna video ka sabse keemti pal kaatna hai; reaction bina punchline adhoora rehta hai
- **Kitni baar:** Har peak par
- **Evidence:** 🟠 — video-use cut-craft ki rule
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`

### R-086 — Structural archetypes — shape pehle chuno
- **Purana ID:** C-103
- **Kab:** Multi-take/multi-clip video assemble karte waqt
- **Kya:** Pehle ek archetype chuno (ya material ke hisaab se banao) aur beats usi se rakho: Tech launch/demo: HOOK → PROBLEM → SOLUTION → BENEFIT → EXAMPLE → CTA. Tutorial: INTRO → SETUP → STEPS → GOTCHAS → RECAP. Interview: (QUESTION → ANSWER → FOLLOWUP) repeat. Travel/event: ARRIVAL → HIGHLIGHTS → QUIET MOMENTS → DEPARTURE. Documentary: THESIS → EVIDENCE → COUNTERPOINT → CONCLUSION. Music: INTRO → VERSE → CHORUS → BRIDGE → OUTRO. Beats ko source clip ke order se nahi, beat ke order se jodo
- **Kyun:** Bina shape ke assembly sirf kronologi banti hai; archetype har take ko uski jagah deta hai
- **Kitni baar:** Har assembled video par
- **Evidence:** 🟠 — video-use editor brief ke archetypes — craft templates
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Takraav note:** SkillMedev ke 5-beat spine (C-050) se overlap hai — C-050 demo-specific hai, ye general archetype set hai (dekho CONFLICTS.md)



### R-263 — Match cut — katne wale do shots me ek rishta rakho *(naya — editor round)*
- **Purana ID:** D1-002
- **Kab:** Do shots ke beech cut lage aur seedha cut kamzor lage
- **Kya:** Match cut ki 4 kismo me se ek rakho — graphic (shape), movement, sound, ya idea/concept match
- **Kyun:** Bina rishte ka cut darshak ko jhatka deta hai; match se do alag shots ek soch ban jate hain
- **Kitni baar:** Har kamzor cut par kam se kam ek match prakar
- **Evidence:** 🟠 — Editor craft parampara (note)
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`

### R-277 — Comedy incident ki 4-act ghadi ⚙️ *(naya — editor round)*
- **Purana ID:** D1-016
- **Kab:** Koi comedy incident/mazaak wala pal kata jaye
- **Kya:** Incident ko ek lagatar 4-act ghatna ki tarah kaato: Premise/Setup 2.0–3.5 s (max 4.0) → Escalation 1.5–3.0 s (max 3.5) → Punchline/Climax 1.5–2.5 s (max 3.0) → Aftermath/Reaction 2.0–4.0 s (max 4.5); kul lambai 8–14 s (zyada se zyada 15 s)
- **Kyun:** Comedy ka samay hi uski jaan hai — setup chhota to prediction nahi banti, reaction chhota to hasi nahi uthti
- **Kitni baar:** Har comedy incident par ye ghadi
- **Evidence:** 🟠 — Suite ki measured-si craft ghadi (note); koi published study nahi
- **Sources:** `notes_mmmnhat_agent-skills.md (note)`
- **Check:** `{"kind": "duration_range_s", "what": "comedy_incident_total", "min": 8, "max": 14}`
- **Takraav note:** koptsev63 ki pacing table comedy beat ko 4–5 s kehti hai (D1-075) — wo ek shot/beat ki baat hai, ye poore incident (4 acts) ki; dono ka paimana alag hai, Step 3 addendum me saaf ho

### R-278 — Reaction ko bachao — punchline ke baad kam se kam 1.5 s ⚙️ *(naya — editor round)*
- **Purana ID:** D1-017
- **Kab:** Comedy/action ke climax ke baad ka hissa kata jaye
- **Kya:** Vaardaat ke baad kam se kam 1.5 s ka reaction rakho; OUT sirf tab lo jab reaction settle ho jaye; reaction ko beech me kaatna sakht mana hai
- **Kyun:** Darshak ki hasi/ehsaas reaction me hi poora hota hai — use kaatna matlab punchline ko aadha karna
- **Kitni baar:** Har climax ke baad, bina apvaad
- **Evidence:** 🟠 — Craft rule (note)
- **Sources:** `notes_mmmnhat_agent-skills.md (note)`
- **Check:** `{"kind": "min_gap_s", "what": "reaction_after_event", "value": 1.5}`

### R-279 — Ek incident = ek hi lagatar cut; lambi scene me climax window ⚙️ *(naya — editor round)*
- **Purana ID:** D1-018
- **Kab:** Comedy incident ya isolated scene ka hissa chunna ho
- **Kya:** Ek incident ko ek hi lagatar cut rakho (4–11 s). Agar isolated scene 9 s se lambi ho to window climax ke aas-paas rakho: peak se 4 s pehle se peak ke 3.5 s baad tak. Bahut tang window (sirf peak −1.5 s) kabhi mat lo — premise mar jayegi
- **Kyun:** Beech se kaata incident apna setup kho deta hai; climax window me poori chhoti kahani bachti hai
- **Kitni baar:** Har incident/scene-isolation par
- **Evidence:** 🟠 — Craft rule (note)
- **Sources:** `notes_mmmnhat_agent-skills.md (note)`
- **Check:** `{"kind": "duration_range_s", "what": "comedy_single_cut", "min": 4, "max": 11}`

### R-283 — Chhote target par W-curve reordering *(naya — editor round)*
- **Purana ID:** D1-022
- **Kab:** 30 s jaise chhote target ke liye clips sajane hon
- **Kya:** Clips ko chronological kram ki jagah retention curve (W-curve) ke hisaab se dobara sajao — ya tez chronological fast-cut rakho; beech ka aadha-adhura kram nahi
- **Kyun:** Chhoti video me har second ko darshak ko pakadna hai; seedha chronological kram sabse mazboot pal ko beech me dubo deta hai
- **Kitni baar:** Har short-target compilation par
- **Evidence:** 🟠 — Suite ki retention soch (note)
- **Sources:** `notes_mmmnhat_agent-skills.md (note)`

### R-290 — Selects pehle, master baad me *(naya — editor round)*
- **Purana ID:** D1-029
- **Kab:** Kisi naye project ki edit shuru ho (Premiere/AE dono)
- **Kya:** Pehle bins/labels/markers ke saath ek selects sequence banao; structural beats aur shot ke maksad par markers lagao; master sequence uske baad hi banao
- **Kyun:** Seedha master banane se chunav aur banawat ek dusre me ghul jate hain aur galti mehngi padti hai
- **Kitni baar:** Har project me ek baar, shuruaat me
- **Evidence:** 🟠 — Workflow discipline (MIT skill notes)
- **Sources:** `github_MuhammadAsad809_AI-EDITING-SKILL.md`

### R-306 — Motion piece = beats ki shrinkhala, ek lambi animation nahi ⚙️ *(naya — editor round)*
- **Purana ID:** D1-045
- **Kab:** 10–15 s ka koi motion piece/intro/title sequence bane
- **Kya:** Use 3–6 alag beats ki shrinkhala ki tarah banao — har beat visual roop se padhne layak, ek hi visual system ke andar; final lockup ko padhne layak samay do
- **Kyun:** Ek lambi behlti animation me koi pal yaad nahi rehta; beats ki shrinkhala hi chhoti kahani banti hai
- **Kitni baar:** Har 10–15 s motion piece par 3–6 beats
- **Evidence:** 🟠 — Motion-direction craft (MIT skill)
- **Sources:** `github_SebastianBoehler_autoresearch_after_effects_finetune.md`
- **Check:** `{"kind": "duration_range_s", "what": "motion_sequence", "min": 10, "max": 15}`

### R-341 — Idea cut jaan-boojh ke — jahaan matlab takkar se bane *(naya — editor round)*
- **Purana ID:** D1-080
- **Kab:** Documentary/teaser/montage me do shots jodne hon
- **Kya:** Wahan idea cuts lagao jahan do shots ki takkar se teesra matlab banta hai; narrative/continuity wali jagah par continuity cuts rakho — dono ko jaan-boojh ke alag rakho, galti se mishrit nahi
- **Kyun:** Idea cut hi montage ki jaan hai; galat jagah laga idea cut sirf gadbad lagta hai
- **Kitni baar:** Montage/teaser hisso me jaan-boojh ke
- **Evidence:** 🟠 — Film-editing craft (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`

### R-342 — Decisive moment — out-point us par ya uske just baad *(naya — editor round)*
- **Purana ID:** D1-081
- **Kab:** Har clip ka out-point tay ho
- **Kya:** Pehle clip ka decisive frame pehchano (jahan pal apne matlab par pahunchta hai); out-point ko usi par ya uske just baad rakho — usse pehle kabhi nahi
- **Kyun:** Decisive pal se pehle kaata clip apni baat aadhi keh kar ruk jata hai
- **Kitni baar:** Har clip par
- **Evidence:** 🟠 — Film-editing craft (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`

### R-351 — Repeated take me sirf ek — aakhri complete take *(naya — editor round)*
- **Purana ID:** D1-090
- **Kab:** Ek hi passage ke kai takes/repeats hon
- **Kya:** Direction/setup wali chatter hamesha kaato; repeated passages me bilkul ek hi take rakho — aakhri complete take
- **Kyun:** Do aadhe takes jodne se behtar ek poora take hai; chatter kahani ko sirf dheema karti hai
- **Kitni baar:** Har repeated passage par
- **Evidence:** 🟠 — Rough-cut craft (MIT skill)
- **Sources:** `github_ZeusSheen_ppro-agent-bridge.md`

### R-358 — Chapter ka 5-beat spine *(naya — editor round)*
- **Purana ID:** D2-001
- **Kab:** Har chapter (travel/long-form) ki planning aur review par
- **Kya:** Har chapter me paanchon beat hon: context, movement, lived-in texture, destination payoff, aftertaste/handoff. Jo beat gayab ho, use pehle footage se repair karo — effects ya BGM hit se kabhi nahi
- **Kyun:** Chapter sirf jagah ki list ban jata hai to viewer ko safar mehsoos nahi hota; movement aur texture hi kahani ko aage badhate hain
- **Kitni baar:** Har chapter = 5/5 beats; missing beat = structure kaam, effect ka kaam nahi
- **Evidence:** 🟠 — Ek travel-studio skill ka house structure contract; koi measured corpus nahi
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-359 — Opening: 40s me vaada, 60s me saboot ⚙️ *(naya — editor round)*
- **Purana ID:** D2-002
- **Kab:** Video ke pehle minute me, khaas taur par travel/long-form opening me
- **Kya:** Pehle 40 second me asli destination/route footage par viewer promise rakho; pehle 60 second ke andar readable destination proof do (aerial, skyline, coast ya landmark)
- **Kyun:** Pehla minute hi decide karta hai ki viewer rukega ya jayega; vaada bina saboot ke clickbait lagta hai
- **Kitni baar:** Promise ≤40s; destination proof ≤60s
- **Evidence:** 🟠 — House opening contract; koi platform data nahi
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "hook_within_s", "max_s": 60, "what": "destination proof"}`

### R-360 — Pehle 3 minute: arrival aur texture, payoff se pehle *(naya — editor round)*
- **Purana ID:** D2-003
- **Kab:** Opening ke baad pehle chapter tak ke hisse me
- **Kya:** Minute 3 se pehle practical arrival dikhao (station, hotel, street) aur pehle chapter payoff se pehle lived-in texture rakho; pehla handoff movement/street/hotel/food/weather/signage bridge se ho, hard reset se nahi
- **Kyun:** Viewer ko pehle jagah par 'pahuncha' hua mehsoos hona chahiye, tabhi payoff ka matlab banta hai
- **Kitni baar:** Arrival <3:00; texture hamesha pehle payoff se pehle
- **Evidence:** 🟠 — House opening contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-361 — Long-form ki ghadi: 20-minute wali shape *(naya — editor round)*
- **Purana ID:** D2-004
- **Kab:** Long-form travel film (target ~20 min) ki structure planning me
- **Kya:** Shape rakho: opening route promise 35–60s, 4–6 main chapters har ek 2.5–5 minute, transitions 15–45s, ending 45–75s callback/aftertaste ke saath. 1–2 minute ki short-video pacing long-form par default nahi
- **Kyun:** Lambi film ko saans aur route chahiye; short pacing se 20 minute ki film thaka deti hai
- **Kitni baar:** Opening 35–60s; chapter 2.5–5 min; transition 15–45s; ending 45–75s
- **Evidence:** 🟠 — Ek reference-style (Bilibili long-form travel) se liya house target; measured nahi
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-362 — Har chapter ko barabar time nahi *(naya — editor round)*
- **Purana ID:** D2-005
- **Kab:** Chapter durations tay karte waqt
- **Kya:** Jis chapter ke paas strong footage, rich human moments, saaf local texture ya zyada route-matlab hai, use zyada time do; kamzor chapter sirf bridge ki bhumika me chhota rahe
- **Kyun:** Barabar time dene se film calendar jaisi lagti hai, kahani jaisi nahi
- **Kitni baar:** koi fixed ratio nahi; strong chapter > bridge chapter hamesha
- **Evidence:** 🟠 — House structure niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-363 — Payoff-se-payoff jump = slideshow *(naya — editor round)*
- **Purana ID:** D2-006
- **Kab:** Chapter boundaries aur bade jagah-badal par
- **Kya:** Ek payoff shot ke seedha dusre payoff shot par mat jao — beech me movement/texture support rakho. Aftertaste hamesha chapter ke AAKHIR me rakho, shuru me nahi
- **Kyun:** Sirf 'best shots' jodne se tourist slideshow banta hai; beech ka safar hi film hai
- **Kitni baar:** Har chapter boundary par ≥1 movement/texture support shot
- **Evidence:** 🟠 — House scene-flow contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-364 — Route task-chain hamesha samajh aaye *(naya — editor round)*
- **Purana ID:** D2-007
- **Kab:** Departure/arrival jaise practical chapters (hotel→airport→flight) me
- **Kya:** Chain ko padhne layak rakho: leave → handoff → travel → arrive → process → threshold → new state. Viewer ko har pal current jagah, current action aur agli manzil pata ho. Action continuity (haath, samaan, darwaze, signs, chalne ki disha) effect continuity se zyada mazboot join hai
- **Kyun:** Practical safar ki kahani kaam ke steps se banti hai; ek step gayab ho to viewer kho jata hai
- **Kitni baar:** Har phase ke paas ≥1 pehchan wala anchor shot
- **Evidence:** 🟠 — Ek 6:13 homeward film ki poori review se nikali grammar (non-copying profile)
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-365 — Ending nayi state par, 3–6s thehrao ke saath ⚙️ *(naya — editor round)*
- **Purana ID:** D2-008
- **Kab:** Video/chapter ke aakhiri shot par
- **Kya:** Ending wahan rakho jahan traveller kisi nayi state me pahunch jaye (seat, window, arrival); uske baad suitable footage ho to 3–6 second stable aftertaste hold rakho. Chalte hue movement ke beech abrupt cut se khatam mat karo
- **Kyun:** Badli hui halat par rukna hi band hone ka ehsaas deta hai
- **Kitni baar:** Final hold 3–6s (footage ho to)
- **Evidence:** 🟠 — Usi homeward review se; house niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "duration_range_s", "min_s": 3, "max_s": 6, "what": "ending aftertaste hold"}`

### R-366 — Story plan cutting se pehle; beech-idea cut kabhi nahi *(naya — editor round)*
- **Purana ID:** D2-009
- **Kab:** Koi bhi talking-head/social edit shuru karne se pehle
- **Kya:** Pehle story plan likho: hook/agenda → body beats → recap/CTA ('jo bologe wo batao, batao, phir bataya hua dohrao'). Duration ghataane ke liye idea ko beech se kabhi mat kaato; word-boundary edits ki jagah lambe coherent blocks ko tarjeeh do
- **Kyun:** Plan bina kaatne se achhe hisse kat jate hain aur baat adhoori reh jati hai
- **Kitni baar:** Har video = 1 story plan pehle; mid-idea cut = 0
- **Evidence:** 🟠 — Editor ke production standard se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-367 — Narration sparse rakho, khamoshi ko kaam karne do *(naya — editor round)*
- **Purana ID:** D2-010
- **Kab:** Long-form travel narration likhte waqt
- **Kya:** Spoken paragraphs sparse rakho; 20-minute film me voiceover kul chand minute hi ho sakta hai. 20–60 second ke hisse aise chhodo jahan sirf source audio, BGM aur visuals film ko aage le jayein. Jo dikh raha hai use bolkar mat samjhao
- **Kyun:** Har cheez bol dene se film lecture ban jati hai; nazara khud bhi bolta hai
- **Kitni baar:** Quiet stretches 20–60s; narration kabhi wall-to-wall nahi
- **Evidence:** 🟠 — House narration style
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-368 — Reference se seekho, copy nahi; route par imaandari *(naya — editor round)*
- **Purana ID:** D2-011
- **Kab:** Kisi reference film ko style guide banate waqt
- **Kya:** Reference se pacing, structure aur rhythm seekho — uske titles, narration lines, music ya footage copy kabhi nahi. Location pakka na ho to narration/plan me confidence bhasa rakho: confirmed / visually likely / route scaffold only / needs human review
- **Kyun:** Copy ki hui pehchan pakdi jati hai aur galat location film ki sachchai tod deta hai
- **Kitni baar:** Copy = 0; har uncertain location par confidence label
- **Evidence:** 🟠 — House non-copying + route-honesty contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-369 — Footage selection selective rakho, local pehle *(naya — editor round)*
- **Purana ID:** D2-012
- **Kab:** Pehli assembly se pehle footage chunte waqt
- **Kya:** Clip sirf isliye timeline me nahi aata ki woh exist karta hai. Pehle local footage, stock baad me. Kisi clip ko final reject karne se pehle full-duration, in-motion review karo — filename/metadata sirf review ke hints hain, faisla nahi
- **Kyun:** Sab kuch daal dene se film bhari ho jati hai; aur bina dekhe reject karne se best moment haath se jata hai
- **Kitni baar:** Har final reject = full in-motion review ke baad hi
- **Evidence:** 🟠 — House footage-select contract (temporal scan ka ~99.5% coverage bar usi skill ke acceptance criteria me hai)
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-370 — Kharaab-par-unique clip, saaf generic scenic se upar *(naya — editor round)*
- **Purana ID:** D2-013
- **Kab:** Do clips me se ek chunna pade to
- **Kya:** Technically imperfect lekin unique story/emotion wala clip saaf lekin generic scenic shot se upar rank karo
- **Kyun:** Viewer ko perfection nahi, pal yaad rehta hai
- **Kitni baar:** Tie-break rule: story/emotion > technical saafai
- **Evidence:** 🟠 — House selection niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-371 — Shot tiers aur function ka badlav *(naya — editor round)*
- **Purana ID:** D2-014
- **Kab:** Creator cut / clip classification me
- **Kya:** Har clip ko tier do: Hero / Main / Texture-bridge / Utility / Reject. Ek hi function wale do adjacent clips ke beech alag function wala clip daalo
- **Kyun:** Ek hi kaam ke shots lagatar aane se film ek-ras (monotone) ho jati hai
- **Kitni baar:** Adjacent same-function pair = 0 (beech me alag function)
- **Evidence:** 🟠 — House creator-cut contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-372 — B-roll = saboot, sajawat nahi *(naya — editor round)*
- **Purana ID:** D2-015
- **Kab:** Cutaway/B-roll lagate waqt
- **Kya:** Har B-roll ke saath uska claim/beat/problem note karo — woh kis baat ka saboot hai ya kis cut ko dhak raha hai. B-roll pehle dhoondo aur WATCH karo, phir action/story ke hisaab se kaato; filler ke liye kabhi nahi
- **Kyun:** Bina-kaam ka B-roll viewer ko turant 'stock' lagta hai aur bharosa todta hai
- **Kitni baar:** Har cutaway = 1 documented purpose
- **Evidence:** 🟠 — Do alag editor sources ka ek hi niyam (production standard + vlog workflow note)
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`, `notes_appariciojunior_video-editor-skills.md (note)`

### R-373 — Rough cut me editor-notes aur punchlines bachaao *(naya — editor round)*
- **Purana ID:** D2-016
- **Kab:** Rough cut me retakes/dead air saaf karte waqt
- **Kya:** Speaker ki khud ki 'notes-to-editor' wali baatein aur punchlines ko galti se mat kaato — ye hamesha protect list me rakho
- **Kyun:** Ye woh hisse hain jo creator ne jaan-bujh kar rakhe hain; kaatna = kahani ka nuksaan
- **Kitni baar:** Protect list = har rough cut se pehle tay
- **Evidence:** 🟠 — Note source: editor workflow apne shabdon me
- **Sources:** `notes_appariciojunior_video-editor-skills.md (note)`

### R-374 — Screencast: shuru 15–30s 'kya aur kyun', aakhir me uplabdhi ⚙️ *(naya — editor round)*
- **Purana ID:** D2-017
- **Kab:** Screen-recording/tutorial videos me
- **Kya:** Pehle 15–30 second me batao kya bana rahe hain aur kyun. Aakhir me accomplishment/diff summary do — video beech safar me khatam mat karo
- **Kyun:** Viewer ko manzil pehle pata ho to beech ke steps sehne layak ho jate hain
- **Kitni baar:** Opening context 15–30s; closing summary hamesha
- **Evidence:** 🟠 — Ek screencast editor ki house style
- **Sources:** `github_matthull_my-skills.md`
- **Check:** `{"kind": "duration_range_s", "min_s": 15, "max_s": 30, "what": "screencast opening context"}`

---

## SAMAJH — baat samajh aaye, kuch chhupe nahi

### R-087 — Chapters ke platform niyam ⚙️
- **Purana ID:** A-016, C-046
- **Kab:** Lambi video (tutorial, podcast, explainer, lamba vlog) publish karte waqt, description me chapters likhte samay
- **Kya:** Pehla timestamp/chapter 00:00 par ho, kam se kam 3 chapters ascending order me, har chapter kam se kam 10 second ka; timestamps edit ke asli times se lo, aankh se naap kar nahi. Har chapter ka title topic-words nahi, us section ka promise ho — 3-5 shabdon me, creator ki awaaz me; jo section 5 shabdon me naam na paye, wo ya do sections hai ya filler hai
- **Kyun:** Ek bhi platform niyam toota to chapter block render hi nahi hota — description me pada reh jata hai; sahi chapters viewer ko apne kaam ke hisse par seedha jump karate hain, wapas aana aasan karte hain, aur retention diagnostic ka kaam bhi karte hain (Guo 2014 me bhi yahi pattern)
- **Kitni baar:** Har long-form video par (Shorts par chapters nahi)
- **Evidence:** 🟡 — 00:00 / 3+ / 10s YouTube ke apne documented platform rules hain; 3-5 shabd wala promise-title hissa craft hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Jakeschincariol_youtube-agent-skill.md`, `github_sergebulaev_youtube-skills.md`
- **Check:** `{"kind": "min_chapter_duration_s", "value": 10}`

### R-088 — B-roll exactness: bola wahi dikhe
- **Purana ID:** A-028
- **Kab:** Voice jo naam le use dikhaya ja sakta ho to
- **Kya:** B-roll/punch wahi cheez literally dikhaye jo boli gayi (spoken noun phrase); exact asset na mile to speaker par hi raho — same-category ki tasveer (kisi bhi darwaze se 'hidden door') fallback nahi, defect hai; photo tabhi jab human-confirmed subject match kare, aur video hamesha photo se pehle
- **Kyun:** Alag ya sajawati visual dhyaan todta hai aur comprehension girata hai; exact visual baat ko pakka karta hai
- **Kitni baar:** Har punch/B-roll par
- **Evidence:** 🟢 — Mayer (2008, peer-reviewed) ka coherence principle; mktkit ka owner rule ('exact or nothing', 2026-09-07) iska sakht roop hai — woh hissa 🟠
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`

### R-089 — Graphic sirf jab samjhaye
- **Purana ID:** A-029
- **Kab:** Koi graphic ya on-screen text jodne se pehle
- **Kya:** Graphic sirf tab: (1) jo camera nahi dikha sakta woh dikhana ho (concept, comparison, number, timeline, map), ya (2) structure mark karna ho (section title, naam, step counter); jo graphic hatane se kuch na ghate woh hatao; voice ki baat ko text me mat dohrao — text woh ho jo bola nahi gaya (naam, number, key term)
- **Kyun:** Shabd + tasveer saath sikhati hai, lekin bekaar graphic aur dohra hua text dono seekhna aur samajh girate hain
- **Kitni baar:** Har graphic par
- **Evidence:** 🟢 — Mayer (2008, peer-reviewed) — multimedia, coherence aur redundancy principles
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-090 — Graphic kabhi khaali nahi, word se bandha ho ⚙️
- **Purana ID:** A-030
- **Kab:** Koi card, table ya graphic screen par aaye to
- **Kya:** Graphic use shabd se zyada se zyada 0.5 s pehle enter kare jo use introduce karta hai; pehla content element 1 s ke andar aa jaye; har row/element us shabd ke ≤0.6 s ke andar enter kare jo use naam de; koi card 1 s se zyada khaali na rahe; aakhri phrase ke ~1.2 s baad graphic chala jaye; elements even stagger se nahi, shabdo se bandh kar aayein
- **Kyun:** Khaali frame intezaar karta hua graphic galti lagta hai aur viewer ka dhyaan wahi atakta hai
- **Kitni baar:** Har graphic par
- **Evidence:** 🟠 — kmilo house rules (reference tutorial ke pehle cut ki review se bane)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "max_lead_s", "what": "graphic_before_its_word", "value": 0.5}`

### R-091 — On-screen text ka reading-time formula ⚙️
- **Purana ID:** A-031
- **Kab:** Koi bhi text screen par rahe to
- **Kya:** Text ki duration = max(1.5 s; words × 0.33 s + 0.5 s) rakho (0.33 s/shabd = 160-180 wpm padhne ki gati); jo label voice ke saath jata hai woh apne shabd ke saath enter kare aur bole jaane ke 0.6 s baad tak rahe — formula se kam kabhi nahi
- **Kyun:** Jaldi gayab text padha hi nahi jata; padhne se pehle use dhoondhne ka bhi samay lagta hai (+0.5 s isiliye)
- **Kitni baar:** Har text event par
- **Evidence:** 🟡 — BBC subtitle guidelines (160-180 wpm) se derived; +0.5 s aur label wala hissa kmilo house
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "formula", "what": "on_screen_text_duration_s", "expr": "max(1.5, words*0.33+0.5)"}`

### R-092 — Captions ke standard specs ⚙️
- **Purana ID:** A-032
- **Kab:** Closed captions/subtitles banate waqt
- **Kya:** ≤42 characters per line, ≤2 lines; reading speed ≤20 characters/s (bachchon ke liye 17); har event ≥20 frames (≈0.83 s); events ke beech gap ≥2 frames; line break punctuation ke baad ya conjunction/preposition se pehle rakho — article ko noun se, pehle naam ko upnaam se kabhi mat todo
- **Kyun:** Ye duniya bhar ke broadcast specs hain — inse tez ya lambe captions padhe nahi jate
- **Kitni baar:** Har caption event par
- **Evidence:** 🟡 — Netflix Timed Text Style Guide (platform/broadcast spec)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_1610-advisory_mktkit.md`
- **Check:** `{"kind": "max_chars", "what": "caption_line", "value": 42}`
- **Takraav note:** mktkit vertical (1080 px wide) ke liye 32 chars × 2 lines rakhta hai kyunki wahan 42 fit nahi hota (DCMP Captioning Key bhi 32 kehta hai) — vertical me 32, 16:9 standard captions me 42 (dekho CONFLICTS.md)

### R-093 — Caption cue join cross na kare, shabd drop na ho
- **Purana ID:** A-033
- **Kab:** Captions ko edit points ke saath rakhte waqt
- **Kya:** Cue kabhi edit join ko cross na kare (har spine boundary par cue split karo); rakha hua koi shabd caption se drop na ho; speech agar cut ke 0.5 s ke andar shuru/khatm ho to cue ko cut par hi rakho, cross sirf tab jab speech khud cross kare
- **Kyun:** Join ke paar latka caption galti dikhta hai; range ke aakhir ke chhote shabd clamp me gayab hona ek asal defect raha hai
- **Kitni baar:** Har caption cue par
- **Evidence:** 🟡 — Netflix timing guide ke shot-change rules (platform spec) + mktkit ka engine-enforced house rule
- **Sources:** `github_1610-advisory_mktkit.md`, `github_kmilo93sd_agent-video-editor.md`

### R-094 — Burned-in social captions ka tareeka
- **Purana ID:** A-034
- **Kab:** Shorts/Reels/TikTok ke liye captions burn karte waqt
- **Kya:** Captions word-timed rakho; chunk chhota rakho; bola ja raha shabd accent color/highlight me dikhao; badi bold sans-serif, outline ya box ke saath; har page ≥20 frames rahe; jab board wahi shabd dikha raha ho to captions hide karo; numbers ko digits me likho (shabdon me nahi); caption engine ke defaults: min cue 0.8 s, max cue 2.8 s
- **Kyun:** 80%+ viewers muted ya kam awaaz me dekhte hain — wahan captions hi awaaz hain
- **Kitni baar:** Har short-form video par
- **Evidence:** 🟠 — Creator practice teeno sources me; muted-viewing wala aankda Melvynx shorts-codes ka (80%+)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_1610-advisory_mktkit.md`
- **Takraav note:** Chunk size par farak: Melvynx 1-3 words per chunk, kmilo 1-5 words per page — dono chalte hain, ek channel par ek hi style consistent rakho (dekho CONFLICTS.md)

### R-095 — Safe zones: text platform UI se bahar ⚙️
- **Purana ID:** A-035
- **Kab:** 9:16 video me text, captions ya CTA rakhte waqt
- **Kya:** Text aur key visuals platform UI bands ke bahar rakho. Universal 9:16 zone: x 9-91%, y 14-86%; hook text y 15-22%; captions/CTA y 78% se neeche nahi; right 14% me kuch zaroori nahi. Pixel hisaab (1080x1920, mktkit): IG/FB top 270 bottom 672, TikTok top 130 bottom 484, Shorts top 180 bottom 350 — kai platforms ke liye sabse sakht intersection lo aur caption MarginV = strictest bottom + 24 px. 1:1/16:9 me text beech ke 80% me rakho
- **Kyun:** UI ke neeche dabaa text padha hi nahi jata — ye retention nahi, seedha samajh ka nuksaan hai
- **Kitni baar:** Har text placement par; check number se karo (text safe jab y ≥14, y+h ≤79, x+w ≤86)
- **Evidence:** 🟡 — mktkit ke specs Meta/TikTok sourced (platform specs); ExpoCut ke % vendor-measured (Free to use and redistribute with attribution to expocut.com); Melvynx ke px zones house-measured
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "safe_zone_pct", "x_min": 9, "x_max": 91, "y_min": 14, "y_max": 79}`
- **Takraav note:** Sources ke numbers format aur platform ke hisaab se alag hain: Melvynx px (top 220, bottom 420, right 140 from y900) ExpoCut ke % aur mktkit ke px se thode alag hain — target platforms ka sakht intersection hi surakshit raasta hai (dekho CONFLICTS.md)

### R-096 — Phone par padhai: size aur contrast ⚙️
- **Purana ID:** A-036
- **Kab:** Koi text screen par aaye to
- **Kya:** Body text 1080p par ≥40-60 px uncha rakho; contrast ≥4.5:1; video ke upar text ko solid/scrim card ya outline do; label fit karne ke liye font chhota mat karo — label ke shabd chhote karo
- **Kyun:** Chhota ya halka text phone par gayab ho jata hai; jo padha na jaye woh information nahi, shor hai
- **Kitni baar:** Har text par; Melvynx ke floors: UI detail ≥34 px, labels 38-42 px, captions ~84 px
- **Evidence:** 🟡 — WCAG AA contrast 4.5:1 (WebAIM standard) + legibility.info; px floors creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`
- **Check:** `{"kind": "min_font_px", "what": "body_text_at_1080p", "value": 40}`

### R-097 — Boards illustrate karein, paraphrase nahi
- **Purana ID:** A-037
- **Kab:** Short me board/visual element lagate waqt
- **Kya:** Board sirf woh dikhaye jo dikhaya ja sakta hai: number, command, folder, asli logo, before/after, asli screen; bola hua paraphrase karke board mat banao; board par 2-4 shabd se zyada text nahi; teen text-board lagatar nahi; har board theek us shabd par land kare jo use naam de
- **Kyun:** Jo board baat ko dohraata hai woh screen bharta hai, samajh nahi; jo dikhata hai woh baat ko pakka karta hai
- **Kitni baar:** Har board par
- **Evidence:** 🟠 — Melvynx short-editing style.md ka house rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-098 — Tutorial me screen lead kare, voice follow
- **Purana ID:** A-038
- **Kab:** Screen tutorial edit karte waqt
- **Kya:** Screen jo dikhaye voice wahi kahe, usi pal: phrase tab aaye jab uska action screen par ho; phrase action se lambi ho to result ko usi second par freeze karo; clip kabhi peeche na jaye, na kisi chhode hue clip par wapas aaye
- **Kyun:** Shabd aur tasveer ka saath (temporal contiguity) hi tutorial ko follow karne layak banata hai; aage-peeche hona sabse bada confusion hai
- **Kitni baar:** Tutorial ki har phrase par
- **Evidence:** 🟠 — kmilo house rule (reference tutorial review se); peeche Mayer ka temporal contiguity principle (🟢) khada hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-099 — Tutorial chapter cards aur edge badge ⚙️
- **Purana ID:** A-039
- **Kab:** Tutorial ke chapter badlein to
- **Kya:** Har chapter 3 s ke title card se khule ('Step 2 of 5'), card ka content 0.55 s me enter kare; screen par step ke naam ka edge badge rakho taaki beech me land karne wale ko jagah samajh aaye; chapter ke andar hard cuts hi rakho
- **Kyun:** Tutorial viewers hisse dohraate aur jump karte hain; bade, saaf markers unhe sahi jagah pahunchaate hain
- **Kitni baar:** Har chapter par
- **Evidence:** 🟠 — kmilo house rule; Guo 2014 (🟡) ka bade-text-at-transitions wala support
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "duration_range_s", "what": "chapter_title_card", "min": 3, "max": 3}`

### R-100 — Lower third pehli pehchan par
- **Purana ID:** A-040
- **Kab:** Podcast/interview me koi vyakti pehli baar dikhe to
- **Kya:** Us vyakti ka naam aur role lower third me dikhao, aur lambe break ke baad dobara dikhao
- **Kyun:** Bina pehchan ke viewer baat ko sahi insaan se jod nahi pata
- **Kitni baar:** Har naye speaker ki pehli appearance par
- **Evidence:** 🟠 — kmilo podcast recipe ka creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-101 — Auto captions review zaroor karo
- **Purana ID:** A-041
- **Kab:** Publish se pehle captions finalize karte waqt
- **Kya:** YouTube ke auto captions ko bina review publish mat karo (accent, dialect, background noise se woh speech ko galat dikha sakte hain) — caption file upload karo ya auto wali sudharo; burned-in ho to word-by-word check karo; numbers hamesha video se verify karo
- **Kyun:** Galat caption samajh ko ulta kar deta hai, aur burn ho jaye to galti permanent dikhti hai
- **Kitni baar:** Har video, publish se pehle
- **Evidence:** 🟡 — YouTube official auto-caption warning (platform) + Melvynx clips ki practical chetaavni
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-102 — Music awaaz se 18-25 dB neeche ⚙️
- **Purana ID:** A-042
- **Kab:** Bolne ke neeche music lage to
- **Kya:** Background music ko voice se 18-25 dB neeche rakho (voice -16 LUFS ho to music lagbhag -34/-41 LUFS)
- **Kyun:** Awaaz se ladta music seedha samajh khatm karta hai — viewer shabd pakadne me thakta hai
- **Kitni baar:** Jahan bhi speech ke neeche music hai
- **Evidence:** 🟠 — Creator source (Pure Audio Insight) kmilo ki tagging me; koi peer-reviewed number nahi
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "db_range", "field": "music_db_under_voice", "min": 18, "max": 25}`
- **Takraav note:** Melvynx ke measured style-copy me ek creator ka beat ~12 dB under naapa gaya tha — woh us style ka naapa hua apvaad hai; aam niyam 18-25 dB hi hai, copy karna ho to original ko naapo (dekho A-091) (dekho CONFLICTS.md)

### R-103 — Ducking: bolte waqt music 6-12 dB dabao
- **Purana ID:** A-043
- **Kab:** Speech ke neeche music chale to
- **Kya:** Jab koi bole to music ko 6-12 dB duck karo — soft attack 10-50 ms, release 250-700 ms (sidechain compressor, auto-ducking ya keyframes se); Melvynx ke mix defaults: bed -28 LUFS, duck ratio 0.5
- **Kyun:** Ducking se music rehta bhi hai aur shabd saaf bhi rehte hain; bina duck ke ya to music gayab ya awaaz dabti hai
- **Kitni baar:** Poore talking hisse par
- **Evidence:** 🟠 — Creator sources (Zella; Auphonic ka official default 18 dB apne tool ke liye hai — isiliye range 6-12 creator wali rakhi)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-104 — SFX ke level aur jagah ke niyam
- **Purana ID:** A-044
- **Kab:** Sound effect lagate waqt
- **Kya:** SFX voice se 12-24 dB neeche rakho; effect ka transient visual change se 2-4 frames pehle rakho taaki peak dikhne ke pal mile; key word (number, naam) ke upar effect kabhi nahi; ek hi sound lagatar 3 baar se zyada nahi; jo awaaz asal recording me pehle se kaam kar rahi hai (real click, darwaza) us par effect mat chadhao; gain ke default andaze: SFX ~15 dB, ambience ~30 dB under
- **Kyun:** Galat jagah ya zyada tez effect shabd ko kha jata hai; sahi jagah wala effect dikhne wali cheez ko pakka karta hai
- **Kitni baar:** Har effect par
- **Evidence:** 🟠 — Creator sources (Storyblocks) + kmilo library ke house defaults
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-105 — Master loudness destination ke hisaab se ⚙️
- **Purana ID:** A-045
- **Kab:** Final master banate waqt
- **Kya:** Ek hi master, destination ke target par, naap kar (guess nahi): YouTube ke liye -14 LUFS integrated, true peak ≤-1 dBTP; podcast feed ke liye -16 LKFS ±1; dono jagah jana ho to do masters banao; loudnorm two-pass lagao (pehle measure, phir linear apply)
- **Kyun:** Zyada loud ghusane se kuch nahi milta (platform neeche kar dega), bahut kam rakho to padosi videos se halka sunai dega
- **Kitni baar:** Har export par ek master; mktkit apni pipeline me -16 LUFS / -1.5 dBTP / LRA 11 rakhta hai
- **Evidence:** 🟡 — Apple Podcasts official spec + YouTube ke measured normalization behaviour + EBU R128 references — platform specs
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_1610-advisory_mktkit.md`
- **Check:** `{"kind": "lufs_target", "value": -14, "tolerance": 1}`
- **Takraav note:** YouTube target -14 LUFS (kmilo/Melvynx) vs mktkit ka house master -16 LUFS: dono apni jagah sahi hain — mktkit ka tark hai ki -16 wala master platform ke ~-14 normalization par bina limiting artifacts ke pahunchta hai; jo pipeline chuno, ek hi target rakho (dekho CONFLICTS.md)

### R-106 — Room tone har gap ke neeche
- **Purana ID:** A-046
- **Kab:** Recording aur edit dono par
- **Kya:** Har location par 30-60 s ka room tone record karo; edit me har cut-gap ke neeche wahi bichao — awaaz kabhi digital silence par na gire; room tone na ho to recording ke sabse saaf khaali hisse se copy karo
- **Kyun:** Digital silence dropout jaisi lagti hai aur har cut par background ka jump sunai deta hai
- **Kitni baar:** Har location, har gap
- **Evidence:** 🟠 — Creator source (StudioBinder) — kmilo ki tagging me creator
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-107 — Dialogue saaf karne ka kram
- **Purana ID:** A-047
- **Kab:** Voice/dialogue clean karte waqt
- **Kya:** Isi kram me chalo: sabse achha source/mic chuno (jo na bole uske mics mute) → halki noise reduction → high-pass ~80 Hz → EQ (clarity) → compression → de-esser (zarurat ho to) → har clip ka level barabar → aakhir me ek master; har breath mat hatao, awaaz robotic ho jati hai
- **Kyun:** Har kadam pichle ke output par behtar kaam karta hai; ulta kram artefacts banata hai
- **Kitni baar:** Har video ki dialogue processing par
- **Evidence:** 🟠 — Creator practice (kmilo audio reference)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-108 — Gain andaze se nahi, formula se
- **Purana ID:** A-048
- **Kab:** Kisi sound ko voice ke neeche set karte waqt
- **Kya:** Gain hamesha naap kar nikalo: gain = 10^((voice_lufs − under − sound_lufs)/20), cap 1 par; 'under' ke defaults — SFX 15 dB, music ~20 dB, ambience/room tone ~30 dB; gain 1 se upar aaye to woh sound us kaam ke liye halka hai, dusra chuno, amplify mat karo
- **Kyun:** Andaze wale levels har video me badalte rehte hain; formula har baar wahi rishta deta hai
- **Kitni baar:** Har sound placement par
- **Evidence:** 🟠 — kmilo house method (library ke measured catalog par chalta hai)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-109 — Podcast mics: jo na bole uska band
- **Purana ID:** A-049
- **Kab:** Multicam podcast/interview edit karte waqt
- **Kya:** Jo vyakti nahi bol raha uska mic mute ya gate karo (dusri awaaz late pakad kar echo/phasing na bane); sab speakers ka level ek barabar rakho; music sirf intro, outro aur topic breaks me rakho, baat-cheet ke neeche nahi
- **Kyun:** Khule mics ka echo aur alag-alag levels hi podcast ko sabse zyada 'amateur' sunate hain
- **Kitni baar:** Poore episode par
- **Evidence:** 🟠 — kmilo podcast recipe ka creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-110 — Join fades: cut par click na aaye ⚙️
- **Purana ID:** A-050
- **Kab:** Talking spine ke segments judte hon to
- **Kya:** Har kept segment ke join par 0.05-0.08 s ka audio fade rakho
- **Kyun:** Bina fade ke range joins click karte hain — chhoti awaaz, lekin har cut par sunne wale ko khichti hai
- **Kitni baar:** Har join par
- **Evidence:** 🟠 — mktkit cut-video engine ka rule (reviewer catches se bana)
- **Sources:** `github_1610-advisory_mktkit.md`
- **Check:** `{"kind": "duration_range_s", "what": "join_fade", "min": 0.05, "max": 0.08}`

### R-111 — Pehla frame bina awaaz ke kaam kare (1-second rule) ⚙️
- **Purana ID:** B-029, C-039
- **Kab:** Short-form/social video ke pehle frame par
- **Kya:** Frame one par payoff result, bold caption line, ya subject mid-action dikhao — itna saaf ki bina audio ke 1 second me topic samajh aa jaye (clear text overlay, impactful image, ya immediate action). Black frame, logo sting, slow zoom, slow fade, bina-context talking head, intro/greeting — sab banned. Frame 0 hi thumbnail aur scroll-stopper hai
- **Kyun:** Autoplay muted hota hai aur viewer 1 second me tay karta hai; pehla frame 'kuch hai yahan' kehne me fail ho ya mute par samajh na aaye to scroll/swipe pakka hai (Hoyos ki 1-second rule)
- **Kitni baar:** Har short-form/social video ke first frame par
- **Evidence:** 🟠 — Creator practice — Jenny Hoyos profile (filnik) + SkillMedev (video-hook-writer, social-video-formatter) aur serge (retention beats) ki shared rule; measured study nahi
- **Sources:** `github_filnik_social-media-manager-AI.md`, `github_SkillMedev_skills.md`, `github_sergebulaev_youtube-skills.md`
- **Check:** `{"kind": "hook_within_s", "value": 1}`

### R-112 — Text overlay jaldi + har number/naam screen par ⚙️
- **Purana ID:** B-030
- **Kab:** Edit ke dauraan text overlays lagate waqt
- **Kya:** Pehla text overlay pehle 10 seconds ke andar lao; aur jo bhi numeric ya named cheez boli jaye (number, stat, key term, naam) use screen par text me dikhao
- **Kyun:** Bole gaye numbers/naam viewer retain nahi karta; screen text samajh aur yaad dono pakki karta hai
- **Kitni baar:** Pehla overlay ≤10s; har key number/stat/term/naam par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`, `github_classicchins_compounding-marketing.md`, `github_humbertobellor_henterprise.md`
- **Check:** `{"kind": "max_first_overlay_s", "value": 10}`

### R-113 — Show, then say — footage bole to jumla kato
- **Purana ID:** B-031
- **Kab:** Script/edit me jahan footage point carry kar sakti hai
- **Kya:** Jahan footage khud point dikha sakti hai wahan use bolne do aur use samjhane wala jumla kaat do
- **Kyun:** Dikhayi gayi baat boli gayi baat se tez samajh aati hai; dohra explanation samay khata hai
- **Kitni baar:** Har aisi jagah jahan visual available ho
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`

### R-114 — B-roll ko apni jagah kamani padegi
- **Purana ID:** B-032
- **Kab:** B-roll chunne/lagane par
- **Kya:** B-roll sirf wahi lagao jo wo dikhaye jo shabd nahi dikha sakte; decorative B-roll mat lagao — wo 'dead air with pictures' hai
- **Kyun:** Bina kaam ka B-roll samajh nahi badhata, sirf dhyaan ghumata hai aur seam kamzor karta hai
- **Kitni baar:** Har B-roll insert par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`
- **Takraav note:** Cadence wale rules (B-055 Craig: B-roll har 30–60s; B-056 Classic: har 5–10s) frequency mangte hain, ye rule relevance mangta hai. Takraav par relevance pehle — cadence ke liye sajawati B-roll mat dalo (Step 3 Order bhi yahi kahega: Samajh > Style). (dekho CONFLICTS.md)

### R-115 — Captions hamesha — shorts aur social par lazmi
- **Purana ID:** B-033
- **Kab:** Har short/social video, aur bolne wale har hisse par
- **Kya:** Captions hamesha rakho (shorts me captions always); auto-generated captions ko accuracy ke liye review karo
- **Kyun:** Zyada tar social video mute par dekha jata hai (source: 80%+ muted); bina captions ke message pahuchta hi nahi
- **Kitni baar:** Har video, har spoken section par
- **Evidence:** 🟡 — platform data (80%+ muted viewing, Wistia/Vidyard hawala) + measured corpus (shorts captions always)
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`, `github_classicchins_compounding-marketing.md`, `github_filnik_social-media-manager-AI.md`

### R-116 — Script kaan ke liye likho: ek jumla = ek idea
- **Purana ID:** B-034
- **Kab:** Script likhte waqt
- **Kya:** Har line bol kar padho; ek jumle me ek hi idea; viewer ke liye second person ('you') use karo; jargon ko concrete bhasha me badlo ('workflow automation platform' → 'tool that does X automatically'); jo line comma ke bina na bache use kato
- **Kyun:** Boli gayi bhasha padhi gayi bhasha se alag hoti hai; saaf jumla hi turant samajh aata hai, corporate/press-release awaaz hamesha haarti hai
- **Kitni baar:** Har script line par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`

### R-117 — Har line ke saath uska visual jodo
- **Purana ID:** B-035
- **Kab:** Script likhte waqt, har line par
- **Kya:** Har voiceover line ke saath uska visual pair karo; jis line ka visual soch na sako wo line zyada abstract hai — use dobara likho
- **Kyun:** Bina visual wali line viewer ke dimaag me tikti nahi; visual pairing hi samajh ko anchor karta hai
- **Kitni baar:** Har script line par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`

### R-118 — Title front-load + title/thumbnail ek dusre ko dohrayein nahi
- **Purana ID:** B-036
- **Kab:** Packaging (title/thumbnail) banate waqt
- **Kya:** Title me distinguishing word aage rakho (titles truncate hote hain), specific rakho clever ke upar; thumbnail ka text ~4 shabdon se kam ya bilkul nahi (B-037 dekho); title aur thumbnail EKK hi baat na kahein — mil kar dono se zyada kahein
- **Kyun:** Truncate hone par asal baat kat jati hai; dohra message CTR ka mauka khota hai
- **Kitni baar:** Har title/thumbnail pair par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`

### R-119 — Thumbnail: ek subject, tez contrast, shabd kam se kam ⚙️
- **Purana ID:** B-037
- **Kab:** Thumbnail design karte waqt
- **Kya:** Ek hi subject rakho jo phone-thumbnail size par padha jaye; high contrast; asli chehra (strong emotion ke saath) aam taur par objects se behtar; text ke liye MrBeast data 0–2 words kehta hai, Henterprise 'about 4 words se kam ya none' — 0–2 ko target rakho, 4 se upar kabhi nahi. Thumbnail ko film karne se pehle test karo
- **Kyun:** Thumbnail hi tay karta hai ki video dekha jayega ya nahi; bheed me ek saaf subject hi rukta hai
- **Kitni baar:** Har thumbnail par; text ≤4 words (target 0–2)
- **Evidence:** 🟠 — creator practice (MrBeast profile + producer practice) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_humbertobellor_henterprise.md`, `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "max_words", "what": "thumbnail_text", "value": 4}`
- **Takraav note:** Sources ke numbers alag hain: MrBeast profile 0–2 words (sabse zyada views wale), Henterprise 'under about four words'. Rule me bada wala hard cap (4) aur chhota wala target (0–2) rakha hai. (dekho CONFLICTS.md)

### R-120 — Pre-emptive on-screen text: text pehle, awaaz baad me
- **Purana ID:** B-038
- **Kab:** Short ki opening me anticipation banane ke liye
- **Kya:** On-screen text ko speaker ke bolne se PEHLE lao (jaise '200 resumes. 3 hours. Zero candidates lost.')
- **Kyun:** Pehle aaya text anticipation banata hai — viewer awaaz ka intezaar karta hai
- **Kitni baar:** Suitable shorts ki opening me
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-121 — Power words pehle 3 second / title / overlay me ⚙️
- **Purana ID:** B-039
- **Kab:** Short ki hook aur packaging me
- **Kya:** Power words use karo — Curiosity (secret, hidden, nobody knows), Urgency (banned, last time, before it disappears), Value (free, $1, half price), Exclusivity (for the first time, never seen, sneak peek) — aur ye pehle 3 seconds, title ya text overlay me aayein
- **Kyun:** Ye shabd turant click/watch trigger karte hain (Hoyos ka system)
- **Kitni baar:** Har suitable short ki shuruaat me
- **Evidence:** 🟠 — creator practice (Jenny Hoyos profile) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "hook_within_s", "value": 3}`

### R-122 — Retention curve ko order me diagnose karo
- **Purana ID:** B-040
- **Kab:** Published video ki analytics dekhte waqt
- **Kya:** Is order me check karo: (1) Low CTR → packaging (title/thumbnail). (2) High CTR + pehle 30s me bada drop → hook ne title/thumbnail ka vaada nahi nibhaya, ya start slow hai — opening recut karo, mid-action shuru karo, intro animation/'hey guys' hatao. (3) Steady decline (1–2%/min) → pacing flat hai — visual variety har 15–30s, retention beats har 2–3 min. (4) Beech me 10%+ cliff → exact timestamp pakdo — aam taur par tangent/boring/confusing hissa, transition ya galat jagah sponsor; use kato/restructure karo ya usse pehle re-hook lagao. (5) End drop-off → ending chhota karo, CTA pehle lao. (6) Spikes (retention UPAR) → ye achha hai — wajah pakdo aur use zyada karo. (7) Retention achhi par growth nahi → packaging impressions nahi kama raha ya topic ka audience maujood subscribers se aage nahi
- **Kyun:** Har curve pattern ki wajah aur ilaaj alag hai; bina diagnosis ke edit karna andaz hai
- **Kitni baar:** Har published video ke review par, isi order me
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`, `github_humbertobellor_henterprise.md`, `github_classicchins_compounding-marketing.md`

### R-123 — Refresh trigger: retention 20%+ gire to restructure/replace ⚙️
- **Purana ID:** B-041
- **Kab:** Purane video ki performance review par
- **Kya:** Agar retention peak se 20%+ gir jaye to video ko restructure ya replace karo; yahi trigger product UI badalne, testimonial customer churn hone, ya nayi positioning aane par bhi lagu hai
- **Kyun:** Purana pada video audience ko thaka deta hai aur galat/stale message deta rehta hai
- **Kitni baar:** Trigger: retention drop ≥20% from peak
- **Evidence:** 🟠 — house threshold (skill ki quality bar) — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`
- **Check:** `{"kind": "min_drop_percent", "what": "retention_from_peak", "value": 20}`

### R-124 — Safe zone + platform ke hisaab se captions ghumao
- **Purana ID:** B-042
- **Kab:** Vertical video (Reels/TikTok) edit/export par
- **Kya:** Text/captions safe zone me rakho — Reels: top 250px (username) aur bottom 400px (CTA/comments) se bacho; TikTok par bhi upar-neeche bacho. Cross-post karte waqt subtitles ko har platform ke safe zone ke hisaab se reposition karo aur dusre platform ka watermark kabhi mat rakho (TikTok watermark wali video Reels par nahi)
- **Kyun:** UI ke neeche daba text padha nahi jata; watermark wali cross-post dono platforms par penalize/laggy lagti hai
- **Kitni baar:** Har vertical video, har platform variant par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-125 — Distribution + repurposing plan production se pehle
- **Purana ID:** B-043
- **Kab:** Har video ke brief stage par
- **Kya:** Pehle tay karo video kahan rahega, kaun dhundhega, aur usse kaun se derivative assets banenge (repurposing matrix: 1 lambi video → clips, quote graphics, blog/transcript aadi). Jo segments akele shorts banke khade hone hain, unhe shoot hi aise karo ki akele khade hon
- **Kyun:** Bina plan ke bana video decoration hai; baad me kaate gaye shorts ko wo context nahi milta jo unhe chahiye
- **Kitni baar:** Har video, brief stage par hi
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`, `github_humbertobellor_henterprise.md`

### R-126 — Ek shot = ek hi attentional magnet
- **Purana ID:** C-007
- **Kab:** Koi important shot design/select karte waqt
- **Kya:** Shot ko EK dominant magnet do (face, motion onset, ya bolti awaaz) aur competing motion hatao; do magnets ladenge to synchrony tootegi
- **Kyun:** Dhyaan involuntary roop se motion/face/speech se khinchta hai; do competing cues gaze ko baant dete hain
- **Kitni baar:** Har shot par; khaaskar key beats par sakht
- **Evidence:** 🟢 — Motion-onset capture aur gaze clustering eye-tracking se measured hai
- **Sources:** `science_tim_smith.md`

### R-127 — Ek beat = ek idea, on-screen bhi mark karo
- **Purana ID:** C-030
- **Kab:** Body ki beats likhte/edit karte waqt
- **Kya:** Har beat me sirf ek idea rakho, aur har beat ke saath likho ki screen par kya dikhega — sirf bolta sir (talking head) bina dekhe jaane wali cheez ke podcast hai, video nahi
- **Kyun:** Ek beat me do ideas dono ko kamzor karte hain; visual mark editor ko aur viewer dono ko orientation deta hai
- **Kitni baar:** Har beat par
- **Evidence:** 🟠 — yt-script ki craft rule; SkillMedev ke inline [B-ROLL]/[GRAPHIC] cues bhi yahi kehte hain
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`

### R-128 — Narration-action sync — ek instruction, ek action
- **Purana ID:** C-048
- **Kab:** Tutorial/demo ki voiceover likhte waqt
- **Kya:** Ek on-screen action ke liye ek hi instruction; shabd action ke saath ya ek beat pehle land hon — jo click ho chuka, use narrate mat karo ('ab humne save kar liya' save ke baad dead air hai). Screen par kuch complex ho raha ho to bolna roko aur visual ko saans lene do
- **Kyun:** Viewer ek saath kar bhi raha hai aur sun bhi raha hai; peeche chali narration aur aage badha visual dono ko harate hain
- **Kitni baar:** Har instruction par
- **Evidence:** 🟠 — SkillMedev narration-script ki cardinal rule
- **Sources:** `github_SkillMedev_skills.md`

### R-129 — Har step ka shape: Goal → Action → Confirmation
- **Purana ID:** C-049
- **Kab:** Tutorial ke steps likhte waqt
- **Kya:** Har step teen hisso me rakho: Goal (kya karne wale hain aur kyun), Action (ek concrete instruction), Confirmation (success kaisa dikhega). Steps ke beech halki signposting rakho. On-screen UI labels bilkul wasi bolo jase button par likha hai — button 'New project' kehta hai to 'create a project' mat bolo
- **Kyun:** Shape viewer ko har pal oriented rakhta hai; label mismatch seedha confusion hai
- **Kitni baar:** Har step par
- **Evidence:** 🟠 — SkillMedev narration-script ki structure rule
- **Sources:** `github_SkillMedev_skills.md`

### R-130 — Likhne ki safaai — em dash aur AI shabdawali ki hadd
- **Purana ID:** C-064
- **Kab:** Koi bhi publish hone wala text (title, description, script, post) likhte waqt
- **Kya:** Em dash lagbhag 1 per 100 shabd se zyada nahi (title/post me zyada se zyada 1); zyada hon to comma, colon ya line break lagao — period kabhi nahi. AI-vocabulary markers (leverage, significant, streamline, foster...) ek paragraph me 1 hai to English hai, 3 hon to poora paragraph dobara likho; ek-line title me ek bhi marker cluster hai. Sincerity openers ('let me be honest', 'not gonna lie') aur reveal bridges ('here's what nobody tells you') bina dated fact ke banned. Keywords stuff mat karo — asal search phrase ek baar, natural
- **Kyun:** Density hi AI-likhai ki pehchan hai; stuffing ranking nahi deta, spam padhta hai
- **Kitni baar:** Har text par, publish se pehle ek pass
- **Evidence:** 🟠 — serge bundle ki voice rules — house craft standard
- **Sources:** `github_sergebulaev_youtube-skills.md`

### R-131 — Captions ke reading niyam (phrase captions) ⚙️
- **Purana ID:** C-085
- **Kab:** SRT/VTT caption track banate waqt
- **Kya:** Cue speech ke saath aaye aur usi ke saath jaye; screen par kam se kam ~1s, zyada se zyada ~7s (lamba ho to baanto). Cue me 1-2 lines, kabhi 3 nahi; ~32-42 characters per line; reading speed ≤ ~17 characters/second (~160-180 wpm) — zyada ho to cue baanto ya duration badhao. Line clause boundary par todo, mid-phrase kabhi nahi. Tutorial ke liye clean captioning: filler ('um', 'uh', false starts) hatao, matlab verbatim rakho; technical terms aur UI labels bilkul sahi rakho. Raw ASR kabhi ship mat karo — galtiyan hamesha sabse keemti shabdon par hoti hain
- **Kyun:** Captions accessibility bhi hain aur muted viewers ko pakadne wala jaal bhi; tez ya galat captions dono kaam kharab karte hain
- **Kitni baar:** Har cue par
- **Evidence:** 🟠 — SkillMedev captions-from-transcript ki line/reading rules — broadcast captioning ke aam standards se milti hui craft values
- **Sources:** `github_SkillMedev_skills.md`
- **Check:** `{"kind": "max_chars", "value": 42, "what": "caption_line"}`
- **Takraav note:** Ye phrase-caption mode hai; word-level mode ke liye C-077 dekho (dekho CONFLICTS.md)

### R-132 — Sirf word-level verbatim ASR
- **Purana ID:** C-095
- **Kab:** Transcription ka tareeka chunte waqt
- **Kya:** Hamesha word-level verbatim ASR lo. SRT/phrase mode kabhi nahi (sub-second gap data khota hai) aur fillers ko normalize kabhi nahi (editorial signal khota hai). Transcript pehli aur aakhri line khud padho — Whisper khamoshi par bani-banayi line (fake subtitler credit/outro) hallucinate kar sakta hai, normal confidence ke saath
- **Kyun:** Cut ke saare faisle gap aur word timing par tikke hain; phrase data unhe andaze me badal deta hai
- **Kitni baar:** Har transcription par
- **Evidence:** 🟠 — video-use Hard Rule 8 + blazerior ki hallucination chetaavni (troubleshooting #17) — dono production pipelines ka sabak
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`, `github_blazerior_videoediting-claude-skill.md`

### R-133 — Self-eval gate — output ko har cut par check karo
- **Purana ID:** C-102
- **Kab:** Render ke baad, user ko dikhane se pehle
- **Kya:** RENDERED output (sources nahi) par har cut boundary ke ±1.5s window me dekho: visual discontinuity/flash, waveform spike (bacha hua audio pop), overlay ke peeche chhupa subtitle, galat frames dikhata overlay. Saath me pehle 2s, aakhri 2s aur 2-3 midpoints sample karo (grade consistency, subtitle readability). Kuch fail ho to fix → re-render → re-eval; zyada se zyada 3 passes — uske baad bachi khamiyan user ko flag karo, loop mat chalao
- **Kyun:** Apna output khud verify kiye bina dikhana aadhi galtiyon ko user tak pahuncha deta hai
- **Kitni baar:** Har render par, dikhane se pehle
- **Evidence:** 🟠 — video-use process step 7 — workflow rule, ek production pipeline ki aadat
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`



### R-268 — Dialogue cleanup ka kram aur numbers ⚙️ *(naya — editor round)*
- **Purana ID:** D1-007
- **Kab:** Dialogue/voice track saaf karna ho
- **Kya:** Isi kram me: normalize (peaks −12..−6 dBFS) → high-pass filter 80–100 Hz → room-tone noise print se de-noise → de-ess 4–8 kHz → halki compression 2:1–3:1
- **Kyun:** Galat kram me safai awaaz ko patla/kritrim kar deti hai; ye kram pehle badi gadbad, phir bareeki sambhalta hai aur baat saaf sunai deti hai
- **Kitni baar:** Har dialogue track par ek baar, mix se pehle
- **Evidence:** 🟠 — Audio craft numbers (note)
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`
- **Check:** `{"kind": "db_range", "field": "dialogue_peak_dbfs", "min": -12, "max": -6}`

### R-269 — Har edit point par chhota audio crossfade *(naya — editor round)*
- **Purana ID:** D1-008
- **Kab:** Koi bhi audio cut lage
- **Kya:** Har edit point par 2–4 frames ka audio crossfade lagao
- **Kyun:** Bina crossfade ke cut par click/pop sunai deta hai jo darshak ko baat se bahar kheenchta hai
- **Kitni baar:** Har audio edit point par, bina apvaad
- **Evidence:** 🟠 — Audio craft (note)
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`
- **Takraav note:** ZeusSheen ka 2-frame fade rule (D1-089) isi baat ka khaas roop hai — sangat hai, takraav nahi

### R-273 — Cut ke dono taraf kam se kam 60 ms asli khamoshi ⚙️ *(naya — editor round)*
- **Purana ID:** D1-012
- **Kab:** Speech par cut lage (word-boundary par)
- **Kya:** Har cut edge ke dono taraf kam se kam 60 ms ki asli (true) khamoshi chhodo taaki audio crossfade saans le sake
- **Kyun:** Khamoshi ke bina laga cut shabd ke kinare ko kaat deta hai aur click deta hai; 60 ms crossfade ki saans hai
- **Kitni baar:** Har speech cut par
- **Evidence:** 🟠 — Agent ki hard rule (note)
- **Sources:** `notes_eacp1991_premiere-agent.md (note)`
- **Check:** `{"kind": "min_gap_ms", "what": "cut_edge_true_silence", "value": 60}`

### R-280 — Zero frame bleed — padosi scene ka ek frame bhi nahi *(naya — editor round)*
- **Purana ID:** D1-019
- **Kab:** Compilation/scene isolation me cut edges tay hon
- **Kya:** Kisi bhi cut edge par padosi scene ka 1–2 frame bhi bleed na ho. Compilation rips ke kinaro par chipke hue pichle/agle clip ke 2–5 s ko isolation me (±0.08 s safety ke saath) poora hatao
- **Kyun:** Ek bhi ajnabee frame darshak ko jhatka deta hai aur edit ko kaccha dikhata hai
- **Kitni baar:** Har cut edge par, bina apvaad
- **Evidence:** 🟠 — Craft rule (note)
- **Sources:** `notes_mmmnhat_agent-skills.md (note)`

### R-289 — Staging ki takneek — aankh ko ek hi jagah le jao *(naya — editor round)*
- **Purana ID:** D1-028
- **Kab:** Frame me main subject ko ubharna ho
- **Kya:** Depth of field/blur se background ko peeche rakho, vignette lagao, secondary elements ki opacity ghatao, aur main subject ko sabse zyada roshan rakho
- **Kyun:** Aankh sabse saaf/roshan cheez par jati hai — staging se darshak wahi dekhta hai jo dikhana hai
- **Kitni baar:** Har ahem frame/scene par
- **Evidence:** 🟠 — Disney parampara ki takneek (MIT skill sheet)
- **Sources:** `github_dylantarre_animation-principles.md`
- **Takraav note:** Dhyaan-anushaasan wale merged rule (D1-057) se sambandhit hai — ye usi baat ke haath ke upaay hain

### R-297 — B-roll dialogue ke upar — A1 ko kaate bina *(naya — editor round)*
- **Purana ID:** D1-036
- **Kab:** B-roll schedule karna ho
- **Kya:** Track banawat rakho: V1 = A-roll, V2 = B-roll, V3 = overlays/text; A1 = dialogue, A2 = SFX, A3 = music. B-roll ko transitions aur key points ke upar rakho lekin A1 dialogue ko kabhi mat kaato
- **Kyun:** B-roll ka kaam baat ko dikhana hai, kaatna nahi; dialogue ki nirantarta hi samajh ki neev hai
- **Kitni baar:** Har edit me yehi track anushaasan
- **Evidence:** 🟠 — Workflow/layout discipline (MIT skill)
- **Sources:** `github_vamshicreates_premiere-editing-dna.md`

### R-311 — Text zones hamesha saaf — microcopy ka bandobast *(naya — editor round)*
- **Purana ID:** D1-050
- **Kab:** Frame me text/copy ke saath decorative elements hon
- **Kya:** Decorative systems ko copy ke peeche ya kinare par rakho, text ke paas clutter kabhi nahi; aur chhota gray microcopy mat rakho — secondary text bhi padhne layak size/rang me ho
- **Kyun:** Text ke paas ki bheed padhna rok deti hai; na-padha-jane-wala text sirf shor hai
- **Kitni baar:** Har text-wale frame par
- **Evidence:** 🟠 — Motion-direction craft (MIT skill)
- **Sources:** `github_SebastianBoehler_autoresearch_after_effects_finetune.md`

### R-318 — Dhyaan ka anushaasan — ek frame, zyada se zyada do maang *(naya — editor round)*
- **Purana ID:** D1-057
- **Kab:** Frame ki composition/motion tay ho
- **Kya:** Ek frame me do se zyada cheezein ek saath dhyaan na maangein; har frame me kam se kam ek crisp/sharp element rakho; aur jaan-boojh ke near-stillness (lagbhag sthirta) ke pal bhi rakho — sab kuchh har samay hilna zaroori nahi
- **Kyun:** Har hilti cheez chillaye to koi nahi sunai deta; sthirta ke pal hi harkat ko matlab dete hain
- **Kitni baar:** Har frame/scene par
- **Evidence:** 🟠 — Do AE sources ke sangat dhyaan-niyam
- **Sources:** `github_Maciejdziuba_youtube-skills.md`, `github_LobzyJay_motion-design-with-claude.md`
- **Takraav note:** dylantarre ki staging takneek (D1-028) isi anushaasan ko pane ke upaay deti hai — takraav nahi

### R-344 — Black card ke neeche room tone — khamoshi kabhi nahi *(naya — editor round)*
- **Purana ID:** D1-083
- **Kab:** Video me koi black card/blank aaye
- **Kya:** Black card ke neeche hamesha room tone rakho; poori khamoshi (silence) kabhi mat rakho
- **Kyun:** Asli khamoshi darshak ko 'video ruk gaya/band ho gaya' jaisa ehsaas deti hai; room tone use zinda rakhta hai
- **Kitni baar:** Har black card par
- **Evidence:** 🟠 — Film-editing pipeline craft (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`
- **Takraav note:** Paheli lage to: 'a talking cut is never silent' wala usi skill ka usool bhi yahi disha deta hai

### R-347 — 30 ms ke andar speech = CLIPPED (shabd kata mana jayega) ⚙️ *(naya — editor round)*
- **Purana ID:** D1-086
- **Kab:** Koi cut speech ke paas gire
- **Kya:** Agar cut se 30 ms ke andar speech hai to use defect mano — shabd kata hua hai; cut ko hamesha asli pause ke beech me rakho
- **Kyun:** Shabd ke kinare ka kataav sunne me sabse pehle pakda jata hai — yehi sabse sasti galti hai
- **Kitni baar:** Har cut par check
- **Evidence:** 🟠 — Defect-lint ka threshold (MIT skill)
- **Sources:** `github_ZeusSheen_ppro-agent-bridge.md`
- **Check:** `{"kind": "min_gap_ms", "what": "speech_to_cut_distance", "value": 30}`
- **Takraav note:** eacp1991 ka 60 ms crossfade niyam (D1-012) isse sakht hai — dono sangat disha me hain: 30 ms = kataav ki hadd, 60 ms = saaf cut ki shart

### R-348 — Room tone ka jump 6 dB se zyada = defect ⚙️ *(naya — editor round)*
- **Purana ID:** D1-087
- **Kab:** Do hisso ke beech cut lage
- **Kya:** Cut ke dono taraf ke room tone me 6 dB se zyada ka jump defect hai (LEVEL_JUMP) — room tone ka mel rakho, warna cut kaan ko sunai dega bhale dikhai na de
- **Kyun:** Kaan background ke badlav ko tasveer ke badlav se pehle pakadta hai
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — Defect-lint ka threshold (MIT skill)
- **Sources:** `github_ZeusSheen_ppro-agent-bridge.md`
- **Check:** `{"kind": "db_range", "field": "room_tone_jump_db", "min": 0, "max": 6}`

### R-350 — Click hatana ho to aakhri 2 frames fade karo *(naya — editor round)*
- **Purana ID:** D1-089
- **Kab:** Cut par click sunai de aur outgoing shabd soft decay par khatm ho raha ho
- **Kya:** Shabd ko kaatne ki jagah outgoing audio ke aakhri 2 frames par fade lagao — click jayega, shabd bachega
- **Kyun:** Click ka ilaaj shabd kaatna nahi hai; 2-frame fade sabse halka aur surakshit ilaaj hai
- **Kitni baar:** Har click wale cut par
- **Evidence:** 🟠 — Rough-cut craft (MIT skill)
- **Sources:** `github_ZeusSheen_ppro-agent-bridge.md`
- **Takraav note:** ADAM-0S ka 2–4 frame crossfade niyam (D1-008) isi ka vistarit roop hai — sangat

### R-352 — Bina-wajah ka A/V cut mismatch = defect *(naya — editor round)*
- **Purana ID:** D1-091
- **Kab:** Video (V1) aur audio (A1) ke cut points alag jagah par hon
- **Kya:** Agar A/V cuts kuch frames idhar-udhar hain aur uski koi wajah nahi hai to use defect mano — cuts ek hi jagah par rakho
- **Kyun:** Bina wajah ka mismatch edit ko bikharra hua dikhata hai; jaan-boojh ka offset hi split edit kehlata hai
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — Defect-lint (MIT skill)
- **Sources:** `github_ZeusSheen_ppro-agent-bridge.md`
- **Takraav note:** ADAM-0S ke split-edit niyam (D1-001) se takraav NAHI hai — wahan offset jaan-boojh ka aur 6–12 frames ka hota hai; ye sirf bina-wajah ke chhote mismatch ki baat hai

### R-375 — Captions sirf darshak ke liye *(naya — editor round)*
- **Purana ID:** D2-018
- **Kab:** Final SRT/TXT narration lines likhte waqt
- **Kya:** Har caption line audience ke liye ho: travel narration, route context, emotion ya visual observation. Workflow state wali baatein captions me KABHI nahi — 'QA pass', 'V14', 'Resolve', 'SRT', 'ye fix ho gaya' jaisi editor-bhasha block hai
- **Kyun:** Ek bhi andar-ki-baat wala caption poori film ko machine-bani hui ghoshit kar deta hai
- **Kitni baar:** Editor-facing caption = 0
- **Evidence:** 🟠 — House caption contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-376 — Title zones me subtitles band *(naya — editor round)*
- **Purana ID:** D2-019
- **Kab:** Opening/chapter/ending title windows me
- **Kya:** Title chal raha ho to us window me rendered subtitle overlay suppress ya trim karo, jab tak user khaas taur par captions-over-title na maange. Scenic/title windows BGM-led rakho
- **Kyun:** Title aur caption ek saath ladte hain — dono padhne mushkil ho jate hain
- **Kitni baar:** Title-zone subtitle overlap = 0
- **Evidence:** 🟠 — House subtitle-overlay contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-377 — Bina-voiceover film me captions hi kahani ⚙️ *(naya — editor round)*
- **Purana ID:** D2-020
- **Kab:** Jab voiceover na ho aur TXT/SRT hi narrative layer ho
- **Kya:** Captions itne dense rakho ki route, emotion aur visual imaandari carry kar sakein — planning target kam se kam 4 cues/minute rakho (slow reference profile justify kare to hi kam)
- **Kyun:** Awaaz na ho to kam captions wala hissa khaali aur khoya hua lagta hai
- **Kitni baar:** ≥4 cues/minute planning target
- **Evidence:** 🟠 — House caption-density target
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "min_per_min", "min": 4, "what": "caption cues (no-VO film)"}`

### R-378 — Caption highlight: line me sirf 1–3 shabd ⚙️ *(naya — editor round)*
- **Purana ID:** D2-021
- **Kab:** Word-highlight/karaoke style captions banate waqt
- **Kya:** Har caption line me sirf 1–3 important shabd highlight karo. Hierarchy: action verbs > numbers > emotional words. Filler/modifier shabd ('this', 'my', 'completely') kabhi highlight nahi
- **Kyun:** Sab kuch highlight = kuch bhi highlight nahi; aankh ko ek hi jagah rukna chahiye
- **Kitni baar:** 1–3 highlighted words per line
- **Evidence:** 🟠 — CapCut director brain ki caption intelligence
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "count_range", "min": 1, "max": 3, "what": "highlighted words per caption line"}`

### R-379 — Captions: pehle proofread, aakhir me finishing pass *(naya — editor round)*
- **Purana ID:** D2-022
- **Kab:** Caption workflow ke dono sire par
- **Kya:** Captions ko import karne se PEHLE saaf aur proofread karo (single-line default). Caption-only finishing pass sirf approved cut par chalao — word-level timing check karo aur sirf high-confidence domain terms fix karo
- **Kyun:** Gande captions import karke theek karna doguna kaam hai; aur cut badalne ke baad caption pass bekaar ho jata hai
- **Kitni baar:** Proofread = import se pehle; finishing pass = sirf approved cut par
- **Evidence:** 🟠 — Do sources: vlog workflow note + Resolve production standard
- **Sources:** `notes_appariciojunior_video-editor-skills.md (note)`, `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-380 — Burned-in captions dikhne wala layer ho *(naya — editor round)*
- **Purana ID:** D2-023
- **Kab:** Caption delivery check par
- **Kya:** Sirf SRT file deliverable nahi hai — burned-in captions timeline me ek visible layer ke roop me hone chahiye aur final render me dikhne ka saboot ho
- **Kyun:** File hai lekin render me caption nahi — ye sabse chhupa hua delivery fail hai
- **Kitni baar:** Har delivery = rendered caption ka visual saboot
- **Evidence:** 🟠 — Production standard ki QA shart
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-381 — Vertical: aankhein upar-wale third me, captions surakshit jagah *(naya — editor round)*
- **Purana ID:** D2-024
- **Kab:** Vertical (9:16) framing aur caption placement me
- **Kya:** Speaker ki aankhein frame ke upper third ke aas-paas rakho. Captions ko chehra/munh aur platform UI ke danger zones se bahar rakho; key lines proofread karo
- **Kyun:** UI ke neeche daba caption = na padha gaya caption
- **Kitni baar:** Caption kabhi face/mouth/UI-safe-zone ke bahar nahi
- **Evidence:** 🟠 — Do sources: Resolve social editor + CapCut mobile workflow
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`, `github_pockebot_openpocket.md`

### R-382 — Bolne wala dikhe; B-roll emotion ko na dhake *(naya — editor round)*
- **Purana ID:** D2-025
- **Kab:** Talking-head par B-roll lagate waqt
- **Kya:** Spoken sections ke dauran speaker visible rakho. Crucial face/emotion beats par B-roll mat lagao — cutaway phrase land hone ke baad, saans par ya naye idea par rakho
- **Kyun:** Jazbaat chehre par hote hain; galat jagah cutaway usi pal ko chura leta hai
- **Kitni baar:** Emotion beats par B-roll = 0
- **Evidence:** 🟠 — Production standard se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-383 — Screencast samajh: intent bolo, action nahi *(naya — editor round)*
- **Purana ID:** D2-026
- **Kab:** Screen-recording narration aur annotations me
- **Kya:** Har interaction se pehle context do; fast-forward hisse me khaas taur par narration rakho. Jo prompt text screen par poora na dikhe, use caption karo. Annotations phase ka label dein. Narration 'main ye click kar raha hoon' ki jagah intent bataye
- **Kyun:** Bina intent ke screen sirf harkat hai; viewer ko 'kyun' chahiye
- **Kitni baar:** Har interaction = pehle intent line
- **Evidence:** 🟠 — Screencast editor ki house style
- **Sources:** `github_matthull_my-skills.md`

### R-384 — Narration ka har daava saboot se bandha ho *(naya — editor round)*
- **Purana ID:** D2-027
- **Kab:** Narration/caption lines likhte waqt
- **Kya:** Har claim actual route evidence ya user-confirmed context se bandha ho. Jo cheez screen par khud dikh rahi hai use bolkar repeat mat karo
- **Kyun:** Bina saboot ke daave aur dikhi cheez ki commentary — dono bharosa ghataate hain
- **Kitni baar:** Unverified claim = 0
- **Evidence:** 🟠 — House narration niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-385 — Title/lower-third: timing aur font ki discipline *(naya — editor round)*
- **Purana ID:** D2-028
- **Kab:** Animated titles aur lower-thirds banate waqt
- **Kya:** Lower-third slide-in ~12 frames rakho (~0.5s @24fps); typewriter follower delay 2 frames per character. Font medium-to-bold sans rakho (Open Sans Extrabold jaisa default). Timing perfect hone ke baad hi use macro/template me save karo. Animated title ke liye Text+ istemaal karo, basic Text nahi
- **Kyun:** Dheere-dheere ghusne wala lower-third purana lagta hai; halka font mobile par ghul jata hai
- **Kitni baar:** Slide-in 12 frames; follower delay 2 frames/char
- **Evidence:** 🟠 — Resolve titles workflow se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-386 — Marker discipline: EDL se, rang-tiers ke saath *(naya — editor round)*
- **Purana ID:** D2-029
- **Kab:** Resolve me review markers lagate waqt
- **Kya:** Markers EDL ke through lagao (Resolve FCP7 XML ke clip colours ignore karta hai). Colour tiers fixed rakho: A = Red, flash frames = Fuchsia, B = Yellow, C = Blue, notes/re-record = Green
- **Kyun:** Marker ka rang hi team ki bhasha hai; rang badla to matlab badla
- **Kitni baar:** 5 tiers, hamesha yahi mapping
- **Evidence:** 🟠 — Note source: dusre editor ke workflow apne shabdon me
- **Sources:** `notes_SamuelAde001_second-brain.md (note)`

### R-387 — Pehle mapo (measure), phir raay do *(naya — editor round)*
- **Purana ID:** D2-030
- **Kab:** Kisi bhi editorial faisle se pehle
- **Kya:** Pacing/audio/structure par pehle scripts se numbers nikalo, editorial opinion uske baad do
- **Kyun:** Bina map ke raाय andaz hai; numbers behes khatam karte hain
- **Kitni baar:** Har bada faisla = pehle ek measured report
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_SamuelAde001_second-brain.md (note)`

### R-388 — HOW aur WHAT alag rakho: preset pehle padho *(naya — editor round)*
- **Purana ID:** D2-031
- **Kab:** Koi bhi edit lane chalane se pehle
- **Kya:** Pehle WHAT padho — preset: look, numbers, done ki definition. Phir HOW chalao — lane ke steps. Dono ko mix mat karo
- **Kyun:** Bina 'done kya hai' jaane steps chalana = ghumte rehna
- **Kitni baar:** Har kaam = pehle preset read, phir execution
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_edwinponcious12_video.md (note)`

### R-389 — Do-stage soch: pehle creative, phir tool *(naya — editor round)*
- **Purana ID:** D2-032
- **Kab:** AI/editor se edit plan banwate waqt
- **Kya:** Stage 1 me tool/catalog ka zikr kiye bina pure creative analysis karo (pacing, emotion, energy, weak spots). Stage 2 me hi suggestions ko asal tool/asset names se ground karo
- **Kyun:** Catalog pehle dikha do to soch catalog ke andar hi band ho jati hai; aur bina grounding ke plan chalaya nahi ja sakta
- **Kitni baar:** Har plan = 2 stages, isi kram me
- **Evidence:** 🟠 — CapCut director ka core design niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-390 — Har edit ka 'kyun' aur weak spots saaf likho *(naya — editor round)*
- **Purana ID:** D2-033
- **Kab:** Edit plan/review dete waqt
- **Kya:** Har action ke saath uski wajah likho. Dead air, pacing drops jaise weak spots chhupao mat — explicitly flag karo. Subjective choices par 2–3 alternatives do taaki editor control me rahe
- **Kyun:** 'Kyun' bina ka plan order hai; kyun ke saath woh direction hai
- **Kitni baar:** Actions bina why = 0; weak spots sab flag
- **Evidence:** 🟠 — CapCut director ke output niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-391 — Handoff ke liye layered timeline *(naya — editor round)*
- **Purana ID:** D2-034
- **Kab:** Timeline kisi insaan ko saumpte waqt
- **Kya:** Timeline layered rakho: disabled/backup tracks ka naam 'DISABLED' rakho, taaki agla editor bina puche samajh jaye ki kya live hai aur kya rakha hua hai
- **Kyun:** Gandi timeline dusre ke liye band kamra hai
- **Kitni baar:** Har handoff = naam-daar layers
- **Evidence:** 🟠 — Production standard se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-392 — Pehli-pass ki taqseem: insaan = taste, agent = mazdoori *(naya — editor round)*
- **Purana ID:** D2-035
- **Kab:** AI agent ke saath edit ka kaam baant-te waqt
- **Kya:** Insaan taste aur film-sense ke faisle rakhe; agent transcribe/log/detect jaise labour kare. Agent raw footage kabhi modify nahi karta — woh sirf ADD karta hai
- **Kyun:** Taste machine ko dena aur mazdoori insaan karna — ulta batenwara kaam kharab karta hai
- **Kitni baar:** Division = har project ki shuruaat me tay
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_appariciojunior_video-editor-skills.md (note)`

### R-393 — Creative azadi: template nahi, video ki energy *(naya — editor round)*
- **Purana ID:** D2-036
- **Kab:** Har naye video ki analysis par
- **Kya:** Har video ko independently analyze karo. Rigid genre rules ('funny hai to X karo') default mat banao. Video ki unique energy hai to usi par lean karo, safe defaults par nahi
- **Kyun:** Template-har-video ek jaisi film banata hai; energy har video ki alag hoti hai
- **Kitni baar:** Genre-template default = 0
- **Evidence:** 🟠 — CapCut director ka creative-freedom rule
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

---

## RHYTHM — gati aur saans sahi jagah

### R-134 — Visual change ki cadence (short-form) ⚙️
- **Purana ID:** A-051
- **Kab:** Short-form (TikTok/Reels/Shorts) edit karte waqt
- **Kya:** Har kuch seconds me screen par kuch badal ho — baseline: 5 s ke andar kam se kam ek visual change (cut, punch-in, overlay, B-roll, text swap); ExpoCut ki kasauti: koi bhi 5 s ka window bina change ke = swipe risk
- **Kyun:** Short-form me rukti hui screen hi swipe ka sabse seedha karan hai
- **Kitni baar:** Pacing offsets: Melvynx har 2-4 s, ExpoCut har 3-5 s, mktkit har 3-7 s (pehle 5 s me aur tight), trend/entertainment me cuts 0.5-1 s
- **Evidence:** 🟠 — Teeno sources creator playbook/house numbers hain (Free to use and redistribute with attribution to expocut.com — ExpoCut ka hissa)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 5}`
- **Takraav note:** Cadence ke numbers sources me alag hain — Melvynx 2-4 s, ExpoCut 3-5 s, mktkit 3-7 s; content type faisla kare (samjhane wala dheema, entertainment tez), lekin 5 s se upar kahin bharosa nahi (dekho CONFLICTS.md)

### R-135 — Film se pacing ka benchmark
- **Purana ID:** A-052
- **Kab:** Kisi bhi format ka shot length sochte waqt
- **Kya:** Reference rakho: aaj ki filmein ~4-5 s average shot length par chalti hain; dialogue wale hisse isse lambe, action wale chhote; apne format ka pacing isi ke aas-paas napo, usse bad-zada tez mat karo
- **Kyun:** Ye das saal ke data ka pattern hai — viewer's aankh is cadence ki aadi hai
- **Kitni baar:** Sirf benchmark; koi sakht target nahi
- **Evidence:** 🟢 — James Cutting (2011) — peer-reviewed film data (kmilo me 'study / official' tag)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Takraav note:** Ye film ka naapa hua average hai, short-form ke liye target nahi — wahan cadence A-051 wali hi chalegi (dekho CONFLICTS.md)

### R-136 — Type ke hisaab se shot lambaai
- **Purana ID:** A-053
- **Kab:** Har segment ka shot length tay karte waqt
- **Kya:** Talking head: 2-5 s per shot; verticals: 2-3 s per shot, 4 s se upar kabhi nahi, aur text wala shot kam se kam ~2 s; tutorial: shot ≥5 s; vlog: clock se nahi, event ke hisaab se kato (ek kaam = ek block)
- **Kyun:** Har format ki samajh-gati alag hai — tutorial ko sochne ka samay chahiye, vertical ko nahi
- **Kitni baar:** Har shot par
- **Evidence:** 🟠 — kmilo creator reference (type-wise shot lengths)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-137 — Explainer ke pattern interrupts
- **Purana ID:** A-054
- **Kab:** Lambe explainer/talking video me dhyaan bachana ho to
- **Kya:** Pehla pattern interrupt (angle, B-roll, graphic, zoom) 25-35 s ke andar laao, phir har 2-3 minute me ek; micro-hook (caption, question, tease) isse ghana rakho
- **Kyun:** Bina badlaav ke dhyaan sabse tez yahi girta hai — interrupt ek nayi shuruaat jaisa kaam karta hai
- **Kitni baar:** Pehla ≤35 s par; phir 2-3 min ke antar par; micro-hook har 30-90 s
- **Evidence:** 🟠 — Creator source (air.io) kmilo me; micro-hook ke numbers TubeBuddy/vidIQ ke alag-alag reports hain
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Takraav note:** Micro-hook interval par sources aapas me takrate hain — TubeBuddy 30-60 s kehta hai, vidIQ 60-90 s; dono creator reports hain, koi pakka number nahi (dekho CONFLICTS.md)

### R-138 — Phrases ke beech ka gap ⚙️
- **Purana ID:** A-055
- **Kab:** Dead air/silence hatate waqt
- **Kya:** Phrase gaps type ke hisaab se rakho: talking head 200-400 ms, Shorts 200-300 ms, tutorial ≥0.4 s (3 s bina voice = warning, 6 s = hard cap jab tak screen khud na samjhaye); saans ki jagah puri tarah zero mat karo — gap hamesha kuch rakho
- **Kyun:** Saans hi bolne ko insaani banati hai; gap type ke samajh-waqt ke barabar ho to edit natural lagta hai
- **Kitni baar:** Har phrase boundary par
- **Evidence:** 🟠 — Creator/house numbers teeno sources se (kmilo, Melvynx pauses.json defaults, mktkit engine defaults)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_1610-advisory_mktkit.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Check:** `{"kind": "gap_range_ms", "what": "phrase_gap_talking_head", "min": 200, "max": 400}`
- **Takraav note:** Numbers style ke hisaab se bahut alag hain: Melvynx ka super-fast style sirf 30-80 ms saans rakhta hai (sentence .08, comma .05, word .03); mktkit engine defaults talking 0.40 s, manifest 0.85 s; ExpoCut silence removal me min gap 450-500 ms + 80 ms padding (Free to use and redistribute with attribution to expocut.com) — ek channel par ek style pakdo (dekho CONFLICTS.md)

### R-139 — Har cut ke paas reason ho
- **Purana ID:** A-056
- **Kab:** Koi cut lagane se pehle
- **Kya:** Cut tabhi jab woh ek kaam kare: (1) dead time hataye, (2) information badle, ya (3) action ko follow kare; word ke beech me cut kabhi nahi
- **Kyun:** Bina reason ke cut viewer ko jhatka deta hai; reason wala cut dikhai hi nahi deta
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — kmilo house rule (yeh editor test); YouTube official bhi 'cuts that do not serve a purpose confuse viewers' kehta hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-140 — Cut motion/action par — action shuru hone ke just baad
- **Purana ID:** A-057, C-005
- **Kab:** Kisi action/movement ke beech cut lagana ho
- **Kya:** Match-on-action: cut us pal ke just BAAD lagao jab action shuru ho chuka ho (darwaza khulna, haath uthna) — movement cut ko dhak deta hai aur motion onset aankh ko cut ke paar le jata hai. Movement shuru hone se pehle ke dead moment me cut mat lagao; gesture ya blink ke beech me bhi cut mat karo
- **Kyun:** Aankh movement ko follow karti hai; cut natural attention shift ka kaam karta hai — motion onset gaze ko naye shot me carry karta hai aur cut invisible ho jata hai
- **Kitni baar:** Har action-cut par
- **Evidence:** 🟢 — Eye-tracking studies me measured aur replicate hua result; AToCC (Tim Smith) isi par bana peer-reviewed theory hai; kmilo editing reference me bhi yahi creator practice ke roop me hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `science_tim_smith.md`

### R-141 — J/L cuts scene badlaav naram karne ke liye
- **Purana ID:** A-058
- **Kab:** Scene ya speaker badle aur transition kathin lage to
- **Kya:** Agli awaaz ko tasveer se pehle aane do (J cut) ya pichli awaaz ko tasveer badalne ke baad rehne do (L cut); offset kuch frames se ~2 s tak; tutorial me inka istemal kam
- **Kyun:** Awaaz ka nirantar flow scene ka badlaav mehsoos hi nahi hone deta
- **Kitni baar:** Scene/speaker changes par zarurat ke hisaab se
- **Evidence:** 🟠 — Creator source (TechSmith) — offset ke liye koi pakka number source nahi deta
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-142 — Jump cuts ka sahi istemal
- **Purana ID:** A-059
- **Kab:** Single-camera talking head se filler hatana ho to
- **Kya:** Jump cuts hi sahi tareeka hain; inhe naram karne ke liye alternate cut par punch-in ya B-roll cover lagao; interview/multicam me jab asli angle maujood hai to jump cut kabhi nahi; subject ko mid-gesture me pakde hue mat chhodo
- **Kyun:** YouTube khud tight talking head ke liye jump cuts ki salah deta hai; bina cover ke lagatar jump cuts kathin lagte hain
- **Kitni baar:** Har take me filler positions par
- **Evidence:** 🟡 — YouTube official recommendation (platform) + kmilo creator refinements
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-143 — Pacing varied rakho, metronome nahi
- **Purana ID:** A-060
- **Kab:** Poori edit ka rhythm banate waqt
- **Kya:** Tez hisso ke baad wohi lamba hold rakho jahan key point land karta hai; ek hi scene ke andar bhi sabse dheemi animation sabse tez ki ~3 guna ho sakti hai; har cheez ko ek hi gati par mat chalao
- **Kyun:** Ek-si gati thoda samay baad sunai/dikhai dena band ho jati hai; contrast hi dhyaan banata hai
- **Kitni baar:** Har section par
- **Evidence:** 🟠 — kmilo creator rules + motion-principles reference
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-144 — Cuts music ki phrase par
- **Purana ID:** A-061
- **Kab:** Music ke saath edit karte waqt
- **Kya:** Cuts aur loops music ki phrases par rakho, mid-note par nahi; video ka ant music ke asli ending ya saaf fade par ho; foreground music (music video/promo) me key cuts downbeat par rakho; music-led video me cuts beats par rakho
- **Kyun:** Phrase ke beech kata music bina bole hi galat lagta hai; phrase par kata hua mehsoos hi nahi hota
- **Kitni baar:** Music wale har section par
- **Evidence:** 🟠 — Creator practice (kmilo music reference; ExpoCut ke music-beat cuts iske saath — Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_expocut_claude-plugin_retention-playbook.md`

### R-145 — Punch ki hadd: lambaai, doori, ginti ⚙️
- **Purana ID:** A-062
- **Kab:** Talking reel me visual punch (clip/still/board/super) lagate waqt
- **Kya:** Clip punch <3.0 s rakho (zyada lamba = woh cutaway ho gaya); still punch 3.5 s; super wala segment 3.5-4.0 s; do punches ke beech A-roll ≥3.0 s rakho, warna punches ko butt karo; punches ≤10/min; stills ≤2 per reel aur lagatar kabhi nahi; still apne noun ke 0.3 s ke andar shuru ho, clip punch ki window 0.8 s
- **Kyun:** Bina hadd ke punches poori reel ko shor bana dete hain aur punch ka matlab hi khatm ho jata hai
- **Kitni baar:** Har reel par (yeh mktkit ke QA gates se enforce hote hain)
- **Evidence:** 🟠 — mktkit owner/reviewer ke khade kiye hue rules (asal reviewer catches se bane)
- **Sources:** `github_1610-advisory_mktkit.md`
- **Check:** `{"kind": "max_per_min", "what": "punch", "value": 10}`

### R-146 — B-roll ki ginti (paper-stage shorts)
- **Purana ID:** A-063
- **Kab:** Short ke liye B-roll lagate waqt (Melvynx system)
- **Kya:** B-roll zyada se zyada har 8-15 s me ek, 2-5 s ka; do B-roll ke beech ~5 s creator screen par; clip tabhi jab image sentence se fit ho; achha hit na mile to board ya creator hi rakho, random clip kabhi nahi
- **Kyun:** Har doosri line par clip pura lagne ki jagah pura hi bekaar lagta hai; kam aur fit B-roll hi premium feel deta hai
- **Kitni baar:** Har short par
- **Evidence:** 🟠 — Melvynx shorts broll house rules
- **Sources:** `github_Melvynx_video-agent-skills.md`
- **Takraav note:** mktkit ke punch system me punches 10/min (har ~6 s) tak ja sakte hain — woh talking-reel ka alag system hai; ye 8-15 s wali cadence paper-stage shorts ki hai; format ke hisaab se chuno, dono ko mat milao (dekho CONFLICTS.md)

### R-147 — Retakes aur false starts hatao
- **Purana ID:** A-064
- **Kab:** Talking footage ki pehli safaai karte waqt
- **Kya:** Har line ka aakhra complete attempt rakho; false starts, half-words, 'uh', off-script awaazein ('wait, redo that') drop karo; chhupe retake ke nishan pehchano: 0.6 s se lamba koi shabd, bola hua phrase dohraaya, ya be-matlab shabd
- **Kyun:** Retake wali gandagi hi raw footage ko amateur banati hai; saaf spine ke bina koi style kaam nahi karta
- **Kitni baar:** Har take par, style se pehle
- **Evidence:** 🟠 — Melvynx script-first pipeline ka house rule + kmilo retake rules
- **Sources:** `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`

### R-148 — Podcast me camera jo bole us par
- **Purana ID:** A-065
- **Kab:** Multicam podcast/interview cut karte waqt
- **Kya:** Jo bol raha hai uska close-up rakho; speaker badle to badlaav ke ek beat baad cut karo; reaction shot sirf tab jab woh kuch kahe; wide shot shuruaat, topic change aur cross-talk ke liye rakho; timer par angle kabhi mat badlo; lambi monologue me close/medium/wide ya punch-in ghumao
- **Kyun:** Camera speaker ko follow kare to baat-cheet dekhna aasan hota hai; timer wale cuts nakli lagte hain
- **Kitni baar:** Poore episode par; koi pakki frequency nahi — speaker changes hi trigger hain
- **Evidence:** 🟠 — kmilo podcast recipe; source khud kehta hai iske liye koi authoritative frequency number nahi hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-149 — Hard-out hamesha shabd ke end par
- **Purana ID:** A-066
- **Kab:** Clip ya reel ka ant tay karte waqt
- **Kya:** Video ka end hamesha aakhri rakhe hue shabd ke END par rakho; ant kabhi SRT cue ke end se mat nikalo (wah aadha sentence late ho sakta hai)
- **Kyun:** Cue timing aur asli awaaz ka end alag hote hain — galat ant par video latka hua ya kata hua lagta hai
- **Kitni baar:** Har edit ke ant par
- **Evidence:** 🟠 — mktkit cut-video engine ka rule (asal defect se bana)
- **Sources:** `github_1610-advisory_mktkit.md`

### R-150 — Tutorial shots aur speed
- **Purana ID:** A-067
- **Kab:** Tutorial edit karte waqt
- **Kya:** Shots ≥5 s rakho; navigation, clicks aur results 1x par; typing zyada se zyada 1.5x; dead time ko speed se nahi, clean cut se hatao; app ki apni animation (modal khulna, loading) ke beech cut mat karo; form kabhi screen par kata hua mat dikhao (submit sirf clicked state me)
- **Kyun:** Tutorial ka kaam follow karwana hai — tez ya kata hua step viewer ko kho deta hai
- **Kitni baar:** Har tutorial shot par
- **Evidence:** 🟠 — kmilo house rules (reference tutorial review se)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-151 — Bolne ki gati type ke hisaab se
- **Purana ID:** A-068
- **Kab:** Script ki lambaai aur pace tay karte waqt
- **Kya:** Technical/tutorial narration 120-150 wpm rakho; short script ka default pace ~160 wpm; script ki lambaai shabdo ki ginti ko pace se bhaag de kar napo (bole hue runtime ke hisaab se likho)
- **Kyun:** Gati hi samajh ka samay deti hai; tez script bechne me bhi aur samjhane me bhi haarti hai
- **Kitni baar:** Har script par
- **Evidence:** 🟠 — Creator practice (kmilo pacing + Melvynx script-length defaults)
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-152 — Short ki lambaai ke targets
- **Purana ID:** A-069
- **Kab:** Short-form video ki lambaai tay karte waqt
- **Kya:** Targets rakho lekin idea ko lambaai tay karne do, platform ki max ko nahi: TikTok entertainment 21-34 s (educational 60-90 s), Shorts 15-30 s, Reels 7-15 s punchy ya 30-60 s value; Melvynx ke naape hue hits 25-40 s aur 30-60 s aam range hai, 45 s se neeche completion behtar
- **Kyun:** Jo lambaai idea se zyada hai woh completion% gira kar video ko dabati hai
- **Kitni baar:** Har short par
- **Evidence:** 🟠 — Creator guidance (ExpoCut playbook — Free to use and redistribute with attribution to expocut.com; Melvynx ke measured ranges)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_Melvynx_video-agent-skills.md`, `github_kmilo93sd_agent-video-editor.md`

### R-153 — Lambe content ko 6 min ke blocks me baanto
- **Purana ID:** A-070
- **Kab:** Lamba educational content banate waqt
- **Kya:** Content ko 6 minute se chhote blocks/chapters me baanto; lambi process ho to ek step = ek video rakho
- **Kyun:** Measured data (6.9M sessions) me 6 minute ke baad engagement girna shuru hota hai — chhote blocks wale videos zyada dekhe jate hain
- **Kitni baar:** Har lambe video ki planning par
- **Evidence:** 🟡 — Guo et al. 2014 — edX ke 6.9 million sessions ka measured study
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-154 — Verify loop: dikhane se pehle filmstrip check
- **Purana ID:** A-071
- **Kab:** Render ya delivery se pehle
- **Kya:** Poori video ko filmstrip/contact sheet par check karo: pehle 3 s (hook frame 0 par padh sakte ho?), poori lambaai (koi 5 s window bina change ke to nahi?), text ke safe-zone numbers (y ≥14, y+h ≤79, x+w ≤86); mktkit ka machine QA gate pass karo; render se pehle stills par iterate karo — stills seconds me bante hain, renders minutes me
- **Kyun:** Jo galti sheet par dikh jati hai woh publish ke baad pakadne se sasti padti hai; aadha kaam yahi pakda jata hai
- **Kitni baar:** Har render/delivery par
- **Evidence:** 🟠 — Teeno sources ke house QA workflows (ExpoCut SVR loop — Free to use and redistribute with attribution to expocut.com; mktkit gate; Melvynx stills rule)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`, `github_1610-advisory_mktkit.md`, `github_Melvynx_video-agent-skills.md`

### R-155 — Pattern interrupt har 15–30s (CraigHewitt wala cadence) ⚙️
- **Purana ID:** B-044
- **Kab:** Long-form main content ke edit par
- **Kya:** Viewer ka dhyaan har 15–30s reset hota hai — itne gap ke andar kuch visual zaroor badlo: cut, angle change, text overlay, B-roll, zoom ya SFX. Koi frame 30s se zyada static na rahe
- **Kyun:** Autopilot par gaya viewer chala jata hai; regular pattern interrupt use jagaye rakhta hai (editor ka anubhav)
- **Kitni baar:** Har 15–30s kam se kam 1 visual change; static frame max 30s
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 30}`
- **Takraav note:** ⚠️ Seedha takraav slopstudio ke B-045 se: wahan measured corpus me pacing FLAT mili aur pattern interrupt sirf ~1 per ACT hai, per minute nahi. Dono rules rakhe gaye hain — Step 3 (Order) me faisla hoga ki kis format/genre par kaun sa jeetega. (dekho CONFLICTS.md)

### R-156 — Pacing FLAT rakho, interrupt ~1 per act (slopstudio wala cadence) ⚙️
- **Purana ID:** B-045
- **Kab:** Long-form (10–55 min) explainers ke edit par
- **Kya:** Per-minute pacing poori video me flat rakho — words aur cuts kisi minute me decay na hon, beech saggy na ho, end par frantic ramp bhi nahi. Pattern interrupt sirf ~1 per act rakho (skit/prop/gag/location change), per minute wala interrupt mat lagao. Consistency escalation se jeet-ti hai
- **Kyun:** Measured corpus (5 top explainers, 54 min tak ki videos) me pacing flat mili — yahi invariant tha, cut count nahi
- **Kitni baar:** ~1 pattern interrupt per act; har minute ka pacing lagbhag ek jaisa
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "max_per_act", "what": "pattern_interrupt", "value": 1}`
- **Takraav note:** ⚠️ Seedha takraav CraigHewitt ke B-044 se: wahan interrupt har 15–30s manga gaya hai. Dono rakhe gaye hain — Step 3 (Order) decide karega (genre/format ke hisaab se alag jeet sakte hain). (dekho CONFLICTS.md)

### R-157 — Visual floor = perceived motion, cut count nahi ⚙️
- **Purana ID:** B-046
- **Kab:** Long-form edit ki review par
- **Kya:** Cut count ka koi fixed number mat rakho (corpus range 2.8–7.5 cuts/min — koi invariant nahi). Asli floor: screen par kuch relevant hamesha MOVING ho — footage/diagram ke neeche floating host, in-shot animation (bars bharna, typewriter), ya bare host ke peeche ambient-motion backdrop. Static host + static frame >~15s = violation; 30–50s ka ek shot sirf tab bachta hai jab in-shot animation ya high narrative tension use uthaye
- **Kyun:** Naapa gaya invariant motion hai, cuts ki ginti nahi; ruka hua frame hi asal retention hole hai
- **Kitni baar:** Har shot par; static host+frame ~15s se zyada nahi (animation/tension exception ke saath)
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 15}`

### R-158 — Hook/fast sections me visual change har 3–5s ⚙️
- **Purana ID:** B-047
- **Kab:** Video ke hook (0:00–0:30) aur fast sections me
- **Kya:** Har 3–5s me cut/B-roll/zoom/angle/text me se kuch badlo; pehle 15s me text overlay, zoom aur B-roll — teeno ki high density rakho. Classicchins ki general rule bhi yahi hai: static talking head har 3–5s me todo
- **Kyun:** Shuruaat ki energy spoken hook ke barabar honi chahiye; static head sabse tez viewers khota hai
- **Kitni baar:** Hook section me har 3–5s; hook ke pehle 15s me teeno interrupts
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`, `github_classicchins_compounding-marketing.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 5}`
- **Takraav note:** Slopstudio ke measured cold open (B-048) me pehle 30s me sirf 2–7 cuts hain — ye usse tez hai. Aur shorts ke liye B-053 (2–4s) isse bhi tez hai. Format ke hisaab se alag number — Step 3 me saaf hoga. (dekho CONFLICTS.md)

### R-159 — Measured cold-open density: pehle 30s me 2–7 cuts ⚙️
- **Purana ID:** B-048
- **Kab:** Long-form cold open ki review par
- **Kya:** Pehle 30 seconds me 2–7 cuts rakho (aur words 65–98, dekho B-006); isse tez काटना measured corpus ke pattern se bahar hai
- **Kyun:** Top explainers ke naape gaye cold opens isi band me hain — tez hona hi retention nahi hai
- **Kitni baar:** Har long-form cold open; cuts 2–7 per first 30s
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "count_range", "what": "cuts_first_30s", "min": 2, "max": 7}`
- **Takraav note:** CraigHewitt/Classicchins ka B-047 hook me har 3–5s change mangta hai (30s me 6–10 changes) — ye measured band (2–7 cuts) se upar ja sakta hai. Dono rakhe hain; Step 3 faisla karega. (dekho CONFLICTS.md)

### R-160 — Section ke hisaab se pace badlo ⚙️
- **Purana ID:** B-049
- **Kab:** Long-form ke sections (Setup/Main/CTA) par
- **Kya:** Setup (0:30–2:00): medium pace, cut har 5–10s, context ke liye text overlay aur referred situations ke liye B-roll. Main (2:00–8:00): content ki energy ke hisaab se pace. CTA/Outro (aakhri 30–60s): medium-to-slow, winding down, end screen overlay + final text reinforcement
- **Kyun:** Har section ka kaam alag hai; ek jaisa pace sab jagah galat hai
- **Kitni baar:** Setup me cut har 5–10s; outro aakhri 30–60s medium-slow
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 10}`

### R-161 — Edit ki energy = content ki energy
- **Purana ID:** B-050
- **Kab:** Poori video ke pacing decisions par
- **Kya:** Edit rhythm ko content ki natural energy se milao — slow reflective pal par tez cuts/zooms mat lagao, high-energy listicle par dheela pace mat rakho. Pace ko deliberately vary karo: uniformly intense video utna hi thakane wala hai jitna flat video
- **Kyun:** Contradiction wala edit viewer ko khichta hai; har jagah ek jaisi intensity thakan ban jati hai
- **Kitni baar:** Har section/beat par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`, `github_humbertobellor_henterprise.md`

### R-162 — Dead air aur filler beherahmi se kato ⚙️
- **Purana ID:** B-051
- **Kab:** Edit par, khaaskar pehle 30 seconds me
- **Kya:** 'Ums', pauses, throat-clearing, repeated points aur tangents kato. Silence >1s kato (exception: intentional dramatic pause + dramatic visual). Pehle 30s me har pause/restart/filler BINA exception kato; baad me thodi breathing room chalegi — relentlessly tight edit thaka deta hai. Poori video ka total unintentional dead air <5s rakho
- **Kyun:** Dead air retention ka dushman hai; lekin saans ki jagah marna bhi delivery ko synthetic/thakane wala banata hai
- **Kitni baar:** Silence >1s = cut; first 30s zero tolerance; total dead air <5s
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`, `github_classicchins_compounding-marketing.md`, `github_humbertobellor_henterprise.md`
- **Check:** `{"kind": "max_silence_s", "value": 1}`
- **Takraav note:** Filnik ke performance rule (B-071) me 1–2s ki jaan-boojh wali khamoshi 'extremely powerful' kahi gayi hai. Takraav nahi hai agar pause INTENTIONAL ho aur visual use uthaye (CraigHewitt khud yahi exception deta hai) — bina wajah ki khamoshi hamesha kategi. (dekho CONFLICTS.md)

### R-163 — Narration 160–195 WPM band me rakho ⚙️
- **Purana ID:** B-052
- **Kab:** Long-form narration/voiceover par
- **Kya:** Narration speed 160–195 WPM rakho (energetic, rushed nahi). <150 WPM sirf dense math/technical beats ke liye rakho — purana 130–150 default is genre ke liye zyada dheema hai
- **Kyun:** Paanchon measured reference videos isi band me mile; dheemi narration pacing ko saggy banati hai
- **Kitni baar:** Har minute 160–195 WPM (flat pacing ke saath, B-045)
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "wpm_range", "what": "narration", "min": 160, "max": 195}`

### R-164 — Shorts cadence: cut har 2–4s, VVSA target 70–90% ⚙️
- **Purana ID:** B-053
- **Kab:** Shorts (portrait, natural-rate speech) par
- **Kya:** Cut har 2–4s rakho; har 20s me 6–12 visual changes; captions hamesha (B-033). Target VVSA (viewed vs swiped-away) 70–90%. Short ki length wo rakho jahan tak near-100% VVSA hold ho — 30s ki cap mat lagao. (Filnik ki post-production checklist bhi fast cuts har 2–4s kehti hai.)
- **Kyun:** Shorts ka algorithm swipe-away se darta hai; naapi gayi cadence aur VVSA band top shorts ke pattern hain
- **Kitni baar:** Cut har 2–4s; 6–12 visual changes / 20s; VVSA 70–90%
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers + Filnik practice checklist
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`, `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 4}`

### R-165 — Long-form APV target 40–55% ⚙️
- **Purana ID:** B-054
- **Kab:** Long-form ki performance target/review par
- **Kya:** Average Percentage Viewed ka target 40–55% rakho (≥50% = A-grade). Raw minutes nahi, percentage + hook ko optimize karo
- **Kyun:** Lambi video ka asal score uska dekha gaya hissa hai; percentage hi formats ke beech tulna ke layak hai
- **Kitni baar:** Har long-form video ka target APV 40–55%
- **Evidence:** 🟡 — measured reference corpus (5 top explainers, 246k–1M views) se nikale gaye numbers
- **Sources:** `github_Francesco149_slopstudio_retention-editing.md`
- **Check:** `{"kind": "percent_range", "what": "average_percentage_viewed", "min": 40, "max": 55}`

### R-166 — Long-form B-roll/screen-share cadence (CraigHewitt) ⚙️
- **Purana ID:** B-055
- **Kab:** Long-form talking-head edit par
- **Kya:** B-roll insert har 30–60s me kam se kam ek baar aaye; aur har 2 minute me kam se kam ek B-roll segment ya screen share zaroor ho
- **Kyun:** Lambi talking-head monotony retention ko dheere-dheere khaati hai; regular visual break use rokta hai
- **Kitni baar:** B-roll har 30–60s; ≥1 B-roll/screen-share per 2 min
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`
- **Check:** `{"kind": "max_gap_s", "what": "broll_or_screen_share", "value": 120}`
- **Takraav note:** Classicchins ka B-056 marketing videos ke liye B-roll har 5–10s mangta hai — ye usse kahin dheema hai. Farak format ka hai (lamba talking-head vs chhota marketing video); B-032 ka relevance gate dono par lagu rahega. (dekho CONFLICTS.md)

### R-167 — Marketing video me B-roll har 5–10s (Classicchins) ⚙️
- **Purana ID:** B-056
- **Kab:** Chhote marketing/social videos ke edit par
- **Kya:** Har 5–10s me B-roll lao — screen recording, stock footage, chart/animation/data-viz, ya customer/team photo
- **Kyun:** Chhote format me dhyaan ka cycle tez hota hai; regular visual badlav hi pace banata hai
- **Kitni baar:** Har 5–10s ek B-roll beat
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`
- **Check:** `{"kind": "max_gap_s", "what": "broll", "value": 10}`
- **Takraav note:** CraigHewitt ka B-055 long-form ke liye 30–60s ka gap deta hai — format ke hisaab se alag number. B-032 (relevance gate) dono par lagu: cadence ke liye bekaar B-roll nahi. (dekho CONFLICTS.md)

### R-168 — Music change = tonal shift ka signal
- **Purana ID:** B-057
- **Kab:** Major section transitions par
- **Kya:** Music sirf major section transitions par badlo, taaki wo tonal shift ka signal bane
- **Kyun:** Music ka badlav viewer ko bina kahe batata hai ki kahani naye hisse me gayi
- **Kitni baar:** Har major section transition par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`

### R-169 — Retention beat par visual punctuation
- **Purana ID:** B-058
- **Kab:** Script ke har retention beat par (aur steady-decline fix me har 2–3 min par)
- **Kya:** Retention beat aate hi visual punctuation lagao: zoom + text overlay + brief pause ka combo
- **Kyun:** Beat ka kaam viewer ko phir jodna hai; sirf shabdon se wo jod kamzor padta hai
- **Kitni baar:** Har retention beat par; steady decline dikhe to beats har 2–3 min par rakho
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`

### R-170 — CTA/Outro ghatao: CTA segment aakhri 5–10s ⚙️
- **Purana ID:** B-059
- **Kab:** Video ke end par
- **Kya:** Outro ko winding-down rakho — end screen overlay + final text reinforcement. CTA (logo + URL + clear CTA visual) aakhri 5–10s me aaye. Agar end drop-off dikhe to ending aur chhota karo aur CTA ko pehle le aao, aur end screen content ko tease karo ('Before you go — the next video I'd recommend is…')
- **Kyun:** Content 'khatam' mehsoos hote hi viewer CTA se pehle nikal jata hai; chhota outro aur specific CTA use rokta hai
- **Kitni baar:** CTA aakhri 5–10s; outro total ~30–60s se zyada nahi
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`, `github_classicchins_compounding-marketing.md`
- **Check:** `{"kind": "duration_range_s", "what": "cta_segment", "min": 5, "max": 10}`

### R-171 — End screen tab rakho jab retention 70–80% ho ⚙️
- **Purana ID:** B-060
- **Kab:** MrBeast-style videos ke end par
- **Kya:** Video ko aakhri second tak high attention par rakho aur end screen us point par rakho jahan retention 70–80% ke aas-paas ho
- **Kyun:** End screen tabhi kaam karta hai jab viewer wahan tak ruka ho; tez retention wala end next video ka click lata hai (MrBeast profile)
- **Kitni baar:** Har aise video ke end par; target retention-at-end-screen 70–80%
- **Evidence:** 🟡 — creator-reported retention practice (MrBeast profile) — measured claim creator ki taraf se, independent study nahi
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "percent_range", "what": "retention_at_end_screen", "min": 70, "max": 80}`

### R-172 — Platform duration windows (Reels/TikTok) ⚙️
- **Purana ID:** B-061
- **Kab:** Short-form ka format chunne par
- **Kya:** Reels: optimal 15–30s (reach ka sweet spot), max recommended 60s, 9:16, 1080×1920. TikTok: optimal 15–45s, max recommended 60s (is content type ke liye), 9:16
- **Kyun:** Har platform ka dhyaan window alag hai; sweet spot se bahar ki length distribution ko nuksan karti hai (playbook ke numbers)
- **Kitni baar:** Har short, platform ke hisaab se
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "duration_range_s", "what": "reels_duration", "min": 15, "max": 30}`

### R-173 — ASL modern band me rakho ⚙️
- **Purana ID:** C-001
- **Kab:** Fast-paced popular-format video ki shot planning/cutting par
- **Kya:** Average shot length lagbhag 3-6 second ke band me rakho; isse kahin lambi stretches modern audience ko slow/old lagti hain
- **Kyun:** Cutting ke 150-film corpus (1935-2005) me ASL ~15s se ~3.5s tak gira aur hit films isi band ki taraf evolve hui
- **Kitni baar:** Poori video ka average is band me; individual shots isse bahar ja sakte hain
- **Evidence:** 🟡 — Measurement 🟢 hai (peer-reviewed corpus), lekin 'is band se retention badhega' ek inference hai, A/B test nahi
- **Sources:** `science_james_cutting.md`
- **Check:** `{"kind": "duration_range_s", "what": "avg_shot_length", "min": 3, "max": 6}`

### R-174 — Metronome cut kabhi nahi, lehren (waves) banao
- **Purana ID:** C-002
- **Kab:** Consecutive shots ki length sequence set karte waqt
- **Kya:** Shot lengths ko fixed beat par mat rakho; paas wale shots ek jaise lambai ke hon, lekin sequence me chhote shots ke clusters bade stretches ke andar neste hue waves (1/f jaisi rhythm) banein
- **Kyun:** Modern films ki shot-length sequence human attention ke natural 1/f fluctuation pattern ki taraf evolve hui hai
- **Kitni baar:** Poori video par lagu; lambi ek-jaisee length wali run = violation
- **Evidence:** 🟡 — 1/f pattern corpus me measured 🟢 hai; use editing rule banana application-level inference hai
- **Sources:** `science_james_cutting.md`

### R-175 — Climax par shots chhote, payoff ke baad lambe
- **Purana ID:** C-003
- **Kab:** Sequence apne climax/payoff ki taraf badh rahi ho
- **Kya:** Payoff ke paas jaate jaate shots progressively chhote karo aur motion badhao; payoff ke baad shots lambe karo taaki moment land kare
- **Kyun:** Cutting ke 'evolution of pace' pattern ke mutabiq films climax ki taraf pace accelerate karti hain
- **Kitni baar:** Har bade payoff/climax par ek baar
- **Evidence:** 🟡 — Ye pattern sirf search-result abstract me dikha, paper full nahi khula — UNVERIFIED-in-full, isliye pakka 🟢 nahi
- **Sources:** `science_james_cutting.md`

### R-176 — Cutting speed ki ceiling — re-fixation ka waqt do
- **Purana ID:** C-008
- **Kab:** Cutting rate bahut tez ho jaye (action montage, intensified style)
- **Kya:** Itna tez mat kato ki viewer do cuts ke beech dobara fixate hi na kar paye; us point ke aage slow karo ya ek shot hold karo — zyada cuts wahan excitement nahi, fatigue aur habituation dete hain
- **Kyun:** Hyper-fast cutting me gaze centre-frame par jam jati hai, arousal flatten ho jata hai aur viewer bore hota hai (Smith ki Bond/Bay analyses)
- **Kitni baar:** Jab bhi cutting rate extreme ho; lambe tez sequences par khaas dhyaan
- **Evidence:** 🟡 — Centre-fixation collapse measured observation hai; 'fatigue/boredom' wala nishkarsh Smith ki apni interpretation hai
- **Sources:** `science_tim_smith.md`
- **Takraav note:** Tez-cadence wale dusre rules (jaise pattern interrupts) se takraav ho to ye ceiling jeetni chahiye — Step 3 confirm kare (dekho CONFLICTS.md)

### R-177 — Cut situation-change par lagao
- **Purana ID:** C-009
- **Kab:** Situation badle — nayi location, naya goal, naya character interaction me aaye, nayi cause/topic shuru ho
- **Kya:** Cut exactly us boundary par lagao; wahan cut invisible lagta hai kyunki dimaag waisi hi apna event model update kar raha hota hai
- **Kyun:** Dimaag experience ko events me baant ta hai; boundary prediction fail hone par mehsoos hoti hai aur fMRI responses exactly unhi palon par aate hain
- **Kitni baar:** Har bade situation change par
- **Evidence:** 🟢 — EST: Psychological Bulletin theory paper + film par fMRI study (n=24, The Red Balloon) — converging evidence
- **Sources:** `science_jeffrey_zacks.md`

### R-178 — Mid-event flow ki hifazat — be-wajah cut nahi
- **Purana ID:** C-010
- **Kab:** Situation wahi hai, event chal raha hai, prediction smoothly chal raha hai
- **Kya:** Bina wajah ke mid-event cut mat lagao; aisa cut viewer ko ek model-update par majboor karta hai jo use chahiye hi nahi tha — jolt/error jaisa lagta hai
- **Kyun:** Jab kuch nahi badla, dimaag ka event model stable hai; zabardasti ka cut usi stability ko todta hai
- **Kitni baar:** Har mid-event segment par
- **Evidence:** 🟢 — Segmentation automatic hai aur passive viewing me bhi hoti hai — behavioural + fMRI evidence
- **Sources:** `science_jeffrey_zacks.md`
- **Takraav note:** Pattern-interrupt rules (C-033/C-034) se satahi takraav hai; interrupt ek deliberate design hona chahiye, aadat nahi (dekho CONFLICTS.md)

### R-179 — Murch 3 — Rhythm sahi pal par (10%)
- **Purana ID:** C-016
- **Kab:** Cut ka exact pal chunna ho
- **Kya:** Cut us pal par lagao jo rhythmically 'sahi' lage — na jaldi, na der; rhythm story aur emotion ke neeche hai, unke upar kabhi nahi
- **Kyun:** Rhythm teesra criterion hai; top-3 (emotion+story+rhythm) aapas me gehri tarah jude hain
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — Craft wisdom; rhythm ka hona measured hai (Cutting/Smith) lekin ye weight Murch ki raay hai
- **Sources:** `science_walter_murch.md`

### R-180 — Hook ki lambai 9-24 shabd ⚙️
- **Purana ID:** C-024
- **Kab:** Spoken hook line likhte waqt
- **Kya:** Hook line 9-24 shabdon ke band me rakho — ~150 wpm par ye 10 second ke andar boli ja sakne wali lambai hai. Isse chhoti = signal kam, lambi = saans aur dhyaan dono khatm
- **Kyun:** hookscore.py ka brevity band calibrated hooks ke data se aaya hai
- **Kitni baar:** Har spoken hook par
- **Evidence:** 🟡 — 74-hook calibration set se derived band hai
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`
- **Check:** `{"kind": "word_range", "what": "hook", "min": 9, "max": 24}`
- **Takraav note:** Shorts ke spoken hook ke liye SkillMedev ki limit aur sakht hai (<12 shabd, C-037) — Shorts par wahi jeetegi (dekho CONFLICTS.md)

### R-181 — Pattern interrupt har 90-120 second ⚙️
- **Purana ID:** C-033
- **Kab:** Long-form body chalte waqt
- **Kya:** Har 90-120 second me ek pattern interrupt lagao: naya camera angle, bold on-screen graphic, rhetorical question, ya chhoti story. 150 wpm par ye har 225-300 shabdon me ek hai. Script me [PATTERN INTERRUPT] flag karo taaki editor use jaanboojh kar lagaye, accident se nahi
- **Kyun:** Ek jaisi presentation par dhyaan decay hota hai; interrupt attention reset karta hai
- **Kitni baar:** Har 90-120s; poori video me barabar phaila hua
- **Evidence:** 🟠 — SkillMedev ki timing rule; koi measured study cited nahi
- **Sources:** `github_SkillMedev_skills.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 120}`
- **Takraav note:** Isi cluster ke CraigHewitt (cluster B) wale 15-30s cadence se ye bahut dheema hai, aur slopstudio ke flat-pacing se tez — Step 3 is takraav ka faisla karega (dekho CONFLICTS.md)

### R-182 — Har section break par re-hook
- **Purana ID:** C-034
- **Kab:** Long-form me natural section break aaye; khaas taur par 30-60s ke aas-paas
- **Kya:** Har section break par chhota re-hook lagao: aane wali cheez ki ek-line tease ('lekin teesri wali ne asal me numbers hilaye'), ya pattern interrupt (B-roll cut, location change, on-screen callout), ya ek chhota payoff bump jo curve uthaye. 30-60s ke paas ek re-hook lazmi rakho
- **Kyun:** Retention sirf pehle 30s me nahi rehta; flat/rising curve suggested placement dilata hai
- **Kitni baar:** Har section break par; 30-60s par ek pakka
- **Evidence:** 🟠 — serge retention-beats ki rule
- **Sources:** `github_sergebulaev_youtube-skills.md`
- **Takraav note:** C-033 (har 90-120s interrupt) se sambandhit hai lekin placement logic alag hai — ye waqt par nahi, section boundaries par lagta hai (dekho CONFLICTS.md)

### R-183 — Loop design jaanboojh kar chuno
- **Purana ID:** C-041
- **Kab:** Short-form video ka ending design karte waqt
- **Kya:** Teen me se ek loop type chun kar design karo: seamless (last frame = first frame — position, scale, color same), hook-back (aakhri line/visual viewer ko shuruaat par wapas bheje), ya hard stop (puri kahani ke liye saaf CTA end card). Loop apne aap par mat chhodo
- **Kyun:** Feed turant replay karta hai; deliberate loop muft ka extra watch-time hai aur loop-through Shorts ka sabse mazboot signal mana jata hai
- **Kitni baar:** Har Short par ek type, jaanboojh kar
- **Evidence:** 🟠 — SkillMedev social-video-formatter + serge Y10 + Jake yt-shorts (loop point) — teenon sources
- **Sources:** `github_SkillMedev_skills.md`, `github_sergebulaev_youtube-skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`

### R-184 — Dead air trim — gap beech se, saansein bacha kar ⚙️
- **Purana ID:** C-042
- **Kab:** Transcript se edit decision list banate waqt
- **Kya:** Spoken cues ke beech floor (default 0.45s) se bade gaps ko BEECH se trim karo — dono taraf breath bache (floor/2 each side). Speech se chipka kar cut karne se take gasping lagta hai
- **Kyun:** Dead air pacing ko marta hai, lekin zero-breath cut bhi unnatural lagta hai; beech se trim dono bacha leta hai
- **Kitni baar:** Har gap > 0.45s par (floor badla ja sakta hai)
- **Evidence:** 🟠 — deadair.py ka default floor aur trim logic — tool author ki craft setting
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`
- **Check:** `{"kind": "max_gap_s", "what": "speech_gap", "value": 0.45}`
- **Takraav note:** Pause ke teen alag model is cluster me hain: ye (floor + beech-trim), blazerior ka remainder 0.2-0.3s (C-072), pifferologo ke silence thresholds + padding (C-091/C-092) — Step 3 me ek model final hoga (dekho CONFLICTS.md)

### R-185 — Filler-only cues hatao
- **Purana ID:** C-043
- **Kab:** Transcript clean karte waqt
- **Kya:** Jo cue sirf filler hai ('um', 'so yeah', 'basically', 'you know') use poora hatao — wo koi information nahi deta
- **Kyun:** Filler-only hissa sirf runtime aur susti badhata hai
- **Kitni baar:** Har filler-only cue par
- **Evidence:** 🟠 — deadair.py ki FILLER category
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`
- **Takraav note:** Dhyaan: filler HATAO sirf jab cue sirf filler ho; bolne ki natural texture bachane wali baat dusre cluster (PandaStudio) me hai — takraav Step 3 dekhega (dekho CONFLICTS.md)

### R-186 — Retake/restart pehchano aur kato
- **Purana ID:** C-044
- **Kab:** Ek hi sentence dobara shuru hui ho
- **Kya:** Restart ko pichle ASAL speech cue se compare karo (beech wala 'um' cue asli pichla nahi hota); pehle 5 shabd match hon to pehli koshish hatao, dusri rakho
- **Kyun:** Zyada tar retakes ke beech ek filler hota hai — literal pichle cue se compare karne se wo miss ho jate hain
- **Kitni baar:** Har restart par
- **Evidence:** 🟠 — deadair.py ki REPEAT detection logic
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`

### R-187 — Retention diagnosis — leak, cliff, slide alag ilaaj
- **Purana ID:** C-045
- **Kab:** Publish hue video ki retention report padhte waqt
- **Kya:** Teen problems ko alag pehchano: HOOK LEAK (pehle 30s ka nuksan; 25% se kam = healthy; ilaaj hamesha pehli 15s ki script hai, edit nahi), CLIFFS (ek tez drop = ek moment — bina signpost ka topic change, sponsor read, lamba setup; transcript se dekho wahan kya kaha ja raha tha), SLIDE (beech ka steady bleed = pacing; ilaaj cutting hai, rewriting nahi). Sabse bada ek leak naam karke ek hi badlav batao
- **Kyun:** Teeno ke kaaran aur ilaaj alag hain; galat diagnosis galat fix deta hai
- **Kitni baar:** Har retention review par
- **Evidence:** 🟠 — retention.py ke thresholds (25%/40% bands, 0.8% cliff) tool author ke heuristics hain, published study nahi
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`

### R-188 — Bolne ki raftaar budget — 150 wpm
- **Purana ID:** C-047
- **Kab:** Script ki lambai aur beat ki timing tay karte waqt
- **Kya:** Script ko 150 words per minute par budget karo; instruction/narration ke liye band 140-160 wpm hai. Har beat ke shabd uske time budget se zyada na hon — 8 second ka beat ~20 shabd hai, 50 nahi
- **Kyun:** Isse tez bolna follow karne walon ko peeche chhod deta hai; budget hi beat sheet ko sach banata hai
- **Kitni baar:** Har script/beat par
- **Evidence:** 🟠 — Dono sources ka shared convention (Jake runtime estimate, SkillMedev beat sheet + narration pace)
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`, `github_SkillMedev_skills.md`

### R-189 — Scene-type ke hisaab se duration
- **Purana ID:** C-051
- **Kab:** Storyboard me har scene ki lambai tay karte waqt
- **Kya:** Scene type se duration do: Hook/title card 2.5-3.5s; Text statement 2.5-4s (padhne ki speed ~2.5 shabd/sec — 7-shabd line ko ~3s chahiye); UI/product demo 4-6s (aankh ko dwell time chahiye); Proof/data 3-5s; Logo/CTA outro 2.5-4s. Hook sabse tez cut, Proof sabse slow. Total lamba ho to ek scene KATO — har scene ko speed up mat karo, rushed video nervous lagta hai
- **Kyun:** Alag scene types ko alag samay chahiye; flat ek-jaisa pacing slideshow banata hai
- **Kitni baar:** Har scene par
- **Evidence:** 🟠 — SkillMedev video-storyboard ki duration table (30fps par)
- **Sources:** `github_SkillMedev_skills.md`

### R-190 — Cut phrase ke end par, stopwatch par nahi
- **Purana ID:** C-071
- **Kab:** Talking-head footage cut karte waqt
- **Kya:** Pauses kato, ideas kabhi nahi. Cut hamesha phrase ke end par lagao; 'har N second me cut' wala stopwatch tareeka ideas ko beech se kaat deta hai. Jahan subject move kar raha ho wahan cut mat lagao — majboori ho to us pal ko infographic card se dhako
- **Kyun:** Talking-head me har sentence matlab uthata hai; aggressive cutting logic ko tod deta hai
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — blazerior pipeline ki cutting rules — asal builds par seekhi hui
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Takraav note:** pifferologo ke word-boundary rule (C-090) se milta hai lekin alag hai: ye phrase-level craft hai, wo word-level technical correctness (dekho CONFLICTS.md)

### R-191 — Har pause ka 0.2-0.3s bacha kar rakho ⚙️
- **Purana ID:** C-072
- **Kab:** Pause trim karte waqt
- **Kya:** Har pause ka 0.2-0.3 second hissa rehne do. Pause ko zero par collapse karna stutter jaisa sunai deta hai
- **Kyun:** Bolne ki natural saans hi take ko insaani rakhti hai; poori tarah chipka hua speech ghut ta hai
- **Kitni baar:** Har trim kiye pause par
- **Evidence:** 🟠 — blazerior ki build-tested rule
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Check:** `{"kind": "min_gap_s", "value": 0.2, "what": "pause_remainder"}`
- **Takraav note:** Jake ke dead-air model (floor 0.45s, beech se trim, ~0.225s har taraf) se talab mel khata hai; pifferologo ke padding (30-200ms) aur silence thresholds (≥400ms clean) se numbers ki bhasha alag hai — Step 3 me ek model bane (dekho CONFLICTS.md)

### R-192 — Dramatic pause ko haath mat lagao
- **Purana ID:** C-073
- **Kab:** Sawaal ke baad ya conclusion se pehle wala pause dikhe
- **Kya:** Use trim hi mat karo — wahan khamoshi hi kaam kar rahi hai (tension, ummeed, wazan)
- **Kyun:** Dramatic silence retention ka hissa hai, dead air nahi; use kaatna moment ko halka kar deta hai
- **Kitni baar:** Har dramatic pause par
- **Evidence:** 🟠 — blazerior ki do jagah dohraayi hui rule
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Takraav note:** Dead-air rules (C-042/C-092) ka ye jaanboojh kiya exception hai — engine ko dramatic pause pehchanna hoga ya human flag lagega (dekho CONFLICTS.md)

### R-193 — Panel rhythm — 2-8 second per panel ⚙️
- **Purana ID:** C-082
- **Kab:** Storyboard ke panels ki timing tay karte waqt
- **Kya:** Panel 2 second se kam aur 8 second se zyada na rakho — kam me padha nahi jata, zyada me wallpaper ban jata hai. Panels ke beech 0.3-1s saaf frame chhodo, warna wo aapas me ghul jate hain. Ek minute ke video me 8-12 panels. Ek hi panel type back-to-back kabhi nahi (list ke baad list = ek lambi text wall)
- **Kyun:** Panel screen ki state hai; uski umar hi padhne aur bore hone ke beech ki lakeer hai
- **Kitni baar:** Har panel par
- **Evidence:** 🟠 — blazerior storyboard ki rhythm table
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Check:** `{"kind": "duration_range_s", "max": 8, "min": 2, "what": "panel"}`

### R-194 — Har segment boundary par 30ms audio fade ⚙️
- **Purana ID:** C-089
- **Kab:** Segments jodte (concat) waqt
- **Kya:** Har segment ke shuru aur aakhir par 30ms ka audio fade lagao (afade in/out, d=0.03). 20ms se neeche click bachta hai, 50ms se upar audio sunai dene wala dip aata hai
- **Kyun:** Waveform ko zero-crossing se door kaatna click paida karta hai; fade use khamoshi se mita deta hai
- **Kitni baar:** Har segment boundary par
- **Evidence:** 🟠 — Do sources ka ek hi number (pifferologo Hard Rule 3 + blazerior troubleshooting #12) — dono ke asal builds par fix hua technical rule
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`, `github_blazerior_videoediting-claude-skill.md`
- **Check:** `{"kind": "fade_ms", "value": 30, "what": "segment_boundary"}`

### R-195 — Shabd ke beech me cut kabhi nahi
- **Purana ID:** C-090
- **Kab:** Koi bhi cut edge tay karte waqt
- **Kya:** Har cut edge ko transcript ke word boundary par snap karo. Shabd ke beech ka cut hamesha kharab lagta hai aur timing data use nasht karta hai
- **Kyun:** Cut ki sabse chhoti sahi ikai shabd hai; isse neeche jaana guesswork hai
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — video-use Hard Rule 6 — technical correctness rule
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`

### R-196 — Cut edge padding 30-200ms ki window ⚙️
- **Purana ID:** C-091
- **Kab:** Har cut edge ko final karte waqt
- **Kya:** Har cut edge ko 30-200ms ke beech pad karo. ASR (Scribe) timestamps 50-100ms drift karte hain — padding wahi drift socheta hai. Fast-paced ke liye tight, cinematic ke liye loose. Shipped example: pehle rakhe shabd se 50ms pehle, aakhri ke 80ms baad
- **Kyun:** Bina padding ke drift shabd ke kinare kaat deta hai; zyada padding pacing dheeli karti hai
- **Kitni baar:** Har cut edge par
- **Evidence:** 🟠 — video-use Hard Rule 7 — ek proven video par shipped values; window house standard hai
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Check:** `{"kind": "padding_range_ms", "max": 200, "min": 30}`
- **Takraav note:** Pause models ka takraav C-042/C-072 me note hai — ye padding cut EDGE ki hai, pause ki lambai ki nahi; Step 3 teeno ko ek saath rakhega (dekho CONFLICTS.md)

### R-197 — Silence ke cut thresholds (400 / 150 / 150) ⚙️
- **Purana ID:** C-092
- **Kab:** Silence gaps ko cut candidates ke roop me judged karte waqt
- **Kya:** Silence ≥400ms = aam taur par sabse saaf cut jagah. 150-400ms wale phrase boundaries visual check ke saath usable hain. <150ms = unsafe (mid-phrase hone ka khatra), wahan mat kato
- **Kyun:** Silence ki lambai hi batati hai ki wo phrase boundary hai ya shabd ke andar ki rukawat
- **Kitni baar:** Har silence candidate par
- **Evidence:** 🟠 — video-use cut-craft ke numbers — ek production pipeline ke tested thresholds
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Check:** `{"kind": "min_gap_s", "value": 0.4, "what": "clean_silence_cut"}`

### R-198 — Speaker handoff me 400-600ms hawa ⚙️
- **Purana ID:** C-093
- **Kab:** Ek speaker se dusre speaker par cut ho
- **Kya:** Do utterances ke beech 400-600ms ki hawa rakho. Fast-paced me kam, cinematic me zyada — ye taste call hai, lekin zero hawa hamesha galat hai
- **Kyun:** Handoff par saans hi 'ab dusra bol raha hai' ka signal hai
- **Kitni baar:** Har speaker handoff par
- **Evidence:** 🟠 — video-use cut-craft ke common values
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Check:** `{"kind": "min_gap_s", "max": 0.6, "min": 0.4, "what": "speaker_handoff"}`

### R-199 — Animation ka payoff bolne wale shabd par land kare
- **Purana ID:** C-101
- **Kab:** Narration ke saath overlay sync karte waqt
- **Kya:** Payoff shabd ka timestamp nikalo aur overlay ko reveal_duration pehle shuru karo, taaki landing frame bilkul us shabd par aaye. Bina is sync ke animation bolti baat se kata hua lagta hai
- **Kyun:** Drisht aur shabd ka ek pal par milna hi 'ye isi ke liye bana tha' wala ehsaas hai
- **Kitni baar:** Har sync-to-narration animation par
- **Evidence:** 🟠 — video-use ki payoff-timing rule
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Takraav note:** blazerior ke graphic timing (shabd se pehle card — cluster B) se sambandh Step 3 dekhega (dekho CONFLICTS.md)



### R-262 — Split edit default — audio/video ek point par na kaato ⚙️ *(naya — editor round)*
- **Purana ID:** D1-001
- **Kab:** Dialogue/interview editing me koi bhi cut lage
- **Kya:** Audio aur video ke cut points ko 6–12 frames offset rakho: J-cut (agle scene ki awaaz pehle) anticipation/transition ke liye, L-cut (pichli awaaz nayi tasveer par) reaction/emotional carry-over ke liye
- **Kyun:** Seedha cut baatcheet me jarring lagta hai; split edit se baat ka pravah aur ehsaas cut ke paar beh jata hai
- **Kitni baar:** Dialogue me lagbhag 80% cuts split edits hone chahiye (source ka daava)
- **Evidence:** 🟠 — Craft parampara/house rule (note); measured study nahi
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`
- **Check:** `{"kind": "percent_range", "what": "split_edit_share_pct", "min": 70, "max": 100}`

### R-265 — Rhythm editing — cut ko kisi taal par rakho *(naya — editor round)*
- **Purana ID:** D1-004
- **Kab:** Sequence ki cutting ki lay tay karni ho
- **Kya:** Cuts ko in chaar taal me se kisi ek par rakho: music ke beats, tension ke saath badhti speed (emotional rhythm), shaant hisso me saans ki gati (breathing rhythm), ya bolne wale ki cadence
- **Kyun:** Bina taal ke cuts yaad nahi rehte; taal hi pacing ko ehsaas banati hai
- **Kitni baar:** Poore sequence me ek chuni hui taal consistent
- **Evidence:** 🟠 — Editor craft parampara (note)
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`

### R-274 — Pause-removal ki perceptual floor — 250 ms ⚙️ *(naya — editor round)*
- **Purana ID:** D1-013
- **Kab:** Khamoshi hatane (silence removal) ka threshold tay karna ho
- **Kya:** Threshold 250 ms se neeche kabhi mat rakho: boli hui connected speech me shabdon ke beech 30–200 ms ke articulation gaps hote hi hain — ye dead air nahi, awaaz ka hissa hai. Asli editorial pause (saans, hichkichahat, soch) lagbhag 250–300 ms se shuru hota hai; ladder 800 ms se 250 ms tak hi rakho
- **Kyun:** 250 ms se neeche ka threshold ek jumle ko ek-shabd wale tukdo me kaat dega — video saaf nahi, kata-kata lagega
- **Kitni baar:** Har silence-removal pass par floor 250 ms
- **Evidence:** 🟠 — Perceptual tark ke saath di gayi house rule (note)
- **Sources:** `notes_eacp1991_premiere-agent.md (note)`
- **Check:** `{"kind": "min_gap_s", "what": "pause_removal_threshold", "value": 0.25}`
- **Takraav note:** SEEDHA TAKRAAV purane pause model se: purana model (ORDER #6) silence ≥400 ms = cut zone kehta hai; eacp1991 250 ms ko floor aur 250–300 ms ko editorial pause ki shuruaat manta hai — cut threshold 400 vs 250 ka faisla Step 3 addendum me hona chahiye

### R-275 — Lead/trail margins — ASR drift ko soak karo ⚙️ *(naya — editor round)*
- **Purana ID:** D1-014
- **Kab:** Transcript/word timings se cut points banein
- **Kya:** Cut se pehle lead margin rakho jo ASR ki aam 50–100 ms drift ko soak kare aur sunne wale ko shabd se pehle saans ki jagah de; margins ki working window 30–200 ms rakho (Calm preset me 500 ms tak ja sakti hai)
- **Kyun:** Word timings hamesha thode idhar-udhar hote hain; bina margin ke cut shabd ke kinare par girta hai
- **Kitni baar:** Har transcript-based cut par
- **Evidence:** 🟠 — House rule (note)
- **Sources:** `notes_eacp1991_premiere-agent.md (note)`
- **Check:** `{"kind": "padding_range_ms", "what": "lead_trail_margin", "min": 30, "max": 200}`
- **Takraav note:** Purana padding model bhi 30–200 ms window kehta hai (sangat hai), lekin Calm preset ka 500 ms us window se bahar hai — preset-wise apvaad Step 3 addendum me tay ho. ZeusSheen ke sentence padding (0.25/0.35 s, D1-085) se bhi sambandh hai — wo isse bade hain

### R-276 — Pacing preset bina confirm kiye edit shuru mat karo *(naya — editor round)*
- **Purana ID:** D1-015
- **Kab:** Kisi naye video/session ki editing shuru ho
- **Kya:** Pehle pacing preset tay karo — Calm / Measured / Paced (default) / Energetic / Jumpy — aur har preset ko chaar numbers me kholo: kitni lambi khamoshi hatani hai, kitni chhoti baat rakhne layak hai, lead margin, trail margin
- **Kyun:** Bina preset ke har cut ka faisla alag mood me hota hai aur video ki lay beech me badal jati hai
- **Kitni baar:** Har session/video me ek baar, shuruaat me
- **Evidence:** 🟠 — Workflow rule (note)
- **Sources:** `notes_eacp1991_premiere-agent.md (note)`

### R-282 — 1 second ya lambi khamoshi hamesha kategi ⚙️ *(naya — editor round)*
- **Purana ID:** D1-021
- **Kab:** Pause removal/cleanup ka pass chale
- **Kya:** 1 second ya usse lambi bina-wajah ki khamoshi hamesha kaato
- **Kyun:** Ek second ki khamoshi video ko ruka hua mehsoos karati hai — retention wahi girta hai
- **Kitni baar:** Har cleanup pass me, bina apvaad
- **Evidence:** 🟠 — Skill ki sakht rule (note); neeche takraav dekho
- **Sources:** `notes_mmmnhat_agent-skills.md (note)`
- **Check:** `{"kind": "max_silence_s", "value": 1.0}`
- **Takraav note:** Yahi suite 10 ms tak ke chhote pauses kaatne ki kshamata bhi rakhti hai — wo sakhti eacp1991 ke 250 ms perceptual floor (D1-013) aur purane 400 ms threshold se seedha takraati hai; kshamata ko default mat bano — faisla Step 3 addendum me

### R-284 — Animation timing ki frame-ghadi (Disney ghadi) *(naya — editor round)*
- **Purana ID:** D1-023
- **Kab:** Kisi element ki animation ki lambai (frames me) tay karni ho
- **Kya:** Frames se ehsaas chuno: 2–4 frames = snappy/instant, 6–8 = quick/energetic, 12–15 = normal pace, 20–30 = slow/heavy, 40+ = dramatic/weighted
- **Kyun:** Frames hi animation ki bhasha hai — galat ghadi par halki cheez bhaari aur bhaari cheez khilona lagti hai
- **Kitni baar:** Har animation ki duration tay karte waqt
- **Evidence:** 🟠 — Disney craft parampara ke frame counts (MIT skill sheet); fps ke hisaab se ehsaas badalta hai
- **Sources:** `github_dylantarre_animation-principles.md`
- **Takraav note:** LobzyJay ki ms-ghadi (D1-059) isse sangat hai: <150 ms instant, 150–250 halka, 250–500 standard, 500 ms–1 s bhaari, >1 s cinematic — 30 fps par dono takreeban milte hain

### R-293 — Editing DNA naapo — andaz se style copy mat karo *(naya — editor round)*
- **Purana ID:** D1-032
- **Kab:** Kisi editor/brand ki style copy karni ho ya apni house style tay karni ho
- **Kya:** Purane approved edits ko naap kar DNA nikalo: ASL (average shot length), pehle 5 s ka Hook ASL, cuts per minute, silence threshold, min silence, cut padding, SFX/music ke dB offsets — style ko shabdon me nahi, numbers me pakdo
- **Kyun:** Style ka andaz har baar badalta hai; naape hue numbers hi style ko dohrane layak banate hain
- **Kitni baar:** Har nayi style/brand ke liye ek baar; phir wahi numbers har video par
- **Evidence:** 🟠 — Method rule (MIT skill); numbers house ke apne corpus se aate hain
- **Sources:** `github_vamshicreates_premiere-editing-dna.md`

### R-294 — House pacing ka udaharan — Hook ASL 1.6 s, Body ASL 2.8 s *(naya — editor round)*
- **Purana ID:** D1-033
- **Kab:** Tez house style ki pacing ka starting point chahiye
- **Kya:** Udaharan DNA ke numbers se shuru karo: Hook ASL 1.6 s (pehle 5 s; scene-detect threshold gt(scene, 0.26)) aur Body ASL 2.8 s; phir apne corpus se inhe badlo
- **Kyun:** Ek kaam karke dikhaya gaya house number bina-naap ke andaz se behtar shuruaat deta hai
- **Kitni baar:** Pacing ka reference point; har video par sakhti se nahi
- **Evidence:** 🟠 — Ek editor ke style-template ke udaharan numbers (MIT skill) — universal study nahi
- **Sources:** `github_vamshicreates_premiere-editing-dna.md`
- **Takraav note:** koptsev63 ki film/teaser pacing table (D1-075) isse bahut dheemi hai (hooks 4–6 s) — farak format ka hai (short-form house style vs film/teaser); Step 3 addendum me format-wise pacing saaf ho

### R-295 — Silence cutting ka house DNA — −35 dB, 0.28 s, padding 0.08 s ⚙️ *(naya — editor round)*
- **Purana ID:** D1-034
- **Kab:** Silence-based cutting/auto-cut chalana ho
- **Kya:** House settings: silence detect threshold −35 dB, kaatne layak kam se kam khamoshi 0.28 s, har cut ke aas-paas padding 0.08 s (80 ms)
- **Kyun:** Ye teen numbers milkar tay karte hain ki kataav kitna tez aur kitna saaf hoga
- **Kitni baar:** Har auto-cut pass par yehi DNA (jab tak naya naapa na jaye)
- **Evidence:** 🟠 — House DNA numbers (MIT skill)
- **Sources:** `github_vamshicreates_premiere-editing-dna.md`
- **Check:** `{"kind": "min_gap_s", "what": "min_silence_to_cut", "value": 0.28}`
- **Takraav note:** TAKRAAV: min silence 0.28 s purane pause model (≥400 ms cut zone, ORDER #6) aur eacp1991 ke 250 ms floor (D1-013) ke beech me hai — teen alag thresholds (250/280/400) ka ek faisla Step 3 addendum me. Padding 0.08 s (80 ms) purane 30–200 ms window ke andar hai — sangat

### R-299 — Element entrance ki ghadi — 0.4–1.2 s ⚙️ *(naya — editor round)*
- **Purana ID:** D1-038
- **Kab:** Koi text/object/graphic screen par aaye
- **Kya:** Har element ke entrance ko 0.4–1.2 s ke beech rakho — isse tez par hichki, isse dheere par susti; aur final state ko padhne layak der tak rukne do
- **Kyun:** Entrance ki ghadi hi element ka wajan batati hai; padhne ki rukawat ke bina aaya-gaya element register nahi hota
- **Kitni baar:** Har entrance par
- **Evidence:** 🟠 — AE workflow craft (MIT skill sheet)
- **Sources:** `github_justajazz_ae-mcp-bridge.md`
- **Check:** `{"kind": "duration_range_s", "what": "element_entrance", "min": 0.4, "max": 1.2}`
- **Takraav note:** ishu86 ke bands (D1-092: UI 0.3–0.5 s, text reveal 0.8–1.2 s) is range se aadhe overlap karte hain — element ke prakar se band chunna Step 3 addendum me saaf ho

### R-305 — Stagger — 2–5 frames ki lay, padhne ki disha me ⚙️ *(naya — editor round)*
- **Purana ID:** D1-044
- **Kab:** Kai related elements (letters, cards, list items, sections) ek ke baad ek aayein
- **Kya:** Elements ke beech 2–5 frames ka stagger rakho (text layers par 3–5 frames); stagger hamesha har element ki apni duration ka 10–20% rakho aur poori cascade ko ~24 frames ke andar band rakho. Samay me: letters ke liye tight 20–50 ms, lists/cards/words ke liye 50–100 ms, sections ke liye 100–200 ms. Kram padhne ki disha me rakho (upar se neeche, baayein se daayein); exits par stagger ulta chalao
- **Kyun:** Ek saath aate elements ek dhakka lagte hain; sahi stagger se aankh ek lay me poori list padh leti hai
- **Kitni baar:** Har multi-element reveal par
- **Evidence:** 🟠 — Chaar AE sources ke sangat numbers ka merged band (2–5 frames)
- **Sources:** `github_justajazz_ae-mcp-bridge.md`, `github_SebastianBoehler_autoresearch_after_effects_finetune.md`, `github_Maciejdziuba_youtube-skills.md`, `github_LobzyJay_motion-design-with-claude.md`
- **Check:** `{"kind": "frame_range", "what": "stagger", "min": 2, "max": 5}`
- **Takraav note:** Naap ki ikai sources me alag hai — koi frames deta hai, LobzyJay ms bands (20–200 ms) deta hai; 30 fps par dono takreeban milte hain, lekin fps badalne par frames wala band hi pakdo — Step 3 addendum me ikai tay ho

### R-307 — Attack tez, settle lamba — 2–4 frame attacks ⚙️ *(naya — editor round)*
- **Purana ID:** D1-046
- **Kab:** Koi transition/move apne sabse tez hisse par ho
- **Kya:** Attacks ko 2–4 frames me rakho aur settles ko usse hamesha lamba; ladkhadaata hua (sloppy) beech ka hissa kahin na ho
- **Kyun:** Tez attack urja deta hai, lamba settle wajan aur aitbaar — ulta karne par motion sust aur nakli lagta hai
- **Kitni baar:** Har bade move/transition par
- **Evidence:** 🟠 — Motion-direction craft (MIT skill)
- **Sources:** `github_SebastianBoehler_autoresearch_after_effects_finetune.md`
- **Check:** `{"kind": "frame_range", "what": "attack_frames", "min": 2, "max": 4}`

### R-310 — Motion piece me nirnayak transition har 1.5–3 s ⚙️ *(naya — editor round)*
- **Purana ID:** D1-049
- **Kab:** 10–15 s ka motion piece chal raha ho
- **Kya:** Har 1.5–3 s par ek nirnayak (decisive) transition rakho — isse lamba sukha antaral piece ko thanda kar deta hai
- **Kyun:** Motion piece ki urja transition ki lay se banti hai; lambi khamoshi wahan susti hai
- **Kitni baar:** Poore piece me, har 1.5–3 s
- **Evidence:** 🟠 — Motion-direction craft (MIT skill)
- **Sources:** `github_SebastianBoehler_autoresearch_after_effects_finetune.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 3}`
- **Takraav note:** Purana default max visual gap 5 s (ORDER #2, talking video ke liye) isse dheema hai — ye 1.5–3 s ki lay SIRF motion-graphics pieces ke liye hai; Step 3 addendum me context alag saaf ho

### R-315 — Exit hamesha entrance se tez — 0.6–0.8 guna ⚙️ *(naya — editor round)*
- **Purana ID:** D1-054
- **Kab:** Koi element screen se jaye (exit animation)
- **Kya:** Exit ki duration entrance ki 0.6–0.8 guna rakho aur exit par accelerate karke jao (ease-in) — dheere float karke kabhi mat ruko
- **Kyun:** Jaane wali cheez par darshak ka dhyaan pehle hi ja chuka hota hai; dheema exit susti aur anakalpan lagta hai
- **Kitni baar:** Har exit animation par
- **Evidence:** 🟠 — Do AE skills ke sangat craft numbers
- **Sources:** `github_Maciejdziuba_youtube-skills.md`, `github_LobzyJay_motion-design-with-claude.md`
- **Check:** `{"kind": "percent_range", "what": "exit_vs_entrance_duration_pct", "min": 60, "max": 80}`

### R-316 — Timing table 30 fps par — kaunsi harkat kitni lambi ⚙️ *(naya — editor round)*
- **Purana ID:** D1-055
- **Kab:** Motion element ki duration tay karni ho
- **Kya:** 30 fps par ye table rakho: opacity fade 5–8 frames (150–270 ms), chhota entrance 8–12 frames (250–400 ms), object/product entrance 12–18 frames (400–600 ms), exit 6–10 frames (200–330 ms), scene transition 15–24 frames (500–800 ms), hero camera move 24–45 frames (800–1500 ms)
- **Kyun:** Bina table ke har duration andaz banti hai aur poori piece ki lay bikhar jati hai
- **Kitni baar:** Har motion element ki duration par
- **Evidence:** 🟠 — Production house ki timing table (MIT skill repo, archived)
- **Sources:** `github_Maciejdziuba_youtube-skills.md`
- **Check:** `{"kind": "duration_range_s", "what": "scene_transition", "min": 0.5, "max": 0.8}`
- **Takraav note:** ishu86 transitions ko 0.5–1.5 s kehta hai (D1-093) — upari hadd par farak (0.8 vs 1.5 s); dhyaan do dono ke neeche ke band (0.5 s) milte hain. justajazz ke entrance band (D1-038) se bhi aadha overlap hai

### R-320 — Duration hi wajan hai — ms ki ghadi *(naya — editor round)*
- **Purana ID:** D1-059
- **Kab:** Kisi bhi animation ki lambai (ms me) tay karni ho
- **Kya:** Wajan ke hisaab se ghadi chuno: <150 ms = instant/mechanical, 150–250 ms = halka/UI, 250–500 ms = standard brand motion, 500 ms–1 s = bhaari/editorial, >1 s = cinematic (ya bas bahut dheema). Har cheez ko ek hi ~300 ms par mat chalao — sab kuchh ek jaisi ghadi par chalana cheezon ko wajan-rahit bana deta hai
- **Kyun:** Aankh lambai se hi wajan padhti hai — ek ghadi sab par matlab koi ghadi kisi par nahi
- **Kitni baar:** Har animation duration par
- **Evidence:** 🟠 — AE craft ghadi (MIT skill); frame-table (D1-023) se sangat
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`
- **Takraav note:** ishu86 ke bands (D1-092: UI 0.3–0.5 s) is ghadi ke 'standard brand' hisse me padte hain — UI ko yahan halka (150–250 ms) kaha gaya hai; chhota farak Step 3 addendum me tay ho

### R-324 — Sequential reveal metronome jaisa na ho *(naya — editor round)*
- **Purana ID:** D1-063
- **Kab:** Kai cheezein ek ke baad ek reveal hon (timings ki shrinkhala)
- **Kya:** Reveals ke beech ke antar barabar mat rakho (200/400/600/800 ms jaisa metronome galat hai) — lay ko tod-tor kar rakho (jaise 0/180/340/550 ms)
- **Kyun:** Barabar antar machine jaisa lagta hai; tooti hui lay hi insaani taal aur dilchaspi deti hai
- **Kitni baar:** Har sequential reveal par
- **Evidence:** 🟠 — AE craft (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`
- **Takraav note:** Stagger (D1-044) se takraav nahi — stagger ELEMENTS ke beech ka offset hai, ye bade reveals ke beech ke antar ki lay hai

### R-333 — Visuals ko audio transients par bithao *(naya — editor round)*
- **Purana ID:** D1-072
- **Kab:** Music/audio ke saath animation sync karni ho
- **Kya:** Har visual event ko audio ke asal transient (hit/beat) par bithao; kadam-ka-antarr (step interval) recording se naapo — (aakhri hit − pehli hit) / (steps − 1) — aur pehle transient ko pehla visual event banao; BPM ka andaz mat lagao
- **Kyun:** Sync ka ehsaas naape hue transients se hi aata hai; andaz wala sync hamesha thoda off lagta hai
- **Kitni baar:** Har audio-sync wali animation par
- **Evidence:** 🟠 — Preset craft (MIT skill pack)
- **Sources:** `github_Mfrostbutter_claude-skills.md`

### R-336 — Shot ki lambai beat ke prakar se — film/teaser ghadi ⚙️ *(naya — editor round)*
- **Purana ID:** D1-075
- **Kab:** Film/teaser/documentary ki pacing tay ho
- **Kya:** Beat ke hisaab se shot rakho: establishing/breath 5–8 s, hook/opening reveal 4–6 s, comedy beat 4–5 s, rhythmic action montage 2–4 s prati shot, interview/talking head 5–7 s (5 s se kam par baat kati hui lagti hai), title card 3–5 s (zor se padho + 1 s)
- **Kyun:** Har beat ki apni saans hoti hai — sab par ek ghadi chalana hi pacing ko marta hai
- **Kitni baar:** Har shot ka chunav isi ghadi se
- **Evidence:** 🟠 — Film-editing craft table (MIT skill); Murch parampara se sambandhit
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`
- **Check:** `{"kind": "duration_range_s", "what": "talking_head_shot", "min": 5, "max": 7}`
- **Takraav note:** Short-form house pacing (D1-033: Hook ASL 1.6 s) se bahut dheema — ye film/teaser ki ghadi hai; format ke hisaab se chunav Step 3 addendum me. Title card 3–5 s ishu86 (D1-093) se bilkul milta hai — sangat

### R-337 — Sabse bade pal ko sabse lambi ghadi do ⚙️ *(naya — editor round)*
- **Purana ID:** D1-076
- **Kab:** Emotional climax/payoff/end title ka shot tay ho
- **Kya:** Cinematic/emotional center ko 6–8 s, climax/payoff reveal ko 6–10 s (ye rhythm ke aam niyamo ko override karta hai), aur end title ko 6–10 s rakho
- **Kyun:** Sabse ahem pal ko sabse zyada waqt hi kahani ka hisaab hai — wahan jaldi karna matlab payoff ko sasta karna
- **Kitni baar:** Har climax/payoff/end title par
- **Evidence:** 🟠 — Film-editing craft table (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`
- **Check:** `{"kind": "duration_range_s", "what": "climax_shot", "min": 6, "max": 10}`
- **Takraav note:** Tez-pacing wale purane rules (jaise max gap/ASL wale) se disha ka takraav hai — source khud kehta hai ye beats rhythm rules ko override karte hain; ORDER ki kahani-sabse-upar wali seedhi bhi yahi kehti hai

### R-338 — Lambai ka ratio — sabse lamba shot sabse chhote ka 2–4 guna ⚙️ *(naya — editor round)*
- **Purana ID:** D1-077
- **Kab:** Kisi teaser/sequence ki shot lambaiyan tay hon
- **Kya:** Sabse lambe shot ko sabse chhote ke 2–4 guna ke andar rakho; chaar lagatar shots ek hi lambai ke kabhi mat rakho; aur teen sabse ahem emotional beats ko hi teen sabse lambe shots banao
- **Kyun:** Ek-jaisi lambai lay ko sust karti hai; lambai ka utaar-chadhaav hi ehsaas ki seedhi hai
- **Kitni baar:** Poore sequence par laagoo
- **Evidence:** 🟠 — Film-editing craft (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`
- **Check:** `{"kind": "ratio_range", "what": "longest_to_shortest_shot", "min": 2, "max": 4}`

### R-339 — Blink cut point — soch ke aakhir par kaato *(naya — editor round)*
- **Purana ID:** D1-078
- **Kab:** Dialogue/performance me cut point chunna ho
- **Kya:** Cut ko soch ke aakhir par rakho; actor ki palak jhapakne (blink) wala frame cut-point ka swabhavik ummeedvaar hai — palak band hote hi cut chhupta hai
- **Kyun:** Insaan soch badalte waqt palak jhapakta hai — wahi pal darshak ke liye bhi cut ki swabhavik jagah hai
- **Kitni baar:** Har performance cut par pehla ummeedvaar yahi
- **Evidence:** 🟠 — Murch ki blink theory ka operational roop (MIT skill); vigyaan harvest me ye siddhant pehle se hai — ye uska Premiere istemal hai, nakal nahi
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`
- **Takraav note:** Purane Murch/science rules se takraav nahi — unhi ka vyavharik roop hai

### R-346 — Jumla-cut ki padding — 0.25 s pehle, 0.35 s baad ⚙️ *(naya — editor round)*
- **Purana ID:** D1-085
- **Kab:** Rough cut me jumlo (sentences) ke hisse kaate jayein
- **Kya:** Har hisse ko pehle shabd se lagbhag 0.25 s pehle shuru karo aur aakhri shabd ke lagbhag 0.35 s baad khatm karo — hamesha asal source pause ke ANDAR rehkar; pause ke beech me kabhi mat kaato; agar chhota pause do hisso me bantna pade to 60% outgoing tail ko do. ASR timestamps ko ±0.2 s ki galti ke saath lo
- **Kyun:** Ye saans ki jagah hi bol ko insaani rakhti hai; kas kar kaata jumla ghuta hua lagta hai
- **Kitni baar:** Har sentence-level cut par
- **Evidence:** 🟠 — Rough-cut tool ke kaam kiye hue numbers (MIT skill)
- **Sources:** `github_ZeusSheen_ppro-agent-bridge.md`
- **Check:** `{"kind": "padding_range_ms", "what": "sentence_cut_padding", "min": 250, "max": 350}`
- **Takraav note:** TAKRAAV purane padding model se: purana edge padding 30–200 ms hai (frame-edge suraksha ke liye); ye 250/350 ms jumla-star ki saans hai — dono ki jagah alag hai lekin numbers takraate dikhte hain; Step 3 addendum me dono ki paribhasha alag saaf ho. eacp1991 ke margins (D1-014, 30–200 ms) se bhi yahi sambandh hai

### R-349 — 0.5 s se chhota tukda = SLIVER — mat rakho ⚙️ *(naya — editor round)*
- **Purana ID:** D1-088
- **Kab:** Cut ke baad koi bahut chhota tukda bane
- **Kya:** 0.5 s se chhote tukde ko hamesha hatao ya padosi me milao — sirf tab rakho jab wo music/SFX ke neeche jaan-boojh ka rakha fragment ho
- **Kyun:** Aadhe second ka tukda darshak ko sirf jhatka deta hai, koi matlab nahi
- **Kitni baar:** Har cut ke baad check
- **Evidence:** 🟠 — Defect-lint ka threshold (MIT skill)
- **Sources:** `github_ZeusSheen_ppro-agent-bridge.md`
- **Check:** `{"kind": "min_gap_s", "what": "min_piece_duration", "value": 0.5}`
- **Takraav note:** Shorts/teaser ke jaan-boojh ke tez tukdo (jaise mmmnhat ke <1.5 s teaser shots) se takraav sambhav hai — apvaad sirf jaan-boojh ke fragments ke liye hai, Step 3 addendum me saaf ho

### R-353 — Chhote elements ki ghadi — UI 0.3–0.5 s, text reveal 0.8–1.2 s ⚙️ *(naya — editor round)*
- **Purana ID:** D1-092
- **Kab:** Chhote motion elements (UI, text, logo/CTA) ki duration tay ho
- **Kya:** Bands rakho: UI elements 0.3–0.5 s, text reveals 0.8–1.2 s (kuch guidelines 0.5–1.5 s tak jati hain), logo/CTA reveal overshoot ke saath 0.4–0.6 s
- **Kyun:** Har prakar ke element ki apni padhne ki ghadi hai — UI ko text jitna aur text ko UI jitna samay dena dono galat hai
- **Kitni baar:** Har chhote element ki duration par
- **Evidence:** 🟠 — Motion guide ke timing bands (MIT skill)
- **Sources:** `github_ishu86_after-effects-mcp.md`
- **Check:** `{"kind": "duration_range_s", "what": "text_reveal", "min": 0.8, "max": 1.2}`
- **Takraav note:** justajazz ka aam entrance band 0.4–1.2 s (D1-038) inse overlap karta hai; LobzyJay ki ms-ghadi (D1-059) UI ko 150–250 ms kehti hai — 0.3–0.5 s usse dheema hai; element-prakar wise faisla Step 3 addendum me

### R-354 — Bade pieces ki ghadi — logo 1–3 s, title card 3–5 s, loop 2–4 s ⚙️ *(naya — editor round)*
- **Purana ID:** D1-093
- **Kab:** Poora logo animation, title card, transition ya ambient loop bane
- **Kya:** Bands rakho: poora logo animation 1–3 s, title cards 3–5 s, transitions 0.5–1.5 s, ambient loops 2–4 s
- **Kyun:** Bade pieces ko chhoto ki ghadi dene se wo ghate hue lagte hain, aur ulta karne se sust
- **Kitni baar:** Har bade piece ki duration par
- **Evidence:** 🟠 — Motion guide ke timing bands (MIT skill)
- **Sources:** `github_ishu86_after-effects-mcp.md`
- **Check:** `{"kind": "duration_range_s", "what": "title_card", "min": 3, "max": 5}`
- **Takraav note:** Title card 3–5 s koptsev63 (D1-075) se bilkul milta hai — sangat. Transitions 0.5–1.5 s ki upari hadd Maciejdziuba ke 0.5–0.8 s (D1-055) se takraati hai — neeche ka band (0.5) dono me ek hai

### R-394 — Travel shot-lengths: reference se calibrate *(naya — editor round)*
- **Purana ID:** D2-037
- **Kab:** Long-form travel pacing set karte waqt
- **Kya:** Ek poori tarah review ki hui homeward travel film ke measured numbers ko calibration anchor rakho: average shot ~10.4s, median ~10.1s, p10 ~3.1s, p90 ~17.9s. Apni film ke avg/median shot lengths in reference-calibrated ranges ke andar rakho
- **Kyun:** Long-form travel ki saans short-video se bilkul alag hai; bina anchor ke pacing ya to sust ya to bechain ho jati hai
- **Kitni baar:** Anchor: avg ≈10.4s, median ≈10.1s, p90 ≈17.9s (ek film ka map)
- **Evidence:** 🟡 — Ek asli film ke 36 shots/35 boundaries ka poora human-reviewed map — measured, par sirf 1 film
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-395 — Pacing ki marammat footage se, effects se nahi *(naya — editor round)*
- **Purana ID:** D2-038
- **Kab:** Rhythm recut / pacing repair me
- **Kya:** Do galtiyan block karo: recut ke baad bache lambe non-scenic raw holds, aur micro-clips ki accidental flicker runs. Dono ki marammat footage badal/chun kar karo — effect daal kar kabhi nahi
- **Kyun:** Effect pacing ki bimari ko dhakta hai, theek nahi karta; viewer ko dhokha mehsoos hota hai
- **Kitni baar:** Long raw holds = 0; flicker runs = 0
- **Evidence:** 🟠 — House pacing-watchability contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-396 — Har bade chapter me kam se kam ek saans-wala shot ⚙️ *(naya — editor round)*
- **Purana ID:** D2-039
- **Kab:** Chapter rhythm review par
- **Kya:** Har substantial chapter me kam se kam ek breathing/payoff/aftertaste shot rakho
- **Kyun:** Bina saans ke chapter ghutan hai; ek thehra shot poore chapter ko wazan deta hai
- **Kitni baar:** ≥1 breathing shot per substantial chapter
- **Evidence:** 🟠 — House pacing contract
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "count_range", "min": 1, "what": "breathing/payoff shot per chapter"}`

### R-397 — Visual rhythm ka pattern: establish → detail → reaction → widen *(naya — editor round)*
- **Purana ID:** D2-040
- **Kab:** Long-form ke andar shot sequence banate waqt
- **Kya:** Pattern dohrao: jagah ko establish karo (aerial/skyline/map/title) → street-level detail me ghuso → human reaction/food/transit/weather/waiting dikhao → jaane se pehle phir widen karo → geography, awaaz ya motion se transition karo
- **Kyun:** Ye upar-neeche ki lehar hi documentary-vlog rhythm hai; sirf beauty shots se film so jati hai
- **Kitni baar:** Har place-block = kam se kam ek poora pattern cycle
- **Evidence:** 🟠 — House visual-rhythm style
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-398 — Visual change gap 3s se zyada (short-form) = pattern interrupt ⚙️ *(naya — editor round)*
- **Purana ID:** D2-041
- **Kab:** Short-form/social edit me jahan 3 second se zyada koi visual change nahi
- **Kya:** Pattern interrupt lagao — bareek se mote kram me: zoom (105–110%) → cut → caption overlay → motion (pan/shake) → effect overlay. Sabse halka kaam kare wahi chuno
- **Kyun:** 3 second bina badlav ke short-form me dhyaan marr jata hai
- **Kitni baar:** Max visual gap 3s (short-form profile)
- **Evidence:** 🟠 — CapCut director ke attention niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 3, "scope": "short-form"}`
- **Takraav note:** TAKRAAV: purane ORDER default me long-form max visual gap 5s hai (Shorts 3s). Ye 3s wala niyam short-form/social ke liye hai — long-form par 5s wala hi rahe; profile se lagu karo, dono ko ek mat samjho.

### R-399 — Platform ke hisaab se pacing table *(naya — editor round)*
- **Purana ID:** D2-042
- **Kab:** Platform tay hote hi edit shuru karne se pehle
- **Kya:** Pacing platform se lo: TikTok/Reels/Shorts — change har 1–3s, hook 1s me; YouTube short-form — change 2–3s, hook 3s; YouTube long-form — change 3–5s; LinkedIn — change 4–6s, saaf aur minimal
- **Kyun:** Ek hi pacing har platform par ya to sust hai ya bechain
- **Kitni baar:** Table upar wali; hook: TikTok 1s / YT-SF 3s
- **Evidence:** 🟠 — CapCut director ke platform-optimization niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-400 — Hook me dead air = retention ki maut ⚙️ *(naya — editor round)*
- **Purana ID:** D2-043
- **Kab:** Video ki shuruaat (khaas taur par hook section ~pehle 4s) me
- **Kya:** Shuru ki silence/dead air kaato — hook action ya baat se shuru ho, khaamoshi se nahi
- **Kyun:** Pehle 2 second ki dead air sabse zyada viewers girati hai
- **Kitni baar:** Initial dead air = 0; hook window ~4s
- **Evidence:** 🟠 — CapCut director ke hook niyam; purane Shorts hook ≤2.5s niyam se milta-julta
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "hook_within_s", "max_s": 2, "what": "shuru ki dead air"}`

### R-401 — Pause ke niyam (talking head): 0.5s / 1.0s / dramatic chhoot *(naya — editor round)*
- **Purana ID:** D2-044
- **Kab:** Talking-head edit me pauses dekhte waqt
- **Kya:** Pause >0.5s ho to jump cut ka sujhav do; pause >1.0s ho to weak spot flag karo. Lekin 0.3–0.5s ke brief pauses dramatic maksad ke liye reh sakte hain
- **Kyun:** Har pause kaat dene se boli robot jaisi ho jati hai; lambe pause rakhe to viewer bore hota hai
- **Kitni baar:** >0.5s = cut sujhav; >1.0s = flag; 0.3–0.5s dramatic = rakho
- **Evidence:** 🟠 — CapCut director ke silence-detection niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Takraav note:** TAKRAAV: purana unified pause model ≥400ms ko cut zone, 150–400ms ko usable aur <150ms ko unsafe kehta hai. Ye source 500ms threshold rakhta hai aur 300–500ms dramatic pause ko surakshit maanta hai. Merge par faisla: threshold 400ms vs 500ms — profile (talking-head social = 0.5s wala; Kang pipeline = purana model) se tay karna bacha hai.

### R-402 — Smart-cut: >1s silence aur duplicate takes pehle pass me bahar *(naya — editor round)*
- **Purana ID:** D2-045
- **Kab:** Auto/smart-cut pehla pass chalate waqt
- **Kya:** Subtitle gaps >1s wali silences aur duplicate takes auto-remove karo. Chalane se PEHLE project ka duplicate/backup zaroor banao (auto-backup nahi hota)
- **Kyun:** Pehla pass haath se karna sabse dheema kaam hai; machine ko wahi do jo bina taste ke ho sakta hai
- **Kitni baar:** Threshold: silence gap >1s; duplicates = sab bahar
- **Evidence:** 🟠 — CapCut smart-cut + note source ke retake-removal workflow ka sangam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`, `notes_AdamGarceau_resolve-toolkit.md (note)`
- **Takraav note:** TAKRAAV: purana pause model ≥400ms ko hi cut zone kehta hai — >1s wala threshold usse zyada conservative hai. Ye sirf AUTO pehle pass ke liye hai (haath ka fine pass purane model par hi rahe), isliye takraav pass-wise sulajh sakta hai.

### R-403 — Cut sirf silence ya word-boundary par; mid-sentence kabhi nahi *(naya — editor round)*
- **Purana ID:** D2-046
- **Kab:** Tighten/cut pass me har cut lagate waqt
- **Kya:** Cut hamesha silence ke andar ya word boundary par rakho — sentence ke beech me kabhi nahi. Shorts aur longform ke liye alag tighten profiles rakho
- **Kyun:** Beech-vaakya cut boli ko kaatta hai aur viewer ko jhatka lagta hai
- **Kitni baar:** Mid-sentence cuts = 0
- **Evidence:** 🟠 — Note source (dr-tighten) + production standard ke coherent-block niyam
- **Sources:** `notes_AdamGarceau_resolve-toolkit.md (note)`, `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-404 — Do-phase discipline: CUT pass → re-cut → TRANSCRIPT pass *(naya — editor round)*
- **Purana ID:** D2-047
- **Kab:** Poore edit ka kram tay karte waqt
- **Kya:** Pehle CUT pass (picture lock ki taraf), phir editor ka re-cut, uske BAAD transcript pass. Purani subtitles ke upar transcript pass chalana bekaar hai — transcript hamesha final cut ke baad bane
- **Kyun:** Galat kram = do baar kaam; transcript pehle banaya to har cut use tod dega
- **Kitni baar:** Kram fixed: cut → re-cut → transcript
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_SamuelAde001_second-brain.md (note)`

### R-405 — Phase-1 ki shikar-list *(naya — editor round)*
- **Purana ID:** D2-048
- **Kab:** Pehle (hunt) pass me footage dekhte waqt
- **Kya:** Sirf ye cheezen dhoondo aur mark karo: duplicate takes, misspeaks, garbled audio, flash frames, redundancy, aur script ke missing sections
- **Kyun:** Pehla pass sab kuch ek saath theek karne nikle to kuch theek nahi hota
- **Kitni baar:** 6 item ki list; is se bahar ka kaam phase-2 ka
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_SamuelAde001_second-brain.md (note)`

### R-406 — Screen-recording cut workflow: transcript pehle, rough 2x, 1.5x par galti-pass *(naya — editor round)*
- **Purana ID:** D2-049
- **Kab:** Screen-recording/talking video ka rough cut banate waqt
- **Kya:** Transcript-first kaato: AI transcription + silent-portion removal ~80% kaam kar deta hai. Rough cut ka target final length ka ~2x rakho (8 min final → ~16 min rough). Refine pass me snapping OFF, audio scrubbing ON, 5-frame nudges. Aakhiri mistake pass 1.5x playback par ripple-delete ke saath chalao (aur 1–3 minute nikalta hai). Verify: koi audible cut edit na sune, saare ums/pauses gaye hon
- **Kyun:** Dekh-dekh kar kaatna sabse dheema hai; transcript se kaatna tez aur pakka hai
- **Kitni baar:** Rough ≈ 2x final; mistake pass 1.5x playback
- **Evidence:** 🟠 — Resolve screen-recording workflow se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-407 — Silence detection ki shart: room noise pehle theek karo *(naya — editor round)*
- **Purana ID:** D2-050
- **Kab:** Auto silence removal chalane se pehle
- **Kya:** Room noise −30 dB se upar ho to silence detection toot jata hai — pehle noise reduction karo ya haath se kaato
- **Kyun:** Shor ko tool khaamoshi samajh nahi pata; galat detection = galat cuts
- **Kitni baar:** Room noise >−30 dB = pehle NR/manual
- **Evidence:** 🟠 — Workflow ki vyavharik shart
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-408 — Screencast speed map: sust hissa delete nahi, tez karo *(naya — editor round)*
- **Purana ID:** D2-051
- **Kab:** Screencast ke boring hisse handle karte waqt
- **Kya:** Boring hisse ko delete karne ki jagah speed up karo taaki poora workflow dikhta rahe. Normal speed = prompts, output review, test results, key decisions. 4x–8x = generation, lambe reads, scrolling. Poora cut = false starts, re-prompts, apni typos. Speed% = (original duration / target audio duration) x 100
- **Kyun:** Delete karne se viewer ko 'beech me kya hua' ka shaq rehta hai; tez karne se poora safar dikhta hai
- **Kitni baar:** 4x–8x sust hisso par; key moments hamesha 1x
- **Evidence:** 🟠 — Screencast editor ki house style
- **Sources:** `github_matthull_my-skills.md`

### R-409 — Talking speed 1.1x (samajh bani rahe to) *(naya — editor round)*
- **Purana ID:** D2-052
- **Kab:** Speaker-led short-form me
- **Kya:** Speaker ki speed 1.1x rakho — sirf tab jab intelligibility poori bani rahe
- **Kyun:** Halki tez boli energy deti hai bina nakli lage
- **Kitni baar:** 1.1x; samajh ghate to wapas 1.0x
- **Evidence:** 🟠 — Production standard se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-410 — A-roll reset: 6–9s se zyada bina reset ke nahi (talking-head social) *(naya — editor round)*
- **Purana ID:** D2-053
- **Kab:** Talking-head social edit (Deya-style retention) me
- **Kya:** 6–9 second se zyada uninterrupted A-roll mat chalne do — beech me visual reset do (B-roll, punch-in, angle ya title)
- **Kyun:** Ek hi frame par thahri boli dhyaan ko sust kar deti hai
- **Kitni baar:** A-roll bina reset ≤6–9s
- **Evidence:** 🟠 — Ek retention creator (Deya) ki style ko production standard ne apnaya
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Takraav note:** TAKRAAV (halka): purana max visual gap default 5s hai. Ye 6–9s wala window sirf 'A-roll reset' ki had hai (speaker frame par lagatar rehne ki), aam visual-change gap se alag mapna — dono ek saath chal sakte hain: visual change 5s ke andar, A-roll reset 9s ke andar.

### R-411 — BPM ke hisaab se cut frequency *(naya — editor round)*
- **Purana ID:** D2-054
- **Kab:** Music-led edit me cut rhythm tay karte waqt
- **Kya:** Cut frequency BPM se lo: 60 BPM → har 4 beats (~4s, ~8 cuts/30s, cinematic); 100 BPM → har 2 beats (~17 cuts/30s); 120 BPM → har 1–2 beats (20–30 cuts/30s); 140 BPM → har beat (~35 cuts/30s). Ambient/bina-BPM music par beat-cut bilkul nahi — cuts visual narrative se motivate hon, 5–15s ke holds aam hain
- **Kyun:** Music ki gati aur cut ki gati alag chale to video do hisso me tootta lagta hai
- **Kitni baar:** Upar wali table; formula: beat frames = 1800/BPM @30fps
- **Evidence:** 🟠 — CapCut KF-07 ka BPM-to-cut map (house table, measured nahi)
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-412 — Cuts beat par; 2–3 frame aage-peeche ka khel *(naya — editor round)*
- **Purana ID:** D2-055
- **Kab:** Beat-synced cuts lagate waqt
- **Kya:** Default: cut theek beat par (kick/snare). Aage ki kheench (anticipation) chahiye to cut beat se 2–3 frames PEHLE; wazan chahiye to 2–3 frames BAAD. Off-beat cuts sirf syncopated/groovy feel ke liye jaan-bujh kar
- **Kyun:** Beat par cut 'lock' mehsoos hota hai; jaan-bujh kar off-beat usi lock ko tod kar jaan deta hai — galti se off-beat sirf galti lagta hai
- **Kitni baar:** Offset sirf ±2–3 frames, jaan-bujh kar
- **Evidence:** 🟠 — KF-07 beat-sync guide
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-413 — Bade phase-change cuts BGM phrase par; har beat par nahi *(naya — editor round)*
- **Purana ID:** D2-056
- **Kab:** Route/phase badlav ke cuts par (travel film)
- **Kya:** Ahem route-phase badlav phrase boundary ya saaf BGM hit par kaato. Har beat par cut mat karo — beat grid sirf bade palon ke liye hai
- **Kyun:** Har beat kaatne se film gana ban jati hai, safar nahi
- **Kitni baar:** Phrase-level cuts sirf bade badlav par
- **Evidence:** 🟠 — Homeward profile + BGM phrase system
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-414 — Build-up → drop: edit ka accelerator *(naya — editor round)*
- **Purana ID:** D2-057
- **Kab:** Music me build-up/riser aur drop wale hisse me
- **Kya:** Pre-drop/riser par cut frequency tez karo, visual density har 2 beats badhao, speed ramps se time sikodo. Drop par sabse sakht cuts, hero shot/reveal rakho. Breakdown par dheere ho jao — lambe holds, viewer ko saans
- **Kyun:** Sangeet jo chadhaw-utaw deta hai, edit use follow na kare to drop fizool jata hai
- **Kitni baar:** Har drop = 1 hero pal; breakdown = jaan-bujh kar dheema
- **Evidence:** 🟠 — KF-07 ki song-structure map
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-415 — Music entry chorus/drop se; climax drop par sync *(naya — editor round)*
- **Purana ID:** D2-058
- **Kab:** Video ke liye music ka hissa chunte waqt
- **Kya:** Cold open/hook par music chorus ya drop se shuru karo — track ke intro se kabhi nahi. Value-delivery hisse me instrumental/low-vocal section rakho taaki narration saans le. Climax/reveal ko drop ya chorus peak se sync karo
- **Kyun:** Track ka intro sabse sust hissa hota hai; hook wahan rakha = video shuru hote hi marr gaya
- **Kitni baar:** Frame 1 = chorus/drop; climax = drop peak par
- **Evidence:** 🟠 — KF-07 music entry points
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-416 — BGM variety: 35% unique, 6 cues me repeat nahi ⚙️ *(naya — editor round)*
- **Purana ID:** D2-059
- **Kab:** Lambe film ke BGM cues (≥20) plan karte waqt
- **Kya:** Unique songs kam se kam max(12, cue_count x 0.35) rakho; koi gaana pichhle 6 cues ke andar repeat nahi. Lambe hero passages ko calm → lift → climax wala arc do
- **Kyun:** Wahi dhun baar-baar sunai de to film chhoti aur sasti lagti hai
- **Kitni baar:** Unique ≥ max(12, 35%); repeat window = 6 cues
- **Evidence:** 🟠 — Travel-studio ka BGM catalog niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "percent_range", "min_pct": 35, "what": "unique BGM songs (≥20 cues par)"}`

### R-417 — Muted-audio desert 18s se zyada nahi; scenic BGM coverage poora *(naya — editor round)*
- **Purana ID:** D2-060
- **Kab:** Scenic/BGM-led windows ki audio planning me
- **Kya:** Bina awaaz ke hisse (muted desert) ~18s se zyada na rakho. Drone/pure-scenic windows me BGM coverage ratio ~0.995 rakho
- **Kyun:** Lambi khaamoshi scenic hisse ko 'rendering adhoori' jaisa bana deti hai
- **Kitni baar:** Muted desert ≤~18s; scenic coverage ≈99.5%
- **Evidence:** 🟠 — House scenic audio policy
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-418 — Speed-ramp ko beat se baandho *(naya — editor round)*
- **Purana ID:** D2-061
- **Kab:** Speed ramps lagate waqt
- **Kya:** Riser ke dauran 30–50% slow-mo rakho aur drop wale frame par 100% par snap karo. Whip-pan ke liye 400% speed sirf 6 frames, beat ke theek center me
- **Kyun:** Ramp bina beat ke geli-geli lagti hai; beat par wahi ramp prahar (hit) ban jata hai
- **Kitni baar:** Slow-mo 30–50% riser par; whip 400% x 6 frames
- **Evidence:** 🟠 — KF-07 ramp-sync table
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-419 — Vlog silence cuts me chhote pads (saans) rakho *(naya — editor round)*
- **Purana ID:** D2-062
- **Kab:** Vlog ke silence cuts par
- **Kya:** Silences kaato lekin cut edges par chhote pads chhodo taaki boli saans leti lage; scene edges par bhi thodi room rakho. Jump cut ko naram karne ke liye halka zoom punch-in kaam aata hai
- **Kyun:** Zero-pad cuts vlog ko machine-gun bana dete hain; saans hi asli-boli ka saboot hai
- **Kitni baar:** Har silence cut = chhota pad; scene edge = halki room
- **Evidence:** 🟠 — Note source; purane remainder 0.2–0.45s model se bhavna milta hai, numbers yahan qualitative
- **Sources:** `notes_appariciojunior_video-editor-skills.md (note)`
- **Takraav note:** Purane unified pause model ka remainder 0.2–0.45s is niyam se takrata nahi — ye usi 'saans' ko vlog context me kehta hai, par exact ms nahi deta.

### R-420 — CapCut edit ka kram: ratio → structure → timing → transitions → text *(naya — editor round)*
- **Purana ID:** D2-063
- **Kab:** CapCut mobile edit shuru karte waqt
- **Kya:** Pehle aspect ratio confirm karo. Structural edit (trim/split/delete) speed/timing se pehle. Transitions tab jab boundaries stable ho jayein. Text/stickers timing fix hone ke baad
- **Kyun:** Galat kram me har baad wala step pehle wale ko tod deta hai
- **Kitni baar:** 5 steps, yahi kram
- **Evidence:** 🟠 — CapCut mobile workflow (openpocket) se
- **Sources:** `github_pockebot_openpocket.md`

### R-421 — AutoCut tabhi kabul jab intent se mile *(naya — editor round)*
- **Purana ID:** D2-064
- **Kab:** Auto-generated cut ka result dekhte waqt
- **Kya:** AutoCut ka output sirf tab accept karo jab pacing/cuts tumhare intent se milte hon. Na mile to baar-baar regenerate karne ki jagah manual edit par switch karo
- **Kyun:** Baar-baar regeneration samay khaata hai aur result waisa ka waisa rehta hai
- **Kitni baar:** Intent-match nahi = manual, dobara generate nahi
- **Evidence:** 🟠 — CapCut mobile workflow
- **Sources:** `github_pockebot_openpocket.md`

---

## STYLE / EFFECT — sajawat sabse neeche, kahani ke neeche hamesha

### R-200 — Punch-in sirf motivated, hadd ke andar ⚙️
- **Purana ID:** A-072
- **Kab:** Talking video me zoom/punch-in lagane se pehle
- **Kya:** Zoom sirf us detail, reaction ya usi line par rakho jis par voice baat kar rahi hai; talking-head punch-in ka scale 110-120% rakho (source resolution ke andar hi, soft frame crop nahi); Melvynx ke naape hue limits: punch-in har ~4 s se zyada baar nahi, ≤1.15x, agle cut tak hold, ek hi shot me in aur out dono nahi; zoom cut ko kabhi cross na kare; screencast me do zooms ke beech 5-7 s ka gap
- **Kyun:** Bina wajah ka zoom sabse pehchani jaane wali amatuer harkat hai; wajah wala zoom dhyaan ko sahi jagah le jata hai
- **Kitni baar:** Har punch-in par
- **Evidence:** 🟠 — Creator practice (kmilo; Envision ke screencast numbers) + Melvynx measured style-copy ke exact numbers
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Check:** `{"kind": "min_gap_s", "what": "punch_in", "value": 4}`
- **Takraav note:** ExpoCut cadence ke saath har 2nd ya 3rd cut par punch-in ki salah deta hai (Free to use and redistribute with attribution to expocut.com) — ye kmilo/Melvynx ke 'sirf motivated' niyam se takrata hai; entertainment short me cadence wali chal sakti hai, samjhane wale content me motivated wali hi surakshit hai (dekho CONFLICTS.md)

### R-201 — Snap punch-in ki technique
- **Purana ID:** A-073
- **Kab:** Punch-in lagate waqt (ExpoCut tareeka)
- **Kya:** Zoom ko ramp mat karo — do hold keyframes lagao (jaise scale 1.0 se 1.1), cut par alternate karo; agar settle chahiye to easeOut key rakho aur 400 ms baad scale 1.0 wapas karo
- **Kyun:** Ramp wala zoom dheere-dheere ghista hua lagta hai; snap cut jaisa saaf lagta hai
- **Kitni baar:** ExpoCut style wale har punch-in par
- **Evidence:** 🟠 — ExpoCut playbook ki technique (Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_expocut_claude-plugin_retention-playbook.md`

### R-202 — Entrances aur exits ki timing
- **Purana ID:** A-074
- **Kab:** Koi element screen par aaye ya jaye to
- **Kya:** Cards/headlines 0.35-0.6 s ease-out me enter karein (bounce nahi), rows 0.3 s; exit hamesha entrance se chhota (0.25 s); elements 20-40 px offset aur opacity ke saath slide-in karein; Melvynx ka niyam: exit entrance se chhota rakho (.26 s smoothstep), theek 0 par khatm karo — spring wala exit ghost chhodta hai; springs kabhi overshoot na karein
- **Kyun:** Yahi chhoti timings 'professional' aur 'PPT jaisa' ke beech ka farak hain
- **Kitni baar:** Har animated element par
- **Evidence:** 🟠 — kmilo motion reference (Material Design ke UI numbers 225/195 ms sirf reference ke roop me) + Melvynx reads ke measured exits
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-203 — Bounce, elastic aur emoji nahi
- **Purana ID:** A-075
- **Kab:** Animation style ya visual language chunte waqt
- **Kya:** Serious content par bounce/elastic easing kabhi nahi (sirf halka overshoot promotional CTA par chal sakta hai); ye bilkul mat use karo: pulse, bounce, elastic, overshoot, glow, shake, spin, confetti; beat ko emoji se illustrate mat karo — motion design, asal logo ya typography use karo
- **Kyun:** Ye effects video ko sasta aur baccho jaisa dikhate hain; ek forbidden cheez poora premium feel tod deti hai
- **Kitni baar:** Har project par (style system me band)
- **Evidence:** 🟠 — kmilo forbidden list + Melvynx motion rules — dono house style
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-204 — Ek moment, ek hi accent color
- **Purana ID:** A-076
- **Kab:** Board ya graphic design karte waqt
- **Kya:** Kisi ek pal me screen par sirf ek accent color rakho; dusra accent kabhi na aaye
- **Kyun:** Do accents ek saath ladte hain aur design ka focus khatm ho jata hai
- **Kitni baar:** Har frame par
- **Evidence:** 🟠 — Melvynx design system ka rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-205 — Har beat action, khadi tasveer nahi
- **Purana ID:** A-077
- **Kab:** Koi beat banate waqt
- **Kya:** Har beat kuch karta hua ho — screenshot, still illustration, akela logo ya text card screen par 'baitha' rahe to woh beat redo hai; screenshot sirf reference hai — UI ko recreate karke animate karo
- **Kyun:** Ruki hui screen hi short ko marta hai; action hi premium motion ka ehsaas deta hai
- **Kitni baar:** Har beat par
- **Evidence:** 🟠 — Melvynx short-editing style.md ka rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-206 — Hero then place; ek idea ek tableau
- **Purana ID:** A-078
- **Kab:** Naya object screen par laate waqt
- **Kya:** Naya object pehle bada aur center me dikhao (scale 1.3-1.7), phir apni jagah (slot) me glide karo, aur agla item aane se pehle use land kar do; ek idea ke saare sentences ek hi tableau par badhte rahein — board har 1.5-2.5 s tabhi badlo jab speech ka idea badle; board ≥3 s hold ho to .025 ka slow push-in rakho
- **Kyun:** Bade pehle dikhne se aankh samajhti hai kya aa raha hai; tableau badalte rehne se viewer har baar nayi jagah seekhta hai
- **Kitni baar:** Har naye object/idea par
- **Evidence:** 🟠 — Melvynx style.md hero-then-place aur tableau rules
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-207 — Asli logos hi, nakli kabhi nahi
- **Purana ID:** A-079
- **Kab:** Screen par kisi tool/product ka naam aaye to
- **Kya:** Us tool ka asal logo/icon rakho (press kit, App Store listing ya official site se); letter glyph, emoji ya look-alike kabhi nahi; logo na mile to creator se file mango, khud mat banao
- **Kyun:** Nakli logo ek jhalak me pakda jata hai aur poori video ki credibility gira deta hai
- **Kitni baar:** Har naam ke saath
- **Evidence:** 🟠 — Melvynx style.md logo rule
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-208 — Layout teen tarah ka ghumao
- **Purana ID:** A-080
- **Kab:** Short ka layout banate waqt
- **Kya:** Teen views ghumao: split (paper/board upar, camera neeche — aam), paper-only (bada moment: key number ya screen), full camera (story, emotion, punchline, CTA — ≥5 s ke stretches); proof (paper) aur face (full camera) ko alternate karo taaki aankh ko aaram mile
- **Kyun:** Ek hi layout poori video me monotonous lagta hai; layout ka badlaav hi bina effect ke variety deta hai
- **Kitni baar:** Har short par
- **Evidence:** 🟠 — Melvynx edit skill ke teen layouts
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-209 — Hook ka visual ek mini-story ho
- **Purana ID:** A-081
- **Kab:** Hook ka visual design karte waqt
- **Kya:** Hook ka visual 2-3 acts ki mini-story ho — reversal ke saath, kai layers saath move karein, har keyword par impact (stamp + thud) aaye, aur payoff badge ki tarah land kare; ek object rakh kar use slide kar dena kaafi nahi
- **Kyun:** Hook ka visual hi pehle 2 s me 'ye alag hai' ka saboot hai; sust visual vaade ko khokhla kar deta hai
- **Kitni baar:** Har hook par
- **Evidence:** 🟠 — Melvynx hook-design reference (house craft)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-210 — Music bed emotion se chuno, dohrao mat
- **Purana ID:** A-082
- **Kab:** Short ke liye music bed chunte waqt
- **Kya:** Bed ko hook ke emotion se chuno; busy ya dynamic track voice ke neeche kabhi mat rakho (aise tracks test me reject ho chuke hain); pichle short me use hua bed is short me dobara mat use karo
- **Kyun:** Galat bed poori video ka mood ulta kar deta hai, aur dohraaya bed 'wahi purana' ka ehsaas deta hai
- **Kitni baar:** Har short par nayi bed chuno
- **Evidence:** 🟠 — Melvynx music defaults aur test-rejected tracks ka house record
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-211 — Music ka offset payoff par land karana
- **Purana ID:** A-083
- **Kab:** Track ko timeline par rakhte waqt
- **Kya:** Bade payoff ko track ke kisi mazboot pal par land karana ho to offset = c − P rakho (jaise full section payoff par aaye, usse pehle 10-20 s ka break pocket ho); full-camera emotional line ke liye offset = brk − E; aam default: offset = a point (10 s ki intro skip, pulse frame 1 se); offset + lambaai kabhi track ke 'out' pal se aage na jaye
- **Kyun:** Track ka sabse mazboot pal video ke sabse mazboot pal par mile to dono ek dusre ko uthate hain
- **Kitni baar:** Har track placement par
- **Evidence:** 🟠 — Melvynx edit plan ke music rules (reads se naape gaye a/b/brk/c points)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-212 — Movement shor nahi, sirf payoff hits
- **Purana ID:** A-084
- **Kab:** Sound design/hits lagate waqt
- **Kya:** Thud sirf number land/die hone par, pop sirf asal arrival par rakho; ek aam short me music ke alawa 2-4 sounds hi rakho; entrance clicks, whooshes aur risers copy ya add mat karo (riser bhi shor hai — sirf hit bache); bundled hit gains: impact-boom −8 dB, zhhh −6 dB, riser −12 dB (voice ke neeche)
- **Kyun:** Har harkat par awaaz lagane se awaaz ka matlab khatm ho jata hai; kam aur sahi jagah wale hits hi mehsoos hote hain
- **Kitni baar:** Har short par 2-4 sounds (music se alag)
- **Evidence:** 🟠 — Melvynx style-steal learnings (galat copies ko reject karke bane house rules)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-213 — Color grade ka kram aur shot matching
- **Purana ID:** A-085
- **Kab:** Color correction/grade karte waqt
- **Kya:** Isi kram me chalo: pehle normalize (log ko delivery color space me) → exposure scopes se set karo → white balance → scene ke saare shots ko hero shot se match karo (consistent grade hi sabse bada professional farak hai) → look/LUT aakhir me, sirf normalized footage par; skin tones ka red/green ka santulan mat bigado; screens aur graphics ko kabhi grade mat karo
- **Kyun:** Galat kram me grade karne se har shot alag lagta hai aur look footage ko tod deta hai
- **Kitni baar:** Har project par
- **Evidence:** 🟠 — kmilo color reference (creator practice) + Melvynx grade system ka ek hi kram
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Melvynx_video-agent-skills.md`

### R-214 — Transitions ke matlab
- **Purana ID:** A-086
- **Kab:** Do shots ke beech transition chunte waqt
- **Kya:** Har transition ka apna matlab rakho: cut = nirantarta (continuity), dissolve = samay/jagah/topic ka badlaav, fade to black = ek block ka ant; Premiere ka default dissolve 1 s hai — use tabhi rakho jab badlaav asal me ho; flashy transitions (spin, glitch) har cut par kabhi nahi
- **Kyun:** Har cut par flashy transition dhyaan ko kahani se hata kar khud par le jata hai
- **Kitni baar:** Har transition par
- **Evidence:** 🟠 — Creator source (StudioBinder) + Adobe official docs
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-215 — Thumbnail ke niyam ⚙️
- **Purana ID:** A-087
- **Kab:** YouTube thumbnail banate waqt
- **Kya:** File 1920×1080 JPG, 2 MB se kam; text 1-5 shabd (ideal 3-4) heavy sans-serif me, ~180 px par padh sakne wale; thumbnail title ko repeat na kare — use complement kare; ek hi dominant subject, 2-3 elements se zyada nahi; bottom-right corner khaali rakho (duration wahan aata hai); thumbnail jo vaada kare woh video ke pehle 30 s me milna chahiye
- **Kyun:** Mobile feed me thumbnail chhota dikhta hai — wahan padh sakne wala, ek-subject wala design hi click lata hai, aur jhootha vaada retention ko marta hai
- **Kitni baar:** Har video par
- **Evidence:** 🟡 — YouTube official spec (1920×1080, <2 MB) + creator testing ke legibility numbers
- **Sources:** `github_kmilo93sd_agent-video-editor.md`
- **Check:** `{"kind": "max_words", "what": "thumbnail_text", "value": 5}`

### R-216 — Title ki lambai (≤100 chars) aur front-loading ⚙️
- **Purana ID:** A-088, C-058
- **Kab:** Video ka title likhte/finalize karte waqt
- **Kya:** Title 100 characters ke andar rakho (hard cap); sweet spot 40-60 rakho aur click decide karne wale shabd SABSE PEHLE (colon se pehle) — desktop search ~60 par aur mobile home feed ~40 par truncate karta hai, mobile truncation subject ko hi kaat sakta hai. Search video ke liye wohi shabd rakho jo log type karte hain, discovery video ke liye curiosity ya stakes pehle rakho; poora caps ya clickbait mat rakho
- **Kyun:** Lamba title feed me kat jata hai aur truncation dono jagah alag tareeke se fail karta hai — desktop par tail jata hai, mobile par subject ja sakta hai; galat iraade wala title galat viewer lata hai jo turant chala jata hai
- **Kitni baar:** Har title par
- **Evidence:** 🟡 — YouTube official title limit (100 chars) + truncation points platform behaviour (dono clusters me documented); sweet spot aur front-loading craft recommendation hai
- **Sources:** `github_kmilo93sd_agent-video-editor.md`, `github_Jakeschincariol_youtube-agent-skill.md`, `github_sergebulaev_youtube-skills.md`
- **Check:** `{"kind": "max_chars", "what": "title", "value": 100}`

### R-217 — Cover frame / title card ⚙️
- **Purana ID:** A-089
- **Kab:** Short/Reel ka cover banate waqt
- **Kya:** Cover par public-safe line ≤7 shabd me rakho (ExpoCut: frame 0 par padh sakne wala 3-5 shabd), center-anchored, ~2.0 s hold, 1-2 lines; Reels ke 1:1 center crop ke liye text x 22-78% ke andar rakho; cover frame video ke 0.3-0.4 s se render karo; test: cover dekh kar koi ajnabi topic bata sake
- **Kyun:** Cover hi grid me video ki pehchan hai — wahan se samajh na aaye to click bhi nahi aata
- **Kitni baar:** Har short par
- **Evidence:** 🟠 — mktkit cover rules (public-safe gate) + ExpoCut frame-0 hook (Free to use and redistribute with attribution to expocut.com)
- **Sources:** `github_1610-advisory_mktkit.md`, `github_expocut_claude-plugin_retention-playbook.md`
- **Check:** `{"kind": "max_words", "what": "cover_title", "value": 7}`

### R-218 — Shorts reframe subject par rakho
- **Purana ID:** A-090
- **Kab:** 16:9 footage ko vertical me badalte waqt
- **Kya:** Crop ko shot-by-shot subject par rakho — fixed center crop kabhi nahi; do speakers hon to dono ko sikoṛne ke bajaye unke beech cut karo ya stack karo; screen ya wide shot ka relevant hissa bada karke dikhao; clips nikalne ka plan ho to 4K me record karo
- **Kyun:** Center crop aksar subject ko hi kaat deta hai; subject-centered reframing hi vertical ko asal lagta hai
- **Kitni baar:** Har reframed shot par
- **Evidence:** 🟠 — kmilo shorts recipe ka creator practice
- **Sources:** `github_kmilo93sd_agent-video-editor.md`

### R-219 — Style copy karna ho to pehle naapo
- **Purana ID:** A-091
- **Kab:** Kisi creator ki editing style copy karne se pehle
- **Kya:** Pehle original ko naapo: cuts/sec (scene detection se), spectrogram se SFX aur hit ke pal, face screen ka kitna % hai, zoom jumps, music ki BPM aur voice ke neeche uski level — sirf frames dekh kar copy mat karo (wahan sound aur rhythm gayab rehte hain, aur copy isi liye nakli lagta hai); apne numbers original ke andar rakho (zyada jumps nahi, bada face nahi); result side-by-side compare karke hi dikhao
- **Kyun:** Do baar ki nakli copies (zyada zoom, bada face, har entrance par whoosh) isi sabak se bane rule hain — naap hi style ka asal DNA deti hai
- **Kitni baar:** Har style-copy project se pehle
- **Evidence:** 🟠 — Melvynx steal skill ke learnings (rejected copies ke aadhar par)
- **Sources:** `github_Melvynx_video-agent-skills.md`

### R-220 — Zoom in = zor, zoom out = naya topic ⚙️
- **Purana ID:** B-062
- **Kab:** Edit me zoom use karte waqt
- **Kya:** Zoom in (push) key point par zor dene ke liye — important palon me 2–4 per minute. Zoom out (pull) naye topic ke transition par
- **Kyun:** Zoom direction ka matlab hota hai: andar = 'ye zaroori hai', bahar = 'hissa badla'
- **Kitni baar:** Zoom in 2–4/min (sirf important palon me); zoom out har topic transition par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`
- **Check:** `{"kind": "per_min_range", "what": "zoom_in", "min": 2, "max": 4}`

### R-221 — Jump cut: dead air hatao, pace tez karo ⚙️
- **Purana ID:** B-063
- **Kab:** Fast sections ke edit par
- **Kya:** Jump cut ka kaam dead air hatana aur pacing tez karna rakho; fast sections me har 5–10s me jump cut aaye
- **Kyun:** Jump cut energy ko banaye rakhta hai bina naye footage ke
- **Kitni baar:** Fast sections me har 5–10s
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`
- **Check:** `{"kind": "max_visual_gap_s", "value": 10}`

### R-222 — SFX kam rakho: poori video me 3–5 max ⚙️
- **Purana ID:** B-064
- **Kab:** Sound effects lagate waqt
- **Kya:** SFX sirf joke ko punctuate karne ya transition par zor dene ke liye; poori video me kul 3–5 se zyada nahi
- **Kyun:** Zyada SFX apna asar kho dete hain aur sasta lagne lagte hain
- **Kitni baar:** Max 3–5 SFX per video
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`
- **Check:** `{"kind": "max_count", "what": "sound_effects_per_video", "value": 5}`

### R-223 — Split screen sirf comparison/transformation par
- **Purana ID:** B-065
- **Kab:** Split screen use karte waqt
- **Kya:** Split screen sirf before/after ya comparison/transformation wale palon par use karo
- **Kyun:** Split screen ka matlab hi tulna hai; bina tulna ke wo sirf shor hai
- **Kitni baar:** Sirf comparison/transformation moments par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`

### R-224 — Subtitle emphasis sirf quotable palon par
- **Purana ID:** B-066
- **Kab:** Captions ke upar emphasis style lagate waqt
- **Kya:** Subtitle emphasis (highlight/bold) sirf quotable moments ya key takeaways par lagao — har line par nahi (poori captions wali lazmi rule B-033 alag hai)
- **Kyun:** Har jagah zor = kahin zor nahi; chune hue pal hi yaad rehte hain
- **Kitni baar:** Sirf quotable/key-takeaway lines par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_TheCraigHewitt_skills_retention-editing.md`

### R-225 — Music awaaz ke neeche, levels me koi jhatka nahi ⚙️
- **Purana ID:** B-067
- **Kab:** Audio mix karte waqt
- **Kya:** Background track −20 se −25 dB par rakho aur voice −6 se −10 dB par (music kabhi voice se takraye nahi). Audio levels poori video me consistent rakho — jarring volume changes nahi. Music speech ke neeche low, non-speech palon me upar; strategic silence bhi ek tool hai. Trending audio tabhi use karo jab content se relevant ho, force mat karo
- **Kyun:** Competing music samajh ko khata hai (Samajh > Style); consistent levels viewer ko bina wajah jhatka nahi dete
- **Kitni baar:** Poora mix; music −20..−25 dB, voice −6..−10 dB
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`, `github_TheCraigHewitt_skills_retention-editing.md`, `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "db_range", "field": "background_music_db", "min": -25, "max": -20}`

### R-226 — Color grade saare clips me ek jaisa
- **Purana ID:** B-068
- **Kab:** Post-production / grade par
- **Kya:** Saare clips ki brightness/contrast match karo aur ek subtle LUT ya color preset lagakar brand consistency rakho
- **Kyun:** Badalte rang har cut par dhyaan kheench lete hain — kahani se hata kar technique par
- **Kitni baar:** Har video, saare clips par
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_classicchins_compounding-marketing.md`

### R-227 — Opening visual pattern interrupt ke 4 roop ⚙️
- **Purana ID:** B-069
- **Kab:** Short ke pehle 3 seconds me visual hook chahiye to
- **Kya:** In me se koi ek chalao: (1) sudden movement (jump up, turn, desk par kuch patakna), (2) strong facial expression (shock/exasperation/huge smile), (3) out-of-context object (absurd sign, badi pile, countdown), (4) unexpected color/lighting
- **Kyun:** Feed scroll ko todne ke liye sabse tez hathiyar visual surprise hai
- **Kitni baar:** Suitable shorts ki opening me, koi ek
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Check:** `{"kind": "hook_within_s", "value": 3}`

### R-228 — Har beat ka 5-layer storyboard banao
- **Purana ID:** B-070
- **Kab:** Short-form script/storyboard likhte waqt
- **Kya:** Har beat ko 5 layers me likho: (1) VISUAL — framing, expression, props, graphics, transition; (2) AUDIO — word-for-word dialogue, tone, pacing; (3) ON-SCREEN TEXT — text, position (top/center/bottom), timing; (4) DIRECTING — cuts kahan, zoom in/out, editing pace; (5) MUSIC/SFX — music type, SFX, volume (speech ke neeche low, non-speech me high)
- **Kyun:** Jo layer script me nahi likhi gayi wo edit me andaze se banti hai; 5-layer format har beat ko pehle se tay karta hai
- **Kitni baar:** Har beat, har short-form script me
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`

### R-229 — Speaker performance: natural, camera se baat, jaan-boojh ke pauses
- **Purana ID:** B-071
- **Kab:** Recording ke dauraan (founder/creator on camera)
- **Kya:** Camera me aise dekho jaise colleague se baat kar rahe ho, audience se nahi; expressions natural, rehearsed nahi; haath dikhai dein (natural gestures); emphasis ke liye 1–2s ke short pauses — ye khamoshi 'extremely powerful' hoti hai; chhoti galtiyan theek hain, imperfection authentic lagta hai. Har segment ke 2–3 takes lo taaki edit ke paas options hon; saaf audio (background noise nahi)
- **Kyun:** Natural delivery bharosa banati hai; jaan-boojh ki khamoshi boli gayi line se zyada zor deti hai
- **Kitni baar:** Har recording session; har segment 2–3 takes
- **Evidence:** 🟠 — creator/editor opinion ya house rule — source me measured data nahi diya gaya
- **Sources:** `github_filnik_social-media-manager-AI.md`
- **Takraav note:** Dead-air rule (B-051) se takraav lag sakta hai: wahan bina-kaarann wali khamoshi kat-ti hai, yahan 1–2s ka pause jaan-boojh kar emphasis ke liye hai aur visual use uthata hai. Dono ka faisla intention se hoga — Step 3 me note rahe. (dekho CONFLICTS.md)

### R-230 — Production value platform aur job se milao
- **Purana ID:** B-072
- **Kab:** Production tier chunne par
- **Kya:** Polish platform/job ke hisaab se rakho, brand ke ego ke hisaab se nahi: performance ads (Meta/TikTok) par scrappy iPhone/UGC video mehngi animated production ko peeche chhod deta hai (source: 2024 Meta studies me 3:1 tak). MrBeast ka siddhant bhi yahi: goal 'best YOUTUBE video' hai, 'best produced video' nahi
- **Kyun:** Galat tier par paisa lagana sabse mehengi galti hai — mehenga hona hi dekha jana nahi hai
- **Kitni baar:** Har production decision par
- **Evidence:** 🟡 — platform study claim skill me cited (Meta creative studies 2024) + creator practice
- **Sources:** `github_classicchins_compounding-marketing.md`, `github_filnik_social-media-manager-AI.md`

### R-231 — Frame declutter — closer, saaf framing
- **Purana ID:** C-004
- **Kab:** Kisi frame me competing subjects ya clutter ho
- **Kya:** Closer aur cleaner framing chuno — frame me elements kam rakho taaki dhyaan ek jagah rahe
- **Kyun:** Cutting ke programme me century-lambi trend fewer elements per frame ki hai; ye attention control hai, fashion nahi
- **Kitni baar:** Har cluttered shot par
- **Evidence:** 🟡 — Trend measured hai; 'isiliye retention badhega' application inference hai
- **Sources:** `science_james_cutting.md`
- **Takraav note:** Tim Smith ke 'one magnet per shot' (C-007, 🟢) se milta-julta hai — wahan dhyaan do (dekho CONFLICTS.md)

### R-232 — Eye-trace landing — subject wahi jahan aankh hai
- **Purana ID:** C-006
- **Kab:** Cut ke baad wala shot compose/select karte waqt
- **Kya:** Shot B ka main subject lagbhag usi screen area me rakho jahan shot A ke end par viewer ka focus tha (ya use sabse strong motion/face cue banao), taaki aankh ko cut ke baad dhundna na pade
- **Kyun:** Attentional synchrony: sab viewers ek saath ek hi jagah dekhte hain; sahi landing par cut mehsoos hi nahi hota
- **Kitni baar:** Har important cut par
- **Evidence:** 🟢 — Gaze clustering frame-by-frame eye-tracking se measured, kai studies me replicated
- **Sources:** `science_tim_smith.md`
- **Takraav note:** Murch ka eye-trace criterion (C-017) yahi baat 🟠 craft ke roop me kehta hai; ye uska measured version hai (dekho CONFLICTS.md)

### R-233 — Murch 4 — Eye-trace ka khayaal (7%)
- **Purana ID:** C-017
- **Kab:** Cut aur composition ka faisla karte waqt
- **Kya:** Dekho ki audience ka focus frame me kahan aur kis taraf move kar raha hai, aur cut usi trace ko acknowledge kare
- **Kyun:** Eye-trace chautha criterion hai — cut ke paar nazar ka safar smooth rahe to cut ghulta hai
- **Kitni baar:** Har cut par
- **Evidence:** 🟠 — Murch ki raay 🟠 hai, lekin isi baat ko Smith ke eye-tracking ne baad me measure karke 🟢 support diya (C-006)
- **Sources:** `science_walter_murch.md`

### R-234 — Murch 5 — 2-D plane / screen direction (5%)
- **Purana ID:** C-018
- **Kab:** Cut par stage line ya screen direction ka sawal aaye
- **Kya:** Screen ki 2-D grammar (stage line, screen direction) ka samman karo — lekin ye upar ke chaar criteria ke liye qurban ho sakta hai
- **Kyun:** Planarity paanchva criterion hai; iska kaam asli 3-D space ko 2-D screen par padhne layak rakhna hai
- **Kitni baar:** Har spatial cut par
- **Evidence:** 🟠 — Craft wisdom, koi measurement nahi
- **Sources:** `science_walter_murch.md`

### R-235 — Murch 6 — 3-D space continuity (4%)
- **Purana ID:** C-019
- **Kab:** Characters ki asal spatial positions ka sawal aaye
- **Kya:** Asli 3-D space ki continuity rakho jab muft me mile; ye sabse halka criterion hai — sabse pehle yahi qurban hoga
- **Kyun:** Sirf 4% weight: perfect spatial continuity bhi emotion-fail cut ko nahi bacha sakti, aur audience engaged ho to spatial jumps notice hi nahi karti
- **Kitni baar:** Har spatial cut par, sabse kam priority
- **Evidence:** 🟠 — Murch ki raay; audience ke spatial details na notice karne wali baat ko Smith ke attention findings se partial support milta hai
- **Sources:** `science_walter_murch.md`

### R-236 — Shorts overlay — dusra hook, 5-7 shabd ⚙️
- **Purana ID:** C-038
- **Kab:** Short-form hook ke saath on-screen text lagate waqt
- **Kya:** Overlay 5-7 shabdon me rakho; spoken line ki tamam — wahi promise, alag shabd — taaki sound-on aur muted dono viewers ko pura hook mile
- **Kyun:** Autoplay aksar muted chalta hai; overlay hi muted viewer ka hook hai
- **Kitni baar:** Har short-form hook par
- **Evidence:** 🟠 — SkillMedev ki rule; Jake bhi Shorts ke pehle 2s ke liye spoken se alag shabdon wala on-screen text kehta hai
- **Sources:** `github_SkillMedev_skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`
- **Check:** `{"kind": "word_range", "what": "hook_overlay", "min": 5, "max": 7}`

### R-237 — Title formulas — corpus-validated ko pehle
- **Purana ID:** C-057
- **Kab:** Title likhte waqt formula chunna ho
- **Kya:** Formulas me se chuno: Y1 Curiosity-Gap, Y2 Number/Listicle, Y3 How-I Outcome, Y4 Mistake/Negativity, Y5 Transformation, Y6 Versus, Y11 Third-Party Success Story. Corpus me Y1/Y3/Y5 confirmed over-performers hain (214-video pull); Y11 sabse zyada frequent uncaptured shape tha. Har title me curiosity ke saath ek concrete noun rakho; number wala dawa sach aur apna ho
- **Kyun:** Formula hi title ko summary se promise banata hai; corpus validation batata hai kaunse shapes asal me over-perform karte hain
- **Kitni baar:** Har title par 1 formula; 3-5 variants kam se kam 2 formulas se
- **Evidence:** 🟡 — 214-video corpus (July 2026, business/creator niche, subscriber-normalized) me Y1/Y3/Y5 validated aur Y11 discover hua — measured corpus, controlled experiment nahi; sirf title formulas is data se test ho sakte hain, opening hooks nahi
- **Sources:** `github_sergebulaev_youtube-skills.md`
- **Takraav note:** Y2/Y4/Y6 is corpus me kamzor ya gayab mile (Y4 aur Y6 business niche me essentially absent) — ye formulas gear/tutorial niches me kaam kar sakte hain, lekin 'proven' mat mano (dekho CONFLICTS.md)

### R-238 — Title ki samagri — number/naam/date, vague shabd nahi
- **Purana ID:** C-059
- **Kab:** Title ke shabd chunte waqt
- **Kya:** Ek number, naam ya date rakho — ye har adjective ko harata hai. Vague shabd (amazing, incredible, insane, ultimate, best, secret...) hatao. Pehle 3 shabd sirf filler na hon — subject aage lao. Title sawaal par khatm ho to open question ka plus milta hai
- **Kyun:** Concreteness hi click ka sabse bharosemand single fix hai; vagueness andaza lagwati hai
- **Kitni baar:** Har title par
- **Evidence:** 🟠 — title.py ke checks + serge ki voice rules — craft heuristics
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`, `github_sergebulaev_youtube-skills.md`
- **Takraav note:** All-caps par sources me halka farak: Jake ceiling 2 caps shabd deta hai, serge full-caps title banned aur 1 emphasized shabd tak rakhta hai — sakht wala (serge) surakshit rahega (dekho CONFLICTS.md)

### R-239 — Thumbnail core — ek focal point, sachhi emotion, 120px test
- **Purana ID:** C-060
- **Kab:** Thumbnail concept banate waqt
- **Kya:** Ek hi focal point rakho (face + specific emotion, ya object/result). Emotion video ki asal feeling se match kare — shaant tutorial par shocked face retention se mehnga padega. High contrast aur subject separation rakho (rim light, darkened/blurred background). Har concept ko 120px par shrink karke dekho: wahan padhna aaye tabhi pass. 3 se zyada visual elements kabhi nahi
- **Kyun:** Thumbnail aadhe second me, 120px par, ek darjan competitors ke beech padha jata hai; do competing subjects impact aadha kar dete hain
- **Kitni baar:** Har thumbnail par
- **Evidence:** 🟠 — Teenon sources ke thumbnail rules ka sangam; 120px test teeno me hai
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_SkillMedev_skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`

### R-240 — Thumbnail text — target 3 shabd, title se alag ⚙️
- **Purana ID:** C-061
- **Kab:** Thumbnail par text overlay likhte waqt
- **Kya:** Overlay ke shabd title ke shabdon se bilkul alag rakho — dono aadhi click surface ek hi baat do baar keh kar barbaad karte hain. Lambai ka target 3 shabd rakho. Text bottom-right third me kabhi nahi (duration badge dhakta hai). Ek emphasis shabd all-caps/color me chalega
- **Kyun:** Title aur thumbnail ek unit hain; duplication aadhi jagah ki barbaadi hai, aur feed size par chautha-paanchva shabd grey smear ban jata hai
- **Kitni baar:** Har thumbnail par
- **Evidence:** 🟠 — Teenon sources overlay ko title se alag rakhne par ekmat hain; ginati par farak hai (neeche conflict dekho)
- **Sources:** `github_Jakeschincariol_youtube-agent-skill.md`, `github_sergebulaev_youtube-skills.md`, `github_SkillMedev_skills.md`
- **Check:** `{"kind": "max_words", "value": 3, "what": "thumbnail_text"}`
- **Takraav note:** Shabd-limit par sources takrate hain: Jake '3 maximum' kehta hai (tool 4 par flag karta hai), serge '4 ya kam', SkillMedev '2-5, target 3, hard ceiling 5'. Target 3 sab me surakshit hai; Step 3 ek number final kare (dekho CONFLICTS.md)

### R-241 — Thumbnail ke 2-3 concepts, ek bada element vary karo
- **Purana ID:** C-062
- **Kab:** Thumbnail finalize karne se pehle
- **Kya:** Hamesha 2-3 concepts banao (jaise face-forward / object-result / text-heavy minimal) aur har concept me sirf EK bada element badlo (face vs object, text vs no-text, warm vs cool color) taaki Test & Compare ka result padhne layak ho. Ek lead concept recommend karo — jeet watch-time share se naapo, sirf CTR se nahi
- **Kyun:** Ek concept dena andaza hai; ek-saath paanch chhoti cheezein badalne se test kuch nahi batata
- **Kitni baar:** Har video par 2-3 concepts
- **Evidence:** 🟠 — serge + SkillMedev ki shared workflow rule
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_SkillMedev_skills.md`

### R-242 — Description — pehle 150 characters hi hook ⚙️
- **Purana ID:** C-063
- **Kab:** Description likhte waqt
- **Kya:** Pehli ~150 characters ko dusra hook banao: payoff ya sawaal + primary keyword natural tareeke se. Yehi 'Show more' se pehle dikhta hai aur search snippet hai. Kul lambai 5,000 characters ke neeche. Keywords natural sentences me (primary phrase pehle 150 me ek baar, body me ek baar), comma-dump kabhi nahi. Hashtags aakhir me 3-5; 15 se zyada hon to YouTube sab ignore kar deta hai. Tags sirf disambiguation ke liye, 15 kaafi
- **Kyun:** Pehli lines ke alawa description zyada tar koi padhta hi nahi; wahi hissa search ko bhi khilati hai
- **Kitni baar:** Har video par
- **Evidence:** 🟡 — 5,000-char cap aur 150-char visibility platform ke documented behaviour hain; baaki structure craft hai
- **Sources:** `github_sergebulaev_youtube-skills.md`, `github_Jakeschincariol_youtube-agent-skill.md`
- **Check:** `{"kind": "max_chars", "value": 5000, "what": "description"}`

### R-243 — Channel page — trailer, banner safe area, About ki pehli 2 lines
- **Purana ID:** C-067
- **Kab:** Channel page audit/setup karte waqt
- **Kya:** Trailer non-subscribers ke liye 30-90s ki bana-banayi pitch rakho (random recent upload nahi) — ye subscriber conversion ka sabse bada lever hai. Banner 2560x1440 par banao lekin value prop + cadence centered 1235x338 safe area ke andar rakho (mobile/TV par kinare cut te hain). About ki pehli 2 lines me poora value prop: kiske liye, kya milta hai, kitni baar, ek proof. Ek hi primary link rakho
- **Kyun:** Video se click karke aaya viewer ek pal me faisla karta hai; trailer/banner/About hi use subscriber banate hain
- **Kitni baar:** Channel setup par aur har audit par
- **Evidence:** 🟠 — serge channel-optimizer ki scorecard rules; banner dimensions platform spec hain
- **Sources:** `github_sergebulaev_youtube-skills.md`

### R-244 — Zoom neighbouring segments me alternate karo
- **Purana ID:** C-074
- **Kab:** Cut par punch-in/zoom lagate waqt
- **Kya:** Paas wale segments ke beech zoom alternate karo (jaise 1.00 / 1.045 / 1.09); climax par maximum zoom rakho. Isse cut angle badalne jaisa padhta hai, galti jaisa nahi
- **Kyun:** Ek jaisa frame cut par 'jump' lagta hai; halka scale farak use deliberate choice bana deta hai
- **Kitni baar:** Har cut par alternating
- **Evidence:** 🟠 — blazerior ki EDL practice (segments me zoom 1.00/1.045 pattern)
- **Sources:** `github_blazerior_videoediting-claude-skill.md`

### R-245 — Ek stretch bina graphics ke — viewer ko hawa do
- **Purana ID:** C-075
- **Kab:** Minute-bhar ke video me overlays/cards lagate waqt
- **Kya:** Har minute me kam se kam ek 4-6 second ka saaf stretch rakho jisme koi graphic na ho. Cards ki thos deewaar viewer ko thaka deti hai
- **Kyun:** Bina saans ki visual bharmar dhyaan ko hi kha jati hai; khaali stretch hi accents ko wazan deta hai
- **Kitni baar:** Har minute me ≥1 saaf stretch
- **Evidence:** 🟠 — blazerior ki do jagah (SKILL rule 7 + storyboard rhythm) dohraayi rule
- **Sources:** `github_blazerior_videoediting-claude-skill.md`

### R-246 — Card face ke upar — kabhi face PAR nahi (safe zones)
- **Purana ID:** C-076
- **Kab:** 1080x1920 vertical video me card/panel rakhte waqt
- **Kya:** Card ko face ke UPAR (above) rakho, face ke upar (on) kabhi nahi — panel beech frame me gira to aankhein dhak jati hain, aur speaker ki nazar hi video ke bharose ka aadha hissa hai. Zones rakho: top 0-150 platform UI (kuch nahi), graphics ka working area 200-1250, face aam taur par 700-1300 (bahar rakho), subtitles 1380-1520, bottom 1600-1920 platform UI (kuch nahi). Zoom wale segment par face bada/unar hota hai — card ki jagah usi hisaab se check karo
- **Kyun:** Aankhein dhakna sabse aam pehli-galti hai; safe zones platform UI se takraav bachate hain
- **Kitni baar:** Har card placement par
- **Evidence:** 🟠 — blazerior design-system ki zones table — is skill ke tested layout numbers
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Takraav note:** SkillMedev ke per-platform safe-area percentages (TikTok/Reels/Shorts ke insets) se ye alag number set hai — dono ek hi sach ke do roop hain; Step 3 me ek zone table final hogi (dekho CONFLICTS.md)

### R-247 — Word-level subtitles — line me zyada se zyada 3 shabd ⚙️
- **Purana ID:** C-077
- **Kab:** Vertical video ke liye burned-in word-level subtitles banate waqt
- **Kya:** Line me zyada se zyada 3 shabd rakho; 0.7s se bada pause nayi line tod de. Active (bola ja raha) shabd tint karo aur 8% bara karo (108% scale; 110% se aage line hilne lagti hai). Font size 72, WrapStyle 0 lazmi (2 par lambi line screen se bahar jati hai). Subtitle text proofread karo — galti picture me jal jaye to permanent hai
- **Kyun:** Shabd-dar-shabd highlight bolne ki gati se milta hai; zyada shabd aur galat wrap padhne ko marta hai
- **Kitni baar:** Har subtitle line par
- **Evidence:** 🟠 — blazerior make_ass.py ke constants (MAX_WORDS 3, MAX_GAP 0.7) — is pipeline ke shipped numbers
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Check:** `{"kind": "max_words", "value": 3, "what": "subtitle_line"}`
- **Takraav note:** Caption ke teen mode is cluster me hain: ye word-level (3 shabd), SkillMedev ki phrase captions 32-42 chars/line (C-085 ke saath dekho), pifferologo ki 2-shabd chunks (C-098) — mode content ke hisaab se batega, Step 3 tay kare (dekho CONFLICTS.md)

### R-248 — Loudness −14 LUFS (social standard) ⚙️
- **Purana ID:** C-078
- **Kab:** Social platforms ke liye final audio normalize karte waqt
- **Kya:** Final loudnorm I=-14 LUFS, TP=-1.5, LRA=11 rakho (two-pass zyada accurate hai). Isse shaant = amateurish, isse tez = platform khud neeche kar dega
- **Kyun:** Reels/TikTok/Shorts ka normalization target yahi hai; platform ki apni ceiling se ladna bekaar hai
- **Kitni baar:** Har final render par
- **Evidence:** 🟡 — Platform loudness standard ke roop me widely documented; blazerior cookbook bhi yahi spec deta hai (mean ~-18 dB expected after loudnorm)
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Check:** `{"kind": "lufs_target", "tolerance": 1, "value": -14}`

### R-249 — Grade tulna karke chuno, moderate rakho
- **Purana ID:** C-079
- **Kab:** Colour grade tay karte waqt
- **Kya:** Grade aankh se andaze par mat chuno: ek frame nikalo, candidate grades us par chalao, frames ko stack (hstack) karke saath-saath dekho, phir chuno. Grade moderate rakho — 8-bit phone footage par aggressive curves gradients par banding la dete hain (khaaskar subject ke peeche wali deewaar par)
- **Kyun:** Akele frame par achha lagne wala grade তুলna me hi sach batata hai; banding ek baar render ho to poora video kharab
- **Kitni baar:** Har naye grade faisle par
- **Evidence:** 🟠 — blazerior cookbook ki method rule
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Takraav note:** pifferologo ke CDL reasoning (C-097) se milta hai — dono 'ek badlav, phir dekho' kehte hain (dekho CONFLICTS.md)

### R-250 — Base grade recipe (tested values)
- **Purana ID:** C-080
- **Kab:** Talking-head ko backlight/mixed light se sudharna ho
- **Kya:** Base grade ye rakho: eq contrast=1.13, brightness=0.012, saturation=1.07, gamma=1.07; curves se shadows uthao (0.22→0.285) aur halka warm (red up, blue down); vignette=PI/9 (subtle; PI/5 strong hai); unsharp 5:5:0.45 scale/crop ki softness ke liye. Alternatives: neutral punch (contrast 1.12, sat 1.06), warm cinematic, pastel/film fade, ya ready .cube LUT (lut3d)
- **Kyun:** Ye values hard backlight par test hue hain: face shadow se uthta hai aur alag locations ek jaise lagte hain
- **Kitni baar:** Har naye project ka starting grade; phir material ke hisaab se badlo
- **Evidence:** 🟠 — blazerior cookbook ke tested filter values; ek hi pipeline ke numbers hain, universal law nahi
- **Sources:** `github_blazerior_videoediting-claude-skill.md`

### R-251 — Transitions me sakhti — hard cut default ⚙️
- **Purana ID:** C-081
- **Kab:** Do clips ke beech transition chunte waqt
- **Kya:** Default hard cut rakho — pause par hard cut lagbhag invisible hota hai aur har effect ko harata hai. Cross-fade (xfade 0.3s) sirf wahan kamata hai jahan frame me movement ho (baithna, khada hona, mudna). Talking head par fade/dissolve se aage ke effects amateur lagte hain. Yaad rakho: xfade result ko transition ke barabar chhota kar deta hai — baad ki saari timings (subtitles, overlays) shift ho jati hain; ya timings dobara ginno ya transitions chain ke aakhir me rakho. Audio par matching acrossfade 0.3s
- **Kyun:** Effect bina wajah ke dhyaan khinchta hai; timing shift chhupa hua kharcha hai jo subtitles ko bigaad deta hai
- **Kitni baar:** Har transition par
- **Evidence:** 🟠 — blazerior cookbook ki transition guidance
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Check:** `{"kind": "duration_range_s", "max": 0.3, "min": 0.3, "what": "crossfade"}`

### R-252 — Design restraint — 2 accent rang, type ki floor
- **Purana ID:** C-083
- **Kab:** Overlay design system tay karte waqt
- **Kya:** Zyada se zyada 2 accent colours rakho; accent frame me maujud cheez se chuno (kapde, deewaar, roshni) ya brand colours se. Type ka floor 36px hai (sirf captions ke liye bhi); chhota type phone par marta hai. Neon rang aur 4px outlines expert content ki credibility khatm kar dete hain. Panel par shadow lazmi hai, warna chipka hua lagta hai
- **Kyun:** Restraint hi design ko 'banaya hua' padhata hai; rangon ki bheed aur chhota type dono sasta lagte hain
- **Kitni baar:** Har overlay par
- **Evidence:** 🟠 — blazerior design-system ki 'what not to do' list
- **Sources:** `github_blazerior_videoediting-claude-skill.md`

### R-253 — Animation me restraint — 0.25s fade kaafi hai
- **Purana ID:** C-084
- **Kab:** Card/overlay ko animate karte waqt
- **Kya:** Sirf 0.25s ka fade rakho; fly-ins aur bounces dhyaan bolne wali baat se kheench lete hain. Animation apne aap ke liye kabhi nahi — motion tabhi jab wohi matlab uthaye
- **Kyun:** Overlay ka kaam speech ko support karna hai, usse compete karna nahi
- **Kitni baar:** Har overlay animation par
- **Evidence:** 🟠 — blazerior design-system ki rule
- **Sources:** `github_blazerior_videoediting-claude-skill.md`
- **Takraav note:** pifferologo ke animation durations/easing (C-099/C-100) se takraav nahi: wahan information-cards ki baat hai, yahan simple overlays ki (dekho CONFLICTS.md)

### R-254 — Social export — captions burned-in, safe area ke andar
- **Purana ID:** C-086
- **Kab:** Kisi platform ke liye export tay karte waqt
- **Kya:** Captions pixels me burn karo (uploaded .srt sidecar har platform par inconsistent aur un-styleable hai); zyada se zyada 2 lines, phrase chunks me speech ke sync; position platform ke safe area ke andar. Har platform ke insets rakho (% me, top/right/bottom/left): TikTok 6/11/17/3, Reels 7/12/18/3, Shorts 5/12/13/3, X 4/4/12/4, LinkedIn 4/4/10/4. Ek 9:16 master TikTok/Reels/Shorts teeno ko de (sabse tang inset — Reels ke bottom — par design karo) aur X/LinkedIn ke liye alag 1:1 ya 4:5 master. Ek hi 16:9 file har platform par mat bhejo — vertical feed me wo stripe ban jati hai
- **Kyun:** Safe area ke bahar rakhi cheez device par dikhti hi nahi (preview me theek lagti hai); sidecar captions style aur bharosa dono kho dete hain
- **Kitni baar:** Har platform export par
- **Evidence:** 🟠 — SkillMedev social-video-formatter ke compiled platform specs; file khud kehta hai specs drift hote hain — shipping se pehle current creator docs se verify karo
- **Sources:** `github_SkillMedev_skills.md`
- **Takraav note:** Safe-zone numbers blazerior ke pixel zones (C-076) se alag set hain — dono ko ek table me Step 3 merge karega (dekho CONFLICTS.md)

### R-255 — Reframe ki quality seedhi — re-layout sabse upar
- **Purana ID:** C-087
- **Kab:** Aspect ratio badalna ho (16:9 se 9:16 ya ulta)
- **Kya:** Quality ke is order me chuno: (1) Re-layout — pixels crop mat karo, scene ko naye canvas ke liye dobara compose karo (stack karo, type bada karo, subject vertical center me); (2) Punch-and-track — crop window action ko follow kare (keyframes do); (3) Center crop — sirf tab jab subject poore samay dead center ho, warna outer thirds ke saath subject bhi jayega; (4) Blur-pad — aakhri upay, talking-head/screen par chalega, motion piece par 'repost' ka signal deta hai. Subject move karta ho to blind center-crop kabhi nahi
- **Kyun:** Re-layout hi video ko platform ke liye 'banaya gaya' padhata hai, 'ghusaya gaya' nahi
- **Kitni baar:** Har reframe par
- **Evidence:** 🟠 — SkillMedev social-video-formatter ki strategy ranking
- **Sources:** `github_SkillMedev_skills.md`

### R-256 — Subtitles filter chain me SABSE LAST
- **Purana ID:** C-088
- **Kab:** Render pipeline ki order tay karte waqt
- **Kya:** Subtitles hamesha har overlay ke BAAD lagao. Pehle lagaye to overlays unhe dhak dete hain — aur ye silent failure hai, koi error nahi aata
- **Kyun:** Galat order kharab output deti hai bina kisi chetaavni ke; ye taste nahi, correctness hai
- **Kitni baar:** Har render par, bina exception
- **Evidence:** 🟠 — video-use ki Hard Rule 1 — production-correctness rule; house standard hai, koi bahari spec nahi (technical invariant)
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`

### R-257 — Per-segment extract → lossless concat; grade per-segment
- **Purana ID:** C-096
- **Kab:** Cuts ko render karte waqt
- **Kya:** Har segment alag extract karke lossless (-c copy) concat karo — overlays ke saath single-pass filtergraph mat chalao, warna har segment do baar encode hota hai. Grade bhi per-segment extraction ke waqt lagao, post-concat nahi
- **Kyun:** Double encoding quality khaata hai aur samay bhi; per-segment tareeka dono bachata hai
- **Kitni baar:** Har multi-segment render par
- **Evidence:** 🟠 — video-use Hard Rule 2 + grade section — pipeline correctness rule
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`

### R-258 — Grade ko CDL se socho — ek badlav, phir dekho
- **Purana ID:** C-097
- **Kab:** Kisi frame ka grade theek karte waqt
- **Kya:** ASC CDL model se socho: slope = highlights, offset = shadows, power = midtones, phir global saturation. Ek frame dekho, galat cheez pehchano, EK cheez adjust karo, dobara dekho. Grade per-segment lagao; skin tones test kiye bina aggressive kabhi mat jao
- **Kyun:** Ek-saath kai badlav karna andaza hai; ek-badlav-iterative tareeka hi batata hai kis cheez ne kya kiya
- **Kitni baar:** Har grade decision par
- **Evidence:** 🟠 — video-use ki grade method; CDL khud ek industry standard model (ASC) hai, lekin 'ek badlav' wali vidhi house craft hai
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Takraav note:** blazerior ki comparison method (C-079) se milta hai — dono ek dusre ko mazboot karte hain (dekho CONFLICTS.md)

### R-259 — Subtitle chunking ke do tested style ⚙️
- **Purana ID:** C-098
- **Kab:** Burned-in subtitles ka style chunte waqt
- **Kya:** Short-form/fast social ke liye 'bold-overlay': 2-shabd chunks, UPPERCASE, punctuation par break, bold, MarginV=35. Narrative/documentary/education ke liye 'natural-sentence': 4-7 shabd chunks, sentence case, natural pauses par break, MarginV=60-80, bada font. Dono me subtitles LAST aur output-timeline offsets lazmi
- **Kyun:** Chunking, case aur placement ka sahi combo content par nirbhar hai; galat combo ya to chillata hai ya padha nahi jata
- **Kitni baar:** Har project ke style faisle par
- **Evidence:** 🟠 — video-use ke shipped worked styles (ek asal launch video se) — ek style dusre context ka law nahi
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Check:** `{"kind": "max_words", "value": 2, "what": "subtitle_chunk_bold"}`
- **Takraav note:** Caption modes ka teesra roop C-077 (word-level 3 shabd) aur C-085 (phrase 32-42 chars) me hai — teeno content-type se batega (dekho CONFLICTS.md)

### R-260 — Animation ki muddatein (cards/diagrams/accents) ⚙️
- **Purana ID:** C-099
- **Kab:** Overlay animation ki duration tay karte waqt
- **Kya:** Narration ke saath chalne wali explanation: floor ~3s, aam taur par simple cards 5-7s, complex diagrams 8-14s (viewer ko 1x par parse karna hai). Beat-synced accents (music/montage): 0.5-2s theek hai — wahan niyam 'parseable' nahi, 'recognizable at 1x' hai. Final frame kam se kam 1s hold karo (universal). Voiceover ke upar overlay ki kul duration narration + 1s se kam kabhi nahi
- **Kyun:** Information ko padhne ka samay chahiye; accent ko sirf pehchanna hai — dono ki ghadiyan alag hain
- **Kitni baar:** Har animation par
- **Evidence:** 🟠 — video-use ke duration rules of thumb — ek shipped video ke numbers, 'context-dependent' source khud kehta hai
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`
- **Check:** `{"kind": "duration_range_s", "max": 7, "min": 5, "what": "explanation_card"}`

### R-261 — Easing kabhi linear nahi; parallel reveal kabhi nahi
- **Purana ID:** C-100
- **Kab:** Animation ka motion design karte waqt
- **Kya:** Easing hamesha cubic rakho: single reveals ke liye ease_out_cubic (slow landing), continuous draws ke liye ease_in_out_cubic. Linear robotic lagta hai. Do independent elements ek saath reveal mat karo — aankh do nayi cheezein ek saath track nahi kar sakti: ek cheez, pause, phir agli
- **Kyun:** Linear motion machine jaisa padhta hai; parallel reveal dhyaan ko baant kar dono ko adhura chhodta hai
- **Kitni baar:** Har animation par
- **Evidence:** 🟠 — video-use ki universal-kahi hui rules; parallel-reveal wali baat Smith ke one-magnet (C-007, 🟢) se taal rakhti hai
- **Sources:** `github_pifferologo_ai-agent-video-editor.md`


### R-264 — Invisible cut ko harkat/roshni ke peeche chhupao *(naya — editor round)*
- **Purana ID:** D1-003
- **Kab:** Cut dikhai de raha ho lekin kahani me seam nahi dikhana
- **Kya:** Cut ko whip pan, frame cross karte object, light flash ya rack-focus blur ke peeche chhupao
- **Kyun:** Darshak ki aankh harkat/roshni ke saath beh jati hai aur seam ghayab ho jata hai
- **Kitni baar:** Har dikhne wale problem cut par
- **Evidence:** 🟠 — Editor craft parampara (note)
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`
- **Takraav note:** koptsev63 ke misdirection rule (D1-079) se sambandhit hai — wo khaas taur par movement/sound spike ki baat karta hai; takraav nahi

### R-266 — Grade ka kram aur LUT ki matra ⚙️ *(naya — editor round)*
- **Purana ID:** D1-005
- **Kab:** Colour grade lagana ho (Premiere Lumetri ya Resolve nodes)
- **Kya:** Kram rakho: Basic/Primary correction (scopes se black/white point, white balance) → Creative (LUT/Look hamesha kam intensity par) → Curves → Wheels/Secondary → skin-tone protection. Creative LUT ki intensity 50–70% rakho; Rec709 material par blend ≤55% rakho
- **Kyun:** Poori taakat ka LUT rang bigaad deta hai; sahi kram se correction aur look alag-alag control me rehte hain
- **Kitni baar:** Har grade par; LUT intensity 50–70% (Rec709 par ≤55%)
- **Evidence:** 🟠 — Do sources ke craft numbers (note + MIT skill); band ka sangat hissa 50–55% hai
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`, `github_koptsev63_premiere-claude-bridge.md`
- **Check:** `{"kind": "percent_range", "what": "creative_lut_intensity_pct", "min": 50, "max": 70}`
- **Takraav note:** Andar ka halka takraav: ADAM-0S 50–70% kehta hai, koptsev63 Rec709 par ≤55% ki hadd deta hai — sangat hissa 50–55%; Step 3 addendum me material-wise hadd tay ho

### R-267 — Pehle hero shot grade karo, phir baaki ko milao *(naya — editor round)*
- **Purana ID:** D1-006
- **Kab:** Ek scene ke kai shots ka grade match karna ho
- **Kya:** Pehle scene ka ek hero shot grade karke uska still bachao; phir har shot ko waveform (exposure), parade (balance), histogram (contrast), vectorscope (skin line) se usi still se milao
- **Kyun:** Har shot ko alag se grade karne se scene ke andar rang badalta rehta hai; hero shot se mel consistency deta hai
- **Kitni baar:** Har scene par ek hero shot pehle
- **Evidence:** 🟠 — Colourist craft (note)
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`

### R-270 — Mix levels ki seedhi (dBFS) ⚙️ *(naya — editor round)*
- **Purana ID:** D1-009
- **Kab:** Final mix ke levels tay karne hon
- **Kya:** Seedhi rakho: dialogue −12..−6 dBFS (sabse upar), dialogue ke neeche music −18..−24, bina dialogue ke featured music −12..−6, SFX −18..−6 (content ke hisaab se), ambience bed −24..−18
- **Kyun:** Levels ki seedhi hi tay karti hai ki kya sunai dega aur kya sirf mehsoos hoga; ulta-pulta mix baat dabaa deta hai
- **Kitni baar:** Poore mix me ye seedhi barkarar
- **Evidence:** 🟠 — Audio craft numbers (note); ye absolute dBFS band hai
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`
- **Check:** `{"kind": "db_range", "field": "music_under_dialogue_dbfs", "min": -24, "max": -18}`
- **Takraav note:** Purana niyam (ORDER #11) music ko voice ke RELATIVE 18–25 dB neeche kehta hai; ye band ABSOLUTE dBFS hai (−18..−24) — sankhya milti-julti hai lekin naap ka aadhar alag hai; Step 3 addendum me basis ek karna hoga

### R-271 — Broadcast/Netflix loudness ke naye band ⚙️ *(naya — editor round)*
- **Purana ID:** D1-010
- **Kab:** Delivery broadcast TV ya Netflix/cinema ke liye ho
- **Kya:** Integrated loudness destination ke hisaab se rakho: broadcast TV −24 LUFS, Netflix/cinema −27 LUFS (Netflix par true peak max −2 dBTP)
- **Kyun:** Har platform ki loudness shart alag hai; YouTube wala −14 wahan chalega nahi aur file reject/normalize hogi
- **Kitni baar:** Har delivery par destination-wise ek target
- **Evidence:** 🟠 — Platform delivery specs ka house sangrah (note)
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`
- **Check:** `{"kind": "lufs_target", "value": -24, "tolerance": 1}`
- **Takraav note:** Purane rules sirf −14 (YouTube) aur −16 (podcast/house) band dete hain — ye −24/−27 wale band naye hain; Step 3 addendum me destination-wise poori table banni chahiye (YouTube −14 / podcast −16 / broadcast −24 / Netflix −27)

### R-272 — Delivery bitrate ki hadd (quality bachane ke liye) *(naya — editor round)*
- **Purana ID:** D1-011
- **Kab:** Final export ki quality tay karni ho
- **Kya:** VBR 2-pass rakho; bitrate ke band: 1080p par lagbhag 10–24 Mbps, 4K par 35–68 Mbps, vertical (Reels/TikTok 1080×1920, 30 fps) 10–15 Mbps; master hamesha ProRes 422/DNxHR HQ jaisi quality me rakho
- **Kyun:** Bahut kam bitrate par saaf edit bhi keechad (muddy) dikhta hai — quality ka faisla export par bhi hota hai
- **Kitni baar:** Har delivery export par
- **Evidence:** 🟠 — Do sources ke delivery bands (note + MIT skill) — neeche conflict dekho
- **Sources:** `notes_ADAM-0S_wayland-m3ta-0s.md (note)`, `github_iart-ai_motion-design-skills.md`
- **Takraav note:** Sources ke beech farak: ADAM-0S 1080p 16–24 Mbps / 4K 45–68 Mbps kehta hai; iart-ai H.264 delivery 1080p ~10–16 Mbps / 4K ~35–50 Mbps kehta hai — aam sangat hissa 16 Mbps (1080p) ke aas-paas hai; Step 3 addendum me ek band tay ho

### R-281 — Climax par music ko −12 dB tak duck karo ⚙️ *(naya — editor round)*
- **Purana ID:** D1-020
- **Kab:** Kisi scene ka climax/action peak aaye
- **Kya:** Background music ko climax moments par −12 dB tak auto-duck karo, aur climax SFX (punch/impact) ko apni alag jagah (track) par rakho taaki wo music se na lade
- **Kyun:** Climax par music aur asar ek saath chillayein to dono marte hain; duck se pal ki taakat saaf uthti hai
- **Kitni baar:** Har climax/action peak par
- **Evidence:** 🟠 — Suite ka template number (note)
- **Sources:** `notes_mmmnhat_agent-skills.md (note)`
- **Check:** `{"kind": "db_range", "field": "music_climax_duck_db", "min": -12, "max": -12}`
- **Takraav note:** Purana ducking niyam (R-103) dialogue ke neeche 6–12 dB duck kehta hai — ye climax par −12 dB ki khaas hadd hai; sangat disha, alag mauqa — Step 3 addendum me dono ki jagah saaf ho

### R-285 — Anticipation ki bani-banai banawat (frames) *(naya — editor round)*
- **Purana ID:** D1-024
- **Kab:** Koi bada action animate ho (jump, launch, reveal)
- **Kya:** Timeline ko aise banao: 0–10 frames wind-up (crouch/pull back) → 10–12 frames transition → 12–30 frames main action → 30–40 frames settle. Wind-up ke keyframes par easy ease rakho
- **Kyun:** Bina taiyaari ke action achanak teleport lagta hai; wind-up aankh ko aane wale zor ke liye taiyaar karta hai
- **Kitni baar:** Har bade action par; chhote UI moves par anupaat se chhota
- **Evidence:** 🟠 — Disney parampara ki frame banawat (MIT skill sheet)
- **Sources:** `github_dylantarre_animation-principles.md`
- **Takraav note:** LobzyJay anticipation ko main action ka 20–30% kehta hai (D1-060) — ye 40-frame banawat me wind-up ~25% hi banta hai; sangat hai, paimana alag (absolute frames vs %) — Step 3 addendum me ek bhasha tay ho

### R-286 — Follow-through — child elements ko 2–5 frames peeche rakho ⚙️ *(naya — editor round)*
- **Purana ID:** D1-025
- **Kab:** Multi-part element (character, lockup, card system) rukta/move karta ho
- **Kya:** Child layers ke keyframes ko 2–5 frames offset rakho (ya ~0.05 s ka time-delay) taaki hisse ek saath na ruk kar ek ke baad ek settle hon
- **Kyun:** Sab kuchh ek hi frame par rukna nakli lagta hai; peeche chalte hisse wajan aur zindagi dete hain
- **Kitni baar:** Har multi-part motion par
- **Evidence:** 🟠 — Disney parampara (MIT skill sheet)
- **Sources:** `github_dylantarre_animation-principles.md`
- **Check:** `{"kind": "frame_range", "what": "follow_through_offset_frames", "min": 2, "max": 5}`
- **Takraav note:** Stagger wale merged rule (D1-044) se sambandhit hai — ye khaas taur par rukne/settle hone ki follow-through hai

### R-287 — Exaggeration — asal se 20–50% aage ⚙️ *(naya — editor round)*
- **Purana ID:** D1-026
- **Kab:** Character/brand animation me koi action padhne layak banana ho
- **Kya:** Values ko realistic se 20–50% aage badhao — bade scales, chaudi rotations, zyada dramatic timing
- **Kyun:** Camera/screen par asal jitna hi dikhana feeka padta hai; thoda badha hua hi saaf padhta hai
- **Kitni baar:** Character/brand motion par; product UI par nahi (wahan D1-052 dekho)
- **Evidence:** 🟠 — Disney parampara (MIT skill sheet)
- **Sources:** `github_dylantarre_animation-principles.md`
- **Check:** `{"kind": "percent_range", "what": "exaggeration_pct", "min": 20, "max": 50}`
- **Takraav note:** BADA TAKRAAV overshoot ki matra par: Maciejdziuba premium UI/product ke liye overshoot sirf 1.5–3% kehta hai (D1-052), LobzyJay follow-through ko move-distance ka 10–20% kehta hai (D1-061), aur LobzyJay ka pop example 110% (10% overshoot) hai — teen alag duniyayein (character animation / brand motion / premium UI); Step 3 addendum me context-wise faisla zaroori

### R-288 — Squash & stretch me volume constant rakho *(naya — editor round)*
- **Purana ID:** D1-027
- **Kab:** Koi object dabta/kheenchta (squash-stretch) ho
- **Kya:** Jab Y compress ho to X ko ulta expand karo — X × Y lagbhag constant rakho taaki object ka volume bana rahe
- **Kyun:** Bina volume-bachat ke deformation object ko phula hua ya pichka hua khilona bana deta hai
- **Kitni baar:** Har squash-stretch wale move par
- **Evidence:** 🟠 — Disney parampara (MIT skill sheet)
- **Sources:** `github_dylantarre_animation-principles.md`

### R-291 — Effect-heavy kaam alag rakho, intensity revise ho sake *(naya — editor round)*
- **Purana ID:** D1-030
- **Kab:** Koi bhaari effect/compositing lagana ho
- **Kya:** Effect-heavy kaam adjustment layers ya nests par rakho taaki uski intensity baad me revise ho sake; aur hamesha sabse chhota native tool chuno jo kaam kare
- **Kyun:** Clip par seedha chipka effect badalna mushkil hota hai; alag parat par rakha effect ek slider se kam-zyada ho sakta hai
- **Kitni baar:** Har bhaari effect par
- **Evidence:** 🟠 — Workflow discipline (MIT skill notes)
- **Sources:** `github_MuhammadAsad809_AI-EDITING-SKILL.md`

### R-292 — AE sirf zaroori shots ke liye — editorial structure ka badal nahi *(naya — editor round)*
- **Purana ID:** D1-031
- **Kab:** Koi shot After Effects me bhejna ho
- **Kya:** AE ko tracked graphics/compositing/typography ke liye rakho, editorial structure ke badle ke roop me nahi; sirf wahi shots bhejo jinhe zaroorat ho, handles bachakar bhejo, aur color management + motion blur wahan verify karo
- **Kyun:** Har shot ko AE me ghumana samay aur structure dono kharab karta hai; kataav (editing) NLE me hi rehta hai
- **Kitni baar:** Har AE round-trip par
- **Evidence:** 🟠 — Workflow discipline (MIT skill notes)
- **Sources:** `github_MuhammadAsad809_AI-EDITING-SKILL.md`

### R-296 — Punch-in alternating — har dusre cut par 100% ↔ 112% ⚙️ *(naya — editor round)*
- **Purana ID:** D1-035
- **Kab:** Talking-head/A-roll me jaan-boojh ki house style ke tor par punch-in lagana ho
- **Kya:** Har dusre cut par scale badlo: ek cut 100%, agla 112% — isi alternating lay me poora video
- **Kyun:** Regular lay wala punch-in style ki pehchan ban jata hai aur static frame me harkat deta hai
- **Kitni baar:** Har dusre cut par, poore video me consistent
- **Evidence:** 🟠 — Ek house ki Editing DNA (MIT skill)
- **Sources:** `github_vamshicreates_premiere-editing-dna.md`
- **Check:** `{"kind": "percent_range", "what": "punch_in_scale_pct", "min": 112, "max": 112}`
- **Takraav note:** SEEDHA TAKRAAV purane faisle se (ORDER #5): punch-in sirf motivated, ≤10/min, gaps ≥4 s. Ye house style bina-wajah har dusre cut par punch-in karta hai — Body ASL 2.8 s par har dusra cut ≈ 10–11 baar/min banta hai, yaani purani hadd ke bilkul kinare/par. Step 3 addendum me house-style apvaad tay ho

### R-298 — House mix offsets — SFX −9 dB, music bed −20 dB ⚙️ *(naya — editor round)*
- **Purana ID:** D1-037
- **Kab:** House style me final mix ke offsets tay karne hon
- **Kya:** Dialogue ko 0 dB reference rakho; SFX uske −9 dB par, music bed −20 dB par (dialogue ke neeche ducked)
- **Kyun:** Reference ke saapeksh offsets har video me ek jaisi awaaz ki pehchan banate hain
- **Kitni baar:** Poore mix me constant
- **Evidence:** 🟠 — House DNA numbers (MIT skill); dialogue ke relative naap hai
- **Sources:** `github_vamshicreates_premiere-editing-dna.md`
- **Check:** `{"kind": "db_range", "field": "music_bed_db_under_voice", "min": -20, "max": -20}`
- **Takraav note:** Music −20 dB purane relative band (18–25 dB neeche, ORDER #11) ke andar hai — takraav nahi. Lekin ADAM-0S ki absolute dBFS seedhi (D1-009) se naap ka aadhar alag hai — dono ko ek table me rakhna Step 3 addendum ka kaam

### R-300 — Timing ki hierarchy — ahem pehle, container pehle, focal aakhir me *(naya — editor round)*
- **Purana ID:** D1-039
- **Kab:** Koi lockup/scene kai elements ke saath animate ho
- **Kya:** Kram rakho: sabse ahem element (primary mark/logo) pehle ya 50 ms ki head-start ke saath aaye; container apne content se pehle move kare; baaki uske baad lay me aayein (jaise wordmark +80 ms, tagline uske +200 ms baad); sabse sajawati element sabse aakhir me aur sabse dheere land kare; focal element sabse aakhir ya sabse strong land kare
- **Kyun:** Jo pehle/strong land karta hai wahi aankh ka malik banta hai — hierarchy ka ulta matlab dhyaan ka ulta
- **Kitni baar:** Har multi-element entrance par
- **Evidence:** 🟠 — Do AE skills ke sangat craft numbers
- **Sources:** `github_justajazz_ae-mcp-bridge.md`, `github_LobzyJay_motion-design-with-claude.md`

### R-301 — Overshoot me poora object react kare *(naya — editor round)*
- **Purana ID:** D1-040
- **Kab:** Koi element overshoot ke saath land kare
- **Kya:** Overshoot sirf ek dimension (jaise height) par mat rakho — poori cheez react kare (width, scale, position sab saath), aur element apni momentum ko aage carry-through kare
- **Kyun:** Aadha react karta object rubber ka khilona lagta hai; poora react karta object wajan wala lagta hai
- **Kitni baar:** Har overshoot landing par
- **Evidence:** 🟠 — AE craft (MIT skill sheet)
- **Sources:** `github_justajazz_ae-mcp-bridge.md`
- **Takraav note:** Overshoot ki MATRA par takraav D1-052/D1-061/D1-026 me darj hai — ye rule sirf react karne ke DHANG ki baat karta hai

### R-302 — Ek object ki saari properties ek hi frame par finish hon *(naya — editor round)*
- **Purana ID:** D1-041
- **Kab:** Ek hi object ki kai properties (position/scale/opacity) animate hon
- **Kya:** Un sabko ek hi frame par khatm karo — sync me; aur saath aane wale text/group ko ek saath treat karo, tukdo me nahi
- **Kyun:** Alag-alag frame par rukti properties object ko bikhra hua aur animation ko adhura dikhati hain
- **Kitni baar:** Har multi-property animation par
- **Evidence:** 🟠 — AE craft (MIT skill sheet)
- **Sources:** `github_justajazz_ae-mcp-bridge.md`
- **Takraav note:** Follow-through (D1-025) iska ulta nahi hai — wahan alag-alag OBJECTS offset hote hain, yahan EK object ki properties sync hoti hain

### R-303 — Number counter ki ghadi — 0.3 s ruk, 1.2 s ginti *(naya — editor round)*
- **Purana ID:** D1-042
- **Kab:** Koi number/statistic animate hokar gina jaye
- **Kya:** Counter ko 0.3 s ki delay ke baad shuru karo aur 1.2 s me ease ke saath target value tak pahunchao
- **Kyun:** Turant shuru hua counter nazar se chook jata hai; bina ease ki ginti machine jaisi lagti hai
- **Kitni baar:** Har animated counter par
- **Evidence:** 🟠 — AE preset craft (MIT skill sheet)
- **Sources:** `github_justajazz_ae-mcp-bridge.md`

### R-304 — Motion blur — har moving layer par, shutter 180 default *(naya — editor round)*
- **Purana ID:** D1-043
- **Kab:** Koi layer/element move kare (AE/motion work)
- **Kya:** Motion blur har moving layer par ON rakho. Shutter angle ka default 180° (natural); crisp UI ke liye 90–120°, tez sweeps ke liye 200–300°; samples ~32. Blur ki matra velocity ke anupaat me rakho — jo element frame me sirf kuch pixels hi hilta hai us par blur OFF
- **Kyun:** Bina blur ke tez motion strobe karta hai; zyada blur chhoti harkat ko keechad bana deta hai
- **Kitni baar:** Har moving layer par; shutter context ke hisaab se
- **Evidence:** 🟠 — Do AE skills ke sangat craft numbers
- **Sources:** `github_justajazz_ae-mcp-bridge.md`, `github_Maciejdziuba_youtube-skills.md`

### R-308 — Transition me hard cut pehle, crossfade aakhir me *(naya — editor round)*
- **Purana ID:** D1-047
- **Kab:** Motion piece me scenes/beats ke beech transition chunna ho
- **Kya:** Hard cuts, matte wipes, shutters aur element-led transitions ko pehle chuno; crossfade ko default mat bano
- **Kyun:** Crossfade sabse kamzor aur sabse zyada istemal hone wala transition hai — nirnayak transition hi piece ko professional deta hai
- **Kitni baar:** Har transition par pehle nirnayak vikalp socho
- **Evidence:** 🟠 — Motion-direction craft (MIT skill)
- **Sources:** `github_SebastianBoehler_autoresearch_after_effects_finetune.md`

### R-309 — Ek piece, ek hi dominant visual grammar *(naya — editor round)*
- **Purana ID:** D1-048
- **Kab:** Motion piece ka visual system tay ho
- **Kya:** Poore piece me ek hi dominant visual grammar rakho (ek hi bhasha: type-led, ya shape-led, ya image-led); beech me dusri bhasha mat ghusao
- **Kyun:** Har scene nayi bhasha bole to piece bikhar jata hai; ek grammar hi pehchan aur aitbaar banati hai
- **Kitni baar:** Har piece par ek grammar
- **Evidence:** 🟠 — Motion-direction craft (MIT skill)
- **Sources:** `github_SebastianBoehler_autoresearch_after_effects_finetune.md`

### R-312 — Amateur lage to pehle element count ghatao *(naya — editor round)*
- **Purana ID:** D1-051
- **Kab:** Koi motion scene banana par bhi amateur/sasta lage
- **Kya:** Pehla ilaaj hamesha dikhne wale elements ki ginti ghatana hai; aur final lockup ko beech ke scenes se simple aur zyada confident rakho
- **Kyun:** Zyada elements = zyada shor; sadgi hi mehenga dikhne ka sabse sasta raaz hai
- **Kitni baar:** Har amateur lagne wale scene par, effects badhane se pehle
- **Evidence:** 🟠 — Motion-direction craft (MIT skill)
- **Sources:** `github_SebastianBoehler_autoresearch_after_effects_finetune.md`

### R-313 — Premium UI/product overshoot — sirf 1.5–3% ⚙️ *(naya — editor round)*
- **Purana ID:** D1-052
- **Kab:** Premium/product/UI motion me element land kare
- **Kya:** Overshoot ko sirf 1.5–3% rakho; damped settle ka namuna: 100 → 102 → 99.5 → 100 (frames 3/2/2 me)
- **Kyun:** Is duniya me zyada overshoot sasta padhta hai — premium ka matlab hai asar dikhe bina mehnat dikhe
- **Kitni baar:** Har premium UI/product landing par
- **Evidence:** 🟠 — Production-verified house craft (MIT skill repo, archived)
- **Sources:** `github_Maciejdziuba_youtube-skills.md`
- **Check:** `{"kind": "percent_range", "what": "overshoot_pct_premium", "min": 1.5, "max": 3}`
- **Takraav note:** BADA TEEN-TARAFA TAKRAAV: dylantarre character animation ke liye exaggeration +20–50% kehta hai (D1-026); LobzyJay brand motion ke liye follow-through overshoot move-distance ka 10–20% aur pop 110% kehta hai (D1-061/D1-065); ye 1.5–3% SIRF premium UI/product ke liye hai. Step 3 addendum me context-wise table zaroori: UI/product 1.5–3% / brand 10–20% / character 20–50%

### R-314 — Easing kabhi symmetric nahi — asymmetric influence hi premium hai *(naya — editor round)*
- **Purana ID:** D1-053
- **Kab:** Kisi bhi move ke keyframes par easing lagani ho
- **Kya:** Keyframe influence ko jaan-boojh ke asymmetric rakho: premium ease-out ke liye key1 out ~12 / key2 in ~84; weighted hero in-out 38/78; pass-through 20 / 54-54 / 88; floor impact par 0.5/0.5 (bilkul cushioning nahi); apex/hang par 90/90. Aam taur par entrance par pehle key ka out-influence kam aur dusre ka in-influence zyada (mazboot ease-out ~80, halka ~33) rakho. Default Easy Ease (~33) ya symmetric 50/50 ko aakhri haal mat samjho
- **Kyun:** Symmetric/default easing hi amateur ki sabse pehchanne layak nishani hai; asymmetric curve hi wajan aur maksad deti hai
- **Kitni baar:** Har keyframed move par
- **Evidence:** 🟠 — Do AE skills ke sangat craft numbers; asliyat me ye design ke faisle hain, naap nahi
- **Sources:** `github_Maciejdziuba_youtube-skills.md`, `github_LobzyJay_motion-design-with-claude.md`, `github_Mfrostbutter_claude-skills.md`
- **Takraav note:** LobzyJay ki chetaavni: easing ke numbers koi jaadu nahi — galat maksad par sahi number bhi bekaar hai; pehle faisla (entrance hai ya exit, halka hai ya bhaari), phir number

### R-317 — Shadow ki teen paratein — kabhi pure black nahi *(naya — editor round)*
- **Purana ID:** D1-056
- **Kab:** Kisi element ko realistic shadow deni ho
- **Kya:** Shadow ko teen blurred copies se banao: contact (blur ~9, opacity ~21%), occlusion (blur ~22, opacity ~11%), ambient (blur ~64, opacity ~5%). Blur radius offset ka 2–3 guna rakho; vertical squash 30–40% rakho; shadow ka rang kabhi pure black nahi — halka cool dark violet/neutral rakho
- **Kyun:** Ek hi hard shadow nakli lagti hai; teen naram paratein aur rang-daar andhera hi asal roshni jaisa padhta hai
- **Kitni baar:** Har realistic shadow par
- **Evidence:** 🟠 — Production house ke look parameters (MIT skill repo, archived)
- **Sources:** `github_Maciejdziuba_youtube-skills.md`

### R-319 — Glow/bloom ka hisaab — stack aur frame ka hissa ⚙️ *(naya — editor round)*
- **Purana ID:** D1-058
- **Kab:** Kisi element ko glow/bloom dena ho
- **Kya:** Glow ko blurred copies ke stack se banao (jaise blur 4px/42%, 22px/17%, 92px/6% — radius dugna to opacity aadhi); bloom ko frame ke sirf 5–20% hisse tak rakho; glass/translucent cheezon par glow ke liye Screen mode rakho, Add nahi
- **Kyun:** Poora frame chamke to kuchh nahi chamakta; seemit bloom hi mehnga aur jaan-boojh ka lagta hai
- **Kitni baar:** Har glow ke istemal par
- **Evidence:** 🟠 — Production house ke look parameters (MIT skill repo, archived)
- **Sources:** `github_Maciejdziuba_youtube-skills.md`
- **Check:** `{"kind": "percent_range", "what": "bloom_frame_coverage_pct", "min": 5, "max": 20}`

### R-321 — Anticipation — main action ka 20–30% ⚙️ *(naya — editor round)*
- **Purana ID:** D1-060
- **Kab:** Koi badi harkat (move/launch/jump) animate ho
- **Kya:** Anticipation ko main action ki duration ka 20–30% rakho (jaise 400 ms ke move se pehle 80–120 ms ki taiyaari); uski matra chhoti rakho — ~300 px ke move se pehle ulta disha me sirf ~15–25 px ka kheenchav
- **Kyun:** Bina taiyaari ki harkat teleport lagti hai; zyada taiyaari use sust bana deti hai
- **Kitni baar:** Har badi harkat se pehle
- **Evidence:** 🟠 — AE craft (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`
- **Check:** `{"kind": "percent_range", "what": "anticipation_vs_action_pct", "min": 20, "max": 30}`
- **Takraav note:** dylantarre ki frame-banawat (D1-024) me wind-up ~40-frame action ka ~25% banta hai — sangat; paimana alag hai (absolute frames vs pratishat)

### R-322 — Follow-through overshoot — move-distance ka 10–20% ⚙️ *(naya — editor round)*
- **Purana ID:** D1-061
- **Kab:** Brand motion me element apni jagah par land kare
- **Kya:** Landing par element ko target se aage move-distance ka 10–20% tak overshoot karao, phir use main duration ke 20–40% samay me settle karo; overshoot wala keyframe target ke 3–5 frames aage rakho; secondary elements ke aakhri keyframes primary ke 3–6 frames baad land hon
- **Kyun:** Thoda sa aage nikal kar wapas aana hi harkat ko zinda aur wajan-daar banata hai
- **Kitni baar:** Har badi landing par
- **Evidence:** 🟠 — AE craft (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`
- **Check:** `{"kind": "percent_range", "what": "follow_through_overshoot_pct_of_distance", "min": 10, "max": 20}`
- **Takraav note:** Overshoot ke teen-taraffa takraav ka hissa (D1-052 me poora varnan): ye 10–20% brand motion ke liye hai; premium UI 1.5–3%, character exaggeration 20–50% — Step 3 addendum me context table bane

### R-323 — Inertial bounce ke tuned defaults *(naya — editor round)*
- **Purana ID:** D1-062
- **Kab:** Landing ke baad element ko natural bounce/settle dena ho
- **Kya:** Damped oscillation ke defaults se shuru karo: amp 0.04–0.12 (default ~0.08), freq 2.0–4.0 (default ~2.0–2.5), decay 4–8 (UI) / 2–4 (naram material) / default ~5; bounce ka asar pehle 1 s ke andar hi khatm ho jana chahiye (t < 1 s)
- **Kyun:** Andaz se lagaya bounce ya to hilta hi nahi ya jelly ban jata hai; ye defaults production me ghise hue hain
- **Kitni baar:** Har bounce/settle par starting point
- **Evidence:** 🟠 — Teen AE sources ke sangat parameter sets ka merged band
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`, `github_iart-ai_motion-design-skills.md`, `github_chvndler_aeft.jsx.md`

### R-325 — Midpoint check — transition ka beech wala frame bhi design ho *(naya — editor round)*
- **Purana ID:** D1-064
- **Kab:** Koi bhi transition bane
- **Kya:** Transition ke 50% wale frame ko alag se dekho — wo kisi jaan-boojh ke design state jaisa lagna chahiye, do states ke beech ka dhundhla saump nahi
- **Kyun:** Darshak beech ke frame ko bhi dekhta hai; bekaar midpoint poori transition ko sasta kar deta hai
- **Kitni baar:** Har transition par ek baar check
- **Evidence:** 🟠 — AE craft (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`

### R-326 — Pop ka snap — 0 se 110%, phir 100% ⚙️ *(naya — editor round)*
- **Purana ID:** D1-065
- **Kab:** Kisi element ko pop ke saath land karana ho
- **Kya:** Scale ko 0 se shuru karke 0.25 s par 110% tak le jao, phir 0.4 s par 100% par settle karo
- **Kyun:** Thoda sa overshoot karke rukna hi pop ko padhne layak aur mazedaar banata hai
- **Kitni baar:** Har pop-style landing par
- **Evidence:** 🟠 — AE craft ka kaam kiya hua udaharan (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`
- **Check:** `{"kind": "duration_range_s", "what": "pop_total", "min": 0.4, "max": 0.4}`
- **Takraav note:** Iska 10% overshoot Maciejdziuba ke premium band (1.5–3%, D1-052) se takraata hai — ye brand/marketing pop ke liye hai, premium UI ke liye nahi; context table Step 3 addendum me

### R-327 — Exit ka raasta = entry ka ulta raasta *(naya — editor round)*
- **Purana ID:** D1-066
- **Kab:** Koi element jis raaste se aaya tha usi se wapas jaye
- **Kya:** Exit path ko entry path ka ulta rakho — jo neeche se aaya wo neeche hi jaye; alag raaste se gayab hona teleport jaisa lagta hai
- **Kyun:** Aankh cheez ko usi raaste par dhoondhti hai jahan se wo aayi thi; raasta badalna = cheez ka badal jana
- **Kitni baar:** Har exit par jahan entry bhi dikhi ho
- **Evidence:** 🟠 — AE craft (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`

### R-328 — Zoom aur pan ek saath kabhi nahi *(naya — editor round)*
- **Purana ID:** D1-067
- **Kab:** Camera jaisi harkat (scale + position) design ho
- **Kya:** Ek hi harkat me zoom aur pan dono mat chalao — pehle ek, phir dusra
- **Kyun:** Dono saath chalein to frame behka hua aur sasta lagta hai; aankh kisi ek ko bhi follow nahi kar pati
- **Kitni baar:** Har camera-style move par
- **Evidence:** 🟠 — AE craft (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`

### R-329 — Camera move ki matra — push-in 2–6%, drift seemit ⚙️ *(naya — editor round)*
- **Purana ID:** D1-068
- **Kab:** Koi camera jaisi harkat (push/drift/rotation) design ho
- **Kya:** Matra seemit rakho: push-in 1–1.5 s me kul 2–6% zoom; lateral drift 1–2 s me 20–80 px; rotation 0.5–2° (jaan-boojh ke reveal par hi 3–5°); product shots ke liye lambi focal length jaisa ehsaas (70–120 mm ke barabar)
- **Kyun:** Camera ki harkat mehsoos honi chahiye, dikhni nahi — zyada matra hi use sasta bana deti hai
- **Kitni baar:** Har camera move par
- **Evidence:** 🟠 — Production house ke camera numbers (MIT skill repo, archived)
- **Sources:** `github_Maciejdziuba_youtube-skills.md`
- **Check:** `{"kind": "percent_range", "what": "push_in_pct", "min": 2, "max": 6}`

### R-330 — Camera hamesha subject se dheema — 1.5–2.5 guna lambi ghadi *(naya — editor round)*
- **Purana ID:** D1-069
- **Kab:** Subject aur camera dono move karein
- **Kya:** Camera ki movement ki duration object ki duration ki 1.5–2.5 guna rakho; ek section me ek hi jaan-boojh ka camera idea rakho (push, ya track, ya orbit, ya parallax — sab nahi); bina maksad ka perpetual drift kabhi nahi
- **Kyun:** Tez camera harkat ko kha jata hai; dheema camera use wajan deta hai aur bhatkav mita deta hai
- **Kitni baar:** Har camera + subject wale scene par
- **Evidence:** 🟠 — Production house craft (MIT skill repo, archived)
- **Sources:** `github_Maciejdziuba_youtube-skills.md`

### R-331 — Finish ki parat — halka grain, near-black background ⚙️ *(naya — editor round)*
- **Purana ID:** D1-070
- **Kab:** Motion piece ka final polish/render ho
- **Kya:** Project ko 16 bpc par rakho (32 bpc nahi — koi fayda nahi, sirf bojh); adjustment layer par 1.5–2% mono noise grain lagao (banding chhupta hai, premium texture aata hai); backgrounds ko near-black rakho, pure black (0,0,0) kabhi nahi
- **Kyun:** Banding aur khaali kaala rang hi do sabse aam 'sasta' nishaan hain; grain aur near-black dono ko ek saath sambhalte hain
- **Kitni baar:** Har final render se pehle
- **Evidence:** 🟠 — Production house craft (MIT skill repo, archived)
- **Sources:** `github_Maciejdziuba_youtube-skills.md`
- **Check:** `{"kind": "percent_range", "what": "grain_noise_pct", "min": 1.5, "max": 2}`

### R-332 — Accent pop ki ghadi — chamak 0.13 s me peak *(naya — editor round)*
- **Purana ID:** D1-071
- **Kab:** Chhota accent (sparkle/glint/star) pop karna ho
- **Kya:** Pop ki ghadi rakho: scale 0 se shuru, lagbhag +0.13 s par peak (~135%) par, +0.50 s tak wapas 0; opacity flash +0.07 s tak 100 par aur +0.45 s tak khatm
- **Kyun:** Accent ka kaam ek pal ki chamak hai — dheema pop dhyaan kheench kar bojh ban jata hai
- **Kitni baar:** Har chhote accent pop par
- **Evidence:** 🟠 — Preset craft ke kaam kiye hue numbers (MIT skill pack)
- **Sources:** `github_Mfrostbutter_claude-skills.md`

### R-334 — Generated SFX ko pehle normalize karo — I=−16 LUFS ⚙️ *(naya — editor round)*
- **Purana ID:** D1-073
- **Kab:** AI/generated SFX ko edit me milana ho
- **Kya:** Generated SFX samples ko pehle loudnorm I=−16 LUFS : TP=−1.5 dB : LRA=11 par laakar phir pipeline me milao
- **Kyun:** Bina normalize kiye generated awaazein har baar alag zor par aati hain aur mix bikhar jata hai
- **Kitni baar:** Har generated SFX asset par, milane se pehle
- **Evidence:** 🟠 — Skill pack ka asset-prep number (MIT)
- **Sources:** `github_Mfrostbutter_claude-skills.md`
- **Check:** `{"kind": "lufs_target", "value": -16, "tolerance": 1}`
- **Takraav note:** Ye ASSET-level normalization hai, final master ka loudness target nahi — purana master target −14 LUFS (YouTube) isse alag cheez hai; Step 3 addendum me asset vs master ka farak saaf likha jaye

### R-335 — Wiggle hamesha maksad ke saath *(naya — editor round)*
- **Purana ID:** D1-074
- **Kab:** Kisi layer par wiggle/ambient harkat lagani ho
- **Kya:** Wiggle ko maksad ke hisaab se chuno: ambient drift ke liye wiggle(0.5, 8), mechanical jitter ke liye wiggle(24, 2); bina-socha wiggle(5, 20) jaisa raw wiggle mat lagao — wo harkat nahi, shor hai
- **Kyun:** Har harkat ka matlab hona chahiye; matlab-rahit harkat frame ko sasta aur bechain karti hai
- **Kitni baar:** Har wiggle ke istemal par
- **Evidence:** 🟠 — AE craft (MIT skill)
- **Sources:** `github_LobzyJay_motion-design-with-claude.md`

### R-340 — Misdirection — cut ko harkat ya awaaz ke dhakke peeche chhupao *(naya — editor round)*
- **Purana ID:** D1-079
- **Kab:** Koi cut zyada dikh raha ho
- **Kya:** Cut point par achanak harkat ya sound spike (darwaza band, taali jaisi tez awaaz) rakho — darshak ka dhyaan wahan jayega aur cut ghayab ho jayega
- **Kyun:** Aankh aur kaan hamesha sabse tez nayi cheez ke peeche bhagte hain — usi pal me seam ghul jati hai
- **Kitni baar:** Har dikhne wale cut par
- **Evidence:** 🟠 — Film-editing craft (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`
- **Takraav note:** ADAM-0S ke invisible-cut upaayo (D1-003) se sambandhit — ye sirf cut-point wale dhakke ki baat karta hai

### R-343 — Stabilize sirf outliers ko — blanket kabhi nahi *(naya — editor round)*
- **Purana ID:** D1-082
- **Kab:** Handheld footage ko stabilize karna ho
- **Kya:** Sirf un shots ko stabilize karo jo baakio ke muqable me zyada hilte hain (relative outliers); poori film par blanket stabilization kabhi mat chalao
- **Kyun:** Zyada safai jaan-boojh ki handheld urja ko maar deti hai — documentary ka sach hi us harkat me hai
- **Kitni baar:** Har stabilization faisle par
- **Evidence:** 🟠 — Film-editing pipeline craft (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`

### R-345 — End card fade ke baad, black par *(naya — editor round)*
- **Purana ID:** D1-084
- **Kab:** End card/title lagana ho
- **Kya:** End card ko fade ke BAAD, black ke upar rakho — aakhri frame ke upar title chipkana galat hai
- **Kyun:** Aakhri frame par chipka title dono ko kharab karta hai; black par saaf card hi khatma deta hai
- **Kitni baar:** Har end card par
- **Evidence:** 🟠 — Film-editing pipeline craft (MIT skill)
- **Sources:** `github_koptsev63_premiere-claude-bridge.md`

### R-355 — Spring presets — mood ke hisaab se spring chuno *(naya — editor round)*
- **Purana ID:** D1-094
- **Kab:** Spring-based motion ka ehsaas tay karna ho
- **Kya:** Mood se spring chuno: gentle/soft = stiffness 80, damping 20 (koi overshoot nahi); default = 100/10 (halka overshoot); wobbly/playful = 150/8 (zyada overshoot); stiff/snappy = 200/20; slow/heavy = mass 3 ke saath 100/15; visual bounce chahiye to 200/5; tez UI feedback = mass 0.5 ke saath 300/20
- **Kyun:** Spring ke numbers hi ehsaas hain — ek hi spring har mood par chalana sab ko ek jaisa bana deta hai
- **Kitni baar:** Har spring animation par mood ke hisaab se ek preset
- **Evidence:** 🟠 — Motion guide ke physics presets (MIT skill)
- **Sources:** `github_ishu86_after-effects-mcp.md`
- **Takraav note:** Inertial bounce wale defaults (D1-062) se sambandhit hai — wahan damped oscillation AE expressions me hai, yahan spring physics ke presets hain; takraav nahi

### R-356 — Parallax ki gehrai — 0.2 / 0.5 / 1.0 *(naya — editor round)*
- **Purana ID:** D1-095
- **Kab:** Parallax/depth wala scene bane
- **Kya:** Ek hi controller ko animate karo aur layers ko uske ansh (fraction) do: door ka background 0.2, midground 0.5, foreground 1.0
- **Kyun:** Har layer ko alag se animate karna bikharav hai; ek controller ke fractions se gehrai khud-ba-khud sahi banti hai
- **Kitni baar:** Har parallax scene par
- **Evidence:** 🟠 — Motion guide craft (MIT skill)
- **Sources:** `github_ishu86_after-effects-mcp.md`

### R-357 — Aakhri frame murda na baithe — slow push-in rakho *(naya — editor round)*
- **Purana ID:** D1-096
- **Kab:** Koi reveal/logo animation apne end frame par ruke
- **Kya:** End frame par halka slow push-in rakho taaki final frame zinda lage, murda still na lage
- **Kyun:** Bilkul ruka hua aakhri frame video ko khatm nahi, atak gaya mehsoos karata hai
- **Kitni baar:** Har reveal ke end frame par
- **Evidence:** 🟠 — Motion guide craft (MIT skill)
- **Sources:** `github_ishu86_after-effects-mcp.md`
- **Takraav note:** Maciejdziuba ke perpetual-drift mana karne (D1-069) se halka tanav hai — ye sirf END frame par halka push-in hai, poore scene ka drift nahi

### R-422 — Transition mix ka budget (travel/POV) ⚙️ *(naya — editor round)*
- **Purana ID:** D2-065
- **Kab:** Poore film ke transition mix ki yojna/review par
- **Kya:** Mix rakho: clean cut / action match / direction match / hidden cut = 55–70%; physical bridge ya short dissolve = 15–30%; motion accent = zyada se zyada 18%, kabhi do adjacent nahi, ek family ko dohrane se pehle kam se kam 5 stable boundaries
- **Kyun:** Ek hi effect ki 77% repetition (reference film ki asli kamzori) poore film ko template bana deti hai
- **Kitni baar:** Motion accent ≤18%; adjacent = 0; family repeat gap ≥5 boundaries
- **Evidence:** 🟡 — Reference film ke map par 27/35 boundaries ek hi transition the — usi kamzori ke ulta banaya house budget; percentages house hain, kamzori measured hai
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "percent_range", "max_pct": 18, "what": "motion accent transitions ka hissa"}`

### R-423 — Motion accent ki 4 shartein, warna downgrade ⚙️ *(naya — editor round)*
- **Purana ID:** D2-066
- **Kab:** Koi motion transition (whip/zoom/slice type) lagane se pehle
- **Kya:** Accent tabhi jab: dono taraf real movement ho, route-phase ki wajah ho, BGM hit saath ho, aur kam se kam 0.8s ki stable landing footage ho. Ek bhi shart kamzor ho to clean match cut ya dissolve par downgrade karo. Accent ko hero title, subtitle collision ya voice-leak ke upar kabhi mat rakho
- **Kyun:** Bina zameen ke accent girta hai — viewer ko effect nahi, jhatka dikhta hai
- **Kitni baar:** 4/4 shartein; landing ≥0.8s stable
- **Evidence:** 🟠 — Homeward transition policy
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "duration_range_s", "min_s": 0.8, "what": "motion accent ke baad stable landing"}`

### R-424 — Hard-reject transitions ki list *(naya — editor round)*
- **Purana ID:** D2-067
- **Kab:** Transition chunne ke har pal
- **Kya:** Ye kabhi nahi: bina story-purpose ke random spin, flash, glitch, shake ya template transition; route jump ko sirf title card se dhakna; do static shots ke beech whip. Spin/zoom/flash/slice ko do kamzor unrelated shots chhupane ke liye kabhi nahi
- **Kyun:** Chhupane wala effect sabse pehle pakda jata hai
- **Kitni baar:** Reject list = 0 exceptions
- **Evidence:** 🟠 — Transition grammar ke hard rejections
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-425 — Pair grammar: har jodi ka apna transition *(naya — editor round)*
- **Purana ID:** D2-068
- **Kab:** Har adjacent clip-pair ke liye transition tay karte waqt
- **Kya:** Pair ke hisaab se chuno: action continuity = straight cut; shape/direction/water/road/window/skyline ka mel = match cut; time/weather/day-night/aftertaste = short dissolve; whip/rotation sirf jab dono taraf route-motion energy ho (rotation durlabh); speed-ramp sirf real movement par. Agar pair ke paas physical bridge evidence nahi hai to faisla 'pehle bridge insert karo' hai — effect-ready nahi
- **Kyun:** Har jodi ki fiziks alag hai; ek formula sab par lagana hi template-bazi hai
- **Kitni baar:** Har pair = 1 grammar-based faisla + fallback
- **Evidence:** 🟠 — Transition grammar engine
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-426 — Cadence: sajawati runs 4 se kam, koi style raja nahi ⚙️ *(naya — editor round)*
- **Purana ID:** D2-069
- **Kab:** Poore film ki transition cadence dekhte waqt
- **Kya:** Decorative transitions ki lagatar runs 4 se kam rakho; koi ek transition style poore film par dominate na kare
- **Kyun:** Ek style ka raaj = dekhne wale ko pattern dikhne lagta hai, kahani nahi
- **Kitni baar:** Decorative run <4; dominance = kisi ek style ka varchasva nahi
- **Evidence:** 🟠 — Transition cadence/motif niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "count_range", "max": 3, "what": "lagatar decorative transitions ki run"}`

### R-427 — Effects ki haden (CapCut director) ⚙️ *(naya — editor round)*
- **Purana ID:** D2-070
- **Kab:** Kisi bhi social edit me effects lagate waqt
- **Kya:** Haden: transitions zyada se zyada 2 per 10s; video effects 2 per 5s; zooms 1 per 5s; caption changes 1 per 3s; screen par ek saath stickers zyada se zyada 2
- **Kyun:** Had bina ke effects ek dusre ko kha jate hain — asar sab ka, yaad koi nahi
- **Kitni baar:** 2 transitions/10s; 2 effects/5s; 1 zoom/5s; 1 caption change/3s; ≤2 stickers
- **Evidence:** 🟠 — CapCut director ke maximum effect limits
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "max_per_min", "value": 12, "what": "transitions (2 per 10s)"}`

### R-428 — Emphasis zoom: 105–110%, 6–15 frames, ease-out ⚙️ *(naya — editor round)*
- **Purana ID:** D2-071
- **Kab:** Speaker kisi baat par zor de to
- **Kya:** Zoom 105–110% tak rakho, duration 6–15 frames, easing ease-out. Zoom hamesha bolne wale ke stress point par lage
- **Kyun:** Chhota, tez-nikalne wala zoom aankh ko 'sunno!' kehta hai; bada dheema zoom natak ban jata hai
- **Kitni baar:** 105–110%; 6–15 frames; ease-out
- **Evidence:** 🟠 — CapCut director ke zoom niyam (hook examples me 108–110% bhi aaya hai)
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "percent_range", "min_pct": 105, "max_pct": 110, "what": "emphasis zoom scale"}`

### R-429 — Ek video, zyada se zyada 2 visual styles ⚙️ *(naya — editor round)*
- **Purana ID:** D2-072
- **Kab:** Style tay karte waqt aur poore edit ke dauran
- **Kya:** Ek video me 2 se zyada visual styles mix mat karo. Transition ek hi family se rakho. Filter/color grade poori film me consistent rakho
- **Kyun:** Har scene alag duniya lage to film bikhar jati hai
- **Kitni baar:** ≤2 styles; 1 transition family; 1 grade
- **Evidence:** 🟠 — Style consistency niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "count_range", "max": 2, "what": "visual styles per video"}`

### R-430 — Cuts > transitions; har cut ka rationale *(naya — editor round)*
- **Purana ID:** D2-073
- **Kab:** Har edit decision par
- **Kya:** Clean editing ko effects par tarjeeh do — cut invisible hota hai, transition dhyaan kheenchta hai. Har hard cut ke paas rationale ho: nayi beat, angle change, gesture, B-roll, title card ya stylistic hit. Har effect ko apni jagah kamani hogi
- **Kyun:** 'Bas aise hi' wala cut viewer ko turant mehsoos hota hai
- **Kitni baar:** Rationale-less cuts/effects = 0
- **Evidence:** 🟠 — Do sources ka sangam: director philosophy + production standard
- **Sources:** `github_tashisleepy_capcut-ai-director.md`, `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-431 — Dikhne wala jump cut dhako; talking-head par video crossfade nahi *(naya — editor round)*
- **Purana ID:** D2-074
- **Kab:** Same camera + same crop ke dono taraf jump cut dikhe to
- **Kya:** Use B-roll, punch-in ya dissolve se dhako. Talking-head video par crossfade kabhi nahi (ghosting hota hai) — picture par hard cut, aur audio par crossfade / J-cut / L-cut ka naram-pan do
- **Kyun:** Ghosting sabse sasta lagta hai; awaaz ka naram-pan cut ko chhupa deta hai
- **Kitni baar:** Video crossfade on talking head = 0
- **Evidence:** 🟠 — Production standard se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-432 — B-roll grammar: wide → medium → close-up; hold 1.2–3.0s ⚙️ *(naya — editor round)*
- **Purana ID:** D2-075
- **Kab:** B-roll sequence banate waqt
- **Kya:** Sequence grammar rakho: wide → medium → close-up. Har B-roll shot 1.2–3.0s hold karo (mobile par padhne layak). Cutaway complete semantic beat par rakho — phrase land hone ke baad, saans par, ya naye idea par
- **Kyun:** Chhota B-roll jhalak hai, bada B-roll rukawat; kram bina sequence random hai
- **Kitni baar:** Hold 1.2–3.0s
- **Evidence:** 🟠 — Production standard se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "duration_range_s", "min_s": 1.2, "max_s": 3.0, "what": "B-roll hold"}`

### R-433 — Punch-in graphics/captions se pehle *(naya — editor round)*
- **Purana ID:** D2-076
- **Kab:** Punch-in zoom aur graphics dono ek hi edit me hon to
- **Kya:** Punch-ins graphics/captions compositing se PEHLE lagao — warna text bhi zoom ke saath hilta hai
- **Kyun:** Kram ulta ho to saaf dikhne wala technical nishan reh jata hai
- **Kitni baar:** Kram fixed: punch-in → graphics/captions
- **Evidence:** 🟠 — Production standard se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-434 — Title reveal shant rakho *(naya — editor round)*
- **Purana ID:** D2-077
- **Kab:** Title/place-card reveals par
- **Kya:** Reveal sirf: short fade, tiny scale settle, ya gentle dissolve. Glitch, random spin, flash, shake, particle, logo-reveal ya generic template-pack effects reject karo. Route transitions understated rakho — map line, ambient street insert, station/vehicle movement, ya colour/motion match cut
- **Kyun:** Shor machane wala title saste pack ki pehchan hai
- **Kitni baar:** Allowed reveals = 3 qismein hi
- **Evidence:** 🟠 — Effect-motion plan ke niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-435 — Ending ka ilaaj: music-tail fade, thehra hua aakhir *(naya — editor round)*
- **Purana ID:** D2-078
- **Kab:** Video ke aakhiri seconds me
- **Kya:** Ending par music-tail fade aur scenic breathing room do; slow zoom-out + fade (~15 frames) se band karo. Abrupt end kabhi nahi
- **Kyun:** Achanak khatam hua video adhoora lagta hai, khatam hua nahi
- **Kitni baar:** Outro fade ~15 frames; abrupt end = 0
- **Evidence:** 🟠 — Do sources: travel effect plan + CapCut director ending niyam
- **Sources:** `github_junwen853_travel-video-studio-skill.md`, `github_tashisleepy_capcut-ai-director.md`

### R-436 — Ek hi hero title, asli footage par, 6–12s ke andar ⚙️ *(naya — editor round)*
- **Purana ID:** D2-079
- **Kab:** Opening title lagate waqt
- **Kya:** Sirf EK saaf hero title, high-recognition asli footage ke upar, pehle 6–12 second ke andar. Dusra title, date, route/debug text ya ghosted duplicate kabhi nahi. Title ko kam se kam 1.2s tak bina competing viewer-text ke rehne do
- **Kyun:** Do title = koi title nahi; khaali card par title = footage par bharosa nahi
- **Kitni baar:** Titles = 1; window 6–12s; clean hold ≥1.2s
- **Evidence:** 🟠 — Opening + homeward title contracts
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "duration_range_s", "min_s": 1.2, "what": "hero title ka clean (bina competing text) hold"}`

### R-437 — Cover/hero-title formula: 1–5 shabd, pehchan wali background ⚙️ *(naya — editor round)*
- **Purana ID:** D2-080
- **Kab:** Cover/hero title design karte waqt
- **Kya:** High-recognition scenic background + oversized destination title (1–5 shabd) + neeche chhota designed subtitle + high-contrast (yellow/orange/white) type. Route/date/project clutter kabhi nahi
- **Kyun:** Cover ka kaam ek nazar me jagah bechna hai, itinerary batana nahi
- **Kitni baar:** Title 1–5 shabd
- **Evidence:** 🟠 — Ek reference channel (Parallel World) ke cover formula se
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "count_range", "min": 1, "max": 5, "what": "cover title ke shabd"}`
- **Takraav note:** TAKRAAV: purana thumbnail niyam target ≤3 shabd, hard cap 4 kehta hai. Ye source 1–5 shabd deta hai. Cover (video hero title) aur thumbnail ko alag maanna sulah ho sakti hai; merge par user/engine faisla kare.

### R-438 — Dialogue chain ka kram: EQ → de-hum → gate → NR → level → duck *(naya — editor round)*
- **Purana ID:** D2-081
- **Kab:** Dialogue/podcast audio saaf karte waqt
- **Kya:** Chain is kram me chalao: EQ → de-hummer → gate → noise reduction → level → ducking. Frequency ki problems dynamics se pehle; noise reduction destructive hai isliye der se. Manual NR ka dry/wet default 80% rakho. Hot external mic (0 dBFS ke paas) ho to use source rakho aur processed duplicate conservative limiting ke saath banao
- **Kyun:** Galat kram me har step pichhle step ki galti ko bada karta hai
- **Kitni baar:** 6 steps, yahi kram; NR dry/wet ≈80%
- **Evidence:** 🟠 — Resolve audio-cleanup (podcast) workflow
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-439 — Dialogue EQ/de-hum/gate ke starting numbers ⚙️ *(naya — editor round)*
- **Purana ID:** D2-082
- **Kab:** Dialogue cleanup ki shuruaat par
- **Kya:** Har dialogue clip par 80 Hz se neeche kaato (shelf jo 80–100 Hz tak −70 dB chhoo jaye). De-hummer 50/60 Hz par, amount −20 se −30 dB. Gate ke starting values: threshold −35 dB, range −18 dB, attack 1.4 ms, hold 0, release 93 ms — gate sirf sentences ke beech kaam kare
- **Kyun:** Neeche ka shor (rumble/hum) har dialogue ki saafai kha jata hai; ye numbers surakshit shuruaat hain
- **Kitni baar:** HPF <80 Hz; de-hum −20..−30 dB; gate −35/−18 dB, 1.4 ms / 93 ms
- **Evidence:** 🟠 — Usi cleanup workflow ke diye starting values
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "db_range", "min_db": -30, "max_db": -20, "what": "de-hum amount"}`

### R-440 — Ducker: shuruaat 2.7 dB, 5 dB se zyada = amateur ⚙️ *(naya — editor round)*
- **Purana ID:** D2-083
- **Kab:** Music ko voice ke neeche duck karte waqt (dialogue chain)
- **Kya:** Ducker 2.7 dB se shuru karo. 5 dB se zyada ducking amateurish lagti hai — audience ko dip sunai dene lagta hai
- **Kyun:** Ducking mehsoos nahi honi chahiye, sirf voice saaf honi chahiye
- **Kitni baar:** Start 2.7 dB; hard had 5 dB
- **Evidence:** 🟠 — Podcast cleanup workflow
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "db_range", "max_db": 5, "what": "ducker depth (dialogue chain)"}`
- **Takraav note:** TAKRAAV: purana ORDER default 'music voice se 18–25 dB neeche' bed-LEVEL ki baat hai; ye 2.7 dB DUCKER ki depth hai (kitna ghatao) — donon alag map hain, takraav asal me map ka hai. Lekin isi cluster ka KF-07 duck −12 dB (D2 style rule 'Narration duck landmarks') is 2.7–5 dB se sach me takrata hai — context farq: ye podcast dialogue-chain ka ducker hai, woh CapCut music-bed duck hai. Merge par profile-wise chuna jaye.

### R-441 — Podcast loudness verify: −16..−20 LUFS, peaks −9..−3 dBFS ⚙️ *(naya — editor round)*
- **Purana ID:** D2-084
- **Kab:** Podcast/dialogue delivery se pehle verify karte waqt
- **Kya:** Integrated loudness −16 se −20 LUFS ke beech rakho; voice peaks −9 se −3 dBFS; clip kabhi nahi
- **Kyun:** Podcast sunne wala lamba sunta hai — thakane wali loudness ya clipping turant chhod deta hai
- **Kitni baar:** −16..−20 LUFS; peaks −9..−3 dBFS; clips = 0
- **Evidence:** 🟠 — Podcast verification checklist
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "lufs_target", "min_lufs": -20, "max_lufs": -16, "profile": "podcast dialogue"}`
- **Takraav note:** Note: purana podcast profile −16 LUFS deta hai. Ye range −16..−20 hai — dialogue-only podcast ke liye neeche tak ijazat deta hai. Takraav halka; profile me range likh kar sulajh sakta hai.

### R-442 — Short-form dialogue: −14..−16 LUFS, true peak <−1 dBTP ⚙️ *(naya — editor round)*
- **Purana ID:** D2-085
- **Kab:** Talking-head short-form ke final mix par
- **Kya:** Dialogue target −14 se −16 LUFS integrated rakho; true peak −1 dBTP se neeche. Music hamesha ducked/conservative — fixed loud bed kabhi nahi; dialogue edits par 2–4 frame constant-power audio fades rakho
- **Kyun:** Platform normalization is range ko inaam deta hai; zyada loud = neeche daba diya jayega
- **Kitni baar:** −14..−16 LUFS; TP <−1 dBTP
- **Evidence:** 🟠 — Social-editor ke audio targets (usi source ke QA gate me Reels −15..−13 LUFS bhi aaya hai — range overlap hai, platform profile se final ho)
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "lufs_target", "min_lufs": -16, "max_lufs": -14, "profile": "talking-head short-form"}`

### R-443 — Narration duck landmarks: −12 dB, 10f/15f fades *(naya — editor round)*
- **Purana ID:** D2-086
- **Kab:** Narration ke aane-jaane par music automation me
- **Kya:** Narration shuru ho to music −12 dB tak duck karo (~10 frame fade me); narration khatam ho to 0 dB par wapas lao (~15 frame fade me). Documentary me music hamesha speech ke neeche −12 dB. End card par music 2s me −inf tak fade karo
- **Kyun:** Achanak ghata-badha music dhyaan khinchta hai; landmark fades use invisible karte hain
- **Kitni baar:** Duck −12 dB; in-fade ~10f; out-fade ~15f; end fade 2s
- **Evidence:** 🟠 — KF-07 volume automation landmarks
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Takraav note:** TAKRAAV: purana default bed music ko voice se 18–25 dB neeche rakhta hai; −12 dB usse kam gehra hai. Aur ChaiWithJai ke ducker (2.7 dB start, >5 dB amateur) se bhi takrata hai. Teeno alag contexts ke numbers hain (bed level / CapCut duck / podcast ducker) — merge par har profile ka ek number tay karna hoga.

### R-444 — Music bed narration ke neeche: −24..−18 LUFS relative ⚙️ *(naya — editor round)*
- **Purana ID:** D2-087
- **Kab:** Travel film me voiceover ke neeche music bed rakhte waqt
- **Kya:** Music ko narration ke neeche lagbhag −24 se −18 LUFS relative bed par rakho; clipping kabhi nahi; chapter badlav ke aas-paas chhote fades do
- **Kyun:** Bed mehsoos ho, sune nahi — voice hamesha aage
- **Kitni baar:** Bed −24..−18 LUFS relative
- **Evidence:** 🟠 — Travel-studio audio QA target
- **Sources:** `github_junwen853_travel-video-studio-skill.md`
- **Check:** `{"kind": "db_range", "min_db": -24, "max_db": -18, "what": "music bed narration ke relative (LUFS)"}`
- **Takraav note:** Purane 18–25 dB under-voice default ke qareeb hai, lekin ye LUFS-relative me mapta hai (dB me nahi) — map farq note karo. Isi cluster ke −12 dB duck (KF-07) se takraav upar wale rule me darj hai.

### R-445 — SFX volume ki seedhi (hierarchy) ⚙️ *(naya — editor round)*
- **Purana ID:** D2-088
- **Kab:** SFX aur music ka balance set karte waqt
- **Kya:** Seedhi rakho (music = 0 dB reference): voice/dialogue music se +3..+6 dB upar; primary SFX 0..+3 dB upar; ambient bed −12..−18 dB neeche; UI sounds (click/pop/ding) −6..−3 dB neeche
- **Kyun:** Har layer ki apni aukaat fix ho to mix kabhi keechad (mud) nahi banta
- **Kitni baar:** Voice +3..+6; SFX 0..+3; ambient −12..−18; UI −6..−3 (music ke relative dB)
- **Evidence:** 🟠 — KF-07 SFX layering rules
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "db_range", "min_db": 3, "max_db": 6, "what": "voice music se upar (dB)"}`

### R-446 — SFX ki haden: 3 stack, duration-match, comedy sirf meme/viral ⚙️ *(naya — editor round)*
- **Purana ID:** D2-089
- **Kab:** SFX lagate waqt
- **Kya:** Ek frame par 3 se zyada SFX stack mat karo (primary + tail + ambient hi kaafi). SFX ki duration transition ki duration se match kare — peak transition ke beech me, tail aakhir me. Comedy SFX (vine boom, fail horn, airhorn) sirf Meme/Viral modes me; Cinematic/Documentary/Aesthetic/Minimal me inki jagah zero hai
- **Kyun:** Teen se zyada awaazein ek saath = shor; galat mode ka comedy SFX poore mood ko maar deta hai
- **Kitni baar:** Stack ≤3; comedy SFX sirf 2 modes me
- **Evidence:** 🟠 — KF-07 SFX rules
- **Sources:** `github_tashisleepy_capcut-ai-director.md`
- **Check:** `{"kind": "count_range", "max": 3, "what": "ek frame par stacked SFX"}`

### R-447 — Audio edges hamesha fade; hard start/stop kabhi nahi *(naya — editor round)*
- **Purana ID:** D2-090
- **Kab:** Har audio clip ke sire par
- **Kya:** Har audio clip ke edges par fade lagao — kabhi hard start/stop nahi. Dissolve/fade par SFX ki jagah kuch nahi ya halka swell; music use carry karta hai
- **Kyun:** Hard audio edges click/pop dete hain jo sabse saste lagte hain
- **Kitni baar:** Bina-fade audio edges = 0
- **Evidence:** 🟠 — KF-07 audio workflow + director niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`

### R-448 — SFX density mode ke hisaab se; foley sirf motivated *(naya — editor round)*
- **Purana ID:** D2-091
- **Kab:** Sound design ki ghanata (density) tay karte waqt
- **Kya:** Density mode se lo: Viral — SFX har 1–2s; Cinematic — har 5–15s; Documentary — sirf functional; Meme — maximum. Foley sirf tab jab motivated ho — random SFX khaamoshi se bhi bura hai
- **Kyun:** Har mode ki apni awaaz ki bhasha hai; ek density sab par = koi pehchan nahi
- **Kitni baar:** Viral 1–2s; Cinematic 5–15s; Documentary functional only
- **Evidence:** 🟠 — KF-07 mode blueprints + production standard ka foley niyam
- **Sources:** `github_tashisleepy_capcut-ai-director.md`, `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-449 — Scenic audio policy: loud BGM sirf muted picture par *(naya — editor round)*
- **Purana ID:** D2-092
- **Kab:** Scenic/BGM-led windows ki audio policy me
- **Kya:** Loud BGM sirf muted picture ke upar chalao. Jahan audible speech hai (face-to-camera ya transcript-backed) woh hamesha sunai de. Frustration/conflict/sensitive/dry windows par BGM forbidden rakho. TTS sirf muted-picture windows par chalao
- **Kyun:** Jazbaati pal par bajta khush music ya bolne par chadha BGM — dono film ko jhootha bana dete hain
- **Kitni baar:** Speech windows me BGM-over-voice = 0; sensitive windows me BGM = 0
- **Evidence:** 🟠 — House audio-scene policy
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-450 — BGM asli named music ho; hum/tone/placeholder = block *(naya — editor round)*
- **Purana ID:** D2-093
- **Kab:** BGM select/final karne se pehle
- **Kya:** Final bed hamesha asal, named aur traceable music ho — sine tone, hum, buzz, silence ya procedural placeholder kabhi final nahi. Har asset ki license ledger me verify ho aur Content-ID risk check ho; bina verify kiye 'usable' kabhi mat kaho
- **Kyun:** Tone-bed technical pass ho sakta hai lekin film ko marr deta hai; license bina ka asset baad me claim laata hai
- **Kitni baar:** Placeholder beds = 0; har asset = verified license row
- **Evidence:** 🟠 — BGM musicality + asset ledger contracts
- **Sources:** `github_junwen853_travel-video-studio-skill.md`

### R-451 — VO finish master peak −6 dBFS *(naya — editor round)*
- **Purana ID:** D2-094
- **Kab:** Voiceover finish/master karte waqt
- **Kya:** VO finish master ka peak −6 dBFS rakho
- **Kyun:** Neeche rakha peak aage ke processing ke liye headroom deta hai
- **Kitni baar:** Peak = −6 dBFS
- **Evidence:** 🟠 — Note source ke VO-finish preset se
- **Sources:** `notes_AdamGarceau_resolve-toolkit.md (note)`
- **Takraav note:** TAKRAAV (map ka): purane targets LUFS-integrated me hain (−14/−16 LUFS). Ye −6 dBFS PEAK hai, integrated loudness nahi — dono ek saath lagu nahi hote. Ye VO production-stage ka number hai, delivery loudness purane LUFS rules se hi tay ho.

### R-452 — Quiet sections ko haath se +3..+6 dB boost ⚙️ *(naya — editor round)*
- **Purana ID:** D2-095
- **Kab:** Cleanup chain ke baad bache dhime hisso par
- **Kya:** Jo hisse gate/NR ke baad bhi dhime reh jayein, unhe haath se +3..+6 dB boost karo
- **Kyun:** Auto chain ausat ko theek karta hai; sabse dhime pal haath se hi uthte hain
- **Kitni baar:** Boost +3..+6 dB sirf quiet sections par
- **Evidence:** 🟠 — Podcast cleanup workflow
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "db_range", "min_db": 3, "max_db": 6, "what": "quiet section manual boost"}`

### R-453 — Rang ka kram: normalize pehle, creative grade baad me *(naya — editor round)*
- **Purana ID:** D2-096
- **Kab:** Webcam/talking-head colour grade karte waqt
- **Kya:** Waveform scope padho, laptop screen ko nahi. Node kram: (1) Normalize — blacks ~5–10% (1023 scale par ~64), highlights ~768, contrast 1.1–1.2, pivot 0.3; (2) Balance — neutrals par RGB overlap; (3) Contrast; (4) Skin — HSL qualifier + power window. Creative grade hamesha normalize ke BAAD
- **Kyun:** Galat base par bani grade har nayi roshni me toot jati hai
- **Kitni baar:** 4 nodes, yahi kram
- **Evidence:** 🟠 — Resolve color-grade (webcam) workflow
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-454 — Skin saturation ~60, 70+ kabhi nahi ⚙️ *(naya — editor round)*
- **Purana ID:** D2-097
- **Kab:** Skin tone theek karte waqt
- **Kya:** Skin saturation ~60 ke aas-paas rakho — 70 ya usse upar kabhi nahi. Skin ko warm gain do aur qualifier + power window se alag sambhalo
- **Kyun:** 70+ saturation par chehra narangi-pakoda ho jata hai
- **Kitni baar:** Skin sat ≈60; >70 = block
- **Evidence:** 🟠 — Usi colour workflow se
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "percent_range", "target": 60, "max_pct": 70, "what": "skin saturation"}`

### R-455 — Grade ko PowerGrade bana kar rakho; har roshni ka alag grade *(naya — editor round)*
- **Purana ID:** D2-098
- **Kab:** Grade mukammal hote hi
- **Kya:** Final grade ko PowerGrade/preset bana kar save karo taaki reuse ho. Har nayi lighting setup ke liye phir se grade karo — purana grade nayi roshni par zabardasti mat lagao
- **Kyun:** Roshni badli to rang ke sawaal badle; copy-paste grade aadhi jagah galat hota hai
- **Kitni baar:** Har setup = apna grade; save hamesha
- **Evidence:** 🟠 — Colour workflow
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`

### R-456 — Audio track layout: A1–A4 aur stack ka kram *(naya — editor round)*
- **Purana ID:** D2-099
- **Kab:** Multicam/podcast ya bade edit ki timeline sajate waqt
- **Kya:** Tracks aise rakho: A1 selected dialogue, A2 processed dialogue, A3 music/ambience, A4 SFX/bumpers. Aam stack ka kram neeche se upar: ambient/room tone → music → SFX → voice sabse upar
- **Kyun:** Bikhre tracks par mix kabhi dobara nahi milta; sajawat hi aadha mix hai
- **Kitni baar:** 4 tracks fixed bhumika; stack kram fixed
- **Evidence:** 🟠 — Do sources: podcast track layout + KF-07 stacking order
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`, `github_tashisleepy_capcut-ai-director.md`

### R-457 — Delivery verify bahari meter se; platform exports tay ⚙️ *(naya — editor round)*
- **Purana ID:** D2-100
- **Kab:** Final export aur delivery check par
- **Kya:** Loudness ko bahari meter se verify karo: YouTube −14 ±1 LUFS. Platform exports: YouTube 1920x1080 −14 LUFS; LinkedIn 1080x1080 −16 LUFS; vertical 1080x1920 −16 LUFS. Manual position keyframes ki jagah AI Smart Reframe ko tarjeeh do (vertical ke liye)
- **Kyun:** Editor ke andar ka meter jhooth bol sakta hai; bahari map hi saboot hai
- **Kitni baar:** YT −14 ±1 LUFS verified
- **Evidence:** 🟡 — YouTube ka −14 LUFS platform normalization spec maana gaya number hai; baaki platform numbers source ke house targets hain
- **Sources:** `github_ChaiWithJai_davinci-resolve-claude-skills.md`
- **Check:** `{"kind": "lufs_target", "value": -14, "tolerance": 1, "platform": "YouTube"}`

### R-458 — Share se pehle silent-track check *(naya — editor round)*
- **Purana ID:** D2-101
- **Kab:** Koi bhi video share/export se pehle
- **Kya:** Audio ka mean_volume check karo: −80 dB se neeche matlab track silent/muted hai — share mat karo, pehle theek karo
- **Kyun:** Muted track wala export sabse sharminda karne wali galti hai aur sabse aasan pakdi jati hai
- **Kitni baar:** Mean volume ≤−80 dB = block
- **Evidence:** 🟠 — Screencast workflow ki pre-share check
- **Sources:** `github_matthull_my-skills.md`

### R-459 — Export: quality rakho, file size par nazar (25 GB trap) *(naya — editor round)*
- **Purana ID:** D2-102
- **Kab:** Final export settings tay karte waqt
- **Kya:** Quality barkarar rakho lekin file size hamesha dekho — bina dekhe export 25 GB jaise trap me phans sakta hai
- **Kyun:** Upload/share par size hi sabse pehli rukawat banta hai
- **Kitni baar:** Har export = size check ke saath
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_appariciojunior_video-editor-skills.md (note)`

### R-460 — Podcast punch-in active speaker par switch kare *(naya — editor round)*
- **Purana ID:** D2-103
- **Kab:** Multicam podcast edit me
- **Kya:** Punch-in/camera switch hamesha us speaker par ho jo bol raha hai (pitch-based speaker pehchan se madad lo)
- **Kyun:** Galat chehre par kata hua jawaab viewer ko gumrah karta hai
- **Kitni baar:** Switch = active speaker par hi
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_AdamGarceau_resolve-toolkit.md (note)`

### R-461 — Filters/retouch mamuli (moderate) rakho *(naya — editor round)*
- **Purana ID:** D2-104
- **Kab:** CapCut mobile me filters/effects/retouch lagate waqt
- **Kya:** Filters aur effects conservative rakho; portrait retouch moderate aur natural rakho — chehra plastic na lage
- **Kyun:** Zyada retouch pehle frame me pakda jata hai aur bharosa todta hai
- **Kitni baar:** Retouch = moderate/natural hamesha
- **Evidence:** 🟠 — CapCut mobile workflow
- **Sources:** `github_pockebot_openpocket.md`

### R-462 — Motion overlays bole gaye shabdon ke saath timed *(naya — editor round)*
- **Purana ID:** D2-105
- **Kab:** Motion graphics/overlays lagate waqt
- **Kya:** Overlays ko un shabdon ke saath time karo jinke baare me woh hain. Face aur caption wale hisse hamesha clear rakho
- **Kyun:** Der se aaya overlay purani khabar hai; chehre par aaya overlay rukawat
- **Kitni baar:** Overlay timing = shabd ke saath; face/caption zone clear
- **Evidence:** 🟠 — Note source
- **Sources:** `notes_appariciojunior_video-editor-skills.md (note)`

### R-463 — Travel delivery master: 4K 60fps, ≥60 Mbps *(naya — editor round)*
- **Purana ID:** D2-106
- **Kab:** Travel footage (DJI/action/phone) ki master delivery par
- **Kya:** Master target rakho: 4K, 59.94/60fps, kam se kam 60 Mbps — jab source footage is kabil ho
- **Kyun:** Neeche ka master baad me har platform par kamzor padta hai
- **Kitni baar:** 4K 60fps ≥60 Mbps (source allow kare to)
- **Evidence:** 🟠 — Travel-studio ka Definition of Done
- **Sources:** `github_junwen853_travel-video-studio-skill.md`