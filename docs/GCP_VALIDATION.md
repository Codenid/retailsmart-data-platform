# Plantilla de verificación manual en Google Cloud

Cada Issue que modifica GCP debe crear un archivo en `docs/runbooks/RS-XXX.md` usando estas secciones.

1. **Prerequisitos**: proyecto, región, APIs, roles y costo esperado.
2. **Comando**: script exacto, variables obligatorias, confirmación y rollback.
3. **Verificar en consola GCP**: ruta de navegación (producto > recurso), nombre, estado, etiquetas, permisos.
4. **Generar prueba**: script fixture, volumen bajo, `simulation_id`/`batch_id`, hora de ejecución.
5. **Resultado esperado**: qué objeto, mensaje, archivo o tabla debe existir; ejemplo de consulta.
6. **Idempotencia**: repetir el script y verificar no duplicación ni cambios inesperados.
7. **Errores**: cómo distinguir 404, 403, agotamiento de cuota y divergencia.
8. **Limpieza**: comandos seguros, componentes persistentes y costos residuales.
9. **Evidencia**: captura, URI, IDs de job, resultado SQL, marca temporal.

> No publicar URLs de proyectos privados, claves, tokens, datos personales reales ni capturas con credenciales en repositorios públicos.
