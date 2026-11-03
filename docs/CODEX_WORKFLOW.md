# Trabajo incremental con Codex (VS Code)

## Preparación (una vez)
1. Abre la carpeta raíz `retailsmart-data-platform` en VS Code.
2. Verifica `bash scripts/verify-local.sh`.
3. Inicializa Git y crea tu repositorio privado (ver README).
4. Abre `AGENTS.md` y `backlog/tasks/RS-003.md` (primer incremento GCP, tras aprobar RS-001).
5. Comienza con un chat/tarea de Codex nuevo y acotado para cada Issue.

## Prompt mínimo reutilizable

> Trabaja en RetailSmart. Lee primero `AGENTS.md`, `docs/PRODUCT.md`, `docs/ROADMAP.md` y `backlog/tasks/RS-XXX.md`. Implementa **solo la fase autorizada** y sus incrementos dependientes. Dentro de ella puedes editar, probar, consultar y aprovisionar sin pedir aprobación por cada paso. Antes de crear Composer, clústeres persistentes o recursos de costo fijo significativo, muestra estimación y solicita autorización. Después ejecuta `bash scripts/verify-local.sh`, reporta el resultado y entrega los pasos de verificación manual en GCP.

## Ciclo de control
`Issue → rama → plan Codex → revisión humana → código → tests → verificación GCP manual → PR → merge → siguiente Issue`.

- Usa ramas `feat/RS-XXX-descripcion`.
- Trabajos sobre IAM, presupuesto, destrucción y servicios de coste fijo **requieren revisión manual antes de despliegue**.
- Cuando Codex proponga un producto fuera de la vista 08, exige **ADR** y justificación antes de aceptar.
- En sesiones nuevas no pegues el historial de toda la conversación: referencia archivos versionados. Esto reduce contexto y trabajo repetitivo.

## Presupuesto de iteración por Issue
- **1 Issue por tarea de Codex**; no continuar al siguiente sin aprobación.
- **Hasta 3 intentos correctivos por fallo**. Si continúa fallando, detenerse y pedir decisión.
- La fase se aprueba como unidad; los incrementos internos continúan automáticamente mientras no exista un bloqueo de seguridad o costo.
- No usar prompts como «reintenta hasta que funcione» ni ejecutar bucles sin límite.
- Antes de un comando con potencial de costo, eliminar datos o modificar IAM, solicitar aprobación y mostrar impacto esperado.


> Actualiza el estado del Issue en `backlog/BACKLOG.md` y el runbook correspondiente. Resume archivos cambiados, comandos comprobados, recursos GCP realmente validados (si los hay) y próxima tarea sugerida. No continúes implementando.

## Reglas para ahorro de contexto
- Solicitar plan y revisión del diff antes de modificar múltiples componentes.
- Evitar prompts generales como «implementa todo RetailSmart».
- Partir una tarea si supera un PR revisable o toca más de un pipeline.
- Referenciar IDs/CSV derivados de ArchiMate en lugar de pedir que inspeccione cada vez el archivo XML completo.
