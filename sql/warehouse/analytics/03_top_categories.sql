
USE ShopFlowDB;
GO

-- =====================================================
-- SCRUM-49 : Top categories de produits
-- Uniquement les commandes livrees
-- =====================================================

CREATE OR ALTER VIEW dw.vw_top_categories
AS
SELECT
    COALESCE(
        p.product_category_name,
        'unknown'
    ) AS product_category,

    COUNT_BIG(*) AS total_items,

    COUNT(DISTINCT o.order_id) AS total_orders,

    SUM(fs.quantity) AS total_quantity,

    SUM(fs.unit_price) AS product_revenue,

    SUM(fs.freight_value) AS freight_revenue,

    SUM(fs.total_amount) AS total_revenue

FROM dw.fact_sales AS fs

INNER JOIN dw.dim_product AS p
    ON p.product_key = fs.product_key

INNER JOIN dw.dim_order AS o
    ON o.order_key = fs.order_key

WHERE o.order_status = 'delivered'

GROUP BY
    COALESCE(
        p.product_category_name,
        'unknown'
    );
GO

-- =====================================================
-- Top 15 categories par chiffre d'affaires produits
-- =====================================================

SELECT TOP (15)
    product_category,
    total_orders,
    total_items,
    product_revenue,
    freight_revenue,
    total_revenue
FROM dw.vw_top_categories
ORDER BY product_revenue DESC;
GO

-- =====================================================
-- Reconciliation des montants
-- =====================================================

SELECT
    SUM(total_items) AS category_items,
    SUM(product_revenue) AS category_product_revenue,
    SUM(freight_revenue) AS category_freight_revenue,
    SUM(total_revenue) AS category_total_revenue
FROM dw.vw_top_categories;
GO
