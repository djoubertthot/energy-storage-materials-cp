"""Exemple d'interrogation Materials Project pour données de stabilité."""
from mp_api.client import MPRester

API_KEY = "VOTRE_CLE_API_ICI"  # À remplacer

with MPRester(API_KEY) as mpr:
    # Oxydes stables contenant Fe ou Mn
    docs = mpr.materials.summary.search(
        elements=["Fe", "Mn", "O"],
        energy_above_hull=(0, 0.05),
        fields=["formula_pretty", "energy_above_hull", "formation_energy_per_atom"]
    )
    print(f"Trouvé {len(docs)} matériaux")
    for doc in docs[:10]:
        print(f"{doc.formula_pretty}: e_hull={doc.energy_above_hull:.4f}, e_form={doc.formation_energy_per_atom:.3f}")
