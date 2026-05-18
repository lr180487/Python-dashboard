"""Database session configuration.

PostgreSQL with SQLite fallback.
"""

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).parent.parent / ".env")

_raw_url = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/dashboard"
)
DATABASE_URL = _raw_url

engine = None
SessionLocal = None


def _add_client_encoding_to_url(url: str) -> str:
    """Add UTF-8 client encoding to PostgreSQL URLs."""
    parsed = urlparse(url)
    if parsed.scheme not in (
        "postgresql",
        "postgres",
        "postgresql+psycopg2",
        "postgresql+psycopg",
    ):
        return url

    query = parse_qs(parsed.query)
    query["client_encoding"] = ["utf8"]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def _safe_print(msg: str) -> None:
    """Print to stdout with UTF-8 encoding (Windows safe)."""
    try:
        sys.stdout.buffer.write(f"{msg}\n".encode("utf-8", errors="replace"))
    except Exception:
        pass


def _create_engine_with_fallback() -> None:
    """Try PostgreSQL, fallback to SQLite."""
    global engine, SessionLocal

    database_url = _add_client_encoding_to_url(DATABASE_URL)

    try:
        engine = create_engine(database_url, pool_pre_ping=True, echo=False)
        engine.connect()
        _safe_print("[DB] Connected to PostgreSQL")
    except Exception as e:
        err_type = type(e).__name__
        err_msg = str(e).encode("utf-8", errors="replace").decode("utf-8")
        _safe_print(f"[DB] PostgreSQL failed ({err_type}): {err_msg}")
        _safe_print(f"[DB] URL: {database_url.replace('://', '://***:***@')}")

        sqlite_path = os.path.join(os.path.dirname(__file__), "..", "dashboard.db")
        engine = create_engine(f"sqlite:///{os.path.abspath(sqlite_path)}", echo=False)
        _safe_print("[DB] Fallback to local SQLite.")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


_create_engine_with_fallback()


def get_db():
    """Get database session generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
