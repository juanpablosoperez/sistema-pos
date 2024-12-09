from datetime import datetime
from datetime import timezone

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .base import Base
from .modulos import usuarios_modulos


class Role(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuarios = relationship("Usuario", back_populates="rol", lazy="dynamic")

    def __repr__(self):
        return f"<Role {self.nombre}>"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column("password", String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    telefono = Column(String(50))
    direccion = Column(Text)
    fecha_nacimiento = Column(DateTime)
    id_rol = Column(Integer, ForeignKey("roles.id_rol", ondelete="SET NULL"))
    activo = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    rol = relationship("Role", back_populates="usuarios")
    modulos = relationship("Modulo", secondary=usuarios_modulos, back_populates="usuarios")

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
            "modulos": [modulo.to_dict() for modulo in self.modulos],  # Añadido
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
