"""Página de análisis de datos."""
import reflex as rx
from app.components.main_content import main_content
from app.components.charts import (
    analytics_sales_over_time,
    analytics_top_products,
    analytics_sales_by_country,
)
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

#@rx.page(route="/analytics", title="Analytics")
def analytics_page() -> rx.Component:
    """La página de análisis de datos."""
    return rx.el.div(
        rx.vstack(
            rx.heading("Análisis de Ventas", size="8", mb="6"),
            rx.grid(
                card(
                    analytics_sales_over_time(),
                    heading="Ventas a lo largo del tiempo",
                ),
                card(
                    analytics_top_products(),
                    heading="Top 5 Productos más vendidos",
                ),
                card(
                    analytics_sales_by_country(),
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
'''
@rx.page(route="/", title="Dashboard")
def dashboard_page() -> rx.Component:
    """The dashboard page."""
    from app.components.charts import (
        sales_over_time_chart,
        top_products_chart,
        category_performance_chart,
        top_customers_table,
        employee_performance_chart,
        geo_sales_chart,
        order_status_overview,
    )
    from app.state import DashboardState

    return rx.el.div(
        rx.grid(
            rx.grid(
                sales_over_time_chart(),
                rx.grid(
                    top_products_chart(),
                    order_status_overview(),
                    grid_template_columns="1fr 1fr",
                    gap=6,
                ),
                grid_template_rows="auto 1fr",
                gap=6,
            ),
            rx.grid(
                category_performance_chart(),
                employee_performance_chart(),
                grid_template_columns="2fr 1fr",
                gap=6,
            ),
            rx.grid(
                top_customers_table(),
                geo_sales_chart(),
                grid_template_columns="1fr 1fr",
                gap=6,
            ),
            grid_template_rows="repeat(3, auto)",
            gap=6,
            width="100%",
            padding_x="2em",
            padding_y="2em",
        ),
        on_mount=DashboardState.load_entries,
        background_color="#F7F9FC",
    )
'''
