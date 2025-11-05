#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, sys, time, os
from pathlib import Path
TAB = Path("src/gsh_prizma/ui/tab_link.py")

def ts(): return time.strftime("%Y-%m-%d_%H-%M-%S")
def rd(p): return p.read_text(encoding="utf-8")
def wr(p,s): p.write_text(s, encoding="utf-8")

INJECT_MARK = "# -- injected:xaxis-radiogroup --"

def ensure_imports(s: str) -> str:
    # Ничего не удаляем, только дозакидываем импорты
    head_pat = re.compile(r"(^from\s+PySide6[^\n]+\n)", re.M)
    def _add(imp):
        nonlocal s
        if imp not in s:
            s = head_pat.sub(r"\1"+imp+"\n", s, count=1)
    _add("import os")
    _add("import sys")
    _add("import json")
    return s

def ensure_helpers(s: str) -> str:
    # Добавим в КОНЕЦ файла утилиты, если их ещё нет — не трогаем существующий код
    add = []
    if "def resource_path(" not in s:
        add.append("""
def resource_path(*parts):
    base = getattr(sys, "_MEIPASS", os.getcwd())
    p = os.path.join(base, *parts)
    return p if os.path.exists(p) else os.path.join(os.getcwd(), *parts)
""")
    if "def load_help_map(" not in s:
        add.append("""
_HELP_MAP = None
def load_help_map():
    global _HELP_MAP
    if _HELP_MAP is not None:
        return _HELP_MAP
    try:
        with open(resource_path("assets","help","help_ru.json"), "r", encoding="utf-8") as f:
            _HELP_MAP = json.load(f)
    except Exception:
        _HELP_MAP = {}
    return _HELP_MAP

def apply_help(widget, key):
    h = load_help_map().get(key, {}) if isinstance(key,str) else {}
    if hasattr(widget, "setToolTip") and "tooltip" in h:
        widget.setToolTip(h["tooltip"])
    if hasattr(widget, "setWhatsThis") and "whats_this" in h:
        widget.setWhatsThis(h["whats_this"])
""")
    if "def _apply_xaxis_mode(" not in s:
        add.append("""
def _apply_xaxis_mode(ax, mode_key: str):
    try:
        if mode_key == "log":
            ax.set_xscale("log")
        else:
            ax.set_xscale("linear")
        if mode_key == "linear_plain":
            try:
                ax.get_xaxis().get_major_formatter().set_scientific(False)
                ax.ticklabel_format(style="plain", axis="x")
            except Exception:
                pass
        if getattr(ax, "figure", None) and getattr(ax.figure, "canvas", None):
            ax.figure.canvas.draw_idle()
    except Exception:
        pass
""")
    if add:
        s = s + "\n" + "\n".join(add)
    return s

def inject_group(s: str) -> str:
    if INJECT_MARK in s:
        return s  # уже вставлено
    # Ищем создание FormLayout (переменная form ИЛИ self.form). Ничего не вырезаем.
    # Вставляем сразу ПОСЛЕ первой строки с созданием форм-лейаута.
    pat = re.compile(r'(\b(form|self\.form)\s*=\s*QtWidgets\.QFormLayout[^\n]*\n)', re.M)
    if not pat.search(s):
        return s  # нет подходящего места — не трогаем файл
    block = f"""{INJECT_MARK}
        try:
            self.xaxis_group_box = QtWidgets.QGroupBox(load_help_map().get('x_axis_mode',{{}}).get('label','Шкала оси X'))
            self.xaxis_group = QtWidgets.QButtonGroup(self.xaxis_group_box)
            self.rb_linear = QtWidgets.QRadioButton('Линейная')
            self.rb_log = QtWidgets.QRadioButton('Логарифмическая')
            self.rb_plain = QtWidgets.QRadioButton('Линейная (без 1eN)')
            lay = QtWidgets.QHBoxLayout(self.xaxis_group_box)
            for i, rb in enumerate((self.rb_linear, self.rb_log, self.rb_plain), 1):
                self.xaxis_group.addButton(rb, i)
                lay.addWidget(rb)
            self.rb_linear.setChecked(True)
            apply_help(self.xaxis_group_box, 'x_axis_mode')
            # добавим в форму, если она называется 'form' или 'self.form'
            try:
                form.addRow('', self.xaxis_group_box)
            except Exception:
                try:
                    self.form.addRow('', self.xaxis_group_box)
                except Exception:
                    pass
            def _apply_from_ui():
                try:
                    ax = getattr(self, 'ax', None)
                    if ax is None and hasattr(self, 'figure'): ax = self.figure.gca()
                    if not ax: return
                    bid = self.xaxis_group.checkedId()
                    mode = 'linear' if bid==1 else ('log' if bid==2 else 'linear_plain')
                    _apply_xaxis_mode(ax, mode)
                except Exception:
                    pass
                for m in ('refresh_plot','redraw','draw','update_plot'):
                    if hasattr(self, m):
                        try: getattr(self, m)()
                        except Exception: pass
            self.rb_linear.toggled.connect(_apply_from_ui)
            self.rb_log.toggled.connect(_apply_from_ui)
            self.rb_plain.toggled.connect(_apply_from_ui)
        except Exception:
            pass

"""
    return pat.sub(r"\1"+block, s, count=1)

def main():
    if not TAB.exists():
        print("[patch] not found:", TAB); sys.exit(2)
    s0 = rd(TAB)
    s = s0
    s = ensure_imports(s)
    s = ensure_helpers(s)
    s = inject_group(s)
    if s != s0:
        bak = TAB.with_suffix(TAB.suffix + ".bak." + ts())
        wr(bak, s0)
        wr(TAB, s)
        print("[patch] tab_link.py updated; backup:", bak.name)
    else:
        print("[patch] no changes (safe)")
if __name__ == "__main__":
    main()
