import requests, json, os, csv
from datetime import datetime

os.makedirs("output", exist_ok=True)

print("🚀 GitHub Trending Repos Analysis shuru...")

# ── 1. GitHub public API se top Python repos fetch karo ──
print("📡 GitHub API se data fetch kar rahe hain...")
res = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "language:python stars:>10000", "sort": "stars", "per_page": 30},
    headers={"Accept": "application/vnd.github+json"},
    timeout=15
)
data = res.json()
repos = data.get("items", [])
print(f"✅ {len(repos)} repos mila!")

# ── 2. CSV mein save karo ──
with open("output/top_python_repos.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["rank","name","stars","forks","issues","description"])
    writer.writeheader()
    for i, r in enumerate(repos, 1):
        writer.writerow({
            "rank":        i,
            "name":        r["full_name"],
            "stars":       r["stargazers_count"],
            "forks":       r["forks_count"],
            "issues":      r["open_issues_count"],
            "description": (r["description"] or "")[:80]
        })
print("✅ top_python_repos.csv saved!")

# ── 3. Stats nikalo ──
total_stars = sum(r["stargazers_count"] for r in repos)
total_forks = sum(r["forks_count"] for r in repos)
top3 = [r["full_name"] for r in repos[:3]]

summary = {
    "fetched_at":    datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "total_repos":   len(repos),
    "total_stars":   total_stars,
    "total_forks":   total_forks,
    "avg_stars":     round(total_stars / len(repos)) if repos else 0,
    "top_3_repos":   top3,
    "most_starred":  repos[0]["full_name"] if repos else "N/A",
    "max_stars":     repos[0]["stargazers_count"] if repos else 0
}

with open("output/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("📊 Summary:")
print(json.dumps(summary, indent=2))
print("🎉 Sab complete!")
