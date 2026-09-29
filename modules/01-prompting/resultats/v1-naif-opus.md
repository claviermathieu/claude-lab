## Erreurs de calcul

**1. Choc actions type 2 : 39 % au lieu de 49 %** (art. 169 du règlement délégué 2015/35)
Le type 2 subit un choc de **49 % + ajustement symétrique**, pas 39 %.
- SCR type 2 = 50,0 × 49 % = **24,5** (et non 19,5)
- SCR actions = √(78,0² + 2×0,75×78,0×24,5 + 24,5²) = √9 550,75 = **97,7** (et non 93,5)

**2. Choc immobilier : 20 % au lieu de 25 %** (art. 174)
Le choc immobilier standard est de 25 %, quel que soit le type de bien.
- SCR immobilier = 150,0 × 25 % = **37,5** (et non 30,0)

**3. Paramètre A mal positionné dans la matrice de corrélation** (art. 164)
A = 0 uniquement quand le SCR taux provient du **choc à la hausse**. Ici le choc à la baisse est retenu (65,0 > 42,0), donc **A = 0,5**. Les corrélations taux/actions, taux/immo et taux/spread valent 0,5, pas 0. C'est l'erreur la plus coûteuse : elle supprime tout le couplage entre le risque de taux et les trois plus gros sous-modules.

## Ce qui est correct
- Sélection du scénario taux le plus défavorable (max des pertes) ✓
- Corrélation type 1 / type 2 de 0,75 ✓
- Ligne/colonne concentration à 0 partout, taux/devise à 0,25 ✓
- L'arithmétique de l'agrégation est juste **compte tenu des intrants** : je retrouve bien 167,4 et 31,8 % de diversification.

## Recalcul corrigé

| Sous-module | Note | Corrigé |
|---|---|---|
| Taux | 65,0 | 65,0 |
| Actions | 93,5 | 97,7 |
| Immobilier | 30,0 | 37,5 |
| Spread | 40,0 | 40,0 |
| Devise | 12,0 | 12,0 |
| Concentration | 5,0 | 5,0 |
| **Somme** | 245,5 | **257,2** |
| **SCR marché** | **167,4** | **206,5** |
| Diversification | 78,1 (31,8 %) | 50,7 (19,7 %) |

Soit **+23 % par rapport au montant publié**. La conclusion « en hausse de 3 % par rapport au 31/12/2024 » tombe donc, sauf si le comparatif 2024 souffre des mêmes erreurs.

## Points à vérifier avant publication
- **Ajustement symétrique** : le poser à 0 % est présenté comme une simplification, mais il varie dans une bande de ±17 pp et s'applique aux deux types d'actions. Il faut la valeur EIOPA publiée pour décembre 2025 — l'impact sur le SCR actions se chiffre en dizaines de M€.
- **Classification du type 2** : si une partie des « non cotées / fonds » relève des participations stratégiques ou des investissements actions de long terme (choc 22 %), le traitement doit être documenté.
- **Revue Solvabilité II** : la refonte du sous-module taux (approche par décalage avec choc plancher) n'est pas applicable à l'arrêté 2025, mais mérite une mention en note prospective — vérifiez le calendrier d'entrée en vigueur retenu par votre place.
- La note ne précise pas si les montants sont nets ou bruts de la capacité d'absorption des provisions techniques ; à expliciter.
