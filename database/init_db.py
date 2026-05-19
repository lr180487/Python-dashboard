"""Inicializa la base de datos con tablas y usuarios de ejemplo."""

import bcrypt

from .crud import create_user
from .models import Base, User
from .session import db_session, engine

_initialized = False


def init_database():
    """Crea tablas y usuarios iniciales (idempotente)."""
    global _initialized
    if _initialized:
        return
    _initialized = True

    print("[INIT] Creando tablas...")
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        print(f"[INIT] Tablas ya existen o error menor: {e}")

    with db_session() as db:
        # Verificar si ya existen usuarios
        existing = db.query(User).first()
        if existing:
            print("[INIT] Usuarios ya existen, saltando inicialización.")
            return

        print("[INIT] Creando usuarios de ejemplo...")

        admin_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        user_hash = bcrypt.hashpw("user123".encode(), bcrypt.gensalt()).decode()

        create_user(db, "admin", "admin@example.com", "Administrador", admin_hash, "admin,user")
        create_user(db, "usuario", "usuario@example.com", "Usuario Demo", user_hash, "user")

        print("[INIT] Usuarios creados: admin / usuario")


if __name__ == "__main__":
    init_database()
