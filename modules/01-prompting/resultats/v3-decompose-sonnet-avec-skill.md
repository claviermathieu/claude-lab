<analyse>

**1. Chocs**
- Taux : SCR = max(42 ; 65) = 65, ce qui est correct. Les chocs par maturité (art. 166-167) ne sont pas vérifiables à partir de la note, car seuls les résultats sont fournis.
- Actions type 1 : 39 % + SA (SA = 0 annoncé), soit 200 × 39 % = 78,0. C'est conforme à l'art. 169 §1 a).
- Actions type 2 : la note applique 39 %, alors que l'art. 169 §1 b) fixe 49 % + SA. Le SCR type 2 vaut donc 50 × 49 % = 24,5, et non 19,5. **Erreur.**
- Immobilier : la note applique 20 %, alors que l'art. 174 fixe 25 %. Le SCR vaut 150 × 25 % = 37,5, et non 30,0. **Erreur.**
- Spread, devise et concentration sont repris des calculs détaillés. Ils ne sont pas recalculables ici.

**2. Agrégation intra-actions**
- La corrélation de 0,75 entre type 1 et type 2 est conforme.
- Avec les bons chocs : √(78² + 2×0,75×78×24,5 + 24,5²) = √(6 084 + 2 866,5 + 600,25) = √9 550,75 = **97,7**.
- La note donne 93,5. Son arithmétique est juste avec ses propres chocs, mais ceux-ci sont faux.

**3. Matrice inter-modules**
- Le scénario retenu pour les taux est la baisse (65 > 42), donc **A = 0,5** (art. 164). La note utilise A = 0, ce qui correspond au scénario à la hausse. **Erreur.**
- Les autres coefficients sont conformes : 0,75 (actions/immo, actions/spread), 0,5 (immo/spread), 0,25 (devise avec taux, actions, immo et spread) et 0 pour la concentration.
- Les cellules taux/actions, taux/immo et taux/spread doivent valoir 0,5 et non 0.

**4. Recalcul** avec S = [65 ; 97,7 ; 37,5 ; 40 ; 12 ; 5].
- Somme des SCR = 257,2.
- Termes diagonaux : 4 225 + 9 550,75 + 1 406,25 + 1 600 + 144 + 25 = 16 951.
- Termes croisés, pris deux fois :

| Paire | Coefficient | Valeur (une fois) |
|---|---|---|
| Taux / actions | 0,5 | 3 176 |
| Taux / immo | 0,5 | 1 219 |
| Taux / spread | 0,5 | 1 300 |
| Taux / devise | 0,25 | 195 |
| Actions / immo | 0,75 | 2 749 |
| Actions / spread | 0,75 | 2 932 |
| Actions / devise | 0,25 | 293 |
| Immo / spread | 0,5 | 750 |
| Immo / devise | 0,25 | 113 |
| Spread / devise | 0,25 | 120 |

  Le total est 12 847 (un seul passage), soit 25 693 en doublant.
- SCR marché = √(16 951 + 25 693) = √42 644 = **206,5**. Le script `scr_marche.py` donne le même résultat (206,5).
- Diversification = 257,2 − 206,5 = 50,7, soit 19,7 %.

Décomposition de l'écart, en séquence :

| Étape | SCR marché |
|---|---|
| Note (A = 0, type 2 à 39 %, immo à 20 %) | 167,4 |
| Type 2 corrigé à 49 % | 171,2 (+3,8) |
| Immobilier corrigé à 25 % | 176,8 (+5,6) |
| A = 0,5 | 206,5 (+29,7) |

**5. Contre-vérification**
- SA = 0 % est une hypothèse annoncée, donc pas une erreur. Je la mets en point d'attention.
- Le calcul de la diversification de la note (78,1 ; 31,8 %) est cohérent avec ses propres chiffres.
- Le classement des « fonds » en type 2 est cohérent avec l'art. 169 §1 b), à condition qu'ils ne soient pas transparisés (art. 84). Je ne le retiens pas comme erreur.
- Le max des chocs de taux est bien appliqué.
</analyse>

<rapport>
**1. Erreurs certaines**

| # | Section | Constat | Référence | Correction | Impact |
|---|---|---|---|---|---|
| 1 | §2 Actions type 2 | Choc de 39 % appliqué au lieu de 49 % (+ SA) | RD art. 169 §1 b) | 50 × 49 % = 24,5, puis SCR actions = 97,7 | Type 2 : +5,0. Actions : +4,2. SCR marché : +3,8 |
| 2 | §3 Immobilier | Choc de 20 % appliqué au lieu de 25 % | RD art. 174 | 150 × 25 % = 37,5 | Immobilier : +7,5. SCR marché : +5,6 |
| 3 | §5 Matrice | A = 0 alors que le scénario de taux retenu est la baisse (65 > 42). Les cellules taux/actions, taux/immo et taux/spread valent 0 au lieu de 0,5 | RD art. 164 | A = 0,5 | SCR marché : +29,7 (le plus lourd) |
| 4 | Conclusion | Le « +3 % vs 31/12/2024 » découle du chiffre erroné | — | À recalculer sur base corrigée | Voir point d'attention 3 |

**2. Points d'attention (non bloquants)**
1. **SA = 0 %** : hypothèse annoncée, donc pas une erreur. Pour un rapport ORSA soumis à l'ACPR, il faut justifier l'écart avec la valeur EIOPA publiée au 31/12/2025 (borne ±10 %). Le SA s'ajoute aux deux chocs actions (39 % + SA et 49 % + SA), donc un SA non nul augmenterait ou réduirait le SCR actions. Je n'ai pas vérifié la valeur publiée.
2. **Sous-modules non recalculables** : les chocs de taux par maturité (art. 166-167), le spread (40,0), la devise (12,0) et la concentration (5,0) sont repris tels quels. Ils demandent un contrôle sur les calculs détaillés. Pour la devise, le choc de 25 % ou les taux réduits (art. 188) dépendent des devises concernées.
3. **Comparaison N-1** : si le SCR au 31/12/2024 était bien de ≈ 162,5 (167,4 / 1,03), le chiffre corrigé de 206,5 représenterait environ +27 %, et non +3 %. Cette évolution doit être réexpliquée (ou la base N-1 contrôlée, car elle peut porter les mêmes erreurs de paramétrage).
4. **Classement type 2** : les fonds doivent être non transparisés pour rester en type 2. Une transparisation (art. 84) déplacerait une partie de l'exposition vers les autres sous-modules.
5. **Sous-modules absents** : la note ne traite ni participations stratégiques, ni infrastructures, ni actions de long terme. Il faut confirmer qu'aucune exposition n'y est éligible.

**3. SCR marché corrigé**
- **206,5 M€** contre 167,4 M€ dans la note.
- Écart : **+39,1 M€, soit +23,4 %** (sous-évaluation de 18,9 % du chiffre corrigé).
- Décomposition : SCR taux 65,0 ; actions 97,7 ; immobilier 37,5 ; spread 40,0 ; devise 12,0 ; concentration 5,0.
- Somme des sous-modules : 257,2. Diversification : 50,7 (19,7 %), contre 31,8 % annoncé.
- La note ne peut pas être diffusée en l'état.
</rapport>
