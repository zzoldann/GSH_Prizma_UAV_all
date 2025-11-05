#!/usr/bin/env python3
import re, sys, time, os, json
from pathlib import Path
TAB_FILE = Path('src/gsh_prizma/ui/tab_link.py')
def ts(): return time.strftime('%Y-%m-%d_%H-%M-%S')
def rd(p): return p.read_text(encoding='utf-8')
def wr(p,s): p.write_text(s, encoding='utf-8')
def ensure_imports(s):
    add=[]; 
    for imp in ('import os','import sys','import json'):
        if imp not in s: add.append(imp)
    if add: s=re.sub(r'(^from PySide6[^\n]+\n)', r"\1"+"\n".join(add)+"\n", s, 1, flags=re.M)
    if 'def resource_path(' not in s:
        s+="\n\ndef resource_path(*parts):\n    base=getattr(sys,'_MEIPASS',os.getcwd())\n    p=os.path.join(base,*parts)\n    return p if os.path.exists(p) else os.path.join(os.getcwd(),*parts)\n"
    return s
def add_help_funcs(s):
    if 'def load_help_map(' in s: return s
    s+="\n_HELP_MAP=None\ndef load_help_map():\n    global _HELP_MAP\n    if _HELP_MAP is None:\n        try:\n            with open(resource_path('assets','help','help_ru.json'),'r',encoding='utf-8') as f:\n                _HELP_MAP=json.load(f)\n        except Exception:\n            _HELP_MAP={}\n    return _HELP_MAP\n\ndef apply_help(w,key,default=None):\n    h=load_help_map().get(key,{})\n    if hasattr(w,'setToolTip') and 'tooltip' in h: w.setToolTip(h['tooltip'])\n    if hasattr(w,'setWhatsThis') and 'whats_this' in h: w.setWhatsThis(h['whats_this'])\n    if hasattr(w,'setPlaceholderText') and 'label' in h: w.setPlaceholderText(h.get('label', default or key))\n"
    return s
def add_xaxis_utils(s):
    if 'def _apply_xaxis_format(' in s: return s
    s+="\n\ndef _apply_xaxis_format(ax, logx, no_pow10):\n    try:\n        ax.set_xscale('log' if logx else 'linear')\n        if not logx and no_pow10:\n            try:\n                ax.get_xaxis().get_major_formatter().set_scientific(False)\n                ax.ticklabel_format(style='plain', axis='x')\n            except Exception:\n                pass\n        ax.figure.canvas.draw_idle()\n    except Exception:\n        pass\n"
    return s
def hook_checkboxes(s):
    if 'self.logx_cb' in s: return s
    return re.sub(r'(form\s*=\s*QtWidgets\.QFormLayout[^\n]*\n)',
                  r"""\1
        # injected: X-axis toggles
        self.logx_cb=QtWidgets.QCheckBox(load_help_map().get('logx',{}).get('label','Логарифмическая ось X'))
        apply_help(self.logx_cb,'logx')
        self.plainx_cb=QtWidgets.QCheckBox(load_help_map().get('no_pow10_x',{}).get('label','Без степени по X'))
        apply_help(self.plainx_cb,'no_pow10_x')
        form.addRow('', self.logx_cb)
        form.addRow('', self.plainx_cb)
        def _reapply():
            try:
                ax=getattr(self,'ax',None) or (self.figure.gca() if hasattr(self,'figure') else None)
                if ax: _apply_xaxis_format(ax, self.logx_cb.isChecked(), self.plainx_cb.isChecked())
            except Exception: pass
            for m in ('refresh_plot','redraw','draw','update_plot'):
                if hasattr(self,m):
                    try: getattr(self,m)()
                    except Exception: pass
        self.logx_cb.toggled.connect(_reapply)
        self.plainx_cb.toggled.connect(_reapply)
""", s, count=1, flags=re.M)
def main():
    if not TAB_FILE.exists(): print('[patch] not found:',TAB_FILE); sys.exit(2)
    s=rd(TAB_FILE); orig=s
    s=ensure_imports(s); s=add_help_funcs(s); s=add_xaxis_utils(s); s=hook_checkboxes(s)
    if s!=orig:
        bak=TAB_FILE.with_suffix(TAB_FILE.suffix+'.bak.'+ts()); wr(bak,orig); wr(TAB_FILE,s); print('[patch] tab_link.py updated:',bak.name)
    else:
        print('[patch] tab_link.py already patched')
if __name__=='__main__': main()
