#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys, time
from pathlib import Path
TAB = Path("src/gsh_prizma/ui/tab_link.py")
def ts(): return time.strftime("%Y-%m-%d_%H-%M-%S")
def rd(p): return p.read_text(encoding="utf-8")
def wr(p,s): p.write_text(s, encoding="utf-8")
def main():
    if not TAB.exists():
        print("[ERR] not found:", TAB); sys.exit(2)
    s0 = rd(TAB); s = s0
    # A) Перенос _attach_help_by_names() НА ПОСЛЕ _build_ui(), чтобы не ронять форму
    s = s.replace(
        "        try:\n            _attach_help_by_names(self)\n        except Exception:\n            pass\n        super().__init__(parent)\n        self.helpmap = load_help()\n        self._build_ui()\n",
        "        super().__init__(parent)\n        self.helpmap = load_help()\n        self._build_ui()\n        try:\n            _attach_help_by_names(self)\n        except Exception:\n            pass\n"
    )
    # B) Развести help-функции: key-based -> apply_help_key, map -> load_help_dict
    s = s.replace("def load_help_map(", "def load_help_dict(")
    s = re.sub(r"\bload_help_map\(\)", "load_help_dict()", s)
    s = s.replace("def apply_help(w,key,default=None):", "def apply_help_key(w,key,default=None):")
    s = s.replace("apply_help(self.xaxis_group_box,", "apply_help_key(self.xaxis_group_box,")
    s = s.replace("apply_help(self.logx_cb,", "apply_help_key(self.logx_cb,")
    s = s.replace("apply_help(self.plainx_cb,", "apply_help_key(self.plainx_cb,")
    # C) Удалить блок раннего «injected: X-axis toggles» (если был)
    s = re.sub(r"\n\s*#\s*injected:\s*X-axis toggles.*?layout\.addLayout\(form\)\n",
               "\n        layout.addLayout(form)\n", s, flags=re.S)
    # D) Удалить дубликаты чекбоксов X-оси (если есть)
    s = re.sub(r"\n\s*self\.logx\s*=\s*QtWidgets\.QCheckBox.*?form\.addRow\(\"\",\s*self\.logx\)\n",
               "\n", s, flags=re.S)
    s = re.sub(r"\n\s*self\.x_plain_ticks\s*=\s*QtWidgets\.QCheckBox.*?form\.addRow\(\"\",\s*self\.x_plain_ticks\)\n",
               "\n", s, flags=re.S)
    if s != s0:
        bak = TAB.with_suffix(TAB.suffix + ".bak." + ts())
        wr(bak, s0); wr(TAB, s)
        print("[OK] Patched:", TAB)
        print("     Backup  :", bak.name)
    else:
        print("[OK] No changes (already fixed)")
if __name__ == "__main__":
    main()
