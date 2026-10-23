# Dictionnaire de données — ShopFlow DataOps

## Table customers

| Colonne | Type SQL Server | NULL |
|---|---|---|
| customer_id (PK) | VARCHAR(32) | Non |
| customer_unique_id | VARCHAR(32) | Non |
| customer_zip_code_prefix | VARCHAR(5) | Non |
| customer_city | NVARCHAR(100) | Non |
| customer_state | CHAR(2) | Non |

## Table orders

| Colonne | Type SQL Server | NULL |
|---|---|---|
| order_id (PK) | VARCHAR(32) | Non |
| customer_id (FK) | VARCHAR(32) | Non |
| order_status | VARCHAR(20) | Non |
| order_purchase_timestamp | DATETIME2(0) | Non |
| order_approved_at | DATETIME2(0) | Oui |
| order_delivered_carrier_date | DATETIME2(0) | Oui |
| order_delivered_customer_date | DATETIME2(0) | Oui |
| order_estimated_delivery_date | DATETIME2(0) | Non |

## Table order_items

| Colonne | Type SQL Server | NULL |
|---|---|---|
| order_id (PK, FK) | VARCHAR(32) | Non |
| order_item_id (PK) | INT | Non |
| product_id (FK) | VARCHAR(32) | Non |
| seller_id | VARCHAR(32) | Non |
| shipping_limit_date | DATETIME2(0) | Non |
| price | DECIMAL(12,2) | Non |
| freight_value | DECIMAL(12,2) | Non |

## Table products

| Colonne | Type SQL Server | NULL |
|---|---|---|
| product_id (PK) | VARCHAR(32) | Non |
| product_category_name | NVARCHAR(100) | Oui |
| product_name_lenght | INT | Oui |
| product_description_lenght | INT | Oui |
| product_photos_qty | INT | Oui |
| product_weight_g | INT | Oui |
| product_length_cm | INT | Oui |
| product_height_cm | INT | Oui |
| product_width_cm | INT | Oui |

## Relations

- customers → orders : customer_id
- orders → order_items : order_id
- products → order_items : product_id

Clé primaire composite de order_items :
(order_id, order_item_id)

## Notes

Les types proposés seront validés lors du chargement SQL Server.
Les CSV bruts restent exclus de Git.

Ticket Jira : SCRUM-18