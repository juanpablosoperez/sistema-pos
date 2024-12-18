# app/models/enums.py
from enum import Enum

class TipoEntidad(Enum):
    CLIENTE = "CLIENTE"
    PROVEEDOR = "PROVEEDOR"
    PUBLICO_GENERAL = "PUBLICO_GENERAL"

class EstadoMovimiento(Enum):
    PENDIENTE = "PENDIENTE"
    COMPLETADO = "COMPLETADO"
    ANULADO = "ANULADO"


class FormaPago(Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    CREDITO = "CREDITO"

class EstadoCaja(Enum):
    ABIERTO = "A"
    CERRADO = "C"

class TipoEgreso(Enum):
    COMPRA = "COMPRA"
    SERVICIO = "SERVICIO"
    SUELDO = "SUELDO"
    GEO = "GEO"  # Gastos extraordinarios