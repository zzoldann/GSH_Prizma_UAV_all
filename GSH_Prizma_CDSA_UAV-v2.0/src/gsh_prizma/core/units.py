def mhz(x_hz_or_mhz, assume_mhz=False):
    x = float(x_hz_or_mhz)
    return x if assume_mhz else x / 1e6

def km(x_m_or_km, assume_km=False):
    x = float(x_m_or_km)
    return x if assume_km else x / 1000.0
