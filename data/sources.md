# Sources de données pour matériaux et stabilité

## Bases principales
- **Materials Project** (https://materialsproject.org) : energy_above_hull, formation_energy, structures. API via mp-api.
- **OQMD** (https://www.oqmd.org) : Open Quantum Materials Database, ~1M+ matériaux, énergies de formation DFT.
- **AFLOW** (http://aflowlib.org) : Large base de propriétés calculées, API disponible.
- **JARVIS** (https://jarvis.nist.gov) : DFT, propriétés électroniques, mécaniques, ML.
- **Materials Cloud** (https://www.materialscloud.org) : Données calculées et expérimentales, ouvert.
- **NOMAD** (https://nomad-lab.eu) : Repository de calculs DFT bruts et parsés.

## Autres utiles
- **ICSD** : Structures expérimentales (accès parfois restreint).
- **Matbench Discovery** : Jeux de données pour ML et stabilité.
- **Battery explorers** : Spécifiques aux matériaux d'électrodes (dans MP ou autres).

## Notes
- Utiliser OPTIMADE pour interroger plusieurs bases via une API commune.
- Pour le modèle CSP : prioriser energy_above_hull / formation energy de plusieurs sources pour robustesse.
- Scripts d'exemple à développer selon besoins.

Mis à jour le 2026-10-17.
