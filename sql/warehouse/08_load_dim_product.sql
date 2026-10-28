
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-48 : Chargement de dw.dim_product
-- Source : dbo.products
-- Destination : dw.dim_product
-- =====================================================

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

-- 1. Verifier la source
IF NOT EXISTS (
    SELECT 1
    FROM dbo.products
)
BEGIN
    THROW 50002,
        'La table dbo.products est vide.',
        1;
END;
GO

-- 2. Chargement transactionnel et idempotent
BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dw.dim_product
    (
        product_id,
        product_category_name,
        product_name_lenght,
        product_description_lenght,
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    )
    SELECT
        p.product_id,
        p.product_category_name,
        p.product_name_lenght,
        p.product_description_lenght,
        p.product_photos_qty,
        p.product_weight_g,
        p.product_length_cm,
        p.product_height_cm,
        p.product_width_cm
    FROM dbo.products AS p
    WHERE NOT EXISTS
    (
        SELECT 1
        FROM dw.dim_product AS d
        WHERE d.product_id = p.product_id
    );

    DECLARE @inserted INT = @@ROWCOUNT;

    COMMIT TRANSACTION;

    PRINT CONCAT(
        'Chargement dw.dim_product termine : ',
        @inserted,
        ' produits inseres.'
    );
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO

-- =====================================================
-- 3. Comparer les volumes
-- =====================================================

SELECT
    (SELECT COUNT(*) FROM dbo.products)
        AS source_products,

    (SELECT COUNT(*) FROM dw.dim_product)
        AS warehouse_products;
GO

-- =====================================================
-- 4. Verifier les doublons
-- =====================================================

SELECT
    product_id,
    COUNT(*) AS occurrences
FROM dw.dim_product
GROUP BY product_id
HAVING COUNT(*) > 1;
GO

-- =====================================================
-- 5. Verifier les categories manquantes
-- =====================================================

SELECT
    COUNT(*) AS products_without_category
FROM dw.dim_product
WHERE product_category_name IS NULL;
GO

-- =====================================================
-- 6. Apercu des produits
-- =====================================================

SELECT TOP (10)
    product_key,
    product_id,
    product_category_name,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM dw.dim_product
ORDER BY product_key;
GO
