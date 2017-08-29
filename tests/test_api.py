import unittest
from unittest import TestCase
from unittest.mock import patch

from payments.rpc.payments import Payments


class TestPayments(TestCase):
    """Testing of payments endpoints"""

    def setUp(self):
        self.id1 = 'prod_BDQT7ifqt1FFc1'
        self.id2 = 'prod_BF2pHek9EyzO2S'
        self.id3 = 'prod_BF3PxrZrcpb09X'
        self.payment = Payments()
        self.return_id2 = [{'parent': 'sku_BF2pmCAARtJkIg',
                            'quantity': 2, 'type': 'sku'}]

        self.body = {'address': {
                                "line1": '1234 Main Street',
                                "city": 'San Francisco',
                                "state": 'CA',
                                "country": 'US',
                                "postal_code": '94111'
                                },
                     'email': 'test_email',
                     'name': 'Vasz pupkin',
                     'phone': '+7889955778'}

    def test_order2(self):
        result = Payments.new_order(self.payment, self.body)
        self.assertIsNotNone(result.get('errors'))

    def test_get_cart(self):
        """Test method get_cart"""
        self.assertEqual(Payments.get_cart(self.payment), [])
        Payments.add_in_cart(self.payment, self.id1, 2)
        Payments.add_in_cart(self.payment, self.id2, 1)
        self.assertNotEqual(Payments.get_cart(self.payment), [])

    def test_add(self):
        """Test added in cart"""
        self.assertNotEqual(Payments.add_in_cart(self.payment,
                                                 self.id1, 2), [])

    def test_add1(self):
        Payments.add_in_cart(self.payment, self.id1, 2)
        return_value = [{'parent': 'sku_BDQTnZpwWglI3a', 'quantity': 4, 'type': 'sku'}]
        self.assertEqual(Payments.add_in_cart(self.payment,
                                              self.id1, 2), return_value)

    def test_update(self):
        Payments.add_in_cart(self.payment, self.id1, 4)
        return_value = [{'parent': 'sku_BDQTnZpwWglI3a', 'quantity': 2, 'type': 'sku'}]
        self.assertEqual(Payments.update_item(self.payment,
                                              self.id1, 2), return_value)

    def test_delete_item(self):
        Payments.add_in_cart(self.payment, self.id1, 4)
        self.assertEqual(Payments.delete_item(self.payment, self.id1), [])

    #@patch('payments.rpc.payments.Payments.new_order', return_value = {})
    def test_order(self):
        error = {'errors': {'address': ['required field'],
                            'email': ['required field'],
                            'name': ['required field'],
                            'phone': ['required field']
                            }
                 }
        Payments.add_in_cart(self.payment, self.id1, 2)
        Payments.add_in_cart(self.payment, self.id2, 1)
        self.assertEqual(Payments.new_order(self.payment, {}), error)

    @patch('payments.rpc.payments.Payments.new_order', return_value='202')
    def test_order1(self, new_order):
        Payments.add_in_cart(self.payment, self.id1, 2)
        Payments.add_in_cart(self.payment, self.id2, 1)
        self.assertEqual(new_order(self.body), '202')

    def test_pay_order(self):
        message_error = {"errors": 'Status is: 404, message is: No such order: 111'}
        self.assertNotEqual(Payments.pay_order(self.payment, '111',
                                               'tok_visa'), {})
        self.assertEqual(Payments.pay_order(self.payment, '111', 'tok_visa'),
                         message_error
                         )

    def test_delete_cart(self):
        """Test checks delete of cart"""
        self.assertEqual(Payments.delete_cart(self.payment), [])

    def tearDown(self):
        """Clear cart after tests"""
        Payments.delete_cart(self.payment)


if __name__ == '__main__':
    unittest.main()
