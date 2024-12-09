import flet as ft

from .theme_config import DarkTheme
from .theme_config import LightTheme


def change_icon(event: ft.ControlEvent):
    icon: ft.IconButton = event.control
    icon.icon = ft.icons.DARK_MODE if icon.icon == ft.icons.LIGHT_MODE else ft.icons.LIGHT_MODE
    icon.update()


def change_theme(event: ft.ControlEvent):
    change_icon(event=event)
    page: ft.Page = event.page

    is_dark = page.theme_mode == ft.ThemeMode.LIGHT
    page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
    page.theme = DarkTheme if is_dark else LightTheme
    page.update()
