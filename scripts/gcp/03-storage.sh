#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"

[[ "${1:-}" != "--dry-run" ]] || DRY_RUN=true
DRY_RUN="${DRY_RUN:-false}"
location="${STORAGE_LOCATION:-$REGION}"
prefix="${RESOURCE_PREFIX:-retailsmart}"
env_name="${ENVIRONMENT:-$RS_ENVIRONMENT}"

declare -A bucket_layers=(
  ["${prefix}-${env_name}-data-gcs-landing-rsg"]="landing"
  ["${prefix}-${env_name}-data-gcs-bronze-rsg"]="bronze"
  ["${prefix}-${env_name}-data-gcs-silver-rsg"]="silver"
  ["${prefix}-${env_name}-data-gcs-models-rsg"]="models"
)
existing_buckets=""
existing_locations=""
if ! $DRY_RUN; then
  existing_locations="$(gcloud_run storage buckets list --format='csv[no-heading](name,location)')"
fi

for bucket in "${!bucket_layers[@]}"; do
  layer="${bucket_layers[$bucket]}"
  if $DRY_RUN; then
    log "DRY-RUN verificar/crear bucket: $bucket ($layer)"
    continue
  fi
  if actual_location="$(awk -F, -v bucket="$bucket" '$1 == bucket {print $2}' <<<"$existing_locations")"; [[ -n "$actual_location" ]]; then
    if [[ "${actual_location^^}" != "${location^^}" ]]; then
      die "bucket $bucket diverge: ubicación $actual_location, esperado $location"
    fi
    log "Bucket existente conservado: $bucket ($layer)"
    continue
  fi
  labels="project=retailsmart,environment=$env_name,managed_by=retailsmart,layer=$layer,data_classification=internal"
  log "Creando bucket: $bucket ($layer)"
  gcloud_run storage buckets create "gs://$bucket" \
    --location="$location" \
    --uniform-bucket-level-access \
    --pap
  gcloud_run storage buckets update "gs://$bucket" --update-labels="$labels"
done

log "Prefijos contractuales (sin crear objetos de estado):"
log "landing/batch/<producer_id>/"
log "bronze/streaming/raw/ y bronze/batch/raw/"
log "silver/streaming/curated/ y silver/batch/curated/"
log "models/demand/<version>/"
log "El estado sintético externo al laboratorio no se modifica ni almacena aquí automáticamente."
