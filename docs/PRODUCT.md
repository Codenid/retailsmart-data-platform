# Producto y alcance

## Problema de negocio
RetailSmart integra canales, inventarios y logística de 12 unidades de negocio en ocho regiones. La plataforma habilita respuestas ante picos de demanda, planificación de stock, reportes operativos y mantenimiento proactivo.

## Arquitectura obligatoria
Única fuente de verdad: `architecture/source/RetailSmart_ArquitecturaSolucion.archimate`, vista `08_integracion_detallada_tobe`. Extraída con `python3 scripts/export_architecture.py` a CSV. Los `ApplicationComponent` externos son **simulados**, los internos son **implementados**; los `DataObject` son contratos/artefactos, no necesariamente un servicio GCP propio.

## Objetivos funcionales
- Streaming E2E: **6 fuentes** publican eventos → Pub/Sub retail → persistencia raw en Bronze en paralelo al procesamiento Beam/Dataflow → Silver → Gold/insights → Pub/Sub insights. Auditoría del procesamiento de manera transversal.
- Batch E2E: **6 fuentes** publican archivos → Landing en GCS → orquestador → ingesta/curación PySpark/Dataproc → Bronze/Silver → forecast/planificación → Gold.
- Mart operativo con unión de Silver streaming/batch; API Cloud Run y consumidores según vista 08.
- Gobierno: cuentas de servicio/IAM desde el día uno; contrato, clasificación, calidad, auditoría; Knowledge Catalog/lineage/DLP en hitos independientes y sin bloquear el E2E.

## Cuatro casos de uso (criterios de negocio)
| Caso | Entradas principales | Salida observable |
|---|---|---|
| CU01 Decisiones en tiempo real | Canal, estanterías, stock, tracking | Insight de riesgo de quiebre y decisión de despacho |
| CU02 Planificación diaria | Pedidos, inventario, almacenes, eventos externos | Plan de reposición por SKU/almacén/día |
| CU03 Informes operativos | Ventas, logística, ERP, competencia | KPIs de conversión, costo, entrega y ventas |
| CU04 Mantenimiento proactivo | Frigoríficos, sensores almacén, IoT | Anomalía/alerta de mantenimiento con activo y ubicación |

Los **12 productores** emiten datos aunque un demo solo necesite una selección. Usar fixtures autónomos inicialmente; integrar los simuladores del equipo mediante contrato después.

## Restricciones aceptadas
GCP personal con créditos promocionales hasta **20 nov 2026** (verificar saldo y fechas reales antes de desplegar); laboratorio efímero, scripts create/status/destroy; no Terraform; arquitectura fiel a la vista 08, equivalencias solo con ADR; estado de empresa sintética persistente fuera del laboratorio; calidad configurable.

## Definición de producto funcional
No basta con recursos creados. Para cada ruta: productor/fixture → recepción → almacenamiento → procesamiento → consumidor y verificación manual. La ausencia de datos, la entrega duplicada y un evento inválido también deben tener comportamiento documentado.
