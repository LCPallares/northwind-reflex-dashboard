import reflex as rx
import sqlite3
from typing import TypedDict, Optional
from datetime import datetime

DB_PATH = "northwind.db"


class Order(TypedDict):
    order_id: int
    customer_name: str
    employee_name: str
    order_date: str
    shipped_date: str | None
    status: str
    total_revenue: float


class OrderDetailItem(TypedDict):
    product_name: str
    unit_price: float
    quantity: int
    discount: float
    total: float


class DetailedOrder(Order):
    items: list[OrderDetailItem]
    freight: float
    ship_city: str
    ship_country: str


class OrderStats(TypedDict):
    total_orders: int
    average_order_value: float
    total_revenue: float
    shipped_orders: int
    pending_orders: int


class OrdersState(rx.State):
    orders: list[Order] = []
    selected_order: DetailedOrder | None = None
    is_modal_open: bool = False
    search_query: str = ""
    status_filter: str = "All"
    sort_by: str = "order_id"
    sort_order: str = "desc"
    current_page: int = 1
    items_per_page: int = 10
    total_orders: int = 0
    loading: bool = False
    stats: OrderStats = {
        "total_orders": 0,
        "average_order_value": 0.0,
        "total_revenue": 0.0,
        "shipped_orders": 0,
        "pending_orders": 0,
    }
    stats: OrderStats = {
        "total_orders": 0,
        "average_order_value": 0.0,
        "total_revenue": 0.0,
        "shipped_orders": 0,
        "pending_orders": 0,
    }

    @rx.var
    def total_pages(self) -> int:
        return -(-self.total_orders // self.items_per_page)

    @rx.event(background=True)
    async def fetch_orders(self):
        async with self:
            self.loading = True
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        base_query = """
            SELECT 
                o.OrderID as order_id, 
                c.CompanyName as customer_name, 
                (e.FirstName || ' ' || e.LastName) as employee_name,
                o.OrderDate as order_date, 
                o.ShippedDate as shipped_date, 
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_revenue
            FROM Orders o
            JOIN Customers c ON o.CustomerID = c.CustomerID
            JOIN Employees e ON o.EmployeeID = e.EmployeeID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
        """
        count_query = """
            SELECT COUNT(DISTINCT o.OrderID) FROM Orders o 
            JOIN Customers c ON o.CustomerID = c.CustomerID
            JOIN Employees e ON o.EmployeeID = e.EmployeeID
        """
        where_clauses = []
        params = []
        if self.search_query:
            search_term = f"%{self.search_query}%"
            where_clauses.append(
                " (o.OrderID LIKE ? OR c.CompanyName LIKE ? OR (e.FirstName || ' ' || e.LastName) LIKE ?) "
            )
            params.extend([search_term, search_term, search_term])
        if self.status_filter != "All":
            if self.status_filter == "Shipped":
                where_clauses.append(" o.ShippedDate IS NOT NULL ")
            else:
                where_clauses.append(" o.ShippedDate IS NULL ")
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)
            count_query += " WHERE " + " AND ".join(where_clauses)
        cursor.execute(count_query, params)
        total_orders = cursor.fetchone()[0]
        base_query += " GROUP BY o.OrderID "
        base_query += f" ORDER BY {self.sort_by} {self.sort_order.upper()} "
        offset = (self.current_page - 1) * self.items_per_page
        base_query += f" LIMIT {self.items_per_page} OFFSET {offset} "
        cursor.execute(base_query, params)
        orders_raw = cursor.fetchall()
        conn.close()
        async with self:
            self.total_orders = total_orders
            self.orders = [
                {
                    "order_id": row["order_id"],
                    "customer_name": row["customer_name"],
                    "employee_name": row["employee_name"],
                    "order_date": datetime.strptime(
                        row["order_date"].split(" ")[0], "%Y-%m-%d"
                    ).strftime("%b %d, %Y"),
                    "shipped_date": datetime.strptime(
                        row["shipped_date"].split(" ")[0], "%Y-%m-%d"
                    ).strftime("%b %d, %Y")
                    if row["shipped_date"]
                    else None,
                    "status": "Shipped" if row["shipped_date"] else "Pending",
                    "total_revenue": row["total_revenue"],
                }
                for row in orders_raw
            ]
            self.loading = False

    @rx.event(background=True)
    async def get_order_details(self, order_id: int):
        async with self:
            self.selected_order = None
            self.is_modal_open = True
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                o.OrderID as order_id, c.CompanyName as customer_name, (e.FirstName || ' ' || e.LastName) as employee_name,
                o.OrderDate as order_date, o.ShippedDate as shipped_date, o.Freight as freight,
                o.ShipCity as ship_city, o.ShipCountry as ship_country,
                p.ProductName as product_name, od.UnitPrice as unit_price, od.Quantity as quantity, od.Discount as discount
            FROM Orders o
            JOIN Customers c ON o.CustomerID = c.CustomerID
            JOIN Employees e ON o.EmployeeID = e.EmployeeID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE o.OrderID = ?
        """,
            (order_id,),
        )
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return
        order_items = []
        total_revenue = 0
        for row in rows:
            total = row["unit_price"] * row["quantity"] * (1 - row["discount"])
            order_items.append(
                {
                    "product_name": row["product_name"],
                    "unit_price": row["unit_price"],
                    "quantity": row["quantity"],
                    "discount": row["discount"],
                    "total": total,
                }
            )
            total_revenue += total
        first_row = rows[0]
        async with self:
            self.selected_order = {
                "order_id": first_row["order_id"],
                "customer_name": first_row["customer_name"],
                "employee_name": first_row["employee_name"],
                "order_date": datetime.strptime(
                    first_row["order_date"].split(" ")[0], "%Y-%m-%d"
                ).strftime("%b %d, %Y"),
                "shipped_date": datetime.strptime(
                    first_row["shipped_date"].split(" ")[0], "%Y-%m-%d"
                ).strftime("%b %d, %Y")
                if first_row["shipped_date"]
                else None,
                "status": "Shipped" if first_row["shipped_date"] else "Pending",
                "total_revenue": total_revenue,
                "items": order_items,
                "freight": first_row["freight"],
                "ship_city": first_row["ship_city"],
                "ship_country": first_row["ship_country"],
            }

    @rx.event
    def close_modal(self, open: bool):
        self.is_modal_open = open
        if not open:
            self.selected_order = None

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1
        return OrdersState.fetch_orders

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status
        self.current_page = 1
        return OrdersState.fetch_orders

    @rx.event
    def set_sort(self, column: str):
        if self.sort_by == column:
            self.sort_order = "asc" if self.sort_order == "desc" else "desc"
        else:
            self.sort_by = column
            self.sort_order = "asc"
        self.current_page = 1
        return OrdersState.fetch_orders

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            return OrdersState.fetch_orders

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            return OrdersState.fetch_orders

    @rx.event(background=True)
    async def fetch_stats(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total orders
        cursor.execute("SELECT COUNT(*) FROM Orders")
        total_orders = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute("""
            SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) 
            FROM OrderDetails od
        """)
        total_revenue = cursor.fetchone()[0] or 0
        
        # Average order value
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Shipped orders
        cursor.execute("SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NOT NULL")
        shipped_orders = cursor.fetchone()[0]
        
        # Pending orders
        cursor.execute("SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NULL")
        pending_orders = cursor.fetchone()[0]
        
        conn.close()
        
        async with self:
            self.stats = {
                "total_orders": total_orders,
                "average_order_value": avg_order_value,
                "total_revenue": total_revenue,
                "shipped_orders": shipped_orders,
                "pending_orders": pending_orders,
            }