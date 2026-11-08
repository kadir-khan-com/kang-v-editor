# NOTES (apne shabdon me) — ADAM-0S/wayland-m3ta-0s → `video-editing-master` skill

**Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**

- Source: ADAM-0S/wayland-m3ta-0s — Link: https://github.com/ADAM-0S/wayland-m3ta-0s
- Licence: repo ka LICENSE **AGPL-3.0** hai (repo page par verify, 2026-11-06). Ek dilchasp inconsistency: skill file ki frontmatter khud ko "Apache-2.0" kehti hai, lekin repo ka asli LICENSE AGPL-3.0 hai — repo licence hi maana gaya, isliye full extraction nahi hua.
- Kya hai ye: Ek bade AI-agent OS repo ke andar band ek `video-editing-master` skill — Premiere Pro aur DaVinci Resolve dono ke liye professional editing craft (cutting, colour, audio, export, project organisation). Skill pura padha gaya (613 lines); neeche sirf techniques/numbers ka sar apne shabdon me hai.

## Techniques ka sar (apne shabdon me)

**Cutting**
- Fine editing razor se nahi, chaar trim operations se hoti hai: ripple (edit point hile, aage ka sab shift), roll (duration same, sirf edit point hile), slip (clip wahi, andar ka content hile), slide (clip hile, duration same). Premiere me Trim Mode (T), Slip = Y tool, Slide = U tool.
- Split edit (J/L-cut) iska sabse bada niyam hai: audio aur video ek hi point par kabhi mat kaato; audio ko video se **6–12 frames** offset rakho. J-cut = agle scene ki awaaz pehle aati hai (anticipation, interview transitions); L-cut = pichli awaaz nayi tasveer par chalti rehti hai (reaction shots, emotional carry-over). Iska daava: dialogue editing me lagbhag **80% cuts split edits** hone chahiye, seedhe cuts baatcheet me jarring lagte hain.
- Match cut ki chaar kism: graphic (shape), movement, sound, idea/concept.
- Invisible cut: cut ko whip pan, frame cross karte object, light flash ya rack-focus blur ke peeche chhupao.
- Rhythm editing: cuts ko kisi taal par rakho — music ke beats, tension ke saath badhti speed (emotional rhythm), shaant hisso me saans ki gati (breathing rhythm), ya bolne wale ki cadence.

**Colour**
- Resolve me 6-node ki pipeline: (1) input transform (camera space → working space), (2) primary correction (scopes dekh kar black/white point, white balance), (3) creative grade — creative LUT hamesha **50–70% intensity** par, (4) secondary (windows/qualifiers), (5) skin-tone protection (vectorscope ki skin line par), (6) output transform.
- Shot matching: pehle scene ka ek hero shot grade karo, uska still bachao, phir har shot ko waveform (exposure), parade (balance), histogram (contrast), vectorscope (skin) se usi se milao.
- Premiere Lumetri ka kram: Basic Correction → Creative (Look kam intensity par) → Curves → Color Wheels → HSL Secondary. Grade adjustment layer par rakho — ek correction ke liye, ek creative ke liye.

**Audio**
- Dialogue cleanup ka kram: normalize (peaks **−12 se −6 dBFS**), high-pass filter **80–100 Hz**, room-tone se noise print lekar de-noise, de-ess **4–8 kHz**, halki compression **2:1–3:1**, aur har edit point par **2–4 frames ka audio crossfade**.
- Mix levels (dBFS): dialogue −12..−6 (sabse upar), dialogue ke neeche music −18..−24, bina dialogue ke featured music −12..−6, SFX −18..−6, ambience bed −24..−18.
- Ducking: dialogue shuru hote hi music ko keyframes se **6–12 dB** neeche, pauses me wapas upar. (Premiere: Essential Sound auto-duck; Resolve: Fairlight automation/sidechain.)
- Loudness targets (integrated LUFS): YouTube **−14**, podcast **−16**, broadcast TV **−24**, cinema/Netflix **−27** (Netflix par true peak max **−2 dBTP**).

**Export / organisation**
- YouTube/Vimeo: VBR 2-pass — 1080p par **16–24 Mbps**, 4K par **45–68 Mbps**, audio AAC 320 kbps 48 kHz. Reels/TikTok: 1080×1920, 30 fps, **10–15 Mbps**, AAC 256 kbps. Master: ProRes 422 / DNxHR HQ, PCM 24-bit.
- Proxy: Premiere ingest me **1/4 resolution** proxy (ProRes LT ya H.264), export se pehle original se relink.
- Project banaan: numbered folders (01_Footage camera-wise, 02_Audio, 03_Graphics, 04_Project_Files, 05_Exports, 06_Documents). Sequence naming `[Project]_v[01]_[description]`; bade badlav se pehle sequence duplicate karo, apni ikloti timeline kabhi overwrite mat karo; export naam me date + version.
- Delivery checklist ka saar: pehla/aakhri frame verify, head/tail par black frames nahi, exported file pura dekh kar hi deliver karo (sirf timeline preview par bharosa nahi).
