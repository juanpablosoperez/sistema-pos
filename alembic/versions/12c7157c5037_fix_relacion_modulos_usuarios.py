"""fix relacion modulos usuarios

Revision ID: 12c7157c5037
Revises: 757271bdc879
Create Date: 2024-12-09 01:11:59.932388

"""

from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "12c7157c5037"
down_revision: Union[str, None] = "757271bdc879"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "modulos",
        sa.Column("id_modulo", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("icono", sa.String(length=50), nullable=True),
        sa.Column("ruta", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id_modulo"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_table(
        "usuarios_modulos",
        sa.Column("id_usuario", sa.Integer(), nullable=True),
        sa.Column("id_modulo", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_modulo"],
            ["modulos.id_modulo"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario"],
            ["usuarios.id_usuario"],
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("usuarios_modulos")
    op.drop_table("modulos")
    # ### end Alembic commands ###
