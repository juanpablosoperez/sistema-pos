# app/core/config.py
import flet as ft
import flet_easy as fs

from .theme_config import LightTheme


class ConfigApp:
    def __init__(self, app: fs.FletEasy):
        self.app = app
        self.start()

    def start(self):
        self._setup_auth()
        self._setup_view()
        self._setup_theme()
        self._setup_events()
        self._setup_fullscreen()

    def _setup_fullscreen(self):
        @self.app.config
        def page_config(page: ft.Page):
            page.window_fullscreen = True
            page.window_maximized = True
            page.window_frameless = False
            page.window_resizable = True
            page.adaptive = True
            page.window.movable = True

    def _setup_theme(self):
        @self.app.config
        def page_config(page: ft.Page):
            # Configuración del tema
            page.theme = LightTheme
            page.theme_mode = ft.ThemeMode.LIGHT

            # Configuración de fuentes
            page.fonts = {"Roboto": "fonts/Roboto-Regular.ttf", "Lato": "fonts/Lato-Regular.ttf"}

    def _setup_view(self):
        @self.app.view
        async def view_config(data: fs.Datasy):
            return fs.Viewsy(
                vertical_alignment=ft.MainAxisAlignment.CENTER,  # Center content vertically
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center content horizontally
                padding=0,  # Optional: set padding to 0 for cleaner alignment
            )

    def _setup_auth(self):
        @self.app.login
        async def login_required(data: fs.Datasy):
            try:
                return await fs.decode_async(key_login="login", data=data)
            except Exception as e:
                print(f"Authentication error: {str(e)}")
                return False

    def _setup_events(self):
        @self.app.config_event_handler
        async def event_handler(data: fs.Datasy):
            page = data.page

            async def on_disconnect(e):
                print("Disconnect test application")

            page.on_disconnect = on_disconnect
