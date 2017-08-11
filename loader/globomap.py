import json
import logging
import requests


class GloboMapClient(object):

    log = logging.getLogger(__name__)

    def __init__(self, host):
        self.host = host

    def update_element_state(self, action, type, collection, element, key):
        if action.upper() == 'CREATE':
            return self.create(type, collection, element)
        elif action.upper() == 'UPDATE':
            return self.update(type, collection, key, element)
        elif action.upper() == 'PATCH':
            return self.patch(type, collection, key, element)
        elif action.upper() == 'DELETE':
            return self.delete(type, collection, key)

    def create(self, type, collection, payload):
        return self._make_request(
            'POST', self._build_uri(type, collection), payload
        )

    def update(self, type, collection, key, payload):
        try:
            return self._make_request(
                'PUT', self._build_uri(type, collection, key), payload
            )
        except ElementNotFoundException:
            return self.create(type, collection, payload)

    def patch(self, type, collection, key, payload):
        try:
            return self._make_request(
                'PATCH', self._build_uri(type, collection, key), payload
            )
        except ElementNotFoundException:
            return self.create(type, collection, payload)

    def delete(self, type, collection, key):
        try:
            return self._make_request(
                'DELETE', self._build_uri(type, collection, key)
            )
        except ElementNotFoundException:
            self.log.debug("Element %s already deleted" % key)

    def list(self, type, collection, keys=None):
        keys = keys if keys else []
        return self._make_request(
            'GET', self._build_uri(type, collection, ';'.join(keys))
        )

    def get(self, collection, key):
        elements = self.list(collection, [key])
        if elements:
            return elements[0]

    def _make_request(self, method, uri, data=None):
        request_url = "%s%s" % (self.host, uri)
        self.log.debug("[GloboMap][request] %s - %s" % (method, request_url))
        response = requests.request(method, request_url, data=json.dumps(data))

        status = response.status_code
        content = response.content

        self.log.debug(
            "[GloboMap][response] %s - %s %s \n%s" %
            (method, request_url, status, content)
        )

        if status == 404:
            raise ElementNotFoundException()
        elif status >= 400:
            raise GloboMapException()
        return self._parse_response(content)

    def _parse_response(self, response):
        if response:
            return json.loads(response)

    def _build_uri(self, type, collection, key=None):
        return '/%s/%s/%s' % (type, collection, key or '')


class GloboMapException(Exception):
    pass


class ElementNotFoundException(GloboMapException):
    pass
