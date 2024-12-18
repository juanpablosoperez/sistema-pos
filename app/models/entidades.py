# entidades.py
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    dni = Column(String(20), unique=True)
    telefono = Column(String(50), nullable=False)
    email = Column(String(100))
    limite_credito = Column(Numeric(12, 2), default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    ventas = relationship("Venta", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(nombre={self.nombre})>"


class Proveedor(Base):
    __tablename__ = "proveedores"

    id_proveedor = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    dni = Column(String(20), unique=True)
    telefono = Column(String(50))
    email = Column(String(100))
    es_frecuente = Column(Boolean)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


    compras = relationship("EgresoCompra", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor(nombre={self.nombre})>"


