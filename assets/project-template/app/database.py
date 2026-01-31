from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Annotated
from fastapi import Depends

from app.config import get_settings

settings = get_settings()

# Engine con pool optimizado para producción
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class para todos los modelos SQLAlchemy."""
    pass


def get_db() -> Session:
    """Dependency para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias conveniente para routers
DBSession = Annotated[Session, Depends(get_db)]
