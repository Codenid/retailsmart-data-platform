#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
bash -n "$ROOT_DIR/scripts/gcp/demo-create.sh" "$ROOT_DIR/scripts/gcp/demo-destroy.sh" "$ROOT_DIR/scripts/gcp/demo-status.sh"
grep -q 'DEMO_CREATE_APPROVED' "$ROOT_DIR/scripts/gcp/demo-create.sh"
grep -q 'DEMO_DESTROY_APPROVED' "$ROOT_DIR/scripts/gcp/demo-destroy.sh"
grep -q 'ELIMINAR-DEMO' "$ROOT_DIR/scripts/gcp/demo-destroy.sh"
grep -q 'datasets' "$ROOT_DIR/scripts/gcp/demo-destroy.sh"
grep -q 'active_dataflow_jobs' "$ROOT_DIR/scripts/gcp/demo-destroy.sh"
echo 'test_demo_lifecycle.sh: OK'
