# controllers/auth_controller.py
from datetime import timedelta

import flet as ft
import flet_easy as fs
from database.connection import get_db
from models.usuarios import Usuario

# controllers/auth_controller.py
from sqlalchemy.orm import joinedload


class AuthController:
    def __init__(self, data: fs.Datasy, redirect: str):
        self.data = data
        self.redirect = redirect
        self.username = fs.Ref[ft.TextField]()
        self.password = fs.Ref[ft.TextField]()

    def _get_user(self, username: str):
        with get_db() as db:
            # Cargamos el rol junto con el usuario usando joinedload
            return (
                db.query(Usuario)
                .options(joinedload(Usuario.rol), joinedload(Usuario.modulos))  # Cargamos los módulos
                .filter(Usuario.username == username)
                .first()
            )

    def check(self, e):
        username = self.username.c.value if self.username.c.value != "" and self.username.c.value else False
        password = self.password.c.value if self.password.c.value != "" and self.password.c.value else False

        if username and password:
            # Obtener usuario con sus relaciones
            with get_db():
                user = self._get_user(username)

                if not user or not user.check_password(password):
                    self.data.page.snack_bar = ft.SnackBar(content=ft.Text("Usuario o contraseña incorrectos"), action="OK", open=True)
                else:
                    # Crear sesión con los datos ya cargados
                    session_data = {
                        "id_usuario": user.id_usuario,
                        "username": user.username,
                        "role": user.rol.nombre if user.rol else "user",
                        "modulos": [modulo.to_dict() for modulo in user.modulos],
                    }

                    self.data.login(key="login", value=session_data, time_expiry=timedelta(seconds=80000), next_route=self.redirect)
        else:
            self.data.page.snack_bar = ft.SnackBar(content=ft.Text("Ingresa todos los datos"), action="OK", open=True)
        self.data.page.update()
