#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
require_project_context
printf 'project=%s\nregion=%s\n' "$PROJECT_ID" "$REGION"
printf '\n-- service accounts --\n'
gcloud_run iam service-accounts list --filter='labels.retailsmart=true' --format='table(email,disabled)' || true
printf '\n-- buckets --\n'
gcloud_run storage buckets list --filter='labels.retailsmart=true' --format='table(name,location)' || true
printf '\n-- pubsub topics --\n'
gcloud_run pubsub topics list --format='value(name)' || true
printf '\n-- bigquery datasets --\n'
gcloud_run bigquery datasets list --format='table(datasetId,location)' || true
