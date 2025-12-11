'''# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDAO, Order
from src.service.customer_service import CustomerService, CustomerError



class OrderError(Exception):
    """Custom exception for order-related errors"""
    pass


class OrderService:
    """Business logic layer for managing orders"""

    def __init__(self, order_dao: OrderDAO = None, customer_service: CustomerService = None):
        self.dao = order_dao or OrderDAO()
        self.customer_service = customer_service or CustomerService()

    def create_order(self, customer_email: str, items: List[Dict]) -> Order:
        # Validate customer exists
        customer = self.customer_service.dao.get_customer_by_email(customer_email)
        if not customer:
            raise OrderError(f"Customer '{customer_email}' does not exist.")

        if not items or not all("prod_id" in item and "quantity" in item for item in items):
            raise OrderError("Order items are invalid or empty.")

        # Create order
        order = self.dao.insert_order(customer_email, items)
        # Link order to customer
        customer.orders.append(order.order_id)
        return order

    def get_order_details(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order '{order_id}' not found.")
        return order

    def cancel_order(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order '{order_id}' not found.")
        if order.status == "Cancelled":
            raise OrderError(f"Order '{order_id}' is already cancelled.")

        order.status = "Cancelled"
        self.dao.update_order(order)

        # Remove from customer orders list
        customer = self.customer_service.dao.get_customer_by_email(order.customer_email)
        if customer and order_id in customer.orders:
            customer.orders.remove(order_id)

        return order

    def list_orders(self) -> List[Order]:
        return self.dao.list_orders()
'''

'''# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDAO, Order
from src.service.customer_service import CustomerService, CustomerError
from src.service.product_service import ProductService, ProductError


class OrderError(Exception):
    pass


class OrderService:
    """Business logic for order management"""

    def __init__(self, order_dao: OrderDAO = None,
                 customer_service: CustomerService = None,
                 product_service: ProductService = None):
        self.dao = order_dao or OrderDAO()
        self.customer_service = customer_service or CustomerService()
        self.product_service = product_service or ProductService()

    def create_order(self, customer_email: str, items: List[Dict]) -> Order:
        """
        items = [{"prod_id": 1, "quantity": 2}, {"prod_id": 3, "quantity": 1}]
        """
        # Check customer exists
        customer = self.customer_service.dao.get_customer_by_email(customer_email)
        if not customer:
            raise OrderError(f"Customer '{customer_email}' does not exist.")

        # Validate products and stock
        order_items = []
        total_amount = 0
        for item in items:
            prod_id = item.get("prod_id")
            quantity = item.get("quantity")
            product = self.product_service.dao.get_product_by_id(prod_id)
            if not product:
                raise OrderError(f"Product ID {prod_id} does not exist.")
            if product.stock < quantity:
                raise OrderError(f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {quantity}")

            # Deduct stock
            product.stock -= quantity
            # CORRECT
            new_stock = product["stock"] - qty  # calculate updated stock
            self.product_service.dao.update_product(product["prod_id"], {"stock": new_stock})


            # Prepare order item
            order_items.append({
                "prod_id": prod_id,
                "quantity": quantity,
                "price": product.price
            })
            total_amount += product.price * quantity

        # Insert order
        order = self.dao.insert_order(customer_email, order_items, total_amount)

        # Link order to customer
        customer.orders.append(order.order_id)
        return order

    def get_order_details(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        customer = self.customer_service.dao.get_customer_by_email(order.customer_email)
        return {
            "order_id": order.order_id,
            "customer": vars(customer),
            "items": order.items,
            "total_amount": order.total_amount,
            "status": order.status
        }

    def list_orders_by_customer(self, customer_email: str) -> List[Order]:
        return self.dao.list_orders_by_customer(customer_email)

    def cancel_order(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        if order.status != "PLACED":
            raise OrderError(f"Only PLACED orders can be cancelled. Current status: {order.status}")

        # Restore stock
        for item in order.items:
            product = self.product_service.dao.get_product_by_id(item["prod_id"])
            if product:
                product.stock += item["quantity"]
                self.product_service.dao.update_product(product)

        # Update status
        order.status = "CANCELLED"
        self.dao.update_order(order)

        # Remove from customer orders
        customer = self.customer_service.dao.get_customer_by_email(order.customer_email)
        if customer and order.order_id in customer.orders:
            customer.orders.remove(order.order_id)

        return order

    def complete_order(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        if order.status != "PLACED":
            raise OrderError(f"Only PLACED orders can be completed. Current status: {order.status}")
        order.status = "COMPLETED"
        self.dao.update_order(order)
        return order'''
'''# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDAO, Order
from src.service.customer_service import CustomerService, CustomerError
from src.service.product_service import ProductService, ProductError


class OrderError(Exception):
    pass


class OrderService:
    """Business logic for order management"""

    def __init__(self, order_dao: OrderDAO = None,
                 customer_service: CustomerService = None,
                 product_service: ProductService = None):
        self.dao = order_dao or OrderDAO()
        self.customer_service = customer_service or CustomerService()
        self.product_service = product_service or ProductService()

    def create_order(self, customer_email: str, items: List[Dict]) -> Order:
        """
        items = [{"prod_id": 1, "quantity": 2}, {"prod_id": 3, "quantity": 1}]
        """
        # Check customer exists
        customer = self.customer_service.dao.get_customer_by_email(customer_email)
        if not customer:
            raise OrderError(f"Customer '{customer_email}' does not exist.")

        total_amount = 0
        order_items = []

        # Validate products and deduct stock
        for item in items:
            prod_id = item.get("prod_id")
            quantity = item.get("quantity")

            product = self.product_service.dao.get_product_by_id(prod_id)
            if not product:
                raise OrderError(f"Product ID {prod_id} does not exist.")
            if product.stock < quantity:
                raise OrderError(f"Not enough stock for product '{product.name}'. "
                                 f"Available: {product.stock}, Requested: {quantity}")

            # Deduct stock
            new_stock = product.stock - quantity
            self.product_service.dao.update_product(prod_id, {"stock": new_stock})

            # Prepare order item
            order_items.append({
                "prod_id": prod_id,
                "quantity": quantity,
                "price": product.price
            })
            total_amount += product.price * quantity

        # Insert order
        order = self.dao.insert_order(customer_email, order_items, total_amount)

        # Link order to customer
        customer.orders.append(order.order_id)
        self.customer_service.dao.update_customer(customer)

        return order

    def get_order_details(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        customer = self.customer_service.dao.get_customer_by_email(order.customer_email)
        return {
            "order_id": order.order_id,
            "customer": vars(customer),
            "items": order.items,
            "total_amount": order.total_amount,
            "status": order.status
        }

    def list_orders_by_customer(self, customer_email: str) -> List[Order]:
        return self.dao.list_orders_by_customer(customer_email)

    def cancel_order(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        if order.status != "PLACED":
            raise OrderError(f"Only PLACED orders can be cancelled. Current status: {order.status}")

        # Restore stock
        for item in order.items:
            product = self.product_service.dao.get_product_by_id(item["prod_id"])
            if product:
                new_stock = product.stock + item["quantity"]
                self.product_service.dao.update_product(product.prod_id, {"stock": new_stock})

        # Update status
        order.status = "CANCELLED"
        self.dao.update_order(order)

        # Remove from customer orders
        customer = self.customer_service.dao.get_customer_by_email(order.customer_email)
        if customer and order.order_id in customer.orders:
            customer.orders.remove(order.order_id)
            self.customer_service.dao.update_customer(customer)

        return order

    def complete_order(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        if order.status != "PLACED":
            raise OrderError(f"Only PLACED orders can be completed. Current status: {order.status}")
        order.status = "COMPLETED"
        self.dao.update_order(order)
        return order
'''
# src/service/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDAO, Order
from src.service.customer_service import CustomerService, CustomerError
from src.service.product_service import ProductService, ProductError


class OrderError(Exception):
    pass


class OrderService:
    """Business logic for order management"""

    def __init__(self, order_dao: OrderDAO = None,
                 customer_service: CustomerService = None,
                 product_service: ProductService = None):
        self.dao = order_dao or OrderDAO()
        self.customer_service = customer_service or CustomerService()
        self.product_service = product_service or ProductService()

    def create_order(self, customer_email: str, items: List[Dict]) -> Order:
        """
        items = [{"prod_id": 1, "quantity": 2}, {"prod_id": 3, "quantity": 1}]
        """
        # Check customer exists
        customer = self.customer_service.dao.get_customer_by_email(customer_email)
        if not customer:
            raise OrderError(f"Customer '{customer_email}' does not exist.")

        total_amount = 0
        order_items = []

        # Validate products and deduct stock
        for item in items:
            prod_id = item.get("prod_id")
            quantity = item.get("quantity")

            product = self.product_service.dao.get_product_by_id(prod_id)
            if not product:
                raise OrderError(f"Product ID {prod_id} does not exist.")
            if product.stock < quantity:
                raise OrderError(
                    f"Not enough stock for product '{product.name}'. "
                    f"Available: {product.stock}, Requested: {quantity}"
                )

            # Deduct stock
            new_stock = product.stock - quantity
            self.product_service.dao.update_product(prod_id, {"stock": new_stock})

            # Prepare order item
            order_items.append({
                "prod_id": prod_id,
                "quantity": quantity,
                "price": product.price
            })
            total_amount += product.price * quantity

        # Insert order (using customer.id, not email)
        order = self.dao.insert_order(customer.id, order_items, total_amount)

        # Link order to customer
        if hasattr(customer, "orders"):
            customer.orders.append(order.order_id)
            self.customer_service.dao.update_customer(customer)

        return order

    def get_order_details(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        customer = self.customer_service.dao.get_customer_by_id(order.customer_id)
        return {
            "order_id": order.order_id,
            "customer": vars(customer),
            "items": order.items,
            "total_amount": order.total_amount,
            "status": order.status
        }

    def list_orders_by_customer(self, customer_email: str) -> List[Order]:
        customer = self.customer_service.dao.get_customer_by_email(customer_email)
        if not customer:
            return []
        return self.dao.list_orders_by_customer(customer.id)

    def cancel_order(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        if order.status != "PLACED":
            raise OrderError(f"Only PLACED orders can be cancelled. Current status: {order.status}")

        # Restore stock
        for item in order.items:
            product = self.product_service.dao.get_product_by_id(item["prod_id"])
            if product:
                new_stock = product.stock + item["quantity"]
                self.product_service.dao.update_product(product.prod_id, {"stock": new_stock})

        # Update status
        order.status = "CANCELLED"
        self.dao.update_order(order)

        return order

    def complete_order(self, order_id: int) -> Order:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found.")
        if order.status != "PLACED":
            raise OrderError(f"Only PLACED orders can be completed. Current status: {order.status}")
        order.status = "COMPLETED"
        self.dao.update_order(order)
        return order
