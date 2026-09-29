<analyse>

**Étape 1 — Contrôle des chocs par sous-module**

*Taux (art. 165 à 167)* : la note présente deux scénarios, tous deux destructeurs de fonds propres (−42,0 et −65,0). Le SCR taux est le maximum des pertes de fonds propres de base entre le scénario de hausse et celui de baisse → 65,0, scénario **à la baisse**. Conforme. À noter pour l'étape 3 : c'est le scénario de baisse qui est retenu.

*Actions (art. 168 et 169)* :
- Type 1 : choc de 39 % + ajustement symétrique (art. 169(1)(a)). Avec SA = 0 % (hypothèse annoncée) → 200,0 × 39 % = 78,0. Conforme.
- Type 2 : le choc réglementaire est de **49 %** + ajustement symétrique (art. 169(1)(b)), et non 39 %. La note applique le choc de type 1 aux actions de type 2. **Erreur.** Correction : 50,0 × 49 % = 24,5.

*Immobilier (art. 174)* : le choc est une baisse instantanée de **25 %** de la valeur des biens immobiliers, et non 20 %. **Erreur.** Correction : 150,0 × 25 % = 37,5.

*Spread, devise, concentration* : repris des calculs détaillés non fournis, non vérifiables ici.

**Étape 2 — Agrégation intra-module actions**

La formule √(SCR₁² + 2 × 0,75 × SCR₁ × SCR₂ + SCR₂²) avec une corrélation de 0,75 entre type 1 et type 2 est bien celle de l'article 168. La structure de calcul est correcte ; seule l'entrée « type 2 » est fausse. L'arithmétique de la note est d'ailleurs exacte sur ses propres données (√8 745,75 = 93,5) — il ne faut donc pas signaler d'erreur de calcul ici.

Recalcul avec le choc correct :
- 78,0² = 6 084,00
- 24,5² = 600,25
- 2 × 0,75 × 78,0 × 24,5 = 1,5 × 1 911 = 2 866,50
- Somme = 9 550,75 → **SCR actions = 97,7** (au lieu de 93,5)

**Étape 3 — Matrice inter-modules (art. 164(3) et annexe IV)**

Vérification cellule par cellule contre l'annexe IV :
- Actions/Immo 0,75, Actions/Spread 0,75, Immo/Spread 0,5 : conformes.
- Devise 0,25 avec taux, actions, immo et spread : conforme (la corrélation taux/devise est fixée à 0,25, ce n'est pas le paramètre A).
- Concentration 0 avec tous les autres sous-modules : conforme.
- Taux/Actions, Taux/Immo, Taux/Spread = **A**. Le paramètre A vaut 0 lorsque le SCR taux résulte du scénario de **hausse** de la courbe, et **0,5** lorsqu'il résulte du scénario de **baisse** (art. 164(3)).

Or la note retient explicitement le scénario à la baisse (§1) tout en posant A = 0 (§5). Les deux affirmations sont incompatibles : A doit valoir **0,5**. La mention « paramètre A = 0 » n'est pas une hypothèse simplificatrice libre — c'est un paramètre déterminé par le règlement. **Erreur.**

**Étape 4 — Recalcul du SCR marché**

Sous-modules corrigés : Taux 65,0 ; Actions 97,7 ; Immo 37,5 ; Spread 40,0 ; Devise 12,0 ; Concentration 5,0. Somme = 257,2.

Carrés : 4 225,00 + 9 550,75 + 1 406,25 + 1 600,00 + 144,00 + 25,00 = **16 951,00**

Termes croisés (2 × ρ × SCRᵢ × SCRⱼ) :
- Taux/Actions : 2 × 0,5 × 65,0 × 97,73 = 6 352,3
- Taux/Immo : 2 × 0,5 × 65,0 × 37,5 = 2 437,5
- Taux/Spread : 2 × 0,5 × 65,0 × 40,0 = 2 600,0
- Taux/Devise : 2 × 0,25 × 65,0 × 12,0 = 390,0
- Actions/Immo : 2 × 0,75 × 97,73 × 37,5 = 5 497,2
- Actions/Spread : 2 × 0,75 × 97,73 × 40,0 = 5 863,7
- Actions/Devise : 2 × 0,25 × 97,73 × 12,0 = 586,4
- Immo/Spread : 2 × 0,5 × 37,5 × 40,0 = 1 500,0
- Immo/Devise : 2 × 0,25 × 37,5 × 12,0 = 225,0
- Spread/Devise : 2 × 0,25 × 40,0 × 12,0 = 240,0
- Tous les termes avec Concentration : 0

Somme des termes croisés = **25 692,1**
Total = 16 951,0 + 25 692,1 = 42 643,1 → **SCR marché = √42 643,1 = 206,5**

Décomposition de l'écart (effets non strictement additifs car la racine n'est pas linéaire) :
- Corrections de chocs seules (A maintenu à 0) : SCR marché = 176,8 → +9,4
- Correction de A seule (chocs erronés maintenus) : SCR marché = 196,6 → +29,2
- Effet combiné : +39,1

Diversification corrigée : 257,2 − 206,5 = 50,7, soit 19,7 % (contre 31,8 % annoncés — la baisse s'explique par le passage de A de 0 à 0,5).

**Étape 5 — Contre-vérification des constats (élimination des fausses alertes)**

- *Ajustement symétrique à 0 %* : explicitement annoncé comme hypothèse simplificatrice en tête de note. Ce n'est pas une erreur de méthode → **retiré** du tableau des erreurs, versé en point d'attention (le chiffre n'est pas diffusable en l'état).
- *SCR taux = max des deux scénarios* : conforme à l'art. 165, pas de sommation ni de moyenne → **retiré**.
- *Corrélation taux/devise = 0,25* : on pourrait croire à un oubli du paramètre A, mais l'annexe IV fixe bien 0,25 sur cette cellule indépendamment du scénario → **retiré**.
- *Arithmétique de l'agrégation finale (167,4)* : recalculée sur les données de la note, elle donne bien √28 024,8 = 167,4 → pas d'erreur de calcul, uniquement des erreurs de paramètres → **retiré**.
- *Somme 245,5 et diversification 78,1 / 31,8 %* : exactes sur les données de la note → **retiré**.
- *Chocs spread, devise, concentration* : non vérifiables faute des calculs détaillés → point d'attention, pas une erreur.

</analyse>

<rapport>

## 1. Erreurs certaines

| # | Section | Constat | Référence | Correction | Impact |
|---|---|---|---|---|---|
| 1 | §2 Actions – type 2 | Choc de 39 % appliqué aux actions de type 2 (choc de type 1) au lieu de 49 % | Art. 169(1)(b) du règlement délégué (UE) 2015/35 | 50,0 × 49 % = 24,5 ; SCR actions = √(78,0² + 2×0,75×78,0×24,5 + 24,5²) = 97,7 | +4,2 sur le sous-module actions |
| 2 | §3 Immobilier | Choc de 20 % au lieu de la baisse instantanée de 25 % | Art. 174 | 150,0 × 25 % = 37,5 | +7,5 sur le sous-module immobilier |
| 3 | §5 Matrice d'agrégation | Paramètre A pris égal à 0 alors que le SCR taux résulte du scénario de **baisse** retenu au §1 ; corrélations taux/actions, taux/immo et taux/spread nulles au lieu de 0,5 | Art. 164(3) et annexe IV | A = 0,5 sur les trois cellules concernées (et leurs symétriques) | +29,2 sur le SCR marché (effet isolé) |

Les erreurs 1 et 2 sont des erreurs de paramètre de choc ; l'erreur 3 est une incohérence interne à la note (le scénario de taux retenu contredit le paramètre A posé) et constitue le poste d'impact le plus lourd. L'arithmétique de la note est exacte sur ses propres données : aucune erreur de calcul n'est relevée.

## 2. Points d'attention (non bloquants)

1. **Ajustement symétrique à 0 %** — hypothèse explicitement annoncée, donc non comptée en erreur. Elle rend toutefois la note non diffusable en l'état pour l'ORSA : au 31/12/2025 la valeur publiée par l'EIOPA doit être substituée, et elle s'applique **aux deux types d'actions** (art. 172, bornée à ±17 %). Un SA de +5 % porterait par exemple le SCR actions à environ 108.
2. **Traitement des fonds en type 2** — l'agrégat « non cotées, fonds » de 50,0 suppose l'absence de transparisation. Le principe de transparence (art. 84) impose de décomposer les OPC et d'affecter les sous-jacents à leur sous-module réel ; une part significative des fonds relève souvent du type 1, du spread ou du taux. À documenter ou à corriger.
3. **Actions bénéficiant d'un régime spécifique** — aucune mention des participations stratégiques (22 %, art. 171), des infrastructures qualifiées (30 % / 36 %, art. 169) ni de la mesure transitoire actions (art. 173). Si l'entité en détient, le SCR actions est surestimé ; à confirmer explicitement dans la note.
4. **Sous-modules spread, devise et concentration** — repris « des calculs détaillés » sans pièce jointe. Ils n'ont pas pu faire l'objet du contrôle de second niveau ; leur revue reste à couvrir avant diffusion.
5. **Brut / net de capacité d'absorption** — la note ne précise pas si les montants sont nets de l'absorption par les provisions techniques. À expliciter pour la remontée au BSCR (art. 83).
6. **Conclusion de variation annuelle** — la « hausse de 3 % par rapport au 31/12/2024 » est calculée sur un SCR erroné et doit être refaite ; si le 31/12/2024 a été produit avec les mêmes paramètres, la comparabilité de la série est également à vérifier (risque d'erreur récurrente).

## 3. SCR marché corrigé

| | Note | Corrigé | Écart |
|---|---|---|---|
| Taux | 65,0 | 65,0 | — |
| Actions | 93,5 | 97,7 | +4,2 |
| Immobilier | 30,0 | 37,5 | +7,5 |
| Spread | 40,0 | 40,0 | — |
| Devise | 12,0 | 12,0 | — |
| Concentration | 5,0 | 5,0 | — |
| **Somme** | 245,5 | 257,2 | +11,7 |
| **SCR marché** | **167,4** | **206,5** | **+39,1** |
| Diversification | 78,1 (31,8 %) | 50,7 (19,7 %) | −27,4 |

**SCR marché corrigé : 206,5 M€**, soit un écart de **+39,1 M€ (+23,4 %)** par rapport à la note.

La note ne peut pas être diffusée en l'état. Les trois corrections sont à intégrer, puis l'ajustement symétrique réel et la transparisation des fonds à traiter avant validation finale ; le SCR corrigé de 206,5 M€ constitue un plancher en l'absence de ces deux derniers retraitements.

</rapport>
