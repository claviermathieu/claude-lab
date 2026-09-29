# Note de calcul — SCR marché au 31/12/2025 (formule standard)

Entité : Mutuelle Exemple SA. Montants en M€. Ajustement symétrique actions (SA) au 31/12/2025 pris égal à 0 % pour simplifier.

## 1. Sous-module taux
| Scénario | Variation des fonds propres |
|---|---|
| Choc à la hausse | −42,0 |
| Choc à la baisse | −65,0 |

SCR taux retenu = max(42,0 ; 65,0) = **65,0** (scénario à la baisse).

## 2. Sous-module actions
| Type | Exposition | Choc appliqué | SCR |
|---|---|---|---|
| Type 1 (actions cotées EEE/OCDE) | 200,0 | 39 % | 78,0 |
| Type 2 (non cotées, fonds) | 50,0 | 39 % | 19,5 |

Agrégation avec corrélation type 1 / type 2 de 0,75 :
SCR actions = √(78,0² + 2 × 0,75 × 78,0 × 19,5 + 19,5²) = **93,5**

## 3. Sous-module immobilier
Exposition immobilière 150,0 × choc 20 % = **30,0**

## 4. Autres sous-modules (repris des calculs détaillés)
- SCR spread = **40,0**
- SCR devise = **12,0**
- SCR concentration = **5,0**

## 5. Agrégation
Matrice de corrélation utilisée (paramètre A = 0) :

|  | Taux | Actions | Immo | Spread | Devise | Concentr. |
|---|---|---|---|---|---|---|
| Taux | 1 | 0 | 0 | 0 | 0,25 | 0 |
| Actions | 0 | 1 | 0,75 | 0,75 | 0,25 | 0 |
| Immo | 0 | 0,75 | 1 | 0,5 | 0,25 | 0 |
| Spread | 0 | 0,75 | 0,5 | 1 | 0,25 | 0 |
| Devise | 0,25 | 0,25 | 0,25 | 0,25 | 1 | 0 |
| Concentr. | 0 | 0 | 0 | 0 | 0 | 1 |

Somme des sous-modules : 245,5
SCR marché = √(Σ Corr(i,j) × SCRᵢ × SCRⱼ) = **167,4**

Bénéfice de diversification : 245,5 − 167,4 = 78,1 (31,8 %).

Conclusion : le SCR marché s'établit à 167,4 M€, en hausse de 3 % par rapport au 31/12/2024.
