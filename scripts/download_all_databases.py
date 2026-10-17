#!/usr/bin/env python3
"""
Script de téléchargement multi-bases avec retries automatiques et protections anti-ban.

Retries avec backoff exponentiel pour les erreurs 429 et réseau.
"""

import pandas as pd
import requests
import os
import time
from mp_api.client import MPRester

# ==================== CONFIGURATION ====================
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"
OUTPUT_DIR = "data"
MAX_RESULTS = 5000
CHUNK_SIZE = 200
DELAY_BETWEEN_REQUESTS = 1.0
MAX_RETRIES = 5

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def safe_sleep(seconds=DELAY_BETWEEN_REQUESTS):
    time.sleep(seconds)

def request_with_retry(url, params=None, headers=None, timeout=90, max_retries=MAX_RETRIES):
    """
    Effectue une requête GET avec retries et backoff exponentiel.
    Gère spécifiquement les erreurs 429 (rate limit).
    """
    headers = headers or {"User-Agent": "MaterialsResearchScript/1.0"}
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=timeout)
            if r.status_code == 429:
                wait = (2 ** attempt) + 1
                print(f"  [Retry] 429 reçu, attente {wait}s (tentative {attempt + 1}/{max_retries})")
                time.sleep(wait)
                continue
            if r.status_code == 200:
                return r
            else:
                print(f"  [Retry] Erreur {r.status_code}, tentative {attempt + 1}/{max_retries}")
                time.sleep(2 ** attempt)
        except requests.RequestException as e:
            print(f"  [Retry] Exception réseau : {e}, tentative {attempt + 1}/{max_retries}")
            time.sleep(2 ** attempt)
    print("  [Retry] Échec après plusieurs tentatives")
    return None

def download_materials_project():
    if not MP_API_KEY or "VOTRE" in MP_API_KEY:
        print("[MP] Clé manquante — ignoré")
        return
    print(f"[MP] Téléchargement (max {MAX_RESULTS})...")
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
                    safe_sleep(2.0)
        df = pd.DataFrame(all_data)
        df.to_csv(f"{OUTPUT_DIR}/mp_materials.csv", index=False)
        print(f"[MP] {len(df)} matériaux sauvegardés")
    except Exception as e:
        print(f"[MP] Erreur : {e}")

def download_oqmd_paginated():
    print(f"[OQMD] Téléchargement paginé (max {MAX_RESULTS})...")
    all_entries = []
    limit_per_page = 200
    offset = 0
    
    while len(all_entries) < MAX_RESULTS:
        params = {"limit": limit_per_page, "offset": offset, "format": "json"}
        r = request_with_retry(
            "https://oqmd.org/oqmdapi/formationenergy",
            params=params
        )
        if r is None:
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
    
    if all_entries:
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

def download_aflow():
    print("[AFLOW] Requête...")
    r = request_with_retry("https://aflow.org/API/aflux/?species(Fe,O),paging(1,50)")
    if r and r.status_code == 200:
        with open(f"{OUTPUT_DIR}/aflow_sample.txt", "w") as f:
            f.write(r.text[:5000])
        print("[AFLOW] Échantillon sauvegardé")
    safe_sleep()

def download_others():
    print("[Autres bases] Privilégier les datasets complets (voir sources/)")

def main():
    ensure_dir()
    print("=== Téléchargement avec retries automatiques ===\n")
    download_materials_project()
    download_oqmd_paginated()
    download_aflow()
    download_others()
    print("\n=== Terminé ===")

if __name__ == "__main__":
    main()
