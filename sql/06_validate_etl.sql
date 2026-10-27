
-- ShopFlow DataOps
-- Validation du chargement ETL Olist

USE ShopFlowDB;
GO

-- 1. Volumes charges
SELECT 'customers' AS table_name, COUNT(*) AS total
FROM dbo.customers
UNION ALL
SELECT 'products', COUNT(*)
FROM dbo.products
UNION ALL
SELECT 'orders', COUNT(*)
FROM dbo.orders
UNION ALL
SELECT 'order_items', COUNT(*)
FROM dbo.order_items;
GO

-- 2. Commandes sans client valide
SELECT COUNT(*) AS orphan_orders
FROM dbo.orders AS o
LEFT JOIN dbo.customers AS c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
GO

-- 3. Articles sans commande valide
SELECT COUNT(*) AS orphan_order_items
FROM dbo.order_items AS oi
LEFT JOIN dbo.orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;
GO

-- 4. Articles sans produit valide
SELECT COUNT(*) AS orphan_products
FROM dbo.order_items AS oi
LEFT JOIN dbo.products AS p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;
GO

-- 5. Commandes sans article
SELECT COUNT(*) AS orders_without_items
FROM dbo.orders AS o
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.order_items AS oi
    WHERE oi.order_id = o.order_id
);
GO
