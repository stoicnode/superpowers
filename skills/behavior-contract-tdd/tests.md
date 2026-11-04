# Independent Expectations and Useful Tests

Expected results come from the contract, a hand-checked example, or an independent oracle. Prefer explicit literals for concrete examples. Never derive expected values from the production helper, private constants, or copied implementation logic.

Variables, parameterized cases, loops over fixtures, and property-based tests are valid. The question is whether the oracle can disagree with broken production behavior. Independent invariants such as conservation, monotonicity, or idempotence can complement example assertions. A round-trip alone can miss matching defects in both directions; include independently known examples where that matters.

## Observe service outcomes

```python
def test_reservation_reduces_available_stock():
    service = ReservationService(stock={"book": 5})
    receipt = service.reserve("alice", "book", 2, key="r1")
    assert receipt == {"actor": "alice", "sku": "book", "quantity": 2, "key": "r1"}
    assert service.available("book") == 3
```

Removing the stock write must fail the availability assertion. Returning a fabricated receipt should fail the receipt assertion. Neither assertion reaches into a private dictionary or depends on a helper's name.

A test that replaces `service.reserve` with a mock returning this receipt only verifies its setup. Keep the service real and isolate infrastructure below it, if necessary.

## Distinguish rejection paths

Test success, invalid input, denied access, and external failure with fixtures that isolate the intended cause. An authorization test must otherwise have valid input and sufficient resources. Check the public error type or stable error code, and check relevant state remains unchanged. Assert exact message text only when that text is part of the contract. A generic exception assertion can pass because an entirely different operation failed.

Use boundary pairs where off-by-one behavior matters. A test above a limit does not prove what happens exactly at the limit.

## Prune without losing protection

- Replace private-helper existence, internal call counts, and private storage-layout assertions with observable results.
- Keep multiple tests when they protect distinct outcomes, even if they traverse the same lines.
- Consolidate duplicate examples only when the remaining inputs and assertions still expose the meaningful faults.
- A contractually required external interaction, such as no duplicate payment, is behavior. It can justify recording outbound requests and asserting their content and multiplicity.
- Synthetic fixtures are useful when grounded in the contract and passed through the real path under test. They do not establish real file extraction, database semantics, or provider compatibility if those paths were replaced. Label the tested boundary honestly.

Run a targeted mutation against replacement coverage before removing the original meaningful check. Record what was retained; fewer tests is not itself a quality result.
