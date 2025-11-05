#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys, time
from pathlib import Path
TAB = Path("src/gsh_prizma/ui/tab_link.py")
def ts(): return time.strftime("%Y-%m-%d_%H-%M-%S")
def rd(p): return p.read_text(encoding="utf-8")
def wr(p,s): p.write_text(s, encoding="utf-8")
def sub_once(s, pat, repl, flags=0):
    new, n = re.subn(pat, repl, s, count=1, flags=flags)
    return new, n>0
def main():
    if not TAB.exists():
        print("[ERR] not found:", TAB); sys.exit(2)
    s0 = rd(TAB); s = s0; changed = False
    # A) Радиогруппа X-оси: использовать self.helpmap для label
    s, ok = sub_once(
        s,
        r"QtWidgets\.QGroupBox\(load_help_dict\(\)\.get\('x_axis_mode',\{\}\)\.get\('label','Шкала оси X'\)\)",
        r"QtWidgets.QGroupBox(self.helpmap.get('x_axis_mode',{}).get('label','Шкала оси X'))"
    ); changed |= ok
    # B) Заменить apply_help_key(...) -> apply_help(..., dict)
    s, ok = sub_once(
        s,
        r"apply_help_key\(\s*self\.xaxis_group_box\s*,\s*'x_axis_mode'\s*\)",
        r"apply_help(self.xaxis_group_box, self.helpmap.get('x_axis_mode'))"
    ); changed |= ok
    # C) Авто-хелпер: брать map из self.helpmap, а не вызывать load_help_map()
    s = re.sub(
        r'hm\s*=\s*globals\(\)\.get\("load_help_map",\s*lambda:\s*\{\}\)\(\)',
        r"hm = getattr(self, 'helpmap', {})",
        s
    )
    if changed:
        bak = TAB.with_suffix(TAB.suffix + ".bak." + ts())
        wr(bak, s0); wr(TAB, s)
        print("[OK] Patched:", TAB); print("     Backup:", bak.name)
    else:
        print("[OK] Nothing to change (already unified)")
if __name__ == "__main__":
    main()
