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

from app.models.imagenes import Imagen

from .base import Base

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import foreign, remote

from .base import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Use foreign() and remote() to explicitly define the join condition
    imagenes = relationship(
        Imagen, 
        primaryjoin="and_(foreign(Categoria.id_categoria) == remote(Imagen.id_entidad), "
                    "Imagen.entidad == 'CATEGORIA')",
        backref="categoria"
    )

    # Existing relationship
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"))
    stock_actual = Column(Numeric(10, 2), nullable=False, default=0)
    stock_minimo = Column(Numeric(10, 2), nullable=False, default=5)
    precio_costo = Column(Numeric(10, 2), nullable=False, default=0)
    precio_venta = Column(Numeric(10, 2), nullable=False, default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    categoria = relationship("Categoria", back_populates="productos")
    movimientos_productos = relationship("MovimientoProducto", back_populates="producto")
    imagenes = relationship("Imagen", primaryjoin="and_(Producto.id_producto==Imagen.id_entidad, " "Imagen.entidad=='PRODUCTO')")
    proveedores = relationship("ProductoProveedor", back_populates="producto")
    imagenes = relationship(
        "Imagen", 
        primaryjoin="and_(Producto.id_producto == Imagen.id_entidad, "
                    "Imagen.entidad == 'PRODUCTO')",
        foreign_keys=[Imagen.id_entidad],
        backref="producto"
    )