import time, sys, os, platform
sys.path.insert(0, os.environ.get("GITHUB_WORKSPACE", "."))
from log_generators.log_gen import start, log, stop

start()

# ── Test 1: Basic logging ──────────────────────────────────────
log("=" * 50)
log("🧪 LOG_GEN KADAK TEST SHURU!")
log("=" * 50)

# ── Test 2: System info ────────────────────────────────────────
log("📦 System Info:")
log(f"  Python  : {sys.version.split()[0]}")
log(f"  OS      : {platform.system()} {platform.release()}")
log(f"  CPU     : {os.cpu_count()} cores")

# ── Test 3: 5-sec auto-push test ──────────────────────────────
log("⏱️  5-sec auto-push test shuru (30 sec)...")
for i in range(1, 7):
    log(f"  🔄 Chunk {i}/6 — {i*5} sec ho gaye")
    time.sleep(5)
log("✅ Auto-push test khatam!")

# ── Test 4: Heavy computation ──────────────────────────────────
log("🔢 Heavy computation shuru...")
result = sum(i**2 for i in range(1_000_000))
log(f"  Sum of squares (0-999999) = {result}")

# ── Test 5: Error levels ───────────────────────────────────────
log("⚠️  Error level test:")
log("  Ye ek warning hai!", "WARN")
log("  Ye ek error hai!", "ERROR")
log("  Wapas normal!", "INFO")

# ── Test 6: Hash change check ──────────────────────────────────
log("🔍 Same message push skip test:")
log("  Same message!", "INFO")
log("  Same message!", "INFO")
time.sleep(6)
log("  Alag message — ab push hoga! ✅")

# ── Test 7: pip install ────────────────────────────────────────
log("📥 pip install test...")
ret = os.system("pip install httpx -q")
log(f"  httpx install: {'✅ OK' if ret == 0 else '❌ FAIL'}")

# ── Final ──────────────────────────────────────────────────────
log("=" * 50)
log("🎉 SAARE TESTS COMPLETE!")
log("=" * 50)

stop()
