-- Reliance Industries Financial Analytics
-- Dataset: data/reliance_financials.csv

-- 1. Annual KPI trend
SELECT period, revenue_cr, ebitda_cr, pat_cr, capex_cr
FROM reliance_financials
WHERE period_type = 'annual'
ORDER BY period;

-- 2. YoY revenue and PAT growth
WITH annual AS (
    SELECT period, revenue_cr, pat_cr,
           LAG(revenue_cr) OVER (ORDER BY period) AS prev_revenue,
           LAG(pat_cr) OVER (ORDER BY period) AS prev_pat
    FROM reliance_financials
    WHERE period_type = 'annual'
)
SELECT period,
       revenue_cr,
       ROUND(100.0 * (revenue_cr - prev_revenue) / NULLIF(prev_revenue,0), 2) AS revenue_yoy_pct,
       pat_cr,
       ROUND(100.0 * (pat_cr - prev_pat) / NULLIF(prev_pat,0), 2) AS pat_yoy_pct
FROM annual;

-- 3. EBITDA margin
SELECT period,
       ROUND(100.0 * ebitda_cr / NULLIF(revenue_cr,0), 2) AS ebitda_margin_pct
FROM reliance_financials
WHERE period_type = 'annual';

-- 4. Latest quarter versus latest full year (do not compare as YoY)
SELECT period, period_type, revenue_cr, ebitda_cr, pat_cr, capex_cr
FROM reliance_financials
ORDER BY CASE WHEN period_type='quarter' THEN 1 ELSE 0 END DESC, period DESC;

-- 5. Segment analysis can be added when segment-level rows are loaded.
-- Recommended fields: period, segment, revenue_cr, ebitda_cr, growth_pct.
