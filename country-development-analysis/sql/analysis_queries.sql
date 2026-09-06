-- Country Development Indicators Analysis
-- Adapt table and column names to the selected dataset.

-- 1. Country ranking by GDP
SELECT
    country,
    gdp
FROM development_indicators
WHERE gdp IS NOT NULL
ORDER BY gdp DESC;

-- 2. Highest internet usage
SELECT
    country,
    internet_usage
FROM development_indicators
WHERE internet_usage IS NOT NULL
ORDER BY internet_usage DESC
LIMIT 10;

-- 3. Average indicators by region
SELECT
    region,
    AVG(gdp) AS avg_gdp,
    AVG(birth_rate) AS avg_birth_rate,
    AVG(internet_usage) AS avg_internet_usage
FROM development_indicators
GROUP BY region
ORDER BY avg_gdp DESC;

-- 4. Countries with high GDP and high internet usage
SELECT
    country,
    gdp,
    internet_usage
FROM development_indicators
WHERE gdp IS NOT NULL
  AND internet_usage IS NOT NULL
ORDER BY gdp DESC, internet_usage DESC;

-- 5. Rank countries within each region by GDP
SELECT
    country,
    region,
    gdp,
    DENSE_RANK() OVER (
        PARTITION BY region
        ORDER BY gdp DESC
    ) AS regional_gdp_rank
FROM development_indicators
WHERE gdp IS NOT NULL;

-- 6. Development-group comparison
SELECT
    development_group,
    COUNT(*) AS countries,
    AVG(gdp) AS avg_gdp,
    AVG(birth_rate) AS avg_birth_rate,
    AVG(internet_usage) AS avg_internet_usage
FROM development_indicators
GROUP BY development_group
ORDER BY avg_gdp DESC;
