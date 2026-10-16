#!/usr/bin/env python3
"""Run every check of the Libertarian Property Theory and regenerate the docs.

  1. build   — parse and type-check source/theory.py; generate all TPTP files
  2. prove   — Vampire and Leo-III (+E) on every minimal problem
  3. models  — Z3: non-trivial consistency model and all scenarios
  4. story   — the hand-written world of MODEL.md, evaluated directly
  5. fmb     — Vampire finite models (re-evaluated) and non-vacuity
  6. docs    — README tables, VERIFICATION.md, dependency diagram

Exit status 0 only if every check passes.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ('prove', ['source/prove.py']),
    ('models', ['source/models.py']),
    ('story', ['source/story.py']),
    ('fmb', ['source/fmb.py']),
    ('docs', ['source/docs.py']),
]


def main():
    failed = []
    for name, cmd in STEPS:
        print("=== %s ===" % name, flush=True)
        r = subprocess.run([sys.executable] + cmd, cwd=ROOT)
        if r.returncode != 0:
            failed.append(name)
    print("\nALL CHECKS PASS" if not failed else "\nFAILED: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
