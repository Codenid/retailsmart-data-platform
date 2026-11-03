#!/usr/bin/env bash
# Read-only checks. --local requires no GCP tooling.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "${1:-}" == "--local" ]]; then
  python3 "$ROOT/scripts/export_architecture.py"
  python3 -m unittest discover -s "$ROOT/tests" -p 'test_*.py' -v
  exit 0
fi
if [[ ! -f "$ROOT/.env" ]]; then
  echo "ERROR: falta .env. Ejecuta: cp .env.example .env" >&2
  exit 2
fi
# shellcheck disable=SC1091
set -a; source "$ROOT/.env"; set +a
for v in PROJECT_ID REGION BQ_LOCATION RESOURCE_PREFIX; do
  if [[ -z "${!v:-}" ]]; then echo "ERROR: falta $v" >&2; exit 2; fi
done
if [[ "$PROJECT_ID" == "your-gcp-project-id" ]]; then
  echo "ERROR: configura un PROJECT_ID válido en .env" >&2; exit 2
fi
if ! command -v gcloud >/dev/null 2>&1; then
  echo 'ERROR: gcloud no está instalado. Usa Cloud Shell o instala Google Cloud CLI.' >&2
  exit 2
fi
if ! gcloud auth list --filter='status:ACTIVE' --format='value(account)' 2>/dev/null | grep -q .; then
  echo 'ERROR: sin cuenta gcloud activa. Ejecuta gcloud auth login.' >&2
  exit 2
fi
# No interpretar ausencia de permisos como recurso inexistente.
if ! gcloud projects describe "$PROJECT_ID" --format='value(projectId)' >/dev/null; then
  echo "ERROR: no se pudo validar acceso a $PROJECT_ID" >&2
  exit 3
fi
printf 'Preflight OK: proyecto accesible=%s region=%s bq=%s prefijo=%s\n' \
  "$PROJECT_ID" "$REGION" "$BQ_LOCATION" "$RESOURCE_PREFIX"
echo 'No se ha creado ni modificado ningún recurso.'
