#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true
prefix="${RESOURCE_PREFIX:-retailsmart}-${ENVIRONMENT:-$RS_ENVIRONMENT}-str-ps"
labels="project=retailsmart,environment=${ENVIRONMENT:-$RS_ENVIRONMENT},managed_by=retailsmart,domain=streaming"
if $DRY_RUN; then
  topics=("$prefix-events" "$prefix-insights" "$prefix-audit")
  subscriptions=("$prefix-events-raw:$prefix-events" "$prefix-events-dataflow:$prefix-events" "$prefix-insights-consumers:$prefix-insights" "$prefix-audit-analytics:$prefix-audit")
  for topic in "${topics[@]}"; do log "DRY-RUN verificar/crear topic $topic"; done
  for spec in "${subscriptions[@]}"; do log "DRY-RUN verificar/crear subscription ${spec%%:*}"; done
  exit 0
fi
existing_topics="$(gcloud_run pubsub topics list --format='value(name)' | sed 's#.*/##')"
if ! grep -Fxq "$prefix-events" <<<"$existing_topics" && grep -Fxq "rs-${ENVIRONMENT}-str-ps-events" <<<"$existing_topics"; then
  prefix="rs-${ENVIRONMENT}-str-ps"
  log "Reutilizando convención existente de Pub/Sub: $prefix"
fi
topics=("$prefix-events" "$prefix-insights" "$prefix-audit")
subscriptions=("$prefix-events-raw:$prefix-events" "$prefix-events-dataflow:$prefix-events" "$prefix-insights-consumers:$prefix-insights" "$prefix-audit-analytics:$prefix-audit")
for topic in "${topics[@]}"; do
  if grep -Fxq "$topic" <<<"$existing_topics"; then
    log "Topic existente conservado: $topic"
  else
    log "Creando topic: $topic"
    gcloud_run pubsub topics create "$topic" --labels="$labels"
  fi
done
existing_subscriptions="$(gcloud_run pubsub subscriptions list --format='value(name)' | sed 's#.*/##')"
for spec in "${subscriptions[@]}"; do
  subscription="${spec%%:*}"
  topic="${spec##*:}"
  if grep -Fxq "$subscription" <<<"$existing_subscriptions"; then
    log "Suscripción existente conservada: $subscription"
  else
    log "Creando suscripción: $subscription → $topic"
    gcloud_run pubsub subscriptions create "$subscription" --topic="$topic" --ack-deadline=60 --expiration-period=604800s
  fi
done
