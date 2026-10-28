
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-47 : Creation de la dimension Product
-- =====================================================

IF OBJECT_ID('dw.dim_product', 'U') IS NULL
BEGIN
    CREATE TABLE dw.dim_product
    (
        product_key INT IDENTITY(1,1) NOT NULL,
        product_id VARCHAR(32) NOT NULL,
        product_category_name NVARCHAR(100) NULL,
        product_name_lenght INT NULL,
        product_description_lenght INT NULL,
        product_photos_qty INT NULL,
        product_weight_g INT NULL,
        product_length_cm INT NULL,
        product_height_cm INT NULL,
        product_width_cm INT NULL,

        CONSTRAINT PK_dim_product
            PRIMARY KEY (product_key),

        CONSTRAINT UQ_dim_product_id
            UNIQUE (product_id)
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
  AND TABLE_NAME = 'dim_product'
ORDER BY ORDINAL_POSITION;
GO

-- Verification du volume initial
SELECT COUNT(*) AS total_products
FROM dw.dim_product;
GO
