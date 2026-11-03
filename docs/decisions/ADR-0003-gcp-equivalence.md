# ADR-0003 — Fuente de verdad tecnológica y discrepancias del modelo

- **Estado:** Pendiente de aprobación detallada antes de RS-003.
- **Fuente:** vista `08_integracion_detallada_tobe`, columnas estructuradas de `TechnologyService` del ArchiMate.
- **Observación 1:** tecnologías estructuradas de los tópicos indican **Cloud Pub/Sub**, mientras documentación interna conserva **Kafka/Managed Kafka**.
- **Observación 2:** `Audit Store` indica **Cloud Logging + Observability Analytics**, pero otros textos del modelo pueden referirse a BigQuery para auditoría.
- **Criterio propuesto:** usar **propiedad `Tecnología GCP`** como referencia principal y conservar semántica de las relaciones de la vista; proponer equivalencias solamente mediante ADR y aprobación humana.
- **Costo:** Managed Service for Apache Airflow (Cloud Composer), Dataflow y Dataproc pueden generar consumo incluso con poca carga; diseñar ciclo de vida, configuraciones y alertas antes de aprovisionar.
- **Pendiente:** fijar versión/región/costo y si algún componente se materializa como recurso GCP o artefacto de software, sin perder capacidad.
