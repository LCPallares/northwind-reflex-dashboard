import reflex as rx
from app.state import DashboardState
from app.components.charts import (
    sales_over_time_chart,
    top_products_chart,
    category_performance_chart,
    top_customers_table,
    employee_performance_chart,
    geo_sales_chart,
    order_status_overview,
)


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
        #class_name="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow duration-300",
        #style={"box-shadow": "0 1px 3px 0 rgba(0, 0, 0, 0.05)"},

        bg=rx.color_mode_cond(light="white", dark="#262626"),
        border=rx.color_mode_cond(light="1px solid #e5e7eb", dark="1px solid #3f3f46"),
        class_name="p-6 rounded-xl shadow-sm",

    )


def main_content() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        rx.cond(
                            DashboardState.is_drawer_open,
                            "panel-left-close",
                            "panel-left-open",
                        ),
                        class_name="h-5 w-5",
                    ),
                    on_click=DashboardState.toggle_drawer,
                    class_name="p-2 rounded-md hover:bg-gray-100 text-gray-600",
                ),
                rx.el.h1(
                    "Dashboard", 
                    #class_name="text-2xl font-bold tracking-tight text-gray-900"
                    class_name=f"text-2xl font-bold tracking-tight {ESTILO_TEXTO}"
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        # Icono con color suave para no distraer
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                        ),
                        # Input con estados focus y hover definidos
                        rx.el.input(
                            type="search",
                            placeholder="Buscar...",
                            class_name="""
                                w-full lg:w-[400px] pl-10 pr-4 py-2 
                                bg-gray-50 border border-gray-200 rounded-xl
                                text-sm transition-all duration-200
                                placeholder:text-gray-500
                                focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 
                                outline-none hover:border-gray-300
                            """,
                        ),
                        class_name="relative group",
                    ),
                    class_name="flex-1 max-w-md",
                ),

                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed=Admin",
                    class_name="size-9 rounded-full border-2 border-white shadow-sm",
                ),
                dark_mode_toggle(),
                class_name="flex items-center gap-4",
            ),
            #class_name="flex items-center justify-between w-full h-14 lg:h-[60px] px-4 lg:px-6 bg-white/50 backdrop-blur-sm border-b sticky top-0 z-30",

            # PROPIEDADES DIRECTAS PARA EL MODO OSCURO
            bg=rx.color_mode_cond(light="rgba(255, 255, 255, 0.5)", dark="rgba(26, 26, 26, 0.5)"),
            border_bottom=rx.color_mode_cond(light="1px solid #e5e7eb", dark="1px solid #374151"),
            #class_name="flex items-center justify-between w-full h-14 lg:h-[60px] px-4 lg:px-6 sticky top-0 z-30 backdrop-blur-sm",
            class_name=f"flex items-center justify-between w-full h-14 border-b sticky top-0 z-30 backdrop-blur-sm {ESTILO_BG_CARD} {ESTILO_BORDER}",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.input(
                    type="date",
                    default_value=DashboardState.date_filter_start,
                    on_change=DashboardState.set_date_filter_start,
                    # bg-gray-50 para el fondo, text-gray-900 para el texto, y scheme-light/dark para el icono
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
                category_performance_chart(),
                employee_performance_chart(),
                class_name="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-2 p-4 lg:p-6 pt-0",
            ),
            rx.el.div(
                top_customers_table(),
                order_status_overview(),
                class_name="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-2 p-4 lg:p-6 pt-0",
            ),
            rx.el.div(geo_sales_chart(), class_name="p-4 lg:p-6 pt-0"),
            #class_name="flex flex-col gap-4",

            # Fondo del área de contenido
            #bg=rx.color_mode_cond(light="#f9fafb", dark="#111111"), 
            #class_name="flex flex-col gap-4",

            # Para el fondo principal, usamos un gris casi negro en dark
            bg=rx.color_mode_cond(light="#f9fafb", dark="#0f0f10"),
            class_name="min-h-screen p-4",


        ),
        #class_name="flex-1 flex flex-col bg-gray-50/50",

        # Fondo total de la página
        bg=rx.color_mode_cond(light="white", dark="#1a1a1a"),
        color=rx.color_mode_cond(light="black", dark="white"), # Cambia el color de fuente global
        class_name="flex-1 flex flex-col min-h-screen",

        # background_color="#87CEFA",  # azul claro
        # background_color=rx.color("grass", 7),  # verde oscuro

    )


from reflex.style import set_color_mode, color_mode

def dark_mode_toggle() -> rx.Component:
    return rx.segmented_control.root(
        rx.segmented_control.item(
            rx.icon("sun", size=16),
            value="light",
        ),
        rx.segmented_control.item(
            rx.icon("moon", size=16),
            value="dark",
        ),
        on_change=set_color_mode, # Función integrada de Reflex
        value=color_mode,        # Variable de estado integrada
        variant="classic",
    )

