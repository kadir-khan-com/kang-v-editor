"""A/B only: Nemotron 3.5 ASR 0.6B via NVIDIA NeMo-Speech.cpp (GGUF q8) on dwarika.mp3, hi-IN.
Run A = no boosting, runs B_* = phrase boosting sweep (v1 boost 3 hallucinated; v2 sweep: 0.25-0.5 safe, >=1.0 bad; v3 = tuned list, no single-word द्वारिकाधीश prefix trap) (--speech-context) for place/temple names.
Outputs JSON with word timestamps. Never imported by kang; nothing here edits our transcript."""
import glob, json, os, subprocess, time
I, W = "/kaggle/input", "/kaggle/working"
O = W + "/out"; os.makedirs(O, exist_ok=True)
def sh(c):
    print("$", c, flush=True)
    r = subprocess.run(c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(r.stdout[-3000:], "[rc=%d]" % r.returncode, flush=True); return r
V = "0.2.0"
REL = f"https://github.com/NVIDIA/NeMo-Speech.cpp/releases/download/v{V}"
PHRASES = ["बेट द्वारका", "बेट द्वारिका", "द्वारकाधीश", "नागेश्वर ज्योतिर्लिंग", "भड़केश्वर महादेव", "वज्रनाभ ने",
           "सिद्धेश्वर महादेव", "शिवराजपुर बीच", "सुदर्शन सेतु", "रुक्मणी माता", "गोपी तालाब", "काठियावाड़",
           "संगम नारायण", "दुर्वासा ऋषि", "स्वर्ग द्वार", "मोक्ष द्वार", "सर्पदोष", "गोमती नदी", "स्वामीनारायण मंदिर"]
audio = glob.glob(I + "/**/dwarika.mp3", recursive=True)[0]
sh("nvidia-smi --query-gpu=name,driver_version --format=csv")
res = {}
for flavor in ("cuda", "cpu"):
    tgz = f"nemo-speech-{V}-linux-x86_64-{flavor}.tar.gz"
    r = sh(f"cd {W} && curl -sfLO {REL}/{tgz} && curl -sfLO {REL}/{tgz}.sha256 && sha256sum -c {tgz}.sha256 && tar xzf {tgz}")
    B = f"{W}/nemo-speech-{V}-linux-x86_64-{flavor}/bin/nemo-speech"
    if r.returncode == 0 and sh(f"{B} --version").returncode == 0:
        res["build"] = flavor; break
sh(f"cd {W} && curl -sfL -o m.gguf https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b/resolve/main/nemotron-3.5-asr-streaming-0.6b.q8_0.gguf && ls -la m.gguf")
sh(f"ffmpeg -hide_banner -loglevel error -y -i {audio} -ac 1 -ar 16000 -c:a pcm_s16le {W}/a.wav")
dev = "--device cuda:0" if res.get("build") == "cuda" else ""
ctx = " ".join(f"--speech-context '{p}'" for p in PHRASES)
RUNS = [("A_base", "")] + [(f"B_boost_{b}", ctx + f" --speech-context-boost {b}") for b in ("0.5", "0.75")]
for name, extra in RUNS:
    t = time.time()
    r = sh(f"{B} transcribe {W}/a.wav --model {W}/m.gguf -l hi-IN -f json -o {O}/{name}.json {dev} {extra} 2>&1 | tail -8")
    res[name] = {"rc": r.returncode, "s": round(time.time() - t, 1)}
res["phrases"] = PHRASES
json.dump(res, open(f"{O}/summary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("SUMMARY", res, flush=True)
