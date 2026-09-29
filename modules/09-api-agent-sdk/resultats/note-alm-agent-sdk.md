# Note ALM — risque de taux

*Arrêté : bilan économique fourni (M€). Données : `obligations.parquet` (DVC 0ed5d119), `flux_passif.parquet` (DVC 2266e3ae). Le fichier `bilan.csv` du dépôt est identique au bilan transmis.*

## Synthèse (3 lignes)
1. L'exposition au risque de taux est faible : un choc de ±100 pb fait varier les fonds propres économiques de moins de 6,0 M€ dans les deux calculs ci‑dessous.
2. **On ne connaît pas le sens de l'exposition.** Avec les montants du bilan, le duration gap est de **−0,40**. Avec les valeurs recalculées par les outils, il est de **+0,65**. Le signe s'inverse.
3. Cette incertitude vient d'un écart entre les sources : le best estimate du bilan vaut 805,0 M€, mais les flux de passif actualisés ne donnent que 659,4 M€, soit 145,6 M€ de moins. Il faut réconcilier ces chiffres avant toute décision de couverture.

## Données et hypothèses

**Bilan**

| Actif | M€ | Poids | | Passif | M€ |
|---|---|---|---|---|---|
| Obligations | 770,0 | 81,5 % | | Best estimate | 805,0 |
| Actions | 90,0 | 9,5 % | | Marge de risque | 20,0 |
| Immobilier | 60,0 | 6,3 % | | Autres passifs | 15,0 |
| Trésorerie | 25,0 | 2,6 % | | **Total passif** | **840,0** |
| **Total actif** | **945,0** | | | **Fonds propres économiques** | **105,0** |

**Résultats des outils**

| Élément | Valeur | Duration Macaulay | Duration modifiée | Convexité |
|---|---|---|---|---|
| Portefeuille obligataire (40 titres, taux de rendement propre à chaque titre) | 731,4 M€ | 9,27 | 8,98 | 139,5 |
| Flux de passif (40 ans, taux plat de 3 %) | 659,4 M€ | 9,33 | 9,06 | 153,6 |

**Écarts entre sources**
- **Obligations :** 770,0 M€ au bilan contre 731,4 M€ recalculés, soit 38,6 M€ de plus au bilan (+5,3 %).
- **Best estimate :** 805,0 M€ au bilan contre 659,4 M€ de flux actualisés, soit 145,6 M€ de plus au bilan (+22,1 %). Les causes possibles sont :
  - une courbe d'actualisation différente (courbe réglementaire plutôt que 3 % plat) ;
  - des options et de la participation aux bénéfices non incluses dans les flux déterministes ;
  - un périmètre ou une date d'arrêté différents.
  
  Aucune de ces causes ne peut être vérifiée avec les données disponibles.

**Hypothèses de calcul**
- Seules les obligations et le best estimate sont sensibles aux taux. Actions, immobilier, trésorerie, marge de risque et autres passifs ont une duration nulle. C'est une hypothèse simplificatrice : leurs durations réelles ne sont pas disponibles.
- On utilise les durations modifiées.
- Deux calculs sont présentés :
  - **A : montants du bilan.** VM_A = 945,0 ; obligations = 770,0 ; VA_P = 805,0.
  - **B : valeurs des outils.** VM_A = 731,4 + 90,0 + 60,0 + 25,0 = 906,4 ; VA_P = 659,4. Dans ce calcul, les fonds propres reconstitués valent 212,0 M€ (906,4 − 659,4 − 20,0 − 15,0).

## Duration gap et sensibilités

**Duration gap = D_A − D_P × (VA_P / VM_A)**

| | Calcul A (bilan) | Calcul B (outils) |
|---|---|---|
| D_A sur tout l'actif (8,98 × obligations / VM_A) | 7,31 | 7,24 |
| D_P × VA_P / VM_A | 7,72 | 6,59 |
| **Duration gap** | **−0,40** | **+0,65** |

**Impact d'un choc parallèle sur les fonds propres économiques (M€)**

| Choc | | Δ Obligations | Δ Best estimate | **Δ Fonds propres** | % des fonds propres |
|---|---|---|---|---|---|
| **A : +100 pb** | 1er ordre | −69,1 | −72,9 | **+3,8** | +3,6 % |
| | avec convexité | −63,7 | −66,7 | **+3,0** | +2,8 % |
| **A : −100 pb** | 1er ordre | +69,1 | +72,9 | **−3,8** | −3,6 % |
| | avec convexité | +74,5 | +79,1 | **−4,6** | −4,4 % |
| **B : +100 pb** | 1er ordre | −65,7 | −59,7 | **−5,9** | −2,8 % |
| | avec convexité | −60,6 | −54,7 | **−5,9** | −2,8 % |
| **B : −100 pb** | 1er ordre | +65,7 | +59,7 | **+5,9** | +2,8 % |
| | avec convexité | +70,8 | +64,8 | **+6,0** | +2,8 % |

Les résultats du calcul B pour les obligations (−60,6 et +70,8) correspondent aux sensibilités renvoyées par l'outil (−60,55 et +70,76).

**Lecture**
- Les durations modifiées de l'actif obligataire (8,98) et du passif (9,06) sont presque égales. Le signe du gap dépend donc surtout des montants retenus pour le passif et les obligations.
- Calcul A : le passif pèse plus que les obligations. La société perd quand les taux baissent.
- Calcul B : c'est l'inverse. La société perd quand les taux montent.
- La convexité du passif (153,6) est plus forte que celle de l'actif (139,5). Dans le calcul A, l'effet net de convexité est donc défavorable (−0,8 M€) dans les deux sens de choc.

## Limites
- **Réconciliation :** l'écart de 145,6 M€ sur le best estimate et de 38,6 M€ sur les obligations rend le signe du gap incertain. C'est la principale limite de l'analyse.
- **Taux d'actualisation :** le passif est actualisé à 3 % plat, alors que les obligations sont valorisées avec le rendement propre à chaque titre. Les deux côtés ne reposent donc pas sur la même courbe. La courbe réglementaire n'est pas disponible.
- **Flux de passif :** ils sont déterministes. Les rachats dynamiques, la participation aux bénéfices et les garanties de taux ne sont pas modélisés. Or, en cas de hausse des taux, les rachats peuvent réduire la duration effective du passif.
- **Type de choc :** seuls des chocs parallèles sont analysés. La sensibilité par maturité, la pentification et l'effet des spreads de crédit ne sont pas disponibles.
- **Autres postes :** actions, immobilier, marge de risque et autres passifs sont supposés insensibles aux taux. L'effet d'absorption par les impôts différés n'est pas pris en compte.

## Actions proposées
1. **Réconcilier les sources (en priorité).** Rapprocher le best estimate du bilan (805,0) des flux actualisés (659,4), et la valeur de marché obligataire du bilan (770,0) de la valeur recalculée (731,4) : courbe, périmètre, date d'arrêté, options. Ensuite, refaire le calcul du gap avec une seule courbe pour l'actif et le passif.
2. **Compléter les mesures de sensibilité.** Calculer la sensibilité par maturité, appliquer des chocs de pente et les chocs réglementaires du capital de solvabilité pour le risque de taux, et utiliser des flux de passif intégrant les rachats dynamiques. L'objectif est de vérifier que l'exposition reste faible hors choc parallèle.
3. **Piloter selon le résultat de la réconciliation, dans une bande de gap fixée par le comité.**
   - Si le calcul A est confirmé (gap négatif) : allonger légèrement l'actif, par des obligations longues ou des swaps où l'on reçoit le taux fixe.
   - Si le calcul B est confirmé (gap positif) : raccourcir légèrement.
   
   Dans les deux cas, les montants en jeu restent limités (< 6,0 M€ pour ±100 pb). Aucune couverture n'est recommandée avant la fin de la réconciliation.