#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true
datasets=(
  "retailsmart_gold_insights:id-b1194951ccb7415e9a6e977fd52c2789"
  "retailsmart_operational_mart:id-2f1d2779d6464c1383e5fbf375aab325"
  "retailsmart_audit:id-91fc8e972e2e420e8a86c3afc6a260c8"
)
location="${BQ_LOCATION:-US}"
for spec in "${datasets[@]}"; do
  dataset="${spec%%:*}"
  archimate_id="${spec##*:}"
  if $DRY_RUN; then
    log "DRY-RUN verificar/crear dataset $dataset ($archimate_id) en $location"
    continue
  fi
  if bq --project_id="$PROJECT_ID" show "$dataset" >/dev/null 2>&1; then
    log "Dataset existente conservado: $dataset ($archimate_id)"
  else
    log "Creando dataset: $dataset ($archimate_id)"
    bq --project_id="$PROJECT_ID" mk --dataset --location="$location" \
      --description="RetailSmart $dataset; archimate_id=$archimate_id" "$dataset"
  fi
done
