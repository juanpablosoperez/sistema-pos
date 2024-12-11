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


class Venta(Base):
    __tablename__ = "ventas"

    id_venta = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    iva_total = Column(DECIMAL(10, 2), nullable=False)
    descuento = Column(DECIMAL(10, 2), default=0)
    total = Column(DECIMAL(10, 2), nullable=False)
    forma_pago = Column(String(1), nullable=False)  # E: Efectivo, T: Tarjeta, C: Crédito, D: Débito
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_cierre_caja = Column(Integer, ForeignKey("cierres_caja.id_cierre"))
    observaciones = Column(Text)
    estado = Column(String(1), default='P')  # P: Pendiente, C: Completada, A: Anulada
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    cliente = relationship("Cliente")
    usuario = relationship("Usuario")
    cierre_caja = relationship("CierreCaja")
    items = relationship("ItemVenta", back_populates="venta")

    def __repr__(self):
        return f"<Venta id={self.id_venta}, total={self.total}>"


class ItemVenta(Base):
    __tablename__ = "items_venta"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(DECIMAL(10, 3), nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    descuento = Column(DECIMAL(10, 2), default=0)
    iva = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    venta = relationship("Venta", back_populates="items")
    producto = relationship("Producto")

    def __repr__(self):
        return f"<ItemVenta venta_id={self.id_venta}, producto_id={self.id_producto}>"
