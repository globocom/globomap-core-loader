import json
import logging
import requests


class GloboMapClient(object):

    log = logging.getLogger(__name__)

    def __init__(self, host):
        self.host = host

    def update_element_state(self, action, element_type, element):
        if action.upper() == 'CREATE':
            return self.create(element_type, element)
        elif action.upper() == 'UPDATE':
            return self.update(element_type, element['id'], element)
        elif action.upper() == 'DELETE':
            return self.delete(element_type, element['id'])

    def create(self, element_type, payload):
        return self._make_request('POST', self._build_uri(element_type), payload)

    def update(self, element_type, id, payload):
        return self._make_request('PUT', self._build_uri(element_type, id), payload)

    def delete(self, element_type, id):
        return self._make_request('DELETE', self._build_uri(element_type, id))

    def list(self, element_type, ids=None):
        ids = ids if ids else []
        return self._make_request('GET', self._build_uri(element_type, ';'.join(ids)))

    def get(self, element_type, id):
        elements = self.list(element_type, [id])
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

    def _build_uri(self, element_type, id=None):
        return '/%s/%s' % (element_type, id or '')


class GloboMapException(Exception):
    pass
