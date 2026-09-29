"""Tests des scripts embarqués dans les skills (.claude/skills/*/scripts)."""

import importlib.util
import math
import sys
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parents[3] / ".claude" / "skills"


def charger(skill: str, script: str):
    spec = importlib.util.spec_from_file_location(
        script, SKILLS / skill / "scripts" / f"{script}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[script] = module  # requis par @dataclass
    spec.loader.exec_module(module)
    return module


scr = charger("scr-marche", "scr_marche")
ecl = charger("ifrs9-ecl", "ecl")
qrt = charger("sii-reporting-qrt", "check_qrt")


# --- scr-marche -------------------------------------------------------------


def test_scr_marche_reproduit_le_corrige_m01():
    res = scr.scr_marche(42, 65, 200, 50, 150, 40, 12, 5)
    assert res["parametre_A"] == 0.5
    assert res["sous_modules"]["actions"] == pytest.approx(97.73, abs=0.01)
    assert res["sous_modules"]["immobilier"] == 37.5
    assert res["scr_marche"] == pytest.approx(206.50, abs=0.01)


def test_scr_marche_parametre_a_nul_si_hausse_retenue():
    res = scr.scr_marche(80, 65, 200, 50, 150, 40, 12, 5)
    assert res["scenario_taux"] == "hausse"
    assert res["parametre_A"] == 0.0


def test_scr_marche_sa_hors_bornes():
    with pytest.raises(ValueError):
        scr.scr_actions(100, 100, sa=0.2)


def test_scr_marche_module_seul_sans_diversification():
    res = scr.scr_marche(0, 0, 0, 0, 100, 0, 0, 0)
    assert res["scr_marche"] == pytest.approx(25.0)
    assert res["diversification"] == pytest.approx(0.0)


# --- ifrs9-ecl ---------------------------------------------------------------

COURBES = {("seg", "base"): [0.02, 0.0396, 0.058808], ("seg", "stress"): [0.04, 0.0784, 0.115264]}


def expo(**kw):
    defaut = {"id": "x", "segment": "seg", "ead": 1000.0, "lgd": 0.5, "tie": 0.05, "maturite": 3.0}
    return ecl.Exposition(**{**defaut, **kw})


def test_ecl_stage1_calcul_a_la_main():
    res = ecl.calculer([expo()], COURBES, {"base": 1.0})
    ligne = res["expositions"][0]
    assert ligne["stage"] == 1
    assert ligne["ecl"] == pytest.approx(0.02 * 0.5 * 1000 / 1.05)


def test_ecl_stage2_lifetime_superieur_au_stage1():
    s1 = ecl.calculer([expo()], COURBES, {"base": 1.0})["total"]["ecl"]
    s2 = ecl.calculer([expo(watchlist=True)], COURBES, {"base": 1.0})
    assert s2["expositions"][0]["stage"] == 2
    attendu = sum(
        (c - p) * 0.5 * 1000 / 1.05**t
        for t, (p, c) in enumerate(zip([0, 0.02, 0.0396], [0.02, 0.0396, 0.058808]), start=1)
    )
    assert s2["total"]["ecl"] == pytest.approx(attendu)
    assert s2["total"]["ecl"] > s1


def test_ecl_stage3_lgd_fois_ead():
    res = ecl.calculer([expo(jours_impayes=120)], COURBES, {"base": 1.0})
    assert res["expositions"][0]["stage"] == 3
    assert res["total"]["ecl"] == pytest.approx(500.0)


@pytest.mark.parametrize(
    "kw, attendu",
    [
        ({"jours_impayes": 31}, 2),
        ({"jours_impayes": 30}, 1),
        ({"jours_impayes": 91}, 3),
        ({"pd_lifetime_origine": 0.01}, 2),  # PD lifetime 5,9 % > 2,5 × 1 %
        ({"pd_lifetime_origine": 0.05}, 1),
    ],
)
def test_ecl_staging(kw, attendu):
    assert ecl.calculer([expo(**kw)], COURBES, {"base": 1.0})["expositions"][0]["stage"] == attendu


def test_ecl_ponderation_des_scenarios():
    base = ecl.calculer([expo()], COURBES, {"base": 1.0})["total"]["ecl"]
    stress = ecl.calculer([expo()], COURBES, {"stress": 1.0})["total"]["ecl"]
    mix = ecl.calculer([expo()], COURBES, {"base": 0.7, "stress": 0.3})["total"]["ecl"]
    assert mix == pytest.approx(0.7 * base + 0.3 * stress)


def test_ecl_poids_invalides():
    with pytest.raises(ValueError):
        ecl.calculer([expo()], COURBES, {"base": 0.5})


def test_ecl_maturite_fractionnaire():
    res = ecl.calculer([expo(maturite=0.5)], COURBES, {"base": 1.0})
    assert res["total"]["ecl"] == pytest.approx(0.01 * 0.5 * 1000 / 1.05**0.5)


def test_ecl_exemples_fournis():
    dossier = SKILLS / "ifrs9-ecl" / "exemples"
    res = ecl.calculer(
        ecl.lire_expositions(dossier / "expositions.csv"),
        ecl.lire_pd(dossier / "pd_cumulees.csv"),
        {"base": 0.5, "favorable": 0.2, "defavorable": 0.3},
    )
    assert [res["par_stage"][s]["nb"] for s in (1, 2, 3)] == [4, 3, 1]
    assert res["par_stage"][1]["couverture"] < res["par_stage"][2]["couverture"]


# --- sii-reporting-qrt -------------------------------------------------------


def test_qrt_exemple_tous_ok():
    tpl = SKILLS / "sii-reporting-qrt" / "templates"
    res = qrt.controler(qrt.lire_valeurs(tpl / "valeurs-exemple.csv"), tpl / "controles.csv")
    assert {r["statut"] for r in res} == {"OK"}


def test_qrt_detecte_un_ecart_et_une_cellule_absente():
    tpl = SKILLS / "sii-reporting-qrt" / "templates"
    valeurs = qrt.lire_valeurs(tpl / "valeurs-exemple.csv")
    valeurs["S.25.01.R0200.C0100"] = 270_000_000
    del valeurs["S.06.02.TOTAL.C0170"]
    statuts = {r["id"]: r["statut"] for r in qrt.controler(valeurs, tpl / "controles.csv")}
    assert statuts["C03"] == "KO"
    assert statuts["C06"] == "N/A"


def test_qrt_evaluation_securisee():
    assert qrt.evaluer("0.25 * S.25.01.R0200.C0100 - 1", {"S.25.01.R0200.C0100": 100}) == 24
    with pytest.raises(ValueError):
        qrt.evaluer("__import__('os')", {})
    assert math.isclose(qrt.evaluer("(1 + 2) * 3", {}), 9)
