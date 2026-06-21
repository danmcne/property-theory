# Formal Axioms for Libertarian Property Theory

A formal axiomatic treatment of libertarian property theory in TPTP **THF**
(higher-order logic with Henkin semantics), verified with **Leo-III v1.7.18**.
The theory captures ownership, use, time, homesteading, transfer, and deontic
norms (obligation, permission, prohibition), grounded in the right to exclude
others from a **rivalrous** resource.

**Current version: 13.0.** See `CHANGELOG.md` for the version history and
`ROADMAP.md` for planned work.

## What is new in v13

- **Rivalrousness and manner of use.** `use(P,O,M,T)` now carries a manner /
  purpose `M`. Two uses conflict only when the object is *rivalrous* and the
  manners are *mutually exclusive* (`excl`). The NAP is guarded by
  `rivalrous(O)`: trespass is interference with control over a scarce resource,
  so a non-owner's use of a non-rivalrous good is not aggression.
- **Consistent joint ownership.** Co-owners with clashing exclusive intentions
  cannot both realise their use (`excl_factual`), so at least one intended use is
  unrealised — **under-utilization**, a coordination loss, not a logical
  contradiction. The permission layer and the physical-exclusion layer are kept
  separate; forcing every permitted intention into realisation is exactly what
  re-introduces inconsistency and is deliberately not asserted.
- **Title extinction.** A disowning event now both blocks persistence (`nodis`)
  and *extinguishes* title at the next instant absent re-acquisition
  (`disown_extinguishes`). This makes `transfer_exclusive` a theorem: the
  transferor actually loses title (previously only persistence failed to
  propagate it).
- **The `nodis` frame atom.** The no-disowns interval condition is atomised as
  `nodis(P,O,Q,T1,T2)`. This keeps cross-lemma matching first-order and lets
  `first_homesteader_exclusive_v2` close instead of timing out on the raw nested
  quantifier.

## Structure: a two-track workflow

Running the full theory at once times out (the deontic closure and temporal
quantifiers blow up proof search). The repository is therefore organised as:

- `libertarian-property-theory-v13.thf` — the consolidated **record**: every
  type, axiom, and proved theorem. Parses cleanly; not meant to be proved whole.
- `minimal/` — one **minimal problem file per theorem**, carrying only the
  types, axioms, and prior lemmas that theorem needs. These are what Leo-III
  actually proves. Larger theorems are split into lemmas (e.g. the
  first-homesteader chain A -> B -> C -> D).

## Running Leo-III

```
java -jar leo3.jar minimal/theft_forbidden_minimal.thf -t 60 -p
```

`-t` sets the timeout (seconds); `-p` prints a proof certificate. Every file in
`minimal/` returns `SZS status Theorem`; see `VERIFICATION.md` for the full
sweep with timings.

## Key concepts

- **Time** — sort `tm`; a strict total order (`before`), no density or successor
  axioms, so both dense and discrete models are admitted.
- **Entities** — sort `en`; `person` and `np_obj` are disjoint. Bodies are
  rivalrous (`person_rivalrous`).
- **Manners** — sort `man`; the way/purpose of a use. `excl(M1,M2)` marks
  mutually-exclusive manners.
- **Ownership** — `owns(P,O,Q,T)` is Hohfeldian: P's claim-right against Q over
  O at T. Primitive (not defined via permission); exclusion is derived through
  the NAP.
- **Acquisition** — homesteading (first use + claim of an unowned `np_obj`, with
  a temporal offset T1 -> T2) or voluntary transfer.
- **Deontic logic** — `ob`, `per`, `fbd` as `$o > $o` under KD plus the liberty
  principle. `per(phi) <=> ~fbd(phi)` for use-atoms; all obligations are duties
  to refrain (no positive obligations).

## Theorem set (all machine-proved)

Foundational: `theft_forbidden`, `bodily_integrity`, `person_unownable`,
`person_protection_prereqs`, `nap_person`, `self`/`owner` use permissions.
Acquisition and title: `homesteader_is_owner_v2`, `homesteader_may_use_v2`,
`homesteader_owns_v2`, `owns_not_unowned`, `persistence_from_homestead`,
`first_homesteader_exclusive_v2`, `nemo_dat`, `transfer_exclusive`.
Normative structure: `per_or_fbd`, `theft_retains_ownership`,
`voluntary_slavery_impossible`.
Rivalrousness and joint ownership: `joint_conflict_no_contradiction`,
`under_utilization`.

## Questions or contributions

Open an issue or submit a pull request.
