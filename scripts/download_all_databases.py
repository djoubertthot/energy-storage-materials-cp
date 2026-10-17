#!/usr/bin/env python3
"""
Script unifié avec pagination complète pour télécharger de grands volumes.

Pagination ajoutée pour :
- Materials Project
- OQMD

Usage :
1. Remplir MP_API_KEY
2. Ajuster MAX_RESULTS si besoin
3. python scripts/download_all_databases.py
"""

import pandas as pd
import requests
import os
import time
from mp_api.client import MPRester

# ==================== CONFIGURATION ====================
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"
OUTPUT_DIR = "data"
MAX_RESULTS = 10000          # Augmenté grâce à la pagination
CHUNK_SIZE = 500

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_materials_project():
    if not MP_API_KEY or "VOTRE" in MP_API_KEY:
        print("[MP] Clé manquante — ignoré")
        return
    print(f"[MP] Téléchargement paginé (max {MAX_RESULTS})...")
    all_data = []
    try:
        with MPRester(MP_API_KEY) as mpr:
            # La bibliothèque mp-api gère la pagination interne via chunk_size
            docs = mpr.materials.summary.search(
                energy_above_hull=(0, 0.1),
                fields=["material_id", "formula_pretty", "formation_energy_per_atom",
                        "energy_above_hull", "elements"],
                chunk_size=CHUNK_SIZE
            )
            for i, d in enumerate(docs):
                if i >= MAX_RESULTS:
                    break
                all_data.append({
                    "source": "MaterialsProject",
                    "id": str(d.material_id),
                    "formula": d.formula_pretty,
                    "elements": ",".join(sorted(d.elements)) if d.elements else "",
                    "formation_energy": d.formation_energy_per_atom,
                    "energy_above_hull": d.energy_above_hull
                })
                if (i + 1) % 1000 == 0:
                    print(f"[MP] {i + 1} matériaux récupérés...")
        
        df = pd.DataFrame(all_data)
        df.to_csv(f"{OUTPUT_DIR}/mp_materials.csv", index=False)
        print(f"[MP] {len(df)} matériaux sauvegardés")
    except Exception as e:
        print(f"[MP] Erreur : {e}")

def download_oqmd_paginated():
    print(f"[OQMD] Téléchargement paginé (max {MAX_RESULTS})...")
    all_entries = []
    limit_per_page = 500
    offset = 0
    
    try:
        while len(all_entries) < MAX_RESULTS:
            params = {
                "limit": limit_per_page,
                "offset": offset,
                "format": "json"
            }
            r = requests.get(
                "https://oqmd.org/oqmdapi/formationenergy",
                params=params,
                timeout=120
            )
            if r.status_code != 200:
                print(f"[OQMD] Erreur HTTP {r.status_code} à l'offset {offset}")
                break
            
            data = r.json().get("data", [])
            if not data:
                break
            
            all_entries.extend(data)
            print(f"[OQMD] {len(all_entries)} entrées récupérées...")
            offset += limit_per_page
            time.sleep(0.5)  # Respect du serveur
            
            if len(data) < limit_per_page:
                break
        
        # Conversion
        records = [{
            "source": "OQMD",
            "id": e.get("id"),
            "formula": e.get("composition"),
            "elements": ",".join(sorted(e.get("element_set", []))),
            "formation_energy": e.get("delta_e"),
            "energy_above_hull": e.get("stability")
        } for e in all_entries[:MAX_RESULTS]]
        
        pd.DataFrame(records).to_csv(f"{OUTPUT_DIR}/oqmd_materials.csv", index=False)
        print(f"[OQMD] {len(records)} matériaux sauvegardés")
    except Exception as e:
        print(f"[OQMD] Exception : {e}")

def download_jarvis():
    print("[JARVIS] Datasets : https://jarvis.nist.gov/jarvisdft/")
    print("[JARVIS] Prêt pour intégration d'un dataset paginé ou Figshare.")

def download_aflow():
    print("[AFLOW] Tentative de requête...")
    try:
        url = "https://aflow.org/API/aflux/?species(Fe,O),paging(1,200)"
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            with open(f"{OUTPUT_DIR}/aflow_sample.txt", "w") as f:
                f.write(r.text[:10000])
            print("[AFLOW] Échantillon sauvegardé")
        else:
            print(f"[AFLOW] Erreur {r.status_code}")
    except Exception as e:
        print(f"[AFLOW] Exception : {e}")

def download_others():
    print("[Matbench / Materials Cloud / NOMAD] Voir documentation dans sources/")
    print("[Info] Pagination disponible sur leurs APIs respectives.")

def main():
    ensure_dir()
    print("=== Téléchargement avec pagination complète ===\n")
    download_materials_project()
    download_oqmd_paginated()
    download_jarvis()
    download_aflow()
    download_others()
    print("\n=== Terminé ===")
    print(f"Fichiers dans {OUTPUT_DIR}/ (jusqu'à {MAX_RESULTS} par source)")

if __name__ == "__main__":
    main()
