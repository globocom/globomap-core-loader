import json
import logging
import unittest
from mock import Mock, patch

from api.app import create_app
from tests.util import open_json


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()

    def test_send_updates(self):
        self._mock_rabbitmq_client(True)
        response = self.app.post(
            '/v1/updates',
            data=json.dumps(open_json('tests/json/driver/driver_output_create.json')),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("1 updates published successfully", json.loads(response.data)["message"])

    def test_send_updates_expected_status_400(self):
        self._mock_rabbitmq_client(False)
        response = self.app.post(
            '/v1/updates',
            data=json.dumps(open_json('tests/json/driver/driver_output_create.json')),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(400, response.status_code)

    def test_send_updates_expected_status_500(self):
        self._mock_rabbitmq_client(Exception())
        response = self.app.post(
            '/v1/updates',
            data=json.dumps(open_json('tests/json/driver/driver_output_create.json')),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(500, response.status_code)

    def _mock_rabbitmq_client(self, data=None):
        rabbit_mq_mock = patch("api.driver_api.get_rabbit_mq_client").start()
        post_message_mock = Mock()
        rabbit_mq_mock.return_value = post_message_mock
        if type(data) is bool:
            post_message_mock.post_message.return_value = data
        else:
            post_message_mock.post_message.side_effect = data
        return post_message_mock