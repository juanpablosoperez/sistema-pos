from datetime import datetime, timezone
from sqlalchemy import Boolean, Table, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base

# Tabla de asociación para roles y módulos
roles_modulos = Table(
    'roles_modulos',
    Base.metadata,
    Column('id_rol', Integer, ForeignKey('roles.id_rol'), primary_key=True),
    Column('id_modulo', Integer, ForeignKey('modulos.id_modulo'), primary_key=True)
)

class Modulo(Base):
    __tablename__ = "modulos"

    id_modulo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(255))
    icono = Column(String(50))
    ruta = Column(String(100))
    orden = Column(Integer)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relaciones
    roles = relationship("Role", secondary=roles_modulos, back_populates="modulos")

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

class Role(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")
    modulos = relationship("Modulo", secondary=roles_modulos, back_populates="roles")

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column("password", String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"))
    activo = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    rol = relationship("Role", back_populates="usuarios")
    ventas = relationship("Venta", back_populates="usuario")
    egresos = relationship("Egreso", back_populates="usuario")
    cajas_apertura = relationship("CajaDiaria", foreign_keys="[CajaDiaria.id_usuario_apertura]", back_populates="usuario_apertura")
    cajas_cierre = relationship("CajaDiaria", foreign_keys="[CajaDiaria.id_usuario_cierre]", back_populates="usuario_cierre")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "username": self.username,
            "nombre": self.nombre,
            "email": self.email,
            "id_rol": self.id_rol,
            "rol_nombre": self.rol.nombre if self.rol else None,
            "activo": self.activo,
            # Ahora obtenemos los módulos a través del rol
            "modulos": [modulo.to_dict() for modulo in self.rol.modulos] if self.rol else [],
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia de Usuario desde un diccionario"""
        return cls(
            username=data.get("username"),
            nombre=data.get("nombre"),
            email=data.get("email"),
            id_rol=data.get("id_rol"),
            activo=data.get("activo", True),
        )

    def update_last_login(self):
        """Actualiza la fecha del último acceso"""
        self.ultimo_acceso = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<Usuario {self.username}>"