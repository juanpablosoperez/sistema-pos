import flet as ft
import flet_easy as fs

from app.components.appbar import AppBar
from app.components.sidebar import SideNav
from app.database.connection import get_db
from app.models.modulos import Modulo
from app.models.usuarios import Usuario

dashboard = fs.AddPagesy(
    route_prefix="/app",
)


async def load_user_modules(data: fs.Datasy):
    try:
        user_data = await fs.decode_async(key_login="login", data=data)
        if not user_data:
            print("No se encontraron datos del usuario en el JWT")
            return []

        user_id = user_data.get("id_usuario")
        with get_db() as db:
            modules = db.query(Modulo).join(Modulo.usuarios).filter(Usuario.id_usuario == user_id).order_by(Modulo.id_modulo).all()
            return modules

    except Exception as e:
        print(f"Error loading modules: {e}")
        return []


def build_info_card(title: str, description: str, color: str, col: int):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(description),
            ],
            spacing=10,
        ),
        padding=20,
        bgcolor=color,
        border_radius=10,
        col=col,
    )


async def build_home_content(data: fs.Datasy):
    user_data = await fs.decode_async(key_login="login", data=data)
    username = user_data.get("username", "Usuario") if user_data else "Usuario"

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(f"Bienvenido, {username}", size=30, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    controls=[
                        build_info_card(
                            "Acciones Rápidas",
                            "Accede a tus herramientas más utilizadas",
                            ft.colors.BLUE_50,
                            col=4,
                        ),
                        build_info_card(
                            "Actividad Reciente",
                            "Visualiza tus actividades y actualizaciones recientes",
                            ft.colors.GREEN_50,
                            col=4,
                        ),
                        build_info_card(
                            "Notificaciones",
                            "Revisa tus últimas notificaciones y alertas",
                            ft.colors.ORANGE_50,
                            col=4,
                        ),
                    ],
                ),
            ],
            spacing=20,
        ),
        padding=30,
        expand=True,
    )


@dashboard.page("/dashboard", title="Dashboard", protected_route=True)
async def dashboard_page(data: fs.Datasy):
    # Configuración inicial de la página
    page = data.page
    page.title = "Dashboard"
    page.window.maximized = True
    page.window.frameless = True
    page.padding = 0

    # Cargar módulos del usuario
    user_modules = await load_user_modules(data)

    # Estado para el título actual del módulo
    current_module = "Dashboard"

    # Crear instancia del AppBar
    appbar_instance = AppBar(data=data)
    app_bar = appbar_instance.build()
    app_bar.title = ft.Text(current_module)  # Establecer título directamente

    async def handle_module_change(e):
        nonlocal current_module
        selected_index = e.control.selected_index
        selected_module = user_modules[selected_index]
        current_module = selected_module.nombre

        # Actualizar el título del AppBar
        app_bar.title = ft.Text(current_module)
        page.update()

    # Construir la vista principal
    view = ft.View(
        controls=[
            ft.Row(
                controls=[
                    SideNav(
                        modules=user_modules,
                        on_change=handle_module_change,
                        selected_index=0,
                    ),
                    await build_home_content(data),
                ],
                expand=True,
                spacing=0,
            )
        ],
        appbar=app_bar,  # Usar la instancia de AppBar ya configurada
        bgcolor=ft.colors.BACKGROUND,
    )

    return view
