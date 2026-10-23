# Relations entre les tables Olist

## Objectif
Vérifier les relations avant la modélisation SQL Server

## Relations identifiées

| Table parent | Clé | Table enfant | Clé étrangère |
|---|---|---|---|
| customers | customer_id | orders | customer_id |
| orders | order_id | order_items | order_id |
| products | product_id | order_items | product_id |

## Clés primaires candidates
- customers : customer_id
- orders : order_id
- products : product_id
- order_items : (order_id, order_item_id)

## Contrôles réalisés
- Aucune clé primaire candidate nulle ou dupliquée
- Aucune clé composite dupliquée dans order_items
- Aucune référence étrangère orpheline détectée...

## Commandes sans article

775 commandes :

| Statut | Nombre |
|---|---:|
| unavailable | 603 |
| canceled | 164 |
| created | 5 |
| invoiced | 2 |
| shipped | 1 |

Ces commandes seront conservées pendant l'exploration.
Leur traitement métier sera défini dans l'ETL...

## Script
src/check_relationships.py

## Ticket Jira
SCRUM-16