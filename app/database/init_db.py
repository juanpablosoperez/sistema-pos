from datetime import datetime
from datetime import timezone

from app.database.connection import get_db
from app.models.modulos import Modulo
from app.models.usuarios import Role
from app.models.usuarios import Usuario


def create_default_roles():
    with get_db() as db:
        # Verificar si ya existen roles
        if db.query(Role).count() == 0:
            # Crear roles básicos
            roles = [
                Role(id_rol=1, nombre="admin", descripcion="Administrador del sistema"),
                Role(id_rol=2, nombre="user", descripcion="Usuario regular"),
            ]
            db.add_all(roles)
            db.commit()
            print("Roles creados exitosamente")


def create_default_admin():
    with get_db() as db:
        # Verifica si ya existe un admin
        admin = db.query(Usuario).filter(Usuario.username == "admin").first()
        if not admin:
            # Primero verificamos que exista el rol de admin
            admin_role = db.query(Role).filter(Role.id_rol == 1).first()
            if not admin_role:
                print("Error: El rol de administrador no existe")
                return

            # Crear usuario admin
            admin = Usuario(
                username="admin",
                nombre="Administrador",
                email="admin@example.com",
                id_rol=1,  # Role admin
                activo=True,
                created_at=datetime.now(timezone.utc),
            )
            admin.password = "admin123"  # Esto usará el setter para hashear la contraseña

            # Obtener o crear módulos de admin
            admin_modules = [
                {"nombre": "dashboard", "descripcion": "Panel principal", "icono": "HOME_OUTLINED", "ruta": "/app/dashboard"},
                {"nombre": "usuarios", "descripcion": "Gestión de usuarios", "icono": "PEOPLE_OUTLINED", "ruta": "/app/users"},
                {"nombre": "configuracion", "descripcion": "Configuración", "icono": "SETTINGS_OUTLINED", "ruta": "/app/settings"},
                {"nombre": "ventas", "descripcion": "Módulo para gestionar las ventas realizadas.", "icono": "SHOPPING_CART", "ruta": "/gestion_ventas"},
                {"nombre": "gastos", "descripcion": "Módulo para gestionar y registrar los gastos.", "icono": "MONEY_OFF", "ruta": "/gestion_gastos"},
                {"nombre": "stock", "descripcion": "Módulo para el control y administración del stock de productos.", "icono": "INVENTORY", "ruta": "/gestion_stock"},
                {"nombre": "precios", "descripcion": "Módulo para configurar y gestionar los precios de los productos.", "icono": "PRICE_CHECK", "ruta": "/gestion_precios"},
                {"nombre": "caja diaria", "descripcion": "Módulo para realizar el cierre diario de caja y registrar movimientos.", "icono": "POINT_OF_SALE", "ruta": "/cierre_caja"},
                {"nombre": "clientes crédito", "descripcion": "Módulo para administrar los clientes con compras a crédito.", "icono": "ACCOUNT_BALANCE", "ruta": "/clientes_credito"},
                {"nombre": "backup", "descripcion": "Módulo para realizar respaldos manuales del sistema.", "icono": "BACKUP", "ruta": "/backup_manual"},
            ]


            for module_data in admin_modules:
                module = db.query(Modulo).filter_by(nombre=module_data["nombre"]).first()
                if not module:
                    module = Modulo(**module_data)
                    db.add(module)
                admin.modulos.append(module)

            db.add(admin)
            db.commit()
            print("Administrador creado exitosamente")


def init_db():
    """Inicializa la base de datos con datos por defecto"""
    print("Iniciando configuración de la base de datos...")
    create_default_roles()
    create_default_admin()
    print("Configuración completada")


if __name__ == "__main__":
    init_db()
