from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class CodigoBarras(Base):
    __tablename__ = "codigo_barras"

    id_codigo_barras = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    codigo = Column(String(100), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    producto = relationship("Producto", back_populates="codigos_barra")


class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto", ondelete="CASCADE"))
    nombre = Column(String(100))
    tipo = Column(String(50))
    orden = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    producto = relationship("Producto", back_populates="imagenes")


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    productos = relationship("Producto", back_populates="categoria")


class Unidad(Base):
    __tablename__ = "unidades"

    id_unidad = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    abreviatura = Column(String(200), nullable=False)

    # Relaciones
    productos = relationship("Producto", back_populates="unidad")


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"))
    id_unidad = Column(Integer, ForeignKey("unidades.id_unidad"))
    stock_actual = Column(Numeric(10, 2), nullable=False, default=0)
    stock_minimo = Column(Numeric(10, 2), nullable=False, default=5)
    precio_costo = Column(Numeric(10, 2), nullable=False, default=0)
    precio_venta = Column(Numeric(10, 2), nullable=False, default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    categoria = relationship("Categoria", back_populates="productos")
    precios = relationship("ListaPrecioItem", back_populates="producto")
    unidad = relationship("Unidad", back_populates="productos")
    imagenes = relationship("Imagen", back_populates="producto", cascade="all, delete-orphan")
    codigos_barra = relationship("CodigoBarras", back_populates="producto")
    items_venta = relationship("ItemVenta", back_populates="producto")
    items_compra = relationship("EgresoCompraItem", back_populates="producto")
