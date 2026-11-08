"""Kaggle GPU kernel ironindiarat/kang-ai-motion (KANG v17): Wan2.2-TI2V-5B (hf:Wan-AI/Wan2.2-TI2V-5B-Diffusers,
Apache-2.0, revision pinned below) image-to-video for the jobs in the input dataset (jobs.json + inputs/*.png from
`kang.py ai-motion-plan`). One worker per GPU (T4 x2 when available), prompt embeddings pre-computed once (UMT5-XXL bf16
on GPU 0 in a subprocess, CPU fallback; same recipe as diffusers WanPipeline._get_t5_prompt_embeds). Output
/kaggle/working/raw/<job>.mp4 (raw job width x height, 24 fps, no post-processing) + kernel_report.json. Gate / composite / labels happen in KANG
(`kang.py ai-motion-apply`). Nothing published."""
import glob, json, os, shutil, subprocess, sys, time, traceback

W = "/kaggle/working"
MODEL_ID = "Wan-AI/Wan2.2-TI2V-5B-Diffusers"
REV = "b8fff7315c768468a5333511427288870b2e9635"
os.environ.setdefault("HF_HOME", "/tmp/hf")
os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
rep = {"steps": [], "t0": time.time(), "model": MODEL_ID, "revision": REV, "kernel_rev": "v4 group offload, LPT split"}
RAW = f"{W}/raw"
os.makedirs(RAW, exist_ok=True)


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    rep["steps"].append({"cmd": cmd, "rc": r.returncode, "tail": (r.stdout + r.stderr)[-800:]})
    print("$", cmd, "rc", r.returncode, (r.stdout + r.stderr)[-300:], flush=True)
    return r


EMBED_PY = r"""
import json, sys, torch
from transformers import AutoTokenizer, UMT5EncoderModel
mdir, dev = sys.argv[1], sys.argv[2]
texts = json.load(open("/tmp/texts.json", encoding="utf-8"))
tok = AutoTokenizer.from_pretrained(mdir, subfolder="tokenizer")
te = UMT5EncoderModel.from_pretrained(mdir, subfolder="text_encoder", torch_dtype=torch.bfloat16).to(dev).eval()
E = {}
with torch.no_grad():
    for s in texts:
        ti = tok([s], padding="max_length", max_length=512, truncation=True, add_special_tokens=True,
                 return_attention_mask=True, return_tensors="pt")
        n = int(ti.attention_mask.gt(0).sum())
        h = te(ti.input_ids.to(dev), ti.attention_mask.to(dev)).last_hidden_state[0, :n].float().cpu()
        h = torch.cat([h, h.new_zeros(512 - n, h.size(1))])[None]
        assert torch.isfinite(h).all(), "non-finite embedding"
        E[s] = h.to(torch.float16)
torch.save(E, "/tmp/embeds.pt")
print("embeds", len(E), "peak_gb", round(torch.cuda.max_memory_allocated() / 1e9, 2) if dev == "cuda" else 0)
"""


def save():
    json.dump(rep, open(f"{W}/kernel_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


jobs_path = glob.glob("/kaggle/input/**/jobs.json", recursive=True)[0]
base = os.path.dirname(jobs_path)
worker = glob.glob("/kaggle/input/**/ai_motion_worker.py", recursive=True)[0]
J = json.load(open(jobs_path))
rep["jobs_in"] = [j["id"] for j in J["jobs"]]
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh("df -h /tmp /kaggle/working | tail -2; free -g | head -2; nproc")
sh("pip install -q -U 'diffusers>=0.35.1' 'transformers>=4.51' accelerate ftfy sentencepiece")
sh("python -c 'import diffusers, transformers, torch; print(diffusers.__version__, transformers.__version__, torch.__version__)'")
save()
try:
    from huggingface_hub import snapshot_download
    t = time.time()
    mdir = snapshot_download(MODEL_ID, revision=REV, allow_patterns=["model_index.json", "scheduler/*", "text_encoder/*",
                                                                     "tokenizer/*", "transformer/*", "vae/*"])
    rep["download_s"] = round(time.time() - t, 1)
    rep["model_dir"] = mdir
    save()
    # ---- prompt embeddings (v3, KANG_017): UMT5-XXL bf16 on GPU 0 in a SUBPROCESS (its CUDA context and 11 GB are gone
    # before the workers load); CPU bf16 fallback (v1/v2 recipe, ~430 s) if the GPU encode fails or is not finite.
    import torch
    texts = sorted({j["prompt"] for j in J["jobs"]} | {j["negative"] for j in J["jobs"]})
    json.dump(texts, open("/tmp/texts.json", "w", encoding="utf-8"), ensure_ascii=False)
    open("/tmp/embed.py", "w", encoding="utf-8").write(EMBED_PY)
    t = time.time()
    r = sh(f"CUDA_VISIBLE_DEVICES=0 {sys.executable} /tmp/embed.py {mdir} cuda")
    rep["embeds_device"] = "cuda"
    if r.returncode != 0 or not os.path.exists("/tmp/embeds.pt"):
        rep["embeds_gpu_error"] = (r.stdout + r.stderr)[-1500:]
        t = time.time()
        r = sh(f"CUDA_VISIBLE_DEVICES= {sys.executable} /tmp/embed.py {mdir} cpu")
        rep["embeds_device"] = "cpu"
    rep["embeds_s"] = round(time.time() - t, 1)
    E = torch.load("/tmp/embeds.pt")
    rep["embeds_n"] = len(E)
    rep["embeds_finite"] = all(bool(torch.isfinite(v).all()) for v in E.values())
    rep["embeds_absmax"] = max(float(v.abs().max()) for v in E.values())
    del E
    save()
    # ---- workers: one per GPU, jobs round-robin (longest first), model loads staggered
    mons = [subprocess.Popen(["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits", "-l", "5"],
                             stdout=open(f"{W}/smi.log", "w")),
            subprocess.Popen(["free", "-m", "-s", "10"], stdout=open(f"{W}/free.log", "w"))]
    ngpu = torch.cuda.device_count()
    rep["gpus"] = ngpu
    order = sorted(J["jobs"], key=lambda j: -j["num_frames"])
    # v4 (KANG_021): longest-processing-time split (each job to the GPU with the fewest frames so far), not round robin
    split, load = [[] for _ in range(max(ngpu, 1))], [0] * max(ngpu, 1)
    for j in order:
        g = load.index(min(load))
        split[g].append(j["id"])
        load[g] += j["num_frames"]
    rep["split_frames"] = load
    procs = []
    for g in range(ngpu):
        if not split[g]:
            continue
        ready = f"/tmp/ready_{g}"
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(g))
        lf = open(f"{W}/worker_{g}.log", "w")
        procs.append(subprocess.Popen([sys.executable, worker, "--gpu", str(g), "--jobs", jobs_path, "--embeds",
                                       "/tmp/embeds.pt", "--model", mdir, "--out", RAW, "--ids", ",".join(split[g]),
                                       "--ready", ready], env=env, stdout=lf, stderr=subprocess.STDOUT))
        t = time.time()
        while not os.path.exists(ready) and procs[-1].poll() is None and time.time() - t < 1800:
            time.sleep(5)
    for p in procs:
        p.wait()
    rep["jobs"] = []
    for g in range(ngpu):
        f = f"{RAW}/worker_{g}.json"
        if os.path.exists(f):
            w = json.load(open(f))
            rep.setdefault("workers", []).append({k: v for k, v in w.items() if k != "jobs"})
            rep["jobs"] += w.get("jobs", [])
        lg = f"{W}/worker_{g}.log"
        if os.path.exists(lg):
            rep.setdefault("worker_log_tail", {})[g] = open(lg).read()[-2000:]
    for m_ in mons:
        m_.terminate()
    try:
        mx = {}
        for ln in open(f"{W}/smi.log"):
            i, u = [x.strip() for x in ln.split(",")[:2]]
            mx[i] = max(mx.get(i, 0), int(u))
        rep["smi_peak_mib"] = mx
    except Exception as e:
        rep["smi_peak_mib"] = str(e)
except Exception:
    rep["error"] = traceback.format_exc()[-3000:]
    print(rep["error"], flush=True)
rep["elapsed_s"] = round(time.time() - rep["t0"], 1)
save()
print(json.dumps({k: rep.get(k) for k in ("gpus", "download_s", "embeds_s", "elapsed_s", "error")}, default=str), flush=True)
print(json.dumps(rep.get("jobs", []), default=str)[:3000], flush=True)
for m_ in globals().get("mons", []):
    try:
        m_.terminate()
    except Exception:
        pass
