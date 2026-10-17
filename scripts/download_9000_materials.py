#!/usr/bin/env python3
"""
Script pour télécharger les données de ~9000 matériaux stables depuis Materials Project.
Nécessite une clé API Materials Project (gratuite sur materialsproject.org).
"""

from mp_api.client import MPRester
import pandas as pd
import json

API_KEY = "VOTRE_CLE_API_ICI"  # À remplacer

def download_stable_materials(max_results=9000):
    with MPRester(API_KEY) as mpr:
        print(f"Téléchargement de jusqu'à {max_results} matériaux stables...")
        
        docs = mpr.materials.summary.search(
            energy_above_hull=(0, 0.05),
            fields=[
                "material_id",
                "formula_pretty",
                "elements",
                "nelements",
                "formation_energy_per_atom",
                "energy_above_hull",
                "band_gap",
                "density",
                "volume"
            ],
            num_chunks=10,
            chunk_size=900
        )
        
        data = []
        for doc in docs[:max_results]:
            data.append({
                "material_id": str(doc.material_id),
                "formula": doc.formula_pretty,
                "elements": ",".join(doc.elements),
                "nelements": doc.nelements,
                "formation_energy_per_atom": doc.formation_energy_per_atom,
                "energy_above_hull": doc.energy_above_hull,
                "band_gap": doc.band_gap,
                "density": doc.density,
                "volume": doc.volume
            })
        
        df = pd.DataFrame(data)
        output_file = "data/mp_stable_materials_9000.csv"
        df.to_csv(output_file, index=False)
        print(f"{len(df)} matériaux sauvegardés dans {output_file}")
        return df

if __name__ == "__main__":
    download_stable_materials(9000)
