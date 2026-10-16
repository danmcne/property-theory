"""Small TPTP toolkit for the property theory.

One formula syntax (the TPTP FOF/TFF/THF-common fragment) is parsed once and
used four ways:
  * emitted as THF problems (Leo-III) and TFF problems (Vampire);
  * grounded over a finite domain into a Z3 propositional problem
    (consistency, scenario and non-vacuity checks);
  * evaluated directly over an explicit finite structure (no solver).

Supported fragment: ![V:s,..]:  ?[V:s,..]:  ~  &  |  =>  <=>  =  !=  $true
$false, predicate atoms p(t1,..,tn) whose terms are variables (Upper case
initial) or constants (lower case initial). There are no function symbols.
The parser follows TPTP grouping rules: & and | chain only with themselves,
=> and <=> are binary and need parentheses to combine, and a quantifier or
~ applies to the following unit formula only.
"""
import re
from itertools import product

# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------
_TOK = re.compile(r"\s*(<=>|=>|!=|!\[|\?\[|[()\[\]:,~&|=]|\$true|\$false|[A-Za-z][A-Za-z0-9_]*)")


def tokenize(s):
    out, i = [], 0
    s = s.strip()
    while i < len(s):
        m = _TOK.match(s, i)
        if not m:
            raise SyntaxError("cannot tokenize at: %r" % s[i:i + 30])
        out.append(m.group(1))
        i = m.end()
        while i < len(s) and s[i].isspace():
            i += 1
    return out


class _P:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def eat(self, x=None):
        tok = self.peek()
        if x is not None and tok != x:
            raise SyntaxError("expected %r, got %r at token %d" % (x, tok, self.i))
        self.i += 1
        return tok

    # formula := unit ( (&unit)* | (|unit)* | => unit | <=> unit )?
    def formula(self):
        a = self.unit()
        op = self.peek()
        if op in ('&', '|'):
            parts = [a]
            while self.peek() == op:
                self.eat(op)
                parts.append(self.unit())
            if self.peek() in ('&', '|', '=>', '<=>'):
                raise SyntaxError("mixed binary connectives need parentheses")
            return ('and' if op == '&' else 'or', parts)
        if op in ('=>', '<=>'):
            self.eat(op)
            b = self.unit()
            if self.peek() in ('&', '|', '=>', '<=>'):
                raise SyntaxError("mixed binary connectives need parentheses")
            return ('imp', a, b) if op == '=>' else ('iff', a, b)
        return a

    def unit(self):
        tok = self.peek()
        if tok in ('![', '?['):
            self.eat()
            vs = []
            while True:
                v = self.eat()
                self.eat(':')
                s = self.eat()
                vs.append((v, s))
                if self.peek() == ',':
                    self.eat(',')
                    continue
                self.eat(']')
                break
            self.eat(':')
            body = self.unit()
            return ('forall' if tok == '![' else 'exists', vs, body)
        if tok == '~':
            self.eat()
            return ('not', self.unit())
        if tok == '(':
            self.eat('(')
            f = self.formula()
            self.eat(')')
            return f
        if tok == '$true':
            self.eat()
            return ('true',)
        if tok == '$false':
            self.eat()
            return ('false',)
        # atom or equality
        name = self.eat()
        if self.peek() == '(':
            self.eat('(')
            args = [self.term()]
            while self.peek() == ',':
                self.eat(',')
                args.append(self.term())
            self.eat(')')
            return ('atom', name, args)
        t1 = self._mk_term(name)
        op = self.eat()
        if op not in ('=', '!='):
            raise SyntaxError("expected = or != after term %s" % name)
        t2 = self.term()
        eq = ('eq', t1, t2)
        return eq if op == '=' else ('not', eq)

    def term(self):
        return self._mk_term(self.eat())

    @staticmethod
    def _mk_term(name):
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", name):
            raise SyntaxError("bad term %r" % name)
        return ('var', name) if name[0].isupper() else ('const', name)


def parse(s):
    p = _P(tokenize(s))
    f = p.formula()
    if p.peek() is not None:
        raise SyntaxError("trailing tokens: %r" % p.t[p.i:])
    return f


# --------------------------------------------------------------------------
# analysis
# --------------------------------------------------------------------------
def preds_of(f, acc=None):
    acc = set() if acc is None else acc
    k = f[0]
    if k == 'atom':
        acc.add(f[1])
    elif k in ('forall', 'exists'):
        preds_of(f[2], acc)
    elif k == 'not':
        preds_of(f[1], acc)
    elif k in ('and', 'or'):
        for g in f[1]:
            preds_of(g, acc)
    elif k in ('imp', 'iff'):
        preds_of(f[1], acc)
        preds_of(f[2], acc)
    return acc


def consts_of(f, acc=None):
    acc = set() if acc is None else acc
    k = f[0]
    if k == 'atom':
        acc.update(t[1] for t in f[2] if t[0] == 'const')
    elif k == 'eq':
        acc.update(t[1] for t in f[1:] if t[0] == 'const')
    elif k in ('forall', 'exists'):
        consts_of(f[2], acc)
    elif k == 'not':
        consts_of(f[1], acc)
    elif k in ('and', 'or'):
        for g in f[1]:
            consts_of(g, acc)
    elif k in ('imp', 'iff'):
        consts_of(f[1], acc)
        consts_of(f[2], acc)
    return acc


def typecheck(f, sig, const_sorts, env=None, where=''):
    """Check sorts of every atom/equality; variables must be bound."""
    env = {} if env is None else env
    k = f[0]

    def sort_of(t):
        if t[0] == 'var':
            if t[1] not in env:
                raise TypeError("%s: unbound variable %s" % (where, t[1]))
            return env[t[1]]
        if t[1] not in const_sorts:
            raise TypeError("%s: undeclared constant %s" % (where, t[1]))
        return const_sorts[t[1]]

    if k == 'atom':
        if f[1] not in sig:
            raise TypeError("%s: undeclared predicate %s" % (where, f[1]))
        want = sig[f[1]]
        got = [sort_of(t) for t in f[2]]
        if list(want) != got:
            raise TypeError("%s: %s expects %s, got %s" % (where, f[1], want, got))
    elif k == 'eq':
        if sort_of(f[1]) != sort_of(f[2]):
            raise TypeError("%s: equality between sorts %s/%s" % (where, sort_of(f[1]), sort_of(f[2])))
    elif k in ('forall', 'exists'):
        e2 = dict(env)
        for v, s in f[1]:
            e2[v] = s
        typecheck(f[2], sig, const_sorts, e2, where)
    elif k == 'not':
        typecheck(f[1], sig, const_sorts, env, where)
    elif k in ('and', 'or'):
        for g in f[1]:
            typecheck(g, sig, const_sorts, env, where)
    elif k in ('imp', 'iff'):
        typecheck(f[1], sig, const_sorts, env, where)
        typecheck(f[2], sig, const_sorts, env, where)


def polarity(f, pred, pol=+1, out=None):
    """Collect the polarities (+1, -1, 0 for both) at which `pred` occurs."""
    out = set() if out is None else out
    k = f[0]
    if k == 'atom':
        if f[1] == pred:
            out.add(pol)
    elif k in ('forall', 'exists'):
        polarity(f[2], pred, pol, out)
    elif k == 'not':
        polarity(f[1], pred, -pol, out)
    elif k in ('and', 'or'):
        for g in f[1]:
            polarity(g, pred, pol, out)
    elif k == 'imp':
        polarity(f[1], pred, -pol, out)
        polarity(f[2], pred, pol, out)
    elif k == 'iff':
        polarity(f[1], pred, 0, out)
        polarity(f[2], pred, 0, out)
    return out


# --------------------------------------------------------------------------
# printing
# --------------------------------------------------------------------------
def show_term(t):
    return t[1]


def show(f):
    """Fully parenthesised TPTP text (valid in FOF, TFF and THF)."""
    k = f[0]
    if k == 'atom':
        return "%s(%s)" % (f[1], ",".join(show_term(t) for t in f[2]))
    if k == 'eq':
        return "(%s = %s)" % (show_term(f[1]), show_term(f[2]))
    if k == 'not':
        if f[1][0] == 'eq':
            return "(%s != %s)" % (show_term(f[1][1]), show_term(f[1][2]))
        return "~ %s" % show(f[1])
    if k == 'true':
        return "$true"
    if k == 'false':
        return "$false"
    if k in ('forall', 'exists'):
        q = '!' if k == 'forall' else '?'
        return "%s[%s]: %s" % (q, ",".join("%s:%s" % vs for vs in f[1]), show(f[2]))
    if k in ('and', 'or'):
        op = ' & ' if k == 'and' else ' | '
        return "(%s)" % op.join(show(g) for g in f[1])
    if k == 'imp':
        return "(%s => %s)" % (show(f[1]), show(f[2]))
    if k == 'iff':
        return "(%s <=> %s)" % (show(f[1]), show(f[2]))
    raise ValueError(k)


def thf_type(argsorts):
    return " > ".join(list(argsorts) + ['$o'])


def tff_type(argsorts):
    if len(argsorts) == 1:
        return "%s > $o" % argsorts[0]
    return "(%s) > $o" % " * ".join(argsorts)


def problem(lang, sorts, sig, const_sorts, axioms, conjecture=None, header=''):
    """Render a complete TPTP problem.

    axioms: list of (name, ast, comment) ; conjecture: (name, ast) or None.
    Only the predicates and constants actually used are declared."""
    used = set()
    for _, f, _ in axioms:
        preds_of(f, used)
    if conjecture:
        preds_of(conjecture[1], used)
    consts = set()
    for _, f, _ in axioms:
        consts_of(f, consts)
    if conjecture:
        consts_of(conjecture[1], consts)
    w = lang  # 'thf' or 'tff'
    lines = []
    if header:
        lines += ["% " + h if h else "%" for h in header.splitlines()]
    for s in sorts:
        lines.append("%s(%s_type, type, %s: $tType)." % (w, s, s))
    for p in sorted(used):
        ty = thf_type(sig[p]) if w == 'thf' else tff_type(sig[p])
        lines.append("%s(%s_decl, type, %s: %s)." % (w, p, p, ty))
    for c in sorted(consts):
        lines.append("%s(%s_decl, type, %s: %s)." % (w, c, c, const_sorts[c]))
    for name, f, comment in axioms:
        if comment:
            lines.append("%% %s" % comment)
        lines.append("%s(%s, axiom,\n    %s)." % (w, name, show(f)))
    if conjecture:
        lines.append("%s(%s, conjecture,\n    %s)." % (w, conjecture[0], show(conjecture[1])))
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# finite semantics: direct evaluation and Z3 grounding
# --------------------------------------------------------------------------
def evaluate(f, dom, interp, env=None):
    """Evaluate over an explicit structure. dom: sort -> list of elements;
    interp: pred -> set of argument tuples (closed world); constants denote
    the element with the same name."""
    env = {} if env is None else env
    k = f[0]

    def val(t):
        return env[t[1]] if t[0] == 'var' else t[1]

    if k == 'atom':
        return tuple(val(t) for t in f[2]) in interp[f[1]]
    if k == 'eq':
        return val(f[1]) == val(f[2])
    if k == 'true':
        return True
    if k == 'false':
        return False
    if k == 'not':
        return not evaluate(f[1], dom, interp, env)
    if k == 'and':
        return all(evaluate(g, dom, interp, env) for g in f[1])
    if k == 'or':
        return any(evaluate(g, dom, interp, env) for g in f[1])
    if k == 'imp':
        return (not evaluate(f[1], dom, interp, env)) or evaluate(f[2], dom, interp, env)
    if k == 'iff':
        return evaluate(f[1], dom, interp, env) == evaluate(f[2], dom, interp, env)
    if k in ('forall', 'exists'):
        names = [v for v, _ in f[1]]
        it = product(*[dom[s] for _, s in f[1]])
        test = all if k == 'forall' else any
        return test(evaluate(f[2], dom, interp, dict(env, **dict(zip(names, vals)))) for vals in it)
    raise ValueError(k)


def counterexample(f, dom, interp):
    """For a universally closed formula that fails, return the first falsifying
    assignment of its outer universal variables (for readable reports)."""
    if f[0] != 'forall':
        return None
    names = [v for v, _ in f[1]]
    for vals in product(*[dom[s] for _, s in f[1]]):
        env = dict(zip(names, vals))
        if not evaluate(f[2], dom, interp, env):
            return env
    return None


class Grounder:
    """Ground formulas over a finite domain into Z3 Booleans (one Bool per
    ground atom). Elements are the strings in `dom`; distinct names denote
    distinct elements (unique-name assumption)."""

    def __init__(self, dom):
        import z3
        self.z3 = z3
        self.dom = dom
        self.atoms = {}

    def atom(self, p, args):
        key = (p, tuple(args))
        if key not in self.atoms:
            self.atoms[key] = self.z3.Bool("%s(%s)" % (p, ",".join(args)))
        return self.atoms[key]

    def g(self, f, env=None):
        z3 = self.z3
        env = {} if env is None else env
        k = f[0]

        def val(t):
            return env[t[1]] if t[0] == 'var' else t[1]

        if k == 'atom':
            return self.atom(f[1], [val(t) for t in f[2]])
        if k == 'eq':
            return z3.BoolVal(val(f[1]) == val(f[2]))
        if k == 'true':
            return z3.BoolVal(True)
        if k == 'false':
            return z3.BoolVal(False)
        if k == 'not':
            return z3.Not(self.g(f[1], env))
        if k == 'and':
            return z3.And([self.g(h, env) for h in f[1]])
        if k == 'or':
            return z3.Or([self.g(h, env) for h in f[1]])
        if k == 'imp':
            return z3.Implies(self.g(f[1], env), self.g(f[2], env))
        if k == 'iff':
            return self.g(f[1], env) == self.g(f[2], env)
        if k in ('forall', 'exists'):
            names = [v for v, _ in f[1]]
            parts = [self.g(f[2], dict(env, **dict(zip(names, vals))))
                     for vals in product(*[self.dom[s] for _, s in f[1]])]
            return z3.And(parts) if k == 'forall' else z3.Or(parts)
        raise ValueError(k)
