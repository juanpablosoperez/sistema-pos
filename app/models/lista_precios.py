from sqlalchemy import Boolean, Numeric
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .base import Base


class ListaPrecio(Base):
    __tablename__ = 'lista_precios'

    id_lista = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    items = relationship("ListaPrecioItem", back_populates="lista_precio", cascade="all, delete-orphan")
    

class ListaPrecioItem(Base):
    __tablename__ = 'lista_precios_items'

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_lista = Column(Integer, ForeignKey('lista_precios.id_lista'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)
    precio = Column(Numeric(10,2), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    lista_precio = relationship("ListaPrecio", back_populates="items")
    producto = relationship("Producto", back_populates="precios")