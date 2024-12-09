import re
from datetime import datetime
from datetime import timezone
from typing import List
from typing import Optional
from typing import Tuple

import flet as ft
import flet_easy as fs
from models.modulos import Modulo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.database.connection import get_db  # Asegúrate de que esta ruta sea correcta
from app.models.usuarios import Usuario


class AuthController:
    def __init__(self, data: fs.Datasy):
        self.data = data
        self.page = data.page

    async def register_user(self, user_data: dict) -> Tuple[bool, str]:
        try:
            # Validate data
            if not self._validate_registration_data(user_data):
                return False, "Datos incompletos o inválidos"

            # Check if user already exists
            if await self._username_exists(user_data["username"]):
                return False, "El nombre de usuario ya está en uso"

            if await self._email_exists(user_data["email"]):
                return False, "El correo electrónico ya está registrado"

            # Forzar rol de usuario regular para nuevos registros
            user_data["id_rol"] = 2  # Siempre asignar rol de usuario

            # Create new user with modules
            with get_db() as db:
                try:
                    # Create user
                    user = Usuario.from_dict(user_data)
                    user.password = user_data["password"]

                    # Get or create default modules based on role
                    default_modules = await self._get_role_modules(db, user_data["id_rol"])
                    user.modulos.extend(default_modules)

                    db.add(user)
                    db.commit()
                    db.refresh(user)

                    return True, "Usuario registrado exitosamente"
                except SQLAlchemyError as e:
                    db.rollback()
                    raise e

        except SQLAlchemyError as e:
            print(f"Database error in registration: {str(e)}")
            return False, "Error en la base de datos"
        except Exception as e:
            print(f"Unexpected error in registration: {str(e)}")
            return False, "Error inesperado"

    async def _get_role_modules(self, db, role_id: int) -> List[Modulo]:
        """
        Gets or creates default modules for a role.

        Args:
            db: Database session
            role_id: Role ID to get modules for

        Returns:
            List[Modulo]: List of modules assigned to the role
        """
        # Define default modules based on role
        default_modules = {
            1: [  # Admin role
                {"nombre": "dashboard", "descripcion": "Panel principal", "icono": "HOME_OUTLINED", "ruta": "/app/dashboard"},
                {"nombre": "usuarios", "descripcion": "Gestión de usuarios", "icono": "PEOPLE_OUTLINED", "ruta": "/app/users"},
                {"nombre": "configuracion", "descripcion": "Configuración", "icono": "SETTINGS_OUTLINED", "ruta": "/app/settings"},
            ],
            2: [  # Regular user role
                {"nombre": "dashboard", "descripcion": "Panel principal", "icono": "HOME_OUTLINED", "ruta": "/app/dashboard"},
                {"nombre": "perfil", "descripcion": "Perfil de usuario", "icono": "PERSON_OUTLINED", "ruta": "/app/profile"},
            ],
        }

        role_modules = default_modules.get(role_id, default_modules[2])  # Default to regular user modules
        modules = []

        for module_data in role_modules:
            # Get existing module or create new one
            module = db.query(Modulo).filter_by(nombre=module_data["nombre"]).first()
            if not module:
                module = Modulo(**module_data)
                db.add(module)
            modules.append(module)

        return modules

    async def authenticate(self, username: str, password: str) -> bool:
        print("Entra a authenticate")

        if not self._validate_credentials(username, password):
            print("Entra a validate credentials")
            return False

        try:
            print("Entra a get user")
            user = self._get_user(username)
            print("Usuario encontrado:", user)

            if not user or not user.check_password(password):
                self._show_error("Usuario o contraseña incorrectos")
                return False

            print("Validación de contraseña exitosa")

            try:
                await self._create_session(user)  # Asegúrate de que _create_session sea síncrono
                return True
            except Exception as e:
                print(f"Error en la creación de sesión: {str(e)}")
                self._show_error("Error al crear la sesión")
                return False

        except Exception as e:
            self._show_error("Error inesperado")
            print(f"Unexpected error: {str(e)}")
            return False

    async def logout(self) -> None:
        """Logs out the user."""
        await self.data.logout("login")

    def _get_user(self, username: str) -> Optional[Usuario]:
        """Retrieves the user from the database."""
        with get_db() as db:
            print(f"Buscando usuario con username: {username}")
            user = db.query(Usuario).filter(
                Usuario.username == username,
                Usuario.activo.is_(True)
            ).first()
            print(f"Resultado de la consulta: {user}")
            return user

    async def _update_last_access(self, user: Usuario) -> None:
        """Updates the user's last access date."""
        with get_db() as db:
            user.ultimo_acceso = datetime.now(timezone.utc)
            db.commit()

    async def _create_session(self, user: Usuario) -> None:
        try:
            with get_db() as db:
                user = (
                    db.query(Usuario)
                    .options(joinedload(Usuario.rol), joinedload(Usuario.modulos))
                    .filter(Usuario.id_usuario == user.id_usuario)
                    .first()
                )

                session_data = {
                    "id_usuario": user.id_usuario,
                    "username": user.username,
                    "role": user.rol.nombre if user.rol else "user",
                    "nombre": user.nombre,
                    "email": user.email,
                    "modulos": [modulo.to_dict() for modulo in user.modulos],
                }

                print("Session data:", session_data)
                print("Creando sesión...")

                # Cambiar a self.data.page.client_storage directamente
                await self.data.page.client_storage.set_async("login", session_data)
                # Hacer la redirección directamente aquí
                self.data.go("/app/dashboard")

                print("Sesión creada y redirección iniciada")

        except Exception as e:
            print(f"Error en _create_session: {str(e)}")
            raise

    def _validate_credentials(self, username: str, password: str) -> bool:
        """Validates that the credentials have been provided."""
        if not username or not password:
            self._show_error("Ingresa todos los datos")
            return False
        return True

    def _show_error(self, message: str) -> None:
        """
        Displays an error message to the user using SnackBar.

        Args:
            message (str): Message to display
        """
        self.page.snack_bar = ft.SnackBar(
            content=ft.Container(content=ft.Text(message, color=ft.colors.ERROR, weight=ft.FontWeight.W_500), padding=10),
            bgcolor=ft.colors.ERROR_CONTAINER,
            action="Entendido",
            action_color=ft.colors.ERROR,
            open=True,
        )
        self.page.update()

    async def _username_exists(self, username: str) -> bool:
        """Checks if a user with the given username already exists."""
        with get_db() as db:
            return db.query(Usuario).filter(Usuario.username == username).first() is not None

    async def _email_exists(self, email: str) -> bool:
        """Checks if a user with the given email already exists."""
        with get_db() as db:
            return db.query(Usuario).filter(Usuario.email == email).first() is not None

    def _validate_registration_data(self, data: dict) -> bool:
        """Valida los datos de registro."""
        required_fields = ["username", "password", "nombre", "email"]
        email_pattern = r"[^@]+@[^@]+\.[^@]+"

        return (
            all(field in data and data[field] for field in required_fields) and re.match(email_pattern, data["email"]) and len(data["password"]) >= 8
        )
