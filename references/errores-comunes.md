# Errores Comunes y Soluciones

## Errores con UV (Gestor de Dependencias)

### Error: `command not found: uv`

**Causa**: UV no está instalado o no está en el PATH.

**Solución**:
```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# O con pip
pip install uv

# Verificar instalación
uv --version
```

### Error: `No module named 'xxx'` al ejecutar con uv run

**Causa**: El entorno virtual no está sincronizado o las dependencias no están instaladas.

**Solución**:
```bash
# Sincronizar dependencias (instala todo desde pyproject.toml)
uv sync

# Si falta una dependencia específica, agregarla
uv add nombre-paquete

# Para dependencias de desarrollo
uv add --dev nombre-paquete
```

### Error: `ModuleNotFoundError` en alembic/env.py

**Causa**: Alembic se ejecuta sin el contexto de uv, por lo que no encuentra los módulos del proyecto.

**Solución**:
```bash
# SIEMPRE usar uv run con alembic
uv run alembic revision --autogenerate -m "descripcion"
uv run alembic upgrade head
uv run alembic current

# NO usar alembic directamente sin uv run
```

### Error: `Cannot install package` o conflictos de versiones

**Causa**: El lock file (uv.lock) está desactualizado o hay incompatibilidades.

**Solución**:
```bash
# Actualizar lock file y sincronizar
uv sync --upgrade

# O regenerar completamente
rm uv.lock
uv sync
```

### Error: `.venv` no se crea o está en ubicación incorrecta

**Causa**: Proyecto no inicializado correctamente.

**Solución**:
```bash
# Inicializar proyecto uv
uv init --name mi-proyecto

# Crear entorno explícitamente
uv venv

# Sincronizar dependencias
uv sync
```

## Errores de Conexión a MySQL

### Error: `Can't connect to MySQL server`

**Causa**: MySQL no está corriendo o credenciales incorrectas.

**Solución**:
```bash
# Verificar que MySQL está activo
sudo systemctl status mysql

# Probar conexión manual
mysql -u root -p -e "SHOW DATABASES;"

# Verificar URL de conexión
# mysql+pymysql://usuario:password@host:puerto/database
```

### Error: `cryptography required for sha256_password or caching_sha2_password`

**Causa**: Falta el paquete `cryptography` o autenticación no soportada.

**Solución**:
```bash
pip install cryptography

# O cambiar método de auth en MySQL:
# ALTER USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

## Errores de Migraciones (Alembic)

### Error: `Target database is not up to date`

**Causa**: Migraciones pendientes por aplicar.

**Solución**:
```bash
# Ver estado actual
alembic current

# Ver historial
alembic history

# Aplicar migraciones pendientes
alembic upgrade head
```

### Error: `Can't locate revision identified by 'xxx'`

**Causa**: La migración registrada en la BD no existe en archivos.

**Solución**:
```bash
# Opción 1: Resetear (solo desarrollo)
alembic downgrade base
alembic upgrade head

# Opción 2: Manual en MySQL
# DELETE FROM alembic_version;
# INSERT INTO alembic_version VALUES ('revision_mas_reciente_local');
```

### Error: `autogenerate` no detecta cambios

**Causas comunes**:
1. Modelos no importados en `env.py`
2. `target_metadata` no configurado correctamente
3. Cambios en tipos no detectados automáticamente

**Solución**:
```python
# alembic/env.py - Asegurar import de todos los modelos
from app.models.base import Base
from app.models.usuario import Usuario  # Importar cada modelo
from app.models.producto import Producto

target_metadata = Base.metadata  # No olvidar esta línea
```

Para tipos no detectados, crear migración manual:
```bash
alembic revision -m "cambia_tipo_columna"
# Editar el archivo generado manualmente
```

## Errores de SQLAlchemy

### Error: `ObjectNotFound` o `DetachedInstanceError`

**Causa**: Acceso a atributos de objeto fuera de la sesión.

**Solución**:
```python
# Mal: acceso después de cerrar sesión
def get_user(db: Session, user_id: int):
    return db.query(User).get(user_id)  # Retorna objeto detached

# Bien: eager loading o mantener sesión
from sqlalchemy.orm import joinedload

def get_user_with_posts(db: Session, user_id: int):
    return db.query(User).options(joinedload(User.posts)).get(user_id)

# O asegurar uso dentro de contexto
with SessionLocal() as db:
    user = get_user(db, 1)
    print(user.posts)  # OK, sesión aún abierta
```

### Error: `IntegrityError: duplicate entry`

**Causa**: Violación de constraint UNIQUE.

**Solución**:
```python
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email ya existe")
```

### Error: `InvalidRequestError: Object already attached to session`

**Causa**: Intentar agregar objeto que ya está en otra sesión.

**Solución**:
```python
# Usar merge en lugar de add
db.merge(obj)  # En lugar de db.add(obj)

# O expirar objeto antes
db.expire(obj)
db.add(obj)
```

## Errores de FastAPI/Pydantic

### Error: `validation_error` en respuesta

**Causa**: El modelo de respuesta no coincide con datos reales.

**Solución**:
```python
# Verificar que ORM mode está activo
class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True  # Pydantic v2
        # orm_mode = True  # Pydantic v1

# Asegurar que estamos pasando el objeto, no dict
return db_user  # OK
# return {"id": db_user.id, ...}  # También OK pero más verboso
```

### Error: `RecursionError` en modelos con relaciones

**Causa**: Referencia circular entre modelos.

**Solución**:
```python
# Usar response_model_exclude o crear schema específico

# Opción 1: Excluir relación
class UserResponse(BaseModel):
    id: int
    email: str
    # No incluir posts aquí

# Opción 2: Schema anidado limitado
class UserSummary(BaseModel):
    id: int
    email: str

class PostResponse(BaseModel):
    id: int
    titulo: str
    autor: UserSummary  # Sin posts anidados
```

### Error: `422 Unprocessable Entity`

**Causa**: Datos de entrada no cumplen validación.

**Debug**:
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    print(exc.errors())  # Ver detalle de errores
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

## Errores de Autenticación JWT

### Error: `Signature has expired`

**Causa**: Token vencido.

**Solución**:
```python
from datetime import datetime, timedelta

# Generar token con expiración adecuada
def create_token(user_id: str, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(hours=24)  # Aumentar si es necesario
    
    expire = datetime.utcnow() + expires_delta
    # ... resto del código
```

### Error: `Not enough segments` (token inválido)

**Causa**: Token mal formateado o corrupto.

**Solución**:
```python
# Asegurar que el token se envía como Bearer
headers = {"Authorization": "Bearer eyJhbG..."}

# No incluir comillas ni espacios extra
```

## Problemas de Rendimiento

### Consultas N+1

**Síntoma**: Muchas queries ejecutándose en loop.

**Solución**:
```python
from sqlalchemy.orm import joinedload, selectinload

# Mal: N queries adicionales
users = db.query(User).all()
for user in users:
    print(user.posts)  # Query adicional por usuario

# Bien: eager loading
users = db.query(User).options(selectinload(User.posts)).all()
# Solo 2 queries totales
```

### Conexiones agotadas

**Síntoma**: `QueuePool limit of size 5 overflow 10 reached`.

**Solución**:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,           # Aumentar pool
    max_overflow=30,        # Conexiones extra en peak
    pool_timeout=30,        # Timeout esperando conexión
    pool_recycle=3600,      # Reciclar cada hora
)
```

## Problemas Comunes de Desarrollo

### Cambios en código no se reflejan

**Causa**: Uvicorn cache o import circular.

**Solución**:
```bash
# Recargar con force
uvicorn app.main:app --reload --reload-dir app

# Verificar no hay imports circulares
python -c "from app.main import app"
```

### Variables de entorno no cargan

**Causa**: `.env` no está en ubicación esperada o formato incorrecto.

**Solución**:
```python
# Verificar ubicación
import os
print(os.getcwd())

# Especificar ruta explícita
class Settings(BaseSettings):
    # ... config
    class Config:
        env_file = "/ruta/absoluta/.env"
        env_file_encoding = "utf-8"
```

### Alembic no encuentra models

**Verificar estructura**:
```
app/
├── __init__.py          # Debe existir
├── models/
│   ├── __init__.py      # Debe existir
│   └── usuario.py
```

**En env.py**:
```python
import sys
from pathlib import Path

# Asegurar que app/ está en path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.base import Base  # Import absoluto
```
