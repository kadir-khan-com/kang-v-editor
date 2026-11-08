# Kaggle-jaisa LOCAL test kit (Kaggle par upload kiye bina)

Problem: Kaggle upload ke files limit khatam hote hi delete ho jaate hain, to testing adhoori rehti hai.
Solution: apne PC par (VS Code se) wahi layout + checks chalao. Kaggle par sirf final, pehle se pass hua project jaye.

## Kaggle ka layout jo ye kit banata hai
- `input/<name>/`  = read-only dataset (aapka project ka frozen copy)
- `working/`       = har run me FRESH writable folder (jaise /kaggle/working)
- Env vars: KAGGLE_KERNEL_RUN_TYPE, KAGGLE_INPUT, KAGGLE_WORKING
Aapka original project kabhi modify nahi hota. Sab `_kaggle_sandbox/` me hota hai.

## Mode 1: Virtual layout simulation (Docker ke bina; sabse tez)
Project folder me ye kit folder copy karo, phir VS Code terminal me:

    python kaggle_local_kit\kaggle_local.py --project "E:\AI Auto Edit" --virtual-only --require numpy,pydantic,PIL,fontTools,pytest --cmd "python build_and_check.py"

Kya hota hai: project ki frozen input copy -> fresh writable working copy -> PREFLIGHT -> test command -> PASS/FAIL report + log. Timeout ab command ke dauran enforce hota hai; stuck process terminate hota hai.
Useful flags: `--require librosa,faster_whisper` (ye modules na ho to FAIL), `--keep` (working purana rakho), `--timeout 3600`.

**Important limitation:** ye virtual Kaggle folder-layout simulation hai, full virtual machine ya security sandbox nahi. Ye host ke installed Python/FFmpeg aur OS ko use karta hai. Untrusted code ke liye Docker/VM use karo. Read-only permissions OS ke hisaab se best-effort hain. `_kaggle_sandbox` ko haath se delete karna ho to pehle write permission wapas do (Windows: `attrib -R /S /D _kaggle_sandbox\*`, Linux: `chmod -R u+w _kaggle_sandbox`), warna "Permission denied" aayega. Kit khud agle run me ise saaf kar leta hai.

## Mode 2: Docker (Kaggle ke aur kareeb: Linux + ffmpeg + fonts, Windows se alag)
Docker ki abhi zaroorat nahi agar tum sirf logic/tests aur Kaggle-like folder layout check karna chahte ho. Linux compatibility ya isolation check ke liye Docker phir bhi useful hai.
Windows me asli fark ye hai ki Kaggle Linux hai (paths, fonts, ffmpeg build). Isliye Docker zyada sach batata hai.
1. Docker Desktop install (WSL2 on).
2. PowerShell:  `.\kaggle_local_kit\docker\run_docker.ps1 -Project "E:\AI Auto Edit" -Cmd "python build_and_check.py"`
   - `-Offline`  = Kaggle "Internet off" jaisa (network band). Ek baar image ban chuki ho tab use karo.
   - `-Gpu`      = NVIDIA GPU ho to (Docker Desktop + NVIDIA toolkit).
   - `-Rebuild`  = requirements badle to image dobara bano.
3. Pehli build me kuch minute lagte hain (ffmpeg, Noto fonts, Tesseract Hindi, Python libs).
**Exact Kaggle image** (bahut bada, 20GB+): `gcr.io/kaggle-images/python` (CPU) ya `gcr.io/kaggle-gpu-images/python` (GPU).
Use karne ke liye `docker run --rm -v "E:\AI Auto Edit:/kaggle/input/kang-project:ro" <image> bash -lc "cp -a /kaggle/input/kang-project/. /kaggle/working/ && cd /kaggle/working && python test_offline.py"`.
(Pull hota hai ya nahi, ye aapke PC par verify karna hoga.)

## "Kaggle-ready" ka matlab (checklist)
1. Virtual layout mode PASS aur Docker mode PASS (dono), jab Linux compatibility required ho.
2. Mode 2 `-Offline` PASS (agar Kaggle par internet off rakhna hai).
3. Paths: code me koi `E:\...` nahi. Config me `INPUT_DIR`/`WORKING_DIR` env se lo:
   `WORK = Path(os.environ.get("KAGGLE_WORKING", "./working"))`; `INPUT = Path(os.environ.get("KAGGLE_INPUT", "./input"))`
4. GPU code ke liye CPU fallback (`device="cpu", compute_type="int8"` offline test me, chhota model).
5. Output sirf working folder me likho; input me kabhi nahi (Kaggle me read-only).
6. Versions: Kaggle notebook me ek baar `!pip freeze > /kaggle/working/kaggle_freeze.txt` karke `requirements-kaggle.txt` me pin karo.

## Limit problem ka permanent fix (GitHub ke bina)
Local PASS ke baad project ko Kaggle par **ek baar private Dataset** ke roop me upload karo (`generate_bundle.py` ka output).
Dataset Kaggle par permanent rehta hai; notebook ke `/kaggle/working` ki tarah delete nahi hota. Notebook me bas "Add Data" se attach karo.
Update: sirf nayi version (`kaggle datasets version`), pura project baar-baar upload nahi.

## Kya ye kit pakad nahi sakta (honestly)
- Kaggle GPU ki asli speed/VRAM limit aur session time limit.
- Kaggle image ke exact library versions (freeze se hi match hoga).
- Aapke project ke andar ki logic bugs: wo aapke `test_offline.py` se pakde jayenge, kit sirf environment sahi karta hai.

## Kang project ke liye (is kit me pehle se set)
- Kit `ENGINE_BASE_DIR` aur `KAGGLE_INPUT_DIR` set karta hai (project ka fixed version inhe padhta hai), isliye Windows par bhi Docker ke bina chalta hai.
- Docker mode project ko `/kaggle/working/ai-video-engine` me rakhta hai, bilkul asli Kaggle path.
- Test command: `python build_and_check.py` (files -> syntax -> env -> test_offline -> pytest -> bundle sync).
