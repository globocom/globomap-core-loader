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
import logging

from api.job.models import Job
from loader.rabbitmq import RabbitMQClient
from loader.settings import GLOBOMAP_RMQ_EXCHANGE
from loader.settings import GLOBOMAP_RMQ_HOST
from loader.settings import GLOBOMAP_RMQ_KEY
from loader.settings import GLOBOMAP_RMQ_PASSWORD
from loader.settings import GLOBOMAP_RMQ_PORT
from loader.settings import GLOBOMAP_RMQ_USER
from loader.settings import GLOBOMAP_RMQ_VIRTUAL_HOST


class LoaderAPIFacade(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self.rabbitmq = self._get_rabbit_mq_client()

    def _get_rabbit_mq_client(self):
        return RabbitMQClient(
            GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
            GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
        )

    def publish_updates(self, updates, driver_name):
        if updates:
            try:
                job = Job(driver_name, len(updates))
                for update in updates:
                    update.update(
                        {'driver_name': driver_name, 'jobid': job.uuid}
                    )

                    self.rabbitmq.post_message(
                        GLOBOMAP_RMQ_EXCHANGE, GLOBOMAP_RMQ_KEY,
                        json.dumps(update), False
                    )

                self.rabbitmq.confirm_publish()
                job.save()
                return job.uuid
            except:
                self.log.exception("Error publishing to rabbitmq")
                self.rabbitmq.discard_publish()
                raise Exception("Failed to sendo updates to queue")
