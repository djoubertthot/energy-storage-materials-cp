"""Exemple simple pour OQMD (Open Quantum Materials Database).

Voir https://www.oqmd.org pour l'API.
"""
import requests

def search_oqmd(elements):
    # Exemple de requête (adapter selon l'API actuelle)
    url = "https://www.oqmd.org/api/materials/"
    params = {"elements": ",".join(elements), "limit": 10}
    # response = requests.get(url, params=params)
    # return response.json()
    print("Voir documentation OQMD pour l'API complète.")
    return []

if __name__ == "__main__":
    print(search_oqmd(["Fe", "O"]))
