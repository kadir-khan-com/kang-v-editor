# Builds the 4 spelling-voter models (CT2 fp16) + hi_IN.dic ONCE into this kernel's output,
# so kang-gpu-full-test can mount them (kernel_sources) instead of converting every run (~6.5 min).
import glob, os, subprocess, sys, zipfile
W = "/kaggle/working"
z = [p for p in glob.glob("/kaggle/input/**/kang_project.zip", recursive=True) if os.path.isfile(p)]
if z:
    zipfile.ZipFile(z[0]).extractall("/tmp/src"); SV = "/tmp/src/kang/tools/setup_voters.py"
else:  # Kaggle auto-extracts dataset zips
    SV = glob.glob("/kaggle/input/**/kang/tools/setup_voters.py", recursive=True)[0]
subprocess.run("pip install -q 'transformers>=4.40' 'ctranslate2>=4.4' 2>&1 | tail -1", shell=True)
r = subprocess.run([sys.executable, SV, "--out", W + "/voters", "--tmp", "/tmp/vt"])
subprocess.run(f"du -sh {W}/voters/*; ls {W}/voters/*", shell=True)
sys.exit(r.returncode)
