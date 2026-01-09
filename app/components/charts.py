import reflex as rx
from app.state import DashboardState
import plotly.express as px
import pandas as pd


def sales_over_time_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Sales Over Time", class_name="font-semibold text-lg text-gray-800"),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#E5E7EB"),
            rx.recharts.area(
                data_key="sales",
                type="natural",
                stroke="#14B8A6",
                fill="#14B8A6",
                fill_opacity=0.2,
                stroke_width=2,
            ),
            rx.recharts.x_axis(data_key="month", stroke="#9CA3AF", font_size=12),
            rx.recharts.y_axis(stroke="#9CA3AF", font_size=12),
            rx.recharts.tooltip(),
            data=DashboardState.sales_data,
            height=300,
            margin={"top": 20, "right": 20, "left": -10, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def top_products_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Top 5 Products", class_name="font-semibold text-lg text-gray-800 mb-4"
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Rank",
                        class_name="text-left text-sm font-medium text-gray-500 py-2",
                    ),
                    rx.el.th(
                        "Product",
                        class_name="text-left text-sm font-medium text-gray-500 py-2",
                    ),
                    rx.el.th(
                        "Revenue",
                        class_name="text-right text-sm font-medium text-gray-500 py-2",
                    ),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    DashboardState.top_products,
                    lambda product, index: rx.el.tr(
                        rx.el.td(index + 1, class_name="py-3 text-sm text-gray-600"),
                        rx.el.td(
                            product["name"],
                            class_name="py-3 text-sm text-gray-800 font-medium",
                        ),
                        rx.el.td(
                            f"${product['revenue']:.2f}",
                            class_name="py-3 text-sm text-gray-600 text-right",
                        ),
                        class_name="border-b border-gray-100",
                    ),
                )
            ),
            class_name="w-full",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-full",
    )


def category_performance_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Category Performance",
            class_name="font-semibold text-lg text-gray-800 mb-4",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#E5E7EB"),
            rx.recharts.x_axis(
                data_key="category", type="category", stroke="#9CA3AF", font_size=12
            ),
            rx.recharts.y_axis(stroke="#9CA3AF", font_size=12),
            rx.recharts.tooltip(),
            rx.recharts.bar(data_key="revenue", fill="#14B8A6", radius=[4, 4, 0, 0]),
            data=DashboardState.category_performance,
            height=350,
            margin={"top": 10, "right": 30, "left": 0, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def top_customers_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Top Customers", class_name="font-semibold text-lg text-gray-800 mb-4"
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Customer",
                        class_name="text-left text-sm font-medium text-gray-500 py-2",
                    ),
                    rx.el.th(
                        "Revenue",
                        class_name="text-right text-sm font-medium text-gray-500 py-2",
                    ),
                    rx.el.th(
                        "Orders",
                        class_name="text-right text-sm font-medium text-gray-500 py-2",
                    ),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    DashboardState.top_customers,
                    lambda customer: rx.el.tr(
                        rx.el.td(
                            customer["name"],
                            class_name="py-3 text-sm text-gray-800 font-medium",
                        ),
                        rx.el.td(
                            f"${customer['revenue']:.2f}",
                            class_name="py-3 text-sm text-gray-600 text-right",
                        ),
                        rx.el.td(
                            customer["orders"],
                            class_name="py-3 text-sm text-gray-600 text-right",
                        ),
                        class_name="border-b border-gray-100",
                    ),
                )
            ),
            class_name="w-full",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-full",
    )


def employee_performance_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Employee Performance (Sales)",
            class_name="font-semibold text-lg text-gray-800 mb-4",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#E5E7EB"),
            rx.recharts.x_axis(
                data_key="name",
                type="category",
                stroke="#9CA3AF",
                font_size=10,
                tick=False,
                axis_line=False,
            ),
            rx.recharts.y_axis(stroke="#9CA3AF", font_size=12),
            rx.recharts.tooltip(),
            rx.recharts.bar(data_key="sales", fill="#3B82F6", radius=[4, 4, 0, 0]),
            data=DashboardState.employee_performance,
            height=300,
            margin={"top": 10, "right": 30, "left": 0, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def geo_sales_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Sales by Country", class_name="font-semibold text-lg text-gray-800 mb-4"
        ),
        rx.plotly(data=DashboardState.geo_sales_fig, class_name="w-full h-full"),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def order_status_overview() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Order Status", class_name="font-semibold text-lg text-gray-800 mb-4"),
        rx.el.div(
            rx.foreach(
                DashboardState.order_statuses,
                lambda status: rx.el.div(
                    rx.el.p(
                        status["status"], class_name="text-sm font-medium text-gray-500"
                    ),
                    rx.el.p(
                        status["count"], class_name="text-2xl font-bold text-gray-800"
                    ),
                    class_name="flex flex-col items-center justify-center p-4 bg-gray-50 rounded-lg",
                ),
            ),
            class_name="grid grid-cols-3 gap-4",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-full",
    )