from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLAlchemyEnum
from .enums import FormaPago, EstadoMovimiento

from .base import Base


class Venta(Base):
    __tablename__ = 'ventas'

    id_venta = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=True)
    fecha = Column(DateTime, nullable=False, default=func.current_timestamp())
    subtotal = Column(Numeric(10,2), nullable=True)
    iva_total = Column(Numeric(10,2), nullable=True)
    descuento = Column(Numeric(10,2), default=0, nullable=True)
    total = Column(Numeric(10,2), nullable=False)
    forma_pago = Column(SQLAlchemyEnum(FormaPago), default=FormaPago.EFECTIVO, nullable=False)  # E: Efectivo, T: Tarjeta, C: Transferencia, D: Depósito
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    id_caja = Column(Integer, ForeignKey('caja_diaria.id_caja'))
    observaciones = Column(Text)
    estado = Column(SQLAlchemyEnum(EstadoMovimiento), nullable=False, default=EstadoMovimiento.PENDIENTE)  # P: Pendiente, C: Completado, A: Anulado
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    cliente = relationship("Cliente", back_populates="ventas")
    usuario = relationship("Usuario", back_populates="ventas")
    caja_diaria = relationship("CajaDiaria", back_populates="ventas")
    items = relationship("ItemVenta", back_populates="venta", cascade="all, delete-orphan")

class ItemVenta(Base):
    __tablename__ = 'items_venta'

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey('ventas.id_venta'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)
    cantidad = Column(Numeric(10,3), nullable=False)
    precio_unitario = Column(Numeric(10,2), nullable=False)
    descuento = Column(Numeric(10,2), default=0, nullable=True)
    iva = Column(Numeric(10,2), nullable=True)
    subtotal = Column(Numeric(10,2), nullable=True)
    total = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    venta = relationship("Venta", back_populates="items")
    producto = relationship("Producto", back_populates="items_venta")