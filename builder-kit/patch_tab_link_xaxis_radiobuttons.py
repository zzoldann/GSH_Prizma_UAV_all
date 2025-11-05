#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace/Inject X-axis controls as a 3-option RadioButton group:
 - Линейная
 - Логарифмическая
 - Линейная (без 1eN)
Compatible with prior checkbox injection: hides/removes those if found.
"""
import re, sys, time, os, json
from pathlib import Path

TAB_FILE = Path("src/gsh_prizma/ui/tab_link.py")

def ts(): return time.strftime("%Y-%m-%d_%H-%M-%S")
def rd(p): return p.read_text(encoding="utf-8")
def wr(p,s): p.write_text(s, encoding="utf-8")

def ensure_imports(s: str) -> str:
    add = []
    for imp in ("import os","import sys","import json"):
        if imp not in s:
            add.append(imp)
    if add:
        s = re.sub(r"(^from PySide6[^\n]+\n)", r"\1" + "\n".join(add) + "\n", s, count=1, flags=re.M)
    if "def resource_path(" not in s:
        s += """
def resource_path(*parts):
    base = getattr(sys, "_MEIPASS", os.getcwd())
    p = os.path.join(base, *parts)
    return p if os.path.exists(p) else os.path.join(os.getcwd(), *parts)
"""
    return s

def ensure_helpers(s: str) -> str:
    if "def load_help_map(" not in s:
        s += """
_HELP_MAP=None
def load_help_map():
    global _HELP_MAP
    if _HELP_MAP is None:
        try:
            with open(resource_path("assets","help","help_ru.json"), "r", encoding="utf-8") as f:
                _HELP_MAP=json.load(f)
        except Exception:
            _HELP_MAP={}
    return _HELP_MAP
def apply_help(w,key):
    h=load_help_map().get(key,{}) if isinstance(key,str) else {}
    if hasattr(w,'setToolTip') and 'tooltip' in h: w.setToolTip(h['tooltip'])
    if hasattr(w,'setWhatsThis') and 'whats_this' in h: w.setWhatsThis(h['whats_this'])
"""
    if "def _apply_xaxis_mode(" not in s:
        s += """
def _apply_xaxis_mode(ax, mode_key: str):
    try:
        if mode_key == 'log':
            ax.set_xscale('log')
        else:
            ax.set_xscale('linear')
        if mode_key == 'linear_plain':
            try:
                ax.get_xaxis().get_major_formatter().set_scientific(False)
                ax.ticklabel_format(style='plain', axis='x')
            except Exception:
                pass
        if hasattr(ax,'figure') and hasattr(ax.figure,'canvas'):
            ax.figure.canvas.draw_idle()
    except Exception:
        pass
"""
    return s

def remove_old_checkboxes(s: str) -> str:
    # Heuristic: remove previously injected block with self.logx_cb / self.plainx_cb
    s = re.sub(r"\n\s*#\s*--\s*injected:\s*x-axis\s*toggles.*?(?:\n\s*\n|\Z)", "\n", s, flags=re.S)
    s = re.sub(r"\n\s*self\.logx_cb\.[^\n]*\n", "\n", s)
    s = re.sub(r"\n\s*self\.plainx_cb\.[^\n]*\n", "\n", s)
    return s

def inject_radiobuttons(s: str) -> str:
    if "self.xaxis_group" in s:
        return s
    # insert after first QFormLayout creation
    return re.sub(r'(form\s*=\s*QtWidgets\.QFormLayout[^\n]*\n)',
                  r"""\1
        # -- injected: X-axis radio buttons (3 options)
        try:
            self.xaxis_group_box = QtWidgets.QGroupBox(load_help_map().get('x_axis_mode',{}).get('label','Шкала оси X'))
            self.xaxis_group = QtWidgets.QButtonGroup(self.xaxis_group_box)
            self.rb_linear = QtWidgets.QRadioButton(load_help_map().get('x_axis_mode_options',[{'label':'Линейная'}])[0].get('label','Линейная'))
            self.rb_log = QtWidgets.QRadioButton(load_help_map().get('x_axis_mode_options',[{}, {'label':'Логарифмическая'}])[1].get('label','Логарифмическая'))
            self.rb_plain = QtWidgets.QRadioButton(load_help_map().get('x_axis_mode_options',[{}, {}, {'label':'Линейная (без 1eN)'}])[2].get('label','Линейная (без 1eN)'))
            lay = QtWidgets.QHBoxLayout(self.xaxis_group_box)
            for i, rb in enumerate((self.rb_linear, self.rb_log, self.rb_plain), 1):
                self.xaxis_group.addButton(rb, i)
                lay.addWidget(rb)
            # default: linear
            self.rb_linear.setChecked(True)
            form.addRow('', self.xaxis_group_box)
            apply_help(self.xaxis_group_box,'x_axis_mode')
            def _apply_from_ui():
                try:
                    ax = getattr(self, 'ax', None) or (self.figure.gca() if hasattr(self,'figure') else None)
                    if not ax: return
                    bid = self.xaxis_group.checkedId()
                    mode = 'linear' if bid==1 else ('log' if bid==2 else 'linear_plain')
                    _apply_xaxis_mode(ax, mode)
                except Exception:
                    pass
                for m in ('refresh_plot','redraw','draw','update_plot'):
                    if hasattr(self,m):
                        try: getattr(self,m)()
                        except Exception: pass
            self.rb_linear.toggled.connect(_apply_from_ui)
            self.rb_log.toggled.connect(_apply_from_ui)
            self.rb_plain.toggled.connect(_apply_from_ui)
        except Exception:
            pass
""", s, count=1, flags=re.M)

def main():
    if not TAB_FILE.exists():
        print("[patch] not found:", TAB_FILE); sys.exit(2)
    s = rd(TAB_FILE)
    orig = s
    s = ensure_imports(s)
    s = ensure_helpers(s)
    s = remove_old_checkboxes(s)
    s = inject_radiobuttons(s)
    if s != orig:
        bak = TAB_FILE.with_suffix(TAB_FILE.suffix + ".bak." + ts())
        wr(bak, orig)
        wr(TAB_FILE, s)
        print("[patch] updated:", bak.name)
    else:
        print("[patch] already up-to-date")
if __name__ == "__main__":
    main()
