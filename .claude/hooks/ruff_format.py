#!/usr/bin/env python3
"""Hook PostToolUse : formate avec ruff chaque fichier .py écrit par Claude.

Entrée : JSON du hook sur stdin (tool_name, tool_input.file_path, …).
Ne bloque jamais : un échec de ruff est signalé à Claude mais n'annule pas l'édition.
"""

import json
import os
import shutil
import subprocess
import sys

event = json.load(sys.stdin)
path = (event.get("tool_input") or {}).get("file_path", "")
if not path.endswith(".py") or not os.path.isfile(path):
    sys.exit(0)

project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
ruff = os.path.join(project, ".venv", "bin", "ruff")
if not os.path.exists(ruff):
    ruff = shutil.which("ruff")
if not ruff:
    sys.exit(0)  # ruff absent : on ne gêne pas le travail

result = subprocess.run(
    [ruff, "format", "--quiet", path], capture_output=True, text=True, check=False
)
if result.returncode != 0:
    # Exit 2 en PostToolUse : stderr est renvoyé à Claude pour qu'il corrige.
    print(f"ruff format a échoué sur {path} :\n{result.stderr}", file=sys.stderr)
    sys.exit(2)
