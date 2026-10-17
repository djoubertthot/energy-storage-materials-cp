# Modèle de contraintes complet

## Variables principales
- Éléments / ions du tableau périodique
- Combinaisons (oxydes, alliages, complexes, hydrures, POM...)
- type_sortie : electrochimique, magnetique, radiative_PV, thermique...
- E_densite, eta_elec, C_mat, C_prod, dispo
- delta_Hf, energy_above_hull, T_decomp

## Contraintes
### Compatibilité chimique
- Oxydes : O présent + métaux adaptés
- Hydrures : H + métaux (Mg, Li, Ca...)
- Alliages : métaux uniquement, critères Hume-Rothery
- POM : Mo ou W + O

### Stabilité thermodynamique
- delta_Hf < 0
- energy_above_hull ≤ 0.05 eV/atome
- T_decomp > 100°C

### Objectifs
- E_utile = E_densite * eta_elec ≥ 250 Wh/kg (dépasser Li-ion)
- Priorité sortie électrique
- Coût et disponibilité contraints

(Voir conversation pour le détail des règles.)
