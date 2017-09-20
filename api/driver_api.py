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
from flask import request, abort, jsonify
from werkzeug.exceptions import BadRequest
from api import api
from loader.rabbitmq import RabbitMQClient
from loader.settings import GLOBOMAP_RMQ_HOST
from loader.settings import GLOBOMAP_RMQ_PORT
from loader.settings import GLOBOMAP_RMQ_USER
from loader.settings import GLOBOMAP_RMQ_VIRTUAL_HOST
from loader.settings import GLOBOMAP_RMQ_PASSWORD
from loader.settings import GLOBOMAP_RMQ_EXCHANGE
from loader.settings import GLOBOMAP_RMQ_KEY


log = logging.getLogger(__name__)


@api.route('/updates', methods=['POST'])
def insert_updates():
    try:
        rabbit_mq = get_rabbit_mq_client()

        updates = request.get_json()
        if updates:
            for update in updates:
                event_published = rabbit_mq.post_message(
                    GLOBOMAP_RMQ_EXCHANGE,
                    GLOBOMAP_RMQ_KEY,
                    json.dumps(update)
                )

                if not event_published:
                    log.error("Error publishing update %s" % update)
                    return abort(400)

        return jsonify({
            "message": "%s updates published successfully" % len(updates or [])
        })
    except Exception, e:
        if type(e) is BadRequest:
            raise e
        log.exception("Error sending updates to rabbitmq")
        abort(500)


def get_rabbit_mq_client():
    return RabbitMQClient(
        GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
        GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
    )
