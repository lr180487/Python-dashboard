"""create_users_and_ventas_tables

Revision ID: 025bdc950ff5
Revises:
Create Date: 2026-05-08 01:50:51.488656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "025bdc950ff5"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crea tablas users y ventas."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("roles", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("failed_login_attempts", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "ventas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=True),
        sa.Column("categoria", sa.String(length=50), nullable=False),
        sa.Column("ventas", sa.Float(), nullable=True),
        sa.Column("unidades", sa.Integer(), nullable=True),
        sa.Column("clientes", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ventas_categoria", "ventas", ["categoria"], unique=False)
    op.create_index("ix_ventas_fecha", "ventas", ["fecha"], unique=False)
    op.create_index("ix_ventas_id", "ventas", ["id"], unique=False)


def downgrade() -> None:
    """Elimina tablas users y ventas."""
    op.drop_index("ix_ventas_id", table_name="ventas")
    op.drop_index("ix_ventas_fecha", table_name="ventas")
    op.drop_index("ix_ventas_categoria", table_name="ventas")
    op.drop_table("ventas")

    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
