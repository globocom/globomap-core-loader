"""
   Copyright 2018 Globo.com

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

from globomap_core_loader.api.job.models import Job
from globomap_core_loader.rabbitmq import RabbitMQClient
from globomap_core_loader.settings import GLOBOMAP_RMQ_EXCHANGE
from globomap_core_loader.settings import GLOBOMAP_RMQ_HOST
from globomap_core_loader.settings import GLOBOMAP_RMQ_KEY
from globomap_core_loader.settings import GLOBOMAP_RMQ_PASSWORD
from globomap_core_loader.settings import GLOBOMAP_RMQ_PORT
from globomap_core_loader.settings import GLOBOMAP_RMQ_USER
from globomap_core_loader.settings import GLOBOMAP_RMQ_VIRTUAL_HOST


logger = logging.getLogger(__name__)


class LoaderAPIFacade(object):

    def __init__(self):
        self.rabbitmq = self._get_rabbit_mq_client()

    def _get_rabbit_mq_client(self):
        return RabbitMQClient(
            GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
            GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
        )

    def publish_updates(self, updates, driver_name, job_controller):
        if updates:
            try:
                if job_controller is True:
                    job = Job(driver_name, len(updates))
                    for update in updates:
                        update.update({
                            'driver_name': driver_name,
                            'jobid': job.uuid
                        })
                        self.rabbitmq.post_message(
                            GLOBOMAP_RMQ_EXCHANGE, GLOBOMAP_RMQ_KEY,
                            json.dumps(update, ensure_ascii=False), False
                        )

                    job.save()
                    self.rabbitmq.confirm_publish()
                    return job.uuid
                else:
                    for update in updates:
                        update.update({
                            'driver_name': driver_name
                        })
                        self.rabbitmq.post_message(
                            GLOBOMAP_RMQ_EXCHANGE, GLOBOMAP_RMQ_KEY,
                            json.dumps(update, ensure_ascii=False), False
                        )
                    self.rabbitmq.confirm_publish()
                    return None
            except:
                logger.exception('Error publishing to rabbitmq')
                self.rabbitmq.discard_publish()
                raise Exception('Failed to sendo updates to queue')
