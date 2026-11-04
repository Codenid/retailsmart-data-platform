#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
require_project_context
[[ "${DEMO_DESTROY_APPROVED:-false}" == true ]] || die 'establece DEMO_DESTROY_APPROVED=true para bajar la demo'

log 'La baja conservará buckets, objetos, contratos, datasets y estado sintético'
active_dataflow_jobs="$(gcloud_run dataflow jobs list --region="$REGION" --status=active --format='value(id,name)' 2>/dev/null || true)"
if [[ -n "$active_dataflow_jobs" ]]; then
  die "hay jobs Dataflow activos; cancélalos explícitamente por ID antes de continuar:\n$active_dataflow_jobs"
fi
read -r -p 'Escribe ELIMINAR-DEMO para eliminar Composer: ' confirmation
[[ "$confirmation" == 'ELIMINAR-DEMO' ]] || die 'baja cancelada'
BATCH_DESTROY_APPROVED=true bash "$ROOT_DIR/scripts/gcp/95-batch-destroy.sh"
log 'Demo dada de baja: Composer eliminado; datos persistentes conservados'
