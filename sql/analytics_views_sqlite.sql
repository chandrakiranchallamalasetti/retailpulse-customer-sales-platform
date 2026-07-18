DROP VIEW IF EXISTS vw_sales_facts;
DROP VIEW IF EXISTS vw_customer_summary;
DROP VIEW IF EXISTS vw_salesperson_performance;
DROP VIEW IF EXISTS vw_product_performance;
DROP VIEW IF EXISTS vw_state_performance;
DROP VIEW IF EXISTS vw_monthly_sales;

CREATE VIEW vw_sales_facts AS
SELECT
    o.order_id,
    o.order_date,
    o.order_status,
    o.data_origin,
    c.customer_id,
    c.customer_name,
    c.state,
    s.salesperson_id,
    s.first_name || ' ' || s.last_name AS salesperson_name,
    p.product_id,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    ROUND(oi.quantity * oi.unit_price, 2) AS line_revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id
JOIN salespersons s ON s.salesperson_id = c.salesperson_id
JOIN products p ON p.product_id = oi.product_id;

CREATE VIEW vw_customer_summary AS
SELECT
    customer_id,
    customer_name,
    state,
    salesperson_name,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(line_revenue), 2) AS total_sales,
    ROUND(SUM(line_revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value,
    MAX(order_date) AS last_order_date
FROM vw_sales_facts
GROUP BY customer_id, customer_name, state, salesperson_name;

CREATE VIEW vw_salesperson_performance AS
SELECT
    salesperson_id,
    salesperson_name,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(line_revenue), 2) AS total_sales,
    ROUND(SUM(line_revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM vw_sales_facts
GROUP BY salesperson_id, salesperson_name;

CREATE VIEW vw_product_performance AS
SELECT
    product_id,
    product_name,
    category,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(line_revenue), 2) AS total_sales
FROM vw_sales_facts
GROUP BY product_id, product_name, category;

CREATE VIEW vw_state_performance AS
SELECT
    state,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(line_revenue), 2) AS total_sales
FROM vw_sales_facts
GROUP BY state;

CREATE VIEW vw_monthly_sales AS
SELECT
    substr(order_date, 1, 7) AS sales_month,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(line_revenue), 2) AS total_sales
FROM vw_sales_facts
GROUP BY substr(order_date, 1, 7)
ORDER BY sales_month;
