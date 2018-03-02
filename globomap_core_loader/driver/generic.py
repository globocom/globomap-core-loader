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
import logging

from pika.exceptions import ChannelClosed
from pika.exceptions import ConnectionClosed

from globomap_core_loader.rabbitmq import RabbitMQClient
from globomap_core_loader.settings import GLOBOMAP_RMQ_HOST
from globomap_core_loader.settings import GLOBOMAP_RMQ_PASSWORD
from globomap_core_loader.settings import GLOBOMAP_RMQ_PORT
from globomap_core_loader.settings import GLOBOMAP_RMQ_QUEUE_NAME
from globomap_core_loader.settings import GLOBOMAP_RMQ_USER
from globomap_core_loader.settings import GLOBOMAP_RMQ_VIRTUAL_HOST


class GenericDriver(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self._connect_rabbitmq()

    def _connect_rabbitmq(self):
        self.rabbitmq = RabbitMQClient(
            GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
            GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
        )

    def process_updates(self, callback):
        """
        Reads and processes messages from the GloboMap event bus until
        there's no message left in the target queue. Only acks message if
        processed successfully by the callback.
        """
        while True:
            delivery_tag = None
            try:
                message, delivery_tag = self.rabbitmq.get_message(
                    GLOBOMAP_RMQ_QUEUE_NAME
                )
                if message:
                    callback(message)
                    self.rabbitmq.ack_message(delivery_tag)
                else:
                    return
            except (ConnectionClosed, ChannelClosed):
                self.log.exception(
                    'Error connecting to RabbitMQ, reconnecting')
                self._connect_rabbitmq()
            except:
                self.rabbitmq.nack_message(delivery_tag)
                raise
