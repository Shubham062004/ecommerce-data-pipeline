-- Production Analytics Views for BI Tools (Power BI / Tableau)

-- 1. Revenue Trends by Date
CREATE VIEW IF NOT EXISTS view_revenue_trends AS
SELECT 
    DATE(transaction_date) as date,
    SUM(total_amount) as daily_revenue,
    COUNT(transaction_id) as total_transactions
FROM transactions
GROUP BY 1
ORDER BY 1;

-- 2. Category Performance
CREATE VIEW IF NOT EXISTS view_category_sales AS
SELECT 
    category,
    SUM(total_amount) as total_revenue,
    SUM(quantity) as total_quantity_sold,
    AVG(price) as avg_unit_price
FROM transactions
GROUP BY 1
ORDER BY 2 DESC;

-- 3. Top Customers by Revenue
CREATE VIEW IF NOT EXISTS view_top_customers AS
SELECT 
    customer_id,
    COUNT(transaction_id) as total_orders,
    SUM(total_amount) as lifetime_value
FROM transactions
GROUP BY 1
ORDER BY 3 DESC
LIMIT 100;

-- 4. Geographical Sales Distribution (assuming city/country exists)
-- If columns exist in your dataset, otherwise these are placeholders for common BI needs
-- SELECT city, SUM(total_amount) FROM transactions GROUP BY 1;
