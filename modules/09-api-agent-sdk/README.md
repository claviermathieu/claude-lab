# M09 — API & Agent SDK

**Objectif** : piloter Claude depuis du code, d'abord « à la main » (API Messages), puis avec le moteur de Claude Code embarqué (Agent SDK), et mesurer coût/latence.

## Repères API (état septembre 2026, source : skill `claude-api` de Claude Code)

| Sujet | À retenir |
|---|---|
| Endpoint | Tout passe par `POST /v1/messages` ; outils, thinking, formats de sortie sont des paramètres de cette requête. |
| Modèle par défaut | `claude-opus-5-5` (4 $ / 20 $ par M tokens) ; `claude-sonnet-5-5` (2 / 10) ; `claude-haiku-4-5` (1 / 5). |
| Thinking | `thinking: {type: "adaptive"}` + `output_config: {effort: low…max}`. **`budget_tokens` → 400** sur les modèles 5.x. Opus 5.5 : thinking non désactivable, effort par défaut `medium`. |
| Tool use | Boucle : `stop_reason == "tool_use"` → exécuter **tous** les `tool_use` → renvoyer **tous** les `tool_result` dans **un** message utilisateur (`is_error: true` en cas d'échec). `tool_choice` forcé (`any`/`tool`) → 400 sur Opus 5.5 / Sonnet 5.5. |
| Tool Runner | `client.beta.messages.tool_runner(...)` + `@beta_tool` : le SDK fait la boucle. Recommandé ; la boucle manuelle sert à comprendre ou à tout contrôler. |
| Prompt caching | Correspondance de **préfixe** (outils → system → messages). `cache_control={"type": "ephemeral"}` au niveau requête = cache automatique du dernier bloc. Écriture 1,25 × le prix d'entrée, lecture ≈ 5 % (Opus 5.5 : 0,20 $/M). Vérifier `usage.cache_read_input_tokens`. |
| Batch API | `client.messages.batches.create(...)` : −50 %, asynchrone (≤ 24 h), résultats à rapprocher par `custom_id`. |
| Files API | `client.files.upload(...)` (sorti de beta) puis référence par `file_id`. |
| Structured outputs | `output_config: {format: …}` ou `client.messages.parse(...)` avec Pydantic ; `strict: true` sur un outil. Pas de prefill. |
| Refus | Vérifier `stop_reason == "refusal"` avant de lire `content` ; `fallbacks: "default"` (beta `server-side-fallback-2026-07-01`) relance côté serveur sur un modèle de repli. |

## Exercice : agent ALM (bilan CSV → MCP `alm-data` → note)

### 1. Boucle manuelle — [alm_agent_api.py](alm_agent_api.py)
SDK `anthropic` 1.9 (async) + client MCP `mcp` 2.2 (`Client(StdioServerParameters)`) : les outils MCP sont convertis au format API (triés par nom → préfixe stable pour le cache), la boucle exécute les appels et renvoie les résultats groupés. Adaptive thinking, effort `high`, `fallbacks: "default"`, arrêt sur `refusal`/`max_tokens`, cache activable (`--no-cache`), mesure tokens / coût / latence par exécution.

⚠️ **Non exécuté** : aucune clé API sur ce poste (`ANTHROPIC_API_KEY` absent, CLI `ant` non installée). La logique est couverte par [tests/test_alm_agent_api.py](tests/test_alm_agent_api.py) : faux client API rejouant des réponses + vrai serveur MCP in-process (appels parallèles regroupés, erreur d'outil propagée en `is_error`, paramètres de requête, refus, calcul de coût). Pour l'exécuter :
```bash
export ANTHROPIC_API_KEY=…   # ou : ant auth login
uv run python modules/09-api-agent-sdk/alm_agent_api.py --runs 2
uv run python modules/09-api-agent-sdk/alm_agent_api.py --runs 2 --no-cache
```

### 2. Claude Agent SDK — [alm_agent_sdk.py](alm_agent_sdk.py)
`claude_agent_sdk.query(prompt, ClaudeAgentOptions(...))` : même consigne système, serveur `alm-data` déclaré dans `mcp_servers`, agent isolé (`setting_sources=[]`, `strict_mcp_config=True`, `tools=[]` → uniquement les 4 outils MCP autorisés). Le SDK pilote le binaire Claude Code et **utilise son authentification** : il tourne ici sans clé API.

### Mesures réelles (Agent SDK, Opus 5.5, 29/09/2026)

| Exécution | Cache | Tours | Tokens entrée non cachés | Écriture cache | Lecture cache | Sortie | Coût | Latence |
|---|---|---|---|---|---|---|---|---|
| 1 (à froid) | oui | 5 | 6 | 7 076 | 9 060 | 4 984 | 0,159 $ | 47 s |
| 2 (à chaud) | oui | 5 | 6 | 476 | 15 656 | 6 019 | 0,128 $ | 57 s |
| 3 | **non** (`DISABLE_PROMPT_CACHING=1`) | 5 | 12 430 | 0 | 0 | 5 782 | 0,167 $ | 57 s |

Lecture :
- Côté **entrée**, le cache divise le coût par ~9 à chaud (≈ 0,006 $ contre 0,050 $), et même à froid chaque tour relit le préfixe du tour précédent (9 060 tokens lus dès la 1re exécution).
- Mais ici la **sortie domine** (5 000–6 000 tokens × 20 $/M ≈ 0,10–0,12 $) : l'économie totale n'est que de ~23 %. Le cache devient décisif quand le contexte est gros (documents, historique long) et la sortie courte.
- **Latence** : pas d'effet mesurable sur un prompt de ~15 k tokens ; elle suit la longueur de la sortie (47 s pour 5 k tokens, 57 s pour 6 k).
- Qualité : la note ([resultats/note-alm-agent-sdk.md](resultats/note-alm-agent-sdk.md)) respecte le format, cite les versions DVC et **signale l'incohérence** du jeu d'exemple (BE au bilan 805 M€ vs flux actualisés 659 M€), qui inverse le signe du duration gap.

## API ou Agent SDK ?
| API Messages (boucle ou Tool Runner) | Agent SDK |
|---|---|
| Contrôle total de chaque requête (paramètres, cache, coût) | Boucle, contexte, compaction, permissions, hooks, subagents fournis |
| Tes outils uniquement | Outils de Claude Code (fichiers, Bash, web) + MCP |
| Clé API, facturation à l'usage | Auth Claude Code (abonnement possible) ou clé API |
| Service en production, faible latence, volume | Agent qui travaille sur des fichiers / un repo, automatisation |

## Exercices
- [x] Boucle manuelle API + MCP (testée hors ligne).
- [x] Agent SDK + MCP, mesures coût/latence avec et sans cache.
- [ ] Exécuter `alm_agent_api.py` avec une clé API et comparer aux mesures de l'Agent SDK.
- [ ] Variante Tool Runner (`@beta_tool`), puis Batch API pour générer 10 notes (−50 %).
