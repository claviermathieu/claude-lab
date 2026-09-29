# M00 — État de l'art (septembre 2026)

**Objectif** : savoir quel modèle choisir, pour quoi, à quel prix, et maîtriser le vocabulaire (contexte, reasoning, tool use, agents, RAG/MCP, cache, batch).

> Sources : skill `claude-api` de Claude Code (table modèles datée du 2026-09-25) + docs.claude.com. Les prix concurrents ne sont pas chiffrés ici : trop volatils, à vérifier sur leurs pages tarifs avant toute décision.

## 1. Gamme Claude actuelle

| Modèle | ID API | Contexte | Sortie max | $ / 1M in | $ / 1M out | Positionnement |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 1M | 128K | 10 | 50 | Tier le plus capable diffusé largement. Raisonnement long, agents longue durée. Thinking toujours actif. |
| Claude Mythos 5.1 | `claude-mythos-5-1` | 1M | 128K | 10 | 50 | Même capacité que Fable 5.1, accès restreint (Project Glasswing). Hors périmètre pour nous. |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | 128K | 4 | 20 | **Défaut** : meilleur rapport intelligence/prix. Code, analyse, agents. |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M | 128K | 2 | 10 | Rapide et solide : code quotidien, agents, gros volumes. |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | — | 1 | 5 | Petit et rapide : classification, extraction, sous-agents simples. |

Générations précédentes encore servies : Opus 5 / 4.8 / 4.7 / 4.6, Sonnet 5 / 4.6, Fable 5. Pas d'intérêt à les choisir pour du neuf.

### Points d'attention API (drift récent)
- **Thinking** : plus de `budget_tokens` sur les modèles 5.x (erreur 400). On utilise `thinking: {type: "adaptive"}` et on règle la profondeur avec `output_config.effort` (`low` → `max`). Sur Opus 5.5 le thinking ne se désactive pas ; effort par défaut `medium` → le fixer explicitement.
- **Pas de prefill** assistant sur les modèles récents → utiliser les *structured outputs* (`output_config.format`).
- **`tool_choice` forcé (`any`/`tool`) refusé** sur Opus 5.5 / Sonnet 5.5 / Fable 5.1 → `auto` + consigne + `strict: true`.
- **Refus** : vérifier `stop_reason == "refusal"` avant de lire la réponse ; paramètre `fallbacks` côté serveur disponible.

## 2. Concurrents (repères qualitatifs)

| Acteur | Gamme | Quand y penser |
|---|---|---|
| OpenAI | Série GPT-5.x + modèles de raisonnement | Écosystème Azure OpenAI, outils déjà en place. |
| Google | Gemini 2.x/3.x (Pro, Flash) | Intégration GCP/Vertex native, très long contexte, multimodal vidéo. |
| Open-weights | Llama, Mistral, Qwen, DeepSeek | Données qui ne doivent pas sortir (on-prem), coût marginal nul à l'échelle, fine-tuning. |

Claude est aussi disponible sur **Vertex AI** (utile côté GCP : auth ADC, pas de clé Anthropic), Bedrock et Foundry — mêmes IDs de modèle sur Vertex.

## 3. Concepts à rafraîchir

| Concept | En une phrase | Ce qu'il faut retenir |
|---|---|---|
| **Fenêtre de contexte** | Nombre max de tokens (entrée + historique) que le modèle voit. | 1M aujourd'hui, mais la qualité baisse si on y déverse tout. |
| **Context engineering** | Choisir *ce qui entre* dans le contexte et quand. | CLAUDE.md, skills chargés à la demande, sous-agents qui résument, compaction. C'est le vrai levier, plus que la taille brute. |
| **Reasoning / extended thinking** | Le modèle « réfléchit » avant de répondre (tokens facturés en sortie). | Adaptive + effort. `high`/`xhigh` pour code et agents, `low` pour tâches simples. |
| **Tool use** | Le modèle émet un appel d'outil structuré (JSON), le code l'exécute et renvoie le résultat. | Base de tout agent. Outils client (tes fonctions) vs outils serveur (web search, code execution). |
| **Agent** | Boucle modèle → outil → résultat → modèle jusqu'à la fin de la tâche. | 4 façons : boucle manuelle, Tool Runner SDK, Agent SDK (= moteur Claude Code), Managed Agents (hébergé). |
| **RAG** | Récupérer des passages pertinents (recherche vectorielle/lexicale) et les injecter dans le prompt. | Pour de gros corpus documentaires statiques. |
| **MCP** | Protocole standard pour brancher des outils/données à un client LLM (serveur ↔ client). | Pas un concurrent du RAG : MCP est la *plomberie* (un serveur MCP peut faire du RAG, interroger BigQuery, GitHub…). |
| **Prompt caching** | Réutiliser un préfixe de prompt déjà calculé. | Lecture cache ≈ 5 % du prix d'entrée (Opus 5.5 : 0,20 $/M). Le préfixe doit être **identique à l'octet près** : stable d'abord, variable ensuite. |
| **Batch API** | Envoi asynchrone de lots de requêtes. | −50 % sur le prix, résultat sous 24 h. Idéal pour du reporting non urgent. |

## 4. Choisir un modèle par cas d'usage

| Cas d'usage | Modèle | Effort | Remarques |
|---|---|---|---|
| Développement dans Claude Code (quotidien) | Opus 5.5 | `high`/`xhigh` | Défaut Claude Code. |
| Revue d'un modèle actuariel / note technique complexe | Opus 5.5 | `high` | Passer à Fable 5.1 si l'enjeu justifie ×2,5 le coût. |
| Problème de raisonnement très difficile, agent de plusieurs heures | Fable 5.1 | `high`+ | Tours longs : streaming obligatoire. |
| Chatbot interne, Q&A sur doc, génération de code standard | Sonnet 5.5 | `medium` | Deux fois moins cher qu'Opus. |
| Extraction/classification en masse (ex. libellés comptables) | Haiku 4.5 | — | + Batch API (−50 %) si non urgent. |
| Sous-agent de lecture / recherche dans le code | Haiku 4.5 ou Sonnet 5.5 | `low` | Garde le contexte principal propre. |
| Reporting réglementaire mensuel généré en lot | Sonnet 5.5 + Batch | `medium` | Cache sur les instructions communes. |
| Données confidentielles ne pouvant sortir du SI | Open-weights on-prem, ou Claude via Vertex (région EU) | — | Vérifier le cadre contractuel avant tout. |

**Règle pratique** : commencer par Opus 5.5 à effort moyen ; descendre en effort avant de descendre en modèle ; mesurer le coût *par tâche réussie*, pas par requête.

## Exercices
- [x] Fiche 1 page + tableau de choix.
- [ ] Vérifier les prix concurrents du mois et compléter la section 2.
- [ ] Appeler `client.models.list()` (Models API) pour confirmer contextes et capacités en direct (fait en M09).
