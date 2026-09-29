# Conventions Python du repo

- Gestion d'environnement : `uv sync` à la racine ; lancer via `uv run …` (pytest, ruff, scripts).
- Dépendances ajoutées avec `uv add <pkg>` (ou `uv add --group dev <pkg>`), jamais à la main dans `uv.lock`.
- Chaque module Python d'un module de formation vit sous `modules/NN-*/` ; ses tests dans `modules/NN-*/tests/`. Ajouter le dossier du module à `pythonpath` dans `pyproject.toml` si besoin.
- Montants en M€ et taux en décimal (0.033 = 3,30 %) dans le code ; affichage en % seulement en sortie.
- Docstrings et commentaires en français, noms de fonctions en anglais.
- `ruff format` est lancé automatiquement par un hook après chaque édition de `.py` (voir M04).
- Le dossier `data/` est en lecture seule pour Claude (hook PreToolUse) ; les jeux d'exemple se régénèrent par script.
