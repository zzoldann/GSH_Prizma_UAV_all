import math

def thermal_noise_dBm(B_Hz: float) -> float:
    return -174.0 + 10.0*math.log10(max(B_Hz, 1e-30))

def sensitivity_dBm(B_Hz: float, NF_dB: float, SNR_req_dB: float, margin_impl_dB: float=0.0) -> float:
    return thermal_noise_dBm(B_Hz) + NF_dB + SNR_req_dB + margin_impl_dB

def Lmax_dB(Ptx_dBm: float, Gtx_dBi: float, Grx_dBi: float, Lsys_dB: float, Smin_dBm: float, Lbf_dB: float) -> float:
    return Ptx_dBm + Gtx_dBi + Grx_dBi - Lsys_dB - (Smin_dBm + Lbf_dB)

def invert_distance(L_target_dB: float, model_fn, d_bounds_km=(0.01, 3000.0), **kwargs) -> float:
    d_lo, d_hi = d_bounds_km
    lo, hi = math.log10(d_lo), math.log10(d_hi)
    for _ in range(80):
        mid = 0.5*(lo+hi)
        d = 10**mid
        Ld = model_fn(d_km=d, **kwargs)
        if Ld < L_target_dB:
            lo = mid
        else:
            hi = mid
    return 10**((lo+hi)/2.0)
