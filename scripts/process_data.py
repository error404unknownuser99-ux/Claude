import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

LOG_FILE = "output/runtimelogs.txt"
os.makedirs("output", exist_ok=True)

def log(msg, level="INFO"):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

log("🚀 Scraping script start!")
log("🌐 Target: https://example.com")

try:
    log("📡 Sending GET request to example.com...")
    response = requests.get("https://example.com", timeout=10)
    log(f"✅ Response received! Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "No title found"
    log(f"📄 Page Title: {title}")

    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
    log(f"📝 Headings found: {headings}")

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    log(f"📜 Paragraphs count: {len(paragraphs)}")
    for i, para in enumerate(paragraphs):
        log(f"   Para {i+1}: {para[:150]}")

    links = [a.get("href") for a in soup.find_all("a", href=True)]
    log(f"🔗 Links found: {links}")

    result = {
        "url": "https://example.com",
        "status_code": response.status_code,
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs,
        "links": links,
        "scraped_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    with open("output/scraped_result.json", "w") as f:
        json.dump(result, f, indent=2)

    log("💾 Result saved to output/scraped_result.json")
    log("🎉 Scraping complete! SUCCESS!")

except Exception as e:
    log(f"❌ ERROR: {e}", level="ERROR")
