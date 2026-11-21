#!/usr/bin/env bash
# Full rebuild + both verification passes. Exits non-zero unless both passes match on every figure.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/pass_a.py
python3 scripts/pass_b.py
python3 scripts/verify.py
python3 scripts/crosscheck.py
python3 scripts/analysis.py > out/analysis_log.txt
python3 scripts/verify_forward.py
python3 scripts/graphs.py
python3 scripts/build_pdf.py
python3 scripts/verify_pdf.py
python3 scripts/build_wiki.py
python3 scripts/build_readme.py
echo ALL CLEAN
