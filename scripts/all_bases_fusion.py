"""
Script de fusion avec retries automatiques et backoff exponentiel.

Gère les erreurs 429 (rate limit) et les erreurs réseau.
"""

import pandas as pd
from pathlib import Path
import requests
import time
import random

MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"
MAX_TOTAL = 10000
PAGE_SIZE = 50
OUTPUT = Path("data/all_bases_unified_safe.csv")
SLEEP = 1.0
MAX_RETRIES = 5

def safe_get(url, params=None):
    """Requête avec retries et backoff exponentiel."""
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, timeout=90)
            if r.status_code == 200:
                return r
            if r.status_code == 429:
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit (429) — attente {wait:.1f}s (tentative {attempt+1})")
                time.sleep(wait)
                continue
            print(f"HTTP {r.status_code} — retry {attempt+1}")
        except requests.exceptions.RequestException as e:
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"Erreur réseau: {e} — attente {wait:.1f}s")
            time.sleep(wait)
    print("Échec après tous les retries")
    return None

def fetch_oqmd_with_retries():
    print("OQMD avec retries...")
    all_data = []
    offset = 0
    while len(all_data) < MAX_TOTAL:
        resp = safe_get("https://oqmd.org/oqmdapi/formationenergy",
                        params={"limit": PAGE_SIZE, "offset": offset})
        if not resp:
            break
        items = resp.json().get("data", [])
        if not items:
            break
        all_data.extend(items)
        print(f"  OQMD: {len(all_data)}")
        offset += PAGE_SIZE
        time.sleep(SLEEP)
    return pd.DataFrame([{
        "source": "OQMD",
        "id": i.get("entry_id"),
        "formula": i.get("composition"),
        "e_hull": i.get("stability"),
        "e_form": i.get("delta_e")
    } for i in all_data[:MAX_TOTAL]])

def main():
    print("=== Fusion avec retries automatiques ===")
    frames = []
    df_oqmd = fetch_oqmd_with_retries()
    if not df_oqmd.empty:
        frames.append(df_oqmd)

    if frames:
        unified = pd.concat(frames, ignore_index=True)
        OUTPUT.parent.mkdir(exist_ok=True)
        unified.to_csv(OUTPUT, index=False)
        print(f"\n✅ Sauvegardé {len(unified)} entrées dans {OUTPUT}")
    else:
        print("Aucune donnée.")

if __name__ == "__main__":
    main()
