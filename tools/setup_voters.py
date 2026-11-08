"""Set up the default spelling-voter models (config/voters.json) as CTranslate2 fp16 + the Hindi wordlist.
Needs: pip install transformers ctranslate2 (+ torch), internet, ~10 GB temp disk. Run once per machine:
    python tools/setup_voters.py --out models/voters        (or set KANG_VOTER_DIR to the same dir)
Sources: ARTPARK-IISc/whisper-large-v3-vaani-hindi, collabora/whisper-medium-hindi,
AI4Bharat IndicWhisper (vistaar, MIT) hindi_models.zip, LibreOffice hi_IN dictionary."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, urllib.request, zipfile

HF = {"vaani": "ARTPARK-IISc/whisper-large-v3-vaani-hindi", "medium": "collabora/whisper-medium-hindi"}
IW_ZIP = "https://indicwhisper.objectstore.e2enetworks.net/hindi_models.zip"
IW = {"indic": "whisper-medium-hi_alldata_multigpu", "indic_large": "whisper-large-hi-noldcil"}
DIC = "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/hi_IN/hi_IN.dic"


LIC = json.loads((pathlib.Path(__file__).resolve().parents[1] / "config" / "model_licenses.json").read_text(encoding="utf-8"))


def _rev(name: str):
    """Pinned HF revision from config/model_licenses.json (None for non-HF sources)."""
    v = LIC["voters"].get(name, {})
    return v.get("revision") if v.get("source", "").startswith("hf:") else None


def _sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_manifest(out: pathlib.Path) -> pathlib.Path:
    """MANIFEST.json: licence/source/revision + sha256 of every file per voter (Roadmap §11.2)."""
    man = {"wordlist": dict(LIC["wordlist"], sha256=_sha256(out / "hi_IN.dic")) if (out / "hi_IN.dic").exists() else None,
           "voters": {}}
    for n, meta in LIC["voters"].items():
        d = out / n
        if (d / "model.bin").exists():
            man["voters"][n] = dict(meta, files={f.name: _sha256(f) for f in sorted(d.iterdir()) if f.is_file()})
    mp = out / "MANIFEST.json"
    mp.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    return mp


def convert(src: str, out: pathlib.Path, revision=None) -> None:
    from transformers import WhisperTokenizerFast
    if revision:  # pin the exact HF revision recorded in config/model_licenses.json
        from huggingface_hub import snapshot_download
        src = snapshot_download(src, revision=revision)
    subprocess.run(["ct2-transformers-converter", "--model", src, "--output_dir", str(out), "--quantization",
                    "float16", "--copy_files", "preprocessor_config.json", "--force"], check=True)
    try:
        tok = WhisperTokenizerFast.from_pretrained(src)
    except Exception:  # IndicWhisper checkpoints ship without tokenizer files: same vocab as the base model
        mel = json.loads((pathlib.Path(src) / "config.json").read_text()).get("num_mel_bins", 80)
        tok = WhisperTokenizerFast.from_pretrained("openai/whisper-large-v3" if mel == 128 else
                                                   "openai/whisper-large-v2" if "large" in src else "openai/whisper-medium")
    tok.save_pretrained(str(out))
    print("ok", out, flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parents[1] / "models" / "voters"))
    ap.add_argument("--tmp", default="/tmp/kang_voter_tmp")
    ap.add_argument("--only", help="comma list of voter names")
    a = ap.parse_args()
    out, tmp = pathlib.Path(a.out), pathlib.Path(a.tmp)
    out.mkdir(parents=True, exist_ok=True); tmp.mkdir(parents=True, exist_ok=True)
    want = set(a.only.split(",")) if a.only else set(HF) | set(IW)
    if not (out / "hi_IN.dic").exists():
        urllib.request.urlretrieve(DIC, out / "hi_IN.dic")
    for n, repo in HF.items():
        if n in want and not (out / n / "model.bin").exists():
            convert(repo, out / n, revision=_rev(n))
    need_iw = [n for n in IW if n in want and not (out / n / "model.bin").exists()]
    if need_iw:
        z = tmp / "hindi_models.zip"
        if not z.exists():
            print("downloading IndicWhisper (4.3 GB)...", flush=True)
            urllib.request.urlretrieve(IW_ZIP, z)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(tmp / "iw")
        z.unlink()
        for n in need_iw:
            src = next((tmp / "iw").rglob(IW[n] + "/config.json")).parent
            convert(str(src), out / n)
        shutil.rmtree(tmp / "iw", ignore_errors=True)
    have = [n for n in sorted(want) if (out / n / "model.bin").exists()]
    print("voters ready:", have, "in", out, "| manifest:", write_manifest(out))
    return 0 if len(have) == len(want) else 1


if __name__ == "__main__":
    sys.exit(main())
