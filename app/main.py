import os
from pathlib import Path
import flet as ft
import flet_easy as fs
from dotenv import load_dotenv

def load_environment():
    envname = os.getenv("ENVNAME", "development")
    root_dir = Path(__file__).parent.parent
    load_dotenv(root_dir / ".env")
    load_dotenv(root_dir / f".env.{envname}", override=True)

app = fs.FletEasy(route_init="/hello")

@app.page(route="/hello", title="Hello")
def hello_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text(
                f"Hola mundo desde {os.getenv('ENV_NAME', 'development')}",
                size=32,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

if __name__ == "__main__":
    load_environment()
    app.run()
