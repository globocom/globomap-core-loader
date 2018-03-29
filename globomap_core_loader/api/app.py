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
from logging import config

from flask import Flask

from globomap_core_loader.api.database import Session
from globomap_core_loader.api.v1.api import blueprint as api_v1
from globomap_core_loader.api.v2.api import blueprint as api_v2
from globomap_core_loader.settings import LOGGING
# from globomap_core_loader.api.middlewares.extra_logging import ExtraLoggingMiddleware


def create_app():

    app = Flask(__name__)
    app.config['LOGGER_HANDLER_POLICY'] = 'default'
    app.config['LOGGER_NAME'] = 'api'
    app.config['BUNDLE_ERRORS'] = True
    app.config.from_object('globomap_core_loader.settings')
    app.logger
    config.dictConfig(LOGGING)

    # app.wsgi_app = ExtraLoggingMiddleware(app.wsgi_app)

    app.register_blueprint(api_v1)
    app.register_blueprint(api_v2)

    # @app.before_request
    # def log_request_info():
    #     get_identity()
    #     app.logger.debug('Headers: %s', request.headers)
    #     app.logger.debug('Body: %s', request.get_data())

    @app.before_request
    def create_session():
        Session()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()
        if exception and Session.is_active:
            Session.rollback()

    return app
