#!/usr/bin/env python3
"""
Kaggle-jaisa local sandbox runner (no Docker needed).

Kaggle layout emulate karta hai:
  <root>/input/<name>/   = read-only copy of your project (jaise Kaggle Dataset)
  <root>/working/        = fresh writable copy (jaise /kaggle/working), har run me naya
Phir preflight chalata hai, phir aapka test command, aur PASS/FAIL report likhta hai.
Aapka original project kabhi modify nahi hota.
"""
import argparse, datetime, os, shutil, signal, stat, subprocess, sys, threading, time
from pathlib import Path

EXCLUDE = {".git", "__pycache__", ".venv", "venv", "node_modules", "_kaggle_sandbox", ".mypy_cache", ".pytest_cache", ".idea",
           "runs", "build_report.json", "workflow_report.json"}  # local outputs, not source (may hold this PC's paths)

def ignore(_dir, names):
    return [n for n in names if n in EXCLUDE or n.endswith(".pyc")]

def rmtree(p: Path):
    def onerr(func, path, _):
        try: os.chmod(path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
        except OSError: pass
        func(path)
    if p.exists():
        make_writable(p)
        shutil.rmtree(p, onerror=onerr)

def readonly(p: Path):
    """Best-effort read-only copy (not a security boundary on every OS)."""
    for root, dirs, files in os.walk(p, topdown=False):
        for f in files:
            try:
                path = Path(root) / f
                os.chmod(path, stat.S_IMODE(path.stat().st_mode) & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            except OSError:
                pass
        for d in dirs:
            try:
                path = Path(root) / d
                os.chmod(path, stat.S_IMODE(path.stat().st_mode) & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            except OSError:
                pass
    try:
        os.chmod(p, stat.S_IMODE(p.stat().st_mode) & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    except OSError:
        pass

def kill_tree(p):
    """Kill the shell AND its children (python, ffmpeg); p.kill() alone leaves them running."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
    else:
        try: os.killpg(p.pid, signal.SIGKILL)
        except OSError: p.kill()

def make_writable(p: Path):
    """Restore write permission so the sandbox can be cleaned/reused."""
    if not p.exists():
        return
    for root, dirs, files in os.walk(p):
        for name in dirs + files:
            try:
                path = Path(root) / name
                os.chmod(path, stat.S_IMODE(path.stat().st_mode) | stat.S_IWUSR)
            except OSError:
                pass
    try:
        os.chmod(p, stat.S_IMODE(p.stat().st_mode) | stat.S_IWUSR)
    except OSError:
        pass

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True, help="aapka project folder (e.g. E:\\AI Auto Edit)")
    ap.add_argument("--name", default="kang-project", help="dataset jaisa naam (input/<name>)")
    ap.add_argument("--cmd", default=f'"{sys.executable}" test_offline.py', help="working folder me chalne wala test command")
    ap.add_argument("--root", default=None, help="sandbox root (default: <project>/_kaggle_sandbox)")
    ap.add_argument("--keep", action="store_true", help="purana working folder mat hatao (default: har run fresh)")
    ap.add_argument("--no-preflight", action="store_true")
    ap.add_argument("--require", default="", help="comma list: python modules jo import hone hi chahiye")
    ap.add_argument("--timeout", type=int, default=1800, help="per-command timeout in seconds; hung process is terminated")
    ap.add_argument("--virtual-only", action="store_true", help="explicitly label this as a local layout simulation, not OS/container isolation")
    a = ap.parse_args()

    project = Path(a.project).resolve()
    if not project.exists():
        sys.exit(f"Project folder nahi mila: {project}")
    root = Path(a.root).resolve() if a.root else project / "_kaggle_sandbox"
    inp, work = root / "input" / a.name, root / "working"
    logs = root / "logs"; logs.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    print(f"[sandbox] root    : {root}")
    # input = frozen dataset copy
    rmtree(inp); shutil.copytree(project, inp, ignore=ignore); readonly(inp)
    # working = fresh copy (Kaggle jaisa ephemeral)
    if not a.keep: rmtree(work)
    if not work.exists(): shutil.copytree(inp, work, ignore=ignore, copy_function=shutil.copyfile)
    make_writable(work)
    print(f"[sandbox] input   : {inp}  (read-only)")
    print(f"[sandbox] working : {work}  ({'kept' if a.keep else 'fresh'})")

    env = os.environ.copy()
    env.update({
        "KAGGLE_KERNEL_RUN_TYPE": "Interactive",
        "KAGGLE_URL_BASE": "https://www.kaggle.com",
        "KAGGLE_ROOT": str(root),
        "KAGGLE_INPUT": str(root / "input"),
        "KAGGLE_WORKING": str(work),
        "ENGINE_BASE_DIR": str(work),            # Kang: engine base dir (Kaggle par /kaggle/working/ai-video-engine)
        "KAGGLE_INPUT_DIR": str(root / "input"),  # Kang: audio dataset yahin dhundhta hai (Kaggle par /kaggle/input)
        "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log = logs / f"run_{stamp}.log"
    steps = []

    def step(name, cmd):
        print(f"\n===== {name} =====\n$ {cmd}")
        started = time.time()
        with open(log, "a", encoding="utf-8") as lf:
            lf.write(f"\n===== {name} =====\n$ {cmd}\n")
            # Live output + real timeout: a reader thread streams lines to screen/log,
            # the main thread waits with a deadline and kills the whole process tree.
            kwargs = dict(shell=True, cwd=work, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1)
            if os.name == "nt":
                kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            else:
                kwargs["start_new_session"] = True
            p = subprocess.Popen(cmd, **kwargs)

            def pump():
                for line in p.stdout:
                    sys.stdout.write(line); sys.stdout.flush()
                    lf.write(line); lf.flush()

            reader = threading.Thread(target=pump, daemon=True)
            reader.start()
            try:
                rc = p.wait(timeout=max(1, a.timeout))
            except subprocess.TimeoutExpired:
                kill_tree(p)
                p.wait()
                rc = 124
            reader.join(timeout=10)  # a grandchild still holding the pipe must not hang the kit
            if rc == 124:
                msg = f"\n[TIMEOUT] Command exceeded {a.timeout} seconds and was terminated.\n"
                print(msg, end=""); lf.write(msg)
        elapsed = time.time() - started
        steps.append((name, rc, elapsed))
        return rc

    ok = True
    if not a.no_preflight:
        pre = Path(__file__).with_name("kaggle_preflight.py")
        rc = step("PREFLIGHT", f'"{sys.executable}" "{pre}" --project "{work}" --require "{a.require}"')
        ok &= rc == 0
    if ok:
        ok &= step("TEST", a.cmd) == 0
    else:
        print("\nPreflight FAIL, isliye test skip hua. Pehle preflight fix karo.")

    print("\n================ KAGGLE-LOCAL REPORT ================")
    for n, rc, d in steps:
        print(f"{'PASS' if rc == 0 else 'FAIL'}  {n:10} rc={rc} {d:6.1f}s")
    print(f"Log     : {log}")
    print(f"Outputs : {work}  (yahi 'kaggle/working' hai)")
    print(f"RESULT  : {'PASS - local checks passed (Kaggle/GPU separately verify)' if ok else 'FAIL'}   ({time.time()-t0:.0f}s)")
    if a.virtual_only:
        print("NOTE    : Virtual layout simulation is not a hardened sandbox; run untrusted code only in a real VM/container.")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
