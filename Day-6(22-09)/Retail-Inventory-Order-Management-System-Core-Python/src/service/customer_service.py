'''class Customer:
    def __init__(self, name, email, phone, city):
        self.name = name
        self.email = email
        self.phone = phone
        self.city = city
        self.orders = []  # List to store customer's orders

class CustomerManager:
    def __init__(self):
        self.customers = []  # List to store all customers

    # Helper to check if email exists
    def email_exists(self, email):
        return any(c.email == email for c in self.customers)

    # Create a new customer
    def add_customer(self, name, email, phone, city):
        if self.email_exists(email):
            print(f"Error: Customer with email '{email}' already exists.")
            return
        customer = Customer(name, email, phone, city)
        self.customers.append(customer)
        print(f"Customer '{name}' added successfully.")

    # Update phone or city of a customer
    def update_customer(self, email, phone=None, city=None):
        for c in self.customers:
            if c.email == email:
                if phone:
                    c.phone = phone
                if city:
                    c.city = city
                print(f"Customer '{email}' updated successfully.")
                return
        print(f"Error: Customer with email '{email}' not found.")

    # Delete a customer if no orders
    def delete_customer(self, email):
        for c in self.customers:
            if c.email == email:
                if c.orders:
                    print(f"Error: Cannot delete customer '{email}' as they have existing orders.")
                    return
                self.customers.remove(c)
                print(f"Customer '{email}' deleted successfully.")
                return
        print(f"Error: Customer with email '{email}' not found.")

    # List all customers
    def list_customers(self):
        if not self.customers:
            print("No customers found.")
            return
        print("Customers List:")
        for c in self.customers:
            print(f"Name: {c.name}, Email: {c.email}, Phone: {c.phone}, City: {c.city}, Orders: {len(c.orders)}")

    # Search customer by email or city
    def search_customers(self, email=None, city=None):
        results = []
        for c in self.customers:
            if (email and c.email == email) or (city and c.city.lower() == city.lower()):
                results.append(c)
        if not results:
            print("No matching customers found.")
            return
        print("Search Results:")
        for c in results:
            print(f"Name: {c.name}, Email: {c.email}, Phone: {c.phone}, City: {c.city}, Orders: {len(c.orders)}")

# ------------------- Example Usage -------------------
manager = CustomerManager()

# Add customers
manager.add_customer("Alice", "alice@example.com", "1234567890", "Hyderabad")
manager.add_customer("Bob", "bob@example.com", "0987654321", "Delhi")

# Update customer
manager.update_customer("alice@example.com", phone="1112223333")

# List customers
manager.list_customers()

# Search customer
manager.search_customers(city="Delhi")

# Delete customer (will fail if orders exist)
manager.delete_customer("alice@example.com")

# Simulate an order
manager.customers[0].orders.append("Order001")
manager.delete_customer("alice@example.com")  '''

#using oops conept
# src/services/customer_service.py
from typing import List
from src.dao.customer_dao import CustomerDAO, Customer


class CustomerError(Exception):
    """Custom exception for customer-related errors"""
    pass


class CustomerService:
    """Business logic layer for customer management"""

    def __init__(self, dao: CustomerDAO = None):
        self.dao = dao or CustomerDAO()

    def add_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Customer:
        if self.dao.get_customer_by_email(email):
            raise CustomerError(f"Customer with email '{email}' already exists.")
        customer = Customer(name, email, phone, city)
        return self.dao.create_customer(customer)

    def update_customer(self, email: str, phone: str | None = None, city: str | None = None) -> Customer:
        customer = self.dao.get_customer_by_email(email)
        if not customer:
            raise CustomerError(f"Customer with email '{email}' not found.")
        if phone:
            customer.phone = phone
        if city:
            customer.city = city
        return self.dao.update_customer(customer)

    def delete_customer(self, email: str) -> bool:
        customer = self.dao.get_customer_by_email(email)
        if not customer:
            raise CustomerError(f"Customer with email '{email}' not found.")
        if customer.orders:
            raise CustomerError(f"Cannot delete '{email}': customer has existing orders.")
        return self.dao.delete_customer(email)

    def list_customers(self) -> List[Customer]:
        return self.dao.list_customers()

    def search_customers(self, email: str = None, city: str = None) -> List[Customer]:
        return self.dao.search_customers(email=email, city=city)


