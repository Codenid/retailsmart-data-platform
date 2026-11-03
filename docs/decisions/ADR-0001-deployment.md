# ADR-0001 — Bash + gcloud como mecanismo de aprovisionamiento

- **Estado:** Aprobada en conversación.
- **Contexto:** laboratorio académico efímero en una cuenta GCP con créditos promocionales; objetivo de replicabilidad sin sobreingeniería.
- **Decisión:** bash + gcloud/bq/gsutil donde aplique. No Terraform. Todos los scripts con preflight, check-exists con diferenciación de errores, validación de configuración, ejecución repetible y destroy explícito.
- **Consecuencias:** no tendremos un state declarativo de Terraform. La fuente de verdad de nombres, parámetros y checks será `config/` y las comprobaciones reales en GCP.
- **Prohibido:** interpretar errores de permiso como inexistencia o borrar recursos sin ownership conocido.
