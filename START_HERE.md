# Empieza aquí — primera sesión con Codex

## 1. Revisa la base

```bash
bash scripts/verify-local.sh
```

Debe confirmar **94 elementos, 165 relaciones, 6 productores batch, 6 streaming**. No necesita GCP.

## 2. Publica el repo privado en GitHub

Sigue el README. La carpeta descargada todavía no constituye un repositorio remoto.

## 3. Primera instrucción para Codex

```text
Actúa como implementador del proyecto RetailSmart. Lee AGENTS.md, docs/PRODUCT.md,
docs/ROADMAP.md, architecture/inventory/view08-gcp-mapping.csv y
backlog/tasks/RS-003.md. Propón el plan de implementación SOLO para RS-003:
archivos, APIs, cuentas/roles, guardrails de costos, secuencia de scripts
idempotentes, pruebas, pasos manuales de verificación en GCP y rollback.
NO ejecutes comandos que escriban en GCP todavía. NO avances a otros Issues.
Primero entrégame el plan para aprobarlo.
```

Después de aprobar, responde a Codex: **«Implementa RS-003 sin desplegar. Ejecuta únicamente pruebas locales. Entrega comandos para que yo valide manualmente en Cloud Shell.»**

## 4. Contratos en paralelo

El responsable de datos/simuladores puede preparar `RS-002` simultáneamente. Ambos frentes comparten `architecture/inventory` y AGENTS.md. Los flujos G2/G3 esperan que los contratos estén acordados.
