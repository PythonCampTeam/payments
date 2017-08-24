# import uuid
import stripe


def _get_sku(id_product):
    prod = stripe.Product.retrieve(id_product)
    return prod.skus.data[0].id


class ShoppingCart(object):
    """This class define a Cart"""
    def __init__(self, email_customer=None):
        self.items = {}
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
        product = _get_sku(id_product)
        for item in self.db:
            if item["parent"] == product:
                    item["quantity"] = quantity
        # return {"error": "Product does not exist in cart"}

    def delete_item(self, id_product):
        product = _get_sku(id_product)
        for it in self.db:
            if it.get("parent") == product:
                self.db.remove(it)
                return "item delete"

    def clear_cart(self):
        """This method clear cart and items"""
        self.db = []
        self.items = {}
