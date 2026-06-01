
# Appliquer la labellisation des marques


1. Télécharger depuis NocoDB le contenu de la table "Scrapp - Post (PROD)" filtré sur chaquer réseau (instagram, tiktok, youtube) dans ./data/scrapped/<network>.csv.

2. Lancer l'exécution du script de labellisation pour chaque réseau:
   `uv run python3 ./apply_extraction.py -n <network>`

3. Voir les résultats dans ./data/results/<network>.csv

# Evaluer les algo de labellisation

Pour évaluer les algo de labellisations:
- Instagram: `uv run python3 ./extraction_instagram.py ./data/labelled/instagram.csv ./data/scrapped/instagram.csv`

TODOs:
* Documenter les prerequis
* Documenter d'où viennent les fichiers dans labelled
* Documenter comment évaluer l'algo pour tiktok et Youtube
* Documenter comment réintégrer les données dans Noco DB





## Development

```bash
# Install dependencies
uv sync

# Type checking
uv run mypy .

# Linting
uv run ruff check .

# Formatting
uv run ruff format .
```