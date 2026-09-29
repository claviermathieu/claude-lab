# M02 — Claude Code : bases

**Objectif** : être autonome sur l'usage quotidien de Claude Code (CLI + extension VS Code), gérer son contexte et savoir l'utiliser en script.

## Installation
- CLI : `claude` (ici `/opt/homebrew/bin/claude`). Mise à jour : `claude update`.
- Extension VS Code : panneau Claude natif, les sélections de l'éditeur sont passées en contexte, diagnostics IDE remontés après chaque édition.
- Authentification : compte claude.ai (abonnement) ou clé API (`ANTHROPIC_API_KEY`), ou Vertex/Bedrock.

## Modes de permission (Shift+Tab pour basculer)
| Mode | Comportement | Quand |
|---|---|---|
| Défaut | Demande avant chaque écriture / commande non autorisée. | Découverte d'un repo. |
| Accept edits | Écritures de fichiers acceptées, commandes toujours soumises. | Tâche cadrée. |
| Plan | Lecture seule : Claude explore et propose un plan, n'écrit rien. | Avant un changement non trivial. |
| Auto | Un classifieur valide les actions sûres, bloque les risquées. | Tâches longues, peu d'interruptions. |

Les règles fines vivent dans `settings.json` (`permissions.allow/ask/deny`) → M04.

## Commandes essentielles
| Commande | Rôle |
|---|---|
| `/init` | Génère un `CLAUDE.md` à partir du code. |
| `/context` | Visualise l'occupation du contexte (system, outils, MCP, mémoire, messages). |
| `/compact [consigne]` | Résume l'historique pour libérer du contexte, en gardant ce que la consigne précise. |
| `/clear` | Repart d'un contexte vide (nouvelle tâche = `/clear`). |
| `/model` | Change de modèle (Opus 5.5 par défaut, Sonnet 5.5, Haiku 4.5…) et d'effort. |
| `/cost` | Coût / tokens de la session (utile en clé API). |
| `/mcp` | État et authentification des serveurs MCP. |
| `/memory` | Édite les fichiers de mémoire (`CLAUDE.md`). |
| `/resume` | Reprend une session passée. |

## Reprise de session
- `claude --continue` (`-c`) : reprend la dernière session du répertoire.
- `claude --resume` (`-r`) : choisit une session dans la liste (ou par ID).

## Mode headless : `claude -p`
```bash
claude -p "résume ce fichier" < note.md                 # sortie texte
claude -p --output-format json "…"                      # JSON avec coût, durée, session_id
claude -p --model sonnet --tools "" < prompt.txt        # sans outils (test de prompt pur)
claude -p --allowedTools "Read,Grep" "…"                # outils restreints
```
Utilisé en M01 ([run.sh](../01-prompting/run.sh)) pour comparer des prompts ; base de l'automatisation CI en M10.

## Exercice : courbe EIOPA + Smith-Wilson

Module [eiopa_curve/](eiopa_curve/) généré avec Claude Code, testé ([tests/](tests/)).

- `calibrate(maturities, rates, ufr, cra_bp)` : retranche la CRA, calcule ζ = W⁻¹(m − μ), cherche le plus petit α ≥ 0,05 tel que l'intensité forward au point de convergence max(LLP + 40, 60) soit à moins de 1 bp de ω = ln(1 + UFR) (bissection).
- `SmithWilsonCurve` : `discount`, `spot` (composition annuelle), `forward_annual`, `forward_intensity` (dérivée analytique au-delà du LLP).

```bash
uv sync                                                  # crée .venv (Python ≥ 3.12, numpy, pytest, ruff)
uv run pytest -q                                         # 13 tests
cd modules/02-claude-code-bases && ../../.venv/bin/python -m eiopa_curve   # démo
```

Démo (courbe swap EUR fictive 1–20 ans, UFR 3,30 %, CRA 10 bp) : α = 0,103, écart au CP = 1,000 bp, forward 1 an à 100 ans = 3,300 %.

Tests couverts : reproduction exacte des taux aux points liquides, application de la CRA, critère de convergence 1 bp, minimalité de α, convergence du forward vers l'UFR, cohérence dérivée analytique / différences finies, matrice W symétrique définie positive, validation des entrées.

### Limites connues
- Pas d'ajustement de volatilité (VA) ni d'interpolation depuis des taux swap par-rate (on part de taux zéro-coupon).
- Courbe d'entrée fictive : comparer à la courbe EIOPA publiée (fichier mensuel `EIOPA_RFR_*.xlsx`) avant tout usage.

## Exercices
- [x] Notes sur modes, commandes, reprise, headless.
- [x] Module Smith-Wilson + tests.
- [ ] Rejouer la courbe EIOPA EUR officielle d'un mois donné et comparer à 0,1 bp près.
