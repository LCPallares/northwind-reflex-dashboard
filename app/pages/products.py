import reflex as rx
from app.states.products_state import ProductsState
from app.components.sidebar import sidebar


def products_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    product_statistics(),
                    filters_and_controls(),
                    products_display(),
                    pagination_controls(),
                    class_name="p-4 lg:p-6 space-y-6",
                )
            ),
            class_name="flex-1 flex flex-col bg-gray-50/50",
        ),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-gray-100",
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.h1("Products", class_name="text-2xl font-bold tracking-tight text-gray-900"),
        class_name="flex items-center justify-between w-full h-14 lg:h-[60px] px-4 lg:px-6 bg-white/50 backdrop-blur-sm border-b sticky top-0 z-10",
    )


def product_statistics() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("package", class_name="h-8 w-8 text-blue-500"),
                rx.el.div(
                    rx.el.p("Total Products", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(ProductsState.stats["total_products"], class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("dollar-sign", class_name="h-8 w-8 text-green-500"),
                rx.el.div(
                    rx.el.p("Inventory Value", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(f"${ProductsState.stats['total_inventory_value']:,.2f}", class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("triangle_alert", class_name="h-8 w-8 text-orange-500"),
                rx.el.div(
                    rx.el.p("Low Stock", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(ProductsState.stats["low_stock_products"], class_name="text-2xl font-bold text-gray-900"),
                ),
                class_name="flex items-center space-x-3",
            ),
            rx.el.div(
                rx.icon("circle_x", class_name="h-8 w-8 text-red-500"),
                rx.el.div(
                    rx.el.p("Out of Stock", class_name="text-sm font-medium text-gray-600"),
                    rx.el.p(ProductsState.stats["out_of_stock_products"], class_name="text-2xl font-bold text-gray-900"),
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
                    placeholder="Search products...",
                    on_change=ProductsState.set_search_query,
                    class_name="w-full max-w-sm pl-10 pr-4 py-2 border rounded-lg bg-white shadow-sm",
                ),
                class_name="relative",
            ),
            # Category filter
            rx.el.select(
                ProductsState.categories,
                value=ProductsState.category_filter,
                on_change=ProductsState.set_category_filter,
                class_name="border rounded-lg px-3 py-2 bg-white shadow-sm appearance-none",
            ),
            # Sort options
            rx.el.select(
                ["product_name", "unit_price", "units_in_stock", "category_name"],
                value=ProductsState.sort_by,
                on_change=ProductsState.set_sort,
                class_name="border rounded-lg px-3 py-2 bg-white shadow-sm appearance-none",
            ),
            class_name="flex items-center gap-4 flex-wrap",
        ),
        # View toggle and sort order
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("layout_grid", class_name="h-4 w-4"),
                    on_click=lambda: ProductsState.set_view_mode("grid"),
                    class_name=rx.cond(
                        ProductsState.view_mode == "grid",
                        "bg-blue-500 text-white",
                        "bg-gray-200 text-gray-700"
                    ) + " px-3 py-2 rounded-l-lg border",
                ),
                rx.el.button(
                    rx.icon("list", class_name="h-4 w-4"),
                    on_click=lambda: ProductsState.set_view_mode("list"),
                    class_name=rx.cond(
                        ProductsState.view_mode == "list",
                        "bg-blue-500 text-white",
                        "bg-gray-200 text-gray-700"
                    ) + " px-3 py-2 rounded-r-lg border border-l-0",
                ),
                class_name="flex",
            ),
            rx.el.button(
                rx.icon(
                    rx.cond(
                        ProductsState.sort_order == "asc",
                        "arrow-up",
                        "arrow-down"
                    ),
                    class_name="h-4 w-4 ml-2",
                ),
                f"Sort by {ProductsState.sort_by.replace('_', ' ').title()}",
                on_click=lambda: ProductsState.set_sort(ProductsState.sort_by),
                class_name="px-3 py-2 border rounded-lg bg-white shadow-sm flex items-center",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between flex-wrap gap-4 bg-white rounded-lg shadow-sm p-4 border",
    )


def products_display() -> rx.Component:
    return rx.cond(
        ProductsState.view_mode == "grid",
        products_grid(),
        products_list(),
    )


def products_grid() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            ProductsState.paginated_products,
            product_card,
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4",
    )


def product_card(product: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    product["product_name"],
                    class_name="font-semibold text-gray-900 mb-1 line-clamp-2",
                ),
                inventory_status_badge(product["inventory_status"]),
                class_name="flex justify-between items-start mb-2",
            ),
            rx.el.p(
                product["category_name"],
                class_name="text-sm text-gray-600 mb-1",
            ),
            rx.el.p(
                product["supplier_name"],
                class_name="text-xs text-gray-500 mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Price:", class_name="text-sm text-gray-600"),
                    rx.el.p(
                        f"${product['unit_price']:.2f}",
                        class_name="font-bold text-gray-900",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Stock:", class_name="text-sm text-gray-600"),
                    rx.el.p(
                        str(f"{product['units_in_stock']}"),
                        class_name="font-semibold text-gray-900",
                    ),
                ),
                class_name="flex justify-between items-center",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer",
    )


def products_list() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        table_header("Product Name", "product_name"),
                        table_header("Category", "category_name"),
                        table_header("Supplier", "supplier_name"),
                        table_header("Price", "unit_price"),
                        table_header("Stock", "units_in_stock"),
                        table_header("Status", "inventory_status"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(ProductsState.paginated_products, product_row)
                ),
                class_name="w-full text-sm text-left text-gray-500",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="relative w-full border shadow-md sm:rounded-lg bg-white overflow-x-auto",
    )


def table_header(text: str, sort_key: str) -> rx.Component:
    return rx.el.th(
        text,
        scope="col",
        class_name="px-6 py-3 bg-gray-50 font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap cursor-pointer hover:bg-gray-100",
        on_click=lambda: ProductsState.set_sort(sort_key),
    )


def product_row(product: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            product["product_name"],
            class_name="px-6 py-4 font-medium text-gray-900 whitespace-nowrap",
        ),
        rx.el.td(product["category_name"], class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(product["supplier_name"], class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            f"${product['unit_price']:.2f}",
            class_name="px-6 py-4 text-right whitespace-nowrap",
        ),
        rx.el.td(
            str(product["units_in_stock"]),
            class_name="px-6 py-4 text-center whitespace-nowrap",
        ),
        rx.el.td(
            inventory_status_badge(product["inventory_status"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        class_name="bg-white border-b hover:bg-gray-50",
    )


def inventory_status_badge(status: str) -> rx.Component:
    status_colors = {
        "In Stock": "bg-green-100 text-green-800",
        "Low Stock": "bg-yellow-100 text-yellow-800",
        "Out of Stock": "bg-red-100 text-red-800",
    }
    return rx.el.span(
        status,
        class_name=f"{status_colors.get(status, 'bg-gray-100 text-gray-800')} text-xs font-medium px-2.5 py-0.5 rounded-full w-fit",
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.span(
            f"Page {ProductsState.current_page} of {ProductsState.total_pages}",
            class_name="text-sm text-gray-700",
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=ProductsState.prev_page,
                disabled=ProductsState.current_page <= 1,
                class_name="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50",
            ),
            rx.el.button(
                "Next",
                on_click=ProductsState.next_page,
                disabled=ProductsState.current_page >= ProductsState.total_pages,
                class_name="inline-flex items-center px-4 py-2 ms-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50",
            ),
        ),
        class_name="flex items-center justify-between pt-4",
    )