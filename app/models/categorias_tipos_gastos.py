from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)
from sqlalchemy.orm import relationship
from .base import Base


class CategoriaGasto(Base):
    __tablename__ = "categorias_gastos"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    gastos = relationship("Gasto", back_populates="categoria")

    def __repr__(self):
        return f"<CategoriaGasto {self.nombre}>"


class TipoGasto(Base):
    __tablename__ = "tipos_gastos"

    id_tipo_gasto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    gastos = relationship("Gasto", back_populates="tipo_gasto")

    def __repr__(self):
        return f"<TipoGasto {self.nombre}>"
