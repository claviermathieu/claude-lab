---
name: note-alm
description: Méthodologie et modèle de la note ALM sur le risque de taux (duration gap, sensibilités ±100 pb avec convexité, réconciliation bilan / flux, actions de pilotage) à partir des données du serveur MCP alm-data. À utiliser pour rédiger, mettre à jour ou relire une note ALM, un duration gap ou une analyse d'adossement actif-passif.
---

# Note ALM — risque de taux

## Données (serveur MCP `alm-data`)
1. `list_datasets` : vérifier la présence de `bilan.csv`, `obligations.parquet`, `flux_passif.parquet` et **relever les versions DVC** (md5) à citer dans la note.
2. `read_dataset("bilan.csv")` : actif/passif en M€.
3. `portfolio_duration_convexity` : VM, D_mod, convexité du portefeuille obligataire, sensibilités ±100 pb.
4. `cashflow_duration(taux=…)` : VA, D_mod, convexité du passif (taux demandé, 3 % à défaut).
5. **`duration_gap(taux=…)`** : réconciliation, duration gap et ΔFP ±100 pb sur les deux bases, déjà calculés. **Reprendre ses chiffres tels quels : ne jamais recalculer gap ou sensibilités à la main** (source d'erreurs, et le valideur ne pourrait pas tracer le chiffre).

## Calculs (effectués par `duration_gap` — rappel de la méthode pour l'interprétation)
- Fonds propres économiques : FP = total actif − total passif (bilan).
- **Réconciliation** avant tout calcul : obligations au bilan vs VM recalculée ; best estimate au bilan vs VA des flux. Écart > 5 % → le signaler en tête de note, calculer le gap sur **les deux bases** (bilan et recalculée) et ne pas conclure sur le signe si les deux bases divergent.
- Duration gap pondéré : DG = D_A − D_P × (P / A), avec A et P les assiettes sensibles aux taux (obligations ; best estimate). Actions, immobilier, trésorerie, marge de risque, autres passifs : duration nulle (hypothèse à écrire).
- ΔFP(±Δy) ≈ −(D_A·A − D_P·P)·Δy + ½(C_A·A − C_P·P)·Δy², pour Δy = ±1 %.
- Ratio ΔFP / FP en %.

## Modèle de note (titres obligatoires, dans cet ordre)
Écrire dans `notes/alm/note-alm-<AAAA-MM-JJ>.md` :

```markdown
# Note ALM — risque de taux — <date>
## Synthèse
(3 lignes max : exposition, chiffre clé, décision attendue)
## Données et hypothèses
(sources + versions DVC, taux d'actualisation, hypothèses de duration nulle)
## Réconciliation des sources
(tableau bilan vs recalculé, écarts en M€ et %)
## Duration gap et sensibilités
(tableau : base, D_A, D_P, DG, ΔFP +100 pb, ΔFP −100 pb, ΔFP/FP)
## Limites
## Actions proposées
(3 au plus, chacune : action, effet attendu sur le DG, coût/risque)
## Validation
(verdict du valideur et suites données)
```

Règles : aucun chiffre sans source (bilan ou outil) ; M€ à une décimale, durations à deux ; toute incohérence de source est signalée, jamais lissée.
