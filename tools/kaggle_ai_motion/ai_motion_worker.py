"""KANG v17 AI motion worker (one per GPU). Shipped inside the input dataset; started by ai_motion_run.py.
Wan2.2-TI2V-5B (Apache-2.0) image-to-video via diffusers WanImageToVideoPipeline, transformer fp16 streamed from CPU
(group offload, block level), VAE fp32 (tiling) on the GPU, text encoder NOT loaded (prompt embeddings pre-computed by
the kernel). Writes raw/<job>.mp4 (job width x height, 24 fps, libx264 crf 12) + worker_<gpu>.json."""
import argparse, json, os, subprocess, sys, time, traceback

ap = argparse.ArgumentParser()
ap.add_argument("--gpu", type=int, required=True)
ap.add_argument("--jobs", required=True)
ap.add_argument("--embeds", required=True)
ap.add_argument("--model", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--ids", required=True)
ap.add_argument("--ready", required=True, help="file touched once the model is on the GPU")
a = ap.parse_args()

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
import numpy as np
import torch
from PIL import Image

rep = {"gpu": a.gpu, "jobs": [], "t0": time.time()}


def save():
    json.dump(rep, open(os.path.join(a.out, f"worker_{a.gpu}.json"), "w"), indent=1, default=str)


try:
    from diffusers import AutoencoderKLWan, WanImageToVideoPipeline, WanTransformer3DModel
    t = time.time()
    # v1 (kernel version 1): transformer fp16 + VAE fp32 resident on the GPU = 12.85 GB -> OOM in the first denoising
    # step on a 15 GB T4. v2: load on CPU and use model CPU offload (only the active component sits on the GPU).
    tr = WanTransformer3DModel.from_pretrained(a.model, subfolder="transformer", torch_dtype=torch.float16,
                                               low_cpu_mem_usage=True)
    vae = AutoencoderKLWan.from_pretrained(a.model, subfolder="vae", torch_dtype=torch.float32)
    vae.enable_tiling()
    for fn in ("enable_slicing",):
        try:
            getattr(vae, fn)()
        except Exception:
            pass
    pipe = WanImageToVideoPipeline.from_pretrained(a.model, transformer=tr, vae=vae, text_encoder=None, tokenizer=None,
                                                   image_encoder=None, image_processor=None, torch_dtype=torch.float16)
    # v3 (KANG_017): v1 (all resident) and v2 (enable_model_cpu_offload: the whole 10 GB fp16 transformer on the GPU
    # during denoising) both OOMed on a 15 GB T4. Now the transformer is streamed block by block from CPU RAM
    # (diffusers group offload, block level, CUDA stream prefetch) so only ~1-2 blocks + activations sit on the GPU;
    # the VAE (fp32, tiled) stays on the GPU. Smaller model size (1024x576) cuts the per-token fp32 timestep tensor.
    mode = os.environ.get("KANG_OFFLOAD", "group_block")
    if mode == "group_block":
        try:
            tr.enable_group_offload(onload_device=torch.device("cuda"), offload_device=torch.device("cpu"),
                                    offload_type="block_level", num_blocks_per_group=1, use_stream=True,
                                    low_cpu_mem_usage=True)
        except TypeError:  # older signature without low_cpu_mem_usage
            tr.enable_group_offload(onload_device=torch.device("cuda"), offload_device=torch.device("cpu"),
                                    offload_type="block_level", num_blocks_per_group=1, use_stream=True)
        vae.to("cuda")
        rep["load_mode"] = "transformer group offload (block_level, stream) + VAE fp32 tiled on GPU"
    else:
        pipe.enable_model_cpu_offload()
        rep["load_mode"] = "cpu + enable_model_cpu_offload"
    pipe.set_progress_bar_config(disable=True)
    rep["load_s"] = round(time.time() - t, 1)
    rep["vram_after_load_gb"] = round(torch.cuda.memory_allocated() / 1e9, 2)
    rep["pipe_config"] = {k: str(v) for k, v in dict(pipe.config).items() if not k.startswith("_")}
except Exception:
    rep["load_error"] = traceback.format_exc()[-3000:]
    save()
    open(a.ready, "w").write("fail")
    sys.exit(1)
open(a.ready, "w").write("ok")
save()

E = torch.load(a.embeds)
jobs = {j["id"]: j for j in json.load(open(a.jobs))["jobs"]}
base = os.path.dirname(a.jobs)
for jid in a.ids.split(","):
    j = jobs[jid]
    r = {"id": jid, "gpu": a.gpu, "num_frames": j["num_frames"], "steps": j["steps"]}
    t = time.time()
    torch.cuda.reset_peak_memory_stats()
    try:
        img = Image.open(os.path.join(base, j["input"])).convert("RGB")
        g = torch.Generator(device="cuda").manual_seed(int(j["seed"]))
        pe = E[j["prompt"]].to("cuda", torch.float16)
        ne = E[j["negative"]].to("cuda", torch.float16)
        out = pipe(image=img, prompt_embeds=pe, negative_prompt_embeds=ne, height=j["height"], width=j["width"],
                   num_frames=j["num_frames"], num_inference_steps=j["steps"], guidance_scale=j["guidance"],
                   generator=g, output_type="np").frames[0]
        fr = np.asarray(out)
        r["nan"] = bool(np.isnan(fr).any())
        r["nan_frac"] = round(float(np.isnan(fr).mean()), 6)
        fr = np.nan_to_num(fr)
        r["mean"] = round(float(fr.mean()), 4)
        u8 = (np.clip(fr, 0, 1) * 255 + 0.5).astype(np.uint8)
        r["shape"] = list(u8.shape)
        dst = os.path.join(a.out, f"{jid}.mp4")
        h, w = u8.shape[1:3]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                              "-r", str(j["fps"]), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "12",
                              "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
        p.stdin.write(u8.tobytes()); p.stdin.close(); r["ffmpeg_rc"] = p.wait()
        r["ok"] = r["ffmpeg_rc"] == 0 and not r["nan"] and r["mean"] > 0.01
    except Exception:
        r["ok"] = False
        r["error"] = traceback.format_exc()[-2500:]
        torch.cuda.empty_cache()
    r["seconds"] = round(time.time() - t, 1)
    r["peak_vram_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 2)
    r["peak_reserved_gb"] = round(torch.cuda.max_memory_reserved() / 1e9, 2)
    try:
        import resource
        r["max_rss_gb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 2)
    except Exception:
        pass
    rep["jobs"].append(r)
    print(json.dumps(r)[:500], flush=True)
    save()
rep["elapsed_s"] = round(time.time() - rep["t0"], 1)
save()
