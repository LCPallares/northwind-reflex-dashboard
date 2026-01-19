import reflex as rx
import sqlite3
from typing import TypedDict, Any
import plotly.graph_objects as go
import os
import random
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

DB_PATH = "northwind.db"


class KPI(TypedDict):
    title: str
    value: str
    icon: str
    color: str


class SalesData(TypedDict):
    month: str
    sales: float


class TopProduct(TypedDict):
    name: str
    revenue: float


class CategoryPerformance(TypedDict):
    category: str
    revenue: float


class TopCustomer(TypedDict):
    name: str
    revenue: float
    orders: int


class EmployeePerformance(TypedDict):
    name: str
    sales: float
    orders: int


class GeoSale(TypedDict):
    country: str
    sales: float


class OrderStatus(TypedDict):
    status: str
    count: int


# Analytics charts data types
class AnalyticsSalesOverTime(TypedDict):
    month: str
    ventas: int


class AnalyticsTopProduct(TypedDict):
    producto: str
    cantidad: int


class AnalyticsSalesByCountry(TypedDict):
    pais: str
    ventas: float


class DashboardState(rx.State):
    is_drawer_open: bool = False
    kpis: list[KPI] = [
        {
            "title": "Total Revenue",
            "value": "$0.00",
            "icon": "dollar-sign",
            "color": "text-green-500",
        },
        {
            "title": "Total Orders",
            "value": "0",
            "icon": "shopping-cart",
            "color": "text-blue-500",
        },
        {
            "title": "Total Customers",
            "value": "0",
            "icon": "users",
            "color": "text-purple-500",
        },
        {
            "title": "Total Products",
            "value": "0",
            "icon": "package",
            "color": "text-orange-500",
        },
    ]
    sales_data: list[SalesData] = []
    top_products: list[TopProduct] = []
    category_performance: list[CategoryPerformance] = []
    top_customers: list[TopCustomer] = []
    employee_performance: list[EmployeePerformance] = []
    geo_sales: list[GeoSale] = []
    order_statuses: list[OrderStatus] = []
    date_filter_start: str = "2024-01-01"
    date_filter_end: str = "2024-12-31"
    
    # Analytics charts data
    analytics_sales_over_time: list[AnalyticsSalesOverTime] = []
    analytics_top_products: list[AnalyticsTopProduct] = []
    analytics_sales_by_country: list[AnalyticsSalesByCountry] = []

    @rx.var
    def geo_sales_fig(self) -> go.Figure:
        if not self.geo_sales:
            fig = go.Figure()
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                geo=dict(bgcolor="rgba(0,0,0,0)"),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            return fig
        df = pd.DataFrame(self.geo_sales)
        fig = px.choropleth(
            data_frame=df,
            locations="country",
            locationmode="country names",
            color="sales",
            hover_name="country",
            color_continuous_scale=px.colors.sequential.Teal,
            template="plotly_white",
        ).update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            geo=dict(bgcolor="rgba(0,0,0,0)"),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    @rx.event
    def toggle_drawer(self):
        self.is_drawer_open = not self.is_drawer_open

    @rx.event
    def set_date_filter_start(self, value: str):
        self.date_filter_start = value

    @rx.event
    def set_date_filter_end(self, value: str):
        self.date_filter_end = value

    @rx.event(background=True)
    async def on_load(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # KPIs y datos principales
        cursor.execute(
            "SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) FROM OrderDetails od JOIN Orders o ON od.OrderID = o.OrderID WHERE o.OrderDate BETWEEN ? AND ?",
            (self.date_filter_start, self.date_filter_end),
        )
        total_revenue = cursor.fetchone()[0] or 0
        
        cursor.execute(
            "SELECT COUNT(*) FROM Orders WHERE OrderDate BETWEEN ? AND ?",
            (self.date_filter_start, self.date_filter_end),
        )
        total_orders = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT COUNT(DISTINCT CustomerID) FROM Orders WHERE OrderDate BETWEEN ? AND ?",
            (self.date_filter_start, self.date_filter_end),
        )
        total_customers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Products")
        total_products = cursor.fetchone()[0]
        
        cursor.execute(
            """
            SELECT strftime('%Y-%m', o.OrderDate) as month, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount))
            FROM OrderDetails od JOIN Orders o ON od.OrderID = o.OrderID
            WHERE o.OrderDate BETWEEN ? AND ?
            GROUP BY month ORDER BY month
        """,
            (self.date_filter_start, self.date_filter_end),
        )
        sales_data_raw = cursor.fetchall()
        
        cursor.execute(
            """
            SELECT p.ProductName, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_revenue
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            JOIN Orders o ON od.OrderID = o.OrderID
            WHERE o.OrderDate BETWEEN ? AND ?
            GROUP BY p.ProductName
            ORDER BY total_revenue DESC
            LIMIT 5
        """,
            (self.date_filter_start, self.date_filter_end),
        )
        top_products_raw = cursor.fetchall()
        
        cursor.execute(
            """
            SELECT c.CategoryName, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_revenue
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            JOIN Categories c ON p.CategoryID = c.CategoryID
            JOIN Orders o ON od.OrderID = o.OrderID
            WHERE o.OrderDate BETWEEN ? AND ?
            GROUP BY c.CategoryName
            ORDER BY total_revenue DESC
        """,
            (self.date_filter_start, self.date_filter_end),
        )
        category_performance_raw = cursor.fetchall()
        
        cursor.execute(
            """
            SELECT c.CompanyName, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_revenue, COUNT(DISTINCT o.OrderID) as total_orders
            FROM Customers c
            JOIN Orders o ON c.CustomerID = o.CustomerID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            WHERE o.OrderDate BETWEEN ? AND ?
            GROUP BY c.CustomerID
            ORDER BY total_revenue DESC
            LIMIT 5
            """,
            (self.date_filter_start, self.date_filter_end),
        )
        top_customers_raw = cursor.fetchall()
        
        cursor.execute(
            """
            SELECT e.FirstName || ' ' || e.LastName as EmployeeName, 
                   SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_sales, 
                   COUNT(DISTINCT o.OrderID) as total_orders
            FROM Employees e
            JOIN Orders o ON e.EmployeeID = o.EmployeeID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            WHERE o.OrderDate BETWEEN ? AND ?
            GROUP BY EmployeeName
            ORDER BY total_sales DESC
            """,
            (self.date_filter_start, self.date_filter_end),
        )
        employee_performance_raw = cursor.fetchall()
        
        cursor.execute(
            """
            SELECT o.ShipCountry as country, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_sales
            FROM Orders o
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            WHERE o.OrderDate BETWEEN ? AND ?
            GROUP BY country
            ORDER BY total_sales DESC
            """,
            (self.date_filter_start, self.date_filter_end),
        )
        geo_sales_raw = cursor.fetchall()
        
        shipped_count = cursor.execute(
            "SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NOT NULL AND OrderDate BETWEEN ? AND ?",
            (self.date_filter_start, self.date_filter_end),
        ).fetchone()[0]
        pending_count = total_orders - shipped_count
        
        # Analytics charts data (sin filtros de fecha para mostrar datos históricos)
        cursor.execute("""
            SELECT
                strftime('%Y-%m', OrderDate) as month,
                COUNT(OrderID) as order_count
            FROM Orders
            GROUP BY month
            ORDER BY month;
        """)
        sales_over_time_data = cursor.fetchall()
        
        cursor.execute("""
            SELECT 
                p.ProductName as producto,
                SUM(od.Quantity) as cantidad
            FROM Products p
            JOIN OrderDetails od ON p.ProductID = od.ProductID
            GROUP BY p.ProductName
            ORDER BY cantidad DESC
            LIMIT 5
        """)
        top_products_analytics_data = cursor.fetchall()
        
        cursor.execute("""
            SELECT 
                c.Country as pais,
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as ventas
            FROM Customers c
            JOIN Orders o ON c.CustomerID = o.CustomerID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY c.Country
            ORDER BY ventas DESC
            LIMIT 10
        """)
        sales_by_country_data = cursor.fetchall()
        
        conn.close()
        
        async with self:
            # Actualizar KPIs
            self.kpis = [
                {
                    "title": "Total Revenue",
                    "value": f"${total_revenue:,.2f}",
                    "icon": "dollar-sign",
                    "color": "text-green-500",
                },
                {
                    "title": "Total Orders",
                    "value": str(total_orders),
                    "icon": "shopping-cart",
                    "color": "text-blue-500",
                },
                {
                    "title": "Total Customers",
                    "value": str(total_customers),
                    "icon": "users",
                    "color": "text-purple-500",
                },
                {
                    "title": "Total Products",
                    "value": str(total_products),
                    "icon": "package",
                    "color": "text-orange-500",
                },
            ]
            
            # Actualizar datos principales
            self.sales_data = [
                {
                    "month": datetime.strptime(row[0], "%Y-%m").strftime("%b"),
                    "sales": row[1],
                }
                for row in sales_data_raw
            ]
            
            self.top_products = [
                {"name": row[0], "revenue": row[1]} for row in top_products_raw
            ]
            
            self.category_performance = [
                {"category": row[0], "revenue": row[1]}
                for row in category_performance_raw
            ]
            
            self.top_customers = [
                {"name": row[0], "revenue": row[1], "orders": row[2]}
                for row in top_customers_raw
            ]
            
            self.employee_performance = [
                {"name": row[0], "sales": row[1], "orders": row[2]}
                for row in employee_performance_raw
            ]
            
            self.geo_sales = [
                {"country": row[0], "sales": row[1]} for row in geo_sales_raw
            ]
            
            self.order_statuses = [
                {"status": "Shipped", "count": shipped_count},
                {"status": "Pending", "count": pending_count},
                {
                    "status": "Delivered",
                    "count": random.randint(int(shipped_count * 0.8), shipped_count),
                },
            ]
            
            # Actualizar datos de analytics
            self.analytics_sales_over_time = [
                {
                    "month": row[0],
                    "ventas": row[1] or 0,
                }
                for row in sales_over_time_data
            ]
            
            self.analytics_top_products = [
                {
                    "producto": row[0],
                    "cantidad": row[1] or 0,
                }
                for row in top_products_analytics_data
            ]
            
            self.analytics_sales_by_country = [
                {
                    "pais": row[0],
                    "ventas": row[1] or 0,
                }
                for row in sales_by_country_data
            ]
        
        return