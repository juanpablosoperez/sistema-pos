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


class Credito(Base):
    __tablename__ = "creditos"

    id_credito = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"), unique=True, nullable=False)
    monto_pagado = Column(DECIMAL(10, 2), default=0)
    saldo_pendiente = Column(DECIMAL(10, 2), nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
    estado = Column(String(1), default='A')  # A: Activo, C: Cancelado
    observaciones = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    venta = relationship("Venta")
    pagos = relationship("PagoCredito", back_populates="credito")

    def __repr__(self):
        return f"<Credito id={self.id_credito}, saldo_pendiente={self.saldo_pendiente}>"


class PagoCredito(Base):
    __tablename__ = "pagos_creditos"

    id_pago = Column(Integer, primary_key=True, autoincrement=True)
    id_credito = Column(Integer, ForeignKey("creditos.id_credito"), nullable=False)
    fecha_pago = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    monto = Column(DECIMAL(10, 2), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    observaciones = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    credito = relationship("Credito", back_populates="pagos")
    usuario = relationship("Usuario")

    def __repr__(self):
        return f"<PagoCredito id={self.id_pago}, monto={self.monto}>"
