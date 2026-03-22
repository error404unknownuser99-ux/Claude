import subprocess
import time
import json
import os

print("🚀 GitHub Actions Internet Speed Test Starting...")
print("=" * 50)

results = {}

# Test 1: Download speed - wget se proper test
print("\n📥 Download Speed Test...")
# Use a reliable file - Ubuntu ISO from fast mirror (100MB)
test_url = "http://speedtest.tele2.net/100MB.zip"
start = time.time()
result = subprocess.run(
    ["wget", "-O", "/dev/null", "--progress=dot:mega", test_url],
    capture_output=True, text=True, timeout=60
)
elapsed = time.time() - start
output = result.stderr + result.stdout
print(output[-500:])

# Parse wget speed from output
import re
speed_match = re.search(r'(\d+\.?\d*)\s*(MB/s|KB/s|GB/s)', output)
if speed_match:
    speed_val = float(speed_match.group(1))
    unit = speed_match.group(2)
    if unit == "KB/s":
        speed_mbps = (speed_val * 8) / 1000
    elif unit == "MB/s":
        speed_mbps = speed_val * 8
    elif unit == "GB/s":
        speed_mbps = speed_val * 8000
    results['download_mbps'] = round(speed_mbps, 2)
    results['download_raw'] = f"{speed_val} {unit}"
    print(f"✅ Download Speed: {speed_mbps:.2f} Mbps ({speed_val} {unit})")
else:
    # Fallback: calculate from time
    file_size_mb = 100
    speed_mbps = (file_size_mb * 8) / elapsed if elapsed > 0 else 0
    results['download_mbps'] = round(speed_mbps, 2)
    print(f"✅ Calculated Download: {speed_mbps:.2f} Mbps (took {elapsed:.1f}s for 100MB)")

# Test 2: Ping latency
print("\n⚡ Ping Test (8.8.8.8)...")
result = subprocess.run(["ping", "-c", "5", "8.8.8.8"], capture_output=True, text=True, timeout=15)
print(result.stdout[-300:])
ping_match = re.search(r'min/avg/max.*?=\s*[\d.]+/([\d.]+)/', result.stdout)
if ping_match:
    avg_ping = float(ping_match.group(1))
    results['avg_ping_ms'] = avg_ping
    print(f"✅ Avg Ping: {avg_ping} ms")
else:
    results['avg_ping_ms'] = "N/A"

# Test 3: DNS speed
print("\n🔍 DNS Resolution Speed...")
start = time.time()
subprocess.run(["nslookup", "google.com"], capture_output=True, timeout=5)
dns_ms = (time.time() - start) * 1000
results['dns_ms'] = round(dns_ms, 2)
print(f"✅ DNS: {dns_ms:.2f} ms")

# Test 4: curl time to first byte
print("\n🌐 TTFB Test (google.com)...")
result = subprocess.run(
    ["curl", "-s", "-o", "/dev/null", "-w", "TTFB: %{time_starttransfer}s\nTotal: %{time_total}s\nSpeed: %{speed_download} bytes/s",
     "https://www.google.com"],
    capture_output=True, text=True, timeout=10
)
print(result.stdout)

# Summary
print("\n" + "=" * 50)
print("📊 FINAL RESULTS:")
print(f"  📥 Download: {results.get('download_mbps', 'N/A')} Mbps")
print(f"  ⚡ Ping:     {results.get('avg_ping_ms', 'N/A')} ms")
print(f"  🔍 DNS:      {results.get('dns_ms', 'N/A')} ms")
print("=" * 50)

os.makedirs("output", exist_ok=True)
with open("output/speed_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("✅ Results saved!")
