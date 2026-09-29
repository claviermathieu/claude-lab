# M03 — Mémoire (CLAUDE.md)

**Objectif** : savoir où placer une consigne pour qu'elle soit chargée au bon endroit, au bon moment, sans gaspiller de contexte.

## Hiérarchie de chargement

| Fichier | Portée | Versionné | Chargement |
|---|---|---|---|
| Politique d'entreprise (managed) | Toute la machine / l'organisation | Non (déployé par l'IT) | Toujours, prioritaire |
| `~/.claude/CLAUDE.md` | Tous tes projets | Non | Toujours |
| `./CLAUDE.md` (ou `./.claude/CLAUDE.md`) | Le projet, partagé en équipe | Oui | Toujours (remontée depuis le cwd jusqu'à la racine) |
| `./CLAUDE.local.md` | Le projet, pour toi seul | Non (`.gitignore`) | Toujours |
| `sous-dossier/CLAUDE.md` | Un sous-arbre | Oui | **À la demande**, quand Claude lit un fichier de ce sous-dossier |

Règle de priorité : en cas de conflit, la consigne la plus spécifique (la plus proche du fichier traité) l'emporte. Mieux vaut ne pas avoir de conflit.

## Imports `@chemin`
Une ligne `@chemin/vers/fichier.md` dans un CLAUDE.md inclut ce fichier (chemins relatifs au fichier qui importe, `~` accepté, profondeur max 5). Usage ici : [`CLAUDE.md`](../../CLAUDE.md) importe [`.claude/conventions-python.md`](../../.claude/conventions-python.md).

⚠️ Un import est chargé **en entier et à chaque session** : ce n'est pas du chargement progressif. Pour de la connaissance volumineuse consultée rarement → un **skill** (M06), ou une simple mention « lire X si besoin » (cf. la ligne sur `ROADMAP.md`).

## Commandes utiles
- `/memory` : ouvre les fichiers de mémoire chargés.
- `/init` : génère un CLAUDE.md initial à partir du code.
- `/context` : voir le poids de la mémoire dans le contexte.

## Ce qui a été mis en place
- **`~/.claude/CLAUDE.md`** (hors repo) : langue et ton, profil actuariel, conventions Python/uv, pas de secrets, GCP par défaut. Copie de référence ci-dessous.
- **`CLAUDE.md` du repo** enrichi : commandes, règle « plugin généré », remote GitHub, import des conventions Python.
- **`CLAUDE.local.md`** : non créé (rien de personnel au projet pour l'instant). Exemple d'usage : `Mon projet GCP de test : xxx-sandbox` — une info propre à ta machine qui ne doit pas aller dans le repo.

### Copie de `~/.claude/CLAUDE.md`
```markdown
# Préférences globales (tous projets)
## Communication
- Répondre en français, directement, sans préambule ni récapitulatif inutile.
- Quand un choix se pose, donner une recommandation argumentée plutôt qu'une liste d'options.
- Signaler clairement ce qui n'a pas pu être vérifié ou exécuté.
## Profil
- Actuaire / data scientist : Solvabilité II, IFRS 9/17, ALM, courbes de taux. …
## Code
- Python : environnement uv local (.venv) … Tests pytest, ruff. Pas de secret en clair. GCP par défaut.
```

## Bonnes pratiques retenues
- Écrire des consignes **vérifiables** (« lancer `uv run pytest -q` ») plutôt que des vœux (« écrire du bon code »).
- Expliquer le *pourquoi* d'une règle non évidente : le modèle généralise mieux.
- Garder chaque CLAUDE.md court (< 100 lignes) : tout y est chargé à chaque tour.
- Relire le CLAUDE.md quand le repo évolue : une consigne périmée est pire qu'aucune.

## Exercices
- [x] `~/.claude/CLAUDE.md` personnel.
- [x] CLAUDE.md du repo enrichi + import `@`.
- [ ] Ajouter un `CLAUDE.md` de sous-dossier (ex. `modules/07-mcp/`) et vérifier avec `/memory` qu'il n'est chargé qu'à la lecture d'un fichier du dossier.
