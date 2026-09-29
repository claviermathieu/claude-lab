"""Tests du hook de contrôle qualité des notes ALM."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[3] / ".claude" / "hooks" / "check_note_alm.py"

NOTE_OK = """# Note ALM — risque de taux — 2026-09-29
## Synthèse
Exposition faible.
Gap +0,65.
Réconcilier le BE.
## Données et hypothèses
obligations.parquet (DVC 0ed5d119), flux_passif.parquet (DVC 2266e3ae).
## Réconciliation des sources
…
## Duration gap et sensibilités
…
## Limites
…
## Actions proposées
…
## Validation
Validé avec réserves.
"""


def lancer(tmp_path, contenu, nom="notes/alm/note.md"):
    chemin = tmp_path / nom
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(contenu, encoding="utf-8")
    event = {"tool_name": "Write", "tool_input": {"file_path": str(chemin)}}
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        check=False,
    )


def test_note_conforme(tmp_path):
    assert lancer(tmp_path, NOTE_OK).returncode == 0


def test_autres_fichiers_ignores(tmp_path):
    assert lancer(tmp_path, "brouillon TODO", nom="notes/autre.md").returncode == 0


@pytest.mark.parametrize(
    "modif, message",
    [
        (lambda t: t.replace("## Limites\n", ""), "sections manquantes : ## Limites"),
        (lambda t: t.replace("DVC 0ed5d119", "v1").replace("DVC 2266e3ae", "v1"), "DVC"),
        (lambda t: t.replace("Validé avec réserves.", "TODO"), "brouillon"),
        (lambda t: t.replace("Exposition faible.", "a\nb\nc"), "3 lignes"),
        (
            lambda t: (
                t.replace("## Limites", "## TMP")
                .replace("## Actions proposées", "## Limites")
                .replace("## TMP", "## Actions proposées")
            ),
            "désordre",
        ),
    ],
)
def test_note_non_conforme(tmp_path, modif, message):
    res = lancer(tmp_path, modif(NOTE_OK))
    assert res.returncode == 2
    assert message in res.stderr


def test_date_n_est_pas_un_hash(tmp_path):
    texte = NOTE_OK.replace("DVC 0ed5d119", "20260929").replace("DVC 2266e3ae", "")
    assert "DVC" in lancer(tmp_path, texte).stderr
