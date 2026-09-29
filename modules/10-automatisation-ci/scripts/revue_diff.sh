#!/usr/bin/env bash
# Revue automatique d'un diff git par Claude Code en mode headless, sortie JSON exploitable.
# Usage : revue_diff.sh [ref_de_base] [modele]   (défaut : HEAD~1, sonnet)
# Code retour 2 si la revue contient au moins un constat « bloquant ».
set -euo pipefail
BASE="${1:-HEAD~1}"
MODEL="${2:-sonnet}"
cd "$(git rev-parse --show-toplevel)"

DIFF="$(git diff "$BASE" -- . ':(exclude)uv.lock' ':(exclude)plugins/')"
if [ -z "$DIFF" ]; then
  echo '{"statut": "rien à relire"}'
  exit 0
fi

SCHEMA='{"type":"object","properties":{"verdict":{"type":"string","enum":["ok","a_corriger","bloquant"]},"constats":{"type":"array","items":{"type":"object","properties":{"gravite":{"type":"string","enum":["bloquant","majeur","mineur"]},"fichier":{"type":"string"},"constat":{"type":"string"}},"required":["gravite","fichier","constat"]}}},"required":["verdict","constats"]}'

REPONSE="$(printf '%s' "$DIFF" | claude -p \
  "Relis ce diff (reçu sur stdin) comme un relecteur senior : bugs, erreurs de calcul actuariel, régressions, secrets. Ignore le style. Ne signale que ce que tu peux justifier. Tu peux lire les fichiers du repo pour le contexte." \
  --model "$MODEL" --output-format json --json-schema "$SCHEMA" \
  --allowedTools "Read,Grep,Glob")"

# Enveloppe JSON de claude -p : result/structured_output, total_cost_usd, duration_ms, session_id…
printf '%s' "$REPONSE" | python3 -c '
import json, sys
env = json.load(sys.stdin)
revue = env.get("structured_output") or json.loads(env["result"])
print(json.dumps({"revue": revue, "cout_usd": round(env["total_cost_usd"], 4),
                  "duree_s": round(env["duration_ms"] / 1000, 1)}, ensure_ascii=False, indent=2))
sys.exit(2 if revue["verdict"] == "bloquant" else 0)'
