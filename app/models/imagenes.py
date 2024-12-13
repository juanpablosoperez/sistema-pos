from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from .base import Base


class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen = Column(Integer, primary_key=True)
    entidad = Column(String(50), nullable=False)
    id_entidad = Column(Integer, nullable=False)
    url = Column(String(255), nullable=False)
    nombre_archivo = Column(String(100))
    es_principal = Column(Boolean, default=False)
    orden = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
