# M08 — Plugins

**Objectif** : distribuer en une installation l'ensemble commandes + agents + skills + hooks + MCP.

## Structure d'un plugin
```
plugins/actuariat-toolkit/
├── .claude-plugin/plugin.json   # manifeste : name, version, description, author…
├── commands/*.md                # → /actuariat-toolkit:review-actuariel
├── agents/*.md                  # → actuariat-toolkit:model-validator
├── skills/<nom>/SKILL.md        # → actuariat-toolkit:scr-marche …
├── hooks/hooks.json             # mêmes événements que settings.json
├── .mcp.json                    # serveurs MCP démarrés avec le plugin
└── servers/, hooks/*.py …       # code référencé via ${CLAUDE_PLUGIN_ROOT}
```
- Tout est **namespacé** par le nom du plugin (pas de collision avec les configs projet).
- `${CLAUDE_PLUGIN_ROOT}` : chemin d'installation du plugin, à utiliser dans hooks et `.mcp.json`.
- **Marketplace** : un `.claude-plugin/marketplace.json` à la racine d'un repo liste des plugins (`source` relative, URL git…). Ici : [`/.claude-plugin/marketplace.json`](../../.claude-plugin/marketplace.json).

## Commandes
```bash
claude plugin validate plugins/actuariat-toolkit     # manifeste + composants
claude plugin validate .                              # marketplace
claude --plugin-dir plugins/actuariat-toolkit         # charger pour une session, sans installer
claude plugin marketplace add claviermathieu/claude-lab
claude plugin install actuariat-toolkit@claude-lab [-s user|project|local]
/plugin                                               # gestion interactive
```

## Le plugin `actuariat-toolkit`
**Généré** par [`plugins/build.sh`](../../plugins/build.sh) depuis `.claude/` (commandes, agents, skills, hooks) et `modules/07-mcp/server/` : une seule source de vérité, le plugin n'est jamais édité à la main. Le build :
- copie les composants ;
- écrit `hooks/hooks.json` avec `${CLAUDE_PLUGIN_ROOT}` ;
- préfixe le serveur MCP d'un en-tête **PEP 723** (dépendances inline) et le lance par `uv run --script` : le plugin n'a pas besoin du venv du repo ;
- passe le dossier de données par `ALM_DATA_DIR` (défaut `./data` du projet où le plugin est utilisé).

### Problèmes rencontrés en le packageant
1. **Chemins en dur dans les skills** (`python3 .claude/skills/…/script.py`) : cassés une fois le skill installé ailleurs. Corrigé : chemins relatifs au *dossier du skill*, que Claude reçoit au chargement.
2. **Faux positif du hook `protect_data`** : `cp <repo>/data/x.parquet /tmp/…/data/` refusé parce que la *source* contenait `data/`. Le hook analyse maintenant les **cibles d'écriture** (destination de `cp`/`mv`, redirections, `rm`/`touch`/`tee`, `sed -i`, `dvc add`) et suit les `cd` (23 tests).

### Test d'intégration (dossier vierge hors repo)
```bash
claude -p "…SCR marché avec le script du skill… duration du passif avec alm-data…" \
  --plugin-dir plugins/actuariat-toolkit --output-format stream-json --verbose --allowedTools "…"
```
Résultat : skills `actuariat-toolkit:{ifrs9-ecl,scr-marche,sii-reporting-qrt}`, agent `actuariat-toolkit:model-validator`, commande `actuariat-toolkit:review-actuariel` et serveur `plugin:actuariat-toolkit:alm-data` chargés ; SCR marché 83,3 (A = 0,5 correctement appliqué) ; duration du passif 9,06. Coût 0,12 $. Noms d'outils MCP d'un plugin : `mcp__plugin_<plugin>_<serveur>__<outil>`.

## Exercices
- [x] Plugin `actuariat-toolkit` (M05–M07 + hooks M04).
- [x] Marketplace dans le repo, validation, test `--plugin-dir`.
- [ ] Installer depuis GitHub (`claude plugin marketplace add claviermathieu/claude-lab`) sur un autre poste, puis versionner avec `claude plugin tag` à chaque release.
