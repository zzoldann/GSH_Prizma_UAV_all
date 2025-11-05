import math

def _a_hm_small_medium_city(f_MHz: float, hm_m: float) -> float:
    lf = math.log10(max(f_MHz, 1e-9))
    return (1.1*lf - 0.7) * hm_m - (1.56*lf - 0.8)

def _a_hm_large_city(f_MHz: float, hm_m: float) -> float:
    if f_MHz <= 200.0:
        return 8.29 * (math.log10(max(1.54*hm_m, 1e-9)))**2 - 1.1
    else:
        return 3.2 * (math.log10(max(11.75*hm_m, 1e-9)))**2 - 4.97

def hata_L_urban(f_MHz: float, hb_m: float, hm_m: float, d_km: float, big_city: bool=False) -> float:
    a_hm = _a_hm_large_city(f_MHz, hm_m) if big_city else _a_hm_small_medium_city(f_MHz, hm_m)
    L = 69.55 + 26.16*math.log10(f_MHz) - 13.82*math.log10(max(hb_m, 1e-6)) - a_hm         + (44.9 - 6.55*math.log10(max(hb_m, 1e-6))) * math.log10(max(d_km, 1e-9))
    return float(L)

def hata_L_suburban(f_MHz: float, hb_m: float, hm_m: float, d_km: float, big_city: bool=False) -> float:
    L_u = hata_L_urban(f_MHz, hb_m, hm_m, d_km, big_city=big_city)
    term = 2.0 * (math.log10(max(f_MHz/28.0, 1e-12)))**2 + 5.4
    return float(L_u - term)

def hata_L_open(f_MHz: float, hb_m: float, hm_m: float, d_km: float, big_city: bool=False) -> float:
    L_u = hata_L_urban(f_MHz, hb_m, hm_m, d_km, big_city=big_city)
    lf = math.log10(max(f_MHz, 1e-9))
    term = 4.78*(lf**2) - 18.33*lf + 40.94
    return float(L_u - term)

def cost231_L(f_MHz: float, hb_m: float, hm_m: float, d_km: float, big_city: bool=False, metropolis: bool=False) -> float:
    a_hm = _a_hm_large_city(f_MHz, hm_m) if big_city else _a_hm_small_medium_city(f_MHz, hm_m)
    C_m = 3.0 if metropolis else 0.0
    L = 46.3 + 33.9*math.log10(f_MHz) - 13.82*math.log10(max(hb_m, 1e-6)) - a_hm         + (44.9 - 6.55*math.log10(max(hb_m, 1e-6))) * math.log10(max(d_km, 1e-9)) + C_m
    return float(L)

def fspl_dB(f_MHz: float, d_km: float) -> float:
    return 32.44 + 20.0*math.log10(max(f_MHz, 1e-12)) + 20.0*math.log10(max(d_km, 1e-12))

def d_horizon_km(ht_m: float, hr_m: float, k: float = 4/3) -> float:
    return 3.57 * (math.sqrt(max(ht_m, 0.0)) + math.sqrt(max(hr_m, 0.0)))
