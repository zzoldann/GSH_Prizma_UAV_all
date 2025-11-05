def export_monopole_qw(model: dict, f_Hz: float) -> str:
    L = model["L_m"]
    rad = 1e-3
    segs = 31
    lines = []
    lines.append("CM Quarter-wave monopole (first-order)")
    lines.append("CE")
    lines.append(f"GW 1 {segs} 0 0 0 0 0 {L:.6f} {rad:.6f}")
    lines.append("GE 1")
    lines.append("EX 0 1 16 0 1 0 0")
    lines.append(f"FR 0 1 0 0 {f_Hz/1e6:.6f} 0")
    lines.append("RP 0 91 1 1000 0 0 1 1")
    lines.append("EN")
    return "\n".join(lines)
