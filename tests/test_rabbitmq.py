import unittest
from mock import patch, MagicMock
from loader.rabbitmq import RabbitMQClient


class TestRabbitMQClient(unittest.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_get_message(self):
        pika_mock = self._mock_pika('{"action": "CREATE", "type": "vip", "element": {}}')
        rabbitmq = RabbitMQClient('localhost', 5672, 'user', 'password', '/')

        message = rabbitmq.get_message('queue_name')

        self.assertIsNotNone(message)
        pika_mock.basic_get.assert_called_once_with('queue_name')

    def test_expected_exception(self):
        self._mock_pika(None)
        rabbitmq = RabbitMQClient('localhost', 5672, 'user', 'password', '/')

        try:
            rabbitmq.get_message(None)
        except Exception, e:
            self.assertEqual("Queue name must be informed", e.message)

    def test_post_message(self):
        pika_mock = self._mock_pika(None)
        rabbitmq = RabbitMQClient('localhost', 5672, 'user', 'password', '/')
        rabbitmq.post_message('exchange', 'key', 'message')

        pika_mock.basic_publish.assert_called_once_with(
            body='message', exchange='exchange',
            routing_key='key',
            mandatory=True
        )

    def _mock_pika(self, message):
        pika_mock = patch('loader.rabbitmq.pika').start()
        pika_mock.ConnectionParameters.return_value = MagicMock()
        connection_mock = MagicMock()
        channel_mock = MagicMock()
        connection_mock.channel.return_value = channel_mock
        pika_mock.BlockingConnection.return_value = connection_mock
        channel_mock.basic_get.return_value = (MagicMock(), None, message)
        return channel_mock