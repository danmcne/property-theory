# Roadmap

## v0.23 — done
- Veto co-ownership versus free-use co-ownership: `veto_settles_conflict`, `free_use_unsettled`.

## v0.22 — done

### Theory
1. **Titles per manner.** `owns(P,O,Q,M,T)`: P may exclude Q from using O in manner M at T.
   Grants, releases and consent become per manner. Homesteading still yields titles in every manner.
2. **Acceptance.** A grant takes effect only if the grantee accepts it at the same instant.
   Theorem: apart from homesteading, nobody acquires a title without accepting it.
3. **Protection of property.** While P aggresses against Q, P forfeits, with respect to Q, his
   titles over his own body and over the things used in the aggressing action. Q may then use them
   without that counting as aggression. No proportionality (listed as a limit). Theorem: in a fight in
   which each uses only the other's body, exactly one is the aggressor.
4. **Named patterns.** Full ownership (titles against every other person in every manner);
   co-ownership (two or more full owners); lease (transfer of the titles for some manners);
   easement (release of the title against one person for one manner).
5. **LiquidZulu's argument formalized.** His premise that every conflict has a "just victor" is a
   contrast axiom. Theorems: with it, an owner can never refuse two rivals (the premise overreaches),
   and co-owners can never deadlock (the premise assumes what it should prove). Without it, both
   situations have models.
6. **Housekeeping.** Axioms derivable from others are labelled "derived, kept for clarity". Limits
   listed: fraud, threats, agency, proportionality, contract, products, endless past.

### Documents (kept separate)
7. **Technical documentation** (README, THEORY, MODEL, VERIFICATION) in controlled English: axioms,
   theorems, proofs and models, with no advocacy.
8. **ARGUMENT.md** (repository, detailed): the case that co-ownership is consistent and that the
   "contradiction" depends on defining ownership as direction or control. Cites LiquidZulu and Kinsella.
9. **Substack essay** (short version of 8).

## Later
- **Products and fruits.** New objects made from owned inputs (a crop from owned seed on co-owned land).
- **Consent over time and contract.** Lease reversion, decision rules agreed among co-owners, exchange.
- **Defence by agents; threats; fraud.**
- **Parts and partition.** Objects with parts; partition in space and in time (time-share).
- **Proof assistant.** Isabelle: re-check the existing proofs in a small trusted kernel. Lean or
  Isabelle: meta-theorems (titles fixed by a well-founded history; compossibility).

## Done
- v0.21: grants as the unit of alienation (share gifts, joint purchase); control analysed.
- v0.20: relational veto fixed; persistence and extinction derived; aggression; control-view contrast;
  life cycle; single source of truth; Vampire + Leo-III; models and non-vacuity.
