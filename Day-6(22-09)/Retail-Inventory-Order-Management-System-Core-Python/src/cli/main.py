'''# src/cli/main.py
import argparse
import json
from src.service import product_service,order_service
from src.dao import product_dao, customer_dao
 
def cmd_product_add(args):
    try:
        p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_product_list(args):
    ps = product_dao.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))
 
def cmd_customer_add(args):
    try:
        c = customer_dao.create_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_create(args):
    # items provided as prod_id:qty strings
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_service.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_show(args):
    try:
        o = order_service.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")
 
    # product add/list
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
 
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)
 
    # customer add
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)
 
    # order
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")
 
    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)
 
    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)
 
    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)
 
    return parser
 
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)
 
if __name__ == "__main__":
    main()'''

"""import argparse
import json
from src.service import product_service
from src.dao import product_dao

# -------------------- Product Command Functions --------------------
def cmd_product_add(args):
    try:
        p = product_service.add_product(
            args.name, args.sku, args.price, args.stock, args.category
        )
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    ps = product_dao.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))

# -------------------- CLI Parser --------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Product commands
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")

    # product add
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)

    # product list
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    return parser

# -------------------- Main --------------------
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()"""

'''#using oops concept
# src/cli/main.py
import argparse
import json
from src.service import product_service, order_service
from src.dao import product_dao, customer_dao


class CLICommand:
    """Base class for CLI commands"""
    def execute(self, args):
        raise NotImplementedError("Each command must implement execute()")


class ProductAddCommand(CLICommand):
    def execute(self, args):
        try:
            p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("Created product:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)


class ProductListCommand(CLICommand):
    def execute(self, args):
        ps = product_dao.list_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))


class CustomerAddCommand(CLICommand):
    def execute(self, args):
        try:
            c = customer_dao.create_customer(args.name, args.email, args.phone, args.city)
            print("Created customer:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)


class OrderCreateCommand(CLICommand):
    def execute(self, args):
        items = []
        for item in args.item:
            try:
                pid, qty = item.split(":")
                items.append({"prod_id": int(pid), "quantity": int(qty)})
            except Exception:
                print("Invalid item format:", item)
                return
        try:
            ord = order_service.create_order(args.customer, items)
            print("Order created:")
            print(json.dumps(ord, indent=2, default=str))
        except Exception as e:
            print("Error:", e)


class OrderShowCommand(CLICommand):
    def execute(self, args):
        try:
            o = order_service.get_order_details(args.order)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)


class OrderCancelCommand(CLICommand):
    def execute(self, args):
        try:
            o = order_service.cancel_order(args.order)
            print("Order cancelled (updated):")
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)


class CLI:
    """Main CLI class"""
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="retail-cli")
        self.subparsers = self.parser.add_subparsers(dest="cmd")
        self.register_commands()

    def register_commands(self):
        # Product commands
        p_prod = self.subparsers.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")

        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category", default=None)
        addp.set_defaults(command=ProductAddCommand())

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(command=ProductListCommand())

        # Customer commands
        pcust = self.subparsers.add_parser("customer")
        pcust_sub = pcust.add_subparsers(dest="action")

        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city", default=None)
        addc.set_defaults(command=CustomerAddCommand())

        # Order commands
        porder = self.subparsers.add_parser("order")
        porder_sub = porder.add_subparsers(dest="action")

        createo = porder_sub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
        createo.set_defaults(command=OrderCreateCommand())

        showo = porder_sub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(command=OrderShowCommand())

        cano = porder_sub.add_parser("cancel")
        cano.add_argument("--order", type=int, required=True)
        cano.set_defaults(command=OrderCancelCommand())

    def run(self):
        args = self.parser.parse_args()
        if not hasattr(args, "command"):
            self.parser.print_help()
            return
        args.command.execute(args)


if __name__ == "__main__":
    CLI().run()'''

# src/cli/main.py
import argparse
import json

from src.service.product_service import ProductService, ProductError
from src.service.customer_service import CustomerService, CustomerError
from src.service.order_service import OrderService, OrderError
from src.dao.product_dao import ProductDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.order_dao import OrderDAO


class CLI:
    """Main CLI handler using services"""

    def __init__(self):
        product_dao = ProductDAO()
        customer_dao = CustomerDAO()
        order_dao = OrderDAO()
        
        self.product_service = ProductService(dao=product_dao)
        self.customer_service = CustomerService(dao=customer_dao)
        self.order_service = OrderService(order_dao=order_dao, customer_service=self.customer_service)


    def cmd_product_add(self, args):
        try:
            p = self.product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("Created product:")
            print(json.dumps(vars(p), indent=2))
        except ProductError as e:
            print("Error:", e)

    def cmd_product_list(self, args):
        products = self.product_service.dao.list_products()
        print(json.dumps([vars(p) for p in products], indent=2))


    def cmd_customer_add(self, args):
        try:
            c = self.customer_service.add_customer(args.name, args.email, args.phone, args.city)
            print("Created customer:")
            print(json.dumps(vars(c), indent=2))
        except CustomerError as e:
            print("Error:", e)

    def cmd_customer_list(self, args):
        customers = self.customer_service.list_customers()
        print(json.dumps([vars(c) for c in customers], indent=2))

    def cmd_customer_update(self, args):
        try:
            c = self.customer_service.update_customer(args.email, args.phone, args.city)
            print("Updated customer:")
            print(json.dumps(vars(c), indent=2))
        except CustomerError as e:
            print("Error:", e)

    def cmd_customer_delete(self, args):
        try:
            self.customer_service.delete_customer(args.email)
            print(f"Customer '{args.email}' deleted successfully.")
        except CustomerError as e:
            print("Error:", e)

    def cmd_customer_search(self, args):
        results = self.customer_service.search_customers(args.email, args.city)
        if not results:
            print("No matching customers found.")
            return
        print(json.dumps([vars(c) for c in results], indent=2))


    def cmd_order_create(self, args):
        try:
            items = []
            for item in args.item:
                try:
                    pid, qty = item.split(":")
                    items.append({"prod_id": int(pid), "quantity": int(qty)})
                except Exception:
                    print("Invalid item format:", item)
                    return
            o = self.order_service.create_order(args.customer, items)
            print("Order created:")
            print(json.dumps(vars(o), indent=2))
        except OrderError as e:
            print("Error:", e)

    def cmd_order_show(self, args):
        try:
            o = self.order_service.get_order_details(args.order)
            print(json.dumps(vars(o), indent=2))
        except OrderError as e:
            print("Error:", e)

    def cmd_order_cancel(self, args):
        try:
            o = self.order_service.cancel_order(args.order)
            print("Order cancelled:")
            print(json.dumps(vars(o), indent=2))
        except OrderError as e:
            print("Error:", e)

    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # Product commands
        p_prod = sub.add_parser("product")
        p_prod_sub = p_prod.add_subparsers(dest="action")

        addp = p_prod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category")
        addp.set_defaults(func=self.cmd_product_add)

        listp = p_prod_sub.add_parser("list")
        listp.set_defaults(func=self.cmd_product_list)

        # Customer commands
        p_cust = sub.add_parser("customer")
        c_sub = p_cust.add_subparsers(dest="action")

        addc = c_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city")
        addc.set_defaults(func=self.cmd_customer_add)

        listc = c_sub.add_parser("list")
        listc.set_defaults(func=self.cmd_customer_list)

        updatec = c_sub.add_parser("update")
        updatec.add_argument("--email", required=True)
        updatec.add_argument("--phone")
        updatec.add_argument("--city")
        updatec.set_defaults(func=self.cmd_customer_update)

        deletec = c_sub.add_parser("delete")
        deletec.add_argument("--email", required=True)
        deletec.set_defaults(func=self.cmd_customer_delete)

        searchc = c_sub.add_parser("search")
        searchc.add_argument("--email")
        searchc.add_argument("--city")
        searchc.set_defaults(func=self.cmd_customer_search)

        # Order commands
        p_order = sub.add_parser("order")
        o_sub = p_order.add_subparsers(dest="action")

        createo = o_sub.add_parser("create")
        createo.add_argument("--customer", required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
        createo.set_defaults(func=self.cmd_order_create)

        showo = o_sub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)

        cano = o_sub.add_parser("cancel")
        cano.add_argument("--order", type=int, required=True)
        cano.set_defaults(func=self.cmd_order_cancel)

        return parser

    def run(self):
        parser = self.build_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()


if __name__ == "__main__":
    CLI().run()
