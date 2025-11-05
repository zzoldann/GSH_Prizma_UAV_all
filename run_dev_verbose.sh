    #!/usr/bin/env bash
    set -euo pipefail
    cd "$(dirname "$0")"
    echo "Python: $(python3 -V)"
    if [[ -d .venv ]]; then source .venv/bin/activate; fi
    python3 -m venv .venv >/dev/null 2>&1 || true
    source .venv/bin/activate
    python -m pip install -U pip >/dev/null
    python - <<'PY'
import importlib, sys, os
pkgs = ["PySide6", "matplotlib"]
for p in pkgs:
    try:
        importlib.import_module(p)
    except Exception:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", p])
print("PYTHONPATH:", os.path.join(os.getcwd(), "src"))
PY
    export PYTHONPATH="$PWD/src"
    # Try python -m gsh_prizma.cli gui
    if python - <<'PY'
import importlib; import sys
m = importlib.import_module("gsh_prizma.cli")
ok = hasattr(m, "main")
sys.exit(0 if ok else 1)
PY
    then
        exec python -m gsh_prizma.cli gui
    else
        # fallback to app
        exec python - <<'PY'
from gsh_prizma.ui.app import main
raise SystemExit(main())
PY
    fi
