"""Alembic environment configuration."""

# ======================================================
# STANDARD LIBRARY
# ======================================================
import os
import sys
from logging.config import fileConfig
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

# ======================================================
# THIRD-PARTY IMPORTS
# ======================================================
from alembic import context

# ======================================================
# LOCAL IMPORTS
# ======================================================

# Agregar raíz del proyecto al PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Cargar variables de entorno
load_dotenv(BASE_DIR / ".env")

# Importar modelos para autogenerate
from database.models import Base  # noqa: E402

# ======================================================
# ALEMBIC CONFIG
# ======================================================
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ======================================================
# DATABASE URL HELPERS
# ======================================================
def _add_client_encoding(url: str) -> str:
    """Ensure PostgreSQL uses UTF-8 client encoding."""
    parsed = urlparse(url)

    if parsed.scheme not in (
        "postgresql",
        "postgres",
        "postgresql+psycopg2",
    ):
        return url

    query = parse_qs(parsed.query)
    query["client_encoding"] = ["utf8"]

    new_query = urlencode(query, doseq=True)

    return urlunparse(parsed._replace(query=new_query))


def _get_database_url() -> str:
    """Get database URL from environment or alembic.ini."""
    env_url = os.getenv("DATABASE_URL")

    if env_url:
        return _add_client_encoding(env_url)

    return config.get_main_option("sqlalchemy.url")


# ======================================================
# OFFLINE MIGRATIONS
# ======================================================
def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = _get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ======================================================
# ONLINE MIGRATIONS
# ======================================================
def run_migrations_online() -> None:
    """Run migrations in online mode."""

    url = _get_database_url()

    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ======================================================
# ENTRYPOINT
# ======================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
