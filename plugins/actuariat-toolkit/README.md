# actuariat-toolkit v0.2.0

> Généré par `plugins/build.sh` depuis `.claude/` et `modules/07-mcp/server/` — ne pas éditer ici.

| Composant | Contenu |
|---|---|
| Commandes | `/review-actuariel <chemin>`, `/note-alm [taux]` |
| Subagent | `model-validator` (lecture seule, Opus) |
| Skills | `ifrs9-ecl`, `note-alm`, `scr-marche`, `sii-reporting-qrt` |
| Hooks | protection de `data/` (PreToolUse), `ruff format` des .py et contrôle des notes ALM (PostToolUse) |
| MCP | `alm-data` (stdio, `uv run --script`) — données dans `$ALM_DATA_DIR` ou `./data` |

Prérequis : `uv` et `python3` dans le PATH ; `ruff` (dans `.venv` du projet ou global) pour le hook de format.

Installation :
```bash
claude plugin marketplace add claviermathieu/claude-lab   # ou un chemin local vers le repo
claude plugin install actuariat-toolkit@claude-lab
```
