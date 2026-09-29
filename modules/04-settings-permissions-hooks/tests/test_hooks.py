"""Tests des hooks : on simule l'appel de Claude Code (JSON sur stdin)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
HOOKS = ROOT / ".claude" / "hooks"


def run_hook(name: str, event: dict, project: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HOOKS / name)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        check=False,
        env={"CLAUDE_PROJECT_DIR": str(project), "PATH": "/usr/bin:/bin"},
    )


def decision(result: subprocess.CompletedProcess) -> str | None:
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"]


@pytest.mark.parametrize(
    "tool, tool_input",
    [
        ("Write", {"file_path": "data/bilan.csv", "content": "x"}),
        ("Edit", {"file_path": str(ROOT / "data" / "sub" / "a.parquet")}),
        ("Write", {"file_path": "modules/../data/x.csv"}),
        ("Bash", {"command": "echo 1 > data/x.csv"}),
        ("Bash", {"command": "rm -rf data/"}),
        ("Bash", {"command": "cp /tmp/x.csv data/"}),
        ("Bash", {"command": f"mv /tmp/x {ROOT}/data/y"}),
        ("Bash", {"command": "cd modules && touch ../data/x"}),
        ("Bash", {"command": "sed -i '' 's/a/b/' data/bilan.csv"}),
        ("Bash", {"command": "cat a.csv | tee data/b.csv"}),
        ("Bash", {"command": "X=1 rm data/bilan.csv"}),
    ],
)
def test_protect_data_refuse(tool, tool_input):
    result = run_hook("protect_data.py", {"tool_name": tool, "tool_input": tool_input})
    assert result.returncode == 0
    assert decision(result) == "deny"


@pytest.mark.parametrize(
    "tool, tool_input",
    [
        ("Write", {"file_path": "modules/data_utils.py"}),
        ("Write", {"file_path": "notes/data.md"}),
        ("Read", {"file_path": "data/bilan.csv"}),
        ("Bash", {"command": "cat data/bilan.csv | head"}),
        ("Bash", {"command": "uv run python modules/07-mcp/server/make_sample_data.py"}),
        ("Bash", {"command": f"cp {ROOT}/data/obligations.parquet /tmp/test/data/"}),
        ("Bash", {"command": "cp data/bilan.csv /tmp/bilan.csv"}),
        ("Bash", {"command": "ls data/ 2>&1 > /tmp/liste.txt"}),
        ("Bash", {"command": "python3 x.py --out /tmp/data/x.csv"}),
    ],
)
def test_protect_data_laisse_passer(tool, tool_input):
    result = run_hook("protect_data.py", {"tool_name": tool, "tool_input": tool_input})
    assert result.returncode == 0
    assert decision(result) is None


def test_ruff_format_formate_un_fichier_python(tmp_path):
    src = tmp_path / "moche.py"
    src.write_text("x=[1,2 ,3]\n")
    result = run_hook(
        "ruff_format.py", {"tool_name": "Write", "tool_input": {"file_path": str(src)}}
    )
    assert result.returncode == 0, result.stderr
    assert src.read_text() == "x = [1, 2, 3]\n"


def test_ruff_format_ignore_les_autres_fichiers(tmp_path):
    md = tmp_path / "note.md"
    md.write_text("x=[1,2 ,3]\n")
    run_hook("ruff_format.py", {"tool_name": "Write", "tool_input": {"file_path": str(md)}})
    assert md.read_text() == "x=[1,2 ,3]\n"


def test_ruff_format_signale_une_erreur_de_syntaxe(tmp_path):
    src = tmp_path / "casse.py"
    src.write_text("def f(:\n")
    result = run_hook(
        "ruff_format.py", {"tool_name": "Edit", "tool_input": {"file_path": str(src)}}
    )
    assert result.returncode == 2
    assert "ruff format a échoué" in result.stderr
