"""Modelo base con timestamps automáticos."""
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa para SQLAlchemy 2.0+"""
    pass


class TimestampMixin:
    """Mixin que agrega created_at y updated_at."""
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )


class BaseModelMixin(TimestampMixin):
    """Mixin con ID y timestamps."""
    id = Column(Integer, primary_key=True, index=True)
