import unittest
from unittest import TestCase
from unittest.mock import patch

import stripe

from payments.rpc.payments import Payments


class TestPayments(TestCase):
    """Testing of payments endpoints"""

    def setUp(self):
        self.sku1 = 'sku_BF2pmCAARtJkIg'
        self.sku2 = 'prod_BF2pHek9EyzO2S'
        self.sku3 = 'prod_BF3PxrZrcpb09X'
        self.payment = Payments()
        self.return_id2 = [{'parent': 'sku_BF2pmCAARtJkIg',
                            'quantity': 2, 'type': 'sku'}]

        self.body = {
                "email": "varvara.malysheva@saritasa.com",
                "phone": "+79994413746",
                "name": "Chloe Taylor",

                "address": {
                           "line1": "1092 Indian Summer Ct",
                           "city": "San Jose",
                           "state": "CA",
                           "country": "US",
                           "postal_code": "95122"
                }
                }
        self.json_body = {'error': {'message': 'Testin exceptions',
                                    'param': 'id',
                                    'type': 'invalid_request_error'}}
        self.exp = stripe.error.InvalidRequestError(
                                                    message="Ooops",
                                                    param="id",
                                                    json_body=self.json_body,
                                                    http_status='400'
                                                    )
        self.order = {"selected_shipping_method": "12gf6fjj_kfs77"}
        self.order_obj = stripe.StripeObject().construct_from(
                              self.order, '')

    def test_get_cart(self):
        """Test method get_cart"""
        self.assertEqual(Payments.get_cart(self.payment), [])
        Payments.add_in_cart(self.payment, self.sku1, 2)
        Payments.add_in_cart(self.payment, self.sku2, 1)
        self.assertNotEqual(Payments.get_cart(self.payment), [])

    def test_add(self):
        """Test added in cart"""
        self.assertNotEqual(Payments.add_in_cart(self.payment,
                                                 self.sku1, 2), [])

    def test_add1(self):
        Payments.add_in_cart(self.payment, self.sku1, 2)
        return_value = [{'parent': 'sku_BDQTnZpwWglI3a',
                        'quantity': 4, 'type': 'sku'}]
        self.assertNotEqual(Payments.add_in_cart(self.payment,
                                                 self.sku1, 2), return_value)

    def test_update(self):
        Payments.add_in_cart(self.payment, self.sku1, 4)
        return_value = [{'parent': 'sku_BDQTnZpwWglI3a',
                        'quantity': 2, 'type': 'sku'}]
        self.assertNotEqual(Payments.update_item(self.payment,
                                                 self.sku1, 2), return_value)

    def test_delete_item(self):
        Payments.add_in_cart(self.payment, self.sku1, 4)
        self.assertEqual(Payments.delete_item(self.payment, self.sku1), [])

    def test_order_validation(self):
        """Check validation parameters for create order"""
        error = {'errors': {'address': ['required field'],
                            'email': ['required field'],
                            'name': ['required field'],
                            'phone': ['required field']
                            }
                 }
        Payments.add_in_cart(self.payment, self.sku1, 2)
        self.assertEqual(Payments.new_order(self.payment, {}), error)
        print("Validation errors check")

    @patch('stripe.Order.create', return_value='200')
    def test_order_create(self, new_order):
        Payments.add_in_cart(self.payment, self.sku1, 2)
        Payments.add_in_cart(self.payment, self.sku2, 1)
        result = self.payment.new_order(self.body)
        self.assertEqual(result.get("response"), '200')
        self.assertIsNone(result.get("errors"))
        self.assertEqual(result.get("phone"), "+79994413746")
        self.assertEqual(result.get("email"), "varvara.malysheva@saritasa.com")
        print("Create order check")

    @patch('stripe.Order.create')
    def test_order_raise(self, raise_order):
        raise_order.side_effect = self.exp
        Payments.add_in_cart(self.payment, self.sku1, 2)
        Payments.add_in_cart(self.payment, self.sku2, 1)
        result = self.payment.new_order(self.body)
        self.assertTrue('message is: Testin exceptions' in
                        result.get("errors"))
        self.assertIsNotNone(result.get("errors"))
        print("Raise order check")

    @patch('stripe.Order.retrieve', return_value='202')
    @patch('stripe.Order.pay', return_value='202')
    def test_pay_order(self, mock_retrive, mock_pay):
        self.assertNotEqual(Payments.pay_order(self.payment, '111',
                                               'tok_visa'), {})
        self.assertTrue(mock_retrive.called)
        self.assertTrue(mock_pay.called)
        print("Paid order check")

    @patch('stripe.Order.retrieve')
    @patch('stripe.Order.save')
    def test_select_shipping(self, mock_save, mock_retrive):
        mock_retrive.return_value = self.order_obj
        mock_save.return_value = {"status": "updated"}
        self.assertEqual(self.payment.select_shipping("adada", "1234hsfd"),
                         {"status": "updated"})
        self.assertTrue(mock_retrive.called)
        self.assertTrue(mock_save.called)
        print("select_shipping check")

    @patch('stripe.Order.retrieve')
    def test_raise_order(self, mock_retrive):
        """Check call raises in pay_order and select_shipping"""
        mock_retrive.side_effect = self.exp
        result_selected = self.payment.select_shipping("adada", "1234hsfd")
        result_pay = self.payment.pay_order("adada", "1234hsfd")
        print(result_pay)
        self.assertTrue('Testin exceptions' in
                        result_selected.get("errors"))
        self.assertTrue('Testin exceptions' in
                        result_pay.get("errors"))
        self.assertTrue(mock_retrive.called)
        print("Raise select_shipping check")

    def test_delete_cart(self):
        """Test checks delete of cart"""
        self.assertEqual(Payments.delete_cart(self.payment), [])

    def tearDown(self):
        """Clear cart after tests"""
        Payments.delete_cart(self.payment)


if __name__ == '__main__':
    unittest.main()
