# Checklist de clôture QRT — [entité] — [date d'arrêté] — [annuel / trimestriel]

## Préparation
- [ ] Version de taxonomie EIOPA applicable identifiée : ______
- [ ] Périmètre des états à remettre confirmé (S.01.01 rempli en conséquence)
- [ ] Calendrier interne partagé (arrêté des comptes, PT, SCR, revue, remise)

## Données sources
- [ ] Inventaire des placements rapproché de la comptabilité (S.06.02 ↔ grand livre)
- [ ] Transparisation des fonds (look-through) à jour
- [ ] Meilleure estimation (BE) et marge de risque validées par la fonction actuarielle
- [ ] Courbe EIOPA du mois d'arrêté utilisée (avec / sans VA selon le cas)
- [ ] Ajustement symétrique actions du mois d'arrêté utilisé

## Calculs
- [ ] SCR recalculé sur les données définitives (pas d'estimation antérieure)
- [ ] MCR recalculé ; plancher/plafond (25 %–45 % du SCR) et plancher absolu vérifiés
- [ ] Fonds propres : dividendes prévisibles déduits, classement par tiers et limites d'éligibilité

## Contrôles
- [ ] Contrôles inter-états (`check_qrt.py`) : tous OK ou écarts expliqués
- [ ] Règles de validation EIOPA (outil de remise) : zéro erreur bloquante
- [ ] Variations N-1 / N > 10 % expliquées par poste
- [ ] Cohérence avec le RSR/SFCR (mêmes chiffres dans les états et les rapports narratifs)

## Validation et remise
- [ ] Revue de second niveau (fonction actuarielle / risques)
- [ ] Validation par la direction (dirigeant effectif)
- [ ] Remise sur le portail de l'autorité, accusé de réception archivé
- [ ] Archivage : instance XBRL, fichiers sources, preuves de contrôle
