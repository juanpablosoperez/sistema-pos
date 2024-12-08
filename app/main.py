import os
from pathlib import Path

import flet_easy as fs
from dotenv import load_dotenv

from app.core.config import ConfigApp


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
        app = fs.FletEasy(route_init="/auth/login", route_login="/auth/login", path_views=Path(__file__).parent / "views")

        ConfigApp(app)
        return app

    except Exception as e:
        print(f"Error creando la aplicación: {str(e)}")
        raise


if __name__ == "__main__":
    load_environment()
    app = create_app()
    app.run()
