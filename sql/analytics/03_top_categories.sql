
-- ShopFlow DataOps
-- SCRUM-36 : Analyse des ventes par categorie
-- Commandes livrees, hors frais de livraison

USE ShopFlowDB;
GO

-- 1. Top 10 des categories par montant vendu

SELECT TOP (10)
    COALESCE(
        p.product_category_name,
        N'Non renseignee'
    ) AS category_name,

    COUNT(*) AS sold_items,

    COUNT(DISTINCT o.order_id) AS delivered_orders,

    SUM(oi.price) AS item_revenue

FROM dbo.orders AS o

INNER JOIN dbo.order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN dbo.products AS p
    ON oi.product_id = p.product_id

WHERE o.order_status = 'delivered'

GROUP BY
    COALESCE(
        p.product_category_name,
        N'Non renseignee'
    )

ORDER BY
    item_revenue DESC,
    category_name;
GO

-- 2. Reconciliation avec le montant global

SELECT
    COUNT(*) AS delivered_items,
    SUM(oi.price) AS total_item_revenue

FROM dbo.orders AS o

INNER JOIN dbo.order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN dbo.products AS p
    ON oi.product_id = p.product_id

WHERE o.order_status = 'delivered';
GO
