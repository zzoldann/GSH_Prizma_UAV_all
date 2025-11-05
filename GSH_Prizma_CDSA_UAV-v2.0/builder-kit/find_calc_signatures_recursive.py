#!/usr/bin/env python3
import ast, sys
from pathlib import Path

roots = [Path("src")]
found_any = False
for root in roots:
    for p in root.rglob("calc.py"):
        try:
            t = p.read_text(encoding="utf-8")
            m = ast.parse(t, filename=str(p))
        except Exception as e:
            print(f"[find] skip {p}: {e}")
            continue
        print(f"[find] in {p}:")
        found_any = True
        for node in m.body:
            if isinstance(node, ast.FunctionDef):
                low = node.name.lower()
                if ("link" in low) or ("budget" in low) or low.startswith("calc") or low.startswith("compute"):
                    args = [a.arg for a in node.args.args]
                    print("  -", node.name, "(", ", ".join(args), ")")
if not found_any:
    print("[find] no calc.py files under src/")
