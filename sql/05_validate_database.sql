
-- ShopFlow DataOps
-- SCRUM-27 : Validation de ShopFlowDB

USE ShopFlowDB;
GO

-- 1. Etat de la base
SELECT name, state_desc
FROM sys.databases
WHERE name = N'ShopFlowDB';
GO

-- 2. Tables principales
SELECT name AS table_name
FROM sys.tables
WHERE schema_id = SCHEMA_ID(N'dbo')
  AND name IN (
      N'customers',
      N'orders',
      N'products',
      N'order_items'
  )
ORDER BY name;
GO

-- 3. Cles primaires
SELECT
    OBJECT_NAME(parent_object_id) AS table_name,
    name AS primary_key
FROM sys.key_constraints
WHERE type = 'PK'
  AND parent_object_id IN (
      OBJECT_ID(N'dbo.customers'),
      OBJECT_ID(N'dbo.orders'),
      OBJECT_ID(N'dbo.products'),
      OBJECT_ID(N'dbo.order_items')
  );
GO

-- 4. Cles etrangeres
SELECT
    name AS foreign_key,
    is_disabled,
    is_not_trusted
FROM sys.foreign_keys
WHERE parent_object_id IN (
    OBJECT_ID(N'dbo.orders'),
    OBJECT_ID(N'dbo.order_items')
);
GO

-- 5. Roles de securite
SELECT name AS role_name
FROM sys.database_principals
WHERE type = 'R'
  AND name IN (
      N'shopflow_reader',
      N'shopflow_etl'
  );
GO
