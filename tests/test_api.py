import unittest
from unittest import TestCase
from payments.rpc.payments import Payments
import stripe


class TestPayments(TestCase):

    def setUp(self):
        self.id1 = 'prod_BDQT7ifqt1FFc1'
        self.id2 = 'prod_BF2pHek9EyzO2S'
        self.id3 = 'prod_BF3PxrZrcpb09X'
        self.payment = Payments()
        self.api_key = "sk_test_K5QUkUgvUNKvDD9fEGYBI6Gi"
        self.return_id2 = [{'parent': 'sku_BF2pmCAARtJkIg',
                            'quantity': 2, 'type': 'sku'}]

    def test_get_cart(self):
        self.assertEqual(Payments.get_cart(self.payment), [])

    def test_add(self):
        self.assertNotEqual(Payments.add_in_cart(self.payment,
                                                 self.id1, 2), [])

    def test_add1(self):
        Payments.add_in_cart(self.payment, self.id1, 2)
        return_value = [{'parent': 'sku_BDQTnZpwWglI3a', 'quantity': 4, 'type': 'sku'}]
        self.assertEqual(Payments.add_in_cart(self.payment,
                                              self.id1, 2), return_value)

    def test_delete_cart(self):
        self.assertEqual(Payments.delete_cart(self.payment), [])

    def tearDown(self):
        Payments.delete_cart(self.payment)



if __name__ == '__main__':
    unittest.main()
