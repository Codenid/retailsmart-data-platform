#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
grep -q 'id-ded4a7cf707743008e148981bac087e2' "$ROOT_DIR/backlog/tasks/RS-005.md"
grep -q 'events-raw' "$ROOT_DIR/scripts/gcp/04-pubsub.sh"
grep -q 'audit-analytics' "$ROOT_DIR/scripts/gcp/04-pubsub.sh"
bash -n "$ROOT_DIR/scripts/gcp/04-pubsub.sh"
echo 'test_pubsub.sh: OK'
