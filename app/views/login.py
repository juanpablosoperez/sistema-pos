import flet as ft
import flet_easy as fs
from app.components.login import LoginForm


@fs.page(route="/auth/login", title="Login")
def login_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        col={
                            "xs": 10,
                            "sm": 5,
                            "md": 5,
                            "lg": 3,
                            "xl": 3,
                        },
                        controls=[
                            LoginForm(data, "/app/dashboard"),
                        ],
                    ),
                ],
                vertical_alignment="center",
                alignment="center",
            )
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
