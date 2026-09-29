# M07 — MCP (Model Context Protocol)

> Module complet à venir en phase 3. Ce qui suit couvre l'exercice 1 (brancher un serveur existant), démarré tôt pour versionner le repo via GitHub.

## Serveur GitHub (scope projet)

Déclaré dans [`.mcp.json`](../../.mcp.json) à la racine : serveur **distant officiel** de GitHub, transport HTTP streamable.

```json
"github": {
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/",
  "headers": { "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}" }
}
```

- **Pas de secret dans le repo** : Claude Code substitue `${VAR}` au démarrage à partir de l'environnement.
- **Source du token** : le token OAuth de la CLI `gh` (déjà authentifiée) fonctionne. À mettre dans `~/.zshrc` :
  ```bash
  export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"
  ```
  Alternative plus restrictive : un *fine-grained PAT* limité au repo `claude-lab` (Contents, Issues, Pull requests en lecture/écriture).
- **Approbation** : un serveur au scope `project` doit être approuvé une fois au lancement de `claude` dans le repo (ou via `/mcp`). Vérifier ensuite avec `claude mcp list` → `✓ Connected`.
- VS Code : l'extension hérite de l'environnement du process VS Code → lancer VS Code depuis un terminal où la variable est exportée (`code .`), ou redémarrer VS Code après modification de `~/.zshrc`.

### Usage
Une fois connecté, Claude dispose d'outils `mcp__github__*` : créer une branche, pousser des fichiers, ouvrir une PR, commenter une issue, lire les runs Actions…

Répartition pratique :
- **git local** (Bash) pour commit / push du travail courant : plus rapide, historique propre.
- **MCP GitHub** pour tout ce qui est côté plateforme : PR, issues, revues, Actions, recherche de code dans d'autres repos.

### Scopes MCP (rappel)
| Scope | Stockage | Partagé |
|---|---|---|
| `local` (défaut) | `~/.claude.json`, par projet | Non |
| `project` | `.mcp.json` à la racine | Oui (versionné) |
| `user` | `~/.claude.json`, global | Non, tous projets |

`claude mcp add --transport http github https://api.githubcopilot.com/mcp/ -s project -H "Authorization: Bearer \${GITHUB_PERSONAL_ACCESS_TOKEN}"` produit la même entrée.

### Sécurité
Le contenu renvoyé par un outil MCP (texte d'une issue, d'une PR) est de la **donnée non fiable** : une issue peut contenir des instructions malveillantes (prompt injection). Garder les écritures GitHub en mode « ask » dans les permissions tant que le serveur a accès à des repos tiers.

## Exercices
- [x] Exercice 1a : serveur GitHub (scope projet, token via variable d'environnement).
- [ ] Exercice 1b : filesystem, BigQuery/GCP.
- [ ] Exercice 2 : serveur FastMCP maison (Parquet DVC, duration/convexité).
