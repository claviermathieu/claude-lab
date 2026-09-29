"""Extrapolation Smith-Wilson d'une courbe de taux sans risque, méthode EIOPA.

Référence : EIOPA, *Technical documentation of the methodology to derive EIOPA's
risk-free interest rate term structures* (section Smith-Wilson).

Conventions :
- taux d'entrée et de sortie en composition annuelle, maturités en années ;
- ω = ln(1 + UFR) est l'intensité forward ultime (composition continue) ;
- l'ajustement pour risque de crédit (CRA) est retranché des taux d'entrée.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

ALPHA_MIN = 0.05
CONVERGENCE_TOLERANCE = 1e-4  # 1 bp sur l'intensité forward au point de convergence


def wilson(t: np.ndarray, u: np.ndarray, alpha: float, omega: float) -> np.ndarray:
    """Matrice de Wilson W(t_i, u_j)."""
    t = np.asarray(t, dtype=float)[:, None]
    u = np.asarray(u, dtype=float)[None, :]
    lo, hi = np.minimum(t, u), np.maximum(t, u)
    return np.exp(-omega * (t + u)) * (alpha * lo - np.exp(-alpha * hi) * np.sinh(alpha * lo))


@dataclass(frozen=True)
class SmithWilsonCurve:
    """Courbe calibrée : prix zéro-coupon P(t) = e^{-ωt} + Σ ζ_j W(t, u_j)."""

    maturities: np.ndarray
    zeta: np.ndarray
    alpha: float
    omega: float

    @property
    def ufr(self) -> float:
        return float(np.expm1(self.omega))

    def discount(self, t) -> np.ndarray:
        t = np.atleast_1d(np.asarray(t, dtype=float))
        return (
            np.exp(-self.omega * t) + wilson(t, self.maturities, self.alpha, self.omega) @ self.zeta
        )

    def spot(self, t) -> np.ndarray:
        """Taux zéro-coupon en composition annuelle."""
        t = np.atleast_1d(np.asarray(t, dtype=float))
        if np.any(t <= 0):
            raise ValueError("les maturités doivent être strictement positives")
        return self.discount(t) ** (-1.0 / t) - 1.0

    def forward_intensity(self, t) -> np.ndarray:
        """Intensité forward instantanée f(t) = -d ln P / dt, formule exacte pour t ≥ dernier point liquide."""
        t = np.atleast_1d(np.asarray(t, dtype=float))
        if np.any(t < self.maturities.max()):
            raise ValueError(
                "formule analytique valable seulement au-delà du dernier point liquide"
            )
        u = self.maturities[None, :]
        tt = t[:, None]
        w = wilson(t, self.maturities, self.alpha, self.omega)
        # Pour t ≥ u : W = e^{-ω(t+u)} (αu − e^{-αt} sinh(αu))
        dw = -self.omega * w + np.exp(-self.omega * (tt + u)) * self.alpha * np.exp(
            -self.alpha * tt
        ) * np.sinh(self.alpha * u)
        dp = -self.omega * np.exp(-self.omega * t) + dw @ self.zeta
        return -dp / self.discount(t)

    def forward_annual(self, t) -> np.ndarray:
        """Taux forward 1 an en composition annuelle entre t et t+1."""
        t = np.atleast_1d(np.asarray(t, dtype=float))
        return self.discount(t) / self.discount(t + 1.0) - 1.0


def _fit(maturities: np.ndarray, rates: np.ndarray, alpha: float, omega: float) -> SmithWilsonCurve:
    prices = (1.0 + rates) ** (-maturities)
    mu = np.exp(-omega * maturities)
    zeta = np.linalg.solve(wilson(maturities, maturities, alpha, omega), prices - mu)
    return SmithWilsonCurve(maturities, zeta, alpha, omega)


def convergence_point(llp: float, convergence_period: float = 40.0) -> float:
    """Point de convergence EIOPA : max(LLP + 40, 60)."""
    return max(llp + convergence_period, 60.0)


def convergence_gap(curve: SmithWilsonCurve, point: float) -> float:
    return float(abs(curve.forward_intensity(point)[0] - curve.omega))


def calibrate(
    maturities,
    rates,
    ufr: float,
    cra_bp: float = 0.0,
    convergence_period: float = 40.0,
    tolerance: float = CONVERGENCE_TOLERANCE,
) -> SmithWilsonCurve:
    """Calibre la courbe : plus petit α ≥ 0,05 tel que |f(CP) − ω| ≤ 1 bp.

    maturities : points liquides en années (le dernier est le LLP).
    rates : taux zéro-coupon de marché (composition annuelle), avant CRA.
    ufr : taux forward ultime en composition annuelle (ex. 0.033).
    cra_bp : ajustement pour risque de crédit en points de base, retranché des taux.
    """
    maturities = np.asarray(maturities, dtype=float)
    rates = np.asarray(rates, dtype=float) - cra_bp / 1e4
    if maturities.shape != rates.shape or maturities.ndim != 1 or maturities.size == 0:
        raise ValueError("maturités et taux doivent être des vecteurs non vides de même taille")
    if np.any(maturities <= 0) or np.any(np.diff(maturities) <= 0):
        raise ValueError("les maturités doivent être strictement positives et croissantes")
    if ufr <= -1:
        raise ValueError("UFR invalide")

    omega = float(np.log1p(ufr))
    point = convergence_point(maturities[-1], convergence_period)

    def gap(alpha: float) -> float:
        return convergence_gap(_fit(maturities, rates, alpha, omega), point)

    if gap(ALPHA_MIN) <= tolerance:
        return _fit(maturities, rates, ALPHA_MIN, omega)

    lo, hi = ALPHA_MIN, 1.0
    while gap(hi) > tolerance:
        lo, hi = hi, hi * 2
        if hi > 100:
            raise RuntimeError("α introuvable : la courbe ne converge pas vers l'UFR")
    # Bissection : la convergence s'améliore quand α augmente.
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if gap(mid) <= tolerance else (mid, hi)
        if hi - lo < 1e-8:
            break
    return _fit(maturities, rates, hi, omega)
