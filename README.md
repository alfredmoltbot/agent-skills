# Agent Skills - Best Practices

Este repositorio contiene los skills principales de buenas prácticas para agentes de IA.

## Propósito

Aquí se irán dejando documentados los patrones, técnicas y mejores prácticas para el desarrollo y operación de agentes inteligentes.

## Contenido

- **[fastapi-mysql-alembic](fastapi-mysql-alembic/)** - Guía para desarrollar sistemas backend con FastAPI, MySQL y Alembic de manera incremental en sesiones interactivas múltiples. Incluye patrones para proyectos modulares, migraciones versionadas y desarrollo colaborativo por agentes.

## Uso

### Cómo usar los skills en Kimi Code CLI

Para utilizar cualquier skill de este repositorio en Kimi Code CLI:

1. **Carga del skill** - Usa el slash command `/skill` para cargar el skill que necesites:
   ```
   /skill /ruta/al/agent-skills/fastapi-mysql-alembic
   ```

2. **Lectura automática** - Al cargar el skill, Kimi Code CLI lee automáticamente el archivo `SKILL.md` del directorio, proporcionando al agente el contexto, patrones y mejores prácticas específicas.

3. **Desarrollo guiado** - Una vez cargado, el agente aplicará los principios y flujos de trabajo documentados en el skill para ayudarte en tu tarea.

### Estructura de un skill

Cada skill sigue una estructura estándar:
- `SKILL.md` - Documentación principal con principios, flujos de trabajo y ejemplos
- `references/` - Material de referencia adicional (estructuras, snippets, etc.)
- `assets/` - Recursos gráficos o archivos complementarios

### Uso independiente

También puedes leer directamente los archivos `SKILL.md` como guías de referencia manual, ya que contienen toda la información necesaria para aplicar las mejores prácticas documentadas.

---

*Repositorio en construcción*
