# M04 — Settings, permissions, hooks

**Objectif** : cadrer ce que Claude peut faire sans demander, et automatiser des contrôles déterministes (le modèle peut oublier une consigne, un hook s'exécute toujours).

## Fichiers de settings (du moins au plus prioritaire)

| Fichier | Portée | Versionné |
|---|---|---|
| `~/.claude/settings.json` | Utilisateur, tous projets | Non |
| `.claude/settings.json` | Projet, équipe | Oui |
| `.claude/settings.local.json` | Projet, toi seul | Non (gitignoré) |
| Arguments CLI (`--allowedTools`, `--model`…) | Session | — |
| Managed settings (IT) | Machine | Non, **non contournable** |

Les listes `permissions` se cumulent entre niveaux ; en cas de conflit **deny > ask > allow**.

## Permissions du repo ([`.claude/settings.json`](../../.claude/settings.json))
- **allow** : lecture git, `uv sync`, `uv run pytest`, `uv run ruff`.
- **ask** : `git push`, et les outils MCP GitHub qui écrivent directement sur la plateforme (push de fichiers, merge de PR…).
- **deny** : lecture des `.env`, `git push --force`.

Syntaxe : `Outil(motif)` ; `Bash(uv run pytest:*)` = préfixe ; `Read(./chemin)` en style gitignore ; `mcp__serveur__outil` pour MCP.

## Hooks

| Événement | Moment | Usage typique |
|---|---|---|
| `SessionStart` | Début de session | Injecter du contexte (branche, tickets ouverts) |
| `UserPromptSubmit` | Avant traitement du prompt | Ajouter du contexte, bloquer un prompt |
| `PreToolUse` | Avant un appel d'outil | **Autoriser / refuser / demander** |
| `PostToolUse` | Après un appel d'outil réussi | Formater, linter, lancer des tests |
| `Stop` / `SubagentStop` | Fin de réponse | Forcer une vérification finale |
| `Notification`, `PreCompact`, `SessionEnd` | … | Alertes, sauvegardes |

Contrat : le hook reçoit un JSON sur stdin (`tool_name`, `tool_input`, `session_id`, `cwd`…). Code retour **0** = OK (stdout éventuellement lu), **2** = blocage, stderr renvoyé à Claude ; ou sortie JSON structurée (`hookSpecificOutput.permissionDecision: allow|deny|ask`). `$CLAUDE_PROJECT_DIR` pointe la racine du projet.

### Hooks mis en place
1. **[`protect_data.py`](../../.claude/hooks/protect_data.py)** — `PreToolUse` sur `Write|Edit|MultiEdit|NotebookEdit|Bash` : refuse (JSON `deny` + raison) toute écriture dans `data/`, y compris via `../`, chemin absolu, `cd`, redirection shell. Pour Bash, seules les **cibles d'écriture** sont examinées (destination de `cp`/`mv`, arguments de `rm`/`touch`/`tee`, `sed -i`, `dvc add`) : lire depuis `data/` reste permis. Exception : le script officiel `make_sample_data.py`.
2. **[`ruff_format.py`](../../.claude/hooks/ruff_format.py)** — `PostToolUse` sur `Write|Edit|MultiEdit` : `ruff format` sur chaque `.py` écrit ; en cas d'erreur de syntaxe, exit 2 → Claude voit l'erreur et corrige.

Scripts en Python (standard library) pour ne pas dépendre de `jq`.

### Vérification
- Tests unitaires : [`tests/test_hooks.py`](tests/test_hooks.py) (23 cas, JSON simulé sur stdin).
- Test réel : `claude -p … --model haiku --allowedTools Write` demandant d'écrire `data/test.txt` puis un `.py` mal formaté → fichier `data/` **non créé** (Claude le signale : « hook de protection ») et `.py` reformaté (`x=[1,2 ,3]` → `x = [1, 2, 3]`).

### Limites
- Le filtre Bash est une heuristique : `python -c "open('data/x','w')"` passe. Pour une vraie garantie, utiliser le **sandbox** Bash de Claude Code (restrictions d'écriture au niveau OS) ou les permissions du système de fichiers.
- Première version (regex sur toute la commande) : `cp <repo>/data/x /tmp/` refusé à tort — découvert en M08, corrigé par l'analyse des cibles.
- Les hooks exécutent du code avec tes droits : relire tout hook venant d'un repo tiers avant d'ouvrir Claude dedans.

## Autres réglages utiles (non activés)
- `"model": "opus"`, `"env": {"VAR": "…"}`, `"statusLine": {"type": "command", "command": "…"}` (ligne d'état : modèle, branche, coût), `"enableAllProjectMcpServers": true` (éviter en équipe : approuver les serveurs un à un).
- `/permissions` pour voir les règles effectives, `/hooks` pour voir les hooks chargés.

## Exercices
- [x] Hook `PostToolUse` ruff format.
- [x] Hook `PreToolUse` protection de `data/`.
- [x] Règles allow/ask/deny.
- [ ] Hook `Stop` qui lance `uv run pytest -q` et renvoie l'échec à Claude avant qu'il rende la main.
