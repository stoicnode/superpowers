---
name: notebook-brainstorming
description: Use when a human partner wants an interactive code and visual brainstorming interview in a Jupyter notebook before finalizing a design or test plan.
---

# Notebook brainstorming (experimental)

Use this fork-specific skill for the incremental interview trial. Read `experiments/notebook-brainstorm/README.md` and the current project's context first. Preserve the human partner's stated goal, audience and success criteria. Research the relevant source code, documents and test boundaries before drafting the demo.

Prepare the full workflow privately as ordered steps, with independently grounded expected outcomes, source links, assumptions, one question per step, and a small runnable code example. Record what was observed versus inferred. Keep the first visible step small enough to inspect in one sitting.

From `experiments/notebook-brainstorm/`, create a Jupyter notebook with `python3 notebook_brainstorm.py init ...`; reveal one step with `python3 notebook_brainstorm.py reveal ... --steps ...`. Each reveal appends an explanatory Markdown cell and one code cell. Show that pair to the human partner and ask the question in the Markdown cell. State the provisional answer you used and what would change if it is corrected. Do not describe unexecuted code as a verified result.

While a question is unanswered, continue independent research and prepare later steps. Keep demo code synthetic and reversible. When a reply arrives, record it with `answer`, update unrevealed steps, and call out any earlier cell that needs revision. Never silently replace a cell the human partner may have edited. Continue the visible sequence one pair at a time. Prepare a full implementation test plan only after the interview has exposed the important contracts and unresolved decisions; label any remaining assumptions in that plan.

For feature tests, use `behavior-contract-tdd`: public behavior examples, independent expectations, an observed red failure, green run and a focused mutation check. Run the notebook top-to-bottom and report execution errors before claiming the demo works. Keep the comparison with upfront questions and assumptions-first in `experiments/notebook-brainstorm/README.md`; do not declare a winner without repeated trials.
