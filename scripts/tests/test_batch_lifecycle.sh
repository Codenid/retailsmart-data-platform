#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
bash -n "$ROOT_DIR/scripts/gcp/05-batch-create.sh" "$ROOT_DIR/scripts/gcp/95-batch-destroy.sh"
grep -q 'BATCH_CREATE_APPROVED' "$ROOT_DIR/scripts/gcp/05-batch-create.sh"
grep -q 'BATCH_DESTROY_APPROVED' "$ROOT_DIR/scripts/gcp/95-batch-destroy.sh"
grep -q 'ELIMINAR' "$ROOT_DIR/scripts/gcp/95-batch-destroy.sh"
grep -q 'id-b31ac9e67a204bd2996043f98f93cec1' "$ROOT_DIR/scripts/gcp/05-batch-create.sh"
echo 'test_batch_lifecycle.sh: OK'
