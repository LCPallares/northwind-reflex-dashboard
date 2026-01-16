import reflex as rx
import sqlite3
from typing import TypedDict, Optional

DB_PATH = "northwind.db"


class Product(TypedDict):
    product_id: int
    product_name: str
    category_name: str
    supplier_name: str
    unit_price: float
    units_in_stock: int
    inventory_status: str


class ProductStats(TypedDict):
    total_products: int
    total_inventory_value: float
    low_stock_products: int
    out_of_stock_products: int
    categories_count: int


class ProductsState(rx.State):
    products: list[Product] = []
    search_query: str = ""
    category_filter: str = "All"
    sort_by: str = "product_name"
    sort_order: str = "asc"
    view_mode: str = "grid"  # "grid" or "list"
    current_page: int = 1
    items_per_page: int = 12
    total_products: int = 0
    loading: bool = False
    stats: ProductStats = {
        "total_products": 0,
        "total_inventory_value": 0.0,
        "low_stock_products": 0,
        "out_of_stock_products": 0,
        "categories_count": 0,
    }
    categories: list[str] = []

    @rx.var
    def total_pages(self) -> int:
        return -(-self.total_products // self.items_per_page)

    @rx.var
    def filtered_products(self) -> list[Product]:
        filtered = self.products
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                p for p in filtered
                if query in p["product_name"].lower() 
                or query in p["category_name"].lower()
                or query in p["supplier_name"].lower()
            ]
        if self.category_filter != "All":
            filtered = [p for p in filtered if p["category_name"] == self.category_filter]
        
        # Sorting
        reverse = self.sort_order == "desc"
        filtered.sort(key=lambda x: x[self.sort_by], reverse=reverse)
        
        return filtered

    @rx.event(background=True)
    async def fetch_products(self):
        async with self:
            self.loading = True
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                p.ProductID as product_id,
                p.ProductName as product_name,
                c.CategoryName as category_name,
                s.CompanyName as supplier_name,
                p.UnitPrice as unit_price,
                p.UnitsInStock as units_in_stock
            FROM Products p
            LEFT JOIN Categories c ON p.CategoryID = c.CategoryID
            LEFT JOIN Suppliers s ON p.SupplierID = s.SupplierID
            ORDER BY p.ProductName
        """)
        
        products_raw = cursor.fetchall()
        
        # Get categories
        cursor.execute("SELECT DISTINCT CategoryName FROM Categories ORDER BY CategoryName")
        categories_raw = cursor.fetchall()
        
        conn.close()
        
        products = []
        for row in products_raw:
            units_in_stock = row["units_in_stock"] or 0
            if units_in_stock == 0:
                inventory_status = "Out of Stock"
            elif units_in_stock < 10:
                inventory_status = "Low Stock"
            else:
                inventory_status = "In Stock"
                
            products.append({
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "category_name": row["category_name"] or "Uncategorized",
                "supplier_name": row["supplier_name"] or "Unknown",
                "unit_price": row["unit_price"] or 0,
                "units_in_stock": units_in_stock,
                "inventory_status": inventory_status,
            })
        
        categories = ["All"] + [cat[0] for cat in categories_raw]
        
        async with self:
            self.products = products
            self.categories = categories
            self.total_products = len(products)
            self.loading = False

    @rx.event(background=True)
    async def fetch_stats(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total products
        cursor.execute("SELECT COUNT(*) FROM Products")
        total_products = cursor.fetchone()[0]
        
        # Total inventory value
        cursor.execute("""
            SELECT SUM(p.UnitPrice * p.UnitsInStock) 
            FROM Products p
        """)
        total_inventory_value = cursor.fetchone()[0] or 0
        
        # Low stock (less than 10 units)
        cursor.execute("SELECT COUNT(*) FROM Products WHERE UnitsInStock < 10 AND UnitsInStock > 0")
        low_stock_products = cursor.fetchone()[0]
        
        # Out of stock
        cursor.execute("SELECT COUNT(*) FROM Products WHERE UnitsInStock = 0")
        out_of_stock_products = cursor.fetchone()[0]
        
        # Categories count
        cursor.execute("SELECT COUNT(*) FROM Categories")
        categories_count = cursor.fetchone()[0]
        
        conn.close()
        
        async with self:
            self.stats = {
                "total_products": total_products,
                "total_inventory_value": total_inventory_value,
                "low_stock_products": low_stock_products,
                "out_of_stock_products": out_of_stock_products,
                "categories_count": categories_count,
            }

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1

    @rx.event
    def set_category_filter(self, category: str):
        self.category_filter = category
        self.current_page = 1

    @rx.event
    def set_sort(self, column: str):
        if self.sort_by == column:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_by = column
            self.sort_order = "asc"

    @rx.event
    def set_view_mode(self, mode: str):
        self.view_mode = mode

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.var
    def paginated_products(self) -> list[Product]:
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_products[start:end]