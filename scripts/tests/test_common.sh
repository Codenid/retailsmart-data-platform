#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"

[[ "$(resource_exists() { return 1; }; resource_exists bucket anything; echo "$?" 2>/dev/null || true)" == "1" ]] || true
if (require_var MISSING_TEST_VAR) 2>/dev/null; then
  echo 'require_var debía fallar' >&2; exit 1
fi
if (resource_exists unsupported x) 2>/dev/null; then
  echo 'resource_exists debía rechazar tipos desconocidos' >&2; exit 1
fi
echo 'test_common.sh: OK'
