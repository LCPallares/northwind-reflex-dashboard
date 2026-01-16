import reflex as rx
from app.states.orders_state import OrdersState
from app.components.sidebar import sidebar


def orders_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    order_statistics(),
                    filters(),
                    orders_table(),
                    pagination_controls(),
                    class_name="p-4 lg:p-6 space-y-6",
                )
            ),
            class_name="flex-1 flex flex-col bg-gray-50/50",
        ),
        order_detail_modal(),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-gray-100",
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.h1("Orders", class_name="text-2xl font-semibold"),
        class_name="flex items-center justify-between w-full h-14 lg:h-[60px] px-4 lg:px-6 bg-white/50 backdrop-blur-sm border-b sticky top-0 z-10",
    )


def order_statistics() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("shopping-cart", class_name="h-8 w-8 text-blue-500"),
                rx.el.div(
                    rx.el.p("Total Orders", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(OrdersState.stats["total_orders"], class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("dollar-sign", class_name="h-8 w-8 text-green-500"),
                rx.el.div(
                    rx.el.p("Total Revenue", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(f"${OrdersState.stats['total_revenue']:.2f}", class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("trending-up", class_name="h-8 w-8 text-purple-500"),
                rx.el.div(
                    rx.el.p("Avg Order Value", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(f"${OrdersState.stats['average_order_value']:.2f}", class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("package", class_name="h-8 w-8 text-orange-500"),
                rx.el.div(
                    rx.el.p("Pending Orders", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(OrdersState.stats["pending_orders"], class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
        ),
        class_name="bg-white rounded-lg shadow-sm p-6 border",
    )


def filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500",
            ),
            rx.el.input(
                placeholder="Search by Order ID, Customer...",
                on_change=OrdersState.set_search_query.debounce(300),
                class_name="w-full max-w-sm pl-10 pr-4 py-2 border rounded-lg bg-white shadow-sm",
            ),
            class_name="relative",
        ),
        rx.el.select(
            ["All", "Shipped", "Pending"],
            value=OrdersState.status_filter,
            on_change=OrdersState.set_status_filter,
            class_name="border rounded-lg px-3 py-2 bg-white shadow-sm appearance-none",
        ),
        class_name="flex items-center gap-4",
    )


def orders_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        table_header("Order ID", "order_id"),
                        table_header("Customer", "customer_name"),
                        table_header("Employee", "employee_name"),
                        table_header("Order Date", "order_date"),
                        table_header("Shipped Date", "shipped_date"),
                        table_header("Status", "status"),
                        table_header("Total", "total_revenue"),
                    )
                ),
                rx.el.tbody(rx.foreach(OrdersState.orders, order_row)),
                class_name="w-full text-sm text-left text-gray-500 min-w-[1200px]",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="relative w-full border shadow-md sm:rounded-lg bg-white overflow-x-auto",
    )


def table_header(text: str, sort_key: str) -> rx.Component:
    return rx.el.th(
        rx.el.button(
            text,
            rx.icon("arrow-up-down", class_name="ml-2 h-4 w-4 shrink-0"),
            on_click=lambda: OrdersState.set_sort(sort_key),
            class_name="flex items-center w-full text-left",
        ),
        scope="col",
        class_name="px-6 py-3 bg-gray-50 font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap",
    )


def order_row(order: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(order["order_id"], class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            order["customer_name"],
            class_name="px-6 py-4 font-medium text-gray-900 whitespace-nowrap",
        ),
        rx.el.td(order["employee_name"], class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(order["order_date"], class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            order.get("shipped_date", "N/A"), class_name="px-6 py-4 whitespace-nowrap"
        ),
        rx.el.td(
            rx.el.span(
                order["status"],
                class_name=rx.cond(
                    order["status"] == "Shipped",
                    "bg-green-100 text-green-800",
                    "bg-yellow-100 text-yellow-800",
                )
                + " text-xs font-medium px-2.5 py-0.5 rounded-full w-fit",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            f"${order['total_revenue']:.2f}",
            class_name="px-6 py-4 font-semibold text-right whitespace-nowrap",
        ),
        class_name="bg-white border-b hover:bg-gray-50 cursor-pointer",
        on_click=lambda: OrdersState.get_order_details(order["order_id"]),
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.span(
            f"Page {OrdersState.current_page} of {OrdersState.total_pages}",
            class_name="text-sm text-gray-700",
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=OrdersState.prev_page,
                disabled=OrdersState.current_page <= 1,
                class_name="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50",
            ),
            rx.el.button(
                "Next",
                on_click=OrdersState.next_page,
                disabled=OrdersState.current_page >= OrdersState.total_pages,
                class_name="inline-flex items-center px-4 py-2 ms-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50",
            ),
        ),
        class_name="flex items-center justify-between pt-4",
    )


def order_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.content(
                rx.cond(
                    OrdersState.selected_order,
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            f"Order #{OrdersState.selected_order['order_id']}",
                            class_name="text-xl font-bold mb-2",
                        ),
                        rx.radix.primitives.dialog.description(
                            f"Customer: {OrdersState.selected_order['customer_name']}",
                            class_name="text-gray-600 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Order Date:", class_name="font-semibold"),
                                rx.el.p(OrdersState.selected_order["order_date"]),
                            ),
                            rx.el.div(
                                rx.el.p("Shipped Date:", class_name="font-semibold"),
                                rx.el.p(
                                    OrdersState.selected_order.get(
                                        "shipped_date", "N/A"
                                    )
                                ),
                            ),
                            rx.el.div(
                                rx.el.p("Status:", class_name="font-semibold"),
                                rx.el.p(OrdersState.selected_order["status"]),
                            ),
                            class_name="grid grid-cols-3 gap-4 text-sm mb-4",
                        ),
                        rx.el.h3("Order Items", class_name="font-semibold mt-6 mb-2"),
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th("Product", class_name="text-left py-2"),
                                    rx.el.th("Price", class_name="text-right py-2"),
                                    rx.el.th("Qty", class_name="text-right py-2"),
                                    rx.el.th("Total", class_name="text-right py-2"),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    OrdersState.selected_order["items"],
                                    lambda item: rx.el.tr(
                                        rx.el.td(item["product_name"]),
                                        rx.el.td(
                                            f"${item['unit_price']:.2f}",
                                            class_name="text-right",
                                        ),
                                        rx.el.td(
                                            item["quantity"], class_name="text-right"
                                        ),
                                        rx.el.td(
                                            f"${item['total']:.2f}",
                                            class_name="text-right font-medium",
                                        ),
                                        class_name="border-b",
                                    ),
                                )
                            ),
                            class_name="w-full text-sm",
                        ),
                        rx.el.div(
                            rx.el.div(class_name="flex-grow"),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p("Freight:"),
                                    rx.el.p(
                                        f"${OrdersState.selected_order['freight']:.2f}"
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.p("Grand Total:", class_name="font-bold"),
                                    rx.el.p(
                                        f"${OrdersState.selected_order['total_revenue'] + OrdersState.selected_order['freight']:.2f}",
                                        class_name="font-bold",
                                    ),
                                ),
                                class_name="flex flex-col items-end gap-1 text-sm",
                            ),
                            class_name="flex mt-4",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon(tag="x"),
                                class_name="absolute top-3 right-3 p-1 rounded-full hover:bg-gray-100",
                            )
                        ),
                        class_name="relative",
                    ),
                    rx.spinner(size="3"),
                )
            )
        ),
        open=OrdersState.is_modal_open,
        on_open_change=OrdersState.close_modal,
    )