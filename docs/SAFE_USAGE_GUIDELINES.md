# Safe Usage Guidelines for Materials Databases

To avoid rate limits, temporary blocks, or account bans, follow these recommendations.

## Materials Project
- **Terms**: https://materialsproject.org/terms
- **API Key required**. Keep it private.
- For heavy usage, email heavy.api.use@materialsproject.org beforehand.
- Prefer bulk downloads via AWS Open Data or official dumps over massive API queries.
- Use chunking and reasonable delays (1-2s between large requests).
- Do not redistribute raw bulk data without attribution.

## OQMD
- No API key required for REST API.
- Full SQL dumps available: https://oqmd.org/download (preferred for large volumes).
- Use moderate page sizes (limit ≤ 500) and small delays between requests.
- Respect server load; full database download is better for large analyses.

## AFLOW
- Public API, no key needed for basic access.
- Use paging (paging directive) rather than requesting everything at once.
- Prefer reasonable page sizes (100-1000).
- Official documentation: https://aflow.org/documentation/

## JARVIS
- Open data via jarvis-tools or Figshare.
- Bulk downloads preferred over repeated API calls.
- No strict rate limits published, but be polite.

## General Best Practices
1. Start with small test queries.
2. Add `time.sleep(0.5 to 2)` between paginated requests.
3. Prefer official bulk downloads / AWS / Figshare when available.
4. Cache results locally; do not re-query unnecessarily.
5. Attribute sources in any publications.
6. Monitor for 429 errors and back off exponentially.

The scripts in this repo include basic delays. Adjust MAX limits conservatively.
