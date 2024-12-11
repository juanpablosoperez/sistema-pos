import flet as ft
import flet_easy as fs

dashboard = fs.AddPagesy(
    route_prefix="/app",
)


# We add a second page
@fs.page(route="/app/dashboard", title="Dashboard", protected_route=True)
async def dashboard_page(data: fs.Datasy):
    try:
        session_data = await fs.decode_async(key_login="login", data=data)

        if not session_data:
            print("No se encontraron datos de sesión")
            return ft.View(controls=[ft.Text("No hay datos de sesión disponibles")])

        return ft.View(
            controls=[
                ft.Column(
                    [
                        ft.Text(f"Bienvenido, {session_data['username']}", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Rol: {session_data['role']}", size=20),
                        # Separador
                        ft.Divider(),
                        # Módulos del usuario
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(
                                        name=getattr(ft.icons, modulo["icono"]),
                                        color=ft.colors.BLUE_400,
                                    ),
                                    title=ft.Text(modulo["nombre"]),
                                    subtitle=ft.Text(modulo["descripcion"]),
                                    on_click=lambda e, ruta=modulo["ruta"]: data.go(ruta),
                                )
                                for modulo in session_data["modulos"]
                            ]
                        ),
                        # Botón de logout
                        ft.ElevatedButton("Cerrar Sesión", icon=ft.icons.LOGOUT, on_click=lambda e: data.logout("login")),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
            # Si tienes un AppBar configurado
            appbar=ft.AppBar(title=ft.Text("Dashboard"), center_title=True, bgcolor=ft.colors.SURFACE_VARIANT),
        )
    except Exception as e:
        print(f"Error al procesar datos de sesión: {str(e)}")
        return ft.View(controls=[ft.Text("Error al cargar los datos de la sesión")])
