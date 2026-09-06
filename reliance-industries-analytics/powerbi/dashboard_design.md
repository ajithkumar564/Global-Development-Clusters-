# Power BI Dashboard Design

## Page 1 — Executive Overview
KPI cards:
- Revenue (₹ crore)
- EBITDA (₹ crore)
- Profit After Tax (₹ crore)
- Capital Expenditure (₹ crore)
- EBITDA Margin %

Visuals:
1. Line chart: Revenue and EBITDA by financial year.
2. Column chart: PAT by financial year.
3. Combo chart: Revenue growth % and PAT growth %.
4. Waterfall or clustered column: Capex by year.

Slicers:
- Period
- Period Type

## Page 2 — Business Segment Performance
Load segment-level rows from the annual report and create:
- Revenue by segment
- EBITDA by segment
- Segment YoY growth
- EBITDA margin by segment
- Revenue share by segment

Recommended segments: Retail, Digital Services, Media & Entertainment, Oil to Chemicals, Oil & Gas, and New Energy where comparable financial fields are available.

## Page 3 — Digital / Social Media Observations
Optional secondary analysis using publicly visible official RIL/Jio social content:
- Content type
- Publication date
- Platform
- Views/reactions/comments where publicly displayed
- Topic category

Keep this separate from audited financial KPIs. Do not mix social engagement counts with financial results.

## Core DAX measures
```DAX
Total Revenue = SUM(Financials[revenue_cr])
Total EBITDA = SUM(Financials[ebitda_cr])
Total PAT = SUM(Financials[pat_cr])
Total Capex = SUM(Financials[capex_cr])
EBITDA Margin % = DIVIDE([Total EBITDA], [Total Revenue])
Revenue YoY % =
VAR PrevRevenue = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, YEAR))
RETURN DIVIDE([Total Revenue] - PrevRevenue, PrevRevenue)
PAT YoY % =
VAR PrevPAT = CALCULATE([Total PAT], DATEADD('Date'[Date], -1, YEAR))
RETURN DIVIDE([Total PAT] - PrevPAT, PrevPAT)
```

## Interview story
The dashboard demonstrates an end-to-end workflow: source validation → structured data → SQL KPI calculations → Python EDA → Power BI modeling → executive storytelling.
