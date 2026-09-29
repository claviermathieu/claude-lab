#!/usr/bin/env python3
"""Hook PreToolUse : interdit toute écriture dans data/ (données de référence).

Couvre Write/Edit/MultiEdit/NotebookEdit via le chemin cible, et Bash via une
détection simple des redirections et commandes d'écriture visant data/.
"""

import json
import os
import re
import sys

event = json.load(sys.stdin)
tool = event.get("tool_name", "")
tool_input = event.get("tool_input") or {}
project = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
data_dir = os.path.join(project, "data")


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def in_data(path: str) -> bool:
    if not path:
        return False
    full = os.path.realpath(os.path.join(project, os.path.expanduser(path)))
    return full == data_dir or full.startswith(data_dir + os.sep)


if tool in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
    path = tool_input.get("file_path") or tool_input.get("notebook_path", "")
    if in_data(path):
        deny(
            f"Écriture interdite dans data/ ({path}). Les données sont régénérées par script ; "
            "écris dans un autre dossier ou demande à l'utilisateur."
        )

if tool == "Bash":
    cmd = tool_input.get("command", "")
    # Redirection, tee, rm/mv/cp/touch… ciblant data/ (heuristique, pas une sandbox).
    pattern = r"(>>?|\btee\b|\brm\b|\bmv\b|\bcp\b|\btouch\b|\bsed\s+-i\b|\bdvc\s+(add|remove)\b)[^|;&]*\bdata/"
    if re.search(pattern, cmd) and "make_sample_data.py" not in cmd:
        deny("Commande qui modifie data/ refusée par le hook protect_data.")
