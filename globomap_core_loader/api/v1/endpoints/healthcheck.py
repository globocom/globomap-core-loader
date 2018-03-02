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
import flask
import six
from flask_restplus import Resource

from globomap_core_loader.api.facade import LoaderAPIFacade
from globomap_core_loader.api.v2 import api


ns = api.namespace(
    'healthcheck', description='Operations related to updates')


def text(data, code, headers=None):
    return flask.make_response(six.text_type(data))


@ns.route('/')
class Healthcheck(Resource):
    representations = {
        'text/plain': text,
    }

    def get(self):
        deps = list_deps()
        problems = {}
        for key in deps:
            if deps[key].get('status') is False:
                problems.update({key: deps[key]})
        if problems:
            return problems, 503
        return 'WORKING', 200


@ns.route('/deps/')
class HealthcheckDeps(Resource):

    def get(self):
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
