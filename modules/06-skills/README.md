# M06 — Skills

**Objectif** : empaqueter de la connaissance métier et des outils (scripts, templates) que Claude charge **seulement quand c'est utile**.

## Anatomie d'un skill
```
.claude/skills/<nom>/
├── SKILL.md          # frontmatter (name, description) + instructions
├── scripts/          # code exécuté par Claude (sortie seule en contexte, pas le code)
├── templates/ …      # fichiers lus à la demande
```
- **Chargement progressif** : seuls `name` + `description` sont dans le contexte en permanence. Le corps de `SKILL.md` n'est lu que quand Claude décide de l'utiliser (outil `Skill`) ; les fichiers annexes seulement s'il les ouvre ; les scripts sont exécutés sans être lus.
- **Scopes** : perso `~/.claude/skills/`, projet `.claude/skills/`, plugin (M08). Mêmes skills utilisables sur claude.ai (upload zip) et via l'API (`container.skills` + code execution).
- Frontmatter optionnel : `allowed-tools`, `model`, `disable-model-invocation: true` (skill appelable seulement à la main, comme une commande).
- `claude plugin validate .claude` vérifie la structure des skills, agents et commandes.

## Skills livrés

| Skill | Contenu | Script |
|---|---|---|
| [`scr-marche`](../../.claude/skills/scr-marche/SKILL.md) | Chocs et matrice de corrélation faisant foi (RD 2015/35), règle du paramètre A, checklist de revue | `scr_marche.py` : SCR marché complet, JSON possible |
| [`ifrs9-ecl`](../../.claude/skills/ifrs9-ecl/SKILL.md) | Staging, SICR (quantitatif, qualitatif, backstops), formule ECL, scénarios pondérés, contrôles | `ecl.py` : staging + ECL 12 mois / lifetime depuis 2 CSV ; jeu d'exemple 8 expositions |
| [`sii-reporting-qrt`](../../.claude/skills/sii-reporting-qrt/SKILL.md) | États QRT et délais, pièges fréquents | `check_qrt.py` : 9 contrôles inter-états paramétrables (CSV) ; checklist de clôture |

Scripts en **bibliothèque standard** (exécutables avec le `python3` système, sans venv) : un skill doit fonctionner partout où il est copié. Tests : [tests/test_skills_scripts.py](tests/test_skills_scripts.py) (23 cas, dont reproduction du corrigé M01 à 0,01 près).

## Tester le déclenchement
[`test_declenchement.sh`](test_declenchement.sh) lance 4 prompts en headless (`--output-format stream-json`) et relève les appels à l'outil `Skill` :

| Prompt | Attendu | 1er essai | Après réécriture de `scr-marche` |
|---|---|---|---|
| Prêt conso à 45 jours d'impayés, stage et provision ? | ifrs9-ecl | ✅ | ✅ |
| Contrôles S.02.01 ↔ S.23.01 avant remise ? | sii-reporting-qrt | ✅ | ✅ |
| Choc de taux à la baisse : corrélation taux/actions ? | scr-marche | ❌ aucun | ✅ ✅ (2/2) |
| Duration de Macaulay vs modifiée (témoin) | aucun | ✅ | ✅ |

**Leçon** : une description purement descriptive (« référentiel et calculateur… ») ne suffit pas quand le modèle *croit* connaître la réponse — il répond de mémoire. La description réécrite dit *quand* charger et *pourquoi* (« charger AVANT de répondre…, même si la réponse paraît connue — source fréquente d'erreurs de mémoire »). La description est un prompt de routage : elle doit être écrite pour la décision, pas pour la documentation.

## Effet mesuré sur l'exercice M01
Prompt v3 (celui qui faisait échouer Sonnet 5.5 : 2/4, règle du A inversée) relancé avec les skills disponibles : **4/4**, A = 0,5 identifié, SCR corrigé 206,5 recalculé avec `scr_marche.py`, impact de chaque erreur isolé. Coût 0,14 $. Sortie : [../01-prompting/resultats/v3-decompose-sonnet-avec-skill.md](../01-prompting/resultats/v3-decompose-sonnet-avec-skill.md).

## Exercices
- [x] Skill `ifrs9-ecl` (méthodo + script).
- [x] Skill `sii-reporting-qrt` (checklist + templates + contrôles).
- [x] Skill `scr-marche` (issu de l'enseignement de M01).
- [x] Test de déclenchement et réécriture de description.
- [ ] Charger `ifrs9-ecl` sur claude.ai (zip) et via l'API (`container.skills`) pour comparer les surfaces.
