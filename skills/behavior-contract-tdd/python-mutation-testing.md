# Python Mutation Checks with mutmut

Use mutmut for a focused automated check when the relevant Python tests run under pytest. It also collects many `unittest` tests through pytest. Keep the project's normal test command as the green baseline; mutation testing does not replace it.

1. Run the focused tests unmutated and confirm green. Use an isolated checkout when test setup or generated files could affect the working tree. Keep the normal project dependency environment available to mutmut and its pytest workers. If mutmut is absent, use the project's development dependency workflow or an isolated tool environment with access to those dependencies; do not add a permanent dependency solely for one check.
2. Scope the source and tests to the behavior under review. For example, in the isolated checkout's `pyproject.toml`:

   ```toml
   [tool.mutmut]
   source_paths = ["src/orders/"]
   pytest_add_cli_args_test_selection = ["tests/test_orders.py"]
   ```

   Adapt paths to the project. If it already configures mutmut, use its config rather than replacing it. Do not narrow scope or exclude mutants simply to improve a score. Record the chosen scope. Source paths may also name a single Python file. mutmut needs a fork-capable system; run inside WSL on Windows. It runs pytest, so a suite that requires a different runner needs a different mutation tool or a manual check.
3. Run `mutmut run`, then `mutmut results`. Inspect surviving or suspicious mutants with `mutmut show <mutant-id>`. `mutmut export-cicd-stats` writes `mutants/mutmut-cicd-stats.json` with killed, survived, no-tests, timeout, and other counts. Keep the `mutants/` results outside deliverable source or in the project's ignored output area. Do not use `mutmut apply` to inspect a mutant; it writes mutated code to disk.
4. For a survivor, determine whether the mutation changes specified public behavior for an input that the suite should cover. Add or strengthen an independent assertion for a real gap, rerun the focused tests and that mutant, then verify the unmutated suite. An equivalent mutation, mutation with no relevant test, timeout, tool crash, or unrelated fixture failure is not proof of a weak assertion. Report it separately and investigate when relevant.
5. Check important contract paths that mutmut did not generate. For example, a tool run that changes literals and comparisons may never test whether returning a mutable internal object allows a later caller to corrupt state. Use a surgical manual mutation for that specific gap. Verify source restoration and final green tests.

Keep runs bounded to the changed service or module and related tests. Expand only when those results expose a concrete need. Do not treat a mutation score as a goal: report the meaningful survivors, exclusions, command, scope, and coverage limits.

See the [mutmut documentation](https://mutmut.readthedocs.io/en/latest/) for current configuration and CLI options.
