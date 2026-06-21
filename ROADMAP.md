# Roadmap

Planned extensions, roughly in priority order. Conjecture stubs live in
Section 16 of the main file.

## Near term

1. **Consistency witness.** Run Nitpick or Paradox on the joint-ownership
   scenario (and the full axiom set) to obtain a positive finite model. Leo-III
   establishes entailments, not satisfiability; "no `$false` in 70 s" is evidence,
   not proof. This is the most important open item.
2. **Abandonment -> res nullius (B5).** With `disown_extinguishes` in place,
   prove that an abandoned resource returns to `unowned` and is open to
   re-homesteading, given no other owner acquires in the interval.
3. **Non-rivalrous use permitted (IP).** Prove `~rivalrous(O) => per(use(Q,O,M,T))`
   for a non-owner Q, via `liberty` plus the fact that the (rivalrous-guarded)
   NAP is the only source of `fbd`. Makes the "creation of a non-rivalrous
   pattern confers no title / no trespass" result explicit rather than implicit.

## Medium term

4. **Object-relative exclusivity.** Replace `excl(M1,M2)` with `excl_o(O,M1,M2)`
   so a manner-pair can be exclusive on one object and not another (e.g.
   *looking at* vs *plowing* the same field, where only some pairs conflict).
   Re-derive the joint-ownership theorems under the indexed relation.
5. **Strong NAP / ownership as sole basis of prohibition.** Prove
   `fbd(use(Q,O,M,T)) => exists P: owns(P,O,Q,T) & ~allows & ~is_owner(Q,O,T)` —
   that unauthorized use of owned rivalrous property is the *only* ground of
   prohibition (no paternalism, no third-party-harm prohibitions).
6. **Permission sublicensing.** `sub_allows(Q,O,R,T)` with typing requiring an
   upstream `allows(P,O,Q,T)`, and a normative axiom permitting R's use.

## Longer term / architectural

7. **Exclusion-primitive refactor.** Take a primitive `right_to_exclude` (or the
   set-valued exclusion relation) and *define* `owns` over it, deriving the NAP
   as a consequence rather than the route by which exclusion enters. Aligns the
   formal theory with the exclusion-as-relation, set-valued ownership treatment.
8. **Kripke / intensional deontics.** Move `ob`/`per`/`fbd` from `$o > $o` to
   `(world > $o) > world > $o` with an accessibility relation, removing the
   Boolean-extensionality caveat. Needed before any nested-deontic extension.
9. **Service contracts.** Model revocable, time-limited labor agreements
   (distinct from the impossible alienation of the self that
   `voluntary_slavery_impossible` rules out).
