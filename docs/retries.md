# Retries automatiques

Le script intègre maintenant :
- Retries jusqu'à 5 tentatives
- Backoff exponentiel (2^attempt + jitter)
- Détection spécifique des erreurs 429 (rate limit)
- Gestion des erreurs réseau

Cela réduit fortement le risque de ban tout en maximisant la récupération des données.
