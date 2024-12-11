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


class Proveedor(Base):
    __tablename__ = "proveedores"

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    razon_social = Column(String(200), nullable=False)
    rut = Column(String(20), unique=True, nullable=False)
    direccion = Column(Text)
    telefono = Column(String(50))
    email = Column(String(100))
    contacto_nombre = Column(String(100))
    contacto_telefono = Column(String(50))
    dias_credito = Column(Integer, default=0)
    limite_credito = Column(DECIMAL(10, 2), default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Proveedor {self.razon_social}>"
