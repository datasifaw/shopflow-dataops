# Git Workflow — ShopFlow DataOps

## Objectif
Organiser le développement du projet avec Git, GitHub et Jira.

## Branches
- `main` : branche principale stable.
- `feature/SCRUM-ID-description` : développement d'une fonctionnalité.
- `fix/SCRUM-ID-description` : correction d'un bug.

## Cycle de développement
1. Sélectionner un ticket Jira et le passer en cours.
2. Créer une branche depuis `main`.
3. Développer et tester les modifications
4. Effectuer un commit avec une référence Jira
5. Pousser la branche sur GitHub
6. Créer une Pull Request vers `main`.
7. Vérifier les changements et les tests.
8. Fusionner la Pull Request et clôturer le ticket Jira.

## Convention de commits
- `feat:` nouvelle fonctionnalité.
- `fix:` correction d'un bug.
- `docs:` documentation.
- `test:` tests.
- `chore:` maintenance et configuration.
- `ci:` intégration continue.

## Exemple
`docs: define git workflow (SCRUM-6)`

## Règle DevOps
La branche `main` doit rester stable. Les changements passent par une Pull Request et les contrôles disponibles avant fusion.