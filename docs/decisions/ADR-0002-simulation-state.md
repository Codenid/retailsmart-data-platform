# ADR-0002 — Estado de empresa simulado fuera del laboratorio GCP

- **Estado:** Principio aprobado; tecnología pendiente de elegir con el equipo de simulación.
- **Problema:** si destruimos GCP y si batch/streaming corren en días distintos, la empresa debe preservar IDs, historia e inventario.
- **Decisión:** mantener estado canónico y snapshots versionados fuera del `destroy` de GCP. Reproducir mismo escenario con `simulation_id`+snapshot+seed+reloj lógico. Dos apps pueden leer el mismo baseline; escritura concurrente requiere coordinación transaccional.
- **Pendiente:** definir quién aloja el estado compartido, política de respaldo y punto de sincronización entre integrantes.
