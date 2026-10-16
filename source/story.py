"""An explicit model: a small world with a history, checked against every axiom.

The PRIMITIVE facts (who uses, claims, consents, grants, accepts and releases
what and when) are written down by hand below. Every DEFINED predicate, and
the title relation `owns`, is then computed in plain Python from its
intended meaning (not from the TPTP text). Finally every axiom and
definition of the theory, parsed from theory.py, is evaluated on the
resulting structure by tptp.evaluate — a direct check that involves no
solver at all.

A second, independent check (Z3) confirms that once the primitive facts are
fixed, the axioms leave NO freedom in `owns` or in who aggresses against
whom: titles and wrongs in this world are uniquely determined by its history.

Writes MODEL.md and results/story.json.
"""
import json
import os
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import theory  # noqa: E402
import tptp  # noqa: E402

PERSONS = ['ada', 'ben', 'cy']
OBJECTS = ['field', 'song']
EN = PERSONS + OBJECTS
TM = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
MAN = ['plow', 'sow', 'walk', 'sing', 'hold']
DOM = {'en': EN, 'tm': TM, 'man': MAN}
IDX = {t: i for i, t in enumerate(TM)}

# ---------------------------------------------------------------------------
# The history (primitive facts). Everything not listed is false.
# ---------------------------------------------------------------------------
STORY = [
    ('t0', "The field is unowned. Ada plows it and Ben sows it; both claim it (joint homestead). "
           "All three sing a song; Cy claims the song."),
    ('t1', "Ada and Ben are co-owners. Ben lets Ada plow; Ada does not let Ben plow, and Ben wants to. "
           "Both let Cy walk across the field, and Cy does."),
    ('t2', "Cy walks across again; Ben consents, Ada does not (a trespass against Ada). Ada pushes Cy off "
           "(she uses his body without his consent). Ben transfers his share of the field to Cy, who accepts."),
    ('t3', "Ada and Cy are co-owners. Ada abandons the field."),
    ('t4', "Cy is the only owner. Cy abandons the field."),
    ('t5', "The field is unowned again. Ada plows it and claims it (re-homestead)."),
    ('t6', "Ada is the only owner. She sells the field to Ben and Cy together (a joint purchase); both accept."),
    ('t7', "Ben and Cy are co-owners. Together they lease the manner 'sow' to Ada, who accepts."),
    ('t8', "Ada holds the titles in 'sow'; Ben and Cy keep their titles in every other manner."),
]

ALL_M = MAN


def _transfer(r, p, o, t, held_against):
    """Grants and releases of a full transfer from r to p: p gets r's titles against each person
    in held_against (other than p) and a title against r, in every manner; r releases all."""
    g = {(r, p, o, q, m, t) for q in held_against if q != p for m in ALL_M}
    g |= {(r, p, o, r, m, t) for m in ALL_M}
    d = {(r, o, q, m, t) for q in held_against for m in ALL_M}
    return g, d


g_ben_cy, d_ben = _transfer('ben', 'cy', 'field', 't2', ['ada', 'cy'])
g_ada_ben, d_ada6 = _transfer('ada', 'ben', 'field', 't6', ['ben', 'cy'])
g_ada_cy, _ = _transfer('ada', 'cy', 'field', 't6', ['ben', 'cy'])
# the lease at t7: Ben and Cy each transfer the manner 'sow' to Ada
g_lease = {('ben', 'ada', 'field', 'ben', 'sow', 't7'), ('ben', 'ada', 'field', 'cy', 'sow', 't7'),
           ('cy', 'ada', 'field', 'cy', 'sow', 't7'), ('cy', 'ada', 'field', 'ben', 'sow', 't7')}
d_lease = {('ben', 'field', 'ada', 'sow', 't7'), ('ben', 'field', 'cy', 'sow', 't7'),
           ('cy', 'field', 'ada', 'sow', 't7'), ('cy', 'field', 'ben', 'sow', 't7')}

PRIM = {
    'person': {(p,) for p in PERSONS},
    'np_obj': {(o,) for o in OBJECTS},
    'before': {(a, b) for a in TM for b in TM if IDX[a] < IDX[b]},
    # two people cannot plow (or sow) the same field at once; two people cannot
    # both hold the same body. The song has no clashing uses.
    'clash': {('field', 'plow', 'plow'), ('field', 'sow', 'sow')} | {(p, 'hold', 'hold') for p in PERSONS},
    'use': {('ada', 'field', 'plow', 't0'), ('ben', 'field', 'sow', 't0'),
            ('ada', 'song', 'sing', 't0'), ('ben', 'song', 'sing', 't0'), ('cy', 'song', 'sing', 't0'),
            ('ada', 'field', 'plow', 't1'), ('cy', 'field', 'walk', 't1'),
            ('cy', 'field', 'walk', 't2'), ('ada', 'cy', 'hold', 't2'),
            ('ada', 'field', 'plow', 't5')},
    'claim': {('ada', 'field', 't0'), ('ben', 'field', 't0'), ('cy', 'song', 't0'), ('ada', 'field', 't5')},
    'wants': {('ben', 'field', 'plow', 't1'), ('ada', 'field', 'plow', 't1')},
    'consents': {('ben', 'field', 'ada', 'plow', 't1'),
                 ('ada', 'field', 'cy', 'walk', 't1'), ('ben', 'field', 'cy', 'walk', 't1'),
                 ('ben', 'field', 'cy', 'walk', 't2')},
    'grants': g_ben_cy | g_ada_ben | g_ada_cy | g_lease,
    'accepts': {('cy', 'ben', 'field', 't2'), ('ben', 'ada', 'field', 't6'), ('cy', 'ada', 'field', 't6'),
                ('ada', 'ben', 'field', 't7'), ('ada', 'cy', 'field', 't7')},
    'disowns': d_ben | d_ada6 | d_lease
               | {('ada', 'field', q, m, 't3') for q in ['ben', 'cy'] for m in ALL_M}     # Ada abandons
               | {('cy', 'field', q, m, 't4') for q in ['ada', 'ben'] for m in ALL_M},    # Cy abandons
}


def compute():
    """Compute owns, the wrongs, and every defined predicate from its intended meaning."""
    I = {k: set(v) for k, v in PRIM.items()}
    use, claim, dis, gr, acc, cons = (I['use'], I['claim'], I['disowns'], I['grants'], I['accepts'],
                                      I['consents'])
    rival = {(o,) for o in EN if any(c[0] == o for c in I['clash'])}
    owns = {(p, p, q, m, t) for p, q, m, t in product(PERSONS, PERSONS, MAN, TM) if p != q}

    def holder(p, o, t):
        return any((p, o, q, m, t) in owns for q in EN for m in MAN)

    def unowned_at(o, t):
        return not any(holder(p, o, t) for p in EN)

    def acquires_at(p, o, q, m, t):
        homestead = ((o,) in rival and (p, o, t) in claim and unowned_at(o, t)
                     and any((p, o, m2, t) in use for m2 in MAN))
        grant = any((r, p, o, q, m, t) in gr and (p, r, o, t) in acc and ((r, o, q, m, t) in owns or q == r)
                    for r in EN)
        return homestead or grant

    acq = set()
    for t in TM:   # each instant depends only on earlier ones
        for p, o, q, m in product(PERSONS, OBJECTS, PERSONS, MAN):
            if p == q:
                continue
            for t1 in TM[:IDX[t]]:
                released = any((p, o, q, m, tt) in dis for tt in TM[IDX[t1]:IDX[t]])
                if (p, o, q, m, t1) in acq and not released:
                    owns.add((p, o, q, m, t))
                    break
        for p, o, q, m in product(EN, EN, EN, MAN):
            if acquires_at(p, o, q, m, t):
                acq.add((p, o, q, m, t))

    # wrongs: aggresses_in and forfeits are defined in terms of each other; solve per instant
    # by checking every assignment to the candidate aggressions, and insist on a unique solution.
    cand = [(p, q, m, o, t) for p, q, m, o, t in product(EN, EN, MAN, EN, TM)
            if (p, o, m, t) in use and (q, o, p, m, t) in owns and (q, o, p, m, t) not in cons]
    agg_in = set()
    for t in TM:
        keys = sorted({(p, q, m) for p, q, m, o, tt in cand if tt == t})
        sols = []
        for bits in product([False, True], repeat=len(keys)):
            A = {k for k, b in zip(keys, bits) if b}

            def forfeits(r, o, q):
                return any((r, q, m) in A and (o == r or (r, o, m, t) in use) for m in MAN)
            ok = all(((p, q, m) in A) == any(not forfeits(q, o, p)
                                             for pp, qq, mm, o, tt in cand
                                             if (pp, qq, mm, tt) == (p, q, m, t))
                     for p, q, m in keys)
            if ok:
                sols.append(A)
        if len(sols) != 1:
            raise ValueError("instant %s: %d solutions for who aggresses" % (t, len(sols)))
        agg_in |= {(p, q, m, t) for p, q, m in sols[0]}
    forf = {(r, o, q, t) for r, o, q, t in product(EN, EN, EN, TM)
            if any((r, q, m, t) in agg_in and (o == r or (r, o, m, t) in use) for m in MAN)}

    I['owns'] = owns
    I['acquires'] = acq
    I['rivalrous'] = rival
    I['aggresses_in'] = agg_in
    I['aggresses'] = {(p, q, t) for p, q, m, t in agg_in}
    I['forfeits'] = forf
    I['is_owner'] = {(p, o, t) for p, o, t in product(EN, EN, TM) if holder(p, o, t)}
    I['full_owner'] = {(p, o, t) for p, o, t in product(EN, EN, TM)
                       if all((p, o, q, m, t) in owns for q in PERSONS for m in MAN if q != p)}
    I['unowned'] = {(o, t) for o, t in product(EN, TM) if unowned_at(o, t)}
    I['nodis_upto'] = {(p, o, q, m, a, b) for p, o, q, m, a, b in product(EN, EN, EN, MAN, TM, TM)
                       if not any((p, o, q, m, tt) in dis for tt in TM if IDX[a] <= IDX[tt] < IDX[b])}
    I['abandons'] = {(p, o, t) for p, o, t in product(EN, EN, TM)
                     if o in OBJECTS and holder(p, o, t)
                     and all((p, o, q, m, t) in dis for q in EN for m in MAN if (p, o, q, m, t) in owns)}
    I['shares'] = {(r, p, o, m, t) for r, p, o, m, t in product(EN, EN, EN, MAN, TM)
                   if (r, p, o, r, m, t) in gr
                   and all((r, p, o, q, m, t) in gr for q in EN if (r, o, q, m, t) in owns and q != p)}
    I['gives_share'] = {(r, p, o, t) for r, p, o, t in product(EN, EN, EN, TM)
                        if all((r, p, o, m, t) in I['shares'] for m in MAN)}
    I['transfers_manner'] = {(r, p, o, m, t) for (r, p, o, m, t) in I['shares']
                             if all((r, o, q, m, t) in dis for q in EN if (r, o, q, m, t) in owns)}
    I['vol_transfer'] = {x for x in I['gives_share'] if (x[0], x[2], x[3]) in I['abandons']}
    I['may_use'] = {(q, o, m, t) for q, o, m, t in product(EN, EN, MAN, TM)
                    if all((r, o, q, m, t) in cons for r in EN
                           if (r, o, q, m, t) in owns and (r, o, q, t) not in forf)}
    I['forbidden_use'] = {x for x in product(EN, EN, MAN, TM) if x not in I['may_use']}
    I['unrealised'] = {(p, o, m, t) for (p, o, m, t) in I['wants'] if (p, o, m, t) not in use}
    I['controls'] = {(p, o, t) for p, o, t in product(EN, EN, TM)
                     if all((p, o, m, t) in I['may_use'] for m in MAN)
                     and all(((q, o, m, t) in I['may_use']) == ((p, o, q, m, t) in cons)
                             for q in PERSONS for m in MAN if q != p)}
    I['permissible'] = {(p, m, t) for p, m, t in product(EN, MAN, TM)
                        if all((p, o, m, t) in I['may_use'] for o in EN if (p, o, m, t) in use)}
    return I


def evaluate_all(I):
    res = {}
    for a in theory.A:
        f = tptp.parse(a['text'])
        ok = tptp.evaluate(f, DOM, I)
        res[a['name']] = ok
        if not ok:
            print("  FAILS:", a['name'], tptp.counterexample(f, DOM, I))
    thm = {}
    for t in theory.TH:
        if t['contrast']:
            continue
        thm[t['name']] = tptp.evaluate(tptp.parse(t['text']), DOM, I)
        if not thm[t['name']]:
            print("  THEOREM FAILS:", t['name'])
    return res, thm


def uniqueness(I):
    """Z3: primitives fixed (closed world) => titles and wrongs are forced to the computed sets."""
    import z3
    g = tptp.Grounder(DOM)
    s = z3.Solver()
    for a in theory.A:
        s.add(g.g(tptp.parse(a['text'])))
    prim_preds = ['person', 'np_obj', 'before', 'clash', 'use', 'claim', 'wants', 'consents',
                  'grants', 'accepts', 'disowns']
    for p in prim_preds:
        for args in product(*[DOM[s_] for s_ in theory.SIG[p]]):
            atom = g.atom(p, list(args))
            s.add(atom if args in I[p] else z3.Not(atom))
    r1 = str(s.check())
    differs = [g.atom('owns', list(args)) != z3.BoolVal(args in I['owns'])
               for args in product(EN, EN, EN, MAN, TM)]
    differs += [g.atom('aggresses', list(args)) != z3.BoolVal(args in I['aggresses'])
                for args in product(EN, EN, TM)]
    s.add(z3.Or(differs))
    r2 = str(s.check())
    return r1, r2


def _cell(I, p, t):
    parts = []
    for q in PERSONS:
        ms = [m for m in MAN if (p, 'field', q, m, t) in I['owns']]
        if not ms:
            continue
        parts.append(q if len(ms) == len(MAN) else "%s (%s)" % (q, ", ".join(ms)))
    return ", ".join(parts) if parts else "—"


def table(I):
    rows = []
    for t in TM:
        cells = [_cell(I, p, t) for p in PERSONS]
        full = [p for p in PERSONS if (p, 'field', t) in I['full_owner']]
        holders = [p for p in PERSONS if (p, 'field', t) in I['is_owner']]
        if not holders:
            state = 'unowned'
        elif len(full) >= 2:
            state = 'co-owned'
        elif len(full) == 1 and holders == full:
            state = 'one full owner'
        else:
            state = 'titles divided by manner (lease)'
        ctrl = [p.capitalize() for p in PERSONS if (p, 'field', t) in I['controls']]
        rows.append((t, cells, state, ", ".join(ctrl) if ctrl else "nobody"))
    return rows


def write_markdown(I, ax_res, th_res, uniq):
    yes = lambda b: 'yes' if b else 'no'
    L = ["# A model of the theory: the story of a field",
         "",
         "This file is generated by `source/story.py`. It describes one finite world and its history.",
         "A script checks this world against every axiom and definition of the theory. The world",
         "satisfies all of them, so the theory is consistent. This world also contains co-ownership,",
         "a lease and an act of defence, so these are consistent with the theory.",
         "",
         "## The world",
         "",
         "- Persons: Ada, Ben, Cy.",
         "- Objects: a field (scarce) and a song (not scarce).",
         "- Instants: t0 to t8, in this order.",
         "- Manners (ways of using things): plow, sow, walk, sing, hold.",
         "- Physical facts (clashes): two persons cannot plow the field at the same instant; two persons",
         "  cannot sow it at the same instant; two persons cannot hold the same body. The song has no clashes.",
         "",
         "## The history",
         "",
         "| Instant | What happens |",
         "|---|---|"]
    for t, txt in STORY:
        L.append("| %s | %s |" % (t, txt))
    L += ["", "## Titles that follow from the history", "",
          "Each cell lists the persons whom that person may exclude from the field at that instant. A name",
          "alone means \"in every manner\"; otherwise the manners are listed. Nobody wrote these titles down:",
          "a program computed them from the history, and a solver confirms that the axioms allow no other",
          "titles and no other wrongs for this history (%s)." % (
              "confirmed" if uniq == ('sat', 'unsat') else "NOT CONFIRMED: %s" % (uniq,)),
          "",
          "The last column names who controls the field: who may use it in every manner, while every other",
          "person may use it exactly when he or she consents.",
          "",
          "| Instant | Ada may exclude | Ben may exclude | Cy may exclude | State of the field | Controls |",
          "|---|---|---|---|---|---|"]
    for t, cells, state, ctrl in table(I):
        L.append("| %s | %s | %s | %s | %s | %s |" % (t, cells[0], cells[1], cells[2], state, ctrl))
    agg = sorted(I['aggresses'], key=lambda x: IDX[x[2]])
    rows = table(I)
    L += ["", "## Permissions and wrongs that follow", "",
          "- At t1, Ada may plow (Ben consents). Ben may not plow (Ada refuses), and his want to plow is",
          "  unrealised: %s." % yes(('ben', 'field', 'plow', 't1') in I['unrealised']),
          "- At t1, Cy holds no title over the field but may walk on it: %s." % yes(
              ('cy', 'field', 'walk', 't1') in I['may_use']),
          "- Aggression events in the whole history: %s." % (
              ", ".join("%s against %s at %s" % (p.capitalize(), q.capitalize(), t) for p, q, t in agg) or "none"),
          "- At t2 Ada pushes Cy off the field without his consent. This is not aggression, because Cy is",
          "  aggressing against her at that instant: Ada aggresses against Cy at t2? %s. Cy forfeits his"
          % yes(('ada', 'cy', 't2') in I['aggresses']),
          "  title over his body with respect to Ada at t2? %s." % yes(('cy', 'cy', 'ada', 't2') in I['forfeits']),
          "- Cy's claim on the song gives no title: is Cy ever a holder of titles over the song? %s." % yes(
              any(('cy', 'song', t) in I['is_owner'] for t in TM)),
          "- After the double abandonment the field is unowned at t5 (%s), and Ada, a former owner, can"
          % yes(('field', 't5') in I['unowned']),
          "  homestead it again.",
          "- Ben's act at t2 is a transfer in the defined sense: %s. Ada's sale at t6 is two transfers at"
          % yes(('ben', 'cy', 'field', 't2') in I['vol_transfer']),
          "  one instant, to Ben and to Cy: %s." % yes(
              {('ada', 'ben', 'field', 't6'), ('ada', 'cy', 'field', 't6')} <= I['vol_transfer']),
          "- The lease at t7 is a transfer of the manner 'sow' by each co-owner: %s. At t8 Ada may sow"
          % yes({('ben', 'ada', 'field', 'sow', 't7'), ('cy', 'ada', 'field', 'sow', 't7')} <= I['transfers_manner']),
          "  without asking (%s), and Ben may sow only with Ada's consent (%s)." % (
              yes(('ada', 'field', 'sow', 't8') in I['may_use']),
              yes(('ben', 'field', 'sow', 't8') in I['forbidden_use'])),
          "- Nobody controls the field at an instant when it is co-owned: %s." % yes(
              not any((p, 'field', t) in I['controls'] for t, _, st, _c in rows if st == 'co-owned' for p in PERSONS)),
          "", "## Check results", "",
          "| Item | Holds in this world |", "|---|---|"]
    for a in theory.A:
        L.append("| %s `%s` | %s |" % (a['kind'], a['name'], 'yes' if ax_res[a['name']] else '**NO**'))
    L += ["", "Every theorem that does not need a contrast axiom also holds in this world: %s of %s."
          % (sum(th_res.values()), len(th_res)), ""]
    with open(os.path.join(ROOT, 'MODEL.md'), 'w') as fh:
        fh.write("\n".join(L))


def main():
    I = compute()
    ax_res, th_res = evaluate_all(I)
    print("story model: %d/%d axioms and definitions hold; %d/%d theorems hold"
          % (sum(ax_res.values()), len(ax_res), sum(th_res.values()), len(th_res)))
    uniq = uniqueness(I)
    print("Z3: primitives fixed -> %s; titles or wrongs differing from the computed ones -> %s" % uniq)
    write_markdown(I, ax_res, th_res, uniq)
    os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
    json.dump(dict(axioms=ax_res, theorems=th_res, uniqueness=uniq,
                   aggression=sorted(I['aggresses'])),
              open(os.path.join(ROOT, 'results', 'story.json'), 'w'), indent=1, sort_keys=True)
    ok = all(ax_res.values()) and all(th_res.values()) and uniq == ('sat', 'unsat')
    print("STORY MODEL OK" if ok else "STORY MODEL FAILED")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
