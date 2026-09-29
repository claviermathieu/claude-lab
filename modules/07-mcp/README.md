# M07 — MCP (Model Context Protocol)

**Objectif** : comprendre le protocole, brancher des serveurs existants et écrire le sien.

## Architecture
- **Hôte / client** (Claude Code, Claude Desktop, ton agent Python) ↔ **serveur** (processus qui expose des capacités). Un client par serveur, négociation des capacités à l'initialisation (JSON-RPC).
- **Transports** : `stdio` (sous-processus local, le plus simple et le plus sûr) ; **HTTP streamable** (serveur distant, un endpoint `/mcp`, auth OAuth ou en-tête) ; SSE est déprécié.
- **Primitives serveur** : **tools** (actions appelées par le modèle), **resources** (données lisibles, adressées par URI, choisies par l'application ou l'utilisateur — `@serveur:uri` dans Claude Code), **prompts** (modèles de prompts → deviennent des slash commands `/mcp__serveur__prompt`).
- **Primitives client** : sampling (le serveur demande une complétion au LLM de l'hôte), elicitation (le serveur demande une info à l'utilisateur), roots.
- Commandes : `claude mcp add|list|get|remove`, `/mcp` (état, authentification OAuth), `--mcp-config fichier.json` (+ `--strict-mcp-config` pour ignorer les autres).

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

## Autres serveurs existants (exercice 1b)
- **filesystem** (`npx -y @modelcontextprotocol/server-filesystem <dossier>`) : inutile dans Claude Code, qui a déjà Read/Write/Glob/Grep ; utile pour Claude Desktop ou un agent API. Non activé.
- **BigQuery** : via *MCP Toolbox for Databases* de Google (`toolbox --prebuilt bigquery --stdio`, auth ADC `gcloud auth application-default login`, variable `BIGQUERY_PROJECT`). Non activé : `gcloud` n'est pas installé sur ce poste. Entrée à ajouter une fois GCP configuré :
  ```json
  "bigquery": { "command": "toolbox", "args": ["--prebuilt", "bigquery", "--stdio"],
                "env": { "BIGQUERY_PROJECT": "${BIGQUERY_PROJECT}" } }
  ```
  Vérifier la syntaxe exacte sur la doc Google au moment de l'installer.

## Serveur maison `alm-data` (exercice 2)

[server/server.py](server/server.py) — SDK Python `mcp` **v2** (`MCPServer`, ex-`FastMCP` en v1 : l'API a été renommée, les tutos v1 ne fonctionnent plus tels quels). Transport stdio.

| Outil | Rôle |
|---|---|
| `list_datasets` | Jeux disponibles dans `data/` : colonnes, nb de lignes, **version DVC** (md5 lu dans le manifeste `.dvc`) |
| `read_dataset(nom, colonnes, limite)` | Lecture Parquet/CSV, plafonnée à 500 lignes |
| `portfolio_duration_convexity(nom, choc_bp)` | Prix, durations Macaulay/modifiée, convexité par titre et agrégées (pondération VM), sensibilité ±choc |
| `cashflow_duration(nom, taux)` | VA, duration, convexité d'une série de flux (passif) |
| `duration_gap(taux, choc_bp)` | Synthèse ALM déterministe : réconciliation bilan / recalculé (seuil 5 %), duration gap et ΔFP ±choc sur deux bases, robustesse du signe (ajouté en M11) |

Données : `uv run python modules/07-mcp/server/make_sample_data.py` (40 obligations, 40 ans de flux de passif, bilan simplifié ; manifestes `.dvc` simulés, DVC n'étant pas installé).

Choix de conception :
- **Sécurité** : racine unique `data/` (ou `$ALM_DATA_DIR`), chemins résolus et refusés s'ils sortent de la racine (`../`, absolus) ; lecture seule ; volume plafonné.
- **Erreurs** : lever `ToolError` pour les erreurs métier — une exception quelconque est masquée par le SDK (« Error executing tool ») et le modèle ne peut pas corriger son appel.
- Retour `dict` → JSON dans le contenu texte ; docstrings = descriptions d'outils lues par le modèle (unités, colonnes attendues).

Déclaré dans [`.mcp.json`](../../.mcp.json) : `uv run --quiet python modules/07-mcp/server/server.py`.

### Tests
- [tests/test_server.py](tests/test_server.py) — 15 cas : formules (zéro-coupon, pair, duration et convexité vs différences finies), protocole via `Client(server)` in-process, **transport stdio réel** (sous-processus), refus de `../secret.csv`, `/etc/passwd`.
- Test réel dans Claude Code (`claude -p … --mcp-config … --strict-mcp-config`) : « duration du portefeuille et du passif, duration gap ? » → actif VM 731,4 M€, D_mod 8,98 ; passif VA 659,4 M€, D_mod 9,06 ; gap pondéré +0,81 an. Claude signale de lui-même la limite (passif à taux plat vs rendements par titre).

## Exercices
- [x] Exercice 1a : serveur GitHub (scope projet, token via variable d'environnement).
- [x] Exercice 1b : filesystem et BigQuery documentés (non activés, voir ci-dessus).
- [x] Exercice 2 : serveur `alm-data` (Parquet DVC, duration/convexité) + tests + entrée `.mcp.json`.
- [ ] Ajouter une *resource* `alm://bilan` et un *prompt* `note-alm` au serveur, et les utiliser depuis Claude Code (`@alm-data:…`, `/mcp__alm-data__note-alm`).
