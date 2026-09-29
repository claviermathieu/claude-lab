import numpy as np
import pytest
from eiopa_curve import calibrate, convergence_point, wilson
from eiopa_curve.smith_wilson import ALPHA_MIN, CONVERGENCE_TOLERANCE, _fit, convergence_gap

MATURITIES = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20], dtype=float)
RATES = np.array(
    [0.0215, 0.0212, 0.0214, 0.0218, 0.0223, 0.0228, 0.0233,
     0.0238, 0.0242, 0.0246, 0.0252, 0.0258, 0.0260]
)  # fmt: skip
UFR = 0.033


@pytest.fixture(scope="module")
def curve():
    return calibrate(MATURITIES, RATES, ufr=UFR)


def test_reproduit_les_taux_aux_points_liquides(curve):
    np.testing.assert_allclose(curve.spot(MATURITIES), RATES, atol=1e-12)


def test_cra_retranche_des_taux_d_entree():
    c = calibrate(MATURITIES, RATES, ufr=UFR, cra_bp=10)
    np.testing.assert_allclose(c.spot(MATURITIES), RATES - 0.0010, atol=1e-12)


def test_convergence_a_1bp_au_point_de_convergence(curve):
    assert convergence_gap(curve, convergence_point(20)) <= CONVERGENCE_TOLERANCE


def test_alpha_minimal(curve):
    """α est le plus petit respectant le critère (ou le plancher 0,05)."""
    assert curve.alpha >= ALPHA_MIN
    if curve.alpha > ALPHA_MIN:
        juste_en_dessous = _fit(MATURITIES, RATES, curve.alpha * 0.99, curve.omega)
        assert convergence_gap(juste_en_dessous, convergence_point(20)) > CONVERGENCE_TOLERANCE


def test_courbe_longue_tend_vers_ufr(curve):
    assert curve.forward_annual(150)[0] == pytest.approx(UFR, abs=1e-5)
    # Le spot converge plus lentement que le forward mais va dans le bon sens.
    assert abs(curve.spot(150)[0] - UFR) < abs(curve.spot(60)[0] - UFR)


def test_intensite_forward_coherente_avec_differences_finies(curve):
    t, h = 45.0, 1e-4
    numerique = -(np.log(curve.discount(t + h)) - np.log(curve.discount(t - h))) / (2 * h)
    assert curve.forward_intensity(t)[0] == pytest.approx(numerique[0], abs=1e-8)


def test_matrice_wilson_symetrique_definie_positive():
    w = wilson(MATURITIES, MATURITIES, 0.1, np.log1p(UFR))
    np.testing.assert_allclose(w, w.T)
    assert np.all(np.linalg.eigvalsh(w) > 0)


def test_point_de_convergence_eiopa():
    assert convergence_point(20) == 60
    assert convergence_point(50) == 90


@pytest.mark.parametrize(
    "maturities, rates",
    [
        ([1, 2], [0.02]),
        ([2, 1], [0.02, 0.02]),
        ([0, 1], [0.02, 0.02]),
        ([], []),
        ([1, 2], [0.02, float("nan")]),
        ([1, 2], [0.02, -1.5]),
    ],
)
def test_entrees_invalides(maturities, rates):
    with pytest.raises(ValueError):
        calibrate(maturities, rates, ufr=UFR)


def test_forward_intensity_refuse_maturite_courte(curve):
    with pytest.raises(ValueError):
        curve.forward_intensity(10)


def test_llp_50_stable_numeriquement():
    """LLP 50 ans (type GBP/USD) : point de convergence 90 ans, pas de dépassement."""
    maturities = np.array([1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50], dtype=float)
    rates = np.linspace(0.035, 0.041, maturities.size)
    c = calibrate(maturities, rates, ufr=UFR)
    assert np.all(np.isfinite(c.spot(np.arange(1, 151))))
    np.testing.assert_allclose(c.spot(maturities), rates, atol=1e-10)
    assert convergence_gap(c, convergence_point(50)) <= CONVERGENCE_TOLERANCE


def test_wilson_grand_alpha_sans_nan():
    w = wilson(np.array([50.0]), np.array([50.0]), 20.0, np.log1p(UFR))
    assert np.all(np.isfinite(w))
