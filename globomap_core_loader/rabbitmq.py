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

import pika


class RabbitMQClient(object):

    def __init__(self, host, port, user, password, vhost):
        credentials = pika.PlainCredentials(user, password)
        parameters = pika.ConnectionParameters(
            host=host, port=port,
            virtual_host=vhost, credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def get_message(self, queue):
        method_frame, _, body = self.channel.basic_get(queue)
        if body:
            body = json.loads(body)
            return body, method_frame.delivery_tag
        else:
            return None, None

    def ack_message(self, delivery_tag):
        self.channel.basic_ack(delivery_tag)

    def nack_message(self, delivery_tag):
        self.channel.basic_nack(delivery_tag)

    def post_message(self, exchange_name, key, message, confirm=True):
        self.channel.tx_select()
        published = self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=key,
            body=message,
            mandatory=True
        )
        if published and confirm:
            self.confirm_publish()
        return confirm

    def confirm_publish(self):
        self.channel.tx_commit()

    def discard_publish(self):
        self.channel.tx_rollback()
