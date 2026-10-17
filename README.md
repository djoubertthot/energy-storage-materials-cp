# Energy Storage Materials — Constraint Programming Platform

Plateforme pour récupérer des informations sur un très grand nombre de matériaux et tester différents systèmes de contraintes (programmation par contraintes, optimisation multi-objectifs, filtrage, etc.).

## Objectif
Permettre d’explorer et de filtrer des dizaines de milliers de matériaux selon des critères variables (stabilité thermodynamique, densité énergétique, coût, disponibilité, type de sortie énergétique…).

## Contenu principal
- `scripts/fuse_materials_sources.py` — script unique de fusion multi-sources
- `scripts/download_9000_materials.py` — téléchargement ciblé Materials Project
- `model/` — exemples de modèles de contraintes
- `sources/` — documentation des bases de données
- `data/` — données générées (CSV)

## Démarrage rapide
1. Cloner le dépôt
2. Installer les dépendances : `pip install mp-api pandas requests`
3. Remplir les clés API dans `scripts/fuse_materials_sources.py`
4. Lancer la fusion : `python scripts/fuse_materials_sources.py`
5. Utiliser le CSV généré avec un solveur (MiniZinc, OR-Tools, etc.)

## Sources supportées
- Materials Project (clé gratuite)
- OQMD
- Extensible à JARVIS, AFLOW, etc.

## Cas d’usage
- Tester différentes contraintes de stabilité (`energy_above_hull`)
- Filtrer par éléments abondants
- Comparer des objectifs (densité énergétique vs coût)
- Générer des jeux de données pour plusieurs modèles de contraintes
