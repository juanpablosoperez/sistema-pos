from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    DateTime,
    DECIMAL
)
from sqlalchemy.orm import relationship

from .base import Base


class Compra(Base):
    __tablename__ = "compras"

    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    numero_factura = Column(String(50), nullable=False, unique=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"))
    fecha = Column(DateTime, nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    iva_total = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    observaciones = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    proveedor = relationship("Proveedor")
    usuario = relationship("Usuario")
    items = relationship("ItemCompra", back_populates="compra")

    def __repr__(self):
        return f"<Compra {self.numero_factura}>"


class ItemCompra(Base):
    __tablename__ = "items_compra"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_compra = Column(Integer, ForeignKey("compras.id_compra"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(DECIMAL(10, 3), nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    iva = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    compra = relationship("Compra", back_populates="items")
    producto = relationship("Producto")

    def __repr__(self):
        return f"<ItemCompra compra_id={self.id_compra}, producto_id={self.id_producto}>"
