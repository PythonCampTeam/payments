from nameko.rpc import rpc
import stripe
from db.database import ShoppingCart


class Payments(object):

    name = 'PaymentsRPC'
    stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"
    cart = ShoppingCart()

    @rpc
    def add_in_cart(self, id_product, quality):
        """This method add new product in cart database
        Args:
            id_product(str) : id of product
            quality(str) : quality of product
        """
        Payments.cart.add_item(id_product, quality)
        return Payments.cart.db

    @rpc
    def get_cart(self):
        """This method rerutn current cart
        Return:
            cart (list) current cart in db
        """
        return Payments.cart.db

    @rpc
    def delete_item(self, id_product):
        """This method delete product from cart and
        return current cart
        Args:
            id_product(str) : id of product
            quality(str) : quality of product
        Return:
            cart (list) current cart in db
        """
        Payments.cart.delete_item(id_product)
        Payments.get_cart()

    @rpc
    def update_item(self, id_product, quality):
        """This method udtate product
        Args:
            id_product(str) : id of product
            quality(str) : quality of product
        Return:
            cart (list) current cart in db
        """
        Payments.cart.update_item(id_product, quality)
        Payments.get_cart()

    @rpc
    def delete_cart(self):
        """This method clear cart
        Return:
            cart (list) current cart in db
        """
        Payments.cart.clear_cart()
        Payments.get_cart()

    @rpc
    def new_order(self, mail, shipping):
        order = stripe.Order.create(currency='usd',
                                    items=Payments.cart.db,
                                    shipping=shipping,
                                    email=mail
                                    )
        return order

    #or_1As6NSBqraFdOKT2yQmMb5w0
    #0719ec510c29407f9bcea461ccdacf39

    @rpc
    def select_shipping(self, order_id, shipping_id):
        order = stripe.Order.retrieve(order_id)
        order.selected_shipping_method = shipping_id
        return order

    @rpc
    def pay_order(self, order, cart):
        charge = order.pay(source=cart)
        return charge
