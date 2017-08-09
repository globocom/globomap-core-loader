from flask import Blueprint

api = Blueprint('v1', __name__)

import driver_api  # noqa
