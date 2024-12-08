# app/views/auth.py
import flet as ft
import flet_easy as fs

from app.controllers.auth_controller import AuthController

auth = fs.AddPagesy(route_prefix="/auth")


@auth.page("/login", title="Login")  # Esto creará la ruta /auth/login
class LoginView:
    def __init__(self, data: fs.Datasy):
        self.data = data
        self.page = data.page
        self.controller = AuthController(data)
        self.init_components()

    def init_components(self):
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
            password=True,
            can_reveal_password=True,
            text_size=14,
            prefix_icon=ft.icons.LOCK,
        )

    def build(self):
        return ft.View(
            controls=[
                ft.Container(
                    content=ft.Card(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Iniciar Sesión",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Divider(height=2, color=ft.colors.BLUE_100),
                                self.username,
                                self.password,
                                ft.ElevatedButton(
                                    text="Iniciar Sesión",
                                    on_click=self.handle_submit,
                                    style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor={"": ft.colors.BLUE_400}),
                                    width=300,
                                    height=50,
                                ),
                                ft.TextButton(text="¿No tienes cuenta? Registrate", on_click=lambda _: self.data.page.go("/auth/register")),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        elevation=5,
                    ),
                    height=700,  # Reducido para mejor apariencia
                    padding=0,
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.TRANSPARENT,
        )

    async def handle_submit(self, e):
        if await self.controller.authenticate(self.username.value, self.password.value):
            # La redirección la maneja el controlador
            pass
