#!/usr/bin/env python3
"""Calcul des ECL IFRS 9 (staging + ECL 12 mois / lifetime, scénarios pondérés).

Bibliothèque standard uniquement : exécutable sans environnement virtuel.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass

SEUIL_SICR_DEFAUT = 2.5  # ratio PD lifetime actuelle / origine
BACKSTOP_STAGE2_JOURS = 30
BACKSTOP_DEFAUT_JOURS = 90


@dataclass(frozen=True)
class Exposition:
    id: str
    segment: str
    ead: float
    lgd: float
    tie: float
    maturite: float
    jours_impayes: int = 0
    watchlist: bool = False
    pd_lifetime_origine: float | None = None


PdCurves = dict[tuple[str, str], list[float]]  # (segment, scénario) -> PD cumulées années 1..N


def lire_expositions(chemin: str) -> list[Exposition]:
    with open(chemin, newline="", encoding="utf-8") as f:
        return [
            Exposition(
                id=r["id"],
                segment=r["segment"],
                ead=float(r["ead"]),
                lgd=float(r["lgd"]),
                tie=float(r["tie"]),
                maturite=float(r["maturite"]),
                jours_impayes=int(r.get("jours_impayes") or 0),
                watchlist=(r.get("watchlist") or "").strip().lower() in {"1", "true", "oui"},
                pd_lifetime_origine=float(r["pd_lifetime_origine"])
                if r.get("pd_lifetime_origine")
                else None,
            )
            for r in csv.DictReader(f)
        ]


def lire_pd(chemin: str) -> PdCurves:
    brut: dict[tuple[str, str], dict[int, float]] = defaultdict(dict)
    with open(chemin, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            brut[(r["segment"], r["scenario"])][int(r["annee"])] = float(r["pd_cum"])
    courbes: PdCurves = {}
    for cle, points in brut.items():
        annees = sorted(points)
        if annees != list(range(1, len(annees) + 1)):
            raise ValueError(f"années manquantes pour {cle} : {annees}")
        valeurs = [points[a] for a in annees]
        croissantes = all(valeurs[i + 1] >= valeurs[i] for i in range(len(valeurs) - 1))
        if any(not 0 <= v <= 1 for v in valeurs) or not croissantes:
            raise ValueError(f"PD cumulées invalides (hors [0,1] ou décroissantes) pour {cle}")
        courbes[cle] = valeurs
    return courbes


def pd_cumulee(courbe: list[float], t: float) -> float:
    """PD cumulée à t années, interpolation linéaire (0 en 0, plate au-delà du dernier point)."""
    if t <= 0:
        return 0.0
    points = [0.0, *courbe]
    if t >= len(courbe):
        return points[-1]
    i = math.floor(t)
    return points[i] + (t - i) * (points[i + 1] - points[i])


def stage(
    expo: Exposition, pd_lifetime_actuelle: float, seuil_sicr: float = SEUIL_SICR_DEFAUT
) -> int:
    if expo.jours_impayes > BACKSTOP_DEFAUT_JOURS:
        return 3
    if expo.jours_impayes > BACKSTOP_STAGE2_JOURS or expo.watchlist:
        return 2
    if expo.pd_lifetime_origine and pd_lifetime_actuelle > seuil_sicr * expo.pd_lifetime_origine:
        return 2
    return 1


def ecl_scenario(expo: Exposition, courbe: list[float], horizon: float) -> float:
    """Σ PD marginale × LGD × EAD × actualisation, par pas annuels (dernier pas fractionnaire)."""
    total, t_prec = 0.0, 0.0
    while t_prec < horizon - 1e-12:
        t = min(t_prec + 1.0, horizon)
        pd_marg = pd_cumulee(courbe, t) - pd_cumulee(courbe, t_prec)
        total += pd_marg * expo.lgd * expo.ead * (1 + expo.tie) ** (-t)
        t_prec = t
    return total


def calculer(
    expositions: list[Exposition],
    courbes: PdCurves,
    poids: dict[str, float],
    seuil_sicr: float = SEUIL_SICR_DEFAUT,
) -> dict:
    if not math.isclose(sum(poids.values()), 1.0, abs_tol=1e-9):
        raise ValueError(
            f"les poids de scénarios doivent sommer à 1 (somme = {sum(poids.values())})"
        )
    lignes = []
    for e in expositions:
        manquants = [s for s in poids if (e.segment, s) not in courbes]
        if manquants:
            raise ValueError(f"pas de courbe PD pour {e.segment} / {manquants}")
        pd_life = sum(w * pd_cumulee(courbes[(e.segment, s)], e.maturite) for s, w in poids.items())
        st = stage(e, pd_life, seuil_sicr)
        if st == 3:
            ecl = e.lgd * e.ead
        else:
            horizon = min(1.0, e.maturite) if st == 1 else e.maturite
            ecl = sum(
                w * ecl_scenario(e, courbes[(e.segment, s)], horizon) for s, w in poids.items()
            )
        lignes.append({"id": e.id, "segment": e.segment, "stage": st, "ead": e.ead, "ecl": ecl})

    par_stage = {}
    for st in (1, 2, 3):
        sel = [ligne for ligne in lignes if ligne["stage"] == st]
        ead = sum(ligne["ead"] for ligne in sel)
        ecl = sum(ligne["ecl"] for ligne in sel)
        par_stage[st] = {
            "nb": len(sel),
            "ead": ead,
            "ecl": ecl,
            "couverture": ecl / ead if ead else 0.0,
        }
    ead_tot = sum(ligne["ead"] for ligne in lignes)
    ecl_tot = sum(ligne["ecl"] for ligne in lignes)
    return {
        "expositions": lignes,
        "par_stage": par_stage,
        "total": {
            "ead": ead_tot,
            "ecl": ecl_tot,
            "couverture": ecl_tot / ead_tot if ead_tot else 0.0,
        },
    }


def parse_poids(texte: str) -> dict[str, float]:
    poids = {}
    for morceau in texte.split(","):
        nom, _, valeur = morceau.partition("=")
        poids[nom.strip()] = float(valeur)
    return poids


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--expositions", required=True)
    p.add_argument("--pd", required=True)
    p.add_argument("--scenarios", required=True, help="ex. base=0.5,favorable=0.2,defavorable=0.3")
    p.add_argument("--seuil-sicr", type=float, default=SEUIL_SICR_DEFAUT)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    res = calculer(
        lire_expositions(args.expositions),
        lire_pd(args.pd),
        parse_poids(args.scenarios),
        args.seuil_sicr,
    )
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return
    print(f"{'id':<8}{'segment':<14}{'stage':>6}{'EAD':>14}{'ECL':>12}")
    for ligne in res["expositions"]:
        print(
            f"{ligne['id']:<8}{ligne['segment']:<14}{ligne['stage']:>6}"
            f"{ligne['ead']:>14,.0f}{ligne['ecl']:>12,.0f}"
        )
    print()
    for st, v in res["par_stage"].items():
        print(
            f"Stage {st} : {v['nb']:>3} expo · EAD {v['ead']:>14,.0f} · ECL {v['ecl']:>12,.0f}"
            f" · couverture {v['couverture']:.2%}"
        )
    t = res["total"]
    print(f"Total   : EAD {t['ead']:,.0f} · ECL {t['ecl']:,.0f} · couverture {t['couverture']:.2%}")


if __name__ == "__main__":
    main()
