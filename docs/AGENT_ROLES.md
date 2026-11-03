# Roles de trabajo con Codex — sin orquestación multiagente obligatoria

Usar un **solo agente ejecutor** y seleccionar instrucciones por Issue. No levantar una plataforma de agentes para construir una plataforma de datos.

| Rol | Responsabilidad | No debe hacer |
|---|---|---|
| Architecture Reviewer | Validar componentes y relaciones de vista 08, ADRs y dependencias | Agregar recursos no modelados sin aprobación |
| GCP Provisioner | Bash/gcloud, IAM, red, buckets, topics, Dataflow/Dataproc/Airflow y destrucción segura | Ejecutar recursos costosos sin aprobación |
| Streaming Engineer | Beam/Dataflow, eventos, Bronze/Silver/Gold, Pub/Sub y auditoría | Alterar contratos sin versionado |
| Batch Engineer | Landing, PySpark/Dataproc, DAG Airflow, forecast y Gold | Generar entidades con IDs ajenos al universo común |
| Data QA | Integridad, replay, calidad, fixtures, conteo, latencias y errores | Afirmar evidencias GCP no verificadas |

El **usuario** aprueba diseño, costos y despliegues; Codex implementa tareas pequeñas y devuelve evidencia.
