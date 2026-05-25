"""SQLAlchemy models for the dashboard application."""

# =========================================================
# 📦 STANDARD LIBRARY
# =========================================================
from datetime import datetime

# =========================================================
# 📦 SQLALCHEMY
# =========================================================
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base


# =========================================================
# 🏗️ BASE MODEL
# =========================================================
Base = declarative_base()


# =========================================================
# 👤 USER MODEL
# =========================================================
class User(Base):
    """
    User model for authentication and authorization.
    """

    __tablename__ = "users"

    # =====================================================
    # 🔑 PRIMARY KEY
    # =====================================================
    id = Column(Integer, primary_key=True, index=True)

    # =====================================================
    # 👤 USER DATA
    # =====================================================
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    # =====================================================
    # 🔐 SECURITY
    # =====================================================
    password_hash = Column(
        String(255),
        nullable=False,
    )

    roles = Column(
        String(255),
        default="user",
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    failed_login_attempts = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # =====================================================
    # 🕒 TIMESTAMPS
    # =====================================================
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # =====================================================
    # 🧾 REPRESENTATION
    # =====================================================
    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"username='{self.username}', "
            f"email='{self.email}')"
        )


# =========================================================
# 💰 SALES MODEL
# =========================================================
class Venta(Base):
    """
    Sales model for historical dashboard analytics.
    """

    __tablename__ = "ventas"

    # =====================================================
    # 🔑 PRIMARY KEY
    # =====================================================
    id = Column(Integer, primary_key=True, index=True)

    # =====================================================
    # 📊 SALES DATA
    # =====================================================
    fecha = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    categoria = Column(
        String(50),
        nullable=False,
        index=True,
    )

    ventas = Column(
        Float,
        default=0.0,
        nullable=False,
    )

    unidades = Column(
        Integer,
        default=0,
        nullable=False,
    )

    clientes = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # =====================================================
    # 🧾 REPRESENTATION
    # =====================================================
    def __repr__(self) -> str:
        return (
            f"Venta(id={self.id}, "
            f"categoria='{self.categoria}', "
            f"fecha='{self.fecha}')"
        )
