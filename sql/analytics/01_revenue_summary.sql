
-- ShopFlow DataOps
-- Premier indicateur e-commerce : ventes livrees
-- Montant des articles hors frais de livraison

USE ShopFlowDB;
GO

SELECT
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    COUNT(*) AS delivered_items,
    SUM(oi.price) AS item_revenue,
    SUM(oi.freight_value) AS shipping_fees,
    SUM(oi.price + oi.freight_value)
        AS total_customer_amount
FROM dbo.orders AS o
INNER JOIN dbo.order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';
GO


-- Panier moyen hors livraison
-- Commandes livrees uniquement

SELECT
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    CAST(
        SUM(oi.price) * 1.0
        / NULLIF(COUNT(DISTINCT o.order_id), 0)
        AS DECIMAL(12,2)
    ) AS average_order_value
FROM dbo.orders AS o
INNER JOIN dbo.order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';
GO
