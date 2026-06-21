# Changelog

All notable changes to the formal theory. Versions refer to the main file
`libertarian-property-theory-vN.thf`. Proof timings are from Leo-III v1.7.18.

## [13.0] — Rivalrousness, joint ownership, title extinction

### Added
- **Sort `man`** (manners / purposes of use). `use` is now 4-ary
  `use(P,O,M,T)`. Every prior `use`-based axiom and theorem is lifted to carry
  the manner argument (universally quantified unless otherwise constrained).
- **`rivalrous(O)`** and **`person_rivalrous`** (`person(P) => rivalrous(P)`):
  bodies are rivalrous resources. Whether a given `np_obj` is rivalrous is left
  open, so non-rivalrous goods are representable.
- **`excl(M1,M2)`** and **`excl_factual`**: on a rivalrous object, two
  mutually-exclusive manners cannot be jointly realised. This is a *physical*
  constraint on co-occurrence, not a normative one.
- **`wants` / `unrealised` (`unrealised_def`)**: model intention and
  under-utilization.
- **`nodis(P,O,Q,T1,T2)` (`nodis_def`)**: atomises the no-disowns interval
  condition used by persistence.
- **`reacquires` and `disown_extinguishes`**: title-extinction. A disowning
  event terminates ownership at the next instant absent re-acquisition.
- **New theorems** (all proved): `transfer_exclusive`,
  `joint_conflict_no_contradiction`, `under_utilization`.

### Changed
- **NAP is now rivalrous-guarded**: `owns(P,O,Q,T) & rivalrous(O) & ~allows &
  ~is_owner(Q,O,T) => fbd(use(Q,O,M,T))`. Trespass is interference with control
  over a scarce resource (Kinsella-routing). `theft_forbidden` carries
  `rivalrous(O)` in its antecedent; `nap_person` and `bodily_integrity` obtain
  rivalrousness of the body from `person_rivalrous`.
- **`ownership_persistence`** restated with `nodis` (was a raw nested
  quantifier). The biconditional `nodis_def` pins the meaning in the record file;
  minimal proof files keep `nodis` opaque to stay fast.
- **`first_homesteader_exclusive_v2` (step D) now proves** (2.1 s). Under v12 the
  raw nested interval quantifier caused Leo-III's clausifier to blow up during
  cross-lemma matching (Timeout at 300 s). Atomising the frame condition as
  `nodis` makes the A/B/C/D chain close.
- Rivalrousness theorems stated in **general (scenario-free) form** rather than
  baking specific scenario constants into the theory.

### Fixed
- **Title extinction gap (from the v12 review).** `disowns` previously only
  blocked persistence; it never removed title, so transfer exclusivity and
  abandonment -> res nullius were not theorems (transferor and transferee could
  both own). `disown_extinguishes` closes this; `transfer_exclusive` is now
  proved.

### Notes / pitfalls recorded
- **The realisation trap.** An axiom "permitted intention => realised use" forces
  both co-owners' exclusive uses and collides with `excl_factual`, making the
  joint-ownership scenario inconsistent and the under-utilization theorem
  *vacuous*. The resource must arbitrate realisation (at most one exclusive
  manner actual). No such forcing axiom is asserted; `under_utilization` was
  re-derived without it and checked non-vacuous (neither disjunct is forced; the
  scenario does not entail `$false`).
- **Consistency is entailment-checked, not model-checked.** No minimal file
  derives `$false`, but a positive finite-model witness (Nitpick / Paradox) is
  still outstanding — see ROADMAP.

## [12.0] and earlier
See the v12 file header for the full prior history: temporal homesteading fix
(ownership begins at T2 > T1), co-owner guard in the NAP (S3), all-owner consent
(S4), removal of `self_ownership_obligation` (S2), `use_typing` widening for
bodily integrity (C2), and the promotion of `theft_forbidden`, `person_unownable`,
`nap_person`, `bodily_integrity`, `homesteader_*_v2`, `voluntary_slavery_impossible`,
`theft_retains_ownership`, `per_or_fbd`, and `nemo_dat` to proved theorems.
