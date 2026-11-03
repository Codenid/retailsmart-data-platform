#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }
die() { log "ERROR: $*" >&2; return 1; }
require_command() { command -v "$1" >/dev/null 2>&1 || die "comando requerido no encontrado: $1"; }
require_var() { [[ -n "${!1:-}" ]] || die "variable requerida: $1"; }

load_config() {
  local config_file="${1:-.env}"
  [[ -f "$config_file" ]] && # shellcheck disable=SC1090
    source "$config_file"
  export PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
  export REGION="${REGION:-us-central1}"
  export ZONE="${ZONE:-us-central1-a}"
  export RS_ENVIRONMENT="${RS_ENVIRONMENT:-lab}"
  export RS_LABELS="retailsmart=true,environment=${RS_ENVIRONMENT},managed-by=retailsmart"
  require_var PROJECT_ID
}

gcloud_run() { gcloud --project="$PROJECT_ID" "$@"; }
resource_exists() {
  local kind="$1" name="$2"
  case "$kind" in
    bucket) gcloud_run storage buckets describe "gs://$name" >/dev/null 2>&1 ;;
    topic) gcloud_run pubsub topics describe "$name" >/dev/null 2>&1 ;;
    subscription) gcloud_run pubsub subscriptions describe "$name" >/dev/null 2>&1 ;;
    dataset) gcloud_run bigquery datasets describe "$name" >/dev/null 2>&1 ;;
    service-account) gcloud_run iam service-accounts describe "$name" >/dev/null 2>&1 ;;
    *) die "tipo de recurso no soportado: $kind"; return 1 ;;
  esac
}

require_project_context() {
  require_command gcloud
  [[ "$(gcloud config get-value project 2>/dev/null)" == "$PROJECT_ID" ]] || die "gcloud no apunta a PROJECT_ID=$PROJECT_ID"
  gcloud_run projects describe "$PROJECT_ID" --format='value(projectId)' >/dev/null || die "no se pudo verificar el proyecto"
}
