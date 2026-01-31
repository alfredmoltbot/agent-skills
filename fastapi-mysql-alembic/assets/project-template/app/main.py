from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine

settings = get_settings()

# Crear tablas (solo para desarrollo rápido, usar Alembic en producción)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="API REST construida con FastAPI, MySQL y Alembic",
    version="0.1.0",
    debug=settings.debug,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check():
    """Endpoint de verificación de salud."""
    return {
        "status": "ok",
        "version": "0.1.0",
        "debug": settings.debug,
    }


@app.get("/", tags=["root"])
def root():
    """Raíz de la API."""
    return {
        "message": "Bienvenido a la API",
        "docs": "/docs",
        "health": "/health",
    }
