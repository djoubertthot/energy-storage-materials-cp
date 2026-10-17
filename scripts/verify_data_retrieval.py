"""
Verification script to test if materials data can be retrieved from open APIs.
Run locally with your keys where required.
"""

import requests
import json

def test_oqmd(limit=5):
    """Test OQMD public API (no key needed)"""
    url = "http://oqmd.org/oqmdapi/formationenergy"
    params = {
        "fields": "name,entry_id,delta_e,stability",
        "limit": limit,
        "filter": "stability<0.1"
    }
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        print(f"OQMD OK: {len(data.get('data', []))} entries returned")
        if data.get('data'):
            print("Sample:", data['data'][0])
        return True
    except Exception as e:
        print(f"OQMD failed: {e}")
        return False

def test_mp_optimade():
    """Test Materials Project OPTIMADE (public, limited)"""
    url = "https://optimade.materialsproject.org/v1/structures"
    params = {"filter": "nelements=2", "page_limit": 3}
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        print(f"MP OPTIMADE OK: {len(data.get('data', []))} structures")
        return True
    except Exception as e:
        print(f"MP OPTIMADE failed: {e}")
        return False

def main():
    print("=== Verifying data retrieval ===")
    oqmd_ok = test_oqmd()
    mp_ok = test_mp_optimade()
    print("\nSummary:")
    print(f"OQMD: {'OK' if oqmd_ok else 'FAILED'}")
    print(f"MP OPTIMADE: {'OK' if mp_ok else 'FAILED'}")
    print("\nFor full Materials Project, set MP_API_KEY and use mp-api client.")
    print("For JARVIS/AFLOW, install respective packages and test locally.")

if __name__ == "__main__":
    main()
