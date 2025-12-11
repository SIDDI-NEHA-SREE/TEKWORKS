# src/dao/payment_dao.py
from typing import List, Optional, Dict
from src.config import get_supabase

class Payment:
    def __init__(self, payment_id: int, order_id: int, amount: float, status: str = "PENDING", method: str = None):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.status = status
        self.method = method

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            payment_id=data.get("payment_id"),
            order_id=data.get("order_id"),
            amount=data.get("amount"),
            status=data.get("status"),
            method=data.get("method")
        )

class PaymentDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_payment(self, order_id: int, amount: float) -> Optional[Payment]:
        payload = {"order_id": order_id, "amount": amount, "status": "PENDING"}
        self._sb.table("payments").insert(payload).execute()
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        if resp.data:
            return Payment.from_dict(resp.data[0])
        return None

    def update_payment(self, payment_id: int, fields: Dict) -> Optional[Payment]:
        self._sb.table("payments").update(fields).eq("payment_id", payment_id).execute()
        resp = self._sb.table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
        if resp.data:
            return Payment.from_dict(resp.data[0])
        return None

    def get_payment_by_order(self, order_id: int) -> Optional[Payment]:
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        if resp.data:
            return Payment.from_dict(resp.data[0])
        return None
