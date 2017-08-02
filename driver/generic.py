import logging

from rabbitmq.client import RabbitMQClient
from settings import GLOBOMAP_RMQ_USER, GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_HOST, \
    GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_VIRTUAL_HOST, GLOBOMAP_RMQ_QUEUE_NAME


class GenericDriver(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self.rabbit_mq = RabbitMQClient(
            GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
            GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
        )

    def updates(self, number_messages=1):
        self.log.debug("Reading %s updates" % number_messages)
        yield self.rabbit_mq.read_messages(GLOBOMAP_RMQ_QUEUE_NAME, number_messages).next()
