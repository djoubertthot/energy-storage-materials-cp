# Data Retrieval Verification

## Quick Test
```bash
pip install requests
python scripts/verify_data_retrieval.py
```

## Expected Results
- **OQMD**: Should return sample formation energy data (public API).
- **Materials Project OPTIMADE**: Limited public access; full data requires API key + mp-api.

## Full Verification
1. Get Materials Project API key from https://materialsproject.org/
2. Set environment variable or edit script.
3. Run the main download scripts with small MAX limits.
4. Check generated CSVs in `data/`.

## Common Issues
- Missing API key for MP → use OPTIMADE or bulk downloads.
- Network/timeout → retries are built into recent scripts.
- Rate limits → see `docs/SAFE_USAGE_GUIDELINES.md`.

Data is considered successfully retrieved when CSVs contain rows with formula, formation_energy, and e_above_hull.
