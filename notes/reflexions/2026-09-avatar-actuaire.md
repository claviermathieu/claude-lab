# L'actuaire et son avatar numérique

*Note de réflexion — 30/09/2026*

## 1. Le constat

Douze modules de ce lab montrent ce qu'un modèle de 2026 fait déjà bien sur des tâches actuarielles :

- **écrire et tester du code de calcul** (Smith-Wilson, ECL IFRS 9, duration gap) plus vite qu'un actuaire seul ;
- **rédiger** une note technique structurée à partir de sorties d'outils ;
- **relire** un livrable avec une grille (subagent `model-validator`) ;
- **orchestrer** une chaîne complète (données MCP → calcul → note → validation → contrôle par hook).

Ils montrent aussi où ça casse :

- **mémoire des paramètres** : chocs, corrélations et paramètre A du SCR marché (art. 164 RD 2015/35) sont restitués de manière plausible mais fausse. C'est pour ça que le skill `scr-marche` impose de charger ses paramètres faisant foi ;
- **absence de source** : sans texte sous les yeux, le modèle cite des articles approximatifs ;
- **jugement** : le choix d'une hypothèse (taux de rachat, dérive de sinistralité, facteur de queue) ne se déduit pas des données, il s'argumente ;
- **responsabilité** : le modèle ne signe rien.

On en tire une conclusion : la valeur ne vient pas du modèle, qui devient une commodité, mais de **ce qu'on met autour** : sources, méthodes, outils, garde-fous. Et ce qu'on met autour, c'est précisément le savoir de l'actuaire.

## 2. Ce que l'IA fait au métier

Le travail actuariel se découpe en trois couches, que l'IA ne touche pas de la même façon.

| Couche | Exemples | Effet de l'IA |
|---|---|---|
| **Savoir codifiable** | formules, textes, paramètres réglementaires, tables | Automatisable, **à condition d'une source faisant foi** injectée au bon moment |
| **Savoir-faire procédural** | clôture QRT, calibrage d'un modèle, revue d'un provisionnement, rédaction d'un rapport de la fonction actuarielle | Orchestrable : une procédure explicite devient une commande ou un agent |
| **Jugement et responsabilité** | choix d'hypothèses, appréciation de la suffisance des provisions, dialogue avec l'ACPR, avis de la fonction actuarielle (art. 48 directive 2009/138/CE, art. 272 RD 2015/35) | Non délégable. L'IA l'éclaire (scénarios, contre-arguments, sensibilités), elle ne le porte pas |

Conséquences probables :

- **Des tâches disparaissent, pas les rôles qui portent une responsabilité.** La production de tableaux, le code standard et la documentation de routine se compriment fortement. La signature, la validation et l'arbitrage restent.
- **Le centre de gravité se déplace vers la conception et la validation** de modèles, qu'ils soient actuariels ou d'IA. L'actuaire est bien placé pour ça. Le règlement (UE) 2024/1689 (AI Act) classe à haut risque l'évaluation des risques et la tarification des personnes physiques en assurance vie et santé (annexe III, point 5 c)). Quelqu'un devra documenter, tester et surveiller ces systèmes, et c'est une extension naturelle de la fonction actuarielle et de la validation de modèles. *(Le calendrier d'application des obligations « haut risque » est en discussion dans l'omnibus numérique : à vérifier.)*
- **Le risque de déqualification est réel.** Les juniors se formaient en produisant ce que l'IA produit désormais. Si on délègue tout, le jugement ne se construit plus. Un avatar bien conçu doit donc aussi **expliquer et former**, pas seulement produire.
- **Un savoir non formalisé devient invisible.** Ce qui reste dans la tête ou dans un Word personnel ne profite pas du levier. Ce qui est formalisé, sourcé et outillé est démultiplié.

## 3. Pourquoi un « avatar numérique »

L'intuition est la bonne, à condition de préciser le mot. L'avatar n'est pas un clone qui répond à ma place : c'est **mon savoir de travail rendu exécutable**, c'est-à-dire :

1. un **référentiel** : ce que je sais, sourcé et daté (le Word de carrière en est le noyau) ;
2. des **méthodes** : comment je traite un sujet, sous forme de skills et de scripts testés ;
3. des **procédures** : les workflows récurrents, sous forme de commandes ;
4. des **accès** aux sources primaires (droit, économie, données), via des serveurs MCP ;
5. des **garde-fous** : validation indépendante, hooks, citations obligatoires ;
6. une **mesure** : des questions de référence qui vérifient que l'avatar répond juste.

Ce qu'on y gagne :

- **Capitalisation** : quinze ans de notes deviennent un actif qui s'enrichit au lieu de dormir.
- **Levier** : un actuaire pilote plusieurs agents qui appliquent *ses* méthodes.
- **Qualité** : les paramètres sont lus dans une source et non dans la mémoire du modèle, et les chiffres sont calculés par du code testé.
- **Portabilité** : Markdown, Python et MCP sont des formats ouverts. L'avatar survit à un changement d'employeur, d'outil ou de fournisseur de modèle.

Les limites à assumer dès la conception :

- **Confidentialité** : aucune donnée d'assuré dans le référentiel. En prévoyance et en santé, ce sont des données de santé (art. 9 RGPD). Les décisions individuelles automatisées relèvent de l'art. 22 RGPD. L'avatar travaille sur des méthodes, des textes et des agrégats.
- **Péremption** : la réglementation bouge. La révision de Solvabilité II (directive (UE) 2025/2) s'applique à partir de janvier 2027 et changera des paramètres. Le référentiel doit être **daté par période d'application**, pas seulement « à jour ».
- **Propriété intellectuelle** : séparer le savoir personnel (portable) des méthodes et données propres à un employeur (non portables).
- **Fausse assurance** : un avatar qui répond avec aplomb est plus dangereux qu'un avatar qui dit « non vérifié ». Il doit toujours signaler ce qu'il n'a pas pu sourcer.

## 4. La question de fond : qu'est-ce qu'un actuaire ?

Construire l'avatar oblige à expliciter une **ontologie du métier**. Voici une proposition à confronter au Word.

**Fondements** (transverses) : probabilités et statistique, mathématiques financières, biométrie et démographie, économie et finance de marché, droit et réglementation, comptabilité, informatique et données.

**Branches** :

- **Vie** : épargne (euro, UC, eurocroissance), retraite (PER, rentes), décès. Enjeux : participation aux bénéfices, taux minimum garanti, tables (art. A.132-18 C. assur.), rachats, options et garanties, ALM.
- **Non-vie** : auto, MRH, RC, construction, dommages aux entreprises. Enjeux : triangles, provisionnement, sinistres graves et cat, réassurance, tarification GLM.
- **Prévoyance et santé** : incapacité, invalidité, dépendance, décès collectif, complémentaire santé. Enjeux : tables BCAC, provisions de maintien, loi Évin, contrats collectifs, cadre code des assurances / code de la mutualité / code de la sécurité sociale (IP).

**Processus** (transverses aux branches) : tarification, provisionnement, solvabilité et capital (SII, ORSA), ALM, réassurance, comptes (normes françaises, IFRS 17), reporting (QRT, RSR, SFCR), fonction actuarielle, pilotage et rentabilité.

L'enseignement structurant est que **le métier est une matrice branche × processus**. Cela oriente l'architecture :

- une compétence **de processus** (ex. chain-ladder, best estimate vie, SCR) est un skill transverse, réutilisé par toutes les branches ;
- une compétence **de branche** (ex. spécificités de la prévoyance collective) est un skill de domaine, qui renvoie aux skills de processus ;
- on évite ainsi trois gros skills « vie / non-vie / prévoyance » qui dupliqueraient 60 % de leur contenu.

## 5. Traduction technique

| Brique de l'avatar | Primitive Claude | Exemples |
|---|---|---|
| Référentiel | fichiers Markdown sourcés et datés, lus par les skills (chargement progressif) | `referentiel/fondements/`, `referentiel/vie/`… issus du Word |
| Méthodes | **skills** + scripts Python testés | transverses : `provisionnement-non-vie`, `best-estimate-vie`, `scr-*`, `ifrs17`, `alm` ; domaine : `vie`, `non-vie`, `prevoyance` |
| Procédures | **commandes** | `/note-technique`, `/revue-actuarielle`, `/question-reglementaire`, `/tarifer`, `/provisionner`, `/veille-reglementaire` |
| Sources primaires | **serveurs MCP** | droit : Légifrance et Judilibre (API PISTE), EUR-Lex (SPARQL Cellar) ; économie : BCE (Data Portal SDMX), Eurostat, INSEE (BDM), Banque de France (Webstat) ; marché : courbes RFR EIOPA ; interne : `alm-data` existant |
| Rôles spécialisés | **subagents** | `model-validator` (existant), `juriste` (lecture seule, cite l'article et sa version en vigueur), `economiste` |
| Garde-fous | **hooks** | citation obligatoire dans les notes, blocage des données personnelles, `data/` en lecture seule |
| Mesure | **evals** | banque de questions de référence par domaine, réponses attendues sourcées, taux de bonnes réponses suivi dans le temps |
| Distribution | **plugin** + marketplace | installable sur n'importe quel poste ou projet |

Principes de conception :

1. **La source fait foi, pas la mémoire du modèle.** Tout paramètre réglementaire vient du référentiel ou d'un MCP, avec l'article cité.
2. **Tout chiffre sort d'un script testé.** Le modèle orchestre et rédige, il ne calcule pas de tête.
3. **Le référentiel est daté et versionné.** Un paramètre porte sa période d'application.
4. **L'humain signe.** L'avatar produit des brouillons, des contrôles et des contre-analyses, jamais une conclusion engageante sans relecture.
5. **Tout est en formats ouverts.** Markdown, Python, MCP.

## 6. Feuille de route proposée

| Étape | Contenu | Livrable |
|---|---|---|
| 0 | Ingestion du Word de carrière → ontologie + référentiel Markdown, lacunes identifiées | `referentiel/` + carte des compétences |
| 1 | Squelette du repo avatar, conventions, plugin vide installable | repo + `plugin.json` |
| 2 | MCP droit : EUR-Lex (sans clé) puis Légifrance (PISTE, OAuth2) | `mcp/droit/` + tests |
| 3 | MCP économie : BCE, Eurostat, INSEE | `mcp/economie/` + tests |
| 4 | Skills transverses puis skills de domaine vie / non-vie / prévoyance | `skills/` + scripts testés |
| 5 | Commandes et subagents | `commands/`, `agents/` |
| 6 | Evals par domaine, mesure de référence | `evals/` + tableau de résultats |
| 7 | Usage réel : 1 mois sur des cas concrets, retours intégrés | journal d'usage |

## 7. Questions ouvertes

- Quel **périmètre de portabilité** : savoir strictement personnel, ou aussi des méthodes d'entreprise dans un espace séparé ?
- Quel **public** : moi seul, ou une équipe (ce qui change le niveau de documentation et la gouvernance) ?
- Quelle **frontière avec l'AI Act** si l'avatar sert un jour à tarifer des personnes physiques en vie ou en santé ?
- Comment l'avatar **forme-t-il** au lieu de seulement produire (mode « tuteur » pour les juniors) ?
