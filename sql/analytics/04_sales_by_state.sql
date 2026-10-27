
-- ShopFlow DataOps
-- SCRUM-37 : Analyse des ventes par Etat bresilien
-- Commandes livrees, montant hors frais de livraison

USE ShopFlowDB;
GO

-- 1. Ventes par Etat

SELECT
    c.customer_state AS state_code,

    COUNT(DISTINCT o.order_id) AS delivered_orders,

    COUNT(*) AS delivered_items,

    SUM(oi.price) AS item_revenue,

    SUM(oi.freight_value) AS shipping_fees,

    CAST(
        SUM(oi.price) /
        NULLIF(COUNT(DISTINCT o.order_id), 0)
        AS DECIMAL(12,2)
    ) AS average_order_value

FROM dbo.customers AS c

INNER JOIN dbo.orders AS o
    ON c.customer_id = o.customer_id

INNER JOIN dbo.order_items AS oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY c.customer_state

ORDER BY item_revenue DESC;
GO

-- 2. Reconciliation avec les ventes globale

WITH sales_by_state AS (
    SELECT
        c.customer_state,
        COUNT(DISTINCT o.order_id) AS delivered_orders,
        SUM(oi.price) AS item_revenue
    FROM dbo.customers AS c
    INNER JOIN dbo.orders AS o
        ON c.customer_id = o.customer_id
    INNER JOIN dbo.order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_state
)
SELECT
    COUNT(*) AS state_count,
    SUM(delivered_orders) AS total_delivered_orders,
    SUM(item_revenue) AS total_item_revenue
FROM sales_by_state;
GO
