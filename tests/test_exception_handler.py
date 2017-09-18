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
import unittest
from mock import patch, Mock
from pika.exceptions import ConnectionClosed
from loader.loader import UpdateExceptionHandler


class TestExceptionHandler(unittest.TestCase):

    def test_handle_exception_ok(self):
        rabbit_mq_mock = self._mock_rabbit_mq_client([True])
        handler = UpdateExceptionHandler()
        handler.handle_exception('DriverName', {"data": "test"})

        self.assertEqual(1, rabbit_mq_mock.call_count)

    def test_handle_exception_on_connection_error(self):
        rabbit_mq_mock = self._mock_rabbit_mq_client([ConnectionClosed(), True])
        handler = UpdateExceptionHandler()
        handler.handle_exception('DriverName', {"data": "test"})

        self.assertEqual(2, rabbit_mq_mock.call_count)

    def _mock_rabbit_mq_client(self, returns):
        rabbit_mq_mock = patch("loader.loader.RabbitMQClient").start()
        rabbit_mq = Mock()
        rabbit_mq_mock.return_value = rabbit_mq
        rabbit_mq.post_message.side_effect = returns
        return rabbit_mq_mock