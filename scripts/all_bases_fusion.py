"""
Script amélioré de fusion multi-bases avec meilleures fonctions de téléchargement.

Améliorations :
- Retries automatiques
- Meilleure gestion d'erreurs
- Pagination pour OQMD
- Plus de champs utiles
- Rate limiting basique
"""

import pandas as pd
from pathlib import Path
import requests
import time
from typing import Optional

# ========== CONFIG ==========
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"
MAX_PER_SOURCE = 5000
OUTPUT = Path("data/all_bases_unified.csv")
RETRIES = 3
SLEEP_BETWEEN = 1.5

def safe_request(url, params=None, retries=RETRIES):
    """Requête avec retries."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=60)
            if resp.status_code == 200:
                return resp
            print(f"Status {resp.status_code}, retry {attempt+1}")
        except Exception as e:
            print(f"Erreur requête (tentative {attempt+1}): {e}")
        time.sleep(SLEEP_BETWEEN * (attempt + 1))
    return None

def fetch_mp_improved():
    if not MP_API_KEY or "VOTRE" in MP_API_KEY:
        print("MP : clé manquante")
        return pd.DataFrame()
    try:
        from mp_api.client import MPRester
        print("Materials Project (amélioré)...")
        with MPRester(MP_API_KEY) as mpr:
            docs = list(mpr.materials.summary.search(
                energy_above_hull=(0, 0.2),
                fields=["material_id", "formula_pretty", "energy_above_hull",
                        "formation_energy_per_atom", "elements", "nelements", "band_gap", "density"],
                chunk_size=1000
            ))[:MAX_PER_SOURCE]
            return pd.DataFrame([{
                "source": "MaterialsProject",
                "id": d.material_id,
                "formula": d.formula_pretty,
                "e_hull": d.energy_above_hull,
                "e_form": d.formation_energy_per_atom,
                "nelements": d.nelements,
                "elements": ",".join(sorted(d.elements or [])),
                "band_gap": getattr(d, "band_gap", None),
                "density": getattr(d, "density", None)
            } for d in docs])
    except Exception as e:
        print(f"MP error: {e}")
        return pd.DataFrame()

def fetch_oqmd_paginated():
    print("OQMD (paginé)...")
    all_items = []
    page_size = 100
    for offset in range(0, MAX_PER_SOURCE, page_size):
        resp = safe_request("https://oqmd.org/oqmdapi/formationenergy",
                            params={"limit": page_size, "offset": offset})
        if not resp:
            break
        items = resp.json().get("data", [])
        if not items:
            break
        all_items.extend(items)
        print(f"  Offset {offset}: {len(items)} items")
        time.sleep(0.5)
    if not all_items:
        return pd.DataFrame()
    return pd.DataFrame([{
        "source": "OQMD",
        "id": i.get("entry_id"),
        "formula": i.get("composition"),
        "e_hull": i.get("stability"),
        "e_form": i.get("delta_e"),
        "nelements": None,
        "elements": "",
        "band_gap": None,
        "density": None
    } for i in all_items[:MAX_PER_SOURCE]])

def main():
    print("=== Fusion améliorée de toutes les bases ===")
    frames = []
    df_mp = fetch_mp_improved()
    if not df_mp.empty:
        frames.append(df_mp)
        print(f"MP: {len(df_mp)}")

    df_oqmd = fetch_oqmd_paginated()
    if not df_oqmd.empty:
        frames.append(df_oqmd)
        print(f"OQMD: {len(df_oqmd)}")

    if not frames:
        print("Aucune donnée.")
        return

    unified = pd.concat(frames, ignore_index=True)
    unified = unified.drop_duplicates(subset=["formula"], keep="first")
    OUTPUT.parent.mkdir(exist_ok=True)
    unified.to_csv(OUTPUT, index=False)
    print(f"\n✅ {len(unified)} matériaux → {OUTPUT}")
    print(unified.head())

if __name__ == "__main__":
    main()
