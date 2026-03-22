import os, subprocess
from datetime import datetime

LOG_FILE = "output/runtimelogs.txt"
os.makedirs("output", exist_ok=True)

def log(msg):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except:
        return "N/A"

log("🔍 GitHub Actions Runner Specs")
log("=" * 50)

# CPU
log(f"🖥️  CPU Model   : {run('cat /proc/cpuinfo | grep \"model name\" | head -1 | cut -d: -f2')}")
log(f"🖥️  CPU Cores   : {run('nproc')}")
log(f"🖥️  CPU Threads : {run('lscpu | grep \"^CPU(s)\" | awk \"{print $2}\"')}")

# RAM
log(f"💾 Total RAM   : {run('free -h | grep Mem | awk \"{print $2}\"')}")
log(f"💾 Free RAM    : {run('free -h | grep Mem | awk \"{print $4}\"')}")

# Storage
log(f"💿 Total Disk  : {run('df -h / | tail -1 | awk \"{print $2}\"')}")
log(f"💿 Free Disk   : {run('df -h / | tail -1 | awk \"{print $4}\"')}")

# OS
log(f"🐧 OS          : {run('lsb_release -d | cut -d: -f2')}")
log(f"🐧 Kernel      : {run('uname -r')}")

# Network
log(f"🌐 IP Address  : {run('curl -s ifconfig.me')}")

log("=" * 50)
log("✅ Done!")
