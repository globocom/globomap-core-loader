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
