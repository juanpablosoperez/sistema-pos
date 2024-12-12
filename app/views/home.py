import flet as ft
import flet_easy as fs

dashboard = fs.AddPagesy(
    route_prefix="/app",
)

# Función para generar tarjetas de estadísticas
def create_stat_cards():
    stats = [
        {
            "title": "Ventas Totales",
            "value": "$25,000",
            "description": "↑ 15% respecto al mes anterior",
            "value_color": "#4CAF50",  # Verde
            "icon": ft.icons.ATTACH_MONEY,
        },
        {
            "title": "Gastos Totales",
            "value": "$12,000",
            "description": "↓ 8% respecto al mes anterior",
            "value_color": "#FF5252",  # Rojo
            "icon": ft.icons.MONEY_OFF,
        },
        {
            "title": "Productos Vendidos",
            "value": "3,450",
            "description": "↑ 5% respecto al mes anterior",
            "value_color": "#4CAF50",  # Verde
            "icon": ft.icons.STORE,
        },
        {
            "title": "Clientes Activos",
            "value": "145",
            "description": "6 clientes nuevos esta semana",
            "value_color": "#FFA726",  # Naranja
            "icon": ft.icons.PEOPLE,
        },
    ]

    cards = []
    for stat in stats:
        cards.append(
            ft.Container(
                width=300,
                height=150,
                bgcolor="#1E1E2D",  # Fondo gris oscuro
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(name=stat["icon"], color="#50BFE6", size=40),  # Ícono azul claro
                                ft.Text(stat["title"], size=18, weight="bold", color="#FFFFFF"),  # Blanco
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(
                            stat["value"],
                            size=28,
                            weight="bold",
                            color=stat["value_color"],  # Color dinámico para el valor
                        ),
                        ft.Text(
                            stat["description"],
                            size=12,
                            color="#B0B0B0",  # Gris claro para texto secundario
                        ),
                    ],
                    spacing=10,
                ),
                margin=ft.margin.all(10),  # Espaciado entre tarjetas
            )
        )
    return cards

# Función para generar el drawer (barra lateral) con scroll
def create_drawer(modulos):
    drawer_items = []
    for modulo in modulos:
        drawer_items.append(
            ft.ListTile(
                leading=ft.Icon(name=getattr(ft.icons, modulo["icono"]), color="#50BFE6"),  # Azul claro
                title=ft.Text(modulo["nombre"], color="#FFFFFF", size=16),
                subtitle=ft.Text(modulo["descripcion"], color="#B0B0B0", size=12),
                on_click=lambda e, ruta=modulo["ruta"]: print(f"Navegar a: {ruta}"),
            )
        )
    return ft.Container(
        width=250,  # Ancho de la barra lateral
        bgcolor="#252631",  # Fondo gris oscuro
        padding=ft.padding.all(15),
        content=ft.ListView(  # Contenedor con scroll vertical
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.MENU, color="#FFFFFF", size=30),
                        ft.Text("Menú", size=20, color="#FFFFFF", weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(color="#3A3B47"),  # Gris medio
                *drawer_items,
            ],
            spacing=15,
        ),
    )

# Página principal del dashboard
@fs.page(route="/app/dashboard", title="Dashboard", protected_route=True)
async def dashboard_page(data: fs.Datasy):
    try:
        # Decodificar datos de la sesión
        session_data = await fs.decode_async(key_login="login", data=data)

        if not session_data:
            print("No se encontraron datos de sesión")
            return ft.View(controls=[ft.Text("No hay datos de sesión disponibles")])

        # Generar el dashboard con un drawer y tarjetas
        return ft.View(
            controls=[
                ft.Row(
                    controls=[
                        # Drawer (barra lateral) con scroll
                        create_drawer(session_data["modulos"]),
                        # Contenido principal
                        ft.Container(
                            expand=True,
                            bgcolor="#181922",  # Fondo gris oscuro del contenido principal
                            content=ft.Column(
                                controls=[
                                    # Título y Bienvenida
                                    ft.Text(
                                        f"Bienvenido, {session_data['username']}",
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF",
                                    ),
                                    ft.Text(f"Rol: {session_data['role']}", size=20, color="#B0B0B0"),  # Gris claro
                                    ft.Divider(color="#3A3B47"),  # Gris medio
                                    # Tarjetas de estadísticas
                                    ft.Row(
                                        controls=create_stat_cards(),
                                        wrap=True,  # Ajuste automático de tarjetas
                                        spacing=20,
                                        run_spacing=20,
                                    ),
                                ],
                                spacing=20,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            ),
                            padding=ft.padding.all(20),  # Espaciado interno del contenido principal
                        ),
                    ],
                    expand=True,
                )
            ],
            vertical_alignment="start",
            horizontal_alignment="start",
            appbar=ft.AppBar(title=ft.Text("Dashboard", color="#FFFFFF"), center_title=True, bgcolor="#181922"),
        )

    except Exception as e:
        print(f"Error al procesar datos de sesión: {str(e)}")
        return ft.View(controls=[ft.Text("Error al cargar los datos de la sesión")])



