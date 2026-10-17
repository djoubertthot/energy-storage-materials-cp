# Scripts

## fuse_materials_sources.py
Script principal. Fusionne plusieurs sources et produit un CSV utilisable par un solveur.

### Paramètres modifiables
- `MAX_PER_SOURCE` : nombre maximum de matériaux par source
- Seuils de `energy_above_hull`
- Champs récupérés

## download_9000_materials.py
Version spécialisée Materials Project pour de gros volumes.

## Extension
Pour ajouter une nouvelle source, créer une fonction `fetch_xxx()` qui retourne un DataFrame avec les colonnes standards, puis l’appeler dans `fuse_and_save()`.
