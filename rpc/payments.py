from nameko.rpc import rpc
import stripe
from db.database import ShoppingCart


class Payments(object):

    name = 'PaymentsRPC'
    stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"
    cart = ShoppingCart()

    @rpc
    def add_in_cart(self, id_product, quality):
        Payments.cart.add_item(id_product, quality)
        return Payments.cart.items

    @rpc
    def get_cart(self):
        return Payments.cart.db

    @rpc
    def delete_item(self, id_product):
        Payments.cart.delete_item(id_product)

    @rpc
    def update_item(self, id_product):
        Payments.cart.update_item(id_product)

    @rpc
    def delete_cart(self):
        Payments.cart.db = []
        Payments.get_cart()

    @rpc
    def new_order(self, mail, shipping):
        order = stripe.Order.create(currency='usd',
                                    items=Payments.cart.db,
                                    shipping=shipping,
                                    email=mail
                                    )
        return order

    @rpc
    def pay_order(self, order, cart):
        charge = order.pay(source=cart)
        return charge
