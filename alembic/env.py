"""Alembic environment configuration."""

import os
import sys
from logging.config import fileConfig
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from sqlalchemy import create_engine, pool

from alembic import context

# ── Asegurar que el proyecto esté en sys.path ──
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ── Importar modelos para autogenerate ──
from database.models import Base

target_metadata = Base.metadata

# ── Configuración ──
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _add_client_encoding(url: str) -> str:
    """Asegura client_encoding=utf8 en URLs PostgreSQL."""
    parsed = urlparse(url)
    if parsed.scheme not in ("postgresql", "postgres", "postgresql+psycopg2"):
        return url
    query = parse_qs(parsed.query)
    query["client_encoding"] = ["utf8"]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def _get_database_url() -> str:
    """Lee DATABASE_URL del entorno; si no existe, usa la de alembic.ini."""
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return _add_client_encoding(env_url)
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = _get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = _get_database_url()
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
