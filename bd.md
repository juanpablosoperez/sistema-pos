from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship 
from sqlalchemy import ForeignKey, Integer, String, DECIMAL, Date, CHAR, CheckConstraint, Enum
import enum


Base = declarative_base()


class Unidad(Base):
    __tablename__ = 'unidades'
    
    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)


class Categoria(Base):
    __tablename__ = 'categorias'

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)


class Marca(Base):
    __tablename__ = 'marcas'

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)


class Producto(Base):
    __tablename__ = 'productos'
    __table_args__ = (
        CheckConstraint('cantidad >= 0'),
        CheckConstraint('precio_costo >= 0'),
        CheckConstraint('precio_venta >= 0'),
        CheckConstraint('nivel_reorden >= 0'),
    )

    id: Mapped[int]               = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_unidad: Mapped[int]        = mapped_column(Integer, ForeignKey('unidades.id'), nullable=False)
    id_categoria: Mapped[int]     = mapped_column(Integer, ForeignKey('categorias.id'), nullable=False)
    id_marca: Mapped[int]         = mapped_column(Integer, ForeignKey('marcas.id'), nullable=False)
    cantidad: Mapped[int]         = mapped_column(Integer, nullable=False)
    precio_costo: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    precio_venta: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    nivel_reorden: Mapped[int]    = mapped_column(Integer, nullable=False, default=1)

    unidad    = relationship("Unidad", backref="productos")
    marca     = relationship("Marca", backref="productos")
    categoria = relationship("Categoria", backref="productos")


class Proveedor(Base):
    __tablename__ = 'proveedores'

    id:        Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre:    Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    direccion: Mapped[str] = mapped_column(String(50), nullable=False)
    telefono:  Mapped[str] = mapped_column(CHAR(10), nullable=False, unique=True)
    email:     Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


class Empleado(Base):
    __tablename__ = 'empleados'

    id:              Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str] = mapped_column(String(50), nullable=False)
    direccion:       Mapped[str] = mapped_column(String(50), nullable=False)
    telefono:        Mapped[str] = mapped_column(CHAR(10), nullable=False, unique=True)
    email:           Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    salario:         Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)


class TipoGasto(enum.Enum):
    COMPRA_PROVEEDOR = "Compra a Proveedor"
    SERVICIO = "Servicio"
    NOMINA = "Nómina"
    GENERAL = "Gasto General"


class Gasto(Base):
    __tablename__ = 'gastos'
    __table_args__ = (
        CheckConstraint('monto > 0'),
    )

    id:           Mapped[int]     = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha:        Mapped[Date]    = mapped_column(Date, nullable=False)
    tipo:         Mapped[enum.Enum] = mapped_column(Enum(TipoGasto), nullable=False)
    descripcion:  Mapped[str]     = mapped_column(String(100), nullable=False)
    monto:        Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    id_proveedor: Mapped[int]     = mapped_column(Integer, ForeignKey('proveedores.id'), nullable=True)
    id_empleado:  Mapped[int]     = mapped_column(Integer, ForeignKey('empleados.id'), nullable=True)
    
    proveedor = relationship("Proveedor", backref="gastos")
    empleado  = relationship("Empleado", backref="gastos")


class DetalleGastoCompra(Base):
    __tablename__ = 'detalles_gasto_compra'
    __table_args__ = (
        CheckConstraint('cantidad > 0'),
        CheckConstraint('precio_unitario > 0'),
        CheckConstraint('precio_total > 0'),
    )

    id_gasto:        Mapped[int]     = mapped_column(Integer, ForeignKey('gastos.id'), primary_key=True, nullable=False)
    id_producto:     Mapped[int]     = mapped_column(Integer, ForeignKey('productos.id'), primary_key=True, nullable=False)
    cantidad:        Mapped[int]     = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    precio_total:    Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)

    gasto    = relationship("Gasto", backref="detalles_compra")
    producto = relationship("Producto", backref="detalles_compra")


class Cliente(Base):
    __tablename__ = 'clientes'
    __table_args__ = (
        CheckConstraint('edad >= 18'),
    )

    id:             Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str] = mapped_column(String(50), nullable=False)
    edad:           Mapped[int] = mapped_column(Integer, nullable=False)
    email:          Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


class Venta(Base):
    __tablename__ = 'ventas'
    __table_args__ = (
        CheckConstraint('total >= 0'),
    )

    id:         Mapped[int]     = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int]     = mapped_column(Integer, ForeignKey('clientes.id'), nullable=True)  # Ahora es opcional
    fecha:      Mapped[Date]    = mapped_column(Date, nullable=False)
    total:      Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)

    cliente = relationship("Cliente", backref="ventas")


class DetalleVenta(Base):
    __tablename__ = 'detalles_venta'
    __table_args__ = (
        CheckConstraint('cantidad > 0'),
        CheckConstraint('precio_unitario_venta >= 0'),
        CheckConstraint('precio_total_unidad >= 0'),
    )

    id_venta:              Mapped[int]     = mapped_column(Integer, ForeignKey('ventas.id'), primary_key=True, nullable=False)
    id_producto:           Mapped[int]     = mapped_column(Integer, ForeignKey('productos.id'), primary_key=True, nullable=False)
    cantidad:              Mapped[int]     = mapped_column(Integer, nullable=False)
    precio_unitario_venta: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    precio_total_unidad:   Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)

    venta    = relationship("Venta", backref="detalles_venta")
    producto = relationship("Producto", backref="detalles_venta")