import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / 'data' / 'reliance_financials.csv'
OUT = ROOT / 'reports'
OUT.mkdir(exist_ok=True)

# Load structured source data
df = pd.read_csv(DATA)
annual = df[df['period_type'].eq('annual')].copy()
annual['ebitda_margin_pct'] = annual['ebitda_cr'] / annual['revenue_cr'] * 100
annual['revenue_yoy_pct'] = annual['revenue_cr'].pct_change() * 100
annual['pat_yoy_pct'] = annual['pat_cr'].pct_change() * 100

print(annual.round(2).to_string(index=False))
annual.to_csv(OUT / 'annual_kpis.csv', index=False)

# Revenue and EBITDA trend
ax = annual.plot(x='period', y=['revenue_cr', 'ebitda_cr'], kind='line', marker='o', figsize=(9, 5))
ax.set_title('Reliance Industries: Revenue and EBITDA Trend')
ax.set_ylabel('₹ crore')
ax.set_xlabel('Financial Year')
plt.tight_layout()
plt.savefig(OUT / 'revenue_ebitda_trend.png', dpi=160)
plt.close()

# PAT trend
ax = annual.plot(x='period', y='pat_cr', kind='bar', figsize=(9, 5), legend=False)
ax.set_title('Reliance Industries: Profit After Tax')
ax.set_ylabel('₹ crore')
ax.set_xlabel('Financial Year')
plt.tight_layout()
plt.savefig(OUT / 'pat_trend.png', dpi=160)
plt.close()

# Margin trend
ax = annual.plot(x='period', y='ebitda_margin_pct', kind='line', marker='o', figsize=(9, 5), legend=False)
ax.set_title('Reliance Industries: EBITDA Margin')
ax.set_ylabel('EBITDA Margin (%)')
ax.set_xlabel('Financial Year')
plt.tight_layout()
plt.savefig(OUT / 'ebitda_margin_trend.png', dpi=160)
plt.close()

latest = annual.iloc[-1]
print('\nLatest annual KPI summary:')
print(f"Revenue: ₹{latest.revenue_cr:,.0f} crore")
print(f"EBITDA: ₹{latest.ebitda_cr:,.0f} crore")
print(f"PAT: ₹{latest.pat_cr:,.0f} crore")
print(f"EBITDA margin: {latest.ebitda_margin_pct:.2f}%")
