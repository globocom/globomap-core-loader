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
import logging

from globomap_api_client import auth
from globomap_api_client import exceptions
from globomap_api_client.document import Document

from globomap_core_loader.settings import KEYSTONE_PASSWORD
from globomap_core_loader.settings import KEYSTONE_USERNAME


class GloboMapClient(object):

    logger = logging.getLogger(__name__)

    def __init__(self, host):
        self.host = host
        self.generate_auth()

    def generate_auth(self):
        self.logger.info('New Auth')
        self.auth = auth.Auth(
            api_url=self.host,
            username=KEYSTONE_USERNAME,
            password=KEYSTONE_PASSWORD
        )
        self.doc = Document(auth=self.auth)

    def update_element_state(self, action, type, collection, element, key, retries=0):
        try:
            if action.upper() == 'CREATE':
                return self.create(type, collection, element)
            elif action.upper() == 'UPDATE':
                return self.update(type, collection, key, element)
            elif action.upper() == 'PATCH':
                return self.patch(type, collection, key, element)
            elif action.upper() == 'DELETE':
                return self.delete(type, collection, key)
            elif action.upper() == 'CLEAR':
                return self.clear(type, collection, element)

        except exceptions.ValidationError as err:
            self.logger.error(
                'Bad request in send element %s %s %s %s %s' %
                (action, type, collection, element, key)
            )
            raise GloboMapException(err.status_code, err.message)

        except exceptions.Unauthorized as err:
            if retries < 3:
                self.logger.warning(
                    'Retry action %s %s %s %s %s' %
                    (action, type, collection, element, key)
                )
                retries += 1
                self.generate_auth()
                self.update_element_state(
                    action, type, collection, element, key, retries)
            else:
                self.logger.error(
                    'Error send element %s %s %s %s %s' %
                    (action, type, collection, element, key)
                )
                raise GloboMapException(err.status_code, err.message)

        except exceptions.Forbidden as err:
            self.logger.error(
                'Forbbiden send element %s %s %s %s %s' %
                (action, type, collection, element, key)
            )
            raise GloboMapException(err.status_code, err.message)

        except exceptions.ApiError as err:

            if err.status_code in (502, 503) and retries < 3:
                self.logger.warning(
                    'Retry send element %s %s %s %s %s' %
                    (action, type, collection, element, key)
                )
                retries += 1
                self.update_element_state(
                    action, type, collection, element, key, retries)
            else:
                self.logger.error(
                    'Error send element %s %s %s %s %s' %
                    (action, type, collection, element, key)
                )
                raise GloboMapException(err.status_code, err.message)

    def create(self, type, collection, payload):
        try:
            return self.doc.post(type, collection, payload)

        except exceptions.DocumentAlreadyExists:
            self.logger.warning('Element already insered')

    def update(self, type, collection, key, payload):
        try:
            return self.doc.put(type, collection, key, payload)

        except exceptions.NotFound:
            return self.create(type, collection, payload)

    def patch(self, type, collection, key, payload):
        try:
            return self.doc.patch(type, collection, key, payload)

        except exceptions.NotFound:
            return self.create(type, collection, payload)

    def delete(self, type, collection, key):
        try:
            return self.doc.delete(type, collection, key)

        except exceptions.NotFound:
            self.logger.warning('Element %s already deleted' % key)

    def clear(self, type, collection, payload):
        return self.doc.clear(type, collection, payload)


class GloboMapException(Exception):

    def __init__(self, status_code, response):
        self.status_code = status_code
        self.response = response
