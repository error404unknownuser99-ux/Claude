"""
log_gen.py — Auto-push logger (Python)
Usage:
    from log_generators.log_gen import start, log, stop
    start()
    log("kuch bhi")
    stop()
"""
import os, subprocess, threading, hashlib
from datetime import datetime, timezone

_WS       = os.environ.get("GITHUB_WORKSPACE", ".")
_OUT      = f"{_WS}/output"
_RUNTIME  = f"{_OUT}/runtimelogs.txt"
_DETAILED = f"{_OUT}/detailedlog.txt"
_stop     = threading.Event()
_lock     = threading.Lock()
_last_h   = None

# ── helpers ────────────────────────────────────────────────────────────
def _ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def _hash():
    c = ""
    for f in [_RUNTIME, _DETAILED]:
        try: c += open(f).read()
        except: pass
    return hashlib.md5(c.encode()).hexdigest()

def _git(*args):
    return subprocess.run(["git"] + list(args), cwd=_WS,
                          capture_output=True)

def _push():
    global _last_h
    with _lock:
        h = _hash()
        if h == _last_h: return          # kuch badla nahi — skip!
        _last_h = h
        _git("add", "output/")
        if _git("diff", "--staged", "--quiet").returncode == 0: return
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        _git("commit", "-m", f"🔄 {ts}")
        _git("pull", "--rebase", "origin", "main")
        _git("push")

def _loop():
    while not _stop.wait(5):
        _push()

# ── public API ─────────────────────────────────────────────────────────
def log(msg, level="INFO"):
    os.makedirs(_OUT, exist_ok=True)
    line = f"[{_ts()}] [{level}] {msg}"
    print(line, flush=True)
    with open(_RUNTIME, "a") as f:
        f.write(line + "\n")

def start():
    os.makedirs(_OUT, exist_ok=True)
    log("🚀 LogGen started!")
    threading.Thread(target=_loop, daemon=True).start()

def stop():
    _stop.set()
    log("🏁 LogGen stopped — final push...")
    _push()
