# src/service/payment_service.py
from src.dao.payment_dao import PaymentDAO, Payment
from src.service.order_service import OrderService, OrderError

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self, dao: PaymentDAO = None, order_service: OrderService = None):
        self.dao = dao or PaymentDAO()
        self.order_service = order_service or OrderService()

    def process_payment(self, order_id: int, method: str) -> Payment:
        order = self.order_service.get_order_details(order_id)
        if not order:
            raise PaymentError("Order not found")
        payment = self.dao.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        if payment.status == "PAID":
            raise PaymentError("Payment already processed")
        # Update payment
        payment = self.dao.update_payment(payment.payment_id, {"status": "PAID", "method": method})
        # Update order status
        self.order_service.complete_order(order_id)
        return payment

    def refund_payment(self, order_id: int) -> Payment:
        payment = self.dao.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        payment = self.dao.update_payment(payment.payment_id, {"status": "REFUNDED"})
        return payment
