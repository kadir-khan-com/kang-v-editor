import glob, json, os, subprocess, sys
def sh(c):
    print("$", c, flush=True); r = subprocess.run(c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(r.stdout[-6000:], "[rc=%d]" % r.returncode, flush=True); return r
I = "/kaggle/input"; O = "/kaggle/working/out"; os.makedirs(O, exist_ok=True)
audio = glob.glob(I + "/**/dwarika.mp3", recursive=True)[0]
src = glob.glob(I + "/**/wx_align.py", recursive=True)
script = src[0] if src else os.path.join(os.path.dirname(os.path.abspath(__file__)), "wx_align.py")
sh("pip install -q whisperx 2>&1 | tail -2; python -c 'import whisperx, torch; print(torch.__version__, torch.cuda.is_available())'")
for name in ("turbo_vote", "v3_vote"):
    wj = glob.glob(I + f"/**/r3_{name}_words.json", recursive=True)[0]
    r = sh(f"python {script} {audio} {wj} {O}/wx_align_{name}.json --device cuda 2>&1 | grep -v Warning | tail -8")
