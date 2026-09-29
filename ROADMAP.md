# Roadmap — remise à niveau IA & configuration de Claude

> État des connaissances : mi-2026. Vérifier chaque point sur docs.claude.com / code.claude.com avant de le graver dans les notes (les fonctionnalités bougent vite).
> Cochez au fil de l'eau. Chaque module = 1 livrable commité.
> État au 29/09/2026 : tous les modules livrés. Restent hors ligne : exécution de `alm_agent_api.py` (clé API), déploiement Cloud Run (gcloud), secret GitHub des workflows Claude. Exercices bonus listés en fin de chaque README de module.

## Phase 0 — État de l'art (½ journée)
- [x] **M00** Panorama modèles 2026 : gamme Claude (Haiku 4.5, Sonnet 5.5, Opus 5.5, tier Mythos/Fable), concurrents (OpenAI, Google, open-weights). Critères : coût/token, contexte, latence, raisonnement (extended thinking).
- [x] Concepts à rafraîchir : fenêtre de contexte vs. context engineering, reasoning models, tool use, agents, RAG vs. MCP, prompt caching, batch.
- [x] Livrable : `modules/00-etat-de-l-art/README.md` — fiche 1 page + tableau de choix de modèle par cas d'usage.

## Phase 1 — Fondamentaux (1 journée)
- [x] **M01 Prompting** : rôle, contexte, balises XML, exemples, format de sortie, décomposition. Lire le guide prompt engineering Anthropic.
  - Exercice : prompt de revue d'un calcul de SCR marché ; itérer 3 versions, comparer.
- [x] **M02 Claude Code — bases** : installation (CLI + extension VS Code), modes (plan, auto-accept), `/init`, `/context`, `/compact`, `/clear`, `/model`, `/cost`, reprise de session (`--continue`, `--resume`), mode headless `claude -p`.
  - Exercice : faire générer par Claude un petit module Python (courbe EIOPA + interpolation Smith-Wilson) avec tests.

## Phase 2 — Configurer Claude Code (2 journées)
- [x] **M03 Mémoire** : hiérarchie `CLAUDE.md` (user `~/.claude/CLAUDE.md` > projet > sous-dossier), `CLAUDE.local.md`, imports `@fichier`.
  - Livrable : `~/.claude/CLAUDE.md` perso (préférences globales) + enrichir celui du repo.
- [x] **M04 Settings, permissions, hooks** : `settings.json` (user/projet/local), règles allow/ask/deny, variables d'env, statusline. Hooks : `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SessionStart`…
  - Exercice : hook `PostToolUse` qui lance `ruff format` sur chaque fichier .py édité ; hook `PreToolUse` qui bloque toute écriture dans `data/`.
- [x] **M05 Slash commands & subagents** : commandes custom (`.claude/commands/*.md`, `$ARGUMENTS`), subagents (`.claude/agents/*.md` : description, tools, model), quand déléguer vs. garder en contexte principal.
  - Livrables : `/review-actuariel` (commande) + subagent `model-validator` (relit un modèle, outils lecture seule).

## Phase 3 — Skills & MCP (2–3 journées) ← cœur du sujet
- [x] **M06 Skills** : structure `SKILL.md` (frontmatter `name`/`description` + corps), scripts et ressources annexes, chargement progressif (seule la description est en contexte jusqu'au déclenchement), scopes (perso `~/.claude/skills`, projet `.claude/skills`, plugin). Skills sur claude.ai et via l'API.
  - Livrables : skill `ifrs9-ecl` (méthodo + script Python de calcul ECL), skill `sii-reporting-qrt` (checklist + templates).
  - Tester le déclenchement : la `description` fait tout — la réécrire jusqu'à ce que le skill se charge au bon moment.
- [x] **M07 MCP (Model Context Protocol)** : architecture client/serveur, transports (stdio, HTTP streamable), primitives (tools, resources, prompts), scopes (`local`, `project` → `.mcp.json`, `user`), `claude mcp add|list|remove`, `/mcp`, authentification OAuth, sécurité (prompt injection via données d'outils).
  - Exercice 1 : brancher des serveurs existants (GitHub ✅, filesystem, BigQuery/GCP).
  - Exercice 2 : écrire son serveur MCP en Python (SDK `mcp` / FastMCP) exposant 2 outils : lecture d'un Parquet DVC, calcul de duration/convexité d'un portefeuille.
  - Livrable : `modules/07-mcp/server/` + entrée dans `.mcp.json`.
- [x] **M08 Plugins** : packager commandes + agents + skills + hooks + MCP dans un plugin, marketplaces, installation `/plugin`.
  - Livrable : plugin `actuariat-toolkit` regroupant M05–M07.

## Phase 4 — Programmatique (2 journées)
- [x] **M09 API & Agent SDK** : Messages API, tool use (boucle manuelle puis tool runner), extended thinking, prompt caching, Batch API, Files API, structured outputs. Claude Agent SDK (Python) : même moteur que Claude Code, embarqué dans ton code.
  - Exercice : agent Python qui lit un bilan (CSV), appelle ton serveur MCP, rédige une note ALM. Mesurer coût/latence avec et sans cache.
- [x] **M10 Automatisation / CI** : `claude -p` en script, sortie JSON, GitHub Actions (`@claude` sur PR), déploiement d'un agent sur Cloud Run (secret API via Secret Manager).
  - Livrable : workflow GitHub Actions de revue auto + service Cloud Run minimal.

## Phase 5 — Projet final (2–3 journées)
- [x] **M11** Assistant ALM de bout en bout : skill méthodo + MCP données (BigQuery/Parquet) + subagent de validation + hooks qualité + UI Streamlit ou commande Claude Code. Démo + README d'architecture.

## Veille continue (15 min/semaine)
- [ ] Changelog Claude Code, release notes API, blog Anthropic (anthropic.com/news), spec MCP (modelcontextprotocol.io). *(chaque vendredi — mode d'emploi : [notes/veille/README.md](notes/veille/README.md), commande `/veille`)*
- [x] Consigner dans `notes/veille/AAAA-MM.md` (thèmes : IA, tech/plateformes data, assurance/actuariat).

## Ressources
- https://docs.claude.com — API, prompt engineering, Agent SDK, skills
- https://code.claude.com/docs — Claude Code (settings, hooks, skills, subagents, MCP, plugins)
- https://modelcontextprotocol.io — spécification et SDKs MCP
- https://github.com/anthropics/skills — exemples de skills officiels
