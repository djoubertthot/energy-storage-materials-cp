#!/usr/bin/env python3
"""
Script d'exemple pour télécharger des données depuis d'autres bases publiques.
À compléter selon les APIs disponibles.
"""

import requests
import pandas as pd

def download_matbench_sample():
    """Exemple de téléchargement depuis Matbench Discovery (datasets publics)."""
    print("Matbench Discovery : voir https://matbench-discovery.materialsproject.org/data")
    print("Datasets disponibles en téléchargement direct (CSV, JSON, etc.).")
    # Exemple de lien direct possible selon les versions
    # url = "https://..."
    # df = pd.read_csv(url)
    # return df
    return None

def download_jarvis_info():
    print("JARVIS : datasets disponibles sur https://jarvis.nist.gov")
    print("Recherche de datasets 'formation energy' ou 'stable materials'.")
    return None

if __name__ == "__main__":
    download_matbench_sample()
    download_jarvis_info()
    print("\nPour une intégration complète, ajouter les fonctions dans fuse_materials_sources.py")
