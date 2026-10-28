
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-48 : Chargement de dw.dim_date
-- Periode : 2016-01-01 au 2020-12-31
-- =====================================================

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

DECLARE @start_date DATE = '20160101';
DECLARE @end_date DATE = '20201231';
DECLARE @current_date DATE = @start_date;
DECLARE @inserted INT = 0;

BEGIN TRY
    BEGIN TRANSACTION;

    WHILE @current_date <= @end_date
    BEGIN
        DECLARE @date_key INT =
            YEAR(@current_date) * 10000
            + MONTH(@current_date) * 100
            + DAY(@current_date);

        -- Lundi = 1, dimanche = 7
        -- Independant de SET DATEFIRST
        DECLARE @day_of_week INT =
            (DATEDIFF(
                DAY,
                '19000101',
                @current_date
            ) % 7) + 1;

        IF NOT EXISTS (
            SELECT 1
            FROM dw.dim_date
            WHERE date_key = @date_key
        )
        BEGIN
            INSERT INTO dw.dim_date
            (
                date_key,
                full_date,
                [year],
                [quarter],
                [month],
                month_name,
                year_month,
                day_of_month,
                day_of_week,
                day_name,
                is_weekend
            )
            VALUES
            (
                @date_key,
                @current_date,
                YEAR(@current_date),
                DATEPART(QUARTER, @current_date),
                MONTH(@current_date),

                CHOOSE(
                    MONTH(@current_date),
                    'January', 'February', 'March',
                    'April', 'May', 'June',
                    'July', 'August', 'September',
                    'October', 'November', 'December'
                ),

                CONVERT(CHAR(7), @current_date, 120),
                DAY(@current_date),
                @day_of_week,

                CHOOSE(
                    @day_of_week,
                    'Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday',
                    'Saturday', 'Sunday'
                ),

                CASE
                    WHEN @day_of_week IN (6, 7)
                        THEN 1
                    ELSE 0
                END
            );

            SET @inserted = @inserted + 1;
        END;

        SET @current_date =
            DATEADD(DAY, 1, @current_date);
    END;

    COMMIT TRANSACTION;

    PRINT CONCAT(
        'Chargement dw.dim_date termine : ',
        @inserted,
        ' dates inserees.'
    );

END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO

-- =====================================================
-- Verification du calendrier
-- =====================================================

SELECT
    COUNT(*) AS total_dates,
    MIN(full_date) AS first_date,
    MAX(full_date) AS last_date
FROM dw.dim_date;
GO

-- Verification des doublons
SELECT
    full_date,
    COUNT(*) AS occurrences
FROM dw.dim_date
GROUP BY full_date
HAVING COUNT(*) > 1;
GO

-- Apercu : une semaine de mars 2018
SELECT
    date_key,
    full_date,
    [year],
    [quarter],
    [month],
    month_name,
    year_month,
    day_of_week,
    day_name,
    is_weekend
FROM dw.dim_date
WHERE full_date BETWEEN
    '20180312' AND '20180318'
ORDER BY full_date;
GO

-- Controle : dates d'achat des commandes
-- absentes du calendrier
SELECT COUNT(*) AS orders_outside_calendar
FROM dbo.orders AS o
LEFT JOIN dw.dim_date AS d
    ON d.full_date =
       CAST(o.order_purchase_timestamp AS DATE)
WHERE d.date_key IS NULL;
GO
