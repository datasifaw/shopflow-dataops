
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-49 : Evolution mensuelle des ventes livrees
-- Source : Data Warehouse ShopFlow
-- =====================================================

CREATE OR ALTER VIEW dw.vw_monthly_sales
AS
SELECT
    d.[year] AS sales_year,
    d.[month] AS sales_month,
    d.year_month,

    COUNT(DISTINCT o.order_id) AS total_orders,

    COUNT_BIG(*) AS total_items,

    SUM(fs.quantity) AS total_quantity,

    SUM(fs.unit_price) AS product_revenue,

    SUM(fs.freight_value) AS freight_revenue,

    SUM(fs.total_amount) AS total_revenue,

    CAST(
        SUM(fs.unit_price)
        / NULLIF(COUNT(DISTINCT o.order_id), 0)
        AS DECIMAL(18,2)
    ) AS average_order_value

FROM dw.fact_sales AS fs

INNER JOIN dw.dim_order AS o
    ON o.order_key = fs.order_key

INNER JOIN dw.dim_date AS d
    ON d.date_key = fs.date_key

WHERE o.order_status = 'delivered'

GROUP BY
    d.[year],
    d.[month],
    d.year_month;
GO

-- =====================================================
-- Verification : evolution chronologique
-- =====================================================

SELECT
    sales_year,
    sales_month,
    year_month,
    total_orders,
    total_items,
    product_revenue,
    freight_revenue,
    total_revenue,
    average_order_value
FROM dw.vw_monthly_sales
ORDER BY sales_year, sales_month;
GO

-- =====================================================
-- Reconciliation avec les KPI globaux
-- =====================================================

SELECT
    SUM(total_items) AS monthly_items,
    SUM(product_revenue) AS monthly_product_revenue,
    SUM(freight_revenue) AS monthly_freight_revenue,
    SUM(total_revenue) AS monthly_total_revenue
FROM dw.vw_monthly_sales;
GO
