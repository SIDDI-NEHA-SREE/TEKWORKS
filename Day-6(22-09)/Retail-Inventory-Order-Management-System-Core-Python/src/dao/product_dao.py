'''# src/dao/product_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase
 
def _sb():
    return get_supabase()
 
def create_product(name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
    """
    Insert a product and return the inserted row (two-step: insert then select by unique sku).
    """
    payload = {"name": name, "sku": sku, "price": price, "stock": stock}
    if category is not None:
        payload["category"] = category
 
    # Insert (no select chaining)
    _sb().table("products").insert(payload).execute()
 
    # Fetch inserted row by unique column (sku)
    resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None
 
def get_product_by_id(prod_id: int) -> Optional[Dict]:
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None
 
def get_product_by_sku(sku: str) -> Optional[Dict]:
    resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None
 
def update_product(prod_id: int, fields: Dict) -> Optional[Dict]:
    """
    Update and then return the updated row (two-step).
    """
    _sb().table("products").update(fields).eq("prod_id", prod_id).execute()
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None
 
def delete_product(prod_id: int) -> Optional[Dict]:
    # fetch row before delete (so we can return it)
    resp_before = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    row = resp_before.data[0] if resp_before.data else None
    _sb().table("products").delete().eq("prod_id", prod_id).execute()
    return row
 
def list_products(limit: int = 100, category: str | None = None) -> List[Dict]:
    q = _sb().table("products").select("*").order("prod_id", desc=False).limit(limit)
    if category:
        q = q.eq("category", category)
    resp = q.execute()
    return resp.data or []'''
'''#using oops concept
# src/dao/product_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase


class ProductDAO:
    """Data Access Object for Product operations"""

    def __init__(self):
        self._sb = get_supabase()

    def create_product(
        self,
        name: str,
        sku: str,
        price: float,
        stock: int = 0,
        category: str | None = None
    ) -> Optional[Dict]:
        """
        Insert a product and return the inserted row.
        """
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category:
            payload["category"] = category

        # Insert product
        self._sb.table("products").insert(payload).execute()

        # Fetch inserted row by unique sku
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_product_by_id(self, prod_id: int) -> Optional[Dict]:
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_product_by_sku(self, sku: str) -> Optional[Dict]:
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_product(self, prod_id: int, fields: Dict) -> Optional[Dict]:
        """
        Update product fields and return the updated row.
        """
        self._sb.table("products").update(fields).eq("prod_id", prod_id).execute()
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_product(self, prod_id: int) -> Optional[Dict]:
        """
        Delete a product and return the deleted row.
        """
        resp_before = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb.table("products").delete().eq("prod_id", prod_id).execute()
        return row

    def list_products(self, limit: int = 100, category: str | None = None) -> List[Dict]:
        """
        List products with optional category filter.
        """
        q = self._sb.table("products").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []
'''


# src/dao/product_dao.py
from typing import Optional, List
from src.config import get_supabase


class Product:
    def __init__(self, prod_id: int, name: str, sku: str, price: float, stock: int, category: str | None = None):
        self.prod_id = prod_id
        self.name = name
        self.sku = sku
        self.price = price
        self.stock = stock
        self.category = category

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(
            prod_id=data.get("prod_id"),
            name=data.get("name"),
            sku=data.get("sku"),
            price=data.get("price"),
            stock=data.get("stock"),
            category=data.get("category")
        )


class ProductDAO:
    """Data Access Object for Product operations"""

    def __init__(self):
        self._sb = get_supabase()

    def create_product(
        self,
        name: str,
        sku: str,
        price: float,
        stock: int = 0,
        category: str | None = None
    ) -> Optional[Product]:
        """Insert a product and return a Product object"""
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category:
            payload["category"] = category

        self._sb.table("products").insert(payload).execute()

        # Fetch inserted row
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        if resp.data:
            return Product.from_dict(resp.data[0])
        return None

    def get_product_by_id(self, prod_id: int) -> Optional[Product]:
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        if resp.data:
            return Product.from_dict(resp.data[0])
        return None

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        if resp.data:
            return Product.from_dict(resp.data[0])
        return None

    def update_product(self, prod_id: int, fields: dict) -> Optional[Product]:
        """Update product fields and return updated Product"""
        self._sb.table("products").update(fields).eq("prod_id", prod_id).execute()
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        if resp.data:
            return Product.from_dict(resp.data[0])
        return None

    def delete_product(self, prod_id: int) -> Optional[Product]:
        """Delete product and return deleted Product"""
        resp_before = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        if resp_before.data:
            product = Product.from_dict(resp_before.data[0])
            self._sb.table("products").delete().eq("prod_id", prod_id).execute()
            return product
        return None

    def list_products(self, limit: int = 100, category: str | None = None) -> List[Product]:
        """List all products with optional category filter"""
        q = self._sb.table("products").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return [Product.from_dict(d) for d in resp.data] if resp.data else []
