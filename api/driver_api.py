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

from flask import jsonify
from flask import request
from jsonspec.validators.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from api import api
from api import decorators
from api import util
from api.facade import LoaderAPIFacade
from api.job.models import Job
from loader.settings import SPECS


log = logging.getLogger(__name__)


@api.route('/updates', methods=['POST'])
@decorators.json_response
def insert_updates():
    try:
        updates = request.get_json()
        if not updates or len(updates) == 0:
            raise BadRequest('Invalid empty request')

        spec = SPECS.get('updates')
        util.json_validate(spec).validate(updates)
        driver_name = request.headers.get('X-DRIVER-NAME', '*')

        job_id = LoaderAPIFacade().publish_updates(updates, driver_name)
        res = {
            'message': 'Updates published successfully',
            'jobid': job_id
        }
        return res, 202, {'Location': '{}/job/{}'.format(request.path, job_id)}
    except ValidationError as error:
        log.exception('Error sending updates to rabbitmq')
        return util.validate(error), 400
    except BadRequest as e:
        return str(e.description), 400
    except Exception as e:
        log.exception('Error sending updates to rabbitmq')
        res = {'message': 'Error sending updates to queue'}
        return res, 500


@api.route('/updates/job/<job_id>', methods=['GET'])
@decorators.json_response
def get_job(job_id):
    job = Job.find_by_uuid(job_id)
    if not job:
        return {'message': 'Job not found'}, 404

    errors = []
    for error in job.errors:
        error_response = error.response
        try:
            error_response = json.loads(error.response)
        except:
            pass

        errors.append({
            'request': json.loads(error.request_body),
            'response': error_response,
            'status_code': error.status_code
        })

    response = {
        'uuid': job_id,
        'completed': job.completed,
        'total_update_count': job.updates_count,
        'successful_update_count': job.success_count,
        'error_update_count': job.error_count,
        'date': job.date_time,
        'errors': errors
    }
    return response, 200


@api.route('/healthcheck', methods=['GET'])
def healthcheck():
    deps = list_deps()
    problems = {}
    for key in deps:
        if deps[key].get('status') is False:
            problems.update({key: deps[key]})
    if problems:
        return jsonify(problems), 503
    return 'WORKING', 200


@api.route('/healthcheck/deps', methods=['GET'])
@decorators.json_response
def healthcheck_deps():
    deps = list_deps()
    return deps, 200


def list_deps():
    deps = {
        'rabbitmq': {}
    }
    try:
        LoaderAPIFacade()
    except:
        deps['rabbitmq']['status'] = False
    else:
        deps['rabbitmq']['status'] = True

    return deps
