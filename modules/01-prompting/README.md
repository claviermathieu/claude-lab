# M01 — Prompting

**Objectif** : maîtriser les leviers d'un bon prompt (rôle, contexte, balises XML, exemples, format de sortie, décomposition) et mesurer leur effet sur un cas métier.

## Leviers (guide Anthropic, résumé)

| Levier | Pourquoi | Piège |
|---|---|---|
| **Rôle** (system ou début de prompt) | Cadre le vocabulaire et le niveau d'exigence. | Un rôle sans contexte n'apporte presque rien. |
| **Contexte + enjeu** | Le modèle arbitre mieux quand il sait *pourquoi* (qui lit, coût d'une erreur, coût d'une fausse alerte). | Oublier l'enjeu inverse : sans lui, le modèle sur-signale. |
| **Balises XML** (`<note>`, `<consignes>`) | Sépare données et instructions, évite que le modèle confonde les deux. | Aucune balise n'est « magique » : les noms doivent juste être clairs et cohérents. |
| **Exemples** (few-shot) | Fixe le format et le niveau de détail attendus. | Le modèle copie aussi le *contenu* de l'exemple → choisir un exemple hors du cas traité. |
| **Format de sortie** | Rend la réponse exploitable (tableau, JSON). Pour du JSON strict : *structured outputs* côté API. | Pas de prefill sur les modèles récents. |
| **Décomposition** (étapes, `<analyse>` puis `<rapport>`) | Force la vérification systématique. | Voir résultats : peut aussi *cristalliser* une erreur de raisonnement. |

Avec les modèles à thinking adaptatif, demander « réfléchis étape par étape » est moins utile qu'avant : le modèle raisonne déjà en interne. La décomposition sert surtout à imposer une **checklist métier** et un **format**.

## Exercice : revue d'une note de calcul SCR marché

- Cas : [cas/note-scr-marche.md](cas/note-scr-marche.md) — 3 erreurs volontaires (choc actions type 2, choc immobilier, paramètre A). Corrigé : [cas/corrige.md](cas/corrige.md).
- Prompts : [v1 naïf](prompts/v1-naif.md) → [v2 structuré](prompts/v2-structure.md) (rôle, contexte, XML, format) → [v3 décomposé](prompts/v3-decompose.md) (+ méthode en 5 étapes, exemple, contre-vérification).
- Lancement : `./run.sh sonnet` ou `./run.sh opus` (Claude Code en headless `claude -p`, sans outils). Sorties dans [resultats/](resultats/).

### Résultats (1 exécution par couple, 29/09/2026)

Grille : +1 par erreur trouvée et corrigée, +1 si SCR corrigé = 206,5 ± 1, −1 par faux positif. Max 4.

| Prompt | Sonnet 5.5 | Opus 5.5 | Longueur (mots, S / O) |
|---|---|---|---|
| v1 naïf | **4/4** | **4/4** | 365 / 505 |
| v2 structuré | **4/4** (+ points d'attention pertinents) | **4/4** (+ liste « ce qui est correct ») | 354 / 673 |
| v3 décomposé | **2/4** — rate le paramètre A (règle inversée), SCR 176,8 | **4/4** + impact isolé de chaque erreur | 909 / 1629 |

### Enseignements
1. **Sur un cas bien connu, le prompt naïf suffit** : les chocs de la formule standard sont dans les connaissances du modèle. Le gain de v2 est dans la *forme* (tableau exploitable, points d'attention, distinction erreur / hypothèse), pas dans la détection.
2. **v3 a fait régresser Sonnet.** En nommant le paramètre A dans la méthode, le prompt a poussé le modèle à rédiger la règle… et il l'a énoncée à l'envers, puis s'est appuyé sur cette règle fausse pour « valider » la matrice. Une checklist rend l'erreur *plus confiante*, pas moins probable. Parade : donner la règle exacte dans le prompt (ou via un skill méthodo, cf. M06) plutôt que de demander au modèle de la retrouver.
3. **Le modèle compte plus que le prompt sur le raisonnement réglementaire fin** : Opus ne se trompe sur aucune version.
4. **La décomposition double la longueur** (et le coût de sortie). À réserver aux cas où la traçabilité du raisonnement a une valeur (dossier de validation).
5. **n = 1 ne prouve rien** : relancer chaque couple 5 fois pour mesurer la variance avant de conclure (cf. `build-eval` en M09).

### Prompt retenu
v2 + référentiel exact des paramètres, industrialisé comme skill [`scr-marche`](../../.claude/skills/scr-marche/SKILL.md) en M06 : avec lui, même le prompt v3 sur Sonnet obtient 4/4.

## Exercices
- [x] 3 versions de prompt, exécutées sur Sonnet et Opus, comparées.
- [x] Apport du référentiel exact : fait sous forme de skill `scr-marche` (M06). Sonnet v3 + skill → **4/4** ([résultat](resultats/v3-decompose-sonnet-avec-skill.md)).
- [ ] Relancer 5× chaque couple pour mesurer la variance.
