# movimientos.py
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from app.models.enums import EstadoMovimiento
from app.models.enums import FormaPago
from app.models.enums import Naturaleza
from app.models.enums import TipoComprobante
from app.models.enums import TipoEntidad


class TipoMovimiento(Base):
    __tablename__ = "tipos_movimiento"

    id_tipo_movimiento = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    naturaleza = Column(Enum(Naturaleza), nullable=False)
    afecta_stock = Column(Boolean, default=False)
    requiere_productos = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    movimientos = relationship("Movimiento", back_populates="tipo_movimiento")


class Movimiento(Base):
    __tablename__ = "movimientos"

    id_movimiento = Column(Integer, primary_key=True)
    id_tipo_movimiento = Column(Integer, ForeignKey("tipos_movimiento.id_tipo_movimiento"), nullable=False)
    numero_comprobante = Column(String(50), nullable=True)
    tipo_comprobante = Column(Enum(TipoComprobante), nullable=True)
    fecha = Column(DateTime, nullable=False)
    tipo_entidad = Column(Enum(TipoEntidad), nullable=False)
    id_entidad = Column(Integer)
    requiere_pago_completo = Column(Boolean, default=True)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    iva = Column(Numeric(12, 2), nullable=False, default=0)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    estado = Column(Enum(EstadoMovimiento), default="PENDIENTE")
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_caja = Column(Integer, ForeignKey("caja_diaria.id_caja"))
    notas = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
    usuario = relationship("Usuario", back_populates="movimientos")
    productos = relationship("MovimientoProducto", back_populates="movimiento")
    pagos = relationship("MovimientoPago", back_populates="movimiento")
    stock_movimientos = relationship("MovimientoStock", back_populates="movimiento")
    caja_diaria = relationship("CajaDiaria", back_populates="movimientos")

    # Relaciones dinámicas según tipo_entidad
    cliente = relationship(
        "Cliente", 
        primaryjoin="and_(Movimiento.tipo_entidad == 'CLIENTE', "
                    "Movimiento.id_entidad == Cliente.id_cliente)",
        foreign_keys=[id_entidad],
        backref="movimientos",
        uselist=False,
        passive_deletes=True,  # No elimina el cliente si se elimina el movimiento
        lazy='select'  # Carga selectiva cuando se accede
    )

    proveedor = relationship(
        "Proveedor", 
        primaryjoin="and_(Movimiento.tipo_entidad == 'PROVEEDOR', "
                    "Movimiento.id_entidad == Proveedor.id_proveedor)",
        foreign_keys=[id_entidad],
        backref="movimientos",
        uselist=False,
        passive_deletes=True,  # No elimina el proveedor si se elimina el movimiento
        lazy='select'  # Carga selectiva cuando se accede
    )


class MovimientoProducto(Base):
    __tablename__ = "movimientos_productos"

    id_detalle = Column(Integer, primary_key=True)
    id_movimiento = Column(Integer, ForeignKey("movimientos.id_movimiento"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Numeric(12, 3), nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    iva_unitario = Column(Numeric(12, 2), nullable=False, default=0)
    subtotal = Column(Numeric(12, 2), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    movimiento = relationship("Movimiento", back_populates="productos")
    producto = relationship("Producto", back_populates="movimientos_productos")


class MovimientoPago(Base):
    __tablename__ = "movimientos_pagos"

    id_pago = Column(Integer, primary_key=True)
    id_movimiento = Column(Integer, ForeignKey("movimientos.id_movimiento"), nullable=False)
    forma_pago = Column(Enum(FormaPago), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    referencia = Column(String(100))
    fecha_pago = Column(DateTime, default=func.current_timestamp(), nullable=False)
    estado = Column(Enum("PENDIENTE", "APROBADO", "RECHAZADO"), default="PENDIENTE")

    # Relaciones
    movimiento = relationship("Movimiento", back_populates="pagos")


class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"

    id_movimiento_stock = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_movimiento = Column(Integer, ForeignKey("movimientos.id_movimiento"), nullable=False)
    tipo_movimiento = Column(Enum(Naturaleza), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False)
    stock_anterior = Column(Numeric(10, 2), nullable=False)
    stock_actual = Column(Numeric(10, 2), nullable=False)
    fecha = Column(DateTime, default=func.current_timestamp())
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    # Relaciones
    producto = relationship("Producto")
    movimiento = relationship("Movimiento", back_populates="stock_movimientos")
    usuario = relationship("Usuario")
