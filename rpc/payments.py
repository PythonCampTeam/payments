from nameko.rpc import rpc
import stripe
from db.database import ShoppingCart
import cerberus
from rpc import validate

Validator = cerberus.Validator
v = Validator()



class Payments(object):

    name = 'PaymentsRPC'
    stripe.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"
    cart = ShoppingCart()

    def get_package(self):
        """This method return main packagedimensions
        Args:
            weight (int): weight of products
            length (int): length of products
            height (int): height of products
            width (int): width of products

        """
        weight = 0
        length = 0
        height = 0
        width = 0
        for item in Payments.cart.db:
            sk = stripe.SKU.retrieve(item['parent'])
            weight += sk.package_dimensions.weight * int(item['quantity'])
            length += sk.package_dimensions.length * int(item['quantity'])
            height += sk.package_dimensions.height * int(item['quantity'])
            width += sk.package_dimensions.width * int(item['quantity'])
        return {
            "length": length,
            "width": width,
            "height": height,
            "distance_unit": "in",
            "weight": weight,
            "mass_unit": "lb",
            }
    # sk = stripe.SKU.retrieve("sku_BDPEtaqvwW7kgt")

    # def parsel(self, pack):
    #     parcel = {
    #         "length": pack.get("length"),
    #         "width": pack.get("width"),
    #         "height": pack.get("height"),
    #         "distance_unit": "in",
    #         "weight": pack.get("weight"),
    #         "mass_unit": "lb",
    #     }
    #     return parcel

    # s.add_item('prod_BDQT7ifqt1FFc1', '2')
    #  s.add_item('prod_BF2pHek9EyzO2S', '2')

    @rpc
    def add_in_cart(self, body):
        """This method add new product in cart database

        Args:
            body(dict) body request
            id_product(str) : id of product
            quality(str) : quality of product

        Returs:
            Object of cart

        """
        if not v.validate(body, validate.schema_add):
            return v.errors
        id_product = body.get('product_id')
        quality = body.get('quality')
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
    def update_item(self, body):
        """This method udtate product
        Args:
            id_product(str) : id of product
            quality(str) : quality of product
        Return:
            cart (list) current cart in db
        """
        if not v.validate(body, validate.schema_add):
            return v.errors
        id_product = body.get('product_id')
        quality = body.get('quality')
        self.cart.update_item(id_product, quality)
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
        email = body.get('email')
        phone = body.get('phone')
        shipping = {
                    "name": body.get('name'),
                    "address": body.get('address'),
                    "phone": phone
                    }
        try:
            result = stripe.Order.create(
                                        currency='usd',
                                        items=self.cart.db,
                                        shipping=shipping,
                                        email=email
                                        )
        except stripe.error.InvalidRequestError as e:
            body = e.json_body
            err = body.get('error', {})
            result = "Status is: {}, message is: {}".format(e.http_status,
                                                            err.get('message'))
        return {"email": email, "phone": phone, "response": result}

    @rpc
    def get_shipping(id_order):
        """Converts an address to from stripe object to
        an address to from Shippo object
        Args:
            id_order (str): uniq number of specific
        Return:
            address_to (str): adress in Shippo schema
        """
        order = stripe.Order.retrieve(id_order)
        addres = order.shipping.address
        city = addres.get("city")
        street1 = addres.get("line1")
        street2 = addres.get("line2")
        zip_code = addres.get("postal_code")
        country = addres.get("country")
        state = addres.get("state")
        name = order.shipping.name
        phone = order.shipping.phone
        address_to = {
            "name": name,
            "street1": street1,
            "street2": street2,
            "city": city,
            "state": state,
            "zip": zip_code,
            "country": country,
            "phone": phone
            }
        return address_to

    @rpc
    def select_shipping(self, body):
        """Change shipping in Order. Shipping should consist of methods.
        Args:
            order_id (str): uniq number of the product
            shipping_id (str): uniq number of the shipping
        Return:
            order (dict): booking of customer
        """
        order_id = body.get("order_id")
        shipping_id = body.get("shipping_id")
        order = stripe.Order.retrieve(order_id)
        order.selected_shipping_method = shipping_id
        order.save()
        return order

    @rpc
    def pay_order(self, body):
        order_id = body.get("order")
        cart = body.get("cart")
        order = stripe.Order.retrieve(order_id)
        charge = order.pay(source=cart)
        return charge
