# claude-lab

Laboratoire personnel pour se remettre à niveau sur l'IA générative et maîtriser la configuration de Claude.

- Feuille de route : [ROADMAP.md](ROADMAP.md)
- Contexte projet lu par Claude Code : [CLAUDE.md](CLAUDE.md)
- Config Claude Code du repo : `.claude/` (settings, skills, agents, commands) et `.mcp.json`

## Structure
```
modules/      un dossier par module de la roadmap (notes + exercices)
notes/        veille, fiches de synthèse
.claude/      config Claude Code versionnée (sert de terrain d'exercice)
.mcp.json     serveurs MCP au scope projet
```

## Démarrage
```bash
uv sync                                                   # .venv local (Python ≥ 3.12)
uv run pytest -q                                          # tests des modules
export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"    # pour le serveur MCP GitHub (.mcp.json)
claude                                                    # approuver le serveur `github` au 1er lancement
```
