import unittest
import json
from datetime import date
from tests.test_base import BaseTestCase, app, db
from model import Feature

MOCK_TITLE = 'Title'
MOCK_DESCRIPTION = 'Description'
MOCK_CLIENT = 'Client C'
MOCK_PRIORITY = 10
MOCK_PRODUCT_AREA = 'Billing'
MOCK_DEADLINE = date.today()

'''Test suite that tests all the functionalities of the Feature Request Tool'''


class IndexViewTests(BaseTestCase):

    def test_request_new_feature(self):
        new_feature = Feature(
            title=MOCK_TITLE,
            description=MOCK_DESCRIPTION,
            client=MOCK_CLIENT,
            priority=MOCK_PRIORITY,
            product_area=MOCK_PRODUCT_AREA,
            deadline=MOCK_DEADLINE,
        )
        db.session.add(new_feature)
        db.session.commit()
        assert new_feature in db.session

    '''Test index page render by querying for submit button'''

    def test_indexpage_render(self):
        response = self.client.get('/')
        self.assertIn('Submit'.encode(), response.data)
        self.assertEqual(response.status_code, 200)

    '''Test AJAX POST call to request a new feature using a valid feature JSON'''

    def test_request_feature_ajax_method(self):
        valid_feature = {
            'title': MOCK_TITLE,
            'description': MOCK_DESCRIPTION,
            'client': MOCK_CLIENT,
            'priority': MOCK_PRIORITY,
            'product_area': MOCK_PRODUCT_AREA,
            'deadline': str(MOCK_DEADLINE),
        }
        expected_response = 'Feature requested. Thank you!'.encode()

        response = self.client.post('/api/v1/feature',
                                    data=json.dumps(valid_feature),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    '''Test AJAX POST call to request a new feature using an invalid feature JSON'''

    def test_add_feature_api_endpoint_POST_returns_error_on_invalid_json(self):
        input_data = 'invalid json'.encode()
        expected_error = '400'.encode()

        response = self.client.post('/api/v1/feature',
                                    data=input_data,
                                    content_type='application/json')
        self.assertIn(expected_error, response.data)

    '''Test AJAX POST call to request a new feature using a feature JSON with missing fields'''

    def test_add_feature_api_endpoint_POST_returns_error_on_missing_item(self):
        invalid_feature = {
            'itle': MOCK_TITLE,
            'escription': MOCK_DESCRIPTION,
            'lient': MOCK_CLIENT,
            'riority': MOCK_PRIORITY,
            'roduct_area': MOCK_PRODUCT_AREA,
            'eadline': str(MOCK_DEADLINE),
        }
        response = self.client.post('/api/v1/feature',
                                    data=json.dumps(invalid_feature),
                                    content_type='application/json')

        self.assertIn("Missing".encode(), response.data)

    '''Test AJAX GET call to query all features from DB'''

    def test_add_feature_api_endpoint_GET_returns_valid_json(self):
        response = self.client.get('/api/v1/feature',
                                   content_type='application/json')
        decoded_json = json.loads(response.data)
        self.assertEqual(type(decoded_json), type([]))


if __name__ == '__main__':
    unittest.main()
