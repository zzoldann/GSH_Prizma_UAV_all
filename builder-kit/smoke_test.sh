#!/usr/bin/env bash
set -euo pipefail
echo "[SMOKE] cwd: $(pwd)"
python3 -m venv .venv || true
source .venv/bin/activate
pip -q install --upgrade pip
pip -q install -r builder-kit/requirements.txt
export PYTHONPATH="$PWD/src"
python - <<'PY'
from gsh_prizma import __version__
print("version:", __version__)
from gsh_prizma_addons.link_budget.core.calc import lora_required_snr_db, rx_sensitivity_dbm, fspl_db
snr = lora_required_snr_db(7, "4/7")
sens = rx_sensitivity_dbm(125_000, nf_db=6.0, req_snr_db=snr)
fspl = fspl_db(10.0, 868.0)
print("snr(7,4/7) =", snr)
print("sens(125kHz, NF6dB) =", round(sens,2), "dBm")
print("fspl(10km,868MHz) =", round(fspl,2), "dB")
PY
QT_QPA_PLATFORM=offscreen python -m gsh_prizma --smoke
python3 -m PyInstaller --noconfirm builder-kit/gsh_prizma_gui.spec
BIN_ONEFILE="dist/gsh-prizma-gen3"
BIN_ONEFOLDER="dist/gsh-prizma-gen3/gsh-prizma-gen3"
[[ -x "$BIN_ONEFILE" || -x "$BIN_ONEFOLDER" ]] || { echo "[SMOKE] no binary"; exit 1; }
echo "[SMOKE] PyInstaller OK."
MODE=pyinstaller bash builder-kit/pack_deb.sh
MODE=pyinstaller bash builder-kit/pack_rpm.sh
ls -lh *.deb *.rpm || true
echo "[SMOKE] DONE"
