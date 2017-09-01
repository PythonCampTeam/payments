class ShoppingCart(object):
    """This class define a Cart.

    Args:
        db (list): List of all SKU for cart.

    """
    def __init__(self, email_customer=None):
        self.db = []

    def add_item(self, sku, quantity):
        """This method add new product in cart.

        Args:
            sku (str): Sku of product.
            quantity (int): Quantity of product.

        Return:
            self.db (list): The cart after added product.

        """
        items = {"parent": sku, "quantity": quantity, "type": 'sku'}
        for item in self.db:
            if item["parent"] == sku:
                    item["quantity"] += quantity
                    return self.db
        self.db.append(items)
        return self.db

    def update_item(self, sku, quantity):
        """Update quantity of product in cart.

        Args:
            sku (str): Sku of product.
            quantity (int): Quantity of product.

        Return:
            self.db (list): The cart after update product.

        """
        for item in self.db:
            if item["parent"] == sku:
                    item["quantity"] = quantity
        return self.db

    def delete_item(self, sku):
        """Delete product in cart.

        Args:
            sku (str): Sku of product.
            quantity (int): Quantity of product.

        Return:
            self.db (list): The cart after delete product.

        """
        for it in self.db:
            if it.get("parent") == sku:
                self.db.remove(it)
        return self.db

    def clear_cart(self):
        """This method clear cart and items

        Return:
            self.db (list): Return empty cart.
        """
        self.db = []
        return self.db
