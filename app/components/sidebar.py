import reflex as rx
from app.state import DashboardState


def nav_item(icon: str, text: str, href: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.cond(
            DashboardState.is_drawer_open,
            rx.el.span(text, class_name="font-medium"),
            None,
        ),
        class_name=rx.cond(
            DashboardState.is_drawer_open,
            rx.cond(
                is_active,
                "flex items-center gap-3 rounded-lg bg-teal-100/50 px-3 py-2 text-teal-600 transition-all",
                "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
            rx.cond(
                is_active,
                "flex items-center justify-center gap-3 rounded-lg bg-teal-100/50 p-3 text-teal-600 transition-all",
                "flex items-center justify-center gap-3 rounded-lg p-3 text-gray-500 transition-all hover:text-gray-900",
            ),
        ),
        href=href,
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("bar-chart-3", class_name="h-6 w-6 text-teal-600"),
                    rx.el.span("Northwind BI", class_name="sr-only"),
                    href="/",
                    class_name="flex items-center gap-2",
                ),
                rx.cond(
                    ~DashboardState.is_drawer_open,
                    None,
                    rx.el.h1(
                        "Northwind BI", class_name="text-xl font-bold text-gray-800"
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6",
        ),
        rx.el.div(
            rx.el.nav(
                nav_item(
                    "home", "Dashboard", "/", DashboardState.router.page.path == "/"
                ),
                nav_item(
                    "shopping-cart",
                    "Orders",
                    "/orders",
                    DashboardState.router.page.path == "/orders",
                ),
                nav_item("package", "Products", "#", False),
                nav_item("users", "Customers", "#", False),
                nav_item("line-chart", "Analytics", "#", False),
                class_name="grid items-start px-2 text-sm font-medium lg:px-4",
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        rx.cond(
            ~DashboardState.is_drawer_open,
            None,
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Upgrade to Pro", class_name="text-base font-semibold"),
                    rx.el.p(
                        "Unlock all features and get unlimited access to our support team.",
                        class_name="text-sm text-gray-500",
                    ),
                    rx.el.button(
                        "Upgrade",
                        class_name="mt-2 w-full bg-teal-500 text-white rounded-lg py-2 text-sm font-medium hover:bg-teal-600",
                    ),
                    class_name="p-4",
                ),
                class_name="mt-auto p-4",
            ),
        ),
        class_name=rx.cond(
            DashboardState.is_drawer_open,
            "flex flex-col w-64 h-screen bg-white border-r transition-all duration-300",
            "flex flex-col w-20 h-screen bg-white border-r transition-all duration-300 items-center",
        ),
    )