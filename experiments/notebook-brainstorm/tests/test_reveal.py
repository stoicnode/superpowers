import json
from pathlib import Path

from notebook_brainstorm import initialize, reveal, record_answer


def test_reveal_preserves_edits_and_does_not_wait_for_answers(tmp_path):
    path = tmp_path / "demo.ipynb"
    steps = [
        {"id": "sources", "title": "Sources", "explanation": "Show sources", "code": "sources = ['agreement']", "assumption": "Synthetic data", "question": "Which real source?"},
        {"id": "links", "title": "Links", "explanation": "Show links", "code": "links = [('agreement', 'consent')]", "assumption": "One link", "question": "Any amendments?"},
    ]
    initialize(path, "Graph evidence demo")
    assert reveal(path, steps, "sources") == "revealed"
    notebook = json.loads(path.read_text())
    assert [cell["cell_type"] for cell in notebook["cells"]] == ["markdown", "markdown", "code"]
    assert "Synthetic data" in "".join(notebook["cells"][1]["source"])
    notebook["cells"][1]["source"].append("\nMy note stays.")
    path.write_text(json.dumps(notebook))
    assert reveal(path, steps, "sources") == "already revealed"
    assert reveal(path, steps, "links") == "revealed"
    notebook = json.loads(path.read_text())
    assert len(notebook["cells"]) == 5
    assert "My note stays." in "".join(notebook["cells"][1]["source"])
    assert "Any amendments?" in "".join(notebook["cells"][3]["source"])


def test_answers_are_recorded_separately_without_rewriting_notebook(tmp_path):
    path = tmp_path / "demo.ipynb"
    initialize(path, "Demo")
    before = path.read_bytes()
    record_answer(path, "sources", "Use executed agreements")
    assert path.read_bytes() == before
    answers = json.loads(Path(str(path) + ".answers.json").read_text())
    assert answers == {"sources": "Use executed agreements"}
