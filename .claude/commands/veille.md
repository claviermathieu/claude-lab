---
description: Prépare le brouillon de veille de la semaine (IA, tech/data, assurance/actuariat) dans notes/veille/
argument-hint: "[thème ou consigne optionnelle]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob
---

Prépare la veille de la semaine écoulée (les 7 derniers jours avant aujourd'hui). Consigne éventuelle : $ARGUMENTS

1. Lis `notes/veille/README.md` : sources, grille de tri 🔴/🟠/⚪, format d'entrée.
2. Ouvre le fichier du mois `notes/veille/AAAA-MM.md` (crée-le depuis `notes/veille/_modele.md` s'il n'existe pas). Lis les semaines déjà saisies pour ne pas répéter une information.
3. Pour chacun des trois thèmes (IA et modèles ; Tech et plateformes data ; Assurance, actuariat et réglementation), consulte les sources listées dans le guide (WebFetch sur les pages d'actualité, WebSearch pour compléter) et retiens **au plus 5 faits par thème** publiés dans la période.
   - Priorité aux faits 🔴 Action et 🟠 À suivre pour un actuaire data scientist qui utilise Claude, GCP et Databricks.
   - Chaque fait doit avoir un lien vers la source primaire (annonce officielle, texte, release note), pas vers un article qui la reprend quand l'original est accessible.
   - Si la date de publication n'est pas vérifiable ou sort de la période, écarte le fait.
   - Si une page est bloquée (403/404), passe par `WebSearch` avec `site:<domaine>` et la période ; ne saute aucune source du guide sans l'avoir tentée.
   - Pour l'EIOPA : si la courbe RFR ou l'ajustement symétrique du mois ont été publiés, les signaler (valeur de l'ajustement symétrique si elle est lisible sur la page).
4. Ajoute une section `## Semaine NN (du JJ/MM au JJ/MM)` au-dessus de « Synthèse du mois », au format du modèle, chaque entrée suffixée de *(à vérifier)*.
5. Ajoute les faits 🔴 dans « À surveiller / À faire » avec une échéance si elle est connue.
6. Réponds par un résumé de 5 lignes maximum : nombre de faits par thème, faits 🔴, sources inaccessibles **et sources non consultées** (à lire à la main). Ne commite pas : le tri manuel vient ensuite.
