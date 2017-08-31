class ShoppingCart(object):
    """This class define a Cart
    Args:
        db (list) list of all SKU for cart"""
    def __init__(self, email_customer=None):
        self.db = []

    def add_item(self, sku, quantity):
        items = {"parent": sku, "quantity": quantity, "type": 'sku'}
        for item in self.db:
            if item["parent"] == sku:
                    item["quantity"] += quantity
                    return self.db
        self.db.append(items)
        return self.db

    def update_item(self, sku, quantity):
        """Update item in cart"""
        for item in self.db:
            if item["parent"] == sku:
                    item["quantity"] = quantity

    def delete_item(self, sku):
        """Delete item in cart"""
        for it in self.db:
            if it.get("parent") == sku:
                self.db.remove(it)

    def clear_cart(self):
        """This method clear cart and items"""
        self.db = []
