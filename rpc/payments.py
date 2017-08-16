from nameko.rpc import rpc
import stripe


class Payments(object):

    name = 'PaymentsRPC'
    stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"

    def add_in_cart(self):
        

    def transaction(self):
        order = stripe.Order.create()
        order.pay
