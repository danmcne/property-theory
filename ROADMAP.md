# Roadmap

## Done
- **[DONE] Consistency witness** (Z3) — and now a standing methodology: every
  axiom change is gated by a full-set satisfiability check, and every theorem is
  checked non-vacuous.
- **[DONE] Non-rivalrous use permitted (IP)** — unconditional via `rivalrous_ownable`.
- **[DONE] Reified / non-collapsing deontics** (v0.14).
- **[DONE] Q-dimension: person-scoped consent** (v0.15) — one rule unifies
  unowned-use, self-use, NAP, theft, bodily integrity, and the co-ownership veto.
- **[DONE] Abandonment → res nullius** (v0.16, item 2).

## Near-term (priority)
- **4. Object-relative exclusivity** `excl_o(O,M1,M2)`: incompatibility of manners
  relative to a specific object (looking-at vs plowing the same field).

## Later
- Partition of co-owned objects; share-vs-whole transfer semantics.
- Consent dynamics over time (given/withdrawn; standing consent).
- A re-homesteading theorem chaining `sole_abandonment_res_nullius` into
  `homesteader_owns_v2` (abandon → res nullius → re-homestead).
- Positive obligations / contracts.
- Run Nitpick / Paradox / Mace4 / cvc5 / Vampire-fmb directly on the TPTP
  (pure first-order after reification — no `$o`-expansion needed).
