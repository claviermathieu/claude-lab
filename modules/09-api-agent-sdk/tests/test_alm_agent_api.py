"""Tests hors ligne de la boucle manuelle : faux client API, vrai serveur MCP in-process."""

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest
from mcp import Client

ICI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ICI))
sys.path.insert(0, str(ICI.parent / "07-mcp" / "server"))

import alm_agent_api as agent
import server as srv


def usage(inp=100, out=50, cw=0, cr=0):
    return NS(
        input_tokens=inp,
        output_tokens=out,
        cache_creation_input_tokens=cw,
        cache_read_input_tokens=cr,
    )


def texte(t):
    return NS(type="text", text=t)


def appel(id_, nom, entree):
    return NS(type="tool_use", id=id_, name=nom, input=entree)


class FauxClient:
    """Rejoue une liste de réponses et mémorise les requêtes envoyées."""

    def __init__(self, reponses):
        self.reponses = list(reponses)
        self.requetes = []
        self.beta = NS(messages=NS(create=self._create))

    async def _create(self, **params):
        self.requetes.append(json.loads(json.dumps(params, default=repr)))
        return self.reponses.pop(0)


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    import pandas as pd

    pd.DataFrame({"annee": [1, 2], "flux": [0.0, 100.0]}).to_parquet(
        tmp_path / "flux_passif.parquet"
    )
    monkeypatch.setattr(srv, "DATA_DIR", tmp_path.resolve())
    return tmp_path


def lancer(reponses, cache=True):
    client = FauxClient(reponses)

    async def run():
        async with Client(srv.server) as mcp:
            outils = agent.outils_api((await mcp.list_tools()).tools)

            async def appeler(nom, entree):
                res = await mcp.call_tool(nom, entree)
                return res.content[0].text, bool(res.is_error)

            return await agent.executer_agent(client, appeler, outils, "cote,poste\n", cache)

    note, mesure = asyncio.run(run())
    return client, note, mesure


def test_boucle_complete_avec_appels_paralleles(data_dir):
    client, note, mesure = lancer(
        [
            NS(
                stop_reason="tool_use",
                usage=usage(cw=2000),
                content=[
                    appel("t1", "cashflow_duration", {"taux": 0.05}),
                    appel("t2", "read_dataset", {"nom": "absent.parquet"}),
                ],
            ),
            NS(stop_reason="end_turn", usage=usage(cr=2000, out=800), content=[texte("# Note")]),
        ]
    )
    assert note == "# Note"
    assert mesure.appels == 2 and mesure.outils == ["cashflow_duration", "read_dataset"]
    # Les deux résultats partent dans UN seul message utilisateur, erreur signalée.
    resultats = client.requetes[1]["messages"][-1]["content"]
    assert [r["tool_use_id"] for r in resultats] == ["t1", "t2"]
    assert json.loads(resultats[0]["content"])["duration_macaulay"] == pytest.approx(2)
    assert resultats[1]["is_error"] is True


def test_parametres_de_requete(data_dir):
    client, _, _ = lancer([NS(stop_reason="end_turn", usage=usage(), content=[texte("ok")])])
    req = client.requetes[0]
    assert req["model"] == "claude-opus-5-5"
    assert req["thinking"] == {"type": "adaptive"}
    assert req["fallbacks"] == "default"
    assert req["cache_control"] == {"type": "ephemeral"}
    assert [t["name"] for t in req["tools"]] == sorted(t["name"] for t in req["tools"])


def test_sans_cache(data_dir):
    client, _, _ = lancer(
        [NS(stop_reason="end_turn", usage=usage(), content=[texte("ok")])], cache=False
    )
    assert "cache_control" not in client.requetes[0]


def test_refus_leve_une_erreur(data_dir):
    # Levée dans le contexte du client MCP : anyio l'enveloppe dans un ExceptionGroup.
    with pytest.raises(BaseExceptionGroup) as exc:
        lancer([NS(stop_reason="refusal", stop_details="cyber", usage=usage(), content=[])])
    assert exc.group_contains(RuntimeError, match="refusée", depth=None)


def test_cout():
    m = agent.Mesure(input=1_000_000, output=100_000, cache_write=200_000, cache_read=1_000_000)
    assert m.cout_usd == pytest.approx(4.0 + 2.0 + 1.0 + 0.2)
