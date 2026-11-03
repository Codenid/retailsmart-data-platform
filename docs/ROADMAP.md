# Roadmap incremental — control de avance

> Las fechas son objetivo, no certificación de cumplimiento. Priorizar los hitos esenciales antes del vencimiento de créditos el 20 de noviembre de 2026.

| Gate | Incremento | Dependencias | Evidencia mínima |
|---|---|---|---|
| G0 | **Bootstrap y fuente de verdad** (RS-001) | Ninguna | Vista 08 exportada; 94 elementos, 165 relaciones; 6+6 productores; tests verdes |
| G1 | **Aprovisionamiento completo GCP** (RS-003 a RS-006) | G0 | `create`/`status` reejecutables; servicios definidos; capturas/manual de consola; costo revisado |
| G2 | **Streaming E2E** (RS-007 a RS-011) | G1, contratos RS-002 | Fixture publica 6 tipos → Pub/Sub → raw Bronze + Dataflow → Silver/Gold → insights y auditoría |
| G3 | **Batch E2E** (RS-012 a RS-016) | G1, contratos RS-002 | 6 archivos → Landing → Airflow → Spark → Bronze/Silver → forecast/planes Gold; repetición segura |
| G4 | **Integración y exposición** (RS-017/RS-018) | G2+G3 | Mart combinado, endpoint Cloud Run y consultas reproducibles |
| G5 | **Cuatro casos de uso y demos** (RS-019/RS-020) | G4 | Resultados esperados vs reales, scripts de fixtures y README por caso |
| G6 | **Gobierno ampliado, lineage y cierre** (RS-021 a RS-023) | G2/G3 | Catálogo, linaje, controles, runbooks y evidencia de recreación/limpieza |

RS-002 (contratos de los 12 productores) puede desarrollarse **en paralelo** al aprovisionamiento G1, con su propia revisión. No debe bloquear la creación de recursos independientes del esquema.

## Construir primero; activar progresivamente
G1 aprovisiona **todos los recursos declarados** en la arquitectura (o registra explícitamente la limitación), pero Dataflow, Airflow y Dataproc pueden tener coste significativo. Los jobs deben poder estar definidos pero **sin cómputo activo** fuera de pruebas cuando el servicio lo permita. En G1, `status` debe distinguir `provisioned`, `configured`, `executing` y `validated`.

## Entregas mínimas de cada Issue
1. Código y parámetros reutilizables sin secretos.
2. Comprobación de idempotencia (ejecutar dos veces, cuando tenga efectos).
3. `tests/fixtures/` o script de prueba con datos pequeños.
4. Documento `docs/runbooks/RS-XXX.md` con navegación paso a paso en la consola GCP, resultado esperado, costo y limpieza.
5. Evidencia y estado en backlog.

## Riesgos a decidir antes de G1
- **Costo/tiempo de arranque** de Managed Airflow y trabajos Dataflow/Dataproc. Incluir estimación/alerta de presupuesto; si limita la demo, documentar alternativa con ADR antes de sustituir.
- **Accesos IAM / APIs y cuotas** del proyecto personal.
- **Discrepancias del modelo:** documentación Kafka vs propiedad Pub/Sub; auditar y aprobar tecnología canónica (véase ADR-0003).
- **Estado externo al laboratorio** y coordinación entre productores de diferentes personas/ordenadores.

## Fases streaming y batch: independientes, no aisladas
El simulador es un productor externo. Ambos flujos tienen contratos, identificadores y calendario empresarial compartido. Bronze/Silver/Gold se separan por modalidad según la vista, y el **Operational Mart** consolida datos curados de ambos caminos.
