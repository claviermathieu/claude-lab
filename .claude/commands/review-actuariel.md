---
description: Revue actuarielle d'un livrable (code, note de calcul) par le subagent model-validator
argument-hint: <chemin du fichier ou dossier à relire> [focus éventuel]
---

Lance une revue actuarielle indépendante de : $ARGUMENTS

1. Délègue la relecture au subagent `model-validator` en lui transmettant le chemin et le focus éventuel. Ne relis pas le livrable toi-même dans le contexte principal : l'intérêt est d'avoir un regard indépendant et de garder ce contexte léger.
2. Si le livrable contient du code Python testé, lance `uv run pytest -q` sur le dossier concerné et joins le résultat (réussite / échecs).
3. Restitue le rapport du valideur tel quel, puis ajoute une section **Suites proposées** : les 3 actions prioritaires, dans l'ordre, chacune en une ligne.
