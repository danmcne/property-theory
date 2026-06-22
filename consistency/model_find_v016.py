"""
v0.16 finite-model search (Z3).

v0.16 adds ONE axiom to v0.15: a definition of `abandons`, which packages
"relinquish ownership against EVERY other party" into a single predicate.
This is the move that lets us cross from the relational `disowns` (which
extinguishes one P-vs-Q claim at a time) to the global `unowned` (no owner
against anyone).

A `sat` result here is the consistency witness we cite in the docs: the whole
axiom set, including the new definition, has a finite model
(|Entity|=3, |Time|=3, |Manner|=2). Run: `python3 consistency/model_find_v016.py`.
"""
from z3 import *
# Pull in the entire v0.15 axiom set unchanged (sorts, predicates, axioms in `ax`).
import importlib.util, os
_spec = importlib.util.spec_from_file_location(
    "v015", os.path.join(os.path.dirname(__file__), "_v015_axioms.py"))
v015 = importlib.util.module_from_spec(_spec)
# Execute only the definitions block (everything before the __main__ guard).
exec(open(_spec.origin).read().split('if __name__')[0], v015.__dict__)

# Bring the names we need into scope.
Entity, Time, Manner = v015.Entity, v015.Time, v015.Manner
p1, p2, obj1 = v015.p1, v015.p2, v015.obj1
t0, t1, t2 = v015.t0, v015.t1, v015.t2
person, np_obj, owns, is_owner = v015.person, v015.np_obj, v015.owns, v015.is_owner
disowns, unowned = v015.disowns, v015.unowned
E, FA = v015.E, v015.FA
B = BoolSort()
ax = list(v015.ax)   # copy so we can extend

# NEW predicate + defining axiom -----------------------------------------------
# abandons(P,O,T): owner P relinquishes O against every other person at T.
abandons = Function('abandons', Entity, Entity, Time, B)
# abandons(P,O,T) <=> O is an object, P currently owns it, and P disowns it
# against every other person Q. (Disowning against ALL parties is exactly what
# makes a sole owner's title vanish globally -> the object can become unowned.)
ax += [FA([Entity, Entity, Time], lambda P, O, T:
          abandons(P, O, T) == And(
              np_obj(O),
              is_owner(P, O, T),
              And([Implies(And(person(Q), Q != P), disowns(P, O, Q, T)) for Q in E])))]

# Re-export for scenario script.
abandons_fn = abandons

if __name__ == '__main__':
    s = Solver(); s.set('mbqi', True); s.add(ax)
    print("full v0.16 axiom set (v0.15 + abandons_def):", s.check())
