# views/home/home_controller.py
import flet_easy as fs

from ..views.home import HomeView


@fs.page(route="/home", title="Home", protected_route=True)
def home_page(data: fs.Datasy):
    return HomeView(data).build()
