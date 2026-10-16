# Changelog

## [0.23] — Veto co-ownership versus free-use co-ownership

### Added
- Theorems `free_use_unsettled` (co-owners with titles against outsiders only: two clashing uses are
  both permitted, at most one can happen) and `veto_settles_conflict` (co-owners who are full owners:
  two uses are both permitted only if each consents to the other's).
- Scenarios `free_use_ada_acts_first` and `free_use_ben_acts_first`: the free-use form allows either
  outcome, with no aggression in either.
- README section "Two forms of co-ownership"; THEORY §2.5.

### Changed
- ARGUMENT.md §7 and the Substack essay: legal "free use" co-ownership is either a bare permission that
  settles nothing (whoever acts first wins) or a guarantee that reproduces the control view's
  contradiction. Either way the parties cannot both have free use and must go to a majority, a court or
  a sale. Earlier text called it merely "not contradictory"; that reading treated legal free use as a bare
  permission and left out the protection against ouster that the law attaches to it.

## [0.22] — Titles per manner, acceptance, defence, leases and easements; the direction view

### Changed
- **Titles per manner.** `owns`, `disowns`, `grants`, `acquires` and `nodis_upto` take a manner
  argument: `owns(P,O,Q,M,T)` = P may exclude Q from using O in manner M at T. Homesteading
  still yields titles in every manner. `self_ownership` covers every manner.
- **Acceptance.** New primitive `accepts(P,R,O,T)`; a grant takes effect only if accepted
  (`acquires_def`).
- **Defence.** New definitions `aggresses_in_def` and `forfeits_def`; `aggresses_def` and
  `may_use_def` ignore forfeited titles. While R aggresses against Q in manner M, R forfeits with
  respect to Q his titles over his own body and over the things used in that action.
- `gives_share` is now defined from the per-manner `shares`; `vol_transfer` unchanged in meaning.
- Theorems restated for the new arity; theorems that depend on titles against a person now carry
  the hypothesis that the title holder is not aggressing against that person.
- README rewritten as technical documentation only; the case against "co-ownership is a
  contradiction" moved to the new ARGUMENT.md.

### Added
- Definitions `full_owner_def`, `shares_def`, `transfers_manner_def` (lease), `aggresses_in_def`,
  `forfeits_def`.
- Contrast axiom `direction_exhaustive` (LiquidZulu's "just victor" premise) and theorems
  `direction_overreach`, `direction_forbids_deadlock`. Contrast axiom `control_protection_outsiders`
  and scenarios showing that each control axiom alone, and the pair with protection only against
  non-owners, are consistent with co-ownership.
- Theorems `homesteader_full_owner`, `no_title_without_acceptance`, `lease_tenant_excludes_landlord`,
  `lessor_loses_manner`, `easement_use`, `defence_is_not_aggression`, `fight_one_aggressor`.
  `joint_homesteading`, `share_gift` and `joint_purchase` now conclude full ownership.
- Scenarios `self_defence`, `fight_one_aggressor`, `fight_ada_started`, `fight_ben_started`,
  `gift_refused`, `lease`, `easement`, `owner_refuses_two_rivals` (and its direction-view
  counterpart), `co_ownership_under_direction_view`. Vampire problem `D_direction_co_ownership`.
- Story world: Ada pushes the trespasser Cy off her field (defence, not aggression); Ben and Cy
  lease the manner "sow" to Ada (t7–t8). The uniqueness check now covers aggression as well as titles.
- Axioms that follow from others (`an_object`, `persons_rivalrous`) are labelled "derived, kept for
  clarity", and the provers check that they follow.
- ARGUMENT.md (detailed case) and a shorter essay for Substack.

### Removed
- `homesteader_is_owner` (superseded by `homesteader_full_owner`); `transferee_inherits`-style
  per-claim statements are covered by `transferee_owns`.

### Verified
- 53/53 theorems proved by Vampire and by Leo-III (E back end); both derived axioms proved from
  their sources; 30/30 scenarios; story world satisfies all 38 axioms and definitions, and its
  titles and wrongs are fixed by its history; Vampire models re-checked; all theorem hypotheses
  satisfiable.

## [0.21] — Grants: share gifts and joint purchase; control analysed

### Fixed
- **Co-ownership could only start from a joint homestead (or a co-owner selling his
  share).** A sole owner could not give a share and keep his own titles, and selling to
  two persons at once was rejected as a "double spend" by `transfer_functional`. The
  defect was taking the whole-object transfer as primitive.

### Changed
- New primitive `grants(R,P,O,Q,T)`: R grants P the right to exclude Q from O and keeps
  his own titles. `grant_typing` replaces `transfer_typing`: only an owner grants, only
  over an object, only to another person.
- `acquires_def`: the second case is now a grant of a held title, or of a title against
  the granter.
- `vol_transfer` is now DEFINED: a share gift plus abandonment at the same instant
  (`vol_transfer_def`), with `gives_share_def` for the share gift.
- `voluntary_slavery_impossible` now states that nobody can grant any title over a body.
- `no_double_spend`: after a transfer, the former owner can grant nothing more.

### Removed
- `transfer_relinquishes` (now part of the definition of transfer) and
  `transfer_functional` (it forbade joint purchase).
- Theorems `transferee_owns_vs_transferor`, `transferee_inherits` (merged into
  `transferee_owns`). Scenario `double_spend_simultaneous` (replaced by `joint_purchase`).

### Added
- Theorems `grant_conveys`, `share_gift`, `transferee_owns`, `joint_purchase`.
- `controls_def` and theorems `sole_owner_controls`, `control_needs_deference`,
  `unanimity`: control is a consequence of sole ownership, and a co-owner has it only by
  the others' leave. Scenario `idleness_is_not_control` answers the "de facto owner"
  objection.
- Scenarios `share_gift`, `joint_purchase`. The story world gains t7: Ada sells the field
  to Ben and Cy jointly; MODEL.md shows who controls the field at each instant.
- README: the de facto owner objection, the four ways co-ownership starts; life-cycle
  diagram redrawn in Graphviz.

### Verified
- 45/45 theorems proved by Vampire and by Leo-III (E back end); 17/17 scenarios; story
  world satisfies all 33 axioms and definitions; Vampire models re-checked; all theorem
  hypotheses satisfiable.

## [0.20] — Exclusion made exact; fewer axioms, more theorems; models; plain-language README

### Fixed
- **Partial titles vetoed people they could not exclude.** `use_veto` fired on
  `is_owner(R,O,T)` (R may exclude *someone*), so an owner who had released his title
  against Ben could still forbid Ben. The veto is now keyed on `owns(R,O,Q,T)`.
  Regression scenario: `partial_title_no_veto`.

### Changed
- **One deontic definition.** `use_liberty`, `use_grant`, `use_veto` and `self_consent`
  are replaced by `may_use_def` (you may use O unless someone who may exclude you from O
  does not consent) and `forbidden_use_def`. `self_consent` is unnecessary because nobody
  holds a title against himself (`no_self_exclusion`).
- **Title axioms rebuilt around one defined notion.** `acquires_def` (homestead, or a
  transfer that carries the claim) + `title_acquired` (sufficient) + `title_genesis`
  (necessary) replace `homesteading`, `vol_transfer_conveys`,
  `vol_transfer_grants_vs_transferor`, `ownership_persistence` and `disown_extinguishes`.
- **`reacquires` defined away.** The unconstrained oracle is replaced by "no acquisition
  event in the window" (roadmap item 1 of v0.19).
- **Scarcity defined.** `rivalrous(O) <=> ?[M1,M2]: clash(O,M1,M2)`; `excl_o` renamed `clash`.
- Renamed: `exist_persons` → `two_persons`, `exist_np_obj` → `an_object`,
  `exist_unowned` → `unowned_exists`, `person_rivalrous` → `persons_rivalrous`,
  `rivalrous_ownable` → `nonrivalrous_unowned`, `vol_transfer_typing` → `transfer_typing`,
  `vol_transfer_disowns` → `transfer_relinquishes`, `excl_o_factual` → `clash_factual`.

### Removed
- Axioms now derived: `anti_slavery` (→ `person_unownable`), `ownership_persistence`
  (→ `title_persists`), `disown_extinguishes` (→ theorem of the same name).
- `excl`, `excl_global` (a global incompatibility would make ideas scarce),
  `excl_o_symmetric` (redundant: `clash_factual` is symmetric in its two use-events).
- `may_claim`, `may_disown`, `may_transfer` and their permission axioms: they occurred only
  positively in their own consequents, so removal is conservative.
- `nodis` (closed window), `reacquires`.
- Python re-encodings `consistency/*.py` and the hand-written `minimal/*.thf`: all
  problems are now generated from `source/theory.py`. `CONSISTENCY.md` is merged into
  `VERIFICATION.md`.

### Added
- **Aggression and action.** `aggresses_def`, `permissible_def`; theorems
  `aggression_iff_forbidden_use`, `ownership_is_not_licence` ("your fist ends where my nose
  begins"), `action_liberty`, `unowned_use_innocent`, `co_owner_trespass`,
  `refraining_innocent`, `no_self_aggression`, `bodily_integrity` (now stated as aggression).
- **Co-ownership.** `joint_homesteading` (joint first use yields mutual titles),
  `co_owner_use_by_consent`, `joint_deadlock` (restated relationally).
- **The control-view contrast.** Contrast axioms `control_use_liberty`,
  `control_protection` (not part of the theory); theorems `control_no_refusal`,
  `control_coownership_contradiction`; scenarios showing the control view is consistent
  with sole ownership and inconsistent with co-ownership.
- **Life cycle.** `transfer_is_abandonment`, `res_nullius` (uniform event hypotheses over
  the defined `acquires`), `life_cycle` (abandon → unowned → re-homestead by anyone).
- **`endless_past_paradox`.** Without a first instant, perpetual use-and-claim makes the
  title axioms contradictory (a Yablo-style regress). Documented as a limit.
- **Toolchain.** `source/tptp.py` (parser, type checker, THF/TFF emitter, Z3 grounder,
  direct evaluator); `source/build.py`, `prove.py`, `models.py`, `story.py`, `fmb.py`,
  `docs.py`; `verify.py` runs everything.
- **Models.** `MODEL.md`: a hand-written world (three persons, a field, a song, seven
  instants) evaluated against every formula; its titles are shown to be uniquely fixed
  by its history. Vampire's finite models are parsed and re-evaluated independently.
- **Non-vacuity** of every theorem hypothesis, by Vampire fmb with re-evaluation.
- **README** rewritten in controlled English with a glossary (`docs/glossary.toml`) and
  diagrams (`docs/diagrams/`); `THEORY.md` for design notes and proof sketches.

### Verified
- 40/40 theorems proved by Vampire 5.1.0 and by Leo-III 1.7.18 (E 3.5.1 back end), each
  from its declared minimal premise set; lemma graph acyclic.
- Full theory satisfiable (story world, Vampire, Z3); 15/15 scenarios as expected;
  all theorem hypotheses satisfiable. Details in `VERIFICATION.md`.

## [0.19] — Weakened abandonment + object-relative exclusion

### Added
- `no_fresh_title` (shared lemma): a claim not held at T1 cannot hold at T2
  absent acquisition events by the holder in the window. Common core of
  `abandoner_not_owner_v2` and `transferor_not_owner`, both now two-case
  assemblies (held claims: disowning + extinction; unheld: no_fresh_title).
- `excl_o(O,M1,M2)`: object-relative exclusion. Axioms: `excl_o_symmetric`;
  `excl_global` (global excl lifts into excl_o on every object);
  `excl_o_factual`, guarded by `~((P1=P2)&(M1=M2))`. excl_o is deliberately
  NOT irreflexive: `excl_o(O,M,M)` is the paradigm case of rivalry (two
  people, one field, both plowing). The guard fixes the v0.15–v0.18 defect
  (review probe P4) where `excl(M,M)` made manner M unusable even by a
  single agent, while keeping one-agent-two-incompatible-manners excluded.
- Theorems: `excl_factual_global` (guarded recovery of the old rule),
  `rival_wants_unrealised` (physical exclusion frustrates the rival's want —
  the conflict-theoretic grounding of property, now a theorem),
  `abandons_forward_v2`, `abandoner_not_owner_v2`,
  `sole_abandonment_res_nullius_v3`.

### Changed
- `abandons_def` WEAKENED: abandonment relinquishes every claim ACTUALLY
  HELD (was: a claim against every person, which made partial titles
  unabandonable — review probe P6). Safe only because `title_genesis` is in
  place; the strong definition had been quietly compensating for the
  then-missing closure axiom.
- `abandoner_not_owner` → `abandoner_not_owner_v2`, EVENT-BASED: under the
  weak definition the abandoner disowns only held claims, and may
  legitimately re-homestead the object once it falls unowned; the theorem
  therefore carries the same event hypotheses as `transferor_not_owner`.
- `sole_abandonment_res_nullius_v2` → `_v3`: event hypotheses now UNIFORM
  over all persons (abandoner included). The v2 statement (events by others
  only) is NOT a theorem under the weak definition: a partial sole owner
  could re-homestead inside the window.
- `transferor_not_owner`: statement unchanged; proof refactored through
  `no_fresh_title` (the v0.18 proof invoked genesis and L1/L2 directly).
- `excl_factual` (unguarded, global) REMOVED; superseded by the excl_o
  machinery, from which the guarded global rule is derivable.

### Verified
- Full v0.19 axiom set: sat (|E|=4,|T|=4,|M|=2).
- Scenarios 20/20, with review probes P6 and P4 as regression tests:
  partial-title abandonment sat with `abandons` and res nullius FORCED
  (strong def: unsat); lone-agent use under `excl_o(O,M,M)` sat (old rule:
  unsat); two rival agents same manner unsat; one agent two incompatible
  manners unsat; rival-want conclusion forced. All v0.17/v0.18 checks
  re-pass.
- Z3 entailment (uninterpreted sorts): 17/17 PROVED.
- Leo-III re-run of the full minimal suite: PENDING (see VERIFICATION.md).

## [0.18] — Temporalised conveyance (transfer overhaul)

### Added
- `vol_transfer_conveys`: the transferee gains, at strictly later times,
  exactly the claims the transferor held at the transfer instant, each
  undisowned since (`nodis_upto`). Replaces `vol_transfer_grants`
  (instantaneous, universal).
- `vol_transfer_grants_vs_transferor`: the transferee additionally gains a
  claim against the transferor himself — the one claim conveyance cannot
  produce (the transferor held no claim against himself).
- `transfer_functional`: one transferee per transferor-object-instant.
- Theorems: `nemo_dat_v2` (SUBSTANTIVE: a claim the transferor lacked never
  reaches the transferee — from `title_genesis` alone), `transferee_is_owner`
  (sanity), `transferor_not_owner` (event-based sibling of
  `abandoner_not_owner`; a transferor who neither reacquires nor freshly
  acquires is not an owner later), `no_double_spend` (assembly: sequential
  re-transfer violates typing).

### Changed
- `title_genesis` transfer clause: now strictly-before and PER-CLAIM — the
  ground must have CARRIED the claim (`owns(P1,O,Q,T1) | Q=P1`). Effects:
  (i) the v0.17 circular-grounding residual (same-instant mutual transfers
  grounding each other) is dissolved; (ii) nemo dat becomes provable;
  (iii) remaining caveat: over a NON-WELL-FOUNDED time order an infinite
  regress of transfers could self-ground — finite models are immune, and any
  well-founded timeline forces chains to bottom out in homesteading.
- `res_nullius_lemma2` re-stated for the new semantics (per-claim ground) and
  its proof SIMPLIFIED: the temporalised grants make the v0.17 detour through
  `ownership_persistence` unnecessary. `res_nullius_lemma3` re-proved under
  the new genesis. The headline `sole_abandonment_res_nullius_v2` statement
  is unchanged and re-verified.
- Old `nemo_dat` retained, relabelled a typing projection (sanity).

### Semantic notes
- At the transfer instant T the transferor still owns and disowns; the
  transferee's title begins at every strictly later time. In dense time there
  is no gap: no instant at which the object is unowned in between (the
  conveyance fires at all T2 > T while `nodis_upto` holds).
- Partial titles now propagate honestly: a co-owner or partial owner conveys
  only their actual claims; the other co-owner's position is untouched.

### Verified
- Full v0.18 axiom set: sat (|E|=4,|T|=4,|M|=2).
- Scenarios (all pass, key conclusions FORCED): transfer life-cycle
  (transferee's title forced; transferor's extinction forced); simultaneous
  double-spend unsat; sequential double-spend unsat; nemo-dat scenario —
  transferee holding the claim the transferor lacked is unsat. All v0.17
  regressions re-pass (abandonment life-cycle, ex nihilo, inert non-rivalrous
  claiming, grounded co-ownership with mutual titles).
- Z3 entailment (uninterpreted sorts): 13/13 PROVED — five regressions, L1,
  L2 (new statement), L3 (new genesis), the headline assembly,
  transferee_is_owner, nemo_dat_v2, transferor_not_owner, no_double_spend.
- Leo-III re-run of the full minimal suite: PENDING (see VERIFICATION.md).

## [0.17] — Title genesis + guarded homesteading

### Added
- `title_genesis` (closure axiom): `owns(P,O,Q,T2)` for an object holds only
  if grounded in a homesteading event strictly before T2, or a voluntary
  transfer at-or-before T2, with no disowning of the P-vs-Q claim on the
  half-open interval up to T2. Self-ownership exempt (`np_obj` guard).
  Ownership ex nihilo — previously satisfiable — is now unsat.
- `nodis_upto(P,O,Q,T1,T2)`: no disowning on the HALF-OPEN interval [T1,T2).
  Right-openness is essential: disowning at T requires owning at T
  (`disowns_typing`), so guards reaching to T2 itself would make disowning —
  hence abandonment and transfer — impossible under the closure.
- Lemma chain for the headline: `res_nullius_lemma1` (pre-window homestead
  ground → title at T1), `res_nullius_lemma2` (pre-window transfer ground →
  title at T1), `res_nullius_lemma3` (no third-party title at T2).
- `sole_abandonment_res_nullius_v2`: res nullius from soleness + abandonment +
  no reacquisition + NO ACQUISITION EVENTS by others (no homesteading in
  [T1,T2), no transfers in [T1,T2]). Supersedes the v0.16 statement, whose
  hypothesis "no third party owns at T2" assumed the hard part.

### Changed
- `homesteading` guarded by `rivalrous(O)` and `nodis_upto(P,O,Q,T1,T2)`.
  Fixes two defects: (i) using-and-claiming a non-rivalrous object was
  *logically impossible* at non-final times (collision with
  `rivalrous_ownable`); it is now possible and juridically inert — no title
  arises, others' use stays permitted, matching the anti-IP position;
  (ii) homesteaded titles were UNRELINQUISHABLE — the unguarded axiom granted
  title at every later time unconditionally, contradicting
  `disown_extinguishes` unless the unconstrained `reacquires` oracle fired.
- Statements of the homestead family updated accordingly:
  `homesteader_owns_v2`, `homesteader_is_owner_v2`, `homesteader_may_use_v2`,
  `persistence_from_homestead`, `first_homesteader_exclusive_v2`.
- Co-ownership is deliberately preserved: mutual titles
  (`owns(P,O,Q,T) & owns(Q,O,P,T)`) remain expressible — they ARE
  co-ownership in the relational semantics (reciprocal veto) — but must now
  be grounded (joint homesteading witnessed sat in `scenarios_v017.py`).

### Consistency / verification infrastructure
- `consistency/` rewritten: `v017_axioms.py` is a plain importable module
  (the exec-based chained import is gone); domain enlarged to |E|=4, |T|=4
  (the old 3/3 domain could not witness partial titles or rival transfers).
- New `prove_v017.py`: genuine entailment proofs over UNINTERPRETED sorts
  (Z3/MBQI), from the same minimal axiom subsets as the Leo-III files.
  Note in-file: nested quantifier helpers must use globally fresh bound
  variables — a name-reuse capture bug initially trivialised several
  definitions and was caught by a false countermodel.

### Verified
- Full v0.17 axiom set: sat (|E|=4,|T|=4,|M|=2).
- Life-cycle witness homestead(t0) → title(t1) → abandon(t1) → unowned(t2):
  sat — this exact scenario was UNSAT in v0.16 (unabandonability bug) — and
  the res-nullius conclusion is FORCED at this domain size (denial unsat).
- Z3 entailment (uninterpreted sorts): homesteader_owns_v2,
  persistence_from_homestead, abandoner_not_owner, theft_forbidden,
  non_rivalrous_use_permitted, res_nullius_lemma1/2/3,
  sole_abandonment_res_nullius_v2 — all PROVED.
- Leo-III re-run of the full minimal suite: PENDING (see VERIFICATION.md).

## [0.16] — Abandonment → res nullius (roadmap item 2)

### Added
- `abandons(P,O,T)` predicate and `abandons_def`; theorems `abandons_forward`,
  `abandoner_not_owner`, `sole_abandonment_res_nullius` (superseded in v0.17).

### Post-release defects found (fixed in v0.17)
- Homesteaded titles unrelinquishable; ownership ex nihilo satisfiable;
  use+claim of non-rivalrous objects impossible; headline theorem's
  third-party hypothesis assumed the hard part.
