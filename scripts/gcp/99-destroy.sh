#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
require_project_context
[[ -n "${PROJECT_ID:-}" ]] || die 'PROJECT_ID es obligatorio'
cat <<'MSG'
No se ejecuta destrucción automática en RS-003.
La eliminación futura deberá listar recursos con labels retailsmart=true,
excluir estado sintético y exigir confirmación interactiva explícita.
MSG
exit 2
