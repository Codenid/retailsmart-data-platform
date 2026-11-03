# AGENTS.md — Contrato de trabajo para Codex

## Misión
Implementar **RetailSmart Data Platform** en GCP, reproducible, trazable y verificable, mediante incrementos pequeños. El modelo `architecture/source/RetailSmart_ArquitecturaSolucion.archimate`, **vista `08_integracion_detallada_tobe`**, es la fuente de verdad arquitectónica.

## Leer antes de editar
1. `README.md` (estado real del proyecto).
2. `docs/PRODUCT.md` (objetivo y reglas de negocio).
3. `docs/ROADMAP.md` (fases, entregables y gates).
4. `backlog/BACKLOG.md` y SOLO la tarea elegida en `backlog/tasks/`.
5. `architecture/inventory/view08-elements.csv`, `view08-relations.csv`, `view08-producers.csv`.
6. `docs/DATA_UNIVERSE.md` cuando la tarea toque datos o pipelines.

## Límites obligatorios
- **No inventar ni omitir componentes** de la vista 08. Identificar cada implementación con su `archimate_id`. Una equivalencia requiere ADR aprobada.
- **Sin Terraform**, sin Kubernetes y sin frameworks adicionales por comodidad. Bash + gcloud; Python/Beam/PySpark/SQL según el componente definido.
- Los scripts GCP serán **idempotentes**: si existe verificar estado/configuración; si coincide, conservar; si diverge, informar y pedir decisión. `PERMISSION_DENIED` NO significa que el recurso no exista.
- Dentro de una fase de aprovisionamiento explícitamente autorizada, Codex puede implementar, probar, consultar y ejecutar cambios en el proyecto configurado sin pedir aprobación por cada paso. Se mantiene aprobación humana explícita para proyectos, billing, IAM fuera del alcance aprobado, recursos de costo fijo significativo, publicación externa y destrucción. Para destruir se exige `PROJECT_ID` y confirmación explícita. Nada de `--quiet` en destrucción por defecto.
- No copiar secretos ni credenciales a Git. Preferir credenciales de usuario de Cloud Shell o identidad adjunta a runtime; evitar service-account keys.
- **El estado de la empresa sintética sobrevive** a `destroy.sh`: nunca eliminarlo desde los scripts del laboratorio.
- Mantener **seis productores streaming y seis batch**; los casos de uso pueden consumir subconjuntos pero el universo se produce completo.
- Contratos y claves compartidas para los dos caminos. Los defectos de calidad se inyectan de forma configurable **después** de crear el evento válido y con trazabilidad del original.
- No sustituir Dataflow, Dataproc, Airflow administrado, Knowledge Catalog, Looker u otras tecnologías de la vista 08 sin un ADR y aprobación. Controlar costos y ciclo de vida. Antes de crear Composer, clústeres persistentes o cualquier recurso de costo fijo significativo, mostrar estimación y solicitar autorización.
- Cada incremento entrega `script + prueba automatizada de datos pequeños + guía de verificación manual en GCP`.
- Preferir código directo, funciones pequeñas, stdlib cuando sea suficiente; sin abstracciones genéricas ni cambios fuera del Issue.
- Streaming: conservar las bifurcaciones de `Tópico Eventos Retail` hacia raw y procesamiento de baja latencia; no serializarlas artificialmente.
- Batch: Landing → planificación/orquestación → Bronze → Silver → Gold; gestionar cargas duplicadas mediante batch_id/file_id.
- La capa Gold puede tener productos propios de cada flujo y un **Operational Mart** combinado; distinguirlos.

## Flujo obligatorio de cada Issue
1. **Inspeccionar** solo los archivos necesarios.
2. **Plan breve**: archivos a modificar, dependencias, riesgo/costo GCP, pruebas.
3. **Implementar** únicamente el Issue actual.
4. **Verificar**: `bash scripts/verify-local.sh` y pruebas específicas.
5. **Reportar**: cambios, pruebas ejecutadas/resultados, pasos manuales GCP, riesgos, pendientes.
6. **Detenerse**: esperar confirmación antes de iniciar otro Issue o ejecutar cambios GCP.

## Control estricto de iteraciones y autonomía
- **No ejecutar ciclos autónomos entre Issues.** Un Issue por sesión/tarea; el cierre exige detenerse y esperar nueva instrucción del usuario.
- **Autonomía por fase autorizada:** una vez aprobada una fase, implementar, probar, desplegar y verificar sus incrementos dependientes sin pedir aprobación por cada archivo o paso. La autorización no incluye proyectos nuevos, billing, destrucción ni recursos de costo fijo significativo.
- **Presupuesto de corrección:** máximo **3 intentos de solución** ante un mismo fallo. Un intento es: cambiar código/configuración y repetir la prueba afectada. Si persiste el error tras el tercero, detenerse, explicar causa probable y solicitar decisión. No reiniciar el contador cambiando el texto del error sin fundamento.
- **Sin bucles abiertos:** no crear ni ejecutar `while true`, reintentos ilimitados, auto-invocaciones, agentes recursivos o "continúa hasta terminar". Los procesos de streaming de larga duración son una excepción técnica **solo cuando forman parte explícita del Issue**, se ejecutan como servicio supervisado y tienen condiciones de parada/observabilidad.
- **Límite de alcance:** si la tarea revela otra dependencia, riesgo inesperado, necesidad de ADR o ampliación sustancial, detenerse y pedir autorización; no incorporar silenciosamente otro Issue.
- **Límite de herramientas/costo:** preferir comandos puntuales y pruebas pequeñas. No ejecutar pruebas de carga, loops de publicación, creaciones masivas, consultas BigQuery de alto consumo ni servicios costosos sin permiso previo y límites explícitos.
- **Puntos de control obligatorios:** (1) plan aprobado, (2) cambios y pruebas locales reportados, (3) validación/despliegue GCP autorizado por separado, (4) cierre aprobado. No pasar automáticamente de un punto al siguiente.
- **Al bloquearse:** entregar resumen de lo probado, error exacto, archivos modificados y máximo dos opciones de continuación; esperar decisión humana.
- Estas reglas son **instrucciones operativas**, no un límite técnico impuesto por `AGENTS.md`. Usar permisos de aprobación de Codex y protección de ramas para complementar el control.

## Definición de terminado
Código, documentación y tests presentes; segunda ejecución segura; contrato/versiones conocidos; prueba pequeña reproducible y verificable en consola GCP; evidencia o instrucciones claras. **No afirmar despliegue real si no se ejecutó y validó.**

## Regla de enfoque para Codex
Un prompt = una tarea. No reescribir todo el repositorio, no explorar archivos binarios/ZIP ni revisar el modelo completo si los CSV ya cubren la pregunta. Preguntar solo si una decisión cambia el diseño.

## Ejecución incremental autónoma
- El backlog y la arquitectura aprobada son suficientes para iniciar una tarea.
- Si falta `backlog/tasks/RS-XXX.md`, generarlo automáticamente a partir del backlog, el mapping ArchiMate y las dependencias existentes; no detenerse únicamente por esa ausencia.
- Toda tarea generada debe documentar objetivo, alcance, `archimate_id`, recursos GCP, dependencias, criterios de aceptación, pruebas y verificación manual.
- No inventar requisitos de negocio ni tecnologías ajenas a la arquitectura; documentar únicamente supuestos técnicos mínimos.
- Respetar dependencias, implementar, probar, verificar, documentar y registrar cada incremento antes de continuar al siguiente.
- Dentro de la fase de aprovisionamiento autorizada, avanzar automáticamente entre tareas; mantener máximo tres intentos de corrección por fallo.
- Evitar exploraciones repetitivas o cambios fuera del alcance; registrar avance en el backlog y realizar un commit por incremento.
