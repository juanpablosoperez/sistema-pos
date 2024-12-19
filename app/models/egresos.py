from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .enums import EstadoMovimiento
from .enums import TipoEgreso


class Egreso(Base):
    __tablename__ = "egresos"

    id_egreso = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    tipo_egreso = Column(SQLAlchemyEnum(TipoEgreso), nullable=False, default=TipoEgreso.COMPRA)
    estado = Column(SQLAlchemyEnum(EstadoMovimiento), nullable=False, default=EstadoMovimiento.COMPLETADO)  # P: Pendiente, C: Completado, A: Anulado
    comprobante = Column(String(100))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_caja = Column(Integer, ForeignKey("caja_diaria.id_caja"), nullable=False)
    observaciones = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    usuario = relationship("Usuario", back_populates="egresos")
    caja_diaria = relationship("CajaDiaria", back_populates="egresos")


class EgresoCompra(Base):
    __tablename__ = "egresos_compras"

    id_egreso_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)
    id_egreso = Column(Integer, ForeignKey("egresos.id_egreso"), nullable=False)
    numero_factura = Column(String(50), nullable=False, unique=True)
    subtotal = Column(Numeric(10, 2), nullable=False)
    iva_total = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    egreso = relationship("Egreso", backref="compra", uselist=False)
    proveedor = relationship("Proveedor", back_populates="compras")
    items = relationship("EgresoCompraItem", back_populates="compra", cascade="all, delete-orphan")


class EgresoCompraItem(Base):
    __tablename__ = "egresos_compras_items"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_egreso_compra = Column(Integer, ForeignKey("egresos_compras.id_egreso_compra"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    cantidad = Column(Numeric(10, 3), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    iva = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    compra = relationship("EgresoCompra", back_populates="items")
    producto = relationship("Producto", back_populates="items_compra")


class EgresoServicio(Base):
    __tablename__ = "egresos_servicios"

    id_egreso_servicio = Column(Integer, primary_key=True, autoincrement=True)
    id_egreso = Column(Integer, ForeignKey("egresos.id_egreso"), nullable=False)
    tipo_servicio = Column(String(50), nullable=False)
    periodo_inicio = Column(DateTime)
    periodo_fin = Column(DateTime)
    numero_referencia = Column(String(100))
    concepto = Column(String(200), nullable=False)

    # Relaciones
    egreso = relationship("Egreso", backref="servicio", uselist=False)


class EgresoGasto(Base):
    __tablename__ = "egresos_gastos"

    id_egreso_gasto = Column(Integer, primary_key=True, autoincrement=True)
    id_egreso = Column(Integer, ForeignKey("egresos.id_egreso"), nullable=False)
    concepto = Column(String(200), nullable=False)

    # Relaciones
    egreso = relationship("Egreso", backref="gasto", uselist=False)
