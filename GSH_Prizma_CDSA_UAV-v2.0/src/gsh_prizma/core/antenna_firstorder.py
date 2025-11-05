import math
C = 299792458.0

def quarterwave_monopole(f_Hz: float, k_end: float=0.97):
    lam = C / f_Hz
    L = 0.25 * lam * k_end
    return {"type": "monopole_qw", "L_m": L, "k_end": k_end, "G_dBi": 2.15, "Z_in_ohm": 36.5}

def patch_rect(f_Hz: float, er: float, h_m: float):
    W = C/(2.0*f_Hz) * math.sqrt(2.0/(er+1.0))
    eeff = (er+1)/2 + (er-1)/2 * 1.0/math.sqrt(1.0 + 12.0*h_m/W)
    dL = 0.412*h_m * ((eeff+0.3)*(W/h_m + 0.264))/((eeff-0.258)*(W/h_m + 0.8))
    L = C/(2.0*f_Hz*math.sqrt(eeff)) - 2.0*dL
    return {"type": "patch_rect", "W_m": W, "L_m": L, "eps_eff": eeff, "deltaL_m": dL, "G_dBi": 7.0, "Z_in_ohm": 200.0}

def mini_yagi_3el(f_Hz: float):
    lam = C / f_Hz
    ref = 0.5*lam*1.05
    drv = 0.5*lam*0.98
    dir1 = 0.45*lam
    s1 = 0.2*lam; s2 = 0.17*lam
    return {"type": "yagi3", "ref_m": ref, "drv_m": drv, "dir1_m": dir1, "s1_m": s1, "s2_m": s2, "G_dBi": 6.0, "Z_in_ohm": 50.0}

def helix_compact(f_Hz: float, turns: int=3, D_lambda: float=0.25, S_lambda: float=0.23):
    lam = C / f_Hz
    D = D_lambda*lam
    S = S_lambda*lam
    L = turns * S
    return {"type": "helix_compact", "turns": turns, "D_m": D, "pitch_m": S, "L_m": L, "G_dBi": 8.0, "pol": "circular"}
