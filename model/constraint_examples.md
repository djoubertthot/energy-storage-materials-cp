# Exemples de systèmes de contraintes à tester

## 1. Stabilité stricte
```text
energy_above_hull <= 0.02
formation_energy < 0
```

## 2. Haute densité énergétique + éléments abondants
```text
E_utile >= 250
elements subset {Fe, Mn, Ti, Al, Mg, O, ...}
dispo >= 7
```

## 3. Sortie électrique prioritaire
```text
type_sortie in {electrochimique, magnetique}
eta_elec >= 0.6
```

## 4. Multi-objectif
Maximiser : densité énergétique utile  
Minimiser : coût + (1 - disponibilité)

Ces exemples peuvent être adaptés selon les colonnes présentes dans le CSV fusionné.
