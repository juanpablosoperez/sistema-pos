import flet as ft
import flet_easy as fs


@fs.page(route="/app/dashboard", title="Home")
def home_page(data: fs.Datasy):
    return ft.View(
        controls=[ft.Text("Home Page", size=30), ft.FilledButton("Go to About", on_click=data.go("/about"))],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
