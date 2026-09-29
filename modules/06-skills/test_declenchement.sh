#!/usr/bin/env bash
# Vérifie quels skills Claude charge (outil Skill) pour une série de prompts.
# Usage : ./test_declenchement.sh [modele]   — sortie : prompt → skills chargés
set -euo pipefail
cd "$(dirname "$0")/../.."
MODEL="${1:-sonnet}"

declare -a PROMPTS=(
  "ifrs9-ecl|Un prêt conso de 10 000 € (LGD 60 %, TIE 7 %, maturité 3 ans) a 45 jours d'impayés. Quel stage et quel ordre de grandeur de provision IFRS 9 avec une PD annuelle de 3 % ?"
  "sii-reporting-qrt|Avant la remise annuelle, quels contrôles de cohérence dois-je faire entre le bilan S.02.01 et les fonds propres S.23.01 ?"
  "scr-marche|Mon SCR taux retient le choc à la baisse. Quelle corrélation dois-je mettre entre taux et actions dans l'agrégation du SCR marché ?"
  "aucun|Quelle est la différence entre duration de Macaulay et duration modifiée ? Réponds en 3 lignes."
)

for entry in "${PROMPTS[@]}"; do
  attendu="${entry%%|*}"
  prompt="${entry#*|}"
  charges=$(claude -p "$prompt" --model "$MODEL" --output-format stream-json --verbose \
      --allowedTools "Skill,Read,Bash(python3:*)" 2>/dev/null |
    python3 -c '
import json, sys
noms = []
for ligne in sys.stdin:
    try:
        ev = json.loads(ligne)
    except ValueError:
        continue
    for bloc in (ev.get("message") or {}).get("content") or []:
        if isinstance(bloc, dict) and bloc.get("type") == "tool_use" and bloc.get("name") == "Skill":
            noms.append(bloc["input"].get("skill") or bloc["input"].get("command"))
print(",".join(noms) or "aucun")')
  statut=$([ "$charges" = "$attendu" ] && echo OK || echo KO)
  printf '[%s] attendu=%-18s chargé=%s\n' "$statut" "$attendu" "$charges"
done
