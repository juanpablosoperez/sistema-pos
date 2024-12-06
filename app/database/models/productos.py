from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
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
    peso = Column(Numeric(10, 3))
    dimension = Column(String(50))
    stock_actual = Column(Numeric(10, 3), nullable=False, default=0)
    stock_minimo = Column(Numeric(10, 3), nullable=False, default=0)
    precio_costo = Column(Numeric(10, 2), nullable=False, default=0)
    precio_venta = Column(Numeric(10, 2), nullable=False, default=0)
    margen_ganancia = Column(Numeric(5, 2), nullable=False, default=0)
    iva = Column(Numeric(5, 2), nullable=False, default=0)
    notas = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    categoria = relationship("Categoria", back_populates="productos")
    codigos_barras = relationship("CodigoBarras", back_populates="producto", cascade="all, delete-orphan")


class CodigoBarras(Base):
    __tablename__ = "codigo_barras"

    id_codigo_barras = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    codigo = Column(String(100), unique=True, nullable=False)
    principal = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())

    producto = relationship("Producto", back_populates="codigos_barras")


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    productos = relationship("Producto", back_populates="categoria")
