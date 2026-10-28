
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-48 : Chargement de dw.dim_customer
-- Source : dbo.customers
-- Destination : dw.dim_customer
-- =====================================================

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

-- Verifier que la table source contient des donnees
IF NOT EXISTS (
    SELECT 1
    FROM dbo.customers
)
BEGIN
    THROW 50001,
        'La table dbo.customers est vide.',
        1;
END;
GO

-- Chargement transactionnel, sans doublons
BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dw.dim_customer
    (
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    )
    SELECT
        c.customer_id,
        c.customer_unique_id,
        c.customer_zip_code_prefix,
        c.customer_city,
        c.customer_state
    FROM dbo.customers AS c
    WHERE NOT EXISTS
    (
        SELECT 1
        FROM dw.dim_customer AS d
        WHERE d.customer_id = c.customer_id
    );

    COMMIT TRANSACTION;

    PRINT 'Chargement dw.dim_customer termine.';
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO

-- =====================================================
-- Validation du volume
-- =====================================================

SELECT
    (SELECT COUNT(*) FROM dbo.customers)
        AS source_customers,

    (SELECT COUNT(*) FROM dw.dim_customer)
        AS warehouse_customers;
GO

-- Controle des doublons
SELECT
    customer_id,
    COUNT(*) AS occurrences
FROM dw.dim_customer
GROUP BY customer_id
HAVING COUNT(*) > 1;
GO

-- Apercu des donnees
SELECT TOP (10)
    customer_key,
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state
FROM dw.dim_customer
ORDER BY customer_key;
GO
