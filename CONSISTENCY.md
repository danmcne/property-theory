# Consistency / model finding — v0.16

`consistency/` (needs `pip install z3-solver`), each script commented:
- `model_find_v016.py` — imports the v0.15 axioms and appends `abandons_def`;
  the full set → **sat** (|Entity|=3,|Time|=3,|Manner|=2).
- `scenarios_v016.py` — res-nullius witness + non-vacuity checks.

**Methodology.** Every axiom introduction or change is gated by a model check:
adding `abandons_def` (the only new axiom in v0.16), we re-ran the full-set
satisfiability check (sat) before accepting it. For each theorem we also assert
its antecedent against the full axiom set and confirm sat, ruling out vacuous
proofs. This pairs with Leo-III: Leo shows the axioms *entail* the theorems;
Z3 shows the axioms are *consistent* and the theorems are *non-vacuous*.

## The abandonment bridge

`disowns(P,O,Q,T)` is relational — it relinquishes one P-vs-Q claim.
`unowned(O,T)` is global — no one owns O against anyone. v0.16 bridges them:

    abandons(P,O,T)  <=>  np_obj(O) & is_owner(P,O,T) &
                          ∀Q( person(Q) & Q≠P  ⇒  disowns(P,O,Q,T) )

i.e. abandonment is relinquishing against *every* other party. Then:
- `abandoner_not_owner`: disowning against all parties (no re-acquisition)
  extinguishes the abandoner's title entirely.
- `sole_abandonment_res_nullius`: if the abandoner was the sole owner and no one
  re-acquires in the interval, the object is unowned at the later time — res
  nullius. (The "no re-acquisition" proviso is exactly the room left for a fresh
  homesteading of the now-ownerless thing; it is not a gap in the result.)

Witnessed in `scenarios_v016.py`: a model where p1 abandons obj1 and obj1 is
unowned at the next instant.
