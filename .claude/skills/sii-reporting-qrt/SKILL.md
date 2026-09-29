---
name: sii-reporting-qrt
description: Préparation et contrôle du reporting quantitatif Solvabilité II (QRT - S.02.01 bilan, S.05.01, S.06.02, S.12.01, S.17.01, S.19.01, S.23.01 fonds propres, S.25.01 SCR, S.28.01 MCR) - checklist de clôture, contrôles de cohérence inter-états, calendrier de remise. À utiliser pour préparer, relire ou contrôler une remise QRT trimestrielle ou annuelle, ou pour expliquer un écart entre états.
---

# Reporting QRT Solvabilité II

Références : règlement d'exécution (UE) 2023/894 (modèles de reporting) ; taxonomie XBRL EIOPA en vigueur (**vérifier la version applicable à la date de remise** sur eiopa.europa.eu avant de citer un code de cellule) ; contrôles de validation EIOPA (fichier des *validation rules* publié avec la taxonomie).

## États principaux

| État | Contenu | Solo annuel | Solo trimestriel |
|---|---|---|---|
| S.01.01 | Contenu de la remise | ✔ | ✔ |
| S.02.01 | Bilan prudentiel | ✔ | ✔ |
| S.05.01 | Primes, sinistres, dépenses par ligne d'activité | ✔ | ✔ |
| S.06.02 | Liste des actifs (ligne à ligne) | ✔ | ✔ |
| S.12.01 / S.17.01 | Provisions techniques vie / non-vie | ✔ | ✔ |
| S.19.01 | Triangles de sinistres non-vie | ✔ | |
| S.23.01 | Fonds propres | ✔ | ✔ |
| S.25.01 | SCR formule standard | ✔ | |
| S.26.xx | Détail des modules de risque SCR (dont S.26.01 marché) | ✔ | |
| S.28.01 / S.28.02 | MCR (mono / mixte) | ✔ | ✔ |

Délais usuels (solo) : annuel **14 semaines** après la clôture, trimestriel **5 semaines**. Groupe : +6 semaines. À confirmer avec le calendrier de l'autorité (ACPR).

## Checklist de clôture
Utiliser [templates/checklist-cloture.md](templates/checklist-cloture.md) : la copier dans le dossier de clôture et cocher au fil de l'eau.

## Contrôles de cohérence inter-états
Les règles sont dans [templates/controles.csv](templates/controles.csv) (id, formule gauche, opérateur, formule droite, tolérance, description). Les valeurs se saisissent dans un CSV `code,valeur` au format de [templates/valeurs-exemple.csv](templates/valeurs-exemple.csv), les codes étant de la forme `S.02.01.R0500.C0010`.

`<dossier du skill>` = dossier de base de ce skill (indiqué au chargement) ; les chemins restent valables que le skill vienne du projet ou d'un plugin.

```bash
python3 <dossier du skill>/scripts/check_qrt.py \
  --valeurs <valeurs.csv> [--controles <dossier du skill>/templates/controles.csv]
```

Le script affiche chaque contrôle OK/KO avec l'écart, et sort en code 1 si un contrôle est KO. Les codes de cellule du modèle sont **indicatifs** : les aligner sur la taxonomie en vigueur.

## Pièges fréquents
- Excédent d'actif sur passif du bilan (S.02.01) ≠ point de départ de la réserve de réconciliation (S.23.01) → dividendes prévisibles ou actions propres oubliés.
- Total S.06.02 ≠ placements S.02.01 → écart de périmètre (UC, trésorerie, dérivés au passif).
- Ratio de couverture S.23.01 ≠ fonds propres éligibles / SCR S.25.01 → SCR non mis à jour après une correction tardive.
- Signes : les états attendent des montants positifs pour les passifs ; un signe négatif dans S.02.01 est presque toujours une erreur.
- Unités : montants en unités monétaires (pas en milliers) dans l'instance XBRL.
