# M05 — Slash commands & subagents

**Objectif** : empaqueter des prompts récurrents en commandes, et déléguer des tâches à des agents spécialisés avec leur propre contexte et leurs propres outils.

## Commandes custom
- Fichier Markdown dans `.claude/commands/<nom>.md` (projet) ou `~/.claude/commands/` (perso) → `/nom`.
- Frontmatter optionnel : `description`, `argument-hint`, `allowed-tools`, `model`.
- Variables : `$ARGUMENTS` (tout), `$1`, `$2`… (positionnels). `!`commande`` injecte la sortie d'une commande shell, `@fichier` injecte un fichier.
- Les commandes et les skills sont désormais unifiés : une commande est un skill déclenché explicitement (elle apparaît dans la liste des skills). Pour du déclenchement **automatique** selon le contexte → skill (M06).

## Subagents
- Fichier `.claude/agents/<nom>.md` : frontmatter `name`, `description` (quand l'utiliser — c'est ce que lit l'agent principal pour décider de déléguer), `tools` (liste blanche), `model` (`opus`, `sonnet`, `haiku`, `inherit`), puis le prompt système.
- Contexte **séparé** : le subagent part d'un contexte vierge, lit ce qu'il veut, et ne renvoie qu'un résumé. Le contexte principal reste léger.
- `/agents` pour les gérer interactivement.

### Déléguer ou garder en contexte principal ?
| Déléguer à un subagent | Garder dans le contexte principal |
|---|---|
| Lecture volumineuse dont seul le résumé compte (explorer un repo, relire un module) | Tâche courte, ou qui s'appuie sur l'échange en cours |
| Regard indépendant (validation, revue) | Modifications itératives avec l'utilisateur |
| Besoin d'outils restreints (lecture seule) ou d'un autre modèle | Quand le résumé perdrait des détails indispensables |
| Travaux parallélisables | |

Coût : un subagent relit tout depuis zéro ; c'est rentable quand il évite de polluer le contexte principal, pas pour une tâche de 30 secondes.

## Livrables
- **[`/review-actuariel`](../../.claude/commands/review-actuariel.md)** : délègue à `model-validator`, lance les tests, puis restitue le rapport et les 3 actions prioritaires.
- **[`model-validator`](../../.claude/agents/model-validator.md)** : outils `Read, Grep, Glob` uniquement, modèle Opus, méthode en 5 étapes, format de rapport imposé (verdict, constats avec gravité et `fichier:ligne`, tests manquants, points non vérifiés).

## Démo : revue du module Smith-Wilson (M02)
```bash
claude -p "/review-actuariel modules/02-claude-code-bases/eiopa_curve" --model sonnet --output-format json \
  --allowedTools "Agent,Read,Grep,Glob,Bash(uv run pytest:*)"
```
Rapport : [demo/review-eiopa-curve.md](demo/review-eiopa-curve.md). Agent principal Sonnet 5.5 + subagent Opus 5.5 · 4 tours · 126 s · **0,54 $**.

Résultat : « validé avec réserves », 3 constats majeurs (CRA à 0 par défaut, taux zéro-coupon au lieu de swaps au pair, méthode LLFR 2027 non couverte) et 5 mineurs. Les constats sur la stabilité numérique et la validation des entrées ont été corrigés dans la foulée (commit `module-02: stabilise…`), les autres documentés dans le README de M02.

Observations :
- Le valideur signale lui-même que `.claude/skills/` est vide et que ses références viennent de sa mémoire → motive le skill de référence de M06.
- L'agent principal a relancé les tests dans le bon dossier après un premier `pytest` qui n'en collectait aucun : la consigne « joindre le résultat » force la vérification.

## Exercices
- [x] Commande `/review-actuariel`.
- [x] Subagent `model-validator` (lecture seule).
- [x] Démo headless sur un vrai module + corrections.
- [ ] Subagent `haiku` d'exploration (« où est calculé X ? ») et comparer coût/qualité avec l'agent Explore intégré.
