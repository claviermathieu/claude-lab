#!/usr/bin/env python3
"""Calcul du SCR marché en formule standard (RD 2015/35, art. 164-188).

Bibliothèque standard uniquement : exécutable sans environnement virtuel.
"""

from __future__ import annotations

import argparse
import json
import math

CHOC_ACTIONS_TYPE1 = 0.39
CHOC_ACTIONS_TYPE2 = 0.49
CORR_ACTIONS_T1_T2 = 0.75
CHOC_IMMOBILIER = 0.25
SA_BORNE = 0.10

MODULES = ["taux", "actions", "immobilier", "spread", "devise", "concentration"]


def correlation_matrix(a: float) -> list[list[float]]:
    """Matrice art. 164, ordre de MODULES."""
    return [
        [1, a, a, a, 0.25, 0],
        [a, 1, 0.75, 0.75, 0.25, 0],
        [a, 0.75, 1, 0.5, 0.25, 0],
        [a, 0.75, 0.5, 1, 0.25, 0],
        [0.25, 0.25, 0.25, 0.25, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]


def scr_actions(
    expo_type1: float, expo_type2: float, sa: float = 0.0
) -> tuple[float, float, float]:
    if not -SA_BORNE <= sa <= SA_BORNE:
        raise ValueError(f"ajustement symétrique hors bornes ±{SA_BORNE:.0%} : {sa}")
    t1 = expo_type1 * (CHOC_ACTIONS_TYPE1 + sa)
    t2 = expo_type2 * (CHOC_ACTIONS_TYPE2 + sa)
    total = math.sqrt(t1**2 + 2 * CORR_ACTIONS_T1_T2 * t1 * t2 + t2**2)
    return t1, t2, total


def scr_marche(
    taux_hausse: float,
    taux_baisse: float,
    actions_type1: float,
    actions_type2: float,
    immobilier: float,
    spread: float,
    devise: float,
    concentration: float,
    sa: float = 0.0,
) -> dict:
    """Pertes de taux et SCR spread/devise/concentration en entrée ; expositions actions/immo."""
    scenario = "baisse" if taux_baisse > taux_hausse else "hausse"
    a = 0.5 if scenario == "baisse" else 0.0
    t1, t2, actions = scr_actions(actions_type1, actions_type2, sa)
    sous_modules = {
        "taux": max(taux_hausse, taux_baisse, 0.0),
        "actions": actions,
        "immobilier": immobilier * CHOC_IMMOBILIER,
        "spread": spread,
        "devise": devise,
        "concentration": concentration,
    }
    v = [sous_modules[m] for m in MODULES]
    corr = correlation_matrix(a)
    total = math.sqrt(sum(corr[i][j] * v[i] * v[j] for i in range(6) for j in range(6)))
    somme = sum(v)
    return {
        "scenario_taux": scenario,
        "parametre_A": a,
        "actions_detail": {"type1": t1, "type2": t2},
        "sous_modules": sous_modules,
        "somme": somme,
        "scr_marche": total,
        "diversification": somme - total,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in [
        "taux-hausse",
        "taux-baisse",
        "actions-type1",
        "actions-type2",
        "immobilier",
        "spread",
        "devise",
        "concentration",
    ]:
        p.add_argument(f"--{name}", type=float, default=0.0)
    p.add_argument("--sa", type=float, default=0.0, help="ajustement symétrique (décimal)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    res = scr_marche(
        args.taux_hausse,
        args.taux_baisse,
        args.actions_type1,
        args.actions_type2,
        args.immobilier,
        args.spread,
        args.devise,
        args.concentration,
        args.sa,
    )
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return
    print(f"Scénario de taux retenu : {res['scenario_taux']} → A = {res['parametre_A']}")
    d = res["actions_detail"]
    print(f"Actions : type 1 = {d['type1']:.1f}, type 2 = {d['type2']:.1f}")
    for m, val in res["sous_modules"].items():
        print(f"  SCR {m:<13} {val:10.1f}")
    print(f"Somme des sous-modules  {res['somme']:10.1f}")
    print(f"SCR marché              {res['scr_marche']:10.1f}")
    div = res["diversification"]
    print(f"Diversification         {div:10.1f} ({div / res['somme']:.1%})")


if __name__ == "__main__":
    main()
