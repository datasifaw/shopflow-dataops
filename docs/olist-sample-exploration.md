# Exploration des données Olist

**Projet :** ShopFlow DataOps  
**Sprint :** Sprint 2 — ETL Olist & SQL Server  
**Ticket Jira :** SCRUM-19

## 1. Objectif

Explorer les principaux fichiers du dataset Olist afin de comprendre les données métier avant la conception du pipeline ETL.

L'exploration a été réalisée avec Python et Pandas à partir du script `src/explore_samples.py`.

## 2. Datasets analysés

| Dataset | Lignes | Colonnes |
|---|---:|---:|
| Orders | 99 441 | 8 |
| Order Items | 112 650 | 7 |
| Customers | 99 441 | 5 |
| Products | 32 951 | 9 |

Les données ont été explorées localement à l'aide de `head()` et `sample()`.

Aucune ligne client brute n'est reproduite dans ce document.

## 3. Statuts des commandes

| Statut | Nombre |
|---|---:|
| delivered | 96 478 |
| shipped | 1 107 |
| canceled | 625 |
| unavailable | 609 |
| invoiced | 314 |
| processing | 301 |
| created | 5 |
| approved | 2 |

### Analyse

Environ 97,02 % des commandes ont le statut `delivered`.

Les autres statuts représentent différentes étapes du cycle de vie d'une commande.

Les commandes annulées ou indisponibles devront être distinguées des ventes réalisées lors de la définition des indicateurs métier.

## 4. Catégories de produits

| Catégorie source | Nombre de produits |
|---|---:|
| cama_mesa_banho | 3 029 |
| esporte_lazer | 2 867 |
| moveis_decoracao | 2 657 |
| beleza_saude | 2 444 |
| utilidades_domesticas | 2 335 |
| automotivo | 1 900 |
| informatica_acessorios | 1 639 |
| brinquedos | 1 411 |
| relogios_presentes | 1 329 |
| telefonia | 1 134 |

Ces nombres correspondent aux références produits présentes dans le catalogue et non aux quantités vendues.

## 5. Observations métier

- Une commande peut contenir plusieurs lignes d'articles.
- Les montants des articles et les frais de livraison sont disponibles séparément.
- Les statuts des commandes devront être utilisés pour définir les ventes prises en compte dans les indicateurs.
- Les catégories produits pourront être traduites grâce au fichier `product_category_name_translation.csv`.
- Les identifiants clients et produits devront être conservés sous forme de chaînes de caractères.
- Les données brutes restent stockées localement et exclues de GitHub.

## 6. Prochaines étapes

- Finaliser les observations et conclusions de l'exploration.
- Concevoir le schéma relationnel SQL Server.
- Définir les règles de transformation des données.
- Développer le pipeline ETL Python.
- Ajouter les tests automatiques.

## 7. Traçabilité

**Script :** `src/explore_samples.py`  
**Documentation :** `docs/olist-sample-exploration.md`  
**Ticket Jira :** SCRUM-19