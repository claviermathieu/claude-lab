---
name: scr-marche
description: Paramètres faisant foi et calculateur du SCR marché en formule standard Solvabilité II - chocs (actions type 1/2, immobilier, devise, taux), matrice de corrélation, paramètre A selon le choc de taux retenu. Charger AVANT de répondre à toute question ou relecture touchant un choc, une corrélation ou l'agrégation du SCR marché, même si la réponse paraît connue - ces paramètres sont une source fréquente d'erreurs de mémoire. Couvre aussi notes de calcul, QRT S.26.01 et ORSA.
---

# SCR marché — formule standard

Référence : règlement délégué (UE) 2015/35 (« RD »), art. 164 à 188. Les paramètres ci-dessous sont ceux à utiliser ; ne pas s'appuyer sur la mémoire pour les chocs ou les corrélations.

## Paramètres de choc

| Sous-module | Choc | Article RD |
|---|---|---|
| Actions type 1 (cotées EEE/OCDE) | 39 % + ajustement symétrique (SA) | 169 §1 a) |
| Actions type 2 (autres : non cotées, hors OCDE, fonds non transparisés…) | 49 % + SA | 169 §1 b) |
| Participations stratégiques | 22 % | 171 |
| Infrastructures qualifiées : projets / entreprises | 30 % + 77 % × SA / 36 % + 92 % × SA | 169 §1 c), d) — à vérifier sur le texte consolidé |
| Actions de long terme (conditions art. 171 bis) | 22 % | 171 bis |
| Immobilier | **25 %** | 174 |
| Devise | 25 % (hausse et baisse, par devise) ; taux réduits pour les devises arrimées à l'euro | 188 |
| Taux | chocs relatifs par maturité, hausse et baisse (tableau art. 166-167) | 165 à 167 |

SA : ajustement symétrique publié mensuellement par l'EIOPA, borné à ±10 %.

Agrégation actions : type 1 / type 2 corrélés à **0,75** (et les infrastructures/long terme rangés avec le type 1 ou 2 selon l'art. 168).

Sous-module taux : SCR taux = max(perte en hausse ; perte en baisse). Le scénario **retenu** détermine le paramètre A.

## Matrice de corrélation inter-sous-modules (art. 164)

|  | Taux | Actions | Immo | Spread | Devise | Concentr. |
|---|---|---|---|---|---|---|
| Taux | 1 | A | A | A | 0,25 | 0 |
| Actions | A | 1 | 0,75 | 0,75 | 0,25 | 0 |
| Immo | A | 0,75 | 1 | 0,5 | 0,25 | 0 |
| Spread | A | 0,75 | 0,5 | 1 | 0,25 | 0 |
| Devise | 0,25 | 0,25 | 0,25 | 0,25 | 1 | 0 |
| Concentr. | 0 | 0 | 0 | 0 | 0 | 1 |

**Règle du paramètre A** (source d'erreur fréquente, y compris pour les modèles de langage) :
- **A = 0** si le SCR taux retenu provient du choc **à la HAUSSE** ;
- **A = 0,5** si le SCR taux retenu provient du choc **à la BAISSE**.

Intuition : en baisse des taux, les pertes sur actions/immo/spread (scénarios de crise) tendent à coïncider avec la baisse → corrélation positive.

## Calcul

Utiliser le script plutôt que de calculer de tête :

`<dossier du skill>` = dossier de base de ce skill (indiqué au chargement) ; les chemins restent valables que le skill vienne du projet ou d'un plugin.

```bash
python3 <dossier du skill>/scripts/scr_marche.py \
  --taux-hausse 42 --taux-baisse 65 --actions-type1 200 --actions-type2 50 \
  --immobilier 150 --spread 40 --devise 12 --concentration 5 [--sa 0.0]
```

Les arguments `--actions-*` et `--immobilier` sont des **expositions** (le script applique les chocs) ; `--taux-*`, `--spread`, `--devise`, `--concentration` sont des **SCR déjà calculés**. Sortie : détail par sous-module, paramètre A retenu, somme, SCR marché, diversification. Option `--json` pour une sortie machine.

## Checklist de revue d'un SCR marché
1. Chaque choc correspond-il au tableau ci-dessus (type d'actions bien classé, SA appliqué aux deux types) ?
2. Le scénario de taux retenu est-il le plus pénalisant, et A est-il cohérent avec lui ?
3. Corrélations intra-actions (0,75) et inter-modules conformes à la matrice ?
4. Recalcul avec le script : écart < 0,1 M€ ?
5. Hypothèses simplificatrices annoncées (SA = 0, transparisation partielle) : les signaler en point d'attention, pas en erreur.
