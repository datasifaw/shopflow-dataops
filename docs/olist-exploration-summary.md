# ShopFlow DataOps — Rapport de synthèse Olist

**Projet :** ShopFlow DataOps  
**Sprint :** Sprint 2 — Exploration e-commerce  
**Ticket Jira :** SCRUM-20  
**Technologies :** Python, Pandas, Git, GitHub, Jira  
**Source :** Brazilian E-Commerce Public Dataset by Olist

## 1. Objectif

Ce document synthétise les travaux d'exploration réalisés sur le dataset Olist afin de préparer la conception d'un pipeline ETL Python vers Microsoft SQL Server.

L'analyse couvre l'inventaire des fichiers, les relations entre tables, la qualité des données, le choix des types SQL et les observations métier.

## 2. Inventaire des données

Le dataset contient neuf fichiers CSV.

| Dataset | Lignes | Colonnes |
|---|---:|---:|
| Customers | 99 441 | 5 |
| Orders | 99 441 | 8 |
| Order Items | 112 650 | 7 |
| Products | 32 951 | 9 |
| Payments | 103 886 | 5 |
| Reviews | 99 224 | 7 |
| Sellers | 3 095 | 4 |
| Geolocation | 1 000 163 | 5 |
| Category Translation | 71 | 2 |

La première version du pipeline ETL utilisera principalement les tables Customers, Orders, Order Items et Products.

## 3. Modèle relationnel

Les relations suivantes ont été identifiées :

| Table parent | Table enfant | Clé de relation |
|---|---|---|
| Customers | Orders | customer_id |
| Orders | Order Items | order_id |
| Products | Order Items | product_id |

Clés primaires candidates :

- Customers : `customer_id`
- Orders : `order_id`
- Products : `product_id`
- Order Items : (`order_id`, `order_item_id`)

Les contrôles réalisés n'ont détecté aucune référence orpheline dans les relations testées.

Cependant, **775 commandes ne possèdent aucune ligne dans Order Items**.

## 4. Qualité des données

### Doublons

Aucun doublon de ligne complète n'a été détecté dans les quatre tables principales analysées.

### Valeurs manquantes

**Orders :**

| Colonne | Valeurs manquantes |
|---|---:|
| order_approved_at | 160 |
| order_delivered_carrier_date | 1 783 |
| order_delivered_customer_date | 2 965 |

**Products :** 610 valeurs manquantes dans plusieurs colonnes descriptives et 2 dans chacune des colonnes de poids et de dimensions.

### Prix et transport

| Contrôle | Résultat |
|---|---:|
| Prix minimum | 0,85 |
| Prix maximum | 6 735,00 |
| Prix négatifs | 0 |
| Prix nuls | 0 |
| Frais de livraison nuls | 383 |
| Frais maximum | 409,68 |

### Dates

| Contrôle | Anomalies |
|---|---:|
| Approbation avant achat | 0 |
| Transport avant achat | 166 |
| Livraison avant achat | 0 |
| Livraison avant transport | 23 |

Ces anomalies chronologiques doivent être signalées et analysées sans modification automatique des données brutes.

## 5. Observations métier

### Statuts des commandes

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

Environ 97 % des commandes sont livrées.

Les commandes annulées ou indisponibles devront être distinguées des ventes retenues dans les indicateurs métier.

### Principales catégories de produits

| Catégorie | Nombre de références |
|---|---:|
| cama_mesa_banho | 3 029 |
| esporte_lazer | 2 867 |
| moveis_decoracao | 2 657 |
| beleza_saude | 2 444 |
| utilidades_domesticas | 2 335 |

Ces chiffres représentent le nombre de références produits et non les quantités vendues.

## 6. Décisions techniques pour SQL Server

| Donnée | Type SQL Server proposé |
|---|---|
| Identifiants alphanumériques | VARCHAR(32) |
| Statut de commande | VARCHAR(20) |
| Prix et frais de livraison | DECIMAL(12,2) |
| Dates | DATETIME2(0) |
| Identifiants de lignes | INT |
| Préfixe postal | VARCHAR(5) |
| Ville | NVARCHAR(100) |
| Colonnes quantitatives entières | INT |

Les types restent à valider lors du chargement.

Les noms des colonnes source seront conservés pour assurer leur traçabilité.

## 7. Règles ETL envisagées

1. Conserver les données brutes intactes.
2. Vérifier la présence des colonnes obligatoires.
3. Convertir les dates avec contrôle des valeurs invalides.
4. Convertir les prix vers des types décimaux adaptés.
5. Contrôler les clés primaires et les relations.
6. Conserver les commandes sans article dans la table Orders.
7. Signaler les incohérences de dates dans un rapport qualité.
8. Éviter les doublons lors des chargements répétés.
9. Définir explicitement les règles de calcul du chiffre d'affaires.
10. Conserver une traçabilité des fichiers traités.

## 8. Architecture cible

```text
Olist CSV
    |
    v
Extraction Python
    |
    v
Validation Data Quality
    |
    v
Transformation Pandas
    |
    v
Microsoft SQL Server
    |
    v
Indicateurs e-commerce
```

L'automatisation avec Docker, Jenkins et les tests Pytest sera introduite progressivement.

## 9. Prochains travaux

- Concevoir les scripts SQL Server `CREATE TABLE`.
- Mettre en place la base ShopFlowDB.
- Développer les scripts d'extraction et de transformation.
- Charger les quatre premières tables dans SQL Server.
- Vérifier les volumes chargés et les contraintes.
- Ajouter des tests automatisés.
- Mettre en place Docker et Jenkins CI/CD.
- Générer des commandes synthétiques avec Faker.

## 10. Conclusion

Les travaux d'exploration ont permis de comprendre la structure du dataset Olist, d'identifier ses principales relations et de caractériser plusieurs anomalies métier.

Ces résultats constituent la base de la conception du pipeline ETL ShopFlow DataOps.

Le prochain objectif technique consiste à créer un modèle relationnel SQL Server cohérent avec les données observées, puis à développer un chargement automatisé, contrôlé et reproductible.

## 11. Références internes

- `src/inspect_olist.py`
- `src/check_relationships.py`
- `src/check_data_quality.py`
- `src/analyze_schema.py`
- `src/explore_samples.py`
- `docs/olist-data-dictionary.md`
- `docs/olist-data-quality.md`
- `docs/olist-relationships.md`

**Ticket Jira : SCRUM-20**