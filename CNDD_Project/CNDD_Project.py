"""CNDD Project - Aplicacion de Sistema de gestion en S3 """

import reflex as rx
from .pages.login import login_page

class State(rx.State):
    """Estado  Global de la Aplicacion"""
    pass

def index() -> rx.Component:
    """Pagina Principal - Refirige al Login"""
    return rx.center(
        rx.vstack(
            rx.heading("CNDD Project", size="9"),
            rx.text("Redirigiendo al Login ...", size="4", color="gray"),
            rx.spinner(size="3", margin_top="2rem"),
            spacing="4",
            align="center",
            min_height="100vh",
        ),
        on_mount=rx.redirect('/login'),
    )

# Crear la Aplicacion

app = rx.App()

#Agregar paginas
app.add_page(index, route='/')
app.add_page(login_page, route='/login')
