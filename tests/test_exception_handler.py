import unittest
from mock import patch, Mock
from pika.exceptions import ConnectionClosed
from loader.loader import UpdateExceptionHandler


class TestExceptionHandler(unittest.TestCase):

    def test_handle_exception_ok(self):
        rabbit_mq_mock = self._mock_rabbit_mq_client([True])
        handler = UpdateExceptionHandler()
        handler.handle_exception({"data": "test"})

        self.assertEqual(1, rabbit_mq_mock.call_count)

    def test_handle_exception_on_connection_error(self):
        rabbit_mq_mock = self._mock_rabbit_mq_client([ConnectionClosed(), True])
        handler = UpdateExceptionHandler()
        handler.handle_exception({"data": "test"})

        self.assertEqual(2, rabbit_mq_mock.call_count)

    def _mock_rabbit_mq_client(self, returns):
        rabbit_mq_mock = patch("loader.loader.RabbitMQClient").start()
        rabbit_mq = Mock()
        rabbit_mq_mock.return_value = rabbit_mq
        rabbit_mq.post_message.side_effect = returns
        return rabbit_mq_mock