#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true
[[ "$DRY_RUN" == true || "${DEMO_CREATE_APPROVED:-false}" == true ]] || die "establece DEMO_CREATE_APPROVED=true para levantar la demo"

log "Creación de demo RetailSmart en $PROJECT_ID"
require_project_context
[[ "$DRY_RUN" == true || "${BATCH_CREATE_APPROVED:-false}" == true ]] || die "Composer requiere BATCH_CREATE_APPROVED=true"

run_step() {
  local label="$1"; shift
  log "$label"
  "$@"
}

if $DRY_RUN; then
  run_step 'DRY-RUN Storage' bash "$ROOT_DIR/scripts/gcp/03-storage.sh" --dry-run
  run_step 'DRY-RUN Pub/Sub' bash "$ROOT_DIR/scripts/gcp/04-pubsub.sh" --dry-run
  run_step 'DRY-RUN BigQuery' bash "$ROOT_DIR/scripts/gcp/06-analytics.sh" --dry-run
  run_step 'DRY-RUN Composer' bash "$ROOT_DIR/scripts/gcp/05-batch-create.sh" --dry-run
  log 'DRY-RUN Dataflow: requiere DEMO_START_DATAFLOW=true y ADC configurado'
  log 'Dataproc y Cloud Run: quedan pendientes hasta disponer de jobs/imagen de demo'
  exit 0
fi

run_step 'Storage' bash "$ROOT_DIR/scripts/gcp/03-storage.sh"
run_step 'Pub/Sub' bash "$ROOT_DIR/scripts/gcp/04-pubsub.sh"
run_step 'BigQuery' bash "$ROOT_DIR/scripts/gcp/06-analytics.sh"
run_step 'Composer' bash "$ROOT_DIR/scripts/gcp/05-batch-create.sh"

if [[ "${DEMO_START_DATAFLOW:-false}" == true ]]; then
  [[ -n "${GOOGLE_APPLICATION_CREDENTIALS:-}" ]] || die 'Dataflow requiere Application Default Credentials'
  log 'Dataflow: usar el comando documentado de RS-009 con límites de 1 worker'
else
  log 'Dataflow no iniciado; establece DEMO_START_DATAFLOW=true para la prueba streaming'
fi
log 'Dataproc y Cloud Run no se activan sin job PySpark o imagen versionada'
log 'Demo creada: verificar con demo-status.sh antes de ejecutar datos'
