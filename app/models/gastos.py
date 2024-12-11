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


class Gasto(Base):
    __tablename__ = "gastos"

    id_gasto = Column(Integer, primary_key=True, autoincrement=True)
    id_categoria = Column(Integer, ForeignKey("categorias_gastos.id_categoria"))
    id_tipo_gasto = Column(Integer, ForeignKey("tipos_gastos.id_tipo_gasto"))
    id_compra = Column(Integer, ForeignKey("compras.id_compra"))
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"))
    monto = Column(DECIMAL(10, 2), nullable=False)
    fecha_gasto = Column(DateTime, nullable=False)
    es_credito = Column(Boolean, default=False)
    estado = Column(String(1), default='P')  # P: Pendiente, C: Completado, A: Anulado
    fecha_vencimiento = Column(DateTime)
    concepto = Column(String(200), nullable=False)
    referencia = Column(String(100))
    comprobante = Column(String(100))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_cierre_caja = Column(Integer, ForeignKey("cierres_caja.id_cierre"))
    observaciones = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    categoria = relationship("CategoriaGasto")
    tipo_gasto = relationship("TipoGasto")
    compra = relationship("Compra")
    proveedor = relationship("Proveedor")
    usuario = relationship("Usuario")
    cierre_caja = relationship("CierreCaja")

    def __repr__(self):
        return f"<Gasto id={self.id_gasto}, monto={self.monto}, estado={self.estado}>"
