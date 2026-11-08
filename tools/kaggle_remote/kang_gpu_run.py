import os, sys, glob, json, shutil, subprocess, time, zipfile
def sh(c, check=False):
    print(f"\n$ {c}", flush=True); t=time.time()
    r = subprocess.run(c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    print(r.stdout[-6000:], flush=True); print(f"[rc={r.returncode} {time.time()-t:.1f}s]", flush=True)
    if check and r.returncode: sys.exit(f"FAILED: {c}")
    return r
print("inputs:", [p for p in glob.glob("/kaggle/input/**", recursive=True) if os.path.isfile(p)][:50])
W = "/kaggle/working"; os.chdir(W)
z = glob.glob("/kaggle/input/**/kang_project.zip", recursive=True)
if z: zipfile.ZipFile(z[0]).extractall(W)
else: shutil.copytree(glob.glob("/kaggle/input/**/kang_project.zip/kang", recursive=True)[0] if glob.glob("/kaggle/input/**/kang_project.zip/kang", recursive=True) else glob.glob("/kaggle/input/**/kang", recursive=True)[0], W+"/kang")
K = W + "/kang"; os.chdir(K); os.makedirs("samples", exist_ok=True)
shutil.copy(glob.glob("/kaggle/input/**/dwarika.mp3", recursive=True)[0], "samples/dwarika.mp3")
sh("nvidia-smi"); sh("ffmpeg -hide_banner -version | head -3; ffmpeg -hide_banner -filters | grep -E ' (ass|subtitles) '")
sh("pip install -q 'faster-whisper>=1.0' 'pydantic>=2.5,<3' fonttools pytest 2>&1 | tail -3")
sh("python -c \"import ctranslate2;print('ctranslate2',ctranslate2.__version__,'cuda',ctranslate2.get_cuda_device_count())\"")
sh("python build_and_check.py", check=True)
t = time.time()
# spelling voter (default ON once set up): 4 Hindi models -> CT2 fp16 + hi_IN wordlist
pre = glob.glob("/kaggle/input/**/voters/vaani/model.bin", recursive=True)
if pre:  # prebuilt by kernel kang-voter-models
    os.environ["KANG_VOTER_DIR"] = os.path.dirname(os.path.dirname(pre[0])); print("prebuilt voters:", os.environ["KANG_VOTER_DIR"])
else:
    sh("pip install -q 'transformers>=4.40' 2>&1 | tail -1")
    sh("python tools/setup_voters.py --out /tmp/voters --tmp /tmp/vt 2>&1 | grep -v Warning | tail -12")
    os.environ["KANG_VOTER_DIR"] = "/tmp/voters"
r = sh("python kang.py workflow samples/dwarika.mp3 --full --device cuda --yes")
print(f"WORKFLOW rc={r.returncode} wall={time.time()-t:.1f}s", flush=True)
os.makedirs(W+"/out", exist_ok=True)
for f in glob.glob("runs/**/vote_changes.json", recursive=True):
    shutil.copy(f, W+"/out/vote_changes.json")
for f in glob.glob("runs/**/manifest.json", recursive=True):
    t_ = open(f, encoding="utf-8").read()
    if "voter_alt_passes" in t_ or "transcribe" in t_: shutil.copy(f, W+"/out/"+os.path.basename(os.path.dirname(f))+"_manifest.json")
for f in glob.glob("runs/**/workflow_report.json", recursive=True): print(f); print(open(f, encoding="utf-8").read()[:8000]); shutil.copy(f, W+"/out/workflow_report.json")
for f in glob.glob("runs/**/*.mp4", recursive=True): print(f, os.path.getsize(f)); shutil.copy(f, W+"/out/"+os.path.basename(os.path.dirname(f))+"_"+os.path.basename(f))
for f in glob.glob("runs/**/*.words.json", recursive=True)+glob.glob("runs/**/words.json", recursive=True)+glob.glob("runs/**/*.ass", recursive=True)+glob.glob("runs/**/speech_gaps.json", recursive=True)+glob.glob("runs/**/glossary_changes.json", recursive=True): shutil.copy(f, W+"/out/"+os.path.basename(os.path.dirname(f))+"_"+os.path.basename(f))
shutil.rmtree(K+"/runs", ignore_errors=True)
sys.exit(r.returncode)
