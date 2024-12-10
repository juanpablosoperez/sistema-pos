import os
from pathlib import Path

import flet as ft
import flet_easy as fs
from core.auth_middleware import auth_middleware
from core.config import ConfigApp
from core.sensitive import SECRET_KEY  # Para algoritmo HS256
from dotenv import load_dotenv


def load_environment():
    try:
        env_name = os.getenv("ENV_NAME", "development")
        root_dir = Path(__file__).parent
        load_dotenv(root_dir / ".env")
        load_dotenv(root_dir / f".env.{env_name}", override=True)
        print(f"Ambiente cargado: {env_name}")
    except Exception as e:
        print(f"Error cargando el ambiente: {str(e)}")
        raise


def create_app():
    try:
        app = fs.FletEasy(
            route_init="/app/dashboard",
            route_login="/auth/login",
            auto_logout=True,
            path_views=Path(__file__).parent / "views",
            secret_key=fs.SecretKey(algorithm=fs.Algorithm.HS256, secret=SECRET_KEY),  # Usa una clave segura
        )
        app.add_middleware([auth_middleware])
        ConfigApp(app)
        return app

    except Exception as e:
        print(f"Error creando la aplicación: {str(e)}")
        raise


if __name__ == "__main__":
    load_environment()
    app = create_app()
    app.run(view=ft.AppView.WEB_BROWSER)
