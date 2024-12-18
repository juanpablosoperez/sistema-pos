# app/components/sidebar.py
from typing import Callable
from typing import List

import flet as ft

from app.models.usuarios import Modulo


class SideNav(ft.NavigationRail):
    def __init__(self, modules: List[Modulo], on_change: Callable, selected_index: int = 0):
        super().__init__()
        self.selected_index = selected_index
        self.on_change = on_change
        self.destinations = [
            ft.NavigationRailDestination(
                icon=module.icono,  # Cambio de icon a icono
                label=module.nombre,  # Cambio de name a nombre
            )
            for module in modules
        ]
        self.group_alignment = -0.9
        self.min_width = 100
        self.min_extended_width = 200
        self.bgcolor = ft.colors.SURFACE_VARIANT
