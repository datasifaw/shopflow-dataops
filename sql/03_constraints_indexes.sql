
-- ShopFlow DataOps
-- SCRUM-24 : Contraintes d'intégrité et index

USE ShopFlowDB;
GO

-- 1. orders -> customers
IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = N'FK_orders_customers'
      AND parent_object_id = OBJECT_ID(N'dbo.orders')
)
BEGIN
    ALTER TABLE dbo.orders WITH CHECK
    ADD CONSTRAINT FK_orders_customers
        FOREIGN KEY (customer_id)
        REFERENCES dbo.customers(customer_id);
END;
GO

-- 2. order_items -> orders
IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = N'FK_order_items_orders'
      AND parent_object_id = OBJECT_ID(N'dbo.order_items')
)
BEGIN
    ALTER TABLE dbo.order_items WITH CHECK
    ADD CONSTRAINT FK_order_items_orders
        FOREIGN KEY (order_id)
        REFERENCES dbo.orders(order_id);
END;
GO

-- 3. order_items -> products
IF NOT EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = N'FK_order_items_products'
      AND parent_object_id = OBJECT_ID(N'dbo.order_items')
)
BEGIN
    ALTER TABLE dbo.order_items WITH CHECK
    ADD CONSTRAINT FK_order_items_products
        FOREIGN KEY (product_id)
        REFERENCES dbo.products(product_id);
END;
GO

-- Index pour les jointures

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = N'IX_orders_customer_id'
      AND object_id = OBJECT_ID(N'dbo.orders')
)
BEGIN
    CREATE INDEX IX_orders_customer_id
    ON dbo.orders(customer_id);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = N'IX_order_items_product_id'
      AND object_id = OBJECT_ID(N'dbo.order_items')
)
BEGIN
    CREATE INDEX IX_order_items_product_id
    ON dbo.order_items(product_id);
END;
GO

-- Vérification des clés étrangères
SELECT
    name AS foreign_key_name,
    OBJECT_NAME(parent_object_id) AS table_name,
    OBJECT_NAME(referenced_object_id) AS parent_table,
    is_disabled,
    is_not_trusted
FROM sys.foreign_keys
WHERE parent_object_id IN (
    OBJECT_ID(N'dbo.orders'),
    OBJECT_ID(N'dbo.order_items')
)
ORDER BY name;
GO
