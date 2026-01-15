import reflex as rx

#from app.components.main_content import main_layout


def customers_page() -> rx.Component:
    """The UI for the customers page."""
    return rx.el.div(
        rx.vstack(
            rx.heading("Customers", size="5"),
        )
    )