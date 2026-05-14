"""Configuración de la sesión de base de datos.

PostgreSQL con fallback a SQLite local.
"""

import os
import sys

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

from contextlib import contextmanager
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _add_client_encoding_to_url(url: str) -> str:
    """Asegura que client_encoding=utf8 esté presente en la URL de PostgreSQL."""
    parsed = urlparse(url)
    if parsed.scheme not in ("postgresql", "postgres", "postgresql+psycopg2", "postgresql+psycopg"):
        return url
    query = parse_qs(parsed.query)
    query["client_encoding"] = ["utf8"]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


_raw_url = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/dashboard"
)
DATABASE_URL = _add_client_encoding_to_url(_raw_url)

engine = None
SessionLocal = None


def _safe_print(msg: str):
    """Imprime a stdout forzando UTF-8, evitando crashes en Windows con codificaciones mixtas."""
    try:
        sys.stdout.buffer.write(f"{msg}\n".encode("utf-8", errors="replace"))
    except Exception:
        pass


def _create_engine_with_fallback():
    """Intenta conectar a PostgreSQL, si falla usa SQLite local."""
    global engine, SessionLocal

    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
        engine.connect()
        _safe_print("[DB] Conectado a PostgreSQL")
    except Exception as e:
        # Log del error real para diagnosticar problemas de conexion
        err_type = type(e).__name__
        err_msg = str(e).encode("utf-8", errors="replace").decode("utf-8")
        _safe_print(f"[DB] Fallo PostgreSQL ({err_type}): {err_msg}")
        _safe_print(f"[DB] URL usada: {DATABASE_URL.replace('://', '://***:***@')}")
        sqlite_path = os.path.join(os.path.dirname(__file__), "..", "dashboard.db")
        engine = create_engine(f"sqlite:///{os.path.abspath(sqlite_path)}", echo=False)
        _safe_print("[DB] Fallback a SQLite local.")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


_create_engine_with_fallback()


def get_db():
    """Retorna una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    """Context manager para sesiones de base de datos."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
