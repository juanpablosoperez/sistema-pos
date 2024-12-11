from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    DECIMAL,
    DateTime
)
from sqlalchemy.orm import relationship

from .base import Base


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    codigo_interno = Column(String(50), unique=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    marca = Column(String(100))
    modelo = Column(String(100))
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"))
    unidad_medida = Column(String(20))
    peso = Column(DECIMAL(10, 3))
    dimension = Column(String(50))
    stock_actual = Column(DECIMAL(10, 3), default=0, nullable=False)
    stock_minimo = Column(DECIMAL(10, 3), default=0, nullable=False)
    precio_costo = Column(DECIMAL(10, 2), default=0, nullable=False)
    precio_venta = Column(DECIMAL(10, 2), default=0, nullable=False)
    margen_ganancia = Column(DECIMAL(5, 2), default=0, nullable=False)
    iva = Column(DECIMAL(5, 2), default=0, nullable=False)
    notas = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    categoria = relationship("Categoria", back_populates="productos")
    codigos_barras = relationship("CodigoBarra", back_populates="producto")

    def __repr__(self):
        return f"<Producto {self.nombre}>"


class CodigoBarra(Base):
    __tablename__ = "codigo_barras"

    id_codigo_barras = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    codigo = Column(String(100), unique=True, nullable=False)
    principal = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    producto = relationship("Producto", back_populates="codigos_barras")

    def __repr__(self):
        return f"<CodigoBarra {self.codigo}>"
