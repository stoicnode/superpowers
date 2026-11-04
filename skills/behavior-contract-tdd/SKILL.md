---
name: behavior-contract-tdd
description: Build features and fix bugs test-first, or strengthen and prune weak tests using public behavior contracts and targeted mutation checks. Use for TDD, red-green-refactor, or requests to replace brittle or tautological tests.
---

# Behavior-Contract TDD

Write tests worth keeping: a small suite that detects meaningful changes to public behavior. Work one behavior at a time through **contract -> red -> green -> mutate -> restore -> refactor**. Passing tests alone do not demonstrate that assertions discriminate correct from broken behavior.

Read relevant `CONTEXT.md` and accepted ADRs when present. Use the project's test runner and test tiers. Read [tests.md](tests.md) for assertion design and suite pruning; read [mocking.md](mocking.md) when choosing test doubles.

## Choose the contract

Start at the public service or application boundary that owns the requested behavior. Record the inputs, independently established expected outcomes, observable state changes, and important rejection paths. Use boundaries already specified by the user or established by the project; ask only when a material contract or scope decision is unresolved.

Exercise real business logic. Do not target private helpers, internal constants, or internal call sequences. A public library function, parser, or pure algorithm can itself be the appropriate boundary; do not invent a service wrapper just for testing. Prefer service read APIs to observe persisted effects. If persistence or an outbound message is the contract, direct observation at that boundary is valid.

Prioritize meaningful failures: lost state, incorrect results, authorization, boundaries, retries, and errors relevant to the request. Do not create one test per method or chase a test count or coverage percentage. Multiple assertions may describe one coherent outcome, including the absence of unintended effects.

## New behavior and bug fixes

1. **Red:** Write one focused contract test. For a bug, reproduce the user-visible failure through the closest practical end-to-end path. Run the test and inspect why it fails. Import, syntax, fixture, or infrastructure failures do not establish behavioral red. If it already passes, determine whether the behavior already exists or the assertion misses it; do not distort a valid expectation just to force failure.
2. **Green:** Implement only the requested behavior needed by this slice. Run the focused test and relevant surrounding tests. Do not weaken a correct assertion to fit the implementation.
3. **Mutate:** Apply the gate below to the behavior just added or changed. For Python tests, use the automated workflow in [python-mutation-testing.md](python-mutation-testing.md) when the test runner supports it.
4. **Restore and refactor:** Restore the unmutated implementation and verify green before local cleanup. Refactor code and tests while keeping the public contract intact, then rerun relevant checks. Repeat the mutation check if the assertion or behavior under scrutiny changes materially.

Write executable tests incrementally, not a batch transcribed from an unrun plan. A plan should describe behavioral examples; any included test code remains unverified until executed.

## Mutation gate

Before declaring a new or strengthened behavior test verified, run a small, deliberate mutation of the production path it exercises. Choose a plausible fault with a specified observable difference: change a boundary comparison, bypass a rejection, drop a state write, return the wrong result, or repeat a side effect. Target important assertions; one arbitrary killed mutant does not validate the whole suite. When a contract applies across distinct public scenarios, such as initial calls and retries, exercise each scenario. A mutation on one path does not verify the others.

- Establish an unmutated green baseline first. Mutate only an isolated test workspace or local code that cannot affect a running service. Preserve pre-existing user edits and capture the exact pre-mutation contents.
- Change one behavior at a time and run the relevant test. Inspect the failure: the expected contract assertion must catch it. Syntax errors, crashes unrelated to the contract, timeouts, and broken fixtures are inconclusive, not killed mutants.
- If it survives, check whether the mutation executed and changed specified behavior for the supplied input. An equivalent mutation, unreachable path, or out-of-scope behavior is not automatically a defective assertion. Explain exclusions rather than manufacturing a test for an implementation detail.
- For a genuine gap, identify the observable difference, restore production, add or strengthen the independent expectation, and rerun both the original and the same mutant. Retain coverage of the contract; simply deleting the blind assertion does not fix the gap.
- Restore exact pre-mutation code after every attempt, including failed or interrupted runs, before continuing. Avoid blanket resets or checkouts. Verify restoration and finish with passing tests on the restored code.

For Python, prefer a focused mutmut run against the changed behavior when its pytest-based execution can run the project's tests; read [python-mutation-testing.md](python-mutation-testing.md) for setup, commands, and result interpretation. Automated mutants sample syntax, not every business fault. Use a targeted manual mutation for an important contract difference mutmut did not generate, or when mutmut cannot run the relevant tests. For other languages, use an existing mutation runner when justified or perform a surgical manual check. If safe execution is unavailable, report the gate as unverified and why. Do not claim a mental mutation was executed or leave mutations behind to make a test pass.

## Existing-suite repair and pruning

For each affected test, identify the contract it protects and whether it exercises production logic. Replace self-fulfilling mocks and private-structure checks with public outcomes. Before deleting a test, demonstrate that its meaningful behavior is preserved elsewhere or is outside the current contract; do not delete valid low-level algorithm, adapter, or integration coverage merely because a service test exists.

Run the affected suite before and after changes. Existing correct behavior need not fail on unmodified production: use an executed mutation to establish discrimination. For uncovered behavior, write a replacement, demonstrate green and the relevant mutant failure, then remove the redundant check. Use distinct inputs for distinct rejection causes so the wrong branch cannot satisfy a generic error assertion.

## Completion evidence

Report the contract tested, tests added/replaced/removed and why, commands and observed red/green outcomes, each mutation and the assertion that caught it, any survivors or unverified paths, and final restored green status. Distinguish sampled mutation evidence from exhaustive correctness or full integration coverage.
