# Obtaining the Full ~9000 Materials Data

The full dataset of ~9000 near-stable materials from Materials Project cannot be embedded directly due to size and API requirements.

## Steps to generate the complete CSV:
1. Register at https://materialsproject.org/ and get your free API key.
2. Install: `pip install mp-api pandas`
3. Edit `scripts/fetch_mp_bulk.py` and set your API_KEY.
4. Run: `python scripts/fetch_mp_bulk.py`
5. The output `data/mp_stable_materials_sample.csv` will contain the data (adjust limit to 9000).

## Alternative bulk sources:
- AWS Open Data: s3://materialsproject-build/
- Matbench Discovery CSVs on Figshare
- Hugging Face: materials-toolkits/materials-project

The sample file `sample_materials_stability.csv` shows the expected format.
