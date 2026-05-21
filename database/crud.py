"""Database CRUD operations."""

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import User, Venta


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    username: str,
    email: str,
    name: str,
    password_hash: str,
    roles: str = "user",
) -> User:
    """Create new user."""
    user = User(
        username=username,
        email=email,
        name=name,
        password_hash=password_hash,
        roles=roles,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, username: str, password_hash: str) -> Optional[User]:
    """Update user password."""
    user = get_user_by_username(db, username)
    if user:
        user.password_hash = password_hash
        db.commit()
        db.refresh(user)
    return user


def get_all_users(db: Session) -> List[User]:
    """Get all users."""
    return db.query(User).all()


def create_venta(
    db: Session,
    fecha,
    categoria: str,
    ventas: float,
    unidades: int,
    clientes: int,
) -> Venta:
    """Create new sale record."""
    venta = Venta(
        fecha=fecha,
        categoria=categoria,
        ventas=ventas,
        unidades=unidades,
        clientes=clientes,
    )
    db.add(venta)
    db.commit()
    db.refresh(venta)
    return venta


def get_ventas(db: Session, skip: int = 0, limit: int = 100) -> List[Venta]:
    """Get sales with pagination."""
    return db.query(Venta).offset(skip).limit(limit).all()


def get_ventas_por_categoria(db: Session, categoria: str) -> List[Venta]:
    """Get sales by category."""
    return db.query(Venta).filter(Venta.categoria == categoria).all()


def get_resumen_ventas(db: Session) -> List:
    """Get sales summary by category."""
    return (
        db.query(
            Venta.categoria,
            func.sum(Venta.ventas).label("total_ventas"),
            func.sum(Venta.unidades).label("total_unidades"),
            func.sum(Venta.clientes).label("total_clientes"),
        )
        .group_by(Venta.categoria)
        .all()
    )
