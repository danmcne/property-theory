# Libertarian Property Theory — v0.16

A formal theory of property grounded in the right to exclude others from
rivalrous resources (TPTP THF, Leo-III v1.7.18; Z3 finite-model checks).

**Current version: 0.16.** All axioms are model-checked: the full axiom set has
a finite Z3 model, and every theorem's antecedent is checked satisfiable (no
vacuous proofs). See CONSISTENCY.md.

## What's new in v0.16 — abandonment → res nullius
Introduces `abandons(P,O,T)`: an owner relinquishing the object against **every**
other party. This bridges the relational `disowns` (one claim at a time) to the
global `unowned` (no owner against anyone), resolving a long-standing gap.
Theorems: `abandoner_not_owner` (abandoning, without re-acquisition, extinguishes
the abandoner's title) and `sole_abandonment_res_nullius` (a sole owner's
abandonment leaves the object unowned, absent re-acquisition — open again to
homesteading).

## Structure
- `libertarian-property-theory-v0.16.thf` — full axiom set + theorem list.
- `minimal/` — 28 self-contained proofs (Leo-III: Theorem).
- `consistency/` — commented Z3 encoding + scenario/non-vacuity checks.
- `VERIFICATION.md`, `CONSISTENCY.md`, `ROADMAP.md`, `CHANGELOG.md`.

## Methodology
Leo-III establishes that the axioms **entail** each theorem; Z3 establishes that
the axioms are **consistent** (a finite model exists) and that each theorem is
**non-vacuous** (its antecedent is satisfiable). Every axiom introduction or
change is gated by re-running the consistency check.

## Running
- Proofs: `java -jar leo3.jar minimal/<name>_minimal.thf -t 70` → `SZS status Theorem`.
- Model checks: `python3 consistency/model_find_v016.py` and `scenarios_v016.py`.
