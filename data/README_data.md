# Données de matériaux

## Fichiers
- `stability_data.csv` : données de stabilité pour familles principales
- `mp_stable_materials_9000.csv` : à générer via le script `scripts/download_9000_materials.py`

## Génération des 9000 matériaux
1. Obtenir une clé API gratuite sur https://materialsproject.org
2. Installer les dépendances : `pip install mp-api pandas`
3. Modifier `API_KEY` dans `scripts/download_9000_materials.py`
4. Exécuter : `python scripts/download_9000_materials.py`

Materials Project contient plus de 30 000 matériaux stables (energy_above_hull ≤ 0.05 eV/atome).
