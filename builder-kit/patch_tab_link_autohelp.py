#!/usr/bin/env python3
import re, sys, os, json, time
from pathlib import Path
TAB = Path("src/gsh_prizma/ui/tab_link.py")
MAP = {
 "model_combo":"model","atten_model_combo":"atten_model","morphology_combo":"terrain_morphology",
 "earth_curv_cb":"earth_curvature","k_factor_spin":"k_factor","profile_step_spin":"profile_step_m",
 "clutter_combo":"clutter_class","epsr_spin":"ground_eps_r","sigma_spin":"ground_sigma_s",
 "rain_rate_spin":"rain_rate_mmph","gas_loss_spin":"gas_loss_db_km","pol_combo":"pol",
 "height_ref_combo":"ant_height_ref","env_combo":"env","f_edit":"f_mhz","bw_edit":"bw_mhz",
 "sf_combo":"sf","cr_combo":"cr","p_tx_edit":"p_tx_dbm","g_tx_edit":"g_tx_db","g_rx_edit":"g_rx_db",
 "l_tx_edit":"l_tx_line_db","l_rx_edit":"l_rx_line_db","h_tx_edit":"h_tx_m","h_rx_edit":"h_rx_m",
 "d_edit":"d_km","sigma_edit":"sigma_db","fadep_edit":"fade_p","nf_edit":"nf_db","xmax_edit":"x_range_km"
}
def ts(): return time.strftime("%Y-%m-%d_%H-%M-%S")
def rd(p): return p.read_text(encoding="utf-8")
def wr(p,s): p.write_text(s, encoding="utf-8")
def ensure(s):
  if "import json" not in s: s=re.sub(r"(^from PySide6[^\n]+\n)", r"\\1import json\n", s, count=1, flags=re.M)
  if "import os" not in s: s=re.sub(r"(^from PySide6[^\n]+\n)", r"\\1import os\n", s, count=1, flags=re.M)
  if "import sys" not in s: s=re.sub(r"(^from PySide6[^\n]+\n)", r"\\1import sys\n", s, count=1, flags=re.M)
  if "def resource_path(" not in s:
    s += "\\n\\ndef resource_path(*parts):\\n    base=getattr(sys,'_MEIPASS',os.getcwd())\\n    p=os.path.join(base,*parts)\\n    return p if os.path.exists(p) else os.path.join(os.getcwd(),*parts)\\n"
  if "def load_help_map(" not in s:
    s += "\\n_HELP_MAP=None\\ndef load_help_map():\\n    global _HELP_MAP\\n    if _HELP_MAP is None:\\n        try:\\n            with open(resource_path('assets','help','help_ru.json'),'r',encoding='utf-8') as f:\\n                _HELP_MAP=json.load(f)\\n        except Exception:\\n            _HELP_MAP={}\\n    return _HELP_MAP\\n\\n"
    s += "def apply_help(w,key):\\n    h=load_help_map().get(key,{})\\n    tt=h.get('tooltip'); wt=h.get('whats_this')\\n    \\n    " \
         "    \\n    " \
         "    \\n    " \
         ""
    s = s.replace("def apply_help(w,key):\\n    h=load_help_map().get(key,{})\\n    tt=h.get('tooltip'); wt=h.get('whats_this')\\n    \\n    " \
                  "    \\n    " \
                  "    \\n    ",
                  "def apply_help(w,key):\\n    h=load_help_map().get(key,{})\\n    if hasattr(w,'setToolTip') and 'tooltip' in h: w.setToolTip(h['tooltip'])\\n    if hasattr(w,'setWhatsThis') and 'whats_this' in h: w.setWhatsThis(h['whats_this'])\\n")
  if "def _apply_xaxis_format(" not in s:
    s += "\\ndef _apply_xaxis_format(ax,logx,no_pow10):\\n    try:\\n        ax.set_xscale('log' if logx else 'linear')\\n        if not logx and no_pow10:\\n            try:\\n                ax.get_xaxis().get_major_formatter().set_scientific(False)\\n                ax.ticklabel_format(style='plain',axis='x')\\n            except Exception: pass\\n        ax.figure.canvas.draw_idle()\\n    except Exception: pass\\n"
  if "self.logx_cb" not in s:
    s = re.sub(r'(form\\s*=\\s*QtWidgets\\.QFormLayout[^\\n]*\\n)',
               r"\\1        self.logx_cb=QtWidgets.QCheckBox(load_help_map().get('logx',{}).get('label','Логарифмическая ось X'))\\n"
               r"        apply_help(self.logx_cb,'logx')\\n"
               r"        self.plainx_cb=QtWidgets.QCheckBox(load_help_map().get('no_pow10_x',{}).get('label','Без степени по X'))\\n"
               r"        apply_help(self.plainx_cb,'no_pow10_x')\\n"
               r"        form.addRow('', self.logx_cb)\\n        form.addRow('', self.plainx_cb)\\n"
               r"        def _reapply():\\n            "
               r"            ax=getattr(self,'ax',None) or (self.figure.gca() if hasattr(self,'figure') else None)\\n            "
               r"            _=ax and _apply_xaxis_format(ax,self.logx_cb.isChecked(),self.plainx_cb.isChecked())\\n"
               r"        self.logx_cb.toggled.connect(_reapply)\\n        self.plainx_cb.toggled.connect(_reapply)\\n", s, count=1, flags=re.M)
  return s
def auto_apply(s):
  for attr,key in MAP.items():
    pat=re.compile(rf'(self\\.{attr}\\s*=\\s*QtWidgets\\.[A-Za-z_0-9]+\\([^\\)]*\\)\\s*\\n)')
    if pat.search(s) and f'apply_help(self.{attr}, "{key}")' not in s:
      s = pat.sub(rf"\\1        try:\\n            apply_help(self.{attr}, \"{key}\")\\n        except Exception: pass\\n", s, count=1)
  return s
def main():
  if not TAB.exists(): print('[patch] not found:',TAB); sys.exit(2)
  s=rd(TAB); o=s; s=ensure(s); s=auto_apply(s)
  if s!=o:
    bak=TAB.with_suffix(TAB.suffix+'.bak.'+ts()); wr(bak,o); wr(TAB,s); print('[patch] updated:',bak.name)
  else:
    print('[patch] already up-to-date')
if __name__=='__main__': main()
