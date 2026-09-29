---
name: ifrs9-ecl
description: Méthodologie et calcul des pertes de crédit attendues IFRS 9 (ECL) - staging 1/2/3, dégradation significative (SICR), PD 12 mois vs lifetime, LGD, EAD, actualisation au TIE, scénarios macro pondérés. À utiliser pour calculer, expliquer, documenter ou contrôler une provision ECL sur un portefeuille de prêts, d'obligations ou de créances.
---

# IFRS 9 — Expected Credit Loss

Référence : IFRS 9 §5.5 (dépréciation), annexe B5.5. Guidance superviseurs : EBA/GL/2017/06.

## 1. Staging

| Stage | Critère | Horizon ECL | Produits d'intérêts |
|---|---|---|---|
| 1 | Pas de dégradation significative depuis l'origine | 12 mois | Sur valeur brute |
| 2 | **SICR** depuis l'origine, non défaut | Durée de vie (lifetime) | Sur valeur brute |
| 3 | Défaut / crédit déprécié (credit-impaired) | Lifetime (PD = 1) | Sur valeur nette |

Critères SICR usuels (à combiner, documenter les seuils) :
- **Quantitatif** : PD lifetime actuelle / PD lifetime à l'origine (même horizon résiduel) > seuil (souvent 2 à 3 ×), avec un plancher absolu d'écart de PD.
- **Qualitatif** : watchlist, restructuration (forbearance), dégradation de notation interne.
- **Backstop** : impayés > 30 jours → stage 2 (présomption réfutable §5.5.11) ; > 90 jours → défaut, stage 3 (présomption §B5.5.37).
- Exemption *low credit risk* (§5.5.10) : investment grade → stage 1 possible sans test SICR.

## 2. Formule

ECL = Σ_scénarios w_s × Σ_{t=1..H} PD_marg,s(t) × LGD × EAD(t) × (1 + TIE)^(−t)

- PD_marg(t) = PD_cum(t) − PD_cum(t−1), **point-in-time** et **forward-looking** (conditionnée au scénario macro), pas la PD TTC réglementaire bâloise.
- H = min(1, maturité résiduelle) en stage 1 ; maturité résiduelle en stage 2.
- Stage 3 : ECL = LGD × EAD (défaut avéré).
- Actualisation au **taux d'intérêt effectif** d'origine de l'instrument.
- Au moins 3 scénarios (base, favorable, défavorable) pondérés par leur probabilité ; la non-linéarité impose de pondérer les ECL, pas les paramètres.

## 3. Calcul avec le script

```bash
python3 .claude/skills/ifrs9-ecl/scripts/ecl.py \
  --expositions .claude/skills/ifrs9-ecl/exemples/expositions.csv \
  --pd .claude/skills/ifrs9-ecl/exemples/pd_cumulees.csv \
  --scenarios base=0.5,favorable=0.2,defavorable=0.3 [--seuil-sicr 2.5] [--json]
```

Entrées (CSV, séparateur virgule, montants en unités monétaires) :
- `expositions.csv` : `id, segment, ead, lgd, tie, maturite, jours_impayes, watchlist, pd_lifetime_origine`
- `pd_cumulees.csv` : `segment, scenario, annee, pd_cum` (PD cumulées par année, 1..N)

Le script calcule le stage (backstops 30/90 jours, watchlist, ratio de PD lifetime vs origine), l'ECL par exposition et par stage, et le taux de couverture. Exemples fournis dans `exemples/`. Dépendances : bibliothèque standard uniquement.

## 4. Points de contrôle
1. Somme des poids de scénarios = 1.
2. PD cumulées croissantes, entre 0 et 1, et stage 2 ≥ stage 1 à exposition égale.
3. Taux de couverture par stage cohérents (ordre de grandeur : S1 < 1 %, S2 quelques %, S3 = LGD).
4. Migrations entre stages expliquées (tableau de passage N-1 → N).
5. Overlays post-modèle documentés séparément, jamais noyés dans les paramètres.
