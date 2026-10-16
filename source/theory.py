"""Libertarian Property Theory, v0.22 — the single source of truth.

Every TPTP file, every Z3 check and every table in the documentation is
generated from the declarations below. Formulas use the TPTP syntax shared
by FOF, TFF and THF (see tptp.py).

Reading guide
  owns(P,O,Q,M,T)      P holds a title against Q over O in manner M at T:
                       P may exclude Q from using O in manner M. Full
                       ownership is the pattern "a title against every other
                       person in every manner" (full_owner).
  use(P,O,M,T)         P uses O in manner M at T. An action is the triple
                       (P,M,T); one action can use several things.
  clash(O,M1,M2)       on O, a use in manner M1 and a different use in
                       manner M2 cannot happen at the same instant.
  consents(R,O,Q,M,T)  R consents to Q using O in manner M at T.
  grants(R,P,O,Q,M,T)  R grants P a title against Q over O in manner M at T;
                       R keeps his own titles.
  accepts(P,R,O,T)     P accepts the grants that R makes to P over O at T.
  disowns(P,O,Q,M,T)   P releases his title against Q over O in manner M.
"""

SORTS = ['tm', 'en', 'man']

SIG = {
    # primitive
    'before': ('tm', 'tm'),
    'person': ('en',),
    'np_obj': ('en',),
    'use': ('en', 'en', 'man', 'tm'),
    'claim': ('en', 'en', 'tm'),
    'clash': ('en', 'man', 'man'),
    'wants': ('en', 'en', 'man', 'tm'),
    'consents': ('en', 'en', 'en', 'man', 'tm'),
    'owns': ('en', 'en', 'en', 'man', 'tm'),
    'disowns': ('en', 'en', 'en', 'man', 'tm'),
    'grants': ('en', 'en', 'en', 'en', 'man', 'tm'),
    'accepts': ('en', 'en', 'en', 'tm'),
    # defined
    'rivalrous': ('en',),
    'is_owner': ('en', 'en', 'tm'),
    'full_owner': ('en', 'en', 'tm'),
    'unowned': ('en', 'tm'),
    'nodis_upto': ('en', 'en', 'en', 'man', 'tm', 'tm'),
    'acquires': ('en', 'en', 'en', 'man', 'tm'),
    'abandons': ('en', 'en', 'tm'),
    'shares': ('en', 'en', 'en', 'man', 'tm'),
    'gives_share': ('en', 'en', 'en', 'tm'),
    'transfers_manner': ('en', 'en', 'en', 'man', 'tm'),
    'vol_transfer': ('en', 'en', 'en', 'tm'),
    'may_use': ('en', 'en', 'man', 'tm'),
    'forbidden_use': ('en', 'en', 'man', 'tm'),
    'aggresses_in': ('en', 'en', 'man', 'tm'),
    'aggresses': ('en', 'en', 'tm'),
    'forfeits': ('en', 'en', 'en', 'tm'),
    'permissible': ('en', 'man', 'tm'),
    'controls': ('en', 'en', 'tm'),
    'unrealised': ('en', 'en', 'man', 'tm'),
}


def _win(t='T', a='T1', b='T2'):
    """The window [a,b) written out: (t = a or a < t) and t < b."""
    return "(((%s = %s) | before(%s,%s)) & before(%s,%s))" % (t, a, a, t, t, b)


# ---------------------------------------------------------------------------
# AXIOMS AND DEFINITIONS
# kind: 'axiom' (a substantive claim) or 'definition' (introduces a name)
# derived: names of axioms/definitions from which this axiom follows (it is
#          kept because it states something a reader expects to see stated)
# ---------------------------------------------------------------------------
A = []


def ax(name, group, kind, text, gloss, derived=None):
    A.append(dict(name=name, group=group, kind=kind, text=text, gloss=gloss, derived=derived))


# --- time -------------------------------------------------------------------
ax('time_irreflexive', 'time', 'axiom',
   "![T:tm]: ~ before(T,T)",
   "No instant is before itself.")
ax('time_transitive', 'time', 'axiom',
   "![A:tm,B:tm,C:tm]: ((before(A,B) & before(B,C)) => before(A,C))",
   "If A is before B and B is before C, then A is before C.")
ax('time_total', 'time', 'axiom',
   "![A:tm,B:tm]: (before(A,B) | before(B,A) | (A = B))",
   "Any two instants are equal or one is before the other.")
ax('time_nonempty', 'time', 'axiom',
   "?[A:tm,B:tm]: before(A,B)",
   "There are at least two instants.")

# --- entities ---------------------------------------------------------------
ax('entity_disjoint', 'entities', 'axiom',
   "![X:en]: ~ (person(X) & np_obj(X))",
   "Nothing is both a person and an object.")
ax('two_persons', 'entities', 'axiom',
   "?[P1:en,P2:en]: (person(P1) & person(P2) & (P1 != P2))",
   "There are at least two persons.")
ax('an_object', 'entities', 'axiom',
   "?[O:en]: np_obj(O)",
   "There is at least one object.",
   derived=['unowned_exists'])
ax('persons_rivalrous', 'entities', 'axiom',
   "![P:en]: (person(P) => rivalrous(P))",
   "Every body is scarce: some two uses of it clash.",
   derived=['self_ownership', 'nonrivalrous_unowned', 'two_persons', 'is_owner_def', 'unowned_def'])

# --- typing -----------------------------------------------------------------
ax('use_typing', 'typing', 'axiom',
   "![P:en,O:en,M:man,T:tm]: (use(P,O,M,T) => (person(P) & (np_obj(O) | person(O))))",
   "Only persons use things; what they use is an object or a body.")
ax('claim_typing', 'typing', 'axiom',
   "![P:en,O:en,T:tm]: (claim(P,O,T) => (person(P) & np_obj(O)))",
   "Only persons claim, and only objects are claimed.")
ax('owns_typing', 'typing', 'axiom',
   "![P:en,O:en,Q:en,M:man,T:tm]: (owns(P,O,Q,M,T) => "
   "(person(P) & person(Q) & (P != Q) & (np_obj(O) | (O = P))))",
   "A title is held by a person against another person, over an object or the holder's own body.")
ax('disowns_typing', 'typing', 'axiom',
   "![P:en,O:en,Q:en,M:man,T:tm]: (disowns(P,O,Q,M,T) => (owns(P,O,Q,M,T) & np_obj(O)))",
   "Only a title that is actually held over an object can be released.")
ax('grant_typing', 'typing', 'axiom',
   "![R:en,P:en,O:en,Q:en,M:man,T:tm]: (grants(R,P,O,Q,M,T) => "
   "(is_owner(R,O,T) & np_obj(O) & person(P) & (R != P)))",
   "Only an owner grants, only titles over an object, and only to another person.")

# --- self-ownership ---------------------------------------------------------
ax('self_ownership', 'persons', 'axiom',
   "![P:en,Q:en,M:man,T:tm]: ((person(P) & person(Q) & (P != Q)) => owns(P,P,Q,M,T))",
   "Every person holds a title over his or her body against every other person, in every manner, at every instant.")

# --- titles: how they start, and that they start no other way ---------------
ax('nodis_upto_def', 'title', 'definition',
   "![P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: (nodis_upto(P,O,Q,M,T1,T2) <=> "
   "![T:tm]: (%s => ~ disowns(P,O,Q,M,T)))" % _win(),
   "The title of P against Q over O in manner M is not released in the window [T1,T2).")
ax('acquires_def', 'title', 'definition',
   "![P:en,O:en,Q:en,M:man,T:tm]: (acquires(P,O,Q,M,T) <=> "
   "((?[M2:man]: (rivalrous(O) & use(P,O,M2,T) & claim(P,O,T) & unowned(O,T))) | "
   "(?[R:en]: (grants(R,P,O,Q,M,T) & accepts(P,R,O,T) & (owns(R,O,Q,M,T) | (Q = R))))))",
   "An acquisition event for a title: P homesteads O (uses and claims it while it is scarce and unowned), "
   "or P accepts a grant of the title from someone who holds it, or from Q himself.")
ax('title_acquired', 'title', 'axiom',
   "![P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((acquires(P,O,Q,M,T1) & person(Q) & (P != Q) & before(T1,T2) "
   "& nodis_upto(P,O,Q,M,T1,T2)) => owns(P,O,Q,M,T2))",
   "After an acquisition event, the title holds at every later instant until it is released.")
ax('title_genesis', 'title', 'axiom',
   "![P:en,O:en,Q:en,M:man,T2:tm]: ((owns(P,O,Q,M,T2) & np_obj(O)) => "
   "?[T1:tm]: (before(T1,T2) & acquires(P,O,Q,M,T1) & nodis_upto(P,O,Q,M,T1,T2)))",
   "A title over an object holds only because of an earlier acquisition event that was not released since.")

# --- owners -----------------------------------------------------------------
ax('is_owner_def', 'ownership', 'definition',
   "![P:en,O:en,T:tm]: (is_owner(P,O,T) <=> (?[Q:en,M:man]: owns(P,O,Q,M,T)))",
   "A holder of rights over O is someone who holds at least one title over O.")
ax('full_owner_def', 'ownership', 'definition',
   "![P:en,O:en,T:tm]: (full_owner(P,O,T) <=> "
   "(![Q:en,M:man]: ((person(Q) & (Q != P)) => owns(P,O,Q,M,T))))",
   "A full owner of O holds a title against every other person in every manner.")
ax('unowned_def', 'ownership', 'definition',
   "![O:en,T:tm]: (unowned(O,T) <=> (![P:en]: ~ is_owner(P,O,T)))",
   "O is unowned when nobody holds any title over it.")

# --- gifts, transfers, leases (defined from grants) ---------------------------
ax('shares_def', 'transfer', 'definition',
   "![R:en,P:en,O:en,M:man,T:tm]: (shares(R,P,O,M,T) <=> (grants(R,P,O,R,M,T) & "
   "(![Q:en]: ((owns(R,O,Q,M,T) & (Q != P)) => grants(R,P,O,Q,M,T)))))",
   "R shares manner M of O with P: R grants P every title in M that R holds, and a title in M against R himself.")
ax('gives_share_def', 'transfer', 'definition',
   "![R:en,P:en,O:en,T:tm]: (gives_share(R,P,O,T) <=> (![M:man]: shares(R,P,O,M,T)))",
   "A share gift: R shares every manner of O with P. R keeps his own titles.")
ax('transfers_manner_def', 'transfer', 'definition',
   "![R:en,P:en,O:en,M:man,T:tm]: (transfers_manner(R,P,O,M,T) <=> (shares(R,P,O,M,T) & "
   "(![Q:en]: (owns(R,O,Q,M,T) => disowns(R,O,Q,M,T)))))",
   "R transfers manner M of O to P: R shares manner M with P and releases all his titles in M. "
   "A lease is such a transfer for the leased manners.")
ax('vol_transfer_def', 'transfer', 'definition',
   "![R:en,P:en,O:en,T:tm]: (vol_transfer(R,P,O,T) <=> (gives_share(R,P,O,T) & abandons(R,O,T)))",
   "A transfer: a share gift and an abandonment at the same instant.")
ax('abandons_def', 'abandonment', 'definition',
   "![P:en,O:en,T:tm]: (abandons(P,O,T) <=> (np_obj(O) & is_owner(P,O,T) & "
   "(![Q:en,M:man]: (owns(P,O,Q,M,T) => disowns(P,O,Q,M,T)))))",
   "To abandon is to release every title one holds over an object.")

# --- use, aggression and defence ------------------------------------------------
ax('may_use_def', 'use', 'definition',
   "![Q:en,O:en,M:man,T:tm]: (may_use(Q,O,M,T) <=> "
   "(![R:en]: ((owns(R,O,Q,M,T) & ~ forfeits(R,O,Q,T)) => consents(R,O,Q,M,T))))",
   "Q may use O in manner M unless someone who holds a title against Q over O in M, and has not forfeited it, "
   "does not consent.")
ax('forbidden_use_def', 'use', 'definition',
   "![Q:en,O:en,M:man,T:tm]: (forbidden_use(Q,O,M,T) <=> ~ may_use(Q,O,M,T))",
   "A use is forbidden exactly when it is not permitted.")
ax('aggresses_in_def', 'use', 'definition',
   "![P:en,Q:en,M:man,T:tm]: (aggresses_in(P,Q,M,T) <=> (?[O:en]: (use(P,O,M,T) & owns(Q,O,P,M,T) "
   "& ~ forfeits(Q,O,P,T) & ~ consents(Q,O,P,M,T))))",
   "P's action in manner M aggresses against Q when it uses something over which Q holds an unforfeited "
   "title against P in M, without Q's consent.")
ax('aggresses_def', 'use', 'definition',
   "![P:en,Q:en,T:tm]: (aggresses(P,Q,T) <=> (?[M:man]: aggresses_in(P,Q,M,T)))",
   "P aggresses against Q when some action of P aggresses against Q.")
ax('forfeits_def', 'use', 'definition',
   "![R:en,O:en,Q:en,T:tm]: (forfeits(R,O,Q,T) <=> (?[M:man]: (aggresses_in(R,Q,M,T) & ((O = R) | use(R,O,M,T)))))",
   "While R aggresses against Q, R forfeits, with respect to Q, his titles over his own body and over the "
   "things he uses in the aggressing action. Q may use them without R's consent.")
ax('permissible_def', 'use', 'definition',
   "![P:en,M:man,T:tm]: (permissible(P,M,T) <=> (![O:en]: (use(P,O,M,T) => may_use(P,O,M,T))))",
   "An action is permissible when each thing it uses may be used in that manner.")
ax('controls_def', 'use', 'definition',
   "![P:en,O:en,T:tm]: (controls(P,O,T) <=> ((![M:man]: may_use(P,O,M,T)) & "
   "(![Q:en,M:man]: ((person(Q) & (Q != P)) => (may_use(Q,O,M,T) <=> consents(P,O,Q,M,T))))))",
   "P controls O when P may use O in every manner and every other person may use O exactly when P consents.")

# --- scarcity -------------------------------------------------------------------
ax('rivalrous_def', 'scarcity', 'definition',
   "![O:en]: (rivalrous(O) <=> (?[M1:man,M2:man]: clash(O,M1,M2)))",
   "A thing is scarce when some two uses of it clash.")
ax('clash_factual', 'scarcity', 'axiom',
   "![O:en,P1:en,P2:en,M1:man,M2:man,T:tm]: ((clash(O,M1,M2) & ~ ((P1 = P2) & (M1 = M2))) "
   "=> ~ (use(P1,O,M1,T) & use(P2,O,M2,T)))",
   "Two different use events in clashing manners do not happen at the same instant.")
ax('nonrivalrous_unowned', 'scarcity', 'axiom',
   "![O:en,T:tm]: (~ rivalrous(O) => unowned(O,T))",
   "Things that are not scarce (ideas, patterns) are never owned.")
ax('unowned_exists', 'scarcity', 'axiom',
   "?[O:en,T:tm]: (np_obj(O) & unowned(O,T))",
   "At some instant some object is unowned (there is a state of nature).")
ax('unrealised_def', 'scarcity', 'definition',
   "![P:en,O:en,M:man,T:tm]: (unrealised(P,O,M,T) <=> (wants(P,O,M,T) & ~ use(P,O,M,T)))",
   "A want is unrealised when the wanted use does not happen.")

# ---------------------------------------------------------------------------
# CONTRAST AXIOMS — NOT part of the theory. Each states a premise of an
# opposing view, so that the checks can show what it implies.
# ---------------------------------------------------------------------------
CONTRAST = []


def cx(name, text, gloss):
    CONTRAST.append(dict(name=name, group='contrast', kind='contrast', text=text, gloss=gloss, derived=None))


cx('control_use_liberty',
   "![P:en,O:en,M:man,T:tm]: (is_owner(P,O,T) => may_use(P,O,M,T))",
   "Control view: an owner may use his property in any manner.")
cx('control_protection',
   "![P:en,Q:en,O:en,M1:man,M2:man,T:tm]: ((is_owner(P,O,T) & wants(P,O,M1,T) & clash(O,M1,M2) "
   "& person(Q) & (Q != P)) => forbidden_use(Q,O,M2,T))",
   "Control view: no other person may use an owner's property in a way that clashes with what the owner wants.")
cx('control_protection_outsiders',
   "![P:en,Q:en,O:en,M1:man,M2:man,T:tm]: ((is_owner(P,O,T) & wants(P,O,M1,T) & clash(O,M1,M2) "
   "& person(Q) & (Q != P) & ~ is_owner(Q,O,T)) => forbidden_use(Q,O,M2,T))",
   "Weakened control view: the protection of an owner's wants runs only against persons who hold no title over the thing.")
cx('direction_exhaustive',
   "![A:en,B:en,O:en,M1:man,M2:man,T:tm]: ((person(A) & person(B) & (A != B) & wants(A,O,M1,T) "
   "& wants(B,O,M2,T) & clash(O,M1,M2)) => ((may_use(A,O,M1,T) & forbidden_use(B,O,M2,T)) "
   "| (may_use(B,O,M2,T) & forbidden_use(A,O,M1,T))))",
   "Direction view (LiquidZulu): every conflict over the use of a thing has a just victor, whose use is "
   "permitted while the other's is forbidden.")

# ---------------------------------------------------------------------------
# THEOREMS
# tag: 'headline' | 'substantive' | 'lemma' | 'sanity'
# deps: axioms/definitions the minimal problem contains
# lemmas: EARLIER theorems the minimal problem may use (so they form a DAG)
# ---------------------------------------------------------------------------
TH = []


def th(name, group, tag, text, gloss, deps, lemmas=(), contrast=()):
    TH.append(dict(name=name, group=group, tag=tag, text=text, gloss=gloss,
                   deps=list(deps), lemmas=list(lemmas), contrast=list(contrast)))


TIME = ['time_irreflexive', 'time_transitive', 'time_total']
AGG = ['aggresses_def', 'aggresses_in_def', 'forfeits_def']

# --- time: a limit of the title axioms ------------------------------------------
th('endless_past_paradox', 'time', 'substantive',
   "![P:en,Q:en,O:en]: ~ ((![T:tm]: (?[S:tm]: before(S,T))) & np_obj(O) & rivalrous(O) & person(Q) & (P != Q) "
   "& (![T:tm]: (?[M:man]: (use(P,O,M,T) & claim(P,O,T)))) "
   "& (![R:en,S:en,Q2:en,M2:man,T:tm]: ~ grants(R,S,O,Q2,M2,T)) "
   "& (![R:en,S:en,M2:man,T:tm]: ~ disowns(R,O,S,M2,T)))",
   "If time has no first instant, a person cannot use and claim a scarce object at every instant "
   "without grants or releases. The title axioms need a first instant.",
   ['title_genesis', 'title_acquired', 'acquires_def', 'unowned_def', 'is_owner_def', 'nodis_upto_def',
    'use_typing'] + TIME)

# --- persons ------------------------------------------------------------------
th('person_unownable', 'persons', 'substantive',
   "![P:en,O:en,Q:en,M:man,T:tm]: ((person(O) & (P != O)) => ~ owns(P,O,Q,M,T))",
   "Nobody holds a title over another person (no slavery).",
   ['owns_typing', 'entity_disjoint'])
th('no_self_exclusion', 'persons', 'sanity',
   "![P:en,O:en,M:man,T:tm]: ~ owns(P,O,P,M,T)",
   "Nobody holds a title against himself, so no owner needs his own consent.",
   ['owns_typing'])
th('body_sole_owner', 'persons', 'substantive',
   "![P:en,R:en,T:tm]: ((person(P) & is_owner(R,P,T)) => (R = P))",
   "Only you hold titles over your body.",
   ['is_owner_def'], ['person_unownable'])
th('self_use', 'persons', 'substantive',
   "![P:en,M:man,T:tm]: (person(P) => may_use(P,P,M,T))",
   "Everyone may use his own body in any manner, as far as the body alone is concerned.",
   ['may_use_def'], ['person_unownable', 'no_self_exclusion'])
th('bodily_integrity', 'persons', 'substantive',
   "![P:en,Q:en,M:man,T:tm]: ((person(P) & person(Q) & (P != Q) & use(Q,P,M,T) & ~ consents(P,P,Q,M,T) "
   "& ~ aggresses(P,Q,T)) => aggresses(Q,P,T))",
   "Using another person's body without consent is aggression against that person, "
   "unless that person is aggressing against the user at that instant.",
   ['self_ownership'] + AGG)
th('selective_consent', 'persons', 'substantive',
   "![P:en,F:en,S:en,M:man,T:tm]: ((person(P) & person(F) & person(S) & (P != F) & (P != S) "
   "& consents(P,P,F,M,T) & ~ consents(P,P,S,M,T) & ~ aggresses(P,S,T)) "
   "=> (may_use(F,P,M,T) & forbidden_use(S,P,M,T)))",
   "Consent is given person by person: the same use can be permitted to one person and forbidden to another.",
   ['may_use_def', 'forbidden_use_def', 'self_ownership', 'is_owner_def'] + AGG, ['body_sole_owner'])
th('voluntary_slavery_impossible', 'persons', 'substantive',
   "![R:en,P:en,O:en,Q:en,M:man,T:tm]: (person(O) => ~ grants(R,P,O,Q,M,T))",
   "Nobody can grant any title over a body, his own included (self-ownership is inalienable).",
   ['grant_typing', 'entity_disjoint'])

# --- titles over time -----------------------------------------------------------
th('title_persists', 'title', 'substantive',
   "![P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((owns(P,O,Q,M,T1) & np_obj(O) & before(T1,T2) "
   "& nodis_upto(P,O,Q,M,T1,T2)) => owns(P,O,Q,M,T2))",
   "A title lasts until it is released.",
   ['title_genesis', 'title_acquired', 'nodis_upto_def', 'owns_typing'] + TIME)
th('no_fresh_title', 'title', 'lemma',
   "![P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((np_obj(O) & ~ owns(P,O,Q,M,T1) & before(T1,T2) "
   "& (![T:tm]: (%s => ~ acquires(P,O,Q,M,T)))) => ~ owns(P,O,Q,M,T2))" % _win(),
   "A title not held at T1 is not held at T2 unless an acquisition event happens in between.",
   ['title_genesis', 'title_acquired', 'nodis_upto_def', 'owns_typing'] + TIME)
th('disown_extinguishes', 'title', 'lemma',
   "![P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((disowns(P,O,Q,M,T1) & before(T1,T2) "
   "& (![T:tm]: ((before(T1,T) & before(T,T2)) => ~ acquires(P,O,Q,M,T)))) => ~ owns(P,O,Q,M,T2))",
   "A released title stays released unless a new acquisition event happens.",
   ['title_genesis', 'nodis_upto_def', 'disowns_typing'] + TIME)

# --- use and the right to exclude ---------------------------------------------
th('unexcluded_use', 'use', 'substantive',
   "![Q:en,O:en,M:man,T:tm]: ((![R:en]: ~ owns(R,O,Q,M,T)) => may_use(Q,O,M,T))",
   "If nobody holds a title against you over a thing in a manner, you may use it in that manner. "
   "Ownership is not needed for use.",
   ['may_use_def'])
th('unowned_use', 'use', 'substantive',
   "![Q:en,O:en,M:man,T:tm]: (unowned(O,T) => may_use(Q,O,M,T))",
   "Anyone may use an unowned thing.",
   ['unowned_def', 'is_owner_def'], ['unexcluded_use'])
th('nonrival_use_free', 'use', 'substantive',
   "![Q:en,O:en,M:man,T:tm]: (~ rivalrous(O) => may_use(Q,O,M,T))",
   "Anyone may use a thing that is not scarce (an idea) in any manner.",
   ['nonrivalrous_unowned'], ['unowned_use'])
th('theft_forbidden', 'use', 'substantive',
   "![R:en,O:en,Q:en,M:man,T:tm]: ((owns(R,O,Q,M,T) & ~ consents(R,O,Q,M,T) & ~ aggresses(R,Q,T)) "
   "=> forbidden_use(Q,O,M,T))",
   "If someone who holds a title against you over a thing does not consent, your use is forbidden "
   "(unless he is aggressing against you at that instant).",
   ['may_use_def', 'forbidden_use_def'] + AGG)
th('joint_deadlock', 'use', 'headline',
   "![A:en,B:en,O:en,M1:man,M2:man,T:tm]: ((owns(A,O,B,M2,T) & owns(B,O,A,M1,T) & ~ consents(A,O,B,M2,T) "
   "& ~ consents(B,O,A,M1,T) & ~ aggresses(A,B,T) & ~ aggresses(B,A,T)) "
   "=> (forbidden_use(A,O,M1,T) & forbidden_use(B,O,M2,T)))",
   "Co-owners who refuse each other are both forbidden. This is a deadlock, not a contradiction.",
   [], ['theft_forbidden'])
th('co_owner_use_by_consent', 'use', 'substantive',
   "![A:en,B:en,O:en,M:man,T:tm]: ((owns(B,O,A,M,T) & consents(B,O,A,M,T) "
   "& (![R:en]: (owns(R,O,A,M,T) => (R = B)))) => may_use(A,O,M,T))",
   "A co-owner may use the common thing when the only other person who may exclude him consents.",
   ['may_use_def'])
th('easement_use', 'use', 'headline',
   "![R:en,E:en,O:en,M:man,T1:tm,T2:tm]: ((disowns(R,O,E,M,T1) & before(T1,T2) "
   "& (![T:tm]: ((before(T1,T) & before(T,T2)) => ~ acquires(R,O,E,M,T))) "
   "& (![S:en]: ((S != R) => ~ owns(S,O,E,M,T2)))) => may_use(E,O,M,T2))",
   "An easement: after an owner releases one person from one manner, that person may use the thing "
   "in that manner without asking, provided nobody else may exclude him from it.",
   [], ['disown_extinguishes', 'unexcluded_use'])

# --- two forms of co-ownership: veto and free use --------------------------------------
th('free_use_unsettled', 'coforms', 'headline',
   "![A:en,B:en,O:en,M1:man,M2:man,T:tm]: (((![R:en]: ~ owns(R,O,A,M1,T)) & (![R:en]: ~ owns(R,O,B,M2,T)) "
   "& clash(O,M1,M2) & (A != B)) => (may_use(A,O,M1,T) & may_use(B,O,M2,T) & ~ (use(A,O,M1,T) & use(B,O,M2,T))))",
   "Free use (the usual legal form of co-ownership: titles against outsiders only). Two clashing uses are both "
   "permitted, but at most one can happen. The titles do not settle which one.",
   ['clash_factual'], ['unexcluded_use'])
th('veto_settles_conflict', 'coforms', 'headline',
   "![A:en,B:en,O:en,M1:man,M2:man,T:tm]: ((full_owner(A,O,T) & full_owner(B,O,T) & person(A) & person(B) "
   "& (A != B) & ~ aggresses(A,B,T) & ~ aggresses(B,A,T) & may_use(A,O,M1,T) & may_use(B,O,M2,T)) "
   "=> (consents(B,O,A,M1,T) & consents(A,O,B,M2,T)))",
   "Veto co-ownership (this theory's co-owners): two uses by co-owners are both permitted only if each consents "
   "to the other's. The titles settle every conflict between co-owners, in favour of an agreed use or of no use.",
   ['full_owner_def', 'may_use_def', 'forfeits_def', 'aggresses_def'])

# --- action, aggression and defence ---------------------------------------------
th('aggression_iff_forbidden_use', 'aggression', 'substantive',
   "![P:en,T:tm]: ((?[Q:en]: aggresses(P,Q,T)) <=> (?[O:en,M:man]: (use(P,O,M,T) & forbidden_use(P,O,M,T))))",
   "To aggress is exactly to make a forbidden use of something; every forbidden use has a victim.",
   ['aggresses_def', 'aggresses_in_def', 'may_use_def', 'forbidden_use_def'])
th('no_self_aggression', 'aggression', 'sanity',
   "![P:en,T:tm]: ~ aggresses(P,P,T)",
   "Nobody aggresses against himself.",
   ['aggresses_def', 'aggresses_in_def'], ['no_self_exclusion'])
th('ownership_is_not_licence', 'aggression', 'headline',
   "![P:en,R:en,O1:en,O2:en,M:man,T:tm]: (((![S:en]: ~ owns(S,O1,P,M,T)) & use(P,O1,M,T) & use(P,O2,M,T) "
   "& owns(R,O2,P,M,T) & ~ consents(R,O2,P,M,T) & ~ aggresses(R,P,T)) "
   "=> (may_use(P,O1,M,T) & aggresses(P,R,T) & ~ permissible(P,M,T)))",
   "Your fist ends where my nose begins: P may use his own knife, but an action that also uses "
   "R's property without R's consent is aggression, and is not permissible.",
   ['permissible_def', 'forbidden_use_def'] + AGG, ['unexcluded_use', 'theft_forbidden'])
th('action_liberty', 'aggression', 'substantive',
   "![P:en,M:man,T:tm]: ((![O:en]: (use(P,O,M,T) => (![R:en]: ~ owns(R,O,P,M,T)))) => permissible(P,M,T))",
   "An action is permissible if nobody holds a title against the person over anything the action uses "
   "(his own sole property, his own body, unowned things).",
   ['permissible_def'], ['unexcluded_use'])
th('unowned_use_innocent', 'aggression', 'substantive',
   "![P:en,Q:en,T:tm]: ((![O:en,M:man]: (use(P,O,M,T) => unowned(O,T))) => ~ aggresses(P,Q,T))",
   "Using only unowned things never wrongs anyone.",
   ['aggresses_def', 'aggresses_in_def', 'unowned_def', 'is_owner_def'])
th('co_owner_trespass', 'aggression', 'substantive',
   "![A:en,B:en,O:en,M:man,T:tm]: ((owns(A,O,B,M,T) & owns(B,O,A,M,T) & use(A,O,M,T) "
   "& ~ consents(B,O,A,M,T) & ~ aggresses(B,A,T)) => aggresses(A,B,T))",
   "A co-owner who uses the common thing against the other co-owner's will aggresses against him.",
   AGG)
th('refraining_innocent', 'aggression', 'sanity',
   "![P:en,Q:en,T:tm]: ((![O:en,M:man]: ~ use(P,O,M,T)) => ~ aggresses(P,Q,T))",
   "Doing nothing never violates anyone's rights.",
   ['aggresses_def', 'aggresses_in_def'])
th('defence_is_not_aggression', 'aggression', 'headline',
   "![P:en,Q:en,T:tm]: ((aggresses(P,Q,T) & (![O:en,M:man]: ((use(Q,O,M,T) & owns(P,O,Q,M,T)) "
   "=> ((O = P) | (?[M2:man]: (aggresses_in(P,Q,M2,T) & use(P,O,M2,T))))))) => ~ aggresses(Q,P,T))",
   "Protecting one's property is not aggression: a person who, against his aggressor, uses only the "
   "aggressor's body and the things the aggressor uses in the aggression does not aggress against him.",
   AGG)
th('fight_one_aggressor', 'aggression', 'headline',
   "![P:en,Q:en,M1:man,M2:man,T:tm]: ((person(P) & person(Q) & (P != Q) & use(P,Q,M1,T) & use(Q,P,M2,T) "
   "& ~ consents(Q,Q,P,M1,T) & ~ consents(P,P,Q,M2,T) "
   "& (![O:en,M:man]: ((use(P,O,M,T) & owns(Q,O,P,M,T)) => (O = Q))) "
   "& (![O:en,M:man]: ((use(Q,O,M,T) & owns(P,O,Q,M,T)) => (O = P)))) "
   "=> (aggresses(P,Q,T) <=> ~ aggresses(Q,P,T)))",
   "In a fight in which each person uses only the other's body, exactly one of them is the aggressor. "
   "The theory does not say which: that is the question of who started it.",
   ['self_ownership'] + AGG)

# --- scarcity -------------------------------------------------------------------
th('rival_wants_unrealised', 'scarcity', 'substantive',
   "![O:en,P1:en,P2:en,M1:man,M2:man,T:tm]: ((clash(O,M1,M2) & (P1 != P2) & use(P1,O,M1,T) "
   "& wants(P2,O,M2,T)) => unrealised(P2,O,M2,T))",
   "When one person uses a scarce thing, a second person who wants a clashing use cannot have it: "
   "conflict is possible, which is why titles are needed.",
   ['clash_factual', 'unrealised_def'])

# --- acquisition by homesteading -------------------------------------------------
th('homesteader_owns', 'homesteading', 'substantive',
   "![P:en,O:en,Q:en,M:man,M2:man,T1:tm,T2:tm]: ((rivalrous(O) & use(P,O,M2,T1) & claim(P,O,T1) "
   "& unowned(O,T1) & person(Q) & (P != Q) & before(T1,T2) & nodis_upto(P,O,Q,M,T1,T2)) "
   "=> owns(P,O,Q,M,T2))",
   "Whoever first uses and claims an unowned scarce thing then holds a title against every other person, "
   "in every manner.",
   ['acquires_def', 'title_acquired'])
th('homesteader_full_owner', 'homesteading', 'headline',
   "![P:en,O:en,M2:man,T1:tm,T2:tm]: ((rivalrous(O) & use(P,O,M2,T1) & claim(P,O,T1) & unowned(O,T1) "
   "& before(T1,T2) & (![Q:en,M:man]: nodis_upto(P,O,Q,M,T1,T2))) => full_owner(P,O,T2))",
   "Homesteading makes the homesteader a full owner: he may exclude everyone else from every use.",
   ['full_owner_def'], ['homesteader_owns'])
th('first_homesteader_exclusive', 'homesteading', 'substantive',
   "![P:en,O:en,Q:en,M:man,M2:man,T1:tm,T2:tm]: ((rivalrous(O) & use(P,O,M2,T1) & claim(P,O,T1) "
   "& unowned(O,T1) & person(Q) & (P != Q) & before(T1,T2) & nodis_upto(P,O,Q,M,T1,T2)) "
   "=> ~ unowned(O,T2))",
   "After a valid homestead the thing is no longer unowned, so later comers cannot homestead it.",
   ['unowned_def', 'is_owner_def'], ['homesteader_owns'])
th('joint_homesteading', 'homesteading', 'headline',
   "![A:en,B:en,O:en,M1:man,M2:man,T1:tm,T2:tm]: ((rivalrous(O) & use(A,O,M1,T1) & claim(A,O,T1) "
   "& use(B,O,M2,T1) & claim(B,O,T1) & unowned(O,T1) & before(T1,T2) "
   "& (![Q:en,M:man]: (nodis_upto(A,O,Q,M,T1,T2) & nodis_upto(B,O,Q,M,T1,T2)))) "
   "=> (full_owner(A,O,T2) & full_owner(B,O,T2)))",
   "Two persons who homestead a thing together both become full owners of it: co-owners.",
   [], ['homesteader_full_owner'])

# --- grants, gifts, transfers and leases ---------------------------------------------
th('grant_conveys', 'transfer', 'substantive',
   "![R:en,P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((grants(R,P,O,Q,M,T1) & accepts(P,R,O,T1) "
   "& (owns(R,O,Q,M,T1) | (Q = R)) & (P != Q) & before(T1,T2) & nodis_upto(P,O,Q,M,T1,T2)) "
   "=> owns(P,O,Q,M,T2))",
   "An accepted grant of a title that the granter holds, or of a title against the granter, gives the "
   "grantee that title at every later instant until he releases it.",
   ['acquires_def', 'title_acquired', 'grant_typing', 'is_owner_def', 'owns_typing'])
th('no_title_without_acceptance', 'transfer', 'headline',
   "![P:en,O:en,Q:en,M:man,T2:tm]: ((np_obj(O) & owns(P,O,Q,M,T2) "
   "& (![M2:man,T:tm]: (before(T,T2) => ~ (use(P,O,M2,T) & claim(P,O,T))))) "
   "=> (?[R:en,T1:tm]: (before(T1,T2) & accepts(P,R,O,T1))))",
   "Apart from homesteading, nobody acquires a title without accepting it.",
   ['title_genesis', 'acquires_def'])
th('share_gift', 'transfer', 'headline',
   "![R:en,P:en,O:en,T1:tm,T2:tm]: ((gives_share(R,P,O,T1) & accepts(P,R,O,T1) & full_owner(R,O,T1) "
   "& before(T1,T2) & (![Q:en,M:man]: (nodis_upto(R,O,Q,M,T1,T2) & nodis_upto(P,O,Q,M,T1,T2)))) "
   "=> (full_owner(R,O,T2) & full_owner(P,O,T2)))",
   "A full owner who gives a share, and whose gift is accepted, makes the recipient a full owner too: "
   "giver and recipient are co-owners.",
   ['gives_share_def', 'shares_def', 'full_owner_def', 'grant_typing'], ['grant_conveys', 'title_persists'])
th('transferee_owns', 'transfer', 'substantive',
   "![R:en,P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((vol_transfer(R,P,O,T1) & accepts(P,R,O,T1) "
   "& (owns(R,O,Q,M,T1) | (Q = R)) & (P != Q) & before(T1,T2) & nodis_upto(P,O,Q,M,T1,T2)) "
   "=> owns(P,O,Q,M,T2))",
   "After an accepted transfer, the new owner holds each title the former owner held, and titles against "
   "the former owner.",
   ['vol_transfer_def', 'gives_share_def', 'shares_def'], ['grant_conveys'])
th('joint_purchase', 'transfer', 'headline',
   "![R:en,A:en,B:en,O:en,T1:tm,T2:tm]: ((vol_transfer(R,A,O,T1) & vol_transfer(R,B,O,T1) "
   "& accepts(A,R,O,T1) & accepts(B,R,O,T1) & full_owner(R,O,T1) & before(T1,T2) "
   "& (![Q:en,M:man]: (nodis_upto(A,O,Q,M,T1,T2) & nodis_upto(B,O,Q,M,T1,T2)))) "
   "=> (full_owner(A,O,T2) & full_owner(B,O,T2)))",
   "A full owner who transfers a thing to two persons at the same instant makes them co-owners "
   "(a joint purchase).",
   ['full_owner_def', 'vol_transfer_def', 'gives_share_def', 'shares_def', 'grant_typing'],
   ['transferee_owns'])
th('nemo_dat', 'transfer', 'headline',
   "![R:en,P:en,O:en,Q:en,M:man,T1:tm,T2:tm]: ((np_obj(O) & grants(R,P,O,Q,M,T1) & (Q != R) "
   "& ~ owns(R,O,Q,M,T1) & before(T1,T2) "
   "& (![S:en,T:tm]: ((before(T,T2) & grants(S,P,O,Q,M,T)) => ((S = R) & (T = T1)))) "
   "& (![M2:man,T:tm]: (before(T,T2) => ~ (use(P,O,M2,T) & claim(P,O,T))))) => ~ owns(P,O,Q,M,T2))",
   "Nobody gives what he does not have: a title that the granter does not hold does not reach the "
   "grantee through the grant.",
   ['title_genesis', 'acquires_def'])
th('transfer_is_abandonment', 'transfer', 'lemma',
   "![P1:en,P2:en,O:en,T:tm]: (vol_transfer(P1,P2,O,T) => abandons(P1,O,T))",
   "A transfer is an abandonment in favour of a named person.",
   ['vol_transfer_def'])
th('abandoner_not_owner', 'abandonment', 'lemma',
   "![P:en,O:en,T1:tm,T2:tm]: ((abandons(P,O,T1) & before(T1,T2) "
   "& (![Q:en,M:man,T:tm]: (%s => ~ acquires(P,O,Q,M,T)))) => ~ is_owner(P,O,T2))" % _win(),
   "Whoever abandons a thing holds no title over it afterwards, unless he acquires one again.",
   ['abandons_def', 'is_owner_def'] + TIME, ['disown_extinguishes', 'no_fresh_title'])
th('transferor_not_owner', 'transfer', 'substantive',
   "![P1:en,P2:en,O:en,T1:tm,T2:tm]: ((vol_transfer(P1,P2,O,T1) & before(T1,T2) "
   "& (![Q:en,M:man,T:tm]: (%s => ~ acquires(P1,O,Q,M,T)))) => ~ is_owner(P1,O,T2))" % _win(),
   "After a transfer the former owner holds no title over the thing, unless he acquires one again.",
   [], ['transfer_is_abandonment', 'abandoner_not_owner'])
th('no_double_spend', 'transfer', 'headline',
   "![P1:en,P2:en,S:en,Q:en,M:man,O:en,T1:tm,T2:tm]: ((vol_transfer(P1,P2,O,T1) & before(T1,T2) "
   "& (![Q2:en,M2:man,T:tm]: (%s => ~ acquires(P1,O,Q2,M2,T)))) => ~ grants(P1,S,O,Q,M,T2))" % _win(),
   "Nobody can sell a thing twice: after a transfer, the former owner can grant nothing over it, "
   "unless he acquires it again. (Selling to two persons at the same instant is a joint purchase.)",
   ['grant_typing'], ['transferor_not_owner'])
th('lease_tenant_excludes_landlord', 'transfer', 'headline',
   "![L:en,N:en,O:en,M:man,T1:tm,T2:tm]: ((transfers_manner(L,N,O,M,T1) & accepts(N,L,O,T1) "
   "& before(T1,T2) & nodis_upto(N,O,L,M,T1,T2)) => owns(N,O,L,M,T2))",
   "A lease of manner M: the tenant may exclude the landlord from using the thing in manner M.",
   ['transfers_manner_def', 'shares_def', 'grant_typing'], ['grant_conveys'])
th('lessor_loses_manner', 'transfer', 'substantive',
   "![L:en,N:en,O:en,M:man,T1:tm,T2:tm]: ((transfers_manner(L,N,O,M,T1) & before(T1,T2) "
   "& (![Q:en,T:tm]: (%s => ~ acquires(L,O,Q,M,T)))) => (![Q:en]: ~ owns(L,O,Q,M,T2)))" % _win(),
   "During a lease of manner M the landlord holds no title in manner M (unless he acquires one again). "
   "His titles in the other manners are untouched.",
   ['transfers_manner_def', 'shares_def', 'grant_typing'] + TIME, ['disown_extinguishes', 'no_fresh_title'])

# --- abandonment and the life cycle ---------------------------------------------------
th('res_nullius', 'abandonment', 'headline',
   "![P:en,O:en,T1:tm,T2:tm]: ((abandons(P,O,T1) & (![R:en]: (is_owner(R,O,T1) => (R = P))) & before(T1,T2) "
   "& (![R:en,Q:en,M:man,T:tm]: (%s => ~ acquires(R,O,Q,M,T)))) => unowned(O,T2))" % _win(),
   "When the only owner abandons a thing and nobody acquires it meanwhile, it becomes unowned again.",
   ['abandons_def', 'unowned_def', 'is_owner_def'], ['abandoner_not_owner', 'no_fresh_title'])
th('life_cycle', 'abandonment', 'headline',
   "![P:en,S:en,Q:en,O:en,M:man,M2:man,T1:tm,T2:tm,T3:tm]: ((abandons(P,O,T1) "
   "& (![R:en]: (is_owner(R,O,T1) => (R = P))) & before(T1,T2) "
   "& (![R:en,Q2:en,M3:man,T:tm]: (%s => ~ acquires(R,O,Q2,M3,T))) "
   "& rivalrous(O) & use(S,O,M2,T2) & claim(S,O,T2) & person(Q) & (S != Q) & before(T2,T3) "
   "& nodis_upto(S,O,Q,M,T2,T3)) => owns(S,O,Q,M,T3))" % _win(),
   "Full cycle: an abandoned thing can be homesteaded again by anyone, the former owner included.",
   [], ['res_nullius', 'homesteader_owns'])

# --- control: what the control view describes ---------------------------------------------
th('sole_owner_controls', 'control', 'headline',
   "![P:en,O:en,T:tm]: (((![R:en,M:man]: ~ owns(R,O,P,M,T)) & (![Q:en]: ~ aggresses(P,Q,T)) "
   "& (![Q:en,M:man]: ((person(Q) & (Q != P)) => (owns(P,O,Q,M,T) & (![R:en]: (owns(R,O,Q,M,T) => (R = P))))))) "
   "=> controls(P,O,T))",
   "A sole full owner controls his property: he may use it in every manner (as far as this thing goes), "
   "and others may use it exactly when he consents. The control view describes this special case.",
   ['controls_def', 'may_use_def', 'forfeits_def', 'aggresses_def'])
th('control_needs_deference', 'control', 'headline',
   "![A:en,B:en,O:en,M:man,T:tm]: ((controls(A,O,T) & owns(B,O,A,M,T) & ~ aggresses(B,A,T)) "
   "=> consents(B,O,A,M,T))",
   "A co-owner controls the thing only if every other person who may exclude him consents to every use he makes. "
   "A co-owner whose wish for idleness prevails does not thereby control the thing.",
   ['controls_def', 'may_use_def', 'forfeits_def', 'aggresses_def'])
th('unanimity', 'control', 'substantive',
   "![A:en,B:en,C:en,O:en,M:man,T:tm]: (((![R:en]: (owns(R,O,C,M,T) => ((R = A) | (R = B)))) "
   "& owns(A,O,C,M,T) & owns(B,O,C,M,T) & ~ aggresses(A,C,T) & ~ aggresses(B,C,T)) "
   "=> (may_use(C,O,M,T) <=> (consents(A,O,C,M,T) & consents(B,O,C,M,T))))",
   "When two co-owners hold the only titles against a third person, he may use the thing exactly when both consent.",
   ['may_use_def', 'forfeits_def', 'aggresses_def'])

# --- contrasts: the control view and the direction view -------------------------------
th('control_no_refusal', 'contrast', 'headline',
   "![A:en,B:en,O:en,M:man,T:tm]: ((owns(A,O,B,M,T) & is_owner(B,O,T) & ~ aggresses(A,B,T)) "
   "=> consents(A,O,B,M,T))",
   "If ownership also gave a right to use, no co-owner could ever refuse another co-owner anything: "
   "the right to exclude between co-owners would vanish.",
   ['may_use_def', 'forfeits_def', 'aggresses_def'], contrast=['control_use_liberty'])
th('control_coownership_contradiction', 'contrast', 'headline',
   "![A:en,B:en,O:en,M1:man,M2:man,T:tm]: ~ (is_owner(A,O,T) & is_owner(B,O,T) & (A != B) "
   "& wants(A,O,M1,T) & clash(O,M1,M2))",
   "If ownership meant control (use as one wishes, protected against clashing uses by anyone), two "
   "co-owners of a scarce thing could never want a clashing use of it. Since wants are free, "
   "co-ownership would be contradictory. Under the exclusion view the same situation has a model.",
   ['forbidden_use_def', 'is_owner_def', 'owns_typing'], contrast=['control_use_liberty', 'control_protection'])
th('direction_overreach', 'contrast', 'headline',
   "![R:en,A:en,B:en,O:en,M1:man,M2:man,T:tm]: ~ (person(A) & person(B) & (A != B) "
   "& owns(R,O,A,M1,T) & owns(R,O,B,M2,T) & ~ consents(R,O,A,M1,T) & ~ consents(R,O,B,M2,T) "
   "& ~ aggresses(R,A,T) & ~ aggresses(R,B,T) & wants(A,O,M1,T) & wants(B,O,M2,T) & clash(O,M1,M2))",
   "If every conflict had a just victor (LiquidZulu's premise), an owner could never refuse two rivals "
   "who want clashing uses of his property: one of them would have to be permitted.",
   ['forbidden_use_def'], ['theft_forbidden'], contrast=['direction_exhaustive'])
th('direction_forbids_deadlock', 'contrast', 'headline',
   "![A:en,B:en,O:en,M1:man,M2:man,T:tm]: ~ (person(A) & person(B) & (A != B) "
   "& owns(A,O,B,M2,T) & owns(B,O,A,M1,T) & ~ consents(A,O,B,M2,T) & ~ consents(B,O,A,M1,T) "
   "& ~ aggresses(A,B,T) & ~ aggresses(B,A,T) & wants(A,O,M1,T) & wants(B,O,M2,T) & clash(O,M1,M2))",
   "Restricted to co-owners, the same premise simply forbids a deadlock between them: it assumes what "
   "the argument against co-ownership sets out to prove.",
   ['forbidden_use_def'], ['theft_forbidden'], contrast=['direction_exhaustive'])


# ---------------------------------------------------------------------------
# SCENARIOS — finite model checks (Z3 over a grounded finite domain)
#   dom: sort -> element names (distinct names = distinct elements)
#   facts: formulas added to the theory
#   expect: 'sat' or 'unsat'
#   forced: formulas that must hold in EVERY model of theory+facts
#           (checked by asserting their negation and expecting unsat)
# ---------------------------------------------------------------------------
P3 = ['ada', 'ben', 'cy']
SC = []


def sc(name, gloss, dom, facts, expect, forced=(), contrast=()):
    SC.append(dict(name=name, gloss=gloss, dom=dom, facts=list(facts), expect=expect,
                   forced=list(forced), contrast=list(contrast)))


def _dom(ents, times, manners):
    return {'en': ents, 'tm': times, 'man': manners}


ORDER4 = ["before(t0,t1)", "before(t1,t2)", "before(t2,t3)"]
ORDER3 = ["before(t0,t1)", "before(t1,t2)"]
KINDS = ["person(ada)", "person(ben)", "person(cy)", "np_obj(field)"]
D4 = _dom(P3 + ['field'], ['t0', 't1', 't2', 't3'], ['plow', 'sow'])
D3 = _dom(P3 + ['field'], ['t0', 't1', 't2'], ['plow', 'sow'])
HOMESTEAD_ADA = ["clash(field,plow,plow)", "use(ada,field,plow,t0)", "claim(ada,field,t0)", "unowned(field,t0)",
                 "![P:en]: ((P != ada) => ~ claim(P,field,t0))"]
CO_AB = lambda t: "![M:man]: (owns(ada,field,ben,M,%s) & owns(ben,field,ada,M,%s))" % (t, t)

sc('co_ownership_consistent',
   "Ada and Ben co-own the field. Each refuses the other every use, Ada wants to plow, plowing "
   "clashes with sowing, and nobody aggresses. The exclusion view has a model.",
   D3, KINDS + ORDER3 + [
       CO_AB('t1'),
       "![M:man]: (~ consents(ada,field,ben,M,t1) & ~ consents(ben,field,ada,M,t1))",
       "wants(ada,field,plow,t1)", "wants(ben,field,sow,t1)", "clash(field,plow,sow)",
       "![P:en,Q:en,T:tm]: ~ aggresses(P,Q,T)"],
   'sat', forced=["forbidden_use(ada,field,plow,t1)", "forbidden_use(ben,field,sow,t1)"])
sc('co_ownership_under_control_view',
   "The same situation, with the two control axioms added: no model.",
   D3, KINDS + ORDER3 + [CO_AB('t1'), "wants(ada,field,plow,t1)", "clash(field,plow,sow)"],
   'unsat', contrast=['control_use_liberty', 'control_protection'])
CO_WANTS = [CO_AB('t1'), "wants(ada,field,plow,t1)", "wants(ben,field,sow,t1)", "clash(field,plow,sow)"]
sc('co_ownership_with_use_liberty_only',
   "Co-ownership with clashing wants, plus only the first control axiom (an owner may use his property "
   "in any manner): consistent.",
   D3, KINDS + ORDER3 + CO_WANTS, 'sat', contrast=['control_use_liberty'])
sc('co_ownership_with_protection_only',
   "Co-ownership with clashing wants, plus only the second control axiom (protection of the owner's wants): "
   "consistent.",
   D3, KINDS + ORDER3 + CO_WANTS, 'sat', contrast=['control_protection'])
sc('co_ownership_with_protection_against_outsiders',
   "Co-ownership with clashing wants, plus the use liberty and a protection that runs only against "
   "non-owners: consistent. Both co-owners may then make clashing uses.",
   D3, KINDS + ORDER3 + CO_WANTS, 'sat', contrast=['control_use_liberty', 'control_protection_outsiders'],
   forced=["may_use(ada,field,plow,t1)", "may_use(ben,field,sow,t1)"])
sc('sole_ownership_under_control_view',
   "The control view is consistent with sole ownership: Ada alone owns the field and wants to plow.",
   D3, KINDS + ORDER3 + [
       "![M:man]: (owns(ada,field,ben,M,t1) & owns(ada,field,cy,M,t1))",
       "![R:en,Q:en,M:man]: (owns(R,field,Q,M,t1) => (R = ada))",
       "wants(ada,field,plow,t1)", "clash(field,plow,sow)"],
   'sat', contrast=['control_use_liberty', 'control_protection'],
   forced=["forbidden_use(ben,field,sow,t1)", "may_use(ada,field,sow,t1)"])
sc('co_ownership_under_direction_view',
   "Co-owners who refuse each other and want clashing uses, with LiquidZulu's just-victor premise added: no model.",
   D3, KINDS + ORDER3 + [
       CO_AB('t1'), "![M:man]: (~ consents(ada,field,ben,M,t1) & ~ consents(ben,field,ada,M,t1))",
       "![P:en,Q:en]: ~ aggresses(P,Q,t1)",
       "wants(ada,field,plow,t1)", "wants(ben,field,sow,t1)", "clash(field,plow,sow)"],
   'unsat', contrast=['direction_exhaustive'])
sc('owner_refuses_two_rivals',
   "Ada is the sole full owner. Ben wants to plow and Cy wants to sow; the uses clash; Ada refuses both. "
   "The exclusion view has a model.",
   D3, KINDS + ORDER3 + [
       "![M:man]: (owns(ada,field,ben,M,t1) & owns(ada,field,cy,M,t1))",
       "![P:en,Q:en]: ~ aggresses(P,Q,t1)",
       "~ consents(ada,field,ben,plow,t1)", "~ consents(ada,field,cy,sow,t1)",
       "wants(ben,field,plow,t1)", "wants(cy,field,sow,t1)", "clash(field,plow,sow)"],
   'sat', forced=["forbidden_use(ben,field,plow,t1)", "forbidden_use(cy,field,sow,t1)"])
sc('owner_refuses_two_rivals_under_direction_view',
   "The same situation with LiquidZulu's just-victor premise added: no model. The premise forces the "
   "owner to admit one of the rivals.",
   D3, KINDS + ORDER3 + [
       "![M:man]: (owns(ada,field,ben,M,t1) & owns(ada,field,cy,M,t1))",
       "![P:en,Q:en]: ~ aggresses(P,Q,t1)",
       "~ consents(ada,field,ben,plow,t1)", "~ consents(ada,field,cy,sow,t1)",
       "wants(ben,field,plow,t1)", "wants(cy,field,sow,t1)", "clash(field,plow,sow)"],
   'unsat', contrast=['direction_exhaustive'])
FREE = KINDS + ORDER4 + [
    "![M:man]: (owns(ada,field,cy,M,t2) & owns(ben,field,cy,M,t2))",
    "![R:en,M:man]: (~ owns(R,field,ada,M,t2) & ~ owns(R,field,ben,M,t2))",
    "clash(field,plow,sow)",
    "![O:en,M:man]: ((O != field) => (~ use(ada,O,M,t2) & ~ use(ben,O,M,t2)))"]
sc('free_use_ada_acts_first',
   "Free use: Ada and Ben hold titles against Cy only. Ada plows at t2; Ben wants to sow, which clashes. "
   "Ada's use goes ahead, Ben's want is unrealised, and nobody aggresses.",
   D4, FREE + ["use(ada,field,plow,t2)", "wants(ben,field,sow,t2)"],
   'sat', forced=["may_use(ben,field,sow,t2)", "unrealised(ben,field,sow,t2)",
                  "~ aggresses(ada,ben,t2)", "~ aggresses(ben,ada,t2)"])
sc('free_use_ben_acts_first',
   "The same free-use co-ownership, but Ben sows first and Ada's want to plow is unrealised. Also no aggression. "
   "The titles allow either outcome: which use goes ahead depends on who acts, not on any right.",
   D4, FREE + ["use(ben,field,sow,t2)", "wants(ada,field,plow,t2)"],
   'sat', forced=["may_use(ada,field,plow,t2)", "unrealised(ada,field,plow,t2)",
                  "~ aggresses(ada,ben,t2)", "~ aggresses(ben,ada,t2)"])
sc('owner_may_be_forbidden',
   "Ownership is not a right to use: Ben holds titles over the field, yet his use is forbidden because "
   "Ada, a co-owner, refuses.",
   D3, KINDS + ORDER3 + [
       "is_owner(ben,field,t1)", "owns(ada,field,ben,plow,t1)", "~ consents(ada,field,ben,plow,t1)",
       "~ aggresses(ada,ben,t1)"],
   'sat', forced=["forbidden_use(ben,field,plow,t1)"])
sc('non_owner_may_use',
   "Use does not need ownership: Cy holds no title over the field, yet may sow it with consent.",
   D3, KINDS + ORDER3 + [
       "~ is_owner(cy,field,t1)", "owns(ada,field,cy,sow,t1)", "consents(ada,field,cy,sow,t1)",
       "![R:en]: (owns(R,field,cy,sow,t1) => (R = ada))"],
   'sat', forced=["may_use(cy,field,sow,t1)"])
sc('partial_title_no_veto',
   "Regression for the v0.19 defect: Ada's titles are partial (against Cy, not Ben). Her refusal does "
   "not forbid Ben, whom nobody may exclude.",
   D3, KINDS + ORDER3 + [
       "![M:man]: owns(ada,field,cy,M,t2)", "![R:en,M:man]: ~ owns(R,field,ben,M,t2)",
       "~ consents(ada,field,ben,plow,t2)"],
   'sat', forced=["may_use(ben,field,plow,t2)"])
sc('fist_and_nose',
   "Cy is sole owner of a knife; one action of Cy uses the knife and Ada's body without her consent.",
   _dom(P3 + ['knife'], ['t0', 't1'], ['cut', 'hold']),
   ["person(ada)", "person(ben)", "person(cy)", "np_obj(knife)", "before(t0,t1)",
    "![S:en,M:man]: ~ owns(S,knife,cy,M,t1)", "![M:man]: (owns(cy,knife,ada,M,t1) & owns(cy,knife,ben,M,t1))",
    "use(cy,knife,cut,t1)", "use(cy,ada,cut,t1)", "~ consents(ada,ada,cy,cut,t1)", "~ aggresses(ada,cy,t1)"],
   'sat', forced=["may_use(cy,knife,cut,t1)", "aggresses(cy,ada,t1)", "~ permissible(cy,cut,t1)"])
DEF = _dom(P3 + ['field'], ['t0', 't1', 't2'], ['walk', 'hold'])
sc('self_defence',
   "Cy walks across Ada's field without her consent; Ada pushes him off (she uses his body). "
   "Cy is the aggressor; Ada's push is not aggression.",
   DEF, KINDS + ORDER3 + [
       "![M:man]: (owns(ada,field,cy,M,t1) & owns(ada,field,ben,M,t1))",
       "use(cy,field,walk,t1)", "~ consents(ada,field,cy,walk,t1)",
       "use(ada,cy,hold,t1)", "~ consents(cy,cy,ada,hold,t1)",
       "![O:en,M:man]: (use(ada,O,M,t1) => ((O = cy) & (M = hold)))",
       "![O:en,M:man]: (use(cy,O,M,t1) => ((O = field) & (M = walk)))"],
   'sat', forced=["aggresses(cy,ada,t1)", "~ aggresses(ada,cy,t1)", "may_use(ada,cy,hold,t1)"])
FIGHT = KINDS + ORDER3 + [
    "use(ada,ben,hold,t1)", "use(ben,ada,hold,t1)",
    "~ consents(ben,ben,ada,hold,t1)", "~ consents(ada,ada,ben,hold,t1)",
    "![O:en,M:man]: (use(ada,O,M,t1) => (O = ben))", "![O:en,M:man]: (use(ben,O,M,t1) => (O = ada))"]
sc('fight_one_aggressor',
   "Ada and Ben grapple; each uses only the other's body, without consent. Exactly one is the aggressor.",
   DEF, FIGHT, 'sat', forced=["(aggresses(ada,ben,t1) <=> ~ aggresses(ben,ada,t1))"])
sc('fight_ada_started', "The same fight, with Ada as the aggressor: consistent.",
   DEF, FIGHT + ["aggresses(ada,ben,t1)"], 'sat', forced=["~ aggresses(ben,ada,t1)"])
sc('fight_ben_started', "The same fight, with Ben as the aggressor: also consistent. The theory does not decide.",
   DEF, FIGHT + ["aggresses(ben,ada,t1)"], 'sat', forced=["~ aggresses(ada,ben,t1)"])
sc('gift_refused',
   "Ada (full owner) grants Ben a title against Cy at t1, but Ben does not accept. Ben gets no title.",
   D3, KINDS + ORDER3 + HOMESTEAD_ADA + [
       "grants(ada,ben,field,cy,sow,t1)", "![R:en]: ~ accepts(ben,R,field,t1)",
       "![R:en,Q:en,M:man,T:tm]: ((T != t1) => ~ grants(R,ben,field,Q,M,T))"],
   'sat', forced=["~ owns(ben,field,cy,sow,t2)"])
sc('lease',
   "Ada homesteads the field at t0 and leases the manner 'sow' to Ben at t1; Ben accepts. At t2 Ben may "
   "sow and may exclude Ada and Cy from sowing; Ada keeps her titles in 'plow', including against Ben.",
   D3, KINDS + ORDER3 + HOMESTEAD_ADA + [
       "transfers_manner(ada,ben,field,sow,t1)", "accepts(ben,ada,field,t1)",
       "![P:en,Q:en,M:man,T:tm]: (disowns(P,field,Q,M,T) => ((P = ada) & (M = sow) & (T = t1)))",
       "![R:en,P:en,Q:en,M:man,T:tm]: (grants(R,P,field,Q,M,T) => ((R = ada) & (P = ben) & (M = sow) & (T = t1)))"],
   'sat', forced=["owns(ben,field,ada,sow,t2)", "owns(ben,field,cy,sow,t2)", "![Q:en]: ~ owns(ada,field,Q,sow,t2)",
                  "owns(ada,field,ben,plow,t2)", "may_use(ben,field,sow,t2)"])
EAS = _dom(P3 + ['field'], ['t0', 't1', 't2'], ['plow', 'walk'])
sc('easement',
   "Ada homesteads the field at t0 and at t1 releases Cy from 'walk' (a right of way). At t2 Cy may walk "
   "across without asking, but Ada may still forbid him to plow.",
   EAS, KINDS + ORDER3 + HOMESTEAD_ADA + [
       "disowns(ada,field,cy,walk,t1)",
       "![P:en,Q:en,M:man,T:tm]: (disowns(P,field,Q,M,T) => ((P = ada) & (Q = cy) & (M = walk) & (T = t1)))",
       "![R:en,P:en,Q:en,M:man,T:tm]: ~ grants(R,P,field,Q,M,T)"],
   'sat', forced=["may_use(cy,field,walk,t2)", "owns(ada,field,cy,plow,t2)",
                  "((~ consents(ada,field,cy,plow,t2) & ~ aggresses(ada,cy,t2)) => forbidden_use(cy,field,plow,t2))"])
sc('joint_homestead',
   "Ada plows and Ben sows the unowned field at t0; both claim it. From t1 both are full owners: co-owners.",
   D3, KINDS + ORDER3 + [
       "clash(field,plow,plow)", "use(ada,field,plow,t0)", "claim(ada,field,t0)",
       "use(ben,field,sow,t0)", "claim(ben,field,t0)", "unowned(field,t0)", "~ claim(cy,field,t0)",
       "![P:en,Q:en,M:man,T:tm]: ~ disowns(P,field,Q,M,T)",
       "![P:en,Q:en,R:en,M:man,T:tm]: ~ grants(P,Q,field,R,M,T)"],
   'sat', forced=["full_owner(ada,field,t1)", "full_owner(ben,field,t1)", "owns(ada,field,ben,sow,t2)",
                  "~ is_owner(cy,field,t2)"])
sc('lone_user_same_manner',
   "clash(field,plow,plow): one person plowing alone is possible.",
   D3, KINDS + ORDER3 + ["clash(field,plow,plow)", "use(ada,field,plow,t0)"], 'sat')
sc('rivals_same_manner',
   "clash(field,plow,plow): two persons cannot plow the field at once.",
   D3, KINDS + ORDER3 + ["clash(field,plow,plow)", "use(ada,field,plow,t0)", "use(ben,field,plow,t0)"],
   'unsat')
sc('ex_nihilo_title',
   "A title with no acquisition event behind it is impossible.",
   D3, KINDS + ORDER3 + [
       "owns(ada,field,ben,plow,t2)", "![P:en,Q:en,M:man,T:tm]: ~ acquires(P,field,Q,M,T)"],
   'unsat')
sc('idea_claim_inert',
   "Using and claiming a thing that is not scarce (a song) gives no title.",
   _dom(P3 + ['song'], ['t0', 't1', 't2'], ['sing', 'hum']),
   ["person(ada)", "person(ben)", "person(cy)", "np_obj(song)"] + ORDER3 + [
       "![M1:man,M2:man]: ~ clash(song,M1,M2)",
       "use(ada,song,sing,t0)", "claim(ada,song,t0)", "use(ben,song,sing,t0)"],
   'sat', forced=["~ is_owner(ada,song,t1)", "may_use(ben,song,sing,t1)"])
sc('double_spend_sequential',
   "Ada transfers the field to Ben at t1 and tries to transfer it to Cy at t2, with no new "
   "acquisition by Ada in between.",
   D4, KINDS + ORDER4 + [
       "vol_transfer(ada,ben,field,t1)", "vol_transfer(ada,cy,field,t2)",
       "![Q:en,M:man]: (~ acquires(ada,field,Q,M,t1) & ~ acquires(ada,field,Q,M,t2))"],
   'unsat')
sc('joint_purchase',
   "Ada homesteads the field at t0 and transfers it to Ben and to Cy at t1; both accept. From t2 Ben and "
   "Cy are co-owners (full owners both) and Ada holds no title.",
   D3, KINDS + ORDER3 + HOMESTEAD_ADA + [
       "vol_transfer(ada,ben,field,t1)", "vol_transfer(ada,cy,field,t1)",
       "accepts(ben,ada,field,t1)", "accepts(cy,ada,field,t1)",
       "![P:en,Q:en,M:man,T:tm]: ((P != ada) => ~ disowns(P,field,Q,M,T))",
       "![S:en,Q:en,M:man,T:tm]: ~ grants(S,ada,field,Q,M,T)"],
   'sat', forced=["full_owner(ben,field,t2)", "full_owner(cy,field,t2)", "~ is_owner(ada,field,t2)"])
sc('share_gift',
   "Ada homesteads the field at t0 and gives Ben a share at t1; Ben accepts. From t2 both are full "
   "owners: co-owners.",
   D3, KINDS + ORDER3 + HOMESTEAD_ADA + [
       "gives_share(ada,ben,field,t1)", "accepts(ben,ada,field,t1)",
       "![P:en,Q:en,M:man,T:tm]: ~ disowns(P,field,Q,M,T)"],
   'sat', forced=["full_owner(ada,field,t2)", "full_owner(ben,field,t2)", "owns(ben,field,cy,plow,t2)"])
sc('idleness_is_not_control',
   "The 'de facto owner' objection. Ada and Ben co-own the field and refuse each other every use. "
   "At t1 Ada wants the field idle (she wants no use) and Ben wants to plow: the field stays idle, "
   "so every want of Ada's is met. At t2 Ada wants to sow, and Ben still refuses.",
   D3, KINDS + ORDER3 + [
       CO_AB('t1'), CO_AB('t2'),
       "![M:man,T:tm]: (~ consents(ada,field,ben,M,T) & ~ consents(ben,field,ada,M,T))",
       "![M:man]: ~ wants(ada,field,M,t1)", "wants(ben,field,plow,t1)", "wants(ada,field,sow,t2)",
       "![P:en,M:man]: (~ use(P,field,M,t1) & ~ use(P,field,M,t2))"],
   'sat', forced=["~ controls(ada,field,t1)", "~ controls(ben,field,t1)", "unrealised(ben,field,plow,t1)",
                  "![M:man]: ~ unrealised(ada,field,M,t1)", "unrealised(ada,field,sow,t2)"])
sc('partial_abandonment',
   "Ada homesteads at t0, releases all her titles against Ben at t1 (partial titles), and abandons at t2. "
   "With no further events, the field is unowned at t3.",
   D4, KINDS + ORDER4 + [
       "clash(field,plow,plow)", "use(ada,field,plow,t0)", "claim(ada,field,t0)", "unowned(field,t0)",
       "![M:man]: disowns(ada,field,ben,M,t1)", "abandons(ada,field,t2)",
       "![P:en,Q:en,M:man,T:tm]: (disowns(P,field,Q,M,T) => (((Q = ben) & (T = t1)) | (T = t2)))",
       "![P:en,T:tm]: ((T != t0) => ~ claim(P,field,T))",
       "![P:en]: ((P != ada) => ~ claim(P,field,t0))",
       "![P:en,Q:en,R:en,M:man,T:tm]: ~ grants(P,Q,field,R,M,T)"],
   'sat', forced=["owns(ada,field,cy,plow,t2)", "~ owns(ada,field,ben,plow,t2)", "unowned(field,t3)"])
