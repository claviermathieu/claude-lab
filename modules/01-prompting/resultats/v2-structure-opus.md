## 1. Tableau des erreurs

| # | Section | Constat | Référence | Correction |
|---|---|---|---|---|
| 1 | §2 Actions | Choc type 2 appliqué à 39 % au lieu de 49 % (+ ajustement symétrique). Le taux de 39 % est réservé au type 1. | Art. 169(1)(b) du RD (UE) 2015/35 | 50,0 × 49 % = **24,5** (au lieu de 19,5) → SCR actions = √(78,0² + 2×0,75×78,0×24,5 + 24,5²) = **97,7** |
| 2 | §3 Immobilier | Choc immobilier appliqué à 20 % au lieu de 25 % | Art. 174 du RD 2015/35 | 150,0 × 25 % = **37,5** (au lieu de 30,0) |
| 3 | §5 Agrégation | Paramètre A fixé à 0 alors que le SCR taux retenu provient du **choc à la baisse**. A = 0 n'est admis que si c'est le choc à la hausse qui est retenu ; sinon A = 0,5. | Art. 164(3) + Annexe IV du RD 2015/35 | A = **0,5** → corr(taux ; actions) = corr(taux ; immo) = corr(taux ; spread) = 0,5 |
| 4 | §5 / Conclusion | Le SCR marché de 167,4 et la variation « +3 % vs 31/12/2024 » découlent des trois erreurs ci‑dessus et ne sont plus valides | recalcul | SCR marché = **206,5** ; la variation annuelle doit être recalculée et re‑commentée |

**Ce qui est correct** : le max(42,0 ; 65,0) du sous‑module taux (art. 165) ; la corrélation 0,75 type 1 / type 2 et la forme de la formule d'agrégation actions (art. 169) ; le choc type 1 à 39 % ; la structure de la matrice de l'annexe IV hors paramètre A (ligne concentration nulle, immo/spread = 0,5, actions/spread = 0,75, devise = 0,25) ; l'ensemble des recalculs arithmétiques sur la base des intrants retenus (93,5 ; 167,4 ; 245,5 ; 31,8 %) — les erreurs sont paramétriques, pas arithmétiques.

## 2. Points d'attention

- **Ajustement symétrique à 0 %** : annoncé comme simplificateur, donc hors périmètre d'erreur — mais il devra être repris à la valeur EIOPA publiée au 31/12/2025 (fourchette ±17 %) avant diffusion ACPR, sur les deux types d'actions.
- **Classement « non cotées, fonds » en type 2** : les OPC doivent faire l'objet d'une transparisation (art. 84) et être ventilés sur les sous‑modules sous‑jacents ; le rattachement global en actions type 2 n'est admissible qu'à défaut de données, et doit être justifié.
- **Composition du type 1** : vérifier l'absence de participations stratégiques (22 %, art. 171), d'investissements en actions de long terme (22 %, art. 171a) et d'infrastructures éligibles (30 %/36 %, art. 164a‑164b) traités par erreur à 39 %.
- **Sous‑module devise** : s'assurer que les 12,0 résultent bien d'une **somme** sur devises des max(hausse ; baisse) à 25 %, sans diversification inter‑devises (art. 188).
- **Les deux scénarios taux sont perdants** (−42,0 et −65,0) : configuration possible mais peu banale ; documenter le profil ALM qui la produit, l'ACPR le demandera.
- **Brut / net de LAC** : préciser si les SCR présentés sont bruts ou nets de la capacité d'absorption des pertes des provisions techniques, la cohérence devant être tenue jusqu'au BSCR.
- Vérifier la version du règlement délégué applicable à l'arrêté (revue Solvabilité II en cours de déploiement), notamment sur le stress de taux.

## 3. SCR marché corrigé

| Sous‑module | Note | Corrigé |
|---|---|---|
| Taux | 65,0 | 65,0 |
| Actions | 93,5 | 97,7 |
| Immobilier | 30,0 | 37,5 |
| Spread | 40,0 | 40,0 |
| Devise | 12,0 | 12,0 |
| Concentration | 5,0 | 5,0 |
| Somme | 245,5 | 257,2 |

**SCR marché corrigé = 206,5 M€** (diversification 50,7 ; 19,7 %).

Écart avec la note : **+39,1 M€, soit +23,4 %**. La baisse du bénéfice de diversification (31,8 % → 19,7 %) vient pour l'essentiel du passage de A à 0,5, qui supprime l'indépendance artificielle entre le taux et les trois principaux sous‑modules.
