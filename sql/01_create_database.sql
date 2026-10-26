
-- ShopFlow DataOps
-- Jira : SCRUM-22
-- Création de la base ShopFlowDB

USE master;
GO

IF DB_ID(N'ShopFlowDB') IS NULL
BEGIN
    CREATE DATABASE ShopFlowDB;
END;
GO

SELECT
    name AS database_name,
    state_desc AS database_status
FROM sys.databases
WHERE name = N'ShopFlowDB';
GO
