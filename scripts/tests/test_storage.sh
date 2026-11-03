#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
grep -q 'id-2fa596f576a84f6293c8fb4acbbcd23f' "$ROOT_DIR/backlog/tasks/RS-004.md"
grep -q 'bronze/streaming/raw' "$ROOT_DIR/scripts/gcp/03-storage.sh"
grep -q 'silver/batch/curated' "$ROOT_DIR/scripts/gcp/03-storage.sh"
bash -n "$ROOT_DIR/scripts/gcp/03-storage.sh"
echo 'test_storage.sh: OK'
