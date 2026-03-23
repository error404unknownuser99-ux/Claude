import time
from datetime import datetime

print(f"  Script start time: {datetime.utcnow().strftime('%H:%M:%S UTC')}")
print("  Calculating something...")
total = sum(i**2 for i in range(1000))
print(f"  Result: sum of squares 0-999 = {total}")
time.sleep(1)
print("  Script khatam! ✅")
