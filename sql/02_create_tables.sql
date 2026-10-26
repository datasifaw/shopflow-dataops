
-- ShopFlow DataOps
-- SCRUM-25 : Structure initiale des tables Olist

USE ShopFlowDB;
GO

-- 1. Clients
IF OBJECT_ID(N'dbo.customers', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.customers (
        customer_id VARCHAR(32) NOT NULL PRIMARY KEY,
        customer_unique_id VARCHAR(32) NOT NULL,
        customer_zip_code_prefix VARCHAR(5) NOT NULL,
        customer_city NVARCHAR(100) NOT NULL,
        customer_state CHAR(2) NOT NULL
    );
END;
GO

-- 2. Produits
IF OBJECT_ID(N'dbo.products', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.products (
        product_id VARCHAR(32) NOT NULL PRIMARY KEY,
        product_category_name NVARCHAR(100) NULL,
        product_name_lenght INT NULL,
        product_description_lenght INT NULL,
        product_photos_qty INT NULL,
        product_weight_g INT NULL,
        product_length_cm INT NULL,
        product_height_cm INT NULL,
        product_width_cm INT NULL
    );
END;
GO

-- 3. Commandes
IF OBJECT_ID(N'dbo.orders', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.orders (
        order_id VARCHAR(32) NOT NULL PRIMARY KEY,
        customer_id VARCHAR(32) NOT NULL,
        order_status VARCHAR(20) NOT NULL,
        order_purchase_timestamp DATETIME2(0) NOT NULL,
        order_approved_at DATETIME2(0) NULL,
        order_delivered_carrier_date DATETIME2(0) NULL,
        order_delivered_customer_date DATETIME2(0) NULL,
        order_estimated_delivery_date DATETIME2(0) NOT NULL
    );
END;
GO

-- 4. Articles commandés
IF OBJECT_ID(N'dbo.order_items', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.order_items (
        order_id VARCHAR(32) NOT NULL,
        order_item_id INT NOT NULL,
        product_id VARCHAR(32) NOT NULL,
        seller_id VARCHAR(32) NOT NULL,
        shipping_limit_date DATETIME2(0) NOT NULL,
        price DECIMAL(12,2) NOT NULL,
        freight_value DECIMAL(12,2) NOT NULL,
        CONSTRAINT PK_order_items PRIMARY KEY (order_id, order_item_id)
    );
END;
GO

-- Vérification
SELECT
    name AS table_name
FROM sys.tables
WHERE name IN ('customers', 'products', 'orders', 'order_items')
ORDER BY name;
GO
  