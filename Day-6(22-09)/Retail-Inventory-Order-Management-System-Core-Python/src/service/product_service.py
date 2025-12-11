'''# src/services/product_service.py
from typing import List, Dict
import src.dao.product_dao as product_dao

class ProductError(Exception):
    pass
 
def add_product(name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
    """
    Validate and insert a new product.
    Raises ProductError on validation failure.
    """
    if price <= 0:
        raise ProductError("Price must be greater than 0")
    existing = product_dao.get_product_by_sku(sku)
    if existing:
        raise ProductError(f"SKU already exists: {sku}")
    return product_dao.create_product(name, sku, price, stock, category)
 
def restock_product(prod_id: int, delta: int) -> Dict:
    if delta <= 0:
        raise ProductError("Delta must be positive")
    p = product_dao.get_product_by_id(prod_id)
    if not p:
        raise ProductError("Product not found")
    new_stock = (p.get("stock") or 0) + delta
    return product_dao.update_product(prod_id, {"stock": new_stock})
 
def get_low_stock(threshold: int = 5) -> List[Dict]:
    allp = product_dao.list_products(limit=1000)
    return [p for p in allp if (p.get("stock") or 0) <= threshold]
 '''
#usimg oops concept
# src/services/product_service.py
from typing import List, Dict
from src.dao.product_dao import ProductDAO


class ProductError(Exception):
    """Custom exception for product-related errors"""
    pass


class ProductService:
    """Service layer for product operations, contains business logic"""

    def __init__(self, dao: ProductDAO = None):
        self.dao = dao or ProductDAO()  # Use DAO instance, default if not provided

    def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
        """
        Validate and insert a new product.
        Raises ProductError on validation failure.
        """
        if price <= 0:
            raise ProductError("Price must be greater than 0")
        if self.dao.get_product_by_sku(sku):
            raise ProductError(f"SKU already exists: {sku}")
        return self.dao.create_product(name, sku, price, stock, category)

    def restock_product(self, prod_id: int, delta: int) -> Dict:
        """Increase stock of an existing product"""
        if delta <= 0:
            raise ProductError("Delta must be positive")
        product = self.dao.get_product_by_id(prod_id)
        if not product:
            raise ProductError("Product not found")
        new_stock = (product.get("stock") or 0) + delta
        return self.dao.update_product(prod_id, {"stock": new_stock})

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        """Return products with stock below or equal to the threshold"""
        all_products = self.dao.list_products(limit=1000)
        return [p for p in all_products if (p.get("stock") or 0) <= threshold]

