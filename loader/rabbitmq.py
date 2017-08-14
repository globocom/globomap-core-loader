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
        self.channel.confirm_delivery()

    def post_message(self, exchange_name, key, message):
        return self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=key,
            body=message,
            mandatory=True
        )

    def read_messages(self, queue_name, number_messages=1):
        messages = []
        while True:
            try:
                message = self.get_message(queue_name)
            except StopIteration:
                if messages:
                    yield messages
                break
            else:
                if message:
                    messages.append(message)
                    if len(messages) == number_messages:
                        yield messages
                        messages = []

    def get_message(self, queue_name):
        if not queue_name:
            raise Exception("Queue name must be informed")
        message = self._consumer(queue_name).next()
        if isinstance(message, dict):
            return message

    def _consumer(self, queue_name):
        while True:
            method_frame, _, body = self.channel.basic_get(queue_name)
            if method_frame:
                self.channel.basic_ack(method_frame.delivery_tag)
                yield json.loads(body)
            else:
                break
