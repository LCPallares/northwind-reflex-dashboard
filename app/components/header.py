import reflex as rx
from reflex.style import set_color_mode, color_mode

# Estilos dinámicos globales
ESTILO_TEXTO = rx.color_mode_cond(light="text-gray-900", dark="text-gray-100")
ESTILO_BG_CARD = rx.color_mode_cond(light="bg-white", dark="bg-gray-900")
ESTILO_BORDER = rx.color_mode_cond(light="border-gray-200", dark="border-gray-800")


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
        on_change=set_color_mode,
        value=color_mode,
        variant="classic",
    )


def header(title: str, dashboard_state=None) -> rx.Component:
    """Header reutilizable que acepta un título y opcionalmente un estado para el toggle del drawer."""
    
    # Componente de búsqueda (común para ambas versiones)
    search_component = rx.el.form(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
            ),
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
    )
    
    # Componente de perfil (común para ambas versiones)
    profile_component = rx.el.div(
        rx.image(
            src="https://api.dicebear.com/9.x/initials/svg?seed=Admin",
            class_name="size-9 rounded-full border-2 border-white shadow-sm",
        ),
        dark_mode_toggle(),
        class_name="flex items-center gap-4",
    )
    
    # Left side: título con o sin botón toggle
    if dashboard_state:
        left_side = rx.el.div(
            rx.el.button(
                rx.icon(
                    rx.cond(
                        dashboard_state.is_drawer_open,
                        "panel-left-close",
                        "panel-left-open",
                    ),
                    class_name="h-5 w-5",
                ),
                on_click=dashboard_state.toggle_drawer,
                class_name="p-2 rounded-md hover:bg-gray-100 text-gray-600",
            ),
            rx.el.h1(
                title,
                class_name=f"text-2xl font-bold tracking-tight {ESTILO_TEXTO}"
            ),
            class_name="flex items-center gap-4",
        )
    else:
        left_side = rx.el.div(
            rx.el.h1(
                title,
                class_name=f"text-2xl font-bold tracking-tight {ESTILO_TEXTO}"
            ),
            class_name="flex items-center gap-4",
        )
    
    return rx.el.header(
        left_side,
        rx.el.div(
            search_component,
            profile_component,
            class_name="flex items-center gap-4",
        ),
        bg=rx.color_mode_cond(light="rgba(255, 255, 255, 0.5)", dark="rgba(26, 26, 26, 0.5)"),
        border_bottom=rx.color_mode_cond(light="1px solid #e5e7eb", dark="1px solid #374151"),
        class_name=f"flex items-center justify-between w-full h-14 border-b sticky top-0 z-30 backdrop-blur-sm {ESTILO_BG_CARD} {ESTILO_BORDER}",
    )