import unittest
from loader.globomap import GloboMapClient, GloboMapException
from mock import patch, MagicMock
from tests.util import open_json, as_json


class TestGloboMapCllient(unittest.TestCase):

    def setUp(self):
        self.globomap_client = GloboMapClient('http://localhost:8080')

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_create_element(self):
        requests_mock = self._mock_request({"key": "globomap_key"}, 201)

        payload = open_json('tests/json/globomap/create_vip.json')
        self.assertIsNotNone(self.globomap_client.create('collections', 'vip', payload))
        requests_mock.request.assert_called_once_with('POST', 'http://localhost:8080/collections/vip/', data=payload)

    def test_create_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            self._mock_request({"id": 1}, 500)
            self.globomap_client.create('collections', 'vip', {'name': 'vip.test.com'})

    def test_update_element(self):
        payload = open_json('tests/json/globomap/update_vip.json')
        requests_mock = self._mock_request(as_json(payload), 200)

        self.assertIsNotNone(self.globomap_client.update('collections', 'vip', "globomap_vip.test.com", payload))
        requests_mock.request.assert_called_once_with('PUT', 'http://localhost:8080/collections/vip/globomap_vip.test.com', data=payload)

    def test_update_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            self._mock_request({"id": 1}, 500)
            payload = open_json('tests/json/globomap/create_vip.json')
            self.globomap_client.update('collections', 'vip', 1, payload)

    def test_patch_element(self):
        payload = open_json('tests/json/globomap/update_vip.json')
        requests_mock = self._mock_request(as_json(payload), 200)

        self.assertIsNotNone(self.globomap_client.patch('collections', 'vip', "globomap_vip.test.com", payload))
        requests_mock.request.assert_called_once_with('PATCH', 'http://localhost:8080/collections/vip/globomap_vip.test.com', data=payload)

    def test_patch_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            self._mock_request({"id": 1}, 500)
            payload = open_json('tests/json/globomap/create_vip.json')
            self.globomap_client.patch('collections', 'vip', 1, payload)

    def test_delete_element(self):
        requests_mock = self._mock_request(None, 200)

        self.assertIsNone(self.globomap_client.delete('collections', 'vip', 'globomap_vip.test.com'))
        requests_mock.request.assert_called_once_with('DELETE', 'http://localhost:8080/collections/vip/globomap_vip.test.com', data=None)

    def test_delete_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            self._mock_request(None, 500)
            self.globomap_client.delete('collections', 'vip', 'globomap_vip.test.com')

    def _mock_request(self, content, status=200):
        requests_mock = patch('loader.globomap.requests').start()
        response_mock = MagicMock(status_code=status, content=as_json(content))
        requests_mock.request.return_value = response_mock
        return requests_mock
