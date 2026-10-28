
USE ShopFlowDB;
GO

-- Schema dedie au Data Warehouse
IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'dw'
)
BEGIN
    EXEC('CREATE SCHEMA dw');
END;
GO

-- Verification du schema
SELECT
    name AS schema_name,
    schema_id
FROM sys.schemas
WHERE name = 'dw';
GO
