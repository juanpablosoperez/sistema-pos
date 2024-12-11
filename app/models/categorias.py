from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship

from .base import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    id_categoria_padre = Column(Integer, ForeignKey("categorias.id_categoria"))
    nivel = Column(Integer, default=1)
    ruta_completa = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    productos = relationship("Producto", back_populates="categoria")
    subcategorias = relationship("Categoria", backref="categoria_padre", remote_side=[id_categoria])

    def __repr__(self):
        return f"<Categoria {self.nombre}>"
