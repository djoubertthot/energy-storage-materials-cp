#!/usr/bin/env python3
"""
Script unique de fusion multi-sources pour le solveur de contraintes.

Sources supportées (clés gratuites) :
- Materials Project
- OQMD
- JARVIS (datasets publics ou API)

Usage :
1. Remplir les clés API ci-dessous
2. python scripts/fuse_materials_sources.py
3. Le fichier data/fused_materials_for_solver.csv est généré
"""

import pandas as pd
from mp_api.client import MPRester
import requests
import os

# ==================== CLÉS API (à remplir) ====================
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"      # https://materialsproject.org
# OQMD n'exige pas toujours de clé pour les requêtes de base
# JARVIS : souvent datasets publics, pas de clé obligatoire pour certains accès

OUTPUT_FILE = "data/fused_materials_for_solver.csv"
MAX_PER_SOURCE = 3000   # limite par source pour rester raisonnable

def fetch_materials_project(max_results=MAX_PER_SOURCE):
    if not MP_API_KEY or MP_API_KEY.startswith("VOTRE"):
        print("Materials Project : clé non fournie, ignoré.")
        return pd.DataFrame()
    
    print("Récupération Materials Project...")
    with MPRester(MP_API_KEY) as mpr:
        docs = mpr.materials.summary.search(
            energy_above_hull=(0, 0.1),
            fields=["material_id", "formula_pretty", "elements", "formation_energy_per_atom",
                    "energy_above_hull", "band_gap", "density"],
            chunk_size=500
        )
        data = []
        for doc in list(docs)[:max_results]:
            data.append({
                "source": "MaterialsProject",
                "id": str(doc.material_id),
                "formula": doc.formula_pretty,
                "elements": ",".join(sorted(doc.elements)),
                "formation_energy": doc.formation_energy_per_atom,
                "energy_above_hull": doc.energy_above_hull,
                "band_gap": doc.band_gap,
                "density": doc.density
            })
        return pd.DataFrame(data)

def fetch_oqmd(max_results=MAX_PER_SOURCE):
    print("Récupération OQMD...")
    try:
        url = "https://oqmd.org/oqmdapi/formationenergy"
        params = {"limit": max_results, "format": "json"}
        r = requests.get(url, params=params, timeout=60)
        if r.status_code != 200:
            print(f"OQMD erreur {r.status_code}")
            return pd.DataFrame()
        entries = r.json().get("data", [])
        data = []
        for e in entries[:max_results]:
            data.append({
                "source": "OQMD",
                "id": e.get("id"),
                "formula": e.get("composition"),
                "elements": ",".join(sorted(e.get("element_set", []))),
                "formation_energy": e.get("delta_e"),
                "energy_above_hull": e.get("stability"),
                "band_gap": None,
                "density": None
            })
        return pd.DataFrame(data)
    except Exception as ex:
        print(f"OQMD exception : {ex}")
        return pd.DataFrame()

def fuse_and_save():
    dfs = []
    
    df_mp = fetch_materials_project()
    if not df_mp.empty:
        dfs.append(df_mp)
    
    df_oqmd = fetch_oqmd()
    if not df_oqmd.empty:
        dfs.append(df_oqmd)
    
    if not dfs:
        print("Aucune donnée récupérée. Vérifie les clés et la connexion.")
        return
    
    fused = pd.concat(dfs, ignore_index=True)
    
    # Nettoyage basique pour le solveur
    fused = fused.dropna(subset=["formula", "energy_above_hull"])
    fused["energy_above_hull"] = pd.to_numeric(fused["energy_above_hull"], errors="coerce")
    fused = fused[fused["energy_above_hull"] <= 0.1]
    
    os.makedirs("data", exist_ok=True)
    fused.to_csv(OUTPUT_FILE, index=False)
    print(f"\nFusion terminée : {len(fused)} matériaux → {OUTPUT_FILE}")
    print(fused["source"].value_counts())

if __name__ == "__main__":
    fuse_and_save()
