#!/usr/bin/env bash
set -euo pipefail
NEW="${1:?Usage: version_tag.sh <new_version>}"
python3 - "$NEW" <<'PY'
import sys, pathlib, re, datetime
new = sys.argv[1]
p = pathlib.Path('src/gsh_prizma/__init__.py')
s = p.read_text(encoding='utf-8')
s = re.sub(r'(__version__\s*=\s*['\"])(.+?)(['\"])', rf"\g<1>{new}\3", s)
p.write_text(s, encoding='utf-8')
stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
ch = pathlib.Path('CHANGELOG.md')
cs = ch.read_text(encoding='utf-8')
entry = f"## v{new} — {stamp} (Europe/Berlin)\n\n- Version bump.\n\n"
ch.write_text(entry + cs, encoding='utf-8')
print("Updated to", new)
PY
