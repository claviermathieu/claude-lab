# Erreurs identifiées

| # | Section | Constat | Référence | Correction |
|---|---|---|---|---|
| 1 | 2. Actions | Choc actions type 2 (non cotées/fonds) appliqué à 39 %, soit le choc type 1 | Règl. délégué (UE) 2015/35, art. 169 — choc type 2 = 49 % (+ SA) | SCR type 2 = 50,0 × 49 % = **24,5** (au lieu de 19,5) → SCR actions agrégé = **97,7** (au lieu de 93,5) |
| 2 | 3. Immobilier | Choc immobilier appliqué à 20 % | Art. 174 — choc property = 25 % | SCR immo = 150,0 × 25 % = **37,5** (au lieu de 30,0) |
| 3 | 5. Agrégation | Corrélations Taux/Actions, Taux/Immo, Taux/Spread fixées à 0, alors que le scénario "baisse des taux" (le plus pénalisant) a été retenu pour SCR taux | Art. 164 — lorsque le scénario baisse est le plus sévère, ces corrélations valent 0,5 (matrice "CorrDown"), et non 0 (matrice "CorrUp") | Remplacer 0 par **0,5** pour ces trois couples dans la matrice |

Vérification : la formule d'agrégation et l'arithmétique de la note sont correctes compte tenu de ses propres paramètres (recalcul confirme 167,4) — les écarts viennent uniquement des trois paramètres ci-dessus, pas de la méthode de calcul.

# Points d'attention

- Les deux scénarios de taux (hausse et baisse) produisent une perte de fonds propres : possible mais atypique pour un profil ALM classique — à vérifier auprès de l'équipe modèle (convexité, duration gap).
- SCR spread (40,0), devise (12,0) et concentration (5,0) sont repris "des calculs détaillés" sans support fourni : non auditables en l'état, à joindre en annexe pour le contrôle de second niveau.
- La hausse de 3 % vs 31/12/2024 n'est pas vérifiable sans les chiffres N-1.
- L'ajustement symétrique à 0 % est annoncé comme simplification (donc pas une erreur ici), mais s'assurer que la valeur réelle publiée par l'EIOPA au 31/12/2025 est utilisée dans la version finale du rapport ORSA.

# SCR marché corrigé

**≈ 206,5 M€**, contre 167,4 M€ dans la note — écart de **+39,1 M€ (+23,4 %)**.
