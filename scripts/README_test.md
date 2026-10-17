# Test Retrieval Script

## Purpose
Quickly verify that materials data can be retrieved from open endpoints.

## Usage
```bash
pip install requests
python scripts/test_retrieval.py
```

## What it tests
- OQMD public REST API (formation energies, stability)
- Materials Project OPTIMADE endpoint (structures)

## Expected Output
Success messages with sample data, or clear error messages.

If tests pass, you can confidently run the larger download scripts.
