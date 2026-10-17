# Pagination complète

Le script `scripts/all_bases_fusion.py` supporte maintenant :
- Pagination complète pour OQMD (offset/limit)
- Chunking natif pour Materials Project
- Retries exponentiels
- Progression en temps réel

Lance :
```bash
python scripts/all_bases_fusion.py
```

Ajuste `MAX_TOTAL` et `PAGE_SIZE` selon tes besoins.
