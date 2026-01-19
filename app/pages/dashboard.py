import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.charts import (
    sales_over_time_chart,
    top_products_chart,
    category_performance_chart,
    top_customers_table,
    employee_performance_chart,
    geo_sales_chart,
    order_status_overview,
    analytics_sales_over_time,
    analytics_top_products,
    analytics_sales_by_country,
)
from app.states.dashboard_state import DashboardState

# Estilos dinámicos globales
ESTILO_TEXTO = rx.color_mode_cond(light="text-gray-900", dark="text-gray-100")
ESTILO_TEXTO_SUAVE = rx.color_mode_cond(light="text-gray-500", dark="text-gray-400")
ESTILO_BG_CARD = rx.color_mode_cond(light="bg-white", dark="bg-gray-900")
ESTILO_BORDER = rx.color_mode_cond(light="border-gray-200", dark="border-gray-800")


def kpi_card(kpi: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(kpi["title"], class_name="text-sm font-medium text-gray-600"),
                rx.icon(kpi["icon"], class_name=f"h-4 w-4 {kpi['color']}"),
                class_name="flex items-center justify-between",
            ),
            rx.el.p(kpi["value"], class_name="text-3xl font-bold text-gray-800 mt-1"),
            rx.el.p("+20.1% from last month", class_name="text-xs text-gray-500 mt-1"),
            class_name="p-6",
        ),
        bg=rx.color_mode_cond(light="white", dark="#262626"),
        border=rx.color_mode_cond(light="1px solid #e5e7eb", dark="1px solid #3f3f46"),
        class_name="p-6 rounded-xl shadow-sm",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header("Dashboard", DashboardState),
            rx.el.main(
                rx.el.div(
                    rx.el.input(
                        type="date",
                        default_value=DashboardState.date_filter_start,
                        on_change=DashboardState.set_date_filter_start,
                        class_name="border border-gray-300 rounded-lg p-2 bg-gray-50 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition-all color-scheme-light",
                    ),
                    rx.el.input(
                        type="date",
                        default_value=DashboardState.date_filter_end,
                        on_change=DashboardState.set_date_filter_end,
                        class_name="border border-gray-300 rounded-lg p-2 bg-gray-50 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:bg-white outline-none transition-all color-scheme-light",
                    ),
                    rx.el.button(
                        "Apply",
                        on_click=DashboardState.on_load,
                        class_name="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600",
                    ),
                    class_name="flex items-center gap-4 p-4 lg:p-6",
                ),
                rx.el.div(
                    rx.foreach(DashboardState.kpis, kpi_card),
                    class_name="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4 p-4 lg:p-6 pt-0",
                ),
                rx.el.div(
                    sales_over_time_chart(),
                    top_products_chart(),
                    class_name="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-2 p-4 lg:p-6 pt-0",
                ),
                rx.el.div(
                    analytics_sales_over_time(),
                    analytics_top_products(),
                    class_name="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-2 p-4 lg:p-6 pt-0",
                ),
                rx.el.div(
                    category_performance_chart(),
                    employee_performance_chart(),
                    class_name="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-2 p-4 lg:p-6 pt-0",
                ),
                rx.el.div(
                    analytics_sales_by_country(),
                    class_name="grid gap-4 md:gap-8 lg:grid-cols-1 xl:grid-cols-1 p-4 lg:p-6 pt-0",
                ),
                rx.el.div(
                    top_customers_table(),
                    order_status_overview(),
                    class_name="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-2 p-4 lg:p-6 pt-0",
                ),
                rx.el.div(geo_sales_chart(), class_name="p-4 lg:p-6 pt-0"),
                
                bg=rx.color_mode_cond(light="#f9fafb", dark="#0f0f10"),
                class_name="min-h-screen p-4",
            ),
            bg=rx.color_mode_cond(light="white", dark="#1a1a1a"),
            color=rx.color_mode_cond(light="black", dark="white"),
            class_name="flex-1 flex flex-col min-h-screen",
        ),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-gray-100",
    )