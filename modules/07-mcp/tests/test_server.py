"""Tests du serveur MCP alm-data : calculs, sécurité des chemins, protocole (in-process et stdio)."""

import asyncio
import json
import sys
from pathlib import Path

import pandas as pd
import pytest
from mcp import Client, StdioServerParameters

SERVER_DIR = Path(__file__).resolve().parents[1] / "server"
sys.path.insert(0, str(SERVER_DIR))

import server as srv


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    pd.DataFrame(
        {
            "isin": ["ZC10", "PAIR5"],
            "nominal": [100.0, 100.0],
            "coupon": [0.0, 0.03],
            "maturite": [10.0, 5.0],
            "rendement": [0.03, 0.03],
        }
    ).to_parquet(tmp_path / "obligations.parquet")
    pd.DataFrame({"annee": [1, 2, 3], "flux": [0.0, 0.0, 100.0]}).to_parquet(
        tmp_path / "flux_passif.parquet"
    )
    (tmp_path / "obligations.parquet.dvc").write_text("outs:\n- md5: " + "a" * 32 + "\n")
    (tmp_path.parent / "secret.csv").write_text("x\n1\n")
    monkeypatch.setattr(srv, "DATA_DIR", tmp_path.resolve())
    return tmp_path


def appeler(outil: str, args: dict | None = None):
    async def run():
        async with Client(srv.server) as c:
            return await c.call_tool(outil, args or {})

    return asyncio.run(run())


def test_zero_coupon_duration_egale_maturite():
    ind = srv.indicateurs_obligation(100, 0.0, 10, 0.03)
    assert ind["duration_macaulay"] == pytest.approx(10)
    assert ind["prix"] == pytest.approx(100 / 1.03**10)
    assert ind["convexite"] == pytest.approx(10 * 11 / 1.03**2)


def test_obligation_au_pair():
    ind = srv.indicateurs_obligation(100, 0.03, 5, 0.03)
    assert ind["prix"] == pytest.approx(100)
    assert ind["duration_modifiee"] < ind["duration_macaulay"] < 5


def test_duration_et_convexite_par_differences_finies():
    h = 1e-4
    prix = {
        y: srv.indicateurs_obligation(100, 0.02, 20, y)["prix"] for y in (0.03 - h, 0.03, 0.03 + h)
    }
    ind = srv.indicateurs_obligation(100, 0.02, 20, 0.03)
    p0, pm, pp = prix[0.03], prix[0.03 - h], prix[0.03 + h]
    assert ind["duration_modifiee"] == pytest.approx((pm - pp) / (2 * h * p0), rel=1e-6)
    assert ind["convexite"] == pytest.approx((pp + pm - 2 * p0) / (p0 * h**2), rel=1e-4)


def test_outils_exposes(data_dir):
    async def run():
        async with Client(srv.server) as c:
            return {t.name for t in (await c.list_tools()).tools}

    assert asyncio.run(run()) == {
        "list_datasets",
        "read_dataset",
        "portfolio_duration_convexity",
        "cashflow_duration",
    }


def test_list_datasets_avec_version_dvc(data_dir):
    res = json.loads(appeler("list_datasets").content[0].text)
    par_nom = {d["nom"]: d for d in res["jeux"]}
    assert par_nom["obligations.parquet"]["version_dvc"] == "a" * 32
    assert par_nom["flux_passif.parquet"]["version_dvc"] is None


def test_portefeuille_agrege(data_dir):
    res = json.loads(appeler("portfolio_duration_convexity").content[0].text)
    zc, pair = 100 / 1.03**10, 100.0
    assert res["valeur_marche"] == pytest.approx(zc + pair)
    assert res["sensibilite"]["+100bp"] < 0 < res["sensibilite"]["-100bp"]


def test_cashflow_duration(data_dir):
    res = json.loads(appeler("cashflow_duration", {"taux": 0.05}).content[0].text)
    assert res["duration_macaulay"] == pytest.approx(3)
    assert res["valeur_actuelle"] == pytest.approx(100 / 1.05**3)


@pytest.mark.parametrize("nom", ["../secret.csv", "/etc/passwd", "absent.parquet"])
def test_acces_refuse_hors_data(data_dir, nom):
    res = appeler("read_dataset", {"nom": nom})
    assert res.is_error
    assert "hors du dossier" in res.content[0].text or "introuvable" in res.content[0].text


def test_read_dataset_colonnes_et_limite(data_dir):
    res = json.loads(
        appeler("read_dataset", {"nom": "obligations.parquet", "colonnes": ["isin"], "limite": 1})
        .content[0]
        .text
    )
    assert res["lignes"] == [{"isin": "ZC10"}]
    assert res["tronque"] is True


def test_transport_stdio_reel(data_dir):
    """Lance le serveur comme le ferait Claude Code (sous-processus stdio)."""
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_DIR / "server.py")],
        env={"ALM_DATA_DIR": str(data_dir)},
    )

    async def run():
        async with Client(params) as c:
            return await c.call_tool("cashflow_duration", {"taux": 0.05})

    res = json.loads(asyncio.run(run()).content[0].text)
    assert res["duration_macaulay"] == pytest.approx(3)
