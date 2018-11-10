from flask import Flask
from copy import deepcopy
import unittest
import json

from app import app
from app.api.v1 import models

BASE_URL = "http://127.0.0.1:5000/api/v1/parcels"
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/2'.format(BASE_URL)


class TestConfig(unittest.TestCase):

    def create_app(self):
        app.config.from_object("instance.config.TestConfig")
        return app

    def setUp(self):
        self.backup_order = deepcopy(models.parcels)
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/api/v1', content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'crackers ni wale wase', response.data)

    def test_get_all_parcel_orders(self):
        response = self.app.get(BASE_URL, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Geforce GTX 1060 iGame', response.data)
        self.assertEqual(len(models.parcels), 3)

    def test_particular_parcel_order(self):
        response = self.app.get("/api/v1/parcels/1")
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_delivery_orders(self):
        response = self.app.get(
            '/api/v1/users/1/parcels',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_post_order(self):
        order = {
            'id': 4,
            'owner_id': 1,
            'item_name': 'Geforce GTX 1040 ti',
            'origin': 'nairobi cbd',
            'pickup_location': 'zimmerman base',
            'price': 105000,
            'status': 'in transit'
        }
        response = self.app.post(BASE_URL,
                                 data=json.dumps(order),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_not_exist(self):
        response = self.app.get(BAD_ITEM_URL)
        self.assertEqual(response.status_code, 404)

    def test_cancel_for_already_cancelled_order(self):
        order = {
            'id': 3,
            'owner_id': 1,
            'item_name': 'Geforce GTX 1040 ti',
            'origin': 'nairobi cbd',
            'pickup_location': 'zimmerman base',
            'price': 105000,
            'status': 'cancelled'
        }
        response = self.app.put(
            '/api/v1/parcels/3/cancel',
            data=json.dumps(order),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'order has already been cancelled', response.data)

    def test_cancel_for_already_delivered_order(self):
        order = {
            'id': 3,
            'owner_id': 1,
            'item_name': 'Geforce GTX 1040 ti',
            'origin': 'nairobi cbd',
            'pickup_location': 'zimmerman base',
            'price': 105000,
            'status': 'cancelled'
        }
        response = self.app.put(
            '/api/v1/parcels/1/cancel',
            data=json.dumps(order),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'order has already been delivered', response.data)

    def test_valid_cancel_order(self):
        order = {
            'id': 2,
            'owner_id': 2,
            'item_name': 'Geforce GTX 1080 ti',
            'origin': 'nairobi cbd',
            'pickup_location': 'zimmerman base',
            'price': 105000,
            'status': 'in transit'
        }
        response = self.app.put(
            '/api/v1/parcels/2/cancel',
            data=json.dumps(order),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'cancelled', response.data)


if __name__ == "__main__":
    unittest.main()
