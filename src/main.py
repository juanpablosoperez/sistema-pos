# sistema_pos/main.py
import os
from pathlib import Path

import flet as ft
from dotenv import load_dotenv


def load_environment():
    """Load environment configuration silently"""
    env_name = os.getenv("ENV_NAME", "development")
    root_dir = Path(__file__).parent.parent

    load_dotenv(root_dir / ".env")
    load_dotenv(root_dir / f".env.{env_name}", override=True)


def main(page: ft.Page):
    page.window.width = 800
    page.window.height = 600
    page.window.center()
    page.theme_mode = ft.ThemeMode.LIGHT

    welcome_message = ft.Text(
        value=f"Hola mundo desde {os.getenv('ENV_NAME', 'development')}",
        size=32,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )

    page.add(welcome_message)


if __name__ == "__main__":
    load_environment()
    ft.app(target=main)
