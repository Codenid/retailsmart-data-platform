# Ciclo de vida de la demo completa

## Crear

```bash
export CLOUDSDK_CONFIG=/tmp/retailsmart-gcloud
export DEMO_CREATE_APPROVED=true
export BATCH_CREATE_APPROVED=true
bash scripts/gcp/demo-create.sh --dry-run
bash scripts/gcp/demo-create.sh
bash scripts/gcp/demo-status.sh
```

Para iniciar Dataflow se requiere además ADC y `DEMO_START_DATAFLOW=true`.
El job streaming debe limitarse a un worker y cancelarse al terminar la prueba.

## Destruir

```bash
export DEMO_DESTROY_APPROVED=true
bash scripts/gcp/demo-destroy.sh
```

El script solicita `ELIMINAR-DEMO` y elimina Composer mediante el script
existente. Conserva Storage, Pub/Sub, BigQuery, contratos y el estado sintético.
Los jobs Dataflow activos se revisan antes de la baja y requieren cancelación
explícita por ID.

Dataproc y Cloud Run se incorporarán al mismo ciclo cuando existan un job PySpark
y una imagen de API versionados; el orquestador informa esa condición y no crea
recursos vacíos.
