"""A/B measurement only: transcribe dwarika.mp3 with nvidia/nemotron-3.5-asr-streaming-0.6b (hi-IN).
Audio is cut at silences into ~25 s chunks (ffmpeg silencedetect); each chunk is transcribed offline with
Transformers. Output: out/nemotron_chunks.json (chunk start/end + text) and timing. Never imported by kang."""
import glob, json, os, re, subprocess, sys, time

def sh(c):
    print("$", c, flush=True)
    r = subprocess.run(c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(r.stdout[-4000:], "[rc=%d]" % r.returncode, flush=True)
    return r

I, O = "/kaggle/input", "/kaggle/working/out"
os.makedirs(O, exist_ok=True)
audio = glob.glob(I + "/**/dwarika.mp3", recursive=True)[0]
sh('pip install -q "transformers>=5.13.0" accelerate soundfile 2>&1 | tail -2')
sh("python -c 'import transformers, torch; print(transformers.__version__, torch.__version__, torch.cuda.is_available())'")

wav = "/kaggle/working/a16k.wav"
sh(f"ffmpeg -hide_banner -loglevel error -y -i {audio} -ac 1 -ar 16000 {wav}")
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).decode())
sd = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "silencedetect=noise=-32dB:d=0.25", "-f", "null", "-"],
                    text=True, stderr=subprocess.PIPE).stderr
sil = [(float(a) + float(b)) / 2 for a, b in zip(re.findall(r"silence_start: ([\d.]+)", sd), re.findall(r"silence_end: ([\d.]+)", sd))]
cuts, last = [0.0], 0.0
while dur - last > 30:
    cand = [s for s in sil if last + 15 <= s <= last + 30]
    nxt = min(cand, key=lambda s: abs(s - (last + 25))) if cand else last + 25
    cuts.append(nxt); last = nxt
cuts.append(dur)
print("chunks", len(cuts) - 1, "silences", len(sil), flush=True)

import numpy as np, soundfile as sf, torch
from transformers import AutoModelForRNNT, AutoProcessor
mid = "nvidia/nemotron-3.5-asr-streaming-0.6b"
t0 = time.time()
proc = AutoProcessor.from_pretrained(mid)
model = AutoModelForRNNT.from_pretrained(mid, device_map="cuda", torch_dtype=torch.float16)
t_load = time.time() - t0
x, sr = sf.read(wav, dtype="float32")
res, t1 = [], time.time()
for a, b in zip(cuts[:-1], cuts[1:]):
    seg = x[int(a * sr):int(b * sr)]
    inp = proc(seg, sampling_rate=sr, language="hi-IN")
    inp = inp.to(model.device, dtype=model.dtype)
    with torch.no_grad():
        out = model.generate(**inp, return_dict_in_generate=True)
    txt = proc.decode(out.sequences, skip_special_tokens=True)
    txt = txt[0] if isinstance(txt, list) else txt
    res.append({"start": round(a, 2), "end": round(b, 2), "text": txt.strip()})
    print(f"{a:7.2f}-{b:7.2f} {txt.strip()[:120]}", flush=True)
t_asr = time.time() - t1
json.dump({"model": mid, "language": "hi-IN", "dtype": "float16", "duration_s": dur, "load_s": round(t_load, 1),
           "asr_s": round(t_asr, 1), "gpu": torch.cuda.get_device_name(0), "chunks": res},
          open(f"{O}/nemotron_chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE load", round(t_load, 1), "asr", round(t_asr, 1), flush=True)
