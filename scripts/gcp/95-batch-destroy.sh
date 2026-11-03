#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
environment_name="${BATCH_ENVIRONMENT_NAME:-retailsmart-batch}"
require_project_context
[[ "${BATCH_DESTROY_APPROVED:-false}" == "true" ]] || die "establece BATCH_DESTROY_APPROVED=true para destruir"

if ! gcloud_run composer environments describe "$environment_name" --location="$REGION" >/dev/null 2>&1; then
  log "Composer no existe: $environment_name"
  exit 0
fi

cat <<MSG
Se eliminará únicamente el entorno Composer de laboratorio:
  proyecto: $PROJECT_ID
  región:   $REGION
  entorno:  $environment_name

No se eliminarán buckets, objetos, contratos ni estado sintético persistente.
MSG
read -r -p 'Escribe ELIMINAR para continuar: ' confirmation
[[ "$confirmation" == "ELIMINAR" ]] || die 'destrucción cancelada'
gcloud_run composer environments delete "$environment_name" --location="$REGION"
log "Entorno Composer eliminado: $environment_name"
