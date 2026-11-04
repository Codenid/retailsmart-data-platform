#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
bash -n "$ROOT_DIR/scripts/gcp/06-analytics.sh"
grep -q 'id-b1194951ccb7415e9a6e977fd52c2789' "$ROOT_DIR/scripts/gcp/06-analytics.sh"
grep -q 'id-2f1d2779d6464c1383e5fbf375aab325' "$ROOT_DIR/scripts/gcp/06-analytics.sh"
echo 'test_analytics.sh: OK'
