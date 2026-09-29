#!/usr/bin/env python3
"""Contrôles de cohérence inter-QRT à partir d'un CSV code,valeur.

Formules : codes de cellule (S.02.01.R0500.C0010), nombres, + - * et parenthèses.
Bibliothèque standard uniquement. Code retour 1 si au moins un contrôle est KO.
"""

from __future__ import annotations

import argparse
import ast
import csv
import operator
import re
import sys
from pathlib import Path

CODE = re.compile(r"S\.\d{2}\.\d{2}\.[A-Z0-9]+\.C\d{4}")
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}
COMPARAISONS = {
    "=": lambda g, d, tol: abs(g - d) <= tol,
    ">=": lambda g, d, tol: g >= d - tol,
    "<=": lambda g, d, tol: g <= d + tol,
}
CONTROLES_DEFAUT = Path(__file__).resolve().parent.parent / "templates" / "controles.csv"


class CodeManquant(KeyError):
    pass


def evaluer(formule: str, valeurs: dict[str, float]) -> float:
    noms: dict[str, float] = {}

    def remplacer(m: re.Match) -> str:
        code = m.group(0)
        if code not in valeurs:
            raise CodeManquant(code)
        nom = f"v{len(noms)}"
        noms[nom] = valeurs[code]
        return nom

    expr = ast.parse(CODE.sub(remplacer, formule), mode="eval").body

    def calc(n: ast.AST) -> float:
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return float(n.value)
        if isinstance(n, ast.Name) and n.id in noms:
            return noms[n.id]
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](calc(n.left), calc(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -calc(n.operand)
        raise ValueError(f"expression non autorisée : {formule}")

    return calc(expr)


def lire_valeurs(chemin: str) -> dict[str, float]:
    with open(chemin, newline="", encoding="utf-8") as f:
        return {r["code"].strip(): float(r["valeur"]) for r in csv.DictReader(f)}


def controler(valeurs: dict[str, float], chemin_controles: str | Path) -> list[dict]:
    resultats = []
    with open(chemin_controles, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            res = {"id": r["id"], "description": r["description"]}
            try:
                g = evaluer(r["gauche"], valeurs)
                d = evaluer(r["droite"], valeurs)
            except CodeManquant as e:
                res.update(statut="N/A", detail=f"cellule absente : {e.args[0]}")
            else:
                ok = COMPARAISONS[r["operateur"]](g, d, float(r["tolerance"]))
                res.update(
                    statut="OK" if ok else "KO",
                    detail=f"{g:,.2f} {r['operateur']} {d:,.2f} (écart {g - d:,.2f})",
                )
            resultats.append(res)
    return resultats


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--valeurs", required=True)
    p.add_argument("--controles", default=str(CONTROLES_DEFAUT))
    args = p.parse_args()
    resultats = controler(lire_valeurs(args.valeurs), args.controles)
    for r in resultats:
        print(f"[{r['statut']:^3}] {r['id']} {r['description']}\n       {r['detail']}")
    nb_ko = sum(r["statut"] == "KO" for r in resultats)
    print(f"\n{len(resultats)} contrôles · {nb_ko} KO")
    sys.exit(1 if nb_ko else 0)


if __name__ == "__main__":
    main()
