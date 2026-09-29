#!/usr/bin/env python3
"""Hook PostToolUse : contrôle qualité des notes ALM écrites dans notes/alm/.

Vérifie les titres obligatoires du modèle (skill note-alm), la citation des versions
DVC et l'absence de marqueurs de brouillon. En cas d'écart : exit 2, le message est
renvoyé à Claude qui doit corriger la note.
"""

import json
import os
import re
import sys

SECTIONS = [
    "## Synthèse",
    "## Données et hypothèses",
    "## Réconciliation des sources",
    "## Duration gap et sensibilités",
    "## Limites",
    "## Actions proposées",
    "## Validation",
]
BROUILLON = re.compile(r"\b(TODO|TBD|XXX|à compléter)\b", re.IGNORECASE)
DVC = re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{8,32}\b")  # hash, pas une date

event = json.load(sys.stdin)
path = (event.get("tool_input") or {}).get("file_path", "")
norm = path.replace(os.sep, "/")
if not re.search(r"(^|/)notes/alm/[^/]+\.md$", norm) or not os.path.isfile(path):
    sys.exit(0)

with open(path, encoding="utf-8") as f:
    texte = f.read()

problemes = []
positions = [texte.find(s) for s in SECTIONS]
manquantes = [SECTIONS[i] for i, p in enumerate(positions) if p < 0]
if manquantes:
    problemes.append(f"sections manquantes : {', '.join(manquantes)}")
elif positions != sorted(positions):
    problemes.append("sections dans le désordre (suivre le modèle du skill note-alm)")
if not DVC.search(texte):
    problemes.append("aucune version DVC (md5) citée pour les données")
if m := BROUILLON.search(texte):
    problemes.append(f"marqueur de brouillon trouvé : « {m.group(0)} »")
synthese = re.search(r"## Synthèse\n(.*?)\n## ", texte, re.DOTALL)
if synthese and len([ligne for ligne in synthese.group(1).splitlines() if ligne.strip()]) > 3:
    problemes.append("la synthèse dépasse 3 lignes")

if problemes:
    print(
        f"Note ALM non conforme ({path}) :\n- " + "\n- ".join(problemes) + "\nCorrige la note.",
        file=sys.stderr,
    )
    sys.exit(2)
