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

# Definir la tabla de asociación
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

    # La relación con usuarios se define aquí
    usuarios = relationship("Usuario", secondary=usuarios_modulos, back_populates="modulos")

    def to_dict(self):
        return {"id_modulo": self.id_modulo, "nombre": self.nombre, "descripcion": self.descripcion, "icono": self.icono, "ruta": self.ruta}
