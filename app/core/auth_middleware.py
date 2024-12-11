# core/middleware/auth_middleware.py
import flet_easy as fs


async def auth_middleware(data: fs.Datasy):
    print("entre")
    public_routes = [
        "/auth/login",
        "/auth/register",
    ]

    # Si la ruta actual está en las rutas públicas, permitir acceso
    if data.route in public_routes:
        return

    try:
        # Verificar si existe sesión
        session = await data.page.client_storage.get_async("login")

        if not session:
            print("No hay sesión activa, redirigiendo a login")
            return data.redirect("/auth/login")

        print("Sesión verificada:", session)

    except Exception as e:
        print(f"Error en middleware de autenticación: {str(e)}")
        return data.redirect("/auth/login")
