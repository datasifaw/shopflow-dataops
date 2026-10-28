
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-48 : Chargement de dw.dim_order
-- Source      : dbo.orders
-- Destination : dw.dim_order
-- =====================================================

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

-- 1. Verifier que la source est chargee
IF NOT EXISTS (
    SELECT 1
    FROM dbo.orders
)
BEGIN
    THROW 50003,
        'La table dbo.orders est vide.',
        1;
END;
GO

-- 2. Chargement transactionnel et idempotent
BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dw.dim_order
    (
        order_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date
    )
    SELECT
        o.order_id,
        o.order_status,
        o.order_purchase_timestamp,
        o.order_approved_at,
        o.order_delivered_carrier_date,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date
    FROM dbo.orders AS o
    WHERE NOT EXISTS
    (
        SELECT 1
        FROM dw.dim_order AS d
        WHERE d.order_id = o.order_id
    );

    DECLARE @inserted INT = @@ROWCOUNT;

    COMMIT TRANSACTION;

    PRINT CONCAT(
        'Chargement dw.dim_order termine : ',
        @inserted,
        ' commandes inserees.'
    );

END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO

-- =====================================================
-- 3. Comparer les volumes source et destination
-- =====================================================

SELECT
    (SELECT COUNT(*) FROM dbo.orders)
        AS source_orders,

    (SELECT COUNT(*) FROM dw.dim_order)
        AS warehouse_orders;
GO

-- =====================================================
-- 4. Verifier les doublons
-- =====================================================

SELECT
    order_id,
    COUNT(*) AS occurrences
FROM dw.dim_order
GROUP BY order_id
HAVING COUNT(*) > 1;
GO

-- =====================================================
-- 5. Repartition des statuts de commandes
-- =====================================================

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM dw.dim_order
GROUP BY order_status
ORDER BY total_orders DESC;
GO

-- =====================================================
-- 6. Dates facultatives absentes
-- =====================================================

SELECT
    SUM(
        CASE WHEN order_approved_at IS NULL
            THEN 1 ELSE 0 END
    ) AS missing_approved_at,

    SUM(
        CASE WHEN order_delivered_carrier_date IS NULL
            THEN 1 ELSE 0 END
    ) AS missing_carrier_date,

    SUM(
        CASE WHEN order_delivered_customer_date IS NULL
            THEN 1 ELSE 0 END
    ) AS missing_delivery_date
FROM dw.dim_order;
GO

-- =====================================================
-- 7. Apercu des commandes
-- =====================================================

SELECT TOP (10)
    order_key,
    order_id,
    order_status,
    order_purchase_timestamp,
    order_delivered_customer_date
FROM dw.dim_order
ORDER BY order_key;
GO
