
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-49 : Optimisation des requetes analytiques
-- Aucun DELETE, DROP TABLE ou TRUNCATE
-- =====================================================

SET NOCOUNT ON;
GO

-- 1. Index : jointure fact_sales -> dim_order
IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE object_id = OBJECT_ID('dw.fact_sales')
      AND name = 'IX_fact_sales_order_key'
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_fact_sales_order_key
    ON dw.fact_sales (order_key)
    INCLUDE (
        product_key,
        date_key,
        quantity,
        unit_price,
        freight_value
    );
END;
GO

-- 2. Index : jointure fact_sales -> dim_product
IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE object_id = OBJECT_ID('dw.fact_sales')
      AND name = 'IX_fact_sales_product_key'
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_fact_sales_product_key
    ON dw.fact_sales (product_key)
    INCLUDE (
        order_key,
        unit_price,
        freight_value
    );
END;
GO

-- 3. Index : filtrage des commandes livrees
IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE object_id = OBJECT_ID('dw.dim_order')
      AND name = 'IX_dim_order_status_key'
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_dim_order_status_key
    ON dw.dim_order (order_status, order_key);
END;
GO

-- 4. Actualiser les statistiques
UPDATE STATISTICS dw.fact_sales WITH FULLSCAN;
UPDATE STATISTICS dw.dim_order WITH FULLSCAN;
UPDATE STATISTICS dw.dim_product WITH FULLSCAN;
UPDATE STATISTICS dw.dim_date WITH FULLSCAN;
GO

-- 5. Verifier les index crees
SELECT
    OBJECT_NAME(object_id) AS table_name,
    name AS index_name,
    type_desc
FROM sys.indexes
WHERE name IN (
    'IX_fact_sales_order_key',
    'IX_fact_sales_product_key',
    'IX_dim_order_status_key'
)
ORDER BY table_name, index_name;
GO

-- 6. Verifier les volumes apres optimisation
SELECT
    (SELECT COUNT_BIG(*) FROM dw.fact_sales)
        AS total_sales,
    (SELECT COUNT_BIG(*) FROM dw.dim_order)
        AS total_orders,
    (SELECT COUNT_BIG(*) FROM dw.dim_product)
        AS total_products;
GO
