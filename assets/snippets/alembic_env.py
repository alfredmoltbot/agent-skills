"""Configuración Alembic para proyectos con estructura app/.

Uso con uv:
    uv run alembic revision --autogenerate -m "descripcion"
    uv run alembic upgrade head
    uv run alembic downgrade -1
    uv run alembic current
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from pathlib import Path

# Agregar app/ al path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importar Base y todos los modelos
from app.database import Base
# IMPORTANTE: Importar todos los modelos para que Alembic los detecte
# from app.models.usuario import Usuario
# from app.models.producto import Producto

# Configuración Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo offline."""
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
    """Ejecutar migraciones en modo online."""
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
