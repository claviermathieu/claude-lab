## Rapport du valideur (`model-validator`)

**Verdict : validé avec réserves.** L'implémentation Smith-Wilson est juste pour la méthode en vigueur jusqu'au 29/01/2027. Deux réglages ne permettent pas de reproduire une courbe EIOPA publiée : la CRA vaut 0 par défaut, et les entrées sont traitées comme des taux zéro-coupon, pas comme des swaps au pair. La méthode LLFR/FSP issue de la révision de Solvabilité II n'est pas couverte.

**Conforme**
- La fonction de Wilson (`smith_wilson.py:27`) est correcte. ω = ln(1+UFR) et la conversion des taux en composition annuelle sont cohérentes.
- La dérivée analytique de l'intensité forward (`:66-71`) est correcte. Elle redonne l'écart |f(T) − ω| = α/|1 − κe^{αT}| de la documentation technique EIOPA.
- Le point de convergence max(LLP + 40, 60) et la tolérance de 1 bp sont conformes.
- La recherche de α (plancher à 0,05, puis bissection qui renvoie la borne `hi`) respecte le critère et la règle du « plus petit α ≥ 0,05 ».
- Les points liquides de la démo correspondent au jeu DLT de l'EUR.

**Constats**

| # | Gravité | Fichier:ligne | Constat | Référence | Correction proposée |
|---|---|---|---|---|---|
| 1 | majeur | `smith_wilson.py:99` | `cra_bp=0.0` par défaut : la courbe est calibrée sans CRA, donc taux trop élevés et BE sous-estimé. La fixture de test (`test_smith_wilson.py:16`) calibre aussi sans CRA. Aucun contrôle de bornes. | Directive 2009/138 art. 77a ; RD 2015/35 art. 45 (bornes 10-35 bp) | Rendre `cra_bp` obligatoire ou le mettre par défaut à 10 bp pour l'EUR. Avertir ou lever une erreur hors de [10, 35] bp, sauf `allow_out_of_bounds`. |
| 2 | majeur | `__main__.py:7`, `smith_wilson.py:80,111` | La variable s'appelle `SWAP_RATES`, mais les taux sont traités comme des zéro-coupon. L'EIOPA calibre sur des swaps au pair (matrice de flux C, m = prix 1) et retranche la CRA des taux au pair. Avec des taux swap publiés, la courbe est fausse, et l'objectif du README (0,1 bp près) est inatteignable. | Documentation technique EIOPA RFR (données d'entrée, calibration Smith-Wilson) | Généraliser `_fit` à ζ = (QᵀWQ)⁻¹(m − Cᵀμ) avec C et m issus des taux au pair. Appliquer la CRA aux taux au pair. Renommer la variable de la démo `ZC_RATES` en attendant. |
| 3 | majeur (périmètre) | module entier | Seule la méthode Smith-Wilson historique est implémentée. La Directive (UE) 2025/2 modifie l'art. 77a et introduit à partir du 30/01/2027 le FSP, le LLFR, une convergence exponentielle et une phase transitoire. Une projection au-delà de cette date utiliserait une méthode obsolète. | Directive (UE) 2025/2, art. 77a modifié | Documenter la limite dans le docstring et le README. Prévoir une fonction `extrapolate_llfr(...)` séparée. |
| 4 | mineur | `smith_wilson.py:27,129-136` | Dépassement numérique de `exp(-α·hi)·sinh(α·lo)` dès α·u > ~710. Avec un LLP de 50 ans, cela arrive dès α ≈ 14. Le gap vaut NaN, `nan > tol` est faux, et la boucle s'arrête sans erreur en renvoyant des NaN. | Robustesse | Forme stable `0.5·(exp(-α(hi−lo)) − exp(-α(hi+lo)))`. Lever une erreur si `not np.isfinite(gap)`. |
| 5 | mineur | `smith_wilson.py:133-136` | La bissection suppose un gap décroissant en α, ce qui n'est pas garanti. Le α trouvé peut ne pas être le plus petit. | Documentation technique EIOPA | Balayer une grille grossière depuis 0,05, puis affiner par bissection. |
| 6 | mineur | `smith_wilson.py:54,110-117` | Taux ≤ −1 ou NaN non rejetés. P(t) ≤ 0 donne un spot NaN sans message. | Robustesse | Valider `np.isfinite(rates)` et `rates > -1`. Lever une erreur si `discount(t) <= 0`. |
| 7 | mineur | `smith_wilson.py:120` | Le LLP est pris égal à la dernière maturité fournie. Des points au-delà du LLP seraient utilisés dans la calibration. | Directive art. 77a | Ajouter un paramètre `llp` explicite et filtrer les maturités supérieures. |
| 8 | mineur | `smith_wilson.py:82` | `np.linalg.solve` sans contrôle du conditionnement de W (mal conditionnée pour α petit). | Robustesse numérique | Journaliser `cond(W)` ou utiliser `scipy.linalg.solve(..., assume_a="pos")`. |

**Tests manquants**
- Rejeu d'une courbe EIOPA officielle (EUR, sans VA) : taux et α à 0,1 bp près. C'est le seul test qui valide vraiment le résultat.
- CRA non nulle par défaut, et bornes 10-35 bp.
- Plancher α = 0,05 atteint (branche `:125-126`).
- Minimalité de α sur toute la plage [0,05 ; α], pas seulement à 0,99·α (`test_smith_wilson.py:36`).
- LLP = 50 (USD/GBP), convergence à 90 : stabilité numérique, pas de NaN.
- Taux négatifs et courbe inversée.
- `convergence_gap` comparé à la forme fermée α/|1 − κe^{αT}|.
- Invariants : P(0) = 1, `ufr` restitué, `convergence_period` ≠ 40, rejet de `ufr ≤ −1` et des NaN.
- Test de fumée de `__main__` (α = 0,103, forward à 100 ans = 3,300 %).

**Non vérifié par le valideur**
- Il n'a rien exécuté (outils en lecture seule). La justesse des formules est vérifiée analytiquement.
- Aucune comparaison avec une courbe EIOPA publiée : pas de fichier de référence dans le repo.
- `.claude/skills/` est vide. Les références viennent de sa mémoire et sont à confirmer avant tout usage officiel : n° d'articles du RD 2015/35, paramètres de la Directive 2025/2 (FSP, a, poids LLFR, phase-in), UFR EUR applicable en 2026.

## Tests

`uv run pytest -q` sur `eiopa_curve` collecte 0 test : les tests sont dans `modules/02-claude-code-bases/tests/`. Relancé sur ce dossier : **13 passed** en 0,07 s. Cela confirme le compte annoncé dans le README. Ces tests ne couvrent pas les cas listés ci-dessus.

## Suites proposées

1. Corriger la CRA (constat 1) : la rendre obligatoire ou à 10 bp par défaut, avec contrôle des bornes 10-35 bp, et l'ajouter aux tests.
2. Traiter les entrées en swaps au pair (constat 2) : généraliser `_fit` avec la matrice C, puis ajouter le test de rejeu d'une courbe EIOPA publiée à 0,1 bp près.
3. Corriger la stabilité numérique et la validation des entrées (constats 4 et 6) : forme stable de `sinh`, erreur sur gap non fini, garde sur taux NaN ou ≤ −1, et test LLP = 50.

Le périmètre LLFR/FSP (constat 3) est à documenter dans le README dès maintenant. Son implémentation peut attendre.