import unittest
from loader.globomap import GloboMapClient, GloboMapException
from mock import patch, MagicMock


class TestGloboMapCllient(unittest.TestCase):

    def setUp(self):
        self.globomap_client = GloboMapClient('http://localhost:8080/api')

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_create_element(self):
        requests_mock = self._mock_request('{"id": 1}', 201)

        payload = {'name': 'vip.test.com'}
        self.assertIsNotNone(self.globomap_client.create('vip', payload))
        requests_mock.request.assert_called_once_with('POST', 'http://localhost:8080/api/vip/', data=payload)

    def test_create_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            self._mock_request('{"id": 1}', 500)
            self.globomap_client.create('vip', {'name': 'vip.test.com'})

    def test_update_element(self):
        requests_mock = self._mock_request('{"id": 1, "name": "vip.test.com"}', 200)

        payload = {'id': 1, 'name': 'vip.test.com'}
        self.assertIsNotNone(self.globomap_client.update('vip', 1, payload))
        requests_mock.request.assert_called_once_with('PUT', 'http://localhost:8080/api/vip/1', data=payload)

    def test_update_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            self._mock_request('{"id": 1}', 500)
            self.globomap_client.update('vip', 1, {'name': 'vip.test.com'})

    def test_delete_element(self):
        requests_mock = self._mock_request(None, 200)

        self.assertIsNone(self.globomap_client.delete('vip', 1))
        requests_mock.request.assert_called_once_with('DELETE', 'http://localhost:8080/api/vip/1', data=None)

    def test_delete_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            self._mock_request(None, 500)
            self.globomap_client.delete('vip', 1)

    def _mock_request(self, content, status=200):
        requests_mock = patch('loader.globomap.requests').start()
        response_mock = MagicMock(status_code=status, content=content)
        requests_mock.request.return_value = response_mock
        return requests_mock
