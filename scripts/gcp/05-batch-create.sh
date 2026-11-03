#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true
environment_name="${BATCH_ENVIRONMENT_NAME:-retailsmart-batch}"
composer_mode="${COMPOSER_MODE:-DEVELOPMENT}"
composer_network="${COMPOSER_NETWORK:-default}"

log "Ciclo batch bajo demanda: $environment_name"
require_project_context
[[ "${BATCH_CREATE_APPROVED:-false}" == "true" || "$DRY_RUN" == true ]] || die "establece BATCH_CREATE_APPROVED=true para crear Composer; el entorno tiene costo fijo"

if gcloud_run composer environments describe "$environment_name" --location="$REGION" >/dev/null 2>&1; then
  log "Entorno Composer existente conservado: $environment_name"
  gcloud_run composer environments describe "$environment_name" --location="$REGION" --format='yaml(name,state,config.nodeConfig)' || true
  exit 0
fi

log "Arquitectura: Orquestación Batch / Managed Service for Apache Airflow (id-b31ac9e67a204bd2996043f98f93cec1)"
log "El modo DEVELOPMENT permite hibernación posterior; no se ejecutan DAGs automáticamente"
if $DRY_RUN; then
  log "DRY-RUN crear Composer pequeño de desarrollo en $REGION sobre red $composer_network"
  exit 0
fi

gcloud_run composer environments create "$environment_name" \
  --location="$REGION" \
  --network="$composer_network" \
  --environment-size=small
log "Composer creado; validar estado RUNNING antes de cargar DAGs"
