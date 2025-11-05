# -*- coding: utf-8 -*-
import math

ENV_MAP_RU2KEY = {
    "Городская":   "urban",
    "Пригород":    "suburban",
    "Село/Дерев":  "rural",
    "Равнинная":   "plain",
    "Лес":         "forest",
    "Холмистая":   "hilly",
    "Горная":      "mountain",
    "Море/Водоём": "sea",
    "Река/Долина": "river",
}

def lora_required_snr_db(sf: int, cr: str = "4/5") -> float:
    table = {6:-5.0, 7:-7.5, 8:-10.0, 9:-12.5, 10:-15.0, 11:-17.5, 12:-20.0}
    base = table.get(int(sf), -7.5)
    cr_bonus = {"4/5":0.0, "4/6":-0.7, "4/7":-1.2, "4/8":-1.8}
    return float(base + cr_bonus.get(cr, 0.0))

def rx_noise_dbm(rx_bw_hz: float, temp_k: float = 290.0) -> float:
    k = 1.380649e-23
    n_w = k*temp_k*float(rx_bw_hz)
    return 10.0*math.log10(n_w) + 30.0

def rx_sensitivity_dbm(rx_bw_hz: float, nf_db: float, req_snr_db: float, temp_k: float = 290.0) -> float:
    return rx_noise_dbm(rx_bw_hz, temp_k) + float(nf_db) + float(req_snr_db)

def fspl_db(d_km: float, f_mhz: float) -> float:
    return 32.44 + 20.0*math.log10(max(d_km, 1e-9)) + 20.0*math.log10(max(f_mhz, 1e-9))
