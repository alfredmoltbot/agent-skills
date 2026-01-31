# Patrones Avanzados

## Async SQLAlchemy

> **Nota**: Para usar async, agregar `aiomysql` con uv:
> ```bash
> uv add aiomysql
> ```

### Cuándo usar

- Alta concurrencia (muchos requests simultáneos)
- Operaciones I/O intensivas
- Cuando se espera mucho tráfico

### Configuración

```python
# app/database.py (async)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "mysql+aiomysql://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Modelos con async

```python
# app/crud/usuario_async.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate

class CRUDUsuarioAsync:
    async def get(self, db: AsyncSession, id: int) -> Optional[Usuario]:
        result = await db.execute(select(Usuario).where(Usuario.id == id))
        return result.scalar_one_or_none()
    
    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Usuario]:
        result = await db.execute(select(Usuario).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: UsuarioCreate) -> Usuario:
        db_obj = Usuario(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
```

## Autenticación JWT Completa

### app/core/security.py

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
```

### app/routers/auth.py

```python
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import Token, LoginRequest
from app.crud.usuario import crud_usuario
from app.core.security import verify_password, create_access_token
from app.config import get_settings

settings = get_settings()
router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud_usuario.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if crud_usuario.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    user_in.password = get_password_hash(user_in.password)
    user = crud_usuario.create(db, obj_in=user_in)
    return {"id": user.id, "email": user.email, "message": "Usuario creado"}
```

## Paginación

### Schema de paginación

```python
# app/schemas/pagination.py
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
```

### Implementación en CRUD

```python
def get_multi_paginated(
    self, 
    db: Session, 
    page: int = 1, 
    page_size: int = 20,
    filters: dict = None
):
    query = db.query(self.model)
    
    if filters:
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.filter(getattr(self.model, key) == value)
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
```

## Soft Delete

### Modelo base con soft delete

```python
# app/models/base.py
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Query, DeclarativeBase

class Base(DeclarativeBase):
    pass

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True))
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = func.now()

class SoftDeleteQuery(Query):
    """Query que filtra automáticamente registros eliminados."""
    def __new__(cls, *entities, **kwargs):
        query = super().__new__(cls, *entities, **kwargs)
        # Filtrar soft deleted
        for entity in query._entities:
            if hasattr(entity, 'is_deleted'):
                query = query.filter(entity.is_deleted == False)
        return query
```

## Relaciones

### One-to-Many

```python
# app/models/usuario.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    
    # Relación
    posts = relationship("Post", back_populates="autor", cascade="all, delete-orphan")

# app/models/post.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    autor = relationship("Usuario", back_populates="posts")
```

### Many-to-Many

```python
# Tabla de asociación
from sqlalchemy import Table, Column, Integer, ForeignKey

usuario_rol = Table(
    "usuario_rol",
    Base.metadata,
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), primary_key=True),
    Column("rol_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

# Modelos
class Rol(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    usuarios = relationship("Usuario", secondary=usuario_rol, back_populates="roles")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    
    roles = relationship("Rol", secondary=usuario_rol, back_populates="usuarios")
```

## Validaciones Avanzadas con Pydantic

```python
from pydantic import BaseModel, field_validator, EmailStr
from datetime import date
import re

class UsuarioCreate(BaseModel):
    email: EmailStr
    nombre: str
    password: str
    telefono: str | None = None
    fecha_nacimiento: date | None = None
    
    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v
    
    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, v: str | None) -> str | None:
        if v is None:
            return v
        # Limpiar y validar formato
        v = re.sub(r"\D", "", v)
        if len(v) < 10:
            raise ValueError("Teléfono inválido")
        return v
    
    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        return v.title()  # Capitalizar
```

## Manejo de Errores Global

```python
# app/core/exceptions.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            errors.append({
                "field": error["loc"][-1],
                "message": error["msg"],
                "type": error["type"]
            })
        return JSONResponse(
            status_code=422,
            content={"detail": "Error de validación", "errors": errors}
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        logger.error(f"Database integrity error: {exc}")
        return JSONResponse(
            status_code=400,
            content={"detail": "Error de integridad de datos. Posible duplicado."}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )
```

## Logging Estructurado

```python
# app/core/logging.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s"
    )
    log_handler.setFormatter(formatter)
    
    # Configurar loggers
    for logger_name in ["app", "uvicorn"]:
        logger = logging.getLogger(logger_name)
        logger.handlers = [log_handler]
        logger.setLevel(logging.INFO)
```

## Background Tasks

```python
from fastapi import BackgroundTasks, APIRouter
from typing import List
import smtplib
from email.mime.text import MIMEText

router = APIRouter()

def send_email(email_to: str, subject: str, body: str):
    """Función que corre en background."""
    # Implementación de envío de email
    pass

@router.post("/usuarios/")
def crear_usuario(
    user: UsuarioCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    usuario = crud_usuario.create(db, obj_in=user)
    
    # Agregar tarea en background
    background_tasks.add_task(
        send_email,
        email_to=user.email,
        subject="Bienvenido",
        body=f"Hola {user.nombre}, bienvenido a nuestra plataforma!"
    )
    
    return usuario
```
