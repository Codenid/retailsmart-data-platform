#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for script in "$ROOT"/scripts/*.sh; do bash -n "$script"; done
for script in "$ROOT"/scripts/lib/*.sh "$ROOT"/scripts/gcp/*.sh "$ROOT"/scripts/tests/*.sh; do bash -n "$script"; done
bash "$ROOT/scripts/tests/test_common.sh"
python3 "$ROOT/scripts/export_architecture.py"
python3 -m unittest discover -s "$ROOT/tests" -p 'test_*.py' -v
printf '\nValidación local correcta; NO se ejecutó ningún despliegue GCP.\n'
