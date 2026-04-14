-- E-Commerce Analytics Queries
-- Target Table: 'transactions'

-- 1. Total Revenue Overview
-- Calculates the top-level KPI metrics for the business.
SELECT 
    COUNT(transaction_id) AS total_completed_transactions,
    SUM(quantity) AS total_items_sold,
    SUM(revenue) AS total_base_revenue,
    SUM(total_amount) AS total_revenue_with_tax
FROM transactions
WHERE status = 'completed';


-- 2. Revenue by City
-- Identifies top-performing regional markets by aggregating total sales data.
SELECT 
    city,
    COUNT(transaction_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM transactions
WHERE status = 'completed'
GROUP BY city
ORDER BY total_revenue DESC;


-- 3. Top Customers (Lifetime Value)
-- Finds our most valuable customers based on their purchasing frequency and total spend.
SELECT 
    customer_id,
    COUNT(transaction_id) AS order_count,
    SUM(total_amount) AS lifetime_value
FROM transactions
WHERE status = 'completed'
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 10;


-- 4. Advanced: Customer Rank by Revenue within City (Window Function)
-- Assigns a regional ranking (1, 2, 3...) to customers in each city based on spend.
-- Useful for regional marketing teams to identify localized VIPs.
WITH CustomerCityRevenue AS (
    SELECT 
        city,
        customer_id,
        SUM(total_amount) AS total_spent
    FROM transactions
    WHERE status = 'completed'
    GROUP BY city, customer_id
)
SELECT 
    city,
    customer_id,
    total_spent,
    DENSE_RANK() OVER(PARTITION BY city ORDER BY total_spent DESC) as rank_in_city
FROM CustomerCityRevenue
ORDER BY city ASC, rank_in_city ASC;
