# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64
import logging
import uuid

from globomap_core_loader.api.extra_logging import local
from globomap_core_loader.api.extra_logging import NO_REQUEST_CONTEXT
from globomap_core_loader.api.extra_logging import NO_REQUEST_ID
from globomap_core_loader.api.extra_logging import NO_REQUEST_USER
from globomap_core_loader.api.extra_logging import REQUEST_ID_HEADER

logger = logging.getLogger(__name__)


def get_identity():

    identity = uuid.uuid4().bytes
    encoded_id = base64.urlsafe_b64encode(identity)
    safe_id = encoded_id.replace('=', '')

    return safe_id.upper()


def get_driver_name(request):

    driver_name_key = 'HTTP_X_DRIVER_NAME'
    driver_name = NO_REQUEST_CONTEXT

    if driver_name_key in request.META:
        driver_name = request.META.get(driver_name_key)
    return driver_name


class ExtraLoggingMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # local.request_id = get_identity()
        # local.request_path = request.get_full_path()
        # local.request_driver_name = get_driver_name(environ)

        # import pdb; pdb.set_trace()
        return self.app(environ, start_response)

    def process_request(self, request):

        msg = u'Start of request %s. Data: [%s].' % (
            request.method, request.raw_post_data)
        logger.debug(msg)

    def process_response(self, request, response):

        if 399 < response.status_code < 600:
            logger.warning(u'Request finished with failure. Data: [%s].' % (
                request.raw_post_data))
        else:
            logger.debug(u'Request finished with success. Data: [%s].' % (
                request.raw_post_data))

        logger.debug(u'End of request.')

        return response

    def process_exception(self, request, exception):

        logger.exception(u'Unexpected error.')


__all__ = [
    'local',
    'NO_REQUEST_CONTEXT',
    'NO_REQUEST_ID',
    'NO_REQUEST_USER',
    'REQUEST_ID_HEADER',
]
