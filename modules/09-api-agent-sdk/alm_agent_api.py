"""Agent ALM — API Messages en boucle manuelle + outils du serveur MCP alm-data.

Lit un bilan (CSV), laisse Claude interroger le serveur MCP (durations actif/passif),
et produit une note ALM. Mesure tokens, coût et latence, avec ou sans prompt caching.

    uv run python modules/09-api-agent-sdk/alm_agent_api.py --runs 2            # avec cache
    uv run python modules/09-api-agent-sdk/alm_agent_api.py --runs 2 --no-cache

Nécessite des identifiants API (ANTHROPIC_API_KEY ou `ant auth login`).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import anthropic
from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parents[2]
MODEL = "claude-opus-5-5"
# $ / million de tokens, Claude Opus 5.5 (écriture cache 5 min = 1,25 × entrée).
PRIX = {"input": 4.00, "output": 20.00, "cache_write": 5.00, "cache_read": 0.20}
MAX_TOURS = 12

SYSTEM = """Tu es actuaire ALM senior dans un assureur vie français. Tu rédiges des notes \
ALM destinées au comité des risques : factuelles, chiffrées, avec les limites de l'analyse.

<methode>
1. Lis le bilan fourni : poids des classes d'actifs, fonds propres économiques (actif − passif).
2. Interroge les outils de données : duration et convexité du portefeuille obligataire, duration \
et valeur actuelle du passif (au taux indiqué ; à défaut 3 %).
3. Calcule le duration gap pondéré : D_A − D_P × (VA_P / VM_A), en précisant les assiettes \
utilisées (le portefeuille obligataire n'est qu'une partie de l'actif).
4. Estime l'impact d'un choc parallèle de ±100 pb sur les fonds propres économiques \
(au premier ordre puis avec convexité).
5. Conclus sur l'exposition au risque de taux et propose au plus 3 actions de pilotage.
</methode>

<regles>
- N'invente aucun chiffre : chaque montant vient du bilan ou d'un outil ; sinon écris \
« non disponible ».
- Montants en M€ avec une décimale, durations avec deux décimales.
- Signale les incohérences entre sources (ex. valeur du passif au bilan ≠ valeur actuelle des flux).
</regles>

<format>
# Note ALM — risque de taux
## Synthèse (3 lignes)
## Données et hypothèses
## Duration gap et sensibilités (tableau)
## Limites
## Actions proposées
</format>"""


@dataclass
class Mesure:
    appels: int = 0
    input: int = 0
    output: int = 0
    cache_write: int = 0
    cache_read: int = 0
    latence_s: float = 0.0
    outils: list[str] = field(default_factory=list)

    def ajouter(self, usage) -> None:
        self.appels += 1
        self.input += usage.input_tokens
        self.output += usage.output_tokens
        self.cache_write += usage.cache_creation_input_tokens or 0
        self.cache_read += usage.cache_read_input_tokens or 0

    @property
    def cout_usd(self) -> float:
        return (
            self.input * PRIX["input"]
            + self.output * PRIX["output"]
            + self.cache_write * PRIX["cache_write"]
            + self.cache_read * PRIX["cache_read"]
        ) / 1e6


def outils_api(outils_mcp) -> list[dict]:
    """Convertit les outils MCP au format de l'API Messages (ordre stable pour le cache)."""
    return [
        {"name": t.name, "description": t.description or "", "input_schema": t.input_schema}
        for t in sorted(outils_mcp, key=lambda t: t.name)
    ]


async def executer_agent(
    client, appeler_outil, outils: list[dict], bilan_csv: str, cache: bool, model: str = MODEL
) -> tuple[str, Mesure]:
    """Boucle manuelle : appel modèle → exécution des tool_use → résultats → … jusqu'à end_turn."""
    mesure = Mesure()
    messages = [
        {
            "role": "user",
            "content": f"Voici le bilan économique (M€) :\n\n<bilan>\n{bilan_csv}</bilan>\n\n"
            "Rédige la note ALM sur le risque de taux.",
        }
    ]
    params = {
        "model": model,
        "max_tokens": 16000,
        "system": SYSTEM,
        "tools": outils,
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": "high"},
        # Si un classifieur de sécurité refuse, l'API relance sur un modèle de repli.
        "betas": ["server-side-fallback-2026-07-01"],
        "fallbacks": "default",
    }
    if cache:
        # Cache automatique du dernier bloc : chaque tour relit le préfixe du tour précédent.
        params["cache_control"] = {"type": "ephemeral"}

    debut = time.perf_counter()
    for _ in range(MAX_TOURS):
        reponse = await client.beta.messages.create(messages=messages, **params)
        mesure.ajouter(reponse.usage)
        if reponse.stop_reason == "refusal":
            raise RuntimeError(f"requête refusée : {reponse.stop_details}")
        if reponse.stop_reason == "max_tokens":
            raise RuntimeError("réponse tronquée (max_tokens)")
        messages.append({"role": "assistant", "content": reponse.content})
        appels = [b for b in reponse.content if b.type == "tool_use"]
        if reponse.stop_reason != "tool_use" or not appels:
            break
        resultats = []
        for bloc in appels:  # tous les résultats dans UN message utilisateur
            mesure.outils.append(bloc.name)
            texte, erreur = await appeler_outil(bloc.name, bloc.input)
            resultats.append(
                {
                    "type": "tool_result",
                    "tool_use_id": bloc.id,
                    "content": texte,
                    "is_error": erreur,
                }
            )
        messages.append({"role": "user", "content": resultats})
    else:
        raise RuntimeError(f"pas de réponse finale après {MAX_TOURS} tours")
    mesure.latence_s = time.perf_counter() - debut
    note = "\n".join(b.text for b in reponse.content if b.type == "text")
    return note, mesure


async def main_async(args) -> None:
    serveur = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "modules/07-mcp/server/server.py")],
        env={"ALM_DATA_DIR": str(args.data_dir)},
    )
    bilan = (args.data_dir / "bilan.csv").read_text()
    client = anthropic.AsyncAnthropic()
    async with Client(serveur) as mcp:
        outils = outils_api((await mcp.list_tools()).tools)

        async def appeler_outil(nom: str, entree: dict) -> tuple[str, bool]:
            res = await mcp.call_tool(nom, entree)
            return "\n".join(c.text for c in res.content if c.type == "text"), bool(res.is_error)

        for i in range(1, args.runs + 1):
            note, m = await executer_agent(client, appeler_outil, outils, bilan, not args.no_cache)
            print(
                json.dumps(
                    {
                        "run": i,
                        "cache": not args.no_cache,
                        "appels_api": m.appels,
                        "outils": m.outils,
                        "tokens": {
                            "input": m.input,
                            "output": m.output,
                            "cache_write": m.cache_write,
                            "cache_read": m.cache_read,
                        },
                        "cout_usd": round(m.cout_usd, 4),
                        "latence_s": round(m.latence_s, 1),
                    },
                    ensure_ascii=False,
                )
            )
    if args.sortie:
        Path(args.sortie).write_text(note)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--runs", type=int, default=2, choices=range(1, 11), metavar="1-10")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--data-dir", type=Path, default=ROOT / "data")
    p.add_argument("--sortie", help="fichier où écrire la dernière note")
    asyncio.run(main_async(p.parse_args()))


if __name__ == "__main__":
    main()
