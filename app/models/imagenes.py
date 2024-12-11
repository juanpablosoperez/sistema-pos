from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)
from .base import Base


class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen = Column(Integer, primary_key=True, autoincrement=True)
    entidad = Column(String(50), nullable=False)
    id_entidad = Column(Integer, nullable=False)
    url = Column(String(255), nullable=False)
    nombre = Column(String(100))
    tipo = Column(String(50))
    orden = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Imagen {self.nombre or self.url}>"
