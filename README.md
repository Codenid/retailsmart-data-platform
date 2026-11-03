# RetailSmart Data Platform

Plataforma Big Data E2E de una empresa retail ficticia; diseño basado **exclusivamente** en la vista `08_integracion_detallada_tobe` del archivo ArchiMate. Infraestructura en Google Cloud mediante **scripts Bash/gcloud idempotentes**; streaming y batch independientes, con Bronze/Silver/Gold y cuatro casos de uso.

> **Estado:** repositorio **bootstrap** listo para Codex, con inventario extraído y pruebas locales. **No hay recursos GCP desplegados por este paquete.** Los despliegues se implementarán progresivamente en los Issues correspondientes.

## Primera tarea en Codex

Ver [START_HERE.md](START_HERE.md): prompt listo para RS-003, primer incremento de aprovisionamiento. Los contratos RS-002 pueden avanzar en paralelo.

## Inicio rápido (sin GCP)

```bash
bash scripts/verify-local.sh
python3 scripts/export_architecture.py
bash scripts/00-preflight.sh --local
```

## Preparar Cloud Shell / VS Code con GCP (solo inspección)

```bash
cp .env.example .env
# Edita .env con PROJECT_ID, REGION y demás valores no secretos.
bash scripts/00-preflight.sh
```

`00-preflight.sh` **no crea ni modifica recursos**. Los scripts de aprovisionamiento se implementan a partir de `RS-003` y nunca se ejecutan sin aprobación.

## Navegación

| Documento | Para qué sirve |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Contexto permanente de Codex y límites de seguridad |
| [docs/PRODUCT.md](docs/PRODUCT.md) | Propósito, reglas y demostraciones |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Etapas y gates |
| [backlog/BACKLOG.md](backlog/BACKLOG.md) | Secuencia de Issues |
| [docs/CODEX_WORKFLOW.md](docs/CODEX_WORKFLOW.md) | Uso paso a paso con Codex VS Code |
| [architecture/inventory](architecture/inventory) | 94 elementos, 165 relaciones y 12 productores de vista 08 |
| [docs/DATA_UNIVERSE.md](docs/DATA_UNIVERSE.md) | Identidades estables, estado común, tiempo y calidad |
| [docs/GCP_VALIDATION.md](docs/GCP_VALIDATION.md) | Cómo evidenciar cada entrega en GCP |

## Qué incluye y qué no

- **Incluye:** modelo original, extractor reproducible de ArchiMate, inventario por IDs, rutas de 12 productores, mapping técnico inicial, contexto de agentes, contratos de ejemplo, backlog, pruebas y preflight solo lectura.
- **No incluye aún:** provisionamiento, pipelines Beam, jobs Spark, DAGs Airflow, entrenamiento ML, API ni simuladores. Esos son entregables versionados posteriores. No simular que están implementados.
- El simulador podrá vivir en un repositorio separado: se integrará mediante **contratos versionados**. El estado de la empresa simulada deberá persistir fuera de los recursos GCP efímeros.

## Reglas de Git

- `main` estable; ramas `feat/RS-XXX-descripcion`; un Issue por PR.
- PR requiere `bash scripts/verify-local.sh`, evidencia de pruebas y revisión manual de costo/seguridad cuando aplique.
- `.env`, archivos de credenciales, datos reales y estado mutable NO se suben al repositorio.

## Publicar desde tu equipo (requiere GitHub CLI autenticado)

```bash
git init
git add .
git commit -m "chore: bootstrap RetailSmart data platform"
gh repo create retailsmart-data-platform --private --source=. --remote=origin --push
```

Si GitHub rechaza un repositorio existente, no sobrescribirlo: elegir otro nombre o clonar y comparar cambios.
