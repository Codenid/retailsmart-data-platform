#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

apis=(serviceusage.googleapis.com cloudresourcemanager.googleapis.com iam.googleapis.com iamcredentials.googleapis.com storage.googleapis.com pubsub.googleapis.com bigquery.googleapis.com logging.googleapis.com monitoring.googleapis.com dataflow.googleapis.com dataproc.googleapis.com storagetransfer.googleapis.com run.googleapis.com)
log "RS-003 preflight para $PROJECT_ID en $REGION"
require_project_context
log "Identidad activa: $(gcloud auth list --filter=status:ACTIVE --format='value(account)' | head -n1)"
log "Facturación: $(gcloud billing projects describe "$PROJECT_ID" --format='value(billingEnabled)' 2>/dev/null || printf 'no verificable')"
for api in "${apis[@]}"; do
  if $DRY_RUN; then log "DRY-RUN verificar API $api"; continue; fi
  state="$(gcloud_run services list --enabled --filter="config.name=$api" --format='value(config.name)' 2>/dev/null || true)"
  [[ "$state" == "$api" ]] && log "API habilitada: $api" || log "API pendiente/no verificable: $api"
done
log "No se crean jobs, Composer, clusters Dataproc ni recursos de costo fijo en RS-003"
