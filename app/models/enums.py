



# app/models/enums.py
from enum import Enum




class TipoComprobante(Enum):
    FACTURA = "FACTURA"
    BOLETA = "BOLETA"
    NOTA_CREDITO = "NOTA_CREDITO"
    RECIBO = "RECIBO"
    INTERNO = "INTERNO"


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


class Naturaleza(Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"


class EstadoCaja(Enum):
    ABIERTO = "A"
    CERRADO = "C"
