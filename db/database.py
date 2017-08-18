# import uuid
import stripe


def _get_sku(id_product):
    prod = stripe.Product.retrieve(id_product)
    return prod.skus.data[0].id


class ShoppingCart(object):
    """This class define a Cart"""
    def __init__(self, email_customer=None):
        self.total = 0
        self.items = {}
        self.db = []
        # self.email_customer = email_customer

    def add_item(self, id_product, quantity):
        self.items = {"parent": _get_sku(id_product), "quantity": quantity, "type": 'sku'}
        self.db.append(self.items)

    def update_item(self, id_product, quantity):
        for item in self.db:
            if item["parent"] == _get_sku(id_product):
                    item["quantity"] += quantity
        return self.db

    def delete_item(self, id_product):
        for it in self.db:
            if it.get("parent") == _get_sku(id_product):
                self.db.remove(it)
                return "item delete"
