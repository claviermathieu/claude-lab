"""Démo : python -m eiopa_curve (depuis modules/02-claude-code-bases)."""

from .smith_wilson import calibrate, convergence_point

# Courbe swap EUR fictive (points liquides 1–20 ans), UFR 3,30 %, CRA 10 bp.
MATURITIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20]
SWAP_RATES = [
    0.0215, 0.0212, 0.0214, 0.0218, 0.0223, 0.0228, 0.0233,
    0.0238, 0.0242, 0.0246, 0.0252, 0.0258, 0.0260,
]  # fmt: skip

curve = calibrate(MATURITIES, SWAP_RATES, ufr=0.033, cra_bp=10)
cp = convergence_point(MATURITIES[-1])
print(f"alpha = {curve.alpha:.4f}   UFR = {curve.ufr:.2%}   point de convergence = {cp:.0f} ans")
print(f"écart forward au CP = {abs(curve.forward_intensity(cp)[0] - curve.omega) * 1e4:.3f} bp\n")
print(" maturité   spot   forward 1a")
for t in [1, 5, 10, 20, 30, 40, 50, 60, 80, 100, 150]:
    print(f"{t:8d}  {curve.spot(t)[0]:6.3%}  {curve.forward_annual(t)[0]:6.3%}")
