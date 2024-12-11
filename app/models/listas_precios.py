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


class ListaPrecios(Base):
    __tablename__ = "lista_precios"

    id_lista = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    items = relationship("ListaPreciosItem", back_populates="lista")

    def __repr__(self):
        return f"<ListaPrecios {self.nombre}>"


class ListaPreciosItem(Base):
    __tablename__ = "lista_precios_items"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_lista = Column(Integer, ForeignKey("lista_precios.id_lista"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    lista = relationship("ListaPrecios", back_populates="items")
    producto = relationship("Producto")

    def __repr__(self):
        return f"<ListaPreciosItem lista_id={self.id_lista}, producto_id={self.id_producto}, precio={self.precio}>"
