'''# src/dao/customer_dao.py
from typing import List, Optional


class Customer:
    def __init__(self, name: str, email: str, phone: str, city: str | None = None):
        self.name = name
        self.email = email
        self.phone = phone
        self.city = city
        self.orders: List[str] = []  # list of order IDs


class CustomerDAO:
    """Data Access Object for customer storage"""

    def __init__(self):
        self._customers: List[Customer] = []

    def create_customer(self, customer: Customer) -> Customer:
    payload = {
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "city": customer.city
    }
    self._sb.table("customers").insert(payload).execute()  # <--- this line must run
    return customer


    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        for c in self._customers:
            if c.email == email:
                return c
        return None

    def update_customer(self, customer: Customer) -> Optional[Customer]:
        for idx, c in enumerate(self._customers):
            if c.email == customer.email:
                self._customers[idx] = customer
                return customer
        return None

    def delete_customer(self, email: str) -> bool:
        for c in self._customers:
            if c.email == email:
                self._customers.remove(c)
                return True
        return False

    def list_customers(self) -> List[Customer]:
        return self._customers

    def search_customers(self, email: str = None, city: str = None) -> List[Customer]:
        results = []
        for c in self._customers:
            if (email and c.email == email) or (city and c.city and c.city.lower() == city.lower()):
                results.append(c)
        return results
'''

# src/dao/customer_dao.py
from typing import List, Optional, Dict
from src.config import get_supabase

class Customer:
    def __init__(self, name: str, email: str, phone: str, city: str | None = None):
        self.name = name
        self.email = email
        self.phone = phone
        self.city = city
        self.orders: List[str] = []  # list of order IDs

    @classmethod
    def from_dict(cls, data: Dict):
        customer = cls(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            city=data.get("city")
        )
        customer.orders = data.get("orders", [])
        return customer

class CustomerDAO:
    """Data Access Object for customer storage in Supabase"""

    def __init__(self):
        self._sb = get_supabase()

    def create_customer(self, customer: Customer) -> Customer:
        payload = {
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "city": customer.city,
            "orders": customer.orders
        }
        self._sb.table("customers").insert(payload).execute()
        resp = self._sb.table("customers").select("*").eq("email", customer.email).limit(1).execute()
        if resp.data:
            return Customer.from_dict(resp.data[0])
        return customer

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        if resp.data:
            return Customer.from_dict(resp.data[0])
        return None

    def update_customer(self, customer: Customer) -> Optional[Customer]:
        payload = {
            "name": customer.name,
            "phone": customer.phone,
            "city": customer.city,
            "orders": customer.orders
        }
        self._sb.table("customers").update(payload).eq("email", customer.email).execute()
        resp = self._sb.table("customers").select("*").eq("email", customer.email).limit(1).execute()
        if resp.data:
            return Customer.from_dict(resp.data[0])
        return None

    def delete_customer(self, email: str) -> bool:
        resp_before = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        if not resp_before.data:
            return False
        customer_data = resp_before.data[0]
        if customer_data.get("orders"):
            # block deletion if orders exist
            return False
        self._sb.table("customers").delete().eq("email", email).execute()
        return True

    def list_customers(self) -> List[Customer]:
        resp = self._sb.table("customers").select("*").order("name", desc=False).execute()
        return [Customer.from_dict(c) for c in resp.data] if resp.data else []

    def search_customers(self, email: str = None, city: str = None) -> List[Customer]:
        q = self._sb.table("customers").select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return [Customer.from_dict(c) for c in resp.data] if resp.data else []
