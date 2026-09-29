"""Génère les jeux de données d'exemple dans data/ (ignoré par git).

- obligations.parquet : portefeuille obligataire (1 ligne par titre)
- flux_passif.parquet : flux de passif projetés (prestations nettes par année)
- bilan.csv : bilan économique simplifié (M€)
Chaque Parquet reçoit un manifeste `.dvc` au format DVC (md5, taille) pour simuler
un fichier versionné par DVC sans dépendre de l'outil.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[3] / "data"


def ecrire_manifeste_dvc(chemin: Path) -> None:
    md5 = hashlib.md5(chemin.read_bytes()).hexdigest()
    chemin.with_suffix(chemin.suffix + ".dvc").write_text(
        f"outs:\n- md5: {md5}\n  size: {chemin.stat().st_size}\n  hash: md5\n  path: {chemin.name}\n"
    )


def obligations(rng: np.random.Generator) -> pd.DataFrame:
    n = 40
    emetteurs = ["OAT", "BUND", "BTP", "BONOS", "CORP_IG", "CORP_FIN"]
    maturites = rng.choice([2, 3, 5, 7, 10, 12, 15, 20, 25, 30], size=n)
    return pd.DataFrame(
        {
            "isin": [f"FR{100000000 + i:010d}" for i in range(n)],
            "emetteur": rng.choice(emetteurs, size=n),
            "nominal": rng.choice([5, 10, 20, 25, 50], size=n).astype(float),  # M€
            "coupon": np.round(rng.uniform(0.0, 0.045, size=n), 4),
            "maturite": maturites.astype(float),
            "frequence": 1,
            "rendement": np.round(0.022 + 0.0006 * maturites + rng.normal(0, 0.002, n), 4),
        }
    )


def flux_passif() -> pd.DataFrame:
    annees = np.arange(1, 41)
    # Portefeuille d'épargne en run-off : prestations décroissantes (M€).
    flux = 60.0 * np.exp(-0.07 * (annees - 1)) + 8.0 * (annees <= 8)
    return pd.DataFrame({"annee": annees, "flux": np.round(flux, 3)})


def bilan(oblig: pd.DataFrame) -> pd.DataFrame:
    valeur_oblig = float((oblig["nominal"] * 1.0).sum())
    lignes = [
        ("actif", "obligations", round(valeur_oblig, 1)),
        ("actif", "actions", 90.0),
        ("actif", "immobilier", 60.0),
        ("actif", "tresorerie", 25.0),
        ("passif", "best_estimate", round(valeur_oblig + 90.0 + 60.0 + 25.0 - 140.0, 1)),
        ("passif", "marge_de_risque", 20.0),
        ("passif", "autres_passifs", 15.0),
    ]
    return pd.DataFrame(lignes, columns=["cote", "poste", "montant_meur"])


def main() -> None:
    DATA.mkdir(exist_ok=True)
    rng = np.random.default_rng(2026)
    oblig = obligations(rng)
    for nom, df in [("obligations", oblig), ("flux_passif", flux_passif())]:
        chemin = DATA / f"{nom}.parquet"
        df.to_parquet(chemin, index=False)
        ecrire_manifeste_dvc(chemin)
    bilan(oblig).to_csv(DATA / "bilan.csv", index=False)
    print(f"Données écrites dans {DATA}")


if __name__ == "__main__":
    main()
