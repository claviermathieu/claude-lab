#!/usr/bin/env python3
"""Hook PreToolUse : interdit toute écriture dans <projet>/data/ (données de référence).

Couvre Write/Edit/MultiEdit/NotebookEdit via le chemin cible, et Bash en analysant
les cibles d'écriture de chaque commande (redirections, destination de cp/mv,
arguments de rm/touch/tee/mkdir, fichiers de sed -i, dvc add/remove).
Heuristique, pas une sandbox : `python -c "open('data/x','w')"` n'est pas détecté.
"""

import json
import os
import re
import shlex
import sys

event = json.load(sys.stdin)
tool = event.get("tool_name", "")
tool_input = event.get("tool_input") or {}
project = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
cwd = event.get("cwd") or project
data_dir = os.path.join(project, "data")

# Commandes dont tous les arguments (hors options) sont des cibles d'écriture.
ECRIT_TOUS = {"rm", "rmdir", "touch", "mkdir", "tee", "truncate", "chmod", "chown"}
# Commandes dont seul le dernier argument est la cible (source(s) → destination).
ECRIT_DERNIER = {"cp", "mv", "rsync", "ln", "install"}
SCRIPTS_AUTORISES = ("make_sample_data.py",)


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
    if not path or "$" in path:  # variable non résolue : on ne peut pas conclure
        return False
    full = os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))
    return full == data_dir or full.startswith(data_dir + os.sep)


def cibles_bash(commande: str) -> list[str]:
    """Chemins absolus susceptibles d'être écrits par une ligne de commande shell."""
    cibles, courant = [], cwd
    for segment in re.split(r"&&|\|\||[;|\n]", commande):
        # Redirections > et >> (hors 2>&1), y compris collées : >fichier
        brutes = re.findall(r"(?<![0-9&])>>?\s*([^\s;&|<>]+)", segment)
        try:
            mots = shlex.split(segment)
        except ValueError:
            mots = segment.split()
        while mots and (mots[0] == "sudo" or ("=" in mots[0] and not mots[0].startswith("-"))):
            mots = mots[1:]  # VAR=val commande … / sudo
        if mots:
            cmd = os.path.basename(mots[0])
            args = [m for m in mots[1:] if not m.startswith("-") and not m.startswith(">")]
            if cmd == "cd" and args and "$" not in args[0]:
                courant = os.path.join(courant, os.path.expanduser(args[0]))
            elif cmd in ECRIT_TOUS:
                brutes += args
            elif cmd in ECRIT_DERNIER and args:
                brutes.append(args[-1])
            elif cmd == "sed" and any(m.startswith("-i") for m in mots[1:]):
                brutes += args[1:]
            elif cmd == "dvc" and args[:1] and args[0] in {"add", "remove", "checkout", "pull"}:
                brutes += args[1:] or ["data"]
        cibles += [os.path.join(courant, os.path.expanduser(c)) for c in brutes if "$" not in c]
    return cibles


if tool in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
    path = tool_input.get("file_path") or tool_input.get("notebook_path", "")
    if in_data(path):
        deny(
            f"Écriture interdite dans data/ ({path}). Les données sont régénérées par script ; "
            "écris dans un autre dossier ou demande à l'utilisateur."
        )

if tool == "Bash":
    commande = tool_input.get("command", "")
    if not any(s in commande for s in SCRIPTS_AUTORISES):
        visees = [c for c in cibles_bash(commande) if in_data(c)]
        if visees:
            deny(f"Commande qui modifie data/ refusée par le hook protect_data : {visees}")
