# app/views/register_view.py
import flet as ft
import flet_easy as fs
from controllers.auth_controller import AuthController

auth = fs.AddPagesy(route_prefix="/auth")


@auth.page("/register", title="Registro")
class RegisterView(ft.UserControl):
    def __init__(self, data: fs.Datasy):
        super().__init__()
        self.data = data
        self.controller = AuthController(data)

    def build(self):
        # Crear los campos del formulario con estilos consistentes
        self.username = ft.TextField(
            label="Usuario",
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_ACCENT,
            width=300,
            text_size=14,
            autofocus=True,
            prefix_icon=ft.icons.PERSON,
        )

        self.password = ft.TextField(
            label="Contraseña",
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_ACCENT,
            width=300,
            text_size=14,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK,
        )

        self.nombre = ft.TextField(
            label="Nombre Completo",
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_ACCENT,
            width=300,
            text_size=14,
            prefix_icon=ft.icons.BADGE,
        )

        self.email = ft.TextField(
            label="Email",
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_ACCENT,
            width=300,
            text_size=14,
            prefix_icon=ft.icons.EMAIL,
        )

        self.telefono = ft.TextField(
            label="Teléfono (opcional)",
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_ACCENT,
            width=300,
            text_size=14,
            prefix_icon=ft.icons.PHONE,
        )

        self.direccion = ft.TextField(
            label="Dirección (opcional)",
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_ACCENT,
            width=300,
            text_size=14,
            prefix_icon=ft.icons.HOME,
        )

        return ft.View(
            controls=[
                ft.Container(
                    content=ft.Card(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Registro de Usuario",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Divider(height=2, color=ft.colors.BLUE_100),
                                self.username,
                                self.password,
                                self.nombre,
                                self.email,
                                self.telefono,
                                self.direccion,
                                ft.ElevatedButton(
                                    text="Registrar",
                                    on_click=self.handle_submit,
                                    style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor={"": ft.colors.BLUE_400}),
                                    width=300,
                                ),
                                ft.TextButton(
                                    text="¿Ya tienes cuenta? Inicia sesión",
                                    on_click=lambda _: self.data.go("/auth/login"),
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.MaterialState.DEFAULT: ft.colors.BLUE_400,
                                            ft.MaterialState.HOVERED: ft.colors.BLUE_ACCENT,
                                        },
                                    ),
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        elevation=5,
                    ),
                    width=500,
                    height=720,  # Aumentado para acomodar todos los campos
                    padding=40,
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.TRANSPARENT,
        )

    async def handle_submit(self, e):
        user_data = {
            "username": self.username.value,
            "password": self.password.value,
            "nombre": self.nombre.value,
            "email": self.email.value,
            "telefono": self.telefono.value,
            "direccion": self.direccion.value,
        }

        success, message = await self.controller.register_user(user_data)
        if success:
            # Redirect the user to the login page
            self.data.page.go("/auth/login")
        else:
            # Handle registration failure
            self._show_error(message)

    def _show_error(self, message: str):
        self.data.page.snack_bar = ft.SnackBar(
            content=ft.Container(content=ft.Text(message, color=ft.colors.ERROR, weight=ft.FontWeight.W_500), padding=10),
            bgcolor=ft.colors.ERROR_CONTAINER,
            action="Entendido",
            action_color=ft.colors.ERROR,
            open=True,
        )
        self.data.page.update()
