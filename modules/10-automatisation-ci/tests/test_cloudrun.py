"""Tests du service Cloud Run avec un faux client Claude (aucun appel réseau)."""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import anthropic
import httpx
import pytest
from fastapi.testclient import TestClient

CHEMIN = Path(__file__).resolve().parents[1] / "cloudrun" / "main.py"
spec = importlib.util.spec_from_file_location("cloudrun_main", CHEMIN)
service = importlib.util.module_from_spec(spec)
sys.modules["cloudrun_main"] = service
spec.loader.exec_module(service)

NOTE = "SCR taux 65 (baisse), matrice avec A = 0, immobilier choqué à 20 %."


class FauxClient:
    def __init__(self, reponse=None, erreur=None):
        self.reponse, self.erreur, self.appels = reponse, erreur, []
        self.beta = NS(messages=NS(create=self._create))

    async def _create(self, **params):
        self.appels.append(params)
        if self.erreur:
            raise self.erreur
        return self.reponse


def reponse_ok(texte="A doit valoir 0,5."):
    return NS(
        stop_reason="end_turn",
        content=[NS(type="thinking", thinking=""), NS(type="text", text=texte)],
        usage=NS(
            input_tokens=40,
            output_tokens=300,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=2500,
        ),
    )


@pytest.fixture
def appel():
    def _appel(faux, corps=None):
        service.app.dependency_overrides[service.client_claude] = lambda: faux
        try:
            return TestClient(service.app).post("/revue", json=corps or {"note": NOTE})
        finally:
            service.app.dependency_overrides.clear()

    return _appel


def test_health():
    r = TestClient(service.app).get("/health")
    assert r.status_code == 200 and r.json()["statut"] == "ok"


def test_revue_renvoie_le_texte_et_l_usage(appel):
    faux = FauxClient(reponse_ok())
    r = appel(faux)
    assert r.status_code == 200
    assert r.json() == {
        "revue": "A doit valoir 0,5.",
        "usage": {"input": 40, "output": 300, "cache_write": 0, "cache_read": 2500},
    }


def test_referentiel_du_skill_en_systeme_cache(appel):
    faux = FauxClient(reponse_ok())
    appel(faux)
    systeme = faux.appels[0]["system"][0]
    assert "Règle du paramètre A" in systeme["text"]
    assert systeme["cache_control"] == {"type": "ephemeral"}
    assert NOTE in faux.appels[0]["messages"][0]["content"]
    assert faux.appels[0]["fallbacks"] == "default"


def test_note_trop_courte_refusee(appel):
    assert appel(FauxClient(reponse_ok()), {"note": "court"}).status_code == 422


def test_refus_du_modele(appel):
    faux = FauxClient(NS(stop_reason="refusal", content=[], usage=None))
    assert appel(faux).status_code == 422


def test_limite_de_debit(appel):
    req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    erreur = anthropic.RateLimitError(
        "rate limited", response=httpx.Response(429, request=req), body=None
    )
    assert appel(FauxClient(erreur=erreur)).status_code == 429
