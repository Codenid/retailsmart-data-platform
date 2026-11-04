# RS-002 — Diccionario canónico

## Claves

`region_id`, `business_unit_id`, `store_id`, `warehouse_id`, `product_id`,
`sku_id`, `customer_id`, `order_id`, `order_line_id`, `delivery_id`,
`vehicle_id`, `asset_id`, `sensor_id`, `campaign_id` y `supplier_id` son IDs
estables, opacos y únicos dentro de la simulación.

## Contratos

Los contratos `streaming/*.json` son JSON Schema para payloads publicados dentro
del envelope común. Los contratos `batch/*.json` describen la fila del archivo
Parquet y comparten el manifest batch.

| Grupo | Productores | Formato | Destino |
|---|---|---|---|
| Streaming | channel-apps, cold-storage-cameras, smart-shelf, store-iot, warehouse-sensors, logistics-tracking | JSON Schema + Pub/Sub envelope | Tópico Eventos Retail |
| Batch | warehouse-app, competitor-benchmark, erp-inventory, local-events, social-media, orders-system | Parquet + manifest JSON | Storage Landing Zone |

Todos los timestamps son RFC 3339 UTC. Las cantidades son no negativas; los
porcentajes están entre 0 y 100; las referencias deben existir en el catálogo
canónico. Los defectos se aplican después de crear el registro válido.
