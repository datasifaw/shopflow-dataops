
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-47 : Creation de la dimension Order
-- =====================================================

IF OBJECT_ID('dw.dim_order', 'U') IS NULL
BEGIN
    CREATE TABLE dw.dim_order
    (
        order_key INT IDENTITY(1,1) NOT NULL,
        order_id VARCHAR(32) NOT NULL,
        order_status VARCHAR(20) NOT NULL,

        order_purchase_timestamp DATETIME2 NULL,
        order_approved_at DATETIME2 NULL,
        order_delivered_carrier_date DATETIME2 NULL,
        order_delivered_customer_date DATETIME2 NULL,
        order_estimated_delivery_date DATETIME2 NULL,

        CONSTRAINT PK_dim_order
            PRIMARY KEY (order_key),

        CONSTRAINT UQ_dim_order_id
            UNIQUE (order_id)
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
  AND TABLE_NAME = 'dim_order'
ORDER BY ORDINAL_POSITION;
GO

-- Verification du volume initial
SELECT COUNT(*) AS total_orders
FROM dw.dim_order;
GO
