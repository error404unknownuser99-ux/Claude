import subprocess
import time
import json
import os

print("🚀 GitHub Actions Internet Speed Test Starting...")
print("=" * 50)

results = {}

# Test 1: Download speed using curl (100MB file from fast.com CDN)
print("\n📥 Download Speed Test (100MB file)...")
start = time.time()
result = subprocess.run(
    ["curl", "-o", "/dev/null", "-s", "-w", "%{speed_download}",
     "https://speed.cloudflare.com/__down?bytes=104857600"],
    capture_output=True, text=True, timeout=60
)
elapsed = time.time() - start
if result.returncode == 0:
    speed_bps = float(result.stdout.strip())
    speed_mbps = (speed_bps * 8) / 1_000_000
    results['download_mbps'] = round(speed_mbps, 2)
    print(f"✅ Download Speed: {speed_mbps:.2f} Mbps")
    print(f"   Time taken: {elapsed:.2f}s")
else:
    results['download_mbps'] = "Error"
    print(f"❌ Error: {result.stderr}")

# Test 2: Upload speed test
print("\n📤 Upload Speed Test (10MB)...")
# Generate 10MB of data and upload
start = time.time()
result = subprocess.run(
    ["curl", "-s", "-w", "%{speed_upload}", "-X", "POST",
     "--data-binary", "@/dev/urandom",
     "-o", "/dev/null",
     "--max-time", "10",
     "https://speed.cloudflare.com/__up"],
    capture_output=True, text=True, timeout=15
)
elapsed = time.time() - start
if result.returncode == 0 and result.stdout.strip():
    speed_bps = float(result.stdout.strip())
    speed_mbps = (speed_bps * 8) / 1_000_000
    results['upload_mbps'] = round(speed_mbps, 2)
    print(f"✅ Upload Speed: {speed_mbps:.2f} Mbps")
else:
    # Alternative upload test
    result2 = subprocess.run(
        ["curl", "-s", "-w", "%{speed_upload}",
         "-F", "file=@/etc/hostname",
         "-o", "/dev/null",
         "https://httpbin.org/post"],
        capture_output=True, text=True, timeout=15
    )
    if result2.returncode == 0:
        speed_bps = float(result2.stdout.strip() or "0")
        speed_mbps = (speed_bps * 8) / 1_000_000
        results['upload_mbps'] = round(speed_mbps, 2)
        print(f"✅ Upload Speed: {speed_mbps:.2f} Mbps")
    else:
        results['upload_mbps'] = "N/A"
        print("⚠️ Upload test skipped")

# Test 3: Latency/Ping test
print("\n⚡ Latency Test (ping to google.com)...")
result = subprocess.run(
    ["ping", "-c", "5", "google.com"],
    capture_output=True, text=True, timeout=15
)
if result.returncode == 0:
    lines = result.stdout.split('\n')
    for line in lines:
        if 'avg' in line or 'rtt' in line:
            # Extract avg ping
            parts = line.split('/')
            if len(parts) >= 5:
                avg_ping = parts[4]
                results['avg_ping_ms'] = float(avg_ping)
                print(f"✅ Avg Ping: {avg_ping} ms")
    print(result.stdout)
else:
    results['avg_ping_ms'] = "N/A"
    print("❌ Ping failed")

# Test 4: DNS resolution speed
print("\n🔍 DNS Resolution Speed...")
start = time.time()
result = subprocess.run(
    ["nslookup", "google.com"],
    capture_output=True, text=True, timeout=5
)
dns_time = (time.time() - start) * 1000
results['dns_ms'] = round(dns_time, 2)
print(f"✅ DNS Resolution: {dns_time:.2f} ms")

# Summary
print("\n" + "=" * 50)
print("📊 FINAL RESULTS:")
print(f"  📥 Download: {results.get('download_mbps', 'N/A')} Mbps")
print(f"  📤 Upload:   {results.get('upload_mbps', 'N/A')} Mbps")
print(f"  ⚡ Ping:     {results.get('avg_ping_ms', 'N/A')} ms")
print(f"  🔍 DNS:      {results.get('dns_ms', 'N/A')} ms")
print("=" * 50)

# Save results
os.makedirs("output", exist_ok=True)
with open("output/speed_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\n✅ Results saved to output/speed_results.json")
