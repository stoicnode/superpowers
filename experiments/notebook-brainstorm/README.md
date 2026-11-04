# Notebook brainstorming experiment

This is a Stoic Node fork experiment. It changes no upstream skill. The first trial uses a Jupyter notebook because the requested visible unit is exactly one Markdown cell followed by one code cell. The full three-step synthetic graph example is prepared in `steps.json`, while `demo.ipynb` currently reveals only step 1.

## Three interview approaches

| Variant | When questions appear | Work while awaiting answers | Visible artifact |
| --- | --- | --- | --- |
| Assumptions-first | After a first sketch | Research, synthetic demo, reversible planning | Draft notebook with assumptions and open questions |
| Upfront interview | Before the demo | Source inspection and research only | Question sheet, then notebook |
| Incremental (first trial) | At each notebook step | Research and remaining workflow preparation | One explanatory Markdown cell and one code cell per step |

The first trial has two lanes. The preparation lane reads source material, drafts the full workflow and test hypotheses, and records provenance. The presentation lane reveals one prepared step, asks the question shown with it, and accepts corrections. An unanswered question leaves its stated assumption in force for reversible demo work. A decision that changes real data access, external publication, or an irreversible action still requires an answer before that specific action.

`notebook_brainstorm.py` appends cells with stable IDs. It never executes them or overwrites a notebook that already exists. Answers go in a sidecar JSON file so human edits to cells survive. Re-revealing a step is idempotent. Reveal steps in order, but the next step does not require an answer to the previous question. When an answer changes an earlier assumption, revise the future prepared steps and explain the change; do not silently rewrite an already revealed cell.

```bash
python3 notebook_brainstorm.py init demo.ipynb "Graph evidence interview"
python3 notebook_brainstorm.py reveal demo.ipynb sources --steps steps.json
python3 notebook_brainstorm.py answer demo.ipynb "Executed agreements and amendments" --step-id sources
python3 notebook_brainstorm.py reveal demo.ipynb edges --steps steps.json
```

Run `python3 -m pytest tests/test_reveal.py -q` for the reveal contract. Run the completed notebook top-to-bottom before claiming that its code produces the described output. In this environment, `nbclient` could not start a kernel because sandbox networking blocks the local socket. The code cells were checked in one Python namespace, but a normal Jupyter run remains an open validation step. The notebook file retains empty outputs so the interview opens cleanly.

For the comparison, use the same problem brief, research budget, evaluator and success criteria in all variants. Record time to first useful artifact, user effort, assumption corrections, rework, notebook execution success, evidence completeness and user control. A single pleasant session is a usability observation, not evidence that one variant is best.

Jupyter's notebook format defines cell IDs and separate Markdown/code cells: https://nbformat.readthedocs.io/en/latest/format_description.html . marimo is a future variant: its reactive dependency graph may rerun downstream cells after edits, so side effects and expensive work need explicit controls: https://docs.marimo.io/guides/reactivity/ .
