import reflex as rx
from app.state import DashboardState
from app.pages.orders import orders_page
from app.pages.products import products_page
from app.pages.customers import customers_page
from app.pages.analytics import analytics_page
from app.states.orders_state import OrdersState
from app.states.products_state import ProductsState
from app.states.customers_state import CustomersState
from app.states.analytics_state import AnalyticsState
from app.components.sidebar import sidebar
from app.components.main_content import main_content


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        main_content(),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-gray-100",
        on_mount=DashboardState.on_load,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(orders_page, route="/orders", on_load=[OrdersState.fetch_orders, OrdersState.fetch_stats])
app.add_page(products_page, route="/products", on_load=[ProductsState.fetch_products, ProductsState.fetch_stats])
app.add_page(customers_page, route="/customers", on_load=[CustomersState.fetch_customers, CustomersState.fetch_stats])
app.add_page(analytics_page, route="/analytics", on_load=AnalyticsState.fetch_analytics_data)