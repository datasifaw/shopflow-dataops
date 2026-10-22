# Inventaire du dataset Olist

## Objectif
Inventorier les fichiers CSV utilisés dans ShopFlow DataOps.

## Source
Brazilian E-Commerce Public Dataset by Olist (Kaggle).

## Inventaire

| Dataset | Lignes | Colonnes |
|---|---:|---:|
| Customers | 99441 | 5 |
| Geolocation | 1000163 | 5 |
| Order Items | 112650 | 7 |
| Order Payments | 103886 | 5 |
| Order Reviews | 99224 | 7 |
| Orders | 99441 | 8 |
| Products | 32951 | 9 |
| Sellers | 3095 | 4 |
| Category Translation | 71 | 2 |

## Méthode
Inventaire réalisé avec Python, Pandas et
le script `src/inspect_olist.py`.

## Stockage
Les CSV sont conservés dans `data/raw/`
et exclus de Git.

## Ticket Jira
SCRUM-15