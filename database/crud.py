"""Operaciones CRUD para la base de datos."""

from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import func

from .models import User, Venta


# --- USUARIOS ---

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, name: str, password_hash: str, roles: str = "user") -> User:
    user = User(
        username=username,
        email=email,
        name=name,
        password_hash=password_hash,
        roles=roles
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, username: str, password_hash: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if user:
        user.password_hash = password_hash
        db.commit()
        db.refresh(user)
    return user


def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()


# --- VENTAS ---

def create_venta(db: Session, fecha, categoria: str, ventas: float, unidades: int, clientes: int) -> Venta:
    v = Venta(
        fecha=fecha,
        categoria=categoria,
        ventas=ventas,
        unidades=unidades,
        clientes=clientes
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


def get_ventas(db: Session, skip: int = 0, limit: int = 100) -> List[Venta]:
    return db.query(Venta).offset(skip).limit(limit).all()


def get_ventas_por_categoria(db: Session, categoria: str) -> List[Venta]:
    return db.query(Venta).filter(Venta.categoria == categoria).all()


def get_resumen_ventas(db: Session):
    """Retorna resumen agregado de ventas por categoría."""
    return db.query(
        Venta.categoria,
        func.sum(Venta.ventas).label("total_ventas"),
        func.sum(Venta.unidades).label("total_unidades"),
        func.sum(Venta.clientes).label("total_clientes")
    ).group_by(Venta.categoria).all()
