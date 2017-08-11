import json
import unittest
from loader.globomap import GloboMapClient, GloboMapException
from mock import patch, MagicMock
from tests.util import open_json


class TestGloboMapCllient(unittest.TestCase):

    def setUp(self):
        self.globomap_client = GloboMapClient('http://localhost:8080')

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_create_element(self):
        requests_mock = self._mock_request([200])

        payload = open_json('tests/json/globomap/vip.json')
        self.globomap_client.update_element_state(
            'CREATE', 'collections', 'vip', payload, None
        )
        self._assert_request_called(
            requests_mock,
            'POST',
            'http://localhost:8080/collections/vip/',
            payload
        )

    def test_create_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request([500])
            payload = {'name': 'vip.test.com'}
            self.globomap_client.update_element_state(
                'CREATE', 'collections', 'vip', payload, None
            )

            self._assert_request_called(
                requests_mock,
                'POST',
                'http://localhost:8080/collections/vip/',
                payload
            )

    def test_update_element(self):
        payload = open_json('tests/json/globomap/vip.json')
        requests_mock = self._mock_request([200])

        self.globomap_client.update_element_state(
            'UPDATE', 'collections', 'vip', payload, 'globomap_vip.test.com'
        )
        self._assert_request_called(
            requests_mock,
            'PUT',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            payload
        )

    def test_update_element_given_target_element_not_found(self):
        payload = open_json('tests/json/globomap/vip.json')
        requests_mock = self._mock_request([404, 200])

        self.globomap_client.update_element_state(
            'UPDATE', 'collections', 'vip', payload, 'globomap_vip.test.com'
        )
        self._assert_request_called(
            requests_mock,
            'PUT',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            payload
        )
        self._assert_request_called(
            requests_mock,
            'POST',
            'http://localhost:8080/collections/vip/',
            payload
        )

    def test_update_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request([500])
            payload = open_json('tests/json/globomap/vip.json')
            self.globomap_client.update_element_state(
                'UPDATE', 'collections', 'vip',  payload, 'globomap_vip.test.com'
            )

            self._assert_request_called(
                requests_mock,
                'UPDATE',
                'http://localhost:8080/collections/vip/globomap_vip.test.com',
                payload
            )

    def test_patch_element(self):
        payload = open_json('tests/json/globomap/vip.json')
        requests_mock = self._mock_request([200])

        self.globomap_client.update_element_state(
            'PATCH', 'collections', 'vip', payload, 'globomap_vip.test.com'
        )
        self._assert_request_called(
            requests_mock,
            'PATCH',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            payload
        )

    def test_patch_element_given_target_element_not_found(self):
        payload = open_json('tests/json/globomap/vip.json')
        requests_mock = self._mock_request([404, 200])

        self.globomap_client.update_element_state(
            'PATCH', 'collections', 'vip', payload, 'globomap_vip.test.com'
        )
        self._assert_request_called(
            requests_mock,
            'PATCH',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            payload
        )
        self._assert_request_called(
            requests_mock,
            'POST',
            'http://localhost:8080/collections/vip/',
            payload
        )

    def test_patch_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request([500])
            payload = open_json('tests/json/globomap/vip.json')
            self.globomap_client.update_element_state(
                'UPDATE', 'collections', 'vip', payload, 'globomap_vip.test.com'
            )

            self._assert_request_called(
                requests_mock,
                'PATCH',
                'http://localhost:8080/collections/vip/globomap_vip.test.com',
                payload
            )

    def test_delete_element(self):
        requests_mock = self._mock_request([200])
        payload = open_json('tests/json/globomap/vip.json')

        self.globomap_client.update_element_state(
            'DELETE', 'collections', 'vip', payload, 'globomap_vip.test.com'
        )
        self._assert_request_called(
            requests_mock,
            'DELETE',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            None
        )

    def test_delete_element_not_found(self):
        requests_mock = self._mock_request([404])
        payload = open_json('tests/json/globomap/vip.json')

        self.globomap_client.update_element_state(
            'DELETE', 'collections', 'vip', payload, 'globomap_vip.test.com'
        )
        self._assert_request_called(
            requests_mock,
            'DELETE',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            None
        )

    def test_delete_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request([500])
            payload = open_json('tests/json/globomap/vip.json')
            self.globomap_client.update_element_state(
                'DELETE', 'collections', 'vip', payload, 'globomap_vip.test.com'
            )

            self._assert_request_called(
                requests_mock,
                'DELETE',
                'http://localhost:8080/collections/vip/globomap_vip.test.com',
                None
            )

    def _assert_request_called(self, requests_mock, method, url, payload):
        requests_mock.request.assert_any_call(method, url, data=json.dumps(payload))

    def _mock_request(self, status_codes):
        requests_mock = patch('loader.globomap.requests').start()
        responses = [MagicMock(status_code=s, content=None) for s in status_codes]
        requests_mock.request.side_effect = responses
        return requests_mock
