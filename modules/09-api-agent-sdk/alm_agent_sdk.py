"""Agent ALM — Claude Agent SDK (moteur de Claude Code embarqué dans du Python).

Même tâche que alm_agent_api.py, mais la boucle, l'appel des outils MCP et la gestion
du contexte sont faits par le SDK. Utilise l'authentification de Claude Code (abonnement
ou clé API). Mesure coût, tokens de cache et latence sur plusieurs exécutions.

    uv run python modules/09-api-agent-sdk/alm_agent_sdk.py --runs 2 --sortie note.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, query
from claude_agent_sdk.types import ToolUseBlock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from alm_agent_api import SYSTEM  # même consigne pour comparer les deux approches

ROOT = Path(__file__).resolve().parents[2]
OUTILS_MCP = [
    "mcp__alm-data__list_datasets",
    "mcp__alm-data__read_dataset",
    "mcp__alm-data__portfolio_duration_convexity",
    "mcp__alm-data__cashflow_duration",
]


async def executer(data_dir: Path, model: str, cache: bool = True) -> tuple[str, dict]:
    options = ClaudeAgentOptions(
        model=model,
        system_prompt=SYSTEM,
        mcp_servers={
            "alm-data": {
                "type": "stdio",
                "command": sys.executable,
                "args": [str(ROOT / "modules/07-mcp/server/server.py")],
                "env": {"ALM_DATA_DIR": str(data_dir)},
            }
        },
        strict_mcp_config=True,  # ignore .mcp.json et les connecteurs du compte
        setting_sources=[],  # ni CLAUDE.md, ni settings, ni skills du projet : agent isolé
        tools=[],  # aucun outil intégré (Bash, Read…) : seulement les outils MCP
        allowed_tools=OUTILS_MCP,
        max_turns=12,
        cwd=str(ROOT),
        env={} if cache else {"DISABLE_PROMPT_CACHING": "1"},
    )
    bilan = (data_dir / "bilan.csv").read_text()
    prompt = (
        f"Voici le bilan économique (M€) :\n\n<bilan>\n{bilan}</bilan>\n\n"
        "Rédige la note ALM sur le risque de taux."
    )
    outils, resultat = [], None
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            outils += [b.name for b in message.content if isinstance(b, ToolUseBlock)]
        elif isinstance(message, ResultMessage):
            resultat = message
    if resultat is None or resultat.is_error:
        raise RuntimeError(f"échec de l'agent : {resultat and resultat.errors}")
    u = resultat.usage or {}
    mesure = {
        "tours": resultat.num_turns,
        "outils": outils,
        "tokens": {
            "input": u.get("input_tokens"),
            "output": u.get("output_tokens"),
            "cache_write": u.get("cache_creation_input_tokens"),
            "cache_read": u.get("cache_read_input_tokens"),
        },
        "cout_usd": round(resultat.total_cost_usd or 0, 4),
        "latence_s": round(resultat.duration_ms / 1000, 1),
        "latence_api_s": round(resultat.duration_api_ms / 1000, 1),
    }
    return resultat.result or "", mesure


async def main_async(args) -> None:
    for i in range(1, args.runs + 1):
        note, mesure = await executer(args.data_dir, args.model, not args.no_cache)
        print(json.dumps({"run": i, "cache": not args.no_cache, **mesure}, ensure_ascii=False))
    if args.sortie:
        Path(args.sortie).write_text(note)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--runs", type=int, default=2, choices=range(1, 11), metavar="1-10")
    p.add_argument("--model", default="claude-opus-5-5")
    p.add_argument("--data-dir", type=Path, default=ROOT / "data")
    p.add_argument("--no-cache", action="store_true", help="DISABLE_PROMPT_CACHING=1")
    p.add_argument("--sortie")
    asyncio.run(main_async(p.parse_args()))


if __name__ == "__main__":
    main()
