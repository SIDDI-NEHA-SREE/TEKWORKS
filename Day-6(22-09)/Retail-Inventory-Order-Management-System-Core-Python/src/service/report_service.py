# src/service/report_service.py
from src.dao.order_dao import OrderDAO
from src.dao.product_dao import ProductDAO
from src.dao.customer_dao import CustomerDAO

class ReportService:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.product_dao = ProductDAO()
        self.customer_dao = CustomerDAO()

    def top_selling_products(self, top_n: int = 5):
        all_orders = self.order_dao.list_orders()  # each order has order_items [{prod_id, quantity}]
        product_count = {}
        for order in all_orders:
            for item in order.items:
                product_count[item["prod_id"]] = product_count.get(item["prod_id"], 0) + item["quantity"]
        sorted_products = sorted(product_count.items(), key=lambda x: x[1], reverse=True)
        result = []
        for prod_id, qty in sorted_products[:top_n]:
            product = self.product_dao.get_product_by_id(prod_id)
            if product:
                result.append({"product": product.name, "quantity_sold": qty})
        return result

    def total_revenue_last_month(self):
        from datetime import datetime, timedelta
        import calendar

        today = datetime.today()
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        all_orders = self.order_dao.list_orders()
        total = sum(o.total_amount for o in all_orders 
                    if first_day_last_month <= o.created_at <= last_day_last_month)
        return total

    def orders_by_customer(self):
        all_orders = self.order_dao.list_orders()
        customer_count = {}
        for order in all_orders:
            cid = order.customer_id
            customer_count[cid] = customer_count.get(cid, 0) + 1
        return customer_count

    def frequent_customers(self, min_orders: int = 2):
        counts = self.orders_by_customer()
        frequent = []
        for cid, count in counts.items():
            if count > min_orders:
                customer = self.customer_dao.get_customer_by_id(cid)
                if customer:
                    frequent.append({"customer": customer.name, "email": customer.email, "orders": count})
        return frequent
