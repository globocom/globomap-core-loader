"""
   Copyright 2017 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import json
import unittest

from mock import MagicMock
from mock import Mock
from mock import patch

from loader.globomap import GloboMapClient
from loader.globomap import GloboMapException
from tests.util import open_json


class TestGloboMapCllient(unittest.TestCase):

    def setUp(self):
        patch('loader.globomap.Session').start()
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
            {'Content-Type': 'application/json'},
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
                'http://localhost:8080/collections/vip',
                {'Content-Type': 'application/json'},
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
            'http://localhost:8080/collections/vip/globomap_vip.test.com/',
            {'Content-Type': 'application/json'},
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
            'http://localhost:8080/collections/vip/globomap_vip.test.com/',
            {'Content-Type': 'application/json'},
            payload
        )
        self._assert_request_called(
            requests_mock,
            'POST',
            'http://localhost:8080/collections/vip/',
            {'Content-Type': 'application/json'},
            payload
        )

    def test_update_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request([500])
            payload = open_json('tests/json/globomap/vip.json')
            self.globomap_client.update_element_state(
                'UPDATE', 'collections', 'vip', payload, 'globomap_vip.test.com'
            )

            self._assert_request_called(
                requests_mock,
                'UPDATE',
                'http://localhost:8080/collections/vip/globomap_vip.test.com',
                {'Content-Type': 'application/json'},
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
            'http://localhost:8080/collections/vip/globomap_vip.test.com/',
            {'Content-Type': 'application/json'},
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
            'http://localhost:8080/collections/vip/globomap_vip.test.com/',
            {'Content-Type': 'application/json'},
            payload
        )
        self._assert_request_called(
            requests_mock,
            'POST',
            'http://localhost:8080/collections/vip/',
            {'Content-Type': 'application/json'},
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
                {'Content-Type': 'application/json'},
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
            'http://localhost:8080/collections/vip/globomap_vip.test.com/'
        )

    def test_clear_element(self):
        requests_mock = self._mock_request([200])
        payload = [[{
            'operator': '<',
            'field': 'timestamp',
            'value': 1511296003
        }]]
        self.globomap_client.update_element_state(
            'CLEAR', 'collections', 'vip', payload, None
        )
        self._assert_request_called(
            requests_mock,
            'POST',
            'http://localhost:8080/collections/vip/clear/',
            {'Content-Type': 'application/json'},
            payload
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
            'http://localhost:8080/collections/vip/globomap_vip.test.com/'
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
                'http://localhost:8080/collections/vip/globomap_vip.test.com/'
            )

    def test_retry_http_request_on_status_503(self):
        requests_mock = self._mock_request([503, 200])

        payload = open_json('tests/json/globomap/vip.json')
        self.globomap_client.update_element_state(
            'CREATE', 'collections', 'vip', payload, None
        )

        self.assertEqual(2, requests_mock.call_count)

    def test_retry_http_request_on_status_409(self):
        requests_mock = self._mock_request([409])

        payload = open_json('tests/json/globomap/vip.json')
        self.globomap_client.update_element_state(
            'CREATE', 'collections', 'vip', payload, None
        )

        self.assertEqual(1, requests_mock.call_count)

    def test_retry_http_request_on_status_400(self):
        requests_mock = self._mock_request([400])

        with self.assertRaises(GloboMapException):
            payload = open_json('tests/json/globomap/vip.json')
            self.globomap_client.update_element_state(
                'CREATE', 'collections', 'vip', payload, None
            )
            self.assertEqual(1, requests_mock.call_count)

    def test_retry_http_request_on_status_503_failed_after_three_retries(self):
        requests_mock = self._mock_request([503, 503, 503])

        try:
            payload = open_json('tests/json/globomap/vip.json')
            self.globomap_client.update_element_state(
                'CREATE', 'collections', 'vip', payload, None
            )
        except GloboMapException, e:
            self.assertEqual(503, e.status_code)
            self.assertEqual(3, requests_mock.call_count)

    def _assert_request_called(self, requests_mock, method, url, headers=None, payload=None):
        requests_mock.assert_any_call(
            method, url, headers=headers, data=json.dumps(payload))

    def _mock_request(self, status_codes):
        self.globomap_client.session = Mock()
        self.globomap_client.session.request = Mock()

        responses = [MagicMock(status_code=s, content=None)
                     for s in status_codes]

        self.globomap_client.session.request.side_effect = responses
        return self.globomap_client.session.request
