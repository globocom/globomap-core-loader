import json
import logging
import requests


class GloboMapClient(object):

    log = logging.getLogger(__name__)

    def __init__(self, host):
        self.host = host

    def update_element_state(self, action, type, collection, element):
        if action.upper() == 'CREATE':
            return self.create(type, collection, element)
        elif action.upper() == 'UPDATE':
            return self.update(collection, type, element['content']['id'], element)
        elif action.upper() == 'DELETE':
            return self.delete(collection, type, element['content']['id'])

    def create(self, type, collection, payload):
        return self._make_request('POST', self._build_uri(type, collection), payload)

    def update(self, type, collection, id, payload):
        return self._make_request('PUT', self._build_uri(type, collection, id), payload)

    def delete(self, type, collection, id):
        return self._make_request('DELETE', self._build_uri(type, collection, id))

    def list(self, type, collection, ids=None):
        ids = ids if ids else []
        return self._make_request('GET', self._build_uri(type, collection, ';'.join(ids)))

    def get(self, collection, id):
        elements = self.list(collection, [id])
        if elements:
            return elements[0]

    def _make_request(self, method, uri, data=None):
        request_url = "%s%s" % (self.host, uri)
        self.log.debug("[GloboMap][request] %s - %s" % (method, request_url))
        response = requests.request(method, request_url, data=data)

        status = response.status_code
        content = response.content

        self.log.debug("[GloboMap][response] %s - %s %s \n%s" % (method, request_url, status, content))
        if status >= 400:
            raise GloboMapException(self._parse_response(content))
        return self._parse_response(content)

    def _parse_response(self, response):
        if response:
            return json.loads(response)

    def _build_uri(self, type, collection, id=None):
        return '/%s/%s/%s' % (type, collection, id or '')


class GloboMapException(Exception):
    pass
