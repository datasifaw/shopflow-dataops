
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-49 : Ventes par Etat bresilien
-- Source : Data Warehouse ShopFlow
-- Commandes livrees uniquement
-- =====================================================

CREATE OR ALTER VIEW dw.vw_sales_by_state
AS
SELECT
    c.customer_state AS state_code,

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

INNER JOIN dw.dim_customer AS c
    ON c.customer_key = fs.customer_key

INNER JOIN dw.dim_order AS o
    ON o.order_key = fs.order_key

WHERE o.order_status = 'delivered'

GROUP BY
    c.customer_state;
GO

-- =====================================================
-- 1. Classement des Etats par CA produits
-- =====================================================

SELECT
    state_code,
    total_orders,
    total_items,
    product_revenue,
    freight_revenue,
    total_revenue,
    average_order_value
FROM dw.vw_sales_by_state
ORDER BY product_revenue DESC;
GO

-- =====================================================
-- 2. Reconciliation des montants
-- =====================================================

SELECT
    COUNT(*) AS total_states,
    SUM(total_items) AS state_items,
    SUM(product_revenue) AS state_product_revenue,
    SUM(freight_revenue) AS state_freight_revenue,
    SUM(total_revenue) AS state_total_revenue
FROM dw.vw_sales_by_state;
GO

-- =====================================================
-- 3. Comparaison avec les KPI globaux
-- =====================================================

SELECT
    s.state_total_revenue,
    r.total_revenue AS global_total_revenue,
    s.state_total_revenue - r.total_revenue
        AS revenue_difference
FROM (
    SELECT SUM(total_revenue) AS state_total_revenue
    FROM dw.vw_sales_by_state
) AS s
CROSS JOIN dw.vw_revenue_summary AS r;
GO
