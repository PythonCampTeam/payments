# import uuid
import stripe


def _get_sku(id_product):
    prod = stripe.Product.retrieve(id_product)
    return prod.skus.data[0].id


class ShoppingCart(object):
    """This class define a Cart
    Args:
        db (list) list of all SKU for cart"""
    def __init__(self, email_customer=None):
        self.db = []

    def add_item(self, id_product, quantity):
        product = _get_sku(id_product)
        items = {"parent": product, "quantity": quantity, "type": 'sku'}
        for item in self.db:
            if item["parent"] == product:
                    item["quantity"] += quantity
                    return self.db
        self.db.append(items)
        return self.db

    def update_item(self, id_product, quantity):
        """Update item in cart"""
        product = _get_sku(id_product)
        for item in self.db:
            if item["parent"] == product:
                    item["quantity"] = quantity

    def delete_item(self, id_product):
        """Delete item in cart"""
        product = _get_sku(id_product)
        for it in self.db:
            if it.get("parent") == product:
                self.db.remove(it)

    def clear_cart(self):
        """This method clear cart and items"""
        self.db = []
