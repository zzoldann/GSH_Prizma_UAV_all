#!/usr/bin/env python3
import ast,sys
from pathlib import Path
p=Path('src/gsh_prizma_addons/link_budget/core/calc.py')
t=p.read_text(encoding='utf-8') if p.exists() else sys.exit('[find] not found: '+str(p))
m=ast.parse(t)
def args(f): return [a.arg for a in f.args.args]
print('[find] functions:')
for n in m.body:
  if isinstance(n,ast.FunctionDef):
    low=n.name.lower()
    if ('link' in low) or ('budget' in low) or low.startswith('calc') or low.startswith('compute'):
      print(' -', n.name, '(', ', '.join(args(n)), ')')
