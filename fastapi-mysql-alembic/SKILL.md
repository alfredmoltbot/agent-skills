---
name: fastapi-mysql-alembic
description: Guía para desarrollar sistemas backend con FastAPI, MySQL y Alembic de manera incremental en sesiones interactivas múltiples. Usa uv para gestión de dependencias y comandos. Usar cuando se necesite crear, extender o mantener APIs REST con persistencia en MySQL, migraciones de base de datos y desarrollo colaborativo por agentes.
---

# FastAPI + MySQL + Alembic - Desarrollo por Agentes

Este skill proporciona buenas prácticas y patrones para desarrollar sistemas backend con FastAPI, MySQL y Alembic, optimizado para desarrollo incremental en múltiples sesiones interactivas. Utiliza **uv** como gestor de dependencias y herramienta de ejecución de comandos.

## Principios Fundamentales

1. **Proyecto modular**: Separar claramente modelos, esquemas, rutas y servicios
2. **Migraciones versionadas**: Cada cambio en BD debe ser reversible y trazable
3. **Desarrollo incremental**: Estructura que permite construir funcionalidad por etapas
4. **Sesiones independientes**: Cada sesión debe poder continuar desde donde quedó la anterior

## Flujo de Trabajo por Sesiones

### Inicio de Proyecto (Sesión 1)

1. Crear estructura de carpetas siguiendo [references/estructura.md](references/estructura.md)
2. Inicializar proyecto con uv: `uv init --name mi-proyecto`
3. Agregar dependencias con uv:
   ```bash
   uv add fastapi uvicorn sqlalchemy alembic pymysql cryptography pydantic-settings python-multipart "passlib[bcrypt]" "python-jose[cryptography]"
   uv add --dev pytest httpx ruff
   ```
4. Configurar conexión a MySQL y variables de entorno
5. Inicializar Alembic con configuración personalizada: `uv run alembic init alembic`
6. Crear modelo base y primer modelo de dominio
7. Generar y ejecutar primera migración: `uv run alembic revision --autogenerate -m "init"`
8. Crear endpoint de health check y ejecutar con: `uv run uvicorn app.main:app --reload`

**Checkpoint de sesión**: Proyecto corre, BD conectada, health check funciona.

### Desarrollo de Módulos (Sesiones N)

Para cada nueva entidad/funcionalidad:

1. **Modelo** (`app/models/`): Definir tabla SQLAlchemy
2. **Esquemas** (`app/schemas/`): Crear Pydantic models (Create, Update, Response)
3. **CRUD** (`app/crud/`): Operaciones básicas de base de datos
4. **Rutas** (`app/routers/`): Endpoints FastAPI
5. **Migración**: `alembic revision --autogenerate -m "descripcion"`
6. **Pruebas**: Verificar endpoints con curl/docs

**Reglas por sesión**:
- Una sesión = una entidad principal o funcionalidad coherente
- Dejar TODOs comentados para la siguiente sesión
- Mantener `session.md` con estado actual del proyecto

## Estructura del Proyecto

```
mi-proyecto/
├── alembic/                    # Migraciones
│   ├── versions/               # Scripts de migración
│   └── env.py                  # Configuración Alembic
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── config.py               # Configuración con Pydantic Settings
│   ├── database.py             # Sesión y engine SQLAlchemy
│   ├── dependencies.py         # Inyección de dependencias
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── base.py             # Clase Base y mixins comunes
│   ├── schemas/                # Pydantic models
│   │   ├── __init__.py
│   │   └── base.py             # Schemas base (BaseModel configurado)
│   ├── crud/                   # Operaciones CRUD
│   │   ├── __init__.py
│   │   └── base.py             # CRUD base genérico
│   ├── routers/                # Rutas/endpoints
│   │   └── __init__.py
│   └── services/               # Lógica de negocio (opcional)
├── tests/                      # Tests
├── pyproject.toml              # Dependencias
├── alembic.ini                 # Configuración Alembic
└── session.md                  # Estado del proyecto (ACTUALIZAR CADA SESIÓN)
```

Ver [references/estructura.md](references/estructura.md) para explicación detallada.

## Patrones de Código

### Modelo SQLAlchemy

```python
# app/models/usuario.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.models.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Esquemas Pydantic

```python
# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str

class UsuarioCreate(UsuarioBase):
    password: str  # Solo en creación

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None

class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # ORM mode en v1
```

### CRUD Base

```python
# app/crud/base.py
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump()  # dict() en Pydantic v1
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, id: int) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
```

### Router FastAPI

```python
# app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.crud.usuario import crud_usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_usuario.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Validar email único
    if crud_usuario.get_by_email(db, email=usuario.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud_usuario.create(db, obj_in=usuario)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud_usuario.get(db, id=usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get(db, id=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return crud_usuario.update(db, db_obj=db_usuario, obj_in=usuario)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    crud_usuario.remove(db, id=usuario_id)
    return None
```

Ver más patrones en [references/patrones.md](references/patrones.md).

## Gestión de Dependencias con UV

[uv](https://docs.astral.sh/uv/) es un gestor de paquetes y entornos virtuales extremadamente rápido escrito en Rust.

### Comandos Esenciales de UV

```bash
# Inicializar un nuevo proyecto
uv init --name mi-proyecto

# Agregar dependencias
uv add fastapi sqlalchemy alembic

# Agregar dependencias de desarrollo
uv add --dev pytest httpx ruff

# Instalar todas las dependencias (lee pyproject.toml)
uv sync

# Ejecutar comandos en el entorno virtual
uv run python script.py
uv run uvicorn app.main:app --reload
uv run pytest

# Activar shell con el entorno (opcional)
source .venv/bin/activate
# o en Windows:
# .venv\Scripts\activate

# Ver entorno actual
uv venv

# Actualizar dependencias
uv sync --upgrade
```

### Estructura del Proyecto con UV

UV crea automáticamente:
- `.venv/` - Entorno virtual (no commitear)
- `pyproject.toml` - Configuración del proyecto y dependencias
- `uv.lock` - Lock file exacto de versiones (sí commitear)

## Migraciones con Alembic

### Configuración Inicial

```bash
# En proyecto con estructura app/
uv run alembic init alembic

# Editar alembic.ini: sqlalchemy.url = mysql+pymysql://user:pass@localhost/db

# Editar alembic/env.py para importar Base:
# from app.models.base import Base
# target_metadata = Base.metadata
```

### Flujo de Migraciones

```bash
# 1. Modificar modelos SQLAlchemy
# 2. Generar migración
uv run alembic revision --autogenerate -m "agrega_tabla_usuarios"

# 3. Revisar script generado en alembic/versions/
# 4. Aplicar migración
uv run alembic upgrade head

# Ver historial
uv run alembic history

# Rollback (cuidado en producción)
uv run alembic downgrade -1
```

### Mejores Prácticas

- Siempre revisar el script autogenerado antes de aplicar
- Migraciones atómicas: una entidad por migración en desarrollo
- En producción: migraciones pequeñas e incrementales
- No modificar migraciones ya aplicadas en equipo compartido

## Gestión de Sesiones (session.md)

Crear y mantener un archivo `session.md` en la raíz del proyecto:

```markdown
# Estado del Proyecto

## Última sesión
Fecha: 2024-01-15
Agente: Kimi
Realizado: CRUD de usuarios, autenticación JWT básica

## Pendientes
- [ ] Implementar roles de usuario
- [ ] CRUD de productos
- [ ] Relación usuario-producto

## Decisiones técnicas
- Usar async SQLAlchemy (evaluar en próxima sesión)
- Password hashing con bcrypt

## Notas
- La tabla usuarios tiene índice en email
- JWT secret en .env (no commitear)
```

## Checklist por Sesión

### Al inicio
- [ ] Leer `session.md` si existe
- [ ] Verificar estado de migraciones: `uv run alembic current`
- [ ] Sincronizar dependencias: `uv sync`
- [ ] Confirmar conexión a BD
- [ ] Revisar estructura existente

### Durante el desarrollo
- [ ] Seguir convenciones de nombres existentes
- [ ] Usar type hints
- [ ] Manejar errores HTTP apropiadamente
- [ ] Documentar endpoints con docstrings
- [ ] Ejecutar con `uv run` para asegurar entorno correcto

### Al finalizar
- [ ] Actualizar `session.md`
- [ ] Verificar que migraciones están aplicadas: `uv run alembic current`
- [ ] Asegurar que `uv.lock` está actualizado: `uv sync`
- [ ] Dejar TODOs comentados para próxima sesión
- [ ] Confirmar que `main.py` incluye nuevos routers

## Recursos Adicionales

- [references/estructura.md](references/estructura.md) - Estructura detallada del proyecto
- [references/patrones.md](references/patrones.md) - Patrones avanzados (async, testing, auth)
- [references/errores-comunes.md](references/errores-comunes.md) - Errores frecuentes y soluciones
- [assets/project-template/](assets/project-template/) - Template base de proyecto
- [assets/snippets/](assets/snippets/) - Snippets de código reutilizables
