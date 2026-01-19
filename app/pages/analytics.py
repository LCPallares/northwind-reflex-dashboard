import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.analytics_state import AnalyticsState


def analytics_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header("Analytics"),
            rx.el.main(
                rx.el.div(
                    key_metrics_cards(),
                    rx.el.div(
                        revenue_trends_section(),
                        category_profitability_section(),
                        class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
                    ),
                    rx.el.div(
                        customer_segmentation_section(),
                        employee_performance_section(),
                        class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
                    ),
                    seasonal_patterns_section(),
                    top_customers_clv_section(),
                    class_name="p-4 lg:p-6 space-y-6",
                )
            ),
            class_name="flex-1 flex flex-col bg-gray-50/50",
        ),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-gray-100",
    )


def key_metrics_cards() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            metric_card(
                "Total Revenue", 
                f"${AnalyticsState.total_revenue:,.2f}",
                "dollar-sign",
                "text-green-500",
                f"{AnalyticsState.profit_margin:.1f}% profit margin"
            ),
            metric_card(
                "Total Orders",
                str(f"{AnalyticsState.total_orders}"),
                "shopping-cart",
                "text-blue-500",
                f"${AnalyticsState.avg_order_value:.2f} avg order value"
            ),
            metric_card(
                "Profit Margin",
                f"{AnalyticsState.profit_margin:.1f}%",
                "trending-up",
                "text-purple-500",
                "Overall business health"
            ),
            metric_card(
                "Growth Rate",
                "+12.5%",
                "bar-chart",
                "text-orange-500",
                "Quarter over quarter"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
        ),
        class_name="bg-white rounded-lg shadow-sm p-6 border",
    )


def metric_card(title: str, value: str, icon: str, color: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-8 w-8 {color}"),
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-600"),
                rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
                rx.el.p(subtitle, class_name="text-xs text-gray-500 mt-1"),
            ),
            class_name="flex items-center space-x-3",
        ),
    )


def revenue_trends_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Revenue Trends", class_name="text-lg font-semibold mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Month", class_name="text-left py-2 text-sm font-medium text-gray-600"),
                        rx.el.th("Revenue", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                        rx.el.th("Orders", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        AnalyticsState.revenue_trends[-12:],  # Last 12 months
                        lambda month: rx.el.tr(
                            rx.el.td(month['month'], class_name="py-2 text-sm"),
                            rx.el.td(f"${month['revenue']:,.2f}", class_name="py-2 text-sm text-right"),
                            rx.el.td(str(f"{month['order_count']}"), class_name="py-2 text-sm text-right"),
                            class_name="border-b hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full bg-white rounded-lg border"
            ),
        ),
    )


def category_profitability_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Category Profitability", class_name="text-lg font-semibold mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Category", class_name="text-left py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Revenue", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Margin", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Units", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AnalyticsState.category_profitability,
                    lambda cat: rx.el.tr(
                        rx.el.td(cat["category"], class_name="py-2 text-sm"),
                        rx.el.td(f"${cat['revenue']:,.2f}", class_name="py-2 text-sm text-right"),
                        rx.el.td(
                            rx.el.span(
                                f"{cat['profit_margin']:.1f}%",
                                class_name=rx.cond(
                                    cat["profit_margin"] > 30,
                                    "text-green-600 font-medium",
                                    rx.cond(
                                        cat["profit_margin"] > 20,
                                        "text-yellow-600",
                                        "text-red-600"
                                    )
                                )
                            ),
                            class_name="py-2 text-sm text-right"
                        ),
                        rx.el.td(str(f"{cat['total_units']}"), class_name="py-2 text-sm text-right"),
                        class_name="border-b hover:bg-gray-50"
                    ),
                )
            ),
            class_name="w-full bg-white rounded-lg border"
        ),
    )


def customer_segmentation_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Customer Segmentation", class_name="text-lg font-semibold mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Segment", class_name="text-left py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Customers", class_name="text-center py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Avg Revenue", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Total Revenue", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AnalyticsState.customer_segments,
                    lambda segment: rx.el.tr(
                        rx.el.td(
                            rx.el.span(
                                segment["segment"],
                                class_name=rx.cond(
                                    segment["segment"] == "VIP",
                                    "bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-0.5 rounded-full",
                                    rx.cond(
                                        segment["segment"] == "Regular",
                                        "bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full",
                                        "bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full"
                                    )
                                )
                            ),
                            class_name="py-2"
                        ),
                        rx.el.td(str(f"{segment['count']}"), class_name="py-2 text-sm text-center"),
                        rx.el.td(f"${segment['avg_revenue']:,.2f}", class_name="py-2 text-sm text-right"),
                        rx.el.td(f"${segment['total_revenue']:,.2f}", class_name="py-2 text-sm text-right"),
                        class_name="border-b hover:bg-gray-50",
                    ),
                )
            ),
            class_name="w-full bg-white rounded-lg border"
        ),
    )


def employee_performance_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Employee Performance", class_name="text-lg font-semibold mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Employee", class_name="text-left py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Orders", class_name="text-center py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Total Sales", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Avg Order", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Performance", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AnalyticsState.employee_performance,
                    lambda emp: rx.el.tr(
                        rx.el.td(emp["employee_name"], class_name="py-2 text-sm font-medium"),
                        rx.el.td(str(f"{emp['order_count']}"), class_name="py-2 text-sm text-center"),
                        rx.el.td(f"${emp['total_sales']:,.2f}", class_name="py-2 text-sm text-right"),
                        rx.el.td(f"${emp['avg_order_value']:.2f}", class_name="py-2 text-sm text-right"),
                        rx.el.td(f"{emp['performance_score']:.1f}%", class_name="py-2 text-sm text-right"),
                        class_name="border-b hover:bg-gray-50",
                    ),
                )
            ),
            class_name="w-full bg-white rounded-lg border"
        ),
    )


def seasonal_patterns_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Seasonal Sales Patterns", class_name="text-lg font-semibold mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Quarter", class_name="text-left py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Revenue", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Growth Rate", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AnalyticsState.seasonal_patterns[-8:],  # Last 8 quarters
                    lambda quarter: rx.el.tr(
                        rx.el.td(quarter["quarter"], class_name="py-2 text-sm"),
                        rx.el.td(f"${quarter['revenue']:.2f}", class_name="py-2 text-sm text-right"),
                        rx.el.td(
                            rx.el.span(
                                f"{quarter['growth_rate']:.1f}%",
                                class_name=rx.cond(
                                    quarter["growth_rate"] > 0,
                                    "text-green-600",
                                    "text-red-600"
                                )
                            ),
                            class_name="py-2 text-sm text-right"
                        ),
                        class_name="border-b hover:bg-gray-50",
                    ),
                )
            ),
            class_name="w-full bg-white rounded-lg border"
        ),
    )


def top_customers_clv_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Top Customers by CLV", class_name="text-lg font-semibold mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Company", class_name="text-left py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Orders", class_name="text-center py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("Revenue", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                    rx.el.th("CLV", class_name="text-right py-2 text-sm font-medium text-gray-600"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AnalyticsState.top_customers_clv[:10],
                    lambda customer: rx.el.tr(
                        rx.el.td(customer["company_name"], class_name="py-2 text-sm font-medium"),
                        rx.el.td(str(f"{customer['order_count']}"), class_name="py-2 text-sm text-center"),
                        rx.el.td(f"${customer['total_revenue']:,.2f}", class_name="py-2 text-sm text-right"),
                        rx.el.td(f"${customer['clv']:,.2f}", class_name="py-2 text-sm text-right font-medium text-green-600"),
                        class_name="border-b hover:bg-gray-50"
                    ),
                )
            ),
            class_name="w-full bg-white rounded-lg border"
        ),
    )