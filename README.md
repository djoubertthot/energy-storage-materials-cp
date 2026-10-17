# Energy Storage Materials - Constraint Programming Model

Modèle de programmation par contraintes pour le screening de matériaux de stockage d'énergie haute densité (objectif : dépasser les batteries Li-ion en densité utile électrique).

## Contenu du dépôt
- `model/` : description des contraintes (compatibilité chimique, stabilité thermodynamique, densité, coût...)
- `data/` : données de stabilité (ΔHf, energy above hull) pour oxydes, hydrures, alliages, etc.
- `scripts/` : exemples d'interrogation Materials Project
- `candidates/` : tableaux des systèmes évalués

Développé dans le cadre de discussions sur le stockage énergétique au-delà des Li-ion.

## Prochaines étapes
- Implémenter le modèle en MiniZinc ou OR-Tools
- Enrichir les données via l'API Materials Project
- Optimiser les contraintes pour densité > Li-ion + sortie électrique
