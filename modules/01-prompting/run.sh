#!/usr/bin/env bash
# Lance chaque version de prompt sur la note SCR via Claude Code en mode headless.
# Usage : ./run.sh [modele]   (défaut : sonnet)
set -euo pipefail
cd "$(dirname "$0")"
MODEL="${1:-sonnet}"
mkdir -p resultats

for prompt in prompts/v*.md; do
  name="$(basename "$prompt" .md)"
  out="resultats/${name}-${MODEL}.md"
  python3 - "$prompt" cas/note-scr-marche.md > /tmp/claude-lab-prompt.txt <<'PY'
import sys
tpl, note = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
print(tpl.replace("{{NOTE}}", note))
PY
  echo "→ $name ($MODEL)"
  # Aucun outil autorisé : on teste le prompt seul, pas la capacité à lire des fichiers.
  claude -p --model "$MODEL" --tools "" < /tmp/claude-lab-prompt.txt > "$out"
done
echo "Résultats dans resultats/ — noter avec cas/corrige.md"
