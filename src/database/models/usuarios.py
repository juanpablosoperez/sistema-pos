# src/app/models/usuarios.py
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    telefono = Column(String(50))
    direccion = Column(Text)
    fecha_nacimiento = Column(DateTime)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"))
    activo = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    rol = relationship("Role", back_populates="usuarios")
