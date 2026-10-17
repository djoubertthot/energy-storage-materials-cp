# Utilisation du script de fusion

## Fichier
`scripts/fuse_materials_sources.py`

## Étapes
1. Obtenir une clé Materials Project gratuite : https://materialsproject.org
2. Éditer le script et remplir `MP_API_KEY`
3. Installer les dépendances :
   ```bash
   pip install mp-api pandas requests
   ```
4. Lancer :
   ```bash
   python scripts/fuse_materials_sources.py
   ```
5. Le fichier `data/fused_materials_for_solver.csv` est prêt pour le solveur.

## Colonnes du CSV fusionné
- source
- id
- formula
- elements
- formation_energy
- energy_above_hull
- band_gap
- density

## Extension
Le script peut être étendu avec d'autres sources (JARVIS, AFLOW) en ajoutant des fonctions `fetch_xxx()`.
