# Veille hebdomadaire — mode d'emploi

**Rythme** : une fois par semaine, le vendredi, 30 minutes maximum. Une fois par mois, 15 minutes de synthèse.
**Objectif** : ne rien rater qui oblige à agir (réglementation, changement d'API, nouvelle version d'outil), et repérer ce qui mérite un essai dans le lab. Ce n'est pas une revue de presse exhaustive.

## Organisation des fichiers

```
notes/veille/
├── README.md        ce guide (sources, méthode, grille)
├── _modele.md       modèle d'un fichier mensuel
└── AAAA-MM.md       un fichier par mois, une section par semaine + synthèse mensuelle
```

## La routine du vendredi (30 min)

1. **Ouvrir le fichier du mois** `notes/veille/AAAA-MM.md`. S'il n'existe pas, copier `_modele.md`.
2. **Préparer un brouillon avec Claude (5 min)** : dans le repo, lancer `claude`, puis `/veille`.
   - La commande parcourt les sources ci-dessous sur les 7 derniers jours, puis ajoute la section de la semaine dans le fichier du mois.
   - Chaque entrée porte sa source et la mention *à vérifier*.
3. **Trier (15 min)** : ouvrir chaque lien du brouillon et appliquer la grille.
   - Supprimer sans regret ce qui est *Info* et sans intérêt.
   - Retirer *à vérifier* seulement après avoir lu la source.
4. **Compléter à la main (5 min)** : ajouter ce que l'outil ne voit pas, comme une newsletter reçue par mail, un échange avec un collègue ou un webinaire.
5. **Reporter les actions (5 min)** :
   - Chaque entrée 🔴 *Action* devient une case dans « À surveiller / À faire » avec une échéance.
   - Si elle touche le lab (nouvelle version d'API, changement du SDK MCP…), ajouter aussi une ligne dans le README du module concerné.
6. **Commiter** : `git commit -am "veille: semaine NN"` puis `git push`.

Sans Claude, faire les étapes 3 à 6 en partant de la liste des sources, avec un lecteur RSS.

### Limites connues de la collecte automatique

Liens vérifiés le 29/09/2026.

- **Sites qui bloquent les robots** (erreur 403) : OpenAI, Snowflake, L'Argus. `/veille` passe alors par une recherche web `site:`.
- **Newsletters sans page consultable**, comme The Batch en version complète : elles restent à lire soi-même.
- **Changelog de Claude Code** : il ne date pas ses entrées. Le comparer au numéro de version indiqué par `claude --version`.

## Grille de tri

| Niveau | Critère | Ce qu'on en fait |
|---|---|---|
| 🔴 **Action** | Change ce que je dois faire : nouvelle obligation réglementaire, API dépréciée, modèle retiré, nouveau paramètre EIOPA | Case à cocher avec échéance, et modification dans le lab si besoin |
| 🟠 **À suivre** | Consultation, proposition de texte, bêta, tendance qui se confirme | Case « À surveiller » sans échéance, relue à chaque synthèse mensuelle |
| ⚪ **Info** | Utile à savoir, sans conséquence directe | Une ligne, rien de plus |

Format d'une entrée, sur une ligne : **fait** · [source](url) · impact pour moi · niveau.

## Sources par thème

### 1. IA et modèles

| Source | Quoi regarder |
|---|---|
| [anthropic.com/news](https://www.anthropic.com/news) | Nouveaux modèles, annonces produit |
| [Release notes de l'API Claude](https://docs.claude.com/en/release-notes/overview) | Changements d'API, dépréciations, bêtas |
| [Changelog de Claude Code](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | Nouvelles commandes, hooks, skills, plugins |
| [modelcontextprotocol.io](https://modelcontextprotocol.io) et [SDK Python](https://github.com/modelcontextprotocol/python-sdk/releases) | Évolutions de la spec MCP et versions du SDK |
| [openai.com/news](https://openai.com/news), [blog Google DeepMind](https://deepmind.google/discover/blog/) | Modèles concurrents (prix, capacités) |
| [huggingface.co/blog](https://huggingface.co/blog) | Modèles open-weights, outillage |
| [simonwillison.net](https://simonwillison.net) | Synthèse quotidienne très fiable sur les LLM |
| [The Batch (deeplearning.ai)](https://www.deeplearning.ai/the-batch/) | Récapitulatif hebdomadaire |

### 2. Tech et plateformes data

| Source | Quoi regarder |
|---|---|
| [Blog Databricks](https://www.databricks.com/blog) et [release notes](https://docs.databricks.com/en/release-notes/index.html) | Unity Catalog, Mosaic AI, agents, Delta Lake, tarification serverless |
| [Blog Snowflake](https://www.snowflake.com/en/blog/) | Cortex AI, fonctionnalités concurrentes de Databricks |
| [Release notes BigQuery](https://cloud.google.com/bigquery/docs/release-notes) et [Vertex AI](https://cloud.google.com/vertex-ai/docs/release-notes) | GCP est l'environnement par défaut ; Claude est disponible sur Vertex |
| [Python Insider](https://blog.python.org), [Astral (uv, ruff)](https://astral.sh/blog) | Versions de Python et de l'outillage du lab |
| [Blog DVC](https://dvc.org/blog), [blog dbt](https://www.getdbt.com/blog) | Versionnage des données, transformation |

### 3. Assurance, actuariat et réglementation

| Source | Quoi regarder |
|---|---|
| [EIOPA : actualités](https://www.eiopa.europa.eu/media/news_en) et [taux sans risque](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en) | Courbe RFR et ajustement symétrique (publiés chaque mois), consultations, stress tests, taxonomie de reporting |
| [ACPR : actualités](https://acpr.banque-france.fr/fr/actualites) | Notices, recommandations, priorités de contrôle, calendrier des remises |
| [EUR-Lex](https://eur-lex.europa.eu) | Textes publiés : transposition de la directive (UE) 2025/2 (Solvabilité II révisée), actes délégués, AI Act, DORA |
| [IFRS Foundation](https://www.ifrs.org/news-and-events/) | IFRS 17 et IFRS 9 : décisions de l'IFRS Interpretations Committee, amendements |
| [Institut des actuaires](https://www.institutdesactuaires.com) | Notes de place, groupes de travail, formations |
| [France Assureurs](https://www.franceassureurs.fr) | Chiffres de marché, positions de place |
| [L'Argus de l'assurance](https://www.argusdelassurance.com) | Actualité du marché français |
| [arXiv q-fin.RM](https://arxiv.org/list/q-fin.RM/recent) | Recherche en gestion des risques, ML appliqué à l'assurance (à parcourir une fois par mois) |

### 4. Presse économique sur abonnement : Les Echos

Lu **dans ton Chrome, où tu es connecté à ton abonnement**, via Claude in Chrome. Voir « Brancher Les Echos » plus bas.

Rubriques à parcourir (URL probables, à confirmer au premier passage : le site bloque les accès automatisés) :
- Banque-Assurance : `lesechos.fr/finance-marches/banque-assurances`
- Intelligence artificielle : `lesechos.fr/tech-medias/intelligence-artificielle`
- Tech-Médias : `lesechos.fr/tech-medias`
- Finance & Marchés, pour les taux et les marchés : `lesechos.fr/finance-marches`

**Règle** : une ligne de résumé, écrite avec tes mots, et le lien. Jamais le texte de l'article ni de longues citations, pour respecter l'abonnement et le droit d'auteur. Les entrées vont dans le thème correspondant (assurance, IA ou tech) avec la mention « (Les Echos, abonné) ».

### Rendez-vous à ne pas manquer

- **Chaque mois** : la courbe EIOPA et l'ajustement symétrique actions.
  - Ce sont les données d'entrée des modules M02 (Smith-Wilson) et M06 (skill `scr-marche`).
  - Les noter dans la veille dès leur publication, en début de mois.
- **Chaque trimestre** : les remises QRT (skill `sii-reporting-qrt`) et une éventuelle nouvelle version de la taxonomie EIOPA.
- **Échéances réglementaires**, avec leur date exacte à vérifier dans la synthèse mensuelle :
  - transposition de la directive 2025/2 (FSP/LLFR, qui touche M02) ;
  - obligations de l'AI Act pour les systèmes à haut risque : la tarification et l'évaluation des risques en assurance vie et santé figurent à l'annexe III, et le calendrier peut encore bouger.

## Synthèse mensuelle (dernier vendredi du mois, 15 min)

Dans la section « Synthèse du mois » du fichier mensuel :
1. **Les 3 faits du mois**, un par thème si possible.
2. Relecture des cases « À surveiller » : cocher ce qui est réglé, reporter le reste dans le mois suivant.
3. Mettre à jour la fiche [M00](../../modules/00-etat-de-l-art/README.md) si la gamme de modèles ou les prix ont changé.
4. Choisir **un** sujet à tester dans le lab le mois suivant, par exemple une fonctionnalité Databricks ou un nouveau paramètre d'API.

## Brancher Les Echos (Claude in Chrome)

À faire une seule fois :
1. Installer l'extension **Claude in Chrome** depuis le Chrome Web Store et la connecter à ton compte Claude.
2. Dans Chrome, se connecter à lesechos.fr avec ton abonnement. La session reste ouverte.
3. Lancer Claude Code avec l'intégration navigateur, depuis un terminal à la racine du repo : `claude --chrome`. Dans une session déjà ouverte, `/chrome` permet de vérifier la connexion.

Ensuite, chaque vendredi : `claude --chrome`, puis `/veille`.
- La commande ouvre les rubriques des Echos dans un nouvel onglet de ton Chrome et lit les titres de la semaine.
- Elle ouvre les articles pertinents et ajoute un résumé d'une ligne pour chacun.
- Chrome te demandera d'autoriser le site lesechos.fr la première fois.
- Sans `--chrome`, `/veille` saute Les Echos et le signale dans son résumé.

Ton mot de passe n'est jamais transmis à Claude : il utilise la session déjà ouverte dans ton navigateur.

## Automatiser davantage (optionnel)

- La commande `/veille` peut tourner seule chaque vendredi grâce à une routine planifiée : demander « planifie /veille tous les vendredis à 8 h ». Une routine qui tourne dans le cloud n'a pas accès à ton Chrome : Les Echos restent à faire en session locale avec `--chrome`.
- Le tri reste manuel : c'est ce tri qui fait la valeur de la veille.
- Un lecteur RSS (Feedly, Inoreader, NetNewsWire) avec un dossier par thème reprenant les sources ci-dessus complète la collecte faite par Claude.
