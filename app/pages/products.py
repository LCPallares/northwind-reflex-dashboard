import reflex as rx

#from app.components.main_content import main_layout


def products_page() -> rx.Component:
    """The UI for the products page."""
    return rx.el.div(
        rx.vstack(
            rx.heading("Products", size="5"),
        )
    )