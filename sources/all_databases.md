# Script pour l'ensemble des bases

## Fichier
`scripts/download_all_databases.py`

## Bases couvertes
- Materials Project (avec clé)
- OQMD (API)
- JARVIS
- AFLOW
- Materials Cloud
- NOMAD
- Matbench Discovery

## Utilisation
```bash
pip install mp-api pandas requests
python scripts/download_all_databases.py
```

Les bases sans clé obligatoire affichent des instructions.  
Les bases avec API génèrent des CSV dans `data/`.

## Fusion
Après téléchargement, utiliser `scripts/fuse_materials_sources.py` ou combiner les fichiers CSV pour le solveur.
