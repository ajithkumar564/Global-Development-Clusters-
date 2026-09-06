-- E-commerce Sales & Customer Analytics
-- Adapt column names to the selected dataset before execution.

-- 1. Monthly revenue
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(sales) AS revenue
FROM orders
GROUP BY 1
ORDER BY 1;

-- 2. Average order value
SELECT
    SUM(sales) / COUNT(DISTINCT order_id) AS average_order_value
FROM orders;

-- 3. Revenue by category
SELECT
    category,
    SUM(sales) AS revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;

-- 4. Top products by revenue
SELECT
    product_name,
    SUM(sales) AS revenue
FROM orders
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;

-- 5. Customer order frequency
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(sales) AS customer_revenue
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC;

-- 6. New vs repeat customer framework
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN order_count = 1 THEN 'New Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS customers
FROM customer_orders
GROUP BY 1;

-- 7. Category ranking using a window function
WITH category_sales AS (
    SELECT category, SUM(sales) AS revenue
    FROM orders
    GROUP BY category
)
SELECT
    category,
    revenue,
    DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM category_sales
ORDER BY revenue_rank;
