# M10 — Automatisation & CI

**Objectif** : faire travailler Claude sans humain au clavier (scripts, CI GitHub, service cloud), en gardant le contrôle sur le coût et les secrets.

## 1. `claude -p` en script — [scripts/revue_diff.sh](scripts/revue_diff.sh)
Revue d'un diff git en headless, **sortie structurée** :
- `--output-format json` : enveloppe avec `result`, `total_cost_usd`, `duration_ms`, `session_id`, `num_turns`… ;
- `--json-schema '<schéma>'` : la réponse est validée contre un schéma (`verdict` ∈ ok/a_corriger/bloquant, liste de `constats`) → exploitable par `python3`/`jq` ;
- `--allowedTools "Read,Grep,Glob"` : lecture seule ; code retour 2 si verdict bloquant (utilisable comme porte de CI ou hook git `pre-push`).

Démo sur le commit du module 09 ([demo/revue-commit-module-09.json](demo/revue-commit-module-09.json)) — Sonnet 5.5, 39 s, 0,29 $ : verdict « ok », 5 constats mineurs dont 4 justes (tarif de cache 1 h de Claude Code, variance n=1, arrondi « < 6,0 M€ », `--runs 0` → `NameError`) et 1 faux positif (le serveur résout déjà `DATA_DIR`). Les deux premiers utiles ont été corrigés (commit `module-09: borne --runs…`).

Autres options utiles : `--max-budget-usd`, `--max-turns`, `--output-format stream-json --verbose` (événements au fil de l'eau, vu en M06/M08), `--resume <session_id>`.

## 2. GitHub Actions
| Workflow | Déclencheur | Rôle | Secret |
|---|---|---|---|
| [tests.yml](../../.github/workflows/tests.yml) | push `main`, PR | `uv sync --locked`, ruff, pytest, **vérifie que le plugin généré est à jour** (`build.sh` + `git diff --exit-code`) | aucun |
| [claude.yml](../../.github/workflows/claude.yml) | mention `@claude` (issue, PR, commentaire de revue) | Claude répond / implémente et pousse une branche | `CLAUDE_CODE_OAUTH_TOKEN` |
| [claude-review.yml](../../.github/workflows/claude-review.yml) | PR ouverte / mise à jour | revue auto avec les skills du repo + subagent `model-validator`, tests, un commentaire de synthèse | `CLAUDE_CODE_OAUTH_TOKEN` |

`anthropics/claude-code-action@v1` exécute Claude Code dans le runner : il lit `CLAUDE.md`, `.claude/` (skills, agents, settings) du repo. `claude_args` passe les options CLI (`--model`, `--max-turns`, `--allowedTools`).

**Activation des workflows Claude (à faire par toi)** :
```bash
claude setup-token                                   # génère un token longue durée lié à ton abonnement
gh secret set CLAUDE_CODE_OAUTH_TOKEN -R claviermathieu/claude-lab   # colle le token
```
Et installer l'app GitHub Claude sur le repo (`/install-github-app` dans Claude Code, ou https://github.com/apps/claude). Alternative facturée à l'usage : secret `ANTHROPIC_API_KEY` et entrée `anthropic_api_key`.

## 3. Service Cloud Run — [cloudrun/](cloudrun/)
API FastAPI `POST /revue {"note": …}` : revue d'une note SCR marché par Claude Sonnet 5.5, avec le **skill `scr-marche` comme prompt système mis en cache** (identique d'une requête à l'autre → ~95 % du prix d'entrée économisé dès la 2e requête), `fallbacks: "default"`, erreurs API traduites en codes HTTP (429/502/503), refus → 422.

Sécurité :
- clé dans **Secret Manager**, injectée en variable d'environnement par Cloud Run (`--set-secrets`), jamais dans l'image ;
- compte de service dédié, seul lecteur du secret ;
- service **privé** (`--no-allow-unauthenticated`) : appel avec un jeton d'identité Google ;
- conteneur non root, `max-instances 3` pour borner le coût.

[deploy.sh](cloudrun/deploy.sh) fait tout (API GCP, secret lu sur stdin, compte de service, IAM, build Cloud Build, déploiement en `europe-west9`).

Vérifications faites : 6 tests avec faux client ([tests/test_cloudrun.py](tests/test_cloudrun.py)) ; démarrage local réel `uvicorn` → `/health` OK, validation 422 sur note trop courte.
⚠️ **Non déployé** : `gcloud` et Docker ne sont pas installés sur ce poste, et le déploiement engage de la facturation GCP. Commande une fois `gcloud` configuré :
```bash
PROJECT_ID=<projet> modules/10-automatisation-ci/cloudrun/deploy.sh
```

## Exercices
- [x] `claude -p` scripté, JSON + schéma, porte bloquante.
- [x] Workflows GitHub : tests (actif), `@claude` et revue auto (prêts, secret à créer).
- [x] Service Cloud Run minimal + Secret Manager (testé localement, non déployé).
- [ ] Créer le secret, ouvrir une PR de test et observer la revue automatique.
- [ ] Déployer le service et mesurer latence / coût par requête avec le cache chaud.
