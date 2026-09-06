"""Country Development Indicators Analysis
Run after placing a CSV at data/development_indicators.csv.
Expected columns: country, gdp, birth_rate, internet_usage.
Optional: region, development_group.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "development_indicators.csv"
OUT = BASE / "reports" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError("Place your CSV at data/development_indicators.csv and run again.")

df = pd.read_csv(DATA)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
required = {"country", "gdp", "birth_rate", "internet_usage"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

for col in ["gdp", "birth_rate", "internet_usage"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

before = len(df)
df = df.drop_duplicates(subset=["country"]).copy()
print(f"Duplicate country rows removed: {before - len(df):,}")
print("Missing values:\n", df[["gdp", "birth_rate", "internet_usage"]].isna().sum())
print("\nDescriptive statistics:\n", df[["gdp", "birth_rate", "internet_usage"]].describe())

corr = df[["gdp", "birth_rate", "internet_usage"]].corr()
corr.to_csv(BASE / "reports" / "correlation_matrix.csv")
print("\nCorrelation matrix:\n", corr)

if "region" in df.columns:
    regional = df.groupby("region", as_index=False)[["gdp", "birth_rate", "internet_usage"]].mean()
    regional.to_csv(BASE / "reports" / "regional_summary.csv", index=False)
    print("\nRegional summary:\n", regional.sort_values("gdp", ascending=False).to_string(index=False))

plot_df = df.dropna(subset=["gdp", "internet_usage"])
plt.figure(figsize=(8, 5))
plt.scatter(plot_df["gdp"], plot_df["internet_usage"])
plt.title("GDP vs Internet Usage")
plt.xlabel("GDP")
plt.ylabel("Internet Usage")
plt.tight_layout()
plt.savefig(OUT / "gdp_vs_internet_usage.png", dpi=150)
plt.close()

print("\nAnalysis completed. Review the generated CSV outputs and charts before writing final business/research conclusions.")
