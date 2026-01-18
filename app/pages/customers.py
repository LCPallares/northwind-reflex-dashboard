import reflex as rx
from app.states.customers_state import CustomersState
from app.components.sidebar import sidebar


def customers_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    customer_statistics(),
                    filters_and_controls(),
                    customers_display(),
                    pagination_controls(),
                    class_name="p-4 lg:p-6 space-y-6",
                )
            ),
            class_name="flex-1 flex flex-col bg-gray-50/50",
        ),
        customer_detail_modal(),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-gray-100",
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.h1("Customers", class_name="text-2xl font-bold tracking-tight text-gray-900"),
        class_name="flex items-center justify-between w-full h-14 lg:h-[60px] px-4 lg:px-6 bg-white/50 backdrop-blur-sm border-b sticky top-0 z-10",
    )


def customer_statistics() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("users", class_name="h-8 w-8 text-blue-500"),
                rx.el.div(
                    rx.el.p("Total Customers", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(CustomersState.stats["total_customers"], class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("dollar-sign", class_name="h-8 w-8 text-green-500"),
                rx.el.div(
                    rx.el.p("Total Revenue", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(f"${CustomersState.stats['total_revenue']:,.2f}", class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("star", class_name="h-8 w-8 text-purple-500"),
                rx.el.div(
                    rx.el.p("VIP Customers", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(CustomersState.stats["vip_customers"], class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("globe", class_name="h-8 w-8 text-orange-500"),
                rx.el.div(
                    rx.el.p("Countries Served", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(CustomersState.stats["countries_served"], class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
        ),
        class_name="bg-white rounded-lg shadow-sm p-6 border",
    )


def filters_and_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            # Search bar
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500",
                ),
                rx.el.input(
                    placeholder="Search customers...",
                    on_change=CustomersState.set_search_query,
                    class_name="w-full max-w-sm pl-10 pr-4 py-2 border rounded-lg bg-white shadow-sm",
                ),
                class_name="relative",
            ),
            # Country filter
            rx.el.select(
                CustomersState.countries,
                value=CustomersState.country_filter,
                on_change=CustomersState.set_country_filter,
                class_name="border rounded-lg px-3 py-2 bg-white shadow-sm appearance-none",
            ),
            # City filter
            rx.el.select(
                CustomersState.cities,
                value=CustomersState.city_filter,
                on_change=CustomersState.set_city_filter,
                class_name="border rounded-lg px-3 py-2 bg-white shadow-sm appearance-none",
            ),
            # Segment filter
            rx.el.select(
                ["All", "VIP", "Regular", "New"],
                value=CustomersState.segment_filter,
                on_change=CustomersState.set_segment_filter,
                class_name="border rounded-lg px-3 py-2 bg-white shadow-sm appearance-none",
            ),
            class_name="flex items-center gap-4 flex-wrap",
        ),
        # Sort options
        rx.el.div(
            rx.el.button(
                rx.icon(
                    rx.cond(
                        CustomersState.sort_order == "asc",
                        "arrow-up",
                        "arrow-down"
                    ),
                    class_name="h-4 w-4 ml-2",
                ),
                f"Sort by {CustomersState.sort_by.replace('_', ' ').title()}",
                on_click=lambda: CustomersState.set_sort(CustomersState.sort_by),
                class_name="px-3 py-2 border rounded-lg bg-white shadow-sm flex items-center",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between flex-wrap gap-4 bg-white rounded-lg shadow-sm p-4 border",
    )


def customers_display() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            CustomersState.paginated_customers,
            customer_card,
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4",
    )


def customer_card(customer: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    customer["company_name"],
                    class_name="font-semibold text-gray-900 mb-1 line-clamp-2",
                ),
                customer_segment_badge(customer["customer_segment"]),
                class_name="flex justify-between items-start mb-2",
            ),
            rx.el.p(
                customer["contact_name"],
                class_name="text-sm text-gray-600 mb-1",
            ),
            rx.el.div(
                rx.icon("map-pin", class_name="h-4 w-4 text-gray-400 mr-1 inline"),
                f"{customer['city']}, {customer['country']}",
                class_name="text-xs text-gray-500 mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Orders:", class_name="text-sm text-gray-600"),
                    rx.el.p(
                        str(f"{customer['total_orders']}"),
                        class_name="font-bold text-gray-900",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Revenue:", class_name="text-sm text-gray-600"),
                    rx.el.p(
                        f"${customer['total_revenue']:.2f}",
                        class_name="font-bold text-gray-900",
                    ),
                ),
                class_name="flex justify-between items-center mb-3",
            ),
            rx.el.div(
                rx.el.p("Last Order:", class_name="text-xs text-gray-600 mb-1"),
                rx.el.p(
                    customer["last_order_date"],
                    class_name="text-xs font-semibold text-gray-900",
                ),
                class_name="text-left",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer",
        on_click=lambda: CustomersState.get_customer_details(customer["customer_id"]),
    )


def customer_segment_badge(segment: str) -> rx.Component:
    segment_colors = {
        "VIP": "bg-purple-100 text-purple-800",
        "Regular": "bg-blue-100 text-blue-800",
        "New": "bg-green-100 text-green-800",
    }
    return rx.el.span(
        segment,
        class_name=f"{segment_colors.get(segment, 'bg-gray-100 text-gray-800')} text-xs font-medium px-2.5 py-0.5 rounded-full w-fit",
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.span(
            f"Page {CustomersState.current_page} of {CustomersState.total_pages}",
            class_name="text-sm text-gray-700",
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=CustomersState.prev_page,
                disabled=CustomersState.current_page <= 1,
                class_name="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50",
            ),
            rx.el.button(
                "Next",
                on_click=CustomersState.next_page,
                disabled=CustomersState.current_page >= CustomersState.total_pages,
                class_name="inline-flex items-center px-4 py-2 ms-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50",
            ),
        ),
        class_name="flex items-center justify-between pt-4",
    )


def customer_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.content(
                rx.cond(
                    CustomersState.selected_customer,
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            CustomersState.selected_customer["company_name"],
                            class_name="text-xl font-bold mb-2",
                        ),
                        rx.radix.primitives.dialog.description(
                            f"Contact: {CustomersState.selected_customer['contact_name']}",
                            class_name="text-gray-600 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("City:", class_name="font-semibold"),
                                rx.el.p(CustomersState.selected_customer["city"]),
                            ),
                            rx.el.div(
                                rx.el.p("Country:", class_name="font-semibold"),
                                rx.el.p(CustomersState.selected_customer["country"]),
                            ),
                            class_name="grid grid-cols-2 gap-4 text-sm mb-4",
                        ),
                        rx.el.h3("Recent Orders", class_name="font-semibold mt-6 mb-4"),
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th("Order ID", class_name="text-left py-2"),
                                    rx.el.th("Order Date", class_name="text-left py-2"),
                                    rx.el.th("Shipped Date", class_name="text-left py-2"),
                                    rx.el.th("Total", class_name="text-right py-2"),
                                    rx.el.th("Status", class_name="text-center py-2"),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    CustomersState.customer_orders,
                                    lambda order: rx.el.tr(
                                        rx.el.td(f"#{order['order_id']}", class_name="py-2"),
                                        rx.el.td(order["order_date"], class_name="py-2"),
                                        rx.el.td(
                                            f"{order['shipped_date']}" or "N/A",
                                            class_name="py-2",
                                        ),
                                        rx.el.td(
                                            f"${order['total_amount']:.2f}",
                                            class_name="text-right py-2",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                order["status"],
                                                class_name=rx.cond(
                                                    order["status"] == "Shipped",
                                                    "bg-green-100 text-green-800",
                                                    "bg-yellow-100 text-yellow-800",
                                                )
                                                + " text-xs font-medium px-2.5 py-0.5 rounded-full w-fit mx-auto",
                                            ),
                                            class_name="text-center py-2",
                                        ),
                                        class_name="border-b",
                                    ),
                                )
                            ),
                            class_name="w-full text-sm mb-4",
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
        open=CustomersState.is_modal_open,
        on_open_change=CustomersState.close_modal,
    )