
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-49 : KPI globaux des ventes livrees
-- Source : Data Warehouse ShopFlow
-- =====================================================

CREATE OR ALTER VIEW dw.vw_revenue_summary
AS
SELECT
    COUNT_BIG(*) AS total_items,

    COUNT(DISTINCT o.order_id) AS total_orders,

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

WHERE o.order_status = 'delivered';
GO

-- =====================================================
-- Verification des KPI
-- =====================================================

SELECT
    total_items,
    total_orders,
    total_quantity,
    product_revenue,
    freight_revenue,
    total_revenue,
    average_order_value
FROM dw.vw_revenue_summary;
GO
