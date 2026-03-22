import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import json, os

os.makedirs("output", exist_ok=True)
print("🚀 Data processing shuru...")

np.random.seed(42)
n = 1000
data = {
    "id":         np.arange(1, n+1),
    "age":        np.random.randint(18, 65, n),
    "salary":     np.random.normal(50000, 15000, n).round(2),
    "experience": np.random.randint(0, 40, n),
    "score":      np.random.uniform(0, 100, n).round(2),
    "category":   np.random.choice(["A", "B", "C", "D"], n)
}
df = pd.DataFrame(data)
df.to_csv("output/raw_data.csv", index=False)
print(f"✅ Raw CSV saved: {len(df)} rows")

stats_data = {
    "total_rows":      int(len(df)),
    "avg_salary":      round(float(df["salary"].mean()), 2),
    "max_salary":      round(float(df["salary"].max()), 2),
    "min_salary":      round(float(df["salary"].min()), 2),
    "avg_age":         round(float(df["age"].mean()), 2),
    "avg_score":       round(float(df["score"].mean()), 2),
    "category_counts": df["category"].value_counts().to_dict()
}

corr, pval = stats.pearsonr(df["experience"], df["salary"])
stats_data["exp_salary_correlation"] = round(float(corr), 4)
stats_data["p_value"]                = round(float(pval), 6)
print(f"📈 Correlation: {corr:.4f}, p-value: {pval:.6f}")

scaler = StandardScaler()
X = scaler.fit_transform(df[["age", "experience", "score"]])
y = df["salary"].values
model = LinearRegression()
model.fit(X, y)
r2 = model.score(X, y)
stats_data["ml_r2_score"] = round(float(r2), 4)
print(f"🤖 ML R² score: {r2:.4f}")

high_earners = df[df["salary"] > 60000].sort_values("salary", ascending=False)
high_earners.to_csv("output/high_earners.csv", index=False)
stats_data["high_earners_count"] = int(len(high_earners))
print(f"💰 High earners (>60k): {len(high_earners)}")

with open("output/summary.json", "w") as f:
    json.dump(stats_data, f, indent=2)

with open("output/processing_log.txt", "a") as f:
    f.write(f"\n📊 Stats:\n{json.dumps(stats_data, indent=2)}\n✅ Done!\n")

print("🎉 Sab complete!")
print(json.dumps(stats_data, indent=2))
