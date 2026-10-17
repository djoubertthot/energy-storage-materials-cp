#!/usr/bin/env python3
"""
Script unifié amélioré pour télécharger / interroger l'ensemble des bases de données matériaux.

Bases couvertes avec fonctions améliorées :
- Materials Project (clé API)
- OQMD (API publique)
- JARVIS (tentative de datasets publics)
- AFLOW (requête API de base)
- Materials Cloud / NOMAD / Matbench (instructions + tentatives)

Usage :
1. Remplir MP_API_KEY
2. python scripts/download_all_databases.py
"""

import pandas as pd
import requests
import os
from mp_api.client import MPRester

# ==================== CLÉS ====================
MP_API_KEY = "VOTRE_CLE_MATERIALS_PROJECT"

OUTPUT_DIR = "data"
MAX_RESULTS = 2000

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_materials_project():
    if not MP_API_KEY or "VOTRE" in MP_API_KEY:
        print("[MP] Clé manquante — ignoré")
        return
    print("[MP] Téléchargement...")
    try:
        with MPRester(MP_API_KEY) as mpr:
            docs = mpr.materials.summary.search(
                energy_above_hull=(0, 0.1),
                fields=["material_id", "formula_pretty", "formation_energy_per_atom", "energy_above_hull", "elements"],
                chunk_size=500
            )
            data = [{
                "source": "MaterialsProject",
                "id": str(d.material_id),
                "formula": d.formula_pretty,
                "elements": ",".join(sorted(d.elements)) if d.elements else "",
                "formation_energy": d.formation_energy_per_atom,
                "energy_above_hull": d.energy_above_hull
            } for d in list(docs)[:MAX_RESULTS]]
            df = pd.DataFrame(data)
            df.to_csv(f"{OUTPUT_DIR}/mp_materials.csv", index=False)
            print(f"[MP] {len(df)} matériaux sauvegardés")
    except Exception as e:
        print(f"[MP] Erreur : {e}")

def download_oqmd():
    print("[OQMD] Téléchargement...")
    try:
        r = requests.get(
            "https://oqmd.org/oqmdapi/formationenergy",
            params={"limit": MAX_RESULTS, "format": "json"},
            timeout=120
        )
        if r.status_code == 200:
            entries = r.json().get("data", [])
            data = [{
                "source": "OQMD",
                "id": e.get("id"),
                "formula": e.get("composition"),
                "elements": ",".join(sorted(e.get("element_set", []))),
                "formation_energy": e.get("delta_e"),
                "energy_above_hull": e.get("stability")
            } for e in entries]
            pd.DataFrame(data).to_csv(f"{OUTPUT_DIR}/oqmd_materials.csv", index=False)
            print(f"[OQMD] {len(data)} matériaux sauvegardés")
        else:
            print(f"[OQMD] Erreur HTTP {r.status_code}")
    except Exception as e:
        print(f"[OQMD] Exception : {e}")

def download_jarvis():
    print("[JARVIS] Tentative de récupération d'informations...")
    # JARVIS propose des datasets via leur site. Exemple de lien connu (peut évoluer)
    print("[JARVIS] Datasets disponibles : https://jarvis.nist.gov/jarvisdft/")
    print("[JARVIS] Pour un téléchargement automatique, consulter leurs archives Figshare ou API.")
    # Placeholder pour future intégration API
    print("[JARVIS] Fonction prête à être étendue avec une URL de dataset directe.")

def download_aflow():
    print("[AFLOW] Tentative de requête API...")
    try:
        # Exemple de requête AFLOW simple (API documentée)
        url = "https://aflow.org/API/aflux/?species(Fe,O),paging(1,100)"
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            print(f"[AFLOW] Réponse reçue ({len(r.text)} caractères)")
            # Sauvegarde brute pour analyse
            with open(f"{OUTPUT_DIR}/aflow_sample.txt", "w") as f:
                f.write(r.text[:5000])
            print("[AFLOW] Échantillon sauvegardé dans data/aflow_sample.txt")
        else:
            print(f"[AFLOW] Erreur {r.status_code}")
    except Exception as e:
        print(f"[AFLOW] Exception : {e}")
    print("[AFLOW] Documentation complète : https://aflow.org/API/")

def download_matbench():
    print("[Matbench Discovery] Instructions de téléchargement...")
    print("[Matbench] Page des données : https://matbench-discovery.materialsproject.org/data")
    print("[Matbench] Fichiers souvent disponibles en CSV/JSON compressés sur Figshare ou Hugging Face.")
    # Exemple de tentative (lien à adapter selon la version)
    print("[Matbench] Fonction prête pour intégration d'un lien direct de dataset.")

def download_others_info():
    print("[Materials Cloud] https://www.materialscloud.org — téléchargements d'archives")
    print("[NOMAD] https://nomad-lab.eu — API et bulk downloads")
    print("[COD] Crystallography Open Database — structures libres")

def main():
    ensure_dir()
    print("=== Téléchargement multi-bases (version améliorée) ===\n")
    download_materials_project()
    download_oqmd()
    download_jarvis()
    download_aflow()
    download_matbench()
    download_others_info()
    print("\n=== Terminé ===")
    print(f"Fichiers dans {OUTPUT_DIR}/")
    print("Prochaine étape : fusionner les CSV avec fuse_materials_sources.py")

if __name__ == "__main__":
    main()
