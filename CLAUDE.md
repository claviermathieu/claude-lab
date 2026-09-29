# claude-lab — contexte pour Claude

Repo d'auto-formation à la configuration de Claude (Claude Code, skills, MCP, subagents, hooks, API/Agent SDK).

## Règles
- Réponses en français, directes, sans préambule.
- Chaque module vit dans `modules/NN-*/` avec un `README.md` (objectif, exercices, notes) et ses livrables.
- Les configs réelles testées vont dans `.claude/` (skills, agents, commands) et `.mcp.json` à la racine.
- Python : venv local `.venv`, pas de dépendance globale. Pas de secret en clair (Secret Manager / `.env` ignoré).
- Commits atomiques, message au présent : `module-06: ajoute skill scr-marche`.
