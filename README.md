# claude-lab

Laboratoire personnel pour se remettre à niveau sur l'IA générative et maîtriser la configuration de Claude — appliqué à des cas actuariels (Solvabilité II, IFRS 9, ALM).

- Feuille de route : [ROADMAP.md](ROADMAP.md) — tous les modules livrés au 29/09/2026
- Contexte projet lu par Claude Code : [CLAUDE.md](CLAUDE.md)
- Veille hebdomadaire : [notes/veille/](notes/veille/README.md) (mode d'emploi, sources, commande `/veille`)

## Structure
```
modules/NN-*/          un dossier par module (README : objectif, notes, résultats mesurés, exercices restants)
.claude/               config Claude Code réelle du repo
  settings.json        permissions + hooks
  hooks/               protect_data (PreToolUse), ruff_format et check_note_alm (PostToolUse)
  commands/            /review-actuariel, /note-alm, /veille
  agents/              model-validator (lecture seule, Opus)
  skills/              scr-marche, ifrs9-ecl, sii-reporting-qrt, note-alm
.mcp.json              serveurs MCP projet : github (distant), alm-data (stdio, modules/07-mcp/server)
plugins/               plugin actuariat-toolkit GÉNÉRÉ depuis .claude/ (plugins/build.sh)
.claude-plugin/        marketplace du repo
.github/workflows/     tests (actif), claude (@claude), claude-review (revue auto des PR)
notes/veille/          veille hebdomadaire (guide, modèle, un fichier par mois)
notes/alm/             notes ALM produites par l'assistant
data/                  données d'exemple (ignorées par git, régénérables)
```

## Démarrage
```bash
uv sync                                                   # .venv local (Python ≥ 3.12)
uv run pytest -q                                          # 92 tests
uv run python modules/07-mcp/server/make_sample_data.py   # données d'exemple dans data/
export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"    # serveur MCP GitHub (voir M07)
claude                                                    # approuver les serveurs github et alm-data
> /note-alm 0.03                                          # assistant ALM de bout en bout (M11)
```

## Modules
| Phase | Module | Livrable principal |
|---|---|---|
| 0 | [M00 État de l'art](modules/00-etat-de-l-art/) | Fiche modèles 2026 + choix par cas d'usage |
| 1 | [M01 Prompting](modules/01-prompting/) | 3 versions de prompt de revue SCR, mesurées sur Sonnet/Opus |
| 1 | [M02 Claude Code — bases](modules/02-claude-code-bases/) | Module Smith-Wilson EIOPA + tests |
| 2 | [M03 Mémoire](modules/03-memoire-claude-md/) | `~/.claude/CLAUDE.md`, CLAUDE.md du repo avec import |
| 2 | [M04 Settings & hooks](modules/04-settings-permissions-hooks/) | Permissions, hooks ruff / protection data |
| 2 | [M05 Commandes & subagents](modules/05-slash-commands-subagents/) | `/review-actuariel` + `model-validator` |
| 3 | [M06 Skills](modules/06-skills/) | 3 skills métier + test de déclenchement |
| 3 | [M07 MCP](modules/07-mcp/) | Serveur `alm-data` (Parquet DVC, durations, gap) + GitHub |
| 3 | [M08 Plugins](modules/08-plugins/) | Plugin `actuariat-toolkit` + marketplace |
| 4 | [M09 API & Agent SDK](modules/09-api-agent-sdk/) | Agent ALM (boucle manuelle / Agent SDK), mesures de cache |
| 4 | [M10 Automatisation & CI](modules/10-automatisation-ci/) | `claude -p` structuré, GitHub Actions, service Cloud Run |
| 5 | [M11 Projet final](modules/11-projet-final/) | Assistant ALM : commande + skill + MCP + subagent + hooks |
