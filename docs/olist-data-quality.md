# Rapport de qualité des données Olist

**Projet :** ShopFlow DataOps  
**Sprint :** Sprint 2 — ETL Olist & SQL Server  
**Ticket Jira :** SCRUM-17  
**Outils :** Python, Pandas  
**Script :** `src/check_data_quality.py`

## 1. Objectif

Analyser la qualité des données e-commerce Olist avant leur transformation et leur chargement dans Microsoft SQL Server.

Les contrôles portent sur les valeurs manquantes, les doublons, les prix, les frais de livraison et la cohérence chronologique des commandes.

## 2. Fichiers analysés

| Dataset | Nombre de lignes | Doublons complets |
|---|---:|---:|
| Orders | 99 441 | 0 |
| Order Items | 112 650 | 0 |
| Customers | 99 441 | 0 |
| Products | 32 951 | 0 |

Aucun doublon de ligne complète n'a été détecté dans les quatre fichiers analysés.

## 3. Valeurs manquantes

### Table Orders

| Colonne | Valeurs manquantes |
|---|---:|
| order_approved_at | 160 |
| order_delivered_carrier_date | 1 783 |
| order_delivered_customer_date | 2 965 |

**Analyse :** les dates absentes peuvent correspondre à des commandes non approuvées, annulées ou non livrées. Leur interprétation dépend du statut de la commande.

### Table Products

| Colonne | Valeurs manquantes |
|---|---:|
| product_category_name | 610 |
| product_name_lenght | 610 |
| product_description_lenght | 610 |
| product_photos_qty | 610 |
| product_weight_g | 2 |
| product_length_cm | 2 |
| product_height_cm | 2 |
| product_width_cm | 2 |

**Analyse :** certaines fiches produits sont incomplètes. Ces valeurs nécessitent une politique de traitement adaptée à leur utilisation dans le pipeline ETL.

Les tables Customers et Order Items ne présentent aucune valeur manquante détectée par les contrôles exécutés.

## 4. Contrôle des prix

Colonne analysée : `price`

| Indicateur | Résultat |
|---|---:|
| Valeurs non numériques ou manquantes | 0 |
| Prix négatifs | 0 |
| Prix égaux à zéro | 0 |
| Prix minimum | 0,85 |
| Prix maximum | 6 735,00 |

**Analyse :** aucune valeur négative, nulle ou non numérique n'a été détectée. Les prix extrêmes, notamment le maximum de 6 735,00, pourront faire l'objet d'une analyse statistique complémentaire.

## 5. Contrôle des frais de livraison

Colonne analysée : `freight_value`

| Indicateur | Résultat |
|---|---:|
| Valeurs non numériques ou manquantes | 0 |
| Valeurs négatives | 0 |
| Valeurs égales à zéro | 383 |
| Frais minimum | 0,00 |
| Frais maximum | 409,68 |

**Analyse :** les 383 lignes dont les frais de livraison sont nuls ne représentent pas nécessairement des anomalies. Elles peuvent notamment correspondre à des livraisons gratuites ou à des règles commerciales particulières.

## 6. Contrôle de cohérence des dates

| Contrôle | Anomalies détectées |
|---|---:|
| Approbation avant achat | 0 |
| Remise au transporteur avant achat | 166 |
| Livraison client avant achat | 0 |
| Livraison client avant remise au transporteur | 23 |

**Analyse :**

- Les dates d'approbation et de livraison client ne présentent aucune inversion par rapport à la date d'achat dans les enregistrements comparables.
- 166 commandes présentent une date de remise au transporteur antérieure à la date d'achat.
- 23 commandes présentent une date de livraison client antérieure à la date de remise au transporteur.

Ces anomalies devront être analysées avant d'appliquer des corrections. Des erreurs de saisie, de synchronisation ou de traitement informatique peuvent en être la cause, sans que cela soit établi à ce stade.

Les comparaisons ont été effectuées uniquement lorsque les deux dates concernées étaient présentes et convertibles.

## 7. Décisions provisoires pour l'ETL

1. Conserver les données brutes intactes dans `data/raw/`.
2. Ne pas supprimer automatiquement les commandes avec des dates manquantes.
3. Signaler les 166 cas de transport avant achat et les 23 cas de livraison avant transport.
4. Conserver provisoirement les frais de livraison égaux à zéro.
5. Examiner les produits incomplets avant de définir des règles de remplacement ou d'exclusion.
6. Prévoir un traitement explicite des anomalies dans la couche de transformation.
7. Conserver la traçabilité des anomalies dans les futurs rapports de qualité.

## 8. Conclusion

Les quatre datasets analysés ne présentent aucun doublon de ligne complète. Les prix ne contiennent aucune valeur négative ou nulle, et les principaux identifiants ont été contrôlés dans l'analyse relationnelle précédente.

Cependant, des valeurs manquantes et des incohérences chronologiques ont été identifiées.

**Le dataset est exploitable pour poursuivre la conception du pipeline ETL, sous réserve de définir et d'appliquer des règles métier adaptées aux anomalies détectées.**

## 9. Traçabilité

- Source : Brazilian E-Commerce Public Dataset by Olist
- Script : `src/check_data_quality.py`
- Documentation : `docs/olist-data-quality.md`
- Ticket Jira : SCRUM-17
- Projet : ShopFlow DataOps