
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-47 : Creation de la table de faits Sales
-- Grain : un article par commande
-- =====================================================

IF OBJECT_ID('dw.fact_sales', 'U') IS NULL
BEGIN
    CREATE TABLE dw.fact_sales
    (
        sales_key BIGINT IDENTITY(1,1) NOT NULL,

        order_key INT NOT NULL,
        customer_key INT NOT NULL,
        product_key INT NOT NULL,
        date_key INT NOT NULL,

        order_item_id INT NOT NULL,

        quantity INT NOT NULL
            CONSTRAINT DF_fact_sales_quantity DEFAULT (1),

        unit_price DECIMAL(12,2) NOT NULL,
        freight_value DECIMAL(12,2) NOT NULL,

        total_amount AS
            (unit_price + freight_value) PERSISTED,

        CONSTRAINT PK_fact_sales
            PRIMARY KEY (sales_key),

        CONSTRAINT UQ_fact_sales_order_item
            UNIQUE (order_key, order_item_id),

        CONSTRAINT FK_fact_sales_order
            FOREIGN KEY (order_key)
            REFERENCES dw.dim_order(order_key),

        CONSTRAINT FK_fact_sales_customer
            FOREIGN KEY (customer_key)
            REFERENCES dw.dim_customer(customer_key),

        CONSTRAINT FK_fact_sales_product
            FOREIGN KEY (product_key)
            REFERENCES dw.dim_product(product_key),

        CONSTRAINT FK_fact_sales_date
            FOREIGN KEY (date_key)
            REFERENCES dw.dim_date(date_key),

        CONSTRAINT CK_fact_sales_quantity
            CHECK (quantity > 0),

        CONSTRAINT CK_fact_sales_amounts
            CHECK (
                unit_price >= 0
                AND freight_value >= 0
            )
    );
END;
GO

-- =====================================================
-- Verification de la structure
-- =====================================================

SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dw'
  AND TABLE_NAME = 'fact_sales'
ORDER BY ORDINAL_POSITION;
GO

-- =====================================================
-- Verification des cles et contraintes
-- =====================================================

SELECT
    fk.name AS foreign_key_name,
    OBJECT_NAME(fk.parent_object_id) AS source_table,
    OBJECT_NAME(fk.referenced_object_id) AS target_table
FROM sys.foreign_keys AS fk
WHERE fk.parent_object_id = OBJECT_ID('dw.fact_sales');
GO

-- =====================================================
-- Verification du volume initial
-- =====================================================

SELECT COUNT(*) AS total_sales
FROM dw.fact_sales;
GO
