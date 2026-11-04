# Isolate Infrastructure, Keep Business Logic Real

Do not mock the service under test or internal business decisions to force a branch or obtain a coverage number. Exercise the actual path from public input to observable output or state change.

Use doubles at external boundaries when needed: network providers, clocks, randomness, storage, or filesystem operations. Prefer a lightweight real database or a stateful repository fake for persistence behavior over shallow canned read/write responses. A fake must preserve the semantics the test relies on and must not implement the service's business rule itself.

A stateful fake cannot prove production database transactions, constraints, concurrency, query behavior, or provider compatibility. Use a separate appropriately tiered integration test when those semantics matter. Follow repository service-dependency rules; do not silently require live infrastructure in the default unit suite.

At outbound boundaries, a recording fake can demonstrate externally meaningful behavior: correct payload, no delivery on rejection, or no duplicate charge. Internal helper call counts and ordering are implementation details. Choose assertions according to the contract rather than banning every spy assertion.

Use distinct inputs and configured external responses for success, failure, and malformed-response cases. Do not let a generic stub return success for every request. Keep fixtures representative of the fields and behavior the real contract requires, without inventing unused fields or recreating an entire SDK.

Use existing dependency seams when possible. Add a seam only when it improves the owning abstraction; do not build wrappers or test-only production APIs merely to accommodate mocks.
