"""Generate the documentation parts that must agree with the theory and the results.

  * README.md       — fills the GENERATED sections (axiom table, theorem table, status)
  * VERIFICATION.md — the full verification record, from results/*.json
  * docs/diagrams/title_dependencies.dot — lemma graph of the title family
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402
import theory  # noqa: E402

GROUP_TITLES = {
    'time': 'Time', 'entities': 'Persons and objects', 'typing': 'Who can do what',
    'persons': 'Persons', 'title': 'Titles', 'transfer': 'Grants, gifts, transfers and leases',
    'abandonment': 'Abandonment', 'ownership': 'Owners', 'use': 'Use, consent and easements',
    'scarcity': 'Scarcity', 'aggression': 'Action, aggression and defence', 'homesteading': 'Homesteading',
    'contrast': 'Contrasts: the control view and the direction view', 'control': 'Control',
    'coforms': 'Two forms of co-ownership: veto and free use',
}


def load(name):
    p = os.path.join(ROOT, 'results', name)
    return json.load(open(p)) if os.path.exists(p) else {}


def axiom_table():
    L = ["| # | Name | Kind | In plain words |", "|---|---|---|---|"]
    for i, a in enumerate(theory.A, 1):
        kind = a['kind'] + (' (derived, kept for clarity)' if a.get('derived') else '')
        L.append("| %d | `%s` | %s | %s |" % (i, a['name'], kind, a['gloss']))
    L += ["", "The contrast axioms below are not part of the theory. They state premises of the control view "
          "and the direction view, so that the checks can test their consequences.", "",
          "| Name | In plain words |", "|---|---|"]
    for c in theory.CONTRAST:
        L.append("| `%s` | %s |" % (c['name'], c['gloss']))
    return "\n".join(L)


def theorem_table(proofs):
    L = []
    group = None
    for t in theory.TH:
        if t['tag'] == 'lemma':
            continue
        if t['group'] != group:
            group = t['group']
            L += ["", "**%s**" % GROUP_TITLES.get(group, group), "",
                  "| Theorem | In plain words | Proved |", "|---|---|---|"]
        r = proofs.get(t['name'], {})
        ok = r.get('vampire') == 'Theorem' and r.get('leo3') == 'Theorem'
        star = ' ★' if t['tag'] == 'headline' else ''
        L.append("| `%s`%s | %s | %s |" % (t['name'], star, t['gloss'], 'both provers' if ok else 'NOT YET'))
    return "\n".join(L).strip()


def status(proofs, models, fmb, story):
    n = len(theory.TH)
    both = sum(1 for t in theory.TH if proofs.get(t['name'], {}).get('vampire') == 'Theorem'
               and proofs.get(t['name'], {}).get('leo3') == 'Theorem')
    sc = models.get('scenarios', {})
    nv = fmb.get('nonvacuity', {})
    nv_ok = sum(1 for v in nv.values() if str(v).startswith('sat (model re-checked)'))
    nv_n = sum(1 for v in nv.values() if v != 'n/a')
    n_ax = sum(1 for a in theory.A if a['kind'] == 'axiom')
    n_def = sum(1 for a in theory.A if a['kind'] == 'definition')
    rows = [
        ("Axioms and definitions", "%d axioms, %d definitions" % (n_ax, n_def)),
        ("Theorems proved by Vampire and by Leo-III (with E)", "%d of %d" % (both, n)),
        ("Axioms marked derived, proved from the axioms they name", "%d of %d" % (
            sum(1 for a in theory.A if a.get('derived') and proofs.get('derived_' + a['name'], {}).get('vampire') == 'Theorem'
                and proofs.get('derived_' + a['name'], {}).get('leo3') == 'Theorem'),
            sum(1 for a in theory.A if a.get('derived')))),
        ("Story world satisfies every axiom and definition",
         "%s (%d of %d)" % ('yes' if story.get('axioms') and all(story['axioms'].values()) else 'NO',
                            sum(story.get('axioms', {}).values()), len(story.get('axioms', {})))),
        ("Titles and wrongs in the story world are fixed by its history", 'yes' if story.get('uniqueness') == ['sat', 'unsat'] else 'NO'),
        ("Vampire finds a model of the theory, re-checked independently",
         'yes' if fmb.get('A_theory', {}).get('all_formulas_hold') else 'NO'),
        ("Vampire finds a model with co-ownership, mutual refusal and no aggression",
         'yes' if fmb.get('B_co_ownership', {}).get('all_formulas_hold') else 'NO'),
        ("Theory plus control view plus co-ownership has no model",
         'yes (Vampire: %s)' % fmb.get('C_control_co_ownership', {}).get('status', '?')),
        ("Theory plus direction view plus co-owners who refuse each other has no model",
         'yes (Vampire: %s)' % fmb.get('D_direction_co_ownership', {}).get('status', '?')),
        ("Scenarios with the expected outcome (Z3)", "%d of %d" % (sum(1 for v in sc.values() if v['ok']), len(sc))),
        ("Theorems whose hypothesis can be true (not vacuous)", "%d of %d" % (nv_ok, nv_n)),
    ]
    return "\n".join(["| Check | Outcome |", "|---|---|"] + ["| %s | %s |" % r for r in rows])


def fill(path, sections):
    text = open(path).read()
    for key, body in sections.items():
        pat = re.compile(r"(<!-- BEGIN GENERATED: %s -->\n).*?(<!-- END GENERATED: %s -->)" % (key, key), re.S)
        if not pat.search(text):
            raise ValueError("marker %s missing in %s" % (key, path))
        text = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)
    open(path, 'w').write(text)


def dependency_dot():
    names = ['life_cycle', 'res_nullius', 'no_double_spend', 'transferor_not_owner', 'transfer_is_abandonment',
             'abandoner_not_owner', 'disown_extinguishes', 'no_fresh_title', 'homesteader_owns', 'title_persists']
    axioms = ['title_acquired', 'title_genesis', 'acquires_def']
    th = {t['name']: t for t in theory.TH}
    L = ["// type: dependency", "// Generated by source/docs.py. An arrow A -> B means: the proof of A uses B.",
         "digraph title_dependencies {", "    rankdir=LR;", '    node [shape=box, fontname="Helvetica"];']
    kinds = {a['name']: a['kind'] for a in theory.A}
    for a in axioms:
        L.append('    %s [shape=box, style=rounded, label="%s\\n(%s)"];' % (a, a, kinds[a]))
    for n in names:
        for l in th[n]['lemmas']:
            if l in names:
                L.append("    %s -> %s;" % (n, l))
        for d in th[n]['deps']:
            if d in axioms:
                L.append("    %s -> %s;" % (n, d))
    L.append("}")
    with open(os.path.join(ROOT, 'docs', 'diagrams', 'title_dependencies.dot'), 'w') as fh:
        fh.write("\n".join(L) + "\n")


def verification_md(proofs, models, fmb, story):
    _, thms = build.load()
    L = ["# Verification record — v%s" % build.VERSION, "",
         "Generated by `source/docs.py` from `results/*.json`. Re-run `python3 verify.py` to refresh.", "",
         "## Summary", "", status(proofs, models, fmb, story), "",
         "## Method", "",
         "- **Single source.** `source/theory.py` holds every axiom, definition, theorem and scenario. "
         "`source/build.py` parses and type-checks each formula and generates every TPTP file. "
         "No formula is maintained by hand in two places.",
         "- **Entailment (unbounded domains).** Each theorem has a minimal problem that contains only the "
         "axioms, definitions and earlier theorems (lemmas) listed for it in `minimal/MANIFEST.md`. "
         "Vampire 5.1.0 proves the TFF version; Leo-III 1.7.18, with E 3.5.1 as its first-order back end, "
         "proves the THF version. A theorem counts as proved only if both report `SZS status Theorem`. "
         "The lemma graph is checked to be acyclic.",
         "- **Consistency.** Three independent routes: (1) the story world in `MODEL.md`, written by hand and "
         "evaluated against every formula by a plain-Python evaluator; (2) Vampire's finite model builder, "
         "whose models are parsed and re-evaluated by the same evaluator; (3) Z3 over a grounded finite domain.",
         "- **Scenarios (Z3).** Concrete situations with an expected outcome; a 'forced' conclusion is "
         "checked by asserting its negation and obtaining unsat. Unsat results hold for the stated finite "
         "domain; their general forms are theorems.",
         "- **Non-vacuity (Vampire fmb).** For each theorem `![X]: (H => C)`, the full theory plus `?[X]: H` "
         "has a finite model, re-checked by the evaluator. No theorem holds only because its hypothesis "
         "is impossible.", "",
         "## Theorems", "",
         "| Theorem | Tag | Vampire | Leo-III (+E) | Rests on (axioms and definitions, transitively) |",
         "|---|---|---|---|---|"]
    for t in theory.TH:
        r = proofs.get(t['name'], {})
        L.append("| `%s` | %s | %s | %s | %s |" % (
            t['name'], t['tag'], r.get('vampire', '—'), r.get('leo3', '—'),
            ", ".join(sorted(build.closure(t['name'], thms)))))
    L += ["", "## Scenarios (Z3, finite domain)", "", "| Scenario | Expected | Outcome | Forced conclusions |",
          "|---|---|---|---|"]
    for s in theory.SC:
        r = models.get('scenarios', {}).get(s['name'], {})
        forced = "; ".join("`%s` %s" % (k, 'forced' if v else 'NOT forced') for k, v in r.get('forced', {}).items())
        L.append("| `%s`: %s | %s | %s | %s |" % (s['name'], s['gloss'], s['expect'], r.get('result', '—'), forced or '—'))
    L += ["", "## Models found by Vampire (re-checked)", "", "| Problem | Status | Domain sizes | All formulas hold |",
          "|---|---|---|---|"]
    for k in ('A_theory', 'B_co_ownership', 'C_control_co_ownership', 'D_direction_co_ownership'):
        r = fmb.get(k, {})
        L.append("| `models/%s.p` | %s | %s | %s |" % (k, r.get('status', '—'), r.get('domain_sizes', '—'),
                                                       r.get('all_formulas_hold', 'n/a (refuted)')))
    L += ["", "## Non-vacuity of theorem hypotheses (Vampire fmb, re-checked)", "",
          "| Theorem | Hypothesis |", "|---|---|"]
    for k, v in fmb.get('nonvacuity', {}).items():
        L.append("| `%s` | %s |" % (k, v if v != 'n/a' else 'n/a (not of the form H => C)'))
    alone = load('proofs_leo_alone.json')
    if alone:
        fails = [t['name'] for t in theory.TH if alone.get(t['name'], {}).get('leo3') != 'Theorem']
        leo_line = ("- Leo-III alone (no E back end, 120 s per problem) proves %d of the %d theorems%s"
                    % (len(theory.TH) - len(fails), len(theory.TH),
                       "; it does not finish on " + ", ".join("`%s`" % f for f in fails) + "." if fails else "."))
    else:
        leo_line = "- Leo-III alone (no E back end) was not run for this record."
    L += ["", "## Known limits of the verification", "", leo_line,
          "- Finite model checks prove satisfiability outright. They do not prove that the theory has models "
          "with infinitely many instants. Over a time order with no first instant (for example the integers) "
          "and a person who uses and claims an object at every instant, the title axioms have no model; "
          "see THEORY.md, 'Time'.",
          "- The compossibility argument in THEORY.md is a proof sketch, not a machine-checked theorem.", ""]
    with open(os.path.join(ROOT, 'VERIFICATION.md'), 'w') as fh:
        fh.write("\n".join(L))


def main():
    proofs, models, fmb, story = load('proofs.json'), load('models.json'), load('fmb.json'), load('story.json')
    fill(os.path.join(ROOT, 'README.md'), {
        'axioms': axiom_table(),
        'theorems': theorem_table(proofs),
        'status': status(proofs, models, fmb, story),
    })
    verification_md(proofs, models, fmb, story)
    dependency_dot()
    print("docs regenerated")


if __name__ == '__main__':
    main()
