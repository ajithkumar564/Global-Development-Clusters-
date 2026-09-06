"""E-commerce Sales & Customer Analytics
Run after placing an e-commerce CSV at data/ecommerce.csv.
The script prints reproducible KPIs and saves charts to reports/charts/.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "ecommerce.csv"
OUT = BASE / "reports" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError("Place your CSV at data/ecommerce.csv and run again.")

df = pd.read_csv(DATA)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

required = {"order_id", "order_date", "customer_id", "sales"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

# Cleaning
before = len(df)
df = df.drop_duplicates().copy()
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.dropna(subset=["order_id", "order_date", "customer_id", "sales"])

# KPIs
revenue = df["sales"].sum()
orders = df["order_id"].nunique()
customers = df["customer_id"].nunique()
aov = revenue / orders if orders else np.nan
print(f"Rows removed during cleaning: {before - len(df):,}")
print(f"Revenue: {revenue:,.2f}")
print(f"Orders: {orders:,}")
print(f"Customers: {customers:,}")
print(f"Average Order Value: {aov:,.2f}")

monthly = df.assign(month=df["order_date"].dt.to_period("M")).groupby("month", as_index=False)["sales"].sum()
monthly["month"] = monthly["month"].astype(str)
monthly.to_csv(BASE / "reports" / "monthly_revenue.csv", index=False)

plt.figure(figsize=(10, 5))
plt.plot(monthly["month"], monthly["sales"], marker="o")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "monthly_revenue.png", dpi=150)
plt.close()

if "category" in df.columns:
    category = df.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    category.to_csv(BASE / "reports" / "category_revenue.csv", index=False)
    plt.figure(figsize=(9, 5))
    plt.bar(category["category"].astype(str), category["sales"])
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "category_revenue.png", dpi=150)
    plt.close()

customer_orders = df.groupby("customer_id")["order_id"].nunique()
repeat_rate = (customer_orders.gt(1).mean() * 100) if len(customer_orders) else np.nan
print(f"Repeat Customer Rate: {repeat_rate:.2f}%")
