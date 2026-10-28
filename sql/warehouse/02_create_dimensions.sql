
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-47 : Creation de la dimension Customer
-- =====================================================

IF OBJECT_ID('dw.dim_customer', 'U') IS NULL
BEGIN
    CREATE TABLE dw.dim_customer
    (
        customer_key INT IDENTITY(1,1) NOT NULL,
        customer_id VARCHAR(32) NOT NULL,
        customer_unique_id VARCHAR(32) NOT NULL,
        customer_zip_code_prefix VARCHAR(5) NOT NULL,
        customer_city NVARCHAR(100) NOT NULL,
        customer_state CHAR(2) NOT NULL,

        CONSTRAINT PK_dim_customer
            PRIMARY KEY (customer_key),

        CONSTRAINT UQ_dim_customer_id
            UNIQUE (customer_id)
    );
END;
GO

-- Verification de la structure
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dw'
  AND TABLE_NAME = 'dim_customer'
ORDER BY ORDINAL_POSITION;
GO

-- Verification : la table vient d'etre creee
SELECT COUNT(*) AS total_customers
FROM dw.dim_customer;
GO
