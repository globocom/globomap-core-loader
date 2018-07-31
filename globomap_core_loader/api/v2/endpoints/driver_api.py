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

from flask import current_app as app
from flask import request
from flask_restplus import Resource
from jsonspec.validators.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from globomap_core_loader.api import util
from globomap_core_loader.api.facade import LoaderAPIFacade
from globomap_core_loader.api.job import models
from globomap_core_loader.api.v2 import api
from globomap_core_loader.api.v2.auth import permissions
from globomap_core_loader.api.v2.auth.decorators import permission_classes
from globomap_core_loader.api.v2.util import get_dict
from globomap_core_loader.settings import SPECS


ns = api.namespace(
    'updates', description='Operations related to updates')


@ns.route('/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
@api.header(
    'x-driver-name',
    'Name of Driver',
    required=True,
    default=''
)
class Updates(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden'
    })
    @api.expect(api.schema_model('Updates',
                                 get_dict(SPECS.get('updates'))))
    @permission_classes((permissions.Update,))
    def post(self):
        """Post a list of messages."""

        try:
            updates = request.get_json()

            driver_name = request.headers.get('X-DRIVER-NAME', '*')

            job_id = LoaderAPIFacade().publish_updates(updates, driver_name)
            res = {
                'message': 'Updates published successfully',
                'jobid': job_id
            }
            return res, 202, {'Location': '{}/job/{}'.format(request.path, job_id)}

        except ValidationError as error:
            app.logger.exception('Error sending updates to rabbitmq')
            api.abort(400, errors=util.validate(error))
        except BadRequest as err:
            app.logger.exception('Error sending updates to rabbitmq')
            api.abort(400, errors=err.description)
        except:
            app.logger.exception('Error sending updates to rabbitmq')
            res = {'message': 'Error sending updates to queue'}
            return api.abort(500, errors=res)


@ns.route('/job/<job_id>')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class Job(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @permission_classes((permissions.Update,))
    def get(self, job_id):

        job = models.Job.find_by_uuid(job_id)
        if not job:
            res = {'message': 'Job not found'}
            api.abort(404, errors=res)

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
            'driver': job.driver,
            'completed': job.completed,
            'total_update_count': job.updates_count,
            'successful_update_count': job.success_count,
            'error_update_count': job.error_count,
            'date': job.date_time,
            'errors': errors
        }
        return response, 200
