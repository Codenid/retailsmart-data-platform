# Contratos entre simuladores y plataforma

Este directorio define el **protocolo propuesto**; debe aprobarse con el equipo productor antes de codificar pipelines. RS-002 definirá los 12 datasets y diccionarios completos.

- `streaming-envelope.example.json`: evento, identidad del productor, trazabilidad y tiempo.
- `batch-manifest.example.json`: entrega de archivo, corte temporal, checksum, partición, versión.
- `quality-profile.example.json`: tasas de defectos controladas (por productor/escenario).

RS-002 añade los contratos definitivos en `streaming/` y `batch/`, los esquemas
comunes `streaming-envelope.schema.json` y `batch-manifest.schema.json`, y el
diccionario `RS-002-DICCIONARIO.md`.
