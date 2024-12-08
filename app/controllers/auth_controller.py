import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional
from typing import Tuple

import flet as ft
import flet_easy as fs
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import get_db  # Asegúrate de que esta ruta sea correcta
from app.models.usuarios import Usuario


class AuthController:
    def __init__(self, data: fs.Datasy):
        self.data = data
        self.page = data.page

    async def register_user(self, user_data: dict) -> Tuple[bool, str]:
        """
        Registers a new user.

        Args:
            user_data (dict): User data to register
                {
                    "username": str,
                    "password": str,
                    "nombre": str,
                    "email": str,
                    "telefono": str,
                    "direccion": str,
                    "fecha_nacimiento": datetime,
                    "id_rol": int
                }

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Validate data
            if not self._validate_registration_data(user_data):
                return False, "Datos incompletos o inválidos"

            # Check if user already exists
            if await self._username_exists(user_data["username"]):
                return False, "El nombre de usuario ya está en uso"

            if await self._email_exists(user_data["email"]):
                return False, "El correo electrónico ya está registrado"

            # Create new user
            with get_db() as db:
                user = Usuario.from_dict(user_data)
                user.password = user_data["password"]  # Use the setter to hash the password

                db.add(user)
                db.commit()
                db.refresh(user)

                return True, "Usuario registrado exitosamente"

        except SQLAlchemyError as e:
            print(f"Database error in registration: {str(e)}")
            return False, "Error en la base de datos"
        except Exception as e:
            print(f"Unexpected error in registration: {str(e)}")
            return False, "Error inesperado"

    async def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticates the user and creates a session if successful.

        Args:
            username (str): Username
            password (str): User password

        Returns:
            bool: True if authentication was successful, False otherwise
        """
        if not self._validate_credentials(username, password):
            return False

        try:
            user = await self._get_user(username)
            if not user or not user.check_password(password):
                self._show_error("Usuario o contraseña incorrectos")
                return False

            # Update last access
            await self._update_last_access(user)

            # Create JWT session
            await self._create_session(user)
            return True

        except SQLAlchemyError as e:
            self._show_error("Error de base de datos")
            print(f"Database error: {str(e)}")
            return False
        except Exception as e:
            self._show_error("Error inesperado")
            print(f"Unexpected error: {str(e)}")
            return False

    async def logout(self) -> None:
        """Logs out the user."""
        await self.data.logout("login")

    async def _get_user(self, username: str) -> Optional[Usuario]:
        """Retrieves the user from the database."""
        with get_db() as db:
            return db.query(Usuario).filter(Usuario.username == username, Usuario.activo is True).first()

    async def _update_last_access(self, user: Usuario) -> None:
        """Updates the user's last access date."""
        with get_db() as db:
            user.ultimo_acceso = datetime.now(timezone.utc)
            db.commit()

    async def _create_session(self, user: Usuario) -> None:
        """Creates the JWT session for the user."""
        session_data = {"id_usuario": user.id_usuario, "username": user.username, "role": user.id_rol, "nombre": user.nombre, "email": user.email}

        await self.data.login(
            key="login",
            value=session_data,
            time_expiry=timedelta(hours=24),
        )

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
            content=ft.Container(content=ft.Text(message, color=ft.colors.ERROR, weight=ft.FontWeight.W500), padding=10),
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
