'''# src/dao/order_dao.py
from typing import List, Dict, Optional


class Order:
    def __init__(self, order_id: int, customer_email: str, items: List[Dict]):
        self.order_id = order_id
        self.customer_email = customer_email
        self.items = items  # list of {"prod_id": int, "quantity": int}
        self.status = "Pending"  # Pending, Cancelled, Completed


class OrderDAO:
    """In-memory DAO for orders"""

    def __init__(self):
        self._orders: List[Order] = []
        self._next_id = 1

    def insert_order(self, customer_email: str, items: List[Dict]) -> Order:
        order = Order(order_id=self._next_id, customer_email=customer_email, items=items)
        self._orders.append(order)
        self._next_id += 1
        return order

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        for o in self._orders:
            if o.order_id == order_id:
                return o
        return None

    def update_order(self, order: Order) -> Order:
        for idx, o in enumerate(self._orders):
            if o.order_id == order.order_id:
                self._orders[idx] = order
                return order
        return order

    def list_orders(self) -> List[Order]:
        return self._orders
'''

'''# src/dao/order_dao.py
from typing import List, Dict, Optional
from src.dao.product_dao import ProductDAO, Product
from src.dao.customer_dao import CustomerDAO, Customer


class Order:
    def __init__(self, order_id: int, customer_email: str, items: List[Dict], total_amount: float):
        self.order_id = order_id
        self.customer_email = customer_email
        self.items = items  # [{"prod_id": int, "quantity": int, "price": float}]
        self.total_amount = total_amount
        self.status = "PLACED"  # PLACED, CANCELLED, COMPLETED


class OrderDAO:
    """In-memory DAO for Orders"""

    def __init__(self):
        self._orders: List[Order] = []
        self._next_id = 1

    def insert_order(self, customer_email: str, items: List[Dict], total_amount: float) -> Order:
        order = Order(order_id=self._next_id, customer_email=customer_email, items=items, total_amount=total_amount)
        self._orders.append(order)
        self._next_id += 1
        return order

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        for o in self._orders:
            if o.order_id == order_id:
                return o
        return None

    def update_order(self, order: Order) -> Order:
        for idx, o in enumerate(self._orders):
            if o.order_id == order.order_id:
                self._orders[idx] = order
                return order
        return order

    def list_orders_by_customer(self, customer_email: str) -> List[Order]:
        return [o for o in self._orders if o.customer_email == customer_email]

    def list_orders(self) -> List[Order]:
        return self._orders
'''

'''# src/dao/order_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

class Order:
    def __init__(self, order_id: int, customer_email: str, items: List[Dict], total_amount: float, status: str = "PLACED"):
        self.order_id = order_id
        self.customer_email = customer_email
        self.items = items
        self.total_amount = total_amount
        self.status = status

class OrderDAO:
    def __init__(self):
        self._sb = get_supabase()
        self._orders_table = "orders"
        self._order_items_table = "order_items"

    def insert_order(self, customer_email: str, items: List[Dict], total_amount: float) -> Order:
        # Insert into orders table
        order_payload = {
            "customer_email": customer_email,
            "total_amount": total_amount,
            "status": "PLACED"
        }
        resp = self._sb.table(self._orders_table).insert(order_payload).execute()
        if not resp.data:
            raise Exception("Failed to insert order")

        # Get generated order_id
        order_id = resp.data[0]["order_id"]

        # Insert order items
        for item in items:
            item_payload = {
                "order_id": order_id,
                "prod_id": item["prod_id"],
                "quantity": item["quantity"],
                "price": item["price"]
            }
            self._sb.table(self._order_items_table).insert(item_payload).execute()

        return Order(order_id, customer_email, items, total_amount)

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        resp = self._sb.table(self._orders_table).select("*").eq("order_id", order_id).limit(1).execute()
        if not resp.data:
            return None

        order_data = resp.data[0]
        # Fetch order items
        items_resp = self._sb.table(self._order_items_table).select("*").eq("order_id", order_id).execute()
        items = items_resp.data or []

        return Order(
            order_id=order_data["order_id"],
            customer_email=order_data["customer_email"],
            items=items,
            total_amount=order_data["total_amount"],
            status=order_data["status"]
        )

    def list_orders_by_customer(self, customer_email: str) -> List[Order]:
        resp = self._sb.table(self._orders_table).select("*").eq("customer_email", customer_email).execute()
        orders = []
        for order_data in resp.data:
            items_resp = self._sb.table(self._order_items_table).select("*").eq("order_id", order_data["order_id"]).execute()
            items = items_resp.data or []
            orders.append(Order(order_data["order_id"], customer_email, items, order_data["total_amount"], order_data["status"]))
        return orders

    def update_order(self, order: Order) -> None:
        self._sb.table(self._orders_table).update({
            "status": order.status,
            "total_amount": order.total_amount
        }).eq("order_id", order.order_id).execute()
'''

# src/dao/order_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase


class Order:
    def __init__(self, order_id: int, customer_id: int, items: List[Dict], total_amount: float, status: str = "PLACED"):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.total_amount = total_amount
        self.status = status


class OrderDAO:
    def __init__(self):
        self._sb = get_supabase()
        self._orders_table = "orders"
        self._order_items_table = "order_items"

    def insert_order(self, customer_id: int, items: List[Dict], total_amount: float) -> Order:
        # Insert into orders table
        order_payload = {
            "customer_id": customer_id,
            "total_amount": total_amount,
            "status": "PLACED"
        }
        resp = self._sb.table(self._orders_table).insert(order_payload).execute()
        if not resp.data:
            raise Exception("Failed to insert order")

        # Get generated order_id
        order_id = resp.data[0]["id"]  # assuming PK column is "id"

        # Insert order items
        for item in items:
            item_payload = {
                "order_id": order_id,
                "prod_id": item["prod_id"],
                "quantity": item["quantity"],
                "price": item["price"]
            }
            self._sb.table(self._order_items_table).insert(item_payload).execute()

        return Order(order_id, customer_id, items, total_amount)

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        resp = self._sb.table(self._orders_table).select("*").eq("id", order_id).limit(1).execute()
        if not resp.data:
            return None

        order_data = resp.data[0]
        # Fetch order items
        items_resp = self._sb.table(self._order_items_table).select("*").eq("order_id", order_id).execute()
        items = items_resp.data or []

        return Order(
            order_id=order_data["id"],
            customer_id=order_data["customer_id"],
            items=items,
            total_amount=order_data["total_amount"],
            status=order_data["status"]
        )

    def list_orders_by_customer(self, customer_id: int) -> List[Order]:
        resp = self._sb.table(self._orders_table).select("*").eq("customer_id", customer_id).execute()
        orders = []
        for order_data in resp.data:
            items_resp = self._sb.table(self._order_items_table).select("*").eq("order_id", order_data["id"]).execute()
            items = items_resp.data or []
            orders.append(Order(order_data["id"], customer_id, items, order_data["total_amount"], order_data["status"]))
        return orders

    def update_order(self, order: Order) -> None:
        self._sb.table(self._orders_table).update({
            "status": order.status,
            "total_amount": order.total_amount
        }).eq("id", order.order_id).execute()
