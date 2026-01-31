# Agent Skills - Best Practices

Este repositorio contiene los skills principales de buenas prácticas para agentes de IA.

## Propósito

Aquí se irán dejando documentados los patrones, técnicas y mejores prácticas para el desarrollo y operación de agentes inteligentes.

## Contenido

- **[fastapi-mysql-alembic](fastapi-mysql-alembic/)** - Guía para desarrollar sistemas backend con FastAPI, MySQL y Alembic de manera incremental en sesiones interactivas múltiples. Incluye patrones para proyectos modulares, migraciones versionadas y desarrollo colaborativo por agentes.

## Uso

### Cómo usar los skills en Claude Code

Para utilizar cualquier skill de este repositorio en Claude Code:

1. **Configura el skill path** - Añade el repositorio a tu configuración de Claude Code:

   En tu archivo de configuración `~/.claude/config.json`:
   ```json
   {
     "skills": [
       "/ruta/al/agent-skills/*"
     ]
   }
   ```

2. **Usa el slash command** - Invoca el skill directamente desde Claude Code:
   ```
   /skill fastapi-mysql-alembic
   ```

3. **Lectura automática** - Al invocar el skill, Claude Code lee automáticamente el archivo `SKILL.md` del directorio correspondiente, proporcionando al agente el contexto, patrones y mejores prácticas específicas.

4. **Desarrollo guiado** - Una vez cargado, el agente aplicará los principios y flujos de trabajo documentados en el skill para ayudarte en tu tarea.

### Uso sin configuración

Alternativamente, puedes cargar un skill directamente usando su ruta completa sin necesidad de configuración previa:
```
/skill /ruta/al/agent-skills/fastapi-mysql-alembic
```

### Estructura de un skill

Cada skill sigue una estructura estándar:
- `SKILL.md` - Documentación principal con principios, flujos de trabajo y ejemplos
- `references/` - Material de referencia adicional (estructuras, snippets, etc.)
- `assets/` - Recursos gráficos o archivos complementarios

### Uso independiente

También puedes leer directamente los archivos `SKILL.md` como guías de referencia manual, ya que contienen toda la información necesaria para aplicar las mejores prácticas documentadas.

---

*Repositorio en construcción*
