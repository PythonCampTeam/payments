import cerberus
import stripe
from nameko.rpc import rpc

try:
    from db.database import ShoppingCart
    from rpc import validate
    from rpc.exception import handling
except ImportError:
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
    def add_in_cart(self, id_product, quality):
        """This method add new product in cart database
        Args:
            body(dict) body request
            id_product(str) : id of product
            quality(str) : quality of product
        Returs:
            Object of cart
        """
        cart = self.cart.add_item(id_product, quality)
        return cart

    @rpc
    def get_cart(self):
        """This method rerutn current cart
        Return:
            cart (list) current cart in db
        """
        return self.cart.db

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
        self.cart.delete_item(id_product)
        return self.get_cart()

    @rpc
    def update_item(self, product_id, quality):
        """This method udtate product
        Args:
            id_product(str) : id of product
            quality(str) : quality of product
        Return:
            cart (list) current cart in db
        """
        self.cart.update_item(product_id, quality)
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
        print(self.cart.db)

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
            order.save()
        except stripe.error.InvalidRequestError as e:
            return handling(e)
        return order

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
            charge = order.pay(source=cart)
        except stripe.error.InvalidRequestError as e:
            return {"errors": handling(e)}
        return charge
