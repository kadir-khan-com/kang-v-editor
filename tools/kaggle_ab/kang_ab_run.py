import os, sys, glob, json, shutil, subprocess, time, zipfile
def sh(c, check=False):
    print(f"\n$ {c}", flush=True); t=time.time()
    r = subprocess.run(c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    print(r.stdout[-12000:], flush=True); print(f"[rc={r.returncode} {time.time()-t:.1f}s]", flush=True)
    if check and r.returncode: sys.exit(f"FAILED: {c}")
    return r
W = "/kaggle/working"; os.chdir(W)
z = glob.glob("/kaggle/input/**/kang_project.zip", recursive=True)
if z: zipfile.ZipFile(z[0]).extractall(W)
else: shutil.copytree(glob.glob("/kaggle/input/**/kang", recursive=True)[0], W+"/kang")
K = W + "/kang"; os.chdir(K); os.makedirs("samples", exist_ok=True)
shutil.copy(glob.glob("/kaggle/input/**/dwarika.mp3", recursive=True)[0], "samples/dwarika.mp3")
ref = glob.glob("/kaggle/input/**/ref_v2_words.json", recursive=True)[0]
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
sh("pip install -q 'faster-whisper>=1.1' 'pydantic>=2.5,<3' fonttools pytest 2>&1 | tail -3")
sh("python -c \"import faster_whisper,ctranslate2;print('fw',faster_whisper.__version__,'ct2',ctranslate2.__version__,'cuda',ctranslate2.get_cuda_device_count())\"")
sh("curl -sL -o /kaggle/working/hi.dic https://raw.githubusercontent.com/LibreOffice/dictionaries/master/hi_IN/hi_IN.dic; wc -l /kaggle/working/hi.dic")
sh("python build_and_check.py", check=True)
CONVERT = r"""
import sys, subprocess, shutil, pathlib
from transformers import WhisperTokenizerFast
src, name = sys.argv[1], sys.argv[2]; out = "/tmp/ct2/" + name
r = subprocess.run(["ct2-transformers-converter", "--model", src, "--output_dir", out, "--quantization", "float16",
                    "--copy_files", "preprocessor_config.json", "--force"])
if r.returncode == 0:
    try:
        tok = WhisperTokenizerFast.from_pretrained(src)
    except Exception as e:  # local checkpoints may ship without tokenizer files: same vocab as the base model
        import json
        mel = json.load(open(pathlib.Path(src) / "config.json")).get("num_mel_bins", 80)
        base = "openai/whisper-large-v3" if mel == 128 else ("openai/whisper-large-v2" if "large" in src else "openai/whisper-medium")
        print("tokenizer fallback", base, type(e).__name__)
        tok = WhisperTokenizerFast.from_pretrained(base)
    tok.save_pretrained(out)   # tokenizer.json for faster-whisper
    print("converted", out, sorted(p.name for p in pathlib.Path(out).iterdir()))
shutil.rmtree(pathlib.Path.home() / ".cache/huggingface/hub", ignore_errors=True)
sys.exit(r.returncode)
"""
open("convert_hi.py", "w").write(CONVERT)
sh("pip install -q 'transformers>=4.40' 2>&1 | tail -1; df -h /kaggle/working /tmp | tail -2")
sh("python convert_hi.py ARTPARK-IISc/whisper-large-v3-vaani-hindi vaani 2>&1 | grep -v Warning | tail -3")
sh("python convert_hi.py collabora/whisper-medium-hindi medium 2>&1 | grep -v Warning | tail -3")
# AI4Bharat IndicWhisper (GitHub AI4Bharat/vistaar, MIT): HF-format checkpoint in a zip, not on the Hub
sh("cd /tmp && curl -sL -o hi_iw.zip https://indicwhisper.objectstore.e2enetworks.net/hindi_models.zip && ls -la hi_iw.zip && unzip -q -o hi_iw.zip -d iw && rm hi_iw.zip && find iw -name config.json")
iw = [os.path.dirname(p) for p in glob.glob("/tmp/iw/**/config.json", recursive=True)]
print("IndicWhisper dirs:", iw)
for d in iw:
    sh(f"python convert_hi.py '{d}' {'indic' if 'medium' in d else 'indic_large'} 2>&1 | grep -v Warning | tail -4")
sh("rm -rf /tmp/iw; df -h /tmp | tail -1")
os.makedirs(W+"/out", exist_ok=True)
voters = ",".join(f"{n}=/tmp/ct2/{n}" for n in ("vaani", "medium", "indic", "indic_large"))
r = sh(f"python tools/ab_whisper.py samples/dwarika.mp3 --ref {ref} --wordlist /kaggle/working/hi.dic --device cuda "
       f"--configs turbo_vote,v3_vote --voters {voters} --out {W}/out/ab_report.json")
# WhisperX alignment cross-check, isolated in its own venv (whisperx pins its own torch).
# R2 failed at "python -m venv" (ensurepip exit 1 on Kaggle) -> venv without pip + get-pip.py.
try:
    rep = json.load(open(W+"/out/ab_report.json"))
    sh("python -m venv --without-pip /tmp/wx && curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && "
       "/tmp/wx/bin/python /tmp/get-pip.py -q && /tmp/wx/bin/pip install -q whisperx 2>&1 | tail -3; "
       "/tmp/wx/bin/python -c 'import whisperx, torch; print(\"whisperx ok, torch\", torch.__version__, torch.cuda.is_available())'")
    for name in ("turbo_vote", "v3_vote"):
        rid = [x["run_id"] for x in rep["results"] if x.get("name") == name and "run_id" in x]
        if not rid:
            continue
        wj = glob.glob(f"runs/**/{rid[0]}/words.json", recursive=True)[0]
        cmd = f"timeout 1800 /tmp/wx/bin/python tools/kaggle_ab/wx_align.py samples/dwarika.mp3 {wj} {W}/out/wx_align_{name}.json"
        r2 = sh(f"{cmd} --device cuda 2>&1 | grep -v Warning | tail -15; test -s {W}/out/wx_align_{name}.json")
        if r2.returncode:
            sh(f"{cmd} --device cpu 2>&1 | grep -v Warning | tail -15")
except Exception as e:
    print("whisperx step error:", type(e).__name__, e)
for f in sum((glob.glob(f"runs/**/{n}", recursive=True) for n in ("words.json", "words_raw.json", "vote_changes.json")), []):
    shutil.copy(f, W+"/out/"+os.path.basename(os.path.dirname(f))+"_"+os.path.basename(f))
shutil.rmtree(K+"/runs", ignore_errors=True)
print("AB rc", r.returncode)
sys.exit(r.returncode)
