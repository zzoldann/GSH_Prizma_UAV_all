#!/usr/bin/env bash
set -euo pipefail
V=1.2.5
HDR=docs/README_HEADER_v${V}.md
BLK=docs/CHANGELOG_v${V}_block.md
if [ -f README.md ] && [ -f "$HDR" ]; then grep -q "v${V}" README.md || (cp README.md README.md.bak.$(date +%F_%H-%M-%S); cat "$HDR" README.md.bak.* > README.md; echo '[docs] README prepended'); fi
if [ -f CHANGELOG.md ] && [ -f "$BLK" ]; then grep -q "v${V}" CHANGELOG.md || (cp CHANGELOG.md CHANGELOG.md.bak.$(date +%F_%H-%M-%S); cat "$BLK" CHANGELOG.md.bak.* > CHANGELOG.md; echo '[docs] CHANGELOG prepended'); fi
