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

### Cómo usar los skills en Gemini CLI

Para utilizar estos skills en Gemini CLI:

1. **Carga del skill** - Solicita explícitamente al agente que lea el archivo `SKILL.md` principal del skill. Puedes usar una ruta relativa o absoluta:
   ```
   Lee y adopta las prácticas definidas en agent-skills/fastapi-mysql-alembic/SKILL.md
   ```

2. **Desarrollo guiado** - El agente incorporará el contenido del archivo a su contexto de conversación y seguirá las directrices especificadas para asistirte.

### Cómo usar los skills en antigravity

Para utilizar cualquier skill de este repositorio en antigravity:

1. **Carga del skill** - Usa el slash command `/skill` para cargar el skill que necesites:
   ```
   /skill /ruta/al/agent-skills/fastapi-mysql-alembic
   ```

2. **Lectura automática** - Al cargar el skill, antigravity lee automáticamente el archivo `SKILL.md` del directorio, proporcionando al agente el contexto, patrones y mejores prácticas específicas.

3. **Desarrollo guiado** - Una vez cargado, el agente aplicará los principios y flujos de trabajo documentados en el skill para ayudarte en tu tarea.

### Cómo usar los skills en opencode

Para utilizar cualquier skill de este repositorio en opencode:

1. **Carga del skill** - Usa el slash command `/skill` para cargar el skill que necesites:
   ```
   /skill /ruta/al/agent-skills/fastapi-mysql-alembic
   ```

2. **Lectura automática** - Al cargar el skill, opencode lee automáticamente el archivo `SKILL.md` del directorio, proporcionando al agente el contexto, patrones y mejores prácticas específicas.

3. **Desarrollo guiado** - Una vez cargado, el agente aplicará los principios y flujos de trabajo documentados en el skill para ayudarte en tu tarea.

### Cómo usar los skills en Goose

Para utilizar cualquier skill de este repositorio en [Goose](https://github.com/block/goose):

1. **Habilita la extensión skills** - Asegúrate de que la extensión `skills` esté habilitada en tu configuración de Goose (`~/.config/goose/config.yaml`):
   ```yaml
   extensions:
     skills:
       enabled: true
       type: platform
       name: skills
       description: Load and use skills from relevant directories
       bundled: true
   ```

2. **Inicia sesión en el directorio del skill** - Navega al directorio que contiene el skill y ejecuta Goose desde ahí:
   ```bash
   cd /ruta/al/agent-skills/fastapi-mysql-alembic
   goose session
   ```

3. **Lectura automática** - Al iniciar la sesión, Goose detecta y lee automáticamente el archivo `SKILL.md` del directorio actual, proporcionando al agente el contexto, patrones y mejores prácticas específicas.

4. **Carga manual (alternativa)** - Si ya tienes una sesión activa, puedes pedirle a Goose que lea el skill directamente:
   ```
   Lee y adopta las prácticas definidas en /ruta/al/agent-skills/fastapi-mysql-alembic/SKILL.md
   ```

5. **Desarrollo guiado** - Una vez cargado, el agente aplicará los principios y flujos de trabajo documentados en el skill para ayudarte en tu tarea.

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
