# RetailSmart Data Platform — Estado de transferencia

## Objetivo

Implementar incrementalmente en GCP la vista ArchiMate
`08_integracion_detallada_tobe`, manteniendo trazabilidad por `archimate_id`,
idempotencia, control de costos y separación de flujos streaming y batch.

El roadmap completo y sus dependencias están en `docs/ROADMAP.md` y
`backlog/BACKLOG.md`.

## Última tarea y resultado

Se prepararon scripts de ciclo de vida batch bajo demanda para el componente
`id-b31ac9e67a204bd2996043f98f93cec1` (Orquestación Batch / Managed Service for
Apache Airflow / Cloud Composer). No se creó Composer ni se eliminaron recursos.

RS-003, RS-004 y RS-005 están completados en GCP.

## Infraestructura operativa

Proyecto: `retailsmart-bigdata`, región: `us-central1`.

- APIs fundacionales verificadas/habilitadas en RS-003.
- Storage: cuatro buckets `retailsmart-dev-data-gcs-{landing,bronze,silver,models}-rsg`.
- Pub/Sub: topics `rs-dev-str-ps-events`, `rs-dev-str-ps-insights`, `rs-dev-str-ps-audit`.
- Pub/Sub: suscripciones raw, Dataflow, insights y auditoría.
- Composer fue creado como `retailsmart-batch` y continúa en estado `CREATING`; aún no está validado como `RUNNING`. BigQuery ya tiene `retailsmart_gold_insights`, `retailsmart_operational_mart` y `retailsmart_audit` en `US`. Dataproc, Storage Transfer, Dataflow jobs y DAGs aún no están activos.

## Validaciones

- `bash scripts/verify-local.sh`: OK; 6 pruebas de arquitectura.
- `bash scripts/tests/test_storage.sh`: OK.
- `bash scripts/tests/test_pubsub.sh`: OK.
- `bash scripts/tests/test_batch_lifecycle.sh`: OK.
- RS-004: segunda ejecución de Storage terminó `RC=0` sin duplicados.
- RS-005: segunda ejecución de Pub/Sub terminó `RC=0` sin duplicados.
- RS-006 parcial: tres datasets BigQuery creados y segunda ejecución terminó `RC=0` sin duplicados.
- Cloud Console/gcloud confirmó ubicación, acceso uniforme, prevención pública,
  topics, suscripciones, ack deadline y expiración.

## Riesgos y limitaciones

- Composer tiene costo fijo; debe crearse solo para una prueba/demo y luego
  hibernarse o eliminarse según el ciclo autorizado.
- Los scripts batch requieren `CLOUDSDK_CONFIG` escribible y credenciales de
  usuario; no usan claves de service account.
- La ejecución Cloud necesita `gcloud`, autenticación activa, acceso al proyecto
  y billing habilitado.
- Algunas consultas gcloud presentaron latencia y consistencia eventual; los
  scripts fueron optimizados para inventarios agrupados e idempotencia.
- No ejecutar `destroy` sin `PROJECT_ID`, aprobación aplicable y confirmación.
- Composer usa `rs-dev-batch-sa-composer@retailsmart-bigdata.iam.gserviceaccount.com` con `roles/composer.worker`; no se crearon claves.

## Archivos relevantes

- `AGENTS.md`
- `docs/ROADMAP.md`
- `backlog/BACKLOG.md`
- `scripts/gcp/03-storage.sh`
- `scripts/gcp/04-pubsub.sh`
- `scripts/gcp/05-batch-create.sh`
- `scripts/gcp/95-batch-destroy.sh`
- `docs/runbooks/RS-003.md`, `RS-004.md`, `RS-005.md` y `BATCH_LIFECYCLE.md`
- `architecture/inventory/view08-gcp-mapping.csv`

## Continuación en Cloud

Pruebas locales:

```bash
bash scripts/verify-local.sh
bash scripts/tests/test_batch_lifecycle.sh
```

Preflight GCP:

```bash
export CLOUDSDK_CONFIG=/tmp/retailsmart-gcloud
gcloud auth login
gcloud config set project retailsmart-bigdata
```

No se requieren Windows, Archi ni jArchi para continuar con RS-006. El modelo
ArchiMate fuente y sus CSV ya están versionados. No incluir `.env`, credenciales,
datos reales ni estados locales en Git.

## Próxima tarea recomendada

Continuar RS-006 cuando Composer pase a `RUNNING`: verificar consola y estado,
registrar evidencia y preparar únicamente los componentes restantes declarados
en el mapping GCP. No marcar RS-006 como completado mientras siga `CREATING`.

## Git

Rama: `main`.

El commit de transferencia se registrará y publicará después de validar estos
archivos.
