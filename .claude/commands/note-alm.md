---
description: Produit la note ALM risque de taux (données MCP alm-data, skill note-alm, validation par model-validator)
argument-hint: "[taux d'actualisation du passif, ex. 0.03] [consignes]"
---

Produis la note ALM sur le risque de taux. Paramètres éventuels : $ARGUMENTS (taux d'actualisation du passif ; 3 % à défaut).

1. Charge le skill `note-alm` et suis sa méthode : données via les outils MCP `alm-data`, réconciliation des sources, duration gap, sensibilités ±100 pb.
2. Rédige la note dans `notes/alm/note-alm-<date du jour AAAA-MM-JJ>.md` selon le modèle du skill, section **Validation** provisoirement remplie par « en attente ». Un hook vérifie la structure : si l'écriture est rejetée, corrige et réécris.
3. Délègue la relecture de la note au subagent `model-validator` (chemin du fichier + « vérifier chaque chiffre contre les sorties d'outils citées et la méthode du skill note-alm »).
4. Corrige les constats bloquants et majeurs dans la note, puis complète la section **Validation** : verdict du valideur, constats traités, constats non traités et pourquoi.
5. Réponds avec le chemin de la note, la synthèse en 3 lignes et le verdict.
