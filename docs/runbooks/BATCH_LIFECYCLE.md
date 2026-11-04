# Ciclo de vida batch bajo demanda

Los scripts preparan el entorno real de **Managed Service for Apache Airflow /
Cloud Composer** de la arquitectura (`id-b31ac9e67a204bd2996043f98f93cec1`).
No se ejecutan automáticamente.

## Crear

```bash
export CLOUDSDK_CONFIG=/tmp/retailsmart-gcloud
export BATCH_CREATE_APPROVED=true
bash scripts/gcp/05-batch-create.sh --dry-run
bash scripts/gcp/05-batch-create.sh
gcloud composer environments describe retailsmart-batch \
  --location=us-central1 --format='yaml(name,state)'
```

El entorno tiene costo fijo. Debe crearse solo durante una prueba o demo y no
carga DAGs automáticamente. El script crea, si falta, la cuenta dedicada
`rs-dev-batch-sa-composer@retailsmart-bigdata.iam.gserviceaccount.com` con
`roles/composer.worker`; no genera claves.

## Destruir

```bash
export BATCH_DESTROY_APPROVED=true
bash scripts/gcp/95-batch-destroy.sh
```

El script exige escribir `ELIMINAR` y solo elimina el entorno Composer indicado.
No elimina Storage, datos ni estado persistente. Los jobs Dataproc efímeros y
transferencias se agregarán cuando sus tareas de implementación estén listas.
