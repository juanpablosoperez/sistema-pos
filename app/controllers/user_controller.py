# app/controllers/auth_controller.py
from typing import Optional
from typing import Tuple

import flet_easy as fs
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import get_db
from app.models.usuarios import Usuario


class UserController:
    def __init__(self, data: fs.Datasy):
        self.data = data
        self.page = data.page

    async def get_user(self, user_id: int) -> Optional[Usuario]:
        """Retrieves a user by ID"""
        with get_db() as db:
            return db.query(Usuario).get(user_id)

    async def update_user(self, user_id: int, update_data: dict) -> Tuple[bool, str]:
        """Updates user profile information"""
        try:
            with get_db() as db:
                user = db.query(Usuario).get(user_id)
                if not user:
                    return False, "Usuario no encontrado"

                # Validar email y actualizar campos
                if "email" in update_data and update_data["email"] != user.email and await self._email_exists(update_data["email"]):
                    return False, "El correo electrónico ya está en uso"

                # Actualizar campos permitidos
                allowed_fields = ["nombre", "email", "telefono", "direccion", "fecha_nacimiento"]
                for field in allowed_fields:
                    if field in update_data:
                        setattr(user, field, update_data[field])

                db.commit()
                return True, "Datos actualizados correctamente"

        except SQLAlchemyError as e:
            print(f"Database error in update: {str(e)}")
            return False, "Error en la base de datos"
        except Exception as e:
            print(f"Unexpected error in update: {str(e)}")
            return False, "Error inesperado"

    async def change_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Changes a user's password"""
        try:
            with get_db() as db:
                user = db.query(Usuario).get(user_id)
                if not user:
                    return False, "Usuario no encontrado"

                if not user.check_password(old_password):
                    return False, "Contraseña actual incorrecta"

                user.password = new_password
                db.commit()
                return True, "Contraseña actualizada correctamente"

        except Exception as e:
            print(f"Error changing password: {str(e)}")
            return False, "Error cambiando la contraseña"
