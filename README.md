# 🛒 ShopFlow DataOps

**Projet Data Engineering & DevOps — Pipeline ETL E-commerce**

## 📌 Présentation

ShopFlow DataOps est un projet de Data Engineering visant à construire un pipeline ETL automatisé pour traiter, contrôler, transformer et charger des données e-commerce dans Microsoft SQL Server.

Le projet applique progressivement les bonnes pratiques DevOps : Git, GitHub, branches de fonctionnalités, Pull Requests, Docker, Jenkins CI/CD et gestion Agile avec Jira Scrum.

## 🎯 Objectifs

- Collecter des données e-commerce historiques et synthétiques.
- Explorer et contrôler la qualité des données.
- Identifier les relations entre les tables.
- Concevoir un modèle relationnel SQL Server.
- Développer un pipeline ETL Python et Pandas.
- Automatiser les tests avec Pytest.
- Conteneuriser l'application avec Docker.
- Mettre en place un pipeline CI/CD avec Jenkins.
- Piloter le développement avec Jira et Scrum.

## 🛠️ Technologies

| Technologie | Utilisation |
|---|---|
| Python 3.14 | Développement des scripts |
| Pandas | Exploration et contrôle des données |
| SQL Server | Base de données cible (à venir) |
| Git / GitHub | Versionnement et Pull Requests |
| Jira / Scrum | Gestion Agile du projet |
| Pytest | Tests automatisés (à venir) |
| Docker | Conteneurisation (à venir) |
| Jenkins | Pipeline CI/CD (à venir) |
| Faker | Données synthétiques (à venir) |

## 📂 Structure du projet

```text
shopflow-dataops/
│
├── data/
│   ├── raw/                     # CSV Olist locaux
│   └── processed/               # Futures données transformées
│
├── src/
│   ├── inspect_olist.py
│   ├── check_relationships.py
│   └── check_data_quality.py
│
├── docs/
│   ├── git-workflow.md
│   ├── olist-inventory.md
│   ├── olist-relationships.md
│   └── olist-data-quality.md
│
├── sql/
├── tests/
├── docker/
├── jenkins/
│
├── .gitignore
└── README.md
```

Les fichiers CSV bruts et l'environnement virtuel `.venv` sont exclus du dépôt GitHub.

## 📊 Source des données

**Brazilian E-Commerce Public Dataset by Olist**

Source : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Le dataset contient neuf fichiers CSV représentant les commandes, clients, produits, paiements, avis, vendeurs et données géographiques.

Des données synthétiques seront également générées avec Python et Faker dans une prochaine phase.

## ✅ Travaux réalisés

### Sprint 1 — Fondations & Git

- Création du dépôt GitHub.
- Initialisation de Git local.
- Configuration du `.gitignore`.
- Création de la structure du projet.
- Définition de la stratégie de branches.
- Mise en place du workflow Git : branche, commit, push, Pull Request et merge.

### Sprint 2 — Exploration et Data Quality

**SCRUM-14 — Acquisition Olist**
- Téléchargement et organisation des neuf CSV Olist.

**SCRUM-15 — Inventaire**
- Script `inspect_olist.py`.
- Inventaire des fichiers, lignes et colonnes.

**SCRUM-16 — Relations**
- Script `check_relationships.py`.
- Analyse des relations entre commandes, clients, produits et articles.
- Vérification des clés primaires candidates et des clés étrangères.
- Identification de 775 commandes sans article.

**SCRUM-17 — Qualité des données**
- Script `check_data_quality.py`.
- Analyse des doublons et valeurs manquantes.
- Contrôle des prix et frais de livraison.
- Contrôle de la cohérence chronologique.
- Rédaction du rapport qualité.

## 🔎 Principaux résultats Data Quality

| Contrôle | Résultat |
|---|---:|
| Commandes analysées | 99 441 |
| Lignes d'articles | 112 650 |
| Produits | 32 951 |
| Doublons complets dans les 4 fichiers analysés | 0 |
| Commandes sans article | 775 |
| Prix négatifs | 0 |
| Frais de livraison nuls | 383 |
| Remises au transporteur avant achat | 166 |
| Livraisons avant remise au transporteur | 23 |

Les anomalies identifiées sont documentées et seront prises en compte lors de la conception des règles ETL.

## ▶️ Exécution locale

Prérequis : Python et les neuf fichiers CSV Olist placés dans `data/raw/`.

Créer l'environnement virtuel :

```powershell
python -m venv .venv
```

L'activer sous PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer Pandas :

```powershell
python -m pip install pandas
```

Lancer les scripts :

```powershell
python src/inspect_olist.py
python src/check_relationships.py
python src/check_data_quality.py
```

## 🔄 Organisation Agile :

Le projet est suivi dans Jira à travers des tickets associés aux branches et aux commits Git.

Convention de branches :

- `main` : version stable.
- `feature/SCRUM-ID-description` : fonctionnalités.
- `fix/SCRUM-ID-description` : corrections.

Les modifications sont intégrées dans `main` via Pull Request.

## 🗺️ Prochaines étapes /

- [ ] SCRUM-18 — Analyser le schéma des données.
- [ ] SCRUM-19 — Explorer des échantillons.
- [ ] SCRUM-20 — Finaliser les observations d'exploration.
- [ ] Concevoir les tables SQL Server.
- [ ] Développer les transformations ETL.
- [ ] Ajouter les tests Pytest.
- [ ] Intégrer Docker.
- [ ] Automatiser la CI/CD avec Jenkins.
- [ ] Générer des données synthétiques avec Faker.

## 📄 Statut

Projet en développement — Sprint 2 : exploration des données et préparation de la modélisation SQL Server.