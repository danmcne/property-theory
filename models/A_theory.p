tff(tm_type, type, tm: $tType).
tff(en_type, type, en: $tType).
tff(man_type, type, man: $tType).
tff(abandons_decl, type, abandons: (en * en * tm) > $o).
tff(accepts_decl, type, accepts: (en * en * en * tm) > $o).
tff(acquires_decl, type, acquires: (en * en * en * man * tm) > $o).
tff(aggresses_decl, type, aggresses: (en * en * tm) > $o).
tff(aggresses_in_decl, type, aggresses_in: (en * en * man * tm) > $o).
tff(before_decl, type, before: (tm * tm) > $o).
tff(claim_decl, type, claim: (en * en * tm) > $o).
tff(clash_decl, type, clash: (en * man * man) > $o).
tff(consents_decl, type, consents: (en * en * en * man * tm) > $o).
tff(controls_decl, type, controls: (en * en * tm) > $o).
tff(disowns_decl, type, disowns: (en * en * en * man * tm) > $o).
tff(forbidden_use_decl, type, forbidden_use: (en * en * man * tm) > $o).
tff(forfeits_decl, type, forfeits: (en * en * en * tm) > $o).
tff(full_owner_decl, type, full_owner: (en * en * tm) > $o).
tff(gives_share_decl, type, gives_share: (en * en * en * tm) > $o).
tff(grants_decl, type, grants: (en * en * en * en * man * tm) > $o).
tff(is_owner_decl, type, is_owner: (en * en * tm) > $o).
tff(may_use_decl, type, may_use: (en * en * man * tm) > $o).
tff(nodis_upto_decl, type, nodis_upto: (en * en * en * man * tm * tm) > $o).
tff(np_obj_decl, type, np_obj: en > $o).
tff(owns_decl, type, owns: (en * en * en * man * tm) > $o).
tff(permissible_decl, type, permissible: (en * man * tm) > $o).
tff(person_decl, type, person: en > $o).
tff(rivalrous_decl, type, rivalrous: en > $o).
tff(shares_decl, type, shares: (en * en * en * man * tm) > $o).
tff(transfers_manner_decl, type, transfers_manner: (en * en * en * man * tm) > $o).
tff(unowned_decl, type, unowned: (en * tm) > $o).
tff(unrealised_decl, type, unrealised: (en * en * man * tm) > $o).
tff(use_decl, type, use: (en * en * man * tm) > $o).
tff(vol_transfer_decl, type, vol_transfer: (en * en * en * tm) > $o).
tff(wants_decl, type, wants: (en * en * man * tm) > $o).
tff(time_irreflexive, axiom,
    ![T:tm]: ~ before(T,T)).
tff(time_transitive, axiom,
    ![A:tm,B:tm,C:tm]: ((before(A,B) & before(B,C)) => before(A,C))).
tff(time_total, axiom,
    ![A:tm,B:tm]: (before(A,B) | before(B,A) | (A = B))).
tff(time_nonempty, axiom,
    ?[A:tm,B:tm]: before(A,B)).
tff(entity_disjoint, axiom,
    ![X:en]: ~ (person(X) & np_obj(X))).
tff(two_persons, axiom,
    ?[P1:en,P2:en]: (person(P1) & person(P2) & (P1 != P2))).
tff(an_object, axiom,
    ?[O:en]: np_obj(O)).
tff(persons_rivalrous, axiom,
    ![P:en]: (person(P) => rivalrous(P))).
tff(use_typing, axiom,
    ![P:en,O:en,M:man,T:tm]: (use(P,O,M,T) => (person(P) & (np_obj(O) | person(O))))).
tff(claim_typing, axiom,
    ![P:en,O:en,T:tm]: (claim(P,O,T) => (person(P) & np_obj(O)))).
tff(owns_typing, axiom,
    ![P:en,O:en,Q:en,M:man,T:tm]: (owns(P,O,Q,M,T) => (person(P) & person(Q) & (P != Q) & (np_obj(O) | (O = P))))).
tff(disowns_typing, axiom,
    ![P:en,O:en,Q:en,M:man,T:tm]: (disowns(P,O,Q,M,T) => (owns(P,O,Q,M,T) & np_obj(O)))).
tff(grant_typing, axiom,
    ![R:en,P:en,O:en,Q:en,M:man,T:tm]: (grants(R,P,O,Q,M,T) => (is_owner(R,O,T) & np_obj(O) & person(P) & (R != P)))).
tff(self_ownership, axiom,
    ![P:en,Q:en,M:man,T:tm]: ((person(P) & person(Q) & (P != Q)) => owns(P,P,Q,M,T))).
tff(nodis_upto_def, axiom,
    ![P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: (nodis_upto(P,O,Q,M,T1,T2) <=> ![T:tm]: ((((T = T1) | before(T1,T)) & before(T,T2)) => ~ disowns(P,O,Q,M,T)))).
tff(acquires_def, axiom,
    ![P:en,O:en,Q:en,M:man,T:tm]: (acquires(P,O,Q,M,T) <=> (?[M2:man]: (rivalrous(O) & use(P,O,M2,T) & claim(P,O,T) & unowned(O,T)) | ?[R:en]: (grants(R,P,O,Q,M,T) & accepts(P,R,O,T) & (owns(R,O,Q,M,T) | (Q = R)))))).
tff(title_acquired, axiom,
    ![P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((acquires(P,O,Q,M,T1) & person(Q) & (P != Q) & before(T1,T2) & nodis_upto(P,O,Q,M,T1,T2)) => owns(P,O,Q,M,T2))).
tff(title_genesis, axiom,
    ![P:en,O:en,Q:en,M:man,T2:tm]: ((owns(P,O,Q,M,T2) & np_obj(O)) => ?[T1:tm]: (before(T1,T2) & acquires(P,O,Q,M,T1) & nodis_upto(P,O,Q,M,T1,T2)))).
tff(is_owner_def, axiom,
    ![P:en,O:en,T:tm]: (is_owner(P,O,T) <=> ?[Q:en,M:man]: owns(P,O,Q,M,T))).
tff(full_owner_def, axiom,
    ![P:en,O:en,T:tm]: (full_owner(P,O,T) <=> ![Q:en,M:man]: ((person(Q) & (Q != P)) => owns(P,O,Q,M,T)))).
tff(unowned_def, axiom,
    ![O:en,T:tm]: (unowned(O,T) <=> ![P:en]: ~ is_owner(P,O,T))).
tff(shares_def, axiom,
    ![R:en,P:en,O:en,M:man,T:tm]: (shares(R,P,O,M,T) <=> (grants(R,P,O,R,M,T) & ![Q:en]: ((owns(R,O,Q,M,T) & (Q != P)) => grants(R,P,O,Q,M,T))))).
tff(gives_share_def, axiom,
    ![R:en,P:en,O:en,T:tm]: (gives_share(R,P,O,T) <=> ![M:man]: shares(R,P,O,M,T))).
tff(transfers_manner_def, axiom,
    ![R:en,P:en,O:en,M:man,T:tm]: (transfers_manner(R,P,O,M,T) <=> (shares(R,P,O,M,T) & ![Q:en]: (owns(R,O,Q,M,T) => disowns(R,O,Q,M,T))))).
tff(vol_transfer_def, axiom,
    ![R:en,P:en,O:en,T:tm]: (vol_transfer(R,P,O,T) <=> (gives_share(R,P,O,T) & abandons(R,O,T)))).
tff(abandons_def, axiom,
    ![P:en,O:en,T:tm]: (abandons(P,O,T) <=> (np_obj(O) & is_owner(P,O,T) & ![Q:en,M:man]: (owns(P,O,Q,M,T) => disowns(P,O,Q,M,T))))).
tff(may_use_def, axiom,
    ![Q:en,O:en,M:man,T:tm]: (may_use(Q,O,M,T) <=> ![R:en]: ((owns(R,O,Q,M,T) & ~ forfeits(R,O,Q,T)) => consents(R,O,Q,M,T)))).
tff(forbidden_use_def, axiom,
    ![Q:en,O:en,M:man,T:tm]: (forbidden_use(Q,O,M,T) <=> ~ may_use(Q,O,M,T))).
tff(aggresses_in_def, axiom,
    ![P:en,Q:en,M:man,T:tm]: (aggresses_in(P,Q,M,T) <=> ?[O:en]: (use(P,O,M,T) & owns(Q,O,P,M,T) & ~ forfeits(Q,O,P,T) & ~ consents(Q,O,P,M,T)))).
tff(aggresses_def, axiom,
    ![P:en,Q:en,T:tm]: (aggresses(P,Q,T) <=> ?[M:man]: aggresses_in(P,Q,M,T))).
tff(forfeits_def, axiom,
    ![R:en,O:en,Q:en,T:tm]: (forfeits(R,O,Q,T) <=> ?[M:man]: (aggresses_in(R,Q,M,T) & ((O = R) | use(R,O,M,T))))).
tff(permissible_def, axiom,
    ![P:en,M:man,T:tm]: (permissible(P,M,T) <=> ![O:en]: (use(P,O,M,T) => may_use(P,O,M,T)))).
tff(controls_def, axiom,
    ![P:en,O:en,T:tm]: (controls(P,O,T) <=> (![M:man]: may_use(P,O,M,T) & ![Q:en,M:man]: ((person(Q) & (Q != P)) => (may_use(Q,O,M,T) <=> consents(P,O,Q,M,T)))))).
tff(rivalrous_def, axiom,
    ![O:en]: (rivalrous(O) <=> ?[M1:man,M2:man]: clash(O,M1,M2))).
tff(clash_factual, axiom,
    ![O:en,P1:en,P2:en,M1:man,M2:man,T:tm]: ((clash(O,M1,M2) & ~ ((P1 = P2) & (M1 = M2))) => ~ (use(P1,O,M1,T) & use(P2,O,M2,T)))).
tff(nonrivalrous_unowned, axiom,
    ![O:en,T:tm]: (~ rivalrous(O) => unowned(O,T))).
tff(unowned_exists, axiom,
    ?[O:en,T:tm]: (np_obj(O) & unowned(O,T))).
tff(unrealised_def, axiom,
    ![P:en,O:en,M:man,T:tm]: (unrealised(P,O,M,T) <=> (wants(P,O,M,T) & ~ use(P,O,M,T)))).
