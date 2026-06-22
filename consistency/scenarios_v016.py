"""
v0.16 scenario / non-vacuity checks for abandonment -> res nullius.

For each new theorem we assert its ANTECEDENT with the full axiom set and check
`sat`: a satisfiable antecedent shows the theorem is non-vacuous. We also
exhibit a model in which the abandoned object actually becomes unowned.
"""
from z3 import *
import importlib.util, os

# Load the v0.16 model module cleanly (its __main__ guard suppresses the check).
spec = importlib.util.spec_from_file_location(
    "m016", os.path.join(os.path.dirname(__file__), "model_find_v016.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ax = m.ax
p1, p2, obj1, t0, t1 = m.p1, m.p2, m.obj1, m.t0, m.t1
person, np_obj = m.person, m.np_obj
owns, is_owner, unowned, disowns = m.owns, m.is_owner, m.unowned, m.disowns
abandons = m.abandons
before, reacquires = m.v015.before, m.v015.reacq
E = m.E

def run(extra, label):
    s = Solver(); s.set('mbqi', True); s.add(ax); s.add(extra)
    r = s.check(); print("[%s] %s" % (r, label)); return s, r

# --- res nullius witness -----------------------------------------------------
# p1 owns obj1 against p2 (p2 is the only other person, so p1 is the sole owner);
# p1 disowns against p2 at t0 (=> abandons by abandons_def); never re-acquires;
# no third party holds obj1 at t1. Expected: obj1 becomes unowned at t1.
scenario = [
    person(p1), person(p2), np_obj(obj1), p1 != p2,
    owns(p1, obj1, p2, t0),                 # p1's only-possible ownership relation
    before(t0, t1),
    disowns(p1, obj1, p2, t0),              # relinquish against the only other party
    Not(reacquires(p1, obj1, p2, t0, t1)),  # and do not take it back
    Not(is_owner(p2, obj1, t1)),            # nobody else holds it at t1
]
s, r = run(scenario, "sole owner abandons -> antecedent satisfiable (non-vacuous)")
if r == sat:
    mdl = s.model(); bi = lambda x: is_true(mdl.eval(x))
    print("   abandons(p1,obj1,t0) holds?      ", bi(abandons(p1, obj1, t0)))
    print("   is_owner(p1,obj1,t1)?            ", bi(is_owner(p1, obj1, t1)), "  (False => title extinguished)")
    print("   unowned(obj1,t1) -> res nullius? ", bi(unowned(obj1, t1)))

# --- non-vacuity of abandoner_not_owner --------------------------------------
run([np_obj(obj1), before(t0, t1), abandons(p1, obj1, t0),
     And([Not(reacquires(p1, obj1, Q, t0, t1)) for Q in E])],
    "abandoner_not_owner antecedent satisfiable")
