"""
Script de fusion avec pagination complète pour grands volumes.

Améliorations :
- Pagination complète OQMD
- Chunking Materials Project
- Retries + progression
- Configurable MAX_TOTAL
"""

import pandas as pd
from pathlib import Path
import requests
import time

# ========== CONFIG ==========
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"
MAX_TOTAL = 20000  # Nombre max total souhaité
PAGE_SIZE = 100
OUTPUT = Path("data/all_bases_unified_paginated.csv")
RETRIES = 4

def safe_get(url, params=None):
    for i in range(RETRIES):
        try:
            r = requests.get(url, params=params, timeout=90)
            if r.status_code == 200:
                return r
            print(f"HTTP {r.status_code} — retry {i+1}")
        except Exception as e:
            print(f"Erreur: {e} — retry {i+1}")
        time.sleep(2 ** i)
    return None

def fetch_oqmd_full_pagination(max_items=MAX_TOTAL):
    """Pagination complète OQMD."""
    print("OQMD : pagination complète...")
    all_data = []
    offset = 0
    while len(all_data) < max_items:
        resp = safe_get("https://oqmd.org/oqmdapi/formationenergy",
                        params={"limit": PAGE_SIZE, "offset": offset})
        if not resp:
            break
        items = resp.json().get("data", [])
        if not items:
            print("  Fin des données OQMD")
            break
        all_data.extend(items)
        print(f"  OQMD offset {offset} → total {len(all_data)}")
        offset += PAGE_SIZE
        time.sleep(0.8)
    if not all_data:
        return pd.DataFrame()
    return pd.DataFrame([{
        "source": "OQMD",
        "id": i.get("entry_id"),
        "formula": i.get("composition"),
        "e_hull": i.get("stability"),
        "e_form": i.get("delta_e"),
        "elements": ""
    } for i in all_data[:max_items]])

def fetch_mp_chunked():
    if "VOTRE" in MP_API_KEY:
        print("MP : clé manquante")
        return pd.DataFrame()
    try:
        from mp_api.client import MPRester
        print("Materials Project : chunking...")
        with MPRester(MP_API_KEY) as mpr:
            docs = list(mpr.materials.summary.search(
                energy_above_hull=(0, 0.25),
                fields=["material_id", "formula_pretty", "energy_above_hull",
                        "formation_energy_per_atom", "elements"],
                chunk_size=1000
            ))[:MAX_TOTAL]
            return pd.DataFrame([{
                "source": "MaterialsProject",
                "id": d.material_id,
                "formula": d.formula_pretty,
                "e_hull": d.energy_above_hull,
                "e_form": d.formation_energy_per_atom,
                "elements": ",".join(sorted(d.elements or []))
            } for d in docs])
    except Exception as e:
        print(f"MP error: {e}")
        return pd.DataFrame()

def main():
    print("=== Pagination complète — fusion multi-bases ===")
    frames = []

    df_mp = fetch_mp_chunked()
    if not df_mp.empty:
        frames.append(df_mp)
        print(f"MP : {len(df_mp)} matériaux")

    df_oqmd = fetch_oqmd_full_pagination()
    if not df_oqmd.empty:
        frames.append(df_oqmd)
        print(f"OQMD : {len(df_oqmd)} matériaux")

    if not frames:
        print("Aucune donnée récupérée.")
        return

    unified = pd.concat(frames, ignore_index=True)
    unified = unified.drop_duplicates(subset=["formula"], keep="first")
    OUTPUT.parent.mkdir(exist_ok=True)
    unified.to_csv(OUTPUT, index=False)
    print(f"\n✅ Total unique : {len(unified)} → {OUTPUT}")

if __name__ == "__main__":
    main()
