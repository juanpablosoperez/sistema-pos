from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    DateTime,
    DECIMAL
)
from sqlalchemy.orm import relationship

from .base import Base


class CierreCaja(Base):
    __tablename__ = "cierres_caja"

    id_cierre = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    hora_apertura = Column(DateTime, nullable=False)
    hora_cierre = Column(DateTime)
    monto_inicial = Column(DECIMAL(10, 2), nullable=False)
    total_ventas_efectivo = Column(DECIMAL(10, 2), default=0)
    total_ventas_tarjeta = Column(DECIMAL(10, 2), default=0)
    total_ventas_transferencia = Column(DECIMAL(10, 2), default=0)
    total_pagos = Column(DECIMAL(10, 2), default=0)
    monto_final_sistema = Column(DECIMAL(10, 2))
    monto_final_real = Column(DECIMAL(10, 2))
    diferencia = Column(DECIMAL(10, 2))
    estado = Column(String(1), default='A')  # A: Abierto, C: Cerrado
    id_usuario_apertura = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_usuario_cierre = Column(Integer, ForeignKey("usuarios.id_usuario"))
    observaciones = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario_apertura = relationship("Usuario", foreign_keys=[id_usuario_apertura])
    usuario_cierre = relationship("Usuario", foreign_keys=[id_usuario_cierre])

    def __repr__(self):
        return f"<CierreCaja fecha={self.fecha}, estado={self.estado}>"
