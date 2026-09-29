#!/usr/bin/env bash
# Génère plugins/actuariat-toolkit/ depuis la config réelle du repo (source unique de vérité).
# Usage : plugins/build.sh   puis   claude plugin validate plugins/actuariat-toolkit
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/plugins/actuariat-toolkit"
VERSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$OUT/.claude-plugin/plugin.json")"

# On repart de zéro, sauf le manifeste (versionné à la main).
find "$OUT" -mindepth 1 -maxdepth 1 ! -name .claude-plugin -exec rm -rf {} +

mkdir -p "$OUT"/{commands,agents,skills,hooks,servers/alm_data}
cp "$ROOT"/.claude/commands/*.md "$OUT/commands/"
cp "$ROOT"/.claude/agents/*.md "$OUT/agents/"
cp -R "$ROOT"/.claude/skills/* "$OUT/skills/"
cp "$ROOT"/.claude/hooks/*.py "$OUT/hooks/"
find "$OUT" -name __pycache__ -type d -prune -exec rm -rf {} +

# Serveur MCP : dépendances déclarées en en-tête PEP 723 pour `uv run --script`.
{
  cat <<'PY'
# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp>=2.2", "numpy>=2.0", "pandas>=2.2", "pyarrow>=15"]
# ///
PY
  cat "$ROOT/modules/07-mcp/server/server.py"
} > "$OUT/servers/alm_data/server.py"

cat > "$OUT/hooks/hooks.json" <<'JSON'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|NotebookEdit|Bash",
        "hooks": [{ "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/protect_data.py\"", "timeout": 10 }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/ruff_format.py\"", "timeout": 30 },
          { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/check_note_alm.py\"", "timeout": 10 }
        ]
      }
    ]
  }
}
JSON

cat > "$OUT/.mcp.json" <<'JSON'
{
  "mcpServers": {
    "alm-data": {
      "command": "uv",
      "args": ["run", "--quiet", "--script", "${CLAUDE_PLUGIN_ROOT}/servers/alm_data/server.py"],
      "env": { "ALM_DATA_DIR": "${ALM_DATA_DIR:-./data}" }
    }
  }
}
JSON

cat > "$OUT/README.md" <<EOF
# actuariat-toolkit v$VERSION

> Généré par \`plugins/build.sh\` depuis \`.claude/\` et \`modules/07-mcp/server/\` — ne pas éditer ici.

| Composant | Contenu |
|---|---|
| Commandes | \`/review-actuariel <chemin>\`, \`/note-alm [taux]\` |
| Subagent | \`model-validator\` (lecture seule, Opus) |
| Skills | $(ls "$OUT/skills" | sed 's/^/`/; s/$/`/' | paste -sd, - | sed 's/,/, /g') |
| Hooks | protection de \`data/\` (PreToolUse), \`ruff format\` des .py et contrôle des notes ALM (PostToolUse) |
| MCP | \`alm-data\` (stdio, \`uv run --script\`) — données dans \`\$ALM_DATA_DIR\` ou \`./data\` |

Prérequis : \`uv\` et \`python3\` dans le PATH ; \`ruff\` (dans \`.venv\` du projet ou global) pour le hook de format.

Installation :
\`\`\`bash
claude plugin marketplace add claviermathieu/claude-lab   # ou un chemin local vers le repo
claude plugin install actuariat-toolkit@claude-lab
\`\`\`
EOF

echo "Plugin généré dans $OUT (v$VERSION)"
