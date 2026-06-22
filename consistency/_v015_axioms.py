# Imported unchanged by model_find_v016.py: this IS the v0.15 axiom set.
# v0.16 = these axioms + abandons_def. Kept as a separate file to avoid
# duplicating ~40 axioms; see model_find_v016.py.
"""v0.15 model search. Person-scoped consent unifies the deontic layer:
consents(R,O,Q,M,T) = owner R consents to person Q using O in manner M.
ONE rule (use_grant + use_veto + self_consent) replaces NAP, allowed_use,
unowned_use, self_use, and the co-owner veto. `allows` is dropped."""
from z3 import *
Entity,(p1,p2,obj1)=EnumSort('Entity',['p1','p2','obj1'])
Time,(t0,t1,t2)=EnumSort('Time',['t0','t1','t2']); Manner,(m1,m2)=EnumSort('Manner',['m1','m2']); B=BoolSort()
person=Function('person',Entity,B); np_obj=Function('np_obj',Entity,B); rivalrous=Function('rivalrous',Entity,B)
before=Function('before',Time,Time,B); use=Function('use',Entity,Entity,Manner,Time,B); claim=Function('claim',Entity,Entity,Time,B)
owns=Function('owns',Entity,Entity,Entity,Time,B); is_owner=Function('is_owner',Entity,Entity,Time,B); unowned=Function('unowned',Entity,Time,B)
disowns=Function('disowns',Entity,Entity,Entity,Time,B); nodis=Function('nodis',Entity,Entity,Entity,Time,Time,B); reacq=Function('reacquires',Entity,Entity,Entity,Time,Time,B)
vtrans=Function('vol_transfer',Entity,Entity,Entity,Time,B); excl=Function('excl',Manner,Manner,B)
wants=Function('wants',Entity,Entity,Manner,Time,B); unreal=Function('unrealised',Entity,Entity,Manner,Time,B)
consents=Function('consents',Entity,Entity,Entity,Manner,Time,B)               # 5-ary: R,O,Q,M,T
may_use=Function('may_use',Entity,Entity,Manner,Time,B); forbidden_use=Function('forbidden_use',Entity,Entity,Manner,Time,B)
may_claim=Function('may_claim',Entity,Entity,Time,B); may_disown=Function('may_disown',Entity,Entity,Entity,Time,B); may_transfer=Function('may_transfer',Entity,Entity,Entity,Time,B)
E=[p1,p2,obj1]; T=[t0,t1,t2]; M=[m1,m2]
def FA(sig,bod):
    vs=[Const('v%d'%i,s) for i,s in enumerate(sig)]; return ForAll(vs,bod(*vs))
ax=[]
ax+=[FA([Time],lambda T:Not(before(T,T))),FA([Time,Time,Time],lambda a,b,c:Implies(And(before(a,b),before(b,c)),before(a,c))),
     FA([Time,Time],lambda a,b:Or(before(a,b),before(b,a),a==b)),Or([before(a,b) for a in T for b in T])]
ax+=[FA([Entity],lambda X:Not(And(person(X),np_obj(X))))]
ax+=[Exists([Const('a',Entity),Const('b',Entity)],And(person(Const('a',Entity)),person(Const('b',Entity)),Const('a',Entity)!=Const('b',Entity))),Exists([Const('o',Entity)],np_obj(Const('o',Entity)))]
ax+=[FA([Entity],lambda P:Implies(person(P),rivalrous(P)))]
ax+=[FA([Entity,Time],lambda O,Tm:Implies(Not(rivalrous(O)),unowned(O,Tm)))]
ax+=[FA([Entity,Entity,Manner,Time],lambda P,O,Mn,Tm:Implies(use(P,O,Mn,Tm),And(person(P),Or(np_obj(O),person(O)))))]
ax+=[FA([Entity,Entity,Time],lambda P,O,Tm:Implies(claim(P,O,Tm),And(person(P),np_obj(O))))]
ax+=[FA([Entity,Entity,Entity,Time],lambda P,O,Q,Tm:Implies(owns(P,O,Q,Tm),And(person(P),Or(np_obj(O),O==P),person(Q),P!=Q)))]
ax+=[FA([Entity,Entity,Entity,Time],lambda P,O,Q,Tm:Implies(And(person(P),person(O),P!=O),Not(owns(P,O,Q,Tm))))]
ax+=[FA([Entity,Entity,Time],lambda P,Q,Tm:Implies(And(person(P),person(Q),P!=Q),owns(P,P,Q,Tm)))]
ax+=[FA([Entity,Entity,Time],lambda P,O,Tm:is_owner(P,O,Tm)==Or([owns(P,O,q,Tm) for q in E]))]
ax+=[FA([Entity,Time],lambda O,Tm:unowned(O,Tm)==And([Not(is_owner(p,O,Tm)) for p in E]))]
ax+=[Exists([Const('o',Entity),Const('tt',Time)],And(np_obj(Const('o',Entity)),unowned(Const('o',Entity),Const('tt',Time))))]
ax+=[FA([Entity,Entity,Entity,Manner,Time,Time],lambda P,O,Q,Mn,a,b:Implies(And(person(P),np_obj(O),use(P,O,Mn,a),claim(P,O,a),unowned(O,a),before(a,b),person(Q),P!=Q),owns(P,O,Q,b)))]
ax+=[FA([Entity,Entity,Entity,Time],lambda P,O,Q,Tm:Implies(disowns(P,O,Q,Tm),And(person(P),np_obj(O),person(Q),P!=Q,owns(P,O,Q,Tm))))]
ax+=[FA([Entity,Entity,Entity,Time,Time],lambda P,O,Q,a,b:nodis(P,O,Q,a,b)==And([Implies(And(Or(tt==a,before(a,tt)),Or(tt==b,before(tt,b))),Not(disowns(P,O,Q,tt))) for tt in T]))]
ax+=[FA([Entity,Entity,Entity,Time,Time],lambda P,O,Q,a,b:Implies(And(owns(P,O,Q,a),before(a,b),nodis(P,O,Q,a,b)),owns(P,O,Q,b)))]
ax+=[FA([Entity,Entity,Entity,Time,Time],lambda P,O,Q,a,b:Implies(And(disowns(P,O,Q,a),before(a,b),Not(reacq(P,O,Q,a,b))),Not(owns(P,O,Q,b))))]
ax+=[FA([Entity,Entity,Entity,Time],lambda P1,P2,O,Tm:Implies(vtrans(P1,P2,O,Tm),And(is_owner(P1,O,Tm),person(P2),P1!=P2,np_obj(O))))]
ax+=[FA([Entity,Entity,Entity,Entity,Time],lambda P1,P2,O,Q,Tm:Implies(And(vtrans(P1,P2,O,Tm),owns(P1,O,Q,Tm)),disowns(P1,O,Q,Tm)))]
ax+=[FA([Entity,Entity,Entity,Entity,Time],lambda P1,P2,O,Q,Tm:Implies(And(vtrans(P1,P2,O,Tm),person(Q),P2!=Q),owns(P2,O,Q,Tm)))]
ax+=[FA([Entity,Entity,Entity,Manner,Manner,Time],lambda O,P1,P2,a,b,Tm:Implies(And(rivalrous(O),excl(a,b)),Not(And(use(P1,O,a,Tm),use(P2,O,b,Tm)))))]
ax+=[FA([Entity,Entity,Manner,Time],lambda P,O,Mn,Tm:unreal(P,O,Mn,Tm)==And(wants(P,O,Mn,Tm),Not(use(P,O,Mn,Tm))))]
# reified bridge + UNIFIED person-scoped consent rule
ax+=[FA([Entity,Entity,Manner,Time],lambda P,O,Mn,Tm: may_use(P,O,Mn,Tm)==Not(forbidden_use(P,O,Mn,Tm)))]
ax+=[FA([Entity,Entity,Manner,Time],lambda Q,O,Mn,Tm: Implies(And(person(Q),Or(np_obj(O),person(O)),And([Implies(is_owner(r,O,Tm),consents(r,O,Q,Mn,Tm)) for r in E])), may_use(Q,O,Mn,Tm)))]   # use_grant
ax+=[FA([Entity,Entity,Entity,Manner,Time],lambda R,O,Q,Mn,Tm: Implies(And(is_owner(R,O,Tm),Not(consents(R,O,Q,Mn,Tm))), forbidden_use(Q,O,Mn,Tm)))]   # use_veto
ax+=[FA([Entity,Entity,Manner,Time],lambda P,O,Mn,Tm: Implies(is_owner(P,O,Tm), consents(P,O,P,Mn,Tm)))]   # self_consent
# action permissions (unchanged)
ax+=[FA([Entity,Entity,Manner,Time],lambda P,O,Mn,Tm:Implies(And(person(P),np_obj(O),use(P,O,Mn,Tm),unowned(O,Tm)),may_claim(P,O,Tm)))]
ax+=[FA([Entity,Entity,Entity,Time],lambda P,O,Q,Tm:Implies(And(is_owner(P,O,Tm),np_obj(O)),may_disown(P,O,Q,Tm)))]
ax+=[FA([Entity,Entity,Entity,Time],lambda P1,P2,O,Tm:Implies(And(is_owner(P1,O,Tm),person(P2),P1!=P2,np_obj(O)),may_transfer(P1,P2,O,Tm)))]
if __name__=='__main__':
    s=Solver(); s.set('mbqi',True); s.add(ax); print("full v0.15 (unified person-scoped consent):", s.check())
