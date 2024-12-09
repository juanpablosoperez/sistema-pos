from typing import Any
from typing import Dict

import flet as ft
import flet_easy as fs

home = fs.AddPagesy(route_prefix="/app")  # Similar a tu auth = fs.AddPagesy(route_prefix="/auth")


@home.page("/dashboard", title="Dashboard", protected_route=True)
class HomeView:
    def __init__(self, data: fs.Datasy, user: Dict[str, Any]):
        self.data = data
        self.page = data.page
        self.user = user
        self.current_module = None

        # Configure window
        self.page.window_maximized = True
        self.page.padding = 0
        self.init_components()

    def init_components(self):
        self.app_bar = self._create_app_bar()
        self.navigation_rail = self._create_navigation_rail()
        self.content_area = self._create_content_area()

    def _create_navigation_rail(self):
        # Create navigation destinations from user modules
        destinations = []
        for module in self.user.get("modulos", []):
            icon_name = module.get("icono", "CIRCLE_OUTLINED")
            selected_icon_name = icon_name.replace("_OUTLINED", "")

            destinations.append(
                ft.NavigationRailDestination(
                    icon=getattr(ft.icons, icon_name),
                    selected_icon=getattr(ft.icons, selected_icon_name),
                    label=module.get("nombre", "").title(),
                )
            )

        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=destinations,
            on_change=self.handle_navigation_change,
        )

    def handle_navigation_change(self, e):
        index = e.control.selected_index
        modules = self.user.get("modulos", [])

        if 0 <= index < len(modules):
            module = modules[index]
            self.current_module = module

            # Update app bar title
            self.app_bar.title = ft.Text(module.get("nombre", "").title())

            # Update content area
            self.content_area.content = ft.Column(
                [
                    ft.Text(module.get("descripcion", "")),
                    # Add more module-specific content here
                ]
            )

            self.content_area.update()
            self.app_bar.update()

    def handle_logout(self, e):
        self.data.logout("login")  # Use the same key as in authentication
        self.data.go("/auth/login")

    def _create_content_area(self):
        return ft.Container(
            content=ft.Text(f"Bienvenido, {self.user.get('nombre', 'Usuario')}!"),
            expand=True,
            margin=10,
        )

    def build(self):
        return ft.View(
            appbar=self.app_bar,
            controls=[
                ft.Row(
                    [
                        self.navigation_rail,
                        ft.VerticalDivider(width=1),
                        self.content_area,
                    ],
                    expand=True,
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
