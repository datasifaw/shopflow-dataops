
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-47 : Creation de la dimension calendrier
-- =====================================================

IF OBJECT_ID('dw.dim_date', 'U') IS NULL
BEGIN
    CREATE TABLE dw.dim_date
    (
        date_key INT NOT NULL,
        full_date DATE NOT NULL,

        [year] SMALLINT NOT NULL,
        [quarter] TINYINT NOT NULL,
        [month] TINYINT NOT NULL,
        month_name NVARCHAR(20) NOT NULL,
        year_month CHAR(7) NOT NULL,

        day_of_month TINYINT NOT NULL,
        day_of_week TINYINT NOT NULL,
        day_name NVARCHAR(20) NOT NULL,

        is_weekend BIT NOT NULL,

        CONSTRAINT PK_dim_date
            PRIMARY KEY (date_key),

        CONSTRAINT UQ_dim_date_full_date
            UNIQUE (full_date)
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
  AND TABLE_NAME = 'dim_date'
ORDER BY ORDINAL_POSITION;
GO

-- Verification du volume initial
SELECT COUNT(*) AS total_dates
FROM dw.dim_date;
GO
