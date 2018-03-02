import logging

from globomap_core_loader.api.extra_logging import local
from globomap_core_loader.api.extra_logging import NO_REQUEST_ID
from globomap_core_loader.api.extra_logging import NO_REQUEST_PATH
from globomap_core_loader.api.extra_logging import NO_REQUEST_USER
# from globomap_core_loader.api.extra_logging import NO_REQUEST_CONTEXT


class StaticFieldFilter(logging.Filter):

    """
    Python logging filter that adds the given static contextual information
    in the ``fields`` dictionary to all logging records.
    """

    def filter(self, record):
        # for k, v in self.static_fields.items():
        #     setattr(record, k, v)
        # return True
        setattr(record, 'teste', 'teste')
        return True


class RequestFilter(logging.Filter):

    """
    Python logging filter that removes the (non-pickable) Django ``request``
    object from the logging record.
    """

    def filter(self, record):
        if hasattr(record, 'request'):
            del record.request
        return True


class ExtraLoggingFilter(logging.Filter):

    def filter(self, record):
        record.request_id = getattr(local, 'request_id', NO_REQUEST_ID)
        record.request_path = getattr(local, 'request_path', NO_REQUEST_PATH)
        record.request_user = getattr(local, 'request_user', NO_REQUEST_USER)
        return True
