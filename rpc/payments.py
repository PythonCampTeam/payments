import cerberus
import stripe
from nameko.rpc import rpc

from payments.db.database import ShoppingCart
from payments.rpc import validate
from payments.rpc.exception import handling

Validator = cerberus.Validator
v = Validator()


class Payments(object):

    name = 'PaymentsRPC'
    stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"
    cart = ShoppingCart()

    @rpc
    def add_in_cart(self, sku, quality):
        """This method add new product in cart database
        Args:
            body(dict) body request
            id_product(str) : id of product
            quality(str) : quality of product
        Returs:
            Object of cart
        """
        cart = self.cart.add_item(sku, quality)
        return cart

    @rpc
    def get_cart(self):
        """This method rerutn current cart
        Return:
            cart (list) current cart in db
        """
        return self.cart.db

    @rpc
    def delete_item(self, sku):
        """This method delete product from cart and
        return current cart
        Args:
            id_product(str) : id of product
            quality(str) : quality of product
        Return:
            cart (list) current cart in db
        """
        self.cart.delete_item(sku)
        return self.get_cart()

    @rpc
    def update_item(self, sku, quality):
        """This method udtate product
        Args:
            id_product(str) : id of product
            quality(str) : quality of product
        Return:
            cart (list) current cart in db
        """
        self.cart.update_item(sku, quality)
        return self.cart.db

    @rpc
    def delete_cart(self):
        """This method clear cart
        Return:
            cart (list) current cart in db
        """
        self.cart.clear_cart()
        return self.get_cart()

    @rpc
    def new_order(self, body):
        """Crated a order
        Args:
            body(dict) parameters for create a order
            email(str) The email address of the customer
            shipping(ditc) shipping address for the order
            phone(str) phone of the customer
        Returns:
            result (dist) if the call succeeded
        """
        if not v.validate(body, validate.schema_order):
            return {"errors": v.errors}
        error_message = None
        email = body.get('email')
        phone = body.get('phone')

        shipping = {
                    "name": body.get('name'),
                    "address": body.get('address'),
                    "phone": phone
                    }
        print(shipping)
        try:
            result = stripe.Order.create(
                                        currency='usd',
                                        items=self.cart.db,
                                        shipping=shipping,
                                        email=email
                                        )
        except stripe.error.InvalidRequestError as e:
            error_message = handling(e)
            result = None
        return {
                "email": email,
                "phone": phone,
                "response": result,
                "errors": error_message
                }

    @rpc
    def select_shipping(self, order_id, shipping_id):
        """Change shipping in Order. Shipping should consist of methods.
        Args:
            order_id (str): uniq number of the product
            shipping_id (str): uniq number of the shipping
        Return:
            order (dict): booking of customer
        """
        try:
            order = stripe.Order.retrieve(order_id)
            order.selected_shipping_method = shipping_id
            result = stripe.Order.save(order)
        except stripe.error.InvalidRequestError as e:
            return {"errors": handling(e)}
        return result

    @rpc
    def pay_order(self, order_id, cart):
        """Pay order with test cart
        Args:
            order_id (str): id of new order
            cart (str): token of cart

        Return:
            charge : Order with status 'paid', stripe's object

        """
        try:
            order = stripe.Order.retrieve(order_id)
            charge = stripe.Order.pay(order, source=cart)
        except stripe.error.InvalidRequestError as e:
            return {"errors": handling(e)}
        return charge
