# Estructura Detallada del Proyecto

## Archivos de Configuración

### pyproject.toml

> **Nota**: Este proyecto usa [uv](https://docs.astral.sh/uv/) para gestión de dependencias. Los comandos deben ejecutarse con `uv run` o activando el entorno con `source .venv/bin/activate`.

```toml
[project]
name = "mi-proyecto"
version = "0.1.0"
description = "API con FastAPI y MySQL"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "pymysql>=1.1.0",          # Driver MySQL
    "cryptography>=42.0.0",     # Para auth seguro en PyMySQL
    "pydantic-settings>=2.1.0", # Configuración con env vars
    "python-multipart>=0.0.6",  # Para form uploads
    "passlib[bcrypt]>=1.7.4",   # Password hashing
    "python-jose[cryptography]>=3.3.0",  # JWT tokens
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "httpx>=0.26.0",
    "ruff>=0.2.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "httpx>=0.26.0",
    "ruff>=0.2.0",
]
```

#### Comandos UV comunes

```bash
# Inicializar proyecto
uv init --name mi-proyecto

# Agregar dependencias
uv add fastapi sqlalchemy alembic

# Agregar dependencias de desarrollo
uv add --dev pytest httpx

# Instalar dependencias (lee pyproject.toml)
uv sync

# Ejecutar comandos
uv run uvicorn app.main:app --reload
uv run pytest
uv run alembic upgrade head

# Activar entorno (opcional)
source .venv/bin/activate
```

### app/config.py

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    database_url: str = "mysql+pymysql://user:password@localhost/dbname"
    
    # Application
    app_name: str = "Mi API"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    
    # JWT
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### .env (ejemplo)

```bash
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/miapp
SECRET_KEY=your-secret-key-here-min-32-chars-long
DEBUG=true
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### .env.example

```bash
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname
SECRET_KEY=change-me-in-production
DEBUG=false
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Alembic (mantener solo versiones)
alembic.ini.local
```

## Core Application

### app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import usuarios, auth

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="API REST construida con FastAPI",
    version="0.1.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar según entorno
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(usuarios.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
def root():
    return {"message": "Bienvenido a la API", "docs": "/docs"}
```

### app/database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from typing import Annotated

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verifica conexiones antes de usar
    pool_recycle=3600,   # Recicla conexiones cada hora
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependency para obtener sesión de DB."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type alias para uso en routers
DBSession = Annotated[Session, Depends(get_db)]
```

### app/models/base.py

```python
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class para todos los modelos."""
    pass

class TimestampMixin:
    """Mixin para agregar created_at y updated_at automáticamente."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class IDMixin:
    """Mixin para agregar id autoincremental."""
    id = Column(Integer, primary_key=True, index=True)
```

### app/schemas/base.py

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    """Schema base con configuración común."""
    model_config = ConfigDict(
        from_attributes=True,  # ORM mode
        populate_by_name=True,
    )

class TimestampedSchema(BaseSchema):
    """Schema con timestamps."""
    created_at: datetime
    updated_at: Optional[datetime] = None

class ResponseSchema(BaseSchema):
    """Schema base para respuestas."""
    success: bool = True
    message: Optional[str] = None
```

### app/dependencies.py

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.crud.usuario import crud_usuario

settings = get_settings()
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency para obtener usuario autenticado."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud_usuario.get(db, id=int(user_id))
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """Dependency para verificar usuario activo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user
```

## Alembic Configuration

> **Nota**: Todos los comandos de alembic deben ejecutarse con `uv run`:
> ```bash
> uv run alembic init alembic
> uv run alembic revision --autogenerate -m "descripcion"
> uv run alembic upgrade head
> ```

### alembic/env.py

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar Base y modelos
from app.models.base import Base
from app.models.usuario import Usuario  # Importar todos los modelos

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerate
target_metadata = Base.metadata

# Otros valores de config
config.set_main_option("sqlalchemy.url", "mysql+pymysql://user:pass@localhost/db")

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Testing Structure

### tests/conftest.py

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.models.base import Base
from app.database import get_db
from app.main import app

# BD en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
```

### tests/test_usuarios.py

```python
import pytest
from fastapi.testclient import TestClient

def test_crear_usuario(client: TestClient):
    response = client.post("/api/v1/usuarios/", json={
        "email": "test@example.com",
        "nombre": "Test User",
        "password": "secret123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_listar_usuarios(client: TestClient):
    response = client.get("/api/v1/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```
