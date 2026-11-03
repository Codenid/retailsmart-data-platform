# Backlog ordenado por dependencias

**Estado real al crear este repositorio:** `RS-001` preparado localmente; todos los demás están `TODO`. Ningún recurso GCP creado. `Criterio de cierre` siempre incluye `código + pruebas + verificación manual en GCP + segunda ejecución segura` cuando corresponda.

| Issue | Gate | Entregable acotado | Depende | Estado |
|---|---|---|---|---|
| RS-001 | G0 | Bootstrap, vista 08, AGENTS.md y pruebas locales | — | PREPARADO |
| RS-002 | G0 | Catálogo y 12 contratos; estados/IDs/manifest comunes al simulador | RS-001 | TODO |
| RS-003 | G1 | Config GCP, validaciones, APIs habilitadas, IAM base, budgets/alertas propuestas | RS-001 | TODO |
| RS-004 | G1 | Storage: Landing/Bronze/Silver; buckets y estructuras idempotentes | RS-003 | TODO |
| RS-005 | G1 | Mensajería: retail/audit/insights, subscriptions y políticas | RS-003 | TODO |
| RS-006 | G1 | Dataflow, Dataproc, Airflow, BigQuery, Cloud Run, catálogo/seguridad: recursos y configuraciones + costo + status, sin jobs activos si no hay pruebas | RS-003/004/005 | TODO |
| RS-007 | G2 | Fixture de seis productores streaming compatible con contratos | RS-002/005 | TODO |
| RS-008 | G2 | Raw Event Writer: Pub/Sub → Bronze immutable, reintentos y auditabilidad | RS-004/005/007 | TODO |
| RS-009 | G2 | Ingesta Streaming Beam/Dataflow → Silver, calidad/quarantine, DLQ | RS-006/007 | TODO |
| RS-010 | G2 | Procesamiento tiempo real + insights; telemetría y mantenimiento base | RS-009 | TODO |
| RS-011 | G2 | Gold Insights Writer + tópico Insights + pruebas streaming E2E | RS-010 | TODO |
| RS-012 | G3 | Fixtures/manifest para seis productores batch y landing | RS-002/004 | TODO |
| RS-013 | G3 | Ingesta Batch planificada: Landing → Bronze, control `batch_id`/replay | RS-006/012 | TODO |
| RS-014 | G3 | Curación PySpark/Dataproc → Silver, calidad y cuarentena | RS-013 | TODO |
| RS-015 | G3 | DAG Airflow y pipelines secuenciales automáticos | RS-013/014 | TODO |
| RS-016 | G3 | Forecast/Modelo de Demanda, scoring y Gold Planes Inventario | RS-014/015 | TODO |
| RS-017 | G4 | Operational Mart de Silver streaming + Silver batch | RS-011/016 | TODO |
| RS-018 | G4 | API RetailSmart Insights con 4 rutas de consulta; reporting mínimo | RS-011/016/017 | TODO |
| RS-019 | G5 | Pruebas de negocio CU01 y CU02, fixtures con consecuencias | RS-018 | TODO |
| RS-020 | G5 | Pruebas CU03 y CU04, entrenamiento PdM e integración, demo global | RS-019 | TODO |
| RS-021 | G6 | Knowledge Catalog, metadatos, owners y lineage con evidencia | RS-011/016 | TODO |
| RS-022 | G6 | Seguridad avanzada KMS/DLP, políticas de retención, observabilidad | RS-021 | TODO |
| RS-023 | G6 | Runbook create/status/destroy, costo real, recuperación y demo final | RS-020/022 | TODO |

## Cómo cerrar un Issue
- [ ] Respeta `archimate_id` y capacidad de la vista 08.
- [ ] Tests verdes + fallos previstos contemplados.
- [ ] Script ejecutado 2 veces sin duplicación ni cambios inesperados (si aplica).
- [ ] Fixture de prueba pequeño generado automáticamente.
- [ ] Pasos manuales en consola con resultado esperado y limpieza.
- [ ] PR revisada y próxima tarea independiente identificada.

## Dependencia externa explícita
El equipo de simulación puede construir su código fuera de este repo, pero debe adherirse a `config/contracts/`. Este backlog implementa **fixtures de validación mínimas** para que la plataforma no dependa de su disponibilidad.

## Orden de prioridad
G1 y RS-002 en paralelo → streaming G2 → batch G3 → consumo G4 → 4 casos G5 → gobierno ampliado G6. Sin embargo, **IAM, auditoría, calidad básica y trazabilidad** se integran desde G1/G2/G3, no se difieren.
