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

from requests import Session


class GloboMapClient(object):

    log = logging.getLogger(__name__)

    def __init__(self, host):
        self.host = host
        self.session = Session()

    def update_element_state(self, action, type, collection, element, key):
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

    def create(self, type, collection, payload):
        return self._make_request(
            'POST', self._build_uri(type, collection), {
                'Content-Type': 'application/json'}, payload
        )

    def update(self, type, collection, key, payload):
        try:
            return self._make_request(
                'PUT', self._build_uri(type, collection, key), {
                    'Content-Type': 'application/json'}, payload
            )
        except ElementNotFoundException:
            return self.create(type, collection, payload)

    def patch(self, type, collection, key, payload):
        try:
            return self._make_request(
                'PATCH', self._build_uri(type, collection, key), {
                    'Content-Type': 'application/json'}, payload
            )
        except ElementNotFoundException:
            return self.create(type, collection, payload)

    def delete(self, type, collection, key):
        try:
            return self._make_request(
                'DELETE', self._build_uri(type, collection, key)
            )
        except ElementNotFoundException:
            self.log.debug('Element %s already deleted' % key)

    def list(self, type, collection, keys=None):
        keys = keys if keys else []
        return self._make_request(
            'GET', self._build_uri(type, collection, ';'.join(keys))
        )

    def get(self, collection, key):
        elements = self.list(collection, [key])
        if elements:
            return elements[0]

    def clear(self, type, collection, payload):
        path = '{}/clear'.format(collection)
        return self._make_request(
            'POST', self._build_uri(type, path), {
                'Content-Type': 'application/json'}, payload
        )

    def _make_request(self, method, uri,
                      headers=None, data=None, retry_count=0):
        request_url = '%s%s' % (self.host, uri)

        self._log_http('REQUEST', method, request_url, headers, data)

        response = self.session.request(
            method,
            request_url,
            headers=headers,
            data=json.dumps(data)
        )
        status = response.status_code
        content = response.content

        self._log_http('RESPONSE', method, request_url, content, status)

        if status == 404:
            raise ElementNotFoundException(404, content)
        elif status == 503 and retry_count < 2:
            self._make_request(method, uri, headers, data, retry_count + 1)
        elif status >= 400 and status != 409:
            raise GloboMapException(status, content)

        return self._parse_response(content, status)

    def _log_http(self, operation, method, url, content=None, status=''):
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug(
                '%s: %s %s %s %s' % (operation, method, url, status, content)
            )
        else:
            self.log.info(
                '%s: %s %s %s' % (operation, method, url, status)
            )

    def _parse_response(self, response, status):
        if response and status in (200, 201):
            return json.loads(response)

    def _build_uri(self, type, collection, key=None):
        uri = '/%s/%s/' % (type, collection)
        uri += '%s/' % (key) if key else ''

        return uri


class GloboMapException(Exception):

    def __init__(self, status_code, response):
        self.status_code = status_code
        self.response = response


class ElementNotFoundException(GloboMapException):
    pass
