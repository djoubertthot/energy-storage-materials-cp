from mp_api.client import MPRester

# Get free API key at https://materialsproject.org/
API_KEY = "YOUR_API_KEY_HERE"

with MPRester(API_KEY) as mpr:
    docs = mpr.materials.summary.search(
        elements=["Fe", "O"],
        energy_above_hull=(0, 0.05),
        fields=["formula_pretty", "energy_above_hull", "formation_energy_per_atom"]
    )
    for doc in docs[:5]:
        print(f"{doc.formula_pretty}: E_hull={doc.energy_above_hull:.4f}")
