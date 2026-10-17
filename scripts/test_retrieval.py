"""
Small test script to verify materials data retrieval.
Tests OQMD (public) and Materials Project OPTIMADE (public).
"""

import requests
import json

def test_oqmd(limit=5):
    print("=== Testing OQMD ===")
    url = "http://oqmd.org/oqmdapi/formationenergy"
    params = {
        "fields": "name,entry_id,delta_e,stability",
        "limit": limit,
        "filter": "stability<0.05"
    }
    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        entries = data.get("data", [])
        print(f"Success: {len(entries)} entries retrieved")
        if entries:
            print("Sample entry:")
            print(json.dumps(entries[0], indent=2))
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

def test_mp_optimade(limit=3):
    print("\n=== Testing Materials Project OPTIMADE ===")
    url = "https://optimade.materialsproject.org/v1/structures"
    params = {
        "filter": "nelements=1",
        "page_limit": limit
    }
    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        structures = data.get("data", [])
        print(f"Success: {len(structures)} structures retrieved")
        if structures:
            print("Sample formula:", structures[0].get("attributes", {}).get("chemical_formula_descriptive"))
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

def main():
    print("Materials Data Retrieval Test\n")
    oqmd_ok = test_oqmd()
    mp_ok = test_mp_optimade()
    
    print("\n=== Summary ===")
    print(f"OQMD: {'OK' if oqmd_ok else 'FAILED'}")
    print(f"MP OPTIMADE: {'OK' if mp_ok else 'FAILED'}")
    print("\nFor full Materials Project access, use your API key with mp-api.")
    print("Run the main download scripts after successful tests.")

if __name__ == "__main__":
    main()
