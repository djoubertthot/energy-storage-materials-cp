# Bases de données supplémentaires téléchargeables

Liste de bases accessibles (en plus de Materials Project et OQMD) pour enrichir les tests de contraintes.

## Bases avec téléchargement ou API libre

| Base                  | Description                              | Accès                          | Lien |
|-----------------------|------------------------------------------|--------------------------------|------|
| **JARVIS**            | Propriétés DFT, élasticité, band gap   | Datasets + API                | https://jarvis.nist.gov |
| **AFLOW**             | Structures et propriétés calculées       | API                           | https://aflow.org |
| **Materials Cloud**   | Données calculées et expérimentales      | Téléchargement direct          | https://www.materialscloud.org |
| **NOMAD**             | Calculs bruts et métadonnées             | API + bulk                    | https://nomad-lab.eu |
| **Matbench Discovery**| Jeux de données ML + stabilité          | Téléchargement                | https://matbench-discovery.materialsproject.org |
| **OQMD**              | Déjà intégré                         | API                           | https://oqmd.org |
| **Materials Project** | Déjà intégré                         | API (clé gratuite)             | https://materialsproject.org |

## Autres sources utiles
- **ICSD** : structures expérimentales (accès souvent institutionnel)
- **COD** (Crystallography Open Database) : structures libres
- **PubChem** / bases chimiques pour ligands ou molécules organiques

## Recommandation
Pour tester un grand nombre de systèmes de contraintes, commencer par :
1. Materials Project + OQMD (déjà scriptés)
2. JARVIS et Matbench Discovery (datasets facilement téléchargeables)
3. Materials Cloud pour des jeux de données spécifiques

## Extension du script de fusion
Les fonctions `fetch_jarvis()`, `fetch_aflow()`, etc. peuvent être ajoutées dans `scripts/fuse_materials_sources.py` selon les besoins.
