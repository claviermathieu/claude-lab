# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp>=2.2", "numpy>=2.0", "pandas>=2.2", "pyarrow>=15"]
# ///
"""Serveur MCP « alm-data » : accès aux données ALM (Parquet/CSV versionnés DVC) et calculs de taux.

Transport stdio. Lancement : uv run python modules/07-mcp/server/server.py
Racine des données : $ALM_DATA_DIR, sinon <repo>/data. Aucun accès hors de cette racine.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

DATA_DIR = Path(
    os.environ.get("ALM_DATA_DIR", Path(__file__).resolve().parents[3] / "data")
).resolve()
MAX_LIGNES = 500

server = MCPServer(
    name="alm-data",
    instructions=(
        "Données ALM d'un assureur (portefeuille obligataire, flux de passif, bilan) et calculs "
        "de duration/convexité. Commencer par list_datasets. Montants en M€, taux en décimal."
    ),
)


def _chemin(nom: str) -> Path:
    chemin = (DATA_DIR / nom).resolve()
    if DATA_DIR not in chemin.parents:
        raise ToolError(f"chemin hors du dossier de données : {nom}")
    if not chemin.is_file():
        raise ToolError(f"jeu de données introuvable : {nom} (voir list_datasets)")
    return chemin


def _lire(nom: str) -> pd.DataFrame:
    chemin = _chemin(nom)
    if chemin.suffix == ".parquet":
        return pd.read_parquet(chemin)
    if chemin.suffix == ".csv":
        return pd.read_csv(chemin)
    raise ToolError("formats acceptés : .parquet, .csv")


def _version_dvc(chemin: Path) -> str | None:
    manifeste = chemin.with_suffix(chemin.suffix + ".dvc")
    if not manifeste.exists():
        return None
    m = re.search(r"md5:\s*([0-9a-f]{32})", manifeste.read_text())
    return m.group(1) if m else None


@server.tool()
def list_datasets() -> dict:
    """Liste les jeux de données disponibles avec colonnes, nombre de lignes et version DVC (md5)."""
    sortie = []
    for chemin in sorted(DATA_DIR.glob("*")):
        if chemin.suffix not in {".parquet", ".csv"}:
            continue
        df = _lire(chemin.name)
        sortie.append(
            {
                "nom": chemin.name,
                "lignes": len(df),
                "colonnes": {c: str(t) for c, t in df.dtypes.items()},
                "version_dvc": _version_dvc(chemin),
            }
        )
    return {"racine": str(DATA_DIR), "jeux": sortie}


@server.tool()
def read_dataset(nom: str, colonnes: list[str] | None = None, limite: int = 100) -> dict:
    """Lit un jeu de données (Parquet ou CSV) du dossier data/.

    nom : nom du fichier tel que renvoyé par list_datasets (ex. obligations.parquet).
    colonnes : sous-ensemble de colonnes (toutes par défaut).
    limite : nombre maximal de lignes renvoyées (plafonné à 500).
    """
    df = _lire(nom)
    if colonnes:
        inconnues = set(colonnes) - set(df.columns)
        if inconnues:
            raise ToolError(f"colonnes inconnues : {sorted(inconnues)}")
        df = df[colonnes]
    limite = max(1, min(limite, MAX_LIGNES))
    return {
        "nom": nom,
        "version_dvc": _version_dvc(_chemin(nom)),
        "lignes_totales": len(df),
        "lignes": df.head(limite).to_dict(orient="records"),
        "tronque": len(df) > limite,
    }


def indicateurs_obligation(
    nominal: float, coupon: float, maturite: float, rendement: float, frequence: int = 1
) -> dict:
    """Prix, duration de Macaulay, duration modifiée et convexité (rendement actuariel)."""
    n = max(1, round(maturite * frequence))
    t = np.arange(1, n + 1) / frequence
    flux = np.full(n, nominal * coupon / frequence)
    flux[-1] += nominal
    y = rendement / frequence
    actualisation = (1 + y) ** (-np.arange(1, n + 1))
    vp = flux * actualisation
    prix = float(vp.sum())
    macaulay = float((t * vp).sum() / prix)
    modifiee = macaulay / (1 + y)
    k = np.arange(1, n + 1)
    convexite = float((vp * k * (k + 1)).sum() / (prix * (1 + y) ** 2 * frequence**2))
    return {
        "prix": prix,
        "duration_macaulay": macaulay,
        "duration_modifiee": modifiee,
        "convexite": convexite,
    }


@server.tool()
def portfolio_duration_convexity(nom: str = "obligations.parquet", choc_bp: float = 100.0) -> dict:
    """Duration et convexité d'un portefeuille obligataire, par titre et agrégées (pondération valeur de marché).

    Colonnes attendues : isin, nominal, coupon, maturite, rendement, [frequence].
    choc_bp : choc parallèle de rendement pour l'estimation de variation de valeur (±).
    """
    df = _lire(nom)
    manquantes = {"isin", "nominal", "coupon", "maturite", "rendement"} - set(df.columns)
    if manquantes:
        raise ToolError(f"colonnes manquantes : {sorted(manquantes)}")
    lignes = []
    for r in df.itertuples(index=False):
        ind = indicateurs_obligation(
            r.nominal, r.coupon, r.maturite, r.rendement, int(getattr(r, "frequence", 1))
        )
        lignes.append({"isin": r.isin, **ind})
    res = pd.DataFrame(lignes)
    vm = res["prix"].sum()
    poids = res["prix"] / vm
    d_mod = float((poids * res["duration_modifiee"]).sum())
    conv = float((poids * res["convexite"]).sum())
    dy = choc_bp / 1e4
    return {
        "nom": nom,
        "version_dvc": _version_dvc(_chemin(nom)),
        "valeur_marche": float(vm),
        "duration_macaulay": float((poids * res["duration_macaulay"]).sum()),
        "duration_modifiee": d_mod,
        "convexite": conv,
        "sensibilite": {
            f"+{choc_bp:g}bp": float(vm * (-d_mod * dy + 0.5 * conv * dy**2)),
            f"-{choc_bp:g}bp": float(vm * (d_mod * dy + 0.5 * conv * dy**2)),
        },
        "titres": res.round(6).to_dict(orient="records"),
    }


@server.tool()
def cashflow_duration(nom: str = "flux_passif.parquet", taux: float = 0.03) -> dict:
    """Valeur actuelle, duration et convexité d'une série de flux (ex. passif) à taux plat.

    Colonnes attendues : annee, flux. taux : taux d'actualisation annuel (décimal).
    """
    df = _lire(nom)
    t = df["annee"].to_numpy(float)
    vp = df["flux"].to_numpy(float) * (1 + taux) ** (-t)
    va = float(vp.sum())
    macaulay = float((t * vp).sum() / va)
    return {
        "nom": nom,
        "version_dvc": _version_dvc(_chemin(nom)),
        "valeur_actuelle": va,
        "duration_macaulay": macaulay,
        "duration_modifiee": macaulay / (1 + taux),
        "convexite": float((vp * t * (t + 1)).sum() / (va * (1 + taux) ** 2)),
    }


SEUIL_RECONCILIATION = 0.05


@server.tool()
def duration_gap(
    taux: float = 0.03,
    choc_bp: float = 100.0,
    bilan: str = "bilan.csv",
    obligations: str = "obligations.parquet",
    passif: str = "flux_passif.parquet",
) -> dict:
    """Synthèse ALM calculée (à utiliser plutôt que de calculer soi-même) : réconciliation
    bilan / valeurs recalculées, duration gap et variation des fonds propres à ±choc.

    Deux bases : « bilan » (montants du bilan, durations des outils) et « recalculee »
    (VM des obligations, VA des flux de passif au taux donné). Seuls obligations et
    best estimate sont sensibles aux taux. ΔFP = −(D_A·A − D_P·P)·Δy + ½(C_A·A − C_P·P)·Δy².
    Les ratios ΔFP/FP sont rapportés aux fonds propres du bilan.
    """
    b = _lire(bilan)
    if not {"cote", "poste", "montant_meur"} <= set(b.columns):
        raise ToolError("bilan : colonnes attendues cote, poste, montant_meur")
    poste = dict(zip(b["poste"], b["montant_meur"], strict=True))
    for requis in ("obligations", "best_estimate"):
        if requis not in poste:
            raise ToolError(f"bilan : poste « {requis} » absent")
    total_actif = float(b.loc[b["cote"] == "actif", "montant_meur"].sum())
    total_passif = float(b.loc[b["cote"] == "passif", "montant_meur"].sum())
    fp = total_actif - total_passif

    act = portfolio_duration_convexity(obligations, choc_bp)
    pas = cashflow_duration(passif, taux)
    d_a, c_a = act["duration_modifiee"], act["convexite"]
    d_p, c_p = pas["duration_modifiee"], pas["convexite"]
    dy = choc_bp / 1e4

    def base(a: float, p: float) -> dict:
        def delta(signe: int) -> float:
            return -(d_a * a - d_p * p) * signe * dy + 0.5 * (c_a * a - c_p * p) * dy**2

        return {
            "actif_sensible": a,
            "passif_sensible": p,
            "duration_gap": d_a - d_p * p / a,
            f"dfp_+{choc_bp:g}bp": delta(+1),
            f"dfp_-{choc_bp:g}bp": delta(-1),
            f"dfp_sur_fp_+{choc_bp:g}bp": delta(+1) / fp,
            f"dfp_sur_fp_-{choc_bp:g}bp": delta(-1) / fp,
        }

    def ecart(bilan_val: float, recalcule: float) -> dict:
        rel = (recalcule - bilan_val) / bilan_val
        return {
            "bilan": bilan_val,
            "recalcule": recalcule,
            "ecart": recalcule - bilan_val,
            "ecart_relatif": rel,
            "au_dela_du_seuil": abs(rel) > SEUIL_RECONCILIATION,
        }

    bases = {
        "bilan": base(float(poste["obligations"]), float(poste["best_estimate"])),
        "recalculee": base(act["valeur_marche"], pas["valeur_actuelle"]),
    }
    signes = {v["duration_gap"] > 0 for v in bases.values()}
    return {
        "versions_dvc": {
            bilan: _version_dvc(_chemin(bilan)),
            obligations: act["version_dvc"],
            passif: pas["version_dvc"],
        },
        "hypotheses": {"taux_passif": taux, "choc_bp": choc_bp, "seuil": SEUIL_RECONCILIATION},
        "fonds_propres_bilan": fp,
        "durations": {"D_A": d_a, "C_A": c_a, "D_P": d_p, "C_P": c_p},
        "reconciliation": {
            "obligations": ecart(float(poste["obligations"]), act["valeur_marche"]),
            "best_estimate": ecart(float(poste["best_estimate"]), pas["valeur_actuelle"]),
        },
        "bases": bases,
        "signe_du_gap_robuste": len(signes) == 1,
    }


if __name__ == "__main__":
    server.run()
