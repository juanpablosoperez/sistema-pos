from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    DECIMAL
)
from .base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(3), nullable=False)
    numero_documento = Column(String(20), nullable=False, unique=True)
    razon_social = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200))
    direccion = Column(Text)
    telefono = Column(String(50))
    email = Column(String(100))
    limite_credito = Column(DECIMAL(10, 2), default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Cliente {self.razon_social}>"
