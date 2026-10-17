#!/usr/bin/env python3
"""
Script de téléchargement multi-bases avec protections anti-ban.

Règles respectées :
- Materials Project : délais, utilisation recommandée de mp-api, éviter les volumes excessifs sans prévenir
- OQMD : pauses entre requêtes
- AFLOW : requêtes modérées

Usage :
1. Remplir MP_API_KEY
2. python scripts/download_all_databases.py
"""

import pandas as pd
import requests
import os
import time
from mp_api.client import MPRester

# ==================== CONFIGURATION ====================
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"
OUTPUT_DIR = "data"
MAX_RESULTS = 5000           # Limite raisonnable pour éviter les abus
CHUNK_SIZE = 200
DELAY_BETWEEN_REQUESTS = 1.0  # secondes

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def safe_sleep(seconds=DELAY_BETWEEN_REQUESTS):
    """Pause pour respecter les rate limits."""
    time.sleep(seconds)

def download_materials_project():
    """
    Materials Project :
    - Utiliser le client officiel mp-api
    - Éviter les téléchargements massifs sans prévenir heavy.api.use@materialsproject.org
    - Le client gère une partie du rate limiting
    """
    if not MP_API_KEY or "VOTRE" in MP_API_KEY:
        print("[MP] Clé manquante — ignoré")
        return
    print(f"[MP] Téléchargement (max {MAX_RESULTS}, avec pauses)...")
    all_data = []
    try:
        with MPRester(MP_API_KEY) as mpr:
            docs = mpr.materials.summary.search(
                energy_above_hull=(0, 0.05),
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
                if (i + 1) % 500 == 0:
                    print(f"[MP] {i + 1} matériaux...")
                    safe_sleep(2.0)  # Pause supplémentaire
        
        df = pd.DataFrame(all_data)
        df.to_csv(f"{OUTPUT_DIR}/mp_materials.csv", index=False)
        print(f"[MP] {len(df)} matériaux sauvegardés")
    except Exception as e:
        print(f"[MP] Erreur : {e}")
        print("[MP] Conseil : réduire MAX_RESULTS ou contacter support@materialsproject.org si besoin de volumes plus importants.")

def download_oqmd_paginated():
    """
    OQMD : API publique, mais respecter des pauses entre les pages.
    """
    print(f"[OQMD] Téléchargement paginé (max {MAX_RESULTS})...")
    all_entries = []
    limit_per_page = 200
    offset = 0
    
    try:
        while len(all_entries) < MAX_RESULTS:
            params = {"limit": limit_per_page, "offset": offset, "format": "json"}
            r = requests.get(
                "https://oqmd.org/oqmdapi/formationenergy",
                params=params,
                timeout=90,
                headers={"User-Agent": "MaterialsResearchScript/1.0"}
            )
            if r.status_code != 200:
                print(f"[OQMD] Erreur {r.status_code}")
                break
            
            data = r.json().get("data", [])
            if not data:
                break
            
            all_entries.extend(data)
            print(f"[OQMD] {len(all_entries)} entrées...")
            offset += limit_per_page
            safe_sleep(1.5)
            
            if len(data) < limit_per_page:
                break
        
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

def download_aflow():
    print("[AFLOW] Requête modérée...")
    try:
        url = "https://aflow.org/API/aflux/?species(Fe,O),paging(1,50)"
        r = requests.get(url, timeout=60, headers={"User-Agent": "MaterialsResearchScript/1.0"})
        if r.status_code == 200:
            with open(f"{OUTPUT_DIR}/aflow_sample.txt", "w") as f:
                f.write(r.text[:5000])
            print("[AFLOW] Échantillon sauvegardé")
        else:
            print(f"[AFLOW] Erreur {r.status_code}")
        safe_sleep()
    except Exception as e:
        print(f"[AFLOW] Exception : {e}")

def download_others():
    print("[JARVIS / Matbench / Materials Cloud / NOMAD]")
    print("  → Privilégier les téléchargements de datasets complets plutôt que des requêtes API massives.")
    print("  → Voir sources/additional_databases.md pour les liens.")

def main():
    ensure_dir()
    print("=== Téléchargement avec protections anti-ban ===\n")
    print("Note : pour des volumes très importants sur Materials Project,")
    print("      contacter heavy.api.use@materialsproject.org au préalable.\n")
    
    download_materials_project()
    download_oqmd_paginated()
    download_aflow()
    download_others()
    
    print("\n=== Terminé ===")
    print(f"Fichiers dans {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
