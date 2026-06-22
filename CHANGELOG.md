# Changelog

## [0.16] — Abandonment → res nullius (roadmap item 2)

### Added
- `abandons(P,O,T)` predicate and `abandons_def`: abandonment is relinquishing
  ownership against **every** other party (the bridge from relational `disowns`
  to global `unowned`).
- Theorems: `abandons_forward`, `abandoner_not_owner` (abandoning without
  re-acquisition extinguishes the abandoner's title), and
  `sole_abandonment_res_nullius` (a sole owner's abandonment yields an unowned
  object, absent re-acquisition).
- `consistency/` Z3 checks for v0.16, with commented code.

### Verified
- 28/28 theorems Theorem (Leo-III).
- **Axioms model-checked:** full v0.16 axiom set is sat (Z3); res nullius is
  witnessed (a model where the abandoned object becomes unowned); both new
  theorems' antecedents are satisfiable (non-vacuous).

### Notes
- The "no re-acquisition in the interval" proviso in
  `sole_abandonment_res_nullius` is the space left for fresh homesteading of the
  now-ownerless object, not a gap in the result.
- Adding `abandons_def` is a conservative definitional extension; all 25 v0.15
  theorems re-verify unchanged.
