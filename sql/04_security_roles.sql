
-- ShopFlow DataOps
-- SCRUM-26 : Roles et permissions SQL Server

USE ShopFlowDB;
GO

-- 1. Role de lecture seule
IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = N'shopflow_reader'
      AND type = 'R'
)
BEGIN
    CREATE ROLE shopflow_reader
        AUTHORIZATION dbo;
END;
GO

-- 2. Role pour le pipeline ETL
IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = N'shopflow_etl'
      AND type = 'R'
)
BEGIN
    CREATE ROLE shopflow_etl
        AUTHORIZATION dbo;
END;
GO

-- 3. Permissions de lecture
GRANT SELECT ON SCHEMA::dbo
TO shopflow_reader;
GO

-- 4. Permissions du pipeline ETL
GRANT SELECT, INSERT, UPDATE
ON SCHEMA::dbo
TO shopflow_etl;
GO

-- 5. Verification des roles
SELECT
    name AS role_name,
    type_desc
FROM sys.database_principals
WHERE name IN (
    N'shopflow_reader',
    N'shopflow_etl'
);
GO

-- 6. Verification des permissions
SELECT
    USER_NAME(p.grantee_principal_id) AS role_name,
    p.permission_name,
    p.state_desc,
    p.class_desc
FROM sys.database_permissions AS p
WHERE p.grantee_principal_id IN (
    DATABASE_PRINCIPAL_ID(N'shopflow_reader'),
    DATABASE_PRINCIPAL_ID(N'shopflow_etl')
)
ORDER BY role_name, permission_name;
GO
