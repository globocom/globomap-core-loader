import unittest
from mock import patch, Mock
from driver.generic import GenericDriver
from tests.util import open_json


class TestGenericDriver(unittest.TestCase):

    def test_get_updates_returning_empty_updates(self):
        self._mock_rabbitmq_client([])
        self.assertEqual([], GenericDriver().updates())

    def test_get_updates_returning_list_of_updates(self):
        updates = [open_json('tests/json/globomap/vip.json')]
        self._mock_rabbitmq_client(updates)
        self.assertEqual(updates, GenericDriver().updates())

    def _mock_rabbitmq_client(self, messages):
        rabbit_mq_mock = patch("driver.generic.RabbitMQClient").start()
        rabbit_mq = Mock()
        rabbit_mq_mock.return_value = rabbit_mq
        read_messages_mock = Mock()
        read_messages_mock.next.return_value = messages
        rabbit_mq.read_messages.return_value = read_messages_mock
        return rabbit_mq_mock
