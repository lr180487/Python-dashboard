"""Modelos SQLAlchemy para el dashboard."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """Modelo de usuario para autenticación."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    roles = Column(String(255), default="user")
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<User(username='{self.username}', name='{self.name}')>"


class Venta(Base):
    """Modelo de ventas para almacenar datos históricos."""

    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now, index=True)
    categoria = Column(String(50), nullable=False, index=True)
    ventas = Column(Float, default=0.0)
    unidades = Column(Integer, default=0)
    clientes = Column(Integer, default=0)

    def __repr__(self):
        return f"<Venta(fecha='{self.fecha}', categoria='{self.categoria}')>"
