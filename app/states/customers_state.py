import reflex as rx
import sqlite3
from typing import TypedDict, Optional
from datetime import datetime, timedelta

DB_PATH = "northwind.db"


class Customer(TypedDict):
    customer_id: str
    company_name: str
    contact_name: str
    city: str
    country: str
    total_orders: int
    total_revenue: float
    last_order_date: str
    customer_segment: str


class CustomerOrder(TypedDict):
    order_id: int
    order_date: str
    shipped_date: str | None
    total_amount: float
    status: str


class CustomerStats(TypedDict):
    total_customers: int
    total_revenue: float
    avg_revenue_per_customer: float
    vip_customers: int
    new_customers: int
    countries_served: int


class CustomersState(rx.State):
    customers: list[Customer] = []
    selected_customer: Customer | None = None
    customer_orders: list[CustomerOrder] = []
    is_modal_open: bool = False
    search_query: str = ""
    country_filter: str = "All"
    city_filter: str = "All"
    segment_filter: str = "All"
    sort_by: str = "company_name"
    sort_order: str = "asc"
    current_page: int = 1
    items_per_page: int = 12
    total_customers: int = 0
    loading: bool = False
    stats: CustomerStats = {
        "total_customers": 0,
        "total_revenue": 0.0,
        "avg_revenue_per_customer": 0.0,
        "vip_customers": 0,
        "new_customers": 0,
        "countries_served": 0,
    }
    countries: list[str] = []
    cities: list[str] = []

    @rx.var
    def total_pages(self) -> int:
        return -(-self.total_customers // self.items_per_page)

    @rx.var
    def filtered_customers(self) -> list[Customer]:
        filtered = self.customers
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                c for c in filtered
                if query in c["company_name"].lower()
                or query in c["contact_name"].lower()
                or query in c["city"].lower()
                or query in c["country"].lower()
            ]
        if self.country_filter != "All":
            filtered = [c for c in filtered if c["country"] == self.country_filter]
        if self.city_filter != "All":
            filtered = [c for c in filtered if c["city"] == self.city_filter]
        if self.segment_filter != "All":
            filtered = [c for c in filtered if c["customer_segment"] == self.segment_filter]
        
        reverse = self.sort_order == "desc"
        filtered.sort(key=lambda x: x[self.sort_by], reverse=reverse)
        
        return filtered

    @rx.event(background=True)
    async def fetch_customers(self):
        async with self:
            self.loading = True
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                c.CustomerID as customer_id,
                c.CompanyName as company_name,
                c.ContactName as contact_name,
                c.City as city,
                c.Country as country,
                COUNT(DISTINCT o.OrderID) as total_orders,
                COALESCE(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 0) as total_revenue,
                MAX(o.OrderDate) as last_order_date
            FROM Customers c
            LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
            LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY c.CustomerID
            ORDER BY c.CompanyName
        """)
        
        customers_raw = cursor.fetchall()
        
        # Get unique countries and cities
        cursor.execute("SELECT DISTINCT Country FROM Customers ORDER BY Country")
        countries_raw = cursor.fetchall()
        cursor.execute("SELECT DISTINCT City FROM Customers ORDER BY City")
        cities_raw = cursor.fetchall()
        
        conn.close()
        
        customers = []
        for row in customers_raw:
            total_revenue = row["total_revenue"] or 0
            total_orders = row["total_orders"] or 0
            
            # Customer segmentation logic
            if total_orders == 0:
                segment = "New"
            elif total_revenue > 5000:
                segment = "VIP"
            else:
                segment = "Regular"
            
            last_order = row["last_order_date"]
            if last_order:
                last_order_date = datetime.strptime(last_order.split(" ")[0], "%Y-%m-%d").strftime("%b %d, %Y")
            else:
                last_order_date = "Never"
                
            customers.append({
                "customer_id": row["customer_id"],
                "company_name": row["company_name"],
                "contact_name": row["contact_name"],
                "city": row["city"],
                "country": row["country"],
                "total_orders": total_orders,
                "total_revenue": total_revenue,
                "last_order_date": last_order_date,
                "customer_segment": segment,
            })
        
        countries = ["All"] + [country[0] for country in countries_raw]
        cities = ["All"] + [city[0] for city in cities_raw]
        
        async with self:
            self.customers = customers
            self.countries = countries
            self.cities = cities
            self.total_customers = len(customers)
            self.loading = False

    @rx.event(background=True)
    async def fetch_stats(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total customers
        cursor.execute("SELECT COUNT(*) FROM Customers")
        total_customers = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute("""
            SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) 
            FROM OrderDetails od
        """)
        total_revenue = cursor.fetchone()[0] or 0
        
        # Average revenue per customer
        avg_revenue = total_revenue / total_customers if total_customers > 0 else 0
        
        # VIP customers (revenue > 5000)
        cursor.execute("""
            SELECT COUNT(DISTINCT c.CustomerID)
            FROM Customers c
            JOIN Orders o ON c.CustomerID = o.CustomerID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY c.CustomerID
            HAVING SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) > 5000
        """)
        vip_customers = len(cursor.fetchall())
        
        # New customers (no orders)
        cursor.execute("""
            SELECT COUNT(*) FROM Customers c
            LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
            WHERE o.OrderID IS NULL
        """)
        new_customers = cursor.fetchone()[0]
        
        # Countries served
        cursor.execute("SELECT COUNT(DISTINCT Country) FROM Customers")
        countries_served = cursor.fetchone()[0]
        
        conn.close()
        
        async with self:
            self.stats = {
                "total_customers": total_customers,
                "total_revenue": total_revenue,
                "avg_revenue_per_customer": avg_revenue,
                "vip_customers": vip_customers,
                "new_customers": new_customers,
                "countries_served": countries_served,
            }

    @rx.event(background=True)
    async def get_customer_details(self, customer_id: str):
        async with self:
            self.selected_customer = None
            self.customer_orders = []
            self.is_modal_open = True
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get customer details
        cursor.execute("""
            SELECT 
                c.CustomerID as customer_id,
                c.CompanyName as company_name,
                c.ContactName as contact_name,
                c.City as city,
                c.Country as country
            FROM Customers c
            WHERE c.CustomerID = ?
        """, (customer_id,))
        
        customer_row = cursor.fetchone()
        
        if customer_row:
            # Get customer orders
            cursor.execute("""
                SELECT 
                    o.OrderID as order_id,
                    o.OrderDate as order_date,
                    o.ShippedDate as shipped_date,
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_amount
                FROM Orders o
                JOIN OrderDetails od ON o.OrderID = od.OrderID
                WHERE o.CustomerID = ?
                GROUP BY o.OrderID
                ORDER BY o.OrderDate DESC
            """, (customer_id,))
            
            orders_raw = cursor.fetchall()
            
            customer_orders = []
            for order_row in orders_raw:
                order_date = datetime.strptime(order_row["order_date"].split(" ")[0], "%Y-%m-%d").strftime("%b %d, %Y")
                shipped_date = None
                if order_row["shipped_date"]:
                    shipped_date = datetime.strptime(order_row["shipped_date"].split(" ")[0], "%Y-%m-%d").strftime("%b %d, %Y")
                
                status = "Shipped" if order_row["shipped_date"] else "Pending"
                
                customer_orders.append({
                    "order_id": order_row["order_id"],
                    "order_date": order_date,
                    "shipped_date": shipped_date,
                    "total_amount": order_row["total_amount"] or 0,
                    "status": status,
                })
            
            async with self:
                self.selected_customer = {
                    "customer_id": customer_row["customer_id"],
                    "company_name": customer_row["company_name"],
                    "contact_name": customer_row["contact_name"],
                    "city": customer_row["city"],
                    "country": customer_row["country"],
                }
                self.customer_orders = customer_orders
        
        conn.close()

    @rx.event
    def close_modal(self, open: bool):
        self.is_modal_open = open
        if not open:
            self.selected_customer = None
            self.customer_orders = []

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1

    @rx.event
    def set_country_filter(self, country: str):
        self.country_filter = country
        self.city_filter = "All"  # Reset city filter when country changes
        self.current_page = 1

    @rx.event
    def set_city_filter(self, city: str):
        self.city_filter = city
        self.current_page = 1

    @rx.event
    def set_segment_filter(self, segment: str):
        self.segment_filter = segment
        self.current_page = 1

    @rx.event
    def set_sort(self, column: str):
        if self.sort_by == column:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_by = column
            self.sort_order = "asc"

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.var
    def paginated_customers(self) -> list[Customer]:
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_customers[start:end]