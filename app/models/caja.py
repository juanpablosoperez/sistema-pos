from sqlalchemy import Column, DateTime, Enum as SQLAlchemyEnum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.enums import EstadoCaja

from .base import Base

class CajaDiaria(Base):
    __tablename__ = "caja_diaria"
    id_caja = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    hora_apertura = Column(DateTime, nullable=False, default=func.current_timestamp())
    hora_cierre = Column(DateTime, nullable=True)
    monto_inicial = Column(Numeric(10, 2), nullable=False)
    total_ventas_efectivo = Column(Numeric(10, 2), default=0)
    total_ventas_tarjeta = Column(Numeric(10, 2), default=0)
    total_ventas_transferencia = Column(Numeric(10, 2), default=0)
    total_pagos = Column(Numeric(10, 2), default=0)
    monto_final_sistema = Column(Numeric(10, 2), nullable=True)
    monto_final_real = Column(Numeric(10, 2), nullable=True)
    diferencia = Column(Numeric(10, 2), nullable=True)
    estado = Column(SQLAlchemyEnum(EstadoCaja), default=EstadoCaja.ABIERTO)
    id_usuario_apertura = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_usuario_cierre = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    usuario_apertura = relationship("Usuario", foreign_keys=[id_usuario_apertura])
    usuario_cierre = relationship("Usuario", foreign_keys=[id_usuario_cierre])
    movimientos = relationship("Movimiento", back_populates="caja_diaria")

    def __repr__(self):
        return f"<CajaDiaria fecha={self.fecha}, estado={self.estado.value}>"