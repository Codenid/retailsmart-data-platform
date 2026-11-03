# Universo de datos de empresa sintética — contrato conceptual

## Principio esencial
La empresa ficticia **evoluciona** en el tiempo. Ejecutar streaming hoy y batch mañana no reinicia el catálogo ni reinventa IDs. La semilla aleatoria no sustituye a un estado de negocio persistente.

## Entidades maestras y claves canónicas
- `region_id`, `business_unit_id`, `store_id`, `warehouse_id`.
- `product_id` / `sku_id`, `customer_id`.
- `order_id`, `order_line_id`, `delivery_id`, `vehicle_id`.
- `asset_id`, `sensor_id`, `campaign_id`, `supplier_id` según caso.

Definir tipos, cardinalidades, catálogo inicial y reglas de referencia en `config/contracts/` durante RS-002. Ningún productor genera su propio namespace independiente de IDs.

## Metadatos comunes (envelope)
`simulation_id`, `scenario_id`, `producer_id`, `event_id` o `batch_id`, `schema_version`, `occurred_at`, `emitted_at`, `trace_id`. Las llegadas conservan aparte `ingested_at` y metadatos de fuente. Los eventos y archivos llevan la misma fecha lógica empresarial.

## Estado y replay
- Mantener un **estado canónico** (baseline inmutable + cambios) en un almacenamiento externo al laboratorio GCP; tecnología por decidir con el equipo de simulación (SQLite compartido mediante artefactos versionados, backend centralizado, o snapshots coordinados). Dos computadoras **no deben editar copias SQLite independientes**.
- Guardar snapshots versionados (`snapshot_id`, `effective_at`) y cursor de simulación. Cada nuevo escenario inicia desde snapshot conocido y puede avanzar cronológicamente.
- Pedidos confirmados afectan inventario; entregas refieren pedidos; sensores refieren activos y ubicaciones reales. Batch publica snapshots coherentes *después* de los eventos hasta el cutoff temporal correspondiente.
- `destroy.sh` **nunca elimina** el estado canónico. Al reconstruir GCP se puede reingestar desde un baseline/export reproducible.

## Calidad: datos válidos antes de defectos
Configuración **por productor y escenario**, en porcentajes: `missing_rate`, `duplicate_rate`, `late_rate`, `out_of_order_rate`, `outlier_rate`, `invalid_reference_rate`, `schema_error_rate`, `malformed_rate`. No todos los defectos tienen sentido para todos los tipos de mensajes.

Se genera primero una verdad válida; luego una **proyección defectuosa** a publicar. Registrar `original_record_id`, defecto aplicado y semilla/cursor fuera del payload de negocio cuando sea necesario. Las tasas reales pueden diferir de las deseadas por volumen pequeño; reportar ambas.

## Los cuatro casos requieren consecuencias
1. Black Friday → alta demanda → decremento stock → quiebre → insights despacho.
2. Demanda/histórico/eventos → estimación → plan de reposición por SKU/almacén.
3. Canales + pedidos + logística + ERP → ventas, conversión, costo y SLA.
4. Frigoríficos/sensores → degradación progresiva → anomalía → riesgo de mantenimiento.

## Contratos entre equipos
Los productores son otros componentes/proyectos. Intercambian `streaming-envelope` JSON para Pub/Sub y archivos batch con manifest JSON e integridad/metadata. La versión de contrato se acuerda **antes** de desplegar pipelines definitivos.
