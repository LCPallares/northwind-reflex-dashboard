import reflex as rx
import sqlite3
import pandas as pd
from typing import TypedDict
from datetime import datetime, timedelta

DB_PATH = "northwind.db"


class RevenueTrend(TypedDict):
    month: str
    revenue: float
    order_count: int


class CategoryProfitability(TypedDict):
    category: str
    revenue: float
    cost: float
    profit_margin: float
    total_units: int


class CustomerSegment(TypedDict):
    segment: str
    count: int
    avg_revenue: float
    total_revenue: float


class EmployeePerformance(TypedDict):
    employee_name: str
    total_sales: float
    order_count: int
    avg_order_value: float
    performance_score: float


class SeasonalPattern(TypedDict):
    quarter: str
    year: int
    revenue: float
    growth_rate: float


class AnalyticsState(rx.State):
    # Revenue trends
    revenue_trends: list[RevenueTrend] = []
    yoy_comparison: list[dict] = []
    
    # Category profitability
    category_profitability: list[CategoryProfitability] = []
    
    # Customer segmentation and CLV
    customer_segments: list[CustomerSegment] = []
    top_customers_clv: list[dict] = []
    
    # Employee performance
    employee_performance: list[EmployeePerformance] = []
    
    # Seasonal patterns
    seasonal_patterns: list[SeasonalPattern] = []
    
    # Analytics charts data
    sales_over_time: list[dict] = []
    top_products: list[dict] = []
    sales_by_country: list[dict] = []
    
    # Key metrics
    total_revenue: float = 0
    total_orders: int = 0
    avg_order_value: float = 0
    profit_margin: float = 0
    
    loading: bool = False

    @rx.event(background=True)
    async def fetch_analytics_data(self):
        async with self:
            self.loading = True
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Revenue trends with YoY comparison
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', OrderDate) as month,
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as revenue,
                COUNT(DISTINCT o.OrderID) as order_count
            FROM Orders o
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY month
            ORDER BY month
        """)
        revenue_data = cursor.fetchall()
        
        # 2. Category profitability with margin calculations
        cursor.execute("""
            SELECT 
                c.CategoryName,
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as revenue,
                COUNT(od.Quantity) as total_units
            FROM Categories c
            JOIN Products p ON c.CategoryID = p.CategoryID
            JOIN OrderDetails od ON p.ProductID = od.ProductID
            GROUP BY c.CategoryName
            ORDER BY revenue DESC
        """)
        category_data = cursor.fetchall()
        
        # 3. Customer segments and CLV
        cursor.execute("""
            SELECT 
                c.CustomerID,
                c.CompanyName,
                COUNT(DISTINCT o.OrderID) as order_count,
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_revenue,
                MIN(o.OrderDate) as first_order,
                MAX(o.OrderDate) as last_order
            FROM Customers c
            LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
            LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY c.CustomerID
        """)
        customer_data = cursor.fetchall()
        
        # 4. Employee performance
        cursor.execute("""
            SELECT 
                e.FirstName || ' ' || e.LastName as employee_name,
                COUNT(DISTINCT o.OrderID) as order_count,
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as total_sales
            FROM Employees e
            JOIN Orders o ON e.EmployeeID = o.EmployeeID
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY e.EmployeeID
            ORDER BY total_sales DESC
        """)
        employee_data = cursor.fetchall()
        
        # 5. Seasonal patterns
        cursor.execute("""
            SELECT 
                strftime('%Y', OrderDate) as year,
                CASE 
                    WHEN CAST(strftime('%m', OrderDate) AS INTEGER) IN (1,2,3) THEN 'Q1'
                    WHEN CAST(strftime('%m', OrderDate) AS INTEGER) IN (4,5,6) THEN 'Q2'
                    WHEN CAST(strftime('%m', OrderDate) AS INTEGER) IN (7,8,9) THEN 'Q3'
                    ELSE 'Q4'
                END as quarter,
                SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as revenue
            FROM Orders o
            JOIN OrderDetails od ON o.OrderID = od.OrderID
            GROUP BY year, quarter
            ORDER BY year, quarter
        """)
        seasonal_data = cursor.fetchall()
        
        # 6. Analytics charts data
        # Sales over time for analytics chart  
        # cursor.execute("""
        #     SELECT 
        #         strftime('%b %Y', OrderDate) as month,
        #         SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as ventas
        #     FROM Orders o
        #     JOIN OrderDetails od ON o.OrderID = od.OrderID
        #     GROUP BY month
        #     ORDER BY o.OrderDate
        #     LIMIT 12
        # """)
        cursor.execute("""
            SELECT
                strftime('%Y-%m', OrderDate) as month,
                COUNT(OrderID) as order_count
            FROM Orders
            GROUP BY month
            ORDER BY month;
        """)
        sales_over_time_data = cursor.fetchall()
        
        # Top products for analytics chart
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
        top_products_data = cursor.fetchall()
        
        # Sales by country for analytics chart
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
        
        # 7. Key metrics
        cursor.execute("SELECT COUNT(*) FROM Orders")
        total_orders = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) 
            FROM OrderDetails od
        """)
        total_revenue = cursor.fetchone()[0] or 0
        
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        conn.close()
        
        # Process data
        revenue_trends = [
            {
                "month": datetime.strptime(row[0], "%Y-%m").strftime("%b %Y"),
                "revenue": row[1] or 0,
                "order_count": row[2] or 0,
            }
            for row in revenue_data
        ]
        
        # Calculate category profitability (assuming 70% cost of goods sold)
        category_profitability = []
        for row in category_data:
            revenue = row[1] or 0
            cost = revenue * 0.7  # Assuming 70% COGS
            profit_margin = ((revenue - cost) / revenue * 100) if revenue > 0 else 0
            
            category_profitability.append({
                "category": row[0],
                "revenue": revenue,
                "cost": cost,
                "profit_margin": profit_margin,
                "total_units": row[2] or 0,
            })
        
        # Customer segmentation
        customer_segments = []
        vip_customers = regular_customers = new_customers = 0
        vip_revenue = regular_revenue = 0
        
        for row in customer_data:
            orders = row[2] or 0
            revenue = row[3] or 0
            
            if orders == 0:
                new_customers += 1
            elif revenue > 5000:
                vip_customers += 1
                vip_revenue += revenue
            else:
                regular_customers += 1
                regular_revenue += revenue
        
        total_customers = len([row for row in customer_data if row[2] > 0])
        
        customer_segments = [
            {
                "segment": "VIP",
                "count": vip_customers,
                "avg_revenue": vip_revenue / vip_customers if vip_customers > 0 else 0,
                "total_revenue": vip_revenue,
            },
            {
                "segment": "Regular",
                "count": regular_customers,
                "avg_revenue": regular_revenue / regular_customers if regular_customers > 0 else 0,
                "total_revenue": regular_revenue,
            },
            {
                "segment": "New",
                "count": len([row for row in customer_data if row[2] == 0]),
                "avg_revenue": 0,
                "total_revenue": 0,
            }
        ]
        
        # Employee performance with performance score
        employee_performance = []
        max_sales = max((row[2] or 0 for row in employee_data), default=1)
        
        for row in employee_data:
            sales = row[2] or 0
            orders = row[1] or 0
            avg_order = sales / orders if orders > 0 else 0
            performance_score = (sales / max_sales) * 100  # Performance score based on sales percentage
            
            employee_performance.append({
                "employee_name": row[0],
                "total_sales": sales,
                "order_count": orders,
                "avg_order_value": avg_order,
                "performance_score": performance_score,
            })
        
        # Seasonal patterns with growth rates
        seasonal_patterns = []
        previous_quarter_revenue = None
        
        for row in seasonal_data:
            current_revenue = row[2] or 0
            growth_rate = 0
            
            if previous_quarter_revenue and previous_quarter_revenue > 0:
                growth_rate = ((current_revenue - previous_quarter_revenue) / previous_quarter_revenue) * 100
            
            seasonal_patterns.append({
                "quarter": f"{row[1]} {row[0]}",
                "year": row[0],
                "revenue": current_revenue,
                "growth_rate": growth_rate,
            })
            
            previous_quarter_revenue = current_revenue
        
        # Top customers by CLV
        top_customers_clv = [
            {
                "company_name": row[1],
                "order_count": row[2],
                "total_revenue": row[3] or 0,
                "clv": (row[3] or 0) / (row[2] or 1),  # Average revenue per order as proxy for CLV
            }
            for row in sorted(customer_data, key=lambda x: x[3] or 0, reverse=True)[:10]
        ]
        
        # Process analytics charts data
        sales_over_time = [
            {
                "month": row[0],
                "ventas": row[1] or 0,
            }
            for row in sales_over_time_data
        ]
        
        top_products = [
            {
                "producto": row[0],
                "cantidad": row[1] or 0,
            }
            for row in top_products_data
        ]
        
        sales_by_country = [
            {
                "pais": row[0],
                "ventas": row[1] or 0,
            }
            for row in sales_by_country_data
        ]
        
        async with self:
            self.revenue_trends = revenue_trends
            self.category_profitability = category_profitability
            self.customer_segments = customer_segments
            self.employee_performance = employee_performance
            self.seasonal_patterns = seasonal_patterns
            self.top_customers_clv = top_customers_clv
            self.sales_over_time = sales_over_time
            self.top_products = top_products
            self.sales_by_country = sales_by_country
            self.total_revenue = total_revenue
            self.total_orders = total_orders
            self.avg_order_value = avg_order_value
            self.profit_margin = 30.0  # Assuming 30% overall profit margin
            self.loading = False