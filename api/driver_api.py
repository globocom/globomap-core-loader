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

from flask import abort
from flask import jsonify
from flask import request
from jsonspec.validators.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from api import api
from api import decorators
from api import util
from loader.rabbitmq import RabbitMQClient
from loader.settings import GLOBOMAP_RMQ_EXCHANGE
from loader.settings import GLOBOMAP_RMQ_HOST
from loader.settings import GLOBOMAP_RMQ_KEY
from loader.settings import GLOBOMAP_RMQ_PASSWORD
from loader.settings import GLOBOMAP_RMQ_PORT
from loader.settings import GLOBOMAP_RMQ_USER
from loader.settings import GLOBOMAP_RMQ_VIRTUAL_HOST
from loader.settings import SPECS


log = logging.getLogger(__name__)


@api.route('/updates', methods=['POST'])
@decorators.json_response
def insert_updates():
    try:
        rabbit_mq = get_rabbit_mq_client()
        updates = request.get_json()
        spec = SPECS.get('updates')
        util.json_validate(spec).validate(updates)

        driver_name = request.headers.get('X-DRIVER-NAME', '*')

        if updates:
            for update in updates:
                update.update({'driver_name': driver_name})
                event_published = rabbit_mq.post_message(
                    GLOBOMAP_RMQ_EXCHANGE,
                    GLOBOMAP_RMQ_KEY,
                    json.dumps(update)
                )

                if not event_published:
                    log.error('Error publishing update %s' % update)
                    res = {'message': 'Error publishing update'}
                    return res, 400

        res = {'message': '%s updates published successfully' %
               len(updates or [])}
        return res, 200

    except ValidationError as error:

        res = util.validate(error)
        log.exception('Error sending updates to rabbitmq')
        return res, 400

    except Exception as e:

        if type(e) is BadRequest:
            return str(e), 400
        log.exception('Error sending updates to rabbitmq')
        res = {'message': 'Error sending updates to rabbitmq'}
        return res, 500


def get_rabbit_mq_client():
    return RabbitMQClient(
        GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
        GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
    )
