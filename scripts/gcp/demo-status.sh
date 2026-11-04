#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/lib/common.sh"
load_config "${CONFIG_FILE:-$ROOT_DIR/.env}"
require_project_context
printf 'project=%s\nregion=%s\n' "$PROJECT_ID" "$REGION"
bash "$ROOT_DIR/scripts/gcp/02-status.sh" || true
gcloud_run composer environments list --locations="$REGION" --format='table(name,state)' || true
gcloud_run dataflow jobs list --region="$REGION" --format='table(id,name,state)' || true
