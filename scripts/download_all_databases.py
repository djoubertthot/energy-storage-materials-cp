#!/usr/bin/env python3
"""
Script unifié pour télécharger / interroger l'ensemble des bases de données matériaux.

Bases couvertes :
- Materials Project (clé API)
- OQMD (API publique)
- JARVIS (datasets / API)
- AFLOW (API)
- Materials Cloud (téléchargement)
- NOMAD (API)
- Matbench Discovery (datasets)

Usage :
1. Remplir les clés nécessaires
2. python scripts/download_all_databases.py
3. Les fichiers sont générés dans data/
"""

import pandas as pd
import requests
import os
from mp_api.client import MPRester

# ==================== CLÉS ====================
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"   # Obligatoire pour MP
# Les autres bases sont souvent accessibles sans clé ou avec accès public

OUTPUT_DIR = "data"
MAX_RESULTS = 2000

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_materials_project():
    if not MP_API_KEY or "VOTRE" in MP_API_KEY:
        print("[MP] Clé manquante — ignoré")
        return
    print("[MP] Téléchargement...")
    with MPRester(MP_API_KEY) as mpr:
        docs = mpr.materials.summary.search(
            energy_above_hull=(0, 0.1),
            fields=["material_id", "formula_pretty", "formation_energy_per_atom", "energy_above_hull"],
            chunk_size=500
        )
        data = [{
            "source": "MaterialsProject",
            "id": str(d.material_id),
            "formula": d.formula_pretty,
            "formation_energy": d.formation_energy_per_atom,
            "energy_above_hull": d.energy_above_hull
        } for d in list(docs)[:MAX_RESULTS]]
        df = pd.DataFrame(data)
        df.to_csv(f"{OUTPUT_DIR}/mp_materials.csv", index=False)
        print(f"[MP] {len(df)} matériaux sauvegardés")

def download_oqmd():
    print("[OQMD] Téléchargement...")
    try:
        r = requests.get("https://oqmd.org/oqmdapi/formationenergy", params={"limit": MAX_RESULTS, "format": "json"}, timeout=90)
        if r.status_code == 200:
            entries = r.json().get("data", [])
            data = [{
                "source": "OQMD",
                "id": e.get("id"),
                "formula": e.get("composition"),
                "formation_energy": e.get("delta_e"),
                "energy_above_hull": e.get("stability")
            } for e in entries]
            pd.DataFrame(data).to_csv(f"{OUTPUT_DIR}/oqmd_materials.csv", index=False)
            print(f"[OQMD] {len(data)} matériaux sauvegardés")
        else:
            print(f"[OQMD] Erreur {r.status_code}")
    except Exception as e:
        print(f"[OQMD] Exception : {e}")

def download_jarvis_info():
    print("[JARVIS] Voir https://jarvis.nist.gov pour datasets téléchargeables")
    print("[JARVIS] Recherche recommandée : 'formation energy' ou 'dft' datasets")

def download_aflow_info():
    print("[AFLOW] API disponible : https://aflow.org/API/")
    print("[AFLOW] Exemple de requête possible via leur REST API")

def download_materials_cloud_info():
    print("[Materials Cloud] Téléchargements directs : https://www.materialscloud.org")
    print("[Materials Cloud] Chercher des archives de données calculées")

def download_nomad_info():
    print("[NOMAD] API et bulk : https://nomad-lab.eu")
    print("[NOMAD] Accès via leur API ou archives")

def download_matbench_info():
    print("[Matbench Discovery] Datasets : https://matbench-discovery.materialsproject.org/data")
    print("[Matbench Discovery] Fichiers CSV/JSON téléchargeables directement")

def main():
    ensure_dir()
    print("=== Téléchargement multi-bases ===\n")
    download_materials_project()
    download_oqmd()
    download_jarvis_info()
    download_aflow_info()
    download_materials_cloud_info()
    download_nomad_info()
    download_matbench_info()
    print("\n=== Terminé ===")
    print(f"Fichiers générés dans {OUTPUT_DIR}/")
    print("Pour fusionner : utiliser scripts/fuse_materials_sources.py ou combiner les CSV manuellement.")

if __name__ == "__main__":
    main()
