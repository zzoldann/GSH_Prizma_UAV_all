# file: builder-kit/patch_tab_link_autohelp_SAFE.py
#!/usr/bin/env python3
import re, sys, time
from pathlib import Path
TAB = Path("src/gsh_prizma/ui/tab_link.py")
def ts(): import time; return time.strftime("%Y-%m-%d_%H-%M-%S")
def rd(p): return p.read_text(encoding="utf-8")
def wr(p,s): p.write_text(s, encoding="utf-8")

BLOCK = r'''
# -- injected:autohelp --
_HELP_KEYS = {
 "model_combo":"model","env_combo":"env","f_edit":"f_mhz","bw_edit":"bw_mhz",
 "sf_combo":"sf","cr_combo":"cr","p_tx_edit":"p_tx_dbm","g_tx_edit":"g_tx_db","g_rx_edit":"g_rx_db",
 "l_tx_edit":"l_tx_line_db","l_rx_edit":"l_rx_line_db","h_tx_edit":"h_tx_m","h_rx_edit":"h_rx_m",
 "d_edit":"d_km","sigma_edit":"sigma_db","nf_edit":"nf_db"
}
def _attach_help_by_names(self):
    hm = globals().get("load_help_map", lambda: {})()
    for attr, key in _HELP_KEYS.items():
        w = getattr(self, attr, None)
        if w is None or not isinstance(key, str): continue
        h = hm.get(key, {})
        if hasattr(w,'setToolTip') and 'tooltip' in h: w.setToolTip(h['tooltip'])
        if hasattr(w,'setWhatsThis') and 'whats_this' in h: w.setWhatsThis(h['whats_this'])
'''
CALL = "        try:\n            _attach_help_by_names(self)\n        except Exception:\n            pass\n"

import re
s0 = rd(TAB); s = s0
if BLOCK not in s:
    s += "\n" + BLOCK + "\n"
# поставить вызов в __init__: после первой строки def __init__(
s = re.sub(r'(def\s+__init__\s*\(self[^\)]*\)\s*:\s*\n)', r'\1'+CALL, s, count=1)
if s != s0:
    wr(TAB.with_suffix(TAB.suffix+".bak."+ts()), s0); wr(TAB, s); print("[patch] autohelp added (safe)")
else:
    print("[patch] already ok")
