import reflex as rx
import sqlite3
import pandas as pd

DB_PATH = "northwind.db"

class AnalyticsState(rx.State):
    """
    Estado para manejar la lógica de la página de análisis.
    """
    
    sales_over_time: list = []
    top_products: list = []
    sales_by_country: list = []

    def _execute_query(self, query: str) -> pd.DataFrame:
        """Ejecuta una consulta SQL y devuelve un DataFrame de pandas."""
        with sqlite3.connect(DB_PATH) as con:
            return pd.read_sql_query(query, con)

    #@rx.background
    @rx.event(background=True)
    async def fetch_analytics_data(self):
        """
        Obtiene todos los datos de análisis de forma asíncrona.
        """
        # Obtener ventas a lo largo del tiempo
        query_sales_time = """
            SELECT
                strftime('%Y-%m', OrderDate) as month,
                COUNT(OrderID) as order_count
            FROM Orders
            GROUP BY month
            ORDER BY month;
        """
        df_sales_time = self._execute_query(query_sales_time)
        async with self:
            self.sales_over_time = df_sales_time.rename(columns={'order_count': 'ventas'}).to_dict(orient='records')

        # Obtener top 5 productos
        query_top_products = """
            SELECT
                p.ProductName,
                SUM(od.Quantity) as total_quantity
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            GROUP BY p.ProductName
            ORDER BY total_quantity DESC
            LIMIT 5;
        """
        df_top_products = self._execute_query(query_top_products)
        async with self:
            self.top_products = df_top_products.rename(columns={'ProductName': 'producto', 'total_quantity': 'cantidad'}).to_dict(orient='records')

        # Obtener ventas por país
        query_sales_country = """
            SELECT
                c.Country,
                SUM(od.Quantity * od.UnitPrice) as total_sales
            FROM Orders o
            JOIN Customers c ON o.CustomerID = c.CustomerID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY c.Country
            ORDER BY total_sales DESC;
        """
        df_sales_country = self._execute_query(query_sales_country)
        async with self:
            self.sales_by_country = df_sales_country.head(10).rename(columns={'Country': 'pais', 'total_sales': 'ventas'}).to_dict(orient='records')

