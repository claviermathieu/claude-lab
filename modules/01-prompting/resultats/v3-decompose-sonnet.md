<analyse>

**1. Chocs réglementaires par sous-module**

- **Taux** : la note prend l'output déjà agrégé (variations de fonds propres −42,0 / −65,0) et retient le scénario le plus pénalisant (65,0, baisse). C'est conforme à l'art. 166 du règlement délégué (SCR taux = max(SCR_up ; SCR_down ; 0)). Pas d'erreur, pas de moyen de recalculer le choc lui-même faute de la courbe des taux détaillée — accepté comme donné.

- **Actions type 1** : 39 % avant ajustement symétrique — conforme à l'art. 168(3). L'hypothèse SA = 0 % est explicitement annoncée comme simplification : je ne la traite pas comme erreur (cf. étape 5 de la méthode), mais je la signale en point d'attention.

- **Actions type 2** : la note applique **39 %**, alors que l'art. 168(3) fixe le choc type 2 (actions non cotées EEE/OCDE, fonds, private equity, hedge funds…) à **49 %** avant ajustement symétrique. C'est une erreur certaine, pas une convention — le règlement fixe un taux différent selon le type, ce n'est pas un choix méthodologique.

- **Immobilier** : la note applique **20 %**, alors que l'art. 174 fixe le choc property à **25 %**. Erreur certaine.

- **Spread, devise, concentration** : repris de calculs détaillés non fournis dans la note — non vérifiables ici, acceptés tels quels.

**2. Agrégation intra-module actions**

Corrélation type1/type2 = 0,75 : conforme à l'art. 168(6). Pas d'erreur sur ce point — seul le choc type 2 est faux (voir ci-dessus).

**3. Matrice inter-modules et paramètre A**

Le paramètre A (corrélation taux × actions/immo/spread) dépend du scénario de taux retenu : A = 0 si le scénario baisse est contraignant, A = 0,5 si c'est le scénario hausse (Annexe IV, art. 164). Ici le scénario baisse est retenu (65,0 > 42,0) → **A = 0 est correct**. Je vérifie chaque coefficient de la matrice fournie (taux-devise 0,25 ; actions-immo 0,75 ; actions-spread 0,75 ; actions-devise 0,25 ; immo-spread 0,5 ; immo-devise 0,25 ; spread-devise 0,25 ; tout ce qui touche à la concentration = 0) : conforme à l'annexe IV pour A = 0. **Pas d'erreur sur la matrice.**

**4. Recalcul**

SCR actions corrigé :
Type 2 = 50,0 × 49 % = 24,5 (au lieu de 19,5)
SCR actions = √(78,0² + 2×0,75×78,0×24,5 + 24,5²) = √9550,75 ≈ **97,7**

SCR immobilier corrigé :
150,0 × 25 % = **37,5**

Sous-modules corrigés : Taux 65,0 / Actions 97,7 / Immo 37,5 / Spread 40,0 / Devise 12,0 / Concentration 5,0
Somme brute = 257,2

Agrégation (même matrice, vérifiée conforme) :
Termes diagonaux : 65²+97,7²+37,5²+40²+12²+5² = 16 951
Termes croisés (×2×corr×SCRi×SCRj) :
- taux-devise (0,25) : 390,0
- actions-immo (0,75) : 5 497,2
- actions-spread (0,75) : 5 863,7
- actions-devise (0,25) : 586,4
- immo-spread (0,5) : 1 500,0
- immo-devise (0,25) : 225,0
- spread-devise (0,25) : 240,0
Total croisés ≈ 14 302,3

Somme totale ≈ 31 253,2 → SCR marché corrigé = √31 253,2 ≈ **176,8**

Vérification arithmétique : j'ai recalculé la version originale de la note (167,4) avec ses propres inputs erronés — l'agrégation matricielle était correcte, seuls les chocs actions type 2 et immobilier sont faux. L'écart provient donc uniquement de ces deux paramètres, pas d'une erreur d'agrégation supplémentaire.

**5. Contre-vérification**

- SA actions = 0 % : hypothèse annoncée → non retenu comme erreur, mais à signaler.
- Choix du scénario taux (baisse) et paramètre A = 0 : conforme, vérifié, pas d'erreur.
- Comparaison "+3 % vs 31/12/2024" : aucune donnée 2024 fournie dans la note pour l'auditer → point d'attention, pas une erreur au sens strict (pas de base de comparaison à contredire).

</analyse>

<rapport>

**1. Erreurs certaines**

| # | Section | Constat | Référence | Correction | Impact |
|---|---|---|---|---|---|
| 1 | Actions type 2 | Choc de 39 % appliqué au lieu de 49 % (choc type 1 utilisé à tort pour le type 2) | Art. 168(3), règl. délégué (UE) 2015/35 | 50,0 × 49 % = 24,5 → SCR actions = √(78,0²+2×0,75×78,0×24,5+24,5²) = 97,7 | SCR actions : 93,5 → 97,7 (+4,2) |
| 2 | Immobilier | Choc de 20 % appliqué au lieu de 25 % | Art. 174, règl. délégué (UE) 2015/35 | 150,0 × 25 % = 37,5 | SCR immo : 30,0 → 37,5 (+7,5) |

**2. Points d'attention (non bloquants)**

- **Ajustement symétrique actions fixé à 0 %** : hypothèse de simplification explicitement annoncée, donc non traitée comme erreur ici. Pour la version diffusée à l'ACPR, remplacer par la valeur EIOPA effectivement publiée au 31/12/2025 (le SA s'applique aux deux types d'actions, art. 172) et indiquer la sensibilité si elle diffère de 0.
- **Sous-modules spread (40,0), devise (12,0) et concentration (5,0)** repris sans détail de calcul dans la note : à documenter en annexe pour permettre l'audit complet par le second niveau / l'ACPR.
- **Comparaison "+3 % vs 31/12/2024"** : aucune donnée du 31/12/2024 n'est fournie dans la note pour vérifier cette variation ; à sourcer explicitement.
- Le paramètre A de la matrice de corrélation (dépendant du scénario de taux) et la matrice inter-modules ont été vérifiés poste par poste et sont conformes à l'annexe IV (scénario baisse retenu → A = 0) — point de vigilance récurrent bien traité ici, à reconfirmer si le scénario taux dominant change à une prochaine clôture.

**3. SCR marché corrigé**

SCR marché corrigé ≈ **176,8 M€** (vs 167,4 M€ dans la note)
Écart : **+9,4 M€, soit +5,6 %**

</rapport>
