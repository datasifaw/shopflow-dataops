
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-48 : Chargement de dw.fact_sales
-- Grain : un article par commande
-- Source : dbo.order_items + dbo.orders
-- =====================================================

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

BEGIN TRY
    BEGIN TRANSACTION;

    -- 1. Verifier que la source existe
    IF NOT EXISTS (
        SELECT 1 FROM dbo.order_items
    )
    BEGIN
        THROW 50011,
            'dbo.order_items est vide.',
            1;
    END;

    -- 2. Verifier que les dimensions sont chargees
    IF NOT EXISTS (SELECT 1 FROM dw.dim_customer)
       OR NOT EXISTS (SELECT 1 FROM dw.dim_product)
       OR NOT EXISTS (SELECT 1 FROM dw.dim_order)
       OR NOT EXISTS (SELECT 1 FROM dw.dim_date)
    BEGIN
        THROW 50012,
            'Une dimension du Data Warehouse est vide.',
            1;
    END;

    -- 3. Verifier toutes les correspondances
    -- avant de commencer les insertions
    IF EXISTS (
        SELECT 1
        FROM dbo.order_items AS oi
        INNER JOIN dbo.orders AS o
            ON o.order_id = oi.order_id

        LEFT JOIN dw.dim_order AS dor
            ON dor.order_id = oi.order_id

        LEFT JOIN dw.dim_customer AS dc
            ON dc.customer_id = o.customer_id

        LEFT JOIN dw.dim_product AS dp
            ON dp.product_id = oi.product_id

        LEFT JOIN dw.dim_date AS dd
            ON dd.full_date =
                CAST(o.order_purchase_timestamp AS DATE)

        WHERE dor.order_key IS NULL
           OR dc.customer_key IS NULL
           OR dp.product_key IS NULL
           OR dd.date_key IS NULL
    )
    BEGIN
        THROW 50013,
            'Certaines lignes ne trouvent pas leur dimension.',
            1;
    END;

    -- 4. Charger la table de faits
    INSERT INTO dw.fact_sales
    (
        order_key,
        customer_key,
        product_key,
        date_key,
        order_item_id,
        quantity,
        unit_price,
        freight_value
    )
    SELECT
        dor.order_key,
        dc.customer_key,
        dp.product_key,
        dd.date_key,
        oi.order_item_id,
        1 AS quantity,
        oi.price,
        oi.freight_value

    FROM dbo.order_items AS oi

    INNER JOIN dbo.orders AS o
        ON o.order_id = oi.order_id

    INNER JOIN dw.dim_order AS dor
        ON dor.order_id = oi.order_id

    INNER JOIN dw.dim_customer AS dc
        ON dc.customer_id = o.customer_id

    INNER JOIN dw.dim_product AS dp
        ON dp.product_id = oi.product_id

    INNER JOIN dw.dim_date AS dd
        ON dd.full_date =
            CAST(o.order_purchase_timestamp AS DATE)

    WHERE NOT EXISTS
    (
        SELECT 1
        FROM dw.fact_sales AS fs
        WHERE fs.order_key = dor.order_key
          AND fs.order_item_id = oi.order_item_id
    );

    DECLARE @inserted INT = @@ROWCOUNT;

    -- 5. Controler les volumes dans la transaction
    DECLARE @source_count INT = (
        SELECT COUNT(*) FROM dbo.order_items
    );

    DECLARE @warehouse_count INT = (
        SELECT COUNT(*) FROM dw.fact_sales
    );

    IF @source_count <> @warehouse_count
    BEGIN
        THROW 50014,
            'Volume fact_sales different de la source.',
            1;
    END;

    COMMIT TRANSACTION;

    PRINT CONCAT(
        'Chargement fact_sales termine : ',
        @inserted,
        ' lignes inserees.'
    );

END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO

-- =====================================================
-- 6. Comparaison des volumes
-- =====================================================

SELECT
    (SELECT COUNT(*) FROM dbo.order_items)
        AS source_items,

    (SELECT COUNT(*) FROM dw.fact_sales)
        AS warehouse_sales;
GO

-- =====================================================
-- 7. Reconciliation des montants
-- Toutes les commandes, tous les statuts
-- =====================================================

SELECT
    'SOURCE' AS origin,
    SUM(price) AS product_revenue,
    SUM(freight_value) AS freight_revenue,
    SUM(price + freight_value) AS total_revenue
FROM dbo.order_items

UNION ALL

SELECT
    'WAREHOUSE' AS origin,
    SUM(unit_price) AS product_revenue,
    SUM(freight_value) AS freight_revenue,
    SUM(total_amount) AS total_revenue
FROM dw.fact_sales;
GO

-- =====================================================
-- 8. Verifier les doublons de la cle metier
-- =====================================================

SELECT
    order_key,
    order_item_id,
    COUNT(*) AS occurrences
FROM dw.fact_sales
GROUP BY order_key, order_item_id
HAVING COUNT(*) > 1;
GO

-- =====================================================
-- 9. Apercu des ventes et dimensions
-- =====================================================

SELECT TOP (10)
    fs.sales_key,
    dor.order_id,
    fs.order_item_id,
    dc.customer_state,
    dp.product_category_name,
    dd.full_date AS purchase_date,
    fs.quantity,
    fs.unit_price,
    fs.freight_value,
    fs.total_amount
FROM dw.fact_sales AS fs

INNER JOIN dw.dim_order AS dor
    ON dor.order_key = fs.order_key

INNER JOIN dw.dim_customer AS dc
    ON dc.customer_key = fs.customer_key

INNER JOIN dw.dim_product AS dp
    ON dp.product_key = fs.product_key

INNER JOIN dw.dim_date AS dd
    ON dd.date_key = fs.date_key

ORDER BY fs.sales_key;
GO
