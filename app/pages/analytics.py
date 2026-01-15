import reflex as rx

#from app.components.main_content import main_layout


def analytics_page() -> rx.Component:
    """The UI for the analytics page."""
    return rx.el.div(
        rx.vstack(
            rx.heading("Analytics", size="5"),
        )
    )