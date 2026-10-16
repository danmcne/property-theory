"""Finite model checks with Z3 (propositional grounding over a finite domain).

  1. consistency  — the full theory has a model in which titles, transfers,
                    abandonment and co-ownership all occur (not a trivial
                    empty model);
  2. scenarios    — each scenario in theory.SC is sat/unsat as expected, and
                    its 'forced' conclusions hold in EVERY model;
(Non-vacuity of the theorems is checked in fmb.py, with Vampire's finite
model builder, which handles the existential witnesses directly.)

Finite checks can establish satisfiability (a model exists) outright.
'unsat' and 'forced' results hold for the stated finite domain only; their
general versions are theorems proved by Leo-III and Vampire.
Writes results/models.json.
"""
import json
import os
import sys
import time

import z3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402
import theory  # noqa: E402
import tptp  # noqa: E402


_CACHE = {}


def solver_for(dom, formulas, key=None):
    """Ground `formulas` over `dom`. With a key, the grounded solver is cached
    and callers must push()/pop() around their own additions."""
    if key is not None and key in _CACHE:
        return _CACHE[key]
    g = tptp.Grounder(dom)
    s = z3.Solver()
    for f in formulas:
        s.add(g.g(f))
    if key is not None:
        _CACHE[key] = (s, g)
    return s, g


def theory_asts(contrast=()):
    out = [tptp.parse(a['text']) for a in theory.A]
    for c in theory.CONTRAST:
        if c['name'] in contrast:
            out.append(tptp.parse(c['text']))
    return out


def check_consistency():
    """A non-trivial model of the full theory: some object is homesteaded
    jointly (co-ownership), later transferred and abandoned."""
    dom = {'en': ['a', 'b', 'c', 'o'], 'tm': ['t0', 't1', 't2', 't3', 't4'], 'man': ['m1', 'm2']}
    rich = [tptp.parse(x) for x in [
        "owns(a,o,b,t1)", "owns(b,o,a,t1)",           # co-ownership
        "?[P:en,Q:en,T:tm]: vol_transfer(P,Q,o,T)",   # a transfer happens
        "?[P:en,T:tm]: abandons(P,o,T)",              # an abandonment happens
        "?[P:en,Q:en,T:tm]: aggresses(P,Q,T)",        # a wrong happens
    ]]
    s, _ = solver_for(dom, theory_asts() + rich)
    r = str(s.check())
    return dict(domain={k: len(v) for k, v in dom.items()}, result=r)


def check_scenarios():
    out = {}
    for sc in theory.SC:
        facts = [tptp.parse(f) for f in sc['facts']]
        consts = {}
        for s, names in sc['dom'].items():
            for n in names:
                consts[n] = s
        for f in facts:
            tptp.typecheck(f, theory.SIG, consts, where=sc['name'])
        key = (repr(sorted(sc['dom'].items())), tuple(sc['contrast']))
        s, g = solver_for(sc['dom'], theory_asts(sc['contrast']), key)
        s.push()
        for f in facts:
            s.add(g.g(f))
        r = str(s.check())
        entry = dict(result=r, expect=sc['expect'], ok=(r == sc['expect']), forced={})
        if r == 'sat':
            for fx in sc['forced']:
                fa = tptp.parse(fx)
                tptp.typecheck(fa, theory.SIG, consts, where=sc['name'])
                s.push()
                s.add(z3.Not(g.g(fa)))
                rr = str(s.check())
                s.pop()
                entry['forced'][fx] = (rr == 'unsat')
                entry['ok'] = entry['ok'] and rr == 'unsat'
        s.pop()
        out[sc['name']] = entry
        flag = 'OK' if entry['ok'] else '<<< CHECK'
        print("  %-36s %-6s (expect %-5s) forced %d/%d  %s" % (
            sc['name'], r, sc['expect'], sum(entry['forced'].values()), len(sc['forced']), flag))
    return out


def main():
    _, thms = build.main()
    res = {}
    t0 = time.time()
    print("consistency (full theory, non-trivial model):")
    res['consistency'] = check_consistency()
    print("  ", res['consistency'])
    print("scenarios:")
    res['scenarios'] = check_scenarios()
    res['seconds'] = round(time.time() - t0, 1)
    os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
    json.dump(res, open(os.path.join(ROOT, 'results', 'models.json'), 'w'), indent=1, sort_keys=True)
    bad = (res['consistency']['result'] != 'sat'
           or not all(v['ok'] for v in res['scenarios'].values()))
    print("\nALL MODEL CHECKS PASS" if not bad else "\nSOME MODEL CHECKS FAILED")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
