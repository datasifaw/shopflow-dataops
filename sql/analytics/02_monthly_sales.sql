
-- ShopFlow DataOps
-- Ventes mensuelles Olist
-- Commandes livrees uniquement
-- Montants hors frais de livraison

USE ShopFlowDB;
GO

SELECT
    YEAR(o.order_purchase_timestamp) AS sales_year,
    MONTH(o.order_purchase_timestamp) AS sales_month,

    COUNT(DISTINCT o.order_id) AS delivered_orders,

    COUNT(*) AS delivered_items,

    SUM(oi.price) AS item_revenue,

    CAST(
        SUM(oi.price)
        / NULLIF(COUNT(DISTINCT o.order_id), 0)
        AS DECIMAL(12,2)
    ) AS average_order_value

FROM dbo.orders AS o

INNER JOIN dbo.order_items AS oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY
    YEAR(o.order_purchase_timestamp),
    MONTH(o.order_purchase_timestamp)

ORDER BY
    sales_year,
    sales_month;
GO


USE ShopFlowDB;
GO

WITH monthly_sales AS (
    SELECT
        YEAR(o.order_purchase_timestamp) AS sales_year,
        MONTH(o.order_purchase_timestamp) AS sales_month,
        COUNT(DISTINCT o.order_id) AS delivered_orders,
        SUM(oi.price) AS item_revenue
    FROM dbo.orders AS o
    INNER JOIN dbo.order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY
        YEAR(o.order_purchase_timestamp),
        MONTH(o.order_purchase_timestamp)
)
SELECT
    SUM(delivered_orders) AS total_delivered_orders,
    SUM(item_revenue) AS total_item_revenue
FROM monthly_sales;
GO
