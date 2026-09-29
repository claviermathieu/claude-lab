Trois erreurs identifiées dans le calcul du SCR marché.

## 1. Choc actions Type 2 : 39 % au lieu de 49 %
Le choc actions Type 2 (non cotées, fonds, hors EEE/OCDE) est de **49 %** en formule standard (Art. 168 du règlement délégué), pas 39 %. Seul le Type 1 est à 39 %.

- SCR Type 2 correct = 50,0 × 49 % = **24,5** (au lieu de 19,5)
- SCR actions correct = √(78,0² + 2×0,75×78,0×24,5 + 24,5²) = **97,7** (au lieu de 93,5)

## 2. Choc immobilier : 20 % au lieu de 25 %
Le choc réglementaire immobilier en formule standard est de **25 %** (Art. 174), pas 20 %.

- SCR immo correct = 150,0 × 25 % = **37,5** (au lieu de 30,0)

## 3. Paramètre A de corrélation : 0,5 au lieu de 0
C'est l'erreur la plus significative. Le paramètre A dans la matrice de corrélation (Art. 164) dépend du scénario de taux retenu :
- A = 0 si le scénario **hausse** est le plus pénalisant,
- A = 0,5 si c'est le scénario **baisse**.

Ici, le SCR taux retenu correspond au scénario à la baisse (65,0 > 42,0). Le paramètre A doit donc être **0,5**, pas 0. Cela change les corrélations Taux-Actions, Taux-Immo et Taux-Spread, qui passent de 0 à 0,5 (Taux-Devise reste à 0,25 et Taux-Concentration à 0, ces deux-là ne dépendent pas de A).

## Recalcul avec les 3 corrections

| Module | SCR corrigé |
|---|---|
| Taux | 65,0 |
| Actions | 97,7 |
| Immo | 37,5 |
| Spread | 40,0 |
| Devise | 12,0 |
| Concentration | 5,0 |
| **Somme** | **257,2** |

Avec la matrice à A = 0,5 :

**SCR marché ≈ 206,5 M€** (au lieu de 167,4 M€), soit un écart de **+39,1 M€ (+23 %)**.

Bénéfice de diversification recalculé : 257,2 − 206,5 = 50,7 (19,7 %, contre 31,8 % annoncé — logique, la diversification est mécaniquement réduite quand A passe de 0 à 0,5).

La conclusion ("hausse de 3 % vs N-1") est donc à revoir puisqu'elle repose sur le chiffre de 167,4 M€, qui est sous-estimé.
