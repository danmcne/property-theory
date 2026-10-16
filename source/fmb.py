"""Independent model finding with Vampire's finite model builder (fmb).

  A. full theory                                       -> expect a finite model
  B. full theory + co-ownership with mutual refusal,
     a clashing want, and no aggression anywhere       -> expect a finite model
  C. full theory + control axioms + co-ownership
     with a clashing want                              -> expect Unsatisfiable
  D. full theory + LiquidZulu's just-victor premise
     + co-ownership with mutual refusal                -> expect Unsatisfiable
  D. non-vacuity: for every theorem  ![X]: (H => C),  the full theory
     (plus its contrast axioms, if any) together with  ?[X]: H  has a finite
     model, so no theorem holds merely because its hypothesis is impossible.

For A and B, the model Vampire prints is parsed and every axiom and
definition is re-evaluated on it by tptp.evaluate (no trust in Vampire's
claim). For C, Vampire must refute the problem.
Writes results/fmb.json and models/*.model.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import theory  # noqa: E402
import tptp  # noqa: E402
from prove import DEFAULT_VAMPIRE  # noqa: E402

CO = ("?[A:en,B:en,O:en,T:tm]: (np_obj(O) & person(A) & person(B) & (A != B) "
      "& (![M:man]: (owns(A,O,B,M,T) & owns(B,O,A,M,T))) "
      "& (![M:man]: (~ consents(A,O,B,M,T) & ~ consents(B,O,A,M,T))) "
      "& ~ aggresses(A,B,T) & ~ aggresses(B,A,T) "
      "& wants(A,O,plow,T) & wants(B,O,sow,T) & clash(O,plow,sow))")
PEACE = "![P:en,Q:en,T:tm]: ~ aggresses(P,Q,T)"
DISTINCT = "(plow != sow)"

PROBLEMS = {
    'A_theory': ([], [], 'Satisfiable'),
    'B_co_ownership': ([], [DISTINCT, CO, PEACE], 'Satisfiable'),
    'C_control_co_ownership': (['control_use_liberty', 'control_protection'], [DISTINCT, CO], 'Unsatisfiable'),
    'D_direction_co_ownership': (['direction_exhaustive'], [DISTINCT, CO], 'Unsatisfiable'),
}


def build_problem(contrast, extra):
    items = [(a['name'], tptp.parse(a['text']), None) for a in theory.A]
    items += [(c['name'], tptp.parse(c['text']), 'CONTRAST') for c in theory.CONTRAST if c['name'] in contrast]
    items += [('extra_%d' % i, tptp.parse(x), None) for i, x in enumerate(extra)]
    consts = {'plow': 'man', 'sow': 'man'} if extra else {}
    return tptp.problem('tff', theory.SORTS, theory.SIG, consts, items)


def parse_model(out):
    dom = {s: [] for s in theory.SORTS}
    for s, e in re.findall(r"tff\(declare_(tm|en|man)\d+,type,(fmb_\w+):", out):
        dom[s].append(e)
    consts = dict(re.findall(r"tff\(\w+_definition,axiom,(\w+) = (fmb_\w+)\)", out))
    interp = {p: set() for p in theory.SIG}
    for name, body in re.findall(r"tff\(predicate_(\w+),axiom,(.*?)\)\.\s*\n", out, re.S):
        for neg, p, args in re.findall(r"(~?)(\w+)\(([^()]*)\)", body):
            if not neg:
                interp[p].add(tuple(a.strip() for a in args.split(',')))
    return dom, consts, interp


def check(dom, consts, interp, contrast, extra):
    """Re-evaluate every formula of the problem on Vampire's model."""
    def subst(f):  # replace named constants by their elements
        k = f[0]
        if k == 'atom':
            return ('atom', f[1], [('const', consts.get(t[1], t[1])) if t[0] == 'const' else t for t in f[2]])
        if k == 'eq':
            return ('eq',) + tuple(('const', consts.get(t[1], t[1])) if t[0] == 'const' else t for t in f[1:])
        if k in ('forall', 'exists'):
            return (k, f[1], subst(f[2]))
        if k == 'not':
            return ('not', subst(f[1]))
        if k in ('and', 'or'):
            return (k, [subst(g) for g in f[1]])
        if k in ('imp', 'iff'):
            return (k, subst(f[1]), subst(f[2]))
        return f
    res = {}
    for a in theory.A + [c for c in theory.CONTRAST if c['name'] in contrast]:
        res[a['name']] = tptp.evaluate(tptp.parse(a['text']), dom, interp)
    for i, x in enumerate(extra):
        res['extra_%d' % i] = tptp.evaluate(subst(tptp.parse(x)), dom, interp)
    return res


def nonvacuity():
    out, ok_all = {}, True
    for t in theory.TH:
        f = tptp.parse(t['text'])
        if not (f[0] == 'forall' and f[2][0] == 'imp'):
            out[t['name']] = 'n/a'
            continue
        hyp = ('exists', f[1], f[2][1])
        items = [(a['name'], tptp.parse(a['text']), None) for a in theory.A]
        items += [(c['name'], tptp.parse(c['text']), None) for c in theory.CONTRAST if c['name'] in t['contrast']]
        items.append(('hypothesis', hyp, 'hypothesis of ' + t['name']))
        path = os.path.join(ROOT, 'models', 'nonvacuity', t['name'] + '.p')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as fh:
            fh.write(tptp.problem('tff', theory.SORTS, theory.SIG, {}, items))
        out_txt = subprocess.run([DEFAULT_VAMPIRE, '-sa', 'fmb', '-t', '120', path],
                                 capture_output=True, text=True, timeout=300).stdout
        m = re.search(r"SZS status (\w+)", out_txt)
        status = m.group(1) if m else 'Unknown'
        verdict = status
        if status == 'Satisfiable':
            dom, _, interp = parse_model(out_txt)
            good = all(tptp.evaluate(tptp.parse(a['text']), dom, interp)
                       for a in theory.A + [c for c in theory.CONTRAST if c['name'] in t['contrast']])
            good = good and tptp.evaluate(hyp, dom, interp)
            verdict = 'sat (model re-checked)' if good else 'sat BUT RE-CHECK FAILED'
            ok_all &= good
        else:
            ok_all = False
        out[t['name']] = verdict
        print("  %-36s hypothesis: %s" % (t['name'], verdict))
    return out, ok_all


def main():
    os.makedirs(os.path.join(ROOT, 'models'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
    summary, ok_all = {}, True
    for name, (contrast, extra, expect) in PROBLEMS.items():
        path = os.path.join(ROOT, 'models', name + '.p')
        with open(path, 'w') as fh:
            fh.write(build_problem(contrast, extra))
        if expect == 'Satisfiable':
            cmd = [DEFAULT_VAMPIRE, '-sa', 'fmb', '-t', '120', path]
        else:
            cmd = [DEFAULT_VAMPIRE, '--mode', 'casc', '-t', '120', path]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
        m = re.search(r"SZS status (\w+)", out)
        status = m.group(1) if m else 'Unknown'
        entry = dict(status=status, expect=expect)
        if status == 'Satisfiable':
            with open(os.path.join(ROOT, 'models', name + '.model'), 'w') as fh:
                fh.write(out)
            dom, consts, interp = parse_model(out)
            res = check(dom, consts, interp, contrast, extra)
            entry['domain_sizes'] = {k: len(v) for k, v in dom.items()}
            entry['all_formulas_hold'] = all(res.values())
            entry['failing'] = [k for k, v in res.items() if not v]
        ok = status == expect and entry.get('all_formulas_hold', True)
        ok_all &= ok
        summary[name] = entry
        print("  %-26s %-14s (expect %s) %s %s" % (
            name, status, expect, entry.get('domain_sizes', ''),
            'OK' if ok else '<<< CHECK %s' % entry.get('failing', '')))
    print("non-vacuity of theorem hypotheses:")
    nv, nv_ok = nonvacuity()
    ok_all &= nv_ok
    summary['nonvacuity'] = nv
    json.dump(summary, open(os.path.join(ROOT, 'results', 'fmb.json'), 'w'), indent=1, sort_keys=True)
    print("VAMPIRE MODEL CHECKS PASS" if ok_all else "VAMPIRE MODEL CHECKS FAILED")
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
