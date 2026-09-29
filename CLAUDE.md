# claude-lab — contexte pour Claude

Repo d'auto-formation à la configuration de Claude (Claude Code, skills, MCP, subagents, hooks, API/Agent SDK). Feuille de route : `ROADMAP.md` (la lire seulement si la tâche porte sur la progression).

## Règles
- Réponses en français, directes, sans préambule. (La langue est aussi fixée dans `~/.claude/CLAUDE.md` ; répétée ici pour les autres contributeurs.)
- Chaque module vit dans `modules/NN-*/` avec un `README.md` (objectif, exercices, notes) et ses livrables.
- Les configs réelles testées vont dans `.claude/` (skills, agents, commands, hooks) et `.mcp.json` à la racine. Le plugin `plugins/actuariat-toolkit/` est **généré** depuis `.claude/` par `plugins/build.sh` : ne jamais l'éditer à la main.
- Pas de secret en clair (Secret Manager / variables d'environnement / trousseau).
- Commits atomiques, message au présent : `module-06: ajoute skill scr-marche`. Pousser sur `origin/main` (GitHub privé `claviermathieu/claude-lab`).

## Commandes
- `uv sync` · `uv run pytest -q` · `uv run ruff check .`
- Serveur MCP maison : `uv run python modules/07-mcp/server/server.py` (stdio).
- Données d'exemple : `uv run python modules/07-mcp/server/make_sample_data.py` (écrit dans `data/`, ignoré par git).

## Conventions Python
@.claude/conventions-python.md
