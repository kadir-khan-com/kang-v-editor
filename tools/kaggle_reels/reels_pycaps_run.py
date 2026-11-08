"""Kaggle CPU kernel: render KANG pycaps styles (pycaps MIT @ e2d36ed, PictexSubtitleRenderer, no browser).
Input dataset kang-reels-input: input_9x16_160s.mp4, transcript_whisper.json, <style>_template/ dirs.
Output (/kaggle/working): reel_<style>.mp4 + reels_report.json. Nothing published."""
import glob, json, os, shutil, subprocess, sys, time, traceback

W = "/kaggle/working"
rep = {"steps": [], "renders": []}

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    rep["steps"].append({"cmd": cmd, "rc": r.returncode, "tail": (r.stdout + r.stderr)[-600:]})
    return r.returncode

sh("pip install -q https://github.com/francozanardi/pycaps/archive/e2d36edfa08e3307d65b15bb20f17399dc2c9b40.zip html2pic")
try:
    import html2pic  # noqa
except ImportError:
    sh("apt-get update -qq && apt-get install -y -qq libegl1 libgl1 libgles2 fonts-dejavu-core")
src = glob.glob("/kaggle/input/**/input_9x16_160s.mp4", recursive=True)[0]
base = os.path.dirname(src)
rep["input_dir"] = base
rep["input_files"] = sorted(glob.glob(os.path.join(base, "**"), recursive=True))[:40]
for z in glob.glob(os.path.join(base, "*_template.zip")):
    d = os.path.join(W, "_in", os.path.basename(z)[:-4])
    shutil.unpack_archive(z, d)
tdirs = sorted(glob.glob(os.path.join(base, "*_template")) + glob.glob(os.path.join(W, "_in", "*_template")))
from pycaps import JsonConfigLoader, PictexSubtitleRenderer

for tdir in tdirs:
    style = os.path.basename(tdir)[:-len("_template")]
    work_t = os.path.join(W, "_t_" + style)
    shutil.copytree(tdir, work_t, dirs_exist_ok=True)
    if not os.path.exists(os.path.join(work_t, "pycaps.template.json")):  # zip may nest one level
        work_t = os.path.dirname(glob.glob(os.path.join(work_t, "**", "pycaps.template.json"), recursive=True)[0])
    out = os.path.join(W, f"reel_{style}.mp4")  # draft/non-draft naming is done by KANG when copying back
    t0 = time.time()
    e = {"style": style}
    try:
        b = JsonConfigLoader(os.path.join(work_t, "pycaps.template.json")).load(False)
        b.with_input_video(src)
        b.with_custom_subtitle_renderer(PictexSubtitleRenderer())
        b.with_transcription_file(os.path.join(base, "transcript_whisper.json"), "whisper_json")
        b.with_output_video(out)
        b.build().run()
        e["ok"] = os.path.exists(out)
    except Exception:
        e["ok"] = False
        e["error"] = traceback.format_exc()[-2500:]
    e["seconds"] = round(time.time() - t0, 1)
    rep["renders"].append(e)
    shutil.rmtree(work_t, ignore_errors=True)
    print(style, e["ok"], e["seconds"], flush=True)

shutil.rmtree(os.path.join(W, "_in"), ignore_errors=True)
json.dump(rep, open(os.path.join(W, "reels_report.json"), "w"), indent=2)
print(json.dumps(rep["renders"], indent=1))
