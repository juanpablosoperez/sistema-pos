# components/app_bar.py
import flet as ft
import flet_easy as fs


class AppBar:
    def __init__(self, data: fs.Datasy):
        self.data = data
        self.page = data.page

    def build(self):
        return ft.AppBar(
            leading=ft.Icon(ft.icons.MENU),
            leading_width=40,
            title=ft.Text("Home"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[self._build_menu()],
        )

    def _build_menu(self):
        return ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Perfil de usuario", icon=ft.icons.PERSON, on_click=self._handle_profile),
                ft.PopupMenuItem(text="Cambiar tema", icon=ft.icons.DARK_MODE, on_click=self._handle_theme),
                ft.PopupMenuItem(text="Configuración", icon=ft.icons.SETTINGS, on_click=self._handle_settings),
                ft.PopupMenuItem(text="Cerrar sesión", icon=ft.icons.LOGOUT, on_click=self._handle_logout),
            ]
        )

    def _handle_profile(self, e):
        self.data.go("/profile")

    def _handle_theme(self, e):
        self.page.theme_mode = ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.page.update()

    def _handle_settings(self, e):
        self.data.go("/settings")

    def _handle_logout(self, e):
        self.data.logout("login")
        self.data.go("/auth/login")
