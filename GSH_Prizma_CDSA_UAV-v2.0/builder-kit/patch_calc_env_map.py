#!/usr/bin/env python3
import re, sys, time
from pathlib import Path
CALC=Path('src/gsh_prizma_addons/link_budget/core/calc.py')
def ts(): return time.strftime('%Y-%m-%d_%H-%M-%S')
def rd(p): return p.read_text(encoding='utf-8')
def wr(p,s): p.write_text(s, encoding='utf-8')
ENV_BLOCK = """
# injected: RU->key mapping and normalizers
ENV_MAP_RU2KEY={
 'Городская':'urban','Пригород':'suburban','Село/Дерев':'village','Равнинная':'plain','Лес':'forest','Водоём':'sea','Река':'river',
 'городская':'urban','пригород':'suburban','село/дерев':'village','равнинная':'plain','лес':'forest','водоём':'sea','река':'river',
}
def normalize_env(env):
    if isinstance(env,str): return ENV_MAP_RU2KEY.get(env,env)
    return env
def clamp_heights(v):
    try:
        v=float(v); 
        if v<0.1: v=0.1
        if v>12000: v=12000.0
        return v
    except Exception: return v
def bw_mhz_to_hz(bw_mhz):
    try: return float(bw_mhz)*1e6
    except Exception: return bw_mhz
"""
def ensure_block(s):
    if 'ENV_MAP_RU2KEY' in s: return s
    return re.sub(r'(^[^\n]*import[^\n]*\n+)', r"\1"+ENV_BLOCK+"\n", s, count=1, flags=re.M)
def inject_calls(s):
    pat=re.compile(r'^(def\s+(?:link_?budget|compute_?link|calc_?link)\s*\((.*?)\):\s*\n)', re.M)
    def repl(m):
        head=m.group(1)
        inj=("    # injected normalization\n"
             "    try:\n        env=normalize_env(locals().get('env'))\n        "+
             "if 'env' in locals(): locals()['env']=env\n    except Exception: pass\n"
             "    for _k in ('h_tx','h_tx_m','h_rx','h_rx_m'):\n        if _k in locals(): locals()[_k]=clamp_heights(locals()[_k])\n"
             "    if 'bw_mhz' in locals(): locals()['bw_hz']=bw_mhz_to_hz(locals()['bw_mhz'])\n" )
        return head+inj
    return pat.sub(repl,s)
def main():
    if not CALC.exists(): print('[patch] not found:',CALC); sys.exit(2)
    s=rd(CALC); orig=s
    s=ensure_block(s); s=inject_calls(s)
    if s!=orig:
        bak=CALC.with_suffix(CALC.suffix+'.bak.'+ts()); wr(bak,orig); wr(CALC,s); print('[patch] calc.py updated:',bak.name)
    else:
        print('[patch] calc.py already patched')
if __name__=='__main__': main()
