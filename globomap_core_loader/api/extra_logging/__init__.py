import base64
import threading
import uuid
local = threading.local()

REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'
NO_REQUEST_ID = 'NoRequestId'  # Used if no request ID is available
NO_REQUEST_USER = 'NoRequestUser'  # Avoid if no User
NO_REQUEST_PATH = 'NoRequestPath'
NO_REQUEST_CONTEXT = 'NoRequestContext'


def get_identity():

    identity = uuid.uuid4().bytes
    encoded_id = base64.urlsafe_b64encode(identity)
    safe_id = encoded_id.replace('=', '')
    local.request_id = safe_id.upper()
