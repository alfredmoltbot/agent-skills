# Agent Skills - Best Practices

Este repositorio contiene los skills principales de buenas prácticas para agentes de IA.

## Propósito

Aquí se irán dejando documentados los patrones, técnicas y mejores prácticas para el desarrollo y operación de agentes inteligentes.

## Contenido

- **[fastapi-mysql-alembic](fastapi-mysql-alembic/)** - Guía para desarrollar sistemas backend con FastAPI, MySQL y Alembic de manera incremental en sesiones interactivas múltiples. Incluye patrones para proyectos modulares, migraciones versionadas y desarrollo colaborativo por agentes.

## Uso

### Cómo usar los skills en Kimi Code CLI

Kimi Code CLI descubre los skills automáticamente desde directorios específicos. Hay tres niveles de skills:

**1. Skills a nivel de usuario** (disponibles en todos los proyectos):

Kimi Code CLI busca skills en los siguientes directorios (en orden de prioridad):
- `~/.config/agents/skills/` (recomendado)
- `~/.agents/skills/`
- `~/.kimi/skills/`

Para usar un skill de este repositorio a nivel global:
```bash
mkdir -p ~/.config/agents/skills
ln -s /ruta/al/agent-skills/fastapi-mysql-alembic ~/.config/agents/skills/
```

**2. Skills a nivel de proyecto** (solo disponibles en el proyecto actual):

Kimi Code CLI busca skills en los siguientes directorios dentro del proyecto:
- `.agents/skills/` (recomendado)
- `.kimi/skills/`

Para usar un skill de este repositorio en un proyecto específico:
```bash
mkdir -p .agents/skills
ln -s /ruta/al/agent-skills/fastapi-mysql-alembic .agents/skills/
```

**3. Especificar un directorio de skills personalizado**:

También puedes usar el flag `--skills-dir` para cargar skills desde cualquier ubicación:
```bash
kimi --skills-dir /ruta/al/agent-skills
```

**Uso de los skills:**

Una vez configurados los skills, puedes cargarlos usando el slash command `/skill:`:

```
/skill:fastapi-mysql-alembic
```

También puedes añadir texto adicional después del comando:
```
/skill:fastapi-mysql-alembic Necesito crear un endpoint para gestionar usuarios
```

**Nota:** Kimi Code CLI también detecta y lee automáticamente los skills relevantes según el contexto de la conversación, por lo que no siempre es necesario invocarlos manualmente.

### Cómo usar los skills en Kilo Code

Para utilizar skills en Kilo Code, consulta la documentación oficial:
https://kilo.ai/docs/customize/skills

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

### Cómo usar los skills en Visual Studio Code (GitHub Copilot)

Para utilizar estos skills en VS Code con GitHub Copilot, tienes dos opciones:

#### Opción 1: Copiar el skill en `.github/skills/` (Recomendado)

1. **Copia el skill a tu proyecto** - Crea un directorio `.github/skills/` en tu proyecto y copia el skill:
   ```bash
   mkdir -p .github/skills
   cp -r /ruta/al/agent-skills/fastapi-mysql-alembic .github/skills/
   ```

2. **Inicia Copilot Chat** - Abre el panel de Copilot Chat (`Ctrl+Alt+I` o `Cmd+Alt+I` en Mac).

3. **Referencia el skill** - GitHub Copilot detectará automáticamente los archivos en `.github/skills/`. Simplemente menciónalos:
   ```
   @workspace Lee y adopta las prácticas definidas en .github/skills/fastapi-mysql-alembic/SKILL.md
   ```

4. **Desarrollo guiado** - Copilot aplicará los principios documentados en el skill para tu proyecto.

**Ventajas:**
- El skill queda integrado en tu proyecto
- Puedes versionarlo junto a tu código
- Facilita la colaboración en equipo

#### Opción 2: Abrir el workspace del skill directamente

1. **Abre el workspace del skill** - Abre el directorio del skill en VS Code:
   ```bash
   code /ruta/al/agent-skills/fastapi-mysql-alembic
   ```

2. **Inicia Copilot Chat** - Abre el panel de Copilot Chat (`Ctrl+Alt+I` o `Cmd+Alt+I` en Mac).

3. **Usa el comando @workspace** - Menciona el archivo del skill en tu conversación:
   ```
   @workspace Lee y adopta las prácticas definidas en SKILL.md
   ```

4. **Referencias específicas** - Puedes referenciar archivos específicos del skill:
   ```
   @workspace #file:SKILL.md #file:references/patrones.md
   ```

**Ejemplo de uso:**
```
@workspace Necesito crear un proyecto FastAPI siguiendo las prácticas del SKILL.md. 
Lee primero SKILL.md y luego ayúdame a iniciar el proyecto.
```

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
