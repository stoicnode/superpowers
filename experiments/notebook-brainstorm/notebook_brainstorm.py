"""Reveal one researched notebook step at a time without blocking on answers."""

import argparse
import json
import os
from pathlib import Path
import tempfile


def _save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        json.dump(value, tmp, indent=1, ensure_ascii=False)
        tmp.write("\n")
        name = tmp.name
    os.replace(name, path)


def _lines(value: str) -> list:
    return value.splitlines(keepends=True)


def initialize(path: Path, title: str) -> None:
    if path.exists():
        raise FileExistsError(path)
    _save(path, {
        "cells": [{"cell_type": "markdown", "id": "intro", "metadata": {},
                   "source": _lines(f"# {title}\n\nSteps appear one at a time. Questions record assumptions and never pause independent research.\n")}],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "nbformat": 4, "nbformat_minor": 5,
    })


def reveal(path: Path, steps: list[dict], step_id: str) -> str:
    ids = [step["id"] for step in steps]
    if len(ids) != len(set(ids)) or step_id not in ids:
        raise ValueError("Step IDs must be unique and requested ID must exist")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    existing = {cell.get("id") for cell in notebook["cells"]}
    if f"{step_id}-code" in existing:
        return "already revealed"
    previous = ids[:ids.index(step_id)]
    if any(f"{item}-code" not in existing for item in previous):
        raise ValueError("Reveal earlier steps first")
    step = steps[ids.index(step_id)]
    markdown = (f"## {step['title']}\n\n{step['explanation']}\n\n"
                f"**Assumption:** {step['assumption']}\n\n"
                f"**Question:** {step['question']}\n\n"
                "You can answer later; the next step is not blocked.\n")
    notebook["cells"].extend([
        {"cell_type": "markdown", "id": f"{step_id}-notes", "metadata": {}, "source": _lines(markdown)},
        {"cell_type": "code", "id": f"{step_id}-code", "metadata": {}, "source": _lines(step["code"]),
         "execution_count": None, "outputs": []},
    ])
    _save(path, notebook)
    return "revealed"


def record_answer(path: Path, step_id: str, answer: str) -> None:
    answer_path = Path(str(path) + ".answers.json")
    answers = json.loads(answer_path.read_text(encoding="utf-8")) if answer_path.exists() else {}
    answers[step_id] = answer
    _save(answer_path, answers)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "reveal", "answer"))
    parser.add_argument("notebook", type=Path)
    parser.add_argument("value", help="Title, step ID, or answer text")
    parser.add_argument("--steps", type=Path, help="Prepared JSON array of researched steps")
    parser.add_argument("--step-id", help="Step ID when recording an answer")
    args = parser.parse_args()
    if args.action == "init":
        initialize(args.notebook, args.value)
    elif args.action == "reveal":
        if args.steps is None:
            parser.error("reveal requires --steps")
        print(reveal(args.notebook, json.loads(args.steps.read_text(encoding="utf-8")), args.value))
    else:
        if args.step_id is None:
            parser.error("answer requires --step-id")
        record_answer(args.notebook, args.step_id, args.value)


if __name__ == "__main__":
    main()
