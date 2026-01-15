"""Página de análisis de datos."""
import reflex as rx
from app.components.main_content import main_content
from app.components.charts import generic_line_chart, generic_bar_chart
from app.states.analytics_state import AnalyticsState

def card(child: rx.Component, heading: str) -> rx.Component:
    """
    Crea una tarjeta para mostrar un gráfico con un encabezado.
    """
    return rx.box(
        rx.heading(heading, size="6", mb="4"),
        child,
        p="6",
        border_radius="10px",
        border="1px solid #E2E8F0",
        bg="white",
        width="100%",
    )

@rx.page(route="/analytics", title="Analytics")
def analytics_page() -> rx.Component:
    """La página de análisis de datos."""
    return rx.el.div(
        rx.vstack(
            rx.heading("Análisis de Ventas", size="8", mb="6"),
            rx.grid(
                card(
                    generic_line_chart(
                        data=AnalyticsState.sales_over_time,
                        x_axis_key="month",
                        y_axis_keys=["ventas"],
                    ),
                    heading="Ventas a lo largo del tiempo",
                ),
                card(
                    generic_bar_chart(
                        data=AnalyticsState.top_products,
                        x_axis_key="producto",
                        y_axis_keys=["cantidad"],
                    ),
                    heading="Top 5 Productos más vendidos",
                ),
                card(
                    generic_bar_chart(
                        data=AnalyticsState.sales_by_country,
                        x_axis_key="pais",
                        y_axis_keys=["ventas"],
                    ),
                    heading="Ventas por País (Top 10)",
                ),
                spacing="6",
                columns="1",
                width="100%",
            ),
            spacing="6",
            width="100%",
            on_mount=AnalyticsState.fetch_analytics_data,
        )
    )
