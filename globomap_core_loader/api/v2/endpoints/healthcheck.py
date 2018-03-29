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
import flask
import six
from flask import current_app as app
from flask_restplus import Resource

from globomap_core_loader.api.facade import LoaderAPIFacade
from globomap_core_loader.api.v2 import api
from globomap_core_loader.api.v2.auth.facade import Auth


ns = api.namespace(
    'healthcheck', description='Operations related to updates')


def text(data, code, headers=None):
    return flask.make_response(six.text_type(data))


@ns.route('/')
class Healthcheck(Resource):
    representations = {
        'text/plain': text,
    }

    @api.doc(responses={
        200: 'Success',
        503: 'Service Unavailable',
    })
    def get(self):
        deps = _list_deps()
        problems = {}
        for key in deps:
            if deps[key].get('status') is False:
                problems.update({key: deps[key]})
        if problems:
            app.logger.error(problems)
            self.representations = {}
            return problems, 503
        return 'WORKING', 200


@ns.route('/deps/')
class HealthcheckDeps(Resource):

    @api.doc(responses={200: 'Success'})
    def get(self):
        deps = _list_deps()
        return deps, 200


def _is_rabbitmq_ok():
    try:
        LoaderAPIFacade()
    except:
        status = {'status': False}
    else:
        status = {'status': True}

    return status


def _is_auth_ok():
    auth_inst = Auth()

    status = True
    if auth_inst.is_enable():
        status = auth_inst.is_url_ok()

    status = {
        'status': status
    }

    return status


def _list_deps():
    deps = {
        'auth': _is_auth_ok(),
        'rabbitmq': _is_rabbitmq_ok()
    }

    return deps
