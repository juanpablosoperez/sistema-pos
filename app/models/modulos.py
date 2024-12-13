from datetime import datetime
from datetime import timezone

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from .base import Base

# Tabla de asociación
usuarios_modulos = Table(
    "usuarios_modulos",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuarios.id_usuario")),
    Column("id_modulo", Integer, ForeignKey("modulos.id_modulo")),
    extend_existing=True,
)


class Modulo(Base):
    __tablename__ = "modulos"

    id_modulo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(255))
    icono = Column(String(50))
    ruta = Column(String(100))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación con usuarios
    usuarios = relationship("Usuario", secondary=usuarios_modulos, back_populates="modulos")

    def __init__(self, nombre: str, icono: str, ruta: str = None, descripcion: str = None):
        self.nombre = nombre
        self.icono = icono
        self.ruta = ruta
        self.descripcion = descripcion

    def to_dict(self):
        return {
            "id_modulo": self.id_modulo,
            "nombre": self.nombre,
            "icono": self.icono,
            "ruta": self.ruta,
            "descripcion": self.descripcion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Modulo {self.nombre}>"
