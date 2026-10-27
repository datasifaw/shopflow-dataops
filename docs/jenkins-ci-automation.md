# Jenkins CI — Déclenchement automatique

## Objectif

Automatiser l'exécution des tests de qualité Python de ShopFlow DataOps à chaque nouveau commit détecté sur la branche `main`.

## Infrastructure

- Jenkins LTS exécuté dans Docker Desktop sur Windows.
- Pipeline `ShopFlow-DataOps-CI`.
- Dépôt GitHub : `datasifaw/shopflow-dataops`.
- Branche surveillée : `main`.
- Tests automatisés : `pytest`.

## Configuration

- Déclencheur : Poll SCM.
- Planning : `H/5 * * * *`.
- Jenkins interroge périodiquement GitHub pour rechercher de nouveaux commits.
- Un build est déclenché lorsqu'un changement est détecté.

## Validation attendue

1. Fusionner une Pull Request vers `main`.
2. Attendre la prochaine vérification Poll SCM.
3. Vérifier qu'un nouveau build Jenkins démarre automatiquement.
4. Confirmer que les six tests pytest réussissent.

## Limites

- Jenkins doit être démarré pour détecter les changements.
- Le déclenchement n'est pas instantané.
- Aucun webhook public n'est nécessaire.
- Le pipeline ne charge pas de données dans SQL Server.

## Jira

SCRUM-41