"""
   Copyright 2018 Globo.com

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
import os

DRIVER_FETCH_INTERVAL = int(os.getenv('DRIVER_FETCH_INTERVAL', 60))

GLOBOMAP_API_URL = os.getenv('GLOBOMAP_API_URL')
GLOBOMAP_API_USERNAME = os.getenv('GLOBOMAP_API_USERNAME')
GLOBOMAP_API_PASSWORD = os.getenv('GLOBOMAP_API_PASSWORD')

GLOBOMAP_RMQ_USER = os.getenv('GLOBOMAP_RMQ_USER')
GLOBOMAP_RMQ_PASSWORD = os.getenv('GLOBOMAP_RMQ_PASSWORD')
GLOBOMAP_RMQ_HOST = os.getenv('GLOBOMAP_RMQ_HOST')
GLOBOMAP_RMQ_PORT = int(os.getenv('GLOBOMAP_RMQ_PORT', 5672))
GLOBOMAP_RMQ_VIRTUAL_HOST = os.getenv('GLOBOMAP_RMQ_VIRTUAL_HOST')
GLOBOMAP_RMQ_QUEUE_NAME = os.getenv('GLOBOMAP_RMQ_QUEUE_NAME')
GLOBOMAP_RMQ_EXCHANGE = os.getenv('GLOBOMAP_RMQ_EXCHANGE')
GLOBOMAP_RMQ_ERROR_EXCHANGE = os.getenv('GLOBOMAP_RMQ_ERROR_EXCHANGE')
GLOBOMAP_RMQ_KEY = os.getenv('GLOBOMAP_RMQ_BINDING_KEY', 'globomap.updates')

DATABASE_POOL_SIZE = os.getenv('DATABASE_POOL_SIZE', 20)
DATABASE_POOL_OVERFLOW = os.getenv('DATABASE_POOL_OVERFLOW', 10)
DATABASE_POOL_RECYCLE = os.getenv('DATABASE_POOL_RECYCLE', 120)
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SCHEDULER_FREQUENCY_EXEC = os.getenv('SCHEDULER_FREQUENCY_EXEC')

LOADER_UPDATE = 'globomap_loader_update'

DRIVERS = [
    {'package': 'globomap_core_loader.driver.generic',
        'class': 'GenericDriver', 'factor': int(os.getenv('FACTOR', 1))},
    {'package': 'globomap_driver_napi.driver', 'class': 'Napi', 'factor': 1},
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'CTA'
        }, 'factor': 1
    },
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'DEV'
        }, 'factor': 1
    },
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'CME'
        }, 'factor': 1
    }
]

SPECS = {
    'updates': 'globomap_core_loader/api/specs/updates.json',
}

SENTRY_DSN = os.getenv('SENTRY_DSN')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': 'level=%(levelname)s timestamp=%(asctime)s module=%(module)s line=%(lineno)d' +
            'message=%(message)s '
        }
    },
    'handlers': {
        'default': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'sentry'],
            'level': 'WARNING',
            'propagate': True
        },
        'werkzeug': {'propagate': True},
    }
}
