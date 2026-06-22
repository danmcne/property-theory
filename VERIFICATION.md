# Verification — v0.16

Prover: Leo-III v1.7.18 (`java -jar leo3.jar FILE -t 70`). **28/28 theorems**
return SZS status Theorem. Each `minimal/*.thf` is self-contained.

**All axioms are model-checked.** The full axiom set (including the new
`abandons_def`) has a finite Z3 model — see CONSISTENCY.md. Every theorem's
antecedent is also checked satisfiable, so no theorem is vacuously true.

## New in v0.16 (abandonment → res nullius)
| Theorem | Statement |
|---|---|
| abandons_forward | `abandons` entails disowning against every other party |
| abandoner_not_owner | after abandoning (no re-acquisition), the abandoner holds no title |
| sole_abandonment_res_nullius | a sole owner's abandonment leaves the object unowned, absent re-acquisition |

## Carried from v0.15 (re-verified)
person_unownable, self_is_owner, body_sole_owner, sole_owner_grant, self_use,
unowned_use, theft_forbidden, bodily_integrity, selective_consent,
joint_deadlock, compatible_manner_permitted, homesteader_is_owner_v2,
homesteader_owns_v2, homesteader_may_use_v2, owns_not_unowned,
persistence_from_homestead, first_homesteader_exclusive_v2, nemo_dat,
transfer_exclusive, share_transfer_unconditional, person_protection_prereqs,
voluntary_slavery_impossible, theft_retains_ownership, may_use_or_forbidden,
non_rivalrous_use_permitted.

## Model checks (Z3 4.16.0, `consistency/`)
| Check | Result |
|---|---|
| full v0.16 axiom set has a finite model | sat |
| sole owner abandons → object unowned at next time | sat; witness has `abandons`=T, `is_owner`=F, `unowned`=T |
| abandoner_not_owner antecedent satisfiable (non-vacuous) | sat |
