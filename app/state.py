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


def setup_database():
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 1024 * 10:
        return
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tables = [
        "OrderDetails",
        "Orders",
        "Products",
        "Categories",
        "Customers",
        "Employees",
        "Shippers",
        "Suppliers",
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    cursor.execute(
        "CREATE TABLE Categories (CategoryID INTEGER PRIMARY KEY, CategoryName TEXT, Description TEXT)"
    )
    cursor.execute(
        "CREATE TABLE Customers (CustomerID TEXT PRIMARY KEY, CompanyName TEXT, ContactName TEXT, City TEXT, Country TEXT)"
    )
    cursor.execute(
        "CREATE TABLE Employees (EmployeeID INTEGER PRIMARY KEY, LastName TEXT, FirstName TEXT, Title TEXT, BirthDate TEXT, City TEXT, Country TEXT)"
    )
    cursor.execute(
        "CREATE TABLE Shippers (ShipperID INTEGER PRIMARY KEY, CompanyName TEXT, Phone TEXT)"
    )
    cursor.execute(
        "CREATE TABLE Suppliers (SupplierID INTEGER PRIMARY KEY, CompanyName TEXT, ContactName TEXT, City TEXT, Country TEXT)"
    )
    cursor.execute(
        "CREATE TABLE Products (ProductID INTEGER PRIMARY KEY, ProductName TEXT, SupplierID INTEGER, CategoryID INTEGER, UnitPrice REAL, UnitsInStock INTEGER, FOREIGN KEY(SupplierID) REFERENCES Suppliers(SupplierID), FOREIGN KEY(CategoryID) REFERENCES Categories(CategoryID))"
    )
    cursor.execute(
        "CREATE TABLE Orders (OrderID INTEGER PRIMARY KEY, CustomerID TEXT, EmployeeID INTEGER, OrderDate TEXT, RequiredDate TEXT, ShippedDate TEXT, ShipVia INTEGER, Freight REAL, ShipCity TEXT, ShipCountry TEXT, FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID), FOREIGN KEY(EmployeeID) REFERENCES Employees(EmployeeID), FOREIGN KEY(ShipVia) REFERENCES Shippers(ShipperID))"
    )
    cursor.execute(
        "CREATE TABLE OrderDetails (OrderID INTEGER, ProductID INTEGER, UnitPrice REAL, Quantity INTEGER, Discount REAL, PRIMARY KEY (OrderID, ProductID), FOREIGN KEY(OrderID) REFERENCES Orders(OrderID), FOREIGN KEY(ProductID) REFERENCES Products(ProductID))"
    )
    categories = [
        (1, "Beverages", "Soft drinks, coffees, teas"),
        (2, "Condiments", "Sweet and savory sauces"),
        (3, "Confections", "Desserts, candies, and sweet breads"),
        (4, "Dairy Products", "Cheeses"),
        (5, "Grains/Cereals", "Breads, crackers, pasta"),
        (6, "Meat/Poultry", "Prepared meats"),
        (7, "Produce", "Dried fruit and bean curd"),
        (8, "Seafood", "Seaweed and fish"),
    ]
    cursor.executemany("INSERT INTO Categories VALUES (?, ?, ?)", categories)
    customers = [
        ("ALFKI", "Alfreds Futterkiste", "Maria Anders", "Berlin", "Germany"),
        ("ANATR", "Ana Trujillo Emparedados", "Ana Trujillo", "México D.F.", "Mexico"),
        ("ANTON", "Antonio Moreno Taquería", "Antonio Moreno", "México D.F.", "Mexico"),
        ("BERGS", "Berglunds snabbköp", "Christina Berglund", "Luleå", "Sweden"),
        ("BLAUS", "Blauer See Delikatessen", "Hanna Moos", "Mannheim", "Germany"),
        ("BONAP", "Bon app", "Laurence Lebihan", "Marseille", "France"),
        ("BOTTM", "Bottom-Dollar Markets", "Elizabeth Lincoln", "Tsawassen", "Canada"),
        ("BSBEV", "Bs Beverages", "Victoria Ashworth", "London", "UK"),
        (
            "CACTU",
            "Cactus Comidas para llevar",
            "Patricio Simpson",
            "Buenos Aires",
            "Argentina",
        ),
        (
            "CENTC",
            "Centro comercial Moctezuma",
            "Francisco Chang",
            "México D.F.",
            "Mexico",
        ),
    ]
    cursor.executemany("INSERT INTO Customers VALUES (?, ?, ?, ?, ?)", customers)
    employees = [
        (1, "Davolio", "Nancy", "Sales Rep", "1948-12-08", "Seattle", "USA"),
        (2, "Fuller", "Andrew", "VP Sales", "1952-02-19", "Tacoma", "USA"),
        (3, "Leverling", "Janet", "Sales Rep", "1963-08-30", "Kirkland", "USA"),
        (4, "Peacock", "Margaret", "Sales Rep", "1937-09-19", "Redmond", "USA"),
        (5, "Buchanan", "Steven", "Sales Manager", "1955-03-04", "London", "UK"),
    ]
    cursor.executemany("INSERT INTO Employees VALUES (?, ?, ?, ?, ?, ?, ?)", employees)
    shippers = [
        (1, "Speedy Express", "(503) 555-9831"),
        (2, "United Package", "(503) 555-3199"),
        (3, "Federal Shipping", "(503) 555-9931"),
    ]
    cursor.executemany("INSERT INTO Shippers VALUES (?, ?, ?)", shippers)
    suppliers = [
        (1, "Exotic Liquids", "Charlotte Cooper", "London", "UK"),
        (2, "New Orleans Cajun Delights", "Shelley Burke", "New Orleans", "USA"),
        (3, "Grandma Kellys Homestead", "Regina Murphy", "Ann Arbor", "USA"),
        (4, "Tokyo Traders", "Yoshi Nagase", "Tokyo", "Japan"),
        (5, "Cooperativa de Quesos", "Antonio del Valle", "Oviedo", "Spain"),
    ]
    cursor.executemany("INSERT INTO Suppliers VALUES (?, ?, ?, ?, ?)", suppliers)
    products = [
        (1, "Chai", 1, 1, 18, 39),
        (2, "Chang", 1, 1, 19, 17),
        (3, "Aniseed Syrup", 1, 2, 10, 13),
        (4, "Chef Antons Cajun Seasoning", 2, 2, 22, 53),
        (5, "Chef Antons Gumbo Mix", 2, 2, 21.35, 0),
        (6, "Grandmas Boysenberry Spread", 3, 2, 25, 120),
        (7, "Uncle Bobs Organic Dried Pears", 3, 7, 30, 15),
        (8, "Northwoods Cranberry Sauce", 3, 2, 40, 6),
        (9, "Mishi Kobe Niku", 4, 6, 97, 29),
        (10, "Ikura", 4, 8, 31, 31),
        (11, "Queso Cabrales", 5, 4, 21, 22),
        (12, "Queso Manchego La Pastora", 5, 4, 38, 86),
    ]
    cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?, ?, ?)", products)
    orders, order_details = ([], [])
    customer_ids = [c[0] for c in customers]
    employee_ids = [e[0] for e in employees]
    product_ids_prices = {p[0]: p[4] for p in products}
    for i in range(100):
        order_id = 10248 + i
        order_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364))
        required_date = order_date + timedelta(days=random.randint(10, 30))
        shipped_date = order_date + timedelta(days=random.randint(2, 9))
        orders.append(
            (
                order_id,
                random.choice(customer_ids),
                random.choice(employee_ids),
                order_date.strftime("%Y-%m-%d"),
                required_date.strftime("%Y-%m-%d"),
                shipped_date.strftime("%Y-%m-%d"),
                random.randint(1, 3),
                random.uniform(10, 200),
                "SomeCity",
                "SomeCountry",
            )
        )
        num_products_in_order = random.randint(1, 5)
        for _ in range(num_products_in_order):
            product_id = random.choice(list(product_ids_prices.keys()))
            unit_price = product_ids_prices[product_id]
            quantity = random.randint(1, 20)
            discount = random.choice([0, 0.05, 0.1, 0.15])
            if not any(
                (od[0] == order_id and od[1] == product_id for od in order_details)
            ):
                order_details.append(
                    (order_id, product_id, unit_price, quantity, discount)
                )
    cursor.executemany(
        "INSERT INTO Orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", orders
    )
    cursor.executemany(
        "INSERT INTO OrderDetails VALUES (?, ?, ?, ?, ?)", order_details
    )
    conn.commit()
    conn.close()


setup_database()


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
        conn.close()
        async with self:
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
        return